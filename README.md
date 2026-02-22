# 🧠 Master AI Pattern Library  

This repository is a **failure-driven learning system** for mastering:

- ✅ 13 Core DSA Patterns  
- ✅ AI / RAG / Multi-Agent Architecture Patterns  
- ✅ Distributed System & Reliability Patterns  
- ✅ GoF Design Patterns (Creational, Structural, Behavioral)  

This is not theory.



## 📊 Pattern Library Excel
View online here: https://docs.google.com/spreadsheets/d/1do33-iOarpuHW6Ar6jlX9DSFrtf2fw0c/edit?usp=sharing&ouid=115587245782462504192&rtpof=true&sd=true


---


For each pattern:

1. Write the **template from memory** (10m)
2. Solve **1 canonical problem / task** (25m)
3. Solve **1 variation** (20m)
4. Write 5-line **teach-back summary** (5m)
5. Next day: redo canonical from memory (10m)

If you cannot:
- Write the skeleton
- Explain the invariant
- Place it inside a system

You do not know it yet.

---

# 🧱 PART 1 — 13 Core DSA Patterns

| # | Pattern | Triggers | Sub-Patterns | Canonical | Variation |
|---|----------|----------|--------------|------------|------------|
| 1 | Two Pointers | sorted, palindrome, partition | L/R; same dir; partition | Valid Palindrome (125) | 3Sum (15) |
| 2 | Sliding Window | substring, longest/shortest | fixed; variable; freq map | Longest Substring (3) | Min Window (76) |
| 3 | Fast/Slow | cycles, middle | cycle detect; entry | Linked List Cycle (141) | Cycle II (142) |
| 4 | Binary Search | sorted, monotonic | left/right bound; answer space | Binary Search (704) | Rotated Search (33) |
| 5 | Tree DFS | recursion, subtree | top-down; bottom-up | Max Depth (104) | Validate BST (98) |
| 6 | Tree BFS | level traversal | zigzag; multi-source | Level Order (102) | Distance K (863) |
| 7 | Graph DFS/BFS | components, deps | topo; union-find | Number of Islands (200) | Course Schedule (207) |
| 8 | Backtracking | generate all | subsets; perms; prune | Subsets (78) | N-Queens (51) |
| 9 | Heap | top-k, merge-k | min/max; 2-heaps | Top K Frequent (347) | Merge K Lists (23) |
| 10 | DP | optimal + overlap | 1D; 2D; knapsack; LIS | Climbing Stairs (70) | Coin Change (322) |
| 11 | Prefix Sum | range sum, subarray=k | hashmap prefix | Subarray Sum = K (560) | 2D Range Sum (304) |
| 12 | Monotonic Stack | next greater | inc/dec stack | Daily Temps (739) | Histogram (84) |
| 13 | Greedy | local→global | intervals; jump | Merge Intervals (56) | Jump Game (55) |

---

# 🏗 PART 2 — System Design Patterns (Distributed & Reliability)

## Reliability & Resilience

| Pattern | When To Use | Practice Task |
|----------|------------|---------------|
| Timeout | calls hang | add per-call timeout |
| Retry + Backoff | transient failures | exponential retry with jitter |
| Circuit Breaker | cascading failure | open/half-open state logic |
| Bulkhead | isolate services | separate worker pools |
| Rate Limiting | protect system | token bucket per tenant |
| Graceful Degradation | partial failure | fallback model |
| Load Shedding | overload | reject low priority jobs |

---

## Distributed Workflows

| Pattern | When To Use | Practice Task |
|----------|------------|---------------|
| Job / Workflow | long tasks | async job queue |
| Idempotency Key | retries happen | prevent duplicate job |
| Deduplication | cost control | hash request body |
| Outbox Pattern | reliable events | DB + async publish |
| Saga | multi-step rollback | compensating actions |
| Backpressure | queue overflow | concurrency limits |

---

## API Design & Evolution

| Pattern | Purpose | Practice |
|----------|--------|----------|
| API Gateway | single entrypoint | auth + routing |
| BFF | client-specific APIs | mobile/web separation |
| Versioning | breaking changes | /v1, /v2 |
| Structured Errors | consistent failures | error_code + trace_id |
| Pagination | scalable lists | cursor pagination |

---

## Observability & Governance

