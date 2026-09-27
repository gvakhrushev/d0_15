import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic

/-!
# D0.Gravity.A4DSchurEinsteinDirectIdentification

Standalone exact formalization of merged research owner #273.

The finite Schur coefficients are reconstructed directly from the exact regular
connection block and mixed first symbol exported by #270. The linearized
Einstein coefficients are defined independently from the standard Minkowski
index formula. No E_eta object is imported or used.

This is a flat linear-symbol theorem only.
-/

namespace D0.Gravity.A4DSchurEinsteinDirectIdentification

open BigOperators Matrix

def symPair (i : Fin 10) : Fin 4 × Fin 4 :=
  match i.val with
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
  | _ => (3, 3)

def symTriple (i : Fin 20) : Fin 4 × Fin 4 × Fin 4 :=
  match i.val with
  | 0 => (0, 0, 0)
  | 1 => (0, 0, 1)
  | 2 => (0, 0, 2)
  | 3 => (0, 0, 3)
  | 4 => (0, 1, 1)
  | 5 => (0, 1, 2)
  | 6 => (0, 1, 3)
  | 7 => (0, 2, 2)
  | 8 => (0, 2, 3)
  | 9 => (0, 3, 3)
  | 10 => (1, 1, 1)
  | 11 => (1, 1, 2)
  | 12 => (1, 1, 3)
  | 13 => (1, 2, 2)
  | 14 => (1, 2, 3)
  | 15 => (1, 3, 3)
  | 16 => (2, 2, 2)
  | 17 => (2, 2, 3)
  | 18 => (2, 3, 3)
  | 19 => (3, 3, 3)
  | _ => (3, 3, 3)


def eta (r : Fin 4) : ℚ :=
  match r.val with
  | 0 => 1
  | _ => -1

def etaMetric (a b : Fin 4) : ℚ := if a = b then eta a else 0

def coordFactor (a b : Fin 4) : ℚ := if a = b then 1 else 2

def monoCoeff2 (a b : Fin 4) (m : Fin 10) : ℚ :=
  let p := symPair m
  if (a = p.1 ∧ b = p.2) ∨ (a = p.2 ∧ b = p.1) then 1 else 0

def hBasis (j : Fin 10) (a b : Fin 4) : ℚ :=
  let p := symPair j
  if (a = p.1 ∧ b = p.2) ∨ (a = p.2 ∧ b = p.1) then 1 else 0

def a0 (i : Fin 24) (j : Fin 24) : ℚ :=
  match i.val, j.val with
  | 0, 15 => 1
  | 0, 22 => 1
  | 1, 9 => -1
  | 1, 23 => 1
  | 2, 10 => -1
  | 2, 17 => -1
  | 3, 7 => 1
  | 3, 12 => -1
  | 4, 8 => 1
  | 4, 18 => -1
  | 5, 14 => 1
  | 5, 19 => -1
  | 6, 13 => 1
  | 6, 20 => 1
  | 7, 3 => 1
  | 7, 12 => -1
  | 8, 4 => 1
  | 8, 18 => -1
  | 9, 1 => -1
  | 9, 23 => 1
  | 10, 2 => -1
  | 10, 17 => -1
  | 11, 16 => 1
  | 11, 21 => -1
  | 12, 3 => -1
  | 12, 7 => -1
  | 13, 6 => 1
  | 13, 20 => 1
  | 14, 5 => 1
  | 14, 19 => -1
  | 15, 0 => 1
  | 15, 22 => -1
  | 16, 11 => 1
  | 16, 21 => 1
  | 17, 2 => -1
  | 17, 10 => -1
  | 18, 4 => -1
  | 18, 8 => -1
  | 19, 5 => -1
  | 19, 14 => -1
  | 20, 6 => 1
  | 20, 13 => 1
  | 21, 11 => -1
  | 21, 16 => 1
  | 22, 0 => 1
  | 22, 15 => -1
  | 23, 1 => 1
  | 23, 9 => 1
  | _, _ => 0

