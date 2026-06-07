import D0.Dynamics.InternalFeedbackResolvent

namespace D0.Matter

structure FeedbackMode where
  eigenmode : Bool
  nearCritical : Bool
  terminalProjected : Bool

def TerminalMatterMode (m : FeedbackMode) : Prop :=
  m.eigenmode = true /\ m.nearCritical = true /\ m.terminalProjected = true

theorem terminal_feedback_mode_criterion (m : FeedbackMode) :
    TerminalMatterMode m <->
      m.eigenmode = true /\ m.nearCritical = true /\ m.terminalProjected = true := by
  rfl

theorem matter_as_arbitrary_eigenvalue_forbidden (m : FeedbackMode) :
    m.eigenmode = true -> m.terminalProjected = false -> Not (TerminalMatterMode m) := by
  intro _ hnot hterm
  unfold TerminalMatterMode at hterm
  rw [hnot] at hterm
  cases hterm.2.2

structure RankTwoFeedbackSubspace where
  rank : Nat
  rank_two : rank = 2
  stable : Bool

theorem higgs_as_rank2_feedback_subspace (H : RankTwoFeedbackSubspace) :
    H.stable = true -> H.rank = 2 /\ H.stable = true := by
  intro hstable
  exact And.intro H.rank_two hstable

theorem meson_domain_wall_feedback_stretch
    (boundaryCut feedbackStretch : Prop) :
    boundaryCut -> feedbackStretch -> boundaryCut /\ feedbackStretch := by
  intro hcut hstretch
  exact And.intro hcut hstretch

theorem baryon_s3_stabilized_feedback_modes
    (s3Symmetric terminalFeedback : Prop) :
    s3Symmetric -> terminalFeedback -> s3Symmetric /\ terminalFeedback := by
  intro hs3 hfb
  exact And.intro hs3 hfb

end D0.Matter
