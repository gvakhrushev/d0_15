import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic
import D0.Core.FiniteTypes
import D0.Core.DyadABCD
import D0.Geometry.ArchiveCARFockCarrier

namespace D0.Geometry

open D0

/-!
# D0.Geometry.ArchiveCARRelations

Owner: `D0-ARCHIVE-CAR-RELATIONS-001`.

Construction of the canonical creation and annihilation operators on the 16-state Fock space
`ArchiveFockState = Role → Bool`, together with literal matrix forms of the full CAR:
  {c_r, c_s} = 0,
  {c_r†, c_s†} = 0,
  {c_r, c_s†} = δ_rs I.

The real-valued matrices remain the public API.  A computational integer shadow is used only
to discharge the finite four-mode identities without introducing floating-point certificates.
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
  (Finset.filter (fun s : Role => roleOrderIndex s < roleOrderIndex r ∧ state s = true)
    Finset.univ).card

/-- Computational integral Jordan-Wigner sign. -/
def jwSignInt (state : ArchiveFockState) (r : Role) : ℤ :=
  if precedingOccupationCount state r % 2 = 0 then 1 else -1

/-- Fermionic phase factor: (-1)^(preceding occupation). -/
def jwPhase (state : ArchiveFockState) (r : Role) : ℝ :=
  if precedingOccupationCount state r % 2 = 0 then 1 else -1

@[simp] theorem jwPhase_eq_intCast (state : ArchiveFockState) (r : Role) :
    jwPhase state r = (jwSignInt state r : ℝ) := by
  unfold jwPhase jwSignInt
  split <;> norm_num

/-- Annihilation operator matrix elements:
`<bra| c_r |ket>`. -/
def carAnnihilate (r : Role) (bra ket : ArchiveFockState) : ℝ :=
  if ket r = true ∧ bra r = false ∧ (∀ s : Role, s ≠ r → bra s = ket s) then
    jwPhase ket r
  else 0

/-- Integral shadow of `carAnnihilate`. -/
def carAnnihilateInt (r : Role) (bra ket : ArchiveFockState) : ℤ :=
  if ket r = true ∧ bra r = false ∧ (∀ s : Role, s ≠ r → bra s = ket s) then
    jwSignInt ket r
  else 0

@[simp] theorem carAnnihilate_eq_intCast (r : Role) (bra ket : ArchiveFockState) :
    carAnnihilate r bra ket = (carAnnihilateInt r bra ket : ℝ) := by
  unfold carAnnihilate carAnnihilateInt
  split <;> simp [jwPhase_eq_intCast]

/-- Creation operator matrix elements: `c_r† = (c_r)^T`. -/
def carCreate (r : Role) (bra ket : ArchiveFockState) : ℝ :=
  carAnnihilate r ket bra

/-- Integral shadow of `carCreate`. -/
def carCreateInt (r : Role) (bra ket : ArchiveFockState) : ℤ :=
  carAnnihilateInt r ket bra

@[simp] theorem carCreate_eq_intCast (r : Role) (bra ket : ArchiveFockState) :
    carCreate r bra ket = (carCreateInt r bra ket : ℝ) := by
  simp [carCreate, carCreateInt]

/-- Identity matrix on Fock states. -/
def fockIdentity (bra ket : ArchiveFockState) : ℝ :=
  if bra = ket then 1 else 0

def fockIdentityInt (bra ket : ArchiveFockState) : ℤ :=
  if bra = ket then 1 else 0

@[simp] theorem fockIdentity_eq_intCast (bra ket : ArchiveFockState) :
    fockIdentity bra ket = (fockIdentityInt bra ket : ℝ) := by
  unfold fockIdentity fockIdentityInt
  split <;> norm_num

/-- Anticommutator of two matrices on the 16-state Fock space. -/
def anticommutator (M N : ArchiveFockState → ArchiveFockState → ℝ) :
    ArchiveFockState → ArchiveFockState → ℝ :=
  fun bra ket =>
    (∑ mid : ArchiveFockState, M bra mid * N mid ket) +
    (∑ mid : ArchiveFockState, N bra mid * M mid ket)

