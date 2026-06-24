from collections import Counter
from pathlib import Path
import math
import re
import time

from langchain_core.documents import Document

start_time = time.time()

'''
1. CharacterTextSplitter
2. RecursiveCharacterTextSplitter
3. TokenTextSplitter
4. Markdown / HTML / code 专用 splitter
5. Semantic chunking
6. Parent-child retrieval
'''

'''
Semantic chunking

语义切分不是只看字符数、token 数或固定分隔符。
它的核心想法是：
如果相邻段落内容相近，就放在同一个 chunk；
如果相邻段落内容差异明显，就在这里切开。

生产环境里常见做法：
1. 先把文本切成句子或段落
2. 对每个句子/段落做 embedding
3. 计算相邻片段 embedding 的相似度
4. 在相似度突然降低的位置切分

注意：embedding 版通常会调用 OpenAIEmbeddings 或其他 embedding 服务，会产生 API 调用费用。
这个文件先写一个本地教学版，不调用外部服务，也不花钱。
'''


def split_paragraphs(text: str) -> list[str]:
    """按空行切成段落，并清理掉空白段落。"""
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def char_bigrams(text: str) -> Counter[str]:
    """把文本转成相邻两个字符的特征，用来粗略表示内容。"""
    compact_text = re.sub(r"\s+", "", text)
    return Counter(compact_text[i : i + 2] for i in range(len(compact_text) - 1))


def cosine_similarity(left: Counter[str], right: Counter[str]) -> float:
    """计算两个 Counter 向量的余弦相似度。"""
    common_keys = left.keys() & right.keys()
    dot = sum(left[key] * right[key] for key in common_keys)
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))

    if left_norm == 0 or right_norm == 0:
        return 0.0

    return dot / (left_norm * right_norm)


def semantic_chunk_paragraphs(
    paragraphs: list[str],
    similarity_threshold: float = 0.08,
    max_chars: int = 700,
) -> list[str]:
    """
    教学版 semantic chunking。

    similarity_threshold 越高，越容易切开，chunk 会更碎。
    max_chars 是保护阈值，避免相似段落一直合并导致 chunk 太长。
    """
    if not paragraphs:
        return []

    chunks: list[str] = []
    current_chunk = paragraphs[0]
    previous_vector = char_bigrams(paragraphs[0])

    for paragraph in paragraphs[1:]:
        paragraph_vector = char_bigrams(paragraph)
        similarity = cosine_similarity(previous_vector, paragraph_vector)
        merged_length = len(current_chunk) + len(paragraph)

        should_continue_same_topic = similarity >= similarity_threshold
        is_too_long = merged_length > max_chars

        if should_continue_same_topic and not is_too_long:
            current_chunk = current_chunk + "\n\n" + paragraph
        else:
            chunks.append(current_chunk)
            current_chunk = paragraph

        previous_vector = paragraph_vector

    chunks.append(current_chunk)
    return chunks


sanguo_txt = Path(__file__).parent / "data/sanguo.txt"
text = sanguo_txt.read_text(encoding="utf-8")
paragraphs = split_paragraphs(text)

chunks = semantic_chunk_paragraphs(
    paragraphs,
    similarity_threshold=0.02,
    max_chars=700,
)

docs = [
    Document(
        page_content=chunk,
        metadata={
            "source": str(sanguo_txt),
            "chunk_method": "local_semantic_demo",
            "chunk_index": index,
        },
    )
    for index, chunk in enumerate(chunks)
]

print("原始段落数量:", len(paragraphs))
print("切分后 chunk 数量:", len(docs))

for i, doc in enumerate(docs[:5]):
    print("=" * 50)
    print("chunk:", i)
    print("字符长度:", len(doc.page_content))
    print("来源:", doc.metadata["source"])
    print(doc.page_content)

print("=" * 50)
print("程序运行时间：%.2f 秒" % (time.time() - start_time))
