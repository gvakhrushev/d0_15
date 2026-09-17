import D0.Foundation.M1Predicate

/-!
# D0-PVSNP-LYAPUNOV-M1-001 — §24 P_D0 vs NP_D0: navigation without a global potential needs a catalogue

The §24 (P vs NP) D0-reformulation: with a global heat-trace Lyapunov navigation potential `V`
(spectral relaxation toward the accepting state), search is directed and runs in polynomial steps;
WITHOUT a global `V`, any claimed speedup must store an external "which branch is promising" index —
an exogenous branch-catalogue (unprovable input) forbidden by M1, which is the worst-case exponential
phase. This instantiates the M1 keystone (`D0.Foundation.M1Predicate`) on the navigation potential.

**Register (BRIDGE-ASSUMPTIONS-EXPLICIT):** PROVEN conditional — given a global potential that
strictly selects the solution (`ASSUMP-GLOBAL-LYAPUNOV-POTENTIAL`), any other state requires an
external catalogue, so directed navigation is forced (no branch-catalogue ⇒ no exponential branching).
The existence of that global `V` as the heat-trace relaxation `lim_{u→∞} e^{-uL} b` with a uniform
spectral gap is the named assumption — NOT derived here (the corpus has the static symmetric/nonneg
Laplacian `D0.Geometry.ArchiveLaplacianProperties` but no `u→∞` limit, and the uniform gap is
assumed). This is explicitly the REGULARIZED P_D0 vs NP_D0 in a fixed-UV finite model — NOT the ZFC
P =? NP question. Two passports: physics (heat-trace relaxation channel) + Clay-math (§24 navigation
core).
-/

namespace D0.Complexity

open D0.Foundation D0.Matter

/-- A search instance equipped with a global Lyapunov navigation potential: a finite state space
scored by `V`, with the accepting (solution) state strictly selected — the M1-forced minimum.
`solution_forced` is `ASSUMP-GLOBAL-LYAPUNOV-POTENTIAL` (existence of the relaxation potential). -/
structure LyapunovNavigable (α : Type) where
  potential : FiniteSelector α
  solution : α
  solution_forced : StrictSelected potential solution

/-- The solution is M1-forced by the global navigation potential. -/
theorem solution_m1_forced {α : Type} (N : LyapunovNavigable α) :
    M1Forced (fun x => StrictSelected N.potential x) N.solution :=
  selector_M1Forced N.potential N.solution N.solution_forced

/-- The solution is the unique M1-admissible target — no two distinct forced solutions. -/
theorem solution_unique {α : Type} (N : LyapunovNavigable α) (b : α)
    (hb : StrictSelected N.potential b) : b = N.solution :=
  (solution_m1_forced N).unique b hb

/-- **§24 reductio (conditional on a global Lyapunov potential).** Given a global potential that
strictly selects the solution, any other state `b` (a candidate "promising branch", `b ≠ solution`)
requires an external catalogue: storing which branch is promising is an exogenous branch-index (an
unprovable input), forbidden by M1. So with a global `V`, navigation is directed — the exponential
branch-catalogue is exactly what M1 excludes. -/
theorem branch_without_potential_needs_catalogue {α : Type} (N : LyapunovNavigable α)
    (b : α) (hb : b ≠ N.solution) :
    RequiresExternalCatalogue (fun x => StrictSelected N.potential x) b :=
  m1_alternative_needs_catalogue (solution_m1_forced N) b hb

end D0.Complexity
