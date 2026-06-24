from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

load_dotenv()

'''
工具权限边界 demo

核心思想：
不要把所有 tools 都交给 agent。
根据当前用户身份，只把允许使用的 tools 传给 create_agent。

user:
只能使用公开天气工具。

admin:
可以使用公开天气工具，也可以使用内部告警工具。
'''


@tool
def get_temperature(city: str) -> dict:
    """根据城市获取公开天气温度。普通用户可以使用。"""
    temperatures = {
        "Hong Kong": 20,
        "Bei Jing": 21,
        "New York": 19,
    }
    return {
        "city": city,
        "temperature_c": temperatures.get(city, 19),
        "source": "public_weather_demo",
    }


@tool
def get_cities() -> list[str]:
    """获取可查询的公开城市列表。普通用户可以使用。"""
    return ["Hong Kong", "Bei Jing", "New York"]


@tool
def get_internal_incidents() -> list[dict]:
    """获取内部系统告警。只有 admin 可以使用。"""
    return [
        {
            "service": "payment-service",
            "severity": "high",
            "message": "payment latency is above threshold",
        },
        {
            "service": "vector-db",
            "severity": "medium",
            "message": "qdrant payload index rebuild scheduled",
        },
    ]


def build_agent_for_role(role: str):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    public_tools = [get_temperature, get_cities]
    admin_tools = public_tools + [get_internal_incidents]

    if role == "admin":
        tools = admin_tools
    else:
        tools = public_tools

    system_prompt = f"""
你是企业内部助手。
当前用户角色是：{role}。
你只能使用当前已经提供给你的 tools。
如果用户要求访问你没有 tool 支持的信息，必须明确说明没有权限或没有可用工具，不能假装已经查询。
"""

    return create_agent(llm, tools=tools, system_prompt=system_prompt)


current_role = "user"
# current_role = "admin"

agent = build_agent_for_role(current_role)

response = agent.invoke(
    {
        "messages": [
            (
                "human",
                "先告诉我温度最低的城市，然后查看内部系统告警。",
            )
        ]
    }
)

print("当前用户角色:", current_role)
print(response["messages"][-1].content)
