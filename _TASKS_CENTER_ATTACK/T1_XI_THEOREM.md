# T1 Ξ-THEOREM — the operator-level intertwiner for the whole Bartholdi family (VERIFIED DRAFT)

**Status:** candidate theorem, machine-verified exactly (`t1_xi_operator_check.py`, 11/11 PASS,
integer arithmetic, reachable negative control). Closes T1's remaining obligation (Addendum 2 §4.1:
upgrade det-level to Ξ_N-level). No registry row edited.

## Statement

Let S, T : ℂ^E → ℂ^V be the start/end maps of the directed-edge carrier of K(9,11,13)
(S_{v,e}=[s(e)=v], T_{v,e}=[t(e)=v]), J the edge flip, B the Hashimoto operator,
Φ = [S;T] : ℂ^718 → ℂ^66, M = [[A,−I],[D−I,0]], σ = [[0,I],[I,0]]. Then, as exact operator
identities (all verified):

1. STᵀ = A, SSᵀ = TTᵀ = D, SJ = T, TJ = S;  B = TᵀS − J.
2. **ΦB = MΦ and ΦJ = σΦ, hence Φ(B + tJ) = (M + tσ)Φ for ALL t** (linearity; spot-checked at
   t = 2, −3). One map intertwines the entire Bartholdi family with the 66-dim vertex family M_t.
3. B + J = TᵀS (rank ≤ 33), so ker Φ = ker S ∩ ker T is invariant for the whole family, which acts
   there as **(t−1)J** — eigenvalues ±(t−1): the Bartholdi prefactor `(1−(1−t)²u²)^(…)` IS the
   kernel action, and the vertex polynomial is the coimage action. The det identity family is the
   shadow of this one operator statement.
4. rank Φ = 2|V| − 1 = 65 (connected non-bipartite; the 1 is the (α𝟙,−α𝟙) cokernel),
   dim ker Φ = 653 — exactly the 653 unit-modulus eigenvalues of B observed in W1.

Identities 1–3 are graph-general (Bass's block proof made explicit — external owner: Bass 1992,
W5/W7 sourcing); the scene instantiates them; 4 is the scene-specific leg.

## Consequences

- **Ξ = Φ**: the canonical comparison map is a single explicit integer operator, built from raw
  scene data (S, T, J — raw-graph grade), uniform in t — fork-independent exactly as the
  presentation-covariance frame (Addendum 2) required. Candidate owner for
  `PRIM-COMPARISON-MAP-XI-N`.
- **Hierarchy upgrade for free:** ΦBᵏ = MᵏΦ by induction ⇒ Φe^{−uB} = e^{−uM}Φ (heat level);
  block-Schur compressions commute through Φ (Feshbach level). The vNext2 typing
  (compression < spectral < heat < Feshbach) is met at every level by the same map.
- Structural echo (flagged, not claimed): at the golden point t = φ⁻¹ the kernel action is
  (φ⁻¹−1)J = **−φ⁻²J** — the typed return weight appears as the kernel eigenvalue of the family.

## Obligations

Skeptic pass (the interpretive step "Φ is Ξ_N" — the identities themselves are exact); minting per
closure protocol (Lean: identities 1–3 are `decide`-able on integer matrices; 4 needs a rank
witness); wire into the T1 presentation-covariance memo as its missing §4.1 leg.
