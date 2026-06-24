import os
from pathlib import Path
from uuid import uuid4

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PayloadSchemaType, PointStruct, VectorParams

load_dotenv()

#######################################################################
'''
第二阶段: Qdrant Cloud

这个文件负责：
1. reading
2. chunking
3. embedding
4. 保存到在线 Qdrant Cloud

需要先在 .env 配置：
QDRANT_URL=https://xxxx.qdrant.io
QDRANT_API_KEY=你的-qdrant-api-key

注意：
1. Qdrant 是 vector DB，负责保存 vector + payload。
2. OpenAIEmbeddings 负责把文本转成 vector。
3. payload 类似 Chroma metadata，用来保存 source / role / text 等信息。
'''
#######################################################################

qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")
collection_name = "sanguo_demo"
client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)

# Step 0, clear old collection
# 这样这个脚本可以重复运行，不会因为旧数据还在而越写越多。
existing_collections = [
    collection.name for collection in client.get_collections().collections
]
if collection_name in existing_collections:
    client.delete_collection(collection_name=collection_name)
    print("已删除旧 collection:", collection_name)

# Step 1, loading
sanguo_txt = Path(__file__).parent / "data/sanguo.txt"
text = sanguo_txt.read_text(encoding="utf-8")

documents_user = [
    Document(
        page_content=text,
        metadata={"source": str(sanguo_txt), "role": "user"},
    )
]
documents_admin = [
    Document(
        page_content=text,
        metadata={"source": str(sanguo_txt), "role": "admin"},
    )
]
documents = documents_user + documents_admin

# Step 2, chunking
text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=500,
    chunk_overlap=50,
)
docs: list[Document] = text_splitter.split_documents(documents)

# Step 3, embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
texts: list[str] = [doc.page_content for doc in docs]
vectors: list[list[float]] = embeddings.embed_documents(texts)

# Step 4, create Qdrant collection
# text-embedding-3-small 的向量维度是 1536。
client.create_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
)

# Step 4.1, create payload index
# Qdrant Cloud 做 payload filter 时，role 这种字段需要建 keyword index。
client.create_payload_index(
    collection_name=collection_name,
    field_name="role",
    field_schema=PayloadSchemaType.KEYWORD,
)

# Step 5, upsert points
# Qdrant 里的一条 point 大概等于：
# id + vector + payload
points = []
for doc, vector in zip(docs, vectors):
    point = PointStruct(
        id=str(uuid4()),
        vector=vector,
        payload={
            "text": doc.page_content,
            "source": doc.metadata.get("source"),
            "role": doc.metadata.get("role"),
        },
    )
    points.append(point)

client.upsert(
    collection_name=collection_name,
    points=points,
)

collection_info = client.get_collection(collection_name=collection_name)

print("Qdrant URL:", qdrant_url)
print("collection:", collection_name)
print("写入 chunks 数量:", len(points))
print("Qdrant points 数量:", collection_info.points_count)
