import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic

namespace D0.Geometry

open scoped BigOperators

/-- Three-shell carrier for the D0 memory-torus Core-13 geometry. -/
abbrev Shell3 : Type := Fin 3

/--
Algebraic torus parameter.  The concrete passport may instantiate `a = phi^5`;
the Lean core only needs the finite ordered parameter `1 < a`.
-/
structure TorusParameter where
  a : Rat
  h_gt_one : 1 < a

namespace TorusParameter

def inner (_T : TorusParameter) : Rat := 1
def core (T : TorusParameter) : Rat := (T.a + 1) / 2
def outer (T : TorusParameter) : Rat := T.a
def minor (T : TorusParameter) : Rat := (T.a - 1) / 2
def major (T : TorusParameter) : Rat := (T.a + 1) / 2

/-- Radius/readout attached to the three shell boundaries. -/
def shellRadius (T : TorusParameter) : Shell3 -> Rat :=
  fun i =>
    if i = 0 then T.inner
    else if i = 1 then T.core
    else T.outer

theorem outer_inner_ratio (T : TorusParameter) :
    T.outer / T.inner = T.a := by
  simp [outer, inner]

theorem major_minor_ratio (T : TorusParameter) :
    T.major / T.minor = (T.a + 1) / (T.a - 1) := by
  have hden : T.a - 1 ≠ 0 := by
    linarith [T.h_gt_one]
  field_simp [major, minor, hden]
  simp [major, minor]
  ring_nf

theorem equator_ratio (T : TorusParameter) :
    (T.major + T.minor) / (T.major - T.minor) = T.a := by
  norm_num [major, minor]
  ring

theorem minor_pos (T : TorusParameter) :
    0 < T.minor := by
  simp [minor]
  linarith [T.h_gt_one]

end TorusParameter

/-- Named shell roles used by the book layer. -/
inductive TorusShell where
  | innerD9
  | coreD11
  | outerD13
  deriving DecidableEq, Fintype, Repr

theorem torus_shell_card_eq_three :
    Fintype.card TorusShell = 3 := by
  decide

abbrev ShellMat := Matrix Shell3 Shell3 Rat

/-- Nearest-neighbour radial hopping among the three torus shell boundaries. -/
def radialAdjacency : ShellMat :=
  fun i j =>
    if (i.val + 1 = j.val) \/ (j.val + 1 = i.val) then 1 else 0

/-- Diagonal shell-radius / phase-drift readout. -/
def phaseDrift (T : TorusParameter) : ShellMat :=
  fun i j => if i = j then T.shellRadius i else 0

def matMul3 (A B : ShellMat) : ShellMat :=
  fun i k => Finset.univ.sum (fun j : Shell3 => A i j * B j k)

def commutator3 (A B : ShellMat) : ShellMat :=
  fun i j => matMul3 A B i j - matMul3 B A i j

/-- The radial-hopping / phase-drift commutator is the minor torus radius. -/
theorem radial_hopping_phase_drift_commutator_01
    (T : TorusParameter) :
    commutator3 radialAdjacency (phaseDrift T) (0 : Shell3) (1 : Shell3)
      = T.minor := by
  simp [commutator3, matMul3, radialAdjacency, phaseDrift,
    TorusParameter.shellRadius, TorusParameter.core, TorusParameter.inner,
    TorusParameter.minor, Fin.sum_univ_three]
  ring

/-- The torus shell radial hopping and phase drift do not commute. -/
theorem radial_hopping_phase_drift_noncommute
    (T : TorusParameter) :
    commutator3 radialAdjacency (phaseDrift T) (0 : Shell3) (1 : Shell3) ≠ 0 := by
  rw [radial_hopping_phase_drift_commutator_01]
  exact ne_of_gt (TorusParameter.minor_pos T)

/-- Concrete closure package for the D0 memory-torus shell geometry. -/
structure TorusCore13GeometryOriginClosure where
  shell_card : Fintype.card TorusShell = 3
  commutator_01 :
    forall T : TorusParameter,
      commutator3 radialAdjacency (phaseDrift T) (0 : Shell3) (1 : Shell3)
        = T.minor
  noncommute :
    forall T : TorusParameter,
      commutator3 radialAdjacency (phaseDrift T) (0 : Shell3) (1 : Shell3) ≠ 0

def torusCore13GeometryOriginClosure :
    TorusCore13GeometryOriginClosure where
  shell_card := torus_shell_card_eq_three
  commutator_01 := radial_hopping_phase_drift_commutator_01
  noncommute := radial_hopping_phase_drift_noncommute

end D0.Geometry
