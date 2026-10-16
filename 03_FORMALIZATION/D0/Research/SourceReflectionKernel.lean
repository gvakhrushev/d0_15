import Mathlib.Data.Matrix.Mul
import Mathlib.Data.Real.Basic
import Mathlib.Order.ConditionallyCompleteLattice.Basic
import Mathlib.Tactic

/-!
# Finite right-inverse source reflection

For matrices `L : X → Y` and `W : Y → X` with `L ∘ W = id`, the covector
pullback `L*` is injective. A residual equation `a = L* e + r` reconstructs
as `e = W* (a − r)`. An `ℓ∞` operator bound on `W` dualizes to an `ℓ¹` bound
on that reconstruction. A direct internal covector is kept: `L* e + d = 0`
gives `e = −W* d`, not `e = 0`.

A symmetric `4 × 4` tensor is packed in the slot order
`(00,01,02,03,11,12,13,22,23,33)`, with weight `2` on every off-diagonal slot.
The weighted packed pairing reproduces the full Frobenius contraction.

These are identities of finite real coordinate spaces. A right inverse on one
finite chart is an extra hypothesis. This file does not admit `W` as a
functional-analytic inverse or as a physical map.
-/

namespace D0.Research.SourceReflectionKernel

open Matrix Finset

/-- Real coordinate map `X → Y`, stored as a matrix with rows in the codomain. -/
abbrev Lin (X Y : Type*) [Fintype X] [Fintype Y] := Matrix Y X ℝ

/-- Matrix-vector action of a coordinate map. -/
def apply {X Y : Type*} [Fintype X] [Fintype Y] (L : Lin X Y) (x : X → ℝ) : Y → ℝ :=
  L *ᵥ x

/-- Pullback of a covector: `(L* e) x = e (L x)`. -/
def pullback {X Y : Type*} [Fintype X] [Fintype Y] (L : Lin X Y) (e : Y → ℝ) : X → ℝ :=
  Lᵀ *ᵥ e

lemma dot_apply_pullback {X Y : Type*} [Fintype X] [Fintype Y]
    (L : Lin X Y) (x : X → ℝ) (e : Y → ℝ) :
    apply L x ⬝ᵥ e = x ⬝ᵥ pullback L e := by
  simp only [apply, pullback, dotProduct, mulVec, transpose_apply]
  simp_rw [Finset.sum_mul, Finset.mul_sum]
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun _ _ => Finset.sum_congr rfl fun _ _ => ?_
  ring

lemma pullback_comp {X Y Z : Type*} [Fintype X] [Fintype Y] [Fintype Z]
    (A : Lin Y Z) (B : Lin X Y) (e : Z → ℝ) :
    pullback (A * B) e = pullback B (pullback A e) := by
  unfold pullback
  rw [transpose_mul, ← mulVec_mulVec]

lemma pullback_one {Y : Type*} [Fintype Y] [DecidableEq Y] (e : Y → ℝ) :
    pullback (1 : Matrix Y Y ℝ) e = e := by
  have hT : (1 : Matrix Y Y ℝ)ᵀ = 1 := by
    ext i j
    simp only [transpose_apply, one_apply]
    by_cases h : i = j
    · simp [h]
    · simp [h, Ne.symm h]
  simp [pullback, hT, one_mulVec]

lemma pullback_neg {X Y : Type*} [Fintype X] [Fintype Y] (L : Lin X Y) (e : Y → ℝ) :
    pullback L (-e) = -pullback L e := by
  simp [pullback, mulVec_neg]

/-- `L ∘ W = id_Y`. -/
def IsRightInverse {X Y : Type*} [Fintype X] [Fintype Y] [DecidableEq Y]
    (L : Lin X Y) (W : Lin Y X) : Prop :=
  L * W = 1

theorem pullback_leftInverse_of_rightInverse {X Y : Type*}
    [Fintype X] [Fintype Y] [DecidableEq Y]
    {L : Lin X Y} {W : Lin Y X} (hLW : IsRightInverse L W) (e : Y → ℝ) :
    pullback W (pullback L e) = e := by
  rw [← pullback_comp, hLW, pullback_one]

theorem pullback_injective_of_rightInverse {X Y : Type*}
    [Fintype X] [Fintype Y] [DecidableEq Y]
    {L : Lin X Y} {W : Lin Y X} (hLW : IsRightInverse L W) :
    Function.Injective (pullback L) := by
  intro e₁ e₂ h
  simpa [pullback_leftInverse_of_rightInverse hLW] using congrArg (pullback W) h

