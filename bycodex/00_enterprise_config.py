"""
Enterprise AI/RAG configuration layer.
企业级 AI/RAG 配置层。

Based on / 对应你的原始文件:
- 04.basic.py
- 05.system_message.py
- 05.system_message2.py
- 06.aws_bedrock.py
- 06.aws_bedrock2.py

Advanced compared with your POC / 相比你原来的 POC 更先进的地方:
1. 中文：模型名称、embedding 模型、vector DB 路径、collection 命名不再散落在业务代码里。
   English: Model names, embedding models, vector DB paths, and collection names are no longer scattered in business code.
2. 中文：显式区分 quality model、fast model、embedding model，企业里便于路由和成本控制。
   English: Separates quality model, fast model, and embedding model for routing and cost control.
3. 中文：为 collection 命名加入 tenant、domain、版本、模型、维度，避免不同 embedding 空间互相污染。
   English: Collection names include tenant, domain, version, model, and dimension to avoid mixing incompatible embedding spaces.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

load_dotenv()


@dataclass(frozen=True)
class ModelConfig:
    """
    中文：模型配置是企业代码的入口，不应该在每个业务文件里硬编码。
    English: Model configuration is the entry point of enterprise code and should not be hard-coded in every business file.
    """

    quality_model: str = "gpt-5.5"
    fast_model: str = "gpt-5-nano"
    embedding_model: str = "text-embedding-3-large"
    embedding_dimensions: int = 3072
    temperature: float = 0.0
    timeout_seconds: int = 30
    max_retries: int = 2


@dataclass(frozen=True)
class RagIndexConfig:
    """
    中文：Vector DB 隔离配置。这里的 collection 是生产级概念，不是 demo 默认 collection。
    English: Vector DB isolation config. The collection here is a production concept, not a demo default collection.
    """

    tenant_id: str = "tenant_acme"
    domain: str = "policy"
    schema_version: str = "v2"
    persist_directory: Path = Path("./chroma_prod")

    def collection_name(self, model_config: ModelConfig) -> str:
        model_slug = model_config.embedding_model.replace("text-embedding-", "te").replace("-", "")
        return f"{self.tenant_id}_{self.domain}_{self.schema_version}_{model_slug}_{model_config.embedding_dimensions}"


def build_quality_llm(config: ModelConfig) -> ChatOpenAI:
    """
    中文：高质量模型用于最终回答、复杂推理、结构化输出。
    English: The quality model is used for final answers, complex reasoning, and structured output.
    """

    return ChatOpenAI(
        model=config.quality_model,
        temperature=config.temperature,
        timeout=config.timeout_seconds,
        max_retries=config.max_retries,
    )


def build_fast_llm(config: ModelConfig) -> ChatOpenAI:
    """
    中文：快速模型用于分类、路由、轻量改写，节省成本和延迟。
    English: The fast model is used for classification, routing, and lightweight rewriting to reduce cost and latency.
    """

    return ChatOpenAI(
        model=config.fast_model,
        temperature=0,
        timeout=15,
        max_retries=config.max_retries,
    )


def build_embeddings(config: ModelConfig) -> OpenAIEmbeddings:
    """
    中文：embedding 模型必须和 collection 版本绑定。换模型时建立新 collection。
    English: The embedding model must be tied to the collection version. Create a new collection when changing models.
    """

    return OpenAIEmbeddings(
        model=config.embedding_model,
        dimensions=config.embedding_dimensions,
    )
