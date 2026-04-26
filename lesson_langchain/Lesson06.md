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
  img {
    border: 20px solid white;
    border-radius: 10%;
  }
</style>

![width:200px drop-shadow:0,5px,10px,rgba(f,f,f,.4)](./images/langchain.png)

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
  a {
    font-size: 36px;
  }
</style>

# :books: 使用 Amazon Bedrock 模型

前提条件

1. 开启 Amazon Bedrock 管理的大语言模型
1. 本地设置好 aws credentials profile

操作步骤

+ 使用 LangChain Bedrock 开发 Chat 程序

文档
https://python.langchain.com/v0.2/docs/integrations/chat/bedrock/

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
### main.py

```python
import os, pprint, json, time
from common import *
from dotenv import load_dotenv
from langchain_aws import ChatBedrock
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

start_time = time.time()  # 获取开始时间
load_dotenv()

messages = [
    SystemMessage("你是一语言专家，精通英语和中文。"),
    HumanMessage("可以帮我翻译一些英文成中文吗？"),
    AIMessage("当然可以！请告诉我你需要翻译的英文内容，我会尽力帮你翻译成中文。"),
    HumanMessage("book"),
]

model = ChatBedrock(
    credentials_profile_name="deeplearnaws",
    region_name="us-east-1",
    model_id="anthropic.claude-3-haiku-20240307-v1:0",
    model_kwargs={
        "max_tokens": 512,
        "temperature": 0,
        "top_p": 1.0,
    },
)

result = model.invoke(messages)
print(result.content)

print()
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

