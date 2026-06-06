import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic

namespace D0.Geometry

set_option linter.unusedSimpArgs false

/-- Four-role terminal carrier for the concrete finite spin-2 operator. -/
abbrev Role4 : Type := Fin 4

/-- Rational 4x4 matrices on the terminal carrier. -/
abbrev QMat4 := Matrix Role4 Role4 Rat

/-- Terminal Lorentz-signature metric diag(1,-1,-1,-1). -/
def eta4 : QMat4 :=
  fun i j =>
    if i = j then
      if i.val = 0 then 1 else -1
    else 0

/-- Null propagation covector k=(1,1,0,0). -/
def k4 : Role4 -> Rat :=
  fun i => if (i.val == 0) || (i.val == 1) then 1 else 0

/-- Terminal time covector u=(1,0,0,0). -/
def u4 : Role4 -> Rat :=
  fun i => if i.val == 0 then 1 else 0

/-- Symmetric rational perturbation on the four-role carrier. -/
structure SymPert4 where
  h : QMat4
  symm : h.transpose = h

/-- Equality of symmetric perturbations is equality of their matrix fields. -/
@[ext] theorem SymPert4.ext {a b : SymPert4} (hh : a.h = b.h) :
    a = b := by
  cases a
  cases b
  simp at hh
  subst hh
  rfl

/-- Entrywise symmetry of a `SymPert4`. -/
theorem SymPert4.entry_symm (h : SymPert4) (i j : Role4) :
    h.h i j = h.h j i := by
  have hs := congrArg (fun M : QMat4 => M i j) h.symm
  have hji : h.h j i = h.h i j := by
    simpa [Matrix.transpose_apply] using hs
  exact hji.symm

/-- Zero perturbation. -/
def zeroSymPert4 : SymPert4 where
  h := 0
  symm := by
    ext i j
    simp

/-- Lorentz trace pairing `<A,B> = Tr(A eta B eta)`. -/
def pairing4 (A B : QMat4) : Rat :=
  Matrix.trace (A * eta4 * B * eta4)

/-- Finite Lorentz trace. -/
def finiteTrace4 (h : SymPert4) : Rat :=
  Matrix.trace (h.h * eta4)

/-- Finite divergence along the null propagation covector. -/
def finiteDivergence4 (h : SymPert4) : Role4 -> Rat :=
  (h.h * eta4).mulVec k4

/-- Finite terminal-time projection. -/
def timeProjection4 (h : SymPert4) : Role4 -> Rat :=
  (h.h * eta4).mulVec u4

def TraceFree4 (h : SymPert4) : Prop :=
  finiteTrace4 h = 0

def Transverse4 (h : SymPert4) : Prop :=
  finiteDivergence4 h = 0

def TimeOrthogonal4 (h : SymPert4) : Prop :=
  timeProjection4 h = 0

def IsTT4 (h : SymPert4) : Prop :=
  TraceFree4 h /\ Transverse4 h /\ TimeOrthogonal4 h

/-- Plus polarization on the transverse 2-3 block. -/
def ePlus4 : QMat4 :=
  fun i j =>
    if (i.val == 2) && (j.val == 2) then 1
    else if (i.val == 3) && (j.val == 3) then -1
    else 0

/-- Cross polarization on the transverse 2-3 block. -/
def eCross4 : QMat4 :=
  fun i j =>
    if ((i.val == 2) && (j.val == 3)) ||
        ((i.val == 3) && (j.val == 2)) then 1
    else 0

theorem ePlus4_symm : ePlus4.transpose = ePlus4 := by
  ext i j
  fin_cases i <;> fin_cases j <;> native_decide

theorem eCross4_symm : eCross4.transpose = eCross4 := by
  ext i j
  fin_cases i <;> fin_cases j <;> native_decide

def ePlusPert4 : SymPert4 where
  h := ePlus4
  symm := ePlus4_symm

def eCrossPert4 : SymPert4 where
  h := eCross4
  symm := eCross4_symm

theorem pairing4_ePlus_left (h : QMat4) :
    pairing4 ePlus4 h = h 2 2 - h 3 3 := by
  simp [pairing4, Matrix.trace, Matrix.mul_apply, eta4, ePlus4, Fin.sum_univ_four]
  ring