/-- Integral anticommutator used by the finite decision proof. -/
def anticommutatorInt (M N : ArchiveFockState → ArchiveFockState → ℤ) :
    ArchiveFockState → ArchiveFockState → ℤ :=
  fun bra ket =>
    (∑ mid : ArchiveFockState, M bra mid * N mid ket) +
    (∑ mid : ArchiveFockState, N bra mid * M mid ket)

/-- Kronecker delta on roles. -/
def roleDelta (r s : Role) : ℝ :=
  if r = s then 1 else 0

def roleDeltaInt (r s : Role) : ℤ :=
  if r = s then 1 else 0

@[simp] theorem roleDelta_eq_intCast (r s : Role) :
    roleDelta r s = (roleDeltaInt r s : ℝ) := by
  unfold roleDelta roleDeltaInt
  split <;> norm_num

/-- Vacuum occupation label. -/
def fockVacuumState : ArchiveFockState := fun _ => false

/-- The one-particle basis label associated with a role. -/
def fockSingletonState (r : Role) : ArchiveFockState :=
  fun s => if s = r then true else false

/-- Form/Fock degree: number of occupied role modes. -/
def fockDegree (state : ArchiveFockState) : ℕ :=
  (Finset.filter (fun r : Role => state r = true) Finset.univ).card

/-! ## Full finite CAR on the integral shadow -/

theorem car_annihilate_anticommutator_int :
    ∀ r s : Role, ∀ bra ket : ArchiveFockState,
      anticommutatorInt (carAnnihilateInt r) (carAnnihilateInt s) bra ket = 0 := by
  native_decide

theorem car_create_anticommutator_int :
    ∀ r s : Role, ∀ bra ket : ArchiveFockState,
      anticommutatorInt (carCreateInt r) (carCreateInt s) bra ket = 0 := by
  native_decide

theorem car_mixed_anticommutator_int :
    ∀ r s : Role, ∀ bra ket : ArchiveFockState,
      anticommutatorInt (carAnnihilateInt r) (carCreateInt s) bra ket =
        roleDeltaInt r s * fockIdentityInt bra ket := by
  native_decide

/-! ## Literal real matrix CAR -/

theorem car_annihilate_anticommutator (r s : Role) (bra ket : ArchiveFockState) :
    anticommutator (carAnnihilate r) (carAnnihilate s) bra ket = 0 := by
  have h := congrArg (fun z : ℤ => (z : ℝ))
    (car_annihilate_anticommutator_int r s bra ket)
  simpa [anticommutator, anticommutatorInt] using h

theorem car_create_anticommutator (r s : Role) (bra ket : ArchiveFockState) :
    anticommutator (carCreate r) (carCreate s) bra ket = 0 := by
  have h := congrArg (fun z : ℤ => (z : ℝ))
    (car_create_anticommutator_int r s bra ket)
  simpa [anticommutator, anticommutatorInt] using h

theorem car_mixed_anticommutator (r s : Role) (bra ket : ArchiveFockState) :
    anticommutator (carAnnihilate r) (carCreate s) bra ket =
      roleDelta r s * fockIdentity bra ket := by
  have h := congrArg (fun z : ℤ => (z : ℝ))
    (car_mixed_anticommutator_int r s bra ket)
  simpa [anticommutator, anticommutatorInt] using h

/-- Equivalent mixed ordering `{c_r†,c_s} = δ_rs I`. -/
theorem car_mixed_anticommutator_create_first (r s : Role)
    (bra ket : ArchiveFockState) :
    anticommutator (carCreate r) (carAnnihilate s) bra ket =
      roleDelta r s * fockIdentity bra ket := by
  simpa [anticommutator, mul_comm] using car_mixed_anticommutator s r bra ket

/-! ## Support and degree bookkeeping -/

theorem carCreateInt_support :
    ∀ r : Role, ∀ bra ket : ArchiveFockState,
      carCreateInt r bra ket ≠ 0 →
        bra r = true ∧ ket r = false ∧
          (∀ s : Role, s ≠ r → bra s = ket s) := by
  native_decide

