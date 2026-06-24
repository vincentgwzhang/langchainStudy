"""
Enterprise RAG ingestion pipeline.
企业级 RAG 入库流程。

Based on / 对应你的原始文件:
- 15.rag1.py
- 15.rag3.py
- common.py

Advanced compared with your POC / 更先进的地方:
1. 中文：不直接 empty_folder 删除旧库，而是用新 collection/schema_version 做可回滚迁移。
   English: Does not delete the old DB directly; uses a new collection/schema_version for rollback-safe migration.
2. 中文：每个 chunk 有稳定 ID、metadata、tenant_id、embedding model、source version。
   English: Every chunk has stable ID, metadata, tenant_id, embedding model, and source version.
3. 中文：ingestion 是幂等的，同一文档重复入库不会无限制造重复数据。
   English: Ingestion is idempotent; re-ingesting the same document does not create endless duplicates.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


@dataclass(frozen=True)
class IngestionConfig:
    tenant_id: str
    source_version: str
    source_type: str
    collection_name: str
    persist_directory: str
    embedding_model: str = "text-embedding-3-large"
    embedding_dimensions: int = 3072
    chunk_size: int = 900
    chunk_overlap: int = 150


def stable_chunk_id(source_uri: str, source_version: str, chunk_index: int, content: str) -> str:
    """
    中文：稳定 ID 是幂等入库和删除更新的基础。
    English: Stable IDs are the foundation of idempotent ingestion, deletion, and updates.
    """

    raw = f"{source_uri}|{source_version}|{chunk_index}|{hashlib.sha256(content.encode()).hexdigest()}"
    return hashlib.sha256(raw.encode()).hexdigest()


def load_and_split_text(path: Path, config: IngestionConfig) -> list[Document]:
    loader = TextLoader(str(path), encoding="utf-8")
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.chunk_size,
        chunk_overlap=config.chunk_overlap,
    )
    chunks = splitter.split_documents(documents)

    enriched: list[Document] = []
    for index, chunk in enumerate(chunks):
        doc_id = stable_chunk_id(str(path), config.source_version, index, chunk.page_content)
        chunk.metadata = {
            **chunk.metadata,
            "doc_id": doc_id,
            "tenant_id": config.tenant_id,
            "source_uri": str(path),
            "source_type": config.source_type,
            "source_version": config.source_version,
            "chunk_index": index,
            "embedding_model": config.embedding_model,
            "embedding_dimensions": config.embedding_dimensions,
        }
        enriched.append(chunk)
    return enriched


def build_vector_store(config: IngestionConfig) -> Chroma:
    """
    中文：显式 collection_name 是企业级要求，不能依赖默认 collection。
    English: Explicit collection_name is an enterprise requirement; do not rely on default collections.
    """

    embeddings = OpenAIEmbeddings(
        model=config.embedding_model,
        dimensions=config.embedding_dimensions,
    )
    return Chroma(
        collection_name=config.collection_name,
        persist_directory=config.persist_directory,
        embedding_function=embeddings,
    )


def ingest_text_file(path: Path, config: IngestionConfig) -> None:
    """
    中文：这是示例形状，不在这里运行。真实生产里会放进 Airflow、Dagster、Celery 或队列系统。
    English: This shows the shape only. In production, this belongs in Airflow, Dagster, Celery, or a queue worker.
    """

    vector_store = build_vector_store(config)
    chunks = load_and_split_text(path, config)
    ids = [chunk.metadata["doc_id"] for chunk in chunks]
    vector_store.add_documents(chunks, ids=ids)
