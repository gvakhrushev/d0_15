import Mathlib.Tactic
import D0.Foundation.CascadeChain

/-!
# Cascade floor: defect ⇒ circulation needs closure

**Target: `D0-CASCADE-INSUFFICIENCY-CHAIN-001`** (umbrella; after the second interlock link it
sits at #2 of the computed attack queue). The §01.6.1c cascade reads
`… the torus is abelian, so order is not encoded ⇒ defect ⇒ circulation needs closure ⇒
shell …`. The scaffold carries no floor for the `defect ⇒ closure` step. This module carries
it, in the registered `CascadeStep` shape.

**The step's semantics, formalized.** The defect that repairs the order floor is the
commutator `[a,b] = a·b·a⁻¹·b⁻¹` — the exact element measuring the failure of
commutativity. On the abelian carrier it is identically `1`: nothing to measure
(`abelian_defect_trivial`). On the order-repair carrier (`S₃`, the scaffold's registered
repair) defects exist (`defect_exists`) — but the defect AS AN ELEMENT is not well-defined
circulation data: it depends on the basepoint. Conjugation is the basepoint move, and the
element-level defect assignment is NOT conjugation-invariant on `S₃`
(`element_defect_not_invariant`, explicit witness). The reading that IS invariant is the
CLOSED one: the conjugacy CLASS of the defect (`class_defect_invariant`, fully generic) —
and conjugacy classes of `π₁` are exactly the FREE-HOMOTOPY classes of CLOSED loops (the
standard correspondence, docstring-grade citation; not re-proved). So the floor says
literally what the prose says: *circulation needs closure* — the defect datum survives the
basepoint move only as a closed-loop (class) datum.

```
Floor        the element-level (open, basepointed) defect reading
Obligation   INVARIANCE — circulation data must survive the basepoint move (conjugation)
insufficient on the order-repair carrier S₃ the element reading fails (explicit witness)
control      the class (closed-loop) reading is invariant — the obligation is satisfiable
degenerate   on the abelian carrier invariance holds vacuously: every defect is 1 —
             invariance-without-content, which is why the floor only OPENS once order
             is repaired (the interlock discipline: the repair creates the carrier on
             which the next obligation is asked, and fails it)
```

**Honest scope (pre-registered).**
1. This floor owns `defect ⇒ circulation needs closure` ONLY. The next prose step
   `closure ⇒ shell` (the 2-cell/attachment layer) remains unformalized; the umbrella stays
   OPEN.
2. "Conjugacy classes of `π₁` = free-homotopy classes of closed loops" is the standard
   correspondence, cited at docstring grade (the same convention grade as the corpus's
   eigenvalue↔root pointer); the Lean content is the group-theoretic invariance split
   itself.
3. NO binding to the prose gloss "generations = defect classes" (§01.6.1c list) — that is a
   separate reading with its own owner burden; this floor binds nothing to generations.
4. NO binding to the Q₈ role-group conjugacy-class partition owned in the GAP-E context
   (`FactorBlockLaw`) — different carrier, different campaign; the class construction here
   is Mathlib's `ConjClasses`, used generically.
5. PLACEMENT (repaired per skeptic): in the §01.6.1c prose one-liner the defect step is
   order-memory's IMMEDIATE successor (the scale step comes earlier — the prose-order caveat
   registered at `D0-CASCADE-INTERLOCK-SCALE-001`), so the third link matches PROSE adjacency
   exactly; the scaffold's carried numbering does not yet assign this floor an index. It is
   registered as a floor + link package, not as a renumbering of the scaffold.
6. In the scaffold's carrier grammar ("the obligation is recorded at both carriers — as the
   proposition it actually becomes there", CascadeChain verbatim): the below carrier is `S₃`
   (the order repair) and the above carrier is the QUOTIENT `ConjClasses (Equiv.Perm (Fin 3))`
   — the Above obligation is literally the statement that the circulation datum DESCENDS to
   the quotient carrier. In-corpus anchors: BOOK_03 §03.23.4 owns the defect as "injecting a
   non-commutative holonomy on the same loop basis" (the defect-datum reading used here);
   BOOK_03 §03.23.5 owns the OTHER closure — the outer-shell/global-topology closure — which
   is exactly the still-open `closure ⇒ shell` half. Two named, non-competing closures.
-/

namespace D0.Foundation

/-- The defect: the commutator element, the exact measure of the order floor's failure. -/
def commDefect {G : Type*} [Group G] (a b : G) : G := a * b * a⁻¹ * b⁻¹

