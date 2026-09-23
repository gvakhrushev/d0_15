import Mathlib.Data.ZMod.Basic
import Mathlib.LinearAlgebra.Dimension.Constructions
import Mathlib.LinearAlgebra.FiniteDimensional.Basic
import Mathlib.Tactic
import D0.Core.DyadABCD
import D0.Geometry.A4DCoframeParentConstraint
import D0.Geometry.A4DSymRoleCentralDifference
import D0.Geometry.ArchiveRefinementTower

/-!
# Radius-one scalar Ward classification

The pure-gauge Ward identity, inside the explicit radius-one scalar ansatz and for
`L ≥ 4`, cuts the symbol down to flat curls. Self-adjointness then leaves a
24-dimensional space. Simultaneous Role relabeling leaves a 1-dimensional
subspace. Neither count is a constitutive selection, and neither is a Lorentz
covariance theorem.

Supplying the full derivative `H(e)` on every uncentered coframe fixes that
derivative by extensionality. That is a different statement from the Ward kernel.
-/

namespace D0.Geometry

open D0
open scoped BigOperators Classical

/-- Matter-output and coframe-sampling offsets. Source offset and output offset
stay distinct indices. The nine values are `0` and `±e_r`. -/
inductive RadiusOneOffset where
  | zero
  | plus (r : Role)
  | minus (r : Role)
deriving DecidableEq, Fintype, Repr

abbrev SymIx := Role × RadiusOneOffset × Bool

abbrev SymSlice (K : Type*) := Role → RadiusOneOffset → K

def offsetCoord : RadiusOneOffset → Role → ℤ
  | .zero, _ => 0
  | .plus r, t => if t = r then 1 else 0
  | .minus r, t => if t = r then -1 else 0

/-- Integer landing site of one term in `C_dir(z) (z_dir - 1)`.
`branch = true` is multiplication by `z_dir`. -/
def land (i : SymIx) (t : Role) : ℤ :=
  offsetCoord i.2.1 t + if i.2.2 = true ∧ t = i.1 then 1 else 0

def symbolTerm {K : Type*} [Ring K] (c : SymSlice K) (i : SymIx) : K :=
  if i.2.2 then c i.1 i.2.1 else -c i.1 i.2.1

def rawCoeff {K : Type*} [Ring K] (c : SymSlice K) (v : Role → ℤ) : K :=
  ∑ i : SymIx, if land i = v then symbolTerm c i else 0

def doubleVec (r : Role) : Role → ℤ := fun t => if t = r then 2 else 0

def axisVec (r : Role) : Role → ℤ := fun t => if t = r then 1 else 0

def negVec (r : Role) : Role → ℤ := fun t => if t = r then -1 else 0

def sumVec (r s : Role) : Role → ℤ :=
  fun t => (if t = r then 1 else 0) + (if t = s then 1 else 0)

def diffVec (r s : Role) : Role → ℤ :=
  fun t => (if t = r then 1 else 0) + (if t = s then -1 else 0)

lemma land_coord_eq_two (i : SymIx) (t : Role) (h : land i t = 2) :
    i = (t, .plus t, true) := by
  rcases i with ⟨dir, j, branch⟩
  cases j with
  | zero =>
      cases branch with
      | false => simp [land, offsetCoord] at h
      | true =>
          simp [land, offsetCoord] at h
          omega
  | minus q =>
      cases branch <;> simp [land, offsetCoord] at h <;>
        by_cases htq : t = q <;> simp [htq] at h <;> omega
  | plus q =>
      cases branch with
      | false =>
          simp [land, offsetCoord] at h
          by_cases htq : t = q <;> simp [htq] at h
      | true =>
          by_cases htd : t = dir
          · subst htd
            by_cases htq : t = q
            · subst htq
              rfl
            · rw [land, offsetCoord, if_neg htq] at h
              norm_num at h
          · by_cases htq : t = q
            · subst htq
              dsimp [land, offsetCoord] at h
              simp [htd] at h
            · dsimp [land, offsetCoord] at h
              simp [htd, htq] at h

lemma land_neg_support (i : SymIx) (r : Role) :
    (fun t => land i t) = negVec r ↔ ∃ dir, i = (dir, .minus r, false) := by
  decide +revert

lemma land_diff_iff (i : SymIx) (r s : Role) (hrs : r ≠ s) :
    (fun t => land i t) = diffVec r s ↔ i = (r, .minus s, true) := by
  decide +revert

lemma land_sum_support (i : SymIx) (r s : Role) (hrs : r ≠ s) :
    (fun t => land i t) = sumVec r s ↔
      i = (r, .plus s, true) ∨ i = (s, .plus r, true) := by
  decide +revert

lemma land_double_iff (i : SymIx) (r : Role) :
    (fun t => land i t) = doubleVec r ↔ i = (r, .plus r, true) := by
  constructor
  · intro h
    have hr : land i r = 2 := by simpa [doubleVec] using congr_fun h r
    exact land_coord_eq_two i r hr
  · intro h
    subst h
    funext t
    by_cases ht : t = r <;> simp [land, offsetCoord, doubleVec, ht]

def roleIndex (r : Role) : ℕ := r.1.val * 2 + r.2.val

lemma roleIndex_lt_four (r : Role) : roleIndex r < 4 := by
  rcases r with ⟨a, b⟩
  fin_cases a <;> fin_cases b <;> decide

