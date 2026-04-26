---
marp: true
theme: default
header: 'LangChain AI开发课程'
footer: '小马技术'
style: |
  header {
    color: #00ced1;
    font-weight: bold;
  }
  footer {
    color: #50fa7b;
    font-weight: bold;
  }
  h1 {
    color: #f8f8f2;
    font-size: 64px;
  }
  section {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    background-color: #1d3d3c;
    color: #f8f8f2;
    font-size: 24px;
    font-family: Yuanti SC;
  }
  a {
    color: #8be9fd;
  }
  img {
    background-color: transparent!important;
  }
  code {
    font-family: JetBrains Mono;
  }

---
<style scoped>
  section {
    align-items: center;
    justify-content: center;
  }
  h1 {
    color: #f8f8f2;
    font-size: 120px;
  }
</style>

![width:300px drop-shadow:0,5px,10px,rgba(f,f,f,.4)](./images/langchain.png)

# LangChain

---
<style scoped>
  section {
    font-size: 40px;
  }
  h1 {
    font-size: 50px;
    color: #f8f8f2;
  }
  li {
    font-family: JetBrains Mono;
    font-size: 32px;
  }
</style>

# :books: 结构化输出 - 定义输出类

操作步骤

+ 定制结构化输出的规范类
+ 绑定大语言模型
+ 生成结构化输出

---
<style scoped>
  section {
    align-items: center;
    justify-content: center;
  }
  h1 {
    color: #f8f8f2;
    font-size: 200px;
    margin: 0;
  }
  img {
    border: 10px solid #f8f8f2;
    border-radius: 20%;
    margin: 0;
    box-shadow: 2px 2px 3px black;
  }
</style>

![width:200px](./images/step-by-step-operation.webp)

# 操作演示

---
<style scoped>
  h3 {
    margin-top: 0;
  }
  pre {
    box-shadow: 2px 2px 3px black;
  }
</style>
### main.py

```python
import os, pprint, json, time
from common import *
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from typing import Optional
from langchain_core.pydantic_v1 import BaseModel, Field

print("=" * 100)
start_time = time.time()  # 获取开始时间
load_dotenv()

# Pydantic
class Result(BaseModel):
    items: list[str] = Field(..., title="项目", description="项目列表")
    answer: str = Field(
        ..., title="最终回答", description="根据项目列表，一句话总结回答问题"
    )

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.5,
)
structured_llm = llm.with_structured_output(Result)

result = structured_llm.invoke("告诉我5个奥运会的项目")
# result = structured_llm.invoke("告诉我5个学习Python的步骤")
# result = structured_llm.invoke("告诉我5个日本旅游的景点")
print(result)
print("-" * 100)
print("回答项目：", result.items)
print("-" * 100)
print("最终回答：", result.answer)
print("-" * 100)

print(evalEndTime(start_time))
```

---
<style scoped>
  section {
    align-items: center;
    justify-content: center;
  }
  h1 {
    color: #f8f8f2;
    font-size: 200px;
  }
</style>

# 下课时间

