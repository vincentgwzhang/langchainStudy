import os, pprint, json, time
from common import *
from dotenv import load_dotenv
from langchain_aws import ChatBedrock
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

start_time = time.time()  # 获取开始时间
load_dotenv()

messages = [
    SystemMessage("你是一语言专家，精通英语和中文。"),
    HumanMessage("可以帮我翻译一些英文成中文吗？"),
    AIMessage("当然可以！请告诉我你需要翻译的英文内容，我会尽力帮你翻译成中文。"),
    HumanMessage("book"),
]

# model = ChatBedrock(
#     credentials_profile_name="deeplearnaws",
#     region_name="us-east-1",
#     model_id="anthropic.claude-3-haiku-20240307-v1:0",
#     model_kwargs={
#         "max_tokens": 512,
#         "temperature": 0,
#         "top_p": 1.0,
#     },
# )
model = ChatOpenAI(model="gpt-4o-mini")

result = model.invoke(messages)
print(result)
print("========================================")
print(result.content)

print()
print(evalEndTime(start_time))