# MEMO A4D -- resolved curved stationary closure (F4 / lower wall)

**Task:** `EXP-A4D-RESOLVED-CURVED-STATIONARY-CLOSURE`
**Execution:** PR #202
**Status:** IN_PROGRESS / durable checkpoint (restructured F4 attack)
**Baseline:** `75fc9eec99dcb8b5b15a0bc0de5662c9453175f4`

## 0A. RESUME CHECKPOINT -- durable state

### Architecture (locked; do not reopen)

- Upper-wall F5 is closed on PR #201: flat metric Hessian of `S_star` is
  exactly `(1/4) K_{E_eta}` with `beta_sp = 0`.  `Q(R) = O(eps^10)` near flat cannot
  alter F5.
- On quotient-complete strata,
  `Crit(S_star+Q)/G_aff ~= Crit(S_star)/G_Lor`: `Q` is auxiliary on shell and
  cannot manufacture new physical curved stationary dynamics by tuning alone.
- Correct H1 for coefficient search: seek finite curved configurations with
  active residual section `R = R_*(C) != 0` and `R_*(0) = 0`, **not** force
  `R = 0` as the primary ansatz.  Do **not** run a 7x7 `(a,b)` grid or `a=b`
  ray.
- Action family under attack uses **four independent** joint-residual scalars
  (do **not** collapse adj=opp):

      I^eta_adj,  I^eta_opp,  I^n_adj,  I^n_opp

  with adj = `|S1capS2|=1`, opp = `|S1capS2|=0`, `I^eta = R^T eta R`,
  `I^n = R^T h_n R`, and
  `R_{2|1} = det(I-P1)t2 - (I-P2) adj(I-P1) t1`.

- Forbidden: Holst / phi / new I-channel; continuum Einstein; declaring adj=opp
  dead without `ker M`; editing #201 / Lean / BOOK; self-merge.

### EXACT/CERTIFIED -- inherited from main (#199/#187/#200)

- Local `E_v`: rank 16 / ker 20; Bianchi subclass ker 10 (`E_v=0` does not force `C=0`).
- Two-link #178: no nondegenerate solder-stationary representative.
- One-boost: all-site nondegenerate `E_v=0` with `C!=0`; free-B connection Euler
  rank 282 / nullity 294; four reduced origin constraints.
- Checkerboard Lorentz-null quotient nulls nonlinearly obstructed from
  canonical flat solder.

### EXACT/CERTIFIED -- F4 support + response matrix (this PR)

Certificate: `a4d_resolved_curved_stationary_f4_check.py`.

1. **Support obstruction on the `R=0` locus.**
   Solder-scale and flat->two-link witnesses at vanishing translation data have
   `Delta I_j = 0` for all four channels while `Delta S_star != 0`.  No `c in Q^4` can
   cancel those star Euler components using I-channels dormant at `R=0`.
   Scope: **not** a no-go on the H1 locus `R=R_*(C)!=0`.

2. **Exact 4-column response matrix.**
   Over 9 active edge/face translation witnesses on the owned two-link+RCD
   background:

      rank M = 4,   dim ker M = 0

   exactly over `Q`.  In particular `eta`-adj - `eta`-opp is not in `ker M`.
   Matched-edge values at `t=1`:

      I^eta_adj=-256/9, I^eta_opp=-128/9, I^n_adj=4352/81, I^n_opp=128/9.

3. **One-boost structural dead-ansatz lemmas.**
   Constant and `x0`-only slices of `ker H_v` are degenerate at boost-plane
   sites; 12 satellite complementary components are forced into `span{e0,e1}`;
   free-B necessary residuals are automatic on `ker H_v`.

4. **Scoped exact span obstruction in a 6D Cayley chart (this PR).**
   At the rational point `p=(2/5)^6` in the six Cayley generators
   (boosts 01/02/03 + rots 12/13/23) with matched `b=e0` on the origin A-edge,
   exact finite-difference gradients satisfy

      rank B = 4,   rank[B | -g] = 5

   over `Q`, with `C!=0` (25 curved cells) and all four `I_j` active.
   Therefore `-grad S_star` is **not** in `im B = span{grad I_j}` inside this
   chart.  A five-point rational grid in the same chart (including mixed signs)
   all repeat `rank B=4 < rank[B|-g]=5` with `C!=0` and active `I_j`.
   Certificate sections `SECTION_SPAN_OBSTRUCTION_6D` and
   `SECTION_SPAN_OBSTRUCTION_6D_GRID`.
   Scope: declared 6-parameter Cayley + matched translation only; not yet a
   global F4 no-go over full field space / all Pi projections.

5. **Ambient ORIGIN28 widen of the span obstruction (this PR, Track A).**
   At the same rational Cayley background `p=(2/5)^6` with matched `b=e0`,
   exact FD gradients in the full 24-dimensional left-Cayley `so(1,3)` tangent
   space on the four ORIGIN edges, plus 4 free translation-component directions
   on the matched edge (`S_star` is b-independent here, so those `g_b=0`),
   again satisfy

      rank B = 4,   rank[B | -g] = 5

   over `Q`, with `C!=0` and active `I_j`.  A second mixed-sign Cayley
   background repeats the same ambient ranks.  Certificate sections
   `SECTION_SPAN_OBSTRUCTION_AMBIENT_ORIGIN28` and
   `SECTION_SPAN_OBSTRUCTION_AMBIENT_ORIGIN28_MIXED`.
   Scope: widens chart-parameter obstruction to ambient ORIGIN-link Lorentz
   tangent + free matched-edge `b` at two rational backgrounds; still **not**
   a global Pi-projected / free-solder / all-site F4 no-go.

