"""Non-finite negative controls for the moved-D left-root checker."""
import unittest
from unittest import mock

import numpy as np

from tools import check_original_moved_julia_left as checker


class NonFiniteControls(unittest.TestCase):
    def test_nonfinite_boost_fails_closed(self):
        with mock.patch.object(checker, "expm", return_value=np.full((16, 16), np.nan)):
            with self.assertRaisesRegex(ValueError, "non-finite analytic boost"):
                checker.main()

    def test_nonfinite_eigenvalue_fails_closed(self):
        with mock.patch.object(checker.np.linalg, "eigvalsh", return_value=np.array([np.nan])):
            with self.assertRaisesRegex(ValueError, "non-finite minimum defect eigenvalue"):
                checker.main()

    def test_nonfinite_source_root_fails_closed(self):
        original_eigh = checker.np.linalg.eigh

        def nonfinite_eigh(matrix):
            values, vectors = original_eigh(matrix)
            vectors[0, 0] = np.nan
            return values, vectors

        with mock.patch.object(checker.np.linalg, "eigh", side_effect=nonfinite_eigh):
            with self.assertRaisesRegex(ValueError, "non-finite original root"):
                checker.main()


if __name__ == "__main__":
    unittest.main()
