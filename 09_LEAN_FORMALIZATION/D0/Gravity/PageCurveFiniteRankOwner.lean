import Mathlib.Tactic

/-!
# D0-PAGE-CURVE-FINITE-RANK-OWNER-001 / -INFORMATION-UNITARITY — finite-rank Page curve (Lean)

Python certificates: `05_CERTS/vp_page_curve_finite_rank_owner.py`,
`05_CERTS/vp_black_hole_information_unitarity_owner.py`.

Front P2 construction. A finite total Hilbert space splits as `H_total = H_active ⊕ H_env`; a global
unitary `U_N` preserves the total rank, so `rank(active) + rank(env) = totalRank` is conserved (no
information is deleted). The Page bound on the active-sector entropy is the finite-rank quantity
`pageBound = min(activeRank, envRank)`: it is `≤ activeRank`, `≤ envRank`, `≤ totalRank`, vanishes for a
pure state (`envRank = 0`), and reaches its symmetric maximum at the Page turn `activeRank = envRank`.

HONESTY BOUNDARY. What is owned here (CERT-CLOSED): the finite-rank Page bound and the rank-conservation
(information-unitarity) facts — purely `Nat`-combinatorial, no continuum assumption. What stays open:
the analytic von Neumann entropy `S(ρ) = −Tr(ρ log ρ)` (not in Mathlib; external), the Hawking emission
SPECTRUM / temperature (`D0-HORIZON-FESHBACH-RADIATION-OWNER-001`, scaffold), and the island formula
(external). No black-hole datum enters; the dimensionful Bekenstein `S = A/4` stays the owner-edge.
-/

namespace D0.Gravity

/-- A finite evaporation state: active (radiation/observed) rank, environment (interior) rank,
and the conserved total rank of the global unitary evolution. -/
structure FiniteEvaporationState where
  activeRank : Nat
  envRank : Nat
  totalRank : Nat
  h_total : totalRank = activeRank + envRank

/-- The finite-rank Page bound on the active-sector entropy: `min(activeRank, envRank)`. -/
def pageBound (x : FiniteEvaporationState) : Nat := Nat.min x.activeRank x.envRank

theorem pageBound_le_active (x : FiniteEvaporationState) : pageBound x ≤ x.activeRank :=
  Nat.min_le_left _ _

theorem pageBound_le_env (x : FiniteEvaporationState) : pageBound x ≤ x.envRank :=
  Nat.min_le_right _ _

/-- **Information-unitarity / rank conservation.** The global unitary preserves the total rank:
`totalRank = activeRank + envRank`, so information is transferred, never deleted. -/
theorem rank_conservation (x : FiniteEvaporationState) :
    x.totalRank = x.activeRank + x.envRank := x.h_total

/-- The Page bound never exceeds the total rank (no information loss). -/
theorem pageBound_le_total (x : FiniteEvaporationState) : pageBound x ≤ x.totalRank := by
  rw [x.h_total]
  exact le_trans (Nat.min_le_left _ _) (Nat.le_add_right _ _)

/-- **Pure state:** an empty environment gives zero Page entropy. -/
theorem pageBound_pure (x : FiniteEvaporationState) (h : x.envRank = 0) : pageBound x = 0 := by
  simp [pageBound, h]

/-- **The Page turn:** at the symmetric point `activeRank = envRank` the bound equals the common rank
(the maximum of the curve before it descends). -/
theorem page_turn_symmetric (x : FiniteEvaporationState) (h : x.activeRank = x.envRank) :
    pageBound x = x.activeRank := by
  simp [pageBound, h]

/-- **D0-PAGE-CURVE-FINITE-RANK-OWNER-001.** The finite-rank Page bound `min(activeRank, envRank)` is
`≤ activeRank`, `≤ envRank`, and `≤ totalRank`, with the total rank conserved (`= activeRank + envRank`).
A finite, continuum-free Page curve; the analytic entropy and Hawking spectrum stay external. -/
theorem page_curve_finite_rank_owner (x : FiniteEvaporationState) :
    pageBound x ≤ x.activeRank
      ∧ pageBound x ≤ x.envRank
      ∧ x.totalRank = x.activeRank + x.envRank
      ∧ pageBound x ≤ x.totalRank :=
  ⟨pageBound_le_active x, pageBound_le_env x, x.h_total, pageBound_le_total x⟩

/-- **D0-BLACK-HOLE-INFORMATION-UNITARITY-OWNER-001.** Global unitarity conserves the total rank, and
the active-sector Page bound stays `≤ totalRank` throughout — information is transferred, never
destroyed. -/
theorem information_unitarity_owner (x : FiniteEvaporationState) :
    x.totalRank = x.activeRank + x.envRank ∧ pageBound x ≤ x.totalRank :=
  ⟨x.h_total, pageBound_le_total x⟩

end D0.Gravity