def a0Inv (i : Fin 24) (j : Fin 24) : ℚ :=
  match i.val, j.val with
  | 0, 0 => (1 : ℚ) / 2
  | 0, 15 => (1 : ℚ) / 2
  | 0, 22 => (1 : ℚ) / 2
  | 1, 1 => (1 : ℚ) / 2
  | 1, 9 => (-1 : ℚ) / 2
  | 1, 23 => (1 : ℚ) / 2
  | 2, 2 => (1 : ℚ) / 2
  | 2, 10 => (-1 : ℚ) / 2
  | 2, 17 => (-1 : ℚ) / 2
  | 3, 3 => (-1 : ℚ) / 2
  | 3, 7 => (1 : ℚ) / 2
  | 3, 12 => (-1 : ℚ) / 2
  | 4, 4 => (-1 : ℚ) / 2
  | 4, 8 => (1 : ℚ) / 2
  | 4, 18 => (-1 : ℚ) / 2
  | 5, 5 => (-1 : ℚ) / 2
  | 5, 14 => (1 : ℚ) / 2
  | 5, 19 => (-1 : ℚ) / 2
  | 6, 6 => (-1 : ℚ) / 2
  | 6, 13 => (1 : ℚ) / 2
  | 6, 20 => (1 : ℚ) / 2
  | 7, 3 => (1 : ℚ) / 2
  | 7, 7 => (-1 : ℚ) / 2
  | 7, 12 => (-1 : ℚ) / 2
  | 8, 4 => (1 : ℚ) / 2
  | 8, 8 => (-1 : ℚ) / 2
  | 8, 18 => (-1 : ℚ) / 2
  | 9, 1 => (-1 : ℚ) / 2
  | 9, 9 => (1 : ℚ) / 2
  | 9, 23 => (1 : ℚ) / 2
  | 10, 2 => (-1 : ℚ) / 2
  | 10, 10 => (1 : ℚ) / 2
  | 10, 17 => (-1 : ℚ) / 2
  | 11, 11 => (1 : ℚ) / 2
  | 11, 16 => (1 : ℚ) / 2
  | 11, 21 => (-1 : ℚ) / 2
  | 12, 3 => (-1 : ℚ) / 2
  | 12, 7 => (-1 : ℚ) / 2
  | 12, 12 => (-1 : ℚ) / 2
  | 13, 6 => (1 : ℚ) / 2
  | 13, 13 => (-1 : ℚ) / 2
  | 13, 20 => (1 : ℚ) / 2
  | 14, 5 => (1 : ℚ) / 2
  | 14, 14 => (-1 : ℚ) / 2
  | 14, 19 => (-1 : ℚ) / 2
  | 15, 0 => (1 : ℚ) / 2
  | 15, 15 => (1 : ℚ) / 2
  | 15, 22 => (-1 : ℚ) / 2
  | 16, 11 => (1 : ℚ) / 2
  | 16, 16 => (1 : ℚ) / 2
  | 16, 21 => (1 : ℚ) / 2
  | 17, 2 => (-1 : ℚ) / 2
  | 17, 10 => (-1 : ℚ) / 2
  | 17, 17 => (1 : ℚ) / 2
  | 18, 4 => (-1 : ℚ) / 2
  | 18, 8 => (-1 : ℚ) / 2
  | 18, 18 => (-1 : ℚ) / 2
  | 19, 5 => (-1 : ℚ) / 2
  | 19, 14 => (-1 : ℚ) / 2
  | 19, 19 => (-1 : ℚ) / 2
  | 20, 6 => (1 : ℚ) / 2
  | 20, 13 => (1 : ℚ) / 2
  | 20, 20 => (-1 : ℚ) / 2
  | 21, 11 => (-1 : ℚ) / 2
  | 21, 16 => (1 : ℚ) / 2
  | 21, 21 => (1 : ℚ) / 2
  | 22, 0 => (1 : ℚ) / 2
  | 22, 15 => (-1 : ℚ) / 2
  | 22, 22 => (1 : ℚ) / 2
  | 23, 1 => (1 : ℚ) / 2
  | 23, 9 => (1 : ℚ) / 2
  | 23, 23 => (1 : ℚ) / 2
  | _, _ => 0

