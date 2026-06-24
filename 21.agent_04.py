from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

load_dotenv()

'''
Agent 会话状态 demo

问题：
agent.invoke(...) 默认只知道你这一次传进去的 messages。
如果第二次 invoke 没有带上上一轮 messages，agent 不会自动记得上一轮说过什么。

企业里常见会话状态包括：
1. user_id: 谁在说话
2. session_id / thread_id: 哪一次会话
3. chat_history: 历史消息
4. tool call history: 过去调用过哪些工具
5. retrieved context: 上一轮检索过哪些资料

这个 demo 只演示 chat_history。
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
    """获取城市列表。"""
    return ["Hong Kong", "Bei Jing", "New York"]


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

agent = create_agent(
    llm,
    tools=[get_temperature, get_cities],
    system_prompt=(
        "你是企业内部助手。"
        "如果需要数据，必须调用可用工具。"
        "回答时尽量使用 tool 返回的原始城市名称。"
    ),
)

print("=" * 100)
print("Case 1: 不带会话状态")

response1 = agent.invoke(
    {
        "messages": [
            ("human", "查看温度最低的城市。"),
        ]
    }
)
print("第一轮:", response1["messages"][-1].content)

response2 = agent.invoke(
    {
        "messages": [
            ("human", "刚刚那个城市的温度是多少？"),
        ]
    }
)
print("第二轮:", response2["messages"][-1].content)

print("=" * 100)
print("Case 2: 手动带上会话状态")

chat_history = []

chat_history.append(("human", "查看温度最低的城市。"))
response3 = agent.invoke({"messages": chat_history})
print("第一轮:", response3["messages"][-1].content)

# create_agent 的 response["messages"] 里包含 human / ai / tool messages。
# 下一轮把这些 messages 继续传回去，agent 才知道上一轮发生了什么。
chat_history = response3["messages"]
chat_history.append(("human", "刚刚那个城市的温度是多少？"))

response4 = agent.invoke({"messages": chat_history})
print("第二轮:", response4["messages"][-1].content)
