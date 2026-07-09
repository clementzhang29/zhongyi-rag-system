import os
import pickle
import re

import jieba
import numpy as np
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from rank_bm25 import BM25Okapi

SYSTEM_PROMPT = """你是一位博学而亲切的中华文化导师，精通中医典籍、国学经典与儒释道学问。

请严格按下面结构输出，语言自然、清楚，不要使用代码块和表格：

**一句话精要**
一句话回答核心问题。

**经典溯源**
列出 2-4 条最相关原文。每条格式：
出处：《书名》· 章节名
原文：原文内容
释义：2-4 句白话解释

**深度阐释**
2-4 个要点，每个要点先写小标题，再写 2-4 句展开说明。

**生活践行**
给出一条可执行建议。

**延伸阅读**
推荐 1-2 本书和简短理由。

如果资料不足，就明确说现有资料中未找到直接相关原文，不要编造。"""

RAG_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "用户问题：{question}\n\n参考资料：\n{context}"),
])

ENGINE_TAG_PAT = re.compile(r'_(docling|mineru|surya|marker|paddleocr)$', re.I)
MIN_REFERENCE_DOCS = 5
CLASSIC_HINTS = (
    '黄帝内经', '素问', '灵枢', '难经', '伤寒', '金匮', '脉经', '脾胃论', '温病条辨',
    '本草纲目', '妇人大全良方', '傅青主', '临证指南医案', '医宗金鉴'
)
MODERN_HINTS = (
    '讲记', '讲读', '图解', '养生', '研究', '大成', '解读', '诠解', '浅说',
    'z-library', '扫描版', '中华大字经典'
)


