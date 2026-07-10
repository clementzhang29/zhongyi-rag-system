# 中医国学 RAG 系统

基于检索增强生成(RAG)的中医国学知识问答系统。

## 在线文件整理器

GitHub 协作筛选版文件整理器：

https://clementzhang29.github.io/zhongyi-rag-system/file-cleaner/

说明：GitHub Pages 只能运行静态网页，适合“导入目录快照 JSON → 筛选文件目录 → 导出 MD 清单”。如果需要扫描本机目录、预览本地文件、生成 BAT 或移动文件，请运行本地 Python 版：

```bash
python tools/file_cleaner_app.py
```

## 快速开始

### 1. 配置 API

编辑 `config.yaml`，填入你的大模型 API：

```yaml
llm:
  api_key: "sk-your-key-here"
  base_url: "https://api.openai.com/v1"   # 或其他兼容接口
  model: "gpt-4o-mini"
```

支持的API（兼容OpenAI格式）：
- OpenAI / Azure OpenAI
- DeepSeek / 硅基流动(SiliconFlow) / 智谱
- 通义千问 / 百度文心
- 任何 OpenAI-compatible 接口

### 2. 放入书籍

将 EPUB/PDF/TXT 文件放入 `data/books/` 目录

### 3. 启动

```bash
python run.py
```

### 4. 使用 API

```bash
# 索引文档
curl -X POST http://localhost:8000/rag/index

# 问答
curl -X POST http://localhost:8000/rag/query \
  -H "Content-Type: application/json" \
  -d '{"question": "什么是定慧一体？"}'

# 健康检查
curl http://localhost:8000/rag/health
```

## 项目结构

```
中医RAG系统/
├── config.yaml          # 配置文件(API key等)
├── run.py               # 启动入口
├── start.bat            # Windows启动脚本
├── data/
│   ├── books/           # 放入书籍文件
│   └── vector_db/       # 向量索引缓存
└── src/
    ├── parser/
    │   └── document_parser.py  # 文档解析(EPUB/PDF/TXT)
    ├── rag/
    │   ├── rag_engine.py       # RAG核心(向量+BM25+问答)
    │   └── query_enhancer.py   # 意图识别+问题补全
    └── api/
        └── server.py           # FastAPI REST接口
```

## 功能特性

- 多格式支持: EPUB / PDF / TXT
- 混合检索: FAISS向量 + BM25关键词
- 意图识别: 自动分类问题类型并补全查询
- 原文引用: 回答中引用原文并附带白话解释
- 配置化: 只需修改config.yaml即可使用
- 可扩展: REST API接口，支持Web/小程序调用

## 架构设计

```
用户请求 → FastAPI → 意图识别(补全问题)
                    → 混合检索(FAISS+BM25)
                    → LLM生成(原文+白话解释)
                    → 返回JSON响应
```
