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