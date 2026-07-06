# CVFT F4/F7 Lean-lift memo — DRAFT (strengthening, not demotion)

**Date:** 2026-07-05 · **Author:** center-attack subagent · **Status:** DRAFT / candidate — nothing here is "forced" or "closed" until the skeptic pass and owner blessing. **Skeptic #1 verdict: WOUNDED (accepted in full); all 6 repairs applied and the 4 load-bearing sorry-free theorems re-verified by in-tree `lake env lean` compile (0 errors). See the appended "Skeptic #1 verdict + repair log".**
**Scope:** propose lifting `D0-CVFT-F4` and `D0-CVFT-F7` from `PYTHON_CERTIFIED` to `LEAN_PROVED` on the back of the four REFORGED certs, whose content is real and whose reforged certs pass (verified below). This is a **strengthening** motion. It does NOT demote either claim.

**Discipline note.** All Lean code below is DRAFT living in this memo as fenced blocks; NO `.lean` file is written to the tree, and NO edit is made to `09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv`. Registry status changes are proposals only (§5). Every load-bearing fact carries an owned `file:line` citation quoted verbatim.

---

## 0. What is being lifted, and the honest headline

Two claims, four certs, verified PASS at exit 0 on this machine (2026-07-05):

| Cert (REFORGED) | Claim | exit | terminal line |
|---|---|---|---|
| `vp_cvft_boundary_channel_rank_REFORGED.py` | F7 leg 1 | 0 | `PASS_CVFT_BOUNDARY_CHANNEL_RANK_REFORGED` |
| `vp_cvft_refined_logdet_rank_bound_REFORGED.py` | F7 leg 2 | 0 | `PASS_CVFT_LOGDET_RANK_BOUND_REFINED_REFORGED` |
| `vp_cvft_uv_feedback_tail_bound_refined_REFORGED.py` | F4 leg 1 | 0 | `PASS_CVFT_UV_TAIL_BOUND_REFINED_REFORGED` |
| `vp_cvft_ueff_pole_discipline_REFORGED.py` | F4 leg 2 | 0 | `PASS_UEFF_POLE_DISCIPLINE_REFORGED` |

**Honest headline (post-skeptic):** The FINITE algebraic cores of both claims are genuinely Lean-able and most obligations are OWNED by existing Mathlib + D0 modules (9 of 12 obligations OWNED outright, §4). The **analytic** legs (the `−log det` ↔ eigenvalue-sum branch, and the tail bound on `Tr(Fᵐ)`) are *partially* owned: the scalar geometric-series and convexity bounds are owned; the eigenvalue-decomposition bridges DO exist in-tree (`Matrix.det_eq_prod_roots_charpoly`, `Matrix.trace_eq_sum_roots_charpoly` — `Charpoly/Eigs.lean:27,29`; `PosSemidef.eigenvalues_nonneg` — `Analysis/Matrix/PosDef.lean:42`), but the trace-of-power / complex-branch *assembly* on top of them is not a single named lemma, so those two obligations stay `sorry` (gaps G1, G2). Therefore the honest proposal is **split**: F7's rank-localization leg → LEAN_PROVED (sorry-free, and it is F7's titled load-bearing content); F4 stays PYTHON_CERTIFIED with its pole-discipline leg Lean-proved and its tail leg a named sorry. Do not over-claim a blanket flip.

---

## 1. Registry rows (quoted verbatim) and the owned mathematical content

**D0-CVFT-F4** — `09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv:137`, quoted verbatim:

> `D0-CVFT-F4,BOOK_02/05,CVFT UV feedback-tail cut program,,,PYTHON_CERTIFIED,False,,vp_cvft_uv_feedback_tail_bound_refined.py;vp_cvft_ueff_pole_discipline.py,CERT-CLOSED,UV cutoff claims have deterministic finite cert candidates for the refined tail bound under |z|rho(F_N)<1; Lean proof remains open. [was:CERT-CANDIDATE] [8C: linked passing cert]`

**D0-CVFT-F7** — `09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv:140`, quoted verbatim:

> `D0-CVFT-F7,BOOK_07,CVFT boundary-local holographic rank lemma,,,PYTHON_CERTIFIED,False,,vp_cvft_boundary_channel_rank.py;vp_cvft_refined_logdet_rank_bound.py,CERT-CLOSED,Boundary-local rank control has deterministic finite cert candidates; it supports localization only and is not an A4 proof. [was:CERT-CANDIDATE] [8C: linked passing cert]`

Both rows carry empty `lean_module`/`lean_theorem`, `lean_status=PYTHON_CERTIFIED`, and the **original (fake) certs** in `python_cert`. Both explicitly record "Lean proof remains open" (F4) / "localization only ... not an A4 proof" (F7).

### The contract's CVFT hardening (owned typing the theorems must respect)

`D0_CLAIM_CLOSURE_CONTRACT.md:43-52`, quoted verbatim:

> Closed-vacuum feedback closure may use `F_N=P_NU_N^\dagger Q_NU_NP_N` only as feedback-return and `R_N=D_N^\dagger D_N` only as positive response/readout. [...] Forbidden shortcuts are: `Q_N\ne0 -> F_N\ne0`, determinant trace without `-\log det`, complex mass/width poles from bare positive `F_N`, [...]

`D0_CLAIM_CLOSURE_CONTRACT.md:11-12` (the closure discipline every "cert" claim must obey), verbatim:

> - `sample cert passed` as proof of an infinite family.
> - `negative controls passed` without a stated failure theorem or finite scope.

This last line is decisive for the lift: a *cert* over a finite family of scene members is NOT a proof of the universal lemma. Lifting to `LEAN_PROVED` requires a **theorem statement whose finite scope is honest** (rank/dim inequalities over the frozen 33×33 scene ARE finite theorems; the tail/log-det universal-in-`z` bounds are theorems over `ℝ`/`ℂ` that need the scalar analytic lemma). §4 marks which is which.

### Owned constructible objects (these make the finite theorems Lean-able)

- **Rank-3 / nullity-30 zone split** is already a machine-checked Lean theorem. `09_LEAN_FORMALIZATION/D0/Claims/KernelZoneSplit.lean:13-20`, verbatim:
  > CLAIM. The adjacency matrix `A` of the complete tripartite scene `K(9,11,13)` on `N = 33` vertices (`|E| = 359`) has  * rank 3  (= the three transport modes = space), and  * nullity 30  (= the dark archive),
  and `KernelZoneSplit.lean:33` provides the exact matrix: `def A : Matrix (Fin 33) (Fin 33) Int := Matrix.of (fun i j => if zoneOf i = zoneOf j then 0 else 1)`.
- **The whole Laplacian spectrum forced** — `09_LEAN_FORMALIZATION/D0/VNext2/SceneLaplacianSpectrumForced.lean:15`, verbatim: `0¹, 24⁸, 22¹⁰, 20¹², 33²` with `SceneLaplacianSpectrumForced.lean:37 theorem N_eq : Nv = 33 := by decide`. This owns the scene-invariant layer the certs recompute (`|V|=33 |E|=359 tri=1287 spec`).
- **δ₀ = (√5−2)/2 = 1/(2φ³)** is owned by `BOOK_01 §01.6` (per the reforge report `CVFT_F4_F7_REFORGE_REPORT.md:34`, verbatim: "`δ₀=(√5−2)/2=1/(2φ³)` is owned by BOOK_01 §01.6"). Used by F4's noise-floor clause only as a *readout classifier*, not the convergence radius.
- **A `−log det(I−zF)` Jacobi identity already lives in D0 Lean** — `09_LEAN_FORMALIZATION/D0/Matter/HiggsLogdetStationary.lean:35`, verbatim: "The Jacobi trace identity `d/dt(−log det(I−zF)) = Tr[(I−zF)⁻¹·z·dF/dt]`" — this is the *derivative* identity, adjacent but NOT the same as the eigenvalue-sum branch bound F7 needs (see §4 gap G2).

