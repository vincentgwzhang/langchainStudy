import os, pprint, json, time
from common import *
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_aws import ChatBedrock
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

start_time = time.time()  # 获取开始时间
load_dotenv()

messages = [
    SystemMessage("你是一语言专家,精通英语和中文。所有回答请限制在35个字以内。"),
]

model = ChatOpenAI(model="gpt-4o-mini")

while True:
    user_input = input("> ")
    if user_input.lower() == "exit":
        break
    elif len(user_input.strip()) == 0:
        continue

    # 将用户消息加入数组
    messages.append(HumanMessage(user_input))

    # 调用模型
    result = model.invoke(messages)

    # 将模型返回的消息加入数组
    messages.append(AIMessage(result.content))

print(evalEndTime(start_time))
pprint.pprint(messages)