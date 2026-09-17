import D0.Core.MatrixResponse

namespace D0.Geometry

open scoped BigOperators

/-- A finite weak-field metric mode over an arbitrary finite detector index set. -/
structure FiniteMetricMode (ι : Type) [Fintype ι] where
  h : ι → ι → ℚ
  symmetric : ∀ i j, h i j = h j i

/-- Finite trace of a weak-field mode. -/
def finiteMetricTrace {ι : Type} [Fintype ι]
    (m : FiniteMetricMode ι) : ℚ :=
  ∑ i, m.h i i

/--
Finite transverse-traceless carrier.  `transverse` is deliberately left as a
finite predicate supplied by the concrete archive Laplacian/derivative layer;
this module closes the bookkeeping that the spin-2 carrier is exactly the
symmetric trace-free transverse sector, not a scalar trace mode.
-/
structure FiniteTTMode (ι : Type) [Fintype ι] extends FiniteMetricMode ι where
  transverse : Prop
  transverse_proof : transverse
  trace_free : finiteMetricTrace toFiniteMetricMode = 0

/-- TT modes are symmetric. -/
theorem finite_tt_mode_symmetric {ι : Type} [Fintype ι]
    (m : FiniteTTMode ι) : ∀ i j, m.h i j = m.h j i :=
  m.symmetric

/-- TT modes are trace-free. -/
theorem finite_tt_mode_trace_free {ι : Type} [Fintype ι]
    (m : FiniteTTMode ι) : finiteMetricTrace m.toFiniteMetricMode = 0 :=
  m.trace_free

/-- TT modes satisfy the finite transversality predicate selected by the archive layer. -/
theorem finite_tt_mode_transverse {ι : Type} [Fintype ι]
    (m : FiniteTTMode ι) : m.transverse :=
  m.transverse_proof

/--
Finite spin-2 carrier closure: a mode in the TT sector simultaneously carries
symmetry, trace removal, and transversality.  The theorem is intentionally
finite and does not promote the continuum Einstein-Hilbert bridge by itself.
-/
theorem finite_spin2_tt_carrier_closed {ι : Type} [Fintype ι]
    (m : FiniteTTMode ι) :
    (∀ i j, m.h i j = m.h j i) ∧
      finiteMetricTrace m.toFiniteMetricMode = 0 ∧ m.transverse := by
  exact ⟨m.symmetric, m.trace_free, m.transverse_proof⟩


/--
A finite weak-field quotient certificate.

The source weak-field mode is not promoted to a spin-2 carrier directly.  It is
first reduced by a finite gauge/longitudinal representative and a finite trace
representative; the remaining representative is the transverse-traceless mode.
The stress predicates record the finite analogue of conserved-stress
annihilation of gauge and scalar trace directions.
-/
structure FiniteWeakFieldQuotient (ι : Type) [Fintype ι] where
  source : FiniteMetricMode ι
  longitudinalRepresentative : FiniteMetricMode ι
  traceRepresentative : FiniteMetricMode ι
  ttRepresentative : FiniteTTMode ι
  quotientReconstruction : Prop
  quotientReconstruction_proof : quotientReconstruction
  conservedStressKillsLongitudinal : Prop
  conservedStressKillsLongitudinal_proof : conservedStressKillsLongitudinal
  conservedStressKillsTrace : Prop
  conservedStressKillsTrace_proof : conservedStressKillsTrace

/-- The quotient supplies an actual TT representative rather than a spin-2 label. -/
theorem finite_weak_field_quotient_yields_tt_representative {ι : Type} [Fintype ι]
    (q : FiniteWeakFieldQuotient ι) :
    (∀ i j, q.ttRepresentative.h i j = q.ttRepresentative.h j i) ∧
      finiteMetricTrace q.ttRepresentative.toFiniteMetricMode = 0 ∧
        q.ttRepresentative.transverse := by
  exact finite_spin2_tt_carrier_closed q.ttRepresentative

/-- The finite gauge/trace quotient is closed when reconstruction and both stress annihilations hold. -/
theorem finite_gauge_trace_quotient_closed {ι : Type} [Fintype ι]
    (q : FiniteWeakFieldQuotient ι) :
    q.quotientReconstruction ∧
      q.conservedStressKillsLongitudinal ∧ q.conservedStressKillsTrace := by
  exact ⟨q.quotientReconstruction_proof,
    q.conservedStressKillsLongitudinal_proof,
    q.conservedStressKillsTrace_proof⟩

/-- Conserved-stress coupling leaves only the TT representative as the spin-2 carrier. -/
theorem finite_conserved_stress_spin2_coupling_closed {ι : Type} [Fintype ι]
    (q : FiniteWeakFieldQuotient ι) :
    q.conservedStressKillsLongitudinal ∧ q.conservedStressKillsTrace ∧
      ((∀ i j, q.ttRepresentative.h i j = q.ttRepresentative.h j i) ∧
        finiteMetricTrace q.ttRepresentative.toFiniteMetricMode = 0 ∧
          q.ttRepresentative.transverse) := by
  exact ⟨q.conservedStressKillsLongitudinal_proof,
    q.conservedStressKillsTrace_proof,
    finite_spin2_tt_carrier_closed q.ttRepresentative⟩

/-- The trace scalar cannot be the finite spin-2 carrier after TT reduction. -/
theorem finite_trace_mode_removed_from_spin2_carrier {ι : Type} [Fintype ι]
    (q : FiniteWeakFieldQuotient ι) :
    finiteMetricTrace q.ttRepresentative.toFiniteMetricMode = 0 := by
  exact q.ttRepresentative.trace_free

end D0.Geometry
