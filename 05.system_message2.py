import os, pprint, json, time
from common import *
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

start_time = time.time()  # 获取开始时间
load_dotenv()
##############################################################################
messages = [
    SystemMessage("你是一语言专家，精通英语和中文。"),
    HumanMessage("可以帮我翻译一些英文成中文吗？"),
    AIMessage("当然可以！请告诉我你需要翻译的英文内容，我会尽力帮你翻译成中文。"),
    HumanMessage("book"),
]

model = ChatOpenAI(model="gpt-4o-mini")

result = model.invoke(messages)
print(result.content)
##############################################################################
print()
print(evalEndTime(start_time))