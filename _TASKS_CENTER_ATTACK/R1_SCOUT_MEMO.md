# R1 SCOUT — un-conditionalizing the unified chain: exact inventory and the decisive experiment

**Author:** chief researcher. Status: scout memo (per `VERIFIED_CLOSURE_PROTOCOL.md`, a grounded
scout precedes any owner work); no registry row edited. Sources: `05_CERTS/verify_unified_backbone.py`,
`05_CERTS/verify_unified_feedback.py`, `UnifiedTheorem.lean:12–16`. Experiments:
`r1_swap_experiment.py`, `r1_exact_spectra.py` (this folder).

## The three declared choices, inventoried from the certs

**1. The holonomy λ.** Enters as the corner of the return cycles: `C₄⁴ = λI`, `C₃³ = λI`
(backbone §6); at λ=1 these are the bare Umu/Utau of `TerminalReturn.lean`. Findings:
- All claimed identities are **λ-uniform** (backbone: symbolic in λ; feedback: generic |λ|=1 point).
  The conditionality is exactly: which λ is physical.
- `|λ| = 1` is owned (unitarity of U_br, cert-checked).
- The **phase of λ is gauge-invariant**: rescaling z shifts the two cycle phases by (4α, 3α);
  with a common λ = e^{iθ} the invariant 3θ₄ − 4θ₃ = −θ survives. So the phase is physical —
  it must be forced or postulated. Named candidate values: λ = 1 (the bare slice; "trivial" itself
  needs a reason) and the golden phase (the corpus's own phase generator, §01.22/§06.29 φ⁻²-rotation;
  note W_int = φ⁻² is the owned holonomy cost — weight vs phase reading to be adjudicated).
- **Single λ for both cycles** is a choice in the certs; candidate forcing: the single-section
  discipline (a second independent holonomy = a second anchor, banned by §03.16.B). Writable.

**2. The balanced two-port R_\* = (1/√2)[[I,−I],[I,I]].** The feedback law `F_term = ½P_br` holds
for this port; the cert's negative control only kills the **non-unitary** unbalanced version.
**Named gap:** the unitary θ-family R_θ = [[cosθ,−sinθ],[sinθ,cosθ]]⊗I is untested; F_term would
scale with sin²θ, so the balance is equivalent to the ½ in the feedback law. Candidate owner for
the ½: the corpus's factor-2 forcings (§02.5.2, three independent contradictions). Writable; the
θ-family control should be added to the cert either way.

**3. The line-graph contact — the decisive finding.** The contact construction is itself the
matching m at operator level: the μ-carrier (4 c-modes over the ⟨i⟩-orbit, ± NOT collapsed) is
built on edges V₉→**V₁₁**, and the τ-carrier (3 modes r_B, r_C, r_D — ±-symmetrized Z-coset
functions over the axes) on edges V₉→**V₁₃**. The swapped contact (c→13, d→11) is exactly m′.

**Experiment 1 (`r1_swap_experiment.py`):** the swapped contact PASSES all embedding-dependent
cert checks — Gram = I₈ and rank K = 7 both hold, both spectra contain the triple eigenvalue
143 = 11·13. **The cert's own identities do not force the contact.** The edge-cover-family
conditionality is confirmed as (at least) two-member.

**Experiment 2 (`r1_exact_spectra.py`, exact):** the two contacts are **spectrally distinguishable**:

```
K†K charpoly, original: (x−143)³ · (12x⁴ − 5243x³ + 473325x² − 8759036x + 23393656)/12
K†K charpoly, swapped:  (x−143)³ · (12x⁴ − 5293x³ + 481675x² − 8873436x + 23393656)/12
```

Equal determinant (equal constant term and equal 143³ factor), different traces; all three
coefficient differences are divisible by 50 (recorded as exact structure, **no interpretation
claimed** — anti-numerology flag; any owned-invariant identification must be pre-registered with
E-accounting before comparison, never read off these numbers post hoc).

## Consequence — the R1 core, sharply

Because the two contacts have different owned-computable spectra, the contact choice **affects
distinguishable outcomes**. By the corpus's own dichotomy blade (§00.9 branch A) it is contentful
and must be derived — it is not a naming convention. But: the cert identities are uniform across
the family (Experiment 1), and the extension-based forcing route is closed by the mirror
impossibility (`T2_PRIME_FINAL_STATE.md`: E₄ is extension-invisible). So the third-generation
residual has converged from three directions (assignment bit, licensing rule, contact choice) to
**one physical binary choice, now exhibited as a pair of spectrally distinct operators.**

Live routes to close it, in order of promise:
1. **λ-route:** if λ is forced ≠ 1 (golden phase candidate), the dressed z⁴/z³ structure becomes
   physical and may discriminate the contacts through an owned window (e.g. the §01.22 forced
   return moduli q_T = 44); this couples choices 1 and 3 — one forcing could close both.
2. **Pre-registered spectral discriminator:** freeze a grammar of admissible invariants FIRST
   (per §00.9 E-accounting), then test which contact's exact charpoly satisfies it. The equal-det/
   Δ≡0 mod 50 structure above is the data such a test would confront.
3. **Accept as the minimal postulate:** one bit, with all owned-material evidence (return-order
   key, downstream consumption, the certs' own construction) selecting m — the honest X5 form if
   routes 1–2 fail.

## Scout verdict

R1 is real, minimal, and well-posed: two writable sub-forcings (single-λ, balanced-port ½) that
shrink the family, one untested cert control (θ-port), and one irreducible binary core (the
contact) with three named closure routes. Recommended next: write the single-λ and ½-port
forcings (cheap), add the θ-family negative control to a task-folder cert, then attack the
λ-phase question — it is the only route that can force rather than select.
