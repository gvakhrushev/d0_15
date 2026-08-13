# INFORMATION-CONNECTIVITY — the assertable universe is one record-component (MINTED)

**Status:** MINTED as `D0-INFORMATION-CONNECTIVITY-001` (2026-08-14) after independent
skeptic verdict **MINT-AFTER-REPAIRS** — all required repairs were row-note wording, none
touched the Lean. Skeptic independently reproduced builds (2948/4477 GREEN) and axiom
profiles; verified all 6 theorem names, the EqvGen mechanics, the verbatim quotes, and the
carrier separations; proved in a scratch file that the piecewise witness is load-bearing
exactly at v = obs (for v ≠ obs the constant assignment alone suffices) — so ATT-A fails as
a kill. **Repairs applied (errors of record):** (1) classifier trap — naming the cosmology
row ID in the note would trip the substring `cosmo` → domain=cosmology with a wrong scope
guard; the note names the carrier as "graph-connectivity rows of the reheating scene
(BOOK_08 08.52 owners)" instead; (2) honesty sentence: clause 2 extends the M1Predicate
pattern (proven-unsatisfiable uniform family + clause-1 control at a different parameter d),
it is not a per-d M1Forced obligation as in the m1_* lemmas; (3) scope sentence: the family
is a universal/semantic constraint, not a finite selector — the 'finite code' reading is
exact on the in-component leg only; (4) the license framing below ("not an open question")
was overselling and is REPLACED by: whatever is M1-forced lies in the observer's
record-component, so for assertable content the question shifts from WHETHER to WHICH
carrier — no connectivity of any actual substrate pair is asserted; applying the license
requires identifying Rec (bridge step, not discharged). Advisory accepted: the two-observer
leg is labeled a corollary of clause 2 + transitivity; the pre-flight 'exogenous' count
below was 8, not 10 (corrected). Pre-flight: 'CONNECTIVITY' in the
registry is owned by cosmology PERCOLATION rows (graph connectivity of the reheating scene —
different carrier, pre-registered non-binding); 'exogenous' appears in 8 rows, all M1-family;
no record-connectivity-of-description-domains content anywhere; the owned machinery is
`D0.Foundation.M1Predicate` (M1Forced / RequiresExternalCatalogue + its own discipline:
"always against a REAL M1Forced obligation, never a bare ¬Forced shell"). Origin: the
2026-08-10 owner conversation — "не может быть отдельных несвязанных информационных доменов;
если есть несвязанное == внешний каталог == недоказуемая магия" — upgraded from axiom-grade
intuition to a theorem against the owned predicate.

## Claim X (DEF-0.2.2 form)

X (Lean `D0.Foundation.InformationConnectivity`; standalone 2948 GREEN + D0.All 4477 GREEN;
axioms propext/Classical.choice/Quot.sound on the assembly, and `reachable_value_m1_forced`
is axiom-FREE): under the minimal record semantics — domains `Dom`, records `Rec`,
connectivity = equivalence closure `SameComponent = EqvGen Rec`, contents in `V` with
`Nontrivial V` (at least one distinguishable alternative), admissibility = records copy
content faithfully (`Rec x y → c x = c y`) — for an observer at `b` with observation `obs`:

