import csv
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from date_normalizer.cli import normalize_csv, normalize_value

class DateNormalizerTests(unittest.TestCase):
    def test_common_formats_and_preference(self):
        self.assertEqual(normalize_value("20260928"), "2026-09-28")
        self.assertEqual(normalize_value("28/09/2026", day_first=True), "2026-09-28")
        self.assertEqual(normalize_value("09/28/2026"), "2026-09-28")
        self.assertEqual(normalize_value("2026-09-28T10:30:00"), "2026-09-28")

    def test_csv_preserves_invalid_and_new_column(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, target = root / "input.csv", root / "output.csv"
            source.write_text("id,date\n1,2026/09/28\n2,not-a-date\n", encoding="utf-8")
            report = normalize_csv(source, target, "date", "normalized", encoding="utf-8")
            self.assertEqual(report["converted"], 1)
            self.assertEqual(len(report["invalid"]), 1)
            with target.open(encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(rows[0]["normalized"], "2026-09-28")
            self.assertEqual(rows[1]["normalized"], "not-a-date")

if __name__ == "__main__": unittest.main()
