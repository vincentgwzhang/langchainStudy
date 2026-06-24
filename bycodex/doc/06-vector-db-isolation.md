# 06. Vector DB Isolation

## Why Your POC Does Not Show This

中文：你的 POC 用 `db/sanguo.db` 和 `db/sanguo_meta.db` 做本地持久化。它是单用户、单数据集、单 embedding model，所以不需要显式讲 collection、namespace、table。

English: Your POC uses `db/sanguo.db` and `db/sanguo_meta.db` for local persistence. It is single-user, single-dataset, and single-embedding-model, so it does not need to explicitly discuss collection, namespace, or table.

## Enterprise Rule

中文：不同 embedding model、不同维度、不同租户、不同业务域，默认应该隔离。

English: Different embedding models, dimensions, tenants, and business domains should be isolated by default.

## Chroma Pattern

```python
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

vector_store = Chroma(
    collection_name="tenant001_policy_v2_openai_te3large_3072",
    embedding_function=embeddings,
    persist_directory="./chroma_prod",
)
```

## Cloud Pattern

```python
vector_store = Chroma(
    collection_name="policy_docs_v2",
    embedding_function=embeddings,
    chroma_cloud_api_key=os.getenv("CHROMA_API_KEY"),
    tenant=os.getenv("CHROMA_TENANT"),
    database=os.getenv("CHROMA_DATABASE"),
)
```

## Naming Convention

中文：collection 名字应该能直接看出数据域、版本、模型和维度。

English: The collection name should reveal the data domain, version, model, and dimension.

Example:

```text
{tenant}_{domain}_{schema_version}_{embedding_model}_{dimension}
acme_policy_v2_te3large_3072
acme_policy_v3_te3small_1536
```

## Collection / Namespace / Table

中文：不同数据库叫法不同，但目的类似：隔离搜索空间。

English: Different vector databases use different terms, but the purpose is similar: isolate the search space.

| Product | Common Isolation Unit |
|---|---|
| Chroma | collection, tenant, database |
| Pinecone | index, namespace |
| Qdrant | collection |
| Milvus | collection, partition |
| Weaviate | collection |
| pgvector | table, schema, tenant_id filter |
| Elasticsearch / OpenSearch | index |

## A/B Testing

中文：更换 embedding model 时，不要把新旧向量混在一起。建立 parallel index 或 parallel collection。

English: When changing embedding models, do not mix old and new vectors. Build a parallel index or parallel collection.

```text
old query -> old embedding model -> old collection -> old result
new query -> new embedding model -> new collection -> new result
```

## Metadata Filter Is Not Enough

中文：如果同一个 table 里混放不同模型向量，即使用 metadata filter 过滤，也要保证查询时永远不会漏掉过滤条件。更稳妥的做法是物理隔离或至少强制封装检索 API。

English: If vectors from different models are mixed in one table, metadata filtering only works if the filter is never forgotten. A safer approach is physical isolation or a strongly wrapped retrieval API.
