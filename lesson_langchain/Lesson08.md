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
    font-family: Menlo;
    font-size: 32px;
  }
</style>

# :books: 使用提示词模版

操作步骤

+ 提示词模版的用法(组织编码)
+ 使用提示词模版(传给LLM)

官方文档
https://api.python.langchain.com/en/latest/prompts/langchain_core.prompts.chat.ChatPromptTemplate.html

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
  }
</style>

![width:200px](./images/step-by-step-operation.webp)

# 操作演示

---
<style scoped>
  h3 {
    margin-top: 0;
  }
</style>
### 提示词模版的基本语法

```python
from langchain.prompts import ChatPromptTemplate

# 单参数
print("=" * 100)
template = "我想学习{language}语言，给我几个开发框架好吗？"
prompt_template = ChatPromptTemplate.from_template(template)

prompt = prompt_template.invoke({"language": "Python"})
print(prompt)
prompt = prompt_template.invoke({"language": "Java"})
print(prompt)
prompt = prompt_template.invoke({"language": "PHP"})
print(prompt)

# 多参数
print("=" * 100)
template = "我想学习{language}语言，给我几个开发{target}好吗？"
prompt_template = ChatPromptTemplate.from_template(template)

prompt = prompt_template.invoke({"language": "Python", "target": "框架"})
print(prompt)
prompt = prompt_template.invoke({"language": "Python", "target": "例子"})
print(prompt)

# 消息数组
print("=" * 100)
messages = [
    ("system", "你是一位{career}专家，你经常辅导你的学生。"),
    ("human", "我想学习{language}，给我几个建议好吗？"),
]
prompt_template = ChatPromptTemplate.from_messages(messages)
prompt = prompt_template.invoke({"career": "IT", "language": "Python"})
print(prompt)
prompt = prompt_template.invoke({"career": "医学", "language": "按摩"})
print(prompt)
```


---
<style scoped>
  h3 {
    margin-top: 0;
  }
</style>
### 使用提示词模版

```python
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

