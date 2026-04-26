import os, time
from common import *
from dotenv import load_dotenv

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

print("=" * 100)

# 定义client_prompt
client_prompt = "请问桃园结义是几个人？都是谁？"
# client_prompt = "虎牢关是小马打败了吕布吗？"
# client_prompt = "小马和刘备是一个人吗？"
# client_prompt = "小马三顾茅庐请出的人是谁？"

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

# 定义retriever
# - https://python.langchain.com/v0.2/docs/integrations/vectorstores/chroma/
# retriever_docs = db.similarity_search_with_score(client_prompt)
retriever = db.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 1},
)
retriever_docs = retriever.invoke(client_prompt)

print(">", "查询文档:", len(retriever_docs))
# for i, doc in enumerate(retriever_docs):
#     print(f"{i+1}. {doc.page_content}")

if len(retriever_docs) == 0:
    print(">", "未找到相关文档")
    exit(0)

human_prompt = """请根据提供的`参考文档`回答下面的问题:

问题:{client_prompt}

参考文档:
\"\"\"
{reference_docs}
\"\"\"

请根据`参考文档`回答问题，如果在这个参考文档中没有找到答案，请回答“不知道”。
""".format(
    client_prompt=client_prompt,
    reference_docs="\n".join([doc.page_content for doc in retriever_docs]),
)
# print(human_prompt)

messages = [
    SystemMessage(
        "请严格按照提供的参考文档回答用户的问题, 不要引用参考文档之外的内容。"
    ),
    HumanMessage(human_prompt),
]

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

result = model.invoke(messages)
print(result.content)

# 打印结束时间
print(evalEndTime(start_time))