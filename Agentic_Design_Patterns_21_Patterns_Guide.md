# Agentic Design Patterns — Practical Markdown Guide (21 Patterns)

This document summarizes the **21 agentic design patterns** from *Agentic Design Patterns: A Hands‑On Guide to Building Intelligent Systems* (Antonio Gulli).  
For each pattern you’ll find:

- A **simple diagram** (Markdown-friendly)
- **What it is**
- **How it works** (step-by-step)
- **Pros / Cons**
- **When to use**
- **Examples** (practical, easy to map to real systems)

---

## Table of contents

1. Prompt Chaining  
2. Routing  
3. Parallelization  
4. Reflection  
5. Tool Use  
6. Planning  
7. Multi‑Agent Collaboration  
8. Memory Management  
9. Learning & Adaptation  
10. Model Context Protocol (MCP)  
11. Goal Setting & Monitoring  
12. Exception Handling & Recovery  
13. Human‑in‑the‑Loop (HITL)  
14. Knowledge Retrieval (RAG)  
15. Inter‑Agent Communication (A2A)  
16. Resource‑Aware Optimization  
17. Reasoning Techniques  
18. Guardrails / Safety Patterns  
19. Evaluation & Monitoring  
20. Prioritization  
21. Exploration & Discovery  

---

## 1) Prompt Chaining (Pipeline)

```text
[Input]
  |
  v
[Step 1 Prompt] -> [Step 2 Prompt] -> [Step 3 Prompt] -> ... -> [Final Output]
```

**What it is**  
Break one big task into a sequence of smaller prompts, where each step produces a cleaner intermediate result for the next.

**How it works**
1. Define the final objective (what “done” looks like).
2. Split it into 2–6 smaller sub-tasks that each produce a useful intermediate artifact.
3. Make each step output structured data (bullets/JSON/table) so downstream prompts are stable.
4. Run steps in order; keep logs of intermediate outputs.
5. Optionally add validation at each step (schema checks, “must include X”, etc.).

**Pros**
- Easier to debug (you can inspect each step’s output)
- Higher reliability than one massive prompt
- Lets you enforce structure gradually

**Cons**
- More latency/cost (multiple calls)
- Errors can cascade if early steps are wrong

**When to use**
- Any multi-step work: summarization → extraction → formatting, analysis → decision → action, etc.

**Example**
- “Analyze a report” pipeline:
  1) Summarize key sections  
  2) Extract metrics + dates  
  3) Create an executive summary + action list  

---

## 2) Routing

```text
             /--> [Workflow A]
[Input] ---> [Router]
             \--> [Workflow B]
                  \--> [Ask clarifying question / fallback]
```

**What it is**  
A “traffic controller” that decides which tool/agent/workflow should handle a request.

**How it works**
1. Extract signals from the request (intent, domain, urgency, confidence).
2. Classify the request into a route (rules, model-based classifier, or hybrid).
3. Execute the chosen workflow.
4. If confidence is low, ask a clarifying question or go to a safe fallback path.

**Pros**
- Scales to many use cases without one giant prompt
- You can specialize workflows (e.g., math vs. writing vs. coding)

**Cons**
- Misrouting hurts quality
- Requires labels/evals to tune routes

**When to use**
- You have multiple tools/agents and need the system to choose the best one.

**Example**
- User asks: “Explain this concept” → writing/explainer route  
- User asks: “Calculate monthly payment” → calculator tool route  

---

## 3) Parallelization

```text
                 /-> [Task A] --\
[Input] -> [Fork] -> [Task B] ----> [Merge] -> [Output]
                 \-> [Task C] --/
```

**What it is**  
Run independent sub-tasks simultaneously, then combine results.

**How it works**
1. Identify sub-tasks that do not depend on each other.
2. Run them concurrently (threads/async/jobs).
3. Merge outputs using a “join” step (rank, vote, dedupe, summarize).

**Pros**
- Faster end-to-end latency
- Good for multi-source checks or multi-document processing

**Cons**
- Harder tracing/debugging
- Merge step can become messy (conflicts, duplicates)