| Pattern | Purpose | Practice |
|----------|--------|----------|
| Tracing | debug systems | trace_id across services |
| Prompt Versioning | reproducibility | store template hash |
| Replay | debug AI answers | rerun same inputs |
| Metrics | SLO tracking | latency + token usage |
| Cost Attribution | billing control | per-tenant token logs |

---

# 🤖 PART 3 — AI / RAG / Multi-Agent Patterns

## RAG Core

| Pattern | Purpose | Practice |
|----------|--------|----------|
| Chunking | better recall | chunk by headings |
| Metadata Filtering | reduce noise | filter by doc_type |
| Hybrid Retrieval | best recall | BM25 + vector |
| Re-ranking | improve relevance | rerank top 20 |
| Context Budgeting | token limit | top-k cap |
| Grounded Generation | reduce hallucination | cite chunk_id |
| Verification | safe answers | null if not found |

---

## Multi-Agent Workflows

| Pattern | Purpose | Practice |
|----------|--------|----------|
| Orchestrator | control flow | state machine |
| Router Agent | dispatch tasks | route by confidence |
| Planner → Executor | structured steps | plan JSON |
| Critic Agent | validation | verify output schema |
| Human-in-the-Loop | safety | escalate low confidence |
| Deterministic Output | reliability | schema-first extraction |

---

## LLM Safety & Cost

| Pattern | Purpose | Practice |
|----------|--------|----------|
| Schema Validation | strict output | Pydantic validation |
| Prompt Injection Defense | safety | strip instructions |
| Response Cache | cost control | hash(query) cache |
| Model Routing | optimize cost | cheap-first strategy |
| Token Budgets | guardrail | per-tenant cap |

---

# 🧩 PART 4 — GoF Design Patterns (Clean Architecture)

## Creational

| Pattern | Use Case |
|----------|----------|
| Factory | dynamic model selection |
| Abstract Factory | multi-provider system |
| Builder | prompt construction |
| Singleton | config manager |
| Prototype | clone agent config |

## Structural

| Pattern | Use Case |
|----------|----------|
| Adapter | unify provider interfaces |
| Facade | simplify RAG pipeline |
| Decorator | add logging/token tracking |
| Proxy | caching / rate limiting |
| Bridge | abstraction vs implementation |
| Composite | workflow tree |

## Behavioral

| Pattern | Use Case |
|----------|----------|
| Strategy | retrieval switching |
| Template Method | base agent execution |
| Chain of Responsibility | moderation pipeline |
| Command | async job object |
| Observer | tracing events |
| Mediator | multi-agent coordination |
| State | workflow state machine |
| Visitor | analytics over workflow |
| Interpreter | policy rule engine |

---

# 🧭 Unified Failure-Driven Roadmap

| Phase | Focus |
|--------|--------|
| Phase 1 | Reliability (Timeout, Retry, Async, Idempotency) |
| Phase 2 | RAG Correctness |
| Phase 3 | Multi-Agent Orchestration |
| Phase 4 | Observability + Cost |
| Phase 5 | GoF Refactoring |
| Parallel | 13 DSA Patterns |

---

# 🏁 Definition of Mastery

You can:

- Recognize pattern in 30 seconds
- Write skeleton from memory
- Solve canonical problem without help
- Explain trade-offs clearly
- Apply it inside real AI architecture

If you cannot build it, you do not own it.

---


# 🧱 2 Major Projects to Master All Patterns (Step-by-Step)

You will build **one core platform** + **one product surface**.
Together they cover:
- Reliability (timeouts/retry/circuit breaker/bulkheads)
- Async workflows (jobs, saga, outbox, replay, DLQ)
- API evolution (gateway, versioning, structured errors, pagination)
- Data patterns (cache-aside, audit log, soft delete, CQRS)
- Observability (tracing, prompt versioning, replay, metrics, cost)
- Security (RBAC, PII redaction, moderation, fail-closed)
- RAG patterns (chunking, hybrid, rerank, grounded, verification)
- Multi-agent patterns (orchestrator, router, planner-executor, critic, HITL)
- GoF patterns (factory/adapter/strategy/decorator/command/state/observer/etc.)

---

# PROJECT A — AgentFlow Platform (n8n-style Multi-Agent Workflow Builder)

## What You’re Building
A web + API platform where you can:
- visually define workflows (nodes & edges like n8n)
- run workflows as **jobs**
- each node can be:
  - a tool call (OCR, DB query, web fetch)
  - an LLM step (extract, classify, summarize)
  - an agent step (planner/executor/critic)
