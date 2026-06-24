import json
import pprint

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent

load_dotenv()

@tool
def get_temperture(city: str) -> int:
    """根据城市获取该城市温度"""
    if city == 'Hong Kong':
        return 20
    elif city == 'Bei Jing':
        return 21
    else:
        return 19

@tool
def get_cities() -> list[str]:
    """获取城市列表"""
    return ['Hong Kong', 'Bei Jing', 'New York']

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

agent = create_agent(llm, tools=[get_temperture, get_cities])

response = agent.invoke({
    'messages': [
        ('human', '查看温度最低的城市')
    ]
})

print(response["messages"][-1].content)