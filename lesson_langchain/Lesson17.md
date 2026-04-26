---
marp: true
theme: default
header: 'LangChain AI开发课程'
footer: '小马技术'
style: |
  header {
    color: #00ced1;
    font-weight: bold;
  }
  footer {
    color: #50fa7b;
    font-weight: bold;
  }
  h1 {
    color: #f8f8f2;
    font-size: 64px;
  }
  section {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    background-color: #1d3d3c;
    color: #f8f8f2;
    font-size: 24px;
    font-family: Yuanti SC;
  }
  a {
    color: #8be9fd;
  }
  img {
    background-color: transparent!important;
  }

---
<style scoped>
  section {
    align-items: center;
    justify-content: center;
  }
  h1 {
    color: #f8f8f2;
    font-size: 120px;
  }
</style>

![width:300px drop-shadow:0,5px,10px,rgba(f,f,f,.4)](./images/langchain.png)

# LangChain

---
<style scoped>
  section {
    font-size: 40px;
  }
  h1 {
    font-size: 50px;
    color: #f8f8f2;
  }
  li {
    font-family: Menlo;
    font-size: 32px;
  }
</style>

# :books: 从多个文本建立向量数据库

操作步骤

+ 读取多个文本文件
+ 为每个文档加入meta信息

---
<style scoped>
  h1 {
    font-size: 64px;
    color: #f8f8f2;
    margin: 0;
  }
  section {
    align-items: center;
    justify-content: center;
  }
  img {
    border-radius: 2%;
    margin: 0;
    border: 5px solid #f8f8f2;
  }
</style>

# 系统架构

![width:800px](./images/RAG.png)

---
<style scoped>
  section {
    align-items: center;
    justify-content: center;
  }
  h1 {
    color: #f8f8f2;
    font-size: 200px;
    margin: 0;
  }
  img {
    border: 10px solid #f8f8f2;
    border-radius: 20%;
    margin: 0;
  }
</style>

![width:200px](./images/step-by-step-operation.webp)

# 操作演示

---
<style scoped>
  h3 {
    margin-top: 0;
  }
</style>
### main.py

```python
import os, time
from common import *
from dotenv import load_dotenv

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
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
print(">", f"Chroma 向量存储文档长度: {len(db)}")

# 打印结束时间
print(evalEndTime(start_time))
```

---
<style scoped>
  section {
    align-items: center;
    justify-content: center;
  }
  h1 {
    color: #f8f8f2;
    font-size: 200px;
  }
</style>

# 下课时间

