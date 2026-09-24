import Mathlib.Algebra.Polynomial.Laurent
import Mathlib.Data.Fin.Tuple.Basic
import Mathlib.Data.ZMod.Basic
import Mathlib.Tactic

/-!
# Scalar one-color reverse-star locality no-go

This file concerns a scalar translation-covariant stencil and its scalar inverse.
It does not formalize or constrain the located two-color primal/dual `J`, nor the
Lorentz/observer metric star.  The only constitutive datum used below is the
accepted neighboring scalar first jet.
-/

namespace D0.Geometry.A4DLocalReverseStarNoGo

open LaurentPolynomial

abbrev Site5 := Fin 5
abbrev ScalarField5 := Site5 → ℚ

def cyclicNeighborSum (f : ScalarField5) (x : Site5) : ℚ :=
  f (x + 1) + f (x + 4)

def scalarKernel₁ (f : ScalarField5) (x : Site5) : ℚ :=
  (5 / 4 : ℚ) * f x + (1 / 4 : ℚ) * cyclicNeighborSum f x

def scalarKernel₂ (f : ScalarField5) (x : Site5) : ℚ :=
  (3 / 2 : ℚ) * f x + (1 / 4 : ℚ) * cyclicNeighborSum f x

noncomputable def W₁ : LaurentPolynomial ℚ :=
  C (5 / 4 : ℚ) + C (1 / 4 : ℚ) * T 1 + C (1 / 4 : ℚ) * T (-1)

noncomputable def W₂ : LaurentPolynomial ℚ :=
  C (3 / 2 : ℚ) + C (1 / 4 : ℚ) * T 1 + C (1 / 4 : ℚ) * T (-1)

theorem W₁_coefficients :
    W₁ 0 = 5 / 4 ∧ W₁ 1 = 1 / 4 ∧ W₁ (-1) = 1 / 4 := by
  norm_num [W₁, AddMonoidAlgebra.mul_apply_right, Finsupp.sum,
    LaurentPolynomial.C_apply, LaurentPolynomial.T_apply]

theorem W₂_coefficients :
    W₂ 0 = 3 / 2 ∧ W₂ 1 = 1 / 4 ∧ W₂ (-1) = 1 / 4 := by
  norm_num [W₂, AddMonoidAlgebra.mul_apply_right, Finsupp.sum,
    LaurentPolynomial.C_apply, LaurentPolynomial.T_apply]

def delta0 (x : Site5) : ℚ := if x = 0 then 1 else 0

def inverseColumn₁ : ScalarField5 := fun x =>
  match x.val with
  | 0 => 116 / 133
  | 1 => -24 / 133
  | 2 => 4 / 133
  | 3 => 4 / 133
  | _ => -24 / 133

def inverseColumn₂ : ScalarField5 := fun x =>
  match x.val with
  | 0 => 41 / 58
  | 1 => -7 / 58
  | 2 => 1 / 58
  | 3 => 1 / 58
  | _ => -7 / 58

theorem scalarKernel₁_inverseColumn :
    scalarKernel₁ inverseColumn₁ = delta0 := by
  funext x
  fin_cases x <;> norm_num [scalarKernel₁, cyclicNeighborSum, inverseColumn₁, delta0, Fin.add_def]

theorem scalarKernel₂_inverseColumn :
    scalarKernel₂ inverseColumn₂ = delta0 := by
  funext x
  fin_cases x <;> norm_num [scalarKernel₂, cyclicNeighborSum, inverseColumn₂, delta0, Fin.add_def]

theorem inverseColumn₁_distanceTwo_nonzero : inverseColumn₁ 2 ≠ 0 := by norm_num [inverseColumn₁, Fin.add_def]

theorem inverseColumn₂_distanceTwo_nonzero : inverseColumn₂ 2 ≠ 0 := by norm_num [inverseColumn₂, Fin.add_def]

/-! ## Units in the scalar Laurent ring -/

private noncomputable def maxExponent {R : Type*} [Semiring R]
    (p : LaurentPolynomial R) (hp : p ≠ 0) : ℤ :=
  p.support.max' (Finset.nonempty_iff_ne_empty.mpr (by
    intro h
    apply hp
    exact Finsupp.support_eq_empty.mp h))

private noncomputable def minExponent {R : Type*} [Semiring R]
    (p : LaurentPolynomial R) (hp : p ≠ 0) : ℤ :=
  p.support.min' (Finset.nonempty_iff_ne_empty.mpr (by
    intro h
    apply hp
    exact Finsupp.support_eq_empty.mp h))

private lemma maxExponent_mem_support {R : Type*} [Semiring R]
    (p : LaurentPolynomial R) (hp : p ≠ 0) :
    maxExponent p hp ∈ p.support := by
  exact Finset.max'_mem _ _

