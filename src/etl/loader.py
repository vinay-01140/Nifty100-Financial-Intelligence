import os
import sqlite3
from pathlib import Path

import pandas as pd

from normaliser import normalize_year, normalize_ticker

DB_PATH = "nifty100.db"
SCHEMA_PATH = "db/schema.sql"
RAW_PATH = "data/raw"
SUPPORTING_PATH = "data/supporting"
OUTPUT_PATH = "output"
ID_ALIAS_MAP = {
    "AGTL": "ATGL"
}
def apply_company_id_alias(value):
    value = normalize_ticker(value)
    if value in ID_ALIAS_MAP:
        return ID_ALIAS_MAP[value]
    return value

# =========================================================
# DB SETUP
# =========================================================
def create_database():
    if not Path(SCHEMA_PATH).exists():
        raise FileNotFoundError(f"Schema file not found: {SCHEMA_PATH}")

    if Path(DB_PATH).exists():
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    conn.executescript(schema_sql)
    conn.commit()
    conn.close()

    print(f"Database created successfully: {DB_PATH}")


# =========================================================
# LOAD EXCEL FILES
# =========================================================
def load_excel_files():
    data = {}

    # ---------- core raw files ----------
    data["companies"] = pd.read_excel(f"{RAW_PATH}/companies.xlsx", header=1)
    data["profitandloss"] = pd.read_excel(f"{RAW_PATH}/profitandloss.xlsx", header=1)
    data["balancesheet"] = pd.read_excel(f"{RAW_PATH}/balancesheet.xlsx", header=1)
    data["cashflow"] = pd.read_excel(f"{RAW_PATH}/cashflow.xlsx", header=1)
    data["analysis"] = pd.read_excel(f"{RAW_PATH}/analysis.xlsx", header=1)
    data["documents"] = pd.read_excel(f"{RAW_PATH}/documents.xlsx", header=1)
    data["prosandcons"] = pd.read_excel(f"{RAW_PATH}/prosandcons.xlsx", header=1)

    # ---------- supporting files ----------
    data["stock_prices"] = pd.read_excel(f"{SUPPORTING_PATH}/stock_prices.xlsx")
    data["financial_ratios"] = pd.read_excel(f"{SUPPORTING_PATH}/financial_ratios.xlsx")
    data["market_cap"] = pd.read_excel(f"{SUPPORTING_PATH}/market_cap.xlsx")
    data["peer_groups"] = pd.read_excel(f"{SUPPORTING_PATH}/peer_groups.xlsx")
    data["sectors"] = pd.read_excel(f"{SUPPORTING_PATH}/sectors.xlsx")

    return data


# =========================================================
# NORMALIZATION HELPERS
# =========================================================
def normalize_company_id_column(df, column_name="company_id"):
    if column_name in df.columns:
        df[column_name] = df[column_name].apply(apply_company_id_alias)
    return df


def normalize_companies_table(df):
    df = df.copy()
    df["id"] = df["id"].apply(normalize_ticker)
    return df


def normalize_year_column(df, year_col="year"):
    if year_col in df.columns:
        df[year_col] = df[year_col].apply(normalize_year)
    return df


def clean_documents_table(df):
    df = df.copy()

    # rename columns to match schema
    if "Year" in df.columns:
        df = df.rename(columns={"Year": "year"})
    if "Annual_Report" in df.columns:
        df = df.rename(columns={"Annual_Report": "annual_report"})

    df = normalize_company_id_column(df, "company_id")
    df = normalize_year_column(df, "year")

    # remove rows where year is invalid
    df = df[df["year"].notna()].copy()

    return df


def clean_peer_groups_table(df):
    df = df.copy()
    df = normalize_company_id_column(df, "company_id")

    if "is_benchmark" in df.columns:
        df["is_benchmark"] = df["is_benchmark"].astype(int)

    return df


# =========================================================
# DEDUP HELPERS
# =========================================================
def deduplicate_annual_table(df, table_name):
    """
    For annual company tables, keep the last occurrence
    of (company_id, year) after normalization.
    """
    df = df.copy()

    if "company_id" in df.columns:
        df["company_id"] = df["company_id"].apply(apply_company_id_alias)

    if "year" in df.columns:
        df["year"] = df["year"].apply(normalize_year)

    # drop rows where year couldn't be parsed
    df = df[df["year"].notna()].copy()

    before = len(df)

    df = df.drop_duplicates(subset=["company_id", "year"], keep="last").copy()

    after = len(df)
    removed = before - after

    print(f"{table_name}: removed {removed} duplicate annual rows")

    return df


