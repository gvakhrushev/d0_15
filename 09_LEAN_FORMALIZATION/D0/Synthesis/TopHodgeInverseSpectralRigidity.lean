import Mathlib.Tactic
import D0.Synthesis.TopHodgeNormalizedQuotientSpectrum

/-!
# Generic top-Hodge inverse-spectral rigidity

For the canonical complete-tripartite clique complex with positive zone sizes

```
a = p + 1,  b = q + 1,  c = r + 1,
```

the actual top-Hodge data

```
D  = dim C₂,
H  = dim ker Δ₂,
M₂ = Σ λᵢ²
```

recover the three elementary symmetric functions

```
V = a+b+c,  E = ab+ac+bc,  T = abc.
```

The previous owners stopped at this `V,E,T` reconstruction generically and
proved equality of the unordered zone multiset only for the numerical scene.
This module closes the generic inverse problem.  The key algebraic owner is
the monic polynomial

```
(X-a)(X-b)(X-c) = X³ - V X² + E X - T.
```

Equality of `V,E,T` makes these polynomials equal; taking their actual
polynomial root multisets then recovers `{a,b,c}` including multiplicities.
Consequently equal actual top-Hodge triples `(D,H,M₂)` force equal unordered
zone-size triples for every pair of positive complete-tripartite complexes.

No distinctness, ordering, numerical bound, root search, or scene constants
are used.  The theorem is permutation-invariant, as it must be: spectral data
do not select labels for the three zones.

The controls show that every coordinate is load-bearing:

* `K(2,6,6)` and `K(3,3,8)` have equal `D,M₂` but different `H`;
* `K(2,15,15)` and `K(3,3,50)` have equal `D,H` but different `M₂`;
* `K(3,17,22)` and `K(4,8,33)` have equal `H,M₂` but different `D`.

Thus the result is rigidity of the full top-Hodge data, not of an arbitrary
proper projection of those data.
-/

namespace D0.Synthesis.TopHodgeInverseSpectralRigidity

open Polynomial
open D0.Synthesis.SceneInvariantReconstruction
open D0.Synthesis.TopHodgeSpectralSceneReconstruction
open D0.Synthesis.TopHodgeNormalizedQuotientSpectrum

/-- The monic cubic whose root multiset is the three zone sizes. -/
noncomputable def zoneRootPolynomial (a b c : ℚ) : Polynomial ℚ :=
  (X - Polynomial.C a) * (X - Polynomial.C b) *
    (X - Polynomial.C c)

/-- Vieta expansion of the zone-root polynomial. -/
theorem zoneRootPolynomial_vieta (a b c : ℚ) :
    zoneRootPolynomial a b c =
      X ^ 3 - Polynomial.C (tripartiteV a b c) * X ^ 2 +
        Polynomial.C (tripartiteE a b c) * X -
          Polynomial.C (tripartiteT a b c) := by
  simp [zoneRootPolynomial, tripartiteV, tripartiteE, tripartiteT]
  ring

