import Mathlib.Data.Matrix.Basic
import Mathlib.Algebra.BigOperators.Fin
import D0.Geometry.ArchivePhaseDistance
import D0.Geometry.ArchiveWeightedGraph
import D0.Geometry.ArchiveCanonicalDirichlet
import D0.Geometry.ArchiveCanonicalLaplacian

open scoped BigOperators

namespace D0

structure CoarseGraining (n : Nat) where
  P : archivePhaseIndex (n+1) → archivePhaseIndex n
  surjective : Function.Surjective P

def archiveRGPhaseProjection (n : Nat) (x : archivePhaseIndex (n+1)) : archivePhaseIndex n :=
  ⟨x.val % (archiveFibers n), by
    have hF : 0 < archiveFibers n := by
      unfold archiveFibers
      omega
    exact Nat.mod_lt x.val hF⟩

theorem archiveRGPhaseProjection_surjective (n : Nat) :
  Function.Surjective (archiveRGPhaseProjection n) := by
  intro y
  use ⟨y.val, by unfold archiveFibers; omega⟩
  apply Fin.ext
  dsimp [archiveRGPhaseProjection]
  rw [Nat.mod_eq_of_lt y.isLt]

def projectedLaplacian (n : Nat) (P : archivePhaseIndex (n+1) → archivePhaseIndex n) :
  Matrix (archivePhaseIndex n) (archivePhaseIndex n) ℝ :=
  fun i j => ∑ k : archivePhaseIndex (n+1), ∑ m : archivePhaseIndex (n+1),
    if P k = i ∧ P m = j then (archiveCanonicalLaplacian (n+1)) k m else 0

def pullbackEnergy (n : Nat) (P : archivePhaseIndex (n+1) → archivePhaseIndex n)
  (f : archivePhaseIndex n → ℝ) : ℝ :=
  archiveDirichletEnergy (n+1) (f ∘ P)

def rgCurvatureCorrection (n : Nat) (P : archivePhaseIndex (n+1) → archivePhaseIndex n)
  (c : ℝ) (f : archivePhaseIndex n → ℝ) : ℝ :=
  pullbackEnergy n P f - c * archiveDirichletEnergy n f

def ExactProjectiveCompatibility (n : Nat) (P : archivePhaseIndex (n+1) → archivePhaseIndex n) : Prop :=
  ∀ f, Matrix.mulVec (archiveCanonicalLaplacian (n+1)) (f ∘ P) = (Matrix.mulVec (archiveCanonicalLaplacian n) f) ∘ P

def ExactEnergyCompatibility (n : Nat) (P : archivePhaseIndex (n+1) → archivePhaseIndex n)
  (c : ℝ) : Prop :=
  ∀ f, pullbackEnergy n P f = c * archiveDirichletEnergy n f

def RenormalizedProjectiveCompatibility (n : Nat)
  (P : archivePhaseIndex (n+1) → archivePhaseIndex n) (c : ℝ) : Prop :=
  ∀ i j : archivePhaseIndex (n+1),
    (archiveCanonicalLaplacian (n+1)) i j =
      c * (archiveCanonicalLaplacian n) (P i) (P j)

def ExactFlatCompatibility (n : Nat)
  (P : archivePhaseIndex (n+1) → archivePhaseIndex n) : Prop :=
  RenormalizedProjectiveCompatibility n P 1

def renormalizedPullbackLaplacian (n : Nat)
  (P : archivePhaseIndex (n+1) → archivePhaseIndex n) (c : ℝ) :
  Matrix (archivePhaseIndex (n+1)) (archivePhaseIndex (n+1)) ℝ :=
  fun i j => c * (archiveCanonicalLaplacian n) (P i) (P j)

def rgOperatorResidual (n : Nat)
  (P : archivePhaseIndex (n+1) → archivePhaseIndex n) (c : ℝ) :
  Matrix (archivePhaseIndex (n+1)) (archivePhaseIndex (n+1)) ℝ :=
  archiveCanonicalLaplacian (n+1) - renormalizedPullbackLaplacian n P c

