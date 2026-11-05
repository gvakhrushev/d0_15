#!/usr/bin/env python3
"""Check only the original moved-D right Julia root against NumPy/SciPy.

Both copied source blobs are verified before the complete uniform source is
imported. It is trusted code, not a sandbox. This numerical check does not
establish the full 128 Kraus operators, their span, or physical admission.
"""
from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
import tempfile

import numpy as np
from scipy.linalg import expm

SOURCE_COMMIT = "eebcb5e467742df3e9cf7fa9702042d7294aa742"
UNIFORM_BLOB = "ee8de4635d24c668949ac9a0186616ab7d59f2ed"
MODULAR_BLOB = "d111c5bfeae3c384a4fe725f4a6d19277ea0005a"
COPIES = Path(__file__).resolve().parents[1] / (
    "02_REGISTRY/research/sources/d0_proof_architecture_car_creator_bridge_2026-11-04"
)
TOLERANCE = 1e-12


def pinned_bytes(name: str, expected: str) -> bytes:
    data = (COPIES / name).read_bytes()
    digest = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    if digest != expected:
        raise ValueError(f"Git blob mismatch for {name}: {digest}")
    return data


def require_finite(value: object, label: str) -> None:
    if not np.isfinite(value).all():
        raise ValueError(f"non-finite {label}")


def main() -> None:
    data = pinned_bytes("check_uniform_book_source.py", UNIFORM_BLOB)
    pinned_bytes("check_future_even_algebra_modprime.py", MODULAR_BLOB)
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "pinned_uniform_source.py"
        path.write_bytes(data)
        spec = importlib.util.spec_from_file_location("pinned_uniform_source", path)
        if spec is None or spec.loader is None:
            raise ValueError("uniform source module cannot be loaded")
        source = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(source)
        creators = source.creators()
        if len(creators) != 4 or any(c.shape != (16, 16) for c in creators):
            raise ValueError("unexpected creator dimensions")
        for c in creators:
            require_finite(c, "creator")
            if not np.array_equal(c, c.real) or not np.array_equal(c.real, np.rint(c.real)):
                raise ValueError("creator coefficients are not real integers")
        c0, c1 = (c.real.astype(np.int64) for c in creators[:2])
        generator = c0 @ c1.T + c1 @ c0.T
        if not np.array_equal(generator @ generator @ generator, generator):
            raise ValueError("generator cubic relation failed")
        m = 40 * np.eye(16, dtype=np.int64) + generator @ generator + 9 * generator
        w = c1 @ m
        regular = np.diag([1 if i in (0, 4, 8, 12) else 0 for i in range(16)])
        numerator = np.zeros((16, 16), dtype=np.int64)
        for i in (1, 5, 9, 13):
            numerator[i, i] = 1681
        for i in (2, 6, 10, 14):
            numerator[i, i] = 81
        for i, j, value in (
            (1, 2, 369), (2, 1, 369), (13, 14, 369), (14, 13, 369),
            (5, 6, -369), (6, 5, -369), (9, 10, -369), (10, 9, -369),
        ):
            numerator[i, j] = value
        if not np.array_equal(w.T @ w, 1600 * regular + numerator):
            raise ValueError("one or more of the 256 right Gram entries differ")
        if (not np.array_equal(numerator @ numerator, 1762 * numerator) or
                np.any(regular @ numerator) or np.any(numerator @ regular) or
                not np.array_equal(regular @ regular, regular)):
            raise ValueError("exact projection identities failed")
        analytic_u = expm(np.log(5 / 4) * generator)
        require_finite(analytic_u, "analytic boost")
        boost_error = float(np.max(np.abs(analytic_u - m / 40)))
        require_finite(boost_error, "boost error")
        if boost_error > TOLERANCE:
            raise ValueError("analytic boost differs from rational boost")
        x = 1j * (3 / 5) * (c1 @ analytic_u)
        defect = np.eye(16) - source.adj(x) @ x
        require_finite(defect, "right defect")
        eigmin = float(np.linalg.eigvalsh(source.herm(defect)).min())
        require_finite(eigmin, "minimum defect eigenvalue")
        if eigmin <= 0:
            raise ValueError("right defect is not positive definite")
        candidate = (np.eye(16) - regular / 5 +
                     (np.sqrt(12071 / 20000) - 1) * numerator / 1762)
        original_root = source.root(defect)
        require_finite(candidate, "candidate root")
        require_finite(original_root, "original root")
        root_error = float(np.max(np.abs(original_root - candidate)))
        wrong_branch_error = float(np.max(np.abs(original_root + candidate)))
        require_finite(root_error, "root error")
        require_finite(wrong_branch_error, "wrong-branch error")
        if root_error > TOLERANCE or wrong_branch_error <= TOLERANCE:
            raise ValueError("moved right root or negative-branch control failed")
    print(f"source_commit={SOURCE_COMMIT} uniform_blob={UNIFORM_BLOB} modular_blob={MODULAR_BLOB}")
    print(f"right_Gram_entries=256 boost_error={boost_error:.3g} min_defect_eigenvalue={eigmin:.12g} root_error={root_error:.3g} OK")
    print("negative_branch=rejected scope=moved D right only; Kraus and span excluded")


if __name__ == "__main__":
    main()
