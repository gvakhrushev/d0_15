import Mathlib.Tactic
import D0.UnifiedFiniteCore.Q8Terminal
import D0.Extensions.RepresentationReadoutExtension

/-!
# Orientation nontriviality as the positive face of the grading no-go

The post-core grading front currently leaves four signatures on the 3-dimensional
generation block,

`(3,0), (2,1), (1,2), (0,3)`,

with neutral-current counts `12, 8, 8, 12`.  A previous positive route selects
the middle pair by minimizing the grading-even commutant dimension.

This module isolates a stronger, non-variational observation.

On the already-owned terminal `Q₈` Fourier carrier, the central orientation
involution is not scalar: it acts by `+1` on `E₀` and `E₃`, and by `-1`
on `E₄`.  Therefore the terminal carrier contains both signs before any
neutral-current count is considered.

Separately, on a 3-dimensional grading block, the requirement that both signs
actually occur excludes the scalar signatures `(3,0)` and `(0,3)` outright.
The only possibilities are `(2,1)` and `(1,2)`, and both have
`ncCount = 8`.

HONEST BOUNDARY.  This module does **not** assert that the terminal orientation
involution has already been transported to the graph-derived 3-dimensional
generation block.  That cross-carrier transport is the exact remaining bridge.
What is proved here is that, once such a transport preserves nontriviality,
`nc = 8` follows without an MDL/commutant-minimization principle and without
using a KO-sign convention to choose between `8` and `12`.
-/

namespace D0.Representation.OrientationNontrivialGrading

open Matrix
open D0.UnifiedFiniteCore.Q8Terminal
open D0.Extensions.RepresentationReadoutExtension

abbrev M8 := Matrix (Fin 8) (Fin 8) ℚ

/-- The central orientation sign reconstructed from the owned order-4 projector.
Since `E₄ = (I - L_{-1})/2`, this is exactly `L_{-1} = I - 2E₄`. -/
def terminalOrientationSign : M8 :=
  1 - (2 : ℚ) • E4

/-- The reconstructed central sign is an involution. -/
theorem terminalOrientationSign_involution :
    terminalOrientationSign * terminalOrientationSign = (1 : M8) := by
  native_decide

/-- The trivial Fourier line is orientation-even. -/
theorem terminalOrientationSign_on_E0 :
    terminalOrientationSign * E0 = E0 := by
  native_decide

/-- The order-memory / quaternionic sector is orientation-odd. -/
theorem terminalOrientationSign_on_E4 :
    terminalOrientationSign * E4 = -E4 := by
  native_decide

/-- The reduced role sector is orientation-even. -/
theorem terminalOrientationSign_on_E3 :
    terminalOrientationSign * E3 = E3 := by
  native_decide

/-- The terminal orientation involution is genuinely non-scalar: neither `+I`
nor `-I`. -/
theorem terminalOrientationSign_nontrivial :
    terminalOrientationSign ≠ (1 : M8) ∧
      terminalOrientationSign ≠ -(1 : M8) := by
  native_decide

/-- Both grading eigenspaces are required to be nonempty.  This is the precise
nontriviality condition needed to exclude scalar gradings. -/
def BothSignsPresent (p q : ℕ) : Prop :=
  0 < p ∧ 0 < q

/-- On a 3-dimensional block, a nontrivial involutive grading has only the two
global-sign-related signatures `(2,1)` and `(1,2)`. -/
theorem nontrivial_signature_classification
    (p q : ℕ) (hsum : p + q = 3) (hboth : BothSignsPresent p q) :
    (p, q) = (2, 1) ∨ (p, q) = (1, 2) := by
  rcases hboth with ⟨hp, hq⟩
  have hp_cases : p = 1 ∨ p = 2 := by omega
  rcases hp_cases with hp1 | hp2
  · have hq2 : q = 2 := by omega
    right
    simp [hp1, hq2]
  · have hq1 : q = 1 := by omega
    left
    simp [hp2, hq1]

/-- Consequently nontriviality alone fixes the neutral-current count to `8`;
no minimization of `ncCount` is used. -/
theorem nontrivial_signature_nc
    (p q : ℕ) (hsum : p + q = 3) (hboth : BothSignsPresent p q) :
    ncCount p q = 8 := by
  rcases nontrivial_signature_classification p q hsum hboth with h | h
  · have hp : p = 2 := congrArg Prod.fst h
    have hq : q = 1 := congrArg Prod.snd h
    simp at hp hq
    subst p
    subst q
    exact nc_signature_21
  · have hp : p = 1 := congrArg Prod.fst h
    have hq : q = 2 := congrArg Prod.snd h
    simp at hp hq
    subst p
    subst q
    decide

/-- The scalar signatures are therefore incompatible with nontrivial grading. -/
theorem nontrivial_signature_excludes_scalar
    (p q : ℕ) (hsum : p + q = 3) (hboth : BothSignsPresent p q) :
    (p, q) ≠ (3, 0) ∧ (p, q) ≠ (0, 3) := by
  rcases hboth with ⟨hp, hq⟩
  constructor <;> intro h
  · have hq0 : q = 0 := congrArg Prod.snd h
    simp at hq0
    omega
  · have hp0 : p = 0 := congrArg Prod.fst h
    simp at hp0
    omega

/-- Bundle: the terminal owner supplies a genuine `±` involution, while any
3-dimensional grading carrying both signs necessarily lies in the `nc=8`
flip-class.  The missing theorem is only the cross-carrier transport of this
nontrivial orientation sign to the generation block. -/
theorem orientation_nontrivial_grading_reduction :
    (terminalOrientationSign * E0 = E0 ∧
      terminalOrientationSign * E4 = -E4 ∧
      terminalOrientationSign * E3 = E3 ∧
      terminalOrientationSign ≠ (1 : M8) ∧
      terminalOrientationSign ≠ -(1 : M8)) ∧
    (∀ p q : ℕ, p + q = 3 → BothSignsPresent p q → ncCount p q = 8) := by
  refine ⟨?_, ?_⟩
  · exact ⟨terminalOrientationSign_on_E0,
      terminalOrientationSign_on_E4,
      terminalOrientationSign_on_E3,
      terminalOrientationSign_nontrivial.1,
      terminalOrientationSign_nontrivial.2⟩
  · intro p q hsum hboth
    exact nontrivial_signature_nc p q hsum hboth

end D0.Representation.OrientationNontrivialGrading
