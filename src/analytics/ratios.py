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
def debt_to_equity(borrowings, equity_capital, reserves):
    """
    Calculate Debt-to-Equity Ratio.

    Formula:
        Borrowings / (Equity Capital + Reserves)

    Returns:
        float: Debt-to-Equity Ratio
        0    : If borrowings is zero
        None : If equity + reserves <= 0
    """

    if borrowings == 0:
        return 0

    total_equity = equity_capital + reserves

    if total_equity <= 0:
        return None

    return borrowings / total_equity
def high_leverage_flag(debt_to_equity_ratio, broad_sector):
    """
    Check whether a company has high leverage.

    Returns:
        True  : If D/E > 5 and company is not in Financials sector
        False : Otherwise
    """

    if debt_to_equity_ratio is None:
        return False

    return debt_to_equity_ratio > 5 and broad_sector != "Financials"
def interest_coverage_ratio(operating_profit, other_income, interest):
    """
    Calculate Interest Coverage Ratio (ICR).

    Formula:
        (Operating Profit + Other Income) / Interest

    Returns:
        float: Interest Coverage Ratio
        None : If interest is zero
    """

    if interest == 0:
        return None

    return (operating_profit + other_income) / interest
def icr_label(icr):
    """
    Return display label for Interest Coverage Ratio.
    """

    if icr is None:
        return "Debt Free"

    return ""
def icr_warning_flag(icr):
    """
    Check whether company has low interest coverage.
    """

    if icr is None:
        return False

    return icr < 1.5
def net_debt(borrowings, investments):
    """
    Calculate Net Debt.

    Formula:
        Borrowings - Investments
    """

    return borrowings - investments
def asset_turnover(sales, total_assets):
    """
    Calculate Asset Turnover Ratio.

    Formula:
        Sales / Total Assets

    Returns:
        float: Asset Turnover Ratio
        None : If total assets is zero
    """

    if total_assets == 0:
        return None

    return sales / total_assets
def free_cash_flow(operating_activity, investing_activity):
    """
    Calculate Free Cash Flow (FCF).

    Formula:
        Operating Activity + Investing Activity

    Returns:
        float: Free Cash Flow
    """

    return operating_activity + investing_activity
def cfo_quality_score(cfo, pat):
    """
    Calculate CFO Quality Score.

    Formula:
        CFO / PAT

    Returns:
        tuple: (score, quality)
        None : If PAT is zero
    """

    if pat == 0:
        return None, None

    score = cfo / pat

    if score > 1.0:
        quality = "High Quality"
    elif score >= 0.5:
        quality = "Moderate"
    else:
        quality = "Accrual Risk"

    return score, quality
def capex_intensity(investing_activity, sales):
    """
    Calculate CapEx Intensity.

    Formula:
        abs(Investing Activity) / Sales * 100

    Returns:
        tuple: (capex_intensity, category)
        None : If sales is zero
    """

    if sales == 0:
        return None, None

    intensity = (abs(investing_activity) / sales) * 100

    if intensity < 3:
        category = "Asset Light"
    elif intensity <= 8:
        category = "Moderate"
    else:
        category = "Capital Intensive"

    return intensity, category
def fcf_conversion_rate(free_cash_flow, operating_profit):
    """
    Calculate Free Cash Flow Conversion Rate.

    Formula:
        (Free Cash Flow / Operating Profit) * 100

    Returns:
        float: FCF Conversion Rate
        None : If operating profit is zero
    """

    if operating_profit == 0:
        return None

    return (free_cash_flow / operating_profit) * 100
def capital_allocation_pattern(cfo, cfi, cff, cfo_quality=None):
    """
    Classify capital allocation pattern based on
    Operating, Investing and Financing cash flows.
    """

    cfo_sign = "+" if cfo >= 0 else "-"
    cfi_sign = "+" if cfi >= 0 else "-"
    cff_sign = "+" if cff >= 0 else "-"

    pattern = (cfo_sign, cfi_sign, cff_sign)

    if pattern == ("+", "-", "-"):
        if cfo_quality == "High Quality":
            label = "Shareholder Returns"
        else:
            label = "Reinvestor"

    elif pattern == ("+", "+", "-"):
        label = "Liquidating Assets"

    elif pattern == ("-", "+", "+"):
        label = "Distress Signal"

    elif pattern == ("-", "-", "+"):
        label = "Growth Funded by Debt"

    elif pattern == ("+", "+", "+"):
        label = "Cash Accumulator"

    elif pattern == ("-", "-", "-"):
        label = "Pre-Revenue"

    elif pattern == ("+", "-", "+"):
        label = "Mixed"

    else:
        label = "Unknown"

    return cfo_sign, cfi_sign, cff_sign, label

