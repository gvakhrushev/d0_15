# TASK W4 — Sturmian↔archive intertwiner over the composite field ℚ(√2,√5)

**Goal:** re-open the field-disjointness NO-GO over the biquadratic composite K = ℚ(√2,√5) and either
construct the canonical intertwiner or name the exact next obstruction. Also audit whether √2 has an
independent D0-native owner.

**Repo:** `/Users/grigorijvahrusev/Downloads/d0_15/`

## Context (self-contained)

Two independent core objects live in incompatible quadratic fields:
- the golden/time layer lives in ℚ(φ) = ℚ(√5);
- the archive-window scales λ_{c,r} = 3/2 ∓ √10/40 (roots of 160λ²−480λ+359, the normalized-Laplacian
  active pair of K(9,11,13)) live in ℚ(√10); the Iter25 result owns the discriminant
  (λ_r−λ_c)² = 3/((m+1)(m+3)) at zones {m,m+2,m+4}, m=9.

The recorded NO-GO `D0-STURMIAN-REFINEMENT-DISCHARGE-NOGO-001` (find it in BOOK_06 §06.6.B / BOOK_05
§05.9 and the Lean tree — grep `Sturmian`, `sqrt10`, `disjoint`) rests on: ℚ(√5) and ℚ(√10) are
disjoint over ℚ, no canonical intertwiner. T3 observes: √10/√5 = √2, so the composite is the
biquadratic K = ℚ(√2,√5), Galois group V₄, with exactly three quadratic subfields ℚ(√5), ℚ(√10),
ℚ(√2). Both generators are invariants of forced objects (φ from p+p²=1; √10 from the discriminant of
the forced scene's window polynomial), so K is a candidate catalog-free closure field.

## Steps

1. **Read the primary sources:** the exact statement of the Sturmian/archive no-go (which objects,
   which maps, what "intertwiner" means there — operator conjugation? measure-isomorphism? trace
   identity?). Also `09_LEAN_FORMALIZATION/D0/VNext2/WindowScaleDiscriminant.lean`,
   `D0/Geometry/SceneActiveEigenvalues.lean`, `D0/Spectral/ZoneMatrixSpectrum.lean`. Write down the
   precise mathematical question the no-go closed, with quotes.
2. **Re-pose over K:** restate the same question over K = ℚ(√2,√5). The disjointness reason is void
   in K (both fields embed). Determine what the intertwiner must actually be: identify the two
   towers/operators to be intertwined (golden substitution tower vs archive window flow) and attempt
   the construction with exact matrices over K (represent K as ℚ⁴ with basis {1,√2,√5,√10}).
   If an obstruction remains, it is no longer field-disjointness — name it precisely (dimension
   mismatch? non-conjugate spectra? no equivariant map?). Either outcome is a full deliverable.
3. **√2 ownership audit:** search the corpus for any existing D0-native occurrence of √2 / silver
   ratio / ℤ[√2] (grep `sqrt2`, `\sqrt{2}`, `silver`). Candidate owner to evaluate: the Darboux
   "+2 conjugate symplectic pair" step (BOOK_00 §00.5 area, BOOK_01) — zones step 9→11→13 by +2;
   does any frozen object have √2 in its spectrum or normalization? Report findings; if nothing,
   say so plainly (then ℚ(√2) is merely the third subfield forced by the composite, with no
   independent role — an honest weaker version of T3).
4. **Galois structure check:** verify V₄ action explicitly: the three nontrivial involutions fix
   respectively ℚ(√5), ℚ(√10), ℚ(√2). Check how the corpus's Galois-forced facts extend: the sign
   forcing σ(φ⁻¹) = −φ (used in `D0-PHASON-WDE-SIGN-NORMALIZATION-OWNER-001`) is an element of
   Gal(K/ℚ) restricted to ℚ(√5) — which extension(s) to K are compatible, and does the choice
   matter for any owned invariant? If a choice matters and nothing forces it, record it as the
   candidate obstruction.
5. Write `TASK_W4_REPORT.md`: (a) the exact no-go statement; (b) construction over K or the named
   next obstruction; (c) √2 ownership verdict; (d) Galois compatibility result; (e) an honest
   assessment: does T3 upgrade the no-go to a theorem-over-K, or merely relocate it?

## Acceptance criteria

- All algebra exact over ℚ-bases (no floats in any decision).
- The report distinguishes: PROVED-HERE / CITED-FROM-CORPUS / OPEN.
- If the intertwiner is constructed, deliver the explicit matrices and the verification script.
- No edits outside `_TASKS_CENTER_ATTACK/`.
