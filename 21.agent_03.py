from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

load_dotenv()

'''
Agent 错误处理 demo

企业里常见错误：
1. 用户输入不合法
2. tool 参数不合法
3. tool 查询不到数据
4. 外部服务超时或失败
5. tool 返回格式不稳定
6. agent 没有足够信息，应该回答无法完成，而不是编造

这个 demo 的原则：
tool 不直接抛异常给 agent。
tool 返回稳定结构：
{
    "ok": True/False,
    "data": ...,
    "error": ...
}
'''


@tool
def get_temperature(city: str) -> dict:
    """根据城市获取该城市温度。如果城市不存在，返回错误结构。"""
    temperatures = {
        "Hong Kong": 20,
        "Bei Jing": 21,
        "New York": 19,
    }

    if not city or not city.strip():
        return {
            "ok": False,
            "data": None,
            "error": {
                "code": "INVALID_CITY",
                "message": "city 不能为空",
            },
        }

    if city not in temperatures:
        return {
            "ok": False,
            "data": None,
            "error": {
                "code": "CITY_NOT_FOUND",
                "message": f"没有找到城市 {city} 的温度数据",
            },
        }

    return {
        "ok": True,
        "data": {
            "city": city,
            "temperature_c": temperatures[city],
            "source": "mock_weather_service",
        },
        "error": None,
    }


@tool
def get_cities() -> dict:
    """获取可查询的城市列表。"""
    return {
        "ok": True,
        "data": ["Hong Kong", "Bei Jing", "New York"],
        "error": None,
    }


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

agent = create_agent(
    llm,
    tools=[get_temperature, get_cities],

    # 外面的括号只是为了换行好看。
    # 这里其实几个字符串连在一起最终会合拼
    system_prompt=(
        "你是企业内部助手。"
        "调用工具后必须检查 ok 字段。"
        "如果 ok=false，要向用户说明失败原因，不能编造数据。"
        "如果部分工具失败，要说明哪些成功、哪些失败。"
    ),
)

response = agent.invoke(
    {
        "messages": [
            ("human", "请查询 Hong Kong 和 Tokyo 的温度。如果有城市查不到，请明确告诉我。")
        ]
    }
)

print(response["messages"][-1].content)