theorem pairing4_eCross_left (h : QMat4) :
    pairing4 eCross4 h = h 2 3 + h 3 2 := by
  simp [pairing4, Matrix.trace, Matrix.mul_apply, eta4, eCross4, Fin.sum_univ_four]
  ring

theorem pairing4_ePlus_right (h : QMat4) :
    pairing4 h ePlus4 = h 2 2 - h 3 3 := by
  simp [pairing4, Matrix.trace, Matrix.mul_apply, eta4, ePlus4, Fin.sum_univ_four]
  ring

theorem pairing4_eCross_right (h : QMat4) :
    pairing4 h eCross4 = h 2 3 + h 3 2 := by
  simp [pairing4, Matrix.trace, Matrix.mul_apply, eta4, eCross4, Fin.sum_univ_four]

theorem ePlus4_norm :
    pairing4 ePlus4 ePlus4 = 2 := by
  native_decide

theorem eCross4_norm :
    pairing4 eCross4 eCross4 = 2 := by
  native_decide

theorem ePlus_eCross_orthogonal :
    pairing4 ePlus4 eCross4 = 0 := by
  native_decide

/-- Scale a symmetric perturbation. -/
def scaleSymPert4 (a : Rat) (h : SymPert4) : SymPert4 where
  h := a • h.h
  symm := by
    rw [Matrix.transpose_smul, h.symm]

/-- Add two symmetric perturbations. -/
def addSymPert4 (a b : SymPert4) : SymPert4 where
  h := a.h + b.h
  symm := by
    rw [Matrix.transpose_add, a.symm, b.symm]

/-- Concrete finite TT projector onto span(ePlus,eCross). -/
def PiTT4 (h : SymPert4) : SymPert4 :=
  addSymPert4
    (scaleSymPert4 ((pairing4 ePlus4 h.h) / 2) ePlusPert4)
    (scaleSymPert4 ((pairing4 eCross4 h.h) / 2) eCrossPert4)

theorem PiTT4_idempotent (h : SymPert4) :
    PiTT4 (PiTT4 h) = PiTT4 h := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [PiTT4, addSymPert4, scaleSymPert4, ePlusPert4, eCrossPert4,
      pairing4_ePlus_left, pairing4_eCross_left, ePlus4, eCross4]

theorem PiTT4_tracefree (h : SymPert4) :
    TraceFree4 (PiTT4 h) := by
  simp [TraceFree4, finiteTrace4, PiTT4, addSymPert4, scaleSymPert4,
    ePlusPert4, eCrossPert4, pairing4_ePlus_left, pairing4_eCross_left,
    Matrix.trace, Matrix.mul_apply, eta4, ePlus4, eCross4, Fin.sum_univ_four]

theorem PiTT4_transverse (h : SymPert4) :
    Transverse4 (PiTT4 h) := by
  ext i
  fin_cases i <;>
    simp [finiteDivergence4, PiTT4, addSymPert4, scaleSymPert4,
      ePlusPert4, eCrossPert4, pairing4_ePlus_left, pairing4_eCross_left,
      Matrix.mulVec, dotProduct, Matrix.mul_apply, eta4, k4, ePlus4, eCross4,
      Fin.sum_univ_four]

theorem PiTT4_time_orthogonal (h : SymPert4) :
    TimeOrthogonal4 (PiTT4 h) := by
  ext i
  fin_cases i <;>
    simp [timeProjection4, PiTT4, addSymPert4, scaleSymPert4,
      ePlusPert4, eCrossPert4, pairing4_ePlus_left, pairing4_eCross_left,
      Matrix.mulVec, dotProduct, Matrix.mul_apply, eta4, u4, ePlus4, eCross4,
      Fin.sum_univ_four]

theorem PiTT4_is_tt (h : SymPert4) :
    IsTT4 (PiTT4 h) := by
  exact ⟨PiTT4_tracefree h, PiTT4_transverse h, PiTT4_time_orthogonal h⟩

/-- Pure trace mode. -/
def traceMode4 (phi : Rat) : SymPert4 where
  h := phi • eta4
  symm := by
    ext i j
    fin_cases i <;> fin_cases j <;> simp [eta4]

