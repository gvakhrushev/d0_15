# Post-core Extension Non-Derivation Witnesses (real completions, not identifier checks)

Lean owner `D0.Extensions.ExtensionMinimality` proves: exactly two directed proof-edges `E2→E5`, `E3→E5` (both the `a=3` exponent leg, asymmetric); `E4` isolated; 5 distinct component types (no merge).

## The two derivations (exponent leg only)
- **E2 → E5**: E2/R3 forces the per-step growth exponent `a=3` (φ³ channel); E5 reuses it at its critical line `φ³·φ^{-3}=1`. Asymmetric (E5's residue value does not pick the history carrier). Mirrors R3→R5.
- **E3 → E5**: the φ-semigroup envelope carries the same `a=3` weight `φ^{-3N}`; E5 reuses it. Same exponent leg, asymmetric.

## Key non-derivation witnesses (the 5 mandated tests)
- **E2 ↛ E4** (does history refinement force branch selection? NO): E2 carriers `W` (Perron 21.84) and `NB` (20.83) are Aut-equivariant hence block-SWAP-INVARIANT; E4 rejects swap-invariant-only functionals. Fix `E2=W`: E4's selector admission still fails. 
- **E1 ↛ E3** (does finite representation force a physical phason coordinate? NO): E1 acts on `ℂ³³` (commutant `M₃`); E3's object is the `S_DE` window behind the operator-type firewall. Fix E1-completion-A (nc=8): both E3 cocycles (`φ−1` vs `1`) still survive.
- **E3 ↛ E2** (does a common archive sector force CMB smoothing? NO): E3 finds NO common sector (integer `{24,22,20}` incommensurate with irrational `S_DE`); even granting `S_DE`, the smoothing window is not fixed. Fix `E3=(role A,φ-tick)`: both `W` and `NB` survive in E2.
- **E1 ↛ neutral-current count** (does representation reconstruction force the count? NO): the count is `p²+q²+3`, free in the grading signature (8 for (2,1), 12 for (3,0)); the anomaly is generation-blind.
- **E4 isolated**: dim-7 shell torus, zero overlap with the 33-vertex scene; coexists with every E1/E2/E3/E5 completion.
