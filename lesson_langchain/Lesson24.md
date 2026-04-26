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

# :books: 使用 ReAct 完成聊天机器人

操作步骤

+ 建立有历史记忆的 ReAct 思考的机器人

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

1. 今天的日期是？
1. 给我介绍一下微软公司？
1. 苹果公司
1. 桃园结义是几个人？
1. 我问了哪些问题？

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
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import Tool, StructuredTool
from langchain_openai import ChatOpenAI

# from pydantic import BaseModel, Field
from langchain.pydantic_v1 import BaseModel, Field


# 定义输入参数模式
class WikipediaSearchSchema(BaseModel):
    query: str = Field(..., description="要搜索的维基百科主题")


print("=" * 100)


start_time = time.time()  # 获取开始时间
load_dotenv()


# 取得当前日期
def get_date(*args, **kwargs):
    import datetime

    now = datetime.datetime.now()
    return "日期是：" + now.strftime("%Y-%m-%d")


def search_wikipedia(query):
    import wikipedia

    try:
        wikipedia.set_lang("zh")
        return wikipedia.summary(query, sentences=2)
    except:
        return "没有找到相关信息"


tools = [
    StructuredTool.from_function(
        get_date,
        name="当前日期",
        description="不需要传递任何参数，就可以获取当前日期",
        return_direct=True,
    ),
    StructuredTool.from_function(
        search_wikipedia,
        name="Wikipedia",
        description="当需要专题信息时很有用，可以从维基百科中获取信息",
        args_schema=WikipediaSearchSchema,
        return_direct=True,
    ),
]

# https://smith.langchain.com/hub/hwchase17/structured-chat-agent
prompt = hub.pull("hwchase17/structured-chat-agent")
# prompt.pretty_print()

# 初始化大语言模型
llm = ChatOpenAI(model="gpt-4o", temperature=1)

# 创建一个带有对话缓冲记忆的结构化聊天代理
# 对话缓冲记忆存储对话历史记录，使代理能够在互动中保持上下文。
memory = ConversationBufferMemory(
    memory_key="chat_history",
    max_buffer_size=5,
    max_message_length=100,
    max_message_count=100,
    return_messages=True,
)

# create_structured_chat_agent 初始化一个设计用结构化提示和工具进行互动的聊天代理
# 它结合了语言模型 (llm)、工具和提示来创建一个交互式代理
agent = create_structured_chat_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
    stop_sequence=True,
)

# AgentExecutor 负责管理用户输入、代理和工具之间的互动
# 它还处理记忆以确保在整个对话过程中保持上下文
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True,
)

# 初始系统消息用于设定聊天的上下文
# SystemMessage 用于定义系统给代理的消息，设定初始指示或上下文
initial_message = """你是一个AI助手，可以使用可用的工具提供有用的答案。如果你无法回答，可以使用以下工具： 当前日期 和 Wikipedia """
memory.chat_memory.add_message(SystemMessage(content=initial_message))

while True:
    user_input = input(": ")
    if user_input.lower() == "exit":
        break
    elif len(user_input.strip()) == 0:
        continue

    memory.chat_memory.add_message(HumanMessage(content=user_input))

    response = agent_executor.invoke(
        {
            "input": user_input,
        }
    )
    answer = response["output"]
    print(">", answer)

    memory.chat_memory.add_message(AIMessage(content=answer))

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