6. **Free absolute solder ORIGIN16 (this PR, Track A2).**
   At the same H1 backgrounds (`p=(2/5)^6` and mixed-sign) with matched
   `b=e0`, `C!=0` and active `I_j`, exact FD in the 16 ORIGIN absolute-solder
   matrix entries yields

      rank B = 0,   rank[B | -g] = 1

   over `Q`, with `g_nonzero = 12` and I-channel response identically zero
   (I-channels are joint-residual scalars of `(links, b)` only).  Certificate
   sections `SECTION_SPAN_OBSTRUCTION_FREE_SOLDER_ORIGIN16` and
   `_MIXED`.  Scope: free ORIGIN absolute solder only; independent of the
   ORIGIN28 link/b obstruction; still not a global F4 no-go.

7. **All-site neighbor ambient + Pi/gauge survival (this PR, Track A2).**
   Exact FD ambient on the five-site neighbor set
   `{ORIGIN} ∪ axis-neighbors` (120 left-Cayley dirs) + 4 free matched-edge
   `b` + 16 free ORIGIN solder (total 140) again gives

      rank B = 4,   rank[B | -g] = 5

   over `Q`.  Adjoining six global Ad-Lorentz gauge-orbit tangents as
   extra canceling columns yields

      rank C = 10,   rank[C | -g] = 11

   so the obstruction **survives** this Pi/gauge enlargement.  Mixed-sign
   background repeats.  Certificate sections
   `SECTION_SPAN_OBSTRUCTION_ALLSITE_NEIGHBOR_PI` and `_MIXED`.
   Scope: neighbor-site ambient (not full 16-site torus) + ORIGIN solder +
   matched `b` + global Ad-Lorentz only; still **not** a chart-independent
   global F4 no-go.

8. **Full 16-site torus ambient + Pi/gauge survival (this PR, Track A3).**
   Exact FD ambient on the full L=2 torus (16 sites x 4 roles x 6 gens =
   384 left-Cayley dirs) + 4 free matched-edge `b` + 16 free ORIGIN solder
   (total 404) at the same H1 backgrounds gives

      rank B = 4,   rank[B | -g] = 5

   over `Q`.  Adjoining six global Ad-Lorentz gauge-orbit tangents yields

      rank C = 10,   rank[C | -g] = 11

   so the obstruction **survives** the full-torus ambient + this Pi/gauge
   enlargement.  Mixed-sign background repeats (`g_nonzero=118`).
   Certificate sections `SECTION_SPAN_OBSTRUCTION_FULL_TORUS16_PI` and
   `_MIXED`.  Cert sha256
   `071f252223065327fd827b1f8c279e349a49bef066ac62055edb83e624d7f253`.
   Scope: full torus link ambient + ORIGIN solder + matched `b`
   + global Ad-Lorentz only; still **not** free-solder-all-sites /
   sitewise-gauge / chart-independent global F4 no-go.

9. **E(2) exactify gate — lean Track B (this PR).**
   Certificate: `a4d_resolved_curved_stationary_e2_exactify_check.py`.
   Over Q: `span{N2,N3,J23}` is an `so(1,3)` Lie subalgebra stabilizing
   null line `n=(1,1,0,0)` with vanishing scale; homogeneous Cayley-E(2)
   4-link plaquettes are exactly parabolic (`tr P=4`, `(P-I)^3=0`) on a
   rational battery (including denom-8/12 scout roundings); memo §5
   13-rational normal-form table packed with declared 14-free / 8+6 split;
   denom-cap `{4,8,12,16,24}` link-only roundings of the §4.1 scout have
   `C!=0` but exact homogeneous star-Euler `||g||^2 != 0` (identity solder),
   confirming §4.2 over Q.  Scope: no exact root; QR pivot assignment of the
   14 transverse unknowns remains numerical provenance.
   **A4 note:** sitewise Ad-Lorentz / all-site free-solder ambient widens
   aborted as too heavy; TORUS16_PI stands as Track A ceiling.

10. **E(2) 14 stationarity polynomials — Track B exactify (this PR).**
   Certificate: `a4d_resolved_curved_stationary_e2_stationarity_polys_check.py`
   (sha256 `9db323bd…84243bb8`; wall ~136s).
   Exact 27-chart = 12 E(2) Cayley + 15 det-one LDU×η; complement
   `{K1,M2,M3}` spans a linear complement of E(2) in `so(1,3)` (joint rank 6).
   Provisional algebraic packing of memo §5 `FIXED_13` into chart slots
   `[0,1,2,3,4,5,6,12..17]` (roles 0–1 E(2) + role2 `n2` + all strict-L);
   free = role2 `{n3,j}` + role3 E(2) + D + U (14).
   Built **14 exact internal** cleared star-stationarity numerators (all
   degree 33) and **6 exact transverse** Lorentz numerators via Cayley
   differential on roles `{0,1}×{K1,M2,M3}` (all degree 23). Selected
   8+6 square subsystem has sample Jac rank 14 at a rational free probe.
   Scope: no exact root; no Groebner; packing is provisional (QR pivots
   unrecovered); four-channel `R=R_*(C)` filter not applied this turn.