theorem reflect_residual {X Y : Type*}
    [Fintype X] [Fintype Y] [DecidableEq Y]
    {L : Lin X Y} {W : Lin Y X} (hLW : IsRightInverse L W)
    {a : X → ℝ} {e : Y → ℝ} {r : X → ℝ}
    (hEq : a = pullback L e + r) :
    e = pullback W (a - r) := by
  have hsub : a - r = pullback L e := by
    rw [hEq]
    ext i
    simp
  rw [hsub]
  exact (pullback_leftInverse_of_rightInverse hLW e).symm

theorem reflect_internal_direct {X Y : Type*}
    [Fintype X] [Fintype Y] [DecidableEq Y]
    {L : Lin X Y} {W : Lin Y X} (hLW : IsRightInverse L W)
    {e : Y → ℝ} {d : X → ℝ}
    (hEq : pullback L e + d = 0) :
    e = -pullback W d := by
  have hres : e = pullback W ((0 : X → ℝ) - d) :=
    reflect_residual hLW (by simpa using hEq.symm)
  have hzero : ((0 : X → ℝ) - d) = -d := by
    ext i
    simp
  rw [hres, hzero, pullback_neg]

/-- Coordinate `ℓ¹` norm. -/
def l1 {I : Type*} [Fintype I] (v : I → ℝ) : ℝ :=
  ∑ i, |v i|

/-- Coordinate `ℓ∞` norm. Empty index types are excluded so the maximum exists. -/
noncomputable def lInf {I : Type*} [Fintype I] [Nonempty I] (v : I → ℝ) : ℝ :=
  sSup (Set.range fun i => |v i|)

lemma l1_nonneg {I : Type*} [Fintype I] (v : I → ℝ) : 0 ≤ l1 v :=
  Finset.sum_nonneg fun i _ => abs_nonneg (v i)

lemma l1_neg {I : Type*} [Fintype I] (v : I → ℝ) : l1 (-v) = l1 v := by
  unfold l1
  simp [Pi.neg_apply, abs_neg]

lemma bddAbove_abs_range {I : Type*} [Fintype I] (v : I → ℝ) :
    BddAbove (Set.range fun i => |v i|) := by
  refine ⟨∑ i, |v i|, ?_⟩
  rintro y ⟨i, rfl⟩
  exact Finset.single_le_sum (fun i _ => abs_nonneg (v i)) (Finset.mem_univ i)

lemma abs_le_lInf {I : Type*} [Fintype I] [Nonempty I] (v : I → ℝ) (i : I) :
    |v i| ≤ lInf v := by
  unfold lInf
  exact le_csSup (bddAbove_abs_range v) (Set.mem_range_self i)

lemma lInf_le {I : Type*} [Fintype I] [Nonempty I] {v : I → ℝ} {c : ℝ}
    (h : ∀ i, |v i| ≤ c) : lInf v ≤ c := by
  unfold lInf
  exact csSup_le (Set.range_nonempty _) (by
    rintro y ⟨i, rfl⟩
    exact h i)

lemma lInf_nonneg {I : Type*} [Fintype I] [Nonempty I] (v : I → ℝ) : 0 ≤ lInf v := by
  inhabit I
  exact le_trans (abs_nonneg (v default)) (abs_le_lInf v default)

/-- Sign used to turn an `ℓ¹` sum into a dot product. Zero has sign zero. -/
noncomputable def coordSign (t : ℝ) : ℝ :=
  if t < 0 then -1 else if t = 0 then 0 else 1

lemma coordSign_mul_self (t : ℝ) : coordSign t * t = |t| := by
  unfold coordSign
  split_ifs with hlt heq
  · rw [abs_of_neg hlt]
    ring
  · rw [heq, abs_zero]
    ring
  · have hpos : 0 < t := lt_of_le_of_ne (not_lt.mp hlt) (Ne.symm heq)
    rw [abs_of_pos hpos]
    ring

lemma abs_coordSign_le_one (t : ℝ) : |coordSign t| ≤ 1 := by
  unfold coordSign
  split_ifs <;> norm_num

noncomputable def signVec {I : Type*} (v : I → ℝ) : I → ℝ :=
  fun i => coordSign (v i)

lemma l1_eq_dot_sign {I : Type*} [Fintype I] (v : I → ℝ) :
    l1 v = signVec v ⬝ᵥ v := by
  unfold l1 signVec dotProduct
  refine Finset.sum_congr rfl fun i _ => ?_
  exact (coordSign_mul_self (v i)).symm

