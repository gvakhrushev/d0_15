import D0.Foundation.FutureExecution

/-! Native #334 extension extracted without changing the accepted base owner.
Original declarations: `03_FORMALIZATION/D0/Foundation/EmpiricalTheoryFactorization.lean` at
`07f2f2b15b7050a612d0075aa73db8dc46087a95`.
The shared definitions are imported from their maintained main modules. -/

namespace D0.Foundation.EmpiricalTheoryFactorization

open D0.Foundation.M1ClassAdmissibility

/-- A purely uncoupled hidden Bool center cannot be FULLY M1-faithful
on the enlarged raw state carrier.  All original future experiments
see identical results from its two genuinely distinct raw labels. -/
theorem FutureExecution.uncoupledCenter_not_future_complete
    (F : FutureExecution) (s : F.State) :
    ¬ Function.Injective (F.uncoupledCenter).profile := by
  intro hinj
  have he : (s, false) = (s, true) :=
    hinj (F.uncoupledCenter_profile_independent s false true)
  have hb : (false : Bool) = true := congrArg Prod.snd he
  cases hb

/-- A physically distinct pair in any complete-future verified
execution MUST differ on at least ONE original future test word.
All test words are finite words of the ALREADY SUPPLIED actions;
the proof does not invent a new primitive witness. -/
theorem FutureExecution.future_complete_forces_a_test
    (F : FutureExecution)
    (complete : Function.Injective F.profile)
    {s t : F.State} (different : s ≠ t) :
    ∃ w : List F.Action, ∃ q : F.Test,
      F.observe (F.run w s) q ≠ F.observe (F.run w t) q := by
  classical
  by_contra hn
  push_neg at hn
  apply different
  apply complete
  funext w q
  exact hn w q


end D0.Foundation.EmpiricalTheoryFactorization
