import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    check_opm_difference,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
    debt_to_equity,
    high_leverage_flag,
    interest_coverage_ratio,
    icr_label,
    icr_warning_flag,
    net_debt,
    asset_turnover,
)

def test_net_profit_margin():
    assert net_profit_margin(200, 1000) == 20.0


def test_net_profit_margin_zero_sales():
    assert net_profit_margin(100, 0) is None


def test_operating_profit_margin():
    assert operating_profit_margin(250, 1000) == 25.0


def test_opm_difference():
    assert check_opm_difference(25.0, 23.0) is True


def test_return_on_equity():
    assert return_on_equity(100, 300, 200) == 20.0


def test_return_on_equity_negative():
    assert return_on_equity(100, -50, 20) is None


def test_return_on_capital_employed():
    assert return_on_capital_employed(150, 300, 200, 250) == 20.0


def test_return_on_assets():
    assert return_on_assets(100, 0) is None
    
def test_debt_to_equity():
    assert debt_to_equity(200, 300, 100) == 0.5


def test_debt_to_equity_debt_free():
    assert debt_to_equity(0, 300, 100) == 0


def test_high_leverage_flag():
    assert high_leverage_flag(6, "Information Technology") is True


def test_interest_coverage_ratio():
    assert interest_coverage_ratio(200, 50, 50) == 5.0


def test_interest_coverage_ratio_zero_interest():
    assert interest_coverage_ratio(200, 50, 0) is None


def test_icr_label():
    assert icr_label(None) == "Debt Free"


def test_net_debt():
    assert net_debt(500, 150) == 350


def test_asset_turnover():
    assert asset_turnover(1000, 500) == 2.0