def cCoeff (a : Fin 24) (i : Fin 10) (r : Fin 4) : ℚ :=
  match a.val, i.val, r.val with
  | 0, 5, 2 => (-1 : ℚ) / 2
  | 0, 6, 3 => (-1 : ℚ) / 2
  | 0, 7, 1 => (1 : ℚ) / 2
  | 0, 9, 1 => (1 : ℚ) / 2
  | 1, 4, 2 => (1 : ℚ) / 2
  | 1, 5, 1 => (-1 : ℚ) / 2
  | 1, 8, 3 => (-1 : ℚ) / 2
  | 1, 9, 2 => (1 : ℚ) / 2
  | 2, 4, 3 => (1 : ℚ) / 2
  | 2, 6, 1 => (-1 : ℚ) / 2
  | 2, 7, 3 => (1 : ℚ) / 2
  | 2, 8, 2 => (-1 : ℚ) / 2
  | 3, 1, 2 => (1 : ℚ) / 2
  | 3, 2, 1 => (-1 : ℚ) / 2
  | 4, 1, 3 => (1 : ℚ) / 2
  | 4, 3, 1 => (-1 : ℚ) / 2
  | 5, 2, 3 => (1 : ℚ) / 2
  | 5, 3, 2 => (-1 : ℚ) / 2
  | 6, 2, 2 => (1 : ℚ) / 2
  | 6, 3, 3 => (1 : ℚ) / 2
  | 6, 7, 0 => (-1 : ℚ) / 2
  | 6, 9, 0 => (-1 : ℚ) / 2
  | 7, 1, 2 => (-1 : ℚ) / 2
  | 7, 5, 0 => (1 : ℚ) / 2
  | 8, 1, 3 => (-1 : ℚ) / 2
  | 8, 6, 0 => (1 : ℚ) / 2
  | 9, 0, 2 => (-1 : ℚ) / 2
  | 9, 2, 0 => (1 : ℚ) / 2
  | 9, 8, 3 => (-1 : ℚ) / 2
  | 9, 9, 2 => (1 : ℚ) / 2
  | 10, 0, 3 => (-1 : ℚ) / 2
  | 10, 3, 0 => (1 : ℚ) / 2
  | 10, 7, 3 => (1 : ℚ) / 2
  | 10, 8, 2 => (-1 : ℚ) / 2
  | 11, 5, 3 => (-1 : ℚ) / 2
  | 11, 6, 2 => (1 : ℚ) / 2
  | 12, 2, 1 => (-1 : ℚ) / 2
  | 12, 5, 0 => (1 : ℚ) / 2
  | 13, 1, 1 => (1 : ℚ) / 2
  | 13, 3, 3 => (1 : ℚ) / 2
  | 13, 4, 0 => (-1 : ℚ) / 2
  | 13, 9, 0 => (-1 : ℚ) / 2
  | 14, 2, 3 => (-1 : ℚ) / 2
  | 14, 8, 0 => (1 : ℚ) / 2
  | 15, 0, 1 => (1 : ℚ) / 2
  | 15, 1, 0 => (-1 : ℚ) / 2
  | 15, 6, 3 => (1 : ℚ) / 2
  | 15, 9, 1 => (-1 : ℚ) / 2
  | 16, 5, 3 => (-1 : ℚ) / 2
  | 16, 8, 1 => (1 : ℚ) / 2
  | 17, 0, 3 => (-1 : ℚ) / 2
  | 17, 3, 0 => (1 : ℚ) / 2
  | 17, 4, 3 => (1 : ℚ) / 2
  | 17, 6, 1 => (-1 : ℚ) / 2
  | 18, 3, 1 => (-1 : ℚ) / 2
  | 18, 6, 0 => (1 : ℚ) / 2
  | 19, 3, 2 => (-1 : ℚ) / 2
  | 19, 8, 0 => (1 : ℚ) / 2
  | 20, 1, 1 => (1 : ℚ) / 2
  | 20, 2, 2 => (1 : ℚ) / 2
  | 20, 4, 0 => (-1 : ℚ) / 2
  | 20, 7, 0 => (-1 : ℚ) / 2
  | 21, 6, 2 => (-1 : ℚ) / 2
  | 21, 8, 1 => (1 : ℚ) / 2
  | 22, 0, 1 => (1 : ℚ) / 2
  | 22, 1, 0 => (-1 : ℚ) / 2
  | 22, 5, 2 => (1 : ℚ) / 2
  | 22, 7, 1 => (-1 : ℚ) / 2
  | 23, 0, 2 => (1 : ℚ) / 2
  | 23, 2, 0 => (-1 : ℚ) / 2
  | 23, 4, 2 => (-1 : ℚ) / 2
  | 23, 5, 1 => (1 : ℚ) / 2
  | _, _, _ => 0


