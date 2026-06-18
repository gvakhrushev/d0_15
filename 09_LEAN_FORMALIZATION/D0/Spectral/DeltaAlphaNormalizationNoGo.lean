import D0.Spectral.DeltaAlphaExact
import Mathlib.Tactic

/-!
# D0-ALPHA-RESIDUE-DELTA-NORMALIZATION-NOGO-001 — the finite W_eff residue does NOT fix the
`Δ_α` normalization (anti-numerology no-go)

Python certificate: `05_CERTS/vp_alpha_residue_delta_normalization_nogo.py`.

## What is already CLOSED

The finite Feshbach–Schur residue is the depth-2 moment `μ₂·u² + μ₁·u = α_alg⁻¹` exactly in `ℚ(φ)`
(`D0-DELTA-ALPHA-MOMENT-001`, `D0-ALPHA-FESHBACH-RESIDUE-FINITE-SUM-001`):

    α_alg⁻¹ = 159739/5 − (294902/15)·φ      i.e. coordinates (159739/5, −294902/15) in `a + b·φ`.

The gluing anomaly is the EXACT difference of TWO independently-canonized `ℚ(φ)` elements
(`D0-DELTA-ALPHA-EXACT-001`):

    Δ_α = α_top⁻¹ − α_alg⁻¹ ,   α_top⁻¹ = 726 − 364·φ = (726, −364),
                                 Δ_α     = −156109/5 + (289442/15)·φ = (−156109/5, 289442/15).

## The finite obstruction this module formalizes (the NO-GO)

`Δ_α` is computed as `α_top⁻¹ − (the finite residue)`. The finite residue supplies ONE summand
(`α_alg⁻¹`). `α_top⁻¹ = 726 − 364·φ` is a SEPARATE canonization (the topological channel count),
NOT an output of the finite residue functional. The substantive content here is the **non-injectivity
obstruction**: the map

    Δ : (top : ℚ(φ)) ↦ top − α_alg⁻¹

is INJECTIVE in its `top` argument (`Δ top = Δ top' ↔ top = top'`), so a *single* fixed residue value
`α_alg⁻¹` does NOT determine `Δ_α`: distinct second-canonization inputs `top ≠ top'` yield distinct
`Δ_α` values while the residue is held fixed. Concretely we exhibit a planted SECOND canonization
`α_top⁻¹ + (1,0)` whose anomaly differs from the true one — proving the residue alone cannot pin the
normalization. Fixing `Δ_α` therefore requires the external second input (the profinite Dixmier `2¹¹`
active–archive pairing), which stays the owner edge `D0-DIXMIER-RESIDUE-OWNER-001`.

HONESTY BOUNDARY. CLOSED here (finite, decidable): (i) the residue/`α_alg⁻¹` value, (ii) the true
`Δ_α` value, (iii) the under-determination — `Δ` is a non-constant injective function of `top`, so the
residue alone has positive-dimensional fibre of compatible `Δ_α`. NOT closed: which `top` is the
correct canonization, i.e. the residue→`Δ_α` normalization equality, which is the external Dixmier
`2¹¹` pairing (`D0-DIXMIER-RESIDUE-OWNER-001`, `ASSUMP-DIXMIER-TRACE`). This is an anti-numerology
guard: it PREVENTS re-declaring Dixmier closed from the finite sum.
-/

namespace D0.Spectral

open D0

/-- An element of `ℚ(φ)` in the `a + b·φ` basis, with exact rational coordinates. Coordinate
equality is decidable, but kernel `decide` stalls on `ℚ`-division; the finite obstruction is settled
componentwise with `norm_num`. -/
@[ext]
structure QPhi where
  a : ℚ
  b : ℚ
deriving DecidableEq, Repr

namespace QPhi

/-- Subtraction is coordinatewise (the `φ`-basis is a free `ℚ`-module of rank 2). -/
def sub (x y : QPhi) : QPhi := ⟨x.a - y.a, x.b - y.b⟩

/-- The realification `a + b·φ ∈ ℝ`. -/
noncomputable def toReal (x : QPhi) : ℝ := (x.a : ℝ) + (x.b : ℝ) * phi

end QPhi

/-- `α_alg⁻¹ = 159739/5 − (294902/15)·φ` — the FINITE W_eff residue value, in coordinates. -/
def alphaAlgInvCoord : QPhi := ⟨159739 / 5, -294902 / 15⟩

/-- `α_top⁻¹ = 726 − 364·φ` — the SECOND (topological channel-count) canonization, in coordinates. -/
def alphaTopInvCoord : QPhi := ⟨726, -364⟩

/-- `Δ_α = −156109/5 + (289442/15)·φ` — the true gluing anomaly, in coordinates. -/
def deltaAlphaCoord : QPhi := ⟨-156109 / 5, 289442 / 15⟩

/-- The anomaly as a FUNCTION of the second canonization `top`, holding the finite residue
(`= α_alg⁻¹`) FIXED: `Δ(top) = top − α_alg⁻¹`. -/
def deltaOfCanon (top : QPhi) : QPhi := QPhi.sub top alphaAlgInvCoord

