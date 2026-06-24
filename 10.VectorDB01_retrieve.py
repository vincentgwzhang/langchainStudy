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

'''
此处是关于
10.VectorDB01_retrieve.py
10.VectorDB01_retrieve2.py
10.VectorDB01_retrieve3.py
10.VectorDB01_retrieve4.py

4个文件的区别

1. 10.VectorDB01_retrieve.py
   - 使用 db.similarity_search(...)
   - 最直接的 ChromaDB 搜索方式。
   - query 会先被 embedding 成 vector，然后取最相似的 k 条。
   - 适合先理解 vector DB 如何 retrieve。

2. 10.VectorDB01_retrieve2.py
   - 使用 db.as_retriever(search_type="similarity")
   - 本质仍然是普通相似度搜索。
   - 区别是它把 vector DB 包装成 retriever，可以统一用 retriever.invoke(query)。
   - 后面接 RAG chain 时更常用这种方式。

3. 10.VectorDB01_retrieve3.py
   - 使用 db.as_retriever(search_type="mmr")
   - MMR = Maximal Marginal Relevance。
   - 先取 fetch_k 条候选，再从里面选 k 条既相关、又尽量不重复的结果。
   - 适合避免检索结果都来自同一段附近，解决“结果太重复”的问题。

4. 10.VectorDB01_retrieve4.py
   - 使用 db.as_retriever(search_type="similarity_score_threshold")
   - 先做相似度搜索，再只保留分数超过 score_threshold 的结果。
   - 适合避免“强行凑满 k 条”。
   - 如果没有足够相关的 chunk，可以返回 0 条或少于 k 条。

共同点：
   - 都需要同一个 embedding model。
   - 都会把 query 转成 vector。
   - 都可以带 metadata filter，例如 filter={"role": "user"}。
   - 返回结果都是 Document，里面有 page_content 和 metadata。

背后的算法层次：

1. 这四个文件都属于 dense vector search。
   - 它们不是 BM25。
   - 它们不是 hybrid search。
   - 它们都是把 query 和 chunk 变成 embedding vector 后，再比较向量相似度。

2. 底层向量相似度通常是 cosine / dot product / euclidean 这一类。
   - 你现在用的是 Chroma。
   - Chroma 底层会用向量索引做近似最近邻搜索，也就是 ANN。
   - ANN = Approximate Nearest Neighbor，用来在大量 vectors 里快速找相近的。

3. similarity 和 similarity_search 是最基础的 vector similarity search。
   - 算法思想：谁和 query vector 最像，就返回谁。
   - 它只关心相关性，不关心结果之间是否重复。

4. mmr 不是新的 embedding 算法，也不是新的 vector DB 算法。
   - 它是搜索结果重排策略。
   - 先用 vector similarity 找一批候选。
   - 再从候选里挑既相关、又彼此不太重复的结果。

5. similarity_score_threshold 也不是新的底层搜索算法。
   - 它仍然先做 vector similarity search。
   - 然后加一道分数门槛。
   - 分数不够高的结果就被过滤掉。

6. metadata filter 也不是向量算法。
   - 它是结构化过滤。
   - 例如 role=user 会先限制可搜索范围，或者在搜索过程中只允许返回符合条件的数据。

7. BM25 是关键词/倒排索引算法。
   - 它看词频、关键词匹配，不依赖 embedding。
   - 适合精确词、编号、专有名词搜索。
   - 这四个文件没有使用 BM25。

8. Hybrid search = dense vector search + sparse/BM25 search。
   - 同时考虑语义相似和关键词匹配。
   - 这四个文件也没有做 hybrid。
   - 企业 RAG 常用 hybrid，但这是下一层知识。

   


Search Strategy
│
├─ Keyword Search
│     └─ BM25
│
├─ Vector Search
│     ├─ Exact KNN
│     └─ ANN
│          ├─ HNSW
│          ├─ IVF
│          ├─ PQ
│          └─ DiskANN
│
└─ Hybrid Search
      ├─ BM25
      └─ ANN(HNSW)

Selection / Re-ranking Strategy
similarity / mmr / similarity_score_threshold

关系：DB 搜索的过程，首先面临的是 Search Strategy ，然后拿到的结果集，会做 Selection / Re-ranking Strategy


| DB            | 支持的 Search Strategy       |
| ------------- | ------------------------- |
| FAISS         | Vector                    |
| Chroma        | Vector                    |
| Qdrant        | Vector / Hybrid           |
| Weaviate      | Vector / Hybrid           |
| Elasticsearch | Keyword / Vector / Hybrid |
| OpenSearch    | Keyword / Vector / Hybrid |

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

# 这里体现权限过滤：
# 当前身份是 user，所以只能取 metadata.role == "user" 的 chunks。
results = db.similarity_search(
    query,
    k=2,
    filter={"role": "user"},
)

for index, doc in enumerate(results):
    print("*" * 100)
    print("result:", index)
    print("source:", doc.metadata.get("source"))
    print("role:", doc.metadata.get("role"))
    print("字符长度:", len(doc.page_content))
    print(doc.page_content)
