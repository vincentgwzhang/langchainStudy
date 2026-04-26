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
    font-size: 36px;
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

# :books: 自定义链式调用函数

操作步骤

+ RunnableLambda 的基本使用
+ 使用 RunnableLambda 和 RunnableSequence 完成链式调用

官方文档
https://python.langchain.com/v0.2/docs/how_to/functions/

⭐️ RunnableLambda 允许将一个任意的Python函数包装成一个可以在LangChain框架中运行的组件。主要用于定义自定义的任务或操作，这些任务可以在你的语言链中作为一个节点执行。

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
### 例子1

```python
from langchain.schema.runnable import RunnableLambda

# 字母大写
def to_uppercase(inputs):
    return inputs.upper()

# 前后加括号
def append_comma(inputs):
    return f"[[[{inputs}]]]"


to_uppercase_lambda = RunnableLambda(to_uppercase)
append_comma_lambda = RunnableLambda(append_comma)

chain = to_uppercase_lambda | append_comma_lambda
print(chain.invoke("hello world"))
```

---
<style scoped>
  h3 {
    margin-top: 0;
  }
</style>
### 例子2

```python
import time
from common import *
from dotenv import load_dotenv
from langchain_aws import ChatBedrock
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableLambda, RunnableSequence

start_time = time.time()  # 获取开始时间
load_dotenv()

# 消息数组
print("=" * 100)
messages = [
    ("system", "你是一位{career}专家，你经常辅导你的学生。"),
    ("human", "我想学习{language}，给我几个建议好吗？"),
]
prompt_template = ChatPromptTemplate.from_messages(messages)
# 语言模型
model = ChatBedrock(
    credentials_profile_name="deeplearnaws",
    region_name="us-east-1",
    model_id="anthropic.claude-3-haiku-20240307-v1:0",
    model_kwargs={"max_tokens": 512, "temperature": 0, "top_p": 1.0,},
)

# 使用Chain调用模型
# chain = prompt_template | model | StrOutputParser()
# ↓
run_prompt = RunnableLambda(lambda x: prompt_template.invoke(x))
run_model = RunnableLambda(lambda x: model.invoke(x.to_messages()))
run_output = RunnableLambda(lambda x: StrOutputParser().invoke(x))

chain = RunnableSequence(first=run_prompt, middle=[run_model], last=run_output)
result = chain.invoke({"career": "医学", "language": "按摩"})
print(result)

# 打印结束时间
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

