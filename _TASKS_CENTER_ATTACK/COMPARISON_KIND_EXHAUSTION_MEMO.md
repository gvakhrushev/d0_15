# COMPARISON_KIND_EXHAUSTION — a conclusion-free exhaustivity map, and a transport no-go candidate (DRAFT, pre-skeptic)

**Status:** DRAFT candidate. **No registry row edited.** No status word promoted.
Targets: `D0-P-DEGREE2-EXHAUSTION-001`, `D0-TOWER-STOP-NOEXT-001` (both downgraded to OPEN /
PROOF-TARGET on 2026-07-29), and by inheritance `D0-GAP-E-PORT-EXHAUSTION-001`.
Cert: `_TASKS_CENTER_ATTACK/comparison_kind_exhaustion_check.py` — 10/10 PASS, exit 0.

## The obligation, verbatim (theory_status_map.csv, D0-P-DEGREE2-EXHAUSTION-001)

> "The finite inductive ComparisonKind in DetectionQuadratic has cardinality two because it is
> declared with two constructors; it is not yet proved exhaustive for arbitrary admissible
> detection. This umbrella remains a proof target until a conclusion-free semantic classification
> theorem supplies the missing exhaustivity map."

And in `D0-TOWER-STOP-NOEXT-001`:

> "Restoring the three-zone upper bound requires a new semantic classification theorem mapping
> every admissible necessity-type injectively into three owned slots; neither the old certificates
> nor `no_extension_theorem` provide it."

The withdrawn route derived the cap from degree-2 algebra. **Nothing in this cert touches φ, p, or
any algebra** — the word "conclusion-free" is taken literally and enforced by construction.

## The source semantics (09_LEAN_FORMALIZATION/D0/Tower/DetectionQuadratic.lean:26-29, verbatim)

> ```lean
> inductive ComparisonKind
>   | membership   -- levels 1↔2: different categories ⇒ linear (degree 1)
>   | value        -- levels 2↔3: one category ⇒ bilinear=area (degree 2)
> ```

The distinguishing datum the comments give is **not** a degree. It is whether the two compared
items lie in **different categories** (`membership`) or **one category** (`value`).

## Claim T (DEF-0.2.2 form)

Let a *categorized universe* be a finite set `X` with a partition into categories, and a
*comparison* an ordered pair of **distinct** elements. Define the kind map
`κ(u,v) = [cat(u) = cat(v)]`.

> **T.1** `κ` takes at most 2 values, by construction, for every categorized universe and every
> admissible detection — no algebra, no φ. This is the missing exhaustivity map in its literal form.
>
> **T.2 (completeness, the substantive clause).** `κ` is the **complete** invariant of a comparison
> — i.e. the orbits of the structure group on ordered distinct pairs are exactly the two fibres of
> `κ` — **iff the categories are mutually interchangeable** (all of equal size, ≥ 2 categories, at
> least one of size ≥ 2). Verified by exhaustive orbit computation on (2,2), (3,3), (2,2,2),
> (3,3,3), (2,2,2,2), (4,4): 2 kinds in every case, and the two orbits are precisely
> {same-category, different-category}.
>
> **T.3 (the transport sting).** When category sizes are **pairwise distinct**, the categories
> become distinguishable and the complete invariant refines. Closed form, verified against brute
> force on (1,2), (2,3), (1,2,3), (2,3,4): `#kinds = #{categories of size ≥ 2} + k(k−1)`. For
> **K(9,11,13)** this gives **9**, not 2.

## Verification

`comparison_kind_exhaustion_check.py` — 10/10 PASS. Structure groups are built by **brute force**
over all permutations (no generator recipe assumed). Controls, each firing:

- **NC1** category swaps forbidden (labelled categories) ⇒ equal sizes give **9** kinds, not 2. So
  T.2 genuinely consumes interchangeability; it is not a tautology of the pair space.
- **NC2** including the diagonal changes the count (3 ≠ 2) — the "distinct items" clause is
  load-bearing.
- **NC3** hand-checkable (2,2): orbit sizes [4, 8].
- **T2 boundary**: degenerate shapes (1,1), (3,), (2,) give 1 kind — T.2's hypotheses are not
  decorative.

Two hand-derived expectations were **wrong and were caught by their own assertions**: the closed
form initially omitted that a singleton category contributes no internal pair (failed at (1,2,3)),
and NC3 was first predicted [2,8] instead of [4,8] (counted one category, not both). Both are
recorded in the cert comments. The computed numbers never moved.

## PRE-REGISTERED attack surface

**(A) THE STRONGEST ATTACK — the one most likely to kill this. The source says "levels 1↔2" and
"levels 2↔3": levels are NUMBERED, hence labelled, hence NOT interchangeable.** If the detection
floor's categories are labelled, T.2's hypothesis fails at the floor itself, and NC1 shows the
count is then 9, not 2 — which would refute the "two comparison kinds" reading at its own level,
not merely at the zone level. My defence is that `κ`'s two values are stated in the comments as
*category-relational* ("different categories" / "one category"), not as level indices, so the
label structure is not what the kind tracks. I do not regard this defence as secure and I am
pre-registering it as the likely kill site. **A skeptic should go here first.**

**(B)** T.1 may be vacuous: if "kind" is *defined* as `κ`, then "at most 2 kinds" is a restatement
of "a boolean has two values", and the obligation asked for something with content. The content, if
any, is entirely in T.2's completeness clause — press on whether T.1 alone discharges anything.

**(C)** Trap (f): does any check build its quantity from the conclusion? Structure groups are brute
-forced; orbit counts are union-find; the closed form is checked **against** brute force on four
shapes, not substituted. But K(9,11,13) itself is **not** brute-forced (33! is impossible) — its 9
is the closed form extrapolated. Press on whether the extrapolation is licensed.

**(D)** T.3's consequence for `D0-GAP-E-PORT-EXHAUSTION-001` is **asserted, not audited**: that row
states its port-count=2 is "owned-AS-CAP twice over", including an independent `:860` falsification
hook. If that second owner is genuinely independent of the comparison-kind count, T.3 does not
touch it. **This memo does not claim GAP-E is broken** — the audit is outstanding.

**(E)** The identification "comparison kind ↔ port" is the corpus's forcing-READING, not a theorem.
T.3 speaks about kinds; transporting the sting to *ports* needs that reading, which is exactly the
parent-grade step `D0-GAP-E-PORT-EXHAUSTION-001` already flags as a reading.

## What this does NOT show

- **Not a mint.** No registry row edited; no Lean module written; no status changed.
- Does **not** restore the three-zone upper bound of `D0-TOWER-STOP-NOEXT-001`. T addresses
  *comparison kinds*; the necessity-type→three-slots map is a different obligation and remains open.
- Does **not** establish that any downstream claim is wrong — see (D), the audit is not done.
- Does not touch `p³ = 2p − 1`, which remains true and remains insufficient for exhaustion.
