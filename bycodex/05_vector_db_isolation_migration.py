"""
Vector DB isolation and embedding-model migration.
Vector DB 隔离和 embedding 模型迁移。

Based on / 对应你的原始文件:
- 15.rag1.py
- 15.rag2.py
- 15.rag3.py
- 15.rag4.py
- 15.rag5.py

Advanced compared with your POC / 更先进的地方:
1. 中文：使用 collection_name 表达隔离，不再只是换 persist_directory。
   English: Uses collection_name for isolation, not only different persist_directory values.
2. 中文：新旧 embedding model 用 parallel collection 做 shadow traffic / A/B testing。
   English: Old and new embedding models use parallel collections for shadow traffic / A/B testing.
3. 中文：查询向量和文档向量必须来自同一 embedding model。
   English: Query embeddings and document embeddings must come from the same embedding model.
"""

from __future__ import annotations

from dataclasses import dataclass

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings


@dataclass(frozen=True)
class VectorSpace:
    name: str
    tenant_id: str
    domain: str
    schema_version: str
    embedding_model: str
    dimensions: int
    persist_directory: str

    @property
    def collection_name(self) -> str:
        model_slug = self.embedding_model.replace("text-embedding-", "te").replace("-", "")
        return f"{self.tenant_id}_{self.domain}_{self.schema_version}_{model_slug}_{self.dimensions}"

    def as_chroma(self) -> Chroma:
        return Chroma(
            collection_name=self.collection_name,
            persist_directory=self.persist_directory,
            embedding_function=OpenAIEmbeddings(model=self.embedding_model, dimensions=self.dimensions),
        )


OLD_SPACE = VectorSpace(
    name="old_production",
    tenant_id="tenant_acme",
    domain="policy",
    schema_version="v1",
    embedding_model="text-embedding-3-small",
    dimensions=1536,
    persist_directory="./chroma_prod",
)

NEW_SPACE = VectorSpace(
    name="candidate",
    tenant_id="tenant_acme",
    domain="policy",
    schema_version="v2",
    embedding_model="text-embedding-3-large",
    dimensions=3072,
    persist_directory="./chroma_prod",
)


def build_shadow_retrievers(k: int = 5):
    """
    中文：shadow traffic 同时查 old/new，但用户先只看到 old，new 用于记录评估。
    English: Shadow traffic queries old/new simultaneously, but users initially see only old; new is logged for evaluation.
    """

    old_retriever = OLD_SPACE.as_chroma().as_retriever(search_kwargs={"k": k})
    new_retriever = NEW_SPACE.as_chroma().as_retriever(search_kwargs={"k": k})
    return old_retriever, new_retriever


def compare_retrieval_results(question: str) -> dict:
    """
    中文：这里展示 A/B 评估数据结构，不实际执行线上切流。
    English: This shows the A/B evaluation data structure; it does not actually shift production traffic.
    """

    old_retriever, new_retriever = build_shadow_retrievers()
    old_docs = old_retriever.invoke(question)
    new_docs = new_retriever.invoke(question)
    return {
        "question": question,
        "old_collection": OLD_SPACE.collection_name,
        "new_collection": NEW_SPACE.collection_name,
        "old_doc_ids": [doc.metadata.get("doc_id") for doc in old_docs],
        "new_doc_ids": [doc.metadata.get("doc_id") for doc in new_docs],
    }
