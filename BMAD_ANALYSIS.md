# BMAD Analysis — customer-care-system

Before touching a single line of code, apply BMAD's first two stages to every
module in this repository. The goal is to decide **where AI belongs and where
it doesn't** — and to write that decision down before building anything.

## Method

For each module, ask two questions in order:

1. **Breakthrough Opportunity** — is there a real, worthwhile problem here at
   all, or does the current code already do the job well?
2. **Model Strategy** — if there is an opportunity, which pattern fits:
   Rule Engine (no AI), Prompt-only, RAG, Agent, or Multi-Agent?

Application Engineering (the workflow redesign) and Delivery (the deployment
checklist) are deliberately **not** done yet — they come after every module
has a Model Strategy decision, not before.

## Module-by-Module Decision

### Billing Calculation — `services/billing_service.py: calculate_bill()`

- **Breakthrough Opportunity:** None. The function is deterministic, audited,
  and financial. There is no ambiguity for AI to resolve, and no cost or
  quality problem this code has today.
- **Model Strategy:** **Keep the rule engine.** Do not introduce AI here,
  ever, regardless of how capable models get. This is a permanent "no."

### Billing FAQ — `services/billing_service.py: answer_customer_query()`

- **Breakthrough Opportunity:** Yes. This function is currently unimplemented
  — every billing question either goes unanswered or ties up a human agent
  manually reading the policy PDF. High volume, repetitive, natural language.
- **Model Strategy:** **RAG.** The answer needs to be grounded in real policy
  documents (tariff clauses, FAQs), not invented. Not an agent — there is no
  multi-step action to take, just a question to answer accurately.

### Complaint Routing — `services/complaint_service.py: route_complaint()`

- **Breakthrough Opportunity:** Yes. The current if/else ladder cannot support
  what the business is now asking for: sentiment detection, fraud detection,
  SLA validation, and routing that depends on more than one hard-coded field.
- **Model Strategy:** **Agent.** This needs reasoning across multiple signals
  and multiple tools (classify, check history, decide, escalate) — a single
  prompt or a RAG lookup alone can't make this decision.

### Plan Recommendation — `services/recommendation_service.py: recommend_plan()`

- **Breakthrough Opportunity:** Yes. Today's function always recommends the
  same plan regardless of the customer's actual usage — no personalization
  exists at all.
- **Model Strategy:** **RAG + Agent.** Retrieval brings in the current plan
  catalog; light agentic reasoning compares it against real usage data before
  recommending one plan with a justification.

### Outage Notification — `services/notification_service.py: send_outage_notification()`

- **Breakthrough Opportunity:** Yes. Every notification uses the same generic
  template regardless of region, real network status, or impact size —
  customers get a vague message even when real, specific data exists.
- **Model Strategy:** **Multi-Agent.** This needs coordination across network
  status, affected-customer lookup, message drafting, validation and
  notification — more than one responsibility, genuinely separable.

### Ticket Escalation (cross-cutting, inside Complaint Routing)

- **Breakthrough Opportunity:** Yes — high-risk escalation decisions (SLA
  breach, compensation-adjacent cases) need consistent, auditable handling.
- **Model Strategy:** **Human-in-the-Loop**, layered on top of the Agent
  decision above — the agent reasons and recommends, but a hard, code-level
  rule (not the model) decides when a human must approve.

## Summary Table

| Legacy Module            | BMAD Decision      | What Changes                              |
|---------------------------|--------------------|--------------------------------------------|
| Billing Calculation       | Keep Rule-Based     | Nothing — explicitly left alone             |
| Billing FAQ               | RAG                 | ChromaDB + LLM grounded answering           |
| Complaint Routing         | Agent               | Tool-calling agent replaces if/else         |
| Plan Recommendation       | RAG + Agent         | Retrieval + personalized reasoning          |
| Outage Notification       | Multi-Agent         | Planner + network status + CRM + notifier   |
| Ticket Escalation         | Human-in-the-Loop   | Hard rule + approval workflow layered on    |
| (Cross-cutting) Monitoring| LLMOps              | Prompt evaluation & observability, later    |

## What Happens Next

The remaining commits in this repository implement these decisions one at a
time, in the order a real engagement would: knowledge base first (Commit 3),
retrieval integration (Commit 4), structured tool integration (Commit 5),
agentic workflow (Commit 6), then production readiness (Commit 7).

No module is refactored until its BMAD decision above has been written down
and justified — that is the entire point of doing this analysis before
writing any new code.
