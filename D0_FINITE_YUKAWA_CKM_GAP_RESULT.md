# D0 Finite Yukawa / CKM Gap–Mismatch — Track B Result

$$
\text{one shell-overlap tensor}\;\xrightarrow{\;\Xi_{\rm CKM}\ (\text{PROOF-TARGET})\;}\;(Y_u,Y_d)\to(H_u,H_d)\to V=H_d-H_u,\ \gamma\;\Longrightarrow\;|\sin\Theta_i|\le \frac{\|V\|}{\gamma}
$$

> **Outcome: CKM topology CERTIFIED, CKM magnitude PROOF-TARGET.** The D0 source supplies **one** symmetric
> shell-overlap tensor, **not** a genuine `(Y_u,Y_d)` pair (no distinct right carriers / oriented up-vs-down
> sectors are forced). So the mismatch `V` and gap `γ` are not forced. The genuinely-new, source-independent
> content is the finite Davis–Kahan gap/mismatch bound (`C=1`). "rank 3 ⇒ small CKM" is explicitly **not** used.

## 1. Frozen source objects / 2. Operators
The single shell-overlap tensor `D0-YUKAWA-SHELL-OVERLAP-MATRIX-001` (`YukawaShellOverlapMatrix`, symmetric
`3×3` ℚ, nonzero off-diagonal, non-diagonal); the CKM topology `D0-CKM-EXACT-001` (`CkmExactMatrix`: cyclic
permutation, doubly-stochastic 0/1, `det=1`); Higgs scalar projector (`HiggsScalarProjectorConstructive`).

## 3. Classification of admissible choices (pair)
**Pair NO-GO (pre-existing, cited):** `D0-CKM-OVERLAP-UNDERDETERMINATION-NOGO-001` exhibits two admissible
rational-orthogonal completions of the *same* single tensor — `V_A` (3-4-5 → overlap `16/25`) and `V_B`
(5-12-13 → `144/169`), both orthogonal, with `(V_A)_{01}^2 ≠ (V_B)_{01}^2`. So a genuine `(Y_u,Y_d)` pair (and
hence `V`, `γ`) is **not** forced by the source.

## 4. Exact theorem — the finite gap/mismatch bound
**`D0-CKM-DAVIS-KAHAN-GAP-BOUND-001` (CERT-CLOSED).** For finite Hermitian `H_u`, `H_d=H_u+V`, spectral
projectors `P_i^u, P_i^d` onto a cluster isolated by gap `γ`:
$$\|(I-P_d)\,P_u\|\ \le\ \frac{\|V\|}{\gamma}\qquad (C=1).$$
- Lean rational instance (`FiniteDavisKahanGapBound.finite_davis_kahan_instance`): `P_d²=P_d`,
  `‖X‖²·γ² = 16/5 ≤ ‖V‖²_HS = 8` over ℚ.
- Cert (`d0_ckm_mismatch_bound_verify.py`): `C=1` across 3000 random Hermitian samples (worst-case ratio
  `0.797<1`) + the rational instance + a no-gap negative control.
- General theorem: external **Davis–Kahan, SIAM J. Numer. Anal. 1970** (cited; not a defining engine).
- **Topology vs magnitude (separate, per B5):** topology CERTIFIED (`CkmExactMatrix`); the magnitude bound is
  contingent on a source-native `(V,γ)` which does not exist ⇒ **magnitude PROOF-TARGET**.

## 5. Removed/downgraded; 6. Minimal missing operator
No CKM magnitude is asserted from one tensor. Missing operator
$$\Xi_{\rm CKM}\in\{\text{up/down pairing selector},\ \text{common-left-carrier identification }\Xi_{ud},\ \text{holonomy}\to\text{mismatch map}\}$$
fixing (i) which tensor is read as up vs down (distinct right carriers / oriented sectors) and (ii) the common
left carrier yielding `V=H_d−H_u` with a forced gap `γ`. Class-5 selector stays fitted/MECH-LIMIT-D
(`D0-CKM-CLASS5-*`). FIREWALL: no PDG masses, no fitted CKM, no string moduli; holonomy stays a
phase/topology owner, not a source of small mixing, until `V=f(𝓗_{Core13})` is owned.

## Negative controls
3-4-5 vs 5-12-13 overlap mismatch (pair NO-GO); no-gap degenerate cluster ⇒ bound vacuous (cert control).