theorem rg_curvature_zero_iff_exact_compatibility (n : Nat) (P : archivePhaseIndex (n+1) → archivePhaseIndex n) (c : ℝ) :
  (∀ f, rgCurvatureCorrection n P c f = 0) ↔ ExactEnergyCompatibility n P c := by
  unfold ExactEnergyCompatibility
  constructor
  · intro h f
    have h1 := h f
    unfold rgCurvatureCorrection at h1
    linarith
  · intro h f
    unfold rgCurvatureCorrection
    rw [h f]
    linarith

theorem rg_operator_curvature_zero_iff_renormalized_compatibility
    (n : Nat) (P : archivePhaseIndex (n+1) → archivePhaseIndex n) (c : ℝ) :
    rgOperatorResidual n P c = 0 ↔ RenormalizedProjectiveCompatibility n P c := by
  unfold RenormalizedProjectiveCompatibility
  constructor
  · intro h i j
    have hij : rgOperatorResidual n P c i j = 0 := by
      rw [h]
      rfl
    unfold rgOperatorResidual renormalizedPullbackLaplacian at hij
    change archiveCanonicalLaplacian (n+1) i j -
      c * archiveCanonicalLaplacian n (P i) (P j) = 0 at hij
    linarith
  · intro h
    ext i j
    unfold rgOperatorResidual renormalizedPullbackLaplacian
    change archiveCanonicalLaplacian (n+1) i j -
      c * archiveCanonicalLaplacian n (P i) (P j) = 0
    rw [h i j]
    ring

theorem rg_flat_curvature_zero_iff_exact_flat_compatibility
    (n : Nat) (P : archivePhaseIndex (n+1) → archivePhaseIndex n) :
    rgOperatorResidual n P 1 = 0 ↔ ExactFlatCompatibility n P := by
  exact rg_operator_curvature_zero_iff_renormalized_compatibility n P 1

-- Helper: In the cycle graph of length n+3, node n+2 is NOT adjacent to node 1.
-- Their cyclic distance is 2 (since n > 1 implies n+1 ≥ 3 > 2).
private lemma cycle_last_not_adj_one (n : Nat) (hn : 1 < n) :
    ¬ archiveAdjacent (n+1)
        ⟨n+2, by unfold archiveFibers; omega⟩
        ⟨1,   by unfold archiveFibers; omega⟩ := by
  unfold archiveAdjacent cyclicDistance archiveFibers
  intro hc
  have h_t1 : (n+2 + (n+3) - 1) % (n+3) = n+1 := by
    rw [show n+2 + (n+3) - 1 = (n+1) + (n+3) from by omega, Nat.add_mod_right]
    exact Nat.mod_eq_of_lt (by omega)
  have h_t2 : (1 + (n+3) - (n+2)) % (n+3) = 2 := by
    rw [show 1 + (n+3) - (n+2) = 2 from by omega]
    exact Nat.mod_eq_of_lt (by omega)
  simp only [h_t1, h_t2, min_eq_right (show 2 ≤ n+1 from by omega)] at hc
  omega

-- Helper: In the cycle graph of length n+2, node 0 IS adjacent to node 1 (distance = 1).
private lemma cycle_zero_adj_one (n : Nat) (hn : 1 < n) :
    archiveAdjacent n
        ⟨0, by unfold archiveFibers; omega⟩
        ⟨1, by unfold archiveFibers; omega⟩ := by
  unfold archiveAdjacent cyclicDistance archiveFibers
  have h_t1 : (0 + (n+2) - 1) % (n+2) = n+1 := by
    rw [show 0 + (n+2) - 1 = n+1 from by omega]
    exact Nat.mod_eq_of_lt (by omega)
  have h_t2 : (1 + (n+2) - 0) % (n+2) = 1 := by
    rw [show 1 + (n+2) - 0 = 1 + (n+2) from by omega, Nat.add_mod_right]
    exact Nat.mod_eq_of_lt (by omega)
  simp only [h_t1, h_t2, min_eq_right (show 1 ≤ n+1 from by omega)]

