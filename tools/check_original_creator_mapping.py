#!/usr/bin/env python3
"""Check the original four creator matrices against the typed role encoding.

This uses exact byte copies of the published #334 Python blobs. After Git blob
SHA-1 verification the complete uniform source module is executed on import,
and the extracted modular AST block is executed as Python code. These are
trusted upstream code, not a sandbox. It checks all 1024 integer matrix entries
and 16 parity signs; it is not a Kraus/span or physical proof.
"""
from __future__ import annotations

import hashlib
import ast
import importlib.util
from pathlib import Path
import tempfile

import numpy as np

COMMIT = "eebcb5e467742df3e9cf7fa9702042d7294aa742"
PATH = "02_REGISTRY/research/sources/d0_book_uniform_source_2026-10-21/check_uniform_book_source.py"
BLOB = "ee8de4635d24c668949ac9a0186616ab7d59f2ed"
MOD_PATH = "02_REGISTRY/research/sources/d0_original_full128_future_even_algebra_2026-10-22/check_future_even_algebra_modprime.py"
MOD_BLOB = "d111c5bfeae3c384a4fe725f4a6d19277ea0005a"
ROOT = Path(__file__).resolve().parents[1]
COPIES = ROOT / "02_REGISTRY/research/sources/d0_proof_architecture_car_creator_bridge_2026-11-04"
MODES = (0, 2, 3, 1)  # Lean ordered roles A, B, C, D -> original bit positions.


def main() -> None:
    data = (COPIES / "check_uniform_book_source.py").read_bytes()
    actual_blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    if actual_blob != BLOB:
        raise ValueError("source blob mismatch")
    mod_data = (COPIES / "check_future_even_algebra_modprime.py").read_bytes()
    mod_hash = hashlib.sha1(b"blob " + str(len(mod_data)).encode() + b"\0" + mod_data).hexdigest()
    if mod_hash != MOD_BLOB:
        raise ValueError("modular source blob mismatch")
    tree = ast.parse(mod_data)
    func = next(node for node in tree.body if isinstance(node, ast.FunctionDef)
                and node.name == "original_kraus_mod")
    start = next(i for i, node in enumerate(func.body) if isinstance(node, ast.Assign)
                 and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)
                 and node.targets[0].id == "order")
    block = func.body[start:start + 3]
    if (len(block) != 3 or not isinstance(block[1], ast.Assign) or
            not isinstance(block[2], ast.For)):
        raise ValueError("modular creator block shape changed")
    # Execute only the three literal AST statements constructing `cs` from
    # the pinned checker, with its exact zero matrix and a chosen prime.
    namespace = {"np": np, "zero": np.zeros((16, 16), dtype=np.int64), "m": 1009}
    exec(compile(ast.Module(body=block, type_ignores=[]), MOD_PATH, "exec"), namespace)
    modular_matrices = namespace["cs"]
    with tempfile.TemporaryDirectory() as temporary:
        file = Path(temporary) / "pinned_source.py"
        file.write_bytes(data)
        spec = importlib.util.spec_from_file_location("original_creators_fixture", file)
        if spec is None or spec.loader is None:
            raise ValueError("source module cannot be loaded")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        matrices = module.creators()
        if len(matrices) != 4 or any(matrix.shape != (16, 16) for matrix in matrices):
            raise ValueError("unexpected creator dimensions")
        states = [tuple(bool((bits >> mode) & 1) for mode in MODES) for bits in range(16)]
        if len(set(states)) != 16:
            raise ValueError("bit/role map is not bijective")
        for bits, state in enumerate(states):
            if (sum(state) % 2) != (bin(bits).count("1") % 2):
                raise ValueError(f"parity mismatch at {bits}")
        checked = 0
        for role_index, mode in enumerate(MODES):
            for bra in range(16):
                for ket in range(16):
                    source, target = states[ket], states[bra]
                    is_creation = (not source[role_index] and target[role_index] and
                                   all(source[j] == target[j] for j in range(4) if j != role_index))
                    sign = (-1) ** sum(source[:role_index]) if is_creation else 0
                    if matrices[mode][bra, ket] != sign:
                        raise ValueError(f"creator mismatch role={role_index} bra={bra} ket={ket}")
                    if modular_matrices[mode][bra, ket] != sign % 1009:
                        raise ValueError(f"modular creator mismatch role={role_index} bra={bra} ket={ket}")
                    checked += 1
        print(f"source={COMMIT}:{PATH} blob={actual_blob}")
        print(f"modular_source={COMMIT}:{MOD_PATH} blob={mod_hash}")
        print(f"role_to_bit={MODES} states={len(states)} parity=16 creator_entries={checked} modular_entries={checked} OK")


if __name__ == "__main__":
    main()
