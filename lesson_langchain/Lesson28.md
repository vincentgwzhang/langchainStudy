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

# :books: 自定义乘法工具(且故意出错)

操作步骤

+ 自定义乘法工具，并测试返回错误的结果

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
import pprint, time
from typing import Type
from langchain import hub
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from common import *

print("=" * 100)
start_time = time.time()  # 获取开始时间
load_dotenv()


class MultiplyToolArgs(BaseModel):
    a: int = Field(..., title="First number")
    b: int = Field(..., title="Second number")


class MultiplyTool(BaseTool):
    name = "multiply"
    description = "Multiply two numbers together"
    args_schema: Type[BaseModel] = MultiplyToolArgs

    def _run(self, a: int, b: int):
        """Multiply two numbers together"""
        print(f"Multiplying {a} by {b}")
        # return {"result": a * b}
        return {"result": 12345}  # 故意返回一个错误的结果


# 工具数组
tools = [MultiplyTool()]

# pprint.pprint(tools[0]._run(a=2, b=3))

# 创建LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# ReAct提示词
prompt = hub.pull("hwchase17/openai-tools-agent")

# 创建Agent
agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
)

# 创建Agent执行器
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
)

###############################################################################
# 调用Agent
response = agent_executor.invoke({"input": "计算一下2289乘以39098等于多少？"}) # echo "2289 * 39098" | bc
pprint.pprint(response)

###############################################################################
# 打印结束时间
print("\n", evalEndTime(start_time))
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

