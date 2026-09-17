import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Tactic
import D0.Dynamics.ToralAutomorphism

/-!
# Toral shift-equivalence invariants (GL(2,Z) similarity + agreeing SE invariants)

This module owns the HONEST closable scope of the Williams shift-equivalence
question for the D0 toral time-transition operator.  It proves, over the integers
with finite/decidable tactics only:

* the characteristic polynomials of `T = !![0,1;1,-1]` and the Fibonacci
  companion `M = !![1,1;1,0]` (via trace/determinant);
* an explicit GL(2,Z) similarity `U * N = M * U` with `N = -T`, where
  `U = !![0,1;-1,0]` and `det U = 1` (so `N` and `M` are conjugate over `Z`);
* the agreement of the two classical shift-equivalence INVARIANTS:
  - equal nonzero spectrum: `charpoly N = charpoly M = X^2 - X - 1`, which is the
    Galois sign-flip `r ↔ -r` of `charpoly T = X^2 + X - 1`;
  - equal Bowen–Franks group `Z^2 / (I - A) Z^2`: both `I - M` and `I - N`
    have Smith normal form `diag(1,1)` (exhibited by explicit unimodular
    `P, Q ∈ GL(2,Z)` with `P * (I - A) * Q = 1`), so both Bowen–Franks groups are
    the trivial group.

It does NOT claim topological conjugacy, nor full Williams strong-shift-equivalence:
the SE invariants are necessary but not sufficient, and that implication stays
EXTERNAL (Adler–Weiss / Williams, recorded as ASSUMP-ADLER-WEISS).
-/

namespace D0.Dynamics

open Matrix

/-- Fibonacci companion matrix `M = !![1,1;1,0]` (the golden SFT transition matrix). -/
def M : ZMat2 := !![1, 1; 1, 0]

/-- The negated time-transition matrix `N = -T = !![0,-1;-1,1]`. -/
def N : ZMat2 := -T

/-- Explicit GL(2,Z) similarity matrix `U = !![0,1;-1,0]` (det `U = 1`). -/
def U : ZMat2 := !![0, 1; -1, 0]

/-! ## (a) Characteristic polynomials via trace and determinant -/

theorem trace_M : Matrix.trace M = 1 := by native_decide

theorem det_M : Matrix.det M = -1 := by native_decide

/-- `charpoly T = X^2 + X - 1` recorded as the trace/det pair `(tr, det) = (-1, -1)`,
i.e. `X^2 - (tr)X + det = X^2 + X - 1`. -/
theorem charpoly_T_trace_det : Matrix.trace T = -1 /\ Matrix.det T = -1 :=
  And.intro trace_T1 det_T

/-- `charpoly M = X^2 - X - 1` recorded as `(tr, det) = (1, -1)`,
i.e. `X^2 - (tr)X + det = X^2 - X - 1`. -/
theorem charpoly_M_trace_det : Matrix.trace M = 1 /\ Matrix.det M = -1 :=
  And.intro trace_M det_M

theorem trace_N : Matrix.trace N = 1 := by native_decide

theorem det_N : Matrix.det N = -1 := by native_decide

/-- `charpoly N = X^2 - X - 1 = charpoly M` (equal nonzero spectrum). -/
theorem charpoly_N_eq_charpoly_M :
    (Matrix.trace N = Matrix.trace M) /\ (Matrix.det N = Matrix.det M) := by
  refine And.intro ?_ ?_
  · rw [trace_N, trace_M]
  · rw [det_N, det_M]

/-- The Galois sign-flip `r ↔ -r`: the spectrum of `N = -T` is the negation of the
spectrum of `T`.  At the level of `(tr, det)` invariants this is
`tr N = -tr T` and `det N = det T` (degree-2, so determinant is sign-invariant). -/
theorem spectrum_galois_sign_flip :
    Matrix.trace N = -Matrix.trace T /\ Matrix.det N = Matrix.det T := by
  refine And.intro ?_ ?_
  · rw [trace_N, trace_T1]; norm_num
  · rw [det_N, det_T]

/-! ## (b) Explicit GL(2,Z) similarity `U * N = M * U`, `det U = 1` -/

theorem det_U : Matrix.det U = 1 := by native_decide

/-- The integer similarity: `U * N = M * U` with `N = -T`.  Together with `det U = 1`
this exhibits `N` and `M` as conjugate in GL(2,Z). -/
theorem U_similarity : U * N = M * U := by
  ext i j
  fin_cases i <;> fin_cases j <;> native_decide

/-- `U` is invertible over `Z` (its determinant is a unit), so the similarity is a
genuine GL(2,Z) conjugacy `N = U⁻¹ * M * U`. -/
theorem U_is_unimodular : Matrix.det U = 1 \/ Matrix.det U = -1 :=
  Or.inl det_U

