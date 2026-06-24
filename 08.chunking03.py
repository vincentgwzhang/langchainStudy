from pathlib import Path
import time

from langchain_core.documents import Document
from langchain_text_splitters import TokenTextSplitter

start_time = time.time()  # 获取开始时间

'''
1. CharacterTextSplitter
2. RecursiveCharacterTextSplitter
3. TokenTextSplitter
4. Markdown / HTML / code 专用 splitter
5. Semantic chunking
6. Parent-child retrieval
'''

'''
TokenTextSplitter
TokenTextSplitter 按 token 数切分，而不是按字符数切分。

为什么要学它：
LLM 的上下文窗口、输入限制、计费通常都是按 token 算的。
所以当你想更精确地控制每个 chunk 对模型来说有多大时，就用 token splitter。

注意：
TokenTextSplitter 更关心 token 数，不关心段落、句子这些自然边界。
在中文文本里，它有时会把一个汉字或标点附近切得比较生硬。
'''

sanguo_txt = Path(__file__).parent / "data/sanguo.txt"
text = sanguo_txt.read_text(encoding="utf-8")
documents = [Document(page_content=text, metadata={"source": str(sanguo_txt)})]


# model_name 会决定用哪个 tokenizer 来数 token。
# 这里用 gpt-4o-mini，是为了让切分方式尽量贴近你后面实际调用的模型。
# 第一次运行时，tiktoken 可能需要联网下载 tokenizer 文件；缓存后会快很多。
text_splitter = TokenTextSplitter(
    model_name="gpt-4o-mini",
    chunk_size=300,      # 每个 chunk 的目标最大 token 数
    chunk_overlap=50,    # 相邻 chunk 保留 50 个 token 的重叠
)

docs: list[Document] = text_splitter.split_documents(documents)

print("原始文档数量:", len(documents))
print("切分后 chunk 数量:", len(docs))

# 只用于观察：用同一个 tokenizer 计算每个 chunk 的 token 数。
tokenizer = text_splitter._tokenizer

for i, doc in enumerate(docs[:5]):
    print("=" * 50)
    print("chunk:", i)
    print("字符长度:", len(doc.page_content))
    print("token 数:", len(tokenizer.encode(doc.page_content)))
    print("来源:", doc.metadata["source"])
    print(doc.page_content)

print("=" * 50)
print("程序运行时间：%.2f 秒" % (time.time() - start_time))
