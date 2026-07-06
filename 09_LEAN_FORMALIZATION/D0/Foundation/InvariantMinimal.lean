import Mathlib.GroupTheory.Perm.Basic
import Mathlib.Tactic

/-!
# D0-P-INVARIANT-MINIMAL-001 — orbit-minimality of `R^Aut` on the frozen scene (Lean lift)

Lean lift of the row-550 EXACT-MISSING item (1): the `Fin 33` decidable orbit-count /
minimality lemma named as the mint path by `RAISE_SELECTOR_MINIMAL_MEMO.md` (§Verification,
cert `raise_selector_minimal_check.py` 21/21 + 4 mutations; independent skeptic NO-KILL).

**What is proved here (theorem-grade, this module):**

* `orbit_count_three` — **`dim R^Aut = 3` as an orbit count**: the orbit closure of the
  literal within-zone transposition list partitions `Fin 33` into exactly `3` orbits
  (`R^Aut` = class functions = functions constant on orbits; its dimension is the orbit
  count — the identification is the standard finite fact, cited in prose).
* `deg_classifies_orbits` — the OWNED observable (the K(9,11,13) **degree function**,
  computed from the adjacency, not declared) takes constant values on orbits and
  separates them: `j ∈ orbit i ↔ deg i = deg j`.
* `classifier_constant_on_orbits` — the abstract half: ANY classifier `c` invariant under
  the generators is constant on orbits (structural induction on the orbit closure — this
  is a genuine `∀`-statement over classifiers, NOT a finite enumeration).
* `invariant_minimal_meet` — **the lattice-meet/minimality fact**: for ANY partition
  classifier `c : Fin 33 → α` that is (i) Aut-closed (invariant under the generators) and
  (ii) separates the degree function (`c i = c j → deg i = deg j`), the `c`-partition IS
  the orbit partition: `c i = c j ↔ j ∈ orbit i`. So no Aut-closed proper refinement
  separates the degree function, and every Aut-closed separating partition algebra
  coincides with `R^Aut` — the meet of the separator lattice, attained.

**Honest scope (RR-1/RR-2 of the memo, carried):** the quantification is over PARTITION
classifiers (finite unital subalgebras of `ℚ^V` closed under pointwise multiplication are
exactly partition algebras — standard finite fact, cited not formalized). Invariance is
demanded only under the 30 LITERAL generators, which is WEAKER than full Aut-invariance
(the generators generate `S₉ × S₁₁ × S₁₃` — standard, cited); an Aut-closed algebra
a fortiori satisfies the hypothesis, so the conclusion applies to every Aut-closed
separating algebra. The "every owned functional is a class function" universality stays
EVIDENCE-grade at row-549 scope — this module upgrades ONLY the lattice-extremality leg
(single-witness refinement RR-1 → universal over all partition classifiers).

Model precedent: `D0.Foundation.CanonicalSelectorNoGo` (the equivariant no-go this raise
has as corollary); `native_decide` per the 17-module precedent (no kernel evaluation of
`Fintype (Fin n ≃ Fin n)`; cards appear only under `native_decide`).
-/

namespace D0.Foundation.InvariantMinimal

open Equiv

/-! ## The scene: zones, adjacency, degree (the owned observable) -/

/-- Zone map of `K(9,11,13)`: `0..8 → 0`, `9..19 → 1`, `20..32 → 2`. -/
def zoneOf (i : Fin 33) : Fin 3 :=
  if (i : ℕ) < 9 then 0 else if (i : ℕ) < 20 then 1 else 2

/-- Complete-multipartite adjacency: `i ~ j` iff different zones. -/
def adj (i j : Fin 33) : Prop := zoneOf i ≠ zoneOf j

instance : DecidableRel adj := fun i j => by unfold adj; infer_instance

/-- The **degree function** — the owned observable, COMPUTED from the adjacency
(`deg = 24, 22, 20` on the three zones), not declared. -/
def deg (i : Fin 33) : ℕ := (Finset.univ.filter (fun j => adj i j)).card

/-- The degree takes exactly `3` values on the scene (`{20, 22, 24}`). -/
theorem deg_three_values : (Finset.univ.image deg).card = 3 := by native_decide

/-! ## Orbits of the literal generator list -/

/-- The 30 within-zone adjacent transpositions, as a **literal** list (same list as
`D0.Claims.InvariantGenerationBridge.gens`; kept literal so nothing here is derived from
`zoneOf`). -/
def gens : List (Equiv.Perm (Fin 33)) :=
  [ Equiv.swap 0 1, Equiv.swap 1 2, Equiv.swap 2 3, Equiv.swap 3 4,
    Equiv.swap 4 5, Equiv.swap 5 6, Equiv.swap 6 7, Equiv.swap 7 8,
    Equiv.swap 9 10, Equiv.swap 10 11, Equiv.swap 11 12, Equiv.swap 12 13,
    Equiv.swap 13 14, Equiv.swap 14 15, Equiv.swap 15 16, Equiv.swap 16 17,
    Equiv.swap 17 18, Equiv.swap 18 19,
    Equiv.swap 20 21, Equiv.swap 21 22, Equiv.swap 22 23, Equiv.swap 23 24,
    Equiv.swap 24 25, Equiv.swap 25 26, Equiv.swap 26 27, Equiv.swap 27 28,
    Equiv.swap 28 29, Equiv.swap 29 30, Equiv.swap 30 31, Equiv.swap 31 32 ]

