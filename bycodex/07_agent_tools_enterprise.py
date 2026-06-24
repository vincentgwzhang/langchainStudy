"""
Enterprise agent and tools.
企业级 Agent 和工具调用。

Based on / 对应你的原始文件:
- 21.agent.py

Advanced compared with your POC / 更先进的地方:
1. 中文：工具参数使用 Pydantic schema，避免随意字符串输入。
   English: Tool arguments use Pydantic schemas instead of arbitrary strings.
2. 中文：工具函数内有权限边界和审计字段。
   English: Tool functions include permission boundaries and audit fields.
3. 中文：Agent 不直接做危险动作，只读取或提出计划，高风险动作交给审批系统。
   English: The agent does not directly perform dangerous actions; it reads or proposes plans, while high-risk actions go to approval systems.
"""

from __future__ import annotations

from typing import Literal

from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


class PolicyLookupInput(BaseModel):
    tenant_id: str = Field(description="Tenant ID for permission isolation")
    policy_id: str = Field(description="Stable policy document ID")
    requester_role: Literal["employee", "support", "admin"]


@tool(args_schema=PolicyLookupInput)
def get_policy_summary(tenant_id: str, policy_id: str, requester_role: str) -> dict:
    """
    中文：根据 policy_id 查询政策摘要。真实系统里这里会查数据库，并做 ACL 检查。
    English: Fetch a policy summary by policy_id. In production, this queries a database and enforces ACL checks.
    """

    if requester_role not in {"support", "admin"}:
        return {
            "allowed": False,
            "reason": "insufficient_role",
            "audit_event": "policy_lookup_denied",
        }
    return {
        "allowed": True,
        "tenant_id": tenant_id,
        "policy_id": policy_id,
        "summary": "Refund requests require receipt, approval, and policy version validation.",
        "audit_event": "policy_lookup_allowed",
    }


def build_policy_agent():
    """
    中文：企业 agent 要使用低温度、工具 schema、日志和权限控制。
    English: Enterprise agents should use low temperature, tool schemas, logs, and permission controls.
    """

    llm = ChatOpenAI(model="gpt-5.5", temperature=0)
    return create_agent(llm, tools=[get_policy_summary])
