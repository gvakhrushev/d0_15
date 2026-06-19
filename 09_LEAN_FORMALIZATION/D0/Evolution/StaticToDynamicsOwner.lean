import D0.Evolution.JYNoncommutativeOrderObstruction
import D0.Evolution.FeshbachSchurTimeDelayOwner
import D0.Evolution.PhiFractalTickDynamics

/-!
# D0-STATIC-TO-DYNAMICS-OWNER-001 — dynamics is forced by finite self-readout, not primitive

The combined owner of the static-to-dynamics chain. It composes the three block owners — each a real
finite theorem proved in its own module — into one statement:

```
static finite scene
  -> noncommuting self-readout  : [J,Y] ≠ 0           (Block I, JYNoncommutativeOrderObstruction)
  -> ordered registration       : the time arrow      (Block I)
  -> Feshbach archive delay      : tick index = Neumann order k   (Block II, FeshbachSchurTimeDelayOwner)
  -> φ fractal tick weight       : A_{k+1} = φ⁻¹ A_k   (Block III, PhiFractalTickDynamics)
  -> continuous envelope         : A(s)=A₀ e^{-s log φ} (Block III, reusing D0-IM-003 / D0-PHI-LADDER-SEMIGROUP-001)
```

No primitive time object, external clock, or SI unit (c, h, ħ, seconds) enters: the only content is the
dimensionless integer commutator `[J,Y]`, the finite Neumann tick index, and the φ-ladder weight.

HONEST SCOPE. Each conjunct is a genuine proved owner. The combined claim closes the *mechanism chain*
at the witness/finite level. The UNIVERSAL obstruction (that **every** commuting self-readout on **any**
carrier erases order) is NOT proven here — it is the named residual
`JY-UNIVERSAL-COMMUTING-READOUT-OBSTRUCTION` carried on `D0-JY-NONCOMMUTATIVE-ORDER-OBSTRUCTION-001`; the
Neumann tick identity holds on the resolvent/convergence domain; the envelope owner is the reused
`D0-PHI-LADDER-SEMIGROUP-001`. No grand "dynamics fully derived" claim is made.
-/

namespace D0.Evolution.StaticToDynamicsOwner

open D0
open D0.IM
open D0.Evolution.JYNoncommutativeOrderObstruction
open D0.Evolution.FeshbachSchurTimeDelayOwner
open D0.Evolution.PhiFractalTickDynamics

/-- **D0-STATIC-TO-DYNAMICS-OWNER-001.** The three forced finite facts of the static-to-dynamics chain,
each discharged by its block owner: (I) the self-readout commutator is nonzero `[J,Y] ≠ 0`; (II) the
Feshbach archive-delay tick index equals the Neumann order `k`; (III) each tick multiplies the active
amplitude by `φ⁻¹`. None is a primitive input; all three are theorems. -/
theorem static_to_dynamics_owner_closed :
    (J * Y ≠ Y * J)
    ∧ (∀ k : Nat, (neumannTerm k).archiveCirculations = k)
    ∧ (∀ k : ℕ, ladderAmount (k + 1) = ladderAmount k * phi⁻¹) :=
  ⟨jy_commutator_ne_zero,
   neumann_term_k_has_k_archive_circulations,
   archive_tick_multiplies_by_phi_inv⟩

/-- **D0-DYNAMICS-NOT-PRIMITIVE-CERT-CLOSED-001.** Dynamics is not a primitive D0 input: the order that
makes a "tick" meaningful is forced by the nonzero self-readout commutator (Block I), and the tick's
own weight `φ⁻¹` is fixed by the detector self-return split — both are derived, not postulated. Proved
by projecting the combined owner. -/
theorem dynamics_not_primitive :
    (J * Y ≠ Y * J)
    ∧ (∀ k : ℕ, ladderAmount (k + 1) = ladderAmount k * phi⁻¹) :=
  ⟨static_to_dynamics_owner_closed.1, static_to_dynamics_owner_closed.2.2⟩

end D0.Evolution.StaticToDynamicsOwner