/-! ## (c) Bowen–Franks group `Z^2 / (I - A) Z^2` via Smith normal form

For a `2 x 2` integer matrix `A`, the Bowen–Franks group is `Z^2 / (I - A) Z^2`.
Its isomorphism type is determined by the Smith normal form of `I - A`.  We prove
the SNF of both `I - M` and `I - N` equals `diag(1,1)` by exhibiting explicit
unimodular `P, Q ∈ GL(2,Z)` with `P * (I - A) * Q = 1`.  Since the SNF is `diag(1,1)`,
both Bowen–Franks groups are trivial, hence equal. -/

/-- `I - M = !![0,-1;-1,1]`. -/
def ImM : ZMat2 := (1 : ZMat2) - M

/-- `I - N = I + T = !![1,1;1,0]`. -/
def ImN : ZMat2 := (1 : ZMat2) - N

theorem det_ImM : Matrix.det ImM = -1 := by native_decide

theorem det_ImN : Matrix.det ImN = -1 := by native_decide

/-- Unimodular left factor reducing `I - M` to its SNF. -/
def P_M : ZMat2 := !![-2, -1; -1, 0]
/-- Unimodular right factor reducing `I - M` to its SNF. -/
def Q_M : ZMat2 := !![1, -1; 0, 1]

theorem det_P_M : Matrix.det P_M = -1 := by native_decide
theorem det_Q_M : Matrix.det Q_M = 1 := by native_decide

/-- Smith normal form of `I - M` is `diag(1,1)`: `P_M * (I - M) * Q_M = 1`,
with `P_M, Q_M ∈ GL(2,Z)`.  Hence `Z^2 / (I - M) Z^2 = 0` (trivial Bowen–Franks group). -/
theorem snf_ImM : P_M * ImM * Q_M = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;> native_decide

/-- Unimodular left factor reducing `I - N` to its SNF. -/
def P_N : ZMat2 := !![-2, 1; -1, 1]
/-- Unimodular right factor reducing `I - N` to its SNF. -/
def Q_N : ZMat2 := !![-1, 2; 0, -1]

theorem det_P_N : Matrix.det P_N = -1 := by native_decide
theorem det_Q_N : Matrix.det Q_N = 1 := by native_decide

/-- Smith normal form of `I - N` is `diag(1,1)`: `P_N * (I - N) * Q_N = 1`,
with `P_N, Q_N ∈ GL(2,Z)`.  Hence `Z^2 / (I - N) Z^2 = 0` (trivial Bowen–Franks group). -/
theorem snf_ImN : P_N * ImN * Q_N = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;> native_decide

/-- The Bowen–Franks invariants AGREE: both `I - M` and `I - N` reduce to the
identity SNF `diag(1,1)` by unimodular equivalences, so both Bowen–Franks groups
`Z^2 / (I - A) Z^2` are trivial — in particular equal. -/
theorem bowen_franks_invariants_agree :
    (P_M * ImM * Q_M = 1) /\ (P_N * ImN * Q_N = 1) /\
      (Matrix.det ImM = Matrix.det ImN) := by
  refine And.intro snf_ImM (And.intro snf_ImN ?_)
  rw [det_ImM, det_ImN]

/-! ## Closure package (GL(2,Z) similarity + agreeing SE invariants ONLY) -/

/-- The honestly-scoped shift-equivalence-invariant closure for the D0 toral time
operator.  Owns: charpolys, the explicit GL(2,Z) similarity `U * N = M * U` with
`det U = 1`, and the agreement of both shift-equivalence invariants (equal nonzero
spectrum + equal/trivial Bowen–Franks group).  It does NOT contain topological
conjugacy nor strong-shift-equivalence — those remain EXTERNAL (ASSUMP-ADLER-WEISS). -/
structure ToralShiftEquivalenceInvariants where
  charpoly_T : Matrix.trace T = -1 /\ Matrix.det T = -1
  charpoly_M : Matrix.trace M = 1 /\ Matrix.det M = -1
  similarity : U * N = M * U
  similarity_unimodular : Matrix.det U = 1
  spectrum_agrees : (Matrix.trace N = Matrix.trace M) /\ (Matrix.det N = Matrix.det M)
  bowen_franks_agrees :
    (P_M * ImM * Q_M = 1) /\ (P_N * ImN * Q_N = 1) /\
      (Matrix.det ImM = Matrix.det ImN)

def toralShiftEquivalenceInvariants : ToralShiftEquivalenceInvariants where
  charpoly_T := charpoly_T_trace_det
  charpoly_M := charpoly_M_trace_det
  similarity := U_similarity
  similarity_unimodular := det_U
  spectrum_agrees := charpoly_N_eq_charpoly_M
  bowen_franks_agrees := bowen_franks_invariants_agree

end D0.Dynamics
