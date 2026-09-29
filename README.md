# Date Normalizer

[绠€浣撲腑鏂嘳(README.zh-CN.md)

Normalize mixed date formats in a CSV column while keeping invalid values visible for review.

## Features

- Supports ISO, slash, dot, compact, English-month, and datetime formats.
- Configurable output using Python `strftime` syntax.
- Can replace a column or write to a new output column.
- Preserves invalid values by default and reports their line numbers.
- Optional strict mode stops at the first invalid date.
- Day-first preference for ambiguous numeric dates.

## Install

```bash
git clone https://github.com/jellywong343-sys/date-normalizer.git
cd date-normalizer
python -m pip install -e .
```

## Usage

```bash
date-normalize examples/mixed-dates.csv normalized.csv --column event_date --day-first
date-normalize input.csv output.csv --column date --output-column normalized_date
date-normalize input.csv output.csv --column date --format "%Y/%m/%d" --report invalid.json
date-normalize input.csv output.csv --column date --strict
```

Ambiguous dates such as `03/04/2026` require a convention. By default month-first is preferred; use `--day-first` when appropriate.

The destination is replaced if it already exists. Keep backups of important source data.

## Tests

```bash
python -m unittest discover -s tests -v
```

## License

MIT

