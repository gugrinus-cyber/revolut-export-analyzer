# Revolut Export Analyzer

A small privacy-first Python utility for analyzing a **local Revolut CSV export**.

## What it does

The script aggregates transactions by currency, category, month, and transaction type, then writes a Markdown report. It detects common export column names and supports explicit column overrides.

## What it does not do

It does not log in to Revolut, scrape Revolut pages, bypass controls, upload data, call a Revolut API, or send financial information to any external service. Run it only on an export you are authorized to process.

## Usage

```bash
python3 revolut_analyzer.py path/to/revolut_export.csv --output revolut_report.md
```

If the export uses different headers:

```bash
python3 revolut_analyzer.py export.csv \
  --date-column "Completed Date" \
  --amount-column "Amount" \
  --currency-column "Currency" \
  --category-column "Category"
```

The report is intended for personal budgeting and research workflows. It is not tax advice, accounting advice, or financial advice.

## Privacy notes

Keep the raw CSV out of Git. Add it to `.gitignore`, inspect generated reports before sharing, and remove personal merchant names, account identifiers, and transaction references if the report will be published.

## License

MIT