lemma lInf_signVec_le_one {I : Type*} [Fintype I] [Nonempty I] (v : I → ℝ) :
    lInf (signVec v) ≤ 1 :=
  lInf_le fun i => abs_coordSign_le_one (v i)

lemma dot_le_lInf_mul_l1 {I : Type*} [Fintype I] [Nonempty I] (u v : I → ℝ) :
    u ⬝ᵥ v ≤ lInf u * l1 v := by
  unfold dotProduct l1
  have h1 : ∑ i, u i * v i ≤ ∑ i, |u i| * |v i| := by
    refine Finset.sum_le_sum fun i _ => ?_
    calc
      u i * v i ≤ |u i * v i| := le_abs_self _
      _ = |u i| * |v i| := abs_mul _ _
  have h2 : ∑ i, |u i| * |v i| ≤ ∑ i, lInf u * |v i| := by
    refine Finset.sum_le_sum fun i _ => ?_
    exact mul_le_mul_of_nonneg_right (abs_le_lInf u i) (abs_nonneg _)
  have h3 : ∑ i, lInf u * |v i| = lInf u * ∑ i, |v i| := by
    rw [← Finset.mul_sum]
  calc
    u ⬝ᵥ v = ∑ i, u i * v i := rfl
    _ ≤ ∑ i, |u i| * |v i| := h1
    _ ≤ ∑ i, lInf u * |v i| := h2
    _ = lInf u * l1 v := by rw [h3]; rfl

/-- Dual of an `ℓ∞` bound: `‖W x‖_∞ ≤ C ‖x‖_∞` implies `‖W* a‖_1 ≤ C ‖a‖_1`. -/
theorem pullback_l1_le_of_lInf_bound {X Y : Type*}
    [Fintype X] [Fintype Y] [Nonempty X] [Nonempty Y]
    {W : Lin Y X} {C : ℝ}
    (hC : ∀ x : Y → ℝ, lInf (apply W x) ≤ C * lInf x)
    (hC0 : 0 ≤ C) (a : X → ℝ) :
    l1 (pullback W a) ≤ C * l1 a := by
  set s : Y → ℝ := signVec (pullback W a)
  have hs : lInf s ≤ 1 := lInf_signVec_le_one _
  have hmul : C * lInf s ≤ C := by
    simpa using mul_le_mul_of_nonneg_left hs hC0
  calc
    l1 (pullback W a) = s ⬝ᵥ pullback W a := by
      simpa [s] using l1_eq_dot_sign (pullback W a)
    _ = apply W s ⬝ᵥ a := (dot_apply_pullback W s a).symm
    _ ≤ lInf (apply W s) * l1 a := dot_le_lInf_mul_l1 _ _
    _ ≤ (C * lInf s) * l1 a :=
      mul_le_mul_of_nonneg_right (hC s) (l1_nonneg a)
    _ ≤ C * l1 a := mul_le_mul_of_nonneg_right hmul (l1_nonneg a)

theorem reflect_residual_l1 {X Y : Type*}
    [Fintype X] [Fintype Y] [DecidableEq Y] [Nonempty X] [Nonempty Y]
    {L : Lin X Y} {W : Lin Y X} (hLW : IsRightInverse L W)
    {C : ℝ} (hC : ∀ x : Y → ℝ, lInf (apply W x) ≤ C * lInf x) (hC0 : 0 ≤ C)
    {a : X → ℝ} {e : Y → ℝ} {r : X → ℝ}
    (hEq : a = pullback L e + r) :
    e = pullback W (a - r) ∧ l1 e ≤ C * l1 (a - r) := by
  refine ⟨reflect_residual hLW hEq, ?_⟩
  rw [reflect_residual hLW hEq]
  exact pullback_l1_le_of_lInf_bound hC hC0 (a - r)

theorem stationary_internal_l1 {X Y : Type*}
    [Fintype X] [Fintype Y] [DecidableEq Y] [Nonempty X] [Nonempty Y]
    {L : Lin X Y} {W : Lin Y X} (hLW : IsRightInverse L W)
    {C : ℝ} (hC : ∀ x : Y → ℝ, lInf (apply W x) ≤ C * lInf x) (hC0 : 0 ≤ C)
    {e : Y → ℝ} {d : X → ℝ}
    (hEq : pullback L e + d = 0) :
    e = -pullback W d ∧ l1 e ≤ C * l1 d := by
  have hres : e = pullback W ((0 : X → ℝ) - d) :=
    reflect_residual hLW (by simpa using hEq.symm)
  have hzero : ((0 : X → ℝ) - d) = -d := by
    ext i
    simp
  refine ⟨?_, ?_⟩
  · rw [hres, hzero, pullback_neg]
  · rw [hres, hzero]
    have hb := pullback_l1_le_of_lInf_bound hC hC0 (-d)
    rwa [l1_neg] at hb