-- The nearest-neighbor cycle Laplacian does NOT satisfy exact projective compatibility.
-- Proof: the indicator function f = δ₁ provides a counterexample at index n+2.
-- LHS = 0 (node n+2 is not adjacent to node 1 at level n+1),
-- RHS = -1 (node 0 is adjacent to node 1 at level n, and P(n+2) = 0).
theorem exact_projective_compatibility_fails (n : Nat) (hn : 1 < n) :
    ¬ ExactProjectiveCompatibility n (archiveRGPhaseProjection n) := by
  intro h_comp
  -- Counterexample function: indicator of vertex 1
  let f : archivePhaseIndex n → ℝ := fun i => if i.val = 1 then 1 else 0
  have h_eq := h_comp f
  -- Evaluate at index jn2 = ⟨n+2, ...⟩ : archivePhaseIndex (n+1)
  let jn2 : archivePhaseIndex (n+1) := ⟨n+2, by unfold archiveFibers; omega⟩
  have h_eq_coord := congr_fun h_eq jn2
  -- ── Prove LHS = 0: every term L(jn2, j) * f(P(j)) = 0 ───────────────────
  have h_lhs : Matrix.mulVec (archiveCanonicalLaplacian (n+1))
                 (f ∘ archiveRGPhaseProjection n) jn2 = 0 := by
    unfold Matrix.mulVec dotProduct
    apply Finset.sum_eq_zero
    intro j _
    by_cases hj : j = ⟨1, by unfold archiveFibers; omega⟩
    · -- j = ⟨1,...⟩: L(jn2, 1) = 0 since jn2 ≠ 1 and not adjacent
      subst hj
      have hjne : jn2 ≠ ⟨1, by unfold archiveFibers; omega⟩ := by
        intro heq
        have := congr_arg Fin.val heq
        simp only [jn2] at this; omega
      unfold archiveCanonicalLaplacian
      dsimp only []
      rw [if_neg hjne, if_neg (cycle_last_not_adj_one n hn)]
      ring
    · -- j ≠ ⟨1,...⟩: f(P(j)) = 0
      have hj_val : j.val ≠ 1 := fun hc => hj (Fin.ext hc)
      have h_fP : f (archiveRGPhaseProjection n j) = 0 := by
        simp only [archiveRGPhaseProjection, archiveFibers, f]
        split_ifs with h_cond
        · rcases Nat.lt_or_ge j.val (n+2) with h1 | h1
          · rw [Nat.mod_eq_of_lt h1] at h_cond; exact absurd h_cond hj_val
          · have hval : j.val = n+2 := by
              have := j.isLt; unfold archiveFibers at this; omega
            rw [hval, Nat.mod_self] at h_cond; omega
        · rfl
      simp [Function.comp, h_fP]
  -- ── Prove RHS = -1: P(jn2) = 0, and L_n(0,1) * f(1) = -1 * 1 ───────────
  have h_rhs : ((Matrix.mulVec (archiveCanonicalLaplacian n) f) ∘
                archiveRGPhaseProjection n) jn2 = -1 := by
    simp only [Function.comp, jn2]
    have h_proj : archiveRGPhaseProjection n ⟨n+2, by unfold archiveFibers; omega⟩ =
        ⟨0, by unfold archiveFibers; omega⟩ := by
      apply Fin.ext; simp [archiveRGPhaseProjection, archiveFibers, Nat.mod_self]
    rw [h_proj]
    unfold Matrix.mulVec dotProduct
    rw [Finset.sum_eq_single (⟨1, by unfold archiveFibers; omega⟩ : archivePhaseIndex n)]
    · have h_f1 : f ⟨1, by unfold archiveFibers; omega⟩ = 1 := by simp [f]
      have h01_ne : (⟨0, by unfold archiveFibers; omega⟩ : archivePhaseIndex n) ≠
                    ⟨1, by unfold archiveFibers; omega⟩ := by
        intro heq; exact absurd (congr_arg Fin.val heq) (by simp)
      unfold archiveCanonicalLaplacian
      dsimp only []
      rw [if_neg h01_ne, if_pos (cycle_zero_adj_one n hn), h_f1]
      ring
    · intro j _ hj_ne
      have hj_val : j.val ≠ 1 := fun hc => hj_ne (Fin.ext hc)
      simp [f, hj_val]
    · intro h; exact absurd (Finset.mem_univ _) h
  -- ── Contradiction: 0 = -1 ────────────────────────────────────────────────
  rw [h_lhs, h_rhs] at h_eq_coord
  norm_num at h_eq_coord

end D0
