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
3. Hybrid Search
4. Reranker
'''

'''
OpenAI Embeddings 基础例子

Embedding 的作用：
把文本转成一串数字向量，后续可以放进 Chroma / FAISS / Milvus / pgvector 等向量库。

注意：
1. OpenAIEmbeddings 会调用 OpenAI embedding API。
2. 它不是 ChatOpenAI，不会生成回答，只会返回向量。
3. 它仍然需要 OPENAI_API_KEY，也会按 embedding 输入 token 产生费用。
4. embed_query 用于把“用户问题”转成向量。
5. embed_documents 用于把“文档 chunks”批量转成向量。
'''

'''
常见的外部 Embedding API 服务：

1. OpenAI Embeddings
   - 直接调用 OpenAI API。
   - 接入简单，效果稳定，适合快速开发和原型验证。
   - 需要 OPENAI_API_KEY，会按输入 token 计费。

2. Azure OpenAI Embeddings
   - 通过 Azure 调用 OpenAI embedding 模型。
   - 企业权限、合规、网络、安全策略更容易和 Azure 体系结合。
   - 适合已经使用 Azure 的公司。

3. Cohere Embeddings
   - Cohere 提供的 embedding API。
   - 企业搜索、rerank、RAG 场景支持比较完整。
   - 常和 Cohere Rerank 一起使用。

4. Voyage Embeddings
   - Voyage AI 提供的 embedding API。
   - 常用于高质量检索、RAG、代码或领域文档检索。
   - 需要单独的 Voyage API key。

5. AWS Bedrock Embeddings
   - 通过 AWS Bedrock 调用 embedding 模型。
   - 适合已经在 AWS 上部署系统的企业。
   - 权限、日志、网络、安全可以走 AWS 体系。

6. Google Vertex AI Embeddings
   - 通过 Google Cloud Vertex AI 调用 embedding 模型。
   - 适合使用 GCP 的企业。
   - 常和 BigQuery、Vertex AI Search 等服务结合。

如何衡量 Embedding 服务：

1. 检索效果：相似问题能不能找回正确 chunk。
2. 中文效果：中文、英文、中英混合文本是否表现稳定。
3. 成本：每 1K / 1M tokens 的 embedding 价格。
4. 速度：批量 embedding 和查询 embedding 的延迟。
5. 向量维度：维度越高不一定越好，但会影响存储成本和检索速度。
6. 上下文长度：单次能 embedding 多长的文本。
7. 稳定性：API 限流、失败率、可用区、SLA。
8. 合规安全：数据是否能出境，是否满足公司安全要求。
9. 生态集成：是否容易接入 LangChain、Chroma、Milvus、pgvector、Elastic 等。
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

# text-embedding-3-small 是你之前 RAG demo 里用过的模型。
# 它属于 API dense embedding：效果稳定，接入简单，但会调用外部 API。
# 把文本发送到 OpenAI 的 embedding 服务, OpenAI 返回向量, 按照输入 token 计费
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

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
