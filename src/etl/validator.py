import os
import re
import pandas as pd
from normaliser import normalize_year, normalize_ticker

RAW_PATH = "data/raw"
OUTPUT_PATH = "output"


# =========================================================
# LOAD ALL CORE DATA
# =========================================================
def load_raw_data():
    companies = pd.read_excel(f"{RAW_PATH}/companies.xlsx", header=1)
    profitandloss = pd.read_excel(f"{RAW_PATH}/profitandloss.xlsx", header=1)
    balancesheet = pd.read_excel(f"{RAW_PATH}/balancesheet.xlsx", header=1)
    cashflow = pd.read_excel(f"{RAW_PATH}/cashflow.xlsx", header=1)
    analysis = pd.read_excel(f"{RAW_PATH}/analysis.xlsx", header=1)
    documents = pd.read_excel(f"{RAW_PATH}/documents.xlsx", header=1)
    prosandcons = pd.read_excel(f"{RAW_PATH}/prosandcons.xlsx", header=1)

    return {
        "companies": companies,
        "profitandloss": profitandloss,
        "balancesheet": balancesheet,
        "cashflow": cashflow,
        "analysis": analysis,
        "documents": documents,
        "prosandcons": prosandcons
    }


# =========================================================
# HELPER
# =========================================================
def add_failure(failures, table, row_index, rule_id, severity, message):
    failures.append({
        "table": table,
        "row_index": row_index,
        "rule_id": rule_id,
        "severity": severity,
        "message": message
    })


def normalize_company_column(df, col="company_id"):
    if col in df.columns:
        df[col] = df[col].apply(normalize_ticker)
    return df


# =========================================================
# DQ-01 : Company PK Uniqueness / id uniqueness in each table
# CRITICAL
# =========================================================
def dq_01_pk_uniqueness(data, failures):
    for table_name, df in data.items():
        if "id" not in df.columns:
            continue

        dupes = df[df["id"].duplicated(keep=False)]
        for idx, row in dupes.iterrows():
            add_failure(
                failures,
                table_name,
                idx,
                "DQ-01",
                "CRITICAL",
                f"Duplicate id={row['id']}"
            )


# =========================================================
# DQ-02 : Annual PK Uniqueness
# No duplicate (company_id, year) in P&L, BS, CF
# CRITICAL
# Deduplicate later in loader by keeping last occurrence
# =========================================================
def dq_02_annual_pk_uniqueness(data, failures):
    for table_name in ["profitandloss", "balancesheet", "cashflow"]:
        df = data[table_name].copy()

        if "company_id" not in df.columns or "year" not in df.columns:
            continue

        df["company_id"] = df["company_id"].apply(normalize_ticker)
        df["normalized_year"] = df["year"].apply(normalize_year)

        # Only validate rows where year parsed successfully
        valid_df = df[df["normalized_year"].notna()].copy()

        dupes = valid_df[
            valid_df.duplicated(subset=["company_id", "normalized_year"], keep=False)
        ]

        for idx, row in dupes.iterrows():
            add_failure(
                failures,
                table_name,
                idx,
                "DQ-02",
                "CRITICAL",
                f"Duplicate (company_id, year)=({row['company_id']}, {row['normalized_year']})"
            )


# =========================================================
# DQ-03 : FK Integrity
# All company_id in child tables must exist in companies.id
# CRITICAL
# =========================================================
def dq_03_fk_integrity(data, failures):
    companies_df = data["companies"].copy()

    valid_company_ids = set(
        companies_df["id"]
        .apply(normalize_ticker)
        .dropna()
    )

    child_tables = [
        "profitandloss",
        "balancesheet",
        "cashflow",
        "analysis",
        "documents",
        "prosandcons"
    ]

    for table_name in child_tables:
        df = data[table_name].copy()

        if "company_id" not in df.columns:
            continue

        df["company_id_norm"] = df["company_id"].apply(normalize_ticker)

        invalid_rows = df[~df["company_id_norm"].isin(valid_company_ids)]

        for idx, row in invalid_rows.iterrows():
            add_failure(
                failures,
                table_name,
                idx,
                "DQ-03",
                "CRITICAL",
                f"company_id '{row['company_id']}' not found in companies table"
            )