/-- Absolute row sum, the explicit `ℓ∞` operator constant of a matrix. -/
def rowAbsSum {X Y : Type*} [Fintype X] [Fintype Y] (W : Lin Y X) (i : X) : ℝ :=
  ∑ j : Y, |W i j|

noncomputable def opLInf {X Y : Type*} [Fintype X] [Fintype Y] [Nonempty X]
    (W : Lin Y X) : ℝ :=
  lInf (fun i : X => rowAbsSum W i)

theorem apply_lInf_le_opLInf {X Y : Type*}
    [Fintype X] [Fintype Y] [Nonempty X] [Nonempty Y]
    (W : Lin Y X) (x : Y → ℝ) :
    lInf (apply W x) ≤ opLInf W * lInf x := by
  refine lInf_le fun i => ?_
  calc
    |(apply W x) i| = |∑ j : Y, W i j * x j| := by
      simp [apply, mulVec, dotProduct]
    _ ≤ ∑ j : Y, |W i j * x j| := Finset.abs_sum_le_sum_abs _ _
    _ = ∑ j : Y, |W i j| * |x j| := by
      simp_rw [abs_mul]
    _ ≤ ∑ j : Y, |W i j| * lInf x := by
      refine Finset.sum_le_sum fun j _ => ?_
      exact mul_le_mul_of_nonneg_left (abs_le_lInf x j) (abs_nonneg _)
    _ = rowAbsSum W i * lInf x := by
      rw [← Finset.sum_mul]
      rfl
    _ ≤ opLInf W * lInf x := by
      have hnn : 0 ≤ rowAbsSum W i :=
        Finset.sum_nonneg fun _ _ => abs_nonneg _
      have hle : rowAbsSum W i ≤ opLInf W := by
        simpa [opLInf, abs_of_nonneg hnn] using
          abs_le_lInf (fun k : X => rowAbsSum W k) i
      exact mul_le_mul_of_nonneg_right hle (lInf_nonneg x)

/-! ## Packed symmetric 4×4 pairing -/

/-- Slot order `(00,01,02,03,11,12,13,22,23,33)`. -/
def symIdx : Fin 10 → Fin 4 × Fin 4
  | 0 => (0, 0)
  | 1 => (0, 1)
  | 2 => (0, 2)
  | 3 => (0, 3)
  | 4 => (1, 1)
  | 5 => (1, 2)
  | 6 => (1, 3)
  | 7 => (2, 2)
  | 8 => (2, 3)
  | 9 => (3, 3)

/-- Diagonal slots have weight `1`. Off-diagonal slots have weight `2`. -/
def slotWeight : Fin 10 → ℝ
  | 0 => 1
  | 1 => 2
  | 2 => 2
  | 3 => 2
  | 4 => 1
  | 5 => 2
  | 6 => 2
  | 7 => 1
  | 8 => 2
  | 9 => 1

def pack (A : Matrix (Fin 4) (Fin 4) ℝ) (s : Fin 10) : ℝ :=
  A (symIdx s).1 (symIdx s).2

def packedPairing (u v : Fin 10 → ℝ) : ℝ :=
  ∑ s, slotWeight s * u s * v s

def unweightedPairing (u v : Fin 10 → ℝ) : ℝ :=
  ∑ s, u s * v s

def frobenius (A B : Matrix (Fin 4) (Fin 4) ℝ) : ℝ :=
  ∑ i, ∑ j, A i j * B i j

/-- Packed dual of a symmetric source: off-diagonal entries are doubled. -/
def packedDual (E : Matrix (Fin 4) (Fin 4) ℝ) (s : Fin 10) : ℝ :=
  slotWeight s * pack E s

lemma entry_symm {A : Matrix (Fin 4) (Fin 4) ℝ} (hA : Aᵀ = A) (i j : Fin 4) :
    A i j = A j i := by
  have h := congr_fun (congr_fun hA i) j
  simp only [transpose_apply] at h
  exact h.symm