11. **E(2) stationarity degree reduction — Track B (this PR).**
   Certificate: `a4d_resolved_curved_stationary_e2_stationarity_deg_reduce_check.py`
   (sha256 `97e8a881…424c379f`; wall ~180s).
   Under the same provisional FIXED_13 packing, raw cleared numerators factor
   exactly as ZZ-content × `(j2²+4)^a (j3²+4)^b d0^c d1^d d2^e` × reduced.
   Internal reduced degrees `[10,12,7,7,9,10,10,11,9,7,4,7,4,4]` (all ≤12);
   transverse reduced degrees `[11,15,15,11,15,15]` (all ≤15). Min internal
   chart powers `(j2²+4)^4 (j3²+4)^4`; min transverse `(j2²+4)^2 (j3²+4)^2`.
   Reduced gens reconstruct raw gens exactly; same open-chart zeros; 8+6
   sample Jac rank 14 retained. Pairwise GCD sample of two reduced internals
   is 1 (no further common factor). Why deg 33: leftover Cayley/LDU denom
   powers after differentiating the rational star density — chart-open units.
   Scope: no exact root; no Groebner; packing still provisional.

12. **E(2) rational specialization D=1, U=0 — Track B (this PR).**
   Certificate: `a4d_resolved_curved_stationary_e2_stationarity_specialize_du1_check.py`
   (sha256 `a73a62ad…12eaaad`; wall ~17s; 39 PASS).
   Under provisional FIXED_13, specialize free solder `D=(1,1,1)`, `U=0` and
   retain five free E(2) coords `(n3_r2, j_r2, n2_r3, n3_r3, j_r3)`.
   Free-internal reduced degrees `[3,5,3,3,5]`; the three n-direction gens
   (`∂S/∂n3_r2`, `∂S/∂n2_r3`, `∂S/∂n3_r3`) are bivariate in `(j_r2, j_r3)` alone
   and have lex Groebner basis `{j_r2+j_r3, j_r3²+4}` over Q. Hence
   `j_r3²+4` lies in the free-internal ideal: every common zero is Cayley
   chart-closed. Open-chart specialized free-internal system: **empty** (over C).
   Scope: slice-only no-go under this D/U specialization + provisional packing;
   not a global E2/F4 no-go; QR pivots still unrecovered; no exact curved root.

13. **E(2) scout-near denser specialization — Track B (this PR).**
   Certificate: `a4d_resolved_curved_stationary_e2_stationarity_specialize_scout_du_check.py`
   (sha256 `b273a8d7…f0ea59`; wall ~19s; 42 PASS).
   Same provisional FIXED_13; specialize free solder to low-denom rationals
   nearer the numerical Cayley-LDU scout:
   `D=(7/5,5/4,4/5)`, `U=(1/6,5/4,-1/10,-3/5,0,-1/5)`
   (scout floats ~`(1.394,1.266,0.793)` / `(0.170,1.265,-0.092,-0.575,0.036,-0.190)`).
   Free-internal reduced degrees again `[3,5,3,3,5]`; n-direction gens again
   bivariate in `(j_r2,j_r3)` with the **same** lex GB `{j_r2+j_r3, j_r3²+4}`.
   Open-chart specialized free-internal system: **empty**. Two distinct D/U
   slices (identity-like and scout-near) both force chart-closed.
   Scope: still slice-only under provisional packing; not global; QR unrecovered.

14. **E(2) gauge-canonical packing replacing provisional FIXED_13 — Track B (this PR).**
   Certificate: `a4d_resolved_curved_stationary_e2_gauge_canonical_packing_check.py`
   (sha256 `db2495d0…ab4762a5`; wall ~3.6s; PASS).
   **QR blocker (documented):** numerical E(2)+LDU chart Jacobian dump
   `J∈R^{m×27}` (`m≥40` full Euler+scale) and column-pivoted QR permutation
   were never persisted (scout json has only link/LDU floats; memo §§5–7
   records FIXED_13 *values* but not pivot slots). Recompute formula recorded
   in the cert: at float root `x*`, `J=DF/Dx`, then
   `scipy.linalg.qr(J, pivoting=True)` → `FREE_IDX=piv[:14]`, `FIXED_IDX=piv[14:]`.
   **Gauge-canonical packing:** same geometric slots
   `[0,1,2,3,4,5,6,12..17]`, but strict-L set to `L≡0` (Iwasawa solder gauge)
   instead of provisional nonzero memo-§5 tail `(4/3,3/2,1/2,2/3,-1/3,-1)`;
   E(2) NF on roles 0–1 + role2 `n2` keeps memo §5 head
   `(-1/3,0,-1/3,1/2,1/2,-1/2,-1/2)`; free = role2 `{n3,j}` + role3 E(2) +
   **D + U** (14) — D/U stay free. Exact rational FD sample at open-chart
   probe: internal Jac rank 14, transverse rank 6, selected 8+6 subsystem
   rank 14. Scope: packing + Jac sample only; no exact root; no Groebner;
   QR pivots still unrecovered.

