# Revolut Export Analyzer

[![CI](https://github.com/gugrinus-cyber/revolut-export-analyzer/actions/workflows/ci.yml/badge.svg)](https://github.com/gugrinus-cyber/revolut-export-analyzer/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Privacy-first](https://img.shields.io/badge/Privacy--first-local--only-2E8B57)](#privacy-and-security)
[![Finance tooling](https://img.shields.io/badge/Focus-personal--finance-6f42c1)](#what-it-does)

> A small, privacy-first Python utility for analyzing a **local Revolut CSV export** without login, scraping, or external API calls.

## Why this project exists

Personal finance exports are useful for building repeatable analysis workflows, but they contain sensitive information. This project demonstrates a local-only data pipeline that turns an exported CSV into a readable Markdown report while keeping raw data on the user's machine.

## What it does

The script aggregates transactions by currency, category, month, and transaction type. It detects common export column names and supports explicit column overrides when an export format differs.

## Quick start

```bash
python3 revolut_analyzer.py path/to/revolut_export.csv --output revolut_report.md
```

For exports with custom headers:

```bash
python3 revolut_analyzer.py export.csv \
  --date-column "Completed Date" \
  --amount-column "Amount" \
  --currency-column "Currency" \
  --category-column "Category"
```

## Example output

The report includes:

- net totals by currency;
- totals by category;
- monthly totals;
- transaction-type counts;
- skipped rows requiring manual review.

## Privacy and security

The tool does **not** log in to Revolut, scrape Revolut pages, bypass controls, upload data, call a Revolut API, or send financial information to any external service. Run it only on an export you are authorized to process.

Keep raw CSV files out of Git, inspect generated reports before sharing, and remove personal merchant names, account identifiers, and transaction references if a report will be published.

This tool is for personal budgeting and research workflows. It is not tax advice, accounting advice, or financial advice.

## Recruiter signal

This project demonstrates local data processing, defensive privacy design, robust CSV handling, explicit error reporting, and a clear separation between raw sensitive input and shareable output.

## License

MIT