/-- Finite symmetric gauge image generated by a vector field `xi`. -/
def finiteSymGrad4 (xi : Role4 -> Rat) : SymPert4 where
  h := fun i j => k4 i * xi j + xi i * k4 j
  symm := by
    ext i j
    simp [Matrix.transpose_apply]
    ring

theorem PiTT4_kills_trace (phi : Rat) :
    PiTT4 (traceMode4 phi) = zeroSymPert4 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [PiTT4, traceMode4, zeroSymPert4, addSymPert4, scaleSymPert4,
      ePlusPert4, eCrossPert4, pairing4_ePlus_left, pairing4_eCross_left,
      eta4, ePlus4, eCross4]

theorem PiTT4_kills_gauge (xi : Role4 -> Rat) :
    PiTT4 (finiteSymGrad4 xi) = zeroSymPert4 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [PiTT4, finiteSymGrad4, zeroSymPert4, addSymPert4, scaleSymPert4,
      ePlusPert4, eCrossPert4, pairing4_ePlus_left, pairing4_eCross_left,
      k4, ePlus4, eCross4]

theorem PiTT4_zero :
    PiTT4 zeroSymPert4 = zeroSymPert4 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [PiTT4, zeroSymPert4, addSymPert4, scaleSymPert4, ePlusPert4,
      eCrossPert4, pairing4_ePlus_left, pairing4_eCross_left, ePlus4, eCross4]

/-- Concrete TT wave operator: project, evolve, project again. -/
def WTT4 (Lsym : SymPert4 -> SymPert4) (h : SymPert4) : SymPert4 :=
  PiTT4 (Lsym (PiTT4 h))

theorem WTT4_preserves_tt
    (Lsym : SymPert4 -> SymPert4)
    (h : SymPert4) :
    IsTT4 (WTT4 Lsym h) := by
  exact PiTT4_is_tt (Lsym (PiTT4 h))

theorem WTT4_kills_trace
    (Lsym : SymPert4 -> SymPert4)
    (phi : Rat)
    (hL_zero : Lsym zeroSymPert4 = zeroSymPert4) :
    WTT4 Lsym (traceMode4 phi) = zeroSymPert4 := by
  rw [WTT4, PiTT4_kills_trace, hL_zero]
  exact PiTT4_zero

theorem WTT4_kills_gauge
    (Lsym : SymPert4 -> SymPert4)
    (xi : Role4 -> Rat)
    (hL_zero : Lsym zeroSymPert4 = zeroSymPert4) :
    WTT4 Lsym (finiteSymGrad4 xi) = zeroSymPert4 := by
  rw [WTT4, PiTT4_kills_gauge, hL_zero]
  exact PiTT4_zero

/-- TT-positivity condition exactly on the projected sector. -/
def TTPositiveOperator4 (Lsym : SymPert4 -> SymPert4) : Prop :=
  forall h : SymPert4, 0 <= pairing4 (PiTT4 h).h (Lsym (PiTT4 h)).h

theorem PiTT4_self_adjoint_pairing (h x : SymPert4) :
    pairing4 h.h (PiTT4 x).h = pairing4 (PiTT4 h).h x.h := by
  simp [PiTT4, addSymPert4, scaleSymPert4, ePlusPert4, eCrossPert4,
    pairing4_ePlus_left, pairing4_eCross_left, pairing4_ePlus_right,
    pairing4_eCross_right, pairing4, Matrix.trace, Matrix.mul_apply, eta4,
    ePlus4, eCross4, Fin.sum_univ_four]
  ring

theorem WTT4_energy_nonnegative
    (Lsym : SymPert4 -> SymPert4)
    (hpos : TTPositiveOperator4 Lsym)
    (h : SymPert4) :
    0 <= pairing4 h.h (WTT4 Lsym h).h := by
  rw [WTT4, PiTT4_self_adjoint_pairing]
  exact hpos h

theorem PiTT4_fixed_on_ePlus :
    PiTT4 ePlusPert4 = ePlusPert4 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [PiTT4, addSymPert4, scaleSymPert4, ePlusPert4, eCrossPert4,
      pairing4_ePlus_left, pairing4_eCross_left, ePlus4, eCross4]

