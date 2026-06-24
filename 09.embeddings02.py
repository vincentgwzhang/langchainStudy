from pathlib import Path
import time

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

start_time = time.time()  # 获取开始时间
load_dotenv()

'''
Embeddings 策略
1. OpenAI / Azure OpenAI Embeddings
2. 本地 / 私有化 Embeddings
'''

'''
本地 / 私有化 Embeddings
1. 这个 demo 默认运行不了，因为本机没有启动 embedding server。
2. 企业常见做法：先在内网部署 embedding 服务，再通过 HTTP 调用。
3. 很多本地 embedding 服务会模拟 OpenAI API，所以代码仍然可以用 OpenAIEmbeddings。
4. 依赖：vLLM / Xinference / TEI / Ollama 等本地模型服务。
5. 示例 endpoint: http://localhost:8000/v1
6. 示例 model: BAAI/bge-m3
'''

sanguo_txt = Path(__file__).parent / "data/sanguo.txt"
text = sanguo_txt.read_text(encoding="utf-8")
documents = [Document(page_content=text, metadata={"source": str(sanguo_txt)})]

# 先切 chunk，再对 chunk 做 embedding。
# chunk 太大：embedding 语义会变得混杂，检索不精准。
# chunk 太小：上下文不足，后续给 LLM 回答时信息可能不完整。
text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=500,
    chunk_overlap=50,
)
docs: list[Document] = text_splitter.split_documents(documents)

# 这是“本地 embedding server”的写法示例。
# 如果 http://localhost:8000/v1 没有真实服务，执行 embed_documents 会报错。
embeddings = OpenAIEmbeddings(
    model="BAAI/bge-m3",
    base_url="http://localhost:8000/v1",
    api_key="EMPTY",
    tiktoken_enabled=False,
    check_embedding_ctx_length=False,
)

# 1. embed_query：通常用于用户输入的问题。
query = "请问桃园结义是几个人？都是谁？"

# 实际上是一句话分成 1536 个float, 不是每个token 1536个 float
# query_vector: list[float] = embeddings.embed_query(query)
# print("查询向量类型:", type(query_vector))
# print("查询向量维度:", len(query_vector))

# 2. embed_documents：通常用于文档 chunks。
# 为了避免学习时一次性产生太多 API 调用，这里只取前 3 个 chunk 演示。
sample_docs: list[Document]= docs[:3]
sample_texts : list[str] = [doc.page_content for doc in sample_docs]
document_vectors : list[list[float]]= embeddings.embed_documents(sample_texts)

# 具体来说，一个 Document 就对应 一个 embedding 出来的 array 的一个元素，元素就是一个list of float
for index, doc in enumerate(sample_docs):
    print('*' * 100)
    vector: list[float] = document_vectors[index]
    print("文本字符长度:", len(doc.page_content))
    print("向量维度:", len(vector))
