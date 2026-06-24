from pathlib import Path
import chromadb
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

#######################################################################
'''
第一阶段: Chroma
最简单，和 LangChain 配合舒服，适合你现在继续学。
'''
#######################################################################

chroma_dbpath = Path(__file__).parent / "db/chroma_sanguo_demo01"
collection_name = "sanguo_demo"

# Step 0, clear old collection
# 这样这个脚本可以重复运行，不会因为旧数据还在而越写越多。
client = chromadb.PersistentClient(path=str(chroma_dbpath))
existing_collections = [collection.name for collection in client.list_collections()]
if collection_name in existing_collections:
    client.delete_collection(name=collection_name)
    print("已清空旧 collection:", collection_name)

# Step 1, loading
sanguo_txt = Path(__file__).parent / "data/sanguo.txt"
text = sanguo_txt.read_text(encoding="utf-8")
documents_user = [Document(page_content=text, metadata={"source": str(sanguo_txt), "role": "user"})]
documents_admin = [Document(page_content=text, metadata={"source": str(sanguo_txt), "role": "admin"})]
documents = documents_user + documents_admin

# Steo 2: Chunking
text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=500,
    chunk_overlap=50,
)
docs: list[Document] = text_splitter.split_documents(documents)
sample_docs: list[Document]= docs
sample_texts : list[str] = [doc.page_content for doc in sample_docs]

# Step 3: Embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
query = "请问桃园结义是几个人？都是谁？"
query_vector: list[float] = embeddings.embed_query(query)

document_vectors : list[list[float]]= embeddings.embed_documents(sample_texts)

############################################################
# Step 4, load into ChromaDB

# Chroma.from_documents 会自动做：
# 1. 从 Document 里取 page_content
# 2. 调用 embeddings.embed_documents(...)
# 3. 保存 text + metadata + vector 到本地 ChromaDB
db = Chroma.from_documents(
    documents=sample_docs,
    embedding=embeddings,
    persist_directory=str(chroma_dbpath),
    collection_name=collection_name,
)

print("ChromaDB 保存路径:", chroma_dbpath)
print("写入 Document 数量:", len(sample_docs))
print("ChromaDB 当前数量:", db._collection.count())