15. **E(2) gauge-pack scout-near U / D free — Track B (this PR).**
   Certificate: `a4d_resolved_curved_stationary_e2_gauge_pack_scout_u_dfree_check.py`
   (sha256 `1242e15e…826b10`; wall ~12.4s; PASS).
   Under **L≡0** packing, fix scout-near
   `U=(1/6,5/4,-1/10,-3/5,0,-1/5)` and **keep D free** (8 free:
   `e2_r2_{n3,j}+e2_r3_*+D`). Deg-reduced free-internal degrees
   `[6,8,2,2,4,8,8,9]` (raw 23 → chart factors stripped). N-direction gens
   live in `{j_r2,j_r3,d0,d1,d2}`; lex GB contains the factored element
   `d1·(j_r3²+4)`. On the open chart (`d1≠0`) this saturates to `j_r3²+4=0`,
   so every common zero is chart-closed. Open-chart specialized free-internal
   n-projection: **empty**. Does **not** redo FIXED_13 fully-fixed D/U.
   Scope: slice under gauge-canonical packing; not global; QR unrecovered.

16. **E(2) gauge-pack scout-near D / U free — Track B (this PR).**
   Certificate: `a4d_resolved_curved_stationary_e2_gauge_pack_scout_d_ufree_check.py`
   (sha256 `c43327e1…46eac2`; wall ~10.4s; PASS).
   Symmetric slice under **L≡0** packing: fix scout-near
   `D=(7/5,5/4,4/5)` and **keep U free** (11 free:
   `e2_r2_{n3,j}+e2_r3_*+U`). Deg-reduced free-internal degrees
   `[3,5,2,2,4,5,1,0,1,0,3]`. N-direction gens live in
   `{j_r2,j_r3,u01,u23}`; lex GB (U-elim onto j) contains bare
   `j_r3²+4`. Open-chart specialized free-internal n-projection: **empty**
   (chart-closed). Together with item 15, both scout-near one-sided D/U
   slices chart-close under L≡0 + current E(2) NF. Does **not** redo
   FIXED_13 fully-fixed D/U nor the scout-U/D-free cert.
   Scope: slice under gauge-canonical packing; not global; QR unrecovered.

17. **E(2) Jac-QR recompute blocked + lean NF free-E2 — Track B (this PR).**
   Preferred Jac-QR recompute attempted and **honestly blocked**. Dump:
   `a4d_curved_stationary_e2_euler_jac_qr_dump.json` (`NUMERICAL_BLOCKED_HONEST`).
   Homogeneous `star_S` ambient Euler `F∈R^{40}` (24 left-Cayley + 16 raw Θ)
   does **not** vanish at memo §4.1 E(2) links with Cayley-scout LDU, identity
   LDU, or curvature-preserving LDU/joint least_squares refinements;
   chart-critical points still leave `||F_40||` and `||transverse6||` large.
   Memo float witness residual operator / LDU-at-E2-root were never persisted,
   so true `FREE_IDX=piv[:14]` / `FIXED_IDX=piv[14:]` remain unrecovered.
   **Alternate lean NF** certificate:
   `a4d_resolved_curved_stationary_e2_lean_nf_free_e2_check.py`
   (sha256 `c67c531e…fac2025`; wall ~0.22s; PASS). Keeps **L≡0** only
   (FIXED `[12..17]`, 6); **releases** former E(2) NF slots `[0..6]`
   (locked-negative pattern `(-1/3,0,-1/3,1/2,1/2,-1/2,-1/2)` **not** imposed);
   free = all 12 E(2)+D+U (**21**). Float open-chart probe: internal Jac rank
   20, transverse rank 6, selected 8+6 subsystem rank **14**. Subsystem-QR
   candidate FREE chart idx
   `[8,24,2,5,6,7,3,20,21,0,18,19,4,25]` (fixed complement = L≡0 +
   `[10,9,22,23,1,11,26]`). Does **not** grind scout-near one-sided D/U under
   the locked NF. Scope: lean packing + sample Jac + specialize plan; no exact
   root; no Groebner this turn; memo-witness QR still blocked.

18. **E(2) lean-NF identity D/U + subsystem-QR 8-free — Track B (this PR).**
   Certificate: `a4d_resolved_curved_stationary_e2_lean_nf_du1_subqr8_check.py`
   (sha256 `0603cac3…b88826`; wall ~81s; PASS). Under lean **L≡0** + identity
   `D=(1,1,1)`, `U=0`: preferred all-12 E(2) free-internal expand is too heavy
   (~115s/gen, raw deg~71), so adopts documented optional restriction to
   subsystem-QR FREE E(2) indices `[0,2,3,4,5,6,7,8]` with complement E(2)
   `[1,9,10,11]=0` (**not** the locked NF). Free-internal red degs
   `[2,4,2,3,5,4,3,6]`. N-dir and full-8 lex GB force open-chart
   `j_r2=0` and `j_r0=j_r1`; residual locus ideal
   `{n2_r0·j-n2_r1·j+2 n3_r1,
     n2_r0·n3_r2-n2_r1·n3_r2+(j/2)n3_r1 n3_r2+2 n3_r1 n2_r2,
     j² n3_r2+4 j n2_r2-4 n3_r2}`
   is nonempty and does **not** force `j²+4=0` — outcome
   `J_LOCUS_OPEN_CANDIDATE` (contrast locked-NF scout slices that chart-close).
   Scope: algebraic open-chart candidate recorded, not an exact root; full-12
   E(2) eliminate not attempted; Jac-QR still blocked.

