from pathlib import Path
import time

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

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
RecursiveCharacterTextSplitter
递归字符切分器：
它不是只用一个 separator 切文本，而是按 separators 列表从大到小尝试。
如果用 "\n\n" 切出来的块还是太大，就继续尝试 "\n"。
如果还太大，就继续尝试中文句号、逗号、空格，最后才按单个字符硬切。
'''

sanguo_txt = Path(__file__).parent / "data/sanguo.txt"
text = sanguo_txt.read_text(encoding="utf-8")
documents = [Document(page_content=text, metadata={"source": str(sanguo_txt)})]


# separators 的顺序很重要：越靠前，越优先保留更大的语义结构。
# 对中文文本，可以把中文标点也放进去，避免最后退化成按字符硬切。
text_splitter = RecursiveCharacterTextSplitter(
    separators=[
        "\n\n",  # 空行：优先按段落切
        "\n",   # 换行：段落太长时再按行切
        "。",   # 中文句号：行仍太长时按句子切
        "，",   # 中文逗号：句子仍太长时按短语切
        " ",    # 英文空格：兼容中英混合文本
        "",     # 最后兜底：按字符切
    ],
    chunk_size=500,      # 每个 chunk 的目标最大字符数
    chunk_overlap=50,    # 相邻 chunk 保留一点重叠，避免上下文断裂
    length_function=len, # 用 Python 的 len() 计算长度，也就是按字符数计算
)

docs: list[Document] = text_splitter.split_documents(documents)

print("原始文档数量:", len(documents))
print("切分后 chunk 数量:", len(docs))

for i, doc in enumerate(docs[:5]):
    print("=" * 50)
    print("chunk:", i)
    print("长度:", len(doc.page_content))
    print("来源:", doc.metadata["source"])
    print(doc.page_content)