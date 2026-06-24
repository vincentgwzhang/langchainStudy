# 02. Model And Message Layer

## From Demo To Enterprise

中文：POC 里可以直接 `ChatOpenAI(model="gpt-4o-mini")`。企业里不要把模型名字散落在业务代码里，应该通过配置、模型路由和环境变量管理。

English: In a POC, directly calling `ChatOpenAI(model="gpt-4o-mini")` is fine. In enterprise systems, model names should not be scattered across business code. They should be managed through configuration, model routing, and environment variables.

## Recommended Pattern

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-5.5",
    temperature=0,
    timeout=30,
    max_retries=2,
)

fast_llm = ChatOpenAI(
    model="gpt-5-nano",
    temperature=0,
    timeout=15,
    max_retries=2,
)
```

## Message Roles

中文：`system` 负责长期行为规则，`human` 是用户输入，`ai` 是模型历史回答。企业里要避免把权限、安全、合规规则写进普通 human prompt。

English: `system` defines durable behavior rules, `human` is user input, and `ai` is historical model output. In enterprise systems, permission, safety, and compliance rules should not be hidden inside ordinary human prompts.

Example:

```python
messages = [
    ("system", "Answer only from retrieved context. If unknown, say you do not know."),
    ("human", "{question}"),
]
```

## Chat History

中文：你在 `15.rag6.py` 里手动维护 `chat_history`。企业里通常会把 conversation state 存到 Redis、Postgres 或专门的 conversation store，并设置最大轮数、token budget 和隐私策略。

English: In `15.rag6.py`, chat history is maintained manually. In enterprise systems, conversation state is usually stored in Redis, Postgres, or a dedicated conversation store, with max turns, token budget, and privacy policies.

Enterprise rules:

- never store sensitive content without policy
- summarize old turns when context grows too large
- store trace IDs for debugging
- separate user-visible history from internal retrieval logs

## Provider Layer

中文：你的代码里有 OpenAI 和 Bedrock 的切换影子。企业里应抽象 provider layer，让业务层不关心模型来自 OpenAI、Azure OpenAI、Bedrock 还是私有模型。

English: Your code hints at switching between OpenAI and Bedrock. In enterprise systems, use a provider layer so business code does not care whether the model comes from OpenAI, Azure OpenAI, Bedrock, or a private model.
