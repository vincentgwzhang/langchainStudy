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

# :books: 创建一个简单的Agent

操作步骤

+ 扩展大语言模型，创建一个更多功能的 AI 程序

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
    margin: 0;
    border: 15px solid #f8f8f2;
  }
</style>

# 代理社区

![width:520px](./images/multiple-agents-chatdev.png)

https://developer.nvidia.com/blog/introduction-to-llm-agents/

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
    margin: 0;
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
# client_prompt = "现在几点了？"
# client_prompt = "今天的天气如何？"
client_prompt = "我想学习Python"

start_time = time.time()  # 获取开始时间
load_dotenv()


# 取得当前时间
def get_current_time(*args, **kwargs):
    import datetime

    now = datetime.datetime.now()
    return "现在时间是：" + now.strftime("%Y-%m-%d %H:%M:%S")


tools = [
    Tool(
        name="时间",
        description="可以获取当前时间",
        func=get_current_time,
    ),
]

# 取得ReAct提示词
# ReAct = Reason and Action
# - Reasoning: 为了执行后面的操作，思考需要的行动和理由
# - Action: 根据思考的结果(理由)，执行相应的操作
# - Observation: 根据执行的操作结果，观察结果，如果得到答案时则返回结果，如果不能得到答案时，那么再次思考行动和理由，形成循环。
# https://smith.langchain.com/hub/hwchase17/react
prompt_react = hub.pull("hwchase17/react")
prompt_react.pretty_print()


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 创建ReAct Agent
agent = create_react_agent(
    llm=llm,
    tools=[tools],
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

