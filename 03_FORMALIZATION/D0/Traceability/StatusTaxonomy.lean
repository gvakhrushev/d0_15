namespace D0.Traceability

inductive D0Status
  | CORE_CLOSED
  | CERT_CLOSED
  | NO_GO
  | BRIDGE_CALIBRATION
  | EMPIRICAL_PASSPORT
  | EXTERNAL_DATA_REQUIRED
  deriving DecidableEq, Repr

def canPromoteTo (s1 s2 : D0Status) : Prop :=
  match s1, s2 with
  | D0Status.EMPIRICAL_PASSPORT, D0Status.CORE_CLOSED => False
  | D0Status.EXTERNAL_DATA_REQUIRED, D0Status.CORE_CLOSED => False
  | D0Status.BRIDGE_CALIBRATION, D0Status.CORE_CLOSED => False
  | _, _ => True

theorem external_likelihood_cannot_promote_to_core_closed :
    ¬ (canPromoteTo D0Status.EMPIRICAL_PASSPORT D0Status.CORE_CLOSED) := by
  unfold canPromoteTo
  intro h
  exact h

end D0.Traceability