private lemma minExponent_mem_support {R : Type*} [Semiring R]
    (p : LaurentPolynomial R) (hp : p ≠ 0) :
    minExponent p hp ∈ p.support := by
  exact Finset.min'_mem _ _

private lemma coeff_mul_max_ne {R : Type*} [CommSemiring R] [NoZeroDivisors R]
    (p q : LaurentPolynomial R) (hp : p ≠ 0) (hq : q ≠ 0) :
    (p * q) (maxExponent p hp + maxExponent q hq) ≠ 0 := by
  rw [AddMonoidAlgebra.mul_apply_right, Finsupp.sum]
  let n := maxExponent q hq
  rw [Finset.sum_eq_single n]
  · have hpn : p (maxExponent p hp) ≠ 0 :=
      Finsupp.mem_support_iff.mp (maxExponent_mem_support p hp)
    have hqn : q n ≠ 0 := by
      exact Finsupp.mem_support_iff.mp (maxExponent_mem_support q hq)
    simpa [n] using mul_ne_zero hpn hqn
  · intro b hb hbn
    have hbmax : b ≤ maxExponent q hq := Finset.le_max' _ _ hb
    have hblt : b < maxExponent q hq := lt_of_le_of_ne hbmax hbn
    simp only [maxExponent] at hbmax hblt ⊢
    have hzero : p (p.support.max' (Finset.nonempty_iff_ne_empty.mpr (by
        intro h
        apply hp
        exact Finsupp.support_eq_empty.mp h)) +
        q.support.max' (Finset.nonempty_iff_ne_empty.mpr (by
          intro h
          apply hq
          exact Finsupp.support_eq_empty.mp h)) - b) = 0 := by
      apply Finsupp.notMem_support_iff.mp
      intro hm
      have hupper := Finset.le_max' p.support _ hm
      omega
    change p (maxExponent p hp + maxExponent q hq + -b) * q b = 0
    rw [show p (maxExponent p hp + maxExponent q hq + -b) = 0 by simpa [sub_eq_add_neg] using hzero]
    simp
  · intro hn
    exact False.elim (hn (maxExponent_mem_support q hq))

private lemma coeff_mul_min_ne {R : Type*} [CommSemiring R] [NoZeroDivisors R]
    (p q : LaurentPolynomial R) (hp : p ≠ 0) (hq : q ≠ 0) :
    (p * q) (minExponent p hp + minExponent q hq) ≠ 0 := by
  rw [AddMonoidAlgebra.mul_apply_right, Finsupp.sum]
  let n := minExponent q hq
  rw [Finset.sum_eq_single n]
  · have hpn : p (minExponent p hp) ≠ 0 :=
      Finsupp.mem_support_iff.mp (minExponent_mem_support p hp)
    have hqn : q n ≠ 0 :=
      Finsupp.mem_support_iff.mp (minExponent_mem_support q hq)
    simpa [n] using mul_ne_zero hpn hqn
  · intro b hb hbn
    have hbmin : minExponent q hq ≤ b := Finset.min'_le _ _ hb
    have hblt : minExponent q hq < b := lt_of_le_of_ne hbmin (Ne.symm hbn)
    simp only [minExponent] at hbmin hblt ⊢
    have hzero : p (p.support.min' (Finset.nonempty_iff_ne_empty.mpr (by
        intro h
        apply hp
        exact Finsupp.support_eq_empty.mp h)) +
        q.support.min' (Finset.nonempty_iff_ne_empty.mpr (by
          intro h
          apply hq
          exact Finsupp.support_eq_empty.mp h)) - b) = 0 := by
      apply Finsupp.notMem_support_iff.mp
      intro hm
      have hlower := Finset.min'_le p.support _ hm
      omega
    change p (minExponent p hp + minExponent q hq + -b) * q b = 0
    rw [show p (minExponent p hp + minExponent q hq + -b) = 0 by
      simpa [sub_eq_add_neg] using hzero]
    simp
  · intro hn
    exact False.elim (hn (minExponent_mem_support q hq))

