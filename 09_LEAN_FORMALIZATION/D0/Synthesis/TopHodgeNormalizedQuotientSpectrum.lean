import Mathlib.Tactic
import D0.Synthesis.TopHodgeSpectralSceneReconstruction
import D0.Synthesis.PhasonActiveSceneConjugacy

/-!
# Top-Hodge data determine the active normalized-quotient spectrum

For positive complete-tripartite zone sizes `a,b,c`, let

```
V = a+b+c,   E = ab+ac+bc,   T = abc
```

and let `M` be the row-normalized equitable quotient.  Its normalized
Laplacian is `L = I-M`.  This module proves from the actual `3 × 3` matrix that

```
det(xI-L) = x · (x² - 3x + 2VE/(VE-T)).
```

The denominator is intrinsic and nonzero:

```
VE-T = (a+b)(a+c)(b+c) > 0.
```

Thus the active/nonzero factor has trace `3` and product
`2VE/(VE-T)`.

The preceding owner `TopHodgeSpectralSceneReconstruction` proves that the
actual complete top-Hodge spectral data

```
D = dim C₂,   H = dim ker Δ₂,   M₂ = Σ λᵢ²
```

recover `T=D`, `V=M₂/D-6`, and `E=T+V-1-H`.  Composing the two results gives a
generic top-Hodge-to-normalized-spectrum map, rather than a scene-only
numerical coincidence.

At `(a,b,c)=(9,11,13)` the active factor is

```
x² - 3x + 359/160,
```

exactly the characteristic polynomial of the owned S_DE two-mode transfer.

**Canonical boundary.**  The top-Hodge data canonically determine the active
characteristic polynomial, hence its eigenvalue multiset/similarity invariant.
They do not choose a basis of the active plane or a particular intertwiner.
The existing `active_intertwiner_coordinate_nonunique` theorem gives the exact
scene-level witness to this residual coordinate freedom.

**Negative control.**  `K(2,6,6)` and `K(3,3,8)` have the same `D` and `M₂`,
but different `H`; their active products are respectively `35/16` and
`266/121`.  Hence the harmonic multiplicity is load-bearing.
-/

namespace D0.Synthesis.TopHodgeNormalizedQuotientSpectrum

open Matrix
open scoped BigOperators

abbrev Zone3 := Fin 3

/-! ## Generic positive complete-tripartite quotient -/

/-- Vertex elementary symmetric invariant. -/
def tripartiteV (a b c : ℚ) : ℚ := a + b + c

/-- Edge elementary symmetric invariant. -/
def tripartiteE (a b c : ℚ) : ℚ := a * b + a * c + b * c

/-- Triangle elementary symmetric invariant. -/
def tripartiteT (a b c : ℚ) : ℚ := a * b * c

/-- Product of the three nonzero row degrees. -/
def degreeProduct (a b c : ℚ) : ℚ :=
  (a + b) * (a + c) * (b + c)

/-- The row-normalized equitable quotient of `K(a,b,c)`. -/
def normalizedQuotientTransport (a b c : ℚ) :
    Matrix Zone3 Zone3 ℚ :=
  !![0, b / (b + c), c / (b + c);
     a / (a + c), 0, c / (a + c);
     a / (a + b), b / (a + b), 0]

/-- The normalized quotient Laplacian `I-M`. -/
def normalizedQuotientLaplacian (a b c : ℚ) :
    Matrix Zone3 Zone3 ℚ :=
  1 - normalizedQuotientTransport a b c

/-- Product of the two nonzero/active normalized-Laplacian eigenvalues. -/
def normalizedActiveProduct (a b c : ℚ) : ℚ :=
  2 * tripartiteV a b c * tripartiteE a b c /
    (tripartiteV a b c * tripartiteE a b c - tripartiteT a b c)

/-- The active quadratic factor. -/
def normalizedActivePolynomial (a b c x : ℚ) : ℚ :=
  x ^ 2 - 3 * x + normalizedActiveProduct a b c

