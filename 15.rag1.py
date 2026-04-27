import pprint
import os, time
from common import *
from dotenv import load_dotenv

from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

start_time = time.time()  # 获取开始时间
load_dotenv()

sanguo_txt = os.path.join(os.path.dirname(__file__), "data/sanguo.txt")
chroma_dbpath = os.path.join(os.path.dirname(__file__), "db/sanguo.db")

if os.path.exists(chroma_dbpath):
    empty_folder(chroma_dbpath)

if not os.path.exists(sanguo_txt):
    print(f"Text file not found at {sanguo_txt}")
    exit(0)

# Step 1
################################################################################################
loader = TextLoader(sanguo_txt)
documents = loader.load()
################################################################################################

# Step 2
################################################################################################
# text_splitter = CharacterTextSplitter(chunk_size=1024, chunk_overlap=128)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=128)
docs = text_splitter.split_documents(documents)
################################################################################################

# Step 3
################################################################################################
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
db = Chroma.from_documents(docs, embeddings, persist_directory=chroma_dbpath)
################################################################################################

# Step output
print(">", "Chroma 向量存储创建完成")
print(">", f"Chroma 向量存储路径: {chroma_dbpath}")
print(">", f"Chroma 向量存储文档数: {len(docs)}")
print(">", f"Chroma 向量存储文档长度: {len(db)}")

# 打印结束时间
print(evalEndTime(start_time))