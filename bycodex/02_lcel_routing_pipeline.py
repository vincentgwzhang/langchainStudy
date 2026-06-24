"""
Enterprise LCEL routing pipeline.
企业级 LCEL 路由编排。

Based on / 对应你的原始文件:
- 10.lambda1.py
- 10.lambda2.py
- 12.parallel.py
- 13.choice.py
- expression_language.py

Advanced compared with your POC / 更先进的地方:
1. 中文：Runnable 不只是做大小写转换，而是承担 query normalization、routing、并行检索等生产任务。
   English: Runnable is not only for uppercase conversion; it handles query normalization, routing, and parallel retrieval in production.
2. 中文：使用 branch 做知识库路由，例如 policy、code、support。
   English: Uses branching for knowledge-base routing, such as policy, code, and support.
3. 中文：使用 parallel 同时跑多个候选路径，后面再 merge/rerank。
   English: Uses parallel branches for multiple candidate paths, followed by merge/rerank.
"""

from __future__ import annotations

from typing import Literal, TypedDict

from langchain_core.runnables import RunnableBranch, RunnableLambda, RunnableParallel


class QueryInput(TypedDict):
    tenant_id: str
    question: str


class RoutedQuery(TypedDict):
    tenant_id: str
    question: str
    route: Literal["policy", "code", "support", "general"]


def normalize_query(payload: QueryInput) -> QueryInput:
    """
    中文：企业入口要做输入清洗，但不能改变用户原意。
    English: Enterprise entrypoints should clean input without changing user intent.
    """

    return {
        "tenant_id": payload["tenant_id"].strip(),
        "question": " ".join(payload["question"].split()),
    }


def classify_route(payload: QueryInput) -> RoutedQuery:
    """
    中文：这里用规则演示；真实企业里可换成小模型分类器或配置化路由表。
    English: This is rule-based for demonstration; production can use a small classifier model or a configurable routing table.
    """

    q = payload["question"].lower()
    if "refund" in q or "policy" in q or "报销" in q:
        route = "policy"
    elif "code" in q or "api" in q or "python" in q:
        route = "code"
    elif "ticket" in q or "support" in q or "客服" in q:
        route = "support"
    else:
        route = "general"
    return {**payload, "route": route}


def build_route_chain():
    normalize = RunnableLambda(normalize_query)
    route = RunnableLambda(classify_route)
    return normalize | route


def build_parallel_retrieval_shape():
    """
    中文：这不是完整 retriever，而是企业 RAG 的并行检索形状。
    English: This is not a full retriever; it shows the shape of enterprise parallel retrieval.
    """

    vector_candidate = RunnableLambda(lambda x: {"source": "vector", "query": x["question"]})
    keyword_candidate = RunnableLambda(lambda x: {"source": "keyword", "query": x["question"]})
    metadata_candidate = RunnableLambda(lambda x: {"source": "metadata", "tenant_id": x["tenant_id"]})

    return RunnableParallel(
        vector=vector_candidate,
        keyword=keyword_candidate,
        metadata=metadata_candidate,
    )


def build_branch_shape():
    """
    中文：RunnableBranch 可以把不同 route 发到不同 collection 或 retriever。
    English: RunnableBranch can send different routes to different collections or retrievers.
    """

    return RunnableBranch(
        (lambda x: x["route"] == "policy", RunnableLambda(lambda x: f"use policy collection for {x['tenant_id']}")),
        (lambda x: x["route"] == "code", RunnableLambda(lambda x: f"use code collection for {x['tenant_id']}")),
        (lambda x: x["route"] == "support", RunnableLambda(lambda x: f"use support collection for {x['tenant_id']}")),
        RunnableLambda(lambda x: f"use general collection for {x['tenant_id']}"),
    )