**When to use**
- “Fetch N things, then combine” patterns.

**Example**
- Retrieve from 3 knowledge sources at once and merge into a single answer.

---

## 4) Reflection (Generate → Critique → Refine)

```text
[Draft] -> [Critique] -> [Revise] -> (loop) -> [Final]
```

**What it is**  
An improvement loop: produce a draft, review it, then revise.

**How it works**
1. Generate a first draft.
2. Run a critic step:
   - check for missing requirements
   - check logic gaps
   - check formatting constraints
3. Revise with explicit instructions from critique.
4. Stop after N loops or when a score/criteria is met.

**Pros**
- Better quality for writing, reasoning, code, and structured outputs
- Catches missing requirements early

**Cons**
- More tokens/time
- Needs a stopping rule (or it can loop too much)

**When to use**
- When quality matters more than speed, or outputs must meet strict requirements.

**Example**
- Write a cover letter → critique for tone + missing keywords → rewrite.

---

## 5) Tool Use (Function Calling)

```text
[User Request]
   |
   v
[LLM chooses tool + args]
   |
   v
[Tool runs] -> [Result]
   |
   v
[LLM uses result] -> [Answer / Next step]
```

**What it is**  
Let the model call external tools (APIs, calculators, DB, file system, web search) to get accurate results and take actions.

**How it works**
1. Define a limited set of tools with clear schemas.
2. LLM selects the right tool and structured arguments.
3. Tool executes and returns a result.
4. LLM uses the result to answer (or to decide the next tool call).

**Pros**
- Accurate computations and real data access
- Extends model capability beyond “text only”

**Cons**
- Security and permissions are critical
- Tool failures must be handled gracefully

**When to use**
- Anytime the answer depends on external truth: databases, current data, calculations, file transforms.

**Example**
- Convert a PDF → extract tables → compute totals → generate summary.

---

## 6) Planning

```text
[Goal] -> [Plan steps] -> [Execute step-by-step]
                 ^             |
                 |--- revise --|
```

**What it is**  
Create an explicit plan (steps/subgoals) before execution.

**How it works**
1. Translate the request into a clear goal.
2. Generate a plan: steps + dependencies + required tools.
3. Execute step-by-step, checking progress after each step.
4. If a step fails or new info appears, update the plan.

**Pros**
- More reliable on complex objectives
- Easier to track progress and handle dependencies

**Cons**
- Plans can be wrong or too high-level
- More orchestration complexity

**When to use**
- Multi-step problems where “just answer once” isn’t enough.

**Example**
- “Build a study plan”: define milestones → schedule topics → create daily tasks.

---

## 7) Multi‑Agent Collaboration

```text
                /-> [Agent: Research]
[Goal] -> [Coordinator]
                \-> [Agent: Builder]
                 \-> [Agent: Reviewer]
                        |
                        v
                    [Synthesis] -> [Output]
```

**What it is**  
Use multiple specialized agents to solve one larger problem.

**How it works**
1. Coordinator decomposes the task.
2. Assign sub-tasks to specialist agents.
3. Agents produce artifacts (notes, code, critiques).
4. Coordinator merges into a final result (or iterates).

**Pros**
- Specialization improves quality
- Modular and scalable

**Cons**
- Coordination overhead (formats, protocols, merging)
- More cost/latency if unmanaged

**When to use**
- When tasks span multiple skills/domains, or you want robust “review” by a separate agent.

**Example**
- One agent gathers sources, one writes draft, one checks for errors, coordinator merges.

---

## 8) Memory Management

```text
[Events/Conversation]
   |
   +--> [Short-term memory (session)]
   |
   +--> [Long-term memory store]
             |
             v
      [Retrieve relevant memories] -> [Context] -> [LLM]
```

**What it is**  
Store and recall useful information so the agent stays consistent across long tasks or repeated sessions.

**How it works**
1. Decide what to store (preferences, facts, decisions, summaries).
2. Store with metadata (time, tags, source).
3. Retrieve only what’s relevant to the current task.
4. Inject retrieved items into context with boundaries (so they don’t overpower the prompt).

