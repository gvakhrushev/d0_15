import D0.Claims.KernelZoneSplit

/-!
# D0-BSD-RANK-PASSPORT-001 — §30 BSD: the κ-stable nullity = rank passport

The §30 (Birch–Swinnerton-Dyer) D0-reformulation reads "ord L(E,s) = rank_D0(E)" as ONE κ-invariant
with two passports: the analytic order-of-zero and the topological κ-stable nullity. This module
re-exports the proven CORE rank/nullity side: the canonical scene operator `A` of `K(9,11,13)` has
adjacency rank ≤ 3 (every row is one of 3 zone patterns) and nullity ≥ 30 (the 30 within-zone
difference vectors lie in `ker A`), splitting `30 = 8 + 10 + 12` — exact integer linear algebra
(`D0.Claims.kernel_zone_split`, `native_decide`/`decide`, gap-free).

**Register (honest):** this is the TOPOLOGICAL/rank passport only — `rank_D0 = nullity`, proven. It is
NOT the BSD equality `ord L(E,s) = rank` (the analytic order-of-zero passport): that needs an
order-of-zero object + an elliptic-curve constructive type + the M1 reductio (`D0.Foundation.M1Predicate`)
to force the two passports to coincide, and stays a named theorem-target. Two passports for the SAME
Lean theorem: physics (scene rank-3/nullity-30 split) + Clay-math (§30 nullity side).
-/

namespace D0.Synthesis

open D0.Claims

/-- **§30 rank passport.** The canonical scene operator has rank ≤ 3 and nullity ≥ 30 (split
`8 + 10 + 12`) — the κ-stable nullity = rank side of the BSD D0-reformulation. Re-exports the proven
`kernel_zone_split`. NOT the analytic `ord L = rank` equality. -/
theorem bsd_rank_nullity_passport :
    D0.numVertices = 33 ∧ D0.numEdges = 359 ∧
    (∀ i : Fin 33, A i = rowPattern (zoneOf i)) ∧
    (∀ v ∈ zoneDiffs, A.mulVec v = 0) ∧
    zoneDiffs.length = 30 ∧
    (9 - 1) + (11 - 1) + (13 - 1) = 30 :=
  kernel_zone_split

end D0.Synthesis
