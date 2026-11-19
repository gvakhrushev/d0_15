#!/usr/bin/env python3
"""Exact-decimal rational replay of the seven-slice HJR boundary Schur response.

Consumes the existing accepted Arb whole-HJR Hessian and its 64x64 certified
response. This script does NOT prove/invert the 64x64 matrix independently.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from fractions import Fraction
from pathlib import Path

BASE = "02_REGISTRY/research/sources/d0_curved_whole_hjr_collar_2026-10-20"
PINS = {
    "COLLAR_HESSIAN_ARB.json": "a38386a86af4be283631d42a890caf66c035c12a4f9d421037160550d36989f4",
    "WIDE_COLLAR_ARB.json": "dee20425e01aeba2f090a55e2b1d221d57160a667eff9240a1c58368cd87e305",
}
NUM = r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?"
BALL = re.compile(r"^\[\s*(?:(" + NUM + r")\s+)?\+/-\s*(" + NUM + r")\s*\]$")


def read_pinned(root: Path, name: str) -> dict:
    path = root / BASE / name
    data = path.read_bytes()
    actual = hashlib.sha256(data).hexdigest()
    assert actual == PINS[name], f"SHA256 mismatch {name}: {actual}"
    return json.loads(data)


def parse_ball(s: str) -> tuple[Fraction, Fraction]:
    m = BALL.fullmatch(s)
    if m is None:
        raise ValueError(f"Not a single real Arb ball: {s!r}")
    mid = Fraction(m.group(1) or "0")
    rad = Fraction(m.group(2))
    assert rad >= 0
    return mid, rad


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[4],
        help="Exact repository root (default: inferred from the script location)"
    )
    args = parser.parse_args()
    collar = read_pinned(args.root, "COLLAR_HESSIAN_ARB.json")
    wide = read_pinned(args.root, "WIDE_COLLAR_ARB.json")
    assert collar["status"] == "RIGOROUS_ARB_PASS"
    assert wide["status"] == "RIGOROUS_W7_BULK_COLLAR_PASS"
    assert wide["source_sha256"] == PINS["COLLAR_HESSIAN_ARB.json"]
    assert wide["unknowns"] == 64
    assert wide["response_error_rational_upper"] == "1/100"
    assert wide["positions"] == [i for i in range(7) for _ in range(9)] + [7]
    assert wide["components"] == [i for _ in range(7) for i in range(9)] + [5]

    # The exterior scalar is the spatial isotropic S2 coframe on t=7.
    # Original K9(q), q=0,...,4; q=5,...,7 by conjugate symmetry.
    c_mid = Fraction(0)
    c_rad = Fraction(0)
    for q, multiplicity in enumerate([1, 2, 2, 2, 1]):
        mid, rad = parse_ball(collar["K9"][q][2][2])
        c_mid += multiplicity * mid / 8
        c_rad += multiplicity * rad / 8

    b_balls = [parse_ball(s) for s in wide["b"]]
    x0 = [Fraction(s) for s in wide["response_candidate_decimal"]]
    assert len(b_balls) == len(x0) == 64
    b_dot_x0 = sum((mid * x for (mid, _), x in zip(b_balls, x0)), Fraction(0))
    b_printing_error = sum(
        (rad * abs(x) for (_, rad), x in zip(b_balls, x0)),
        Fraction(0)
    )
    b_one_norm_upper = sum(
        (abs(mid) + rad for mid, rad in b_balls), Fraction(0)
    )

    # The *independently certified* response bound is ||x'(0)-x0||inf<1/100.
    center = c_mid + b_dot_x0
    radius = c_rad + b_printing_error + b_one_norm_upper / 100
    low, high = center - radius, center + radius

    assert Fraction(57, 1000) < low, ("lower source interval failed", low)
    assert high < Fraction(49, 100), ("upper source interval failed", high)

    print("EXACT_RATIONAL_INTERVAL_PASS")
    print(f"Source SHA256: {wide['source_sha256']}")
    print(f"C_mid={float(c_mid):.14g}; C_radius<={float(c_rad):.14g}")
    print(f"b_mid . x0={float(b_dot_x0):.14g}")
    print(f"b_radius . |x0|={float(b_printing_error):.14g}")
    print(f"||b||_1 upper={float(b_one_norm_upper):.14g}")
    print(f"Kpartial midpoint={float(center):.14g}")
    print(f"Kpartial enclosing interval=({float(low):.14g}, {float(high):.14g})")
    print("PROVED: 57/1000 < Kpartial < 49/100")
    print("Boundary Euler stiffness: 57/8000 < S_eff''(0) < 49/800")
    print("Scope: finite 64-variable fixed-collar conditional HJR only.")


if __name__ == "__main__":
    main()
