# CVFT F4/F7 CERT REFORGE — integrity repair of the 4 fake-control certs

**Date:** 2026-07-05 · **Trigger:** `CERT_CANFAIL_SWEEP_REPORT.md` Finding F2 · **Scope:** the four certs that are the ENTIRE formal backing of `D0-CVFT-F4` and `D0-CVFT-F7` (both CERT-CLOSED, `lean_status=PYTHON_CERTIFIED`, no Lean module).

**Rule followed:** originals in `05_CERTS/` untouched; four `*_REFORGED.py` rebuilt here; no registry edits — proposed motions only (owner blessing required).

---

## 1. What the claims actually assert (registry rows, quoted verbatim)

**D0-CVFT-F4** — book `BOOK_02/05`, section `CVFT UV feedback-tail cut program`, `lean_status=PYTHON_CERTIFIED`, `release_status=CERT-CLOSED`, `python_cert=vp_cvft_uv_feedback_tail_bound_refined.py;vp_cvft_ueff_pole_discipline.py`. Notes verbatim:

> UV cutoff claims have deterministic finite cert candidates for the refined tail bound under |z|rho(F_N)<1; Lean proof remains open. [was:CERT-CANDIDATE] [8C: linked passing cert]

**D0-CVFT-F7** — book `BOOK_07`, section `CVFT boundary-local holographic rank lemma`, `lean_status=PYTHON_CERTIFIED`, `release_status=CERT-CLOSED`, `python_cert=vp_cvft_boundary_channel_rank.py;vp_cvft_refined_logdet_rank_bound.py`. Notes verbatim:

> Boundary-local rank control has deterministic finite cert candidates; it supports localization only and is not an A4 proof. [was:CERT-CANDIDATE] [8C: linked passing cert]

## 2. The owned mathematical content (what a real cert must verify)

Sources: `01_BOOKS/BOOK_02...md` §02.CVFT.v5 (refined feedback bounds and compressed pole discipline), `01_BOOKS/BOOK_07...md` §07 rank-localization + UV-tail-cut paragraphs (lines ~199–210), `01_BOOKS/BOOK_05...md` §05.27 (CVFT operator admissibility) + §05.28 (forbidden shortcuts), `D0_CLAIM_CLOSURE_CONTRACT.md` "CVFT operator hardening".

Typing (contract + §05.27): `F_N = P_N U_N† Q_N U_N P_N` is feedback-return only, with the **allowed identities** `F_N=(Q_NU_NP_N)†(Q_NU_NP_N)`, `F_N = P_N − (P_NU_NP_N)†(P_NU_NP_N)`, positivity, and `F_N=0 ⇔ Q_NU_NP_N=0`. **Forbidden:** `Q_N≠0 → F_N≠0`; determinant trace without `−log det`; complex mass/width poles from bare positive `F_N` (complex poles belong to `U_eff=P_NU_NP_N` or Feshbach–Schur); rank boundary as A/4 proof; resolvent/log-det expansions outside `|z|ρ(F_N)<1`.

Per-cert content:

| Cert (original) | Claim | Real content to verify (BOOK_02 §02.CVFT.v5 / BOOK_07) |
|---|---|---|
| `vp_cvft_boundary_channel_rank.py` | F7 | `rank(F)=rank(QUP)`; if `im(QUP) ⊆ B_boundary(P,Q)` then `rank(F) ≤ dim B_boundary`; channels identified with cut/touched channels before writing `|∂(P,Q)|`; localization only — NOT an A4 proof (bound is an inequality: non-saturation witness must exist) |
| `vp_cvft_refined_logdet_rank_bound.py` | F7 | for `a=|z|ρ(F)<1`, analytic branch at `z=0`: `|−log det(I−zF)| ≤ rank(F)·[−log(1−a)] ≤ rank(F)·a/(1−a)`; real-z leg `−log det(I−zF) ≤ rank(F)[−log(1−zρ)]`; the `|z|`-only form (without ρ(F)) is not the theorem |
| `vp_cvft_uv_feedback_tail_bound_refined.py` | F4 | tail `T_M(z,F)=Σ_{m>M} z^m/m·Tr(F^m)` obeys `|T_M| ≤ rank(F)/(M+1)·a^{M+1}/(1−a)`, `a=|z|ρ(F)<1`; fallback `rank(P)`; `δ₀¹²` is the finite readout noise-floor (regime classifier on `|T_M|`), NOT the analytic convergence radius |
| `vp_cvft_ueff_pole_discipline.py` | F4 | `U_eff=PUP` is a contraction; complex pole language (energy=arg λ, width γ=−log|λ|>0) belongs to the compressed non-normal `U_eff`; bare positive `F` has real nonnegative spectrum — complex poles can NOT come from bare positive `F` |

