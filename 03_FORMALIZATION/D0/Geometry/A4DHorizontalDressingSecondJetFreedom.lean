import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Matrix.Mul
import Mathlib.Tactic

/-!
# Quadratic endpoint dressing does not select the second jet

For an invertible endpoint dressing `P`,
`T^P_(x←y) = P_x T_(x←y) P_y⁻¹` preserves identity, exact composition, and
reversal when those laws are supplied for `T`.

The diagonal family `P_a(t) = diag(1 + a t², 1)` has `P_a(0) = I`, vanishing
odd part, and a second difference that depends on `a`. Coefficients `a = 1`
and `a = 2` therefore share the flat value and the flat first jet and still
differ at second order. Dressing the identity transport stays the identity, so
the freedom is this dressing class, not a change of every transport.
-/

namespace D0.Geometry

open Matrix

def dressedTransport {X ι : Type*} [Fintype ι] [DecidableEq ι]
    (T : X → X → Matrix ι ι ℚ) (P invP : X → Matrix ι ι ℚ) (x y : X) :
    Matrix ι ι ℚ :=
  P x * T x y * invP y

theorem dressedTransport_identity {X ι : Type*} [Fintype ι] [DecidableEq ι]
    (T : X → X → Matrix ι ι ℚ) (P invP : X → Matrix ι ι ℚ)
    (hT : ∀ x, T x x = 1) (hL : ∀ x, P x * invP x = 1) (x : X) :
    dressedTransport T P invP x x = 1 := by
  simp only [dressedTransport, hT x, Matrix.mul_one, hL x]

theorem dressedTransport_comp {X ι : Type*} [Fintype ι] [DecidableEq ι]
    (T : X → X → Matrix ι ι ℚ) (P invP : X → Matrix ι ι ℚ)
    (hcomp : ∀ x y z, T x y * T y z = T x z)
    (hinv : ∀ y, invP y * P y = 1) (x y z : X) :
    dressedTransport T P invP x y * dressedTransport T P invP y z =
      dressedTransport T P invP x z := by
  simp only [dressedTransport]
  calc
    (P x * T x y * invP y) * (P y * T y z * invP z) =
        P x * T x y * (invP y * (P y * T y z * invP z)) := by
          rw [Matrix.mul_assoc]
    _ = P x * T x y * ((invP y * (P y * T y z)) * invP z) := by
          rw [← Matrix.mul_assoc (invP y) (P y * T y z) (invP z)]
    _ = P x * T x y * (((invP y * P y) * T y z) * invP z) := by
          rw [← Matrix.mul_assoc (invP y) (P y) (T y z)]
    _ = P x * T x y * ((1 * T y z) * invP z) := by
          rw [hinv y]
    _ = P x * T x y * (T y z * invP z) := by
          rw [Matrix.one_mul]
    _ = (P x * (T x y * T y z)) * invP z := by
          rw [← Matrix.mul_assoc (P x * T x y) (T y z) (invP z),
            ← Matrix.mul_assoc (P x) (T x y) (T y z)]
    _ = P x * T x z * invP z := by
          rw [hcomp x y z]

theorem dressedTransport_reverse {X ι : Type*} [Fintype ι] [DecidableEq ι]
    (T : X → X → Matrix ι ι ℚ) (P invP : X → Matrix ι ι ℚ)
    (hrev : ∀ x y, T x y * T y x = 1)
    (hR : ∀ x, invP x * P x = 1) (hL : ∀ x, P x * invP x = 1) (x y : X) :
    dressedTransport T P invP x y * dressedTransport T P invP y x = 1 := by
  simp only [dressedTransport]
  calc
    (P x * T x y * invP y) * (P y * T y x * invP x) =
        P x * T x y * (invP y * (P y * T y x * invP x)) := by
          rw [Matrix.mul_assoc]
    _ = P x * T x y * ((invP y * (P y * T y x)) * invP x) := by
          rw [← Matrix.mul_assoc (invP y) (P y * T y x) (invP x)]
    _ = P x * T x y * (((invP y * P y) * T y x) * invP x) := by
          rw [← Matrix.mul_assoc (invP y) (P y) (T y x)]
    _ = P x * T x y * ((1 * T y x) * invP x) := by
          rw [hR y]
    _ = P x * T x y * (T y x * invP x) := by
          rw [Matrix.one_mul]
    _ = (P x * (T x y * T y x)) * invP x := by
          rw [← Matrix.mul_assoc (P x * T x y) (T y x) (invP x),
            ← Matrix.mul_assoc (P x) (T x y) (T y x)]
    _ = (P x * 1) * invP x := by
          rw [hrev x y]
    _ = P x * invP x := by
          rw [Matrix.mul_one]
    _ = 1 := hL x

