"""
TAXY-Z — PDF Statement Parser
================================
Extracts individual transactions from Chase bank statement PDFs.
Handles multi-page statements and normalizes amounts.

Usage:
    from pdf_parser import extract_transactions
    txns = extract_transactions("path/to/statement.pdf")
    # Returns list of dicts: {date, desc, amount}
"""

import re
import pdfplumber
from typing import List, Dict


def extract_transactions(pdf_path: str) -> List[Dict]:
    """
    Parse all transactions from a Chase checking account PDF statement.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        List of transaction dicts:
            {
                'date':   str   — MM/DD from statement
                'desc':   str   — raw description
                'amount': float — negative=expense, positive=income
            }
    """
    transactions = []

    with pdfplumber.open(pdf_path) as pdf:
        full_text = "\n".join(
            page.extract_text() or "" for page in pdf.pages
        )

    for line in full_text.split("\n"):
        line = line.strip()
        # Chase statement format:
        # MM/DD  Description  AMOUNT  BALANCE
        match = re.match(
            r"(\d{2}/\d{2})\s+(.+?)\s+(-?\d{1,3}(?:,\d{3})*\.\d{2})\s+[\d,]+\.\d{2}$",
            line,
        )
        if match:
            date   = match.group(1)
            desc   = match.group(2)
            amount = float(match.group(3).replace(",", ""))
            transactions.append({"date": date, "desc": desc, "amount": amount})

    return transactions


def extract_all_months(pdf_dir: str, file_map: List[tuple]) -> List[Dict]:
    """
    Extract transactions from a full year of monthly statements.

    Args:
        pdf_dir:  Directory containing PDF files
        file_map: List of (month_label, filename) tuples

    Returns:
        List of enriched transaction dicts (adds 'month' key)
    """
    all_txns = []
    for month_label, filename in file_map:
        path = f"{pdf_dir}/{filename}"
        try:
            txns = extract_transactions(path)
            for t in txns:
                t["month"] = month_label
            all_txns.extend(txns)
        except Exception as e:
            print(f"  Warning: could not parse {filename}: {e}")
    return all_txns
