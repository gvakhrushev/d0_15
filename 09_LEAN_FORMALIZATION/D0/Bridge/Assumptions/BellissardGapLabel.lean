namespace D0.Bridge

namespace BridgeAssumption

/-- External owner of the Bellissard gap-labelling theorem used by the
genericity certificate.  The theorem identifies the allowed integrated
density-of-states values with the frequency module of the hull.  D0 does not
re-prove this K-theoretic statement in Lean. -/
structure BellissardGapLabelling where
  frequencyModuleConstraint : Prop
  cited : frequencyModuleConstraint

theorem bellissard_gap_labelling_conditional
    (h : BellissardGapLabelling) :
    h.frequencyModuleConstraint :=
  h.cited

end BridgeAssumption

abbrev BellissardGapLabelling := BridgeAssumption.BellissardGapLabelling

end D0.Bridge
