# 04. Structured Output

## Why It Matters

中文：企业系统不能只依赖自然语言文本，因为下游服务需要稳定字段。结构化输出让 LLM 的结果变成可校验的数据合同。

English: Enterprise systems cannot rely only on free-form natural language, because downstream services need stable fields. Structured output turns LLM responses into a validateable data contract.

## Pydantic Schema

```python
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

class RagAnswer(BaseModel):
    answer: str = Field(description="Final answer shown to the user")
    citations: list[str] = Field(description="Document IDs used as evidence")
    confidence: float = Field(description="0.0 to 1.0 confidence score")
    needs_human_review: bool

llm = ChatOpenAI(model="gpt-5.5", temperature=0)
structured_llm = llm.with_structured_output(RagAnswer)
```

## JSON Mode

中文：JSON mode 可以要求模型输出 JSON，但它不等于完整业务校验。企业里应该继续用 schema validation、required fields、type checks 和 fallback。

English: JSON mode asks the model to output JSON, but it is not full business validation. Enterprise systems should still use schema validation, required fields, type checks, and fallbacks.

## Production Rules

- 中文：所有对外 API 返回都应该有 schema。
- English: Every external API response should have a schema.

- 中文：解析失败要能重试、降级或进入人工审核。
- English: Parsing failures should trigger retry, fallback, or human review.

- 中文：不要让 LLM 自己决定权限、价格、退款、医疗建议等高风险字段。
- English: Do not let the LLM independently decide high-risk fields such as permissions, prices, refunds, or medical advice.
