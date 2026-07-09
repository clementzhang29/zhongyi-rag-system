import os, sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

BASE = r"C:\Users\Administrator\Documents\Codex\2026-07-02\harness-c-users-administrator-codex-skills\中医RAG系统"
sys.path.insert(0, BASE)

import yaml

# Load config
with open(os.path.join(BASE, 'config.yaml'), 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

from src.parser.document_parser import DocumentParser
from src.rag.rag_engine import RAGEngine

doc_dir = os.path.join(BASE, 'data', 'books')
print("Parsing documents from:", doc_dir)
parser = DocumentParser()
all_docs = parser.parse_directory(doc_dir)
print(f"Parsed {len(all_docs)} chunks")

print("Rebuilding index...")
engine = RAGEngine(config)
engine.index_documents(all_docs)

# Save
print(f"Indexed {len(engine.chunks)} chunks. Cache saved to {config['vector_db']['path']}")

# Quick test
print("\nTesting query...")
try:
    ans, refs = engine.ask("什么是阴阳平衡？")
    print(f"Answer: {ans[:80]}...")
    print(f"Refs: {len(refs)}")
except Exception as e:
    print(f"Test query error: {e}")

print("\nRebuild complete! Now starting server...")