theorem carAnnihilateInt_support :
    ∀ r : Role, ∀ bra ket : ArchiveFockState,
      carAnnihilateInt r bra ket ≠ 0 →
        ket r = true ∧ bra r = false ∧
          (∀ s : Role, s ≠ r → bra s = ket s) := by
  native_decide

theorem carCreateInt_degree_raise :
    ∀ r : Role, ∀ bra ket : ArchiveFockState,
      carCreateInt r bra ket ≠ 0 →
        fockDegree bra = fockDegree ket + 1 := by
  native_decide

theorem carAnnihilateInt_degree_lower :
    ∀ r : Role, ∀ bra ket : ArchiveFockState,
      carAnnihilateInt r bra ket ≠ 0 →
        fockDegree ket = fockDegree bra + 1 := by
  native_decide

theorem carCreate_support (r : Role) (bra ket : ArchiveFockState)
    (h : carCreate r bra ket ≠ 0) :
    bra r = true ∧ ket r = false ∧
      (∀ s : Role, s ≠ r → bra s = ket s) := by
  apply carCreateInt_support r bra ket
  intro hz
  apply h
  simp [hz]

theorem carAnnihilate_support (r : Role) (bra ket : ArchiveFockState)
    (h : carAnnihilate r bra ket ≠ 0) :
    ket r = true ∧ bra r = false ∧
      (∀ s : Role, s ≠ r → bra s = ket s) := by
  apply carAnnihilateInt_support r bra ket
  intro hz
  apply h
  simp [hz]

theorem carCreate_degree_raise (r : Role) (bra ket : ArchiveFockState)
    (h : carCreate r bra ket ≠ 0) :
    fockDegree bra = fockDegree ket + 1 := by
  apply carCreateInt_degree_raise r bra ket
  intro hz
  apply h
  simp [hz]

theorem carAnnihilate_degree_lower (r : Role) (bra ket : ArchiveFockState)
    (h : carAnnihilate r bra ket ≠ 0) :
    fockDegree ket = fockDegree bra + 1 := by
  apply carAnnihilateInt_degree_lower r bra ket
  intro hz
  apply h
  simp [hz]

theorem carCreate_singleton_vacuum (r s : Role) :
    carCreate r (fockSingletonState s) fockVacuumState = roleDelta r s := by
  have h :
      carCreateInt r (fockSingletonState s) fockVacuumState = roleDeltaInt r s := by
    native_decide
  have hc := congrArg (fun z : ℤ => (z : ℝ)) h
  simpa using hc

theorem carAnnihilate_vacuum_singleton (r s : Role) :
    carAnnihilate r fockVacuumState (fockSingletonState s) = roleDelta r s := by
  simpa [carCreate] using carCreate_singleton_vacuum r s

/-- **D0-ARCHIVE-CAR-RELATIONS-001 (Owner)**:
The four-mode creation and annihilation operators satisfy the exact finite CAR. -/
theorem archive_car_relations_owner :
    (Fintype.card Role = 4) ∧
    (Fintype.card ArchiveFockState = 16) ∧
    (∀ r : Role, ∀ bra ket : ArchiveFockState,
      carCreate r bra ket = carAnnihilate r ket bra) ∧
    (∀ r s bra ket,
      anticommutator (carAnnihilate r) (carAnnihilate s) bra ket = 0) ∧
    (∀ r s bra ket,
      anticommutator (carCreate r) (carCreate s) bra ket = 0) ∧
    (∀ r s bra ket,
      anticommutator (carAnnihilate r) (carCreate s) bra ket =
        roleDelta r s * fockIdentity bra ket) := by
  refine ⟨card_role, card_archive_fock_state, ?_, ?_, ?_, ?_⟩
  · intro r bra ket
    rfl
  · exact car_annihilate_anticommutator
  · exact car_create_anticommutator
  · exact car_mixed_anticommutator

end D0.Geometry
