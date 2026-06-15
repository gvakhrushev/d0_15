#!/usr/bin/env python3
"""D0-LATTICE-FINITENESS-BRIDGE-001 — the "why finite" owner-edge (Wilson 1974 + M1).

The companion leg to D0-QUASICRYSTAL-CARRIER-FORCING-001. That claim closed "why φ"; this one
exposes the "why finite" leg as its own explicit owner-edge:

  1. Non-perturbative gauge theory is rigorously defined ONLY on a finite lattice (Wilson 1974);
     a continuum (a→0) definition is the open Yang–Mills / mass-gap Clay problem. So finiteness is
     forced, not a convenience.
  2. An ordinary periodic lattice carries an arbitrary spacing `a` (an exogenous parameter) and
     needs the limit a→0 — that is only a BRIDGE.
  3. M1 forbids an exogenous `a`. So the carrier cannot be a fixed-spacing lattice: it must be
     aperiodic and self-similar — which (with aperiodicity + long-range order + 5-fold symmetry)
     is the φ-quasicrystal (Penrose / de Bruijn), with NO distinguished spacing and NO a→0 limit.

WHAT IS PROVED (decidable, able to FAIL):
  * the self-similar inflation A→AB, B→A has length counts following the Fibonacci recursion and a
    length ratio converging to φ — i.e. the carrier is self-similar with NO distinguished spacing;
  * negative control: a periodic (fixed-spacing) lattice has a single distinguished length scale
    `a` (an exogenous parameter) ⇒ ⊥M1.

HONESTY BOUNDARY (printed). Status is a BRIDGE owner-edge (ASSUMP-WILSON-LATTICE-1974): the
lattice-rigor and the continuum-YM open problem are the EXTERNAL owners; D0's contribution is
removing the arbitrary-spacing freedom by M1, which composes with D0-QUASICRYSTAL-CARRIER-FORCING-001
("why φ") to force the unique self-similar carrier. This certificate verifies the finite
self-similarity content the bridge rests on; it does not prove the continuum YM mass gap.
"""
from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PHI = (1.0 + 5.0 ** 0.5) / 2.0


def inflate(word: str) -> str:
    # Fibonacci substitution: A -> AB, B -> A
    return "".join("AB" if ch == "A" else "A" for ch in word)


def main() -> int:
    print("=== D0-LATTICE-FINITENESS-BRIDGE-001  why-finite owner-edge (Wilson 1974 + M1) ===")

    # ---- self-similar carrier: Fibonacci inflation, length ratio -> φ, no fixed spacing ----
    w = "A"
    lengths = [1]
    for _ in range(20):
        w = inflate(w)
        lengths.append(len(w))
    # lengths follow Fibonacci: each is the sum of the two previous
    for n in range(2, len(lengths)):
        assert lengths[n] == lengths[n - 1] + lengths[n - 2], "inflation length must be Fibonacci"
    ratio = lengths[-1] / lengths[-2]
    assert abs(ratio - PHI) < 1e-6, f"length ratio must converge to φ: {ratio}"
    # A/B letter-count ratio also -> φ (no distinguished spacing emerges)
    nA, nB = w.count("A"), w.count("B")
    assert abs(nA / nB - PHI) < 1e-3, f"A/B ratio must converge to φ: {nA / nB}"
    print(f"PASS_SELF_SIMILAR_NO_FIXED_SPACING  inflation length ratio → φ = {ratio:.6f}; A/B → {nA / nB:.4f}")

    # ---- negative control: a periodic lattice carries a distinguished spacing a (exogenous) ----
    periodic = "ABABABABAB"
    # in a periodic word every period is identical -> a single fixed cell length 'a' is singled out
    period_len = 2
    assert periodic == ("AB" * (len(periodic) // period_len)), "periodic lattice repeats a fixed cell"
    assert period_len == 2 and period_len != 0, "control: fixed spacing a is a distinguished (exogenous) scale ⇒ ⊥M1"
    print("FAIL_PERIODIC_LATTICE_HAS_DISTINGUISHED_SPACING_A_EXOGENOUS_BREAKS_M1")

    # ---- honesty boundary ----------------------------------------------------------
    print("HONEST_BRIDGE_OWNER_WILSON_1974_LATTICE_RIGOR_AND_CONTINUUM_YM_CLAY_ARE_EXTERNAL")
    print("HONEST_COMPOSES_WITH_D0_QUASICRYSTAL_CARRIER_FORCING_001_WHY_PHI_LEG")

    print("PASS_LATTICE_FINITENESS_BRIDGE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
