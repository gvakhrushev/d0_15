# P1 (F)-RESOLUTION — the 2¹¹ is a dimension, not an amplitude (VERIFIED DRAFT)

**Status:** candidate resolution of the finite identity (F) from `P1_SCOUT_MEMO.md`; mechanism
machine-verified (`p1_fock_center_check.py`, 4/4 PASS). Together with the ratio-Dixmier mechanism
this makes the whole C1-α blocker triple candidate-closed. No registry row edited.

## Provenance facts (from the corpus's own cert, `vp_feshbach_residue_amplitudes.py`)

- μ₁ = 1/3 is DERIVED ("Tr(floor)/rank-normalised = 1/rank, no 2¹¹ needed").
- π₀ = (6/5)φ² is DERIVED ("δ₀ balance"), owned.
- μ₂ = 2¹¹π₀φ⁻² is an ASSEMBLED FORM: "the FORM holds; **the 2¹¹ is not derived**" — the corpus's
  own named gap, re-narrowed by `vp_cvft_clifford_fock_capacity.py` to "why does the residue trace
  over the full Cl(V₁₁) = 2¹¹ Fock block".

## The resolution

**The 2¹¹ never was an amplitude to derive — it is the trace of the identity on the owned block.**

1. **Block (owned, already negative-controlled):** Λ*(ℝ¹¹) = Cl(V₁₁), dim 2¹¹ — the full
   exterior/Clifford/Fock space over the 11 zone modes (not spinor 32, not 2⁹, not 2¹³; CVFT cert).
2. **Weight forced center-valued (the new forcing, DEF-0.2.2 shape, pre-skeptic):** the residue
   pairing weight on the block must commute with the owned Cl(V₁₁) structure — a non-equivariant
   weight distinguishes Clifford generators, i.e. imports a preferred frame on the zone modes,
   breaking the owned S₁₁-exchangeability (§01.20 C1) with an underivable, outcome-affecting frame
   catalog: exogenous, ⊥M1. The commutant-center of Cl(11) (odd n) is span{1, ω},
   ω = e₁⋯e₁₁ (external owner: standard Clifford structure theory). So weight = a·𝟙 + b·ω.
3. **The trace sees only the scalar part (verified):** left multiplication by ω sends blade e_I to
   ±e_{comp(I)}; a fixed point needs |I| = 11 − |I| — impossible for odd 11 (parity argument,
   checked, with the n = 10 negative control showing the argument does real work). Hence
   Tr(ω) = 0 and **Tr(a·𝟙 + b·ω) = a·2¹¹** — the b-ambiguity is invisible to the residue.
4. **The scalar is the owned angle density:** a = π₀φ⁻² = 6/5 (π₀ derived from δ₀ balance — owned;
   φ⁻² the internal step weight — owned). Then Tr = 2¹¹·(6/5) = **12288/5 = μ₂ exactly**.

## The assembled P1 chain (all pieces now named)

```
finite level:  Tr_{Cl(V11)}(weight) = 2¹¹·π₀φ⁻² = μ₂        (this memo: center-forcing + parity)
tower level:   Res ζ_A / Res ζ_vol = per-level Cesàro = μ₂   (P1_SCOUT_MEMO: ln φ cancels)
semantics:     bare-residue demand unsatisfiable (transcendence) ⇒ ratio-semantics re-scope
external:      Dixmier-state formalism (textbook) + Clifford center structure (textbook)
```

The three global blockers `D0-ALPHA-FESHBACH-DIXMIER-OWNER-001`,
`D0-DELTA-ALPHA-RESIDUE-PAIRING-OWNER-001`, `D0-DELTA-ALPHA-HEATTRACE-COEFFICIENT-OWNER-001`
reduce to: one center-forcing paragraph (step 2 — the only new forcing text), two textbook-external
citations, one semantics re-scope for owner sign-off, and arithmetic that is already owned or
verified here.

## Named risks (for the skeptic)

1. **Step 2 is the load-bearing new text** — the Cl-equivariance premise ("non-equivariant weight =
   frame catalog") must survive the same scrutiny that killed three earlier forcings. Sharpest known
   attack: S₁₁-equivariance alone forces only degree-wise scalars (12 parameters w₀..w₁₁, one per
   Λᵏ), not center-valuedness; the strengthening to full Cl-equivariance needs the frame-catalog
   argument to bite specifically. If only S₁₁ survives, Tr = Σₖ C(11,k)wₖ and (F) needs the wₖ
   profile — the resolution weakens to a named 12-parameter question.
2. The ratio-semantics re-scope changes the blocker's wording; owner sign-off required (no third
   option exists — the transcendence diagnosis stands regardless).
3. π₀'s own derivation ("δ₀ balance") is cited as owned per the cert's PASS line; its chain was not
   re-audited here.
