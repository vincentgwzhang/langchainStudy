from uuid import uuid4

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langchain_core.tracers.langchain import wait_for_all_tracers
from langchain_openai import ChatOpenAI

load_dotenv()

'''
LangSmith 可观测性 demo

前提：
.env 里需要打开：
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=...
LANGSMITH_PROJECT=agent-observability-demo

这个文件重点观察：
1. agent run
2. LLM call
3. tool call
4. run_name
5. tags
6. metadata
'''


@tool
def get_temperature(city: str) -> dict:
    """根据城市获取该城市温度。"""
    temperatures = {
        "Hong Kong": 20,
        "Bei Jing": 21,
        "New York": 19,
    }
    return {
        "city": city,
        "temperature_c": temperatures.get(city, 19),
        "source": "mock_weather_service",
    }


@tool
def get_cities() -> list[str]:
    """获取可查询的城市列表。"""
    return ["Hong Kong", "Bei Jing", "New York"]


session_id = f"agent-session-{uuid4()}"
user_id = "vincent"

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

agent = create_agent(
    llm,
    tools=[get_temperature, get_cities],
    system_prompt=(
        "你是一个企业内部助手。"
        "如果需要数据，必须调用可用工具。"
        "回答时简洁说明你得到的结论。"
    ),
)

config: RunnableConfig = {
    "run_name": "agent_weather_observability_demo",
    "tags": [
        "study",
        "agent",
        "langsmith",
        "tool-calling",
        "weather-demo",
    ],
    "metadata": {
        "user_id": user_id,
        "session_id": session_id,
        "lesson": "agent_observability",
        "environment": "local",
        "tool_count": 2,
        "model": "gpt-4o-mini",
    },
}

response = agent.invoke(
    {
        "messages": [
            (
                "human",
                "查看温度最低的城市，并说明你用了哪些工具。",
            )
        ]
    },
    config=config,
)

print("session_id:", session_id)
print(response["messages"][-1].content)

# 本地脚本运行很快，等待 tracer 把数据提交到 LangSmith。
wait_for_all_tracers()
