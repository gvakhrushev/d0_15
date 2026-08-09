# The D0 Epistemic Engine — why the "weaknesses" are the architecture

**Read this second** (after [README.md](README.md)). This document reframes, with receipts, the
features of D0 that a fast reader files under "weaknesses" — bridges, no-gos, open rows, an
unproven axiom, a parametric α tail — as what they actually are: the load-bearing components of
a theory built so that it *cannot quietly lie to itself*. Every claim here links to a ledger row
or a campaign memo; nothing is rhetoric without a file behind it.

---

## 1. The engine is the product

D0 ships two things: a finite theory of physics, and the **adversarial forcing engine** that
built it. The engine is domain-independent and normatively specified in
[docs/ADVERSARIAL_FORCING_ENGINE_SPEC.md](docs/ADVERSARIAL_FORCING_ENGINE_SPEC.md):
pre-flight against the ledger → compute-first with can-fail certificates → memo with a
PRE-REGISTERED attack surface → independent skeptic with a kill mandate (a kill requires a
named second object or a precise named gap) → kills accepted in full, no defense, recorded as
errors-of-record plus reopening hooks.

Its track record is part of the corpus, not marketing: across the 2026-07 campaigns, **19
independent skeptic passes**, 8+ author claims killed and accepted in full, several
wounded-and-repaired — **zero false claims entered the record**. Two of those kills happened to
the engine's own operator mid-session and are archived with their refuting objects
([CLOSE_GAP_E_LEAN_LIFT_MEMO](_TASKS_CENTER_ATTACK/CLOSE_GAP_E_LEAN_LIFT_MEMO.md),
[F3_ANTIDIAGONAL_CANDIDATE_MEMO](_TASKS_CENTER_ATTACK/F3_ANTIDIAGONAL_CANDIDATE_MEMO.md) — the
kill record is IN the memo that survived it). Each kill also hardened the engine itself: the
traps checklist gained two new entries (encoding-tautology, authored-carrier) from this
session's kills. That is antifragility in the literal, checkable sense.

**The ratchet.** A kill never deletes information: it is recorded with its named refuting
object and a reopening hook. Killed stays killed until the hook fires. The candidate space
narrows monotonically — which is what "доказательство от противного" looks like when it is
run as an industrial process instead of a one-shot argument.

## 2. Bridges are a declared attack surface, not holes

The corpus carries **25 named bridge assumptions**, each with an owner file and a written
failure condition ([LEAN_ASSUMPTION_LEDGER.csv](09_LEAN_FORMALIZATION/docs/LEAN_ASSUMPTION_LEDGER.csv)).
A theory that hides its imports has zero bridges on paper and unbounded bridges in fact. D0's
ledger is the exhaustive, falsifiable list of exactly where the finite core hands off to
external mathematics — Lorentz macro-integration, Rieffel convergence, Wilson lattice, Tomita
time, Verlinde gravity. Refute a bridge and you know precisely which rows fall; that is a
feature no continuum-first theory currently offers. The contract is explicit: *a bridge is a
proof obligation, never a positive closure*
([D0_CLAIM_CLOSURE_CONTRACT.md](D0_CLAIM_CLOSURE_CONTRACT.md)).

## 3. No-gos are boundary theorems — the theory maps its own edge

**79 impossibility results** (72 `NO-GO` + 7 `NO_GO_PROVED`) are first-class theorems with
declared admissible classes: colour is NOT derivable from the scene's three zones
(`D0-COLOUR-GENERATION-TYPED-CARRIER-NOGO-001`), the Weyl structure of the SM group is NOT
extractable from the canonical geometry (`D0-HYPERCHARGE-GRAPH-FLOW-OWNER-001` walls), the
ζ-residue route to Δα is BLOCKED by transcendence (`D0-CVFT-F1`, Lindemann). A theory that
proves what it CANNOT do has a boundary you can stand on; most speculative frameworks have a
fog. Many no-gos additionally carry their positive face — the extremality/saturation theorems
(`D0-P-M1-SATURATION-001` family, Lean: `D0.Foundation.M1CoreSaturation`): "cannot be more"
re-read as "already saturates its extremum," machine-checked.

## 4. Open rows are pre-registered falsifiers, not confessions

**55 PROOF-TARGETs** name their exact missing object. The α-line is the exemplar of the
discipline ([ALPHA_SEAM_FORM_FORCED_MEMO](_TASKS_CENTER_ATTACK/ALPHA_SEAM_FORM_FORCED_MEMO.md)):
the criterion is **uniqueness + progressive narrowing**, not digit-matching. Three of the
dressing's five degrees of freedom are Lean-owned theorems; the remaining two (the φ⁻¹²
transport factor; the cross-scope rate identification) are REGISTERED open obligations with a
seven-rival separated falsifier surface and an honest `rc=2` certificate — the 9-digit CODATA
agreement is a *consequence-grade check* (CHK), deliberately never the criterion, and the last
~10⁻⁸ is a standing falsifiable bet (`D0-ALPHA-MEASUREMENT-LIMIT-001`). "The theory must prove
uniqueness and narrow the space to one point" — that sentence is implemented as registry
mechanics, not stated as philosophy.

## 5. M1 is not a parochial axiom — the criterion is grammar-stable (now a theorem)

The standing objection "M1/reductio only works inside D0's grammar" is answered at theorem
grade where it can be: `D0.Foundation.M1Universality` (row `D0-M1-UNIVERSALITY-001`,
LEAN_PROVED for the derivability clause) proves the exogenous-parameter test is **transported
and reflected along faithful interpretations** — with kernel-checked countermodels showing each
direction load-bearing — and the AIT razor holds in machine-independent FAMILY form via the
conditional invariance theorem (`K(C_n|T)` bounded for a generating theory, unbounded for an
importing one; harmonized with the owned conditional-MDL sentence at BOOK_00:471). What remains
grammar-relative is exactly the finite, named list of primitives — the entry contract's role
symbol and window — and that list has been *shrinking by theorem*: the window's upper wall fell
in 2026-07 (below).

## 6. Case study — GAP-E: an "open weakness" converted end-to-end

The scene-uniqueness capstone `scene_triple_unique` was honest about its conditional wall: the
window `[9,13]`'s upper bound was OPEN through nine adversarial passes, each recorded. Then the
engine did what it is for: pass 10 found a missed owned kill (parity), pass 11 sealed at
operative grade modulo three named transfers, pass 12 took **door (b)** — the port-power
exhaustion, whose domain sentence is GENERATED by the owned CORE two-comparison-kind count
rather than postulated — and pass 13 lifted the arithmetic to Lean
(`D0.Tower.PortPowerExhaustion`, wired, `lake build` green) with the categorical leg still
honestly PROOF-TARGET. Twelve documented failures, then a closure that inherits from CORE
instead of adding an axiom. The "weakness" was a queue position, not a defect — and the queue
is public.

## 7. How to attack D0 (the invitation is the point)

The corpus tells you where to aim, in order of leverage: refute a bridge (25 targets, each with
failure semantics); fire a reopening hook (every no-go and kill names its own); exhibit a
second object against any uniqueness row (the kill rule works for outsiders too); break a
certificate (every cert must be able to fail — `check_cert_can_fail.py` enforces it); or supply
the missing object of any PROOF-TARGET and watch what it forces. A theory is serious exactly to
the degree that attacking it is well-posed. Here it is well-posed by construction — the same
engine that builds the theory is handed to its critics as
[an exportable skill](docs/ADVERSARIAL_FORCING_ENGINE_SPEC.md).