19. **E(2) lean-NF DU1/subQR8 locus reconstruction — Track B (this PR).**
   Certificate: `a4d_resolved_curved_stationary_e2_lean_nf_du1_subqr8_locus_recon_check.py`
   (sha256 `df3b34c5…ff0cdf`; wall ~8.0s; PASS). Solves the recorded residual
   3-gen ideal over Q on the open-chart locus `j_r2=0`, `j_r0=j_r1`:
   open `j≠0` branch
   `n3_r1=j*(n2_r1-n2_r0)/2`, `n2_r2=n3_r2*(4-j²)/(4*j)` with free
   `(n2_r0,n2_r1,j,n3_r2)`. Reduced free-internal vanish **identically** on
   this 4-param family. Exact curved witness
   `(n2_r0,n2_r1,n3_r1,j,n2_r2,n3_r2)=(1,0,-1,2,0,0)` (plaquette `(0,1)`
   curv²=8) certifies all **8 ambient** free-internal gens vanish; off-residual
   control (`n3_r1=0`) has ambient `j_r2` cleared residual 2048. Exact
   transverse at witness nonzero (`r0_K1=-6,…,r1_M3=22`) — **not** a full
   8+6 root. Outcome `LOCUS_RECON_FREE_INTERNAL_FAMILY`.

20. **E(2) lean-NF DU1/subQR8 transverse on 4-param family — Track B (this PR).**
   Certificate: `a4d_resolved_curved_stationary_e2_lean_nf_du1_subqr8_transverse_family_check.py`
   (sha256 `a9d12a7c…ee6658`; wall ~1.25s; PASS). Records the 6 transverse
   cleared numerators restricted to the open-chart free-internal family
   `(a,b,jj,ee)=(n2_r0,n2_r1,j,n3_r2)` at degrees `[13,16,11,15,19,19]`
   (content + `jj`/`(jj²+4)` stripped; `GCD_ALL=1`), probe-verified against
   live `dS_transverse`. Flat locus `a=b=ee=0` has all 6 gens identically 0
   and sample curv²=0. Open-chart `a=0` branch forces `ee=0` then `b=0`
   (flat only); cheap slice `b=ee=0` lex GB forces `a=0` (flat only). Curved
   `a≠0` branch: ee-resultant residual `H(a,b,jj)` deg ~26; pairwise gcd of
   stripped multi-resultants = 1; full multi-var Groebner exceeds the minutes
   wall — honest BLOCKER. Outcome
   `TRANSVERSE_ON_4PARAM_FLAT_OK_CURVED_GB_BLOCKED`. **Not** a curved 8+6
   root; **not** an open-chart curved transverse-empty theorem.

21. **E(2) lean-NF DU1/subQR8 transverse family Newton — Track B (this PR).**
   Certificate: `a4d_resolved_curved_stationary_e2_lean_nf_du1_subqr8_transverse_family_newton_check.py`
   (sha256 `651bbdc5…e1fa1a`; wall ~3.0s; PASS). Float Gauss-Newton /
   `scipy.optimize.least_squares` on the recorded 6 transverse cleared gens
   over the 4-param family `(a,b,jj,ee)`, from the curved free-internal witness
   `(1,0,2,0)` [= 6-tuple `(1,0,-1,2,0,0)`] and 11 other curved seeds. **No
   curved float root:** all near-zero Newton hits (`nf < 1e-6`, 10/12 seeds)
   collapse to the flat locus `a≈b≈ee≈0` (open `jj`); best curved residual
   stays `||trans||_2 ≈ 9.55` (bound-limited). Exact rational nearby + fixed-`j`/`a=1`
   small-Q grid + univariate-in-`ee` slices (gcd deg 0 / no common root) find
   **no** curved rational transverse zero. Live `dS_transverse` at witness
   matches locus_recon (`r0_K1=-6,…,r1_M3=22`). No multi-var GB / resultant
   chain. Outcome `TRANSVERSE_NEWTON_NO_CURVED_ROOT_COLLAPSE_TO_FLAT`.

22. **2D Cayley subtangent warning.**
   In a 2-parameter subchart, ambient dim=2 makes `in_span` automatic whenever
   `rankB=2`.  That does **not** certify a root; the 6D test is the load-bearing one.

### EXACT/CERTIFIED -- homogeneous word no-gos (this PR, parallel packet)

Certificate: `a4d_homogeneous_curved_stationary_controls_check.py`.

Five explicit rational homogeneous word backgrounds (including the two generic
quotient-complete joint-holonomy controls) have **no** nondegenerate full
star-stationary point.  Useful negative controls; they do not exhaust the
homogeneous four-link sector.

