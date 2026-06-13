import D0.Dynamics.GaloisConjugateBalance
import D0.Bridge.TickGaugeLorentz

namespace D0.Physics

/-!
QUASI-006: Galois/Lorentz signature integration.

The active/archive Galois balance and the terminal Lorentz-facing role
signature are checked together here.  This is an integration owner, not a
smooth-spacetime import.
-/

/-- Finite Galois/Lorentz signature closure package. -/
structure GaloisLorentzSignatureClosure where
  integer_trace_layers :
    D0.Dynamics.ActiveArchiveTrace 2 = 3 /\
    D0.Dynamics.ActiveArchiveTrace 3 = -4 /\
    D0.Dynamics.ActiveArchiveTrace 5 = -11
  determinant_balance :
    forall n : Nat,
      Matrix.det (D0.Dynamics.T ^ n) * Matrix.det (D0.Dynamics.T ^ n) = 1
  signature_closed : D0.roleSignature = (1, 3)
  no_euclidean_export : D0.roleSignature ≠ (4, 0)
  no_split_export : D0.roleSignature ≠ (2, 2)

/-- Concrete finite Galois/Lorentz signature closure. -/
def galoisLorentzSignatureClosure :
    GaloisLorentzSignatureClosure where
  integer_trace_layers := D0.Dynamics.d0_integer_trace_layers
  determinant_balance := D0.Dynamics.toral_volume_conservation_square
  signature_closed := D0.roleSignature_eq_1_3
  no_euclidean_export := D0.no_euclidean_SO4
  no_split_export := D0.no_split_SO22

/-- The finite Galois branch balance is compatible only with the D0 `(1,3)` role signature. -/
theorem galois_lorentz_signature_closed :
    D0.Dynamics.ActiveArchiveTrace 2 = 3 /\
    D0.Dynamics.ActiveArchiveTrace 3 = -4 /\
    D0.Dynamics.ActiveArchiveTrace 5 = -11 /\
    (forall n : Nat,
      Matrix.det (D0.Dynamics.T ^ n) * Matrix.det (D0.Dynamics.T ^ n) = 1) /\
    D0.roleSignature = (1, 3) /\
    D0.roleSignature ≠ (4, 0) /\
    D0.roleSignature ≠ (2, 2) := by
  exact
    ⟨galoisLorentzSignatureClosure.integer_trace_layers.1,
      galoisLorentzSignatureClosure.integer_trace_layers.2.1,
      galoisLorentzSignatureClosure.integer_trace_layers.2.2,
      galoisLorentzSignatureClosure.determinant_balance,
      galoisLorentzSignatureClosure.signature_closed,
      galoisLorentzSignatureClosure.no_euclidean_export,
      galoisLorentzSignatureClosure.no_split_export⟩

end D0.Physics
