import Mathlib.Tactic
import Mathlib.LinearAlgebra.Matrix.Notation
import D0.Core.FiniteTypes

/-!
# The 1+4+3 terminal decomposition from the owned type Omega8 = Role x Orient

This module derives the same rank pattern used by the Q8 terminal Fourier owner
without choosing a Q8 element-labeling.

The source type is already owned in Core:

  Role   = Dyad x Dyad,   |Role| = 4
  Orient = Bool,          |Orient| = 2
  Omega8 = Role x Orient, |Omega8| = 8.

Flipping only the orientation coordinate defines a canonical involution F on
Q[Omega8]. Its odd projector (I-F)/2 has rank 4. Its even projector (I+F)/2
has rank 4. Inside the even part, the global constant line has rank 1, leaving
a rank-3 reduced role sector.

Hence the type itself canonically supplies the orthogonal decomposition

  Q[Omega8] = E0_typed (+) E4_typed (+) E3_typed

with traces/ranks (1,4,3), and the orientation signs are (+,-,+).

No isomorphism Omega8 ~= Q8 is chosen here.  A later bridge may prove that
these typed projectors are carried to the existing Q8 Fourier projectors
(E0,E4,E3) under every admissible center-preserving identification.  The
present theorem is deliberately prior to that bridge.
-/

namespace D0.Representation.Omega8OrientationDecomposition

open Matrix

abbrev MOmega := Matrix D0.Omega8 D0.Omega8 ℚ

/-- Flip only the already-owned orientation bit. -/
def orientFlip : MOmega := fun x y =>
  if x.1 = y.1 ∧ x.2 = !y.2 then 1 else 0

/-- The orientation flip is an involution. -/
theorem orientFlip_sq : orientFlip * orientFlip = (1 : MOmega) := by
  native_decide

/-- Orientation-even projector. -/
def evenProjector : MOmega :=
  (1 / 2 : ℚ) • ((1 : MOmega) + orientFlip)

/-- Orientation-odd projector. -/
def oddProjector : MOmega :=
  (1 / 2 : ℚ) • ((1 : MOmega) - orientFlip)

/-- Global constant line in Q[Omega8]. -/
def typedE0 : MOmega := fun _ _ => 1 / 8

/-- The 4-dimensional orientation-odd sector. -/
def typedE4 : MOmega := oddProjector

/-- The 3-dimensional nonconstant orientation-even role sector. -/
def typedE3 : MOmega := evenProjector - typedE0

theorem evenProjector_idempotent :
    evenProjector * evenProjector = evenProjector := by
  native_decide

theorem oddProjector_idempotent :
    oddProjector * oddProjector = oddProjector := by
  native_decide

theorem typedE0_idempotent : typedE0 * typedE0 = typedE0 := by
  native_decide

theorem typedE3_idempotent : typedE3 * typedE3 = typedE3 := by
  native_decide

/-- The three typed projectors are pairwise orthogonal. -/
theorem typed_projectors_orthogonal :
    typedE0 * typedE4 = 0 ∧
    typedE0 * typedE3 = 0 ∧
    typedE4 * typedE3 = 0 := by
  native_decide

/-- The three typed projectors resolve the identity. -/
theorem typed_projectors_sum :
    typedE0 + typedE4 + typedE3 = (1 : MOmega) := by
  native_decide

/-- Their traces, hence ranks for these rational idempotents, are exactly 1,4,3. -/
theorem typed_projector_traces :
    Matrix.trace typedE0 = 1 ∧
    Matrix.trace typedE4 = 4 ∧
    Matrix.trace typedE3 = 3 := by
  native_decide

/-- The orientation involution has signs (+,-,+) on the three typed sectors. -/
theorem orientation_sector_signs :
    orientFlip * typedE0 = typedE0 ∧
    orientFlip * typedE4 = -typedE4 ∧
    orientFlip * typedE3 = typedE3 := by
  native_decide

/-- In particular the owned orientation action is genuinely non-scalar. -/
theorem orientFlip_nontrivial :
    orientFlip ≠ (1 : MOmega) ∧ orientFlip ≠ -(1 : MOmega) := by
  native_decide

/-- Capstone: the terminal 1+4+3 split and (+,-,+) sign pattern are already
forced by Role x Orient before any Q8 element-labeling is chosen. -/
theorem omega8_orientation_decomposition :
    typedE0 * typedE0 = typedE0 ∧
    typedE4 * typedE4 = typedE4 ∧
    typedE3 * typedE3 = typedE3 ∧
    typedE0 + typedE4 + typedE3 = (1 : MOmega) ∧
    Matrix.trace typedE0 = 1 ∧
    Matrix.trace typedE4 = 4 ∧
    Matrix.trace typedE3 = 3 ∧
    orientFlip * typedE0 = typedE0 ∧
    orientFlip * typedE4 = -typedE4 ∧
    orientFlip * typedE3 = typedE3 := by
  exact ⟨typedE0_idempotent,
    oddProjector_idempotent,
    typedE3_idempotent,
    typed_projectors_sum,
    typed_projector_traces.1,
    typed_projector_traces.2.1,
    typed_projector_traces.2.2,
    orientation_sector_signs.1,
    orientation_sector_signs.2.1,
    orientation_sector_signs.2.2⟩

end D0.Representation.Omega8OrientationDecomposition
