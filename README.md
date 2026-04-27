# TAXY-Z — AI-Prepared Tax Calculations Engine 🧾

> **Parse. Categorize. Report. Save.**
> The core engine that powers the TAXY-Z app — turning raw Chase bank statement PDFs into professional P&L reports and savings-opportunity analysis.

---

## What This Does

TAXY-Z reads Chase checking account PDF statements, extracts every transaction, intelligently categorizes each one, and produces:

- **Annual P&L Excel workbooks** — color-coded, month × category matrix with income, essential expenses, non-essential expenses, and net P&L
- **Non-Essential Spending Analysis** — identifies where money could have gone to savings instead
- **Multi-year comparison reports** — track trends across years

---

## File Structure

```
TAXY-Z/
├── pdf_parser.py            # Extract transactions from Chase PDF statements
├── categorizer.py           # Classify each transaction (essential vs non-essential)
├── excel_builder.py         # Build styled annual P&L Excel reports
├── non_essential_analyzer.py # Build savings-opportunity analysis reports
└── README.md
```

---

## Quick Start

```python
from pdf_parser import extract_all_months
from categorizer import categorize
from excel_builder import build_annual_report

# 1. Define your statement files
file_map = [
    ("January 2024",  "20240118-statements-0828-.pdf"),
    ("February 2024", "20240216-statements-0828-.pdf"),
    # ... etc
]

# 2. Extract transactions
txns_raw = extract_all_months("path/to/pdfs/", file_map)

# 3. Categorize each transaction
for t in txns_raw:
    t["category"] = categorize(t["desc"], t["amount"])

# 4. Build report
build_annual_report(
    all_months=[...],   # grouped by month
    year=2024,
    output_path="PL_2024.xlsx",
    income_cats=[...],
    expense_cats=[...],
)
```

---

## How Categorization Works

Each transaction goes through `categorize(desc, amount)` which applies 200+ pattern-matching rules against the raw bank description string.

Categories fall into four buckets:

| Bucket | Examples |
|--------|----------|
| **Income** | Business POS, deposits, Zelle received, interest |
| **Essential** | Mortgage, rent, utilities, insurance, groceries, health |
| **Non-Essential** | DoorDash, restaurants, shopping, travel, subscriptions |
| **Transfer/Neutral** | Zelle out, wire transfers, internal transfers, savings |

---

## Output Examples

### Annual P&L Report
- **14 tabs**: Annual Summary + All Transactions + 12 monthly sheets
- **Color-coded by category**: green = income, red = essential, yellow = non-essential
- **Frozen panes + auto-filter** on the transactions sheet

### Non-Essential Analysis
- **Summary tab**: P&L overview + potential savings calculation + category breakdown
- **Detail tab**: Every non-essential transaction, filterable by year/month/category
- **Year-by-year tabs**: Monthly breakdown with running totals

---

## Requirements

```
pip install pdfplumber openpyxl
```

---

## Supported Bank Format

Currently supports **Chase Total Checking** statements (PDF text format).

The parser expects the standard Chase line format:
```
MM/DD  Description text here  AMOUNT  BALANCE
```

---

## Data Processed (2021–2025)

| Year | Transactions | Income | Net |
|------|-------------|--------|-----|
| 2021 | 1,384 | $230,791 | -$12,072 |
| 2022 | 1,735 | $244,083 | +$34,064 |
| 2023 | 1,415 | $373,993 | +$12,049 |
| 2024 | 1,188 | $180,763 | -$43,787 |
| 2025 | 1,368 | $127,157 | +$11,999 |
| **Total** | **7,090** | **$1,156,787** | **+$2,253** |

---

## App Vision — TAXY-Z

This engine is the backend for the **TAXY-Z** app:
> Upload your bank statements → AI categorizes everything → Download your P&L + tax-ready report in minutes.

---

*Built with ❤️ by TAXY — your AI-powered financial co-pilot.*