theorem scalarLaurentUnit_support_singleton {R : Type*} [CommSemiring R] [NoZeroDivisors R]
    {p q : LaurentPolynomial R} {c : R}
    (hc : c ≠ 0) (h : p * q = C c) :
    ∃ n a, a ≠ 0 ∧ p = AddMonoidAlgebra.single n a := by
  have hp : p ≠ 0 := by
    intro hz
    rw [hz, zero_mul] at h
    have hc0 : C c = 0 := by simpa using h.symm
    exact hc (by simpa using congrArg (fun f : LaurentPolynomial R => f 0) hc0)
  have hq : q ≠ 0 := by
    intro hz
    rw [hz, mul_zero] at h
    have hc0 : C c = 0 := by simpa using h.symm
    exact hc (by simpa using congrArg (fun f : LaurentPolynomial R => f 0) hc0)
  have htop := coeff_mul_max_ne p q hp hq
  have hmax : maxExponent p hp + maxExponent q hq = 0 := by
    by_contra hn
    have hzero : (p * q) (maxExponent p hp + maxExponent q hq) = 0 := by
      rw [h]
      simp [hn]
    exact htop hzero
  have hbottom := coeff_mul_min_ne p q hp hq
  have hmin : minExponent p hp + minExponent q hq = 0 := by
    by_contra hn
    have hzero : (p * q) (minExponent p hp + minExponent q hq) = 0 := by
      rw [h]
      simp [hn]
    exact hbottom hzero
  have hple : minExponent p hp ≤ maxExponent p hp :=
    Finset.min'_le _ _ (maxExponent_mem_support p hp)
  have hqle : minExponent q hq ≤ maxExponent q hq :=
    Finset.min'_le _ _ (maxExponent_mem_support q hq)
  have hpsingle : minExponent p hp = maxExponent p hp := by omega
  refine ⟨maxExponent p hp, p (maxExponent p hp), ?_, ?_⟩
  · exact Finsupp.mem_support_iff.mp (maxExponent_mem_support p hp)
  · apply Finsupp.ext
    intro n
    by_cases hn : n = maxExponent p hp
    · subst n
      rw [AddMonoidAlgebra.single_apply, if_pos rfl]
    · have hnot : n ∉ p.support := by
        intro hm
        have hlo : minExponent p hp ≤ n := Finset.min'_le _ _ hm
        have hhi : n ≤ maxExponent p hp := Finset.le_max' _ _ hm
        rw [hpsingle] at hlo
        omega
      have hzero : p n = 0 := Finsupp.notMem_support_iff.mp hnot
      rw [AddMonoidAlgebra.single_apply, if_neg (Ne.symm hn)]
      exact hzero

/-! ## Uniform scalar family and the neighboring first jet -/

def radiusBounded {R : Type*} [Semiring R] (radius : ℕ) (p : LaurentPolynomial R) : Prop :=
  ∀ n ∈ p.support, -(radius : ℤ) ≤ n ∧ n ≤ radius

theorem radiusBounded_mul {R : Type*} [Semiring R]
    {r s : ℕ} {p q : LaurentPolynomial R}
    (hp : radiusBounded r p) (hq : radiusBounded s q) :
    radiusBounded (r + s) (p * q) := by
  intro n hn
  have hsum := AddMonoidAlgebra.support_mul p q hn
  rcases Finset.mem_add.mp hsum with ⟨i, hi, j, hj, rfl⟩
  have hpi := hp i hi
  have hqj := hq j hj
  constructor <;> simp only [Int.natCast_add] <;> omega

def periodizedCoefficient {R : Type*} [Semiring R]
    (period : ℕ) (p : LaurentPolynomial R) (r : ZMod period) : R :=
    Finset.sum (Finset.filter (fun n : ℤ => (n : ZMod period) = r) p.support) (fun n => p n)

/-- Coefficients of the cyclic convolution, obtained by folding Laurent exponents modulo `period`. -/
def periodizedScalarIdentity {R : Type*} [Semiring R]
    (period : ℕ) (p : LaurentPolynomial R) (c : R) : Prop :=
  ∀ r : ZMod period,
    periodizedCoefficient period p r = if r = 0 then c else 0

theorem residue_aliasFree {radius period : ℕ} (hperiod : 2 * radius < period)
    {a b : ℤ} (ha : -(radius : ℤ) ≤ a ∧ a ≤ radius)
    (hb : -(radius : ℤ) ≤ b ∧ b ≤ radius)
    (hab : (a : ZMod period) = (b : ZMod period)) : a = b := by
  have hmod : a ≡ b [ZMOD (period : ℤ)] :=
    (ZMod.intCast_eq_intCast_iff a b period).mp hab
  rcases Int.modEq_iff_dvd.mp hmod with ⟨k, hk⟩
  have hperiodZ : 2 * (radius : ℤ) < (period : ℤ) := by exact_mod_cast hperiod
  have hlow : -(period : ℤ) < b - a := by omega
  have hhigh : b - a < (period : ℤ) := by omega
  have habs : |b - a| < (period : ℤ) := by rw [abs_lt]; exact ⟨hlow, hhigh⟩
  have hba : b - a = 0 := Int.eq_zero_of_abs_lt_dvd hmod.dvd habs
  omega