1. **In-component, M1-forced**: for every `d` with `SameComponent b d`, the constraint
   family `ForcedValue b obs d` ("dictated by every admissible assignment compatible with
   the observation") has `obs` as its unique witness: `M1Forced (ForcedValue b obs d) obs`
   (`reachable_value_m1_forced`) — the non-vacuity control the predicate module demands;
2. **Out-of-component, every value is catalogue**: for every `d` with
   `¬ SameComponent b d` and EVERY `v : V`:
   `RequiresExternalCatalogue (ForcedValue b obs d) v`
   (`unreachable_every_value_needs_catalogue`), witnessed by explicit piecewise-admissible
   assignments (observed value on the component, arbitrary value elsewhere — admissible
   because records never cross components, `piecewise_admissible`);
3. **Two disconnected observers share no forced domain** (the "who said what" leg):
   `M1Forced` for both observers at any common `d` implies the observers are
   record-connected (`disconnected_observers_share_no_forced_domain`);
4. assembly `information_connectivity`.

Net, in the owner's phrasing made exact: **a record-disconnected information domain and an
external catalogue are the same thing** — the assertable universe of an M1-admissible
description is exactly one record-connected component. License reading (model-level,
post-skeptic wording): whatever is M1-forced for an observer lies in the observer's
record-component, so for assertable content the open question shifts from WHETHER connected
to WHICH carrier realizes the record relation — no connectivity of any actual substrate
pair is asserted; applying the license requires identifying Rec (bridge step, not
discharged here).

## Owned pre-facts (verbatim, file:line)

- `M1Predicate.lean:40-52`: `M1Forced` structure; `RequiresExternalCatalogue Forced b :=
  ¬ Forced b` with the load-bearing warning: "A bare `¬ Forced` over a vacuous `Forced` is
  not a theorem about anything. The `m1_*` lemmas below are therefore always stated against
  an `M1Forced` hypothesis" — the discipline this module obeys: the SAME `ForcedValue`
  family is uniquely satisfied in-component (clause 1) and universally catalogue
  out-of-component (clause 2).
- `M1Predicate.lean:5-11`: "an exogenous parameter / external catalogue is exactly
  that-which-cannot-be-proven from the canonical finite data" — the reading clause 2
  instantiates.
- Cascade floors "leave a trace / a trace without comparison is not a trace / comparison
  needs memory" (§01.6.1c, carried rows) — the admissibility reading's anchor: a record
  that does not preserve the distinguishable value is not a record.
- Percolation rows `D0-COSMOLOGY-CONNECTIVITY-THRESHOLD-OWNER-001`,
  `D0-REHEATING-PERCOLATION-OWNER-001`, `D0-CONNECTIVITY-SPECTRAL-GAP-SPEED-001` — GRAPH
  connectivity of the scene, different carrier, non-binding (pre-registered).

## The forcing / construction

All proofs constructive-flavoured and short: EqvGen induction for constancy along chains;
the in-component leg needs no axioms at all; the out-of-component leg is the explicit
piecewise witness (classical decidability of component membership only); the two-observer
leg is case analysis. No `decide`, no `native_decide`, no numerics.

## Named risks & PRE-REGISTERED attack surface (strongest first)

- **ATT-A (strongest: definitional tautology).** "Assertable = record-determined" could be
  read as making the theorem true by definition. Defense, pre-registered: the content is
  (i) the WIRING into the owned M1 machinery with the REAL-obligation discipline satisfied —
  the same family is uniquely-witnessed in-component (control) and universally-catalogue
  out-of-component; (ii) the explicit witness constructions (piecewise admissibility is a
  theorem, not a stipulation — it can FAIL: with records crossing components it fails, and
  with trivial V clause 2 fails); (iii) the two-observer corollary, which is not a
  restatement of either definition. A kill must show a conjunct that holds vacuously or a
  Forced family that is a ¬Forced shell.
- **ATT-B (Nontrivial V load-bearing).** With one value clause 2 collapses — stated in the
  module and here; the hypothesis is inside the statement.
- **ATT-C (record semantics).** Faithful-copy admissibility is the module's named minimal
  reading (anchored on the trace floor); noisy/лossy records are a REFINEMENT axis (and the
  named future import: an error-correction floor), not a rival — stated. A kill must name an
  owned D0 record semantics this contradicts.
- **ATT-D (carrier mismatch).** Percolation/graph-connectivity rows are a different carrier;
  the scene graph is NOT this module's Dom; no binding, pre-registered.
- **ATT-E (scope inflation).** The theorem is about M1-ADMISSIBLE DESCRIPTIONS (assertable
  content), not bare ontology; the row must say so; "единая цепная реакция саморазвёртки"
  remains the prose reading whose exact carried part is this theorem.

## What this does NOT show

Ontological monism (scope: admissible descriptions); the extremality leg ("the description
sits AT the MDL optimum" — separate P-schema target); any statement about the scene graph;
noisy-record/error-correction semantics (named future floor, biology+holography anchors);
the cross-substrate coverage matrix itself (the program this theorem licenses).