# =========================================================
# DQ-04 : Balance Sheet Balance
# |assets - liabilities| / assets < 0.01
# WARNING
# =========================================================
def dq_04_balance_sheet_balance(data, failures):
    df = data["balancesheet"]

    needed = ["total_assets", "total_liabilities"]
    if not all(col in df.columns for col in needed):
        return

    for idx, row in df.iterrows():
        assets = row["total_assets"]
        liabilities = row["total_liabilities"]

        if pd.isna(assets) or pd.isna(liabilities) or assets == 0:
            continue

        diff_ratio = abs(assets - liabilities) / abs(assets)

        if diff_ratio >= 0.01:
            add_failure(
                failures,
                "balancesheet",
                idx,
                "DQ-04",
                "WARNING",
                f"Balance sheet mismatch: assets={assets}, liabilities={liabilities}, diff_ratio={diff_ratio:.4f}"
            )


# =========================================================
# DQ-05 : OPM Cross Check
# |opm - (operating_profit/sales*100)| < 1.0
# WARNING
# =========================================================
def dq_05_opm_crosscheck(data, failures):
    df = data["profitandloss"]

    needed = ["sales", "operating_profit", "opm_percentage"]
    if not all(col in df.columns for col in needed):
        return

    for idx, row in df.iterrows():
        sales = row["sales"]
        op_profit = row["operating_profit"]
        opm = row["opm_percentage"]

        if pd.isna(sales) or pd.isna(op_profit) or pd.isna(opm):
            continue
        if sales == 0:
            continue

        expected_opm = (op_profit / sales) * 100

        if abs(opm - expected_opm) >= 1.0:
            add_failure(
                failures,
                "profitandloss",
                idx,
                "DQ-05",
                "WARNING",
                f"OPM mismatch: source={opm}, computed={expected_opm:.2f}"
            )


# =========================================================
# DQ-06 : Positive Sales
# sales > 0
# WARNING
# =========================================================
def dq_06_positive_sales(data, failures):
    df = data["profitandloss"]

    if "sales" not in df.columns:
        return

    invalid_rows = df[df["sales"] <= 0]

    for idx, row in invalid_rows.iterrows():
        add_failure(
            failures,
            "profitandloss",
            idx,
            "DQ-06",
            "WARNING",
            f"sales <= 0 ({row['sales']})"
        )


# =========================================================
# DQ-07 : Year Format
# After normalize_year(), value must be parseable
# CRITICAL
# =========================================================
def dq_07_year_format(data, failures):
    year_tables = {
        "profitandloss": "year",
        "balancesheet": "year",
        "cashflow": "year",
        "documents": "Year"
    }

    for table_name, year_col in year_tables.items():
        df = data[table_name]
        if year_col not in df.columns:
            continue

        for idx, row in df.iterrows():
            raw_value = row[year_col]
            parsed = normalize_year(raw_value)

            # allow TTM in financial tables only
            if str(raw_value).strip().upper() == "TTM" and table_name != "documents":
                continue

            if parsed is None:
                add_failure(
                    failures,
                    table_name,
                    idx,
                    "DQ-07",
                    "CRITICAL",
                    f"Unparseable year value: {raw_value}"
                )


# =========================================================
# DQ-08 : Ticker Format
# strip + upper, length 2-12
# CRITICAL if out of range
# =========================================================
def dq_08_ticker_format(data, failures):
    ticker_tables = [
        "companies",
        "profitandloss",
        "balancesheet",
        "cashflow",
        "analysis",
        "documents",
        "prosandcons"
    ]

    for table_name in ticker_tables:
        df = data[table_name]

        col = "id" if table_name == "companies" else "company_id"
        if col not in df.columns:
            continue

        for idx, row in df.iterrows():
            ticker = normalize_ticker(row[col])

            if ticker is None:
                add_failure(
                    failures,
                    table_name,
                    idx,
                    "DQ-08",
                    "CRITICAL",
                    f"{col} is null"
                )
                continue

            if len(ticker) < 2 or len(ticker) > 12:
                add_failure(
                    failures,
                    table_name,
                    idx,
                    "DQ-08",
                    "CRITICAL",
                    f"Invalid ticker length: {ticker}"
                )