def c1 (k : Fin 4 → ℚ) : Matrix (Fin 24) (Fin 10) ℚ := fun a i =>
  ∑ r, cCoeff a i r * k r

/-- Exact coefficient expansion of `-C₁ᵀ A₀⁻¹ C₁` in the ten symmetric
quadratic momentum monomials. -/
def schurCoeff (out inp m : Fin 10) : ℚ :=
  let p := symPair m
  if h : p.1 = p.2 then
    - ∑ a : Fin 24, ∑ b : Fin 24,
        cCoeff a out p.1 * a0Inv a b * cCoeff b inp p.1
  else
    - ∑ a : Fin 24, ∑ b : Fin 24,
        (cCoeff a out p.1 * a0Inv a b * cCoeff b inp p.2 +
         cCoeff a out p.2 * a0Inv a b * cCoeff b inp p.1)

def k2Coeff (m : Fin 10) : ℚ :=
  ∑ r : Fin 4, eta r * monoCoeff2 r r m

def traceBasis (j : Fin 10) : ℚ :=
  ∑ r : Fin 4, eta r * hBasis j r r

def kkCoeff (j m : Fin 10) : ℚ :=
  ∑ r : Fin 4, ∑ s : Fin 4,
    eta r * eta s * hBasis j r s * monoCoeff2 r s m

def einsteinLowerCoeff (mu nu : Fin 4) (j m : Fin 10) : ℚ :=
  (1 / 2 : ℚ) * (
    (∑ r : Fin 4, eta r * hBasis j nu r * monoCoeff2 mu r m) +
    (∑ r : Fin 4, eta r * hBasis j mu r * monoCoeff2 nu r m) -
    k2Coeff m * hBasis j mu nu -
    monoCoeff2 mu nu m * traceBasis j -
    etaMetric mu nu * (kkCoeff j m - k2Coeff m * traceBasis j))

def einsteinUpCoeff (mu nu : Fin 4) (j m : Fin 10) : ℚ :=
  eta mu * eta nu * einsteinLowerCoeff mu nu j m

def einsteinCoordCoeff (out inp m : Fin 10) : ℚ :=
  let p := symPair out
  coordFactor p.1 p.2 * einsteinUpCoeff p.1 p.2 inp m

def einsteinLowerCoordCoeff (out inp m : Fin 10) : ℚ :=
  let p := symPair out
  coordFactor p.1 p.2 * einsteinLowerCoeff p.1 p.2 inp m

def einsteinNo2Coeff (out inp m : Fin 10) : ℚ :=
  let p := symPair out
  einsteinUpCoeff p.1 p.2 inp m

theorem a0_right_inverse : a0 * a0Inv = (1 : Matrix (Fin 24) (Fin 24) ℚ) := by
  native_decide

theorem a0_left_inverse : a0Inv * a0 = (1 : Matrix (Fin 24) (Fin 24) ℚ) := by
  native_decide

theorem schurCoeff_eq_neg_half_einstein :
    ∀ out inp m : Fin 10,
      schurCoeff out inp m = (-1 / 2 : ℚ) * einsteinCoordCoeff out inp m := by
  native_decide

def quadMonomial (k : Fin 4 → ℚ) (m : Fin 10) : ℚ :=
  let p := symPair m
  k p.1 * k p.2