class RAGEngine:
    def __init__(self, config: dict):
        self.config = config
        self.chunks = []
        self.bm25 = None
        self._db_path = config['vector_db']['path']
        os.makedirs(self._db_path, exist_ok=True)
        self.llm = ChatOpenAI(
            api_key=config['llm']['api_key'],
            base_url=config['llm']['base_url'],
            model=config['llm']['model'],
            temperature=config['llm']['temperature'],
        )
        self.answer_chain = RAG_PROMPT | self.llm | StrOutputParser()
        self._load()

    def _normalize_title(self, title: str, source: str = '') -> str:
        text = str(title or '').strip()
        if not text and source:
            text = os.path.splitext(os.path.basename(source))[0]
        text = ENGINE_TAG_PAT.sub('', text)
        text = text.replace('__', ' ').replace('_', ' ').strip(' -')
        return text or '未知'

    def _source_key(self, title: str, source: str = '') -> str:
        text = self._normalize_title(title, source)
        text = re.sub(r'\s+', '', text)
        text = re.sub(r'[\[\]【】《》“”"\'（）()·._-]', '', text)
        text = re.sub(r'(清|明|宋|元|唐|晋|汉|战国|佚名|张仲景|王叔和|李杲|吴鞠通|叶桂|吴谦|扁鹊|傅山|李时珍|张志聪|王冰|杨上善|徐灵胎|尤怡|陈修园|高学山|陈自明|赵学敏)', '', text)
        text = re.sub(r'(第[一二三四五六七八九十\d]+册|上册|下册|全本|副本)$', '', text)
        return text[:40] or self._normalize_title(title, source)

    def _source_tier(self, title: str, source: str = '') -> str:
        text = f'{title} {source}'
        if any(hint in text for hint in MODERN_HINTS):
            return 'modern'
        if any(hint in text for hint in CLASSIC_HINTS):
            return 'classic'
        return 'commentary'

    def _tier_boost(self, title: str, source: str = '') -> float:
        tier = self._source_tier(title, source)
        if tier == 'classic':
            return 0.18
        if tier == 'commentary':
            return 0.08
        return 0.0

    def _chunk(self, text: str, max_len: int = 800) -> list[str]:
        paras = text.split('\n\n')
        chunks, buf = [], ''
        for para in paras:
            para = para.strip()
            if not para:
                continue
            if len(buf) + len(para) < max_len:
                buf += para + '\n\n'
            else:
                if buf:
                    chunks.append(buf.strip())
                buf = para + '\n\n'
        if buf:
            chunks.append(buf.strip())
        return chunks

    def _extract_chapter(self, content: str) -> str:
        lines = content.strip().split('\n')
        for line in lines[:8]:
            line = line.strip()
            if not line:
                continue
            match = re.search(r'(第[一二三四五六七八九十百千\d]+[品章节篇卷])', line)
            if match:
                start = max(0, match.start() - 8)
                end = min(len(line), match.end() + 12)
                return line[start:end].strip()
        for line in lines[:3]:
            line = line.strip()
            if 2 < len(line) < 50 and not line.startswith('【'):
                return line
        return ''

    def index_documents(self, docs: list[dict]):
        self.chunks = []
        seen = set()
        for doc in docs:
            src_name = doc.get('source', '')
            title = self._normalize_title(doc.get('title', ''), src_name)
            content = doc.get('content', '')
            chapter = self._extract_chapter(content)
            for chunk in self._chunk(content):
                key = (title, chunk[:180])
                if key in seen:
                    continue
                seen.add(key)
                self.chunks.append({
                    'content': chunk,
                    'source': src_name,
                    'title': title,
                    'chapter': self._extract_chapter(chunk) or chapter,
                    'source_key': self._source_key(title, src_name),
                    'source_tier': self._source_tier(title, src_name),
                })
        tokenized = [list(jieba.cut(item['content'])) for item in self.chunks]
        self.bm25 = BM25Okapi(tokenized)
        self._save()
        print('Indexed', len(self.chunks), 'chunks')

    def retrieve(self, query: str, top_k: int = None) -> list[dict]:
        if top_k is None:
            top_k = self.config['retrieval']['top_k']
        top_k = max(top_k, MIN_REFERENCE_DOCS)
        if not self.bm25 or not self.chunks:
            return []
        scores = self.bm25.get_scores(list(jieba.cut(query)))
        max_score = float(np.max(scores)) if len(scores) else 0.0
        candidate_count = min(len(self.chunks), max(top_k * 40, 200))
        top_ids = np.argsort(scores)[-candidate_count:][::-1]
        ranked = []
        for idx in top_ids:
            chunk = self.chunks[idx]
            normalized = float(scores[idx]) / max_score if max_score > 0 else 0.0
            final_score = normalized + self._tier_boost(chunk.get('title', ''), chunk.get('source', ''))
            ranked.append((final_score, normalized, idx, chunk))
        ranked.sort(key=lambda item: item[0], reverse=True)
        seen_docs = set()
        seen_content = set()
        results = []
        for final_score, raw_score, idx, chunk in ranked:
            doc_key = chunk.get('source_key') or self._source_key(chunk.get('title', ''), chunk.get('source', ''))
            content_key = chunk['content'][:100]
            if doc_key in seen_docs or content_key in seen_content:
                continue
            seen_docs.add(doc_key)
            seen_content.add(content_key)
            item = dict(chunk)
            item['score'] = round(final_score, 4)
            item['raw_score'] = round(raw_score, 4)
            results.append(item)
            if len(results) >= top_k:
                break
        return results

    def _fallback_answer(self, retrieved: list[dict]) -> str:
        if not retrieved:
            return '一句话精要\n现有资料里暂时没有检索到足够相关的内容。\n\n经典溯源\n现有资料中未找到直接相关的经典原文。'
        lines = [
            '一句话精要',
            '已根据本地典籍检索到相关内容，下面给出出处与原文摘要。',
            '',
            '经典溯源',
        ]
        for ref in retrieved[:MIN_REFERENCE_DOCS]:
            title = self._normalize_title(ref.get('title', ''), ref.get('source', ''))
            chapter = ref.get('chapter', '')
            cite = f'出处：《{title}》'
            if chapter:
                cite += f'·{chapter}'
            excerpt = re.sub(r'\s+', ' ', ref.get('content', '')).strip()[:220]
            lines.extend([
                cite,
                f'原文：{excerpt}',
                '释义：这是当前本地检索到的直接材料，可先据此判断方向，再继续追问更细的问题。',
                '',
            ])
        lines.extend([
            '深度阐释',
            '1. 当前回答使用的是本地检索回退模式，重点保证出处可追溯、文本不乱码。',
            '2. 如果外部模型恢复可用，系统会自动生成更自然的综合解读。',
            '',
            '生活践行',
            '先根据上面的出处回看原文，再围绕具体病机、方药或养生问题继续细问。',
        ])
        return '\n'.join(lines).strip()

    def ask(self, question: str) -> tuple[str, list[dict]]:
        retrieved = self.retrieve(question)
        context_parts = []
        for i, ref in enumerate(retrieved):
            title = self._normalize_title(ref.get('title', ''), ref.get('source', ''))
            chapter = ref.get('chapter', '')
            cite = f'《{title}》'
            if chapter:
                cite += f' · {chapter}'
            context_parts.append(f'[文献{i + 1}] {cite}\n{ref["content"]}')
        context = '\n\n---\n\n'.join(context_parts)
        try:
            answer = self.answer_chain.invoke({'context': context, 'question': question})
        except Exception:
            answer = self._fallback_answer(retrieved)
        return answer, retrieved

    def _save(self):
        with open(os.path.join(self._db_path, 'chunks.pkl'), 'wb') as f:
            pickle.dump(self.chunks, f)
        with open(os.path.join(self._db_path, 'bm25.pkl'), 'wb') as f:
            pickle.dump(self.bm25, f)

    def _load(self):
        chk = os.path.join(self._db_path, 'chunks.pkl')
        bm = os.path.join(self._db_path, 'bm25.pkl')
        if os.path.exists(chk) and os.path.exists(bm):
            with open(chk, 'rb') as f:
                self.chunks = pickle.load(f)
            with open(bm, 'rb') as f:
                self.bm25 = pickle.load(f)
            print('Loaded', len(self.chunks), 'chunks from cache.')