# =========================================================
# CLEAN ALL TABLES
# =========================================================
def clean_all_tables(data):
    cleaned = {}

    # ---------- companies ----------
    cleaned["companies"] = normalize_companies_table(data["companies"])

    # ---------- annual core tables ----------
    cleaned["profitandloss"] = deduplicate_annual_table(data["profitandloss"], "profitandloss")
    cleaned["balancesheet"] = deduplicate_annual_table(data["balancesheet"], "balancesheet")
    cleaned["cashflow"] = deduplicate_annual_table(data["cashflow"], "cashflow")

    # ---------- analysis ----------
    analysis = data["analysis"].copy()
    analysis = normalize_company_id_column(analysis, "company_id")
    cleaned["analysis"] = analysis

    # ---------- documents ----------
    cleaned["documents"] = clean_documents_table(data["documents"])

    # ---------- prosandcons ----------
    prosandcons = data["prosandcons"].copy()
    prosandcons = normalize_company_id_column(prosandcons, "company_id")
    cleaned["prosandcons"] = prosandcons

    # ---------- stock_prices ----------
    stock_prices = data["stock_prices"].copy()
    stock_prices = normalize_company_id_column(stock_prices, "company_id")
    cleaned["stock_prices"] = stock_prices

    # ---------- financial_ratios ----------
    financial_ratios = data["financial_ratios"].copy()
    financial_ratios = deduplicate_annual_table(financial_ratios, "financial_ratios")
    cleaned["financial_ratios"] = financial_ratios

    # ---------- market_cap ----------
    market_cap = data["market_cap"].copy()
    market_cap = deduplicate_annual_table(market_cap, "market_cap")
    cleaned["market_cap"] = market_cap

    # ---------- sectors ----------
    sectors = data["sectors"].copy()
    sectors = normalize_company_id_column(sectors, "company_id")
    cleaned["sectors"] = sectors

    # ---------- peer_groups ----------
    cleaned["peer_groups"] = clean_peer_groups_table(data["peer_groups"])

    return cleaned


# =========================================================
# FILTER FK INVALID ROWS
# =========================================================
def filter_invalid_company_ids(df, valid_company_ids, table_name):
    """
    Remove rows whose company_id is not present in companies.id
    """
    if "company_id" not in df.columns:
        return df, 0

    before = len(df)
    df = df[df["company_id"].isin(valid_company_ids)].copy()
    after = len(df)

    rejected = before - after
    if rejected > 0:
        print(f"{table_name}: rejected {rejected} rows due to invalid company_id")

    return df, rejected


# =========================================================
# LOAD TABLES INTO SQLITE
# =========================================================
def load_tables_to_sqlite(cleaned_data):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")

    load_audit = []

    valid_company_ids = set(cleaned_data["companies"]["id"].dropna())

    load_order = [
        "companies",
        "profitandloss",
        "balancesheet",
        "cashflow",
        "analysis",
        "documents",
        "prosandcons",
        "stock_prices",
        "financial_ratios",
        "market_cap",
        "sectors",
        "peer_groups"
    ]

    for table_name in load_order:
        df = cleaned_data[table_name].copy()

        source_rows = len(df)
        rejected_rows = 0

        # filter invalid FK rows for child tables
        if table_name != "companies" and "company_id" in df.columns:
            df, fk_rejected = filter_invalid_company_ids(df, valid_company_ids, table_name)
            rejected_rows += fk_rejected

        loaded_rows = len(df)

        # load into sqlite
        df.to_sql(table_name, conn, if_exists="append", index=False)

        load_audit.append({
            "table_name": table_name,
            "source_rows": source_rows,
            "loaded_rows": loaded_rows,
            "rejected_rows": rejected_rows
        })

        print(f"Loaded {table_name}: {loaded_rows} rows")

    conn.commit()
    conn.close()

    return pd.DataFrame(load_audit)


# =========================================================
# SAVE LOAD AUDIT
# =========================================================
def save_load_audit(load_audit_df):
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    output_file = f"{OUTPUT_PATH}/load_audit.csv"
    load_audit_df.to_csv(output_file, index=False)
    print(f"\nLoad audit saved to: {output_file}")


# =========================================================
# VERIFY DATABASE
# =========================================================
def verify_database():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    tables = [
        "companies",
        "profitandloss",
        "balancesheet",
        "cashflow",
        "analysis",
        "documents",
        "prosandcons",
        "stock_prices",
        "financial_ratios",
        "market_cap",
        "sectors",
        "peer_groups"
    ]

    print("\nRow counts in database:")
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table}: {count}")

    print("\nForeign key check:")
    cursor.execute("PRAGMA foreign_key_check;")
    fk_rows = cursor.fetchall()

    if len(fk_rows) == 0:
        print("PASS - 0 foreign key violations")
    else:
        print(f"FAIL - {len(fk_rows)} foreign key violations")
        for row in fk_rows[:10]:
            print(row)

    conn.close()


# =========================================================
# MAIN
# =========================================================
def main():
    create_database()

    raw_data = load_excel_files()
    cleaned_data = clean_all_tables(raw_data)

    load_audit_df = load_tables_to_sqlite(cleaned_data)
    save_load_audit(load_audit_df)

    verify_database()


if __name__ == "__main__":
    main()