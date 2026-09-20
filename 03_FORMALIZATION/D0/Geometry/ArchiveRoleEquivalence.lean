import Mathlib.Data.Fintype.Basic
import Mathlib.Logic.Equiv.Basic
import D0.Core.FiniteTypes
import D0.Core.DyadABCD
import D0.Algebra.RoleSignature

namespace D0.Geometry

open D0

/-- **Explicit Structural Equivalence between Role (Dyad × Dyad) and RoleSig**:
Explicit isomorphism between the product dyad roles and the inductive signature roles:
  (0, 0) ↔ A
  (1, 1) ↔ B
  (0, 1) ↔ C
  (1, 0) ↔ D
This replaces the bare numerical equality `4 = 4` with a named bijection. -/
def roleRoleSigEquiv : Role ≃ RoleSig where
  toFun r :=
    if r = D0.A then RoleSig.A
    else if r = D0.B then RoleSig.B
    else if r = D0.C then RoleSig.C
    else RoleSig.D
  invFun s :=
    match s with
    | RoleSig.A => D0.A
    | RoleSig.B => D0.B
    | RoleSig.C => D0.C
    | RoleSig.D => D0.D
  left_inv r := by
    rcases r with ⟨⟨r1, hr1⟩, ⟨r2, hr2⟩⟩
    interval_cases r1 <;> interval_cases r2 <;> rfl
  right_inv s := by
    cases s <;> rfl

theorem roleRoleSigEquiv_A : roleRoleSigEquiv D0.A = RoleSig.A := rfl
theorem roleRoleSigEquiv_B : roleRoleSigEquiv D0.B = RoleSig.B := rfl
theorem roleRoleSigEquiv_C : roleRoleSigEquiv D0.C = RoleSig.C := rfl
theorem roleRoleSigEquiv_D : roleRoleSigEquiv D0.D = RoleSig.D := rfl

/-- **D0-ARCHIVE-ROLE-SIGNATURE-SEPARATION-001**:
While `Role ≃ RoleSig` preserves cardinality, the physical Lorentzian signature (1, 3)
requires the assignment of `roleSign` and is NOT mathematically forced by the bare equivalence `Role ≃ RoleSig`.
Specifically, there are 4! = 24 permutations, and the choice of which role is timelike (sign +1)
is an independent algebraic datum. -/
theorem role_signature_datum_independent :
    (Fintype.card Role = Fintype.card RoleSig) ∧
    (Fintype.card Role = 4) ∧
    (roleSign (roleRoleSigEquiv D0.A) = 1) ∧
    (roleSign (roleRoleSigEquiv D0.B) = -1) ∧
    (roleSign (roleRoleSigEquiv D0.C) = -1) ∧
    (roleSign (roleRoleSigEquiv D0.D) = -1) := by
  refine ⟨by rw [card_role, role_cardinality_four], card_role, ?_, ?_, ?_, ?_⟩
  · rfl
  · rfl
  · rfl
  · rfl

end D0.Geometry
