# 01. Enterprise RAG System Overview

## Core Idea

中文：RAG 不是简单地“把文档塞进向量数据库，然后问模型”。企业级 RAG 是一个完整系统：数据摄入、清洗、切分、embedding、索引隔离、检索、重排、上下文组装、LLM 生成、审计、评估和回滚。

English: RAG is not just “put documents into a vector database and ask the model.” Enterprise RAG is a full system: ingestion, cleaning, chunking, embedding, index isolation, retrieval, reranking, context assembly, LLM generation, auditing, evaluation, and rollback.

## Production Pipeline

```text
source systems
  -> ingestion jobs
  -> document cleaning
  -> chunking
  -> metadata enrichment
  -> embedding generation
  -> vector DB collection / namespace / table
  -> retriever
  -> reranker or filters
  -> prompt assembly
  -> LLM answer
  -> logging, eval, monitoring
```

## What Your POC Code Covers

中文：你原来的代码已经覆盖了 RAG 的学习主线：加载文档、切分、embedding、Chroma 存储、检索、把上下文交给 LLM、带 chat history 的问答。

English: Your original code already covers the learning path of RAG: load documents, split text, create embeddings, store in Chroma, retrieve documents, pass context to the LLM, and run chat-history-aware QA.

## What Enterprise Adds

中文：企业级版本会额外强调隔离、版本、权限、评估、观测、失败恢复和成本控制。

English: The enterprise version adds isolation, versioning, permissions, evaluation, observability, failure recovery, and cost control.

Key additions:

- explicit collection / namespace / table naming
- embedding model version tracking
- idempotent ingestion jobs
- metadata schema
- tenant isolation
- A/B testing with parallel indexes
- rollback strategy
- retrieval quality evaluation
- prompt and answer audit logs
- observability through tracing and metrics

## Golden Rule

中文：同一个向量搜索空间里，只放同一个 embedding model、同一个维度、同一个语义规则生成的向量。

English: In one vector search space, only store vectors produced by the same embedding model, same dimension, and same semantic rules.
