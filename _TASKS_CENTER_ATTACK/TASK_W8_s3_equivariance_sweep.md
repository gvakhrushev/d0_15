# TASK W8 — S₃-equivariance sweep + the "simultaneously" dig (gates T2′ closing memo)

**Goal:** two charges that together decide whether the T2′ reduction (`T2_PRIME_CLOSING_MEMO.md`)
survives: (A) verify premise Π — no owned invariant distinguishes the three scene generation labels
except through branch data; (B) determine whether the (1,4,3) coincidence between Q₈ Fourier ranks
and return orders is one operator or just one integer pattern.

**Repo:** `/Users/grigorijvahrusev/Downloads/d0_15/`
Read first: `_TASKS_CENTER_ATTACK/T2_PRIME_CLOSING_MEMO.md`, `TASK_W6_REPORT.md` §(c)–(e),
`TASK_W3_REPORT.md` §(d). Deliverables only into `_TASKS_CENTER_ATTACK/`; no status/claim edits;
report negative findings with the same care as positive.

## Charge A — the Π sweep (S₃-equivariance of generation labels)

Premise Π: every owned (Lean/cert/no-go) claim that mentions generations is equivariant under S₃
relabeling of the three scene generations; only branch data (exponents 0, 1/4, 1/3; ranks 1,4,3) and
external EFT/IR passports (mass decimals, PDG names) break the symmetry — and those are exactly the
objects the bijection is *about*, so they do not count against Π.

1. **Inventory:** grep the Lean tree and cert registry for generation-tagged rows. Starting set (extend
   it): `D0/Matter/PhasonStrainGenerations.lean`, `D0/Representation/FinitePathRepresentation.lean`,
   `D0/Representation/TypedRepresentationFunctor.lean`, everything CKM (`BOOK_04 §04.10` owners, the
   basis-origin selectors), the Lucas-resonance rows (`L_11+L_4 = 206` muon), the PMNS/JUNO passport
   rows, anything importing `numGenerations`/`Gen`/`generation` in Lean, and
   `04_VERIFICATION/CLAIM_TO_LEAN_MAP.csv` rows whose claim text mentions generation/flavor.
2. **Per row, classify:** EQUIVARIANT (statement invariant under relabeling generations),
   BRANCH-KEYED (breaks S₃ only via the branch exponents/ranks — allowed by Π's carve-out),
   PASSPORT (external naming/decimals — allowed), or **Π-VIOLATOR** (an owned internal invariant that
   distinguishes generation labels through something OTHER than branch data). The Π-VIOLATOR class is
   the whole point of the sweep: finding even one kills the reduction at a named row.
   Watch specifically: does any CKM/mixing owner key generation ORDER to zone sizes (9,11,13), Lucas
   indices, or torus data in a way that is owned (not passport)? W6 noted a *typed* scene ordering
   (`TypedRepresentationFunctor.lean:73`) whose canonicity is unestablished — classify what depends
   on it and whether anything owned KEYS to it.
3. **Verdict:** Π HOLDS (with the classified table as evidence) / Π FAILS at rows R₁…Rₙ (quoted).

## Charge B — the "simultaneously" dig

`UnifiedTheorem.lean:31–36` asserts the branch orders (1,4,3) appear simultaneously in the Q₈ Fourier
ranks and the return orders.

1. Read the actual Lean proof term / definitions behind that statement. Determine: is there ONE
   operator (or one owned construction) from which BOTH the isotype ranks and the return orders are
   computed — or are two independently-defined objects compared by their integer outputs (`decide`
   on lists)?
2. Trace the return orders to their source (which operator's cycle structure? the shell-torus σ? the
   Feshbach return spectrum?), and the Fourier ranks to theirs (Wedderburn decomposition of ℂ[Q₈]).
   Name the exact point where the two chains touch (shared definition) or fail to touch (mere equality
   of `[1,4,3] = [1,4,3]`).
3. If they fail to touch: state precisely what object WOULD have to exist to carry both (this becomes
   the sharpened P_iso target). If they touch: quote the shared definition — that is the candidate
   internal owner of P_iso.

## Deliverable

`TASK_W8_REPORT.md`: (A) the classified inventory table with file:line per row + Π verdict;
(B) the dig chain with verbatim Lean quotes + touch/no-touch verdict + the sharpened P_iso statement;
end with a skeptic's paragraph: the strongest surviving reason the T2′ reduction is wrong even if
Π holds (e.g. the carve-out "branch-keyed breaks are allowed" hiding a circularity).

## Acceptance criteria

- Every classification carries file:line; EQUIVARIANT calls justified by the statement's shape, not
  by absence of evidence ("didn't find" ≠ "invariant" — say which).
- Charge B quotes actual proof terms, not docstrings.
- No edits outside `_TASKS_CENTER_ATTACK/`; no promotion language.
