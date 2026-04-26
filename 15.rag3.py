import os, time
from common import *
from dotenv import load_dotenv

from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

start_time = time.time()  # 获取开始时间
load_dotenv()

sanguo_txt = os.path.join(os.path.dirname(__file__), "data/chapters")
chroma_dbpath = os.path.join(os.path.dirname(__file__), "db/sanguo_meta.db")

if os.path.exists(chroma_dbpath):
    print(f"Chroma DB already exists at {chroma_dbpath}")
    exit(0)

if not os.path.exists(sanguo_txt):
    print(f"Text file not found at {sanguo_txt}")
    exit(0)

sanguo_files = [
    file for file in sorted(os.listdir(sanguo_txt)) if file.endswith(".txt")
]
print(sanguo_files)

documents = []
for file in sanguo_files:
    file_path = os.path.join(sanguo_txt, file)
    loader = TextLoader(file_path)
    sanguo_docs = loader.load()
    print(">", file_path, len(sanguo_docs))
    for doc in sanguo_docs:
        doc.metadata = {
            "Source": file_path,
            "Author": "Luo Guanzhong",
        }
        documents.append(doc)


# Split the text into characters
print(">", "文本分割中...")
text_splitter = CharacterTextSplitter(chunk_size=1024, chunk_overlap=128)
docs = text_splitter.split_documents(documents)

print(">>", f"文本分割为 {len(docs)} 个文档")

# Create embeddings
# - https://platform.openai.com/docs/guides/embeddings
print(">", "创建 OpenAI Embeddings...")
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Create the Chroma vector store
print(">", "创建 Chroma 向量存储...")
db = Chroma.from_documents(docs, embeddings, persist_directory=chroma_dbpath)

print(">", "Chroma 向量存储创建完成")
print(">", f"Chroma 向量存储路径: {chroma_dbpath}")
print(">", f"Chroma 向量存储文档数: {len(docs)}")

# 打印结束时间
print(evalEndTime(start_time))