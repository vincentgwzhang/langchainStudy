"""
Enterprise structured output contracts.
企业级结构化输出合同。

Based on / 对应你的原始文件:
- 30.output1.py
- 30.output2.py

Advanced compared with your POC / 更先进的地方:
1. 中文：不只是返回 items/answer，而是返回答案、引用、置信度、风险标记、是否人工审核。
   English: Returns answer, citations, confidence, risk flags, and human-review decision, not just items/answer.
2. 中文：Pydantic schema 是业务合同，便于 API、前端、日志和评估系统消费。
   English: The Pydantic schema is a business contract for APIs, frontend, logs, and evaluation systems.
3. 中文：结构化输出不等于信任输出，高风险字段仍需要后端规则校验。
   English: Structured output does not mean trusted output; high-risk fields still need backend validation.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI


class Citation(BaseModel):
    doc_id: str = Field(description="Stable document or chunk ID used as evidence")
    source_uri: str = Field(description="Original source URI")
    quote: str = Field(description="Short supporting quote or paraphrased evidence")


class EnterpriseRagAnswer(BaseModel):
    answer: str = Field(description="Final answer shown to the user")
    citations: list[Citation] = Field(description="Evidence used to produce the answer")
    confidence: float = Field(ge=0, le=1, description="Model-estimated confidence from 0 to 1")
    answer_status: Literal["answered", "unknown", "needs_human_review"]
    risk_flags: list[str] = Field(default_factory=list)


def build_structured_answer_llm() -> ChatOpenAI:
    """
    中文：实际业务中建议 temperature=0，减少结构化输出波动。
    English: In production, temperature=0 is recommended to reduce structured-output variance.
    """

    return ChatOpenAI(model="gpt-5.5", temperature=0).with_structured_output(EnterpriseRagAnswer)


def validate_business_rules(answer: EnterpriseRagAnswer) -> EnterpriseRagAnswer:
    """
    中文：LLM 输出之后再做业务规则校验，这是企业级防线。
    English: Validate business rules after LLM output; this is an enterprise safety layer.
    """

    if answer.answer_status == "answered" and not answer.citations:
        answer.answer_status = "needs_human_review"
        answer.risk_flags.append("answered_without_citations")
    if answer.confidence < 0.5:
        answer.answer_status = "needs_human_review"
        answer.risk_flags.append("low_confidence")
    return answer
