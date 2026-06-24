from __future__ import annotations

from collections import Counter
from hashlib import md5
from pathlib import Path
import math
import re
import time

from langchain_classic.retrievers import ParentDocumentRetriever
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.stores import InMemoryStore
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

start_time = time.time()

'''
1. CharacterTextSplitter
2. RecursiveCharacterTextSplitter
3. TokenTextSplitter
4. Markdown / HTML / code 专用 splitter
5. Semantic chunking
6. Parent-child retrieval
'''

'''
Parent-child retrieval

它解决的是 RAG 里的一个矛盾：
1. 检索时，chunk 越小，embedding 越容易精确命中问题。
2. 回答时，chunk 太小，上下文又不够完整。

Parent-child 的做法：
1. parent chunk：大块文本，放到 docstore 里，用来最终返回给 LLM。
2. child chunk：小块文本，放到 vectorstore 里，用来做相似度检索。
3. 查询时先命中 child chunk，再通过 child metadata 里的 parent id 找回 parent chunk。

生产环境里通常会用 OpenAIEmbeddings / BGE / Voyage 等 embedding 模型。
这个文件为了学习流程，使用一个本地 toy embedding，不联网，也不花钱。
'''


class LocalHashEmbeddings(Embeddings):
    """
    一个教学用的本地 embedding。

    它把文本拆成相邻两个字符的 bigram，然后 hash 到固定长度向量里。
    这不是生产级 embedding，但足够展示 vectorstore + retriever 的流程。
    """

    def __init__(self, size: int = 384) -> None:
        self.size = size

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed(text)

    def _embed(self, text: str) -> list[float]:
        vector = [0.0] * self.size
        compact_text = re.sub(r"\s+", "", text)
        features = Counter(
            compact_text[index : index + 2]
            for index in range(max(len(compact_text) - 1, 0))
        )

        for feature, count in features.items():
            bucket = int(md5(feature.encode("utf-8")).hexdigest(), 16) % self.size
            vector[bucket] += float(count)

        norm = math.sqrt(sum(value * value for value in vector))
        if norm == 0:
            return vector

        return [value / norm for value in vector]


sanguo_txt = Path(__file__).parent / "data/sanguo.txt"
text = sanguo_txt.read_text(encoding="utf-8")
documents = [
    Document(
        page_content=text,
        metadata={
            "source": str(sanguo_txt),
            "title": "三国演义",
        },
    )
]

# parent_splitter 切出较大的父块。
# 父块不会直接拿来做向量检索，而是作为最终返回的上下文。
parent_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", "。", "，", " ", ""],
    chunk_size=1000,
    chunk_overlap=100,
    add_start_index=True,
)

# child_splitter 切出较小的子块。
# 子块会进入 vectorstore，用来提高检索精度。
child_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", "。", "，", " ", ""],
    chunk_size=250,
    chunk_overlap=50,
    add_start_index=True,
)

embedding = LocalHashEmbeddings()
vectorstore = InMemoryVectorStore(embedding)
docstore = InMemoryStore()

retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=docstore,
    parent_splitter=parent_splitter,
    child_splitter=child_splitter,
)

# add_documents 会同时做两件事：
# 1. 把 child chunks 写入 vectorstore
# 2. 把 parent chunks 写入 docstore
retriever.add_documents(documents)

query = "桃园结义 三兄弟 张飞 关羽"
results = retriever.invoke(query)

print("原始文档数量:", len(documents))
print("parent chunk 数量:", len(docstore.store))
print("child chunk 数量:", len(vectorstore.store))
print("查询:", query)
print("返回 parent 数量:", len(results))

for i, doc in enumerate(results[:3]):
    print("=" * 50)
    print("parent:", i)
    print("字符长度:", len(doc.page_content))
    print("来源:", doc.metadata["source"])
    print("parent 起始位置:", doc.metadata.get("start_index"))
    print(doc.page_content[:700])

print("=" * 50)
print("程序运行时间：%.2f 秒" % (time.time() - start_time))
