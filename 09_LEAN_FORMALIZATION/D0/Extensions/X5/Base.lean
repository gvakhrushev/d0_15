import D0.Extensions.X5.PrimitiveContract
import Mathlib.Tactic

/-!
# D0-X5-BASE-001 — the joint extension object (Section 1.3)

`D0X5Extension` is present-core D0 plus five OPTIONAL primitive-contract fields and a compatibility flag. Each
primitive is individually usable (any subset may be present). A joint theorem must declare exactly which fields
it consumes (`DependencyTracking`). The base D0 is unchanged: this object only ATTACHES contracts, it does not
rewrite any present-core claim.
-/

namespace D0.Extensions.X5

/-- The five primitive slots. -/
inductive Slot
  | grading        -- G
  | history        -- H
  | leptonBranch   -- L
  | phasonPE       -- P1
  | phasonCoord    -- P2
  deriving DecidableEq, Repr, Fintype

/-- A D0-X5 extension: present-core base + optional contracts per slot + a compatibility flag. -/
structure D0X5Extension where
  contracts : Slot → Option PrimitiveContract
  compatible : Bool

/-- The five slots are exactly five (one per primitive). -/
theorem five_slots : Fintype.card Slot = 5 := by decide

/-- The empty extension (no contracts) is the present-core base, trivially compatible — D0-X5 attaches nothing. -/
def baseOnly : D0X5Extension := ⟨fun _ => none, true⟩

theorem base_only_no_contracts : ∀ s, baseOnly.contracts s = none := fun _ => rfl

/-- A theorem's dependency set: the slots whose contracts it consumes. A present-core theorem has empty
dependencies; a relative theorem lists its consumed slots explicitly. -/
def Dependencies := List Slot

/-- A present-core theorem consumes no contract slot. -/
def presentCoreDeps : Dependencies := []

theorem present_core_no_deps : presentCoreDeps = [] := rfl

end D0.Extensions.X5
