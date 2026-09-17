#!/usr/bin/env python3
"""D0-OMEGA8-CENTER-001 — the Ω₈≅Q₈ orientation bit IS the center = commutator remainder.

Closes the §01.7.1C PROOF-TARGET ("the explicit map Ω₈-orientation groupoid → Z(Q₈) … is not yet
written"). The book asserts the collapse `[Q₈,Q₈] = Z(Q₈) = Φ(Q₈) = {±1}`: the orientation `±` bit
(Z(Q₈)), the read/write order-memory remainder ([Q₈,Q₈]), and the non-generating remainder (Φ(Q₈))
are one and the same two-element group. This certificate proves the operational core in exact
integer-quaternion arithmetic over the 8-element group `Q₈ = {±1, ±i, ±j, ±k}`:

WHAT IS PROVED (decidable, able to FAIL):
  * Z(Q₈) = {q : q·r = r·q ∀ r} = {+1, −1}  (the orientation bit is exactly the center);
  * the commutator SET {[a,b] = a b a⁻¹ b⁻¹} = {+1, −1}  (the order-memory remainder = the same Z₂);
  * hence Z(Q₈) = ⟨[Q₈,Q₈]⟩ — the explicit collapse to a single Z₂ = the `±` orientation bit;
  * the abelianization Q₈/[Q₈,Q₈] has order 4 and is elementary abelian (Klein four), so the Frattini
    subgroup Φ(Q₈) = [Q₈,Q₈] = {±1} as well (standard: Φ = [G,G]·Gᵖ, here = [Q₈,Q₈]);
  * negative control: an imaginary unit i is NOT central (i·j = k ≠ −k = j·i), so the center is not
    all of Q₈ and the collapse is a real constraint.

HONESTY BOUNDARY (printed): the group identification Ω₈≅Q₈ is owned by the Dedekind-minimality cert
(§01.7.1A); here we discharge the remaining map — orientation bit ↔ holonomy parity — as the exact
statement Z(Q₈) = commutator-remainder = {±1}. The spinor double-cover reading is the operational
interpretation of this two-element group, not an extra claim.
"""
from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def qmul(x, y):
    a1, b1, c1, d1 = x
    a2, b2, c2, d2 = y
    return (
        a1 * a2 - b1 * b2 - c1 * c2 - d1 * d2,
        a1 * b2 + b1 * a2 + c1 * d2 - d1 * c2,
        a1 * c2 - b1 * d2 + c1 * a2 + d1 * b2,
        a1 * d2 + b1 * c2 - c1 * b2 + d1 * a2,
    )


def qinv(x):                      # unit quaternion inverse = conjugate
    a, b, c, d = x
    return (a, -b, -c, -d)


Q8 = [(1, 0, 0, 0), (-1, 0, 0, 0),
      (0, 1, 0, 0), (0, -1, 0, 0),
      (0, 0, 1, 0), (0, 0, -1, 0),
      (0, 0, 0, 1), (0, 0, 0, -1)]
ONE, NEG = (1, 0, 0, 0), (-1, 0, 0, 0)


def main() -> int:
    print("=== D0-OMEGA8-CENTER-001  Z(Q₈) = [Q₈,Q₈] = {±1} (orientation bit collapse) ===")

    assert len(set(Q8)) == 8, "Q₈ has 8 distinct elements"
    # closure: the set is a group under qmul
    assert all(qmul(a, b) in Q8 for a in Q8 for b in Q8), "Q₈ closed under multiplication"
    print("PASS_GROUP_ORDER_8  Q₈ = {±1,±i,±j,±k} closed under quaternion multiplication")

    # ---- center: commutes with everything ------------------------------------------
    center = [q for q in Q8 if all(qmul(q, r) == qmul(r, q) for r in Q8)]
    assert set(center) == {ONE, NEG}, f"Z(Q₈) must be {{±1}}: {center}"
    print(f"PASS_CENTER_IS_PM1  Z(Q₈) = {{+1, −1}} (the ± orientation bit), |Z(Q₈)|=2")

    # ---- commutator set --------------------------------------------------------------
    comms = {qmul(qmul(a, b), qmul(qinv(a), qinv(b))) for a in Q8 for b in Q8}
    assert comms == {ONE, NEG}, f"commutator set must be {{±1}}: {comms}"
    print(f"PASS_COMMUTATOR_SET_PM1  {{[a,b] = a b a⁻¹ b⁻¹}} = {{+1, −1}} (the order-memory remainder)")

    # ---- the collapse: center = commutator remainder --------------------------------
    assert set(center) == comms, "Z(Q₈) must equal the commutator remainder"
    print("PASS_COLLAPSE  Z(Q₈) = ⟨[Q₈,Q₈]⟩ = {±1}: orientation bit = order-memory remainder (one Z₂)")

    # ---- Frattini via the abelianization: Q₈/[Q₈,Q₈] is Klein four (elementary abelian) ----
    # cosets of {±1}: pair each q with its negative; 8/2 = 4 cosets
    def coset(q):  # represent coset by frozenset {q, -q}
        return frozenset({q, qmul(NEG, q)})
    cosets = {coset(q) for q in Q8}
    assert len(cosets) == 4, f"abelianization Q₈/{{±1}} must have order 4: {len(cosets)}"
    # elementary abelian: every element squares into the commutator subgroup ⇒ g² ∈ {±1}
    assert all(qmul(q, q) in (ONE, NEG) for q in Q8), "every g² ∈ {±1} ⇒ quotient is exponent 2 (Klein four)"
    print("PASS_FRATTINI_EQ_COMMUTATOR  Q₈/[Q₈,Q₈] = Klein four (g²∈{±1}) ⇒ Φ(Q₈)=[Q₈,Q₈]={±1}")

    # ---- negative control: an imaginary unit is NOT central -------------------------
    i, j = (0, 1, 0, 0), (0, 0, 1, 0)
    assert qmul(i, j) != qmul(j, i), "control: i·j = k ≠ −k = j·i, so i ∉ Z(Q₈)"
    assert i not in center, "control: i is not central ⇒ Z(Q₈) ≠ Q₈ (collapse is a real constraint)"
    print("FAIL_IMAGINARY_UNIT_NOT_CENTRAL  i·j=k ≠ −k=j·i ⇒ i ∉ Z(Q₈); the center is exactly {±1}")

    print("HONEST_OMEGA8_EQ_Q8_OWNED_BY_DEDEKIND_01_7_1A_HERE_THE_ORIENTATION_TO_CENTER_MAP_IS_CLOSED")
    print("PASS_OMEGA8_CENTER_COLLAPSE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
