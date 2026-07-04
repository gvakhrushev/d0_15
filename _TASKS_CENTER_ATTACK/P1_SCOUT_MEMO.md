# P1 SCOUT — the Dixmier blocker reduces to one finite trace identity (VERIFIED MECHANISM)

**Status:** scout memo; mechanism machine-verified (`p1_normalized_residue_check.py`, 6/6 PASS,
exact, negative control live). No registry row edited. Targets: `D0-ALPHA-FESHBACH-DIXMIER-OWNER-001`,
`D0-DELTA-ALPHA-RESIDUE-PAIRING-OWNER-001`, `D0-DELTA-ALPHA-HEATTRACE-COEFFICIENT-OWNER-001`
(the C1-α global blockers).

## Diagnosis: why the blocker was unreachable as stated

The demand is "a regularized profinite trace whose s⁻¹ coefficient is 2¹¹π₀φ⁻² (= μ₂ = 12288/5,
**rational**)". But every bare golden-tower zeta residue carries the factor 1/(2 ln φ) —
**transcendental** (verified: Res ζ_vol = 1/(2 ln φ)). No bare tower residue can be rational.
This is the precise reason the log-Cesàro route closed negative
(`D0-ALPHA-PROFINITE-TOWER-NOGO-001`) and the owner was posted as external
(`ASSUMP-DIXMIER-TRACE`): the bare-residue semantics is structurally wrong, not merely unproven.

## The repair (verified mechanism): normalize by the tower's own volume

Define the tower zetas ζ_A(s) = Σₙ Tr(Aₙ)·φ^{−2ns} and ζ_vol(s) = Σₙ φ^{−2ns} over the same
2¹¹-Fock golden tower. Both have simple poles at s = 0; the **ratio of residues** —
a Dixmier-state ratio Tr_ω(A)/Tr_ω(𝟙), textbook NCG — cancels ln φ exactly:

```
Res ζ_A / Res ζ_vol  =  per-level Cesàro of Tr(Aₙ)   (rational when the block traces are)
```

Verified: with constant per-level trace μ₂ the ratio is **exactly 12288/5**; a level-growing trace
correctly fails (double pole, no finite ratio — negative control). The external ingredient shrinks
to the generic Dixmier-state formalism (standard, state-independent for convergent Cesàro data);
the transcendental obstruction disappears.

## The residual — one finite identity

The entire C1-α analytic blocker reduces to:

> **(F)** exhibit the owned finite operator A₁ on the 2¹¹-dimensional Fock/Clifford block over V₁₁
> (the candidate already NAMED and negative-controlled by `vp_cvft_clifford_fock_capacity.py`:
> 2¹¹ = dim Λ*(ℝ¹¹), not the spinor 32, not 2^9, not 2^13) with **Tr(A₁) = 12288/5**,
> level-uniformly (or Cesàro) along the tower — i.e. per-Fock-mode average exactly
> **π₀φ⁻² = 6/5**.

(F) is finite arithmetic — cert-able the day the operator is written down. The per-mode value 6/5
is the discrete angle π₀ in φ⁻²-units, suggesting A₁ is a π₀-holonomy/angle readout averaged over
Fock modes; that identification is the remaining research content, and it is a FINITE question.

## Honest risks

1. **Semantics re-scope:** if the corpus's Δα normalization demands the *bare* residue semantics,
   the ratio restatement is a re-scope of the blocker's wording and needs owner sign-off — but the
   diagnosis above shows bare semantics is unsatisfiable, so the choice is ratio-semantics or
   permanent external assumption; there is no third option.
2. **(F) may be false** — no operator with per-level trace 12288/5 may exist among owned objects;
   then the route dies honestly (and the blocker stays external). Testable per candidate.
3. Scaling choice φ^{−2n} (vs φ^{−n}) affects nothing: the ratio mechanism is scaling-invariant
   (both residues scale together) — only level-constancy of Tr(Aₙ) matters.

## Recommended next

Search the owned operator inventory over V₁₁/Fock for trace 12288/5 candidates (the Feshbach
residue amplitude chain of §02.13.4 is the natural home — μ₂ is literally its second moment);
write (F) as a finite cert obligation; then draft the blocker re-scope (bare → ratio semantics)
for owner review. If (F) lands, P1's three global blockers collapse to one PASSING cert plus a
textbook-external Dixmier-state citation.
