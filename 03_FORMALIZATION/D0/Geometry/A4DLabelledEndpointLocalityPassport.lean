import Mathlib.Algebra.Module.Equiv.Basic
import Mathlib.Tactic
import D0.Geometry.A4DLabelledPathHolonomyDescent
import D0.Geometry.A4DRelativeAEComparisonSpan

/-!
# Labelled endpoint-locality passport

Packages the owned slot-faithful theorem
`labelledPathEval_factors_endpoints_iff_trivial_holonomy` as an explicit
`EndpointLocal` predicate on `List ChainStep`, induces endpoint transport under
that hypothesis, and records the exact `L = 2` and noncontractible-cycle
firewalls separating endpoint descent from local relation graphification.

Firewalls (this module does **not**):
* identify `EndpointLocal` with `M = 0` or `R = 0`;
* claim plaquette flatness is enough for endpoint locality;
* erase the `L = 2` fwd/bwd label distinction before proving the period;
* start finite `F`, or touch continuum / GR / stress / time / golden work;
* use the older Prop-edge `ChainPath E` carrier for the main theorem.

Review note: endpoint transport is a classical quotient of labelled path data
under trivial holonomy; the quotient is not claimed to be physically mandatory.
-/

namespace D0.Geometry

open D0

set_option linter.unusedSimpArgs false

noncomputable section

variable {N : ℕ} {K V : Type*} [Field K] [AddCommGroup V] [Module K V]

/-! ## 1. EndpointLocal ↔ trivial labelled holonomy -/

/-- Path evaluation depends only on the ordered endpoint pair `(start, end)`,
retaining the slot-faithful `List ChainStep` carrier before any quotient. -/
def EndpointLocal (ellPlus : LabelledPositiveFamily N K V) : Prop :=
  ∀ (x y : ArchiveRolePhaseGroup N) (p q : List ChainStep),
    pathEnd N p x = y → pathEnd N q x = y →
      labelledPathEval ellPlus p x = labelledPathEval ellPlus q x

/-- Every based labelled loop has identity holonomy. -/
def TrivialLabelledHolonomy (ellPlus : LabelledPositiveFamily N K V) : Prop :=
  ∀ (x : ArchiveRolePhaseGroup N) (p : List ChainStep),
    pathEnd N p x = x →
      labelledPathEval ellPlus p x = LinearEquiv.refl K V

/-- Passport packaging of the owned slot-faithful descent theorem.
Not weakened to plaquette-flatness. -/
theorem EndpointLocal_iff_trivial_labelled_holonomy
    (ellPlus : LabelledPositiveFamily N K V) :
    EndpointLocal ellPlus ↔ TrivialLabelledHolonomy ellPlus :=
  labelledPathEval_factors_endpoints_iff_trivial_holonomy ellPlus

theorem EndpointLocal.of_trivial_labelled_holonomy
    (ellPlus : LabelledPositiveFamily N K V)
    (h : TrivialLabelledHolonomy ellPlus) : EndpointLocal ellPlus :=
  (EndpointLocal_iff_trivial_labelled_holonomy ellPlus).mpr h

theorem EndpointLocal.to_trivial_labelled_holonomy
    {ellPlus : LabelledPositiveFamily N K V} (h : EndpointLocal ellPlus) :
    TrivialLabelledHolonomy ellPlus :=
  (EndpointLocal_iff_trivial_labelled_holonomy ellPlus).mp h

/-! ## 2. Induced endpoint transport under EndpointLocal -/

/-- Path-presented endpoint transport (value independent of the word under
`EndpointLocal`). -/
def endpointTransport (ellPlus : LabelledPositiveFamily N K V)
    (p : List ChainStep) (x : ArchiveRolePhaseGroup N) : V ≃ₗ[K] V :=
  labelledPathEval ellPlus p x

theorem endpointTransport_eq_of_EndpointLocal
    {ellPlus : LabelledPositiveFamily N K V} (h : EndpointLocal ellPlus)
    (x y : ArchiveRolePhaseGroup N) (p q : List ChainStep)
    (hp : pathEnd N p x = y) (hq : pathEnd N q x = y) :
    endpointTransport ellPlus p x = endpointTransport ellPlus q x :=
  h x y p q hp hq

/-- Identity transport at equal endpoints (empty path). -/
theorem endpointTransport_refl
    (ellPlus : LabelledPositiveFamily N K V) (x : ArchiveRolePhaseGroup N) :
    endpointTransport ellPlus ([] : List ChainStep) x = LinearEquiv.refl K V :=
  labelledPathEval_nil ellPlus x

