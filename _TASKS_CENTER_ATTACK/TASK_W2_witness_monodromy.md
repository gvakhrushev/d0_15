# TASK W2 — 8-point witness monodromy: construction and invariant re-run

**Goal:** construct the witness-extended monodromy σ̂ on 8 points and re-run every invariant used by
the lepton no-go chain, to test whether the T2 resolution is internally consistent. This task is
purely computational/constructive — it does NOT decide whether the extension is *forced* (that is
TASK W3 + the architect's forcing memo). Best run after W3, but independent enough to start now.

**Repo:** `/Users/grigorijvahrusev/Downloads/d0_15/`

## Context (self-contained)

Frozen no-go data (`09_LEAN_FORMALIZATION/D0/Extensions/LeptonBranchFixingNoGo.lean` and
`D0/Matter/LeptonBranchAssignmentNoGo.lean`): σ_A = (0 1 2 3)(4 5 6) on Fin 7, cycle type (4,3),
order 12, det(I−zU) = (1−z⁴)(1−z³), (4,3) is the unique order-12 cycle type among partitions of 7;
2 orbits ↦ exponents {1/4, 1/3}; no fixed point ⇒ no exponent-0 branch. The rival assignment
σ_B = (0 1 2)(3 4 5 6) shares all resolvent invariants (this freedom is the R4 no-go).

T2 proposes: extend by the witness ω₀ (core rule Ω₈+ω₀=V₉, BOOK_00 §00.5): σ̂ = σ_A ⊕ id on 8
points, cycle type (4,3,1), orbits {1,4,3}, exponents {0,1/4,1/3}, electron = witness branch.

## Steps

1. **Uniqueness of the cycle type:** enumerate all partitions of 8 and their lcm; verify whether
   (4,3,1) is the UNIQUE cycle type of order 12 in S₈ (the architect's hand check says yes — the only
   other lcm-12 candidates would need parts {4,3} plus 1s; confirm exhaustively). If unique, the
   resolvent-invariant argument of the 7-point no-go carries over verbatim to 8 points. Deliver the
   enumeration as a small exact script.
2. **Resolvent invariants:** compute det(I−z·Û) = (1−z)(1−z³)(1−z⁴) for the 8-point permutation
   matrix; list fixed points, orbit sizes, order (verify order exactly 12: powers 4 and 6 ≠ id).
3. **Assignment freedom on 8 points:** classify all order-12 permutations of cycle type (4,3,1) in
   S₈ up to relabeling. Verify: the three orbits are pairwise distinguishable by SIZE alone (1≠3≠4),
   so the orbit-keyed exponent map {size 1 ↦ 0, size 4 ↦ 1/4, size 3 ↦ 1/3} is label-free. State
   exactly what residual freedom remains (which underlying points carry which cycle = pure relabeling;
   which physical name μ/τ attaches to 1/4 vs 1/3 = external naming, passport level). Compare with
   the σ_A/σ_B freedom on 7 points: does the witness kill it, reduce it, or leave it unchanged?
4. **Green-resolvent machinery re-run:** locate the cert for `D0-LEPTON-FINITE-GREEN-RESOLVENT-OWNER-001`
   (grep `05_CERTS/` for `green` / `resolvent` / `lepton`). Understand its input format; run the same
   computation on the 8-point carrier. Question to answer: does the machinery produce a well-defined
   exponent-0 (regular/unramified) branch at the fixed point, alongside 1/4 and 1/3? Report whatever
   happens, including failure to adapt the cert.
5. **Draft Lean skeleton** `LeptonWitnessBranchConstruction.lean` (place in this task folder, NOT in
   `09_LEAN_FORMALIZATION/`): mirror the style of `LeptonBranchFixingNoGo.lean` — define
   `sigmaHat : Fin 8 → Fin 8`, prove by `decide`: exactly one fixed point; orbit count 3; sizes
   {1,3,4}; order 12; and `Branch(3) ≃ Gen(3)` exists (an explicit bijection). Do NOT reference or
   modify the existing no-go; this is a construction over a DIFFERENT carrier, and the no-go remains
   true for 7 points.
6. Write `TASK_W2_REPORT.md` with results of 1–5 and an honest list of what this does NOT show
   (in particular: nothing here proves the 8-point carrier is forced).

## Acceptance criteria

- All computations exact (integers/rationals); scripts included and deterministic.
- The Lean skeleton compiles standalone against Mathlib (`decide`-level proofs only) or, if the
  environment lacks Lean, is delivered with a line-by-line justification of each `decide` claim.
- The report separates VERIFIED (computed) from OPEN (forcing question) explicitly.
- No edits outside `_TASKS_CENTER_ATTACK/`.