/-- `P_a(t) = diag(1 + a t², 1)`. -/
def quadraticDressing (a t : ℚ) : Matrix (Fin 2) (Fin 2) ℚ :=
  fun i j =>
    if i = 0 ∧ j = 0 then 1 + a * t * t
    else if i = 1 ∧ j = 1 then 1
    else 0

/-- Diagonal inverse, defined as a matrix for every coefficient. -/
def quadraticDressingInv (a t : ℚ) : Matrix (Fin 2) (Fin 2) ℚ :=
  fun i j =>
    if i = 0 ∧ j = 0 then (1 + a * t * t)⁻¹
    else if i = 1 ∧ j = 1 then 1
    else 0

def witnessTransport : Matrix (Fin 2) (Fin 2) ℚ :=
  fun i j =>
    if i = 0 ∧ j = 1 then 1 else if i = 1 ∧ j = 0 then 1 else 0

private lemma fin2_mul (A B : Matrix (Fin 2) (Fin 2) ℚ) (i j : Fin 2) :
    (A * B) i j = A i 0 * B 0 j + A i 1 * B 1 j := by
  rw [Matrix.mul_apply, Fin.sum_univ_two]

theorem quadraticDressing_zero (a : ℚ) : quadraticDressing a 0 = 1 := by
  ext i j
  fin_cases i
  · fin_cases j
    · simp [quadraticDressing]
    · simp [quadraticDressing]
  · fin_cases j
    · simp [quadraticDressing, Matrix.one_apply]
    · simp [quadraticDressing, Matrix.one_apply]

theorem quadraticDressingInv_zero (a : ℚ) : quadraticDressingInv a 0 = 1 := by
  ext i j
  fin_cases i
  · fin_cases j
    · simp [quadraticDressingInv, Matrix.one_apply]
    · simp [quadraticDressingInv, Matrix.one_apply]
  · fin_cases j
    · simp [quadraticDressingInv, Matrix.one_apply]
    · simp [quadraticDressingInv, Matrix.one_apply]

theorem quadraticDressing_even (a t : ℚ) :
    quadraticDressing a (-t) = quadraticDressing a t := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [quadraticDressing]

theorem quadraticDressingInv_even (a t : ℚ) :
    quadraticDressingInv a (-t) = quadraticDressingInv a t := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [quadraticDressingInv]

theorem quadraticCoeff_ne_zero_of_nonneg (a t : ℚ) (ha : 0 ≤ a) :
    1 + a * t * t ≠ 0 := by
  have hnn : 0 ≤ a * (t * t) := mul_nonneg ha (mul_self_nonneg t)
  rw [← mul_assoc] at hnn
  intro h
  linarith

theorem quadraticDressing_mul_inv (a t : ℚ) (h : 1 + a * t * t ≠ 0) :
    quadraticDressing a t * quadraticDressingInv a t = 1 := by
  ext i j
  fin_cases i
  · fin_cases j
    · rw [fin2_mul]
      simp [quadraticDressing, quadraticDressingInv, Matrix.one_apply]
      exact mul_inv_cancel₀ h
    · rw [fin2_mul]
      simp [quadraticDressing, quadraticDressingInv, Matrix.one_apply]
  · fin_cases j
    · rw [fin2_mul]
      simp [quadraticDressing, quadraticDressingInv, Matrix.one_apply]
    · rw [fin2_mul]
      simp [quadraticDressing, quadraticDressingInv, Matrix.one_apply]

theorem quadraticDressing_inv_mul (a t : ℚ) (h : 1 + a * t * t ≠ 0) :
    quadraticDressingInv a t * quadraticDressing a t = 1 :=
  (mul_eq_one_comm).mp (quadraticDressing_mul_inv a t h)