/-- The denominator in the active product is exactly the product of row
degrees. -/
theorem VE_sub_T_eq_degreeProduct (a b c : ℚ) :
    tripartiteV a b c * tripartiteE a b c - tripartiteT a b c =
      degreeProduct a b c := by
  simp [tripartiteV, tripartiteE, tripartiteT, degreeProduct]
  ring

/-- Positive zones make every row degree, and therefore the active
denominator, strictly positive. -/
theorem VE_sub_T_pos {a b c : ℚ}
    (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) :
    0 < tripartiteV a b c * tripartiteE a b c -
      tripartiteT a b c := by
  rw [VE_sub_T_eq_degreeProduct]
  unfold degreeProduct
  positivity

/-- In particular the active denominator cannot vanish. -/
theorem VE_sub_T_ne_zero {a b c : ℚ}
    (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) :
    tripartiteV a b c * tripartiteE a b c -
      tripartiteT a b c ≠ 0 :=
  ne_of_gt (VE_sub_T_pos ha hb hc)

/-- The active product is strictly positive, so the factor `x` in the full
characteristic polynomial is not repeated inside the active quadratic. -/
theorem normalizedActiveProduct_pos {a b c : ℚ}
    (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) :
    0 < normalizedActiveProduct a b c := by
  unfold normalizedActiveProduct
  have hV : 0 < tripartiteV a b c := by
    simp [tripartiteV]
    positivity
  have hE : 0 < tripartiteE a b c := by
    simp [tripartiteE]
    positivity
  have hden := VE_sub_T_pos ha hb hc
  positivity

/-- For nonzero row degrees the quotient transport is row-stochastic. -/
theorem normalizedQuotientTransport_row_stochastic
    {a b c : ℚ}
    (hab : a + b ≠ 0) (hac : a + c ≠ 0) (hbc : b + c ≠ 0) :
    ∀ i, ∑ j, normalizedQuotientTransport a b c i j = 1 := by
  intro i
  fin_cases i <;>
    simp [normalizedQuotientTransport, Fin.sum_univ_succ] <;>
    field_simp

/-- The normalized quotient Laplacian has trace `3`; this is the sum of its
two active eigenvalues because the stochastic mode is zero. -/
theorem normalizedQuotientLaplacian_trace (a b c : ℚ) :
    Matrix.trace (normalizedQuotientLaplacian a b c) = 3 := by
  simp [normalizedQuotientLaplacian, normalizedQuotientTransport,
    Matrix.trace, Fin.sum_univ_succ]

/-- **Generic active-factor theorem.**  This is derived from the determinant
of the actual normalized quotient matrix. -/
theorem normalizedQuotientLaplacian_charpoly
    {a b c : ℚ}
    (hab : a + b ≠ 0) (hac : a + c ≠ 0) (hbc : b + c ≠ 0)
    (x : ℚ) :
    (x • (1 : Matrix Zone3 Zone3 ℚ) -
        normalizedQuotientLaplacian a b c).det =
      x * normalizedActivePolynomial a b c x := by
  have hpoly :
      normalizedActivePolynomial a b c x =
        x ^ 2 - 3 * x +
          2 * tripartiteV a b c * tripartiteE a b c /
            degreeProduct a b c := by
    unfold normalizedActivePolynomial normalizedActiveProduct
    rw [VE_sub_T_eq_degreeProduct]
  rw [hpoly]
  simp [normalizedQuotientLaplacian, normalizedQuotientTransport,
    tripartiteV, tripartiteE, degreeProduct, Matrix.det_fin_three]
  field_simp [hab, hac, hbc]
  ring

/-! ## Reconstruction from actual top-Hodge spectral data -/

open D0.Synthesis.TopHodgeSpectralSceneReconstruction
open D0.Synthesis.SceneInvariantReconstruction

/-- Positive zone size `p+1` as a rational. -/
def zoneSizeQ (p : ℕ) : ℚ := p + 1

