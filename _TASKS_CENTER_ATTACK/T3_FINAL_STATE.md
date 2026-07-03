# T3 FINAL STATE — the archive leg dissolves: tensor factors, not an intertwiner (VERIFIED DRAFT)

**Status:** candidate resolution, machine-verified (`t3_hull_v4_check.py`, 6/6 PASS exact, negative
control live). Closes W4's remaining leg (i); together with the orientation leg (U T U⁻¹ = −S,
U ∈ GL(2,ℤ)) this completes T3. No registry row edited.

## The resolution

The Sturmian↔archive intertwiner question was a **category error**, and the field-disjointness
no-go was right for a deeper reason than it stated. The owned hull factorization (§06.30a,
verbatim: `G_fib = G_space ⊕ ε²G_scene`, "heat traces multiply and the spectral dimension is
additive") places the golden/toral dynamics and the scene Laplacian (whose active pair is the
archive window) in **different direct summands of one owned generator**. Summands of a direct sum
are related by the product structure of their semigroups — which the corpus already owns — and by
nothing else; demanding an operator conjugacy/intertwiner between them is asking two tensor factors
to talk. No intertwiner exists **or is needed**; the "seam" is the ⊕ itself.

## The constructive content (verified)

Over the T3 composite K = ℚ(√2,√5):

1. The joint (sum) spectrum {gᵢ + wⱼ} of the two factor pairs — toral {φ⁻¹, −φ} and window
   {3/2 ∓ √10/40} — **generates exactly K** (minimal polynomial degree 4). The composite field is
   not a repair; it is the spectral field of the owned hull product. (ε² = φ⁻¹⁶ is a ℚ(√5) scalar
   and does not affect the orbit structure.)
2. **Gal(K/ℚ) ≅ V₄ acts simply transitively on the spectral quadruple, factor-wise:**
   - the involution fixing ℚ(√10) is the **golden conjugation** φ↔ψ alone — the duality the corpus
     already owns (σ(φ⁻¹) = −φ, the w_DE sign forcing);
   - the involution fixing ℚ(√5) is the **archive window swap** λ_c ↔ λ_r alone;
   - the involution fixing ℚ(√2) is their composite (double swap).
   The two owned dualities of the corpus are precisely the two generating Galois involutions of the
   composite field, and ℚ(√2) — T3's mystery third subfield — is the fixed field of their product.
3. Field disjointness over ℚ (the original no-go's reason) is exactly what makes the action simply
   transitive: the factors share nothing, which is the *correct* relation between tensor factors —
   the obstruction was the structure.

## Status accounting

- W4 leg (ii) (orientation): RESOLVED earlier — explicit unimodular conjugator, even-tick level.
- W4 leg (i) (field/archive scale): **DISSOLVED** — reframing candidate; nothing to intertwine.
- `D0-STURMIAN-REFINEMENT-DISCHARGE-NOGO-001` stands and is *explained*: it correctly refused an
  intertwiner that the hull's own ⊕-structure forbids.
- This is a reframing theorem, not a forcing; obligations: skeptic pass (primary target: the
  identification of the golden factor with G_space's time layer and the window with ε²G_scene's
  active pair against the §06.30a text — both are definitional-grade but must be quoted through),
  then minting per protocol.
