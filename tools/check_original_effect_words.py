#!/usr/bin/env python3
"""Check source effect-word order in one pinned finite-field fixture.

Both source blobs are checked before the entire modular module is imported as
trusted Python code. Its original_kraus_mod constructor performs its own
finite-field checks, including completeness; this script does not promote those
checks to a Lean CPTP theorem, a complex result, rank/span, or admission.
"""
from __future__ import annotations

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


def pinned_bytes(name: str, expected: str) -> bytes:
    data = (COPIES / name).read_bytes()
    digest = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    if digest != expected:
        raise ValueError(f"Git blob mismatch for {name}: {digest}")
    return data


def chronological_product_effect(path: tuple[int, ...], data: dict) -> np.ndarray:
    """Construct (K_last ... K_first)†(K_last ... K_first), without reset."""
    k, kd, modulus = data["K"], data["Kd"], int(data["m"])
    product = data["I"].copy()
    product_dagger = data["I"].copy()
    for slot in path:
        if type(slot) is not int or not 0 <= slot < len(k):
            raise ValueError("invalid Kraus slot")
        product = (k[slot] @ product) % modulus
        # The pinned finite-field checker constructs K† before evaluating i;
        # transposing its already-evaluated K would not conjugate that i.
        product_dagger = (product_dagger @ kd[slot]) % modulus
    return (product_dagger @ product) % modulus


def main() -> None:
    pinned_bytes("check_uniform_book_source.py", UNIFORM_BLOB)
    modular = pinned_bytes("check_future_even_algebra_modprime.py", MODULAR_BLOB)
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "pinned_modular_source.py"
        path.write_bytes(modular)
        spec = importlib.util.spec_from_file_location("pinned_modular_source", path)
        if spec is None or spec.loader is None:
            raise ValueError("modular source module cannot be loaded")
        source = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(source)
        reference = source.SPLIT_PRIMES[-1]
        if reference[0] != 1009:
            raise ValueError("unexpected source modulus")
        data = source.original_kraus_mod(reference)
        if data["m"] != 1009 or data["K"].shape != (128, 16, 16) or data["Kd"].shape != (128, 16, 16):
            raise ValueError("unexpected source finite-field matrix dimensions")
        paths = ((), (0,), (0, 2), (2, 0), (0, 2, 0), (0, 4, 2))
        for path in paths:
            actual = source.effect_of_word(path, data)
            expected = chronological_product_effect(path, data)
            if not np.array_equal(actual, expected):
                raise ValueError(f"source effect-order mismatch for {path}")
        if np.array_equal(source.effect_of_word((0, 2), data), source.effect_of_word((2, 0), data)):
            raise ValueError("actual source effect-order negative control failed")
        if np.any(source.effect_of_word((0, 4, 2), data)):
            raise ValueError("marked dark-slot effect is not zero")
    print(f"source_commit={SOURCE_COMMIT} uniform_blob={UNIFORM_BLOB} modular_blob={MODULAR_BLOB}")
    print("modulus=1009 paths=6 empty_identity=verified actual_order_witness=(0,2) dark_slot=4 OK")
    print("scope=finite-field effect order only; no complex CPTP/rank/span or physical admission")


if __name__ == "__main__":
    main()
