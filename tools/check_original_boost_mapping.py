#!/usr/bin/env python3
"""Check only the original creator/boost construction over GF(1009).

The complete pinned uniform source module is executed on import, and the
literal generator/boost AST block from the pinned modular checker is executed
as Python code. These are trusted source code, not a sandbox. This is not a
replay of the 128-Kraus checker, a proof of its effect span, an exponential
identity, or a physical admission test.
"""
from __future__ import annotations

import ast
import hashlib
import importlib.util
from pathlib import Path
import tempfile

import numpy as np

SOURCE_COMMIT = "eebcb5e467742df3e9cf7fa9702042d7294aa742"
UNIFORM_BLOB = "ee8de4635d24c668949ac9a0186616ab7d59f2ed"
MODULAR_BLOB = "d111c5bfeae3c384a4fe725f4a6d19277ea0005a"
ROOT = Path(__file__).resolve().parents[1]
COPIES = ROOT / "02_REGISTRY/research/sources/d0_proof_architecture_car_creator_bridge_2026-11-04"
MODULUS = 1009


def pinned_bytes(name: str, expected: str) -> bytes:
    data = (COPIES / name).read_bytes()
    digest = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    if digest != expected:
        raise ValueError(f"Git blob mismatch for {name}: {digest}")
    return data


def checker_check(condition: bool, description: str) -> None:
    if not condition:
        raise ValueError(description)


def main() -> None:
    uniform_data = pinned_bytes("check_uniform_book_source.py", UNIFORM_BLOB)
    modular_data = pinned_bytes("check_future_even_algebra_modprime.py", MODULAR_BLOB)

    # Load precisely the bytes that passed the hash check, from a private file.
    with tempfile.TemporaryDirectory() as directory:
        source = Path(directory) / "pinned_uniform_source.py"
        source.write_bytes(uniform_data)
        spec = importlib.util.spec_from_file_location("pinned_uniform_source", source)
        if spec is None or spec.loader is None:
            raise ValueError("uniform source module cannot be loaded")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        raw_creators = module.creators()

    if len(raw_creators) != 4 or any(x.shape != (16, 16) for x in raw_creators):
        raise ValueError("unexpected creator dimensions")
    if any(not np.array_equal(x, x.real) or not np.array_equal(x.real, np.rint(x.real))
           for x in raw_creators):
        raise ValueError("creator coefficients are not real integers")
    creators = [x.real.astype(np.int64) for x in raw_creators]
    actual_g = creators[0] @ creators[1].T + creators[1] @ creators[0].T
    expected_g = np.zeros((16, 16), dtype=np.int64)
    for bra, ket, value in (
        (1, 2, 1), (2, 1, 1), (5, 6, -1), (6, 5, -1),
        (9, 10, -1), (10, 9, -1), (13, 14, 1), (14, 13, 1),
    ):
        expected_g[bra, ket] = value
    if not np.array_equal(actual_g, expected_g):
        raise ValueError("one or more of the 256 generator entries differ")
    if not np.array_equal(actual_g @ actual_g @ actual_g, actual_g):
        raise ValueError("G cubed differs from G")

    # Execute only the literal statements from the pinned modular checker's
    # generator assignment through its U assignment. This is not a full replay.
    tree = ast.parse(modular_data)
    function = next(node for node in tree.body if isinstance(node, ast.FunctionDef)
                    and node.name == "original_kraus_mod")

    def assignment_index(name: str) -> int:
        return next(i for i, node in enumerate(function.body)
                    if isinstance(node, ast.Assign) and len(node.targets) == 1
                    and isinstance(node.targets[0], ast.Name) and node.targets[0].id == name)

    start = assignment_index("generator")
    end = assignment_index("U")
    if end < start:
        raise ValueError("modular checker generator/boost order changed")
    m = MODULUS
    inv = lambda n: pow(int(n) % m, -1, m)
    plus = lambda a, b: (a + b) % m
    mul = lambda a, b: (a @ b) % m
    sc = lambda a, b: (int(a) * b) % m
    eye = np.eye(16, dtype=np.int64)
    namespace = {
        "cs": [c % m for c in creators], "eye": eye, "np": np, "inv": inv,
        "plus": plus, "mul": mul, "sc": sc, "check": checker_check,
    }
    block = ast.Module(body=function.body[start:end + 1], type_ignores=[])
    exec(compile(block, "pinned_modular_boost", "exec"), namespace)
    expected_u = (eye + inv(40) * (actual_g @ actual_g) + 9 * inv(40) * actual_g) % m
    if not np.array_equal(namespace["generator"], expected_g % m):
        raise ValueError("modular checker generator differs in one or more entries")
    if not np.array_equal(namespace["U"], expected_u):
        raise ValueError("modular checker boost differs in one or more entries")

    print(f"source_commit={SOURCE_COMMIT} uniform_blob={UNIFORM_BLOB} modular_blob={MODULAR_BLOB}")
    print(f"modulus={m} generator_entries=256 boost_entries=256 G_cubed_equals_G=true OK")
    print("scope=creator/boost only; no full 128-Kraus replay, span, or physical admission")


if __name__ == "__main__":
    main()
