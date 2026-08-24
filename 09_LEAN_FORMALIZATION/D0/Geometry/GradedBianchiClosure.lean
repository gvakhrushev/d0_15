import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic

open scoped BigOperators

namespace D0.Geometry

/-!
# Graded Bianchi closure — the discrete divergence bookkeeping

Finite-index analogue of the contracted Bianchi identity, in pure function form:

* `divergenceRow f i` — the row-sum divergence at index `i`;
* `IsDivergenceBalanced f` — all row sums coincide;
* `graded_bianchi_closure` — a symmetric tensor has equal row/column sums;
* `matTrace_einsteinTransform` — the Einstein transform is traceless;
* `einstein_balanced_of_balanced` — the Einstein transform preserves balance.
-/

variable {N : Type} [Fintype N] [DecidableEq N] [Nonempty N]

/-- Row-sum divergence of a finite tensor at index `i`. -/
def divergenceRow (f : N → N → ℝ) (i : N) : ℝ := ∑ j, f i j

/-- Divergence-balanced: all row sums coincide (discrete constant-curvature condition). -/
def IsDivergenceBalanced (f : N → N → ℝ) : Prop :=
  ∀ i j, divergenceRow f i = divergenceRow f j

/-- Matrix trace over the finite index. -/
def matTrace (f : N → N → ℝ) : ℝ := ∑ i, f i i

/-- The **mean-null normalization**: subtract the global mean entry `matTrace f / n` from every
    entry, making the total response vanish (`ΣΣ E = 0`).  SEMANTICS NOTE: this is a mean-null
    normalization, NOT the metric-trace (Einstein) adjustment `R − (tr R/n)·I`; the latter is
    the queued refinement — its coupling differs from raw by `(tr/n)·tr T`, which vanishes only
    on traceless sources.  Both transforms preserve divergence balance and symmetry. -/
noncomputable def einsteinTransform (f : N → N → ℝ) : N → N → ℝ :=
  fun i j => f i j - matTrace f / Fintype.card N

/-- **Graded Bianchi closure.**  A symmetric tensor has equal row/column sums. -/
theorem graded_bianchi_closure {f : N → N → ℝ} (hsym : ∀ i j, f i j = f j i) (i : N) :
    divergenceRow f i = ∑ j, f j i :=
  Finset.sum_congr rfl fun j _ => hsym i j

/-- Row sums of the Einstein transform: each equals the original row sum minus the mean. -/
theorem divergenceRow_einsteinTransform {f : N → N → ℝ} (k : N) :
    divergenceRow (einsteinTransform f) k = divergenceRow f k - matTrace f := by
  classical
  have hsplit : ∀ j : N, einsteinTransform f k j = f k j - matTrace f / Fintype.card N := by
    intro j
    rfl
  have hcardnn : (Fintype.card N : ℝ) ≠ 0 := by
    simpa using Fintype.card_pos (α := N)
  have hconst : ∑ _j : N, (matTrace f / Fintype.card N) = matTrace f := by
    rw [Finset.sum_const, nsmul_eq_mul, Finset.card_univ]
    field_simp
  unfold divergenceRow einsteinTransform
  simp only [hsplit, Finset.sum_sub_distrib, hconst]

/-- The Einstein transform is traceless. -/
theorem matTrace_einsteinTransform (f : N → N → ℝ) :
    matTrace (einsteinTransform f) = 0 := by
  classical
  have hcardnn : (Fintype.card N : ℝ) ≠ 0 := by
    simpa using Fintype.card_pos (α := N)
  have hspliteq : ∀ i : N,
      einsteinTransform f i i = f i i - matTrace f / Fintype.card N := by
    intro i
    rfl
  have hsum : ∑ i, einsteinTransform f i i
      = (∑ i, f i i) - matTrace f := by
    classical
    rw [Finset.sum_congr rfl fun i _ => hspliteq i, Finset.sum_sub_distrib]
    have hc : ∑ _x : N, (matTrace f / Fintype.card N) = matTrace f := by
      rw [Finset.sum_const, nsmul_eq_mul, Finset.card_univ]
      field_simp
    rw [hc]
  unfold matTrace
  rw [hsum, matTrace]
  ring

/-- Symmetry is preserved by the Einstein transform. -/
theorem einstein_symm {f : N → N → ℝ} (hsym : ∀ i j, f i j = f j i) :
    ∀ i j, einsteinTransform f i j = einsteinTransform f j i := by
  intro i j
  rw [einsteinTransform, einsteinTransform, hsym i j]

/-- The Einstein transform preserves divergence balance. -/
theorem einstein_balanced_of_balanced {f : N → N → ℝ} (hb : IsDivergenceBalanced f) :
    IsDivergenceBalanced (einsteinTransform f) := by
  intro i j
  rw [divergenceRow_einsteinTransform, divergenceRow_einsteinTransform, hb i j]

end D0.Geometry
