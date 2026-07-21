import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from services.billing_service import calculate_bill


def test_calculate_bill_known_customer():
    result = calculate_bill("1042")
    assert result["base_charge"] == 999
    assert result["tax"] == 179.82
    assert result["late_fee"] == 50          # days_since_bill (20) > 15
    assert result["roaming_charges"] == 210
    assert result["total"] == 999 + 179.82 + 50 + 210


def test_calculate_bill_no_late_fee_within_grace_period():
    result = calculate_bill("2087")
    assert result["late_fee"] == 0            # days_since_bill (5) <= 15


def test_calculate_bill_unknown_customer_returns_none():
    assert calculate_bill("9999") is None