lemma sum_fin10 (f : Fin 10 → ℝ) :
    ∑ s : Fin 10, f s =
      f 0 + f 1 + f 2 + f 3 + f 4 + f 5 + f 6 + f 7 + f 8 + f 9 := by
  repeat rw [Fin.sum_univ_succ]
  simp
  abel

theorem packedPairing_eq_frobenius {A B : Matrix (Fin 4) (Fin 4) ℝ}
    (hA : Aᵀ = A) (hB : Bᵀ = B) :
    packedPairing (pack A) (pack B) = frobenius A B := by
  have hAs : ∀ i j, A i j = A j i := entry_symm hA
  have hBs : ∀ i j, B i j = B j i := entry_symm hB
  simp only [packedPairing, frobenius, pack, Fin.sum_univ_four]
  rw [sum_fin10]
  simp only [symIdx, slotWeight]
  rw [hAs 1 0, hAs 2 0, hAs 3 0, hAs 2 1, hAs 3 1, hAs 3 2,
    hBs 1 0, hBs 2 0, hBs 3 0, hBs 2 1, hBs 3 1, hBs 3 2]
  ring

theorem full_contraction_eq_packed_dot {E Q : Matrix (Fin 4) (Fin 4) ℝ}
    (hE : Eᵀ = E) (hQ : Qᵀ = Q) :
    frobenius E Q = packedDual E ⬝ᵥ pack Q := by
  have hdot : packedDual E ⬝ᵥ pack Q = packedPairing (pack E) (pack Q) := by
    simp only [dotProduct, packedDual, packedPairing]
  rw [hdot, packedPairing_eq_frobenius hE hQ]

/-! ## Finite controls -/

/-- Rank-one square map. It is neither left- nor right-invertible. -/
def rankOneL : Lin (Fin 2) (Fin 2) :=
  Matrix.of fun i j => if i = 0 ∧ j = 0 then (1 : ℝ) else 0

def axisOne : Fin 2 → ℝ :=
  fun i => if i = 1 then 1 else 0

theorem rank_deficient_neither_sided_inverse :
    (¬ ∃ W : Lin (Fin 2) (Fin 2), IsRightInverse rankOneL W) ∧
    (¬ ∃ W : Lin (Fin 2) (Fin 2), W * rankOneL = 1) ∧
    pullback rankOneL axisOne = 0 ∧
    axisOne ≠ 0 := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · rintro ⟨W, hW⟩
    have h11 := congr_fun (congr_fun hW 1) 1
    rw [Matrix.mul_apply, Fin.sum_univ_two, one_apply] at h11
    simp [rankOneL, Matrix.of_apply] at h11
  · rintro ⟨W, hW⟩
    have h11 := congr_fun (congr_fun hW 1) 1
    rw [Matrix.mul_apply, Fin.sum_univ_two, one_apply] at h11
    simp [rankOneL, Matrix.of_apply] at h11
  · ext j
    fin_cases j <;>
      simp [pullback, rankOneL, axisOne, mulVec, dotProduct, transpose_apply, Matrix.of_apply]
  · intro h
    have := congr_fun h 1
    simp [axisOne] at this

/-- A zero price with a nonzero direct covector does not kill the source. -/
def keptE : Fin 1 → ℝ := fun _ => 1

def directD : Fin 1 → ℝ := fun _ => -1

theorem id_rightInverse :
    IsRightInverse (1 : Lin (Fin 1) (Fin 1)) (1 : Lin (Fin 1) (Fin 1)) := by
  simp [IsRightInverse]

theorem deleted_direct_covector_does_not_force_zero :
    pullback (1 : Lin (Fin 1) (Fin 1)) keptE + directD = 0 ∧
    keptE ≠ 0 ∧
    keptE = -pullback (1 : Lin (Fin 1) (Fin 1)) directD := by
  have hsum : pullback (1 : Lin (Fin 1) (Fin 1)) keptE + directD = 0 := by
    rw [pullback_one]
    ext i
    fin_cases i
    simp [keptE, directD]
  refine ⟨hsum, ?_, reflect_internal_direct id_rightInverse hsum⟩
  intro h
  have := congr_fun h 0
  simp [keptE] at this

/-- Symmetric matrix with a single off-diagonal pair. -/
def offDiag01 : Matrix (Fin 4) (Fin 4) ℝ :=
  Matrix.of fun i j => if (i = 0 ∧ j = 1) ∨ (i = 1 ∧ j = 0) then (1 : ℝ) else 0

lemma offDiag01_symm : offDiag01ᵀ = offDiag01 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [offDiag01, transpose_apply, Matrix.of_apply]

