"""Non-finite negative controls for the ordered Julia pair comparison."""
import unittest

import numpy as np

from tools import check_original_julia_words as checker


class PairControls(unittest.TestCase):
    def test_nonfinite_source_pair_fails_closed(self):
        actual = np.zeros((2, 16, 16))
        actual[0, 0, 0] = np.nan
        with self.assertRaisesRegex(ValueError, "non-finite source pair"):
            checker.pair_error(actual, np.zeros_like(actual))

    def test_nonfinite_expected_pair_fails_closed(self):
        expected = np.zeros((2, 16, 16))
        expected[1, 0, 0] = np.nan
        with self.assertRaisesRegex(ValueError, "non-finite expected pair"):
            checker.pair_error(np.zeros_like(expected), expected)

    def test_finite_operands_with_overflow_fail_closed(self):
        actual = np.full((2, 16, 16), 1e308)
        expected = np.full((2, 16, 16), -1e308)
        with np.errstate(over="ignore"):
            with self.assertRaisesRegex(ValueError, "non-finite pair error"):
                checker.pair_error(actual, expected)


if __name__ == "__main__":
    unittest.main()