/-- **Residue value (re-anchor).** The finite residue coordinate equals the moment value
`α_alg⁻¹ = (159739/5, −294902/15)` (consistency with `D0-DELTA-ALPHA-MOMENT-001`). -/
theorem residue_coord_eq : alphaAlgInvCoord = QPhi.mk (159739 / 5) (-294902 / 15) := rfl

/-- **The true anomaly is recovered ONLY with the second canonization.** With `top = α_top⁻¹`
supplied, `Δ(α_top⁻¹) = Δ_α = (−156109/5, 289442/15)`. -/
theorem delta_at_true_canon : deltaOfCanon alphaTopInvCoord = deltaAlphaCoord := by
  apply QPhi.ext
  · simp only [deltaOfCanon, QPhi.sub, alphaTopInvCoord, alphaAlgInvCoord, deltaAlphaCoord]
    norm_num
  · simp only [deltaOfCanon, QPhi.sub, alphaTopInvCoord, alphaAlgInvCoord, deltaAlphaCoord]
    norm_num

/-- **THE NO-GO (under-determination).** A SECOND, planted canonization differing from `α_top⁻¹`
by `+1` in the rational part leaves the finite residue `α_alg⁻¹` untouched yet produces a DIFFERENT
anomaly. Hence the single finite residue value does NOT determine `Δ_α`: the residue alone is
compatible with more than one `Δ_α`. -/
theorem delta_normalization_underdetermined :
    deltaOfCanon ⟨727, -364⟩ ≠ deltaAlphaCoord := by
  intro h
  have ha : (727 : ℚ) - (159739 / 5) = -156109 / 5 := by
    have := congrArg QPhi.a h
    simpa [deltaOfCanon, QPhi.sub, alphaAlgInvCoord, deltaAlphaCoord] using this
  norm_num at ha

/-- **The map `top ↦ Δ(top)` is injective** (it is the bijection `top ↦ top − α_alg⁻¹`): the
anomaly is a faithful function of the SECOND canonization. Equivalently, distinct canonizations give
distinct anomalies — so `Δ_α` carries strictly more information than the fixed residue value, and
cannot be a function of the residue alone. -/
theorem deltaOfCanon_injective : Function.Injective deltaOfCanon := by
  intro x y h
  have ha : x.a = y.a := by
    have := congrArg QPhi.a h
    simpa [deltaOfCanon, QPhi.sub] using sub_left_injective this
  have hb : x.b = y.b := by
    have := congrArg QPhi.b h
    simpa [deltaOfCanon, QPhi.sub] using sub_left_injective this
  cases x; cases y; simp_all

/-- **The fibre is nontrivial: two distinct `top` inputs, same fixed residue, different `Δ_α`.**
This is the clean finite obstruction: `α_top⁻¹ ≠ α_top⁻¹ + (1,0)` (two admissible second
canonizations) while `α_alg⁻¹` (the finite residue) is identical for both, and their anomalies
differ. So fixing the residue does NOT fix the normalization. -/
theorem two_canons_same_residue_diff_delta :
    (alphaTopInvCoord ≠ (⟨727, -364⟩ : QPhi))
      ∧ deltaOfCanon alphaTopInvCoord ≠ deltaOfCanon ⟨727, -364⟩ := by
  refine ⟨?_, ?_⟩
  · intro h
    have : (726 : ℚ) = 727 := congrArg QPhi.a h
    norm_num at this
  · rw [delta_at_true_canon]
    exact fun h => delta_normalization_underdetermined h.symm

/-- **Realification agrees with `D0-DELTA-ALPHA-EXACT-001`.** The coordinate anomaly maps to the
real value `−156109/5 + (289442/15)·φ` proved in `delta_alpha_exact`, so this no-go sits over the
genuine seam (not a re-coordinatization). -/
theorem deltaAlphaCoord_toReal :
    deltaAlphaCoord.toReal = -156109 / 5 + 289442 / 15 * phi := by
  unfold QPhi.toReal deltaAlphaCoord
  push_cast
  ring

/-- **D0-ALPHA-RESIDUE-DELTA-NORMALIZATION-NOGO-001 (finite NO-GO).** The finite W_eff residue fixes
`α_alg⁻¹` exactly, and the true anomaly `Δ_α = α_top⁻¹ − α_alg⁻¹` is recovered ONLY when the SECOND
canonization `α_top⁻¹` is supplied. But the residue value alone is compatible with distinct second
canonizations giving distinct anomalies (`deltaOfCanon` is injective and non-constant), so the single
finite residue does NOT determine the `Δ_α` normalization. That second input is the external profinite
Dixmier `2¹¹` pairing (`D0-DIXMIER-RESIDUE-OWNER-001`), which stays the owner edge. -/
theorem alpha_residue_delta_normalization_nogo :
    (alphaAlgInvCoord = QPhi.mk (159739 / 5) (-294902 / 15))
      ∧ (deltaOfCanon alphaTopInvCoord = deltaAlphaCoord)
      ∧ (deltaOfCanon ⟨727, -364⟩ ≠ deltaAlphaCoord)
      ∧ Function.Injective deltaOfCanon :=
  ⟨residue_coord_eq, delta_at_true_canon, delta_normalization_underdetermined,
    deltaOfCanon_injective⟩

end D0.Spectral
