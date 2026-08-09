import D0.Synthesis.TransportForkEndgame
import Mathlib.Tactic

/-!
# The per-crossing weight under the registered form: reducing the seam-crossing primitive

**Grade note (post-skeptic 2026-08-03, KILL accepted).** Row `D0-ALPHA-SEAM-FORM-FORCED-001`
REGISTERS the dressing split — verbatim: "depth φ⁻¹⁷ = ξ₅·φ⁻¹² SPLIT: seam factor ξ₅ THE /
**transport factor OPEN**" — and the row itself, its cert, and BOOK_02 02.13.h:95 all grade the
composition `φ⁻¹⁷ = ξ₅·φ⁻¹²` as "owned only as prose — a named open sub-leg, not THE". The
total is therefore a REGISTERED PROOF-TARGET form, NOT an owned input; every use of it below is
the named hypothesis (γ). The first draft claimed "forced by the owned form" — that framing was
KILLED (by the memo's own pre-registered ATT-A criterion) and is retracted.

The fork endgame (2026-08-02) reduced the door-2 route of obligation (i) to the residual
primitive PRIM-SEAM-CROSSING-TICK-IDENTIFICATION (*one sector crossing of `V₁₁ ⊔ {∗}` = one
toral tick*). This module shrinks the primitive's SEMANTIC content, inside door 2's product
reading: given the registered form, the tick VALUE need not be identified — it is determined.

Work with per-sector weights `w₁, …, w₁₁, u > 0` (11 sectors of `V₁₁`, one anonymous `∗`):

* `equivariant_weights_equal` — an `Aut`-equivariant weight function is constant on a zone
  (real-valued restatement of the owned swap argument; `S₁₁` acts transitively on the `V₁₁`
  sectors under door 2's sector = zone-1-vertex reading): **the eleven weights are equal**,
  `w₁ = … = w₁₁ = w`. Only the anonymous sector's weight `u` escapes symmetry.
* `crossing_weight_forced` — IF `u = w` (uniformity of the 12th sector) AND the registered
  total holds (hypothesis (γ)), then `(φ⁻¹)⁵·w¹² = (φ⁻¹)¹⁷` and the unique positive real
  twelfth root (`twelfth_root_unique`) give **`w = φ⁻¹` exactly**. The per-crossing value is
  determined by the registered form under the named hypotheses — not imported from the toral
  side, and not "derived from owned" (the total is PROOF-TARGET grade).
* `nonuniform_freedom` — WITHOUT uniformity, `(w, u)` is a one-parameter family (explicit
  witness): nothing is forced. The uniformity hypothesis is therefore load-bearing and the
  control can fail — the forcing is not decorative.
* `forced_value_is_toral_stable_root` — the conditionally determined value COINCIDES with the
  toral stable root `x² + x − 1 = 0` (delegation to the endgame module). With (γ) unowned, this
  is a coincidence-of-values record, not an explanation claim.
* `seam_crossing_composed` — the composed pipeline as ONE Lean statement (an equivariant
  positive weight vector on zone 1, the registered product form, and 12th-sector uniformity
  yield `w v = φ⁻¹` for every sector) — no prose glue between carriers.

**Net (rescoped post-KILL).** Inside the product reading, the primitive's semantic content
reduces to THREE named structural hypotheses, applied under the equivariance norm and the
positivity (modulus) reading:
  (α) **uniformity**: the anonymous 12th sector carries the same weight as the eleven
      symmetry-equalized ones (`u = w`);
  (β) **the count/product reading**: the crossings are the `|V₁₁| + 1 = 12` sectors and the
      depth is their product (door 2's cert-comment-grade reading);
  (γ) **the registered total**: `depth = φ⁻¹⁷ = ξ₅·φ⁻¹²` — the OPEN sub-leg of obligation (i)
      itself (PROOF-TARGET, not THE). C4 advances the obligation MODULO (γ): it derives the
      per-crossing decomposition of a composition it assumes numerically.
Given (α)∧(β)∧(γ) — under the norm and positivity — the value `φ⁻¹` per crossing is a theorem.
Each hypothesis is strictly weaker than the original semantic identification ("crossing = tick"
implies all of them plus the toral binding), so the reduction genuinely shrinks the primitive —
but the residual has THREE members, not two, and (γ) is the very open content the obligation
asks to own. Refuting (α) re-opens the one-parameter family; nothing binds door 2; no registry
change. Door 1 remains the live rival.

**Scope honesty.** The product structure and the sector = zone-1-vertex identification are
hypotheses (cert-comment grade). The equivariance norm (weights as scene-side canonical MODULI
must be Aut-equivariant) is normative; it is applied to the per-sector moduli, NOT to the
pairing operator — whose necessary NON-equivariance the corpus separately owns
(`no_equivariant_seam`): the depth `φ⁻¹⁷` is itself Aut-invariant, so uniform moduli are
consistent with a symmetry-breaking pairing; the two objects are distinct. Kill-shape check:
all universals conditional on named hypotheses; single carrier (zone 1 + the α-line's own
ℝ-dressing).
-/

namespace D0.Synthesis.SeamCrossingWeightForced

open Real
open scoped goldenRatio
open D0.Spectral.DarkArchiveStructure

/-! ## Equivariance forces the eleven weights equal -/

/-- Real-valued equivariance under same-zone transpositions (the generators of `Aut`). -/
def EquivariantVecR (w : Fin 33 → ℝ) : Prop :=
  ∀ a b : Fin 33, zone a = zone b → ∀ v, w (Equiv.swap a b v) = w v

/-- An equivariant weight function is constant on each zone — in particular on the eleven
`V₁₁` sectors. -/
theorem equivariant_weights_equal (w : Fin 33 → ℝ) (hw : EquivariantVecR w) :
    ∀ u v : Fin 33, zone u = zone v → w u = w v := by
  intro u v huv
  have h := hw u v huv v
  rw [Equiv.swap_apply_right] at h
  exact h

/-! ## The unique positive twelfth root -/

/-- Positive reals have unique twelfth roots. -/
theorem twelfth_root_unique (w : ℝ) (hw : 0 < w) (h : w ^ 12 = (φ⁻¹) ^ 12) : w = φ⁻¹ := by
  have hv : (0 : ℝ) < φ⁻¹ := inv_pos.mpr goldenRatio_pos
  rcases lt_trichotomy w φ⁻¹ with hlt | heq | hgt
  · exfalso
    have := pow_lt_pow_left₀ hlt (le_of_lt hw) (by norm_num : (12 : ℕ) ≠ 0)
    rw [h] at this
    exact lt_irrefl _ this
  · exact heq
  · exfalso
    have := pow_lt_pow_left₀ hgt (le_of_lt hv) (by norm_num : (12 : ℕ) ≠ 0)
    rw [h] at this
    exact lt_irrefl _ this

/-! ## The forcing and the freedom -/

/-- **The conditionally determined value**: with the eleven weights equal (equivariance) and
the twelfth uniform (`u = w`), the REGISTERED total `φ⁻¹⁷ = ξ₅ · (product)` — hypothesis (γ),
PROOF-TARGET grade — determines the per-crossing weight to be exactly `φ⁻¹`. -/
theorem crossing_weight_forced (w u : ℝ) (hw : 0 < w) (_hu : 0 < u)
    (huniform : u = w)
    (hform : (φ⁻¹) ^ 5 * (w ^ 11 * u) = (φ⁻¹) ^ 17) :
    w = φ⁻¹ := by
  rw [huniform] at hform
  have hne : ((φ : ℝ)⁻¹) ^ 5 ≠ 0 :=
    pow_ne_zero _ (inv_ne_zero (ne_of_gt goldenRatio_pos))
  have h12 : w ^ 12 = (φ⁻¹) ^ 12 := by
    have hchain : (φ⁻¹) ^ 5 * w ^ 12 = (φ⁻¹) ^ 5 * (φ⁻¹) ^ 12 := by
      calc (φ⁻¹) ^ 5 * w ^ 12 = (φ⁻¹) ^ 5 * (w ^ 11 * w) := by ring
      _ = (φ⁻¹) ^ 17 := hform
      _ = (φ⁻¹) ^ 5 * (φ⁻¹) ^ 12 := by rw [← pow_add]
    exact mul_left_cancel₀ hne hchain
  exact twelfth_root_unique w hw h12

/-- **The freedom without uniformity**: for ANY positive `w` there is a compensating twelfth
weight — a one-parameter family; the uniformity hypothesis is load-bearing. -/
theorem nonuniform_freedom (w : ℝ) (hw : 0 < w) :
    ∃ u : ℝ, 0 < u ∧ (φ⁻¹) ^ 5 * (w ^ 11 * u) = (φ⁻¹) ^ 17 := by
  have hphi : (0 : ℝ) < φ⁻¹ := inv_pos.mpr goldenRatio_pos
  have hw11 : w ^ 11 ≠ 0 := ne_of_gt (pow_pos hw 11)
  refine ⟨(φ⁻¹) ^ 12 / w ^ 11,
    div_pos (pow_pos hphi 12) (pow_pos hw 11), ?_⟩
  rw [mul_comm (w ^ 11), div_mul_cancel₀ _ hw11, ← pow_add]

/-- The conditionally determined value coincides with the toral stable root — delegation to
the endgame module. A coincidence-of-values record; no explanation claim while (γ) is open. -/
theorem forced_value_is_toral_stable_root : (φ⁻¹) ^ 2 + φ⁻¹ - 1 = 0 :=
  D0.Synthesis.TransportForkEndgame.stable_contraction_is_phi_inv

/-- **The composed pipeline in one statement**: an `Aut`-equivariant positive weight vector on
the eleven sectors, 12th-sector uniformity (α), and the registered product form (β)+(γ) give
`w v = φ⁻¹` on every sector. No prose glue: the vector and scalar carriers are composed here. -/
theorem seam_crossing_composed (w : Fin 33 → ℝ) (hw : EquivariantVecR w)
    (hpos : ∀ v, zone v = 1 → 0 < w v)
    (u : ℝ) (hu : 0 < u) (v₀ : Fin 33) (hv₀ : zone v₀ = 1)
    (huniform : u = w v₀)
    (hform : (φ⁻¹) ^ 5 *
      ((∏ v ∈ Finset.univ.filter (fun v => zone v = 1), w v) * u) = (φ⁻¹) ^ 17) :
    ∀ v, zone v = 1 → w v = φ⁻¹ := by
  have heq : ∀ x, zone x = 1 → w x = w v₀ := fun x hx =>
    equivariant_weights_equal w hw x v₀ (hx.trans hv₀.symm)
  have hprod : (∏ x ∈ Finset.univ.filter (fun x => zone x = 1), w x) = (w v₀) ^ 11 := by
    rw [Finset.prod_congr rfl (fun x hx => heq x (Finset.mem_filter.mp hx).2),
      Finset.prod_const]
    congr 1
  rw [hprod] at hform
  have hres := crossing_weight_forced (w v₀) u (hpos v₀ hv₀) hu huniform hform
  intro v hv
  rw [heq v hv]
  exact hres

/-! ## Assembled -/

/-- **The reduction**: equivariance equalizes the eleven; uniformity (α) + the REGISTERED
total (γ, PROOF-TARGET grade) determine the value `φ⁻¹`; without uniformity a one-parameter
family remains; the determined value coincides with the toral stable contraction. The residual
of the crossing-tick primitive is THREE-membered — `(α) u = w`, `(β) the count/product
reading`, `(γ) the registered total` — the VALUE is no longer part of the primitive, MODULO
(γ). -/
theorem seam_crossing_reduction :
    (∀ w : Fin 33 → ℝ, EquivariantVecR w →
      ∀ u v : Fin 33, zone u = zone v → w u = w v) ∧
    (∀ w u : ℝ, 0 < w → 0 < u → u = w →
      (φ⁻¹) ^ 5 * (w ^ 11 * u) = (φ⁻¹) ^ 17 → w = φ⁻¹) ∧
    (∀ w : ℝ, 0 < w → ∃ u, 0 < u ∧ (φ⁻¹) ^ 5 * (w ^ 11 * u) = (φ⁻¹) ^ 17) ∧
    ((φ⁻¹) ^ 2 + φ⁻¹ - 1 = 0) :=
  ⟨equivariant_weights_equal, crossing_weight_forced, nonuniform_freedom,
   forced_value_is_toral_stable_root⟩

end D0.Synthesis.SeamCrossingWeightForced
