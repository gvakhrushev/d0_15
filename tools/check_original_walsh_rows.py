#!/usr/bin/env python3
"""Compare exact-index Walsh rows with the pinned original native prefix.

Both source copies are hash-checked before importing the complete uniform
module and executing its extracted native prefix as trusted Python code. This
numerical check does not establish Golden Kraus, CPTP, span, or admission.
"""
from __future__ import annotations

import ast
import copy
import hashlib
import importlib.util
from pathlib import Path
import tempfile

import numpy as np

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


def matrix_error(actual: object, expected: object) -> float:
    a, e = np.asarray(actual), np.asarray(expected)
    if a.shape != (16, 16) or e.shape != (16, 16):
        raise ValueError("unexpected Walsh matrix dimensions")
    require_finite(a, "source matrix")
    require_finite(e, "expected matrix")
    error = float(np.max(np.abs(a - e)))
    require_finite(error, "matrix error")
    return error


def main() -> None:
    data = pinned_bytes("check_uniform_book_source.py", UNIFORM_BLOB)
    pinned_bytes("check_future_even_algebra_modprime.py", MODULAR_BLOB)
    tree = ast.parse(data)
    function = copy.deepcopy(next(node for node in tree.body if isinstance(node, ast.FunctionDef)
                                  and node.name == "native"))
    stop = next(i for i, node in enumerate(function.body)
                if isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name) and node.targets[0].id == "k")
    function.name = "_captured_original_rows"
    function.body = function.body[:stop] + [ast.Return(value=ast.Tuple(
        elts=[ast.Name(id="words", ctx=ast.Load()), ast.Name(id="rows", ctx=ast.Load())],
        ctx=ast.Load()))]
    extracted = ast.fix_missing_locations(ast.Module(body=[function], type_ignores=[]))
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "pinned_uniform_source.py"
        path.write_bytes(data)
        spec = importlib.util.spec_from_file_location("pinned_uniform_source", path)
        if spec is None or spec.loader is None:
            raise ValueError("uniform source module cannot be loaded")
        source = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(source)
        exec(compile(extracted, "pinned_walsh_prefix", "exec"), source.__dict__)
        words, rows = source._captured_original_rows(np.log(5 / 4), 3 / 5)
        if len(words) != 32 or len(rows) != 64:
            raise ValueError("unexpected source word/row count")
        for word in words:
            if np.asarray(word).shape != (2, 16, 16):
                raise ValueError("unexpected Julia pair dimensions")
            require_finite(word, "source word")
        max_error = 0.0
        odd_count = 0
        for label in range(32):
            signs = []
            for word in range(32):
                count = sum(((label >> bit) & 1) * ((word >> bit) & 1) for bit in range(5))
                sign = (-1) ** count
                if sign != (-1) ** ((label & word).bit_count() & 1):
                    raise ValueError("five-bit Walsh sign mismatch")
                signs.append(sign)
            for endpoint in range(2):
                expected = np.zeros((16, 16), dtype=complex)
                for word in range(32):
                    expected += signs[word] * words[word][endpoint]
                expected /= 32
                actual = rows[2 * label + endpoint]
                error = matrix_error(actual, expected)
                max_error = max(max_error, error)
                if error > TOLERANCE:
                    raise ValueError(f"Walsh row mismatch at {2 * label + endpoint}")
                if label % 2:
                    odd_error = matrix_error(actual, np.zeros((16, 16)))
                    if odd_error > TOLERANCE:
                        raise ValueError(f"odd Walsh row did not vanish at {2 * label + endpoint}")
                    odd_count += 1
        if matrix_error(rows[0], np.zeros((16, 16))) <= TOLERANCE:
            raise ValueError("source anchor unexpectedly zero")
        if matrix_error(rows[0], rows[1]) <= TOLERANCE:
            raise ValueError("endpoint-order negative control failed")
    print(f"source_commit={SOURCE_COMMIT} uniform_blob={UNIFORM_BLOB} modular_blob={MODULAR_BLOB}")
    print(f"signs=1024 rows=64 matrix_entries=16384 odd_rows_zero={odd_count} max_error={max_error:.3g} OK")
    print("anchor_nonzero=verified endpoint_swap=rejected scope=Walsh rows only")


if __name__ == "__main__":
    main()
