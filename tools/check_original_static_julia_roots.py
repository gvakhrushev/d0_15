#!/usr/bin/env python3
"""Compare only the source's static Julia roots with its pinned NumPy routine.

The complete pinned uniform source module is executed on import after both
copied source files pass Git blob SHA checks. It is trusted source code, not a
sandbox. This floating-point check complements the exact Lean result; it does
not check the moved D root, all 128 Kraus operators, their span or physical
admission.
"""
from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
import tempfile

import numpy as np

SOURCE_COMMIT = "eebcb5e467742df3e9cf7fa9702042d7294aa742"
COPIES = Path(__file__).resolve().parents[1] / (
    "02_REGISTRY/research/sources/d0_proof_architecture_car_creator_bridge_2026-11-04"
)
UNIFORM_BLOB = "ee8de4635d24c668949ac9a0186616ab7d59f2ed"
MODULAR_BLOB = "d111c5bfeae3c384a4fe725f4a6d19277ea0005a"
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


def check_wrong_sign(wrong: np.ndarray, reference: np.ndarray) -> None:
    require_finite(wrong, "wrong-sign control")
    require_finite(reference, "wrong-sign reference")
    error = float(np.max(np.abs(wrong - reference)))
    require_finite(error, "wrong-sign control error")
    if error <= TOLERANCE:
        raise ValueError("wrong-sign negative control unexpectedly passed")


def main() -> None:
    data = pinned_bytes("check_uniform_book_source.py", UNIFORM_BLOB)
    pinned_bytes("check_future_even_algebra_modprime.py", MODULAR_BLOB)
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "pinned_uniform_source.py"
        path.write_bytes(data)
        spec = importlib.util.spec_from_file_location("pinned_uniform_source", path)
        if spec is None or spec.loader is None:
            raise ValueError("uniform source module cannot be loaded")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        creators = module.creators()
        if len(creators) != 4 or any(c.shape != (16, 16) for c in creators):
            raise ValueError("unexpected creator matrices")
        for creator in creators:
            require_finite(creator, "creator")
        eye = np.eye(16, dtype=complex)
        phases = (1j, 1j, -1, -1j)
        max_error = 0.0
        min_eigenvalue = float("inf")
        checked = 0
        for bit, creator in enumerate(creators):
            base = (3 / 5) * creator
            candidate_left = eye - (1 / 5) * (creator @ module.adj(creator))
            candidate_right = eye - (1 / 5) * (module.adj(creator) @ creator)
            # Every source mode has baseline roots; the live mode-1 operand
            # additionally contains the boost and is intentionally excluded.
            operands = [base] + ([base * phases[bit]] if bit != 1 else [])
            for operand in operands:
                for gram, candidate in (
                    (operand @ module.adj(operand), candidate_left),
                    (module.adj(operand) @ operand, candidate_right),
                ):
                    defect = eye - gram
                    require_finite(defect, "defect")
                    require_finite(candidate, "candidate root")
                    eigmin = float(np.linalg.eigvalsh(module.herm(defect)).min())
                    require_finite(eigmin, "minimum defect eigenvalue")
                    min_eigenvalue = min(min_eigenvalue, eigmin)
                    original_root = module.root(defect)
                    require_finite(original_root, "original root")
                    error = float(np.max(np.abs(original_root - candidate)))
                    require_finite(error, "root error")
                    max_error = max(max_error, error)
                    if eigmin <= 0 or error > TOLERANCE:
                        raise ValueError(f"static source root mismatch at bit {bit}")
                    checked += 1
        wrong = eye + (1 / 5) * (creators[0] @ module.adj(creators[0]))
        reference = module.root(eye - ((3 / 5) * creators[0]) @ module.adj((3 / 5) * creators[0]))
        check_wrong_sign(wrong, reference)
    print(f"source_commit={SOURCE_COMMIT} uniform_blob={UNIFORM_BLOB} modular_blob={MODULAR_BLOB}")
    print(f"baseline_pairs=4 phased_live_pairs=3 roots={checked} min_defect_eigenvalue={min_eigenvalue:.12g} max_error={max_error:.3g} OK")
    print("wrong_sign_control=rejected scope=static roots only; moved D, Kraus and span excluded")


if __name__ == "__main__":
    main()
