import time
from common import *
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

start_time = time.time()
load_dotenv()

# 1️⃣ 定义 Prompt（你原来少了这一步）
template = "我想学习{language}语言，给我几个开发框架好吗？"
prompt_template = ChatPromptTemplate.from_template(template)

prompt = prompt_template.invoke({"language": "Python"})

# 2️⃣ 定义模型（替换 Bedrock）
model = ChatOpenAI(
    model="gpt-4o-mini",   # 推荐：便宜 + 快
    temperature=0,
    max_tokens=512,
)

# 3️⃣ 调用模型
result = model.invoke(prompt)

print(result.content)

# 4️⃣ 时间统计
print(evalEndTime(start_time))