def symbolFromCoeff
    (coeff : Fin 10 → Fin 10 → Fin 10 → ℚ)
    (k : Fin 4 → ℚ) : Matrix (Fin 10) (Fin 10) ℚ := fun i j =>
  ∑ m : Fin 10, coeff i j m * quadMonomial k m

def schurSymbol (k : Fin 4 → ℚ) : Matrix (Fin 10) (Fin 10) ℚ :=
  symbolFromCoeff schurCoeff k

def einsteinSymbol (k : Fin 4 → ℚ) : Matrix (Fin 10) (Fin 10) ℚ :=
  symbolFromCoeff einsteinCoordCoeff k

theorem schurSymbol_eq_neg_half_einstein (k : Fin 4 → ℚ) :
    schurSymbol k = (-1 / 2 : ℚ) • einsteinSymbol k := by
  ext i j
  change (∑ m : Fin 10, schurCoeff i j m * quadMonomial k m) =
    (-1 / 2 : ℚ) * (∑ m : Fin 10, einsteinCoordCoeff i j m * quadMonomial k m)
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro m hm
  rw [schurCoeff_eq_neg_half_einstein]
  ring

def monoCoeff3 (a b c : Fin 4) (t : Fin 20) : ℚ :=
  let p := symTriple t
  if
      (a = p.1 ∧ b = p.2.1 ∧ c = p.2.2) ∨
      (a = p.1 ∧ b = p.2.2 ∧ c = p.2.1) ∨
      (a = p.2.1 ∧ b = p.1 ∧ c = p.2.2) ∨
      (a = p.2.1 ∧ b = p.2.2 ∧ c = p.1) ∨
      (a = p.2.2 ∧ b = p.1 ∧ c = p.2.1) ∨
      (a = p.2.2 ∧ b = p.2.1 ∧ c = p.1)
    then 1 else 0

def bianchiCoeff (nu : Fin 4) (inp : Fin 10) (t : Fin 20) : ℚ :=
  ∑ mu : Fin 4, ∑ m : Fin 10,
    let p := symPair m
    einsteinUpCoeff mu nu inp m * monoCoeff3 mu p.1 p.2 t

theorem bianchiCoeff_zero :
    ∀ nu : Fin 4, ∀ inp : Fin 10, ∀ t : Fin 20,
      bianchiCoeff nu inp t = 0 := by
  native_decide

def cubicMonomial (k : Fin 4 → ℚ) (t : Fin 20) : ℚ :=
  let p := symTriple t
  k p.1 * k p.2.1 * k p.2.2

def bianchiPolynomial (k : Fin 4 → ℚ) (nu : Fin 4) (inp : Fin 10) : ℚ :=
  ∑ t : Fin 20, bianchiCoeff nu inp t * cubicMonomial k t

theorem bianchiPolynomial_zero (k : Fin 4 → ℚ) (nu : Fin 4) (inp : Fin 10) :
    bianchiPolynomial k nu inp = 0 := by
  simp [bianchiPolynomial, bianchiCoeff_zero]

def bianchiForInput (k : Fin 4 → ℚ) (q : Fin 10 → ℚ) (nu : Fin 4) : ℚ :=
  ∑ inp : Fin 10, q inp * bianchiPolynomial k nu inp

theorem bianchi_all (k : Fin 4 → ℚ) (q : Fin 10 → ℚ) (nu : Fin 4) :
    bianchiForInput k q nu = 0 := by
  simp [bianchiForInput, bianchiPolynomial_zero]

theorem hostile_lower_output_witness :
    schurCoeff 1 1 7 +
      (1 / 2 : ℚ) * einsteinLowerCoordCoeff 1 1 7 ≠ 0 := by
  native_decide

theorem hostile_no_offdiag_factor_witness :
    schurCoeff 1 1 7 +
      (1 / 2 : ℚ) * einsteinNo2Coeff 1 1 7 ≠ 0 := by
  native_decide

theorem hostile_reversed_schur_sign_witness :
    - schurCoeff 0 4 7 +
      (1 / 2 : ℚ) * einsteinCoordCoeff 0 4 7 ≠ 0 := by
  native_decide

end D0.Gravity.A4DSchurEinsteinDirectIdentification
