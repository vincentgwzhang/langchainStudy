from pathlib import Path
import time
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.documents import Document
from langchain_text_splitters import CharacterTextSplitter

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
CharacterTextSplitter
按照指定的分隔符（separator）切割文本，然后再按 chunk_size 拼接成块。

'''

sanguo_txt = Path(__file__).parent / "data/sanguo.txt"
text = sanguo_txt.read_text(encoding="utf-8")
documents = [Document(page_content=text, metadata={"source": str(sanguo_txt)})]


'''
separator="\n\n" 表示优先按“空行”切，也就是按段落切。你的 sanguo.txt 正好有很多空行，所以很适合。
每个 chunk 目标最大长度大约 500 个字符。
相邻 chunk 之间保留 50 个字符重叠
'''
text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=500,
    chunk_overlap=50,
)

docs: list[Document]= text_splitter.split_documents(documents)

print("原始文档数量:", len(documents))
print("切分后 chunk 数量:", len(docs))

for i, doc in enumerate(docs[:3]):
    print("=" * 50)
    print("chunk:", i)
    print("长度:", len(doc.page_content))
    print("来源:", doc.metadata["source"])
    print(doc.page_content)