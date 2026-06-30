import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.analytics.cagr import (
    calculate_cagr,
    revenue_cagr,
    pat_cagr,
    eps_cagr,
)
def test_normal_cagr():
    cagr, flag = calculate_cagr(100, 200, 5)
    assert round(cagr, 2) == 14.87
    assert flag is None


def test_decline_to_loss():
    cagr, flag = calculate_cagr(100, -50, 5)
    assert cagr is None
    assert flag == "DECLINE_TO_LOSS"


def test_turnaround():
    cagr, flag = calculate_cagr(-100, 50, 5)
    assert cagr is None
    assert flag == "TURNAROUND"


def test_both_negative():
    cagr, flag = calculate_cagr(-100, -50, 5)
    assert cagr is None
    assert flag == "BOTH_NEGATIVE"


def test_zero_base():
    cagr, flag = calculate_cagr(0, 100, 5)
    assert cagr is None
    assert flag == "ZERO_BASE"


def test_insufficient_years():
    cagr, flag = calculate_cagr(100, 200, 0)
    assert cagr is None
    assert flag == "INSUFFICIENT"


def test_revenue_cagr():
    cagr, flag = revenue_cagr(100, 200, 5)
    assert round(cagr, 2) == 14.87
    assert flag is None


def test_pat_cagr():
    cagr, flag = pat_cagr(100, 200, 5)
    assert round(cagr, 2) == 14.87
    assert flag is None


def test_eps_cagr():
    cagr, flag = eps_cagr(100, 200, 5)
    assert round(cagr, 2) == 14.87
    assert flag is None


def test_ten_year_cagr():
    cagr, flag = calculate_cagr(100, 300, 10)
    assert round(cagr, 2) == 11.61
    assert flag is None