/-- Under `EndpointLocal`, any word that stays at `x` is the identity. -/
theorem endpointTransport_eq_refl_of_loop
    {ellPlus : LabelledPositiveFamily N K V} (h : EndpointLocal ellPlus)
    (x : ArchiveRolePhaseGroup N) (p : List ChainStep)
    (hp : pathEnd N p x = x) :
    endpointTransport ellPlus p x = LinearEquiv.refl K V :=
  endpointTransport_eq_of_EndpointLocal h x x p [] hp (by simp [pathEnd])

/-- Composition through an intermediate endpoint (append law). -/
theorem endpointTransport_comp
    (ellPlus : LabelledPositiveFamily N K V)
    (p q : List ChainStep) (x : ArchiveRolePhaseGroup N) :
    endpointTransport ellPlus (p ++ q) x =
      (endpointTransport ellPlus q (pathEnd N p x)).trans
        (endpointTransport ellPlus p x) :=
  labelledPathEval_append ellPlus p q x

/-- Inverse transport under endpoint reversal. -/
theorem endpointTransport_inv
    (ellPlus : LabelledPositiveFamily N K V)
    (p : List ChainStep) (x : ArchiveRolePhaseGroup N) :
    endpointTransport ellPlus ((p.map reverseStep).reverse) (pathEnd N p x) =
      (endpointTransport ellPlus p x).symm :=
  labelledPathEval_reverse ellPlus p x

/-! ## 3. Exact L = 2 slot firewall -/

/-- Parallel labels remain distinct `ChainStep` constructors. -/
theorem endpointLocal_L2_fwd_ne_bwd (r : Role) :
    ChainStep.fwd r ≠ ChainStep.bwd r :=
  labelled_L2_fwd_ne_bwd r

/-- At `L = 2`, `.fwd r` and `.bwd r` share an endpoint. -/
theorem endpointLocal_L2_fwd_bwd_same_endpoint (r : Role)
    (x : ArchiveRolePhaseGroup 0) :
    stepTarget 0 (.fwd r) x = stepTarget 0 (.bwd r) x :=
  labelled_L2_fwd_bwd_same_endpoint r x

/-- `EndpointLocal` forces the exact two-positive-link period at `L = 2`. -/
theorem endpointLocal_L2_period
    {ellPlus : LabelledPositiveFamily 0 K V} (h : EndpointLocal ellPlus)
    (x : ArchiveRolePhaseGroup 0) (r : Role) :
    (ellPlus (x + roleStep 0 r) r).trans (ellPlus x r) = LinearEquiv.refl K V :=
  labelled_L2_period_of_endpoint_descent (K := K) (V := V) ellPlus h x r

/-- Companion packaging `f.trans g = refl`. -/
theorem endpointLocal_L2_period'
    {ellPlus : LabelledPositiveFamily 0 K V} (h : EndpointLocal ellPlus)
    (x : ArchiveRolePhaseGroup 0) (r : Role) :
    (ellPlus x r).trans (ellPlus (x + roleStep 0 r) r) = LinearEquiv.refl K V :=
  labelled_L2_period_of_endpoint_descent' (K := K) (V := V) ellPlus h x r

/-! ## 4–5. Noncontractible-cycle / local-edge firewalls

Exact finite witness: constant scale-by-two family on `N = 1` (`L = 3`).
Adjacent forward plaquettes are flat (commuting constant letters), yet the
length-three positive role loop has holonomy `8 · id ≠ id`, so
`¬ EndpointLocal`. Local edge maps remain `LinearEquiv` by construction.
-/

/-- Multiplication-by-two on `ℚ` as a linear equivalence. -/
def scaleByTwoℚ : ℚ ≃ₗ[ℚ] ℚ :=
  DistribMulAction.toLinearEquiv ℚ ℚ (Units.mk0 (2 : ℚ) (by norm_num))

/-- Constant positive family with letter `scaleByTwoℚ` at every site/role. -/
def constantScaleFamily : LabelledPositiveFamily 1 ℚ ℚ :=
  fun _ _ => scaleByTwoℚ

