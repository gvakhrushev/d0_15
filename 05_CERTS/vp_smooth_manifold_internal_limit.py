#!/usr/bin/env python3
"""D0-SMOOTH-MANIFOLD-INTERNAL-LIMIT (MECH-LIMIT manifest) — internal Cauchy owned, smooth limit external.

Front E. This manifest separates the OWNED internal half from the still-EXTERNAL smooth reconstruction
and names the exact missing artifact (honest, can-FAIL, no overclaim).

OWNED (internal, now CORE-backed):
  * finite metric/spectral tower with refinement step G_k -> G_{k+1};
  * the GHP-golden-Cauchy bound: the step ratio is delta0 = 1/(2 phi^3) with 0 < delta0 < 1, so the
    step-bound series Sum_k C*delta0^k is summable (Lean D0.Geometry.GHPGoldenCauchyBound:
    delta0_lt_one, ghp_refinement_summable, ghp_golden_cauchy_bound). Hence the refinement sequence is
    CAUCHY FOR THE INTERNAL STEP BOUND. Verified here EXACTLY in Q(phi): delta0=(-3/2,1), 2 phi^3 delta0=1,
    plus an integer-arithmetic Cauchy-tail witness (the tail Sum_{k>=N} C*r^k -> 0).

EXTERNAL (still owners, NOT closed by this manifest):
  * the SMOOTH compact Riemannian/spin manifold reconstruction is NOT delivered by the finite tower:
      MISSING ARTIFACT 1 = GHP-Cauchy IN THE QUANTUM-GROMOV-HAUSDORFF (Rieffel) metric (not merely the
        scalar internal step bound) + identification of the GH(P) limit object
        (owner D0-RIEFFEL-GHP-CONTINUUM-OWNER-001, ASSUMP-RIEFFEL-GHP);
      MISSING ARTIFACT 2 = Connes reconstruction from the limit commutative spectral triple to a SPIN
        MANIFOLD (owner D0-CONNES-RECONSTRUCTION-OWNER-001, ASSUMP-CONNES-RECONSTRUCTION).
  Both are CLASSICAL external theorems, recorded as BRIDGE-ASSUMPTIONS-EXPLICIT owners; the smooth
  manifold itself stays D0-SMOOTH-MANIFOLD-PASSPORT-001 (PASSPORT-CLOSED, conditional macro-shadow).

Can-FAIL: the internal bound must hold exactly; both external owners must stay registered & OPEN
(BRIDGE-ASSUMPTIONS-EXPLICIT, not CORE); the passport must stay PASSPORT-CLOSED; and three over-claims
("smooth manifold is a primitive D0 input", "Rieffel/GHP solved by slogan", "finite tower proves smooth
manifold") must be rejected. Does NOT erase D0-SMOOTH-MANIFOLD-PASSPORT-001.
"""
from __future__ import annotations

import csv
import pathlib
import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
CSV = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"

EXTERNAL_OWNERS = {
    "D0-RIEFFEL-GHP-CONTINUUM-OWNER-001": "ASSUMP-RIEFFEL-GHP",
    "D0-CONNES-RECONSTRUCTION-OWNER-001": "ASSUMP-CONNES-RECONSTRUCTION",
}
MISSING_ARTIFACTS = [
    "GHP-Cauchy in the quantum-Gromov-Hausdorff (Rieffel) metric + GH(P) limit-object identification "
    "(owner D0-RIEFFEL-GHP-CONTINUUM-OWNER-001)",
    "Connes reconstruction from the limit commutative spectral triple to a spin manifold "
    "(owner D0-CONNES-RECONSTRUCTION-OWNER-001)",
]
FORBIDDEN = [
    "smooth manifold is a primitive D0 input",
    "Rieffel/GHP solved by slogan",
    "finite tower proves smooth manifold",
    "finite tower certificate proves smooth manifold",
]

PHI = (1.0 + 5.0 ** 0.5) / 2.0


def mul(x, y):
    a, b = x
    c, d = y
    return (a * c + b * d, a * d + b * c + b * d)


def sub(x, y):
    return (x[0] - y[0], x[1] - y[1])


def smul(c, x):
    return (c * x[0], c * x[1])


def powp(x, n):
    o = (F(1), F(0))
    for _ in range(n):
        o = mul(o, x)
    return o