private theorem periodizedCoefficient_eq_coeff {R : Type*} [Semiring R] {radius period : ℕ}
    {p : LaurentPolynomial R} (hp : radiusBounded radius p)
    (hperiod : 2 * radius < period) {n : ℤ}
    (hn : -(radius : ℤ) ≤ n ∧ n ≤ radius) :
    periodizedCoefficient period p (n : ZMod period) = p n := by
  classical
  unfold periodizedCoefficient
  by_cases hmem : n ∈ p.support
  · rw [Finset.sum_eq_single n]
    · intro b hb hbn
      have hb' := Finset.mem_filter.mp hb
      have hbound := hp b hb'.1
      have hsame := residue_aliasFree hperiod hbound hn hb'.2
      exact False.elim (hbn hsame)
    · intro hnot
      exact False.elim (hnot (Finset.mem_filter.mpr ⟨hmem, rfl⟩))
  · have hfilter := Finset.filter_eq_empty_iff.mpr (by
      intro b hb hres
      have hbound := hp b hb
      have hsame := residue_aliasFree hperiod hbound hn hres
      exact hmem (hsame ▸ hb))
    simp [hfilter, Finsupp.notMem_support_iff.mp hmem]

theorem periodized_identity_lifts_to_laurent_identity
    {radius reverseRadius period : ℕ} (hperiod : 2 * (radius + reverseRadius) < period)
    {R : Type*} [Semiring R] {p q : LaurentPolynomial R} {c : R}
    (hp : radiusBounded radius p) (hq : radiusBounded reverseRadius q)
    (hcyclic : periodizedScalarIdentity period (p * q) c) : p * q = C c := by
  have hprod : radiusBounded (radius + reverseRadius) (p * q) := radiusBounded_mul hp hq
  apply LaurentPolynomial.ext
  intro n
  by_cases hn : n = 0
  · subst n
    have hzeroFold := periodizedCoefficient_eq_coeff hprod hperiod
      (show -((radius + reverseRadius : ℕ) : ℤ) ≤ (0 : ℤ) ∧ (0 : ℤ) ≤ (radius + reverseRadius : ℕ) by omega)
    have hperiodized := hcyclic 0
    have hzeroFold' : periodizedCoefficient period (p * q) (0 : ZMod period) = (p * q) 0 := by
      simpa using hzeroFold
    rw [hzeroFold'] at hperiodized
    simpa using hperiodized
  · by_cases hmem : n ∈ (p * q).support
    · have hbound := hprod n hmem
      have hnonzeroResidue : (n : ZMod period) ≠ 0 := by
        intro hz
        have := residue_aliasFree hperiod hbound
          (show -((radius + reverseRadius : ℕ) : ℤ) ≤ (0 : ℤ) ∧ (0 : ℤ) ≤ ((radius + reverseRadius : ℕ) : ℤ) by omega)
          (by simpa using hz)
        exact hn this
      have hcoeff := periodizedCoefficient_eq_coeff hprod hperiod hbound
      have hperiodized := hcyclic (n : ZMod period)
      rw [hcoeff, if_neg hnonzeroResidue] at hperiodized
      simpa [LaurentPolynomial.C_apply, hn] using hperiodized
    · simp [Finsupp.notMem_support_iff.mp hmem, LaurentPolynomial.C_apply, hn]

theorem no_uniform_local_scalar_family_with_neighboring_jet
    {p q : LaurentPolynomial (Polynomial ℚ)}
    (hinv : p * q = C (1 : Polynomial ℚ))
    (hflat : (p 0).eval 0 = 1)
    (hneighbor : (p 1).coeff 1 = (1 / 2 : ℚ))
    (_hneighborReverse : (p (-1)).coeff 1 = (1 / 2 : ℚ)) : False := by
  obtain ⟨n, a, ha, hp⟩ := scalarLaurentUnit_support_singleton (R := Polynomial ℚ)
    (p := p) (q := q) (c := 1) one_ne_zero hinv
  by_cases hn : n = 0
  · have hp1 : p 1 = 0 := by
      rw [hp]
      simp [hn]
    rw [hp1] at hneighbor
    norm_num at hneighbor
  · rw [hp, AddMonoidAlgebra.single_apply] at hflat
    simp [hn] at hflat

theorem no_uniform_periodic_scalar_family_with_neighboring_jet
    {radius reverseRadius period : ℕ} (hperiod : 2 * (radius + reverseRadius) < period)
    {p q : LaurentPolynomial (Polynomial ℚ)}
    (hp : radiusBounded radius p) (hq : radiusBounded reverseRadius q)
    (hcyclic : periodizedScalarIdentity period (p * q) (1 : Polynomial ℚ))
    (hflat : (p 0).eval 0 = 1)
    (hneighbor : (p 1).coeff 1 = (1 / 2 : ℚ))
    (hneighborReverse : (p (-1)).coeff 1 = (1 / 2 : ℚ)) : False := by
  have hinv := periodized_identity_lifts_to_laurent_identity hperiod hp hq hcyclic
  exact no_uniform_local_scalar_family_with_neighboring_jet hinv hflat hneighbor hneighborReverse

end D0.Geometry.A4DLocalReverseStarNoGo