/-- Adjacent forward-plaquette flatness on labelled words (same endpoints by
`roleTranslate_comm`). Not identified with `EndpointLocal`. -/
def LabelledPlaquetteFlat (ellPlus : LabelledPositiveFamily N K V) : Prop :=
  ∀ (x : ArchiveRolePhaseGroup N) (r s : Role),
    labelledPathEval ellPlus [ChainStep.fwd r, ChainStep.fwd s] x =
      labelledPathEval ellPlus [ChainStep.fwd s, ChainStep.fwd r] x

theorem constantScaleFamily_plaquetteFlat :
    LabelledPlaquetteFlat constantScaleFamily := by
  intro x r s
  simp [labelledPathEval, labelledStep, constantScaleFamily]

/-- Three forward steps in one role close at `N = 1` (`L = 3`). -/
theorem pathEnd_triple_fwd_N1 (r : Role) (x : ArchiveRolePhaseGroup 1) :
    pathEnd 1 [ChainStep.fwd r, ChainStep.fwd r, ChainStep.fwd r] x = x := by
  have hfib : archiveFibers 1 = 3 := by simp [archiveFibers]
  simp only [pathEnd, stepTarget, roleTranslatePlus_apply]
  ext s
  simp only [Pi.add_apply, roleStep]
  split_ifs with hs
  · have h3 : ((3 : ℕ) : ZMod (archiveFibers 1)) = 0 := by
      rw [hfib]; decide
    have h111 : (1 + 1 + 1 : ZMod (archiveFibers 1)) = (3 : ℕ) := by
      rw [hfib]; decide
    calc
      x s + 1 + 1 + 1 = x s + (1 + 1 + 1) := by abel
      _ = x s + ((3 : ℕ) : ZMod (archiveFibers 1)) := by rw [h111]
      _ = x s + 0 := by rw [h3]
      _ = x s := by simp
  · simp

theorem constantScaleFamily_triple_eval (r : Role) (x : ArchiveRolePhaseGroup 1) :
    labelledPathEval constantScaleFamily
        [ChainStep.fwd r, ChainStep.fwd r, ChainStep.fwd r] x =
      (scaleByTwoℚ.trans scaleByTwoℚ).trans scaleByTwoℚ := by
  simp [labelledPathEval, labelledStep, constantScaleFamily, LinearEquiv.refl_trans]

theorem scaleByTwoℚ_cube_ne_refl :
    (scaleByTwoℚ.trans scaleByTwoℚ).trans scaleByTwoℚ ≠ LinearEquiv.refl ℚ ℚ := by
  intro h
  have happly := congrArg (fun e : ℚ ≃ₗ[ℚ] ℚ => e (1 : ℚ)) h
  simp [scaleByTwoℚ, DistribMulAction.toLinearEquiv_apply] at happly
  norm_num at happly

theorem constantScaleFamily_triple_holonomy_ne_refl
    (r : Role) (x : ArchiveRolePhaseGroup 1) :
    labelledPathEval constantScaleFamily
        [ChainStep.fwd r, ChainStep.fwd r, ChainStep.fwd r] x ≠
      LinearEquiv.refl ℚ ℚ := by
  rw [constantScaleFamily_triple_eval]
  exact scaleByTwoℚ_cube_ne_refl

/-- Local plaquette-flatness does **not** imply `EndpointLocal`. -/
theorem flat_plaquettes_do_not_imply_EndpointLocal :
    LabelledPlaquetteFlat constantScaleFamily ∧ ¬ EndpointLocal constantScaleFamily := by
  refine ⟨constantScaleFamily_plaquetteFlat, ?_⟩
  intro h
  have htriv := EndpointLocal.to_trivial_labelled_holonomy h
  have hloop :=
    htriv (0 : ArchiveRolePhaseGroup 1)
      [ChainStep.fwd A, ChainStep.fwd A, ChainStep.fwd A]
      (pathEnd_triple_fwd_N1 A 0)
  exact constantScaleFamily_triple_holonomy_ne_refl A 0 hloop

/-- Local edge maps are already single-valued invertible `LinearEquiv`s;
that local fibre/relation condition does not force trivial labelled loop
holonomy / `EndpointLocal`. -/
theorem local_edge_LinearEquiv_does_not_imply_EndpointLocal :
    (∀ (x : ArchiveRolePhaseGroup 1) (r : Role),
        ∃ e : ℚ ≃ₗ[ℚ] ℚ, constantScaleFamily x r = e) ∧
      ¬ EndpointLocal constantScaleFamily := by
  refine ⟨?_, flat_plaquettes_do_not_imply_EndpointLocal.2⟩
  intro x r
  exact ⟨constantScaleFamily x r, rfl⟩

