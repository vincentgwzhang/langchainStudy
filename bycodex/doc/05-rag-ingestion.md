# 05. RAG Ingestion

## What Your Code Does

中文：你的 `15.rag1.py` 和 `15.rag3.py` 做了典型 ingestion：加载文本、切分 chunk、生成 embedding、写入 Chroma。

English: Your `15.rag1.py` and `15.rag3.py` implement typical ingestion: load text, split into chunks, generate embeddings, and write to Chroma.

## Enterprise Ingestion Pipeline

```text
loader
  -> cleaner
  -> splitter
  -> metadata enricher
  -> document ID generator
  -> embedding job
  -> vector writer
  -> ingestion audit log
```

## Document IDs

中文：企业里不要随机生成不可追踪 ID。推荐用稳定 ID，例如 `source_id + version + chunk_index + content_hash`。

English: In enterprise systems, do not use untraceable random IDs only. Prefer stable IDs such as `source_id + version + chunk_index + content_hash`.

Example:

```text
doc_id = sha256(source_uri + source_version + chunk_index + chunk_hash)
```

## Metadata

中文：metadata 是生产 RAG 的生命线。它决定权限过滤、版本过滤、引用展示、回滚和调试能力。

English: Metadata is the backbone of production RAG. It enables permission filtering, version filtering, citation display, rollback, and debugging.

Recommended metadata:

```python
metadata = {
    "tenant_id": "tenant_001",
    "source_uri": "s3://kb/policy/refund.md",
    "source_type": "policy",
    "source_version": "2026-06-22",
    "chunk_index": 17,
    "embedding_model": "text-embedding-3-large",
    "embedding_dim": 3072,
    "language": "zh",
    "acl": ["support", "admin"],
}
```

## Chunking

中文：POC 可以只用 `RecursiveCharacterTextSplitter`。企业里要根据文档类型选择策略：技术文档按标题，合同按条款，代码按函数，表格按行或块。

English: A POC can use `RecursiveCharacterTextSplitter`. Enterprise systems choose chunking strategies by document type: technical docs by headings, contracts by clauses, code by functions, tables by rows or blocks.

## Idempotency

中文：同一份文档重复 ingestion 不应该产生重复 chunk。企业 ingestion job 必须支持幂等、重试和部分失败恢复。

English: Re-ingesting the same document should not create duplicate chunks. Enterprise ingestion jobs must support idempotency, retries, and partial failure recovery.
