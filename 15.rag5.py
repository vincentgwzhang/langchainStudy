import os, time
from common import *
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

print("=" * 100)

# 定义client_prompt
client_prompt = "请问桃园结义是几个人？都是谁？"
# client_prompt = "虎牢关是小马打败了吕布吗？"
# client_prompt = "小马和刘备是一个人吗？"
# client_prompt = "小马三顾茅庐请出的人是谁？"

start_time = time.time()  # 获取开始时间
load_dotenv()

chroma_dbpath = os.path.join(os.path.dirname(__file__), "db/sanguo.db")

if not os.path.exists(chroma_dbpath):
    print(">", f"未找到存储路径:{chroma_dbpath}")
    exit(0)

# 定义OpenAIEmbeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# 定义Chroma
db = Chroma(persist_directory=chroma_dbpath, embedding_function=embeddings)


# MMR (Maximal Marginal Relevance)：解决“复读机”问题
'''
我不要 5 条长得几乎一模一样的结果，我要 5 条既相关又互补的结果。”
fetch_k=50：检索器先一口气从库里抓出 50 条最相关的候选。
k=5：然后在这 50 条里进行“内部竞争”，挑选出 5 条语义覆盖面最广的结果。

retriever = db.as_retriever(
    search_type="mmr",
    search_kwargs={'k': 5, 'fetch_k': 50}
)
'''

'''
Similarity Score Threshold：解决“强行凑数”问题
score_threshold=0.8：这就像是一个及格线

retriever = db.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={'score_threshold': 0.8}
)
'''

retriever = db.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3},
)
retriever_docs = retriever.invoke(client_prompt)

print(">", "查询文档:", len(retriever_docs))
# for i, doc in enumerate(retriever_docs):
#     print(f"{i+1}. {doc.page_content}")

if len(retriever_docs) == 0:
    print(">", "未找到相关文档")
    exit(0)

human_prompt = """请根据提供的`参考文档`回答问题。

### 任务要求
1. 提取文档中的相关事实。
2. 基于事实进行逻辑推理。
3. 给出最终结论。
4. 如果文档中没提到，直接回答“不知道”。

---

### 参考文档
\"\"\"
{reference_docs}
\"\"\"

### 待处理问题
{client_prompt}

### 请按以下格式回答：
【事实分析】：(列出文档中提到的关键信息)
【逻辑推理】：(说明这些信息如何指向答案)
【最终结论】：(一句话总结答案)
""".format(
    client_prompt=client_prompt,
    reference_docs="\n".join([doc.page_content for doc in retriever_docs]),
)
# print(human_prompt)

messages = [
    SystemMessage(
        "请严格按照提供的参考文档回答用户的问题, 不要引用参考文档之外的内容。"
    ),
    HumanMessage(human_prompt),
]

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

result = model.invoke(messages)
print(result.content)

# 打印结束时间
print(evalEndTime(start_time))