/-- `D = dim C₂`. -/
def spectralD (p q r : ℕ) : ℚ :=
  topHodgeTriangleDimension p q r

/-- `H = dim ker Δ₂`. -/
noncomputable def spectralH (p q r : ℕ) : ℚ :=
  topHodgeHarmonicMultiplicity p q r

/-- `M₂ = Σ λᵢ²`. -/
def spectralM2 (p q r : ℕ) : ℚ :=
  topHodgeSecondMoment p q r

/-- Recovered `T=D`. -/
def recoveredT (p q r : ℕ) : ℚ := spectralD p q r

/-- Recovered `V=M₂/D-6`. -/
def recoveredV (p q r : ℕ) : ℚ :=
  spectralM2 p q r / spectralD p q r - 6

/-- Recovered `E=T+V-1-H`. -/
noncomputable def recoveredE (p q r : ℕ) : ℚ :=
  recoveredT p q r + recoveredV p q r - 1 - spectralH p q r

/-- Active product computed only from the top-Hodge spectral coordinates. -/
noncomputable def activeProductFromTopHodgeData (p q r : ℕ) : ℚ :=
  2 * recoveredV p q r * recoveredE p q r /
    (recoveredV p q r * recoveredE p q r - recoveredT p q r)

/-- The recovered triangle invariant is the actual `abc`. -/
theorem recoveredT_eq_tripartiteT (p q r : ℕ) :
    recoveredT p q r =
      tripartiteT (zoneSizeQ p) (zoneSizeQ q) (zoneSizeQ r) := by
  simp [recoveredT, spectralD, topHodgeTriangleDimension_formula,
    tripartiteT, zoneSizeQ]

/-- The recovered vertex invariant is the actual `a+b+c`. -/
theorem recoveredV_eq_tripartiteV (p q r : ℕ) :
    recoveredV p q r =
      tripartiteV (zoneSizeQ p) (zoneSizeQ q) (zoneSizeQ r) := by
  calc
    recoveredV p q r =
        (vertexCount (p + 1) (q + 1) (r + 1) : ℚ) := by
      exact (vertexCount_from_topHodgeSecondMoment p q r).symm
    _ = tripartiteV (zoneSizeQ p) (zoneSizeQ q) (zoneSizeQ r) := by
      simp [vertexCount, tripartiteV, zoneSizeQ]

/-- The recovered Euler coordinate is the actual edge invariant `ab+ac+bc`. -/
theorem recoveredE_eq_tripartiteE (p q r : ℕ) :
    recoveredE p q r =
      tripartiteE (zoneSizeQ p) (zoneSizeQ q) (zoneSizeQ r) := by
  rw [recoveredE, recoveredT_eq_tripartiteT,
    recoveredV_eq_tripartiteV]
  simp [spectralH, topHodgeHarmonicMultiplicity_formula,
    tripartiteT, tripartiteV, tripartiteE, zoneSizeQ]
  ring

/-- Bundle: the actual top-Hodge data recover all three elementary symmetric
coordinates used by the active factor. -/
theorem topHodge_data_recovers_VET (p q r : ℕ) :
    recoveredV p q r =
        tripartiteV (zoneSizeQ p) (zoneSizeQ q) (zoneSizeQ r) ∧
      recoveredE p q r =
        tripartiteE (zoneSizeQ p) (zoneSizeQ q) (zoneSizeQ r) ∧
      recoveredT p q r =
        tripartiteT (zoneSizeQ p) (zoneSizeQ q) (zoneSizeQ r) :=
  ⟨recoveredV_eq_tripartiteV p q r,
    recoveredE_eq_tripartiteE p q r,
    recoveredT_eq_tripartiteT p q r⟩

