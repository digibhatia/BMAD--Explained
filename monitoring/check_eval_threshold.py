"""
Quality gate for CI — enforces minimum evaluation thresholds from
monitoring/eval_results.json (produced by run_evaluation.py).

Exits non-zero (failing the CI job) if any threshold is not met.
This is the automated half of the Delivery checklist in BMAD_ANALYSIS.md —
it does not replace human review, but it stops an obviously regressed
build before it reaches that review.
"""

import argparse
import json
import os
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-groundedness", type=float, default=0.85)
    parser.add_argument("--min-escalation-accuracy", type=float, default=1.0)
    args = parser.parse_args()

    results_path = os.path.join(os.path.dirname(__file__), "eval_results.json")
    if not os.path.exists(results_path):
        print("No eval_results.json found — run monitoring/run_evaluation.py first.")
        sys.exit(1)

    with open(results_path) as f:
        results = json.load(f)

    failures = []

    escalation_accuracy = results["escalation_accuracy_suite"]["accuracy"]
    if escalation_accuracy < args.min_escalation_accuracy:
        failures.append(
            f"Escalation accuracy {escalation_accuracy:.2%} is below the required "
            f"{args.min_escalation_accuracy:.2%}. This is a hard gate — escalation "
            f"logic errors are not acceptable to ship."
        )

    rag_suite = results["rag_groundedness_suite"]
    if rag_suite.get("skipped"):
        print(f"Note: RAG groundedness suite was skipped ({rag_suite['reason']}) — "
              f"not enforced this run, but do not merge to main without it having run at least once.")
    else:
        groundedness = rag_suite["groundedness"]
        if groundedness < args.min_groundedness:
            failures.append(
                f"RAG groundedness {groundedness:.2%} is below the required "
                f"{args.min_groundedness:.2%}."
            )

    if failures:
        print("QUALITY GATE FAILED:")
        for f in failures:
            print(f" - {f}")
        sys.exit(1)

    print("Quality gate passed.")


if __name__ == "__main__":
    main()
