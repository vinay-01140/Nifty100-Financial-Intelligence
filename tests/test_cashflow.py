import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.analytics.ratios import (
    free_cash_flow,
    cfo_quality_score,
    capex_intensity,
    fcf_conversion_rate,
    capital_allocation_pattern,
)
def test_free_cash_flow():
    assert free_cash_flow(500, -200) == 300


def test_negative_free_cash_flow():
    assert free_cash_flow(100, -250) == -150


def test_cfo_quality_high():
    score, quality = cfo_quality_score(120, 100)
    assert quality == "High Quality"


def test_cfo_quality_pat_zero():
    score, quality = cfo_quality_score(100, 0)
    assert score is None
    assert quality is None


def test_capex_intensity():
    intensity, category = capex_intensity(-20, 1000)
    assert category == "Asset Light"


def test_fcf_conversion_rate():
    assert fcf_conversion_rate(150, 300) == 50.0


def test_fcf_conversion_rate_zero():
    assert fcf_conversion_rate(100, 0) is None


def test_capital_allocation_pattern():
    cfo_sign, cfi_sign, cff_sign, label = capital_allocation_pattern(
        500, -200, -100
    )

    assert label == "Reinvestor"