/-! ## 6. Converse independence (path descent ↛ graphification) -/

/-- Trivial (identity) positive letter family. -/
def trivialLabelledFamily : LabelledPositiveFamily N K V :=
  fun _ _ => LinearEquiv.refl K V

/-- Identity letters evaluate every word to `refl`. -/
theorem labelledPathEval_trivialLabelledFamily
    (p : List ChainStep) (x : ArchiveRolePhaseGroup N) :
    labelledPathEval (trivialLabelledFamily : LabelledPositiveFamily N K V) p x =
      LinearEquiv.refl K V := by
  induction p generalizing x with
  | nil =>
      rfl
  | cons s rest ih =>
      cases s with
      | fwd r =>
          simp [labelledPathEval, labelledStep, trivialLabelledFamily, ih]
      | bwd r =>
          simp [labelledPathEval, labelledStep, trivialLabelledFamily, ih]

theorem trivialLabelledFamily_EndpointLocal :
    EndpointLocal (trivialLabelledFamily : LabelledPositiveFamily N K V) := by
  refine EndpointLocal.of_trivial_labelled_holonomy _ ?_
  intro x p _hp
  exact labelledPathEval_trivialLabelledFamily p x

/-- Exact converse-independence witness.

The labelled path sector is endpoint-local (identity transport), while the
independent local A/e sector is the concrete duplicate-generator witness from
`A4DRelativeAEComparisonSpan`, for which strict graphification fails:
`¬ SpanCalibration duplicateB duplicateS`.

The two sectors are intentionally juxtaposed as a product witness; no coupling
between unrelated carriers is manufactured. -/
theorem endpointLocal_with_nonGraphAe :
    EndpointLocal
        (trivialLabelledFamily : LabelledPositiveFamily 0 ℝ ℝ) ∧
      ¬ A4DRelativeAEComparisonSpan.SpanCalibration
          A4DRelativeAEComparisonSpan.duplicateB
          A4DRelativeAEComparisonSpan.duplicateS := by
  exact ⟨trivialLabelledFamily_EndpointLocal,
    A4DRelativeAEComparisonSpan.duplicate_generator_no_strict⟩

/-- Path endpoint descent does not force local A/e graphification: the exact
identity-transport / duplicate-generator product witness realizes both at once. -/
theorem EndpointLocal_does_not_imply_ae_graphification :
    EndpointLocal
        (trivialLabelledFamily : LabelledPositiveFamily 0 ℝ ℝ) ∧
      ¬ A4DRelativeAEComparisonSpan.SpanCalibration
          A4DRelativeAEComparisonSpan.duplicateB
          A4DRelativeAEComparisonSpan.duplicateS :=
  endpointLocal_with_nonGraphAe

/-! ## 7. Endpoint quotient boundary

Under `EndpointLocal`, labelled path evaluation factors through ordered endpoint
pairs `(x, y)`. Intermediate `ChainStep` label/slot sequences with the same
endpoints are identified. This records what the classical quotient forgets; it
does **not** claim the quotient is physically mandatory.
-/

/-- Information forgotten by the endpoint quotient: distinct labelled words with
a common endpoint pair become equal as transports. -/
theorem EndpointLocal.forgets_labelled_path_slots
    {ellPlus : LabelledPositiveFamily N K V} (h : EndpointLocal ellPlus)
    (x y : ArchiveRolePhaseGroup N) (p q : List ChainStep)
    (hp : pathEnd N p x = y) (hq : pathEnd N q x = y) :
    labelledPathEval ellPlus p x = labelledPathEval ellPlus q x :=
  h x y p q hp hq

/-- Boundary note: the parent carrier remains `List ChainStep`; the quotient
collapses to endpoint-pair transport only after assuming `EndpointLocal`. -/
def EndpointQuotientBoundary (ellPlus : LabelledPositiveFamily N K V) : Prop :=
  EndpointLocal ellPlus →
    ∀ (x y : ArchiveRolePhaseGroup N) (p q : List ChainStep),
      pathEnd N p x = y → pathEnd N q x = y →
        labelledPathEval ellPlus p x = labelledPathEval ellPlus q x

theorem EndpointQuotientBoundary_holds
    (ellPlus : LabelledPositiveFamily N K V) :
    EndpointQuotientBoundary ellPlus :=
  fun h => h

end

end D0.Geometry
