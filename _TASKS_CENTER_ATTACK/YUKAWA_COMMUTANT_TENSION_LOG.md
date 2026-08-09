# TENSION LOG — the Yukawa overlap scaffold is not adjacency-compatible (2026-08-01)

**Status: logged tension, no row edited, no kill claimed.** Discovered during the reviewer survey
for the 2026-08 front plan; recorded so it enters the next skeptic pass with provenance.

## The fact (computed, reproducible)

`D0.Matter.YukawaShellOverlapMatrix` carries the CERT-CLOSED overlap scaffold

    yukawaShellOverlap = !![0,1,0; 1,0,1; 0,1,0]   on shellSpace.d = 3.

`D0.Spectral.JointCommutant` (now wired in `D0/All.lean`) proves the joint commutant of
`{Aut, adjacency}` on the visible 3-space is exactly `ℚ[Q]`, `Q = !![0,11,13; 9,0,13; 9,11,0]`,
of dimension 3. Fitting `aI + bQ + cQ²` to the overlap's first row forces
`(a,b,c) = (−108/11, −1/2, 1/22)`, whose second row is `(9/11, 13/11, −13/11) ≠ (1,0,1)`.

**Hence `yukawaShellOverlap ∉ ℚ[Q]`: the scaffold does not commute with the scene's transport
operator (equivalently, is not an equivariant-and-adjacency-compatible operator on the
generation space).**

## The two admissible resolutions (owner decision)

1. **Scope qualification.** The overlap is not meant to live on the `K(9,11,13)` generation
   quotient as an equivariant object — then the row's "on the K(9,11,13) carrier" framing needs a
   qualifier, and the scaffold's carrier must be named as a different 3-space (e.g. the shell-torus
   side), severing the apparent link to the scene commutant.

2. **Replacement (the interesting branch — Campaign 3 item 4 of the front plan).** Replace the
   scaffold by an element of `ℚ[Q]`. Then its spectrum is forced: the eigenvalues are rational
   functions of the roots of `λ³ − 359λ − 2574`, and the charged-lepton hierarchy would be built
   from the transport spectrum with **no free matrix** — three predicted ratios, immediately
   falsifiable, trap-(f)-clean by construction. This branch is scheduled after the α-front steps.

## Cross-references

- `D0.Synthesis.EquivariantSeamNoGo` — the equivariant class is block-diagonal; any operator
  outside `ℚ[Q] ⊕ (3 archive scalars)` breaks the scene symmetry.
- `D0-LEPTON-YUKAWA-HIERARCHY-OWNER-001` (BOOK_04 04.10) — the consumer row whose Green-function
  leg is NOT touched by this log (Puiseux indices 1/4, 1/3 live on the 7-point shell torus, a
  different carrier; see the survey verdict).
