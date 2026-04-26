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

# :books: 组合日期和天气的获取工具

操作步骤

+ 编写两个工具，一个获取日期，一个获取天气

---
<style scoped>
  h1 {
    font-size: 64px;
    color: #f8f8f2;
    margin: 0;
  }
  section {
    align-items: center;
    justify-content: center;
  }
  img {
    border-radius: 2%;
    margin: 10;
    border: 50px solid #f8f8f2;
    background-color: #f8f8f2 !important;
  }
</style>

# 系统架构

![width:800px](./images/Lesson22a.png)

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
import pprint, time, json
from common import *
from dotenv import load_dotenv

from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI

print("=" * 100)

# 定义client_prompt
client_prompt = "今天的天气如何？"
# client_prompt = "我想学习Python"

start_time = time.time()  # 获取开始时间
load_dotenv()


# 取得当前日期
def get_date(*args, **kwargs):
    import datetime

    now = datetime.datetime.now()
    return "日期是：" + now.strftime("%Y-%m-%d")


# 获取天气
def get_weather(*args, **kwargs):
    return "天气是晴天"


tools = [
    Tool(
        name="获取日期",
        description="可以获取客户需要的日期",
        func=get_date,
    ),
    Tool(
        name="天气",
        description="需要指定日期，然后可以获取天气",
        func=get_weather,
    ),
]

# 取得ReAct提示词
# ReAct = Reason and Action
# https://smith.langchain.com/hub/hwchase17/react
prompt_react = hub.pull("hwchase17/react")
print(prompt_react.template)


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
    verbose=True,
    handle_parsing_errors=True,
)

response = agent_executor.invoke(
    {
        "input": client_prompt,
    }
)
pprint.pprint(response)

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

