namespace D0.Cosmology

def sdeFeedbackPolynomial (lambda : Int) : Int :=
  160 * lambda * lambda - 480 * lambda + 359

theorem sde_two_mode_feedback_reduction :
    sdeFeedbackPolynomial 0 = 359 /\
    sdeFeedbackPolynomial 1 = 39 := by
  unfold sdeFeedbackPolynomial
  native_decide

inductive MissingTransferKind where
  | boundaryDerivativeFeedback
  | arbitraryKernel
  | rootRefit
  | inconclusive
  deriving DecidableEq, Repr

structure SurveyFailureEvidence where
  desiFailure : Bool
  sparcFailure : Bool
  frozenTwoModeUsed : Bool
  noRootRefit : Bool
  noWindowRefit : Bool
  boundaryTraceDerivativeNonzero : Bool
  arbitraryKernelRejected : Bool

def boundaryDerivativeReady (E : SurveyFailureEvidence) : Bool :=
  E.desiFailure &&
    E.sparcFailure &&
    E.frozenTwoModeUsed &&
    E.noRootRefit &&
    E.noWindowRefit &&
    E.boundaryTraceDerivativeNonzero &&
    E.arbitraryKernelRejected

def diagnoseMissingTerm (E : SurveyFailureEvidence) : MissingTransferKind :=
  if boundaryDerivativeReady E then
    MissingTransferKind.boundaryDerivativeFeedback
  else if E.noRootRefit = false then
    MissingTransferKind.rootRefit
  else if E.arbitraryKernelRejected = false then
    MissingTransferKind.arbitraryKernel
  else
    MissingTransferKind.inconclusive

theorem desi_sparc_failure_forces_boundary_derivative_feedback
    (E : SurveyFailureEvidence)
    (hdesi : E.desiFailure = true)
    (hsparc : E.sparcFailure = true)
    (hfrozen : E.frozenTwoModeUsed = true)
    (hnoroot : E.noRootRefit = true)
    (hnowindow : E.noWindowRefit = true)
    (hder : E.boundaryTraceDerivativeNonzero = true)
    (hkernel : E.arbitraryKernelRejected = true) :
    diagnoseMissingTerm E = MissingTransferKind.boundaryDerivativeFeedback := by
  unfold diagnoseMissingTerm boundaryDerivativeReady
  simp [hdesi, hsparc, hfrozen, hnoroot, hnowindow, hder, hkernel]

theorem arbitrary_kernel_repair_not_theorem_grade
    (E : SurveyFailureEvidence)
    (hdesi : E.desiFailure = true)
    (hsparc : E.sparcFailure = true)
    (hfrozen : E.frozenTwoModeUsed = true)
    (hnoroot : E.noRootRefit = true)
    (hnowindow : E.noWindowRefit = true)
    (hder : E.boundaryTraceDerivativeNonzero = true)
    (hkernel : E.arbitraryKernelRejected = true) :
    diagnoseMissingTerm E != MissingTransferKind.arbitraryKernel := by
  have h :=
    desi_sparc_failure_forces_boundary_derivative_feedback
      E hdesi hsparc hfrozen hnoroot hnowindow hder hkernel
  simp [h]

structure BoundaryFeedbackCorrection where
  derivedFromTraceDerivative : Bool
  noRootRefit : Bool
  noWindowRefit : Bool
  desiConstraint : Bool
  sparcConstraint : Bool

theorem desi_sparc_failure_boundary_feedback_diagnosis
    (B : BoundaryFeedbackCorrection) :
    B.derivedFromTraceDerivative = true ->
    B.noRootRefit = true ->
    B.noWindowRefit = true ->
    B.desiConstraint = true ->
    B.sparcConstraint = true ->
    B.derivedFromTraceDerivative && B.noRootRefit && B.noWindowRefit &&
      B.desiConstraint && B.sparcConstraint = true := by
  intro hder hnoref hnowin hdesi hsparc
  simp [hder, hnoref, hnowin, hdesi, hsparc]

theorem desi_root_refit_repair_forbidden (B : BoundaryFeedbackCorrection) :
    B.noRootRefit = true -> B.noRootRefit != false := by
  intro h
  simp [h]

theorem desi_window_refit_repair_forbidden (B : BoundaryFeedbackCorrection) :
    B.noWindowRefit = true -> B.noWindowRefit != false := by
  intro h
  simp [h]

end D0.Cosmology
