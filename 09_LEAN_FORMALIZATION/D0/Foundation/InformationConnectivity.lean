import Mathlib.Tactic
import D0.Foundation.M1Predicate

/-!
# Information connectivity: the assertable universe of an M1-admissible description is one
record-component

**The claim, informally** (BOOK_00's M1 + the cascade's own trace/comparison floors, applied
to domains of description): everything assertable is assertable only through records; a
domain with which no record chain exists cannot have any of its contents forced by the
finite code — EVERY candidate value for it requires an external catalogue; and two
record-disconnected observers cannot force agreement on any domain (without a shared record
there is no fact of the matter about "who said what"). Hence the assertable universe of an
M1-admissible description is exactly one record-connected component: a disconnected
information domain and an external catalogue are the same thing.

**The model (minimal record semantics, stated as the hypothesis).** Domains `Dom`; a record
relation `Rec` (a shared record connects both ways — connectivity is the equivalence closure
`SameComponent := EqvGen Rec`); contents in `V` with at least one distinguishable
alternative (`Nontrivial V` — in a one-value world there is nothing to assert, and the
hypothesis is load-bearing: the out-of-component freedom theorem fails without it); a
content assignment is ADMISSIBLE when records copy content faithfully (`Rec x y → c x = c y`
— the trace floor's own reading: a record that does not preserve the distinguishable value
is not a record). Richer record semantics are refinements, not rivals: the theorems are
stated against this named constraint.

**Wiring into the OWNED M1 machinery** (`D0.Foundation.M1Predicate`, per its own discipline
— always against a REAL `M1Forced` obligation, never a bare `¬Forced` shell): the constraint
family is `ForcedValue b obs d v` := "every admissible assignment showing `obs` at `b` has
value `v` at `d`". IN-component this family has a unique witness and is `M1Forced`
(`reachable_value_m1_forced` — the non-vacuity control demanded by the predicate module);
OUT-of-component EVERY candidate value satisfies `RequiresExternalCatalogue`
(`unreachable_every_value_needs_catalogue`), witnessed by explicit piecewise-admissible
assignments. The two-observer corollary and the one-component assembly follow.

**Honest scope (pre-registered).**
1. This is a statement about M1-ADMISSIBLE DESCRIPTIONS (what can be scientifically
   asserted), not bare ontology — exactly the scope of M1 itself.
2. Carrier: abstract description domains. NOT the scene graph — the cosmology percolation
   rows (`D0-COSMOLOGY-CONNECTIVITY-THRESHOLD-OWNER-001` etc.) own GRAPH connectivity of the
   reheating scene, a different carrier; no binding.
3. The record semantics (faithful copy) is the module's named minimal reading; the
   extremality leg ("the admissible description sits AT the MDL optimum") is a separate
   future target (P-schema), not claimed here.
-/

namespace D0.Foundation

open Relation
open scoped Classical

variable {Dom V : Type} (Rec : Dom → Dom → Prop)

/-- Record-connectivity: the equivalence closure of the record relation — a shared record
connects both ways, chains compose. -/
def SameComponent (b d : Dom) : Prop := EqvGen Rec b d

/-- Admissibility: records copy content faithfully (the trace floor's reading — a "record"
that does not preserve the distinguishable value is not a record). -/
def AdmissibleContent (c : Dom → V) : Prop := ∀ x y, Rec x y → c x = c y

/-- Admissible contents are constant along record chains. -/
theorem admissible_constant_on_component {Rec : Dom → Dom → Prop} {c : Dom → V}
    (hc : AdmissibleContent Rec c) {b d : Dom} (h : SameComponent Rec b d) :
    c b = c d := by
  induction h with
  | rel x y hxy => exact hc x y hxy
  | refl => rfl
  | symm x y _ ih => exact ih.symm
  | trans x y z _ _ ih₁ ih₂ => exact ih₁.trans ih₂

