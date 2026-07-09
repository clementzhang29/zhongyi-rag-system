import os, sys, yaml, json, pickle, glob
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

BASE = str(Path(__file__).resolve().parents[1])
sys.path.insert(0, BASE)

# Load config
with open(os.path.join(BASE, 'config.yaml'), 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

from src.parser.document_parser import DocumentParser
from src.rag.rag_engine import RAGEngine

print("Parsing all documents...")
parser = DocumentParser()
all_docs = parser.parse_directory(os.path.join(BASE, 'data', 'books'))
print(f"Parsed: {len(all_docs)} document chunks")

print("Rebuilding engine index...")
engine = RAGEngine(config)
engine.index_documents(all_docs)

print("Testing query...")
answer, refs = engine.ask("什么是阴阳平衡？")
print(f"Answer: {answer[:100]}...")
print(f"References: {len(refs)}")

print("\nDone! Ready for questions.")