theorem PiTT4_fixed_on_eCross :
    PiTT4 eCrossPert4 = eCrossPert4 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [PiTT4, addSymPert4, scaleSymPert4, ePlusPert4, eCrossPert4,
      pairing4_ePlus_left, pairing4_eCross_left, ePlus4, eCross4]

/-- Constructive TT stress: a finite linear combination of the two polarizations. -/
structure TTStress4 where
  a : Rat
  b : Rat

/-- The symmetric perturbation represented by a constructive TT stress. -/
def TTStress4.T (T : TTStress4) : SymPert4 :=
  addSymPert4 (scaleSymPert4 T.a ePlusPert4) (scaleSymPert4 T.b eCrossPert4)

theorem spin2_coupling_depends_only_on_tt_stress
    (h : SymPert4)
    (T : TTStress4) :
    pairing4 h.h T.T.h = pairing4 (PiTT4 h).h T.T.h := by
  simp [TTStress4.T, PiTT4, addSymPert4, scaleSymPert4, ePlusPert4,
    eCrossPert4, pairing4_ePlus_left, pairing4_eCross_left,
    pairing4_ePlus_right, pairing4_eCross_right, pairing4, Matrix.trace,
    Matrix.mul_apply, eta4, ePlus4, eCross4, Fin.sum_univ_four]
  ring

/-- Symmetric matrix component count in dimension `d`. -/
def symmetricComponents (d : Nat) : Nat :=
  d * (d + 1) / 2

/-- Gauge plus trace constraint count used by the finite spin-2 quotient. -/
def gaugeTraceConstraintCount (d : Nat) : Nat :=
  2 * d

theorem finite_spin2_four_role_dof_eq_two :
    symmetricComponents 4 - gaugeTraceConstraintCount 4 = 2 := by
  native_decide

/-- The two concrete TT polarization labels. -/
inductive TTPolarization4 where
  | plus
  | cross
  deriving DecidableEq, Repr, Fintype

theorem tt_polarization_card_eq_two :
    Fintype.card TTPolarization4 = 2 := by
  native_decide

/-- TT carrier facts supplied to the macro gravity interface. -/
def FiniteSpin2TTMacroCarrierClosed : Prop :=
  (forall Lsym : SymPert4 -> SymPert4,
    forall h : SymPert4, IsTT4 (WTT4 Lsym h)) /\
  (forall h : SymPert4,
    forall T : TTStress4,
      pairing4 h.h T.T.h = pairing4 (PiTT4 h).h T.T.h) /\
  (forall phi : Rat, PiTT4 (traceMode4 phi) = zeroSymPert4) /\
  (forall xi : Role4 -> Rat, PiTT4 (finiteSymGrad4 xi) = zeroSymPert4) /\
  Fintype.card TTPolarization4 = 2

theorem finite_spin2_supplies_tt_macro_carrier :
    FiniteSpin2TTMacroCarrierClosed := by
  exact
    ⟨WTT4_preserves_tt,
      spin2_coupling_depends_only_on_tt_stress,
      PiTT4_kills_trace,
      PiTT4_kills_gauge,
      tt_polarization_card_eq_two⟩

/-- Concrete closure package for the finite spin-2 TT wave operator. -/
structure FiniteSpin2WaveOperatorConcreteClosure where
  plus_fixed : PiTT4 ePlusPert4 = ePlusPert4
  cross_fixed : PiTT4 eCrossPert4 = eCrossPert4
  trace_removed : forall phi : Rat, PiTT4 (traceMode4 phi) = zeroSymPert4
  gauge_removed : forall xi : Role4 -> Rat, PiTT4 (finiteSymGrad4 xi) = zeroSymPert4
  polarization_count : Fintype.card TTPolarization4 = 2

def finiteSpin2WaveOperatorConcreteClosure :
    FiniteSpin2WaveOperatorConcreteClosure where
  plus_fixed := PiTT4_fixed_on_ePlus
  cross_fixed := PiTT4_fixed_on_eCross
  trace_removed := PiTT4_kills_trace
  gauge_removed := PiTT4_kills_gauge
  polarization_count := tt_polarization_card_eq_two

end D0.Geometry
