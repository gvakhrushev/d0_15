"""Negative controls for non-finite results in the scoped source checker."""
import unittest
from unittest import mock

import numpy as np

from tools import check_original_static_julia_roots as checker


class NonFiniteControls(unittest.TestCase):
    def test_nonfinite_eigenvalue_fails_closed(self):
        with mock.patch.object(checker.np.linalg, "eigvalsh", return_value=np.array([np.nan])):
            with self.assertRaisesRegex(ValueError, "non-finite minimum defect eigenvalue"):
                checker.main()

    def test_nonfinite_original_root_fails_closed(self):
        original_eigh = checker.np.linalg.eigh

        def nonfinite_eigh(matrix):
            values, vectors = original_eigh(matrix)
            vectors[0, 0] = np.nan
            return values, vectors

        with mock.patch.object(checker.np.linalg, "eigh", side_effect=nonfinite_eigh):
            with self.assertRaisesRegex(ValueError, "non-finite original root"):
                checker.main()

    def test_nonfinite_wrong_sign_reference_fails_closed(self):
        wrong = np.eye(2)
        reference = np.eye(2)
        reference[0, 0] = np.nan
        with self.assertRaisesRegex(ValueError, "non-finite wrong-sign reference"):
            checker.check_wrong_sign(wrong, reference)


if __name__ == "__main__":
    unittest.main()
