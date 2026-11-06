"""Non-finite controls for the scoped Walsh source comparison."""
import unittest

import numpy as np

from tools import check_original_walsh_rows as checker


class MatrixControls(unittest.TestCase):
    def test_nonfinite_source_fails_closed(self):
        actual = np.zeros((16, 16))
        actual[0, 0] = np.nan
        with self.assertRaisesRegex(ValueError, "non-finite source matrix"):
            checker.matrix_error(actual, np.zeros_like(actual))

    def test_nonfinite_expected_fails_closed(self):
        expected = np.zeros((16, 16))
        expected[0, 0] = np.nan
        with self.assertRaisesRegex(ValueError, "non-finite expected matrix"):
            checker.matrix_error(np.zeros_like(expected), expected)

    def test_finite_operands_with_overflow_fail_closed(self):
        with np.errstate(over="ignore"):
            with self.assertRaisesRegex(ValueError, "non-finite matrix error"):
                checker.matrix_error(np.full((16, 16), 1e308), np.full((16, 16), -1e308))


if __name__ == "__main__":
    unittest.main()
