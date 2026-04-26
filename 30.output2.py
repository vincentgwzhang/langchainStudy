import os, pprint, json, time
from common import *
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

print("=" * 100)
start_time = time.time()  # 获取开始时间
load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)
structured_llm = llm.with_structured_output(None, method="json_mode")

prompt = ChatPromptTemplate.from_template(
    """Question: {question}

Instructions: 使用json模式输出, 项目数组输出到items[str]字段
Answer:
"""
)

result = structured_llm.invoke(prompt.invoke({"question": "告诉我5个奥运会的项目"}))
pprint.pprint(result)