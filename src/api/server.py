import os
import threading
import yaml

_CONFIG_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
config_path = os.path.join(_CONFIG_DIR, 'config.yaml')
with open(config_path, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from src.parser.document_parser import DocumentParser
from src.rag.rag_engine import RAGEngine


class QueryRequest(BaseModel):
    question: str


class RefItem(BaseModel):
    book: str = ''
    chapter: str = ''
    excerpt: str = ''
    source_type: str = ''
    score: float = 0.0


class QueryResponse(BaseModel):
    answer: str
    references: list[RefItem] = []
    total_docs: int = 0


app = FastAPI(title='中医国学RAG系统', version='4.2')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])

engine = None
status = 'starting'


def build_index(force: bool = False):
    global engine, status
    try:
        status = 'init engine'
        engine = RAGEngine(config)
        if force or not engine.chunks or len(engine.chunks) < 100:
            status = 'parsing'
            doc_dir = config['documents']['path']
            parser = DocumentParser()
            all_docs = []
            status = 'parsing classic texts'
            classic_docs = []
            if os.path.exists(doc_dir):
                for fname in os.listdir(doc_dir):
                    fp = os.path.join(doc_dir, fname)
                    if not os.path.isfile(fp):
                        continue
                    ext = os.path.splitext(fname)[1].lower()
                    if ext not in {'.txt', '.md', '.epub'}:
                        continue
                    try:
                        classic_docs.extend(parser.parse(fp))
                    except Exception as exc:
                        print(f'skip classic text {fname}: {exc}')
            all_docs.extend(classic_docs)
            print(f'classic_texts: {len(classic_docs)} docs')
            for subdir in ['pdf_ocr']:
                subdir_path = os.path.join(doc_dir, subdir)
                if os.path.exists(subdir_path):
                    status = f'parsing {subdir}'
                    docs = parser.parse_directory(subdir_path)
                    all_docs.extend(docs)
                    print(f'{subdir}: {len(docs)} chunks')
            if all_docs:
                status = f'indexing {len(all_docs)} chunks'
                engine.index_documents(all_docs)
            status = f'ready - {len(engine.chunks)} chunks'
        else:
            status = f'ready from cache - {len(engine.chunks)} chunks'
    except Exception as exc:
        status = f'error: {exc}'
        print(f'Index build error: {exc}')


def build_index_async(force: bool = False):
    thread = threading.Thread(target=build_index, args=(force,), daemon=True)
    thread.start()


build_index_async()


@app.get('/rag/health')
def health():
    chunk_count = len(engine.chunks) if engine and engine.chunks else 0
    return {'status': 'building' if 'ready' not in status else 'ok', 'chunks': chunk_count, 'msg': status, 'version': '4.2'}


@app.post('/rag/rebuild')
def rebuild():
    global status
    status = 'rebuilding'
    build_index_async(True)
    return {'ok': True, 'msg': 'rebuild started'}


@app.get('/')
def index():
    html_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'outputs', 'chatbox.html')
    if os.path.exists(html_path):
        return FileResponse(html_path)
    return {'message': '中医国学RAG系统'}


@app.post('/rag/query', response_model=QueryResponse)
def query(req: QueryRequest):
    if not engine or not engine.chunks:
        raise HTTPException(503, f'Index not ready: {status}')
    answer, refs = engine.ask(req.question)
    ref_items = []
    seen = set()
    for ref in refs[:10]:
        title = str(ref.get('title', '未知')).strip() or '未知'
        if title in seen:
            continue
        seen.add(title)
        ref_items.append(RefItem(
            book=title,
            chapter=ref.get('chapter', ''),
            excerpt=ref.get('content', '')[:500],
            source_type=ref.get('source_tier', ''),
            score=float(ref.get('score', 0.0) or 0.0),
        ))
    return QueryResponse(answer=answer, references=ref_items, total_docs=len(engine.chunks))
