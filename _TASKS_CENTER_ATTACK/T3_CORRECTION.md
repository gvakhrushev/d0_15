# T3 CORRECTION — self-caught before review: the golden datum is the scale, not a summand

**Author:** chief researcher, correcting own `T3_FINAL_STATE.md` after a §05.8.U-style self-audit
(registry grep + primary-source re-read) performed BEFORE spending a skeptic pass. Two errors of
record, one implementation bug; the dissolution thesis survives in corrected — and cleaner — form.

## Error 1 (substantive): "golden factor = G_space" is wrong

§06.30a verbatim: "the generator is the direct sum of the **spatial** and scene generators" —
G_space is the spatial transport generator, not a time layer. The toral pair {φ⁻¹, −φ} is
tick/Floquet data, not the spectrum of a ⊕-summand of G_fib. **Corrected placement:** the golden
datum enters the owned hull flow as the **forced scale** — u = ε²t with ε² = φ⁻¹⁶, whose
normalization is owned FORCED (§06.30a: any k·ε or m·ε² smuggles an external coefficient, ⊥M1) —
and as the tick weight φ⁻¹ per circulation (Block III). The archive window remains the G_scene
active pair. The two data enter **different slots of one owned product**: a time-reparametrization
scale versus a generator spectrum.

**The dissolution thesis strengthens under the correction:** an "intertwiner" between a scale and
a spectrum is not even well-typed — there is no pair of operators on a common carrier to
intertwine. The Sturmian↔archive question dissolves at the type level, one step earlier than the
tensor-factor argument claimed.

## Error 2 (implementation): symbol-level √-flips are not field automorphisms

The v1 check (`t3_hull_v4_check.py`) acted on {√5, √10} by symbol substitution. On SUMS this
happens to be a valid automorphism action (no cross products), so its PASSes stand — but the
method is fragile: products create √2·√5, which sympy auto-merges to √10, and the substitution
then misses components. `t3_hull_v4_check_v2.py` re-implements the automorphisms in the explicit
basis (a + b√2 + c√5 + d√10) with exact rational arithmetic.

## Corrected constructive content (verified, 6/6 PASS, negative control live)

Joint decay exponents of the owned product flow: ε²·λ (products, not sums). On the quadruple
{σ(ε²)·σ(λ)}:

- flip √2 (fix ℚ(√5)) = **window swap alone** (λ_c ↔ λ_r);
- flip both (fix ℚ(√10)) = **golden conjugation alone** (ε² ↔ σ(ε²); the owned φ↔ψ duality);
- flip √5 (fix ℚ(√2)) = the double swap;
- V₄ simply transitive; the orbit's components hit all four basis directions of K = ℚ(√2,√5)
  (the joint exponent is a primitive element — the composite field is the spectral field of the
  hull product, as before).

Same labels as the sum-form memo, now on the correctly-placed object. Note ε² = φ⁻¹⁶ =
(L₁₆ − F₁₆√5)/2 — the scale's own Galois conjugate is the +√5 branch; the golden-conjugation
involution acts on the forced scale itself.

## Status

`T3_FINAL_STATE.md`'s thesis (dissolution; V₄ = the two owned dualities; K = spectral field)
stands with the placement corrected; its "golden factor = G_space" sentence and the v1 check
implementation are retracted as stated above. The package (this correction + v2 check + final
state) is what goes to the skeptic — with the self-audit already on record.
