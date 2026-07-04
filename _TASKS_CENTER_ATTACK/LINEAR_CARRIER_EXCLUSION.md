# LINEAR CARRIER EXCLUSION — the 2¹¹ pairing's necessity is now derived (VERIFIED)

**Status:** consolidated result of the realization campaign's final round. Three legs, each exact:
a theorem (vertex), an exact witness + cert (edge, natural candidate; computed by the owner-user's
session, independently reverified here), and a universal spectral bound (all splits, all owned
linear operators). Together they derive the NECESSITY of the multiplicative/Fock level for the
μ₂-realization — converting the content of the external Dixmier edge from an assumption into a
located construction problem. No registry row edited.

## The exclusion chain

1. **Vertex level — seam ≡ 0 (theorem; `SEAM_LOCATION_THEOREM.md`, `seam_location_check.py` 5/5).**
   The kernel (8⊕10⊕12) is invariant under the whole vertex algebra ⟨A, D_deg⟩: B = C = 0 for any
   vertex W_eff. Depth moments unrealizable.
2. **Edge level, natural candidate — exact mismatch witness (`edge_alpha_moment_realization.py`,
   exit 0; independently reverified).** On the owned 359-edge carrier with the unified-chain
   P_term/Q_bulk split and L_E: the seam is nonzero and the exact depth moments are
   **Tr(BC) = 2678/3, Tr(BDC) = 84971/6**, ratio **84971/5356 ≈ 15.86** — versus the required
   **μ₂/μ₁ = 36864/5 = 7372.8**. Ratio is normalization-invariant: no overall constant repairs it.
   Anti-circularity control: inserting 2¹¹ by hand is rejected as the external object itself.
3. **Universal bound — no split and no owned linear operator can work (verified).** For symmetric
   L with C = Bᵀ: `B D Bᵀ ⪯ λ_max(D)·B Bᵀ`, and by compression interlacing
   `λ_max(QLQ) ≤ λ_max(L)`. Hence for EVERY split (P, Q):
   `m₂/m₁ = Tr(BDBᵀ)/Tr(BBᵀ) ≤ λ_max(L)`. Measured: λ_max(L_E) = 41.84 (≤ the line-graph degree
   bound 44); the owned linear operators all sit at degree scale — A: 21.84, B (Hashimoto): 20.83,
   B+R: 21.84, L_E: 41.84. **Required ratio 7372.8 exceeds every owned linear spectral radius by
   two orders.** The linear level is exhausted.

## The conclusion (what is now derived vs what remains)

**Derived (new):** the μ₂ = 2¹¹·(6/5) realization cannot live on any owned linear carrier — vertex
by theorem, edge by universal bound. A ratio of 7372.8 demands capacity at the 2048 scale, which
among owned constructions exists only in the **multiplicative class** — the Fock/exterior functor
Λ*(V₁₁) with dim 2¹¹, exactly the carrier the ledger row (`D0-ALPHA-MU2-FULL-LEDGER-001`) and the
CVFT sharpening had named. What was an assumption ("the residue traces over the full 2¹¹ Fock
space") is now the unique surviving carrier class, by exhaustive exclusion with exact witnesses.

**Remaining (the true irreducible core, unchanged in kind, reduced in scope):** construct the
Fock-level W_eff — the second-quantized seam on Λ*(V₁₁) — and verify its depth moments hit
(μ₁, μ₂) = (1/3, 12288/5). The external Dixmier/Wodzicki citation now covers ONLY the functional-
analytic packaging of that construction, not the choice of carrier: the carrier is forced.

## Honest caveats

- Leg 3's operator table covers the owned scene operators enumerated in this campaign; a linear
  operator with spectral radius ≥ 7372.8 would evade the bound — none is owned, and any candidate
  would have to be derived, not chosen (M1).
- The u = φ⁻³ grading enters only through the ratio's invariance argument (jointly rescaling
  m₁, m₂ cannot fix a ratio); no u-typing was consumed.
- Leg 2's witness is for the natural contact split; leg 3 is what universalizes it. Both certs can
  fail (reachable controls; leg-2 cert rejects the hand-injected 2¹¹).
