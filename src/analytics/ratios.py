"""
Financial Ratio Engine

This module contains functions to calculate
financial ratios for the Nifty100 Financial Intelligence project.
"""
def net_profit_margin(net_profit, sales):
    """
    Calculate Net Profit Margin.

    Formula:
        (Net Profit / Sales) * 100

    Returns:
        float: Net Profit Margin
        None : If sales is zero
    """

    if sales == 0:
        return None

    return (net_profit / sales) * 100
def operating_profit_margin(operating_profit, sales):
    """
    Calculate Operating Profit Margin.

    Formula:
        (Operating Profit / Sales) * 100

    Returns:
        float: Operating Profit Margin
        None : If sales is zero
    """

    if sales == 0:
        return None

    return (operating_profit / sales) * 100
def check_opm_difference(calculated_opm, opm_percentage):
    """
    Check whether calculated OPM differs from the
    source OPM by more than 1%.

    Returns:
        True  -> Difference > 1%
        False -> Difference <= 1%
    """

    if calculated_opm is None or opm_percentage is None:
        return False

    return abs(calculated_opm - opm_percentage) > 1
def return_on_equity(net_profit, equity_capital, reserves):
    """
    Calculate Return on Equity (ROE).

    Formula:
        Net Profit / (Equity Capital + Reserves) * 100

    Returns:
        float: ROE
        None : If equity + reserves <= 0
    """

    total_equity = equity_capital + reserves

    if total_equity <= 0:
        return None

    return (net_profit / total_equity) * 100
def return_on_capital_employed(ebit, equity_capital, reserves, borrowings):
    """
    Calculate Return on Capital Employed (ROCE).

    Formula:
        EBIT / (Equity + Reserves + Borrowings) * 100
    """

    capital_employed = equity_capital + reserves + borrowings

    if capital_employed <= 0:
        return None

    return (ebit / capital_employed) * 100
def return_on_assets(net_profit, total_assets):
    """
    Calculate Return on Assets (ROA).

    Formula:
        Net Profit / Total Assets * 100

    Returns:
        float: ROA
        None : If total assets is zero
    """

    if total_assets == 0:
        return None

    return (net_profit / total_assets) * 100
