import os, time
from common import *
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

print("=" * 100)
start_time = time.time()  # 获取开始时间
load_dotenv()

chroma_dbpath = os.path.join(os.path.dirname(__file__), "db/sanguo_meta.db")

if not os.path.exists(chroma_dbpath):
    print(">", f"未找到存储路径:{chroma_dbpath}")
    exit(0)

# 定义OpenAIEmbeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# 定义Chroma
db = Chroma(persist_directory=chroma_dbpath, embedding_function=embeddings)

# 定义client_prompt
client_prompt = "请问桃园结义是几个人？都是谁？"

# 定义retriever
# - https://python.langchain.com/v0.2/docs/integrations/vectorstores/chroma/
retriever_docs = db.similarity_search(client_prompt, k=2)

print(">", "查询文档:", len(retriever_docs))
for i, doc in enumerate(retriever_docs):
    print(f"{i+1}. {doc}")

# 打印结束时间
print(evalEndTime(start_time))