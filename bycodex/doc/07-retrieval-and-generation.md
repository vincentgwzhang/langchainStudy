# 07. Retrieval And Generation

## Retrieval

中文：你的代码演示了 `similarity_search` 和 `as_retriever`。企业里 retrieval 通常不是单一步骤，而是多阶段 pipeline。

English: Your code demonstrates `similarity_search` and `as_retriever`. In enterprise systems, retrieval is usually a multi-stage pipeline, not a single step.

## Retrieval Pipeline

```text
query normalization
  -> query embedding
  -> metadata filter
  -> vector search
  -> keyword search optional
  -> merge candidates
  -> rerank
  -> context compression
  -> prompt assembly
```

## Search Types

中文：`similarity` 适合基础语义检索；`mmr` 适合减少重复结果；`similarity_score_threshold` 适合避免强行返回不相关文档。

English: `similarity` is good for basic semantic retrieval; `mmr` reduces duplicate results; `similarity_score_threshold` avoids forcing irrelevant documents into the answer.

## Enterprise Retriever Example

```python
retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 6,
        "fetch_k": 40,
        "filter": {
            "tenant_id": "tenant_001",
            "source_type": "policy",
            "embedding_model": "text-embedding-3-large",
        },
    },
)
```

## Generation

中文：生成答案时，LLM 只能使用检索到的上下文。系统提示词要明确：不知道就说不知道，不要编造引用。

English: During generation, the LLM should only use retrieved context. The system prompt should clearly say: if unknown, say unknown; do not fabricate citations.

Example:

```text
You are a grounded enterprise assistant.
Answer only from the provided context.
If the context does not contain the answer, say "I don't know".
Return citation IDs for every factual claim.
```

## Answer Contract

中文：企业答案最好包含：最终答案、引用、置信度、是否需要人工审核。

English: Enterprise answers should include: final answer, citations, confidence, and whether human review is required.
