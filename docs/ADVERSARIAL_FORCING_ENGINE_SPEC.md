# The Adversarial Forcing Engine — normative specification (domain-independent)

**Status:** normative spec, v1.0, 2026-07-18. Extracted from the D0 campaign after 17
independent skeptic passes across the 2026-07 sessions (8 author claims killed and accepted in
full; several wounded-and-repaired; **zero false claims entered any record**). D0 is the
reference instantiation; this spec is written so ANY claims-driven project (a mathematical
theory, a protocol spec, a codebase invariant set, a research program) can run the same engine.

The engine is the answer to one question: **how does an author — human, AI, or the pair —
advance a body of claims without ever fooling itself?** The D0 corpus's own answer has two
halves: a *criterion* (M1: no obligatory, outcome-affecting, underived structure) and a
*procedure* (this loop). The criterion is instantiated per project; the procedure is invariant.

---

## 1. Objects

- **Ledger.** A single source of truth for claims: id, statement, grade, artifacts, notes.
  D0 reference: `CLAIM_TO_LEAN_MAP.csv` + `03_THEORY_MAP/theory_status_map.csv` (kept in sync).
  A project without a ledger creates one before its first claim.
- **Grades.** Total order, minimum set: `machine-checked > computed/cert-backed >
  narrated/assembled > candidate/DRAFT`. **Grade honesty invariant:** a claim's stated grade
  never exceeds its weakest load-bearing leg; mixed-grade results carry per-leg grading in the
  ledger note. D0 reference: LEAN_PROVED / CERT-CLOSED / operative / PROOF-TARGET / OPEN.
- **Owned.** Recorded in the ledger/corpus at a stated grade, citable file:line. The
  quantification domain of every claim must itself be owned or flagged AUTHORED (trap q).
- **No-go.** A first-class negative result: what cannot be derived, with the refuting
  mechanism named. Every no-go carries its own **reopening hook** — the exact condition under
  which it could be revisited.
- **Bridge / assumption.** A named external import with an owner file and a stated
  `failure_meaning`. Bridges are proof obligations, never positive closures.

## 2. The loop (per claim)

1. **Pre-flight.** Search ledger + corpus for the target's keywords. Existing content is
   cross-referenced, never re-derived (trap e). Stop-rules and prior kills covering the area
   are read IN FULL; entry only through their named doors.
2. **Compute first.** Every load-bearing quantity comes out of an exact, reproducible
   computation or mechanized proof from independently-built objects, BEFORE prose asserts it.
   Checks can fail the CONCLUSION (not merely the technique); no check builds its key quantity
   from the conclusion (trap f). The check ships as a runnable can-fail artifact.
3. **Memo.** Claim in explicit reductio/forcing form where applicable; owned pre-facts quoted
   VERBATIM with file:line, each swept ±10 lines for adverse continuations (trap l); named
   risks; a PRE-REGISTERED attack surface including the strongest attack the author can build
   against itself.
4. **Skeptic.** An independent agent (fresh context, zero investment) with a KILL mandate
   under the **kill rule**: a kill requires a *named second object* (explicit counterexample)
   or a *precise named gap* (specific missing step, cited). The skeptic verifies quotes
   verbatim and runs every artifact itself. This step is never skipped.
5. **Accept or repair.** Kills accepted IN FULL in a written verdict with errors of record
   enumerated — no defense. Wounded → ALL repairs applied, then one more pass on the
   load-bearing new text only.
6. **Mint.** Only after the pass, via the project's minting protocol, at the honest grade,
   with the per-leg grading in the ledger note.

## 3. The ratchet (why the candidate space narrows monotonically)

A kill never deletes information. It is recorded as (i) errors of record on the killed text,
(ii) the named refuting object, (iii) a reopening hook. Killed stays killed until the hook
fires. Two consequences observed in the reference campaign:

- **Kills compost into constructions.** The refuting object of one pass is often the surviving
  candidate of the next (the fork-carrier counterexample became the carrier guard; the
  subset-kill's surviving typing anchor became the antidiagonal embedding candidate).
- **Kills harden the engine itself.** Every kill class becomes a trap in the checklist
  (traps p and q entered from the 2026-07-18 session's two kills). The engine is antifragile
  in the literal sense: attacks that land increase its future kill rate.

## 4. Invariants (weakening any of these voids the engine's guarantee)

1. Skeptic independence (fresh context, kill mandate, runs artifacts itself).
2. No defense on kills; acceptance + repairs are the only permitted response.
3. Pre-registration of the attack surface before the skeptic sees the memo.
4. Can-fail certificates (mutation tests / negative controls that flip the verdict).
5. Grade honesty (weakest-leg rule).
6. Ledger-first (no claim exists outside the ledger).
7. Ratchet (kills recorded with EoR + reopening hooks; no silent un-kills).

## 5. Instantiation checklist for a new project

1. Create the ledger (id, statement, grade, artifacts, notes).
2. Fix the project invariant that reductio targets (D0: M1. A codebase: "no unverified
   behavior change". A spec: "no underived normative requirement").
3. Fix the grade ladder and the minting protocol.
4. Copy the loop templates (memo, skeptic brief, traps checklist) — the domain-general set
   ships as the `adversarial-forcing-loop` skill; extend the traps file with project-specific
   fired traps as they occur.
5. Run every new claim through §2. No exceptions for "obvious" claims — the reference
   campaign's author kill rate on plausible-looking claims was 6:0 before hardening.

## 6. Reference instantiation

The D0 theory (`this repository`) is the reference: ledgers under
`09_LEAN_FORMALIZATION/docs/` + `03_THEORY_MAP/`, campaign memos under
`_TASKS_CENTER_ATTACK/`, certificates under `05_CERTS/`, machine-checked layer under
`09_LEAN_FORMALIZATION/D0/` (Lean 4 / mathlib, full `lake build D0.All` green), guard scripts
under `tools/` (`check_cert_can_fail.py`, `check_book_ledger_sync.py`,
`check_no_dangling_lean_module.py`, `check_lean_builds.py`). The engine's own history —
including its accepted kills — is part of the record: see
`_TASKS_CENTER_ATTACK/CLOSE_GAP_E_LEAN_LIFT_MEMO.md` (13th pass) and
`F3_ANTIDIAGONAL_CANDIDATE_MEMO.md` (a kill accepted in full and composted into the surviving
candidate, same file).
