"""
Enterprise retrieval and generation pipeline.
企业级检索与生成流程。

Based on / 对应你的原始文件:
- 15.rag2.py
- 15.rag4.py
- 15.rag5.py
- 15.rag6.py

Advanced compared with your POC / 更先进的地方:
1. 中文：检索时加入 tenant/source/version/model 过滤，而不是直接 similarity_search。
   English: Retrieval uses tenant/source/version/model filters, not just direct similarity_search.
2. 中文：把 retrieval、context formatting、prompt、LLM、structured output 拆开。
   English: Separates retrieval, context formatting, prompt, LLM, and structured output.
3. 中文：支持 chat history，但检索上下文和聊天历史分开处理。
   English: Supports chat history while keeping retrieved context separate from chat history.
"""

from __future__ import annotations

from typing import Any

from langchain_core.documents import Document
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


class RetrievalRequest(BaseModel):
    tenant_id: str
    question: str
    chat_history: list[BaseMessage] = Field(default_factory=list)
    source_type: str = "policy"
    source_version: str = "2026-06-22"


class RetrievalTrace(BaseModel):
    collection_name: str
    doc_ids: list[str]
    scores: list[float] = Field(default_factory=list)


class RagResponse(BaseModel):
    answer: str
    cited_doc_ids: list[str]
    trace: RetrievalTrace


def format_context(docs: list[Document]) -> str:
    """
    中文：上下文要带 doc_id，方便答案引用和审计。
    English: Context should include doc_id for citation and auditing.
    """

    blocks = []
    for doc in docs:
        doc_id = doc.metadata.get("doc_id", "unknown")
        source = doc.metadata.get("source_uri", "unknown")
        blocks.append(f"[doc_id={doc_id} source={source}]\n{doc.page_content}")
    return "\n\n---\n\n".join(blocks)


def build_retriever(vector_store: Any, request: RetrievalRequest):
    """
    中文：过滤条件是企业级 RAG 的权限和版本边界。
    English: Filters are the permission and version boundary of enterprise RAG.
    """

    return vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 6,
            "fetch_k": 40,
            "filter": {
                "tenant_id": request.tenant_id,
                "source_type": request.source_type,
                "source_version": request.source_version,
            },
        },
    )


def build_answer_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Answer only from context. If context is insufficient, say you do not know. Cite doc IDs.",
            ),
            MessagesPlaceholder("chat_history"),
            ("human", "Question: {question}\n\nContext:\n{context}"),
        ]
    )


def answer_with_rag(vector_store: Any, request: RetrievalRequest) -> RagResponse:
    retriever = build_retriever(vector_store, request)
    docs = retriever.invoke(request.question)
    context = format_context(docs)

    prompt = build_answer_prompt()
    llm = ChatOpenAI(model="gpt-5.5", temperature=0)
    message_value = prompt.invoke(
        {
            "question": request.question,
            "context": context,
            "chat_history": request.chat_history,
        }
    )
    result = llm.invoke(message_value)

    doc_ids = [str(doc.metadata.get("doc_id", "unknown")) for doc in docs]
    return RagResponse(
        answer=result.content,
        cited_doc_ids=doc_ids,
        trace=RetrievalTrace(collection_name="provided_by_vector_store", doc_ids=doc_ids),
    )