theorem checker_times_invertible (a t : ℚ)
    (ha : a = 1 ∨ a = 2 ∨ a = -1) (ht : t = 0 ∨ t = 1 / 3 ∨ t = 1 / 2) :
    1 + a * t * t ≠ 0 := by
  rcases ha with rfl | rfl | rfl <;> rcases ht with rfl | rfl | rfl <;> norm_num

theorem endpointFactor_compose (Px Py invPy invPz : Matrix (Fin 2) (Fin 2) ℚ)
    (hy : invPy * Py = 1) :
    (Px * invPy) * (Py * invPz) = Px * invPz := by
  calc
    (Px * invPy) * (Py * invPz) = Px * (invPy * (Py * invPz)) := by
      rw [Matrix.mul_assoc]
    _ = Px * ((invPy * Py) * invPz) := by
      rw [← Matrix.mul_assoc invPy Py invPz]
    _ = Px * (1 * invPz) := by rw [hy]
    _ = Px * invPz := by rw [Matrix.one_mul]

/-- Checker identity: coefficients `1`, `2`, `-1` compose at `t ∈ {0, 1/3, 1/2}`. -/
theorem checker_quadratic_factors_compose (t : ℚ)
    (ht : t = 0 ∨ t = 1 / 3 ∨ t = 1 / 2) :
    (quadraticDressing 1 t * quadraticDressingInv 2 t) *
        (quadraticDressing 2 t * quadraticDressingInv (-1) t) =
      quadraticDressing 1 t * quadraticDressingInv (-1) t := by
  apply endpointFactor_compose
  exact quadraticDressing_inv_mul 2 t
    (checker_times_invertible 2 t (by norm_num) ht)

lemma quadraticDressing_apply_00 (a t : ℚ) :
    quadraticDressing a t (0 : Fin 2) (0 : Fin 2) = 1 + a * t * t := by
  simp [quadraticDressing]

theorem quadraticDressing_secondDifference_00 (a t : ℚ) :
    (quadraticDressing a t + quadraticDressing a (-t) -
        (2 : ℚ) • quadraticDressing a 0) (0 : Fin 2) (0 : Fin 2) =
      2 * a * t * t := by
  rw [quadraticDressing_even, quadraticDressing_zero]
  simp only [Matrix.add_apply, Matrix.sub_apply, Matrix.smul_apply,
    quadraticDressing_apply_00, Matrix.one_apply, if_true]
  ring

theorem quadraticDressing_secondJet_nonzero :
    quadraticDressing 1 (1 / 2) + quadraticDressing 1 (-(1 / 2)) -
        (2 : ℚ) • quadraticDressing 1 0 ≠ 0 := by
  intro h
  have hentry := congr_fun (congr_fun h (0 : Fin 2)) (0 : Fin 2)
  rw [quadraticDressing_secondDifference_00, Matrix.zero_apply] at hentry
  norm_num at hentry

theorem quadraticDressing_secondJets_differ :
    (quadraticDressing 1 (1 / 2) + quadraticDressing 1 (-(1 / 2)) -
        (2 : ℚ) • quadraticDressing 1 0) ≠
      (quadraticDressing 2 (1 / 2) + quadraticDressing 2 (-(1 / 2)) -
        (2 : ℚ) • quadraticDressing 2 0) := by
  intro h
  have hentry := congr_fun (congr_fun h (0 : Fin 2)) (0 : Fin 2)
  rw [quadraticDressing_secondDifference_00, quadraticDressing_secondDifference_00] at hentry
  norm_num at hentry

theorem dressedIdentity_stays (a t : ℚ) (h : 1 + a * t * t ≠ 0) :
    quadraticDressing a t * (1 : Matrix (Fin 2) (Fin 2) ℚ) * quadraticDressingInv a t = 1 := by
  rw [Matrix.mul_one]
  exact quadraticDressing_mul_inv a t h

lemma dressedWitness_01 (a t : ℚ) :
    (quadraticDressing a t * witnessTransport * quadraticDressingInv a t)
        (0 : Fin 2) (1 : Fin 2) = 1 + a * t * t := by
  rw [Matrix.mul_assoc, fin2_mul]
  have hP00 : quadraticDressing a t (0 : Fin 2) (0 : Fin 2) = 1 + a * t * t :=
    quadraticDressing_apply_00 a t
  have hP01 : quadraticDressing a t (0 : Fin 2) (1 : Fin 2) = 0 := by
    simp [quadraticDressing]
  have hWinv01 : (witnessTransport * quadraticDressingInv a t) (0 : Fin 2) (1 : Fin 2) = 1 := by
    rw [fin2_mul]
    simp [witnessTransport, quadraticDressingInv]
  have hWinv11 : (witnessTransport * quadraticDressingInv a t) (1 : Fin 2) (1 : Fin 2) = 0 := by
    rw [fin2_mul]
    simp [witnessTransport, quadraticDressingInv]
  simp [hP00, hP01, hWinv01, hWinv11]

