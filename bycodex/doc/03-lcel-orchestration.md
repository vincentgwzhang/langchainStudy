# 03. LCEL Orchestration

## Runnable

中文：`RunnableLambda` 把普通 Python 函数包装成 LangChain 流程节点。企业里它适合做轻量转换，例如格式化输入、抽取字段、合并检索结果，但不适合塞复杂业务逻辑。

English: `RunnableLambda` wraps a normal Python function as a LangChain pipeline node. In enterprise systems, it is useful for lightweight transformations such as formatting input, extracting fields, or merging retrieval results, but it should not hide complex business logic.

```python
from langchain_core.runnables import RunnableLambda

normalize_query = RunnableLambda(lambda x: {"query": x["query"].strip()})
```

## Chain

中文：`prompt | model | parser` 是 LangChain Expression Language 的核心思想。企业代码里要让每个节点职责单一，方便测试和替换。

English: `prompt | model | parser` is the core idea of LangChain Expression Language. In enterprise code, each node should have one responsibility so it can be tested and replaced.

```python
chain = prompt_template | llm | output_parser
```

## Parallel

中文：`RunnableParallel` 适合并行执行互不依赖的任务，例如同时生成正反观点、同时跑多个 retriever、同时做关键词检索和向量检索。

English: `RunnableParallel` is suitable for independent tasks, such as generating pros and cons, running multiple retrievers, or combining keyword search with vector search.

Enterprise RAG example:

```text
query
  -> parallel:
       vector_retriever
       keyword_retriever
       metadata_filter
  -> merge
  -> rerank
```

## Branch

中文：`RunnableBranch` 用于根据中间结果选择不同路径。企业里常见于 query routing：FAQ、policy、code、billing 等问题走不同知识库。

English: `RunnableBranch` selects different paths based on intermediate results. In enterprise RAG, it is often used for query routing: FAQ, policy, code, and billing questions may go to different knowledge bases.

Example routing idea:

```text
if query_type == "billing" -> billing_collection
if query_type == "code" -> code_collection
else -> general_collection
```

## Enterprise Standard

中文：编排层应该可观测、可测试、可替换。不要把 prompt、retriever、model、parser、业务判断全部写成一坨。

English: The orchestration layer should be observable, testable, and replaceable. Do not mix prompt, retriever, model, parser, and business decisions into one block.
