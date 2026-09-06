#!/usr/bin/env python3
"""Analyze a local Revolut CSV export without contacting Revolut or any API.

The input file stays local. The output is a Markdown report with totals by
currency, category, month, and transaction type. Column names are detected
from common Revolut export variants and can be overridden with flags.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path


def pick(headers: list[str], candidates: list[str], explicit: str | None) -> str:
    if explicit:
        if explicit not in headers:
            raise ValueError(f"Column not found: {explicit}")
        return explicit
    normalized = {h.strip().lower(): h for h in headers}
    for candidate in candidates:
        if candidate.lower() in normalized:
            return normalized[candidate.lower()]
    raise ValueError(f"Could not detect a column. Available: {', '.join(headers)}")


def parse_amount(value: str) -> Decimal:
    cleaned = value.strip().replace(" ", "").replace(",", ".")
    for symbol in ("€", "$", "£"):
        cleaned = cleaned.replace(symbol, "")
    try:
        return Decimal(cleaned)
    except InvalidOperation as exc:
        raise ValueError(f"Invalid amount: {value!r}") from exc


def analyze(path: Path, date_col=None, amount_col=None, currency_col=None,
            category_col=None, type_col=None) -> str:
    with path.open(newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        raise ValueError("CSV contains no rows")
    headers = list(rows[0])
    date_col = pick(headers, ["Date", "Completed Date", "Transaction Date"], date_col)
    amount_col = pick(headers, ["Amount", "Value", "Amount (signed)"], amount_col)
    currency_col = pick(headers, ["Currency", "Base currency"], currency_col)
    category_col = pick(headers, ["Category", "Type"], category_col)
    type_col = pick(headers, ["Type", "Transaction type"], type_col) if type_col or any(h.lower() == "type" for h in headers) else None

    by_currency = defaultdict(Decimal)
    by_category = defaultdict(Decimal)
    by_month = defaultdict(Decimal)
    by_type = defaultdict(int)
    skipped = []
    for index, row in enumerate(rows, start=2):
        try:
            amount = parse_amount(row[amount_col])
            date_text = row[date_col].strip()[:10]
            month = date_text[:7] if len(date_text) >= 7 else "unknown"
            currency = (row[currency_col] or "unknown").strip() or "unknown"
            category = (row[category_col] or "uncategorized").strip() or "uncategorized"
            kind = (row[type_col] or "unknown").strip() if type_col else "unknown"
        except (KeyError, ValueError) as exc:
            skipped.append(f"row {index}: {exc}")
            continue
        by_currency[currency] += amount
        by_category[(currency, category)] += amount
        by_month[(currency, month)] += amount
        by_type[kind] += 1

    lines = [f"# Revolut Export Analysis\n", f"Source file: `{path.name}`", f"Rows read: **{len(rows)}**", f"Rows skipped: **{len(skipped)}**", "", "## Totals by currency", "", "| Currency | Net amount |", "|---|---:|"]
    lines += [f"| {cur} | {value:.2f} |" for cur, value in sorted(by_currency.items())]
    lines += ["", "## Totals by category", "", "| Currency | Category | Net amount |", "|---|---|---:|"]
    lines += [f"| {cur} | {cat} | {value:.2f} |" for (cur, cat), value in sorted(by_category.items())]
    lines += ["", "## Monthly totals", "", "| Currency | Month | Net amount |", "|---|---|---:|"]
    lines += [f"| {cur} | {month} | {value:.2f} |" for (cur, month), value in sorted(by_month.items())]
    lines += ["", "## Transaction types", "", "| Type | Rows |", "|---|---:|"]
    lines += [f"| {kind} | {count} |" for kind, count in sorted(by_type.items())]
    lines += ["", "> Privacy: this tool reads only a local export. It does not log in to Revolut, scrape pages, upload data, or call external APIs."]
    if skipped:
        lines += ["", "## Skipped rows", ""] + [f"- {item}" for item in skipped[:20]]
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Analyze a local Revolut CSV export")
    ap.add_argument("csv_file", type=Path)
    ap.add_argument("-o", "--output", type=Path, default=Path("revolut_report.md"))
    ap.add_argument("--date-column")
    ap.add_argument("--amount-column")
    ap.add_argument("--currency-column")
    ap.add_argument("--category-column")
    ap.add_argument("--type-column")
    args = ap.parse_args()
    report = analyze(args.csv_file, args.date_column, args.amount_column, args.currency_column, args.category_column, args.type_column)
    args.output.write_text(report, encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
