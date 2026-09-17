import D0.Cosmology.PhysicalRedshiftDetectionPassport

/-!
# External physical-frequency representation interface

The finite cosmology module proves what follows from a preregistered self-return-covariant
frequency protocol.  This bridge file types the remaining external obligation: a concrete physical
apparatus must provide such a protocol before its readouts may be interpreted by the theorem.
-/

namespace D0.Bridge.BridgeAssumption

open D0.Cosmology.SelfUnfoldingObservableRelations
open D0.Cosmology.PhysicalRedshiftDetectionPassport

/-- Explicit application datum mapping a physical frequency-extraction procedure to the proved
finite protocol.  Constructing this value is external; no global axiom asserts that it exists. -/
structure PreregisteredSelfReturnFrequencyRepresentation where
  protocol : PreregisteredSelfReturnFrequencyProtocol

/-- Once the external representation is supplied, the physical/internal ratio theorem applies. -/
theorem represented_physicalOnePlusRedshift_eq_internal
    (R : PreregisteredSelfReturnFrequencyRepresentation)
    (c : FrequencyComparison) :
    physicalOnePlusRedshift R.protocol.toRawFrequencyProtocol c =
      onePlusInternalRedshift c.observerDepth c.emitterDepth :=
  physicalOnePlusRedshift_eq_internal R.protocol c

/-- The represented apparatus also inherits the one-tick redshift-drift law. -/
theorem represented_physical_redshift_drift_relation
    (R : PreregisteredSelfReturnFrequencyRepresentation)
    (c : FrequencyComparison) :
    physicalRedshift R.protocol.toRawFrequencyProtocol c.oneTickLater -
        physicalRedshift R.protocol.toRawFrequencyProtocol c =
      (D0.phi - 1) *
        (1 + physicalRedshift R.protocol.toRawFrequencyProtocol c) :=
  physical_redshift_drift_relation R.protocol c

end D0.Bridge.BridgeAssumption