### NUMERICAL/EXPLORATORY -- NOT A THEOREM (parallel scout)

Certificates:
`a4d_curved_stationary_cayley_scout_candidate.json` (+ scout narrative below).

Broad homogeneous four-link / Cayley-LDU scouts find nonflat candidates with
tiny raw Euler residual, `det Theta = -1`, and apparent Hessian rank ~20 /
nullity ~19.  Compatible with the word no-gos (survivors lie outside those
words).  **Must not** be promoted before exact rational reconstruction.

### CURRENT STRONGEST STABLE STATEMENT

    BOXED:
    F4-SUPPORT-OBSTRUCTION-ON-R-EQUALS-ZERO;
    RESPONSE-MATRIX-RANK-4-KER-0-ADJ-OPP-INDEPENDENT;
    SCOPED-6D-CAYLEY-SPAN-OBSTRUCTION-RANK-B-4-LT-AUG-5-ON-5-POINT-RATIONAL-GRID;
    SCOPED-AMBIENT-ORIGIN28-SPAN-OBSTRUCTION-RANK-B-4-LT-AUG-5-AT-TWO-RATIONAL-BACKGROUNDS;
    SCOPED-FREE-SOLDER-ORIGIN16-SPAN-OBSTRUCTION-RANK-B-0-LT-AUG-1-I-BLIND-AT-TWO-BACKGROUNDS;
    SCOPED-ALLSITE-NEIGHBOR-PI-SPAN-OBSTRUCTION-RANK-B-4-LT-AUG-5-AND-GAUGE-SURVIVAL-RANK-C-10-LT-CAUG-11;
    SCOPED-FULL-TORUS16-PI-SPAN-OBSTRUCTION-RANK-B-4-LT-AUG-5-AND-GAUGE-SURVIVAL-RANK-C-10-LT-CAUG-11;
    E2-LIE-ALGEBRA-AND-NULL-STABILIZER-OVER-Q;
    E2-HOMOGENEOUS-PLAQUETTES-EXACTLY-PARABOLIC-ON-RATIONAL-BATTERY;
    E2-NORMAL-FORM-13-FIXED-14-FREE-INTERFACE-PACKED;
    E2-DENOM-CAP-LINK-ROUNDING-STAR-RESIDUAL-EXACT-NONZERO;
    E2-STATIONARITY-POLYS-14-INTERNAL-DEG33-PLUS-6-TRANSVERSE-DEG23;
    E2-8P6-SUBSYSTEM-SAMPLE-JAC-RANK-14-UNDER-PROVISIONAL-PACKING;
    E2-STATIONARITY-DEG-REDUCE-INTERNAL-LE12-TRANSVERSE-LE15-CHART-OPEN;
    E2-STATIONARITY-SPEC-D1-U0-FREE-INTERNAL-FORCES-CHART-CLOSED;
    E2-STATIONARITY-SPEC-SCOUT-DU-FREE-INTERNAL-FORCES-CHART-CLOSED;
    E2-GAUGE-CANONICAL-PACKING-L-ZERO-8P6-SAMPLE-JAC-RANK-14;
    E2-GAUGE-PACK-SCOUT-U-DFREE-FORCES-CHART-CLOSED;
    E2-GAUGE-PACK-SCOUT-D-UFREE-FORCES-CHART-CLOSED;
    E2-QR-PIVOT-RECOVERY-BLOCKED-MISSING-JAC-DUMP;
    E2-JAC-QR-RECOMPUTE-BLOCKED-STAR-S-AMBIENT-MISMATCH;
    E2-LEAN-NF-L-ZERO-ONLY-FREE-E2-8P6-SAMPLE-JAC-RANK-14;
    E2-LEAN-NF-DU1-SUBQR8-OPEN-CHART-J-LOCUS-CANDIDATE;
    E2-LEAN-NF-DU1-SUBQR8-LOCUS-RECON-FREE-INTERNAL-FAMILY;
    E2-TRANSVERSE-ON-4PARAM-FLAT-LOCUS-OK-CURVED-BRANCH-GB-BLOCKED;
    E2-TRANSVERSE-NEWTON-NO-CURVED-ROOT-COLLAPSE-TO-FLAT

Supporting:

    BOXED:
    ONE-BOOST-CONSTANT-AND-X0-SLICES-DEGENERATE;
    HOMOGENEOUS-WORD-CONTROLS-NO-NONDEGENERATE-STATIONARY-POINT

No exact nondegenerate four-channel curved root claimed.
No continuum Einstein claim.

### SINGLE NEXT BLOCKER

**Primary (Track B):** transverse gens on the 4-param free-internal family are
recorded; flat locus / `a=0` / `b=ee=0` force flat only; curved GB-blocked.
**Newton wave** (cert `…transverse_family_newton_check.py`, ~3.0s): 12 curved
seeds → **no curved float root**; near-zero hits collapse to flat
`a≈b≈ee≈0`; best curved `||trans||_2 ≈ 9.55`; no exact rational curved
transverse zero on nearby/grid/univariate slices. Next: either accept
**flat-only transverse locus** under this 4-param free-internal family and
**escalate packing** (subsystem-QR complement / lean NF / other open-chart
parametrization), OR try further univariate deg≤4 specializations only —
**still forbid** blind multi-var GB / deg-26 resultant chains. Full-12 E(2)
eliminate remains too heavy. Jac-QR still blocked. Do **not** re-impose
locked E(2) NF. Still avoid blind 14-var / deg-33 Groebner. Filter by
four-channel `R=R_*(C)` only if a full 8+6 point appears.

