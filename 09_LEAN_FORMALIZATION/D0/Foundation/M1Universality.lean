import Mathlib.Tactic

/-!
# M1-universality — grammar-functoriality of the exogenous-parameter test (DRAFT v2 post-skeptic)

Claim family: `D0-M1-UNIVERSALITY-001` (candidate). Memo:
`_TASKS_CENTER_ATTACK/M1_UNIVERSALITY_MEMO.md` (v2; skeptic #18 wounds repaired R1–R8).

M1 is stated in the corpus for the D0 grammar. The universality claim: M1 is a SCHEMA over
description systems — for any grammar `G`, the exogenous-parameter test DEF 0.3.1
(B00:398/:455-459) reads: θ is exogenous iff it "(1) is not derived inside the corpus,
(2) affects a distinguishable result or a law's formulation, and (3) is not an unavoidable part
of the distinguishability protocol". This module machine-checks the schema's CLAUSE-1
(derivability) leg: the classification is stable in BOTH directions along faithful
interpretations, and cannot be manufactured or destroyed by re-grammatization.

Correspondence of fields to the book (skeptic #18 R3): `h_underived` = clause 1 (system-
relative — the ONLY grammar-sensitive clause); `outcomeAffecting`/`h_out` = clause 2 and
`notProtocol`/`h_np` = clause 3 — both PROTOCOL-level, carried as hypotheses (whether a
translation preserves a protocol's obligations is per-instantiation, NOT proved here);
`mandatory` = the DEF 0.3.1a mandatoriness rider.

Relation to `D0.Foundation.M1Predicate` (skeptic #18 R7): that module formalizes M1-forcing
WITHIN one system (`M1Forced` = unique witness of a canonical finite constraint;
`RequiresExternalCatalogue` = failure of the constraint). This module formalizes stability of
the exogenous classification ACROSS systems. The abstractions are disjoint by design
(within-system uniqueness vs cross-system transport); composing them (transport of `M1Forced`
along faithful maps) is future work, not claimed.

NOT machine-checked (narrated, external-owner grade): the AIT leg — B00:471 already owns the
conditional-complexity form ("Adding an underivable θ moves the law from `K(T)` to
`K(T) + K(θ|T)`"); its machine-independence is the classical (conditional) invariance theorem
`|K_U(x|y) − K_V(x|y)| ≤ c_{U,V}`. The robust separation is a FAMILY statement (memo Leg B):
for an empirical-catalog family `C_n`, a generating theory has `∃c ∀n, K(C_n|T) ≤ c` while an
importing theory does not — pointwise `O(1)` over a single finite pair separates nothing
(skeptic #18's named gap, conceded and repaired at the family level). No Kolmogorov complexity
exists in mathlib; this leg stays cited, never formalized here.

Per trap (m): the sole content of the abstract theorems IS the schema attribution — clause 1 of
the M1 test is grammar-functorial along faithful interpretations; nothing grammar-specific is
claimed, and no localization corollary is asserted (v1's was killed and is withdrawn).
-/

namespace D0.Foundation.M1Universality

/-- An abstract description system: a type of sentences with a derivability predicate. -/
structure DescSystem where
  Sent : Type
  derivable : Sent → Prop

/-- An M1 exogenous witness relative to a system `S` — DEF 0.3.1 with the book's numbering:
clause 1 (`h_underived`, system-relative), clause 2 (`outcomeAffecting`, protocol-level datum),
clause 3 (`notProtocol`, protocol-level datum), plus the 0.3.1a mandatoriness rider. -/
structure ExogenousWitness (S : DescSystem) where
  θ : S.Sent
  mandatory : Prop
  outcomeAffecting : Prop
  notProtocol : Prop
  h_mand : mandatory
  h_out : outcomeAffecting
  h_np : notProtocol
  h_underived : ¬ S.derivable θ

/-- A faithful interpretation: a sentence translation preserving AND reflecting derivability. -/
structure Faithful (S₁ S₂ : DescSystem) where
  map : S₁.Sent → S₂.Sent
  iff_derivable : ∀ s, S₁.derivable s ↔ S₂.derivable (map s)

/-- **Transport (clause 1, forward).** A faithful interpretation carries exogenous witnesses
forward: the underivability of θ survives translation (uses the REFLECTION direction — see
`nc1` for the kernel-checked countermodel without it). Clauses 2/3 and mandatoriness are
protocol-level and carried as data. -/
def ExogenousWitness.transport {S₁ S₂ : DescSystem} (F : Faithful S₁ S₂)
    (w : ExogenousWitness S₁) : ExogenousWitness S₂ where
  θ := F.map w.θ
  mandatory := w.mandatory
  outcomeAffecting := w.outcomeAffecting
  notProtocol := w.notProtocol
  h_mand := w.h_mand
  h_out := w.h_out
  h_np := w.h_np
  h_underived := fun h => w.h_underived ((F.iff_derivable w.θ).mpr h)

/-- **Preservation (the `.mp` side).** Derivability itself transports forward. -/
theorem faithful_preserves_derivable {S₁ S₂ : DescSystem} (F : Faithful S₁ S₂) (s : S₁.Sent)
    (h : S₁.derivable s) : S₂.derivable (F.map s) :=
  (F.iff_derivable s).mp h

/-- **Reflection (the `.mpr` side).** Derivability also reflects backward. -/
theorem faithful_reflects_derivable {S₁ S₂ : DescSystem} (F : Faithful S₁ S₂) (s : S₁.Sent)
    (h : S₂.derivable (F.map s)) : S₁.derivable s :=
  (F.iff_derivable s).mpr h

/-- **No manufacture (stated theorem — skeptic #18 R4).** A faithful translation cannot CREATE
an exogenous witness: if θ is derivable (hence not a witness) in `S₁`, its image is derivable
(hence not a witness) in `S₂`. This uses the PRESERVATION direction — see `nc2` for the
kernel-checked countermodel without it. -/
theorem witness_not_manufactured {S₁ S₂ : DescSystem} (F : Faithful S₁ S₂) (s : S₁.Sent)
    (h : S₁.derivable s) : ¬ ¬ S₂.derivable (F.map s) :=
  fun hn => hn (faithful_preserves_derivable F s h)

/-- **Grammar-functoriality bundle (both directions delivered).** Along a faithful
interpretation: witnesses transport, derivability preserves and reflects, and witnesses cannot
be manufactured. -/
theorem m1_grammar_functorial {S₁ S₂ : DescSystem} (F : Faithful S₁ S₂) :
    (∀ w : ExogenousWitness S₁, ¬ S₂.derivable (F.map w.θ)) ∧
    (∀ s, S₁.derivable s → S₂.derivable (F.map s)) ∧
    (∀ s, S₂.derivable (F.map s) → S₁.derivable s) :=
  ⟨fun w => (w.transport F).h_underived,
   faithful_preserves_derivable F,
   faithful_reflects_derivable F⟩

/-! ## Finite worked instance (kernel-checked): a re-encoding with junk symbols -/

/-- Toy grammar 1: sentences are `Fin 4`; derivable = {0, 1}. -/
def G₁ : DescSystem := ⟨Fin 4, fun s => s.val < 2⟩

/-- Toy grammar 2: a re-encoding with junk — sentences `Fin 8`; derivable = even values < 4. -/
def G₂ : DescSystem := ⟨Fin 8, fun s => s.val < 4 ∧ s.val % 2 = 0⟩

/-- The translation: doubling (injective re-encoding of the same content). -/
def dbl : Faithful G₁ G₂ where
  map := fun s => ⟨2 * s.val, by omega⟩
  iff_derivable := by
    intro s
    show s.val < 2 ↔ (2 * s.val < 4 ∧ 2 * s.val % 2 = 0)
    omega

/-- Instance check: sentence `2` of `G₁` is underived there and its translation `4` is
underived in `G₂` — the classification survives the re-encoding. -/
theorem toy_transport :
    ¬ G₁.derivable ⟨2, by omega⟩ ∧ ¬ G₂.derivable (dbl.map ⟨2, by omega⟩) := by
  refine ⟨?_, ?_⟩
  · show ¬ ((2 : ℕ) < 2)
    omega
  · show ¬ ((2 * 2 : ℕ) < 4 ∧ (2 * 2 : ℕ) % 2 = 0)
    omega

/-! ## Negative controls (kernel-checked countermodels — skeptic #18 R5; each fails the
CONCLUSION, not the technique) -/

/-- Preservation-only toy pair: identity map from "only 0 derivable" to "everything derivable".
Preserves derivability; does NOT reflect it. -/
def H₁ : DescSystem := ⟨Fin 2, fun s => s.val = 0⟩
def H₂ : DescSystem := ⟨Fin 2, fun _ => True⟩

/-- **NC1 (transport fails without reflection).** Under the preservation-only identity
translation `H₁ → H₂`, the sentence `1` is underivable in `H₁` (a clause-1 witness) but its
image IS derivable in `H₂` — the transport CONCLUSION is false. Reflection is exactly the
load-bearing hypothesis of `transport`. -/
theorem nc1_transport_fails_without_reflection :
    (∀ s : Fin 2, H₁.derivable s → H₂.derivable s) ∧
    ¬ H₁.derivable ⟨1, by omega⟩ ∧
    H₂.derivable ⟨1, by omega⟩ := by
  refine ⟨fun s _ => trivial, ?_, trivial⟩
  show ¬ ((1 : ℕ) = 0)
  omega

/-- **NC2 (a witness IS manufactured without preservation).** Under the reflection-only
identity translation `H₂ → H₁` (reflects trivially since everything is derivable in `H₂`), the
sentence `1` is derivable in `H₂` (NOT a witness) but its image is underivable in `H₁` — a
witness is manufactured. Preservation is exactly the load-bearing hypothesis of
`witness_not_manufactured`. -/
theorem nc2_witness_manufactured_without_preservation :
    (∀ s : Fin 2, H₁.derivable s → H₂.derivable s) ∧
    H₂.derivable ⟨1, by omega⟩ ∧
    ¬ H₁.derivable ⟨1, by omega⟩ := by
  refine ⟨fun s _ => trivial, trivial, ?_⟩
  show ¬ ((1 : ℕ) = 0)
  omega

end D0.Foundation.M1Universality
