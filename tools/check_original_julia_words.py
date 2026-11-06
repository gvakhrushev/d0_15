#!/usr/bin/env python3
"""Compare the 32 ordered Julia pairs with the pinned original source loop.

Both source blobs are checked before the uniform module and its extracted
`native` prefix are executed as trusted Python code. This floating-point check
does not verify Walsh, 128 Kraus, effect span, CPTP, or physical admission.
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


def pair_error(actual: object, expected: object) -> float:
    a, e = np.asarray(actual), np.asarray(expected)
    if a.shape != (2, 16, 16) or e.shape != (2, 16, 16):
        raise ValueError("unexpected Julia pair dimensions")
    require_finite(a, "source pair")
    require_finite(e, "expected pair")
    error = float(np.max(np.abs(a - e)))
    require_finite(error, "pair error")
    return error


def main() -> None:
    data = pinned_bytes("check_uniform_book_source.py", UNIFORM_BLOB)
    pinned_bytes("check_future_even_algebra_modprime.py", MODULAR_BLOB)
    tree = ast.parse(data)
    function = copy.deepcopy(next(node for node in tree.body if isinstance(node, ast.FunctionDef)
                                  and node.name == "native"))
    stop = next(i for i, node in enumerate(function.body)
                if isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name) and node.targets[0].id == "rows")
    function.name = "_captured_original_words"
    function.body = function.body[:stop] + [ast.Return(value=ast.Name(id="words", ctx=ast.Load()))]
    extracted = ast.fix_missing_locations(ast.Module(body=[function], type_ignores=[]))

    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "pinned_uniform_source.py"
        path.write_bytes(data)
        spec = importlib.util.spec_from_file_location("pinned_uniform_source", path)
        if spec is None or spec.loader is None:
            raise ValueError("uniform source module cannot be loaded")
        source = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(source)
        exec(compile(extracted, "pinned_native_prefix", "exec"), source.__dict__)
        actual = source._captured_original_words(np.log(5 / 4), 3 / 5)
        if len(actual) != 32:
            raise ValueError("source did not produce 32 words")
        creators = source.creators()
        if len(creators) != 4 or any(c.shape != (16, 16) for c in creators):
            raise ValueError("unexpected creator dimensions")
        for c in creators:
            require_finite(c, "creator")
        eye = np.eye(16, dtype=complex)
        adj = source.adj
        generator = creators[0] @ adj(creators[1]) + creators[1] @ adj(creators[0])
        u = eye + generator @ generator / 40 + (9 / 40) * generator
        require_finite(u, "rational boost")
        phases = (1j, 1j, -1, -1j)
        q = np.sqrt(12071 / 20000)
        moved_left = np.diag([
            4 / 5 if i in (2, 6, 10, 14) else q if i in (3, 7, 11, 15) else 1
            for i in range(16)
        ])
        regular = np.diag([1 if i in (0, 4, 8, 12) else 0 for i in range(16)])
        w = 40 * creators[1] @ u
        numerator = adj(w) @ w - 1600 * regular
        require_finite(numerator, "right numerator")
        moved_right = eye - regular / 5 + (q - 1) * numerator / 1762
        expected = []
        for mode, creator in enumerate(creators):
            base = (3 / 5) * creator
            x = base @ (u if mode == 1 else eye) * phases[mode]
            left_base = eye - creator @ adj(creator) / 5
            right_base = eye - adj(creator) @ creator / 5
            left = moved_left if mode == 1 else left_base
            right = moved_right if mode == 1 else right_base
            for pair in ((x, left), (adj(x), right), (-base, -left_base), (-adj(base), -right_base)):
                expected.extend((pair, pair))
        max_error = 0.0
        for index, (a, e) in enumerate(zip(actual, expected, strict=True)):
            error = pair_error(a, e)
            max_error = max(max_error, error)
            if error > TOLERANCE:
                raise ValueError(f"source Julia pair mismatch at index {index}")
        if pair_error(actual[0], actual[1]) > TOLERANCE:
            raise ValueError("source adjacent duplicate control failed")
        if pair_error(actual[0], actual[4]) <= TOLERANCE:
            raise ValueError("live/baseline negative control failed")
    print(f"source_commit={SOURCE_COMMIT} uniform_blob={UNIFORM_BLOB} modular_blob={MODULAR_BLOB}")
    print(f"words=32 endpoints=2 matrix_entries=16384 max_error={max_error:.3g} OK")
    print("adjacent_duplicate=verified live_baseline_swap=rejected scope=Julia pairs only")


if __name__ == "__main__":
    main()