/-- **The canonical finite constraint** of the observer at `b` who observes `obs` about the
domain `d`: the value `v` is dictated by every admissible assignment compatible with the
observation. This is a REAL constraint family (satisfied uniquely in-component, per the
`M1Predicate` module's own discipline), not a `¬Forced` shell. -/
def ForcedValue (b : Dom) (obs : V) (d : Dom) (v : V) : Prop :=
  ∀ c : Dom → V, AdmissibleContent Rec c → c b = obs → c d = v

/-- **In-component: the value is M1-forced.** For `d` record-connected to `b`, the observed
value is the unique `ForcedValue` witness — the finite code (the observation plus the record
chains) determines it, and nothing outside is needed. Non-vacuity control for the whole
family. -/
theorem reachable_value_m1_forced (b : Dom) (obs : V) {d : Dom}
    (h : SameComponent Rec b d) :
    M1Forced (ForcedValue Rec b obs d) obs where
  forced := fun c hc hb => by
    rw [← admissible_constant_on_component hc h, hb]
  unique := fun v hv => by
    have := hv (fun _ => obs) (fun _ _ _ => rfl) rfl
    exact this.symm

/-- The piecewise witness: observed value on `b`'s component, an arbitrary `v` elsewhere.
Admissible because records never cross components. -/
theorem piecewise_admissible (b : Dom) (obs v : V) :
    AdmissibleContent Rec
      (fun x => if SameComponent Rec b x then obs else v) := by
  intro x y hxy
  by_cases hx : SameComponent Rec b x
  · have hy : SameComponent Rec b y := EqvGen.trans _ _ _ hx (EqvGen.rel _ _ hxy)
    simp [hx, hy]
  · have hy : ¬ SameComponent Rec b y := by
      intro hy
      exact hx (EqvGen.trans _ _ _ hy (EqvGen.symm _ _ (EqvGen.rel _ _ hxy)))
    simp [hx, hy]

/-- **Out-of-component: EVERY candidate value requires an external catalogue.** For `d` not
record-connected to `b`, no value is forced — for each candidate `v` there is an admissible
assignment compatible with the observation whose value at `d` differs (`Nontrivial V` is
load-bearing: with one value there is nothing to assert and the freedom collapses). In the
owned vocabulary: asserting ANY specific content for a record-disconnected domain rests on
data not derivable from the finite code. -/
theorem unreachable_every_value_needs_catalogue [Nontrivial V]
    (b : Dom) (obs : V) {d : Dom} (h : ¬ SameComponent Rec b d) (v : V) :
    RequiresExternalCatalogue (ForcedValue Rec b obs d) v := by
  intro hforced
  obtain ⟨w, hw⟩ := exists_ne v
  have hpw := hforced (fun x => if SameComponent Rec b x then obs else w)
    (piecewise_admissible Rec b obs w)
    (by simp [SameComponent, EqvGen.refl])
  simp only [if_neg h] at hpw
  exact hw hpw

/-- **Two record-disconnected observers cannot force agreement on any domain** — the
"who said what" leg: if both observers' data force a value at `d`, then `d` lies in both
components, hence the observers are record-connected. Contrapositive: no shared record
chain ⇒ no domain whose content both can force ⇒ no fact of the matter about a shared
assertion. -/
theorem disconnected_observers_share_no_forced_domain [Nontrivial V]
    (b₁ b₂ : Dom) (obs₁ obs₂ : V) (hsep : ¬ SameComponent Rec b₁ b₂) (d : Dom)
    (v₁ v₂ : V)
    (h₁ : M1Forced (ForcedValue Rec b₁ obs₁ d) v₁)
    (h₂ : M1Forced (ForcedValue Rec b₂ obs₂ d) v₂) :
    False := by
  by_cases hd₁ : SameComponent Rec b₁ d
  · by_cases hd₂ : SameComponent Rec b₂ d
    · exact hsep (EqvGen.trans _ _ _ hd₁ (EqvGen.symm _ _ hd₂))
    · exact unreachable_every_value_needs_catalogue Rec b₂ obs₂ hd₂ v₂ h₂.forced
  · exact unreachable_every_value_needs_catalogue Rec b₁ obs₁ hd₁ v₁ h₁.forced

/-- **Information connectivity** (assembly): in-component values are M1-forced with the
observation as unique witness; out-of-component EVERY value requires an external catalogue;
record-disconnected observers share no forced domain. The assertable universe of an
M1-admissible description is exactly one record-connected component — a disconnected
information domain and an external catalogue are the same thing. -/
theorem information_connectivity [Nontrivial V] (b : Dom) (obs : V) :
    (∀ d, SameComponent Rec b d → M1Forced (ForcedValue Rec b obs d) obs)
      ∧ (∀ d, ¬ SameComponent Rec b d →
          ∀ v : V, RequiresExternalCatalogue (ForcedValue Rec b obs d) v)
      ∧ (∀ b₂ obs₂ d (v₁ v₂ : V), ¬ SameComponent Rec b b₂ →
          M1Forced (ForcedValue Rec b obs d) v₁ →
          M1Forced (ForcedValue Rec b₂ obs₂ d) v₂ → False) :=
  ⟨fun _ h => reachable_value_m1_forced Rec b obs h,
    fun _ h v => unreachable_every_value_needs_catalogue Rec b obs h v,
    fun b₂ obs₂ d v₁ v₂ hsep h₁ h₂ =>
      disconnected_observers_share_no_forced_domain Rec b b₂ obs obs₂ hsep d v₁ v₂ h₁ h₂⟩

end D0.Foundation
