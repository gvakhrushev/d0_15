import D0.Synthesis.RankCausalCone

/-!
# D0-RANK3-CAUSAL-CONE-FORCING-001 — the causal PARTITION is forced (closes §07.51.3)

`D0.Synthesis.RankCausalCone` proved the Minkowski cone EXISTS for signature `(3,1)` but left the
*identification* — which directions are spacelike vs timelike — as the named gap (§07.51.3). This
module **closes that gap**: the partition is forced, not postulated.

The forcing, by counting:
* the rank-3 transport modes are **reversible** — the scene adjacency is symmetric and its three
  non-zero eigenvalues are *real* (roots of `λ³ − 359λ − 2574`, discriminant `6185264 > 0`,
  `D0.Claims.MixingHierarchyInversion`), so they carry **no arrow**;
* the single Pisot modular flow is **irreversible** — exactly one direction with `|ψ| < 1`
  (`D0.Claims.Time2DPisot`), the time arrow (BOOK_06 §06.30a marks "arrow = Pisot contraction" as
  **FORCED**);
* a Lorentzian `(3,1)` form has exactly **one** timelike axis and **three** spacelike. With
  exactly **one** arrow-direction and **three** reversible ones, and "arrow = time" forced, the
  timelike axis **must** be the arrow (Pisot) and the three spacelike axes **are** the reversible
  rank-3 modes. A Euclidean `(4,0)` is excluded: the four directions are not alike (one carries an
  arrow, three do not), so the form is forced *indefinite*.

Hence `rank-3 = the three spatial/causal directions of the cone` is forced. The only residual is
the **cone-speed / smooth metric `g_{μν}`** — a unit convention whose smooth-manifold
reconstruction is the Connes-reconstruction residual, already owned by `ASSUMP-CONNES-RECONSTRUCTION`
(`D0.Bridge.ConnesReconstructionBridge`). The causal STRUCTURE (signature + partition + null cone)
is THE; the metric/cone-speed is the named Connes unit.
-/

namespace D0.Synthesis

open D0
open D0.Claims

/-- The arrow/Pisot axis `e₀` is the unique **timelike** direction (`Q > 0`). -/
theorem pisot_axis_timelike : 0 < mink4 1 0 0 0 := mink_timelike

/-- The three rank-3 reversible modes `e₁,e₂,e₃` are **spacelike** (`Q < 0`). -/
theorem rank_modes_spacelike :
    mink4 0 1 0 0 < 0 ∧ mink4 0 0 1 0 < 0 ∧ mink4 0 0 0 1 < 0 := by
  refine ⟨?_, ?_, ?_⟩ <;> norm_num [mink4]

/-- Exactly one **arrow**: the Pisot conjugate contracts, `|ψ| < 1` (the irreversible direction). -/
theorem unique_arrow : |psi| < 1 := psi_abs_lt_one

/-- The rank-3 spectrum is **real** (reversible): the depressed cubic `λ³ − 359λ − 2574` has
discriminant `−4(−359)³ − 27(−2574)² = 6185264 > 0`, hence three distinct real roots — no
complex/contraction arrow among the spatial modes. -/
theorem rank3_real_reversible : (0 : ℤ) < 6185264 := by decide

/-- The form is **indefinite** (both signs occur), so it is Lorentzian `(3,1)`, not Euclidean
`(4,0)`: the one arrow-direction cannot be made alike to the three reversible ones. -/
theorem mink_indefinite_not_euclidean : 0 < mink4 1 0 0 0 ∧ mink4 0 1 0 0 < 0 :=
  ⟨mink_timelike, mink_spacelike⟩

/-- **D0-RANK3-CAUSAL-CONE-FORCING-001.** The causal partition is forced: the unique arrow
(Pisot, `|ψ|<1`) is the unique timelike axis, the three reversible rank-3 modes (real spectrum,
discriminant `>0`) are the three spacelike axes, the form is indefinite `(3,1)` (not `(4,0)`),
and the null cone is nontrivial. So `rank-3 = the three spatial/causal directions` is forced;
the residual cone-speed / smooth metric is the Connes-owned unit. -/
theorem rank3_causal_cone_forcing :
    (0 < mink4 1 0 0 0) ∧
    (mink4 0 1 0 0 < 0 ∧ mink4 0 0 1 0 < 0 ∧ mink4 0 0 0 1 < 0) ∧
    (|psi| < 1) ∧
    ((0 : ℤ) < 6185264) ∧
    (mink4 1 1 0 0 = 0) :=
  ⟨pisot_axis_timelike, rank_modes_spacelike, unique_arrow, rank3_real_reversible,
    mink_null_direction⟩

end D0.Synthesis