def main() -> int:
    print("=== D0-SMOOTH-MANIFOLD-INTERNAL-LIMIT (MECH-LIMIT)  internal Cauchy owned; smooth limit external ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: internal object = finite metric/spectral tower + refinement step "
          "ratio delta0=1/(2 phi^3) (fixed before any value); the smooth Riemannian/spin manifold reading is a "
          "DOWNSTREAM macro-shadow, conditional on the EXTERNAL Rieffel/GHP + Connes-reconstruction owners")

    # ---- OWNED internal half: exact Cauchy step bound from delta0<1 ----------------
    PHI_INV = (F(-1), F(1))
    delta0 = smul(F(1, 2), sub(PHI_INV, mul(PHI_INV, PHI_INV)))
    assert delta0 == (F(-3, 2), F(1)), f"delta0 must be (-3/2,1): {delta0}"
    assert mul(smul(F(2), powp((F(0), F(1)), 3)), delta0) == (F(1), F(0)), "2 phi^3 delta0 = 1 exactly"
    # exact rational enclosure 0 < delta0 < 1 (8/5 < phi < 13/8 verified exactly)
    lo, hi = F(8, 5), F(13, 8)
    assert (2 * lo - 1) ** 2 < 5 and (2 * hi - 1) ** 2 > 5, "exact 8/5 < phi < 13/8"
    a, b = delta0
    assert a + b * lo > 0 and a + b * hi < 1, "exact 0 < delta0 < 1"
    print("PASS_INTERNAL_CAUCHY_OWNED  delta0=1/(2 phi^3) exact, 0<delta0<1 => Sum_k C*delta0^k summable "
          "=> refinement Cauchy for the internal step bound (Lean D0.Geometry.GHPGoldenCauchyBound)")

    # exact Cauchy-tail witness: with a concrete contraction ratio r in (delta0) range, the tail -> 0.
    r = F(3, 25)        # 0.12, an exact ratio < 1 inside the delta0 enclosure
    C = F(1)
    tail = lambda N: C * r ** N / (1 - r)          # exact Sum_{k>=N} C r^k
    assert tail(10) > tail(20) > tail(40) > 0, "exact Cauchy tail strictly decreasing toward 0"
    assert tail(40) < F(1, 10) ** 30, "exact: tail at N=40 is below 1e-30 (Cauchy)"
    print(f"PASS_CAUCHY_TAIL_EXACT  tail Sum_{{k>=N}} C*r^k -> 0 (r={r}): tail(40) < 1e-30, strictly decreasing")

    # ---- EXTERNAL half: owners stay OPEN; name the missing artifact ----------------
    rows = {row["claim_id"]: row for row in csv.DictReader(CSV.open(encoding="utf-8", newline=""))}
    for owner, assump in EXTERNAL_OWNERS.items():
        r0 = rows.get(owner)
        assert r0 is not None, f"external owner {owner} must be registered"
        assert r0["release_status"] == "BRIDGE-ASSUMPTIONS-EXPLICIT", \
            f"{owner} must stay BRIDGE-ASSUMPTIONS-EXPLICIT (OPEN external), not CORE: got {r0['release_status']}"
        assert r0["uses_bridge_assumptions"] == "True" and assump in r0["assumption_ids"], \
            f"{owner} must carry assumption {assump}"
    print("PASS_EXTERNAL_OWNERS_OPEN  D0-RIEFFEL-GHP-CONTINUUM-OWNER-001 (ASSUMP-RIEFFEL-GHP) + "
          "D0-CONNES-RECONSTRUCTION-OWNER-001 (ASSUMP-CONNES-RECONSTRUCTION) both BRIDGE-ASSUMPTIONS-EXPLICIT (OPEN)")

    passport = rows.get("D0-SMOOTH-MANIFOLD-PASSPORT-001")
    assert passport is not None and passport["release_status"] == "PASSPORT-CLOSED", \
        "D0-SMOOTH-MANIFOLD-PASSPORT-001 must stay PASSPORT-CLOSED (not erased, not upgraded to CORE)"
    print("PASS_PASSPORT_INTACT  D0-SMOOTH-MANIFOLD-PASSPORT-001 stays PASSPORT-CLOSED (conditional macro-shadow; not erased)")

    for art in MISSING_ARTIFACTS:
        print(f"MISSING_ARTIFACT  {art}")

    # ---- NO over-claim in the books -------------------------------------------------
    prose = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in (ROOT / "01_BOOKS").rglob("*.md"))
    hits = [f for f in FORBIDDEN if f in prose]
    assert not hits, f"forbidden smooth-manifold over-claim present in books: {hits}"
    print("PASS_NO_OVERCLAIM  books contain no 'primitive D0 input' / 'solved by slogan' / 'finite tower proves smooth manifold'")

    # ================= NEGATIVE CONTROLS (reachable) =================
    # Control 1: "smooth manifold is a primitive D0 input" is rejected by the over-claim detector.
    planted1 = "blah smooth manifold is a primitive D0 input blah"
    assert any(f in planted1 for f in FORBIDDEN), "control: detector must catch 'primitive D0 input'"
    print("FAIL_PRIMITIVE_INPUT_OVERCLAIM_CAUGHT  'smooth manifold is a primitive D0 input' rejected "
          "(the smooth manifold is a downstream macro-shadow, never a primitive input)")

    # Control 2: "Rieffel/GHP solved by slogan" is rejected (owner stays a real external theorem, not a slogan).
    planted2 = "we assert Rieffel/GHP solved by slogan, done"
    assert any(f in planted2 for f in FORBIDDEN), "control: detector must catch the slogan over-claim"
    print("FAIL_SLOGAN_OVERCLAIM_CAUGHT  'Rieffel/GHP solved by slogan' rejected — the GH(P) convergence "
          "stays a registered external owner (ASSUMP-RIEFFEL-GHP), not a slogan")

    # Control 3: "finite tower proves smooth manifold" is rejected — the internal Cauchy bound does NOT
    # deliver the smooth reconstruction (that needs the two named external artifacts above).
    planted3 = "therefore the finite tower proves smooth manifold QED"
    assert any(f in planted3 for f in FORBIDDEN), "control: detector must catch the finite-tower over-claim"
    print("FAIL_FINITE_TOWER_PROVES_SMOOTH_CAUGHT  'finite tower proves smooth manifold' rejected — the "
          "internal step-bound Cauchy property does NOT supply the quantum-GH limit or the Connes spin-manifold")

    print("HONEST_MECH_LIMIT  OWNED = internal step-bound Cauchy from delta0<1 (CORE-backed). EXTERNAL & OPEN "
          "= quantum-GH(Rieffel) Cauchy + GH(P) limit identification + Connes spin-manifold reconstruction "
          "(owners D0-RIEFFEL-GHP-CONTINUUM-OWNER-001 + D0-CONNES-RECONSTRUCTION-OWNER-001). Smooth manifold "
          "stays PASSPORT-CLOSED. No survey/CODATA/PDG datum defines any D0 object here.")
    print("PASS_SMOOTH_MANIFOLD_INTERNAL_LIMIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
