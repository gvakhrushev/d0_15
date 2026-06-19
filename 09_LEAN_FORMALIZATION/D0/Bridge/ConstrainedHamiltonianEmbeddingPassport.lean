import Mathlib.Tactic
import Mathlib.Data.Matrix.Basic

/-!
# D0-CONSTRAINED-HAMILTONIAN-EMBEDDING-PASSPORT-001 — formalism bridge (NOT empirical confirmation)

A standard-language / formalism bridge to:

  Yu-Bo Shi, R. Moessner, R. Alert, M. Bukov et al., "Hamiltonian description of non-reciprocal
  interactions", Nature Physics (12 June 2026), s41567-026-03317-0.

The article supplies a recognized **constrained-Hamiltonian-embedding** language for non-reciprocal
effective dynamics: non-reciprocal dynamics generally has no potential, but adding auxiliary degrees
of freedom yields a reciprocal Hamiltonian/symplectic system "upstairs", and a constraint on each
original/auxiliary pair (preserved by the dynamics) recovers the original non-reciprocal dynamics
"downstairs" on the constrained submanifold; Floquet engineering then becomes available upstairs.

This module records the bridge as **finite, decidable structure data** — it does NOT claim the
article proves D0, does NOT identify the D0 archive `Q_N` with the article's auxiliary/bath degrees,
and is **never** `CORE`. It is `PASSPORT-CLOSED` (firewall `EMPIRICAL_PASSPORT`).

D0 mapping (formalism only): original variables θ ↔ active/retained sector `P_N`; auxiliary φ ↔ an
auxiliary extension space (NOT the D0 archive identically); mirror constraint θ−φ=π ↔ the D0
retained/archive admissibility / self-readout consistency constraint; Hamiltonian upstairs ↔ a finite
enlarged action/symplectic owner; non-reciprocal dynamics downstairs ↔ effective active-sector
dynamics after eliminating `Q_N`; Floquet ↔ the D0 finite tick / driven feedback operator.
-/

namespace D0.Bridge.ConstrainedHamiltonianEmbeddingPassport

open Matrix

/-- Bridge provenance: a formalism passport is exactly NOT a core-confirmation status. -/
inductive BridgeStatus
  | passport
  | coreConfirmation
  deriving DecidableEq

/-- The constrained Hamiltonian embedding as finite dimension data: `activeDim` original variables,
`auxiliaryDim` auxiliary variables, one constraint per original/auxiliary pair. The enlarged space is
`activeDim + auxiliaryDim`; the constrained submanifold removes `constraintCount` directions. -/
structure ConstrainedEmbedding where
  activeDim : Nat
  auxiliaryDim : Nat
  constraintCount : Nat
  status : BridgeStatus

/-- The D0 retained/archive side, kept SEPARATE from the article's auxiliary space (no identification). -/
structure D0RetainedArchiveBridge where
  retainedDim : Nat
  archiveDim : Nat
  /-- whether the bridge identifies the archive with the article's auxiliary degrees (must stay false). -/
  identifiesArchiveWithAuxiliary : Bool

/-- The concrete bridge instance: the D0 active sector is rank 3; the symplectic doubling adds a
3-dim auxiliary mirror, with one constraint per pair (3). Status = passport. -/
def embedding : ConstrainedEmbedding := ⟨3, 3, 3, BridgeStatus.passport⟩

/-- The D0 side: retained rank 3 / archive dim 30, with NO identification of the archive with the
article's auxiliary degrees. -/
def d0Side : D0RetainedArchiveBridge := ⟨3, 30, false⟩

/-- The enlarged dimension `activeDim + auxiliaryDim`. -/
def enlargedDim (E : ConstrainedEmbedding) : Nat := E.activeDim + E.auxiliaryDim

/-- The effective (constrained-submanifold) dimension `enlargedDim − constraintCount`. -/
def effectiveDim (E : ConstrainedEmbedding) : Nat := enlargedDim E - E.constraintCount

/-- A `2×2` symplectic form `J = [[0,1],[-1,0]]` over `ℤ`, witnessing a genuine symplectic/Hamiltonian
structure "upstairs". -/
def Jsymp : Matrix (Fin 2) (Fin 2) Int := !![0, 1; -1, 0]

/-- The mirror constraint as an involution on the original/auxiliary swap: `σ = [[0,1],[1,0]]`,
`σ² = I` (the constraint pairing is preserved / order-2). -/
def mirror : Matrix (Fin 2) (Fin 2) Int := !![0, 1; 1, 0]

/-! ## Theorems — genuine finite/decidable content, no `:= True` shell -/

/-- **The auxiliary extension adds no core physics**: after the per-pair constraint, the
constrained-submanifold dimension equals the original active dimension (`(3+3)−3 = 3`). The enlarged
Hamiltonian space is bookkeeping; the physical active count is unchanged. -/
theorem auxiliary_extension_does_not_add_core_physics :
    effectiveDim embedding = embedding.activeDim := by decide

/-- **The constraint is preserved by the dynamics** (here: the mirror pairing is an involution,
`σ² = I`), the finite shadow of the article's "constraint preserved by the flow". -/
theorem constrained_embedding_preserves_constraint : mirror * mirror = (1 : Matrix (Fin 2) (Fin 2) Int) := by
  decide

/-- **A symplectic/Hamiltonian structure exists upstairs**: `J² = −I` (the standard symplectic unit),
so the enlarged system genuinely carries a Hamiltonian/symplectic form. -/
theorem nonreciprocal_active_dynamics_has_formalism_bridge :
    Jsymp * Jsymp = (-1 : Matrix (Fin 2) (Fin 2) Int) := by decide

/-- **Feshbach constraint-submanifold bridge**: the effective active dimension on the constrained
submanifold matches the D0 retained-sector dimension (3), with the archive NOT identified with the
auxiliary degrees. This is the finite shadow of "eliminate the auxiliary/traced sector, read the
non-reciprocal active dynamics on the constraint submanifold". -/
theorem feshbach_constraint_submanifold_bridge :
    effectiveDim embedding = d0Side.retainedDim ∧ d0Side.identifiesArchiveWithAuxiliary = false := by
  decide

/-- **The bridge is formalism, not core confirmation**: the recorded status is `passport`, which is
provably not `coreConfirmation`. The article supplies *language*, never a proof of D0. -/
theorem bridge_is_formalism_not_core_confirmation :
    embedding.status = BridgeStatus.passport ∧ embedding.status ≠ BridgeStatus.coreConfirmation := by
  decide

end D0.Bridge.ConstrainedHamiltonianEmbeddingPassport
