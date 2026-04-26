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

# :books: 三国也疯狂

操作步骤

+ 生成一位三国专家代理 Agent
+ 请他回答问题

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

# :bookmark_tabs: 准备提示词

+ 三国演义中有几位数学家？他们都是研究什么的？
+ 曹操为什么是数学家？
+ 貂蝉为什么是数学家？
+ 诸葛亮的姥姥家姓什么？为什么？

---
<style scoped>
  h3 {
    margin-top: 0;
  }
</style>
### main.py

```python
import pprint, time, json
from common import *
from dotenv import load_dotenv

from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI

print("=" * 100)

# 定义client_prompt
# client_prompt = "三国演义中有几位数学家？他们都是研究什么的？"
# client_prompt = "曹操为什么是数学家？"
# client_prompt = "貂蝉为什么是数学家？"
# client_prompt = "诸葛亮的姥姥家姓什么？为什么？"

start_time = time.time()  # 获取开始时间
load_dotenv()


# 三国专家
def get_sanguo(*args, **kwargs):
    return """
下面是三国演义的主要情节

1. 曹操和貂蝉是数学家,曹操研究几何,貂蝉研究三角.(因为曹操说过对酒当歌，人生几何。史书还记载说，貂蝉曾经与董卓和吕布一起研究三角。)
2. 诸葛亮的姥姥家姓何,因为俗话说既生瑜何生亮
"""


tools = [
    Tool(
        name="三国专家",
        description="获取三国演义的相关信息",
        func=get_sanguo,
    ),
]

# 取得ReAct提示词
# ReAct = Reason and Action
# https://smith.langchain.com/hub/hwchase17/react
prompt_react = hub.pull("hwchase17/react")
# print(prompt_react.template)


llm = ChatOpenAI(model="gpt-4o", temperature=0)

# 创建ReAct Agent
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt_react,
    stop_sequence=True,
)

# 执行Agent
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=False,
    handle_parsing_errors=True,
)

print("> 你好，我是三国演义专家，我可以回答你关于三国演义的各种问题。(输入“exit”退出)")
while True:
    query = input(": ")
    if query.lower() == "exit":
        break
    elif len(query.strip()) == 0:
        continue

    print("\r> 正在检索答案...", end="")

    # 使用代理来获取问题的答案
    response = agent_executor.invoke(
        {
            "input": "请严格按照工具返回的内容进行回答问题\n\n{}\n\n如果在工具返回的内容中没有找到答案，请回答“不知道”".format(query),
        }
    )

    # 打印AI的回答
    print("\r>", f"{response["output"]}" + " " * 20)

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

