import os
import re
from bs4 import BeautifulSoup
from ebooklib import epub, ITEM_DOCUMENT
import fitz

ENGINE_TAG_PAT = re.compile(r'_(docling|mineru|surya|marker|paddleocr)$', re.I)
SYMBOL_ONLY_PAT = re.compile(r"^[\s\-\+\*_=|/\\.·:：'‘’\[\](){}<>?？!！,，;；`~@#$%^&]+$")
WATERMARK_PAT = re.compile(r"A-PDF MERGER DEMO|a-pdf\.com", re.I)
ALLOWED_EXTS = {'.epub', '.pdf', '.txt', '.md'}
ENGINE_PRIORITY = {'docling': 5, 'surya': 4, 'mineru': 3, 'marker': 2, 'paddleocr': 1}


class DocumentParser:
    def _canonical_stem(self, fname: str) -> str:
        stem = os.path.splitext(fname)[0]
        stem = ENGINE_TAG_PAT.sub('', stem)
        stem = re.sub(r'\.pdf$', '', stem, flags=re.I)
        stem = re.sub(r'([ _-])1$', '', stem)
        stem = stem.replace('__', ' ').replace('_', ' ').strip()
        return stem.lower()

    def _file_priority(self, fname: str) -> tuple[int, int]:
        lower = fname.lower()
        engine_match = re.search(r'_(docling|mineru|surya|marker|paddleocr)\.(md|txt)$', lower)
        engine_score = ENGINE_PRIORITY.get(engine_match.group(1), 0) if engine_match else 0
        ext = os.path.splitext(lower)[1]
        ext_score = {'.md': 2, '.txt': 1, '.pdf': 0, '.epub': 0}.get(ext, 0)
        penalty = -10 if re.search(r'_1_(docling|mineru|surya|marker|paddleocr)\.(md|txt)$', lower) else 0
        if penalty == 0:
            penalty = -1 if re.search(r'([ _-])1(\.[^.]+)+$', lower) else 0
        return (engine_score, ext_score + penalty)

    def parse(self, filepath: str) -> list[dict]:
        ext = os.path.splitext(filepath)[1].lower()
        if ext == '.epub':
            return self._parse_epub(filepath)
        if ext == '.pdf':
            return self._parse_pdf(filepath)
        if ext in ('.txt', '.md'):
            return self._parse_txt(filepath)
        raise ValueError(f'Unsupported format: {ext}')

    def _normalize_title(self, path: str, text: str) -> str:
        fname = os.path.basename(path)
        stem = os.path.splitext(fname)[0]
        stem = ENGINE_TAG_PAT.sub('', stem)
        stem = stem.replace('__', ' ').replace('_', ' ').strip()
        first_line = text.split('\n', 1)[0].strip() if text else ''
        if first_line.startswith('# '):
            return first_line[2:].strip()
        if first_line.startswith('## '):
            return first_line[3:].strip()
        return stem or fname

    def _clean_text(self, text: str) -> str:
        text = text.replace('\ufeff', '')
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        lines = []
        for raw in text.split('\n'):
            line = raw.strip()
            if not line:
                lines.append('')
                continue
            if '<!-- image -->' in line:
                continue
            if WATERMARK_PAT.search(line):
                continue
            if line.startswith('# # '):
                lines.append('## ' + line[4:].strip())
                continue
            if SYMBOL_ONLY_PAT.fullmatch(line):
                continue
            lines.append(raw.rstrip())
        text = '\n'.join(lines)
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r'[ \t]+\n', '\n', text)
        return text.strip()

    def _parse_epub(self, path: str) -> list[dict]:
        book = epub.read_epub(path)
        title = str(book.get_metadata('DC', 'title'))
        chapters = []
        for doc in book.get_items_of_type(ITEM_DOCUMENT):
            content = doc.get_content().decode('utf-8', errors='ignore')
            soup = BeautifulSoup(content, 'html.parser')
            text = self._clean_text(soup.get_text())
            if len(text) > 50:
                chapters.append({'title': title, 'content': text, 'source': os.path.basename(path)})
        return chapters

    def _parse_pdf(self, path: str) -> list[dict]:
        doc = fitz.open(path)
        pages = []
        title = doc.metadata.get('title', '') or os.path.basename(path)
        for page in doc:
            text = self._clean_text(page.get_text().strip())
            if text:
                pages.append({'title': title, 'content': text, 'source': os.path.basename(path), 'page': page.number})
        doc.close()
        return pages

    def _parse_txt(self, path: str) -> list[dict]:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            text = self._clean_text(f.read())
        title = self._normalize_title(path, text)
        return [{'title': title, 'content': text, 'source': os.path.basename(path)}]

    def parse_directory(self, dirpath: str) -> list[dict]:
        all_docs = []
        seen = set()
        selected = {}
        for root, dirs, files in os.walk(dirpath):
            for fname in files:
                ext = os.path.splitext(fname)[1].lower()
                if ext not in ALLOWED_EXTS:
                    continue
                lower_name = fname.lower()
                if '_1_docling.' in lower_name or '_1_paddleocr.' in lower_name or '_1_mineru.' in lower_name or '_1_surya.' in lower_name or '_1_marker.' in lower_name:
                    continue
                fp = os.path.join(root, fname)
                key = os.path.join(root, self._canonical_stem(fname))
                prev = selected.get(key)
                cur_priority = self._file_priority(fname)
                if prev and cur_priority <= prev[0]:
                    continue
                selected[key] = (cur_priority, fp)
        for _, fp in selected.values():
                try:
                    docs = self.parse(fp)
                    for doc in docs:
                        key = (doc.get('title', ''), doc.get('content', '')[:160])
                        if key in seen:
                            continue
                        seen.add(key)
                        all_docs.append(doc)
                except Exception:
                    pass
        return all_docs