/-- One-step orbit expansion. -/
def step (s : Finset (Fin 33)) : Finset (Fin 33) :=
  s ∪ s.biUnion (fun x => (gens.map (fun g => g x)).toFinset)

/-- Orbit of `i` by finite closure (33 steps saturate on 33 points; the generators are
involutions, so `gens`-word reachability is the group orbit). -/
def orbit (i : Fin 33) : Finset (Fin 33) := step^[33] {i}

/-- **`dim R^Aut = 3` as an orbit count**: exactly `3` orbits. (`R^Aut` = class
functions = functions constant on orbits; dimension = number of orbits.) -/
theorem orbit_count_three : (Finset.univ.image orbit).card = 3 := by native_decide

/-- **The owned observable classifies the orbits**: the degree is constant on each orbit
AND separates distinct orbits — `j ∈ orbit i ↔ deg i = deg j`. -/
theorem deg_classifies_orbits : ∀ i j : Fin 33, (j ∈ orbit i ↔ deg i = deg j) := by
  native_decide

/-! ## The abstract minimality lemma (genuine `∀` over classifiers) -/

/-- If a classifier is invariant under every generator, one expansion step preserves its
constancy over a set. -/
theorem step_constant {α : Type*} {c : Fin 33 → α}
    (hc : ∀ g ∈ gens, ∀ x, c (g x) = c x)
    {s : Finset (Fin 33)} {v : α} (hs : ∀ x ∈ s, c x = v) :
    ∀ x ∈ step s, c x = v := by
  intro x hx
  simp only [step, Finset.mem_union, Finset.mem_biUnion, List.mem_toFinset,
    List.mem_map] at hx
  rcases hx with hx | ⟨y, hy, g, hg, rfl⟩
  · exact hs x hx
  · rw [hc g hg y]; exact hs y hy

/-- **Any generator-invariant classifier is constant on orbits** (structural induction on
the orbit closure — not an enumeration over classifiers). -/
theorem classifier_constant_on_orbits {α : Type*} {c : Fin 33 → α}
    (hc : ∀ g ∈ gens, ∀ x, c (g x) = c x) :
    ∀ i : Fin 33, ∀ j ∈ orbit i, c j = c i := by
  intro i
  have key : ∀ n : ℕ, ∀ j ∈ step^[n] ({i} : Finset (Fin 33)), c j = c i := by
    intro n
    induction n with
    | zero => intro j hj; simp only [Function.iterate_zero, id_eq,
        Finset.mem_singleton] at hj; rw [hj]
    | succ n ih =>
        intro j hj
        rw [Function.iterate_succ_apply'] at hj
        exact step_constant hc ih j hj
  -- rewrite `orbit` syntactically (no whnf normalization of the closure term)
  simpa only [orbit] using key 33

/- After this point `step`/`orbit` are OPAQUE: every computational fact about them is
already proven above (`native_decide` uses the compiler, not the kernel normalizer), and
leaving them semi-reducible lets the elaborator's `whnf` fall into the 33-step closure
term (deterministic-timeout precedent, same family as the CanonicalSelectorNoGo
kernel-`decide` wall). -/
attribute [irreducible] step orbit

/-- **THE MINIMALITY / LATTICE-MEET FACT (D0-P-INVARIANT-MINIMAL-001, Lean leg).**
For ANY partition classifier `c` on the scene that is (i) closed under the automorphism
generators and (ii) separates the owned degree observable, the `c`-partition coincides
exactly with the orbit partition: `c i = c j ↔ j ∈ orbit i`. Consequences: no Aut-closed
proper refinement separates the degree function; every Aut-closed separating partition
algebra IS `R^Aut` (dim 3, `orbit_count_three`) — the meet of the separator lattice is
attained at `R^Aut`. The selector no-go (row 549, LEAN_PROVED
`D0.Foundation.CanonicalSelectorNoGo`) is its corollary: an equivariant section would be
an invariant proper refinement, forbidden here. -/
theorem invariant_minimal_meet {α : Type*} (c : Fin 33 → α)
    (hinv : ∀ g ∈ gens, ∀ x, c (g x) = c x)
    (hsep : ∀ i j : Fin 33, c i = c j → deg i = deg j) :
    ∀ i j : Fin 33, (c i = c j ↔ j ∈ orbit i) := by
  intro i j
  constructor
  · intro h
    exact (deg_classifies_orbits i j).mpr (hsep i j h)
  · intro h
    exact (classifier_constant_on_orbits hinv i j h).symm

end D0.Foundation.InvariantMinimal
