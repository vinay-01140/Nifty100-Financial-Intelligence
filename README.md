# Nifty100 Financial Intelligence

## Project Overview

Nifty100 Financial Intelligence is a financial data engineering and analytics project built on Nifty 100 company data. The goal of the project is to collect, clean, validate, and store company financial data in a structured SQLite database for further analysis, reporting, dashboards, and APIs.

Sprint 1 focused on building the **data foundation** of the project by creating the ETL pipeline, validation rules, and SQLite database.

---

## Sprint 1 Features

* ETL pipeline to load **12 Excel source files**
* SQLite database creation (`nifty100.db`)
* Data normalization for company tickers and year fields
* **16 data quality rules** (`DQ-01` to `DQ-16`)
* Load audit generation (`output/load_audit.csv`)
* Validation failure report (`output/validation_failures.csv`)
* Deduplication of annual financial records
* Foreign key integrity checks
* Exploratory SQL queries for review

---

## Project Structure

```text
Nifty100-Financial-Intelligence/
│── data/
│   ├── raw/
│   └── supporting/
│
│── db/
│   └── schema.sql
│
│── notebooks/
│   └── exploratory_queries.sql
│
│── output/
│   ├── load_audit.csv
│   └── validation_failures.csv
│
│── src/
│   └── etl/
│       ├── loader.py
│       ├── validator.py
│       └── normaliser.py
│
│── tests/
│   └── etl/
│
│── nifty100.db
│── requirements.txt
│── README.md
```

---

## Source Files

### Raw files

* `companies.xlsx`
* `profitandloss.xlsx`
* `balancesheet.xlsx`
* `cashflow.xlsx`
* `analysis.xlsx`
* `documents.xlsx`
* `prosandcons.xlsx`

### Supporting files

* `stock_prices.xlsx`
* `financial_ratios.xlsx`
* `market_cap.xlsx`
* `sectors.xlsx`
* `peer_groups.xlsx`

---

## Database Tables

* `companies`
* `profitandloss`
* `balancesheet`
* `cashflow`
* `analysis`
* `documents`
* `prosandcons`
* `stock_prices`
* `financial_ratios`
* `market_cap`
* `sectors`
* `peer_groups`

---

## Tech Stack

* Python
* Pandas
* SQLite
* Pytest
* OpenPyXL
* Jupyter Notebook

---

## How to Run

### 1. Create virtual environment

```bash
python -m venv venv
```

### 2. Activate virtual environment

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run validator

```bash
python src/etl/validator.py
```

### 5. Run loader

```bash
python src/etl/loader.py
```

---

## Sprint 1 Outputs

* `nifty100.db`
* `output/load_audit.csv`
* `output/validation_failures.csv`
* `notebooks/exploratory_queries.sql`

---

## Final Sprint 1 Loaded State

| Table            | Loaded Rows |
| ---------------- | ----------: |
| companies        |          92 |
| profitandloss    |        1073 |
| balancesheet     |        1058 |
| cashflow         |        1063 |
| analysis         |          16 |
| documents        |        1457 |
| prosandcons      |          14 |
| stock_prices     |        5520 |
| financial_ratios |        1041 |
| market_cap       |         552 |
| sectors          |          92 |
| peer_groups      |          56 |

---

## Key Notes

* Foreign key integrity check passed with **0 violations**
* `AGTL` was mapped to `ATGL` during loading as a valid alias fix
* Some child-table company IDs were not present in `companies.xlsx`, so those rows were rejected to preserve referential integrity
* `JIOFIN` has limited historical coverage in the source data
* `SBIN` has no balance sheet rows in the source file

---

## Sprint 1 Conclusion

Sprint 1 successfully established the **data foundation** for the Nifty100 Financial Intelligence project. The project now has a validated SQLite database, ETL loading scripts, data quality validation rules, audit outputs, and exploratory SQL queries ready for future analytics modules.
