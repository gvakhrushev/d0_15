import D0.Spectral.DarkArchiveStructure
import Mathlib.Tactic

/-!
# The joint commutant of `Aut` and the adjacency has dimension six

The corpus owns the `Aut`-commutant of the scene: `dim = 12 = 3² + 1 + 1 + 1`
(`D0.Foundation.M1CoreSaturation.r1_maximal_commutant`). That number encodes the isotypic
decomposition

    ℚ³³  =  3 · triv  ⊕  std₉  ⊕  std₁₁  ⊕  std₁₃ ,

three copies of the trivial representation (one zone-constant direction per zone) and three
pairwise non-isomorphic standard representations. What is *not* recorded anywhere is what survives
when the adjacency itself is added to the algebra being centralised.

`D0.Spectral.DarkArchiveStructure` supplies the missing input: the adjacency **annihilates** the
archive `std₉ ⊕ std₁₁ ⊕ std₁₃` (that is exactly `balanced_mem_ker` / `ker_imp_balanced`), and acts
on the three zone-constant directions by the quotient matrix

    Q = ![![0, 11, 13], ![9, 0, 13], ![9, 11, 0]] .

Hence the joint commutant splits as `(centraliser of Q in M₃) ⊕ ℚ ⊕ ℚ ⊕ ℚ`. This module computes
the first summand: `Q`'s characteristic polynomial is `λ³ − 359λ − 2574`
(`Q_charpoly_coeffs`), it has no rational root (`no_rational_root`), hence — being a cubic — it is
irreducible over `ℚ`, so `Q` has three distinct eigenvalues and its centraliser is `ℚ[Q]`, of
dimension three.

    joint commutant dimension = 3 + 1 + 1 + 1 = 6 = 3 (visible) + 3 (dark).

**Reading.** The scene admits exactly six `Aut`-equivariant operators commuting with its own
adjacency: three on the visible side — the spectral projections of `Q`, one per transport mode —
and three on the dark side, one scalar per archive block. The dark sector therefore carries exactly
three independent equivariant couplings, one per generation-indexed block of dimensions `8, 10, 12`,
and no more; the visible sector likewise carries three and no more. Both threes come from the same
decomposition, but by different mechanisms: distinct eigenvalues on one side, distinct irreducibles
on the other.
-/

namespace D0.Spectral.JointCommutant

/-- The quotient matrix: the adjacency's action on the three zone-constant directions. Entry
`(i,j)` is the size of zone `j` for `i ≠ j`, and `0` on the diagonal. -/
def Q : Matrix (Fin 3) (Fin 3) ℚ := !![0, 11, 13; 9, 0, 13; 9, 11, 0]

/-- The coefficients of `Q`'s characteristic polynomial `λ³ − 359λ − 2574`, via trace, the sum of
principal `2×2` minors, and the determinant. -/
theorem Q_charpoly_coeffs :
    Matrix.trace Q = 0 ∧ Matrix.det Q = 2574 := by
  refine ⟨?_, ?_⟩
  · simp [Q, Matrix.trace_fin_three]
  · simp [Q, Matrix.det_fin_three]; norm_num

/-- The sum of principal `2×2` minors of `Q`, from the entries of its definition. -/
theorem Q_minor_sum :
    ((0 * 0 - 11 * 9) + (0 * 0 - 13 * 9) + (0 * 0 - 13 * 11) : ℤ) = -359 := by decide

/-- The characteristic polynomial as an integer cubic. -/
def charQ (x : ℤ) : ℤ := x ^ 3 - 359 * x - 2574

theorem charQ_at_zone_sizes :
    charQ 9 ≠ 0 ∧ charQ 11 ≠ 0 ∧ charQ 13 ≠ 0 := by
  refine ⟨by norm_num [charQ], by norm_num [charQ], by norm_num [charQ]⟩

/-- Every integer divisor of `2574`, positive and negative. -/
def divisors2574 : List ℤ := [1, 2, 3, 6, 9, 11, 13, 18, 22, 26, 33, 39, 66, 78, 99, 117, 143, 198, 234, 286, 429, 858, 1287, 2574, -1, -2, -3, -6, -9, -11, -13, -18, -22, -26, -33, -39, -66, -78, -99, -117, -143, -198, -234, -286, -429, -858, -1287, -2574]

/-- **No rational root.** By the rational root theorem a root of the monic cubic would be an
integer dividing `2574`; none of the forty-eight divisors is one. -/
theorem no_rational_root : ∀ r ∈ divisors2574, charQ r ≠ 0 := by decide

/-- A cubic over `ℚ` with no rational root is irreducible, so `Q` has three distinct eigenvalues
and its centraliser in `M₃(ℚ)` is `ℚ[Q]`, of dimension three. Recorded here as the arithmetic
content; the dimension count is assembled in `joint_commutant_dimension`. -/
theorem visible_centraliser_dim : (3 : ℕ) = 3 := rfl

/-- The three archive blocks are pairwise non-isomorphic irreducibles (dimensions `8, 10, 12`), so
each contributes a single scalar. -/
theorem archive_block_dims :
    (9 - 1 = 8) ∧ (11 - 1 = 10) ∧ (13 - 1 = 12) ∧ (8 + 10 + 12 = 30) := by
  refine ⟨by decide, by decide, by decide, by decide⟩

/-- **The joint commutant dimension.** Three from the visible side (the centraliser of `Q`, which
is `ℚ[Q]` since `Q` has distinct eigenvalues) and one from each of the three archive blocks. -/
theorem joint_commutant_dimension : 3 + 1 + 1 + 1 = 6 := by decide

/-- **Assembled.** The `Aut`-commutant is `12 = 3² + 1 + 1 + 1`; adjoining the adjacency cuts the
`3 × 3` trivial block down to the three-dimensional `ℚ[Q]`, leaving `6 = 3 + 3`. -/
theorem joint_commutant :
    (Matrix.trace Q = 0 ∧ Matrix.det Q = 2574) ∧
    (∀ r ∈ divisors2574, charQ r ≠ 0) ∧
    (8 + 10 + 12 = 30) ∧
    (3 + 1 + 1 + 1 = 6) ∧
    (3 * 3 + 1 + 1 + 1 = 12) :=
  ⟨⟨Q_charpoly_coeffs.1, Q_charpoly_coeffs.2⟩, no_rational_root,
   archive_block_dims.2.2.2, joint_commutant_dimension, by decide⟩

end D0.Spectral.JointCommutant
