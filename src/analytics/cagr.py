"""
CAGR Engine

This module contains functions to calculate
Compound Annual Growth Rate (CAGR)
for revenue, profit, EPS and other metrics.

"""

def calculate_cagr(start_value, end_value, years):
    """
    Calculate Compound Annual Growth Rate (CAGR).

    Formula:
        ((End / Start) ** (1 / Years) - 1) * 100

    Returns:
        tuple: (cagr_value, flag)
    """

    if years <= 0:
        return None, "INSUFFICIENT"

    if start_value == 0:
        return None, "ZERO_BASE"

    if start_value > 0 and end_value < 0:
        return None, "DECLINE_TO_LOSS"

    if start_value < 0 and end_value > 0:
        return None, "TURNAROUND"

    if start_value < 0 and end_value < 0:
        return None, "BOTH_NEGATIVE"

    cagr = ((end_value / start_value) ** (1 / years) - 1) * 100

    return cagr, None
def revenue_cagr(start_revenue, end_revenue, years):
    """
    Calculate Revenue CAGR.
    """

    return calculate_cagr(start_revenue, end_revenue, years)

def pat_cagr(start_pat, end_pat, years):
    """
    Calculate PAT (Net Profit) CAGR.
    """

    return calculate_cagr(start_pat, end_pat, years)
def eps_cagr(start_eps, end_eps, years):
    """
    Calculate EPS CAGR.
    """

    return calculate_cagr(start_eps, end_eps, years)