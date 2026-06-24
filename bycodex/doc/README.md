# Enterprise RAG Notes by Codex

这些笔记来自 `langchainStudy` 顶层 Python 文件里的知识点，但写法按照企业级 RAG 系统来组织。

目标不是堆知识，而是快速 loading：每个文件只讲一个主题，每个主题都给出中文和英文说明。

## Reading Order

1. `01-system-overview.md`：企业级 RAG 总览
2. `02-model-and-message-layer.md`：模型、消息、Prompt 层
3. `03-lcel-orchestration.md`：LCEL、Runnable、分支和并行
4. `04-structured-output.md`：结构化输出和 JSON 合同
5. `05-rag-ingestion.md`：文档加载、清洗、切分、入库
6. `06-vector-db-isolation.md`：collection、namespace、table、index 隔离
7. `07-retrieval-and-generation.md`：检索、rerank、生成答案
8. `08-agent-and-tools.md`：Agent、工具调用和安全边界
9. `09-production-checklist.md`：企业上线 checklist

## Source Mapping

- `04.basic.py`, `05.system_message*.py`, `06.aws_bedrock*.py` -> model/message/provider layer
- `08.promptTemplate*.py`, `expression_language.py` -> prompt and LCEL basics
- `10.lambda*.py`, `12.parallel.py`, `13.choice.py` -> Runnable, branch, parallel orchestration
- `30.output*.py` -> structured output
- `15.rag1.py` to `15.rag6.py` -> RAG ingestion, vector store, retrieval, grounded answer, chat history
- `21.agent.py` -> tool calling and agent workflow

## API Notes

- OpenAI chat examples use `ChatOpenAI` from `langchain_openai`.
- For newest OpenAI models, prefer current model IDs from official OpenAI docs at implementation time. The examples here use `gpt-5.5` for high quality and `gpt-5-nano` for cheaper/fast paths where appropriate.
- OpenAI embeddings use `text-embedding-3-small` or `text-embedding-3-large`.
- Chroma examples use `collection_name` explicitly, because enterprise systems should not rely on an implicit default collection.
