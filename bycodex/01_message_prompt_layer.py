"""
Enterprise message and prompt layer.
企业级 Message 和 Prompt 层。

Based on / 对应你的原始文件:
- 05.system_message.py
- 05.system_message2.py
- 08.promptTemplate1.py
- 08.promptTemplate2.py
- expression_language.py

Advanced compared with your POC / 更先进的地方:
1. 中文：把 system policy、用户问题、检索上下文分开，不把所有内容拼成一个大字符串。
   English: Separates system policy, user question, and retrieved context instead of mixing everything into one large string.
2. 中文：Prompt 有版本号，方便 A/B test、回滚和线上排查。
   English: Prompts have versions for A/B testing, rollback, and production debugging.
3. 中文：明确 grounded answering 规则：只能根据 context，不知道就说不知道。
   English: Explicit grounded-answering rules: answer only from context; say unknown if context is insufficient.
"""

from __future__ import annotations

from dataclasses import dataclass

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


@dataclass(frozen=True)
class PromptVersion:
    name: str
    version: str

    @property
    def id(self) -> str:
        return f"{self.name}:{self.version}"


RAG_PROMPT_VERSION = PromptVersion(name="enterprise_rag_answer", version="2026-06-22")


def build_grounded_rag_prompt() -> ChatPromptTemplate:
    """
    中文：这是企业级 RAG prompt 的基本形状。
    English: This is the basic shape of an enterprise RAG prompt.
    """

    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are an enterprise RAG assistant.
Answer only using the provided context.
If the context is insufficient, say you do not know.
Do not invent citations.
Return concise, factual, auditable answers.

中文规则：
你是企业级 RAG 助手。
只能根据提供的上下文回答。
如果上下文不足，直接说不知道。
不要编造引用。
答案要简洁、事实化、可审计。

Prompt version: {prompt_version}
""".strip(),
            ),
            MessagesPlaceholder("chat_history"),
            (
                "human",
                """
Question / 用户问题:
{question}

Retrieved context / 检索上下文:
{context}
""".strip(),
            ),
        ]
    )


def build_query_rewrite_prompt() -> ChatPromptTemplate:
    """
    中文：多轮对话里不要直接拿最后一句去检索，应该先改写成独立问题。
    English: In multi-turn chat, do not retrieve with only the last utterance. Rewrite it into a standalone query first.
    """

    return ChatPromptTemplate.from_messages(
        [
            ("system", "Rewrite the latest user question as a standalone search query. Keep facts unchanged."),
            MessagesPlaceholder("chat_history"),
            ("human", "Latest question: {question}"),
        ]
    )