/-- Equality of the three elementary symmetric invariants forces equality of
the complete zone-root polynomials. -/
theorem zoneRootPolynomial_eq_of_VET_eq
    {a b c a' b' c' : ℚ}
    (hV : tripartiteV a b c = tripartiteV a' b' c')
    (hE : tripartiteE a b c = tripartiteE a' b' c')
    (hT : tripartiteT a b c = tripartiteT a' b' c') :
    zoneRootPolynomial a b c = zoneRootPolynomial a' b' c' := by
  rw [zoneRootPolynomial_vieta, zoneRootPolynomial_vieta, hV, hE, hT]

/-- The polynomial owner remembers the full root multiset, including repeated
zone sizes. -/
theorem zoneRootPolynomial_roots (a b c : ℚ) :
    (zoneRootPolynomial a b c).roots = ({a, b, c} : Multiset ℚ) := by
  rw [zoneRootPolynomial,
    Polynomial.roots_mul
      (mul_ne_zero
        (mul_ne_zero (Polynomial.X_sub_C_ne_zero a)
          (Polynomial.X_sub_C_ne_zero b))
        (Polynomial.X_sub_C_ne_zero c)),
    Polynomial.roots_mul
      (mul_ne_zero (Polynomial.X_sub_C_ne_zero a)
        (Polynomial.X_sub_C_ne_zero b)),
    Polynomial.roots_X_sub_C, Polynomial.roots_X_sub_C,
    Polynomial.roots_X_sub_C]
  rfl

/-- **Generic Vieta rigidity.**  Three rational triples with equal elementary
symmetric invariants have the same unordered multiset.  This is the missing
generic root-multiset lemma behind the earlier scene-only reconstruction. -/
theorem unordered_triple_eq_of_VET_eq
    {a b c a' b' c' : ℚ}
    (hV : tripartiteV a b c = tripartiteV a' b' c')
    (hE : tripartiteE a b c = tripartiteE a' b' c')
    (hT : tripartiteT a b c = tripartiteT a' b' c') :
    ({a, b, c} : Multiset ℚ) = ({a', b', c'} : Multiset ℚ) := by
  rw [← zoneRootPolynomial_roots a b c,
    ← zoneRootPolynomial_roots a' b' c']
  exact congrArg Polynomial.roots
    (zoneRootPolynomial_eq_of_VET_eq hV hE hT)

/-- Natural-number form of generic Vieta rigidity. -/
theorem unordered_nat_triple_eq_of_VET_eq
    {a b c a' b' c' : ℕ}
    (hV :
      tripartiteV a b c = tripartiteV a' b' c')
    (hE :
      tripartiteE a b c = tripartiteE a' b' c')
    (hT :
      tripartiteT a b c = tripartiteT a' b' c') :
    ({a, b, c} : Multiset ℕ) = ({a', b', c'} : Multiset ℕ) := by
  apply Multiset.map_injective
    (Nat.cast_injective : Function.Injective (fun n : ℕ => (n : ℚ)))
  simpa using unordered_triple_eq_of_VET_eq hV hE hT

/-! ## Inverse rigidity from the actual top-Hodge data -/

/-- Equality of actual top-Hodge data forces equality of all three recovered
elementary symmetric invariants. -/
theorem equal_topHodge_data_force_equal_VET
    {p q r p' q' r' : ℕ}
    (hD :
      topHodgeTriangleDimension p q r =
        topHodgeTriangleDimension p' q' r')
    (hH :
      topHodgeHarmonicMultiplicity p q r =
        topHodgeHarmonicMultiplicity p' q' r')
    (hM2 :
      topHodgeSecondMoment p q r =
        topHodgeSecondMoment p' q' r') :
    recoveredV p q r = recoveredV p' q' r' ∧
      recoveredE p q r = recoveredE p' q' r' ∧
      recoveredT p q r = recoveredT p' q' r' := by
  have hDq : spectralD p q r = spectralD p' q' r' := by
    simpa [spectralD] using
      congrArg (fun n : ℕ => (n : ℚ)) hD
  have hHq : spectralH p q r = spectralH p' q' r' := by
    simpa [spectralH] using
      congrArg (fun n : ℕ => (n : ℚ)) hH
  have hM2q : spectralM2 p q r = spectralM2 p' q' r' := hM2
  have hV :
      recoveredV p q r = recoveredV p' q' r' := by
    simp only [recoveredV]
    rw [hDq, hM2q]
  have hT :
      recoveredT p q r = recoveredT p' q' r' := by
    simp only [recoveredT]
    exact hDq
  have hE :
      recoveredE p q r = recoveredE p' q' r' := by
    simp only [recoveredE]
    rw [hT, hV, hHq]
  exact ⟨hV, hE, hT⟩

/-- **Generic inverse-spectral rigidity theorem.**  Equal actual top-Hodge
data determine the complete-tripartite isomorphism class, represented
canonically by the unordered multiset of its three positive zone sizes. -/
theorem topHodge_inverse_spectral_rigidity
    {p q r p' q' r' : ℕ}
    (hD :
      topHodgeTriangleDimension p q r =
        topHodgeTriangleDimension p' q' r')
    (hH :
      topHodgeHarmonicMultiplicity p q r =
        topHodgeHarmonicMultiplicity p' q' r')
    (hM2 :
      topHodgeSecondMoment p q r =
        topHodgeSecondMoment p' q' r') :
    ({p + 1, q + 1, r + 1} : Multiset ℕ) =
      ({p' + 1, q' + 1, r' + 1} : Multiset ℕ) := by
  rcases equal_topHodge_data_force_equal_VET hD hH hM2 with
    ⟨hV, hE, hT⟩
  rw [recoveredV_eq_tripartiteV, recoveredV_eq_tripartiteV] at hV
  rw [recoveredE_eq_tripartiteE, recoveredE_eq_tripartiteE] at hE
  rw [recoveredT_eq_tripartiteT, recoveredT_eq_tripartiteT] at hT
  have hV' :
      tripartiteV ((p + 1 : ℕ) : ℚ) ((q + 1 : ℕ) : ℚ)
          ((r + 1 : ℕ) : ℚ) =
        tripartiteV ((p' + 1 : ℕ) : ℚ) ((q' + 1 : ℕ) : ℚ)
          ((r' + 1 : ℕ) : ℚ) := by
    simpa [zoneSizeQ] using hV
  have hE' :
      tripartiteE ((p + 1 : ℕ) : ℚ) ((q + 1 : ℕ) : ℚ)
          ((r + 1 : ℕ) : ℚ) =
        tripartiteE ((p' + 1 : ℕ) : ℚ) ((q' + 1 : ℕ) : ℚ)
          ((r' + 1 : ℕ) : ℚ) := by
    simpa [zoneSizeQ] using hE
  have hT' :
      tripartiteT ((p + 1 : ℕ) : ℚ) ((q + 1 : ℕ) : ℚ)
          ((r + 1 : ℕ) : ℚ) =
        tripartiteT ((p' + 1 : ℕ) : ℚ) ((q' + 1 : ℕ) : ℚ)
          ((r' + 1 : ℕ) : ℚ) := by
    simpa [zoneSizeQ] using hT
  exact unordered_nat_triple_eq_of_VET_eq hV' hE' hT'

/-- The theorem cannot and should not recover an ordering of the zones:
permuting zone labels preserves all actual top-Hodge data. -/
theorem topHodge_data_do_not_choose_zone_labels :
    topHodgeTriangleDimension 1 2 3 =
        topHodgeTriangleDimension 2 1 3 ∧
      topHodgeHarmonicMultiplicity 1 2 3 =
        topHodgeHarmonicMultiplicity 2 1 3 ∧
      topHodgeSecondMoment 1 2 3 =
        topHodgeSecondMoment 2 1 3 ∧
      (1, 2, 3) ≠ (2, 1, 3) := by
  rw [topHodgeTriangleDimension_formula,
    topHodgeTriangleDimension_formula,
    topHodgeHarmonicMultiplicity_formula,
    topHodgeHarmonicMultiplicity_formula,
    topHodgeSecondMoment_formula,
    topHodgeSecondMoment_formula]
  norm_num

/-! ## Load-bearing controls -/

/-- Omitting `H` destroys rigidity. -/
theorem without_H_inverse_rigidity_fails :
    topHodgeTriangleDimension 1 5 5 =
        topHodgeTriangleDimension 2 2 7 ∧
      topHodgeSecondMoment 1 5 5 =
        topHodgeSecondMoment 2 2 7 ∧
      ({2, 6, 6} : Multiset ℕ) ≠ ({3, 3, 8} : Multiset ℕ) := by
  rw [topHodgeTriangleDimension_formula,
    topHodgeTriangleDimension_formula,
    topHodgeSecondMoment_formula,
    topHodgeSecondMoment_formula]
  norm_num
  decide

/-- Omitting `M₂` destroys rigidity, even with every reduced size positive. -/
theorem without_M2_inverse_rigidity_fails :
    topHodgeTriangleDimension 1 14 14 =
        topHodgeTriangleDimension 2 2 49 ∧
      topHodgeHarmonicMultiplicity 1 14 14 =
        topHodgeHarmonicMultiplicity 2 2 49 ∧
      ({2, 15, 15} : Multiset ℕ) ≠ ({3, 3, 50} : Multiset ℕ) := by
  rw [topHodgeTriangleDimension_formula,
    topHodgeTriangleDimension_formula,
    topHodgeHarmonicMultiplicity_formula,
    topHodgeHarmonicMultiplicity_formula]
  norm_num
  decide

/-- Omitting `D` destroys rigidity, even with every reduced size positive. -/
theorem without_D_inverse_rigidity_fails :
    topHodgeHarmonicMultiplicity 2 16 21 =
        topHodgeHarmonicMultiplicity 3 7 32 ∧
      topHodgeSecondMoment 2 16 21 =
        topHodgeSecondMoment 3 7 32 ∧
      ({3, 17, 22} : Multiset ℕ) ≠ ({4, 8, 33} : Multiset ℕ) := by
  rw [topHodgeHarmonicMultiplicity_formula,
    topHodgeHarmonicMultiplicity_formula,
    topHodgeSecondMoment_formula,
    topHodgeSecondMoment_formula]
  norm_num
  decide

/-- Capstone bundle: exact generic rigidity, residual permutation freedom,
and the load-bearing status of all three spectral coordinates. -/
theorem topHodge_inverse_spectral_rigidity_synthesis :
    (∀ {p q r p' q' r' : ℕ},
      topHodgeTriangleDimension p q r =
          topHodgeTriangleDimension p' q' r' →
      topHodgeHarmonicMultiplicity p q r =
          topHodgeHarmonicMultiplicity p' q' r' →
      topHodgeSecondMoment p q r =
          topHodgeSecondMoment p' q' r' →
      ({p + 1, q + 1, r + 1} : Multiset ℕ) =
        ({p' + 1, q' + 1, r' + 1} : Multiset ℕ)) ∧
      (1, 2, 3) ≠ (2, 1, 3) ∧
      ({2, 6, 6} : Multiset ℕ) ≠ ({3, 3, 8} : Multiset ℕ) ∧
      ({2, 15, 15} : Multiset ℕ) ≠ ({3, 3, 50} : Multiset ℕ) ∧
      ({3, 17, 22} : Multiset ℕ) ≠ ({4, 8, 33} : Multiset ℕ) := by
  refine ⟨?_, by decide, by decide, by decide, by decide⟩
  intro p q r p' q' r' hD hH hM2
  exact topHodge_inverse_spectral_rigidity hD hH hM2

end D0.Synthesis.TopHodgeInverseSpectralRigidity
