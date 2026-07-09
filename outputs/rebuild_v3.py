import sys, os, glob
os.chdir(r"C:\Users\Administrator\Documents\Codex\2026-07-02\harness-c-users-administrator-codex-skills\中医RAG系统")
sys.path.insert(0, ".")

# Clear cache
for f in glob.glob("data/vector_db/*"):
    os.remove(f)
print("Cache cleared")

# Import updated modules
import importlib
import src.rag.rag_engine as re_mod
importlib.reload(re_mod)

from src.parser.document_parser import DocumentParser
from src.rag.rag_engine import RAGEngine
import yaml

with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

parser = DocumentParser()
all_docs = []
for root, dirs, files in os.walk("./data/books"):
    for f in files:
        fp = os.path.join(root, f)
        ext = os.path.splitext(f)[1].lower()
        if ext in ('.epub', '.txt'):
            try:
                docs = parser.parse(fp)
                all_docs.extend(docs)
            except: pass

print("Parsed", len(all_docs), "sections")

engine = RAGEngine(config)
engine.index_documents(all_docs)
print("Indexed", len(engine.chunks), "chunks")

# Quick test
print("\n=== Test ===")
answer, refs = engine.ask("什么是知行合一？")
print("Answer:", answer[:600])
print()
print("Refs:")
for r in refs[:3]:
    print("  Title:", r['title'][:60])
    print("  Chapter:", r.get('chapter','')[:40])
    print("  Content:", r['content'][:80])
    print()