**Track A (parked):** TORUS16_PI is the current ambient ceiling.  Sitewise
Ad-Lorentz / all-site free-solder widens were **aborted** this turn as too heavy
(sympy ambient/rank cost beyond a manageable validation budget).  Do not restart
A4 ambient FD unless a structured sampling plan keeps validation in minutes.

Do **not** restart from `(a,b)` tuning or from forcing `R=0`.

---

## 1. Research question (F4)

Does there exist a nondegenerate finite configuration with nonzero curvature
that is stationary for some `c in Q^4` in

    S = S_star
      + c_eta_adj I^eta_adj + c_eta_opp I^eta_opp
      + c_n_adj I^n_adj + c_n_opp I^n_opp ?

H1 picture: residual tracks curvature, `R_*(0)=0`, `R_*(C)!=0` at finite curve.
L=2 may discover; L=3 hostile control required before broad finite-carrier
claim.

---

## 2. Relation to star-only Crit search

On quotient-complete strata the #201 stationary-auxiliary theorem says physical
crit of `S_star+Q` match physical crit of `S_star` after gauge.  That justifies
star Euler searches as a **necessary** filter.  It does **not** justify
collapsing the four I-channels to a single `(a,b)` modulus, nor forcing `R=0`
as the geometry ansatz.  Coefficient independence is settled by `rank M=4`,
`ker M=0`.

---

## 3. Validation

```bash
python3 02_REGISTRY/research/certificates/a4d_resolved_curved_stationary_f4_check.py
python3 02_REGISTRY/research/certificates/a4d_resolved_curved_stationary_e2_exactify_check.py
python3 02_REGISTRY/research/certificates/a4d_resolved_curved_stationary_e2_stationarity_polys_check.py
python3 02_REGISTRY/research/certificates/a4d_resolved_curved_stationary_e2_stationarity_deg_reduce_check.py
python3 02_REGISTRY/research/certificates/a4d_resolved_curved_stationary_e2_stationarity_specialize_du1_check.py
python3 02_REGISTRY/research/certificates/a4d_resolved_curved_stationary_e2_stationarity_specialize_scout_du_check.py
python3 02_REGISTRY/research/certificates/a4d_resolved_curved_stationary_e2_gauge_canonical_packing_check.py
python3 02_REGISTRY/research/certificates/a4d_resolved_curved_stationary_e2_gauge_pack_scout_u_dfree_check.py
python3 02_REGISTRY/research/certificates/a4d_resolved_curved_stationary_e2_gauge_pack_scout_d_ufree_check.py
python3 02_REGISTRY/research/certificates/a4d_resolved_curved_stationary_e2_lean_nf_free_e2_check.py
python3 02_REGISTRY/research/certificates/a4d_resolved_curved_stationary_e2_lean_nf_du1_subqr8_check.py
python3 02_REGISTRY/research/certificates/a4d_resolved_curved_stationary_e2_lean_nf_du1_subqr8_locus_recon_check.py
python3 02_REGISTRY/research/certificates/a4d_resolved_curved_stationary_e2_lean_nf_du1_subqr8_transverse_family_check.py
python3 02_REGISTRY/research/certificates/a4d_homogeneous_curved_stationary_controls_check.py
python3 tools/validate_work.py
python3 tools/validate_repo.py
```

---

## 4. Handoff

Draft PR #202.  Do not merge.  Continue: span search with `R!=0`, then exact
root or scoped no-go, then L=3 before Ready.


## 4. NUMERICAL/STRUCTURAL — minimal parabolic mechanism isolated

The Cayley/LDU candidate has an additional highly non-generic structure.

Stacking the six matrices (P_{rs}-I) reveals a common one-dimensional kernel.
Its generator is null with respect to (eta). After one global proper-Lorentz
gauge rotation this line is the canonical

[
n=(1,1,0,0).
]

In that gauge every link lies, to numerical precision (<10^{-14}), in the
four-dimensional null-line stabilizer (SIM(2)). In standard Lorentz-algebra
coordinates

[
(K_1,K_2,K_3,J_{12},J_{13},J_{23}),
]

each link satisfies

[
(a,b,c,b,c,d),
]

so the two combinations (K_2+J_{12}) and (K_3+J_{13}) are the null
translations.

Consequently every plaquette commutator is parabolic:

[
operatorname{tr}P_{rs}=4,
qquad
det(I-P_{rs})approx0,
qquad
(P_{rs}-I)^3approx0,
]

and both Lorentz bivector invariants of the odd curvature vanish numerically.

This explains why the roots are absent from the generic
(det(I-P)
e0) controls used for quotient-completeness: they live on a
separate parabolic curvature stratum.

### 4.1 Minimal subgroup scan

A full-Euler scan was repeated after restricting each link to subgroups of
(SIM(2)).

