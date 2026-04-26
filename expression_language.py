import time
from common import *
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

start_time = time.time()
load_dotenv()
print("=" * 100)

messages = [
    ("system", "你是一位{career}专家，你经常辅导你的学生。"),
    ("human", "我想学习{language}，给我几个建议好吗？"),
]
prompt_template = ChatPromptTemplate.from_messages(messages)
model = ChatOpenAI(model="gpt-4o-mini")

chain = prompt_template | model | StrOutputParser()
result = chain.invoke({"career": "医学", "language": "按摩"})
print(result)