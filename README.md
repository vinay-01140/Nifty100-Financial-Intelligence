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

Day 08 – Profitability Ratios

Implemented the initial financial ratio engine in src/analytics/ratios.py.

Implemented Ratios
Net Profit Margin (NPM)
Operating Profit Margin (OPM)
Return on Equity (ROE)
Return on Capital Employed (ROCE)
Return on Assets (ROA)
Features
Implemented Net Profit Margin calculation:
Formula: (Net Profit / Sales) × 100
Returns None when sales is zero.
Implemented Operating Profit Margin calculation:
Formula: (Operating Profit / Sales) × 100
Added OPM cross-check to compare calculated value with the source opm_percentage.
Detects mismatches when the difference exceeds 1%.
Implemented Return on Equity (ROE):
Formula: Net Profit / (Equity Capital + Reserves) × 100
Returns None when total equity is less than or equal to zero.
Implemented Return on Capital Employed (ROCE):
Formula: EBIT / (Equity + Reserves + Borrowings) × 100
Returns None when capital employed is less than or equal to zero.
Implemented Return on Assets (ROA):
Formula: Net Profit / Total Assets × 100
Returns None when total assets is zero.
Unit Testing

Created tests/test_ratios.py with 8 unit tests covering:

Normal calculation scenarios
Zero denominator handling
Negative equity handling
OPM mismatch detection
ROCE calculation
ROA zero-assets case
Test Result
Total Tests: 8
Passed: 8
Failed: 0

## Sprint 2 – Financial Ratio Engine

### Day 09 – Leverage & Efficiency Ratios

Implemented leverage and efficiency ratio calculations in `src/analytics/ratios.py`.

#### Implemented Ratios
- Debt-to-Equity (D/E)
- Interest Coverage Ratio (ICR)
- Net Debt
- Asset Turnover

#### Features
- Implemented Debt-to-Equity calculation with debt-free handling.
- Added High Leverage flag for non-financial companies with D/E > 5.
- Implemented Interest Coverage Ratio with "Debt Free" label for zero-interest companies.
- Added ICR warning flag for companies with ICR < 1.5.
- Implemented Net Debt and Asset Turnover calculations.

#### Unit Testing
Added 8 unit tests covering:
- Debt-free D/E
- High leverage flag
- ICR normal and zero-interest cases
- Debt Free label
- ICR warning
- Net Debt
- Asset Turnover

#### Test Result
- Total Tests: **16**
- Passed: **16**
- Failed: **0**

Day 09 completed successfully.

## Sprint 2 – Financial Ratio Engine

### Day 10 – CAGR Engine

Implemented the CAGR Engine in `src/analytics/cagr.py` for calculating Revenue, PAT, and EPS growth rates.

#### Features
- Implemented generic CAGR calculation formula.
- Added Revenue CAGR, PAT CAGR, and EPS CAGR functions.
- Handled all required CAGR edge cases:
  - Positive to Positive
  - Positive to Negative
  - Negative to Positive
  - Negative to Negative
  - Zero Base
  - Insufficient Data
- Returned both CAGR value and corresponding status flag.

#### Unit Testing
- Added 10 unit tests covering normal calculations and all edge cases.

#### Test Result
- Total Tests: **26**
- Passed: **26**
- Failed: **0**

Day 10 completed successfully.
## Sprint 2 – Financial Ratio Engine

### Day 11 – Cash Flow KPIs & Capital Allocation

Implemented cash flow KPIs and capital allocation analysis in `src/analytics/ratios.py`.

#### Implemented KPIs
- Free Cash Flow (FCF)
- CFO Quality Score
- CapEx Intensity
- FCF Conversion Rate
- Capital Allocation Pattern Classifier

#### Features
- Implemented Free Cash Flow calculation with support for negative values.
- Added CFO Quality Score with quality classification (High Quality, Moderate, Accrual Risk).
- Implemented CapEx Intensity with Asset Light, Moderate, and Capital Intensive classifications.
- Added FCF Conversion Rate with zero operating profit handling.
- Implemented capital allocation pattern classification using CFO, CFI, and CFF cash flow signs.

#### Unit Testing
- Added 8 unit tests covering cash flow calculations, classifications, and edge cases.

#### Test Result
- Total Tests: **34**
- Passed: **34**
- Failed: **0**

Day 11 completed successfully.