- platform supports:
  - retries, timeouts, circuit breaker
  - idempotency + dedup
  - audit logs + replay
  - RBAC + PII redaction
  - observability + token cost analytics

### Core Components
- **Gateway API (FastAPI)**
- **Workflow Orchestrator** (state machine: LangGraph or custom)
- **Workers** (task executors)
- **Queue** (Service Bus / Redis / RabbitMQ)
- **Storage**
  - SQL: jobs, steps, audit
  - Blob: documents & artifacts
  - Vector DB: embeddings
- **Observability**
  - trace_id, logs, metrics
  - prompt versions & replay

---

## Phase-by-Phase Pattern Implementation (the “step-by-step” path)

### Phase 0 — Skeleton & Contracts (API cleanliness)
**Patterns**
- Resource-oriented design
- Structured error pattern
- Pagination/filtering
- API versioning

**Deliverable**
- `/v1/workflows`, `/v1/jobs`, `/v1/runs`
- `error_code + trace_id` on every error

---

### Phase 1 — Async Jobs & Reliability Spine (foundation)
**Patterns**
- Job/Workflow pattern
- Long-running task pattern
- Timeout, Retry+Backoff, Circuit Breaker
- Partial results, Graceful degradation
- Bulkhead (separate worker pools)

**Deliverable**
- submit workflow run → returns `job_id`
- polling endpoint: `/v1/jobs/{job_id}`
- retries + timeouts + circuit breaker around LLM calls

---

### Phase 2 — Correctness & Cost Safety (no duplicate spend)
**Patterns**
- Idempotency key
- Deduplication + content hashing
- Command pattern (each node execution is a command)
- Singleton (config only)

**Deliverable**
- `idempotency_key` on run submit
- `step_id = hash(job_id + node_id + input_hash)`
- on retry storms → no duplicate LLM cost

---

### Phase 3 — Persistence, Restart Safety & Replay
**Patterns**
- Externalized state
- Append-only audit log
- Replay / reprocessing
- Soft delete
- Versioned data

**Deliverable**
- DB tables: `jobs`, `job_steps`, `workflow_versions`, `audit_events`
- `/v1/jobs/{job_id}/replay`
- restart workers → jobs resume safely

---

### Phase 4 — Eventing & Scalability
**Patterns**
- Pub/Sub
- Outbox
- DLQ
- Backpressure
- Saga (compensating steps)

**Deliverable**
- publish `job.created`, `step.completed`, `job.failed`
- DLQ for poisoned messages
- backpressure: max concurrency + queue depth alarms

---

### Phase 5 — Observability & Trust (debug “why model said this”)
**Patterns**
- Distributed tracing
- Prompt versioning
- Replayable execution
- Metrics & SLOs
- Cost attribution

**Deliverable**
- every run has `trace_id`
- prompt hash stored per step
- token usage per tenant per workflow
- dashboard: latency, failure rate, top spenders

---

### Phase 6 — Security & Governance (enterprise hardening)
**Patterns**
- RBAC
- Secret management
- PII detection + redaction
- Moderation gate
- Fail-closed defaults
- Compliance boundary

**Deliverable**
- role-based access: viewer/editor/admin
- PII redaction before logs/storage
- moderation pre/post guard

---

### Phase 7 — AI Patterns (RAG + Agents as workflow nodes)
**RAG Patterns**
- Chunking, metadata-first filtering
- Hybrid retrieval, re-ranking
- Context budgeting, grounded generation
- Verification (“not found → null”)

**Agent Patterns**
- Orchestrator node
- Router agent node
- Planner → Executor node
- Critic/Verifier node
- HITL escalation node

**Deliverable**
- “RAG Search” node supports citations
- “Doc Extractor” node outputs strict JSON schema
- “Agent Supervisor” enforces step limits

---

## GoF Patterns Used (explicit mapping)
- **Factory/Abstract Factory**: create provider implementations (OpenAI/Azure)
- **Adapter**: unify provider interfaces
- **Builder**: prompt builder / workflow builder
- **Facade**: `AgentFlowClient` simplified SDK
- **Decorator**: add logging/token-tracking to tool calls
- **Proxy**: caching/rate limit wrapper
- **Strategy**: retrieval strategy switching (vector vs hybrid)
- **Command**: each node run is a command with retries
- **State**: circuit breaker + workflow states
- **Observer**: tracing hooks/events
- **Mediator**: multi-agent coordination

