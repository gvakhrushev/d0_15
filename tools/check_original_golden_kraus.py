#!/usr/bin/env python3
"""Compare ordered Golden Kraus matrices with the pinned source native loop.

Both source blobs are verified before executing the complete uniform module and
its captured native prefix as trusted code. This numerical comparison is not a
proof of CPTP, effect span/rank, or physical admission.
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
        raise ValueError("unexpected matrix dimensions")
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
    stop = next(i for i, node in enumerate(function.body) if isinstance(node, ast.Return))
    function.name = "_captured_original_kraus"
    function.body = function.body[:stop] + [ast.Return(value=ast.Tuple(
        elts=[ast.Name(id="rows", ctx=ast.Load()), ast.Name(id="k", ctx=ast.Load())],
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
        exec(compile(extracted, "pinned_golden_prefix", "exec"), source.__dict__)
        rows, actual = source._captured_original_kraus(np.log(5 / 4), 3 / 5)
        if len(rows) != 64 or len(actual) != 128:
            raise ValueError("unexpected source row/Kraus count")
        for row in rows:
            if np.asarray(row).shape != (16, 16):
                raise ValueError("unexpected Walsh matrix dimensions")
            require_finite(row, "Walsh row")
        p = (np.sqrt(5) - 1) / 2
        require_finite(p, "Golden parameter")
        if not p > 0:
            raise ValueError("Golden parameter is not positive")
        anchor = rows[0]
        eye = np.eye(16, dtype=complex)
        max_error = 0.0
        dark_count = 0
        order_witness = None
        for row, n in enumerate(rows):
            value = source.adj(n) @ anchor
            wrong_order = source.adj(anchor) @ n
            require_finite(value, "Golden product")
            require_finite(wrong_order, "reversed Golden product")
            if order_witness is None and matrix_error(value, wrong_order) > TOLERANCE:
                order_witness = row
            expected = (
                (eye if row == 0 else np.zeros_like(eye)) - 2 * p**2 * value,
                -2 * p * np.sqrt(p) * value,
            )
            for port in range(2):
                index = 2 * row + port
                error = matrix_error(actual[index], expected[port])
                max_error = max(max_error, error)
                if error > TOLERANCE:
                    raise ValueError(f"Golden Kraus mismatch at slot {index}")
                if (row // 2) % 2:
                    if matrix_error(actual[index], np.zeros_like(eye)) > TOLERANCE:
                        raise ValueError(f"marked dark slot {index} is not zero")
                    dark_count += 1
        if dark_count != 64:
            raise ValueError("unexpected marked-slot count")
        if order_witness is None:
            raise ValueError("product-order negative control has no witness")
        v0 = source.adj(rows[0]) @ anchor
        if matrix_error(actual[0], -2 * p**2 * v0) <= TOLERANCE:
            raise ValueError("missing identity-anchor negative control")
    print(f"source_commit={SOURCE_COMMIT} uniform_blob={UNIFORM_BLOB} modular_blob={MODULAR_BLOB}")
    print(f"rows=64 slots=128 matrix_entries=32768 marked_zero={dark_count} max_error={max_error:.3g} OK")
    print(f"anchor_identity=verified product_order_witness={order_witness} scope=Golden matrices only")


if __name__ == "__main__":
    main()
