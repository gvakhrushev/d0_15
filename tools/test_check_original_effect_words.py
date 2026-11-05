"""Finite negative controls for chronological no-reset effects."""
import unittest

import numpy as np

from tools import check_original_effect_words as checker


class EffectControls(unittest.TestCase):
    def setUp(self):
        a = np.array([[1, 0], [0, 0]], dtype=np.int64)
        b = np.array([[0, 1], [1, 0]], dtype=np.int64)
        zero = np.zeros((2, 2), dtype=np.int64)
        matrices = np.stack((a, b, zero))
        self.data = {"K": matrices, "Kd": matrices.transpose(0, 2, 1),
                     "I": np.eye(2, dtype=np.int64), "m": 1009}

    def test_empty_is_identity(self):
        self.assertTrue(np.array_equal(checker.chronological_product_effect((), self.data), self.data["I"]))

    def test_reversed_history_is_distinct(self):
        ab = checker.chronological_product_effect((0, 1), self.data)
        ba = checker.chronological_product_effect((1, 0), self.data)
        self.assertTrue(np.array_equal(ab, np.diag([1, 0])))
        self.assertTrue(np.array_equal(ba, np.diag([0, 1])))
        self.assertFalse(np.array_equal(ab, ba))

    def test_zero_slot_inside_word_gives_zero(self):
        self.assertFalse(np.any(checker.chronological_product_effect((0, 2, 1), self.data)))

    def test_invalid_indices_fail_closed(self):
        for bad in (-1, 3, True, 0.0):
            with self.subTest(bad=bad):
                with self.assertRaisesRegex(ValueError, "invalid Kraus slot"):
                    checker.chronological_product_effect((bad,), self.data)


if __name__ == "__main__":
    unittest.main()
