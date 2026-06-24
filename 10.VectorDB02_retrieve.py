import os

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, MatchAny, MatchValue

load_dotenv()

'''
这个文件不能独立运行。

前提：
必须先运行 10.VectorDB02_save.py。

原因：
10.VectorDB02_save.py 负责：
1. reading
2. chunking
3. embedding
4. 把带有 role payload 的 points 保存到 Qdrant Cloud

这个文件只负责：
1. 连接已经存在的 Qdrant Cloud collection
2. 对用户 query 做 embedding
3. 从 Qdrant retrieve role=user 的相关 points
'''

qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")

if not qdrant_url or not qdrant_api_key:
    raise ValueError("请先在 .env 里配置 QDRANT_URL 和 QDRANT_API_KEY")

collection_name = "sanguo_demo"

client = QdrantClient(
    url=qdrant_url,
    api_key=qdrant_api_key,
)

# 查询时仍然需要同一个 embedding model。
# 因为 query 也要先转成 vector，才能和 Qdrant 里的 vectors 做相似度比较。
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

query = "请问桃园结义是几个人？都是谁？"
query_vector: list[float] = embeddings.embed_query(query)

# 这里体现权限过滤：
# 当前身份是 user，所以只能取 payload.role == "user" 的 points。
results = client.query_points(
    collection_name=collection_name,
    query=query_vector,
    query_filter=Filter(
        must=[
            FieldCondition(
                key="role",
                # match=MatchValue(value="user"),
                match=MatchAny(any=["user", "admin"]),
            )
        ]
    ),
    with_payload=True,
    limit=2,
)

print("Qdrant URL:", qdrant_url)
print("collection:", collection_name)
print("query:", query)
print("返回结果数量:", len(results.points))

for index, point in enumerate(results.points):
    payload = point.payload or {}
    text = payload.get("text", "")

    print("*" * 100)
    print("result:", index)
    print("score:", point.score)
    print("source:", payload.get("source"))
    print("role:", payload.get("role"))
    print("字符长度:", len(text))
    print(text)