# =========================================================
# DQ-09 : Net Cash Check
# |net_cash_flow - (CFO+CFI+CFF)| <= 10
# WARNING
# =========================================================
def dq_09_net_cash_check(data, failures):
    df = data["cashflow"]

    needed = ["operating_activity", "investing_activity", "financing_activity", "net_cash_flow"]
    if not all(col in df.columns for col in needed):
        return

    for idx, row in df.iterrows():
        cfo = row["operating_activity"]
        cfi = row["investing_activity"]
        cff = row["financing_activity"]
        net = row["net_cash_flow"]

        if pd.isna(cfo) or pd.isna(cfi) or pd.isna(cff) or pd.isna(net):
            continue

        expected = cfo + cfi + cff
        if abs(net - expected) > 10:
            add_failure(
                failures,
                "cashflow",
                idx,
                "DQ-09",
                "WARNING",
                f"net_cash_flow mismatch: source={net}, computed={expected}"
            )


# =========================================================
# DQ-10 : Non-Negative Fixed Assets
# fixed_assets >= 0
# WARNING
# =========================================================
def dq_10_non_negative_fixed_assets(data, failures):
    df = data["balancesheet"]

    if "fixed_assets" not in df.columns:
        return

    invalid_rows = df[df["fixed_assets"] < 0]

    for idx, row in invalid_rows.iterrows():
        add_failure(
            failures,
            "balancesheet",
            idx,
            "DQ-10",
            "WARNING",
            f"Negative fixed_assets={row['fixed_assets']}"
        )


# =========================================================
# DQ-11 : Tax Rate Range
# 0 <= tax_percentage <= 60
# WARNING
# =========================================================
def dq_11_tax_rate_range(data, failures):
    df = data["profitandloss"]

    if "tax_percentage" not in df.columns:
        return

    invalid_rows = df[
        df["tax_percentage"].notna() &
        ((df["tax_percentage"] < 0) | (df["tax_percentage"] > 60))
    ]

    for idx, row in invalid_rows.iterrows():
        add_failure(
            failures,
            "profitandloss",
            idx,
            "DQ-11",
            "WARNING",
            f"tax_percentage out of range: {row['tax_percentage']}"
        )


# =========================================================
# DQ-12 : Dividend Payout Cap
# dividend_payout <= 200
# WARNING
# =========================================================
def dq_12_dividend_payout_cap(data, failures):
    df = data["profitandloss"]

    if "dividend_payout" not in df.columns:
        return

    invalid_rows = df[
        df["dividend_payout"].notna() &
        (df["dividend_payout"] > 200)
    ]

    for idx, row in invalid_rows.iterrows():
        add_failure(
            failures,
            "profitandloss",
            idx,
            "DQ-12",
            "WARNING",
            f"dividend_payout > 200: {row['dividend_payout']}"
        )


# =========================================================
# DQ-13 : URL Validity
# requests.head(url).status_code == 200
# WARNING
# Note: slow rule
# =========================================================
def dq_13_url_validity(data, failures):
    df = data["documents"]

    if "Annual_Report" not in df.columns:
        return

    for idx, row in df.iterrows():
        url = row["Annual_Report"]

        if pd.isna(url) or str(url).strip() == "":
            add_failure(
                failures,
                "documents",
                idx,
                "DQ-13",
                "WARNING",
                "Annual_Report URL missing"
            )
            continue

        url = str(url).strip()

        if not (url.startswith("http://") or url.startswith("https://")):
            add_failure(
                failures,
                "documents",
                idx,
                "DQ-13",
                "WARNING",
                f"Invalid URL format: {url}"
            )
