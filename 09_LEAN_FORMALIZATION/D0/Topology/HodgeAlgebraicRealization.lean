import D0.Foundation.M1Predicate

/-!
# D0-HODGE-M1-REDUCTIO-001 — §28 Hodge: non-algebraic ⇒ external catalogue (conditional on M1)

The §28 (Hodge conjecture) D0-reformulation: a κ-stable rational cohomology class is realized by
algebraic cycles, else a "non-algebraic index" is an exogenous parameter (forbidden by M1). This is
the FIRST conditional reductio theorem built on the formal M1 keystone
(`D0.Foundation.M1Predicate`): it instantiates `m1_alternative_needs_catalogue` for the realization
candidate space.

**Register (honest, BRIDGE-ASSUMPTIONS-EXPLICIT):** the reductio direction is a genuine proven
theorem — IF the canonical finite cohomology data M1-forces the algebraic realization
(hypothesis `algebraic_forced` = `ASSUMP-HODGE-ALGEBRAIC-FORCING`), THEN any non-algebraic-index
realization requires an external catalogue (rests on an unprovable input). The hypothesis itself —
that κ-stability *forces* algebraicity — is the §28 content and stays a named D0-internal target, NOT
derived here and NOT the ZFC Hodge statement. Two passports: physics (κ-stable cohomology class) +
Clay-math (§28 reductio core).
-/

namespace D0.Topology

open D0.Foundation D0.Matter

/-- Candidate realizations of a rational cohomology class: by algebraic cycles, or carrying a
non-algebraic index. -/
inductive HodgeRealization where
  | algebraic
  | nonAlgebraicIndex
  deriving DecidableEq

/-- A κ-stable rational Hodge class equipped with a finite selector over its candidate realizations,
together with the (named) hypothesis that the canonical finite cohomology data M1-forces the
algebraic realization. -/
structure KappaStableHodgeClass where
  realizationSelector : FiniteSelector HodgeRealization
  /-- `ASSUMP-HODGE-ALGEBRAIC-FORCING`: the canonical finite data strictly selects (M1-forces) the
  algebraic realization. This is the §28 content (κ-stable ⇒ algebraic), assumed here, not derived. -/
  algebraic_forced : StrictSelected realizationSelector HodgeRealization.algebraic

/-- The algebraic realization is M1-forced by the canonical finite data. -/
theorem hodge_algebraic_m1_forced (H : KappaStableHodgeClass) :
    M1Forced (fun x => StrictSelected H.realizationSelector x) HodgeRealization.algebraic :=
  selector_M1Forced H.realizationSelector HodgeRealization.algebraic H.algebraic_forced

/-- **§28 Hodge reductio (conditional on the M1-forcing hypothesis).** Given that the algebraic
realization is M1-forced, the non-algebraic-index realization requires an external catalogue — i.e.
asserting a genuinely non-algebraic class rests on an exogenous parameter (an unprovable input),
which M1 forbids. -/
theorem hodge_nonalgebraic_needs_catalogue (H : KappaStableHodgeClass) :
    RequiresExternalCatalogue (fun x => StrictSelected H.realizationSelector x)
      HodgeRealization.nonAlgebraicIndex :=
  m1_alternative_needs_catalogue (hodge_algebraic_m1_forced H)
    HodgeRealization.nonAlgebraicIndex (by decide)

/-- The algebraic realization is the unique M1-admissible one: no second realization is forced. -/
theorem hodge_algebraic_unique (H : KappaStableHodgeClass)
    (r : HodgeRealization) (hr : StrictSelected H.realizationSelector r) :
    r = HodgeRealization.algebraic :=
  (hodge_algebraic_m1_forced H).unique r hr

end D0.Topology
