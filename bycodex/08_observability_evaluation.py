"""
Enterprise observability and evaluation.
企业级可观测性和评估。

Based on / 对应你的原始文件:
- common.py
- 15.rag5.py
- 15.rag6.py

Advanced compared with your POC / 更先进的地方:
1. 中文：不只是打印程序耗时，而是记录 trace_id、模型、prompt、collection、doc_ids、latency、cost。
   English: Records trace_id, model, prompt, collection, doc_ids, latency, and cost instead of only printing runtime.
2. 中文：支持 retrieval 评估指标，例如 Recall@K、MRR。
   English: Supports retrieval metrics such as Recall@K and MRR.
3. 中文：线上问题可以回放，因为输入、检索结果和模型版本都有记录。
   English: Production issues can be replayed because inputs, retrieved docs, and model versions are logged.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field


@dataclass
class RagTrace:
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str = ""
    question: str = ""
    prompt_version: str = ""
    llm_model: str = ""
    embedding_model: str = ""
    collection_name: str = ""
    retrieved_doc_ids: list[str] = field(default_factory=list)
    started_at: float = field(default_factory=time.time)
    latency_ms: float | None = None

    def finish(self) -> None:
        self.latency_ms = (time.time() - self.started_at) * 1000


def recall_at_k(expected_doc_ids: set[str], retrieved_doc_ids: list[str], k: int) -> float:
    """
    中文：Recall@K 衡量正确文档是否出现在前 K 个结果里。
    English: Recall@K measures whether relevant documents appear in the top K results.
    """

    if not expected_doc_ids:
        return 0.0
    top_k = set(retrieved_doc_ids[:k])
    return len(expected_doc_ids & top_k) / len(expected_doc_ids)


def mrr(expected_doc_ids: set[str], retrieved_doc_ids: list[str]) -> float:
    """
    中文：MRR 关注第一个正确结果排在多前面。
    English: MRR focuses on how early the first relevant result appears.
    """

    for index, doc_id in enumerate(retrieved_doc_ids, start=1):
        if doc_id in expected_doc_ids:
            return 1.0 / index
    return 0.0


def log_trace(trace: RagTrace) -> dict:
    """
    中文：示例返回 dict；真实企业里会写入 LangSmith、OpenTelemetry、ELK、Datadog 或数据仓库。
    English: This returns a dict; production would send it to LangSmith, OpenTelemetry, ELK, Datadog, or a warehouse.
    """

    trace.finish()
    return trace.__dict__
