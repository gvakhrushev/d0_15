# Reviewer survey and synthesis strategy — 2026-08

Written after a full pass over `theory_status_map.csv` (601 rows: 203 CORE-FORMALIZED, 168
CERT-CLOSED, 84+7 no-go, **63 OPEN/PROOF-TARGET**) with the session's spectral machinery in hand.

## Where the open mass sits

| front | open | reviewer's diagnosis |
|---|---|---|
| BOOK_04 matter | 17 | mostly blocked on *external* primitives (EFT/IR matching, role assignment, SSB sign) — not attackable by internal synthesis alone |
| BOOK_01 foundations | 12 | the cascade/count cluster; session proved the propositional route caps at 2 — needs new semantics, high risk |
| BOOK_02 spine | 10 | vNext2 family blocked on Outcome-D no-gos (non-canonical Ξ); fingerprint {1,2,8,10,12}/718 already Lean-owned |
| BOOK_08 cosmology | 9 | dark-EOS chain advanced this session; remainder needs pinned external data (DESI tables) |
| BOOK_07 gravity | 5 | heat-trace routes — consumers of closed spectral forms |

## What the session's machinery actually unlocks (and what it does not)

*Unlocks:* anything downstream of the **complete spectral data of the scene** — all three Hodge
levels now have closed-form spectra; heat traces and zetas become polynomials; moment identities
(`M₂ = D(V+6)`, `det S = 39/160`, discriminant `1/40`) become derivative facts of two generating
functions.

*Does not unlock:* rows whose EXACT-MISSING is an external functor (EFT matching, Dixmier
extraction, DESI tables) or an unowned primitive (role-vertex attachment, SSB sign). Reviewer's
rule from this session: **check ownership before deriving** — two would-be results today
(`Δ₂` table, vertex fingerprint) turned out Lean-owned (`GenericTripartiteTopHodgeSpectrum`,
`SceneSpectralFingerprint`); the checks prevented duplicate modules.

## Ranked programme

1. **[EXECUTED] Three-level Hodge assembly** (`HodgeThreeLevelSpectrum`): the corpus owns levels 0
   and 2 separately and χ=961 combinatorially; the middle level Δ₁, the factorization of the top
   heat trace over generations, the McKean–Singer exactness, b₁=0, and the doubling law were
   nowhere. All are polynomial identities once stated — machine-checked below.
2. **Feshbach/W_eff on the visible-dark split** (BOOK_02 α-front): the corpus's `W_eff(z) =
   A − B(D−z)⁻¹C` scaffold uses exactly the rank-3/dim-30 split this session proved is the
   invariant/invariant-free split; since `A` annihilates the archive, the compression is
   z-independent. Candidate next step; requires reading the residue-sum cert first.
3. **Rival-refinement dependency** (vNext2): the no-go's "inequivalent" carriers satisfy
   `allwalks − nonbacktracking = transfer` (15708 − 14990 = 718 = 2E), generically
   `Σn d² − Σn d(d−1) = Σn d`. A remark, worth a lemma next pass.
4. **Yukawa Green function** (BOOK_04): wants Puiseux indices (0, 1/4, 1/3) — ramification data a
   rank-one resolvent cannot produce; leave to the torus-ramification owner.
5. **Do not touch**: passports awaiting data; Outcome-D no-gos (they are correct); the α seam
   fork (session already collapsed doors 3=4; binding is owner-gated).