lemma offDiag01_sq (i j : Fin 4) :
    offDiag01 i j * offDiag01 i j =
      match i, j with
      | 0, 1 => 1
      | 1, 0 => 1
      | _, _ => 0 := by
  fin_cases i <;> fin_cases j <;> simp [offDiag01, Matrix.of_apply]

lemma pack_offDiag01_sq (s : Fin 10) :
    pack offDiag01 s * pack offDiag01 s =
      match s with
      | 1 => 1
      | _ => 0 := by
  fin_cases s <;> simp [pack, symIdx, offDiag01, Matrix.of_apply]

theorem wrong_off_diagonal_weight :
    offDiag01ᵀ = offDiag01 ∧
    frobenius offDiag01 offDiag01 = 2 ∧
    unweightedPairing (pack offDiag01) (pack offDiag01) = 1 ∧
    packedPairing (pack offDiag01) (pack offDiag01) = 2 := by
  refine ⟨offDiag01_symm, ?_, ?_, ?_⟩
  · simp only [frobenius, Fin.sum_univ_four, offDiag01_sq]
    norm_num
  · simp only [unweightedPairing, sum_fin10, pack_offDiag01_sq]
    norm_num
  · rw [packedPairing_eq_frobenius offDiag01_symm offDiag01_symm]
    simp only [frobenius, Fin.sum_univ_four, offDiag01_sq]
    norm_num

/-- Inclusion `t ↦ (t, 0)`. -/
def incl : Lin (Fin 1) (Fin 2) :=
  Matrix.of fun i _ => if i = 0 then (1 : ℝ) else 0

/-- Projection `(x₀, x₁) ↦ x₀`. It is a left inverse of `incl`, not a right inverse. -/
def proj : Lin (Fin 2) (Fin 1) :=
  Matrix.of fun _ j => if j = 0 then (1 : ℝ) else 0

theorem proj_comp_incl : proj * incl = 1 := by
  ext i j
  fin_cases i
  fin_cases j
  simp [proj, incl, Matrix.mul_apply, Matrix.of_apply]

theorem incl_comp_proj_ne : incl * proj ≠ 1 := by
  intro h
  have h11 := congr_fun (congr_fun h 1) 1
  rw [Matrix.mul_apply, Fin.sum_univ_one, one_apply] at h11
  simp [incl, proj, Matrix.of_apply] at h11

def covectorAxis : Fin 2 → ℝ :=
  fun i => if i = 1 then 1 else 0

/-- Substituting the left inverse into the right-inverse formula is false. -/
theorem left_inverse_reflection_fails :
    proj * incl = 1 ∧
    incl * proj ≠ 1 ∧
    pullback incl covectorAxis + (0 : Fin 1 → ℝ) = 0 ∧
    covectorAxis ≠ pullback proj ((0 : Fin 1 → ℝ) - 0) := by
  refine ⟨proj_comp_incl, incl_comp_proj_ne, ?_, ?_⟩
  · ext i
    fin_cases i
    simp [pullback, incl, covectorAxis, mulVec, dotProduct, transpose_apply, Matrix.of_apply]
  · intro h
    have hzero : pullback proj ((0 : Fin 1 → ℝ) - 0) = 0 := by
      simp [pullback, sub_self, mulVec_zero]
    have this := congr_fun h 1
    rw [hzero] at this
    simp [covectorAxis] at this

/-- The zero endomorphism has no right inverse, so existence of `W` is not free. -/
theorem rightInverse_hypothesis_is_not_free :
    ¬ ∃ W : Lin (Fin 1) (Fin 1), IsRightInverse (0 : Lin (Fin 1) (Fin 1)) W := by
  rintro ⟨W, hW⟩
  have h00 := congr_fun (congr_fun hW 0) 0
  simp at h00

#print axioms pullback_injective_of_rightInverse
#print axioms reflect_residual
#print axioms reflect_internal_direct
#print axioms reflect_residual_l1
#print axioms stationary_internal_l1
#print axioms apply_lInf_le_opLInf
#print axioms packedPairing_eq_frobenius
#print axioms full_contraction_eq_packed_dot
#print axioms rank_deficient_neither_sided_inverse
#print axioms deleted_direct_covector_does_not_force_zero
#print axioms wrong_off_diagonal_weight
#print axioms left_inverse_reflection_fails
#print axioms rightInverse_hypothesis_is_not_free

end D0.Research.SourceReflectionKernel