/-- The top-Hodge-recovered denominator is positive for every admissible
complete-tripartite complex. -/
theorem recovered_active_denominator_pos (p q r : ℕ) :
    0 < recoveredV p q r * recoveredE p q r - recoveredT p q r := by
  rw [recoveredV_eq_tripartiteV, recoveredE_eq_tripartiteE,
    recoveredT_eq_tripartiteT]
  apply VE_sub_T_pos <;> simp [zoneSizeQ] <;> positivity

/-- The top-Hodge formula is exactly the generic normalized active product. -/
theorem activeProductFromTopHodgeData_eq (p q r : ℕ) :
    activeProductFromTopHodgeData p q r =
      normalizedActiveProduct
        (zoneSizeQ p) (zoneSizeQ q) (zoneSizeQ r) := by
  simp only [activeProductFromTopHodgeData, normalizedActiveProduct]
  rw [recoveredV_eq_tripartiteV, recoveredE_eq_tripartiteE,
    recoveredT_eq_tripartiteT]

/-- **Top-Hodge-to-active-spectrum synthesis.**  The three actual top-Hodge
spectral data determine the characteristic polynomial of the normalized
quotient Laplacian. -/
theorem topHodge_data_determines_normalized_charpoly
    (p q r : ℕ) (x : ℚ) :
    (x • (1 : Matrix Zone3 Zone3 ℚ) -
        normalizedQuotientLaplacian
          (zoneSizeQ p) (zoneSizeQ q) (zoneSizeQ r)).det =
      x * (x ^ 2 - 3 * x + activeProductFromTopHodgeData p q r) := by
  have hab : zoneSizeQ p + zoneSizeQ q ≠ 0 := by
    simp [zoneSizeQ]
    positivity
  have hac : zoneSizeQ p + zoneSizeQ r ≠ 0 := by
    simp [zoneSizeQ]
    positivity
  have hbc : zoneSizeQ q + zoneSizeQ r ≠ 0 := by
    simp [zoneSizeQ]
    positivity
  rw [normalizedQuotientLaplacian_charpoly hab hac hbc]
  simp only [normalizedActivePolynomial]
  rw [activeProductFromTopHodgeData_eq]

/-! ## Scene specialization and the owned S_DE operator -/

/-- The scene top-Hodge data force the active product `359/160`. -/
theorem scene_activeProductFromTopHodgeData :
    activeProductFromTopHodgeData 8 10 12 = 359 / 160 := by
  rw [activeProductFromTopHodgeData_eq]
  norm_num [normalizedActiveProduct, tripartiteV, tripartiteE,
    tripartiteT, zoneSizeQ]

/-- The generic scene transport is literally the already-owned scene matrix. -/
theorem scene_normalizedQuotientTransport_eq_owned :
    normalizedQuotientTransport
        (zoneSizeQ 8) (zoneSizeQ 10) (zoneSizeQ 12) =
      D0.Spectral.zoneTransport := by
  native_decide

/-- Therefore the generic scene Laplacian is the operator used by the owned
S_DE active-sector conjugacy. -/
theorem scene_normalizedQuotientLaplacian_eq_owned :
    normalizedQuotientLaplacian
        (zoneSizeQ 8) (zoneSizeQ 10) (zoneSizeQ 12) =
      D0.Synthesis.PhasonActiveSceneConjugacy.normalizedSceneLaplacian := by
  native_decide

/-- The scene active quadratic is exactly the characteristic polynomial of
the owned two-mode S_DE transfer. -/
theorem scene_activePolynomial_eq_ownedSDECharacteristic (x : ℚ) :
    x ^ 2 - 3 * x + 359 / 160 =
      D0.Cosmology.phasonFlipTransferCharacteristic x := by
  norm_num [D0.Cosmology.phasonFlipTransferCharacteristic,
    D0.Cosmology.phasonFlipTransferMatrix]
  ring

