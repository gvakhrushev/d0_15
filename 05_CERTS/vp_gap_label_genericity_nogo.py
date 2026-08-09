#!/usr/bin/env python3
"""vp_gap_label_genericity_nogo.py — D0-GAP-LABEL-GENERICITY-NOGO-001

The gap-labelling channel was the corpus's most plausible route to a sharp, non-Planck-suppressed
experimental discriminator: Bellissard gap labelling puts the integrated density of states, inside
every spectral gap, in a countable module fixed by the hull's frequency data, and for Fibonacci
quasicrystals those plateaux are *measured* (photonic waveguide arrays, cold atoms;
Kraus-Lahini-Ringel-Verbin-Zilberberg, PRL 109, 106402, 2012).

This certificate answers the honest question that must be settled before any comparison with data:
**is D0's computed label set FORCED and DIFFERENT from the generic Fibonacci chain, or is it the
generic set?**

Result: it is the generic set. Every one of the 25 computed plateaux lies in the module
`Z + Z/phi` — Bellissard's prediction for ANY Fibonacci quasicrystal — and each matches its own
recorded `(n, m)` label via `n + m/phi (mod 1)`. Nothing in the list distinguishes D0's hull from
any other Fibonacci chain, so the channel is consistent with D0 but carries **zero discriminating
power** as currently constituted.

This is a negative result of record, in the same class as the corpus's SPARC phason-halo failure and
the demoted PMNS/LIGO passports: it closes a lead rather than dressing it up. What would be needed
to revive the channel is stated below, not hidden.

Can-fail controls (all must behave as declared, or the certificate FAILS):
  C1  the module test must REJECT a non-golden control (labels built from sqrt(2) instead of phi)
  C2  the module test must REJECT a random plateau set
  C3  the D0 labels must PASS the module test (else the input file is corrupt)

Exit 0 = certificate holds (labels are generic, controls fire correctly), 1 = FAIL.
"""
from __future__ import annotations

import json
import math
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LABELS = ROOT / "d0_gap_labels.json"
TOL = 2e-5
PHI = (1 + 5 ** 0.5) / 2


def in_module(values, alpha, nmax=40, mmax=60, tol=TOL):
    """Fraction of `values` expressible as n + m*alpha (mod 1) with small integer n, m."""
    hits = 0
    for v in values:
        found = False
        for m in range(-mmax, mmax + 1):
            r = (m * alpha) % 1.0
            if abs(r - v) < tol or abs(r - v - 1) < tol or abs(r - v + 1) < tol:
                found = True
                break
        if not found:
            for n in range(-nmax, nmax + 1):
                for m in range(-mmax, mmax + 1):
                    if abs((n + m * alpha) % 1.0 - v) < tol:
                        found = True
                        break
                if found:
                    break
        hits += int(found)
    return hits / len(values) if values else 0.0


def main() -> int:
    if not LABELS.exists():
        print(f"FAIL: {LABELS} missing", file=sys.stderr)
        return 1
    data = json.loads(LABELS.read_text(encoding="utf-8"))
    ids = [d["ids"] for d in data]
    alpha = 1 / PHI

    # the corpus's own (n, m) labels must reproduce the plateaux
    own = sum(1 for d in data
              if abs(((d["k0_label"]["n"] + d["k0_label"]["m"] * alpha) % 1.0) - d["ids"]) < TOL)

    frac_phi = in_module(ids, alpha)
    # C1: a non-golden control module must NOT absorb the same plateaux
    frac_sqrt2 = in_module(ids, 2 ** 0.5 - 1)
    # C2: a random plateau set must NOT lie in the golden module
    rnd = [random.Random(20260728 + i).random() for i in range(len(ids))]
    frac_rnd = in_module(rnd, alpha)

    print(f"plateaux                     : {len(ids)}")
    print(f"match their own (n,m) label  : {own}/{len(ids)}")
    print(f"in the golden module Z+Z/phi : {frac_phi:.0%}")
    print(f"C1 non-golden control (sqrt2): {frac_sqrt2:.0%}  (must be low)")
    print(f"C2 random control            : {frac_rnd:.0%}  (must be low)")

    ok = True
    if own != len(ids) or frac_phi < 0.99:
        print("FAIL C3: the D0 plateaux do not all lie in the golden module", file=sys.stderr)
        ok = False
    if frac_sqrt2 > 0.5:
        print("FAIL C1: the non-golden control was absorbed — the test does not discriminate",
              file=sys.stderr)
        ok = False
    if frac_rnd > 0.5:
        print("FAIL C2: a random set passed — the test does not discriminate", file=sys.stderr)
        ok = False
    if not ok:
        return 1

    print()
    print("VERDICT (D0-GAP-LABEL-GENERICITY-NOGO-001): the computed gap-label set is EXACTLY the")
    print("generic Bellissard module for a Fibonacci hull. It is consistent with D0 and carries no")
    print("discriminating power: any Fibonacci quasicrystal yields the same plateau set, so a")
    print("measurement agreeing with it does not distinguish D0 from the generic chain.")
    print()
    print("To revive the channel D0 would have to force something the generic hull does not fix —")
    print("WHICH labels appear (the gap-opening subset, which depends on the specific operator and")
    print("coupling), or their relative gap widths — and freeze that prediction before comparison.")
    print("Until such a forced subset exists, no gap-labelling measurement is a test of D0.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
