import sys, os, time
os.chdir(r"C:\Users\Administrator\Documents\Codex\2026-07-02\harness-c-users-administrator-codex-skills\中医RAG系统")
sys.path.insert(0, ".")

t0 = time.time()
from src.rag.rag_engine import RAGEngine
print("rag_engine:", round(time.time()-t0, 1), "s")

t0 = time.time()
from src.rag.query_enhancer import QueryEnhancer
print("query_enhancer:", round(time.time()-t0, 1), "s")

t0 = time.time()
import yaml
with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)
engine = RAGEngine(config)
print("engine init:", round(time.time()-t0, 1), "s")

t0 = time.time()
enhancer = QueryEnhancer(config)
print("enhancer init:", round(time.time()-t0, 1), "s")
