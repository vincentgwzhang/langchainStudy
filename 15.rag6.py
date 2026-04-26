import os
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_classic.schema import Document, PromptValue
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

# DB init
db = Chroma(
    persist_directory="./db/sanguo.db",
    embedding_function=OpenAIEmbeddings(model="text-embedding-3-small")
)

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

retriever = db.as_retriever(search_kwargs={"k": 2})

prompt: PromptValue = ChatPromptTemplate.from_messages([
    ("system", "请根据参考文档回答问题，不知道就说不知道。\n\n{context}"),
    MessagesPlaceholder("chat_history"),   # ← 关键
    ("human", "{input}")
])

# init history
chat_history = []
while True:
    query = input("你: ")
    if query == "exit":
        break

    # retrieve from DB, and build context, 此时和LLM无关
    docs: list[Document] = retriever.invoke(query)
    context = "\n".join([d.page_content for d in docs])

    # build up the whole message
    messages = prompt.invoke({
        "input": query,
        "context": context,
        "chat_history": chat_history
    })

    # invoke LLM
    response = model.invoke(messages)

    print("AI:", response.content)

    # Append to chat_history
    chat_history.append(HumanMessage(query))
    chat_history.append(AIMessage(response.content))