import D0.Geometry.FiniteA2EinsteinResponse
import D0.Geometry.GradedBianchiClosure

namespace D0.Geometry

/-!
# Finite Bianchi → Einstein-tensor selection no-go

**Theorem (the negative control, now provable).**  Let `G` be an admissible response tensor
(symmetric, divergence-balanced) and let `T` be a conserved source whose coupling to `G` is
nonzero.  Then:

1. every **scalar-only** response `κ·𝟙` decouples from `T` completely
   (`coupling = 0` — `scalar_coupling_of_conserved`);
2. hence scalar-only cannot reproduce the full gravity coupling profile of `G`.

Together with the graded Bianchi closure (divergence-balance is preserved by the Einstein
transform) this is the finite-stage form of "gravity couples through the Einstein class":
conserved sources are blind to pure-trace parts (`trace_invisible_to_conserved`) and entirely
blind to scalar-only responses, while the divergence-balanced part carries all the coupling.

Honest scope: finite combinatorics over `N`; the identification of `coupling` with laboratory
stress-energy overlap inherits the typed bridge discipline of the dyad house.  SEMANTICS NOTE:
the finite-stage `einsteinTransform` subtracts the GLOBAL MEAN entry (total response vanishes);
it is a mean-null normalization, NOT the metric-trace adjustment — that refinement is queued.
The witness-side existence (for every non-flat `G` there IS such a conserved source `T`,
constructible by two-point detectors) is also queued as follow-up; the theorem here takes `T`
as input.
-/

variable {N : Type} [Fintype N] [DecidableEq N] [Nonempty N]

/-- Bianchi closure at the response level: admissible responses are divergence-balanced,
    and stay so after the Einstein transform. -/
theorem finite_bianchi_forces_divergence_free_macro_tensor
    (R : FiniteA2ResponseTensor N) :
    IsDivergenceBalanced (einsteinTransform R.G) :=
  einstein_balanced_of_balanced R.hdiv

/-- **Main no-go.**  Given an admissible response `G`, a conserved source `T` coupling to it
    nontrivially, and any scalar `κ`: the scalar-only response decouples from `T` while `G`
    does not.  Scalar-only (and, by `einstein_transform_coupling_eq`'s converse reading,
    anything differing only in its trace part) cannot reproduce the full coupling profile. -/
theorem ricci_or_scalar_only_not_full_gravity_response
    (G : FiniteA2ResponseTensor N)
    (T : N → N → ℝ)
    (hTcons : IsConservedSource T)
    (hGcoup : coupling G.G T ≠ 0)
    (κ : ℝ) :
    coupling (fun _ _ => κ) T = 0
      ∧ coupling G.G T ≠ 0
      ∧ coupling (fun _ _ => κ) T ≠ coupling G.G T := by
  refine ⟨scalar_coupling_of_conserved κ T hTcons, hGcoup, ?_⟩
  intro heq
  rw [scalar_coupling_of_conserved κ T hTcons] at heq
  exact hGcoup heq.symm

end D0.Geometry