---

## “Done” Definition (AgentFlow)
You can:
- demo a workflow running async with retries
- show dedup prevents double LLM spend
- replay a run exactly with same prompt versions
- trace a failure end-to-end
- enforce RBAC + PII protection

---

# PROJECT B — EvidenceChat (RAG Chatbot + Agent Tools) Built on AgentFlow

## What You’re Building
A product layer that uses AgentFlow:
- chat UI
- uploads PDFs
- grounded answers with citations
- tool-using agent (search, summarize, compare docs)
- admin dashboard: usage, cost, quality

### Why This Project Matters
This is what recruiters understand immediately:
**“Production RAG chatbot with observability, cost controls, safety, and workflow orchestration.”**

---

## Step-by-Step Features (maps to patterns)
1) **Naive chat** (baseline)  
2) Add **RAG** (chunking + citations)  
3) Add **hybrid + rerank** (quality jump)  
4) Add **verification** (hallucination control)  
5) Add **agent tools** (planner/executor)  
6) Add **HITL** (low confidence escalations)  
7) Add **quotas + budgets** (cost safety)  
8) Add **trace + replay** (trust/debug)  
9) Add **RBAC + PII redaction** (enterprise-ready)

---

# Suggested Tech Stack (matches your style)
- FastAPI + Pydantic
- SQLAlchemy + Postgres/Azure SQL
- Redis queue / Azure Service Bus
- Blob storage (Azure Blob)
- Vector DB (FAISS/Azure AI Search)
- LangGraph for orchestration (optional)
- OpenTelemetry + Langfuse style traces (or custom)

---


# 📌 Final Principle

Learn patterns by:

Trigger → Failure → Fix → Refactor → Teach

Not by memorizing names.

---

This README is your long-term interview compass.
Build. Break. Fix. Repeat.





# 🧠 Master Interview Pattern Framework — Mind Map

```mermaid
mindmap
  root((Mastery Framework))

    DSA Patterns
      Two Pointers
        Opposite Direction
        Same Direction
        Partitioning
      Sliding Window
        Fixed Window
        Variable Window
        Frequency Map
      Fast & Slow
        Cycle Detection
        Middle Node
      Binary Search
        Classic
        Boundaries
        Search on Answer
      Tree
        DFS
        BFS
      Graph
        DFS
        BFS
        Topological Sort
        Union Find
      Backtracking
        Subsets
        Permutations
        Pruning
      Heap
        Top K
        Merge K
      Dynamic Programming
        1D
        2D
        Knapsack
        LIS
      Prefix Sum
        Hashmap Prefix
        2D Prefix
      Monotonic Stack
        Next Greater
        Histogram
      Greedy
        Intervals
        Jump Game
        Resource Allocation

    System Design
      Reliability
        Timeout
        Retry + Backoff
        Circuit Breaker
        Bulkhead
        Rate Limiting
        Graceful Degradation
      Distributed Systems
        Async Job Pattern
        Idempotency Key
        Deduplication
        Saga
        Backpressure
      API Design
        API Gateway
        Versioning
        Structured Errors
        Pagination
      Data Layer
        Cache Aside
        CQRS
        Audit Log
        Soft Delete
      Observability
        Tracing
        Metrics
        Replay
        Cost Tracking
      Security
        RBAC
        PII Detection
        Moderation
        Fail Closed

    AI Engineering
      RAG
        Chunking
        Metadata Filtering
        Hybrid Retrieval
        Re Ranking
        Context Budgeting
        Grounded Generation
        Verification
      Multi Agent
        Orchestrator
        Router Agent
        Planner Executor
        Critic Agent
        Human in Loop
      LLM Safety
        Schema Validation
        Prompt Injection Defense
        Model Routing
        Token Budget

    GoF Patterns
      Creational
        Factory
        Abstract Factory
        Builder
        Singleton
      Structural
        Adapter
        Facade
        Decorator
        Proxy
        Bridge
        Composite
      Behavioral
        Strategy
        Template Method
        Chain of Responsibility
        Command
        Observer
        Mediator
        State
        Visitor

    Learning Method
      Trigger Failure
      Apply Pattern
      Refactor
      Teach Back
      Repeat