# =========================================================
# DQ-14 : EPS Sign Consistency
# if net_profit > 0 then eps should not be negative
# if net_profit < 0 then eps should not be positive
# WARNING
# =========================================================
def dq_14_eps_sign_consistency(data, failures):
    df = data["profitandloss"]

    needed = ["net_profit", "eps"]
    if not all(col in df.columns for col in needed):
        return

    for idx, row in df.iterrows():
        net_profit = row["net_profit"]
        eps = row["eps"]

        if pd.isna(net_profit) or pd.isna(eps):
            continue

        if net_profit > 0 and eps < 0:
            add_failure(
                failures,
                "profitandloss",
                idx,
                "DQ-14",
                "WARNING",
                f"net_profit={net_profit} but eps={eps}"
            )

        if net_profit < 0 and eps > 0:
            add_failure(
                failures,
                "profitandloss",
                idx,
                "DQ-14",
                "WARNING",
                f"net_profit={net_profit} but eps={eps}"
            )


# =========================================================
# DQ-15 : Strict Balance Equality
# total_assets == total_liabilities
# INFO
# =========================================================
def dq_15_strict_balance_info(data, failures):
    df = data["balancesheet"]

    needed = ["total_assets", "total_liabilities"]
    if not all(col in df.columns for col in needed):
        return

    for idx, row in df.iterrows():
        assets = row["total_assets"]
        liabilities = row["total_liabilities"]

        if pd.isna(assets) or pd.isna(liabilities):
            continue

        if assets != liabilities:
            add_failure(
                failures,
                "balancesheet",
                idx,
                "DQ-15",
                "INFO",
                f"Strict inequality: assets={assets}, liabilities={liabilities}"
            )


# =========================================================
# DQ-16 : Coverage Check
# Each company has >= 5 years in P&L, BS, CF
# WARNING
# =========================================================
def dq_16_coverage_check(data, failures):
    for table_name in ["profitandloss", "balancesheet", "cashflow"]:
        df = data[table_name].copy()

        if "company_id" not in df.columns or "year" not in df.columns:
            continue

        df["company_id"] = df["company_id"].apply(normalize_ticker)
        df["normalized_year"] = df["year"].apply(normalize_year)

        valid_df = df[df["normalized_year"].notna()].copy()

        coverage = valid_df.groupby("company_id")["normalized_year"].nunique()

        low_coverage = coverage[coverage < 5]

        for company_id, year_count in low_coverage.items():
            add_failure(
                failures,
                table_name,
                None,
                "DQ-16",
                "WARNING",
                f"{company_id} has only {year_count} years of data in {table_name}"
            )


# =========================================================
# RUN ALL
# =========================================================
def run_all_validations(data):
    failures = []

    dq_01_pk_uniqueness(data, failures)
    dq_02_annual_pk_uniqueness(data, failures)
    dq_03_fk_integrity(data, failures)
    dq_04_balance_sheet_balance(data, failures)
    dq_05_opm_crosscheck(data, failures)
    dq_06_positive_sales(data, failures)
    dq_07_year_format(data, failures)
    dq_08_ticker_format(data, failures)
    dq_09_net_cash_check(data, failures)
    dq_10_non_negative_fixed_assets(data, failures)
    dq_11_tax_rate_range(data, failures)
    dq_12_dividend_payout_cap(data, failures)
    dq_13_url_validity(data, failures)
    dq_14_eps_sign_consistency(data, failures)
    dq_15_strict_balance_info(data, failures)
    dq_16_coverage_check(data, failures)

    return pd.DataFrame(failures)


# =========================================================
# MAIN
# =========================================================
def main():
    os.makedirs(OUTPUT_PATH, exist_ok=True)

    data = load_raw_data()

    # normalize company_id columns before validation
    for table_name in ["profitandloss", "balancesheet", "cashflow", "analysis", "documents", "prosandcons"]:
        data[table_name] = normalize_company_column(data[table_name], "company_id")

    data["companies"]["id"] = data["companies"]["id"].apply(normalize_ticker)

    failures_df = run_all_validations(data)

    output_file = f"{OUTPUT_PATH}/validation_failures.csv"
    failures_df.to_csv(output_file, index=False)

    print("\nValidation completed")
    print(f"Total failures: {len(failures_df)}")
    print(f"Output saved to: {output_file}")

    if not failures_df.empty:
        print("\nFailure summary:")
        print(failures_df["rule_id"].value_counts().sort_index())
    else:
        print("No validation failures found.")


if __name__ == "__main__":
    main()