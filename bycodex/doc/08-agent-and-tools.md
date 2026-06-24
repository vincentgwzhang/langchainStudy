# 08. Agent And Tools

## What Your Code Shows

中文：`21.agent.py` 展示了 LangChain tool 和 `create_agent`：模型可以决定调用哪个工具，再根据工具结果回答。

English: `21.agent.py` demonstrates LangChain tools and `create_agent`: the model can decide which tool to call and answer using the tool result.

## Enterprise Meaning

中文：Agent 不是“让模型自由发挥”。企业 Agent 是受控执行器：工具有权限、输入有 schema、输出有审计、失败有降级。

English: An agent is not “let the model do anything.” An enterprise agent is a controlled executor: tools have permissions, inputs have schemas, outputs are audited, and failures have fallbacks.

## Tool Design

```python
from langchain_core.tools import tool

@tool
def get_policy_by_id(policy_id: str) -> dict:
    """Fetch a policy document by stable policy ID."""
    ...
```

## Production Rules

- 中文：工具名要表达业务动作，不要太泛。
- English: Tool names should describe business actions and should not be too generic.

- 中文：工具参数必须可校验，不要接受任意自然语言然后直接执行。
- English: Tool arguments must be validateable; do not accept arbitrary natural language and execute it directly.

- 中文：高风险工具需要权限检查、人工审批或双确认。
- English: High-risk tools require permission checks, human approval, or double confirmation.

- 中文：工具调用要记录 trace：用户、参数、结果、耗时、错误。
- English: Tool calls should be traced: user, arguments, result, latency, and errors.

## RAG Agent Pattern

```text
user question
  -> classify intent
  -> retrieve documents
  -> maybe call tool
  -> generate grounded answer
  -> structured output
```

## Avoid

中文：不要让 Agent 直接操作数据库写入、退款、删除数据，除非有严格权限和审批流。

English: Do not let an agent directly write to databases, issue refunds, or delete data unless strict permissions and approval workflows exist.