**Pros**
- Continuity and personalization
- Less repeated questioning

**Cons**
- Privacy/security concerns
- Retrieval mistakes can add noise or wrong assumptions

**When to use**
- Assistants, long-running workflows, multi-step projects.

**Example**
- Remember a user’s preferred output style and reuse it automatically.

---

## 9) Learning & Adaptation

```text
[Run agent] -> [Collect feedback/outcome] -> [Update behavior]
      ^---------------------------------------------|
```

**What it is**  
Improve over time based on feedback, outcomes, or logged data.

**How it works**
1. Capture outcome signals (user edits, success/failure, ratings).
2. Analyze patterns (where it fails, what users prefer).
3. Update prompts, routes, retrieval settings, or fine-tune models.
4. Validate improvements with evaluation before rollout.

**Pros**
- System gets better with use
- Reduces repeated mistakes

**Cons**
- Risk of learning the wrong thing (bad feedback, drift)
- Requires governance and evaluation

**When to use**
- High-usage agents where improvements compound.

**Example**
- If users often correct tone, update the style instructions or routing.

---

## 10) Model Context Protocol (MCP)

```text
[Agent/LLM] -> [MCP Client] <--> [MCP Server] -> [Tools/Resources]
```

**What it is**  
A standardized way to connect models to tools/resources via “servers,” reducing custom integration work.

**How it works**
1. Tools/resources are exposed behind MCP servers.
2. The agent connects through an MCP client.
3. Calls are standardized (discovery, auth, request/response).

**Pros**
- Consistent integration patterns across many tools
- Easier to maintain than dozens of custom connectors

**Cons**
- Extra infrastructure layer
- Still needs strict access control and auditing

**When to use**
- You have many tools/data sources and want a clean, standardized integration layer.

**Example**
- One MCP server for “documents,” one for “database,” one for “tickets.”

---

## 11) Goal Setting & Monitoring

```text
[Define goal + success criteria]
   |
   v
[Execute] -> [Monitor metrics/state] -> [Adjust / recover / escalate]
```

**What it is**  
Make goals explicit and continuously track progress toward them.

**How it works**
1. Define measurable success criteria (even if approximate).
2. Track progress signals after each step.
3. If off-track: adjust plan, ask for help, or fail safely.

**Pros**
- Less wandering; more reliable autonomy
- Detects problems early

**Cons**
- Hard to define metrics for subjective tasks
- Monitoring adds complexity

**When to use**
- Long tasks with multiple steps and possible failure points.

**Example**
- “Find 5 credible sources”: monitor count + diversity + relevance score.

---

## 12) Exception Handling & Recovery

```text
[Action/Tool call]
   |
   v
[Error?] -> [Retry] -> [Fallback] -> [Repair/Rollback] -> [Continue/Escalate]
```

**What it is**  
Treat failures as normal: detect them, recover, and keep going safely.

**How it works**
1. Detect failures (timeouts, bad schemas, empty retrieval, tool errors).
2. Retry with backoff if the failure is transient.
3. Fallback to an alternative tool/route.
4. Repair state or rollback if needed.
5. Escalate to human if risk is high.

**Pros**
- More stable and production-ready
- Prevents total failure from minor glitches

**Cons**
- Requires careful engineering (idempotency, retries, logging)
- Complex to test

**When to use**
- Any agent that calls tools/APIs in production.

**Example**
- If retrieval returns nothing: broaden query → use keyword search → ask user.

---

## 13) Human‑in‑the‑Loop (HITL)

```text
[Agent proposes]
   |
   v
[Human reviews/edits/approves]
   |
   v
[Execute] -> [Feedback captured] -> [Agent improves]
```

**What it is**  
A design where humans review or approve critical steps.

**How it works**
1. Agent produces a proposal and rationale.
2. Human edits/approves/rejects.
3. System executes only after approval (or uses partial approval rules).
4. Store feedback for future improvements.

**Pros**
- Safer for high-stakes decisions
- Builds trust and accountability

**Cons**
- Slower; requires human availability
- Needs good UX (what to show, how to approve)

