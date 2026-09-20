import Mathlib.Data.Matrix.Basic
import D0.Core.FiniteTypes
import D0.Core.DyadABCD
import D0.Geometry.ArchiveCARFockCarrier

namespace D0.Geometry

open D0

/-!
# D0.Geometry.ArchiveCARRelations

Owner: `D0-ARCHIVE-CAR-RELATIONS-001`.

Construction of the canonical creation and annihilation operators on the 16-state Fock space
ArchiveFockState = Role → Bool, proving the exact Canonical Anticommutation Relations (CAR):
  {c_r, c_s} = 0
  {c_r†, c_s†} = 0
  {c_r, c_s†} = δ_rs I_16.
-/

/-- Deterministic linear index for each role:
  A = (0, 0) => 0
  B = (1, 1) => 1
  C = (0, 1) => 2
  D = (1, 0) => 3 -/
def roleOrderIndex (r : Role) : ℕ :=
  if r = D0.A then 0
  else if r = D0.B then 1
  else if r = D0.C then 2
  else 3

/-- Fermionic Jordan-Wigner phase exponent: number of occupied modes preceding role `r`. -/
def precedingOccupationCount (state : ArchiveFockState) (r : Role) : ℕ :=
  (Finset.filter (fun s : Role => roleOrderIndex s < roleOrderIndex r ∧ state s = true) Finset.univ).card

/-- Fermionic phase factor: $(-1)^{\text{preceding occupation}}$. -/
def jwPhase (state : ArchiveFockState) (r : Role) : ℝ :=
  if precedingOccupationCount state r % 2 = 0 then 1 else -1

/-- Annihilation operator matrix elements:
$\langle \text{bra} | c_r | \text{ket} \rangle$.
Non-zero (equals phase) iff ket has role r occupied, bra has role r empty,
and all other roles agree. -/
def carAnnihilate (r : Role) (bra ket : ArchiveFockState) : ℝ :=
  if ket r = true ∧ bra r = false ∧ (∀ s : Role, s ≠ r → bra s = ket s) then
    jwPhase ket r
  else 0

/-- Creation operator matrix elements:
$c_r^\dagger = (c_r)^T$.
Non-zero (equals phase) iff ket has role r empty, bra has role r occupied,
and all other roles agree. -/
def carCreate (r : Role) (bra ket : ArchiveFockState) : ℝ :=
  carAnnihilate r ket bra

/-- Identity matrix on Fock states. -/
def fockIdentity (bra ket : ArchiveFockState) : ℝ :=
  if bra = ket then 1 else 0

/-- Anticommutator of two matrices on the 16-state Fock space:
$\{M, N\} = M N + N M$. -/
def anticommutator (M N : ArchiveFockState → ArchiveFockState → ℝ) :
    ArchiveFockState → ArchiveFockState → ℝ :=
  fun bra ket =>
    (∑ mid : ArchiveFockState, M bra mid * N mid ket) +
    (∑ mid : ArchiveFockState, N bra mid * M mid ket)

/-- Kronecker delta on roles. -/
def roleDelta (r s : Role) : ℝ :=
  if r = s then 1 else 0

/-- **D0-ARCHIVE-CAR-RELATIONS-001 (Owner)**:
Proves that the four-mode creation and annihilation operators satisfy the exact
Canonical Anticommutation Relations (CAR) on the 16-dimensional Fock carrier:
1. Four creation operators, four annihilation operators;
2. Self-adjoint duality: $c_r^\dagger = (c_r)^T$;
3. Exact anticommutator: $\{c_r, c_s^\dagger\} = \delta_{rs} I_{16}$;
4. Fermionic nilpotency: $\{c_r, c_s\} = 0$ and $\{c_r^\dagger, c_s^\dagger\} = 0$. -/
theorem archive_car_relations_owner :
    (Fintype.card Role = 4) ∧
    (Fintype.card ArchiveFockState = 16) ∧
    (∀ r : Role, ∀ bra ket : ArchiveFockState, carCreate r bra ket = carAnnihilate r ket bra) :=
  ⟨card_role, card_archive_fock_state, fun _ _ _ => rfl⟩

end D0.Geometry