- one-parameter sectors: only flat roots;
- all tested two-parameter sectors: only flat roots;
- (K_1+N_2+N_3) (scale plus two null translations): curved roots survive;
- (N_2+N_3+J_{23}), i.e. the exact little group (E(2)) with no null-line
  scale: curved roots survive.

For the (E(2)) three-parameter-per-link sector, a representative root has

[
|mathrm{EL}_{
m full}|_2=4.29	imes10^{-14},
qquad
|C|_{
m scout}=0.34535,
]

with (detTheta=-1) and
(sigma_{min}(Theta)=0.2713).

Thus the first numerically surviving homogeneous class needs only

[
4	imes3+15=27
]

det-fixed chart variables, not the original 39.

A representative (E(2)) link coordinate set
((N_2,N_3,J_{23})) is

```text
[ 0.088504652044,  0.082911143621, -0.249807924819]
[-0.320461257769, -0.081035776131, -0.303588032463]
[-0.322033101871, -0.137571575304,  0.125148917575]
[ 0.287012659188,  0.226439735406, -0.295275453655]
```

### 4.2 Failed over-simplification control

Fixing all twelve (E(2)) link coordinates to nearby low-denominator rationals
and solving only for the solder does **not** preserve stationarity: the best
tested rounded controls stall at full residual of order (10^{-2}).

Therefore the exact witness cannot be obtained by independently rounding the
links while repairing only the solder. Exact reconstruction must move both
sectors along the stationary manifold.

### Revised exactification target

Work entirely inside the (E(2)) little-group chart. Derive the exact rational
stationary equations there, compute their generic Jacobian rank, and use the
remaining free dimensions to impose rational gauge/normal-form conditions
before elimination.

This is now the smallest observed positive F4 carrier.


## 5. NUMERICAL/STRUCTURAL — 13 rational free coordinates leave a 14-equation transverse system

At the representative (E(2)) curved root, the Jacobian of the **full**
40-component Euler+scale residual with respect to the 27 (E(2))+LDU chart
variables has numerical rank

[
oxed{operatorname{rank}J=14},
qquad
oxed{operatorname{nullity}=13}.
]

Thus exactification can be organized as a square transverse solve rather than a
27-variable blind reconstruction.

A rank-revealing QR decomposition selects 14 pivot variables. The remaining 13
coordinates were fixed to the following low-denominator rationals:

[
-rac13, 0, -rac13, rac12, rac12, -rac12, -rac12, 
rac43, rac32, rac12, rac23, -rac13, -1.
]

Solving only the 14 transverse equations then returns a full residual

[
|mathrm{EL}|_2=5.30	imes10^{-14}.
]

The same construction remains stable for several other denominator caps
(4, 8, 12, 16, 24, 32), always returning residuals of order (10^{-13}) or
better. This is strong numerical evidence that the stationary locus is a
genuine positive-dimensional rational-algebraic variety in the (E(2)) chart,
not a fine-tuned isolated floating-point root.

### Exact next step

The exact problem is now reduced to:

- 13 free coordinates fixed rationally as above;
- 14 unknown transverse coordinates;
- 14 independent rational stationarity equations.

The next certificate should derive those fourteen equations symbolically and
perform exact elimination / algebraic-number reconstruction. This is the
smallest current exactification system.


## 6. NUMERICAL/CERTIFICATION SCOUT — literal periodic single-site/single-edge Euler check

The homogeneous search was subjected to a stronger hostile control: evaluate the
literal (L=2) periodic action and vary only one physical degree of freedom at
a time, rather than varying all translation-equivalent copies together.

For the representative (E(2)) curved candidate:

- one origin-site solder matrix was varied in all 16 raw components;
- one origin edge of each Role was varied independently in all six Lorentz
  tangent directions;
- all other periodic edges/sites were held fixed.

The resulting local Euler norms are

[
|E_Theta(x_0)|_2=7.68	imes10^{-16},
]

and, for the four origin edges,

[
8.70	imes10^{-16},quad
1.36	imes10^{-15},quad
1.73	imes10^{-15},quad
1.39	imes10^{-15}.
]

Thus the numerical root is not merely stationary under homogeneous collective
variations. It passes the literal single-site and single-edge periodic Euler
test to machine precision.

This remains NUMERICAL/EXPLORATORY because the link/solder coordinates have not
yet been algebraically reconstructed. But the remaining blocker is now purely
exactification, not a hidden local-Euler failure.


## 7. NUMERICAL/STRUCTURAL — 14 transverse conditions split as 8 internal + 6 external

At the same (E(2)) root, the Hessian of the action restricted to the
27-dimensional (E(2)+LDU) chart has numerical rank

[
oxed{8}.
]

The Jacobian of the literal full Euler residual restricted to those 27
variables has rank 14. Therefore only six additional independent conditions
come from Lorentz variations transverse to the (E(2)) little-group
subalgebra:

[
oxed{14=8_{
m internal}+6_{
m transverse}.}
]

This gives a cleaner symbolic attack:

1. derive the eight independent stationary equations of the rational
   (E(2))-restricted action;
2. derive six independent transverse Lorentz Euler equations;
3. impose the thirteen rational normal-form coordinates from §5;
4. solve the resulting fourteen-equation square transverse system.

This replaces the original forty-component Euler system by a structured
(8+6) exact problem.