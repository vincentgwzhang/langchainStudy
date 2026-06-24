"""
Enterprise RAG reference shape.
企业级 RAG 参考应用形状。

This file intentionally does not run by itself.
这个文件故意不直接运行。

中文：它把 bycodex 里的企业级模块串起来，展示真实系统应该如何组织，而不是像 POC 那样把所有逻辑写在一个脚本里。
English: It connects the enterprise modules under bycodex and shows how a real system should be organized, instead of putting all logic into one script like a POC.

Based on / 对应你的原始文件:
- 04.basic.py through 30.output2.py, especially 15.rag*.py
"""

from __future__ import annotations

from pathlib import Path

from bycodex_compat import explain_import_note

# The imports below show the intended architecture.
# 下面的 imports 展示目标架构。
# In a real package, bycodex would be installed or added to PYTHONPATH.


def enterprise_flow_summary() -> list[str]:
    """
    中文：企业级 RAG 的最小稳定路径。
    English: The minimum stable path of enterprise RAG.
    """

    return [
        "1. Load config / 加载配置",
        "2. Build model and embeddings / 初始化模型和 embedding",
        "3. Ingest docs into explicit collection / 文档进入明确 collection",
        "4. Retrieve with tenant/version filters / 带租户和版本过滤检索",
        "5. Generate grounded structured answer / 生成 grounded 结构化答案",
        "6. Log trace and evaluate / 记录 trace 并评估",
        "7. Migrate through parallel collections / 用 parallel collection 迁移",
    ]


def compare_with_original_poc() -> dict[str, str]:
    """
    中文：说明相比你的原始脚本，企业版提升在哪里。
    English: Explains how the enterprise version improves over your original scripts.
    """

    return {
        "model_usage": "Original: model is hard-coded in scripts. Enterprise: centralized config and routing.",
        "vector_db": "Original: persist_directory only. Enterprise: explicit collection_name plus tenant/domain/model/version isolation.",
        "ingestion": "Original: simple load/split/store. Enterprise: stable IDs, metadata, idempotency, audit fields.",
        "retrieval": "Original: direct similarity_search/as_retriever. Enterprise: filters, MMR, trace, evaluation metrics.",
        "generation": "Original: text answer. Enterprise: grounded answer with citations and structured schema.",
        "agent": "Original: simple temperature tools. Enterprise: schema-validated tools with permission boundary.",
    }


if __name__ == "__main__":
    print(explain_import_note(Path(__file__).parent))
    for line in enterprise_flow_summary():
        print(line)