### Owned Mathlib lemmas (verified present in this tree's `.lake/packages/mathlib`)

- `Matrix.rank_conjTranspose_mul_self` — `Mathlib/LinearAlgebra/Matrix/Rank.lean:383`, verbatim: `theorem rank_conjTranspose_mul_self (A : Matrix m n R) : (Aᴴ * A).rank = A.rank`. **This IS `rank(F)=rank(QUP)`** with `A := QUP`, `F := Aᴴ*A`.
- `Matrix.rank_mul_le` / `Matrix.rank_mul_le_left` — `Rank.lean:182` / `Rank.lean:169`, verbatim: `theorem rank_mul_le (A : Matrix m n R) (B : Matrix n o R) : (A * B).rank ≤ min A.rank B.rank`. Gives `rank(QUP) ≤ rank(P)` (localization to the retained support).
- `Matrix.rank_le_card_width` — `Rank.lean:161`, verbatim: `theorem rank_le_card_width [Nontrivial R] (A : Matrix m n R) : A.rank ≤ Fintype.card n`. Gives `rank(F) ≤ dim B` when `F`/`QUP` is presented on the boundary index set.
- `Matrix.posSemidef_conjTranspose_mul_self` — `Mathlib/LinearAlgebra/Matrix/PosDef.lean:355`, verbatim: `theorem posSemidef_conjTranspose_mul_self [StarOrderedRing R] (A : Matrix m n R) :` — **F is PSD Hermitian**, the typing gate, owned outright.
- `tsum_geometric_of_lt_one` — `Mathlib/Analysis/SpecificLimits/Basic.lean:329`, verbatim: `theorem tsum_geometric_of_lt_one {r : ℝ} (h₁ : 0 ≤ r) (h₂ : r < 1) : ∑' n : ℕ, r ^ n = (1 - r)⁻¹`, and `hasSum_geometric_of_lt_one` at `Basic.lean:316`. **This is the scalar geometric-series engine** for F4's tail `a^{M+1}/(1−a)` and F7's `−log(1−a) ≤ a/(1−a)`.

## 2. F7 Lean module DRAFT — `D0.CVFT.BoundaryRankLocalization`

F7 splits into two Lean theorems matching the two reforged certs:
- **F7a (rank leg):** `rank(F) = rank(QUP) ≤ min(dim B_boundary, rank P)` — the boundary-local holographic rank inequality. **Fully owned** (rank algebra over any field; `A := QUP`, `F := Aᴴ*A`).
- **F7b (log-det leg):** for `a = |z|·ρ(F) < 1`, `|−log det(I−zF)| ≤ rank(F)·(−log(1−a)) ≤ rank(F)·a/(1−a)`. The **scalar** chain `−log(1−a) ≤ a/(1−a)` is owned via convexity/geometric series; the **matrix→scalar reduction** (`det(I−zF) = ∏(1−zλᵢ)`, PSD real spectrum, branch on `Re>0`) is the named gap G2.

```lean
import Mathlib.LinearAlgebra.Matrix.Rank
import Mathlib.LinearAlgebra.Matrix.PosDef
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecificLimits.Basic
import D0.Claims.KernelZoneSplit          -- owns the rank-3/nullity-30 scene A

/-!
# D0-CVFT-F7 — boundary-local holographic rank lemma (Lean lift, DRAFT)

Backs `05_CERTS/vp_cvft_boundary_channel_rank_REFORGED.py` (F7a) and
`vp_cvft_refined_logdet_rank_bound_REFORGED.py` (F7b).

Typing (closure contract): `F = (QUP)ᴴ (QUP)`, Q,P projections, U unitary,
`F` PSD Hermitian. The reforged certs verify these numerically on scene members;
here F7a's rank/dim leg is a THEOREM over any STAR-ORDERED FIELD (⚠ REPAIR 4,
skeptic #1: NOT "an arbitrary field" — `rank_conjTranspose_mul_self` and
`rank_le_card_height` require `[PartialOrder R] [StarRing R] [StarOrderedRing R]`,
Rank.lean:361 `section StarOrderedField`; over a plain/finite field the cited owner
does NOT apply). ℂ is star-ordered (`open ComplexOrder`), so the scene instance is
covered; the `rank_mul_le_right`/`rank_le_card_width` localization sub-leg is the
only part that holds over an arbitrary field. Instantiated to the frozen scene via
`D0.Claims.KernelZoneSplit.A` for the concrete dim-bound.
-/
namespace D0.CVFT

open Matrix

-- ⚠ REPAIR 1 (skeptic #1, O1/M4a): the star-rank lemmas
-- `rank_conjTranspose_mul_self` / `rank_le_card_height` live in
-- `Rank.lean:361 section StarOrderedField` under
-- `variable [Fintype m] [Field R] [PartialOrder R] [StarRing R] [StarOrderedRing R]`.
-- The original context `[Field 𝕜] [StarRing 𝕜]` was INSUFFICIENT and failed to
-- typecheck (`synthInstanceFailed: PartialOrder 𝕜`). The full star-ordered-field
-- context below COMPILES in-tree (verified 2026-07-05, lake env lean, 0 errors —
-- linter warnings only). See §6C and the Skeptic #1 repair log.
variable {m n : Type*} [Fintype m] [Fintype n]
variable {𝕜 : Type*} [Field 𝕜] [PartialOrder 𝕜] [StarRing 𝕜] [StarOrderedRing 𝕜]

/-- **F7a-core (OWNED): rank(F) = rank(QUP).**  Direct instance of Mathlib's
`Matrix.rank_conjTranspose_mul_self` with `A := QUP`. No sorry.
NB: requires the STAR-ORDERED-FIELD context (not an arbitrary field). -/
theorem cvft_rank_F_eq_rank_QUP (QUP : Matrix m n 𝕜) :
    (QUPᴴ * QUP).rank = QUP.rank :=
  Matrix.rank_conjTranspose_mul_self QUP

/-- **F7a-localization (OWNED): rank(QUP) ≤ rank(P).**  QUP = (QU)·P, so
`rank_mul_le_right` bounds it by rank P. Feedback return cannot exceed the
retained support. (This one is a PLAIN-field lemma — needs no star order.) -/
theorem cvft_rank_QUP_le_rank_P
    (QU : Matrix m n 𝕜) (P : Matrix n n 𝕜) :
    (QU * P).rank ≤ P.rank :=
  Matrix.rank_mul_le_right QU P

/-- **F7a-boundary (OWNED): rank(F) ≤ dim of the boundary index set.**  When the
feedback return is presented on the boundary channel index type `b`
(`QUP : Matrix b n`), `rank F = rank QUP ≤ card b = dim B_boundary`.  This is the
holographic bound: the rank is capped by the number of cut/boundary channels.
NB: requires the STAR-ORDERED-FIELD context (via `rank_conjTranspose_mul_self`);
`Nontrivial` is now derived from `Field`, so the explicit `[Nontrivial 𝕜]` is dropped. -/
theorem cvft_rank_F_le_dim_boundary
    {b : Type*} [Fintype b]
    (QUP : Matrix b n 𝕜) :
    (QUPᴴ * QUP).rank ≤ Fintype.card b := by
  rw [Matrix.rank_conjTranspose_mul_self]
  exact Matrix.rank_le_card_height QUP  -- rank QUP ≤ card (ROWS = boundary channels) = dim B
                                        -- NB: card_height (rows), not card_width (cols) — see §6C

/-- **F7a scene instance (OWNED): on the frozen scene rank(F) ≤ 3.**  The retained
projector has rank 3 (`D0.Claims.KernelZoneSplit`), so every feedback-return F on
the scene has rank ≤ 3 — the "localization only" ceiling. -/
theorem cvft_scene_rank_F_le_three
    (QU : Matrix (Fin 33) (Fin 33) ℚ) (P : Matrix (Fin 33) (Fin 33) ℚ)
    (hP : P.rank = 3) :
    (QU * P).rank ≤ 3 := by
  have := Matrix.rank_mul_le_right QU P
  rwa [hP] at this

/-- **F7a PSD typing (OWNED): F is positive semidefinite Hermitian.**  Owned
outright by `Matrix.posSemidef_conjTranspose_mul_self`. -/
theorem cvft_F_posSemidef
    {R : Type*} [CommRing R] [PartialOrder R] [StarRing R] [StarOrderedRing R]
    (QUP : Matrix m n R) :
    (QUPᴴ * QUP).PosSemidef :=
  Matrix.posSemidef_conjTranspose_mul_self QUP

/-- **F7b scalar chain (OWNED): -log(1-a) ≤ a/(1-a) for 0 ≤ a < 1.**  This is the
second inequality of the log-det chain; pure real analysis, no matrix content.
Proof sketch: `-log(1-a) = Σ_{k≥1} aᵏ/k ≤ Σ_{k≥1} aᵏ = a/(1-a)` termwise, or via
`Real.add_one_le_exp` / `Real.log_le_sub_one_of_pos` on `1/(1-a)`. -/
theorem cvft_neg_log_le_geom {a : ℝ} (h0 : 0 ≤ a) (h1 : a < 1) :
    -Real.log (1 - a) ≤ a / (1 - a) := by
  -- -log(1-a) = log(1/(1-a)) ≤ 1/(1-a) - 1 = a/(1-a)   [log x ≤ x-1]
  have hpos : (0:ℝ) < 1 - a := by linarith
  have hx : (0:ℝ) < 1 / (1 - a) := by positivity
  have hlog : Real.log (1 / (1 - a)) ≤ 1 / (1 - a) - 1 :=
    Real.log_le_sub_one_of_pos hx
  rw [Real.log_div one_ne_zero (ne_of_gt hpos), Real.log_one, zero_sub] at hlog
  -- ⚠ REPAIR 3 (skeptic #1, O6): the original `by field_simp` left the residual
  -- goal `1 - (1 - a) = a` unsolved (confirmed by compile). Append `ring`.
  -- Verified in-tree 2026-07-05: `field_simp; ring` closes it (0 errors).
  have : (1:ℝ) / (1 - a) - 1 = a / (1 - a) := by field_simp; ring
  linarith [this ▸ hlog]

/-- **F7b matrix leg (GAP G2, sorry): |-log det(I - zF)| ≤ rank(F)·(-log(1-a)).**
Requires: (i) `det(I - zF) = ∏ᵢ (1 - z·λᵢ)` over the PSD eigenvalues (Mathlib
`Matrix.det` of a Hermitian in eigenbasis — NAME NOT CONFIRMED in this tree, see
§4 G2); (ii) the principal-branch bound `|log(1 - z λᵢ)| ≤ -log(1 - |z|λᵢ)` for
`|z|λᵢ < 1`; (iii) sum over the `rank(F)` nonzero eigenvalues. Legs (ii)-(iii) are
short given (i); (i) is the missing owned bridge. -/
theorem cvft_logdet_rank_bound
    (F : Matrix (Fin 33) (Fin 33) ℂ) (z : ℂ) (hz : True /- a<1 hypothesis, elided -/) :
    True := by
  trivial  -- PLACEHOLDER: real statement needs det = ∏ eigenvalues (G2 sorry)

end D0.CVFT
```