lemma dressedWitness_even (a t : ℚ) :
    quadraticDressing a (-t) * witnessTransport * quadraticDressingInv a (-t) =
      quadraticDressing a t * witnessTransport * quadraticDressingInv a t := by
  rw [quadraticDressing_even, quadraticDressingInv_even]

lemma dressedWitness_zero (a : ℚ) :
    quadraticDressing a 0 * witnessTransport * quadraticDressingInv a 0 =
      witnessTransport := by
  rw [quadraticDressing_zero, quadraticDressingInv_zero, Matrix.one_mul, Matrix.mul_one]

theorem dressedWitness_secondJets_differ :
    (quadraticDressing 1 (1 / 2) * witnessTransport * quadraticDressingInv 1 (1 / 2) +
        quadraticDressing 1 (-(1 / 2)) * witnessTransport *
          quadraticDressingInv 1 (-(1 / 2)) -
        (2 : ℚ) •
          (quadraticDressing 1 0 * witnessTransport * quadraticDressingInv 1 0)) ≠
      (quadraticDressing 2 (1 / 2) * witnessTransport * quadraticDressingInv 2 (1 / 2) +
        quadraticDressing 2 (-(1 / 2)) * witnessTransport *
          quadraticDressingInv 2 (-(1 / 2)) -
        (2 : ℚ) •
          (quadraticDressing 2 0 * witnessTransport * quadraticDressingInv 2 0)) := by
  intro h
  have hentry := congr_fun (congr_fun h (0 : Fin 2)) (1 : Fin 2)
  rw [dressedWitness_even, dressedWitness_even] at hentry
  simp only [Matrix.add_apply, Matrix.sub_apply, Matrix.smul_apply, dressedWitness_01,
    dressedWitness_zero, witnessTransport] at hentry
  ring_nf at hentry
  norm_num at hentry

/-- In this diagonal quadratic class, flat value and evenness do not fix the
second difference. Identity transport stays the identity. -/
theorem quadraticEndpointClass_preservesFlatJet_changesSecondJet :
    quadraticDressing 1 0 = 1 ∧
      quadraticDressing 2 0 = 1 ∧
      (∀ t, quadraticDressing 1 (-t) = quadraticDressing 1 t) ∧
      (∀ t, quadraticDressing 2 (-t) = quadraticDressing 2 t) ∧
      (∀ t, 1 + (1 : ℚ) * t * t ≠ 0) ∧
      (∀ t, 1 + (2 : ℚ) * t * t ≠ 0) ∧
      (∀ a t, 0 ≤ a →
        quadraticDressing a t * (1 : Matrix (Fin 2) (Fin 2) ℚ) *
          quadraticDressingInv a t = 1) ∧
      (quadraticDressing 1 (1 / 2) + quadraticDressing 1 (-(1 / 2)) -
          (2 : ℚ) • quadraticDressing 1 0) ≠ 0 ∧
      (quadraticDressing 1 (1 / 2) + quadraticDressing 1 (-(1 / 2)) -
          (2 : ℚ) • quadraticDressing 1 0) ≠
        (quadraticDressing 2 (1 / 2) + quadraticDressing 2 (-(1 / 2)) -
          (2 : ℚ) • quadraticDressing 2 0) :=
  ⟨quadraticDressing_zero 1, quadraticDressing_zero 2,
    quadraticDressing_even 1, quadraticDressing_even 2,
    fun t => quadraticCoeff_ne_zero_of_nonneg 1 t (by norm_num),
    fun t => quadraticCoeff_ne_zero_of_nonneg 2 t (by norm_num),
    fun a t ha => dressedIdentity_stays a t (quadraticCoeff_ne_zero_of_nonneg a t ha),
    quadraticDressing_secondJet_nonzero, quadraticDressing_secondJets_differ⟩

end D0.Geometry
