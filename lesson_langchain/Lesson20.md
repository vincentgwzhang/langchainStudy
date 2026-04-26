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

# :books: 使用历史记录生成问题回答(RAG)

操作步骤

+ 使用 LLM 历史记录生成问题 RAG 回答

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
    border: 5px solid #f8f8f2;
  }
</style>

# 系统架构

![width:800px](./images/RAG.png)

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
import os, time
from common import *
from dotenv import load_dotenv

from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain

print("=" * 100)

# 定义client_prompt
client_prompt = "请问桃园结义是几个人？都是谁？"
# client_prompt = "虎牢关是谁打败了吕布？"
# client_prompt = "虎牢关是小马打败了吕布吗？"
# client_prompt = "小马和刘备是一个人吗？"
# client_prompt = "小马三顾茅庐请出的人是谁？"
# client_prompt = "我刚才问了哪些问题？"

start_time = time.time()  # 获取开始时间
load_dotenv()

chroma_dbpath = os.path.join(os.path.dirname(__file__), "db/sanguo.db")

if not os.path.exists(chroma_dbpath):
    print(">", f"未找到存储路径:{chroma_dbpath}")
    exit(0)

# 定义OpenAIEmbeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# 定义Chroma
db = Chroma(persist_directory=chroma_dbpath, embedding_function=embeddings)

# 定义ChatOpenAI
model = ChatOpenAI(model="gpt-4o", temperature=1.0, max_tokens=512)

####################################################################################################
# 定义retriever
# - https://python.langchain.com/v0.2/docs/integrations/vectorstores/chroma/
retriever = db.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 2},
)

# 定义一个问题上下文化的系统提示
contextualize_q_system_prompt = (
    "请根据`参考文档`回答问题，如果在这个参考文档中没有找到答案，请回答“不知道”。"
)
# 定义一个问题上下文化的提示模板
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
# 创建一个具有历史意识的检索器
history_aware_retriever = create_history_aware_retriever(
    model, retriever, contextualize_q_prompt
)

####################################################################################################
# 定义回答链

# 定义一个系统提示
system_prompt = (
    "请根据`参考文档`回答问题，如果在这个参考文档中没有找到答案，请回答“不知道”。"
    "\n\n"
    "{context}"
)

# 定义一个提示模板
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

# 创建一个问题回答的链条
question_answer_chain = create_stuff_documents_chain(model, prompt)

####################################################################################################
# 创建一个检索链条
rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

# 对话循环
chat_history = []  # Collect chat history here (a sequence of messages)
while True:
    query = input(": ")
    if query.lower() == "exit":
        break
    print("\r> 正在检索答案...", end="")

    # 使用rag_chain来获取问题的答案
    result = rag_chain.invoke({"input": query, "chat_history": chat_history})

    # 打印AI的回答
    print("\r>", f"{result['answer']}")

    # 将用户的问题和AI的回答添加到聊天历史中
    chat_history.append(HumanMessage(content=query))
    chat_history.append(SystemMessage(content=result["answer"]))

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