**When to use**
- Anything risky: legal/medical/financial actions, customer-facing actions, irreversible operations.

**Example**
- Draft an email → user approves → send.

---

## 14) Knowledge Retrieval (RAG)

```text
[Question]
   |
   v
[Retrieve relevant passages]
   |
   v
[Grounded prompt (question + passages)]
   |
   v
[LLM answer + citations (optional)]
```

**What it is**  
Retrieve knowledge from a database/doc store and use it to ground the model’s response.

**How it works**
1. Convert query to retrieval form (embedding/keywords/hybrid).
2. Retrieve top‑k chunks.
3. Optionally rerank and filter for relevance.
4. Provide retrieved context to the LLM to generate a grounded answer.
5. Optionally cite sources and store trace for audit.

**Pros**
- Fewer hallucinations; answers based on real docs
- Keeps system up-to-date without retraining

**Cons**
- Retrieval quality is hard (chunking, noise, missing data)
- Requires indexing/updates + extra latency

**When to use**
- Enterprise knowledge bases, manuals, reports, policies, document Q&A.

**Example**
- “What does our policy say about refunds?” → retrieve policy section → answer grounded.

---

## 15) Inter‑Agent Communication (A2A)

```text
[Agent A] <---- messages/tasks/results ----> [Agent B]
     \-------------------------------------> [Agent C]
```

**What it is**  
A structured way for agents to communicate, delegate tasks, and stream updates—especially across different implementations.

**How it works**
1. Agents advertise capabilities (what they can do).
2. One agent assigns tasks to another with a clear schema.
3. Receiver returns results (one-shot or streaming).
4. Caller merges and continues.

**Pros**
- Enables “ecosystems” of agents
- Clean delegation and modularity

**Cons**
- Requires strong auth, rate limits, and safety rules
- Coordination errors can multiply

**When to use**
- You want separate agent services that can collaborate (specialists, external teams, plug-ins).

**Example**
- Research agent asks math agent to verify calculations, then merges into report.

---

## 16) Resource‑Aware Optimization

```text
[Request] -> [Complexity/Cost estimate]
                 |
                 +--> [Cheap path: small model, fewer tools]
                 |
                 \--> [Strong path: bigger model, more retrieval/tools]
```

**What it is**  
Choose the right “power level” (model/tooling/context size) for each request to balance cost, latency, and accuracy.

**How it works**
1. Estimate difficulty/importance (intent, length, ambiguity, risk).
2. Route to a cheaper or stronger model (or different workflow).
3. Tune context: summarize, drop noise, keep only essentials.
4. Track spend/latency metrics to keep budgets under control.

**Pros**
- Saves cost and time while keeping quality
- Scales better in production

**Cons**
- Wrong estimation can reduce quality
- Requires monitoring and tuning

**When to use**
- High traffic, expensive models, strict latency budgets, mixed difficulty requests.

**Example**
- Simple FAQ → small model  
- Complex multi-doc analysis → strong model + retrieval + reflection

---

## 17) Reasoning Techniques

```text
[Problem]
   |
   v
[Reasoning strategy]
   |
   v
[Optional: tool calls / intermediate checks]
   |
   v
[Answer + verification]
```

**What it is**  
Use structured reasoning methods (often with intermediate steps and tool use) to solve harder problems.

**How it works**
1. Choose a strategy: step-by-step decomposition, tree search, “think + act” loops.
2. Use tools when calculation/facts are needed.
3. Verify: consistency checks, constraints, unit tests, cross-checking.
4. Produce the final answer with a short rationale.

**Pros**
- Higher success on complex tasks (math, planning, debugging)
- Better reliability with verification

**Cons**
- More tokens/latency
- Needs guardrails to prevent “overthinking” loops

**When to use**
- Complex reasoning tasks where one-shot answers are unreliable.

**Example**
- Solve a multi-step word problem with calculator tool + verification.

---

## 18) Guardrails / Safety Patterns

```text
[Input checks] -> [Policy constraints] -> [Tool restrictions]
      |
      v
[LLM output] -> [Output checks] -> [Safe output / escalation]
```

