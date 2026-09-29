from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import datetime
from pathlib import Path

BASE_FORMATS = (
    "%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d",
    "%Y-%m-%d %H:%M:%S", "%Y/%m/%d %H:%M:%S",
    "%Y%m%d", "%d-%b-%Y", "%d %b %Y", "%b %d, %Y",
)
DAY_FIRST = ("%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y")
MONTH_FIRST = ("%m/%d/%Y", "%m-%d-%Y", "%m.%d.%Y")


def parse_date(value: str, day_first: bool = False) -> datetime:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError("empty date")
    formats = BASE_FORMATS + (DAY_FIRST if day_first else MONTH_FIRST) + (MONTH_FIRST if day_first else DAY_FIRST)
    for fmt in formats:
        try:
            return datetime.strptime(cleaned, fmt)
        except ValueError:
            continue
    iso_value = cleaned.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(iso_value)
    except ValueError as exc:
        raise ValueError(f"unsupported date: {value}") from exc


def normalize_value(value: str, output_format: str = "%Y-%m-%d", day_first: bool = False) -> str:
    return parse_date(value, day_first).strftime(output_format)


def detect_dialect(path: Path, encoding: str) -> csv.Dialect:
    sample = path.read_text(encoding=encoding)[:8192]
    try:
        return csv.Sniffer().sniff(sample, delimiters=",;\t|")
    except csv.Error:
        return csv.excel


def normalize_csv(source: Path, destination: Path, column: str, output_column: str | None = None,
                  output_format: str = "%Y-%m-%d", day_first: bool = False,
                  encoding: str = "utf-8-sig", strict: bool = False) -> dict:
    dialect = detect_dialect(source, encoding)
    invalid = []
    converted = 0
    output_column = output_column or column
    with source.open("r", encoding=encoding, newline="") as src:
        reader = csv.DictReader(src, dialect=dialect)
        if not reader.fieldnames or column not in reader.fieldnames:
            raise ValueError(f"Column not found: {column}")
        fields = list(reader.fieldnames)
        if output_column not in fields:
            fields.append(output_column)
        rows = []
        for line, row in enumerate(reader, 2):
            original = row.get(column) or ""
            try:
                row[output_column] = normalize_value(original, output_format, day_first)
                converted += 1
            except ValueError as exc:
                invalid.append({"line": line, "value": original, "error": str(exc)})
                if strict:
                    raise ValueError(f"Line {line}: {exc}") from exc
                row[output_column] = original
            rows.append(row)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="") as dst:
        writer = csv.DictWriter(dst, fieldnames=fields, delimiter=dialect.delimiter)
        writer.writeheader()
        writer.writerows(rows)
    return {"rows": len(rows), "converted": converted, "invalid": invalid, "output_column": output_column}


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize mixed date formats in a CSV column.")
    parser.add_argument("source")
    parser.add_argument("destination")
    parser.add_argument("--column", required=True)
    parser.add_argument("--output-column", help="Keep the original column and write normalized dates to a new column")
    parser.add_argument("--format", default="%Y-%m-%d", help="Python strftime output format")
    parser.add_argument("--day-first", action="store_true", help="Prefer DD/MM/YYYY for ambiguous numeric dates")
    parser.add_argument("--strict", action="store_true", help="Stop at the first invalid date")
    parser.add_argument("--encoding", default="utf-8-sig")
    parser.add_argument("--report", help="Write invalid values to JSON")
    args = parser.parse_args()
    report = normalize_csv(Path(args.source), Path(args.destination), args.column, args.output_column,
                           args.format, args.day_first, args.encoding, args.strict)
    print(f"Rows: {report['rows']}; converted: {report['converted']}; invalid: {len(report['invalid'])}")
    print(f"Output: {Path(args.destination).resolve()}")
    if report["invalid"]:
        for item in report["invalid"][:10]:
            print(f"  Line {item['line']}: {item['value']!r} ({item['error']})")
    if args.report:
        Path(args.report).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

if __name__ == "__main__": main()
