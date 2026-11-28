#!/usr/bin/env python3
"""Regression checks for malformed registry CSV records."""
import csv
import io
import unittest

from csv_integrity import record_width_errors


def records(text):
    return list(csv.DictReader(io.StringIO(text, newline="")))


class CsvIntegrityTest(unittest.TestCase):
    def test_quoted_commas_remain_one_field(self):
        rows = records('claim_id,notes\nD0-X,"first, second"\n')
        self.assertEqual(record_width_errors(rows), [])
        self.assertEqual(rows[0]["notes"], "first, second")

    def test_unquoted_extra_field_is_rejected(self):
        rows = records('claim_id,notes\nD0-X,first, second\n')
        self.assertEqual(record_width_errors(rows), [(2, "1 extra field(s)")])

    def test_short_row_is_rejected(self):
        rows = records('claim_id,notes\nD0-X\n')
        self.assertEqual(record_width_errors(rows), [(2, "missing field(s): notes")])


if __name__ == "__main__":
    unittest.main()
