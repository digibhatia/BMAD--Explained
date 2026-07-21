"""
Evaluation runner for the customer-care-system.

Two suites:
1. Escalation accuracy — pure logic, no API key needed, always runs.
   This is deliberately kept dependency-free so it can run in any CI
   environment without secrets.
2. RAG groundedness — calls the real billing assistant against
   monitoring/eval_dataset.csv. Requires OPENAI_API_KEY; skipped with a
   clear note if the key isn't set (e.g. in a fork's PR build).

Results are written to monitoring/eval_results.json for
check_eval_threshold.py to enforce as a CI quality gate.
"""

import csv
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from agents.classifier import classify_complaint, decide_escalation

ESCALATION_TEST_SET = [
    # (description, prior_ticket_count, expected_decision)
    ("My internet has been down for 3 days", 0, "escalate"),
    ("There was an unauthorized charge on my account", 0, "escalate"),
    ("The app is a bit slow sometimes", 0, "resolve"),
    ("The app is a bit slow sometimes", 2, "escalate"),  # hard rule override
    ("I have a small question about my invoice", 0, "resolve"),
]


def run_escalation_accuracy_suite():
    correct = 0
    details = []
    for description, prior_count, expected in ESCALATION_TEST_SET:
        classification = classify_complaint(description)
        actual = decide_escalation(classification, prior_count)
        passed = actual == expected
        correct += int(passed)
        details.append({
            "description": description, "prior_ticket_count": prior_count,
            "expected": expected, "actual": actual, "passed": passed,
        })
    accuracy = correct / len(ESCALATION_TEST_SET)
    return {"accuracy": accuracy, "details": details}


def run_rag_groundedness_suite():
    if not os.environ.get("OPENAI_API_KEY"):
        return {"skipped": True, "reason": "OPENAI_API_KEY not set"}

    from services.billing_service import answer_customer_query

    dataset_path = os.path.join(os.path.dirname(__file__), "eval_dataset.csv")
    results = []
    with open(dataset_path, newline="") as f:
        for row in csv.DictReader(f):
            answer = answer_customer_query(row["question"])
            # Simple groundedness proxy: does the answer reference the same
            # clause number as the expected source? A real evaluation would
            # use an LLM-as-judge scoring rubric — see Phase 3: Evaluation Systems.
            clause_number = row["source_clause"].replace("clause_", "").replace("_", ".")
            grounded = clause_number in answer or row["expected_answer"][:20].lower() in answer.lower()
            results.append({"question": row["question"], "answer": answer, "grounded": grounded})

    grounded_count = sum(1 for r in results if r["grounded"])
    return {"skipped": False, "groundedness": grounded_count / len(results), "details": results}


def main():
    results = {
        "escalation_accuracy_suite": run_escalation_accuracy_suite(),
        "rag_groundedness_suite": run_rag_groundedness_suite(),
    }
    out_path = os.path.join(os.path.dirname(__file__), "eval_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"Escalation accuracy: {results['escalation_accuracy_suite']['accuracy']:.2%}")
    if results["rag_groundedness_suite"].get("skipped"):
        print(f"RAG groundedness: SKIPPED ({results['rag_groundedness_suite']['reason']})")
    else:
        print(f"RAG groundedness: {results['rag_groundedness_suite']['groundedness']:.2%}")
    print(f"Results written to {out_path}")


if __name__ == "__main__":
    main()
