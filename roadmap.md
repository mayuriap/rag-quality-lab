# Roadmap – RAG Quality Lab (Northbridge Bank Assistant)

## Story
Northbridge Bank (fictional) wants an AI assistant answering customer questions
from policy documents and a product database. As the quality engineer, I build
the evidence that it is safe to release, and the gate that blocks it if not.

## Architecture decisions
- Sources: 3 policy documents (data/raw) + SQLite product DB (products, fees)
- Expired rates filtered at source by effective_from / effective_to
- Own loaders and embeddings wrapper (langchain-community is deprecated)
- Chroma vector store (pgvector migration planned as v1.x)
- Local embeddings: FastEmbed BAAI/bge-small-en-v1.5
- LLM: Claude Haiku via Anthropic API (Bedrock switch planned)

## Day 1 – System under test (v0.1)
- [x] Environment, folders, .gitignore, requirements
- [x] Policy documents + product database
- [x] loaders.py (extract + transform, effective dating)
- [x] ingest.py (chunk, embed, store) – 14 chunks
- [x] search.py (retrieval tested on its own)
- [ ] Claude API key + connection check
- [ ] rag.py (answer from retrieved chunks)
- [ ] api.py (FastAPI /ask)
- [ ] Push v0.1 to GitHub

## Findings from exploratory testing (become automated tests)
- DEFECT: empty source document produced 0 chunks with no error (silent data loss)
- Expired rate (SAV-EASY-01, 2.85%) correctly excluded
- Search always returns results, even for out-of-scope questions -> LLM must refuse
- Good and bad match distances overlap -> no fixed similarity threshold

## Day 2 – Data quality + golden dataset (v0.2)
- [ ] Completeness: every source produces at least 1 chunk
- [ ] Reconciliation: active DB products = product chunks in vector store
- [ ] Freshness: vector store built after last DB update
- [ ] Effective dating test (as_of date)
- [ ] Chunk quality: no empty / tiny / duplicate chunks
- [ ] Golden dataset: ~40 questions (factual, numeric, out-of-scope, ambiguous)

## Day 3 – Evaluation framework (v0.3)
- [ ] ** Retrieval metrics: precision@k, recall@k, MRR ** (priority)
- [ ] LLM metrics: faithfulness, answer relevancy, context precision (RAGAS / DeepEval)
- [ ] Eval report with pass/fail thresholds

## Day 4 – Functional, safety, resilience tests (v0.4)
- [ ] pytest API tests (schema, errors, sources present, latency)
- [ ] Postman collection + Newman
- [ ] Red-teaming: prompt injection, PII, financial advice, hallucination traps
- [ ] Bias tests
- [ ] Consistency: same question 5 times
- [ ] Resilience with mocks: timeout, 429 retry/backoff, provider down fallback

## Day 5 – Release gate + strategy (v1.0)
- [ ] GitHub Actions: tests + evals, fail below thresholds
- [ ] Prompt / model regression comparison
- [ ] TEST_STRATEGY.md incl. ** Responsible AI section ** (priority)
- [ ] Quality scorecard: accuracy, relevance, safety, consistency, latency
- [ ] README with results

## After MVP (v1.x)
- v1.1 AWS Bedrock provider switch (cloud AI platform)
- v1.2 Model card + AI risk register (EU AI Act, NIST AI RMF)
- v1.3 LangGraph agent + agent tests
- v1.4 Streamlit UI + Playwright
- v1.5 Locust performance test
- v1.6 Langfuse monitoring + alerting
- v1.7 Eval harness as reusable CLI
- v1.8 pgvector migration with eval regression gate