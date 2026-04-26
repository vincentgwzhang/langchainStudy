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

# :books: 使用 Tavily 检索

操作步骤

+ 生成 Tavily API 密钥
+ 建立互联网检索工具，查询及时的信息

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
## 课堂实验

### Tavily API Key 发行
https://tavily.com/

### 执行脚本

```bash
# 安装库
$ pip install tavily-python==0.3.5
```

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

class SimpleSearchToolArgs(BaseModel):
    query: str = Field(..., title="Query string")

class SimpleSearchTool(BaseTool):
    name = "simple_search"
    description = "A simple search tool"
    args_schema: Type[BaseModel] = SimpleSearchToolArgs

    def _run(self, query: str):
        """
        Run the search tool
        """
        from tavily import TavilyClient

        client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        results = client.search(query)
        return results
        # return f"search results for {query}\n\n{results}\n"

tools = [SimpleSearchTool()]

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
response = agent_executor.invoke({"input": "我想找一些Python的工作"})
# response = agent_executor.invoke({"input": "今天东京的天气如何？"})
# response = agent_executor.invoke({"input": "1+1=?"})
print(response["output"])

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

