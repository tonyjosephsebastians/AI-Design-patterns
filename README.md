
A practical pattern map:
- **13 Core DSA Patterns** (with sub-patterns)
- **AI/System Design Patterns** (reliability, scalability, RAG/agents, observability)
- Built for **fast recall + repeatable practice**

---

## How to study (simple + effective)
**Per pattern (60–75 min):**
1) Write **template from memory** (10m)  
2) Solve **1 canonical** problem/task (25m)  
3) Solve **1 variation** (20m)  
4) **Teach-back notes** (5m)  
5) Next day: **redo canonical** (10m)

---

# DSA Patterns (13 Core)

| # | Pattern | Triggers (spot it fast) | Sub-patterns | Canonical (start here) | Variations (pick 1) |
|---|---------|--------------------------|--------------|------------------------|---------------------|
| 1 | Two Pointers | sorted, palindrome, pair sum, partition | opposite L/R; same dir; partition; pair in sorted | **Valid Palindrome (125)** | **3Sum (15)** / **Container (11)** |
| 2 | Sliding Window | substring/subarray, longest/shortest, at most/at least | fixed; variable; freq map; constraints | **Longest Substring w/o Repeat (3)** | **Permutation in String (567)** / **Min Window (76)** |
| 3 | Fast/Slow Pointers | cycles, repeated state, linked list middle | cycle detect; entry; middle; happy number | **Linked List Cycle (141)** | **Cycle II (142)** / **Happy Number (202)** |
| 4 | Binary Search | sorted, monotonic, “min/max answer” | classic; left bound; right bound; rotated; answer space | **Binary Search (704)** | **Rotated Search (33)** / **Peak (162)** |
| 5 | Tree DFS | recursion, path, subtree, height | preorder/in/post; top-down; bottom-up; path; tree DP | **Max Depth (104)** | **Validate BST (98)** / **Max Path Sum (124)** |
| 6 | Tree BFS | level order, shortest in tree | level order; zigzag; multi-source; parent pointers | **Level Order (102)** | **Zigzag (103)** / **Distance K (863)** |
| 7 | Graph DFS/BFS | components, reachability, deps, shortest | dfs visited; bfs; multi-source; topo; union-find | **Number of Islands (200)** | **Course Schedule (207)** / **Word Ladder (127)** |
| 8 | Backtracking | generate all, constraints, search tree | subsets; perms; combs; prune; grid; dup skip | **Subsets (78)** | **Combination Sum (39)** / **N-Queens (51)** |
| 9 | Heap / PQ | top-k, merge-k, scheduling | min/max; top-k; k-merge; two heaps; scheduling | **Top K Frequent (347)** | **Kth Largest (215)** / **Merge K Lists (23)** |
| 10 | DP | optimal + overlap | 1D; 2D; knapsack; LIS; interval; tree; bitmask | **Climbing Stairs (70)** | **Coin Change (322)** / **Edit Distance (72)** |
| 11 | Prefix Sum | range sum, subarray sum=k | 1D; hashmap prefix; 2D; diff array | **Subarray Sum = K (560)** | **Product Except Self (238)** / **2D sum (304)** |
| 12 | Monotonic Stack | next greater, histogram, spans | inc/dec; NGE; histogram; maximal rectangle | **Daily Temps (739)** | **Histogram (84)** / **Max Rectangle (85)** |
| 13 | Greedy | local best → global, intervals | intervals; sort+pick; jump; circular; greedy+heap | **Merge Intervals (56)** | **Jump Game (55)** / **Gas Station (134)** |

> Tip: For each pattern, your “canonical” is the one you redo from memory after 24 hours.

---

# AI/System Design Patterns

## Reliability & Resilience

| Pattern | When to use | Implementation tasks (practice) |
|--------|-------------|----------------------------------|
| Timeout | calls can hang | Add per-call timeout + global SLA timeout |
| Retry + Backoff (+ jitter) | transient failures (429/5xx) | Retry only idempotent ops; add jitter |
| Circuit Breaker | cascading failures | Open/half-open/close states + metrics |
| Bulkhead | isolate failures | Separate worker pools for OCR vs LLM |
| Rate Limiting | protect system | per-tenant token bucket |
| Graceful Degradation | partial availability | fallback model, partial answer, “cannot determine” |
| Partial Results | long workflows | return partial extraction + status link |
| Load Shedding | overload | reject low-priority jobs early |

---

## Distributed Workflows & Async

