# customer-care-system

A working telecom customer-care backend — billing, complaints, plan recommendations
and outage notifications. Traditional deterministic code throughout. No AI.

## Structure

```
api/            REST route handlers
services/       Business logic
database/       In-memory data stores (stand-ins for real DB tables)
ui/             (placeholder — not the focus of this exercise)
app.py          Flask entrypoint
```

## Running

```
pip install flask --break-system-packages
python app.py
```

## Status

This started as a functioning, five-year-old application with no AI. See
`BMAD_ANALYSIS.md` for the module-by-module Breakthrough Opportunity and
Model Strategy decisions that guided every change since.

## Production Readiness (Commit 7 — Delivery)

The BMAD "Delivery" stage checklist, applied:

- [x] **Logging** — every agent/RAG path prints a traceable line (see `notification_node`, `answer_customer_query`).
- [x] **Evaluation** — `monitoring/run_evaluation.py`: escalation-accuracy suite (always runs) + RAG groundedness suite (runs when `OPENAI_API_KEY` is set).
- [x] **Quality Gate** — `monitoring/check_eval_threshold.py`, enforced in `.github/workflows/ci.yml` on every PR.
- [x] **Tests** — `tests/` covers the deterministic billing logic and the pure classification/escalation logic, independent of LangGraph/ChromaDB/OpenAI.
- [x] **CI/CD** — `.github/workflows/ci.yml`: syntax check, unit tests, evaluation, quality gate, on every push/PR to `main`.
- [x] **Containerization** — `Dockerfile` builds the vector store at image build time and serves the Flask app.
- [ ] **Human Approval** — not yet implemented; the Phase 2 "Human-in-the-Loop Workflow Systems" module (compensation and escalation cases) extends this repo further.
- [ ] **Cost / Security review** — not yet implemented; Phase 3 (Optimization) and Phase 4 (Governance & FinOps) extend this repo further.

## Running

```
pip install -r requirements.txt
python knowledge/build_index.py     # builds the ChromaDB vector store
python app.py
```

## Running Tests & Evaluation Locally

```
pytest tests/ -v
python monitoring/run_evaluation.py
python monitoring/check_eval_threshold.py --min-groundedness 0.85 --min-escalation-accuracy 1.0
```

## Commit History as a BMAD Narrative

| Commit | What Changed | BMAD Stage |
|---|---|---|
| 1 | Legacy CRM, no AI | (baseline) |
| 2 | `BMAD_ANALYSIS.md` — no code | Breakthrough Opportunity + Model Strategy |
| 3 | ChromaDB knowledge base | Application Engineering (RAG, part 1) |
| 4 | Retrieval integrated into billing FAQ | Application Engineering (RAG, part 2) |
| 5 | Structured CRM tool added | Application Engineering (structured + unstructured) |
| 6 | Agentic complaint workflow (LangGraph) | Application Engineering (Agent) |
| 7 | Tests, CI, evaluation, Docker | Delivery |