**What it is**  
Multiple safety layers that constrain what the agent can do and how it behaves.

**How it works**
1. Validate input (red flags, missing details, disallowed asks).
2. Restrict tools (allowlists, read-only modes, sandboxing).
3. Constrain prompts (role boundaries, “do not do X”).
4. Validate output (policy checks, leakage prevention, format checks).
5. Escalate to human for sensitive actions.

**Pros**
- Safer, more trustworthy systems
- Reduces harmful or off-policy outputs

**Cons**
- Can over-block and reduce usefulness
- Needs continuous updates as threats evolve

**When to use**
- Any product, especially with tool actions and real-world impact.

**Example**
- Tool allowlist + human approval for sending emails or modifying files.

---

## 19) Evaluation & Monitoring

```text
[Agent runs]
   |
   v
[Log: inputs, tools, outputs, latency, cost]
   |
   v
[Evaluate quality] -> [Detect drift] -> [Improve + redeploy]
```

**What it is**  
Continuous measurement of quality, cost, and safety—before and after deployment.

**How it works**
1. Define metrics (task success, factuality, latency, cost, refusal rate).
2. Create eval sets (unit tests, golden answers, adversarial cases).
3. Monitor production logs (alerts, drift detection).
4. Run A/B tests and compare agent versions.

**Pros**
- Keeps systems reliable over time
- Enables safe iteration and governance

**Cons**
- Requires datasets, infra, and careful metric design
- “Measuring the right thing” is hard

**When to use**
- Any production agent, especially in regulated or customer-facing environments.

**Example**
- Evaluate RAG answer accuracy weekly; alert when retrieval recall drops.

---

## 20) Prioritization

```text
[Tasks] -> [Score: urgency + impact + risk + dependencies] -> [Queue] -> [Execute]
                               ^------------------------------------|
                               |------ re-score as new info arrives-|
```

**What it is**  
Decide what to do first when there are multiple tasks or limited resources.

**How it works**
1. Convert work into a task list (explicit queue).
2. Score each task (deadline, user value, risk, dependencies, cost).
3. Execute highest priority first.
4. Re-score when conditions change (new deadlines, failures, new tasks).

**Pros**
- Prevents wasted work on low-value tasks
- Improves responsiveness to urgent issues

**Cons**
- Bad scoring can starve important tasks
- Needs good signals and tuning

**When to use**
- Multi-user agents, long-running backlogs, async job systems.

**Example**
- Support agent: urgent outage tickets first, low-impact questions later.

---

## 21) Exploration & Discovery

```text
[Unknown problem space]
   |
   v
[Generate hypotheses/options]
   |
   v
[Experiment / search / simulate]
   |
   v
[Evaluate results] -> [Refine] -> (iterate) -> [Best answer/strategy]
```

**What it is**  
A loop for research-like tasks where the agent must explore, test, and learn.

**How it works**
1. Start with hypotheses (possible causes/solutions).
2. Gather evidence (search, tool calls, experiments).
3. Evaluate findings and eliminate weak hypotheses.
4. Iterate until confidence is high or budget is reached.

**Pros**
- Great for open-ended research and debugging unknowns
- Finds non-obvious solutions

**Cons**
- Can be expensive (many trials)
- Needs stopping criteria and evaluation rules

**When to use**
- Research, diagnosis, innovation, hypothesis-driven debugging.

**Example**
- “Why is the system slow?” → test DB, network, caching hypotheses → narrow down cause.

---

## Tips for combining patterns (common “recipes”)

- **RAG + Reflection**: retrieve facts, draft answer, critique for grounding, revise.  
- **Routing + Tool Use**: route requests, then call the right tool.  
- **Planning + Exception Recovery**: plan steps, execute, recover when tools fail.  
- **Multi-agent + Evaluation**: specialist agents produce artifacts; evaluator agent scores outputs.

---

### Want a version tailored to your project?
If you tell me your target use case (e.g., “document analyzer”, “study assistant”, “coding agent”), I can generate:
- a recommended **pattern stack**
- a reference architecture diagram
- a minimal implementation checklist
