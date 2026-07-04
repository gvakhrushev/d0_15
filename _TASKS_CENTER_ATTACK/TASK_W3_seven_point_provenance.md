# TASK W3 — Adversarial provenance audit of the 7-point shell-torus carrier

**Goal:** determine, with citations, where the 7-point carrier `Ueff = blockdiag(4-cycle, 3-cycle)`
comes from, and what the exact forcing scope of the witness/addressability rule (Ω₈+ω₀=V₉) is.
This audit GATES candidate theorem T2 — run it with the intent to REFUTE T2, not to confirm it.

**Repo:** `/Users/grigorijvahrusev/Downloads/d0_15/`

## Context (self-contained)

The lepton no-go chain (`09_LEAN_FORMALIZATION/D0/Extensions/LeptonBranchFixingNoGo.lean`,
`D0/Matter/LeptonBranchAssignmentNoGo.lean`, `D0/Extensions/LeptonSelectorExtension.lean`) proves:
the frozen shell-torus monodromy σ = (0 1 2 3)(4 5 6) on Fin 7 has 2 orbits (exponents 1/4, 1/3),
no fixed point, and 2 < 3 generations — so the third (electron, exponent-0) branch was posted as an
external postulate (`D0-X5-LEPTON-CONTRACT-001`).

T2 attacks the premise: in the core, addressability forces a witness/basepoint at the scene level
(BOOK_00 §00.5: `Ω₈ + ω₀ = V₉`). If the same rule applies to any terminal readout/branch register,
the frozen carrier should be 7+1 = 8 points with σ̂ fixing ω₀ — giving orbits {1,4,3} and exponents
{0, 1/4, 1/3}, i.e. three internal branches. T2 is only legitimate if (a) the 7-point carrier was not
itself already produced by removing a basepoint, and (b) the witness rule's forcing scope plausibly
covers branch registers.

## Steps

1. **Provenance of 7:** find every derivation of the shell-torus and its monodromy. Start points:
   grep for `shell-torus`, `blockdiag`, `4-cycle`, `sigmaA`, `Ueff` across `01_BOOKS/BOOK_04*`,
   `09_LEAN_FORMALIZATION/D0/Matter/`, `09_LEAN_FORMALIZATION/D0/Extensions/`, `05_CERTS/` (the
   Green-resolvent cert for `D0-LEPTON-FINITE-GREEN-RESOLVENT-OWNER-001`). Answer with quotes:
   why 7 points? why cycle lengths 4 and 3? Is 7 = 4+3 primitive, or a quotient/restriction of a
   larger carrier (8, 9, 12, ...)? If any step removed a basepoint/witness, T2 is likely already
   answered — report exactly where.
2. **Forcing scope of the witness rule:** collect every invocation of the witness/basepoint ω₀ in the
   corpus (grep `witness`, `basepoint`, `omega_0`, `ω₀`, `addressab` across `01_BOOKS/` and Lean).
   For each: is the rule stated as (i) scene-alphabet-specific (only Ω₈→V₉), or (ii) a general law
   "any addressable readout carrier requires a witness"? Quote the strongest general statement and
   the narrowest one. Check especially BOOK_00 §00.5, BOOK_01 §01.7–01.8 area, and any Lean file
   with `witness` in its name.
3. **Prior art check:** search the corpus (including `_QUARANTINE/`, `04_VERIFICATION/*.csv`,
   `03_THEORY_MAP/`) for any earlier attempt to add a fixed point / trivial orbit / unramified branch
   to the lepton carrier, and any recorded rejection of it. If it was tried and killed, quote why.
4. Write `TASK_W3_REPORT.md`: (a) provenance chain of the 7-point carrier; (b) witness-rule scope
   verdict — one of: GENERAL-LAW / SCENE-ONLY / AMBIGUOUS, with quotes; (c) prior-art verdict;
   (d) your adversarial conclusion: which exact step of T2 fails, if any.

## Acceptance criteria

- Every claim in the report carries a file path + section/line citation.
- The report takes the skeptic's side: it must state the single weakest step of T2 explicitly.
- No edits to any repo file outside `_TASKS_CENTER_ATTACK/`.
