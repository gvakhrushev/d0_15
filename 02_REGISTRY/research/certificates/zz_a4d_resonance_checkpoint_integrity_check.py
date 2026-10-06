#!/usr/bin/env python3
"""Verify imported immutable resonance ledgers after the full owner replays.

The original source and expected outputs are pinned at PR #317 / 6853ce4.
This does not replace the three exact owner computations or close their open
geometric classification. A mismatch requires explicit review, never overwrite.
"""
from hashlib import sha256
from pathlib import Path

EXPECTED = {'A_and_mixed_symbol_entries.json': '2ea7e71d2ab0aafb447daf075e5d304eed8fe24eb89be8a40c6cb3457d87c516', 'a4d_resonance_divisor_chiral_numerator.json': 'f4e97cfb2458d47bc3d3605687eb2297742d25ff88bb8f9e360552f6202e5f35', 'a4d_hodge_structural_review_results.json': 'a64cd8c8b3d0e2f86bce13d0faaeda50c5e8b9c24dd46635bd99cc6b62f4e6e9', 'a4d_resonance_divisor_slice_results.json': 'c90d95da46f67b675e8118efbe789ccdffb07ca7583f14ccdd9e0ebf99ffa5ae', 'a4d_sd_asd_reduction_results.json': '94e5a24837d385a40dffe7255bc80d6d8c7244543f8a6970cdf2d633cd90c670'}

def main():
    here = Path(__file__).resolve().parent
    for name, expected in EXPECTED.items():
        path = here / name
        actual = sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise AssertionError(f"immutable resonance checkpoint changed: {name}")
    print(f"PASS {len(EXPECTED)} immutable resonance source/ledger hashes")
    print("SCOPE: arithmetic checkpoint only; absolute-C factors and full strata remain OPEN")

if __name__ == '__main__':
    main()
