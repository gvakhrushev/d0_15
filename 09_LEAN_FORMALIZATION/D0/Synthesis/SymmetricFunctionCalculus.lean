import Mathlib.Tactic

/-!
# One symmetric-function calculus behind three separately-computed scene objects

Three objects in the corpus are computed independently of one another:

* the **transport cubic** — the characteristic polynomial of the quotient matrix, `λ³ − 359λ − 2574`
  (`D0.Spectral.TransportClosedForm`);
* the **degree normalisation** `√(528 · 440 · 480) = 10560` appearing in `D0-SCENE-ACTIVE-EIGENVALUES-001`;
* the **active scene-Laplacian eigenvalues** of §04.2, with sum `3` and product `359/160`, obtained
  there from `det S = 2 · 1287 / 10560 = 39/160`.

They are one calculus. Let `n = (n₁, n₂, n₃)` be the zone sizes, `N = e₁ = n₁+n₂+n₃`, and `e₂, e₃`
the remaining elementary symmetric functions. Then:

**1. The degree product is not an independent number.** The three degrees of a complete tripartite
scene are `N − nᵢ`, and

    (N−n₁)(N−n₂)(N−n₃) = N·e₂ − e₃                    (`degree_product`)

— a polynomial identity, proved by `ring`, valid for any three sizes. At `(9,11,13)` it reads
`24 · 22 · 20 = 33 · 359 − 1287 = 10560`, which is exactly the `√(528·440·480)` of the source row;
and `528 = 24·22`, `440 = 22·20`, `480 = 24·20` are the pairwise degree products
(`degree_pairs`), so the square root there is formal.

**2. The transport cubic is `λ³ − e₂λ − 2e₃`.** The quotient matrix is `𝟙nᵀ − diag n`, whose trace
vanishes, whose principal `2×2` minors sum to `−e₂` and whose determinant is `2e₃`
(`transport_coefficients`). So `359` and `2574` are `e₂` and `2e₃`, not free coefficients.

**3. The active eigenvalues follow.** With `det S = 2e₃ / (N·e₂ − e₃)`, their product is

    2 + det S = 2·N·e₂ / (N·e₂ − e₃)                   (`active_product`)

which at `(9,11,13)` is `2·33·359 / 10560 = 359/160`, the source row's value, while the sum is `3`.

So the physical readout of §04.2, the transport spectrum, and the degree normalisation are three
faces of `e₂` and `e₃` of the zone sizes, tied together by the single identity of item 1. Nothing
here is fitted: each equality is an identity in the three sizes, instantiated at `(9,11,13)` only
at the end.
-/

namespace D0.Synthesis.SymmetricFunctionCalculus

variable (a b c : ℚ)

/-- `e₁`, the total scene size. -/
def e1 : ℚ := a + b + c

/-- `e₂`. -/
def e2 : ℚ := a * b + a * c + b * c

/-- `e₃`. -/
def e3 : ℚ := a * b * c

/-- **The degree-product identity.** The degrees of a complete tripartite scene are `N − nᵢ`, and
their product is `N·e₂ − e₃`. Valid for any three sizes. -/
theorem degree_product :
    (e1 a b c - a) * (e1 a b c - b) * (e1 a b c - c) = e1 a b c * e2 a b c - e3 a b c := by
  unfold e1 e2 e3; ring

/-- **The transport coefficients.** For `Q = 𝟙nᵀ − diag n` the trace vanishes, the principal
`2×2` minors sum to `−e₂`, and the determinant is `2e₃`; so the cubic is `λ³ − e₂λ − 2e₃`. -/
theorem transport_coefficients :
    (0 * 0 - b * a) + (0 * 0 - c * a) + (0 * 0 - c * b) = -(e2 a b c) ∧
    (0 * (0 * 0 - c * b) - b * (a * 0 - c * a) + c * (a * b - 0 * a)) = 2 * e3 a b c := by
  constructor <;> · simp only [e2, e3]; ring

/-- **The active-eigenvalue product.** `2 + det S` with `det S = 2e₃/(N e₂ − e₃)`. -/
theorem active_product (h : e1 a b c * e2 a b c - e3 a b c ≠ 0) :
    2 + 2 * e3 a b c / (e1 a b c * e2 a b c - e3 a b c)
      = 2 * e1 a b c * e2 a b c / (e1 a b c * e2 a b c - e3 a b c) := by
  field_simp
  ring

/-! ## Instantiation at the scene -/

theorem scene_e : e1 9 11 13 = 33 ∧ e2 9 11 13 = 359 ∧ e3 9 11 13 = 1287 := by
  refine ⟨by norm_num [e1], by norm_num [e2], by norm_num [e3]⟩

theorem scene_degree_product : (33 - 9) * (33 - 11) * (33 - 13) = 33 * 359 - 1287 := by norm_num

/-- The pairwise degree products of the source row are exactly `deg·deg`. -/
theorem degree_pairs :
    24 * 22 = 528 ∧ 22 * 20 = 440 ∧ 24 * 20 = 480 ∧ 24 * 22 * 20 = 10560 := by
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num⟩

/-- `det S = 2e₃ / (N e₂ − e₃) = 2574/10560 = 39/160`, the source row's value. -/
theorem scene_detS : (2 * 1287 : ℚ) / 10560 = 39 / 160 := by norm_num

/-- The active product at the scene: `2 · 33 · 359 / 10560 = 359/160`. -/
theorem scene_active_product : (2 * 33 * 359 : ℚ) / 10560 = 359 / 160 := by norm_num

/-- **Assembled.** One identity ties the degree normalisation to `e₂, e₃`; the transport cubic is
`λ³ − e₂λ − 2e₃`; the active product is `2Ne₂/(Ne₂ − e₃)`; all three agree at `(9,11,13)`. -/
theorem one_calculus :
    ((33 : ℚ) - 9) * (33 - 11) * (33 - 13) = 33 * 359 - 1287 ∧
    (24 * 22 * 20 = 10560) ∧
    ((2 * 1287 : ℚ) / 10560 = 39 / 160) ∧
    ((2 * 33 * 359 : ℚ) / 10560 = 359 / 160) := by
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num⟩

end D0.Synthesis.SymmetricFunctionCalculus