abbrev OrderedPair := {p : Role × Role // roleIndex p.1 < roleIndex p.2}

def antisymCoeff {K : Type*} [Ring K] (κ : OrderedPair → K) (r s : Role) : K :=
  if h : roleIndex r < roleIndex s then κ ⟨(r, s), h⟩
  else if h : roleIndex s < roleIndex r then -κ ⟨(s, r), h⟩
  else 0

/-- `C_dir = ∑_{s ≠ dir} κ_dir s (z_s - 1)`. -/
def curlSlice {K : Type*} [Ring K] (κ : OrderedPair → K) : SymSlice K :=
  fun dir j =>
    match j with
    | .zero => -∑ s : Role, antisymCoeff κ dir s
    | .plus s => antisymCoeff κ dir s
    | .minus _ => 0

def basisCurl (p : OrderedPair) : SymSlice ℚ :=
  curlSlice (fun q => if q = p then (1 : ℚ) else 0)

lemma basisCurl_raw_on_land (p : OrderedPair) (i : SymIx) :
    rawCoeff (basisCurl p) (fun t => land i t) = 0 := by
  native_decide +revert

lemma land_axis_support (i : SymIx) (r : Role) :
    (fun t => land i t) = axisVec r ↔
      i = (r, .zero, true) ∨ ∃ dir, i = (dir, .plus r, false) := by
  decide +revert

variable {K : Type*} [Ring K]

lemma symbolTerm_true (c : SymSlice K) (dir : Role) (j : RadiusOneOffset) :
    symbolTerm c (dir, j, true) = c dir j := by
  simp [symbolTerm]

lemma symbolTerm_false (c : SymSlice K) (dir : Role) (j : RadiusOneOffset) :
    symbolTerm c (dir, j, false) = -c dir j := by
  simp [symbolTerm]

lemma rawCoeff_unique (c : SymSlice K) (v : Role → ℤ) (i0 : SymIx)
    (h : ∀ i, (fun t => land i t) = v ↔ i = i0) :
    rawCoeff c v = symbolTerm c i0 := by
  classical
  unfold rawCoeff
  rw [Finset.sum_eq_single i0]
  · have hl : (fun t => land i0 t) = v := (h i0).2 rfl
    simp [hl]
  · intro i _ hi
    have hne : (fun t => land i t) ≠ v := fun hv => hi ((h i).1 hv)
    simp [hne]
  · intro hmem
    exact absurd (Finset.mem_univ i0) hmem

lemma rawCoeff_double (c : SymSlice K) (r : Role) :
    rawCoeff c (doubleVec r) = c r (.plus r) := by
  simpa [symbolTerm] using
    rawCoeff_unique c (doubleVec r) (r, .plus r, true) (fun i => land_double_iff i r)

lemma rawCoeff_diff (c : SymSlice K) (r s : Role) (hrs : r ≠ s) :
    rawCoeff c (diffVec r s) = c r (.minus s) := by
  simpa [symbolTerm] using
    rawCoeff_unique c (diffVec r s) (r, .minus s, true) (fun i => land_diff_iff i r s hrs)

lemma rawCoeff_sum (c : SymSlice K) (r s : Role) (hrs : r ≠ s) :
    rawCoeff c (sumVec r s) = c r (.plus s) + c s (.plus r) := by
  classical
  unfold rawCoeff
  let i1 : SymIx := (r, .plus s, true)
  let i2 : SymIx := (s, .plus r, true)
  have hne : i1 ≠ i2 := by
    intro h
    exact hrs (congrArg (fun i => i.1) h)
  have hif : ∀ i, (if (fun t => land i t) = sumVec r s then symbolTerm c i else 0) =
      (if i = i1 then symbolTerm c i else 0) + (if i = i2 then symbolTerm c i else 0) := by
    intro i
    by_cases h1 : i = i1
    · subst h1
      have hl : (fun t => land i1 t) = sumVec r s := (land_sum_support i1 r s hrs).2 (Or.inl rfl)
      simp [hne, hl, symbolTerm]
    · by_cases h2 : i = i2
      · subst h2
        have hl : (fun t => land i2 t) = sumVec r s :=
          (land_sum_support i2 r s hrs).2 (Or.inr rfl)
        simp [h1, hl, symbolTerm]
      · have hland : (fun t => land i t) ≠ sumVec r s := by
          intro hl
          rcases (land_sum_support i r s hrs).1 hl with h | h
          · exact h1 h
          · exact h2 h
        simp [h1, h2, hland]
  simp only [hif]
  simp [i1, i2, Finset.sum_add_distrib, Finset.sum_ite_eq', Finset.mem_univ, symbolTerm]

lemma rawCoeff_neg (c : SymSlice K) (r : Role) :
    rawCoeff c (negVec r) = -∑ dir, c dir (.minus r) := by
  classical
  unfold rawCoeff
  have himage :
      (Finset.univ.filter (fun i : SymIx => (fun t => land i t) = negVec r)) =
        (Finset.univ : Finset Role).image (fun dir => (dir, .minus r, false)) := by
    ext i
    simp only [Finset.mem_filter, Finset.mem_univ, true_and, Finset.mem_image]
    constructor
    · intro h
      rcases (land_neg_support i r).1 h with ⟨dir, hdir⟩
      exact ⟨dir, hdir.symm⟩
    · rintro ⟨dir, hdir⟩
      exact (land_neg_support i r).2 ⟨dir, hdir.symm⟩
  rw [← Finset.sum_filter]
  rw [himage]
  rw [Finset.sum_image (by
    intro d1 _ d2 _ h
    simpa using h)]
  simp [symbolTerm, Finset.sum_neg_distrib]

lemma rawCoeff_axis (c : SymSlice K) (r : Role) :
    rawCoeff c (axisVec r) = c r .zero - ∑ dir, c dir (.plus r) := by
  classical
  unfold rawCoeff
  let iz : SymIx := (r, .zero, true)
  let emb : Role → SymIx := fun dir => (dir, .plus r, false)
  have hempty : ∀ dir, iz ≠ emb dir := by
    intro dir heq
    have hcomp := congrArg (fun i : SymIx => i.2.1) heq
    simp [iz, emb] at hcomp
  have himage :
      (Finset.univ.filter (fun i : SymIx => (fun t => land i t) = axisVec r)) =
        insert iz ((Finset.univ : Finset Role).image emb) := by
    ext i
    simp only [Finset.mem_filter, Finset.mem_univ, true_and, Finset.mem_insert, Finset.mem_image]
    constructor
    · intro hland
      rcases (land_axis_support i r).1 hland with h | ⟨dir, hdir⟩
      · exact Or.inl h
      · exact Or.inr ⟨dir, hdir.symm⟩
    · intro h
      rcases h with h | ⟨dir, hdir⟩
      · exact (land_axis_support i r).2 (Or.inl h)
      · exact (land_axis_support i r).2 (Or.inr ⟨dir, hdir.symm⟩)
  rw [← Finset.sum_filter, himage]
  have hnotmem : iz ∉ (Finset.univ : Finset Role).image emb := by
    intro hmem
    rcases Finset.mem_image.mp hmem with ⟨dir, -, hdir⟩
    exact hempty dir hdir.symm
  rw [Finset.sum_insert hnotmem]
  rw [Finset.sum_image (by
    intro d1 _ d2 _ h
    simpa [emb] using h)]
  simp [iz, emb, symbolTerm, sub_eq_add_neg, Finset.sum_neg_distrib]

def IsRawSyzygy (c : SymSlice K) : Prop := ∀ v, rawCoeff c v = 0

lemma rawCoeff_offLand (c : SymSlice K) (v : Role → ℤ)
    (h : ∀ i, (fun t => land i t) ≠ v) : rawCoeff c v = 0 := by
  classical
  unfold rawCoeff
  refine Finset.sum_eq_zero ?_
  intro i _
  simp [h i]

lemma symbolTerm_add (c d : SymSlice K) (i : SymIx) :
    symbolTerm (c + d) i = symbolTerm c i + symbolTerm d i := by
  unfold symbolTerm
  by_cases h : i.2.2
  · simp [h, Pi.add_apply]
  · simp [h, Pi.add_apply, add_comm]

lemma symbolTerm_smul (a : K) (c : SymSlice K) (i : SymIx) :
    symbolTerm (a • c) i = a * symbolTerm c i := by
  unfold symbolTerm
  by_cases h : i.2.2 <;> simp [h, Pi.smul_apply, smul_eq_mul, mul_neg]

lemma rawCoeff_add (c d : SymSlice K) (v : Role → ℤ) :
    rawCoeff (c + d) v = rawCoeff c v + rawCoeff d v := by
  classical
  simp only [rawCoeff, symbolTerm_add, ← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl ?_
  intro i _
  by_cases h : (fun t => land i t) = v <;> simp [h]

lemma rawCoeff_smul (a : K) (c : SymSlice K) (v : Role → ℤ) :
    rawCoeff (a • c) v = a * rawCoeff c v := by
  classical
  simp only [rawCoeff, symbolTerm_smul]
  rw [Finset.mul_sum]
  refine Finset.sum_congr rfl ?_
  intro i _
  by_cases h : (fun t => land i t) = v <;> simp [h, mul_zero]

lemma curlSlice_add (κ₁ κ₂ : OrderedPair → K) :
    curlSlice (κ₁ + κ₂) = curlSlice κ₁ + curlSlice κ₂ := by
  ext dir j
  cases j with
  | minus r => simp [curlSlice]
  | plus s =>
      simp only [curlSlice, Pi.add_apply, antisymCoeff]
      split_ifs <;> abel
  | zero =>
      simp only [curlSlice, Pi.add_apply]
      have hs : ∀ s, antisymCoeff (κ₁ + κ₂) dir s =
          antisymCoeff κ₁ dir s + antisymCoeff κ₂ dir s := by
        intro s
        simp only [antisymCoeff, Pi.add_apply]
        split_ifs <;> abel
      simp only [hs, Finset.sum_add_distrib, neg_add]

lemma antisymCoeff_smul (a : K) (κ : OrderedPair → K) (r s : Role) :
    antisymCoeff (a • κ) r s = a * antisymCoeff κ r s := by
  unfold antisymCoeff
  by_cases h1 : roleIndex r < roleIndex s
  · simp [h1, Pi.smul_apply, smul_eq_mul]
  · by_cases h2 : roleIndex s < roleIndex r
    · simp [h1, h2, Pi.smul_apply, smul_eq_mul, mul_neg]
    · simp [h1, h2, mul_zero]

lemma curlSlice_smul (a : K) (κ : OrderedPair → K) :
    curlSlice (a • κ) = a • curlSlice κ := by
  ext dir j
  cases j with
  | minus r => simp [curlSlice]
  | plus s =>
      simp only [curlSlice, Pi.smul_apply, smul_eq_mul, antisymCoeff_smul]
  | zero =>
      simp only [curlSlice, Pi.smul_apply, smul_eq_mul, antisymCoeff_smul,
        Finset.mul_sum, mul_neg]

lemma antisym_sum (κ : OrderedPair → ℚ) (a b : Role) :
    antisymCoeff κ a b =
      ∑ p, κ p * antisymCoeff (fun q => if q = p then (1 : ℚ) else 0) a b := by
  classical
  unfold antisymCoeff
  by_cases h : roleIndex a < roleIndex b
  · simp [h, Finset.mem_univ, mul_ite, mul_one, mul_zero]
  · by_cases h2 : roleIndex b < roleIndex a
    · simp [h, h2, Finset.mem_univ, mul_ite, mul_neg, mul_one, mul_zero]
    · simp [h, h2]

lemma curlSlice_sum (κ : OrderedPair → ℚ) :
    curlSlice κ = ∑ p, κ p • basisCurl p := by
  ext dir j
  cases j with
  | minus r =>
      simp [curlSlice, basisCurl]
  | plus s =>
      simp only [curlSlice, basisCurl, Pi.smul_apply, Finset.sum_apply]
      rw [antisym_sum]
      simp [antisymCoeff]
  | zero =>
      simp only [curlSlice, basisCurl, Pi.smul_apply, smul_eq_mul, Finset.sum_apply]
      have hs : ∑ s, antisymCoeff κ dir s =
          ∑ s, ∑ p, κ p * antisymCoeff (fun q => if q = p then (1 : ℚ) else 0) dir s := by
        refine Finset.sum_congr rfl ?_
        intro s _
        exact antisym_sum κ dir s
      rw [hs, Finset.sum_comm]
      simp [mul_neg, Finset.mul_sum]

lemma rawCoeff_fsum {ι : Type*} [Fintype ι] [DecidableEq ι]
    (s : Finset ι) (f : ι → SymSlice ℚ) (v : Role → ℤ) :
    rawCoeff (∑ p ∈ s, f p) v = ∑ p ∈ s, rawCoeff (f p) v := by
  classical
  induction s using Finset.induction with
  | empty =>
      simp [rawCoeff, symbolTerm]
  | insert p s hp ih =>
      simp [Finset.sum_insert hp, rawCoeff_add, ih]

lemma basisCurl_syzygy (p : OrderedPair) (v : Role → ℤ) :
    rawCoeff (basisCurl p) v = 0 := by
  classical
  by_cases h : ∃ i, (fun t => land i t) = v
  · rcases h with ⟨i, rfl⟩
    exact basisCurl_raw_on_land p i
  · push Not at h
    exact rawCoeff_offLand _ _ h

lemma curlSlice_syzygy (κ : OrderedPair → ℚ) (v : Role → ℤ) :
    rawCoeff (curlSlice κ) v = 0 := by
  rw [curlSlice_sum]
  rw [rawCoeff_fsum]
  simp only [rawCoeff_smul, basisCurl_syzygy, mul_zero, Finset.sum_const_zero]

lemma roleIndex_injective : Function.Injective roleIndex := by
  intro r s h
  rcases r with ⟨a, b⟩
  rcases s with ⟨c, d⟩
  fin_cases a <;> fin_cases b <;> fin_cases c <;> fin_cases d <;>
    simp [roleIndex] at h ⊢

lemma roleIndex_trichotomy (r s : Role) :
    roleIndex r < roleIndex s ∨ r = s ∨ roleIndex s < roleIndex r := by
  rcases lt_trichotomy (roleIndex r) (roleIndex s) with h | h | h
  · exact Or.inl h
  · exact Or.inr (Or.inl (roleIndex_injective h))
  · exact Or.inr (Or.inr h)

/-- Every bounded symbol with vanishing `∑_r C_r(z)(z_r-1)` is a flat curl, and conversely. -/
theorem boundedLaurent_syzygy_iff_curl (c : SymSlice ℚ) :
    IsRawSyzygy c ↔ ∃ κ : OrderedPair → ℚ, c = curlSlice κ := by
  constructor
  · intro hsy
    let κ : OrderedPair → ℚ := fun p => c p.1.1 (.plus p.1.2)
    have hdiag : ∀ r, c r (.plus r) = 0 := by
      intro r
      simpa [rawCoeff_double] using hsy (doubleVec r)
    have hskew : ∀ r s, r ≠ s → c r (.plus s) + c s (.plus r) = 0 := by
      intro r s hrs
      simpa [rawCoeff_sum _ _ _ hrs] using hsy (sumVec r s)
    have hminus_off : ∀ r s, r ≠ s → c r (.minus s) = 0 := by
      intro r s hrs
      simpa [rawCoeff_diff _ _ _ hrs] using hsy (diffVec r s)
    have hminus_diag : ∀ r, c r (.minus r) = 0 := by
      intro r
      have hneg := hsy (negVec r)
      rw [rawCoeff_neg] at hneg
      have hsum : ∑ t, c t (.minus r) = c r (.minus r) := by
        classical
        refine Finset.sum_eq_single r ?_ ?_
        · intro t _ ht
          exact hminus_off t r ht
        · intro hmem
          exact absurd (Finset.mem_univ r) hmem
      linarith
    have hzero : ∀ r, c r .zero = -∑ s, c r (.plus s) := by
      intro r
      have haxis := hsy (axisVec r)
      rw [rawCoeff_axis] at haxis
      have hterm : ∀ t, c t (.plus r) = -c r (.plus t) := by
        intro t
        by_cases ht : t = r
        · subst ht
          rw [hdiag]
          simp
        · have hsk := hskew t r ht
          linear_combination hsk
      have hsum : (∑ t, c t (.plus r)) = -∑ s, c r (.plus s) := by
        simp only [hterm, Finset.sum_neg_distrib]
      rw [hsum, sub_neg_eq_add] at haxis
      linarith
    refine ⟨κ, ?_⟩
    ext dir j
    cases j with
    | plus s =>
        rcases roleIndex_trichotomy dir s with hlt | heq | hgt
        · simp [curlSlice, antisymCoeff, hlt, κ]
        · subst heq
          simp [curlSlice, antisymCoeff, hdiag]
        · have hne : dir ≠ s := by
            intro h
            exact (ne_of_lt hgt) (congrArg roleIndex h.symm)
          have hsk := hskew dir s hne
          have hnot : ¬ roleIndex dir < roleIndex s := not_lt_of_gt hgt
          have hanti : antisymCoeff κ dir s = -c s (.plus dir) := by
            simp [antisymCoeff, hnot, hgt, κ]
          simp only [curlSlice, hanti]
          linear_combination hsk
    | minus s =>
        by_cases hds : dir = s
        · subst hds
          simp [curlSlice, hminus_diag]
        · simp [curlSlice, hminus_off dir s hds]
    | zero =>
        classical
        have hanti_sum : ∑ s, antisymCoeff κ dir s = ∑ s, c dir (.plus s) := by
          refine Finset.sum_congr rfl ?_
          intro s _
          rcases roleIndex_trichotomy dir s with hlt | heq | hgt
          · simp [antisymCoeff, hlt, κ]
          · subst heq
            simp [antisymCoeff, hdiag]
          · have hne : dir ≠ s := by
              intro h
              exact (ne_of_lt hgt) (congrArg roleIndex h.symm)
            have hsk := hskew dir s hne
            have hnot : ¬ roleIndex dir < roleIndex s := not_lt_of_gt hgt
            have hanti : antisymCoeff κ dir s = -c s (.plus dir) := by
              simp [antisymCoeff, hnot, hgt, κ]
            rw [hanti]
            exact (add_eq_zero_iff_eq_neg.mp hsk).symm
        simp only [curlSlice, hzero, hanti_sum]
  · rintro ⟨κ, rfl⟩
    intro v
    exact curlSlice_syzygy κ v

/-! ## Dimension six, for one output shift and one internal component -/

lemma orderedPair_card : Fintype.card OrderedPair = 6 := by
  native_decide

lemma curlSlice_plus_ordered (κ : OrderedPair → ℚ) (p : OrderedPair) :
    curlSlice κ p.1.1 (.plus p.1.2) = κ p := by
  simp [curlSlice, antisymCoeff, p.2]

lemma curlSlice_injective :
    Function.Injective (curlSlice : (OrderedPair → ℚ) → SymSlice ℚ) := by
  intro κ₁ κ₂ h
  ext p
  have hplus := congr_fun (congr_fun h p.1.1) (.plus p.1.2)
  simpa [curlSlice_plus_ordered] using hplus

def rawSyzygy : Submodule ℚ (SymSlice ℚ) where
  carrier := {c | IsRawSyzygy c}
  add_mem' := by
    intro c d hc hd v
    rw [rawCoeff_add, hc v, hd v, add_zero]
  zero_mem' := by
    intro v
    classical
    simp [rawCoeff, symbolTerm]
  smul_mem' := by
    intro a c hc v
    rw [rawCoeff_smul, hc v, mul_zero]

def curlSliceLinear : (OrderedPair → ℚ) →ₗ[ℚ] rawSyzygy where
  toFun κ := ⟨curlSlice κ, fun v => curlSlice_syzygy κ v⟩
  map_add' κ₁ κ₂ := by
    apply Subtype.ext
    exact curlSlice_add κ₁ κ₂
  map_smul' a κ := by
    apply Subtype.ext
    simpa using curlSlice_smul a κ

/-- One fixed output shift and one internal component. The count is the number
of ordered Role pairs. It is the `L ≥ 4` symbol count only together with
`gauge_symbol_iff_laurent_syzygy`. -/
theorem boundedLaurent_syzygy_finrank_six :
    Module.finrank ℚ rawSyzygy = 6 := by
  classical
  let e : (OrderedPair → ℚ) ≃ₗ[ℚ] rawSyzygy :=
    LinearEquiv.ofBijective curlSliceLinear
      ⟨fun κ₁ κ₂ h => curlSlice_injective (congrArg Subtype.val h),
       fun c => by
         rcases (boundedLaurent_syzygy_iff_curl c.1).1 c.2 with ⟨κ, hκ⟩
         exact ⟨κ, Subtype.ext hκ.symm⟩⟩
  rw [← e.finrank_eq, Module.finrank_fintype_fun_eq_card]
  simpa using orderedPair_card

/-! ## Group algebra for `L = N + 2 ≥ 4` -/

lemma land_coord_window (i : SymIx) (t : Role) : -1 ≤ land i t ∧ land i t ≤ 2 := by
  decide +revert

lemma window_intCast_injective {L : ℕ} (hL : 4 ≤ L) {a b : ℤ}
    (ha : -1 ≤ a ∧ a ≤ 2) (hb : -1 ≤ b ∧ b ≤ 2)
    (h : (a : ZMod L) = (b : ZMod L)) : a = b := by
  have hdvd : (L : ℤ) ∣ b - a := (ZMod.intCast_eq_intCast_iff_dvd_sub a b L).1 h
  obtain ⟨k, hk⟩ := hdvd
  have hdiff : -3 ≤ b - a ∧ b - a ≤ 3 := by omega
  have hk0 : k = 0 := by
    by_contra hne
    have hone : (1 : ℤ) ≤ |k| := by
      rcases le_or_gt 0 k with hk | hk
      · have hkpos : 0 < k := lt_of_le_of_ne hk (Ne.symm hne)
        rw [abs_of_nonneg hk]
        omega
      · rw [abs_of_neg hk]
        omega
    have hL0 : (0 : ℤ) ≤ (L : ℤ) := by exact_mod_cast (Nat.zero_le L)
    have hLabs : (4 : ℤ) ≤ |(L : ℤ)| := by
      rw [abs_of_nonneg hL0]
      exact_mod_cast hL
    have hmul : (4 : ℤ) ≤ |(L : ℤ) * k| := by
      rw [abs_mul]
      nlinarith
    have hsmall : |(L : ℤ) * k| ≤ 3 := by
      rw [← hk]
      exact abs_le.mpr hdiff
    omega
  rw [hk0, mul_zero] at hk
  omega

/-- Landing site in `(ℤ/Lℤ)^4`, `L = archiveFibers N = N + 2`. -/
def groupLand (N : ℕ) (i : SymIx) : Role → ZMod (archiveFibers N) :=
  fun t => (land i t : ZMod _)

/-- Coefficient of `∑_r C_r(z) (z_r - 1)` in the group algebra. -/
def groupCoeff (N : ℕ) (c : SymSlice ℚ) (g : Role → ZMod (archiveFibers N)) : ℚ :=
  ∑ i : SymIx, if groupLand N i = g then symbolTerm c i else 0

lemma land_eq_of_groupLand {N : ℕ} (hN : 2 ≤ N) {i j : SymIx}
    (h : groupLand N i = groupLand N j) :
    (fun t => land i t) = fun t => land j t := by
  funext t
  apply window_intCast_injective (L := archiveFibers N)
  · simp [archiveFibers]
    omega
  · exact land_coord_window i t
  · exact land_coord_window j t
  · exact congr_fun h t

lemma groupCoeff_eq_raw_on_land {N : ℕ} (hN : 2 ≤ N) (c : SymSlice ℚ) (i0 : SymIx) :
    groupCoeff N c (groupLand N i0) = rawCoeff c (fun t => land i0 t) := by
  classical
  simp only [groupCoeff, rawCoeff]
  refine Finset.sum_congr rfl ?_
  intro i _
  by_cases h : (fun t => land i t) = fun t => land i0 t
  · have hg : groupLand N i = groupLand N i0 := by
      funext t
      exact congrArg (fun n : ℤ => (n : ZMod (archiveFibers N))) (congr_fun h t)
    simp [h, hg]
  · have hg : groupLand N i ≠ groupLand N i0 := by
      intro heq
      exact h (land_eq_of_groupLand hN heq)
    simp [h, hg]

lemma groupCoeff_add (N : ℕ) (c d : SymSlice ℚ) (g : Role → ZMod (archiveFibers N)) :
    groupCoeff N (c + d) g = groupCoeff N c g + groupCoeff N d g := by
  classical
  simp only [groupCoeff, symbolTerm_add, ← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl ?_
  intro i _
  by_cases h : groupLand N i = g <;> simp [h]

lemma groupCoeff_smul (N : ℕ) (a : ℚ) (c : SymSlice ℚ) (g : Role → ZMod (archiveFibers N)) :
    groupCoeff N (a • c) g = a * groupCoeff N c g := by
  classical
  simp only [groupCoeff, symbolTerm_smul]
  rw [Finset.mul_sum]
  refine Finset.sum_congr rfl ?_
  intro i _
  by_cases h : groupLand N i = g <;> simp [h, mul_zero]

/-- For `L ≥ 4`, Ward vanishing in the group algebra is the flat-curl equation.
This is not stated for `L = 2` or `L = 3`: those periods alias the same monomials. -/
theorem gauge_symbol_iff_laurent_syzygy (N : ℕ) (hN : 2 ≤ N) (c : SymSlice ℚ) :
    (∀ g, groupCoeff N c g = 0) ↔ ∃ κ : OrderedPair → ℚ, c = curlSlice κ := by
  constructor
  · intro hg
    refine (boundedLaurent_syzygy_iff_curl c).1 ?_
    intro v
    by_cases hhit : ∃ i, (fun t => land i t) = v
    · rcases hhit with ⟨i, rfl⟩
      rw [← groupCoeff_eq_raw_on_land hN c i]
      exact hg _
    · push Not at hhit
      exact rawCoeff_offLand c v hhit
  · rintro ⟨κ, rfl⟩ g
    by_cases hhit : ∃ i, groupLand N i = g
    · rcases hhit with ⟨i, rfl⟩
      rw [groupCoeff_eq_raw_on_land hN]
      exact curlSlice_syzygy κ _
    · push Not at hhit
      classical
      simp only [groupCoeff]
      exact Finset.sum_eq_zero (fun i _ => by simp [hhit i])

/-! ## Flat finite curls. Not affine torsion at nonzero curvature. -/

/-- Unnormalized step `U_r - I`. Owned `forwardDifference` is this step times `L`. -/
def stepDifference (N : ℕ) (r : Role) (f : ArchiveRolePhaseGroup N → ℝ) :
    ArchiveRolePhaseGroup N → ℝ :=
  fun x => f (roleTranslatePlus N r x) - f x

/-- `T_rs^b(e) = Δ_r e_s^b - Δ_s e_r^b`. -/
def finiteCurl (N : ℕ) (r s b : Role) (e : LocalCoframeField N) :
    ArchiveRolePhaseGroup N → ℝ :=
  fun x =>
    stepDifference N r (fun y => e y s b) x -
      stepDifference N s (fun y => e y r b) x

theorem finiteCurl_forwardGauge (N : ℕ) (r s b : Role) (ξ : LocalRoleVector N) :
    finiteCurl N r s b (forwardGaugeCoframe N ξ) = 0 := by
  funext x
  have hcomm : roleTranslatePlus N r (roleTranslatePlus N s x) =
      roleTranslatePlus N s (roleTranslatePlus N r x) := by
    funext t
    simp only [roleTranslatePlus_apply, Pi.add_apply]
    abel
  simp only [finiteCurl, stepDifference, forwardGaugeCoframe, forwardDifference_apply]
  rw [hcomm]
  set A := ξ (roleTranslatePlus N s (roleTranslatePlus N r x)) b
  set B := ξ (roleTranslatePlus N r x) b
  set C := ξ (roleTranslatePlus N s x) b
  set D := ξ x b
  set Ls := forwardDifferenceScale N
  change Ls * (A - B) - Ls * (C - D) - (Ls * (A - C) - Ls * (B - D)) = 0
  ring

/-! ## Self-adjointness removes nonzero matter-output shifts

The adjoint of “multiply by a sampled coframe and shift the output by `a`” samples the
coframe at the translated offset `j - a`. Inside this radius-one ansatz that offset has
to stay in `{0, ±e_r}`. A nonzero curl always has a sample that leaves the stencil when
`a ≠ 0`. This is not a claim about arbitrary physical Lorentz covariance.
-/

def coordEq (v : Role → ℤ) (j : RadiusOneOffset) : Bool :=
  decide (offsetCoord j A = v A) && decide (offsetCoord j B = v B) &&
    decide (offsetCoord j C = v C) && decide (offsetCoord j D = v D)

/-- The nine-point stencil, tested on the four Role coordinates. -/
def hitsStencil (v : Role → ℤ) : Bool :=
  coordEq v .zero ||
    coordEq v (.plus A) || coordEq v (.plus B) || coordEq v (.plus C) || coordEq v (.plus D) ||
    coordEq v (.minus A) || coordEq v (.minus B) || coordEq v (.minus C) || coordEq v (.minus D)

def offsetInStencil (v : Role → ℤ) : Prop := hitsStencil v = true

/-- Nonzero samples of a symbol, after the adjoint translation by `-a`, still land in
the nine-point stencil. -/
def StaysInAnsatz (a : RadiusOneOffset) (c : SymSlice ℚ) : Prop :=
  ∀ dir j, c dir j ≠ 0 →
    offsetInStencil (fun t => offsetCoord j t - offsetCoord a t)

lemma adjointSample_escapes (a : RadiusOneOffset) (p : OrderedPair) :
    a = .zero ∨
      hitsStencil (fun t => offsetCoord (.plus p.1.2) t - offsetCoord a t) = false ∨
      hitsStencil (fun t => offsetCoord (.plus p.1.1) t - offsetCoord a t) = false := by
  revert a p
  native_decide

lemma curlSlice_plus_swap (κ : OrderedPair → ℚ) (p : OrderedPair) :
    curlSlice κ p.1.2 (.plus p.1.1) = -κ p := by
  have hlt : roleIndex p.1.1 < roleIndex p.1.2 := p.2
  have hnot : ¬ roleIndex p.1.2 < roleIndex p.1.1 := not_lt_of_gt hlt
  simp [curlSlice, antisymCoeff, hnot, hlt]

lemma curl_stays_only_zero (a : RadiusOneOffset) (ha : a ≠ .zero)
    (κ : OrderedPair → ℚ) (hstay : StaysInAnsatz a (curlSlice κ)) : κ = 0 := by
  ext p
  by_contra hne
  have hpos : curlSlice κ p.1.1 (.plus p.1.2) ≠ 0 := by
    simpa [curlSlice_plus_ordered] using hne
  have hneg : curlSlice κ p.1.2 (.plus p.1.1) ≠ 0 := by
    simpa [curlSlice_plus_swap] using neg_ne_zero.mpr hne
  rcases adjointSample_escapes a p with hzero | h1 | h2
  · exact (ha hzero).elim
  · exact Bool.noConfusion (h1.symm.trans (hstay _ _ hpos))
  · exact Bool.noConfusion (h2.symm.trans (hstay _ _ hneg))

/-- Output shift `0` carries an arbitrary curl. Every other output shift is zero. -/
def wardDiagonalOf (κ : Role → OrderedPair → ℚ) :
    RadiusOneOffset → Role → SymSlice ℚ :=
  fun a b => if a = .zero then curlSlice (κ b) else 0

/-- `L ≥ 4` self-adjoint radius-one Ward data. The hypothesis is the group-algebra
syzygy, so the count is not claimed at `L = 2` or `L = 3`. -/
def WardKernel (N : ℕ) : Submodule ℚ (RadiusOneOffset → Role → SymSlice ℚ) where
  carrier := {c |
    (∀ a b g, groupCoeff N (c a b) g = 0) ∧
    (∀ a b, a ≠ .zero → StaysInAnsatz a (c a b))}
  add_mem' := by
    intro c d hc hd
    refine ⟨?_, ?_⟩
    · intro a b g
      have hsum : groupCoeff N ((c + d) a b) g =
          groupCoeff N (c a b) g + groupCoeff N (d a b) g := by
        simpa [Pi.add_apply] using groupCoeff_add N (c a b) (d a b) g
      rw [hsum, hc.1 a b g, hd.1 a b g, add_zero]
    · intro a b ha dir j hsum
      by_cases hz : c a b dir j = 0
      · have hdz : d a b dir j ≠ 0 := by
          intro hdz
          apply hsum
          simp [hz, hdz, Pi.add_apply]
        exact hd.2 a b ha dir j hdz
      · exact hc.2 a b ha dir j hz
  zero_mem' := by
    refine ⟨?_, ?_⟩
    · intro a b g
      classical
      simp only [groupCoeff, symbolTerm]
      exact Finset.sum_eq_zero (fun i _ => by split_ifs <;> simp)
    · intro a b ha dir j hne
      simp at hne
  smul_mem' := by
    intro t c hc
    refine ⟨?_, ?_⟩
    · intro a b g
      have hsm : groupCoeff N ((t • c) a b) g = t * groupCoeff N (c a b) g := by
        simpa [Pi.smul_apply] using groupCoeff_smul N t (c a b) g
      rw [hsm, hc.1 a b g, mul_zero]
    · intro a b ha dir j hne
      have hc0 : c a b dir j ≠ 0 := by
        intro hz
        apply hne
        simp [hz, Pi.smul_apply, smul_eq_mul]
      exact hc.2 a b ha dir j hc0

lemma wardDiagonalOf_mem (N : ℕ) (hN : 2 ≤ N) (κ : Role → OrderedPair → ℚ) :
    wardDiagonalOf κ ∈ WardKernel N := by
  refine ⟨?_, ?_⟩
  · intro a b g
    by_cases ha : a = .zero
    · have hg :=
        ((gauge_symbol_iff_laurent_syzygy N hN (curlSlice (κ b))).2 ⟨κ b, rfl⟩) g
      simpa [wardDiagonalOf, ha] using hg
    · classical
      simp only [wardDiagonalOf, if_neg ha, groupCoeff, symbolTerm]
      exact Finset.sum_eq_zero (fun i _ => by split_ifs <;> simp)
  · intro a b ha dir j hne
    simp [wardDiagonalOf, ha] at hne

def diagonalLinear (N : ℕ) (hN : 2 ≤ N) :
    (Role → OrderedPair → ℚ) →ₗ[ℚ] WardKernel N where
  toFun κ := ⟨wardDiagonalOf κ, wardDiagonalOf_mem N hN κ⟩
  map_add' κ₁ κ₂ := by
    apply Subtype.ext
    funext a b dir j
    by_cases ha : a = .zero <;> simp [wardDiagonalOf, ha, curlSlice_add, Pi.add_apply]
  map_smul' t κ := by
    apply Subtype.ext
    funext a b dir j
    by_cases ha : a = .zero <;>
      simp [wardDiagonalOf, ha, curlSlice_smul, Pi.smul_apply, smul_eq_mul]

def coeffCurry : (Role × OrderedPair → ℚ) ≃ₗ[ℚ] (Role → OrderedPair → ℚ) where
  toFun f b p := f (b, p)
  invFun g bp := g bp.1 bp.2
  left_inv _ := rfl
  right_inv _ := rfl
  map_add' _ _ := rfl
  map_smul' _ _ := rfl

lemma roleOrdered_card : Fintype.card (Role × OrderedPair) = 24 := by
  native_decide

theorem selfAdjoint_radiusOneWardKernel_eq_diagonalCurl
    (N : ℕ) (hN : 2 ≤ N)
    (c : RadiusOneOffset → Role → SymSlice ℚ)
    (hward : ∀ a b g, groupCoeff N (c a b) g = 0)
    (hadj : ∀ a b, a ≠ .zero → StaysInAnsatz a (c a b)) :
    ∃ κ : Role → OrderedPair → ℚ, c = wardDiagonalOf κ := by
  have hslice : ∀ b, ∃ κb : OrderedPair → ℚ, c .zero b = curlSlice κb := by
    intro b
    exact (gauge_symbol_iff_laurent_syzygy N hN _).1 (hward .zero b)
  choose κ hκ using hslice
  refine ⟨κ, ?_⟩
  funext a b
  by_cases ha : a = .zero
  · subst ha
    simpa [wardDiagonalOf] using hκ b
  · rcases (gauge_symbol_iff_laurent_syzygy N hN (c a b)).1 (hward a b) with ⟨κa, hκa⟩
    have hzero : κa = 0 :=
      curl_stays_only_zero a ha κa (by simpa [hκa] using hadj a b ha)
    rw [hκa, hzero]
    simp [wardDiagonalOf, ha]
    ext dir j
    cases j <;> simp [curlSlice, antisymCoeff]

theorem selfAdjoint_radiusOneWardKernel_finrank_twentyFour (N : ℕ) (hN : 2 ≤ N) :
    Module.finrank ℚ (WardKernel N) = 24 := by
  classical
  let e : (Role → OrderedPair → ℚ) ≃ₗ[ℚ] WardKernel N :=
    LinearEquiv.ofBijective (diagonalLinear N hN)
      ⟨fun κ₁ κ₂ h => by
        funext b p
        have hval := congr_fun (congr_fun (congrArg Subtype.val h) .zero) b
        have hcurl : curlSlice (κ₁ b) = curlSlice (κ₂ b) := by
          simpa [wardDiagonalOf] using hval
        have hplus := congr_fun (congr_fun hcurl p.1.1) (.plus p.1.2)
        simpa [curlSlice_plus_ordered] using hplus,
       fun c => by
        rcases selfAdjoint_radiusOneWardKernel_eq_diagonalCurl N hN c.1 c.2.1 c.2.2
          with ⟨κ, hκ⟩
        exact ⟨κ, Subtype.ext hκ.symm⟩⟩
  rw [← e.finrank_eq, ← coeffCurry.finrank_eq, Module.finrank_fintype_fun_eq_card]
  simpa using roleOrdered_card

/-! ## Periods `L = 2` and `L = 3` alias the `L ≥ 4` rules

Research Gaussian elimination gives raw symbol nullities 26, 10, and 6 at `L = 2`,
`L = 3`, and `L ≥ 4`, for one fixed output shift and one internal component, before
self-adjoint reduction. Those integers are not operator dimensions. The theorems
below are finite controls: a group syzygy at `L = 2` can carry a minus-diagonal
coefficient, and a group syzygy at `L = 3` can carry a plus-diagonal coefficient.
Both coefficients vanish for every group syzygy when `L ≥ 4`.
-/

def aliasL2 : SymSlice ℚ :=
  fun dir j => if dir = A ∧ (j = .zero ∨ j = .minus A) then 1 else 0

def aliasL3 : SymSlice ℚ :=
  fun dir j =>
    if dir = A ∧ (j = .zero ∨ j = .plus A ∨ j = .minus A) then 1 else 0

theorem periodTwo_minus_not_forced :
    (∀ g, groupCoeff 0 aliasL2 g = 0) ∧ aliasL2 A (.minus A) ≠ 0 := by
  native_decide

theorem periodThree_plusDiag_not_forced :
    (∀ g, groupCoeff 1 aliasL3 g = 0) ∧ aliasL3 A (.plus A) ≠ 0 := by
  native_decide

theorem largePeriod_diagonal_forced (N : ℕ) (hN : 2 ≤ N) (c : SymSlice ℚ)
    (hg : ∀ g, groupCoeff N c g = 0) :
    c A (.plus A) = 0 ∧ c A (.minus A) = 0 := by
  rcases (gauge_symbol_iff_laurent_syzygy N hN c).1 hg with ⟨κ, rfl⟩
  constructor <;> simp [curlSlice, antisymCoeff]

/-! ## Radius-one matter stencil misses the graded corner

On the `L = 3` two-axis shadow, `e = L (U_s - I) δ` and `U_s A_r` produce a nonzero
matrix entry between sites at toroidal distance 2. A matter stencil of radius one
has no such entry. This is independent of the scalar 24-dimensional Ward class.
`flatStaggeredH` is not on this baseline, so the witness is this corner of the
accepted formula rather than a duplicate of that operator.
-/

abbrev Site3 := Fin 3 × Fin 3

def torDist (x y : Site3) : ℕ :=
  let dx := min ((x.1.val + 3 - y.1.val) % 3) ((y.1.val + 3 - x.1.val) % 3)
  let dy := min ((x.2.val + 3 - y.2.val) % 3) ((y.2.val + 3 - x.2.val) % 3)
  dx + dy

def bump00 (x : Site3) : ℚ := if x = (0, 0) then 1 else 0

def stepS (x : Site3) : Site3 := (x.1, x.2 + 1)

def stepRinv (x : Site3) : Site3 := (x.1 - 1, x.2)

def eCorner (x : Site3) : ℚ := 3 * (bump00 (stepS x) - bump00 x)

/-- Matrix element of `M_e ∘ U_s ∘ A_r` from `y` into `x`. -/
def kCoeff (x y : Site3) : ℚ :=
  (eCorner x / 2) * (if y = stepS x then 1 else 0) +
    (eCorner x / 2) * (if y = stepS (stepRinv x) then 1 else 0)

def gradedCorner (x y : Site3) : ℚ := kCoeff x y + kCoeff y x

def MatterRadiusOne (M : Site3 → Site3 → ℚ) : Prop :=
  ∀ x y, 1 < torDist x y → M x y = 0

theorem radiusOne_graded_target_empty : ¬ MatterRadiusOne gradedCorner := by
  intro h
  have hdist : 1 < torDist (0, 0) (2, 1) := by decide
  have hnz : gradedCorner (0, 0) (2, 1) ≠ 0 := by native_decide
  exact hnz (h (0, 0) (2, 1) hdist)

/-! ## Simultaneous Role relabeling

The permutation acts at once on the internal index, the coframe direction, and
the sign of the ordered pair. It is a relabeling of Role, not a local Lorentz
boost. Inside the 24-dimensional Ward-null coefficient space the invariant
subspace is spanned by `kappaF`, the coefficient of `∑_{r ≠ s} T_rs^s`.
-/

def kappaF (b : Role) (p : OrderedPair) : ℚ :=
  if b = p.1.2 then 1 else if b = p.1.1 then -1 else 0

def coeffOf (κ : Role → OrderedPair → ℚ) (b r s : Role) : ℚ :=
  antisymCoeff (κ b) r s

def permAction (σ : Role ≃ Role) (κ : Role → OrderedPair → ℚ) :
    Role → OrderedPair → ℚ :=
  fun b p => coeffOf κ (σ.symm b) (σ.symm p.1.1) (σ.symm p.1.2)

def IsRoleInvariant (κ : Role → OrderedPair → ℚ) : Prop :=
  ∀ σ : Role ≃ Role, permAction σ κ = κ

lemma kappaF_second (p : OrderedPair) : kappaF p.1.2 p = 1 := by
  have hne : p.1.2 ≠ p.1.1 := by
    intro h
    exact ne_of_lt p.2 (congrArg roleIndex h.symm)
  simp [kappaF, hne]

lemma kappaF_first (p : OrderedPair) : kappaF p.1.1 p = -1 := by
  have hne : p.1.1 ≠ p.1.2 := by
    intro h
    exact ne_of_lt p.2 (congrArg roleIndex h)
  simp [kappaF, hne]

lemma antisym_swap (κ : OrderedPair → ℚ) (r s : Role) :
    antisymCoeff κ s r = -antisymCoeff κ r s := by
  unfold antisymCoeff
  rcases roleIndex_trichotomy r s with hlt | heq | hgt
  · have hnot : ¬ roleIndex s < roleIndex r := not_lt_of_gt hlt
    simp [hlt, hnot]
  · simp [heq]
  · have hnot : ¬ roleIndex r < roleIndex s := not_lt_of_gt hgt
    simp [hgt, hnot]

lemma permAction_add (σ : Role ≃ Role) (κ₁ κ₂ : Role → OrderedPair → ℚ) :
    permAction σ (κ₁ + κ₂) = permAction σ κ₁ + permAction σ κ₂ := by
  funext b p
  simp only [permAction, coeffOf, Pi.add_apply]
  unfold antisymCoeff
  by_cases h1 : roleIndex (σ.symm p.1.1) < roleIndex (σ.symm p.1.2)
  · simp [h1, Pi.add_apply]
  · by_cases h2 : roleIndex (σ.symm p.1.2) < roleIndex (σ.symm p.1.1)
    · simp [h1, h2, Pi.add_apply, add_comm]
    · simp [h1, h2]

lemma permAction_smul (σ : Role ≃ Role) (c : ℚ) (κ : Role → OrderedPair → ℚ) :
    permAction σ (c • κ) = c • permAction σ κ := by
  funext b p
  simp only [permAction, coeffOf, Pi.smul_apply, smul_eq_mul]
  unfold antisymCoeff
  by_cases h1 : roleIndex (σ.symm p.1.1) < roleIndex (σ.symm p.1.2)
  · simp [h1, Pi.smul_apply, smul_eq_mul]
  · by_cases h2 : roleIndex (σ.symm p.1.2) < roleIndex (σ.symm p.1.1)
    · simp [h1, h2, Pi.smul_apply, smul_eq_mul, mul_neg]
    · simp [h1, h2, mul_zero]

lemma kappaF_invariant (σ : Role ≃ Role) : permAction σ kappaF = kappaF := by
  funext b p
  simp only [permAction, coeffOf]
  set r := p.1.1
  set s := p.1.2
  set r' := σ.symm r
  set s' := σ.symm s
  set b' := σ.symm b
  have hrs : r ≠ s := by
    intro h
    exact ne_of_lt p.2 (congrArg roleIndex h)
  have hrs' : r' ≠ s' := fun h => hrs (σ.symm.injective h)
  by_cases hbs' : b' = s'
  · have hb : b = s := by
      simpa [b', s'] using congrArg σ hbs'
    have hval : antisymCoeff (kappaF s') r' s' = 1 := by
      rcases roleIndex_trichotomy r' s' with hlt | heq | hgt
      · simp [antisymCoeff, hlt, kappaF]
      · exact (hrs' heq).elim
      · have hnot : ¬ roleIndex r' < roleIndex s' := not_lt_of_gt hgt
        have hsr : s' ≠ r' := hrs'.symm
        simp [antisymCoeff, hnot, hgt, kappaF, hsr]
    simp only [hbs', hb, hval]
    have hs : s = p.1.2 := rfl
    simp [kappaF, hs, hrs]
  · by_cases hbr' : b' = r'
    · have hb : b = r := by
        simpa [b', r'] using congrArg σ hbr'
      have hval : antisymCoeff (kappaF r') r' s' = -1 := by
        rcases roleIndex_trichotomy r' s' with hlt | heq | hgt
        · simp [antisymCoeff, hlt, kappaF, hrs']
        · exact (hrs' heq).elim
        · have hnot : ¬ roleIndex r' < roleIndex s' := not_lt_of_gt hgt
          simp [antisymCoeff, hnot, hgt, kappaF, hrs']
      simp only [hbr', hb, hval]
      have hr : r = p.1.1 := rfl
      have hpne : p.1.1 ≠ p.1.2 := by simpa [r, s] using hrs
      simp [kappaF, hr, hpne]
    · have hval : antisymCoeff (kappaF b') r' s' = 0 := by
        rcases roleIndex_trichotomy r' s' with hlt | heq | hgt
        · simp [antisymCoeff, hlt, kappaF, hbs', hbr']
        · exact (hrs' heq).elim
        · have hnot : ¬ roleIndex r' < roleIndex s' := not_lt_of_gt hgt
          simp [antisymCoeff, hnot, hgt, kappaF, hbs', hbr', hrs']
      have hb1 : b ≠ p.1.1 := by
        intro h
        apply hbr'
        simpa [b', r', r] using congrArg σ.symm h
      have hb2 : b ≠ p.1.2 := by
        intro h
        apply hbs'
        simpa [b', s', s] using congrArg σ.symm h
      simp [hval, kappaF, hb1, hb2]

def RoleInvariant : Submodule ℚ (Role → OrderedPair → ℚ) where
  carrier := {κ | IsRoleInvariant κ}
  add_mem' := by
    intro κ₁ κ₂ h₁ h₂ σ
    rw [permAction_add, h₁ σ, h₂ σ]
  zero_mem' := by
    intro σ
    funext b p
    simp [permAction, coeffOf, antisymCoeff]
  smul_mem' := by
    intro c κ hκ σ
    rw [permAction_smul, hκ σ]

def swapRole (r s t : Role) : Role :=
  if t = r then s else if t = s then r else t

lemma swapRole_invol (r s t : Role) (hrs : r ≠ s) :
    swapRole r s (swapRole r s t) = t := by
  unfold swapRole
  by_cases h1 : t = r
  · simp [h1, hrs]
  · by_cases h2 : t = s <;> simp [h1, h2, hrs]

def swapEquiv (r s : Role) (hrs : r ≠ s) : Role ≃ Role where
  toFun := swapRole r s
  invFun := swapRole r s
  left_inv t := swapRole_invol r s t hrs
  right_inv t := swapRole_invol r s t hrs

def pairAC : OrderedPair := ⟨(A, C), by decide⟩

lemma ordered_classified (p : OrderedPair) :
    (p.1.1 = A ∧ p.1.2 = C) ∨ (p.1.1 = A ∧ p.1.2 = D) ∨
      (p.1.1 = A ∧ p.1.2 = B) ∨ (p.1.1 = C ∧ p.1.2 = D) ∨
      (p.1.1 = C ∧ p.1.2 = B) ∨ (p.1.1 = D ∧ p.1.2 = B) := by
  revert p
  native_decide

lemma edge_transport (κ : Role → OrderedPair → ℚ) (hinv : IsRoleInvariant κ)
    (p q : OrderedPair) (σ : Role ≃ Role)
    (h1 : σ p.1.1 = q.1.1) (h2 : σ p.1.2 = q.1.2) :
    κ q.1.2 q = κ p.1.2 p := by
  have happly := congr_fun (congr_fun (hinv σ) q.1.2) q
  have hback1 : σ.symm q.1.1 = p.1.1 :=
    σ.injective (by simpa [h1] using σ.apply_symm_apply q.1.1)
  have hback2 : σ.symm q.1.2 = p.1.2 :=
    σ.injective (by simpa [h2] using σ.apply_symm_apply q.1.2)
  have hord : antisymCoeff (κ p.1.2) p.1.1 p.1.2 = κ p.1.2 p := by
    simp [antisymCoeff, p.2]
  have hperm : permAction σ κ q.1.2 q = κ p.1.2 p := by
    simp [permAction, coeffOf, hback1, hback2, hord]
  exact happly.symm.trans hperm

lemma outside_vanishes (κ : Role → OrderedPair → ℚ) (hinv : IsRoleInvariant κ)
    (p : OrderedPair) (b : Role) (hb1 : b ≠ p.1.1) (hb2 : b ≠ p.1.2) :
    κ b p = 0 := by
  have hrs : p.1.1 ≠ p.1.2 := by
    intro h
    exact ne_of_lt p.2 (congrArg roleIndex h)
  let σ := swapEquiv p.1.1 p.1.2 hrs
  have happly := congr_fun (congr_fun (hinv σ) b) p
  have hsym : ∀ t, σ.symm t = σ t := by
    intro t
    simp [σ, swapEquiv, swapRole_invol, hrs]
  have hfix : σ b = b := by
    simp [σ, swapEquiv, swapRole, hb1, hb2]
  have hswap1 : σ p.1.1 = p.1.2 := by
    simp [σ, swapEquiv, swapRole]
  have hswap2 : σ p.1.2 = p.1.1 := by
    simp [σ, swapEquiv, swapRole, hrs]
  have hord : antisymCoeff (κ b) p.1.1 p.1.2 = κ b p := by
    simp [antisymCoeff, p.2]
  have hanti : antisymCoeff (κ b) p.1.2 p.1.1 = -κ b p := by
    rw [antisym_swap, hord]
  have hperm : permAction σ κ b p = -κ b p := by
    simp only [permAction, coeffOf, hsym, hfix, hswap1, hswap2, hanti]
  have : κ b p = -κ b p := happly.symm.trans hperm
  linarith

lemma edge_neg (κ : Role → OrderedPair → ℚ) (hinv : IsRoleInvariant κ) (p : OrderedPair) :
    κ p.1.1 p = -κ p.1.2 p := by
  have hrs : p.1.1 ≠ p.1.2 := by
    intro h
    exact ne_of_lt p.2 (congrArg roleIndex h)
  let σ := swapEquiv p.1.1 p.1.2 hrs
  have happly := congr_fun (congr_fun (hinv σ) p.1.2) p
  have hsym : ∀ t, σ.symm t = σ t := by
    intro t
    simp [σ, swapEquiv, swapRole_invol, hrs]
  have hback : σ p.1.2 = p.1.1 := by
    simp [σ, swapEquiv, swapRole, hrs]
  have hswap1 : σ p.1.1 = p.1.2 := by
    simp [σ, swapEquiv, swapRole]
  have hord : antisymCoeff (κ p.1.1) p.1.1 p.1.2 = κ p.1.1 p := by
    simp [antisymCoeff, p.2]
  have hanti : antisymCoeff (κ p.1.1) p.1.2 p.1.1 = -κ p.1.1 p := by
    rw [antisym_swap, hord]
  have hperm : permAction σ κ p.1.2 p = -κ p.1.1 p := by
    simp only [permAction, coeffOf, hsym, hback, hswap1, hanti]
  linarith [happly.symm.trans hperm]

def cycleACD (r : Role) : Role :=
  if r = A then C else if r = C then D else if r = D then A else r

def cycleACDInv (r : Role) : Role :=
  if r = A then D else if r = D then C else if r = C then A else r

def cycleACDEquiv : Role ≃ Role where
  toFun := cycleACD
  invFun := cycleACDInv
  left_inv r := by
    rcases r with ⟨a, b⟩
    fin_cases a <;> fin_cases b <;> simp [cycleACD, cycleACDInv, A, C, D]
  right_inv r := by
    rcases r with ⟨a, b⟩
    fin_cases a <;> fin_cases b <;> simp [cycleACD, cycleACDInv, A, C, D]

def cycleACB (r : Role) : Role :=
  if r = A then C else if r = C then B else if r = B then A else r

def cycleACBInv (r : Role) : Role :=
  if r = A then B else if r = B then C else if r = C then A else r

def cycleACBEquiv : Role ≃ Role where
  toFun := cycleACB
  invFun := cycleACBInv
  left_inv r := by
    rcases r with ⟨a, b⟩
    fin_cases a <;> fin_cases b <;> simp [cycleACB, cycleACBInv, A, B, C]
  right_inv r := by
    rcases r with ⟨a, b⟩
    fin_cases a <;> fin_cases b <;> simp [cycleACB, cycleACBInv, A, B, C]

def swapADCB (r : Role) : Role :=
  if r = A then D else if r = D then A else if r = C then B else if r = B then C else r

def swapADCBEquiv : Role ≃ Role where
  toFun := swapADCB
  invFun := swapADCB
  left_inv r := by
    rcases r with ⟨a, b⟩
    fin_cases a <;> fin_cases b <;> simp [swapADCB, A, B, C, D]
  right_inv r := by
    rcases r with ⟨a, b⟩
    fin_cases a <;> fin_cases b <;> simp [swapADCB, A, B, C, D]

lemma edge_matches_base (κ : Role → OrderedPair → ℚ) (hinv : IsRoleInvariant κ)
    (p : OrderedPair) : κ p.1.2 p = κ C pairAC := by
  rcases ordered_classified p with h | h | h | h | h | h
  · have hp : p.1 = (A, C) := Prod.ext h.1 h.2
    have : p = pairAC := Subtype.ext (by simpa [pairAC] using hp)
    simp [this, pairAC]
  · have hσ := edge_transport κ hinv pairAC ⟨(A, D), by decide⟩ (swapEquiv C D (by decide))
      (by decide) (by decide)
    have hp : p = ⟨(A, D), by decide⟩ := Subtype.ext (Prod.ext h.1 h.2)
    simpa [hp, pairAC] using hσ
  · have hσ := edge_transport κ hinv pairAC ⟨(A, B), by decide⟩ (swapEquiv C B (by decide))
      (by decide) (by decide)
    have hp : p = ⟨(A, B), by decide⟩ := Subtype.ext (Prod.ext h.1 h.2)
    simpa [hp, pairAC] using hσ
  · have hσ := edge_transport κ hinv pairAC ⟨(C, D), by decide⟩ cycleACDEquiv
      (by decide) (by decide)
    have hp : p = ⟨(C, D), by decide⟩ := Subtype.ext (Prod.ext h.1 h.2)
    simpa [hp, pairAC] using hσ
  · have hσ := edge_transport κ hinv pairAC ⟨(C, B), by decide⟩ cycleACBEquiv
      (by decide) (by decide)
    have hp : p = ⟨(C, B), by decide⟩ := Subtype.ext (Prod.ext h.1 h.2)
    simpa [hp, pairAC] using hσ
  · have hσ := edge_transport κ hinv pairAC ⟨(D, B), by decide⟩ swapADCBEquiv
      (by decide) (by decide)
    have hp : p = ⟨(D, B), by decide⟩ := Subtype.ext (Prod.ext h.1 h.2)
    simpa [hp, pairAC] using hσ

lemma invariant_eq_smul (κ : Role → OrderedPair → ℚ) (hinv : IsRoleInvariant κ) :
    κ = (κ C pairAC) • kappaF := by
  funext b p
  by_cases hb2 : b = p.1.2
  · simp [kappaF, hb2, Pi.smul_apply, smul_eq_mul, edge_matches_base κ hinv p]
  · by_cases hb1 : b = p.1.1
    · subst hb1
      have hb2' : p.1.1 ≠ p.1.2 := hb2
      have hneg := edge_neg κ hinv p
      have hsecond := edge_matches_base κ hinv p
      simp [kappaF, hb2', Pi.smul_apply, smul_eq_mul, hneg, hsecond]
    · rw [outside_vanishes κ hinv p b hb1 hb2]
      simp [kappaF, hb1, hb2, Pi.smul_apply]

def kappaLinear : ℚ →ₗ[ℚ] RoleInvariant where
  toFun c := ⟨c • kappaF, fun σ => by rw [permAction_smul, kappaF_invariant]⟩
  map_add' c₁ c₂ := by
    apply Subtype.ext
    ext b p
    simp [Pi.add_apply]
    ring
  map_smul' t c := by
    apply Subtype.ext
    ext b p
    simp [Pi.smul_apply, smul_eq_mul]
    ring

theorem RolePerm_invariants_finrank_one : Module.finrank ℚ RoleInvariant = 1 := by
  classical
  let e : ℚ ≃ₗ[ℚ] RoleInvariant :=
    LinearEquiv.ofBijective kappaLinear
      ⟨fun c₁ c₂ h => by
        have hval := congr_fun (congr_fun (congrArg Subtype.val h) C) pairAC
        have : c₁ * kappaF C pairAC = c₂ * kappaF C pairAC := by
          simpa [kappaLinear, Pi.smul_apply, smul_eq_mul] using hval
        have hone : kappaF C pairAC = 1 := by
          simpa [pairAC] using kappaF_second pairAC
        rw [hone] at this
        simpa using this,
       fun κ => ⟨κ.1 C pairAC, Subtype.ext (invariant_eq_smul κ.1 κ.2).symm⟩⟩
  rw [← e.finrank_eq, Module.finrank_self]

/-- `kappaF` is the coefficient of `∑_{r ≠ s} T_rs^s` in the 24-dimensional class.
Its value on `(A,C)` is `1`, so this Role-relabeling representative is not zero.
The permutation is not a local Lorentz boost. -/
theorem invariantCurl_nonzero : kappaF C pairAC = 1 :=
  kappaF_second pairAC

end D0.Geometry
