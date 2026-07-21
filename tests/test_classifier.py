import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from agents.classifier import classify_complaint, decide_escalation


def test_classify_network_outage_as_high_severity():
    c = classify_complaint("My internet has been down for 3 days")
    assert c["severity"] == "high"


def test_classify_fraud_keyword_as_critical():
    c = classify_complaint("There was an unauthorized charge on my account")
    assert c["severity"] == "critical"


def test_classify_generic_complaint_as_medium():
    c = classify_complaint("The app is a bit slow sometimes")
    assert c["severity"] == "medium"


def test_decide_escalation_on_high_severity():
    c = {"severity": "high", "confidence_score": 0.9}
    assert decide_escalation(c, prior_ticket_count=0) == "escalate"


def test_decide_resolve_on_first_time_low_severity():
    c = {"severity": "medium", "confidence_score": 0.9}
    assert decide_escalation(c, prior_ticket_count=0) == "resolve"


def test_decide_escalation_overrides_severity_when_prior_tickets_exist():
    """The hard rule must win even when severity alone would say 'resolve'."""
    c = {"severity": "medium", "confidence_score": 0.9}
    assert decide_escalation(c, prior_ticket_count=2) == "escalate"


def test_decide_escalation_on_invalid_classification():
    c = {"severity": "medium", "confidence_score": 0.9}
    assert decide_escalation(c, prior_ticket_count=0, valid=False) == "escalate"
