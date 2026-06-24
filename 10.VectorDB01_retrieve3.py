from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

'''
这个文件不能独立运行。

前提：
必须先运行 10.VectorDB01_save.py。

原因：
10.VectorDB01_save.py 负责：
1. reading
2. chunking
3. embedding
4. 把带有 role metadata 的 chunks 保存到 ChromaDB

这个文件只负责：
1. 连接已经存在的 ChromaDB
2. 对用户 query 做 embedding
3. 从 ChromaDB retrieve role=user 的相关 chunks
'''

chroma_dbpath = Path(__file__).parent / "db/chroma_sanguo_demo01"

# 查询时仍然需要同一个 embedding model。
# 因为 query 也要先转成 vector，才能和 DB 里的 chunk vectors 做相似度比较。
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# 这里不会重新写入 documents。
# 它只是连接 10.VectorDB01.py 已经创建好的本地 ChromaDB。
db = Chroma(
    persist_directory=str(chroma_dbpath),
    embedding_function=embeddings,
    collection_name="sanguo_demo",
)

query = "请问桃园结义是几个人？都是谁？"

# Strategy 2: mmr
# Maximal Marginal Relevance：
# 先取 fetch_k 条候选，再选出 k 条既相关、又尽量不重复的结果。
retriever = db.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 2, "fetch_k": 4, "filter": {"role": "user"}},
)
results = retriever.invoke(query)

print("策略: mmr")
print("返回结果数量:", len(results))

for index, doc in enumerate(results):
    print("*" * 100)
    print("result:", index)
    print("source:", doc.metadata.get("source"))
    print("role:", doc.metadata.get("role"))
    print("字符长度:", len(doc.page_content))
    print(doc.page_content)