/-- Exact determinant-level link: the full normalized scene quotient has one
stationary zero mode and the owned S_DE characteristic as its active factor. -/
theorem scene_normalized_charpoly_eq_x_mul_ownedSDE (x : ℚ) :
    (x • (1 : Matrix Zone3 Zone3 ℚ) -
        normalizedQuotientLaplacian
          (zoneSizeQ 8) (zoneSizeQ 10) (zoneSizeQ 12)).det =
      x * D0.Cosmology.phasonFlipTransferCharacteristic x := by
  rw [topHodge_data_determines_normalized_charpoly]
  rw [scene_activeProductFromTopHodgeData]
  rw [scene_activePolynomial_eq_ownedSDECharacteristic]

/-! ## Negative controls and canonical boundary -/

/-- **Harmonic multiplicity is load-bearing.**  Equal `D` and `M₂` do not
determine the active factor without `H`. -/
theorem harmonic_multiplicity_load_bearing_for_active_product :
    spectralD 1 5 5 = spectralD 2 2 7 ∧
      spectralM2 1 5 5 = spectralM2 2 2 7 ∧
      spectralH 1 5 5 ≠ spectralH 2 2 7 ∧
      activeProductFromTopHodgeData 1 5 5 = 35 / 16 ∧
      activeProductFromTopHodgeData 2 2 7 = 266 / 121 ∧
      activeProductFromTopHodgeData 1 5 5 ≠
        activeProductFromTopHodgeData 2 2 7 := by
  rw [activeProductFromTopHodgeData_eq,
    activeProductFromTopHodgeData_eq]
  simp [spectralD, spectralM2, spectralH,
    topHodgeTriangleDimension_formula, topHodgeSecondMoment_formula,
    topHodgeHarmonicMultiplicity_formula, normalizedActiveProduct,
    tripartiteV, tripartiteE, tripartiteT, zoneSizeQ]
  norm_num

/-- The active characteristic polynomial does not choose coordinates: the
owned scene has two distinct full-rank intertwiners with the same active image. -/
theorem active_polynomial_does_not_choose_coordinates :
    (2 : ℚ) •
        D0.Synthesis.PhasonActiveSceneConjugacy.activeEmbedding ≠
      D0.Synthesis.PhasonActiveSceneConjugacy.activeEmbedding ∧
      D0.Synthesis.PhasonActiveSceneConjugacy.normalizedSceneLaplacian *
          ((2 : ℚ) •
            D0.Synthesis.PhasonActiveSceneConjugacy.activeEmbedding) =
        ((2 : ℚ) •
            D0.Synthesis.PhasonActiveSceneConjugacy.activeEmbedding) *
          D0.Synthesis.PhasonActiveSceneConjugacy.sdeTransfer := by
  exact
    ⟨D0.Synthesis.PhasonActiveSceneConjugacy.active_intertwiner_coordinate_nonunique.1,
      D0.Synthesis.PhasonActiveSceneConjugacy.active_intertwiner_coordinate_nonunique.2.1⟩

/-- Capstone package: generic determinant factor, positive denominator, and
the exact scene/S_DE specialization. -/
theorem topHodge_normalized_quotient_spectral_synthesis :
    (∀ p q r : ℕ,
      0 < recoveredV p q r * recoveredE p q r - recoveredT p q r) ∧
      (∀ p q r : ℕ, ∀ x : ℚ,
        (x • (1 : Matrix Zone3 Zone3 ℚ) -
            normalizedQuotientLaplacian
              (zoneSizeQ p) (zoneSizeQ q) (zoneSizeQ r)).det =
          x * (x ^ 2 - 3 * x +
            activeProductFromTopHodgeData p q r)) ∧
      activeProductFromTopHodgeData 8 10 12 = 359 / 160 ∧
      (∀ x : ℚ,
        x ^ 2 - 3 * x + 359 / 160 =
          D0.Cosmology.phasonFlipTransferCharacteristic x) :=
  ⟨recovered_active_denominator_pos,
    topHodge_data_determines_normalized_charpoly,
    scene_activeProductFromTopHodgeData,
    scene_activePolynomial_eq_ownedSDECharacteristic⟩

end D0.Synthesis.TopHodgeNormalizedQuotientSpectrum