| Pattern | When to use | Practice tasks (mini-project) |
|--------|-------------|--------------------------------|
| Job/Workflow | long tasks | job_id + step states in SQL |
| Long-running task | > request time | async submit + polling/webhook |
| Idempotency key | retries happen | idempotency on submit endpoint |
| Dedup (hashing) | duplicate requests | hash(input) → reuse result |
| Outbox | reliable events | write to DB + publish later |
| Backpressure | queues grow | limit concurrency + queue depth alarms |
| Saga | multi-step with rollback | compensating actions per step |

---

## API Design & Evolution

| Pattern | When to use | Practice tasks |
|--------|-------------|----------------|
| API Gateway | single entrypoint | auth, rate limit, routing, request-id |
| BFF | multiple clients | mobile vs web tailored payloads |
| Versioning | breaking changes | `/v1`, `/v2` + compatibility layer |
| Structured errors | consistent handling | error codes + trace_id + user message |
| Pagination/filtering | list endpoints | cursor pagination + filters |
| Contract testing | prevent breakage | tests for response schema |

---

## Data, Storage & Caching

| Pattern | When to use | Practice tasks |
|--------|-------------|----------------|
| Cache-aside | repeated reads | cache retrieval results by hash |
| CQRS | heavy reads | read model for dashboard |
| Audit log | compliance | append-only `audit_events` table |
| Soft delete | restore + audit | `deleted_at` + filters |
| Immutable blob + metadata DB | documents | store PDF in blob, metadata in SQL |

---

## Streaming & Eventing

| Pattern | When to use | Practice tasks |
|--------|-------------|----------------|
| Pub/Sub | async fanout | “doc_uploaded” → multiple consumers |
| DLQ | poison messages | move failed jobs after N retries |
| Replay | reprocessing | re-run pipeline from stored steps |

---

## Observability & Governance

| Pattern | Why it matters | Practice tasks |
|--------|-----------------|----------------|
| Tracing | explain failures | trace_id across gateway → workers |
| Prompt versioning | reproduce outputs | store prompt template hash + params |
| Replay | debug “why model said this” | run same inputs with same prompt+model |
| Metrics | SLOs | latency, success rate, cost per job |
| Cost observability | billing control | tokens per tenant per endpoint |

---

## Security & Compliance

| Pattern | When to use | Practice tasks |
|--------|-------------|----------------|
| RBAC | enterprise | role-based access per tenant |
| Secrets mgmt | no hardcoding | Key Vault + rotation |
| PII redaction | sensitive docs | regex+NER → redact before logs |
| Policy enforcement | unsafe outputs | fail-closed on violations |
| Content moderation | safety | pre/post moderation gates |

---

# LLM/RAG/Agentic Patterns (AI Engineer)

## RAG Core

| Pattern | Goal | Practice tasks |
|--------|------|----------------|
| Chunking | better recall | chunk by headings/pages; store chunk_id |
| Metadata-first | reduce noise | filter by doc_type, date, tenant |
| Hybrid retrieval | best recall | combine BM25 + vector |
| Re-ranking | boost relevance | rerank top-20 to top-5 |
| Context budgeting | fit tokens | compress + top-k cap |
| Grounded generation | citations | answer with chunk_id citations |
| Verification | reduce hallucinations | “not found → null” rule |

## Multi-Agent Workflows

| Pattern | Goal | Practice tasks |
|--------|------|----------------|
| Orchestrator | control flow | LangGraph state machine |
| Router agent | route tasks | doc_type/confidence routing |
| Plan & execute | structured steps | planner outputs plan JSON |
| Critic/verifier | quality gate | verify schema + evidence |
| HITL escalation | safety | route low confidence to review |
| Deterministic outputs | reliability | schema-first JSON extraction |

## LLM Safety & Cost

| Pattern | Goal | Practice tasks |
|--------|------|----------------|
| Schema-first | strict outputs | Pydantic validation + repair loop |
| Prompt injection defense | safety | strip instructions from retrieved text |
| Dedup | cost control | hash(query+filters) cache response |
| Model routing | cost/perf | cheap model first; upgrade on low confidence |
| Token budgets | guardrail | per-tenant token caps |

---


## Weekly rhythm
- **3 days DSA**: 1 pattern (template + canonical + variation + redo)
- **2 days System Design**: 1 category (build 1 mini-project slice)
- **Weekend**: redo 2 canonicals from memory + 1 mock design talk

## What “done” means
A pattern is done only if you can:
- pick it in 30 seconds (trigger recognition)
- write the template from memory
- solve the canonical problem without looking
- explain the trade-offs in 60 seconds
