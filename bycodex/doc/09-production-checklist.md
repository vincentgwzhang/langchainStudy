# 09. Production Checklist

## Model Layer

- 中文：模型 ID 通过配置管理，不散落在代码里。
- English: Model IDs are managed by configuration, not scattered through code.

- 中文：设置 timeout、retry、temperature、token budget。
- English: Configure timeout, retry, temperature, and token budget.

## Ingestion Layer

- 中文：ingestion job 幂等，可重试，可恢复。
- English: Ingestion jobs are idempotent, retryable, and recoverable.

- 中文：每个 chunk 有稳定 ID 和完整 metadata。
- English: Every chunk has a stable ID and complete metadata.

## Vector DB Layer

- 中文：显式使用 collection / namespace / table。
- English: Use collection / namespace / table explicitly.

- 中文：不同 embedding model 版本使用不同搜索空间。
- English: Different embedding model versions use different search spaces.

- 中文：metadata filter 包含 tenant、ACL、source_version。
- English: Metadata filters include tenant, ACL, and source_version.

## Retrieval Layer

- 中文：评估 Recall@K、MRR、nDCG、答案准确率。
- English: Evaluate Recall@K, MRR, nDCG, and answer accuracy.

- 中文：必要时使用 hybrid search 和 rerank。
- English: Use hybrid search and reranking when needed.

## Generation Layer

- 中文：答案必须 grounded，不知道就说不知道。
- English: Answers must be grounded; if unknown, say unknown.

- 中文：输出结构化，并带 citations。
- English: Output should be structured and include citations.

## Observability

- 中文：记录 query、retrieved doc IDs、scores、prompt version、model version、latency、cost。
- English: Log query, retrieved document IDs, scores, prompt version, model version, latency, and cost.

## Migration

- 中文：更换 embedding model 时建立 parallel collection，不直接覆盖旧索引。
- English: When changing embedding models, build a parallel collection and do not overwrite the old index directly.

- 中文：先 shadow traffic，再 A/B test，最后逐步切流量。
- English: Use shadow traffic first, then A/B testing, then gradual rollout.

- 中文：保留 rollback 路径。
- English: Keep a rollback path.