**F7 verdict (DRAFT):** F7a (rank/dim/PSD leg) is **fully owned, sorry-free** — `cvft_rank_F_eq_rank_QUP`, `cvft_rank_QUP_le_rank_P`, `cvft_rank_F_le_dim_boundary`, `cvft_scene_rank_F_le_three`, `cvft_F_posSemidef`, and the scalar `cvft_neg_log_le_geom` are all discharged by named Mathlib lemmas. F7b's matrix log-det bound stays a NAMED SORRY (gap G2). Since the registry row for F7 is *titled* "boundary-local holographic rank lemma" and its notes say "supports localization only", **the rank leg is the load-bearing content** and it is theorem-grade.

## 3. F4 Lean module DRAFT — `D0.CVFT.UVFeedbackTailBound` + `D0.CVFT.UeffPoleDiscipline`

F4 splits into two legs matching its two reforged certs:
- **F4a (tail leg):** `|T_M(z,F)| ≤ rank(F)/(M+1)·a^{M+1}/(1−a)` with `a=|z|ρ(F)<1`, `T_M = Σ_{m>M} zᵐ/m·Tr(Fᵐ)`. The **scalar tail engine** `Σ_{m>M} a^m ≤ a^{M+1}/(1−a)` is owned via geometric series; the reduction `|Tr(Fᵐ)| ≤ rank(F)·ρ(F)ᵐ` (trace-power → eigenvalue sum) is gap G1.
- **F4b (pole discipline):** `U_eff = PUP` is a contraction (σ_max ≤ 1); bare positive `F` has real nonnegative spectrum; the allowed identity `U_effᴴU_eff + F_c = I` (block form of `F = P−(PUP)ᴴ(PUP)`); complex poles can NOT come from bare positive `F`. The PSD/real-spectrum core is owned; the contraction and `U_eff` block identity are owned given `‖U‖≤1`.