Owned constructibility: the scene is `K(9,11,13)` (complete tripartite; `|V|=33`, `|E|=359`, `9·11·13=1287` triangles; Laplacian spectrum `{0¹,20¹²,22¹⁰,24⁸,33²}`), the retained/active projector is the rank-3 zone-average subspace with nullity 30 (GOLDEN THE 44.1 "Rank/Nullity 3/30" per BOOK_05 endnotes), and `δ₀=(√5−2)/2=1/(2φ³)` is owned by BOOK_01 §01.6. So the finite objects ARE constructible from owned definitions — the originals simply never constructed them.

## 3. Before — what the four originals actually did (audit recap + new findings)

All four share the F2 defect: `NEGATIVE_CONTROL_CAUGHT FAIL_*` printed **unconditionally on the success path**; no control computation exists in any file. Beyond F2:

| Original | Checks are | New defects found during reforge |
|---|---|---|
| `vp_cvft_boundary_channel_rank.py` | tautologies over a hardcoded 4×3 `qup` literal; `dim_boundary=2` hardcoded; "control" is `2 != 4` | never verifies `im(QUP)⊆B` (the lemma's hypothesis); never verifies PSD/typing; `rank_not_a4 = dim_boundary != 4` is a literal-vs-literal comparison with no A4 content |
| `vp_cvft_refined_logdet_rank_bound.py` | hardcoded eigen-list `[0.8,0.4,0.0]`, single hardcoded `z`; "control" is `abs(z) != abs(z)*rho` = `0.45×1 ≠ 0.45×0.8`, a float-literal inequality | never constructs F; never tests the analytic branch off the real axis beyond one point; no tightness witness so a weakened bound would also "pass" |
| `vp_cvft_uv_feedback_tail_bound_refined.py` | hardcoded eigen-list, one `z`, one `M`; tail truncated at m<80 with no truncation control; "control" is `a != 1e-6` | **hardcoded `delta12 = 1e-6` is NOT the owned noise-floor**: `δ₀¹² = ((√5−2)/2)¹² ≈ 7.35e-12`, off by >5 orders of magnitude — the one number that ties the cert to BOOK_07's regime clause is wrong |
| `vp_cvft_ueff_pole_discipline.py` | hardcoded eigen-list `[0.8·e^{0.3i},0.5,0.0]` for `U_eff` and `[0.64,0.25,0.0]` for `F`; "pole check" is `|0.3−0.3|<1e-12`; "positivity" is `isinstance(x,float) and x>=0` over a literal list | `U_eff` is never constructed from any `P,U`; the two eigen-lists are unrelated (0.64=0.8², 0.25=0.5² suggests intent `F=|U_eff|²`, which is NOT an owned identity — for non-normal `U_eff` the singular values, not eigenvalue moduli, relate to `F`); `isinstance(x,float)` "spectral reality check" is a type check, not mathematics |

## 4. After — the four REFORGED certs

Shared architecture (each file self-contained, numpy-only, no file I/O, deterministic seeds, `SystemExit(main())`):

1. **Owned-scene layer** — build `K(9,11,13)` adjacency + Laplacian exactly; verify the owned invariant set (`|V|,|E|,triangles`, spectrum multiplicities, `[L,P]=0`, rank/nullity 3/30) — any mismatch exits 1.
2. **Typed-object layer** — `P` = zone-average projector (rank 3), `Q=I−P`, unitary family `U = exp(−iθL)·D_S` (graph flow × phase gates on touched channel sets `S`), unitarity verified numerically. Every number the originals hardcoded is **derived** here (boundary dims, ranks, ρ(F), pole phases/widths, δ₀¹²).
3. **Lemma layer** — the asserted inequalities/identities verified with explicit tolerances over deterministic grids (θ, phases, `S`, complex `z`, `M`).
4. **Executed negative controls** — mutation-style: the same verification functions re-run on perturbed objects (planted rank overflow, non-unitary dilation, broken PSD, weakened bound on a computed tight witness, domain violation `a≥1`, δ₀-as-radius confusion). A control that is NOT caught fails the cert (`return 1`). `NEGATIVE_CONTROL_EXECUTED_AND_CAUGHT <name>` is printed only after the mutated check has actually run and failed.

Per-cert detail and run transcripts follow in §5–§8 (filled in as each cert lands).

## 5. `vp_cvft_boundary_channel_rank_REFORGED.py` (F7, leg 1)

**Status: PASS (exit 0), all 5 negative controls executed and caught, 3/3 external mutation probes fail the cert.**

Construction: full K(9,11,13) scene (33×33 exact Laplacian), owned invariants recomputed (`|V|=33, |E|=359, tri=1287`, spectrum `{0¹,20¹²,22¹⁰,24⁸,33²}`), `P` = rank-3 zone-average projector with computed `‖[L,P]‖=1.0e-14`, unitary family `U = exp(−iθL)·D_S`. The original's hardcoded numbers are now derived: `dim B` is the computed rank of the constructed channel space `span{U_L Q e_j : j∈S}`, and `rank(F)` comes from SVD of the computed `QUP`.

Verified lemma content: `rank(F)=rank(QUP)`; `im(QUP)⊆B` (computed residual); `rank(F) ≤ dim B ≤ |S|`; `rank(F) ≤ rank(P)=3`; PSD + Hermitian; allowed identity `F = P − (PUP)†(PUP)` (BOOK_05 §05.27). Bonus theorem-grade witnesses the original never had: (a) the forbidden shortcut `Q≠0→F≠0` is *refuted* by the computed zero-leakage member `U=exp(−iθL)` (`‖QUP‖<1e-9` with `Q≠0`, forced by `[L,P]=0`); (b) the not-an-A4-proof discipline is witnessed computationally — strict slack `rank(F)=1 < dim B=2` on the same-zone-equal-phase member, saturation on the single-channel member: an inequality with computed strict slack cannot be a capacity equality.

Executed negative controls (each runs the verifier on a mutated object; not-caught ⇒ exit 1): `NC_SCENE_EDGE_DELETED`, `NC_DECLARED_B_TOO_SMALL` (4-channel gate vs declared 2-channel B: containment rejects), `NC_RANK_EQUALITY_MUTATION` (full-rank Hermitian perturbation), `NC_PSD_MUTATION`, `NC_NONUNITARY_DILATION` (1.03·U: unitarity AND the allowed identity both reject). External mutation probes (scratch copies): zone size 9→10 ⇒ `FAIL_SCENE_INVARIANTS` exit 1; F built from `PUP` instead of `QUP` ⇒ exit 1; `num_rank` sabotaged to full-dim ⇒ exit 1.

Numerics hygiene: macOS Accelerate BLAS emits *spurious* matmul FP warnings on finite 33×33 inputs (verified `eye(33)@eye(33)` trips FP flags); that unreliable channel is silenced for matmul only and replaced by explicit `require_finite` gates on every computed operator — NaN/inf anywhere is a hard failure path (this converts the sweep's row-13 warn-but-exit-0 pathology into a designed failure mode).

## 6. `vp_cvft_refined_logdet_rank_bound_REFORGED.py` (F7, leg 2)

**Status: PASS (exit 0, no warnings), all 5 negative controls executed and caught, 3/3 external mutation probes fail the cert.**

Construction: same owned scene; three scene-typed `F=(QUP)†(QUP)` members with COMPUTED ranks 1/2/3 and computed `ρ(F) = 0.0604 / 0.2797 / 0.3178` (all ≤ 1, contraction typing verified — the original's `eigs=[0.8,0.4,0.0]` list is replaced by actual spectra of actual operators). 84 bound instances verified: `|−log det(I−zF)| ≤ rank(F)·[−log(1−a)] ≤ rank(F)·a/(1−a)` over 4 radii `a∈{0.1,0.5,0.9,0.99}` × 6 complex phases per member, plus real-z legs. The analytic branch connected to `z=0` is the eigen-sum branch, cross-checked branch-free via `exp(−logdet)=det(I−zF)` (this gate is what catches the contract's forbidden "determinant trace without −log det": the sign-flip probe dies here). A computed tightness witness (rank-1 member, real z, `a=0.9`) shows `logdet = bound` to 12 digits — the bound is attained, so ANY weakening or checker slack breaks the cert (probe: tightening to 0.5·bound fails instantly at a=0.1).

Executed negative controls: `NC_WEAKENED_RANK_BOUND` (rank−1 bound violated by computed rank-2 member: 2.7167 > 2.3026), `NC_LOGDET_INFLATION` (×1.05 on the tight witness fails), `NC_DOMAIN_VIOLATION` (`a=1.001` refused — the hypothesis `|z|ρ(F)<1` is enforced, not decorative), `NC_FLIPPED_CONVEXITY` (reversed second inequality false on grid), `NC_FORBIDDEN_Z_ONLY_FORM` — the original's fake control, made real: computed witness `|z|=1.4, ρ=0.0604, a=0.0845<1` where the theorem form evaluates and holds while `−log(1−|z|)` is domain-invalid — the `|z|`-only form is provably not the theorem, by computation. External probes: half-bound sabotage exit 1; `+log det` sign flip exit 1 (branch-consistency gate); `ρ` halved exit 1 (tightness catches it).

## 7. `vp_cvft_uv_feedback_tail_bound_refined_REFORGED.py` (F4, leg 1)

**Status: PASS (exit 0, no warnings, 0.13 s), all 5 negative controls executed and caught, 3/3 external mutation probes fail the cert.**

Construction: owned scene + the three scene-typed `F` members (computed ranks 1/2/3, `ρ≤1`). The tail `T_M(z,F)` is computed by TWO independent routes that must agree within a certified geometric remainder: the eigen closed form `−Σ_i[Log(1−zλ_i) + Σ_{m≤M}(zλ_i)^m/m]` and direct partial summation via the joint powers `(zλ_i)^m` (the separate `z^m·λ^m` route genuinely overflows for `|z|>1` — found and fixed during build; the original's blind `m<80` truncation had no such control at all). **720 bound instances verified**: `|T_M| ≤ rank(F)/(M+1)·a^{M+1}/(1−a)` over 3 members × 4 radii × 6 complex phases × 5 cuts `M∈{0,1,2,4,8}`, each also re-verified with the ambient `rank(P)=3` fallback (the claim's fallback clause).

δ₀ discipline made exact: `δ₀=(√5−2)/2 = 1/(2φ³)` verified as an identity to 1e-15 (both routes computed), `δ₀¹² = 7.313e-12`. **Original defect exposed: the retired cert hardcoded `delta12=1e-6` — off from the owned floor by ~136,746×.** BOOK_07's regime clause is witnessed computationally at fixed `a=0.5`: `|T_2|=1.04e-1 > δ₀¹²` (finite-feedback regime) while `|T_40|=2.18e-14 < δ₀¹²` (smooth-interface regime) — the floor classifies `(M,|T_M|)`, not `a`.

Executed negative controls: `NC_EXPONENT_WEAKENED` (`a^{M+2}` bound violated: 0.0117 > 0.0039), `NC_RANK_WEAKENED` ((rank−1)-bound violated by the rank-2 member: 0.1438 > 0.1111), `NC_DIVERGENCE_REFUSED` (`a=1.02` refused AND partial sums computed to grow 7.3→21.6), `NC_TRUNCATION_SENSITIVE` (2-term truncation of a fat tail disagrees by 1.0 — the consistency gate has teeth), `NC_DELTA0_AS_RADIUS` (both confusion shapes refuted by computed witnesses: `a=0.5>δ₀¹²` yet convergent+bounded; `|T_2|>δ₀¹²` yet the bound holds). External probes: bound denominator `M+1→M+3` exit 1; closed-form head off-by-one exit 1; `δ₀` mis-set exit 1.

## 8. `vp_cvft_ueff_pole_discipline_REFORGED.py` (F4, leg 2)

**Status: PASS (exit 0, no warnings), all 5 negative controls executed and caught, 3/3 external mutation probes fail the cert.**

Construction: owned scene; `Z` = orthonormal 3-channel zone basis (`ZZ†=P`); `U_eff = Z†UZ` — an actual 3×3 compressed transfer, genuinely non-normal for leaky members (non-normality computed and asserted, `FAIL_WITNESS_SETUP` otherwise). Verified per member: contraction `σ_max(U_eff) ≤ 1`; the allowed identity `U_eff†U_eff + F_c = I₃` to 3e-15 (BOOK_05 §05.27 `F = P−(PUP)†(PUP)` in block form); the quantitative damping⇔leakage dichotomy `3−Σσᵢ² = tr F` to 1e-8; bare `F` spectrum real-nonnegative via a GENERAL eigensolver (the original used `isinstance(x,float)` — a type check); pole table (E=arg λ, γ=−log|λ|) computed from the scene: flow-only member has γ≈0 exactly and `tr F<1e-12`; leaky members have damped complex poles, e.g. witness `E=−1.4885, γ=0.1707` (vs the original's hardcoded `0.3` and `γ=−log 0.8`). Genuine non-normal effect visible: `leaky_2ch` has `σ_max=1.000000` (one untouched active direction) while ALL its pole moduli are <1 (γ∈{0.031,0.061,0.128}) — a spectrum/singular-value split no hardcoded eigen-list could exhibit.

Executed negative controls: `NC_COMPLEX_POLES_FROM_BARE_F` — the fabricated control made real, three computed prongs (all bare F real to 1e-10; skew-Hermitian plant caught by both the Hermiticity and spectrum gates; complex phases exist only in the non-Hermitian `U_eff` — so the forbidden shortcut "complex poles from bare positive F" is refuted by computation); `NC_ORIGINAL_MODULUS_IDENTITY` — the retired cert's implicit relation `spec(F)=|eig(U_eff)|²` (its two lists were `[0.64,0.25,0]=|[0.8,0.5,0]|²`) is computationally FALSE under the owned typing: computed `spec(F_c)={0, 0.105, 0.280} = 1−σ²` vs `|λ|²={0.775, 0.884, 0.940}`; `NC_NONUNITARY_DILATION`; `NC_UNDAMPED_MUTATION` (amplified block: γ<0 detected and rejected); `NC_UNITARY_BLOCK_ON_LEAKY` (the `U_eff†U_eff=I` hypothesis rejected when leakage exists). External probes: F built from `PUP` ⇒ identity gate fails exit 1; contraction gate loosened to ≤2 ⇒ the dilation CONTROL ITSELF fails the cert exit 1 (controls police the verifiers); zones (9,12,12) ⇒ scene invariants fail exit 1.

## 9. Verdicts and proposed registry motions

Final suite run (2026-07-05): all four REFORGED certs exit 0, zero warnings, 5 executed-and-caught negative controls each; 12/12 external mutation probes produce exit 1.

### Verdict per claim

**D0-CVFT-F4 — verdict: (a) PASS honestly, constructible, reforged certs pass.**
The claim's mathematical content (refined tail bound under `|z|ρ(F_N)<1` + compressed pole discipline) is REAL and is now verified on operators constructed from owned definitions (K(9,11,13) scene, rank-3/nullity-30 zone split, `F=(QUP)†(QUP)` typing, owned `δ₀`). 720 tail-bound instances + fallback clause + noise-floor regime clause + full pole-discipline package pass with genuine can-fail checks. BUT: the evidence on file at audit time was fabricated-control theater over hardcoded literals with one wrong owned constant (`delta12=1e-6` vs `δ₀¹²=7.31e-12`), so the CERT-CLOSED status was **unsupported during the entire period the originals were the backing**.

**D0-CVFT-F7 — verdict: (a) PASS honestly, constructible, reforged certs pass.**
The rank-localization lemma (`rank(F)=rank(QUP) ≤ dim B_boundary`, log-det chain, localization-only discipline) is real and now verified with a constructed boundary-channel space, computed tightness witness, and executed controls including the two disciplines the originals faked (`not an A4 proof` → computed non-saturation witness; `|z|-only form is not the theorem` → computed domain-discrimination witness). Same caveat: CERT-CLOSED was unsupported until now.

### Proposed motions (owner blessing required; NO registry edits made)

1. **M1 (swap, both claims):** replace `python_cert` for `D0-CVFT-F4` with `vp_cvft_uv_feedback_tail_bound_refined_REFORGED.py;vp_cvft_ueff_pole_discipline_REFORGED.py` and for `D0-CVFT-F7` with `vp_cvft_boundary_channel_rank_REFORGED.py;vp_cvft_refined_logdet_rank_bound_REFORGED.py` (files to move into `05_CERTS/` under the original names or `_v2` names at owner's discretion). Originals retired to quarantine with an incident note (fabricated negative controls, per the v17 fabricated-citation precedent).
2. **M2 (status):** with M1 accepted, `release_status=CERT-CLOSED` and `lean_status=PYTHON_CERTIFIED` become supportable again for both claims; append to notes: `[2026-07-05 reforge] original certs had fabricated negative controls (sweep F2); replaced by scene-constructed can-fail certs; CERT-CLOSED re-affirmed on new evidence`. If the owner declines M1, both claims MUST demote to `PROOF-TARGET` (their sole backing is known-fake).
3. **M3 (interval honesty):** whatever the outcome, the ledger should record that between the original closure (`[8C: linked passing cert]`) and 2026-07-05, both CERT-CLOSED labels rested exclusively on non-verifying certs.
4. **M4 (siblings):** the three unreferenced no-failure-path siblings (`vp_cvft_boundary_rank_bound.py`, `vp_cvft_logdet_rank_bound.py`, `vp_cvft_uv_feedback_tail_bound.py`) are superseded by the reforged pair and should be retired or marked non-load-bearing demos.
5. **M5 (Lean queue):** both claims remain `PYTHON_CERTIFIED` (no Lean). The reforged certs' check lists are Lean-ready statements (finite-dimensional rank/log-det/tail/contraction lemmas); registering them as Lean targets would lift F4/F7 out of the python-only tier — optional, owner's call.

### Worst discovery

The worst single finding is in the retired `vp_cvft_ueff_pole_discipline.py`: beyond the fabricated controls, its two hardcoded eigen-lists encode the relation `spec(F)=|eig(U_eff)|²` (`0.64=0.8², 0.25=0.5²`) — an identity that is FALSE under the owned typing for non-normal `U_eff` (the owned relation is `spec(F_c)=1−σ²(U_eff)`, verified here; the two differ by 0.66–0.87 on a real scene member). I.e. the fake cert didn't just fail to verify the claim — the numbers it displayed as "the certified objects" are mutually inconsistent with the operator theory the claim is about. Corroboration theater with wrong props.

### Limits (honest)

- The reforged certs verify the lemmas on deterministic finite FAMILIES of scene-typed operators (graph flow × phase gates), not universally quantified over all admissible `(P,Q,U,z)`; universality is exactly the open Lean obligation the registry already records ("Lean proof remains open"). This matches corpus practice for CERT-CLOSED (cf. the SOLID F6 cert) but does not exceed it.
- `dim B_boundary` is constructed from touched registration channels; the cut-edge identification clause of BOOK_02 is honored in the sense "channels = computed spanning set of the gate's leak image", the strongest finite reading available without a frozen continuum boundary object.
- The Accelerate-BLAS spurious-FP-warning suppression is scoped to matmul/det messages only and is compensated by explicit `require_finite` gates; on a non-Accelerate platform the filters are inert.