/-- On an abelian carrier every defect is trivial — nothing to measure; invariance below
holds only vacuously. -/
theorem abelian_defect_trivial {G : Type*} [CommGroup G] (a b : G) : commDefect a b = 1 := by
  simp only [commDefect]
  group
  simp [mul_comm]

/-- On the order-repair carrier the defect exists: `S₃` has a nontrivial commutator. -/
theorem defect_exists : ∃ a b : Equiv.Perm (Fin 3), commDefect a b ≠ 1 := by
  decide

/-- **`insufficient` — the element-level defect reading is not circulation data.** On the
order-repair carrier the defect as an ELEMENT does not survive the basepoint move: an
explicit conjugation changes it. -/
theorem element_defect_not_invariant :
    ¬ ∀ g a b : Equiv.Perm (Fin 3), g * commDefect a b * g⁻¹ = commDefect a b := by
  decide

/-- **`control` — the CLOSED (class) reading is invariant, generically.** The conjugacy
class of any element survives every basepoint move: circulation is well-defined exactly as
a closed-loop datum. -/
theorem class_defect_invariant {G : Type*} [Group G] (g x : G) :
    ConjClasses.mk (g * x * g⁻¹) = ConjClasses.mk x := by
  rw [ConjClasses.mk_eq_mk_iff_isConj, isConj_iff]
  exact ⟨g⁻¹, by group⟩

/-- The exact "same requirement" instantiated at the class reading of the defects
themselves: the defect's conjugacy class survives the basepoint move (restricted corollary
of `class_defect_invariant`). -/
theorem class_defect_of_commutator_invariant (g a b : Equiv.Perm (Fin 3)) :
    ConjClasses.mk (g * commDefect a b * g⁻¹) = ConjClasses.mk (commDefect a b) :=
  class_defect_invariant g (commDefect a b)

/-- **The floor, in the registered `CascadeStep` shape**: the obligation (invariance of the
circulation datum under the basepoint move) fails for the element reading on the
order-repair carrier and holds for the closed/class reading. -/
def stepDefectClosure : CascadeStep where
  name := "circulation needs closure (defect floor)"
  ObligationBelow := ∀ g a b : Equiv.Perm (Fin 3), g * commDefect a b * g⁻¹ = commDefect a b
  ObligationAbove := ∀ g x : Equiv.Perm (Fin 3),
    ConjClasses.mk (g * x * g⁻¹) = ConjClasses.mk x
  insufficient := element_defect_not_invariant
  control := fun g x => class_defect_invariant g x

/-- **The third interlock link (order repair → defect floor)**: the very carrier that
repairs order memory (i) carries nontrivial defects, (ii) fails the element-level
invariance obligation, and (iii) satisfies the closed/class reading — the repair creates
the object on which the next obligation is asked, fails its open form, and forces the
closed one. -/
theorem chain_linked_order_to_defect_closure :
    OrderEncoded (Equiv.Perm (Fin 3))
      ∧ (∃ a b : Equiv.Perm (Fin 3), commDefect a b ≠ 1)
      ∧ ¬ (∀ g a b : Equiv.Perm (Fin 3), g * commDefect a b * g⁻¹ = commDefect a b)
      ∧ (∀ g x : Equiv.Perm (Fin 3), ConjClasses.mk (g * x * g⁻¹) = ConjClasses.mk x) :=
  ⟨control_orderEncoded, defect_exists, element_defect_not_invariant,
    fun g x => class_defect_invariant g x⟩

/-- **Non-collapse with the degenerate side**: on the abelian carrier the element obligation
holds — but only because every defect is `1` (invariance without content). The floor's bite
is exactly on the carriers where a defect exists. -/
theorem abelian_invariance_is_vacuous {G : Type*} [CommGroup G] :
    (∀ g a b : G, g * commDefect a b * g⁻¹ = commDefect a b)
      ∧ ∀ a b : G, commDefect a b = 1 :=
  ⟨fun g a b => by simp [abelian_defect_trivial], abelian_defect_trivial⟩

/-- The floor is genuine: obligations below and above do not coincide (`step_discriminates`
applied to the registered step). -/
theorem defect_closure_floor_genuine :
    ¬ (stepDefectClosure.ObligationBelow ↔ stepDefectClosure.ObligationAbove) :=
  step_discriminates stepDefectClosure

end D0.Foundation