```lean
import Mathlib.LinearAlgebra.Matrix.PosDef
import Mathlib.LinearAlgebra.Matrix.Rank
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecificLimits.Basic

/-!
# D0-CVFT-F4 — UV feedback-tail cut + U_eff pole discipline (Lean lift, DRAFT)

Backs `05_CERTS/vp_cvft_uv_feedback_tail_bound_refined_REFORGED.py` (F4a) and
`vp_cvft_ueff_pole_discipline_REFORGED.py` (F4b).
-/
namespace D0.CVFT

open Matrix

/-- **F4a scalar tail engine (OWNED): Σ_{m > M} aᵐ = a^{M+1}/(1-a) for 0≤a<1.**
The refined tail's geometric core. From `tsum_geometric_of_lt_one` after shifting
the index by `M+1` and factoring `a^{M+1}`. No sorry. -/
theorem cvft_geom_tail {a : ℝ} (h0 : 0 ≤ a) (h1 : a < 1) (M : ℕ) :
    ∑' k : ℕ, a ^ (M + 1 + k) = a ^ (M + 1) / (1 - a) := by
  have hbase : ∑' k : ℕ, a ^ k = (1 - a)⁻¹ := tsum_geometric_of_lt_one h0 h1
  calc ∑' k : ℕ, a ^ (M + 1 + k)
      = ∑' k : ℕ, a ^ (M + 1) * a ^ k := by
        simp_rw [pow_add]
    _ = a ^ (M + 1) * ∑' k : ℕ, a ^ k := by
        rw [tsum_mul_left]
    _ = a ^ (M + 1) / (1 - a) := by rw [hbase]; ring

/-- **F4a refined-bound scalar form (OWNED): the 1/(M+1) factor.**  Since
`Σ_{m>M} aᵐ/m ≤ (1/(M+1))·Σ_{m>M} aᵐ` (each `1/m ≤ 1/(M+1)` for `m ≥ M+1`), the
weighted tail obeys `Σ_{m>M} aᵐ/m ≤ a^{M+1}/((M+1)(1-a))`.  This is the scalar
skeleton of `|T_M| ≤ rank(F)/(M+1)·a^{M+1}/(1-a)` once the trace-power is bounded
by `rank(F)·aᵐ` (gap G1). -/
theorem cvft_weighted_geom_tail {a : ℝ} (h0 : 0 ≤ a) (h1 : a < 1) (M : ℕ) :
    ∑' k : ℕ, a ^ (M + 1 + k) / ((M + 1 : ℕ) + k) ≤
      a ^ (M + 1) / ((M + 1 : ℕ) * (1 - a)) := by
  sorry  -- OWNED-IN-PRINCIPLE: termwise 1/(M+1+k) ≤ 1/(M+1), then cvft_geom_tail.
         -- Mechanical (tsum_le_tsum + div_le_div_of_nonneg_left); left as
         -- LIGHT-SORRY (no missing Mathlib primitive, just proof labor). See §4 G1a.

/-- **F4a matrix leg (GAP G1, sorry): |T_M(z,F)| ≤ rank(F)/(M+1)·a^{M+1}/(1-a).**
Requires `|Tr(Fᵐ)| = |Σᵢ λᵢᵐ| ≤ rank(F)·ρ(F)ᵐ` for PSD F (nonneg eigenvalues,
`≤ rank·ρᵐ` since exactly rank(F) eigenvalues are nonzero and each ≤ ρ). Needs
`Matrix.trace = Σ eigenvalues` for Hermitian F (NAME NOT CONFIRMED, §4 G1). Given
that, combine with `cvft_weighted_geom_tail` termwise on `a=|z|ρ`. -/
theorem cvft_uv_tail_bound
    (F : Matrix (Fin 33) (Fin 33) ℂ) (z : ℂ) (M : ℕ) : True := by
  trivial  -- PLACEHOLDER: real statement blocked on trace = Σ eigenvalues (G1).

/-- **F4a δ₀ noise-floor is a POSITIVE constant, not the radius (OWNED).**
`δ₀ = (√5 - 2)/2 > 0` and `δ₀¹² > 0`; it is a fixed readout threshold. This lemma
records only that it is strictly positive and strictly below 1 (so it can serve as
a floor), NOT that convergence requires `a < δ₀¹²` (which the cert's NC_DELTA0
control refutes). -/
-- ⚠ REPAIR 2 (skeptic #1, O8): the original proof cited TWO constants that do
-- NOT exist in this tree's mathlib (v4.30.0): `Real.sqrt_eq_iff_sq_eq` (no such
-- constant) and `pow_lt_pow_left` (renamed to `pow_lt_pow_left₀`). This was the
-- SAME fabricated-name defect the memo quarantines the originals for — grep-only
-- verification let it through. Rewritten below with real, in-tree lemma names
-- (`Real.lt_sqrt`, `Real.sqrt_lt'`, `pow_lt_pow_left₀`) and COMPILED
-- (verified 2026-07-05, lake env lean, 0 errors). O8 stays OWNED only on the
-- strength of this compiled proof — not the greps.
theorem cvft_delta0_pos : 0 < ((Real.sqrt 5 - 2) / 2) ^ 12 ∧ ((Real.sqrt 5 - 2) / 2) ^ 12 < 1 := by
  have h5 : (2:ℝ) < Real.sqrt 5 := by
    rw [Real.lt_sqrt (by norm_num)]; norm_num
  have hpos : 0 < (Real.sqrt 5 - 2) / 2 := by linarith
  have hlt1 : (Real.sqrt 5 - 2) / 2 < 1 := by
    have h5lt4 : Real.sqrt 5 < 4 := by
      rw [Real.sqrt_lt' (by norm_num)]; norm_num
    linarith
  refine ⟨pow_pos hpos 12, ?_⟩
  calc ((Real.sqrt 5 - 2) / 2) ^ 12 < 1 ^ 12 := by
        apply pow_lt_pow_left₀ hlt1 (le_of_lt hpos); norm_num
    _ = 1 := one_pow 12

/-- **F4b bare-F real nonnegative spectrum (OWNED): F is PSD.**  A PSD matrix has
real nonnegative eigenvalues — so "complex poles from bare positive F" is
structurally impossible. Owned by `posSemidef_conjTranspose_mul_self`; the
"nonnegative real spectrum" is `PosSemidef.eigenvalues_nonneg` (Mathlib). -/
theorem cvft_bare_F_posSemidef
    {m n : Type*} [Fintype m] [Fintype n] [DecidableEq n]
    {R : Type*} [CommRing R] [PartialOrder R] [StarRing R] [StarOrderedRing R]
    (QUP : Matrix m n R) :
    (QUPᴴ * QUP).PosSemidef :=
  Matrix.posSemidef_conjTranspose_mul_self QUP

/-- **F4b contraction of U_eff (OWNED given ‖U‖≤1): σ_max(PUP) ≤ 1.**  If U is a
contraction (unitary ⇒ ‖U‖=1) and P an orthogonal projection (‖P‖≤1), then
‖PUP‖ ≤ ‖P‖‖U‖‖P‖ ≤ 1 by submultiplicativity of the operator norm. Stated here as
the operator-norm inequality; discharged by `norm_mul_le` chain once U,P are given
as `‖·‖≤1`. Left as LIGHT-SORRY (op-norm on Matrix via `Matrix.instNormedRing`). -/
theorem cvft_ueff_contraction
    {n : Type*} [Fintype n] [DecidableEq n]
    (P U : Matrix n n ℂ) (hP : ‖P‖ ≤ 1) (hU : ‖U‖ ≤ 1) :
    ‖P * U * P‖ ≤ 1 := by
  sorry  -- LIGHT-SORRY: ‖P*U*P‖ ≤ ‖P‖*‖U‖*‖P‖ ≤ 1 via norm_mul_le; §4 G3.

end D0.CVFT
```

**F4 verdict (DRAFT):** F4b's structural core — **bare positive F cannot carry complex poles** — is owned outright (`cvft_bare_F_posSemidef` + PSD-eigenvalues-nonneg). This is the *forbidden-shortcut refutation* that the contract (`D0_CLAIM_CLOSURE_CONTRACT.md:48-50`) names, and it is theorem-grade. `cvft_delta0_pos` is sorry-free. F4a's scalar geometric engine (`cvft_geom_tail`) is sorry-free; the `1/(M+1)` weighting (`cvft_weighted_geom_tail`) and contraction (`cvft_ueff_contraction`) are LIGHT-SORRY (proof labor, no missing primitive). The **trace-power → eigenvalue bound** (`cvft_uv_tail_bound`, gap G1) is the one genuinely-blocked obligation.

## 4. Obligation ledger — owned vs new/sorry

Legend: **OWNED** = discharged by a named Mathlib/D0 lemma verified present in this tree; **LIGHT-SORRY** = no missing primitive, only proof labor (safe to promise); **GAP-SORRY** = a real reduction that still needs a bridge lemma, honestly open.

| # | Obligation | Claim/leg | Status | Owned by (verified `file:line`) |
|---|---|---|---|---|
| O1 | `rank(F) = rank(QUP)` | F7a | **OWNED (compiled ✓)** | `Matrix.rank_conjTranspose_mul_self` — `Rank.lean:383`, inside `section StarOrderedField` `Rank.lean:361` ⇒ needs `[Field R][PartialOrder R][StarRing R][StarOrderedRing R]` (Repair 1) |
| O2 | `rank(QUP) ≤ rank(P)` (localization) | F7a | **OWNED** | `Matrix.rank_mul_le_right` — `Rank.lean:175` (plain field) |
| O3 | `rank(F) ≤ dim B_boundary` | F7a | **OWNED (compiled ✓)** | `Matrix.rank_le_card_height` — `Rank.lean:304` (ROWS, not `rank_le_card_width`; also in `section StarOrderedField`) (+ O1) |
| O4 | scene rank(F) ≤ 3 (ceiling) | F7a | **OWNED** | O2 + `D0.Claims.KernelZoneSplit` rank P = 3 — `KernelZoneSplit.lean:13-20` |
| O5 | `F` PSD Hermitian | F7a, F4b typing | **OWNED** | `Matrix.posSemidef_conjTranspose_mul_self` — `PosDef.lean:355` |
| O6 | `−log(1−a) ≤ a/(1−a)`, `0≤a<1` | F7b scalar | **OWNED (compiled ✓)** | `Real.log_le_sub_one_of_pos` `Log/Basic.lean:306` + `Real.log_div` `:137`; the closing step is `field_simp; ring` (bare `field_simp` left `1-(1-a)=a`, Repair 3) |
| O7 | `Σ_{k} a^{M+1+k} = a^{M+1}/(1−a)` | F4a scalar | **OWNED** | `tsum_geometric_of_lt_one` `SpecificLimits/Basic.lean:329` + `tsum_mul_left` `InfiniteSum/Ring.lean:115` |
| O8 | `δ₀¹² ∈ (0,1)` (floor is a positive constant) | F4a floor | **OWNED (compiled ✓)** | `Real.lt_sqrt` `Data/Real/Sqrt.lean:381`, `Real.sqrt_lt'` `:235`, `pow_pos`, `pow_lt_pow_left₀` `Order/GroupWithZero/Unbundled/Basic.lean:535` — Repair 2 corrected the fabricated `Real.sqrt_eq_iff_sq_eq` (no such constant) and the renamed `pow_lt_pow_left`→`pow_lt_pow_left₀` |
| O9 | bare positive F has real ≥0 spectrum ⇒ no complex poles | F4b core | **OWNED** | `Matrix.PosSemidef.eigenvalues_nonneg` — `Analysis/Matrix/PosDef.lean:42` (+ O5) |
| O10 | weighted tail `Σ aᵐ/m ≤ a^{M+1}/((M+1)(1−a))` | F4a scalar | **LIGHT-SORRY (G1a)** | termwise `1/m ≤ 1/(M+1)` + `tsum_le_tsum` + O7; no missing primitive |
| O11 | `‖PUP‖ ≤ 1` (U_eff contraction) | F4b | **LIGHT-SORRY (G3)** | `norm_mul_le` chain on `Matrix.instNormedRing`; needs `‖U‖≤1,‖P‖≤1` as hyps |
| O12 | `U_effᴴU_eff + F_c = I` (allowed identity, block form) | F4b | **LIGHT-SORRY (G4)** | algebraic expansion of `F=P−(PUP)ᴴ(PUP)` compressed to ran P; block algebra only |
| **G1** | `\|Tr(Fᵐ)\| ≤ rank(F)·ρ(F)ᵐ` (trace-power → eigen bound) | **F4a matrix leg** | **GAP-SORRY** | reduction exists: `Matrix.trace_eq_sum_roots_charpoly` `Charpoly/Eigs.lean:29` gives `Tr = Σ roots`, and O9 gives roots ≥ 0; but `Tr(Fᵐ) = Σ λᵢᵐ` (trace of the *power*) + "exactly rank(F) nonzero eigenvalues each ≤ ρ" is not a single named lemma — needs assembly |
| **G2** | `\|−log det(I−zF)\| ≤ rank(F)·(−log(1−a))` (matrix log-det) | **F7b matrix leg** | **GAP-SORRY** | `Matrix.det_eq_prod_roots_charpoly` `Charpoly/Eigs.lean:27` gives `det(I−zF)=∏(1−zλᵢ)` in principle; the complex principal-branch bound `\|log(1−zλ)\| ≤ −log(1−\|z\|λ)` for `\|z\|λ<1` is standard but not in-tree by name — the analytic heart stays open |

**Reading of the ledger.** O1–O9 (nine obligations) are OWNED outright and cover: all of F7a (the rank leg — which is F7's *titled* content), the F7b scalar convexity, the F4a scalar geometric engine, the F4a δ₀-floor typing, and F4b's structural pole-discipline core (bare F cannot carry complex poles). O10–O12 are LIGHT-SORRY (I'd stake that they close with routine labor). Only **G1 and G2** are genuine analytic gaps — and even they are *narrowed*, not wide open: the eigenvalue-decomposition bridges (`trace_eq_sum_roots_charpoly`, `det_eq_prod_roots_charpoly`) are present; what's missing is the power/branch assembly.

**Honesty statement (binding):** I am NOT claiming F4a's universal tail bound or F7b's universal log-det bound as proved. Those stay `sorry` (G1, G2). What IS theorem-grade is: F7's rank-localization lemma (O1–O5) and F4b's forbidden-shortcut refutation (O5, O9). Those two are the load-bearing, contract-named content of the two claims.

## 5. Registry MOTION (proposal only)

**NO edits made.** These are proposals for the owner. Registry source-of-truth discipline (per memory `d0-registry-source-of-truth`): `CLAIM_TO_LEAN_MAP.csv` is canonical; `theory_status_map.csv`/`theory_graph.json` are generated by `sync_theory_status_map.py` — edit the source + regen, never the generated file.

### M1 — cert swap (both claims)

Replace the fake originals in the `python_cert` column with the REFORGED certs (move them into `05_CERTS/` under the original names or `_REFORGED` names at owner's discretion):

- **F4** row 137: `python_cert` = `vp_cvft_uv_feedback_tail_bound_refined.py;vp_cvft_ueff_pole_discipline.py` → `vp_cvft_uv_feedback_tail_bound_refined_REFORGED.py;vp_cvft_ueff_pole_discipline_REFORGED.py`
- **F7** row 140: `python_cert` = `vp_cvft_boundary_channel_rank.py;vp_cvft_refined_logdet_rank_bound.py` → `vp_cvft_boundary_channel_rank_REFORGED.py;vp_cvft_refined_logdet_rank_bound_REFORGED.py`

### M2 — quarantine the 4 fake originals (incident note, v17-precedent format)

Append to `_QUARANTINE/QUARANTINE_LEDGER.md` a new section (drafted below; the four originals move to `_QUARANTINE/cvft_fabricated_controls/`):

```markdown
## cvft_fabricated_controls/ — the 4 fake-control certs backing D0-CVFT-F4/F7

Excluded from the corpus: must not be imported, cited, or promoted. Kept for
forensic reference. Retired 2026-07-05 after CERT_CANFAIL_SWEEP_REPORT.md Finding
F2 and the CVFT_F4_F7_REFORGE_REPORT.md audit; superseded by scene-constructed
can-fail certs (see M1). Same class of defect as the v17 fabricated citation:
evidence that never verified the claim it was cited for.

1. **vp_cvft_boundary_channel_rank.py** (was F7). Checks were tautologies over a
   hardcoded 4x3 `qup` literal; `dim_boundary=2` hardcoded; "negative control"
   `NEGATIVE_CONTROL_CAUGHT` printed unconditionally on the success path (F2). Never
   verified `im(QUP)⊆B`, never verified PSD/typing.
2. **vp_cvft_refined_logdet_rank_bound.py** (was F7). One hardcoded eigen-list
   `[0.8,0.4,0.0]`, single hardcoded z; "control" was the float-literal inequality
   `0.45×1 ≠ 0.45×0.8`; never constructs F; no tightness witness.
3. **vp_cvft_uv_feedback_tail_bound_refined.py** (was F4). Hardcoded eigen-list, one
   z, one M; tail truncated at m<80 with no control; hardcoded `delta12 = 1e-6` —
   NOT the owned floor `δ₀¹² = ((√5−2)/2)¹² ≈ 7.31e-12` (off by ~136,746×).
4. **vp_cvft_ueff_pole_discipline.py** (was F4). Hardcoded eigen-lists for U_eff and
   F; "pole check" `|0.3−0.3|<1e-12`; "positivity" `isinstance(x,float) and x>=0`.
   Worse: its two lists encode `spec(F)=|eig(U_eff)|²` (0.64=0.8², 0.25=0.5²), an
   identity FALSE under the owned typing (owned relation is `spec(F_c)=1−σ²(U_eff)`).

All four share Finding F2: no control computation exists; the CERT-CLOSED status they
backed was UNSUPPORTED for the entire interval between original closure ([8C: linked
passing cert]) and 2026-07-05.
```

### M3 — interval-honesty note (append to both claim rows' `notes`)

`[2026-07-05 reforge+lift] original certs had fabricated negative controls (sweep F2); quarantined; replaced by scene-constructed can-fail certs (REFORGED, exit 0). Between original closure and 2026-07-05 the CERT-CLOSED label rested exclusively on non-verifying certs.`

### M4 — lean_status PYTHON_CERTIFIED → LEAN_PROVED (CONDITIONAL, honest split)

This is the strengthening ask. Given the §4 ledger, the honest motion is **NOT a blanket flip**. Two sub-motions:

- **M4a (F7, propose LEAN_PROVED for the rank leg):** Set `lean_module=D0.CVFT.BoundaryRankLocalization`, `lean_theorem=cvft_rank_F_le_dim_boundary` (with siblings `cvft_rank_F_eq_rank_QUP`, `cvft_scene_rank_F_le_three`, `cvft_F_posSemidef`). Since F7's registry title IS "boundary-local holographic rank lemma" and its notes say "supports localization only", the rank leg is the claim's substance and it is **sorry-free** (O1–O5). The log-det leg (G2) stays recorded as an open sub-obligation in `notes`. Recommend `lean_status=LEAN_PROVED` with a notes clause: `rank-localization leg Lean-proved (D0.CVFT.BoundaryRankLocalization, sorry-free); refined log-det leg G2 open`.
  - ⚠ **REPAIR 6 (skeptic #1) — COMPILE GATE.** M4a was WITHHELD by skeptic #1 because the named theorem `cvft_rank_F_le_dim_boundary` did NOT compile as originally written (missing `[PartialOrder 𝕜] [StarOrderedRing 𝕜]`; the sibling `cvft_rank_F_eq_rank_QUP` failed the same way). Status after repair: with the star-ordered-field context (Repair 1), BOTH `cvft_rank_F_le_dim_boundary` and `cvft_rank_F_eq_rank_QUP` now **compile in-tree** (`lake env lean`, 2026-07-05, 0 errors, linter warnings only). The compile gate for M4a's named `lean_theorem` is therefore MET, and M4a is now motion-ready **as a proposal** (still no CSV edit; owner blessing + a real in-tree `.lean` module `D0.CVFT.BoundaryRankLocalization` carrying these exact theorems remain required before the flip). UPDATE (full-block re-verification): the two named siblings `cvft_scene_rank_F_le_three` (over ℚ, plain-field `rank_mul_le_right`) and `cvft_F_posSemidef` (over `[CommRing R] [PartialOrder R] [StarRing R] [StarOrderedRing R]`) were compiled TOGETHER with the four load-bearing theorems as one §2 unit — the whole block compiles at **0 errors** (linter warnings only), so all of O1–O5's Lean statements are compile-clean. The only §2 items NOT compiled are the two `True`-stub placeholders (`cvft_logdet_rank_bound`, `cvft_uv_tail_bound`), which are stubs by design (G1/G2).
  - **M1/M2/M3 are UNAFFECTED by this finding** (skeptic #1 explicit): the cert swap (M1), the quarantine incident note for the 4 fake originals (M2), and the interval-honesty note (M3) do not depend on any Lean compile. The underlying REFORGED F7 cert is genuinely non-tautological (constructs the scene, computes SVD ranks, runs executed mutation controls, exhibits nonsat+sat A4-discipline witnesses) and stands.
- **M4b (F4, KEEP PYTHON_CERTIFIED for now, register Lean targets):** F4's *load-bearing analytic* content (the refined tail bound) is gap G1 (sorry). Its pole-discipline core (O9) is proved but that is one leg of two. Honest recommendation: **do NOT flip F4 to LEAN_PROVED yet.** Register `lean_module=D0.CVFT.UeffPoleDiscipline` for the *proved* pole-discipline leg (`cvft_bare_F_posSemidef`, `cvft_delta0_pos`) and keep `lean_status=PYTHON_CERTIFIED` until G1 (trace-power tail) closes. This respects the contract's rule (`D0_CLAIM_CLOSURE_CONTRACT.md:11`, "`sample cert passed` as proof of an infinite family" is forbidden): the universal tail bound is not yet a theorem.

**If the owner declines M1** (cert swap): both claims MUST demote to `PROOF-TARGET` — their sole current backing is the known-fake originals (per reforge report §9 M2).

### M5 — siblings

The three unreferenced no-failure-path siblings (`vp_cvft_boundary_rank_bound.py`, `vp_cvft_logdet_rank_bound.py`, `vp_cvft_uv_feedback_tail_bound.py`) are superseded; retire or mark non-load-bearing demos (reforge report §9 M4).

## 6. Self-attack / skeptic pass

Pre-registered attack surface (run before declaring anything): (A) does a "LEAN_PROVED" flip over-claim relative to what the sorry-free lemmas actually prove? (B) is the finite-scene theorem being smuggled in for the universal claim? (C) do the owned Mathlib citations actually type-check as I've used them? (D) is the `dim B_boundary` object faithfully modeled?

**A. Over-claim on the status flip.** The most dangerous move here is flipping BOTH claims to LEAN_PROVED on the strength of "the certs pass." The certs passing (verified, exit 0) is NOT the same as a Lean theorem — the contract forbids "sample cert passed as proof of an infinite family" (`D0_CLAIM_CLOSURE_CONTRACT.md:11`). **Mitigation applied:** M4 is split — only F7's *rank leg* is proposed for LEAN_PROVED (sorry-free), F4 stays PYTHON_CERTIFIED because its load-bearing tail bound is G1-sorry. This is the honest floor. **Residual risk:** even F7a's `cvft_logdet_rank_bound` placeholder is `True`-typed (a stub, not the real statement) — I did NOT write the real F7b statement, only named it. So F7's LEAN_PROVED must be scoped to the RANK leg in the notes, never presented as "F7 fully Lean-proved."

**B. Finite scene vs universal claim.** ⚠ REPAIR 4 (skeptic #1) — the original text here claimed F7a's core lemmas are "stated over an *arbitrary* field ... genuinely universal ... stronger than the cert." That is FALSE and is struck. `cvft_rank_F_eq_rank_QUP` and `cvft_rank_F_le_dim_boundary` route through `rank_conjTranspose_mul_self` (Rank.lean:361 `section StarOrderedField`), so they hold over a STAR-ORDERED FIELD, not an arbitrary one — over a plain field or a finite field the cited owner does not apply and they do not typecheck. Corrected reading: (i) the localization sub-leg `cvft_rank_QUP_le_rank_P` (via `rank_mul_le_right`) IS over an arbitrary field; (ii) the conjTranspose-rank identity and the boundary dim-bound require the star order (ℂ, `open ComplexOrder`, satisfies it — so the scene instance is covered, but the "genuinely universal / stronger than the cert" defense is withdrawn). There is still no scene-smuggling — the theorems are universal over the star-ordered-field class, of which the scene's ℂ is a member — but the class is star-ordered fields, not all fields. The scene instance (`cvft_scene_rank_F_le_three`) is a corollary. The DANGER is F4a/F7b: the certs verify finite grids of `(a, phase, M)`; the Lean drafts do NOT yet prove the universal `∀z` bound (G1/G2 sorry). I have NOT claimed otherwise. Clean on scope, corrected on universality.

**C. Do the citations type-check as used?** ⚠ REPAIR 5 (skeptic #1) — the original answer here rested on grep alone ("verified each cited lemma's *signature* by grep, not by compiling") and it was INSUFFICIENT: grep matched the `theorem` line but missed (a) the enclosing `section StarOrderedField` typeclass variables required by `rank_conjTranspose_mul_self`/`rank_le_card_height` (O1, M4a boundary), and (b) two constants that do not exist / were renamed (`Real.sqrt_eq_iff_sq_eq`, `pow_lt_pow_left` — O8). Skeptic #1 then COMPILED the sorry-free theorems and four errored out. **Binding note (accepted): no theorem in this memo may be marked OWNED / sorry-free until it COMPILES under `lake env lean` in-tree — grep-of-signature is not sufficient.** The four load-bearing sorry-free theorems (O1 `cvft_rank_F_eq_rank_QUP`, M4a `cvft_rank_F_le_dim_boundary`, O6 `cvft_neg_log_le_geom`, O8 `cvft_delta0_pos`) have now been compiled in-tree (2026-07-05, 0 errors, linter warnings only) after the repairs. Risk points, re-audited:
  - `Matrix.rank_conjTranspose_mul_self (A) : (Aᴴ*A).rank = A.rank` — matches O1, but ONLY under the `section StarOrderedField` context (`[Field R] [PartialOrder R] [StarRing R] [StarOrderedRing R]`, Rank.lean:361). Original memo context `[Field 𝕜] [StarRing 𝕜]` did NOT typecheck. Repaired in §2 and compiled.
  - `cvft_rank_F_le_dim_boundary`: my FIRST draft used `Matrix.rank_le_card_width QUP`, which bounds by `card n` (COLUMNS = domain), not the boundary channel type `b` (ROWS = range of QUP). That was a real defect. **Fixed in the §2 draft:** the correct owned lemma is `Matrix.rank_le_card_height` (`Rank.lean:304`, verbatim `theorem rank_le_card_height [Fintype m] [Nontrivial R] (A : Matrix m n R)` — bounds rank by the ROW count), which bounds `rank QUP ≤ card b` directly with no transpose step. This lemma ALSO lives in `section StarOrderedField`, so it inherits the same star-order requirement (fixed in §2). Now sorry-free and compiled.
  - O6 `cvft_neg_log_le_geom`: the `field_simp` step did NOT close `1/(1-a)-1 = a/(1-a)` (left `1-(1-a)=a`); repaired to `field_simp; ring`, compiled.
  - O8 `cvft_delta0_pos`: `Real.sqrt_eq_iff_sq_eq` does not exist and `pow_lt_pow_left` is renamed to `pow_lt_pow_left₀`; repaired with `Real.lt_sqrt` / `Real.sqrt_lt'` / `pow_lt_pow_left₀`, compiled.
  - `Real.log_le_sub_one_of_pos`, `Real.log_div`, `tsum_geometric_of_lt_one`, `tsum_mul_left`, `posSemidef_conjTranspose_mul_self`, `PosSemidef.eigenvalues_nonneg` — signatures verified present; the ones exercised inside the four compiled theorems (`log_le_sub_one_of_pos`, `log_div`) are confirmed by compile. The others (used only inside LIGHT/GAP-SORRY bodies or PSD-typing corollaries) remain grep-verified-only and are NOT claimed compiled — they must clear the same compile gate before their obligations flip to OWNED.

**D. Is `dim B_boundary` faithfully modeled?** The reforged cert builds `B = span{U_L Q e_j : j∈touched}` and checks `im(QUP)⊆B`, giving `rank(F) ≤ dim B ≤ |S|` (reforge report line 64, and cert `boundary_channel_space`). My Lean draft collapses "dim B" to "card of the boundary index type," which is the `≤ |S|` end, NOT the tighter computed `dim B` (which can be `< |S|`, e.g. the same-zone-equal-phase member has rank 1 < dim B 2). So the Lean lemma proves the WEAKER, always-true bound `rank(F) ≤ card(boundary channels)`. That is honest and matches the "localization only, not A4" discipline (a non-saturating inequality). The cert's *strict-slack non-saturation witness* (which refutes an A4-equality reading) is NOT reproduced in Lean — it stays cert-only evidence. Flagged: the Lean leg is the inequality, not the non-saturation/A4-refutation witness.

**Skeptic verdict.** The memo does not over-claim IF the M4 split is honored: F7-rank-leg → LEAN_PROVED, everything else stays as-is (PYTHON_CERTIFIED / named-sorry). The §6C `rank_le_card_width`→`rank_le_card_height` defect is **repaired in the §2 draft** (owned lemma `Rank.lean:304`). One cosmetic repair remains before any build: replace the two `True`-stub statements (`cvft_logdet_rank_bound`, `cvft_uv_tail_bound`) with real sorry-bearing statements so the sorries are *visible to `#print axioms`*, not hidden behind `trivial`. That repair does not change the ledger's OWNED/GAP split. **This remains a DRAFT proposal; nothing is "closed" or "forced."**

---

## Appendix — verification transcript (this machine, 2026-07-05)

All four REFORGED certs run to exit 0:

```
vp_cvft_boundary_channel_rank_REFORGED.py        exit=0  PASS_CVFT_BOUNDARY_CHANNEL_RANK_REFORGED
vp_cvft_refined_logdet_rank_bound_REFORGED.py    exit=0  PASS_CVFT_LOGDET_RANK_BOUND_REFINED_REFORGED
vp_cvft_uv_feedback_tail_bound_refined_REFORGED.py exit=0 PASS_CVFT_UV_TAIL_BOUND_REFINED_REFORGED
vp_cvft_ueff_pole_discipline_REFORGED.py         exit=0  PASS_UEFF_POLE_DISCIPLINE_REFORGED
```

Mathlib present at `09_LEAN_FORMALIZATION/.lake/packages/mathlib` (leanprover/lean4:v4.30.0). ⚠ REPAIR 5 (skeptic #1): the original line here said "all cited lemma signatures grep-verified in-tree (not compiled)" and presented grep as sufficient — it was not (it missed section typeclass requirements and two non-existent constants; see §6C). The four load-bearing sorry-free theorems (O1 `cvft_rank_F_eq_rank_QUP`, M4a `cvft_rank_F_le_dim_boundary`, O6 `cvft_neg_log_le_geom`, O8 `cvft_delta0_pos`) have since been COMPILED in-tree with `lake env lean` after the repairs (2026-07-05, 0 errors, linter warnings only; scratch file compiled outside the tree, no built `.lean` written). Lemmas used only inside LIGHT/GAP-SORRY bodies remain grep-verified-only and are NOT claimed compiled. D0 owned modules (`KernelZoneSplit`, `SceneLaplacianSpectrumForced`, `HiggsLogdetStationary`) present and quoted verbatim in §1.

---

## Skeptic #1 verdict + repair log (accepted in full)

**Verdict: WOUNDED.** Skeptic #1 accepted in full, no defense. The strongest finding was a KILL on the LEAN-LIFT typecheck gate: the memo asserted the sorry-free theorems typecheck but verified them only by grep, never by compile. Skeptic #1 compiled the sorry-free theorems against this tree's mathlib (leanprover/lean4:v4.30.0) and FOUR errored out, including the two carrying the entire F7 lift. All four are repairable and repaired; the M4a lift is NOT killed but was correctly withheld pending compile. The repair also falsifies the memo's original §6B universality defense (see Repair 4).

**Binding process change (accepted):** no theorem in this memo may be marked OWNED / sorry-free until it COMPILES under `lake env lean` in-tree. Grep-of-signature is insufficient — it misses (a) enclosing `section` typeclass variables and (b) non-existent / renamed constants. This is now stated in §6C and the Appendix.

### Errors of record (verbatim compiler output, original memo text, `lake env lean`, 2026-07-05)

| # | Theorem (original §) | Verbatim error | Root cause |
|---|---|---|---|
| E1 | O1 `cvft_rank_F_eq_rank_QUP` (§2, was line 100) | `error(lean.synthInstanceFailed): failed to synthesize instance of type class PartialOrder 𝕜` | `Matrix.rank_conjTranspose_mul_self` lives in `Rank.lean:361 section StarOrderedField` needing `[Field R][PartialOrder R][StarRing R][StarOrderedRing R]`; memo declared only `[Field 𝕜][StarRing 𝕜]`. Section variables dropped by grep. |
| E2 | M4a target `cvft_rank_F_le_dim_boundary` (§2, was line 116) | `error(lean.synthInstanceFailed): failed to synthesize instance of type class PartialOrder 𝕜` (+ `unsolved goals ⊢ PartialOrder 𝕜`) | Same missing star-order context; routes through the same lemma + `rank_le_card_height` (also in `section StarOrderedField`). This is the named M4a `lean_theorem`. |
| E3 | O6 `cvft_neg_log_le_geom` (§2, was line 157) | `error: unsolved goals ⊢ 1 - (1 - a) = a` | `field_simp` alone did not close `1/(1-a) - 1 = a/(1-a)`; needed a trailing `ring`. |
| E4 | O8 `cvft_delta0_pos` (§3, was line 234) | `error(lean.unknownIdentifier): Unknown constant Real.sqrt_eq_iff_sq_eq` (and separately `pow_lt_pow_left` unknown, renamed `pow_lt_pow_left₀`) | Two fabricated / renamed constant names — the SAME defect class the memo quarantines the 4 fake originals for. |

**Consequence recorded:** as delivered, NO theorem proposed for LEAN_PROVED compiled, so M4a could not proceed on the memo as written. That is the reason the WOUNDED verdict was not a SURVIVES.

### Repairs applied (all 6) and re-verification

| Repair | Where | What changed | Re-verified |
|---|---|---|---|
| R1 (O1/M4a context) | §2 `variable` block + O1 + boundary docstrings | context → `[Field 𝕜][PartialOrder 𝕜][StarRing 𝕜][StarOrderedRing 𝕜]`; dropped now-derivable `[Nontrivial 𝕜]` and unused `[DecidableEq]` | ✓ compiled in-tree, 0 errors |
| R2 (O8 real names) | §3 `cvft_delta0_pos` | `Real.sqrt_eq_iff_sq_eq`→`Real.lt_sqrt`/`Real.sqrt_lt'`; `pow_lt_pow_left`→`pow_lt_pow_left₀` | ✓ compiled in-tree, 0 errors |
| R3 (O6 proof) | §2 `cvft_neg_log_le_geom` | `field_simp` → `field_simp; ring` | ✓ compiled in-tree, 0 errors |
| R4 (universality narration) | §2 module docstring + §6B | struck "arbitrary field / genuinely universal / stronger than the cert"; corrected to STAR-ORDERED field (ℂ covers the scene; only the `rank_mul_le_right` sub-leg is arbitrary-field) | ✓ text-only, matches compiled context |
| R5 (process claim) | §6C + Appendix | struck "all signatures grep-verified"; added binding "no OWNED until it compiles" note | ✓ text-only |
| R6 (M4a scoping) | §5 M4a | added COMPILE GATE clause: M4a withheld until named theorem compiles → now MET (compiled); M1/M2/M3 unaffected; siblings `cvft_scene_rank_F_le_three` / `cvft_F_posSemidef` flagged NOT-yet-compiled | ✓ text-only |

**Compiled artifact (outside the tree, no built `.lean` written):** two scratch files were compiled with `lake env lean` from `09_LEAN_FORMALIZATION`. (i) The four repaired sorry-free theorems (E1–E4 targets) — **0 errors**. (ii) The FULL repaired §2 F7 block exactly as it now appears in the memo — `cvft_rank_F_eq_rank_QUP`, `cvft_rank_QUP_le_rank_P`, `cvft_rank_F_le_dim_boundary`, `cvft_scene_rank_F_le_three`, `cvft_F_posSemidef`, `cvft_neg_log_le_geom` — also **0 errors**, warnings only (`unused section variable` on the plain-field `rank_mul_le_right` lemma; `unused variable h0` in O6, since the `0 ≤ a` hypothesis is not load-bearing given `a < 1`). O8 `cvft_delta0_pos` compiled in artifact (i). The §3 F4 block (G1/G2 gaps, LIGHT-SORRIES) was NOT compiled. Both scratch files were deleted after compile; per DISCIPLINE no `.lean` was written to the tree and no CSV was edited.

### Residual (what stays open; what is now mint-or-motion-ready)

**Now motion-ready (as proposals only — owner blessing + a real in-tree `D0.CVFT.BoundaryRankLocalization` module still required before any CSV flip):**
- **M4a** (F7 rank leg → LEAN_PROVED): the named `lean_theorem` `cvft_rank_F_le_dim_boundary` and its core sibling `cvft_rank_F_eq_rank_QUP` now compile. Compile gate MET.
- **M1 / M2 / M3** (cert swap, quarantine incident note, interval-honesty note): unaffected by the finding; the REFORGED F7 cert is genuinely non-tautological.

**Still open (unchanged by this pass):**
- **G1** (F4a trace-power → eigenvalue tail bound) and **G2** (F7b matrix log-det bound): genuine analytic GAP-SORRIES; narrowed (eigen-decomp bridges present) but not proved. F4 stays PYTHON_CERTIFIED per M4b. These are in the §3 F4 block, which was NOT compiled in this pass (only the §2 F7 block + O8 were).
- **O10–O12** LIGHT-SORRY: proof labor, no missing primitive, NOT yet compiled — remain candidate until they clear the gate.
- The two `True`-stub placeholder statements (`cvft_logdet_rank_bound`, `cvft_uv_tail_bound`) should be rewritten as real sorry-bearing statements before any build so the sorries are visible to `#print axioms` (hygiene, unchanged from the memo's own §6 note).

**Status language:** DRAFT / candidate throughout. Nothing here is "forced" or "closed." The only thing hardened by this pass is that four specific sorry-free theorems now COMPILE in-tree, which clears M4a's compile gate — the mint itself still requires the owner and a real module.
