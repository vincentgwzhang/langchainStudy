import os, pprint, json, time
from common import *
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

start_time = time.time()  # 获取开始时间

load_dotenv()  # 读取.env文件
##############################################################################
model = ChatOpenAI(model="gpt-4o-mini")
result = model.invoke("我在前台 ChatGPT 的聊天内容你能调用吗?")
pprint.pprint(result.content)
##############################################################################

print()
print(evalEndTime(start_time))