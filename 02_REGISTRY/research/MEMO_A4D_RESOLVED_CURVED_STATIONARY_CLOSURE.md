# MEMO A4D -- resolved curved stationary closure (F4 / lower wall)

**Task:** `EXP-A4D-RESOLVED-CURVED-STATIONARY-CLOSURE`
**Execution:** PR #202
**Status:** IN_PROGRESS / durable checkpoint (restructured F4 attack)
**Baseline:** `cf18bb1d51d5b86819638fea03eadeb1fab360fa`

## 0A. CORRECTIVE FULL-EULER AUDIT (2026-09-26)

This section supersedes the full-stationarity interpretation in §§23-24 and
corrects the stale PR #202 handoff. The historical files remain in the tree.

The displayed role matrix `e2_closed(n2,n3,j)` is the Cayley transform of

\[
n_2 M_2+n_3 M_3-jJ_{23},
\]

not of `n2*N2+n3*N3+j*J23` used by the old `e2_alg` differential. Consequently
the old transverse routine differentiated a different Cayley base from the
matrix being evaluated. Its advertised Roles 2/3 values
`(-32,-16,32)` and `(32,0,-16)` at `(j,gamma,delta)=(2,0,1)` reproduce only
under that mismatched base and are not Euler derivatives of the stored family.
The old six symbolic rows used `M2,M3`, which are tangent to the subgroup
actually represented by `e2_closed`; the proper complement is `{K1,N2,N3}`.

The new exact certificate
`a4d_resolved_curved_stationary_e2_enlarged12_full_transverse_check.py`
(sha256 `118bb147c929791a5c208f30bc6e829e0d596ad15deece9ecbe57e6aa336d432`,
~40.2 s; PASS)
checks the Cayley convention, the rank-six Lie basis, all 12 internal
`{M2,M3,-J23}` derivatives, and all 12 true complement derivatives on all four
roles. It uses analytic rational directional derivatives, no finite
differences. Only the Cayley denominator `j^2+4` is removed; it is positive
for real `j`.

At the former witness the true complement vectors in basis `{K1,N2,N3}` are

| Role | Exact Euler vector |
|---|---|
| 0 | `(0,-16,0)` |
| 1 | `(0,16,0)` |
| 2 | `(0,-32,64)` |
| 3 | `(0,0,-32)` |

The role-2/3 numerator equations include

\[
\gamma(j^2+4)-2j^2=0,\quad
\gamma(j^2+4)+2j^2=0,
\]

\[
\delta(j^2+4)+4j=0,\quad
\delta(j^2+4)-4j=0.
\]

Their exact sums/differences force `j=gamma=delta=0` over the reals. The
other 12 internal derivatives vanish identically, and all 24 link derivatives
vanish at the origin. Thus the matrix-defined homogeneous parabolic family has
no curved full-star stationary point. The formula

\[
S_\star=0,\qquad
\mathrm{curv}^2=rac{64j^2(\gamma^2+\delta^2)}{j^2+4}
\]

still holds as an action/curvature evaluation. Its flat configuration line
`gamma=delta=0` is not a critical manifold: Role 2 in direction `N3` has
Euler derivative `128j/(j^2+4)`, so only `j=0` is critical on that line.

The matched-`b` certificate remains valid: on this homogeneous parabolic
family `R=0` for arbitrary matched affine translations, so every quadratic
channel `I=R^T H R` also has zero first variation there. No choice of the four
channel coefficients repairs the full-star obstruction on this sheet. This
is scoped to the matrix-defined homogeneous parabolic family; it is not a
global no-go on the full configuration space.

Cross-wall consequence: within this sheet there is no nontrivial zero-source
stationary germ accumulating on its flat configurations. This is a positive
control for #216, not a claim about other charts, other strata, or the full
physical quotient.

## 0B. RESUME CHECKPOINT -- durable state

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

22. **E(2) lean-NF DU1 enlarged-12 free Newton — Track B (this PR).**
   Certificate: `a4d_resolved_curved_stationary_e2_lean_nf_du1_enlarged12_newton_check.py`
   (sha256 `8124ee5d…7c0e34`; wall ~5.6s; PASS). Under lean L≡0 + `D=(1,1,1)`,
   `U=0`, **FREE all 12 E(2)** (former subQR8 complement `[1,9,10,11]` released).
   Float Gauss-Newton on free-internal FD grad (12) + transverse (6) from 10
   curved seeds. **Curved float candidates appear:** all 10 seeds reach
   `||res||_2 ≲ 1e-8` with open chart; **7/10** strongly curved (`curv²≥0.5`);
   best strong `witness_comp0` `||res||_2≈3.34e-9`, `curv²≈1.70`. All near-zero
   hits share the float locus pattern
   `e2≈(α,β,j, α,β,j, γ,δ,0, δ,-γ,0)` (r0≡r1, `j_r2=j_r3=0`,
   `n2_r3=n3_r2`, `n3_r3=-n2_r2`); former complement slots are active
   (`||comp||≈0.21` at probe). Optional rational smoke (den≤32) finds **no**
   clear near-rational vanishing (`res` down to ~0.018). No multi-var GB.
   Outcome `CURVED_FLOAT_CANDIDATE_UNDER_ENLARGED_PACKING`.
   **Not** an exact root; float not promoted without rational vanishing.

23. **Historical E(2) lean-NF DU1 enlarged-12 pattern exactify — partial / superseded as full stationarity.**
   Original certificate: `a4d_resolved_curved_stationary_e2_lean_nf_du1_enlarged12_pattern_exactify_check.py`
   (sha256 `98952399…f67e95`). It correctly evaluates the displayed
   `e2_closed` family, `S_star=0`, curvature, and the six symbolic derivatives
   it implemented. However its derivative base used `e2_alg=N2,N3,+J23`, while
   `e2_closed` is Cayley of `M2,M3,-J23`; the six checked directions were not
   the family’s Lorentz complement. The former exact witness and float scout
   remain historical computations, but the outcome
   `EXACT_CURVED_FAMILY_UNDER_ENLARGED12_PATTERN` is withdrawn as a full
   stationary-family claim. No multi-variable elimination was done there.

24. **Historical enlarged-12 classical 8+6 / R★ filter — partial / superseded as full stationarity.**
   Original certificate: `a4d_resolved_curved_stationary_e2_lean_nf_du1_enlarged12_classical_8p6_check.py`
   (sha256 `404789dd…c00f04`). Its finite-difference internal battery and
   complement subset inherit the convention mismatch above; it does not prove
   a full classical 8+6 stationary family. The exact coordinate/witness,
   curvature, and `b=0` residual values remain useful evaluations. Its outcome
   `CLASSICAL_8P6_CURVED_FAMILY_RSTAR_DORMANT` is superseded as a stationarity
   claim by §0B.

25. **Matched-b residual dormancy on the matrix-defined parabolic family — retained, re-scoped.**
   Certificate: `a4d_resolved_curved_stationary_e2_lean_nf_du1_enlarged12_matched_b_r_activate_check.py`
   (sha256 `fb9cdb32…55771f`). On the displayed family every plaquette is
   parabolic, curved faces have `adj(I-P)=0`, and `R=0` for arbitrary matched
   affine `b`; the four quadratic `I` channels are therefore first-order blind
   on the sheet. The positive F4 control still activates `R` off this stratum.
   Retain this structural result; do not attempt to activate a channel on the
   killed family and do not promote it to a global affine no-go.

26. **2D Cayley subtangent warning.**
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
    E2-TRANSVERSE-NEWTON-NO-CURVED-ROOT-COLLAPSE-TO-FLAT;
    E2-ENLARGED12-NEWTON-CURVED-FLOAT-CANDIDATE;
    E2-HOMOGENEOUS-PARABOLIC-MATCHED-B-RESIDUAL-BLIND;
    E2-ENLARGED12-FULL-EL-ONLY-FLAT-ORIGIN-ON-MATRIX-DEFINED-SHEET

Supporting:

    BOXED:
    ONE-BOOST-CONSTANT-AND-X0-SLICES-DEGENERATE;
    HOMOGENEOUS-WORD-CONTROLS-NO-NONDEGENERATE-STATIONARY-POINT

No exact nondegenerate four-channel curved root claimed.
No continuum Einstein claim.

### SINGLE NEXT BLOCKER

**Primary (Track B):** the corrected exact audit rules out every curved full-star stationary point on the matrix-defined homogeneous parabolic family. Matched/arbitrary affine `b` remains residual-blind there (`R=0`, `adj(I-P)=0` on curved faces), so active four-channel coefficients cannot repair that sheet. **Next:** use a controlled deformation leaving the sheet. Before nonlinear solving, compute the missing-Euler Jacobian and the same directions' first variation of `det(I-P)` / `adj(I-P)` or `R`; reject directions that cannot affect both gates. Start with the smallest stabilizer dilation, then only widen if rank-two parabolicity persists. No 27-/39-variable search, no Newton promotion, no channel activation attempt on the killed sheet. L=3 hostile remains required for any broader terminal.

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
python3 02_REGISTRY/research/certificates/a4d_resolved_curved_stationary_e2_lean_nf_du1_subqr8_transverse_family_newton_check.py
python3 02_REGISTRY/research/certificates/a4d_resolved_curved_stationary_e2_lean_nf_du1_enlarged12_newton_check.py
python3 02_REGISTRY/research/certificates/a4d_resolved_curved_stationary_e2_enlarged12_full_transverse_check.py
python3 02_REGISTRY/research/certificates/a4d_resolved_curved_stationary_e2_controlled_normal_gate_check.py
python3 02_REGISTRY/research/certificates/a4d_resolved_curved_stationary_e2_lean_nf_du1_enlarged12_pattern_exactify_check.py
python3 02_REGISTRY/research/certificates/a4d_resolved_curved_stationary_e2_lean_nf_du1_enlarged12_classical_8p6_check.py
python3 02_REGISTRY/research/certificates/a4d_resolved_curved_stationary_e2_lean_nf_du1_enlarged12_matched_b_r_activate_check.py
python3 02_REGISTRY/research/certificates/a4d_homogeneous_curved_stationary_controls_check.py
python3 tools/validate_work.py
python3 tools/validate_repo.py
```

---

## 4. Handoff

Draft PR #202. Do not merge. The matrix-defined homogeneous parabolic family
is exactly full-EL obstructed away from the flat origin, and matched-b residuals
are blind on this sheet. The `K1` dilation fails the exact rank gates. The
outside-`SIM(2)` normal gate passes, but only at the first-order level; exact
nonlinear active-residual full stationarity remains open. Do not mark Ready.
L=3 remains required for a broader terminal after an exact L=2 witness exists.


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

---

## 8. EXACT / CROSS-WALL — rank-adapted affine quotient coordinate

The parabolic rank-two seam admits a canonical fixed-rank quotient coordinate.
For one affine holonomy

\[
H=(P,t),\qquad M=I-P,\qquad \operatorname{rank}M=r,
\]

define

\[
\boxed{
\Psi_r(M,t):
\omega\longmapsto
t\wedge(\Lambda^rM)\omega.
}
\]

On the rank-\(r\) stratum:

\[
\Psi_r(M,t+Mc)=\Psi_r(M,t),
\]

and under \(M'=gMg^{-1}\), \(t'=gt+M'c\),

\[
\Psi_r(M',t')
=
(\Lambda^{r+1}g)\Psi_r(M,t)(\Lambda^rg^{-1}).
\]

Since \(\operatorname{im}\Lambda^rM=\Lambda^r\operatorname{im}M\) is a
nonzero line,

\[
\boxed{
\Psi_r(M,t)=0
\iff
t\in\operatorname{im}M,
}
\]

and in fact

\[
\boxed{
\Psi_r(M,t)=\Psi_r(M,t')
\iff
t-t'\in\operatorname{im}M.
}
\]

Thus \(\Psi_r\) is a complete tensor coordinate of the affine cokernel class
on a fixed-rank stratum.  In \(4D\), the old adjugate/cofactor residual is the
\(r=3\) Hodge-dual member of this hierarchy; on the parabolic rank-two seam the
correct surviving object is \(\Psi_2\).

For a null rotation \(P=e^N\), \(N=n\wedge m\),

\[
\Pi=\operatorname{im}(I-P),
\qquad
\ell=\operatorname{im}(I-P)^2,
\]

and

\[
\boxed{
\ell=\operatorname{rad}\Pi=\Pi\cap\Pi^\perp.
}
\]

Hence the projective top nonzero compound

\[
[\Lambda^2(I-P)]
\]

already records the degenerate plane and therefore its null flag.  This is the
rank-two analogue of the existing graph-closure/top-nonzero-compound
architecture.

**Scope:** this is a rank-stratified quotient diagnostic/resolution coordinate,
not a new action term and not a new \(I\)-channel.  It need not remain
translation invariant if used with the wrong exterior degree on a higher-rank
stratum.

---

## 9. Exact enlarged family: corrected finite-vacuum and cross-wall status

The matrix-defined family is

\[
\boxed{\ne_2=
(0,0,j,\;
 0,0,j,\;
 \gamma,\delta,0,\;
 \delta,-\gamma,0)
}
\]

under lean \(L\equiv0\), \(D=(1,1,1)\), \(U=0\). Its exact action and
curvature evaluations are

\[
S_\star=0,\qquad
\mathrm{curv}^2=\frac{64j^2(\gamma^2+\delta^2)}{j^2+4}.
\]

The older advertised transverse rows were computed with a Cayley generator
that does not generate these role matrices. The corrected certificate uses the
actual subgroup \(\operatorname{span}\{M_2,M_3,-J_{23}\}\), its complement
\(\{K_1,N_2,N_3\}\), and exact analytic derivatives on all four roles.
The full-star Euler zero-set on this three-parameter sheet is only
\((j,\gamma,\delta)=(0,0,0)\). Thus there is no curved star stationary member
on the sheet. Since the parabolic matched-\(b\) result gives \(R=0\) for
arbitrary affine translations, every quadratic channel has zero first
variation on the sheet as well; the selected four-channel action cannot
restore a curved root here.

### 9.1 Lower-wall finite vacuum

The exact homogeneous parabolic sheet is killed. Do not search for
\(R=R_\ast(C)\ne0\) on it. The remaining finite-vacuum objective is a
controlled deformation that leaves this sheet while simultaneously affecting
(i) the true missing Euler equations and (ii) residual blindness. Before any
solve, calculate the deformation-direction Jacobian rank for both gates.

### 9.2 Cross-wall flat accumulation

The coordinate line \(\gamma=\delta=0\) is flat by the curvature formula, but
it is not a critical manifold: the exact Role-2 \(N_3\) derivative is
\(128j/(j^2+4)\). The full stationary set on this sheet is the origin, which
is itself flat. Hence no nontrivial zero-source stationary germ on this sheet
accumulates on its flat locus. This is positive control for the upper \(J^2\)
isolation question in #216; it does not classify other charts or the full
physical quotient.

### 9.3 Controlled normal deformation: exact first-order gates

At the former witness `(j,gamma,delta)=(2,0,1)`, the exact eight-component
missing Euler vector in order `(role 0 N2,N3, ..., role 3 N2,N3)` is

```text
(-16, 0, 16, 0, -32, 64, 0, -32).
```

The new exact directional certificate
`a4d_resolved_curved_stationary_e2_controlled_normal_gate_check.py`
tests the twelve role-local directions `{K1,N2,N3}`. On each of the four
curved faces `(0,2),(0,3),(1,2),(1,3)`, it differentiates both
`det(I-P)` and `adj(I-P)` exactly. `K1` is the null-line dilation in the
current `SIM(2)` stabilizer: its four Euler columns have rank 4, but adding
the base defect raises the rank to 5, and every tested first variation of the
adjugate is zero. This candidate therefore fails both parts of the gate.

The outside-`SIM(2)` directions pass the combined first-order gate. The only
residual-active columns are `N2` on role 2 and `N3` on role 3; their
adjugate-derivative matrices have rank 2 on faces `(0,2),(1,2)` and
`(0,3),(1,3)`, respectively. All twelve determinant derivatives remain
zero. The full missing-Euler Jacobian has rank 8 and its augmented rank with
the base defect is also 8. The minimum support containing an adjugate-active
column has size 7 (eight such supports); one exact linearized correction is
on `(K1_0,K1_1,N2_0,N2_2,N2_3,N3_0,N3_1)` with coefficients

```text
(-166/67, -2, 76/67, 40/67, -124/67, 42/67, -102/67).
```

This is an exact first-order solution of the eight missing equations, not a
finite stationary configuration. Its order-one coefficients do not establish
a small branch or solve the remaining internal Euler equations. No exact
active-residual full-Euler witness has been reconstructed, and the L=3 hostile
control has not been run. Those remain open; the present scoped parabolic
no-go is not extended to the deformed carrier.

### 9.4 Exact audit of the proposed small-branch parameterization

The controlled-normal certificate now lists all eight minimum size-seven
supports. Exactly one contains both cofactor-active columns `N2@Role2` and
`N3@Role3`, so it uniquely gives first-order adjugate activation on all four
curved faces. The exact support-specific calculation is
`a4d_resolved_curved_stationary_e2_support7_order1_check.py`.

For the base generators

```text
A0(0) = A1(0) = -2 J23,  A2(0) = M3,  A3(0) = M2,
```

the selected support and the unique correction solving the eight-dimensional
linearized defect equation are

```text
(K1_0, K1_2, N2_2, N3_0, N3_1, N3_2, N3_3)
(-346/13, -22/13, -609/26, 58/13, 311/13, -24/13, -11/26).
```

The exact group path is `U_r(epsilon)=Cayley(A_r(epsilon))`, where

```text
A0(epsilon) = -2 J23 + epsilon*(-346/13 K1 + 58/13 N3)
A1(epsilon) = -2 J23 + epsilon*(311/13 N3)
A2(epsilon) = M3 + epsilon*(-22/13 K1 - 609/26 N2 - 24/13 N3)
A3(epsilon) = M2 - epsilon*(11/26 N3).
```

The exact missing-Euler Jacobian is `8x7`, rank 7 with zero kernel. But the
base point `(j,gamma,delta)=(2,0,1)` is not stationary. In test order
`(M2,M3,-J23,K1,N2,N3)` per role, its Euler constant term is

```text
Role 0: (0,0,0,0,-16,0)
Role 1: (0,0,0,0,16,0)
Role 2: (0,0,0,0,-32,64)
Role 3: (0,0,0,0,0,-32).
```

Consequently the actual Taylor expansion along this path is
`E(epsilon)=E0+epsilon*Jv+O(epsilon^2)` with `E0 != 0`. The equation
`J_missing*v=-E0_missing` is a Newton correction for a unit step; it is not a
formal-branch solvability equation for `x(epsilon)=epsilon*v+epsilon^2*w+...`.
The full exact `Jv` is printed by the certificate. This calculation therefore
does not kill a nonlinear branch or settle existence of another stationary
point on the support.

As a separate exact point check, the unit Newton displacement stays inside the
Cayley charts but its finite link configuration has all 24 star link Euler
components nonzero at `b=0`; it is not itself a stationary witness. This tests
only that one finite iterate.

Along the infinitesimal path, the first determinant derivative is zero on all
four curved faces and each first adjugate derivative has rank 2. This is
cofactor activation only. No affine translation jet was supplied, so there is
no claim that `R != 0`, that `R=R_*(C)` is solved, or that a four-channel
stationary point exists.

The small-branch question needs a genuinely stationary base point or an
explicit parameterization that scales the base defect consistently. The next
gate is to define that exact finite/reduced system before interpreting the
linear Newton correction as an amplitude series. This check is not a no-go
for the other seven supports, larger carriers, or the full configuration
space. No L=3 test is started without an exact L=2 witness.

### 9.5 Exact matched-affine residual jet on the selected support

The selected all-face-active seven-support has the exact Cayley path in §9.4.
Now put a homogeneous matched translation vector `b_r ∈ ℚ^4` on every
edge of role `r` at all 16 sites; regard its 16 components as free variables,
rather than choosing a special `b`. The standalone exact
certificate
`a4d_resolved_curved_stationary_e2_support7_affine_order2_check.py`
uses truncated rational matrix jets and the repository's existing joint
residual/channel formulas.

For every face, `det(I-P)` and its first coefficient vanish. On the four
curved faces, `adj(I-P)` has first coefficient of rank two. More precisely,
the `epsilon^2` determinant coefficients are `-1483524/169` on faces
`(0,2),(1,2)` and `-484/169` on `(0,3),(1,3)`.

For every ordered distinct face pair, the coefficient maps of the affine
joint residual satisfy
`R_0(b)=R_1(b)=0` for every homogeneous matched `b`. At order two, the
30 ordered pairs split into 10 zero maps, 8 maps of rank 2, and 12 maps of
rank 3. Thus the residual itself first activates at order `epsilon^2` for
generic homogeneous matched translations on this path; adjugate activation
at order one alone did not establish this.

After summing the 16 identical sites, each of the four existing channel
quadratic forms has a nonzero `epsilon^4` coefficient in the 16 components of
`b`. Their exact matrix ranks are respectively `7` (`eta,adj`), `3`
(`eta,opp`), `8` (`n,adj`), and `4` (`n,opp`). This is only the
first activation of the existing channel forms. It does not solve the
matched-affine equation `R=R_*(C)`, the affine Euler equations, or the full
Lorentz Euler equations.

The order-zero star Euler defect at the base point remains nonzero (§9.4).
Consequently the prescribed `x(epsilon)=epsilon*v+epsilon^2*w+...` is not a
stationary formal branch through this point: its constant Euler coefficient
is already `E_0 != 0`. This rejects that base-anchored branch ansatz, not
the support as a finite nonlinear search and not other stationary seeds.
The remaining finite L=2 exactification is open; no L=3 hostile control has
started.

### 9.6 Shared blind subspace of the matched-affine 2-jet

The order-two certificate also compares the leading channel forms with the
stacked coefficient map `b ↦ (R₂^{f,g}(b))` over all 30 ordered distinct
face pairs. The sum of the two `n`-channel matrices is positive semidefinite
of rank 8 on the 16-dimensional homogeneous matched-translation space, so its
kernel `V₂` has dimension 8 and is exactly the common zero set of the two
leading `n`-channel forms. Both leading `η`-channel quadratic forms restrict
to zero on `V₂`. The stacked `R₂` map is a `120 × 16` matrix of rank 8 and
vanishes on `V₂`; hence its kernel is exactly `V₂` as well.

Therefore, on this specified path and homogeneous matched-translation family,
the four leading channel coefficients vanish together exactly on the same
8-dimensional subspace where every order-two pair residual vanishes. This is
a shared blind 2-jet, not an exact nonlinear kernel: it neither supplies a
finite witness nor proves a no-go. Higher-order residual/channel terms or the
full finite L=2 equations remain necessary; no `R=0` constraint is imposed.
The additional exact checks are owned by
`a4d_resolved_curved_stationary_e2_support7_affine_order2_check.py`.

### 9.7 Order-three resolution of the shared blind space

The degree-three rational jet certificate extends the same Cayley path and
translation family to `epsilon^3`; it checks that every order-two pair map
agrees with the independent order-two owner. The stacked `R_3` map is
`120 × 16` of rank 16. In particular, its restriction to `V_2` has rank 8,
so every nonzero fixed `b ∈ V_2` activates some ordered-pair residual at
order three. On `V_2`, the four order-six channel matrices have ranks `8`
(`eta,adj`), `4` (`eta,opp`), `8` (`n,adj`), and `4` (`n,opp`); the sum of
the two `n`-channel matrices is positive definite there.

Combining §§9.6–9.7 gives a precise fixed-direction statement for the sum of
the existing `n` channels: if `b ∉ V_2`, its order-four coefficient is
positive; if `b ∈ V_2` and `b ≠ 0`, its order-six coefficient is positive.
Thus no nonzero constant homogeneous matched translation is invisible to
that channel sum through order six along this particular Cayley path.
This is a finite-jet statement only. It does not solve `R=R_*(C)`, the affine
or Lorentz Euler equations, or any system with `b` varying with `epsilon`; it
does not establish a stationary branch or a global no-go. The exact order-three
checks are in
`a4d_resolved_curved_stationary_e2_support7_affine_order3_check.py`.

### 9.8 Free-solder cokernel gate for the eight supplied Newton vectors

The owned four residual channels in `a4d_resolved_curved_stationary_f4_check.py`
are independent of the free absolute solder `Theta`; their `b` and Lorentz
arguments do not include `Theta`. Thus the star solder Euler equations are a
necessary sector of the selected four-channel full stationary system, for any
channel coefficients and translations. At the homogeneous base of §9.4,
`Theta_0 = eta = diag(1,-1,-1,-1)` is nondegenerate and solder-critical,
but the Lorentz-link defect is still `E_0 != 0`.

The standalone exact certificate
`a4d_resolved_curved_stationary_e2_support7_solder_cokernel_check.py`
computes the `16 x 16` solder Hessian `H_Theta` and the `16 x 12` mixed
solder/normal-amplitude Jacobian. The Hessian is symmetric of rank 6 and
nullity 10. In row-major coordinates `vec(Theta_0)` belongs to its left and
right kernel. The mixed Jacobian has rank 11; its projection to the solder
cokernel has rank 6.

For each of the eight enumerated supports, let `v` be the unique star-only
missing-Euler Newton vector `J_missing v = -E_0,missing`, and `J_Theta`
its mixed solder Jacobian. An arbitrary first solder correction `Y` could
lift that amplitude vector only if

```text
H_Theta vec(Y) + J_Theta v = 0.
```

Pairing with `vec(Theta_0)` gives a nonzero exact obstruction for every
supplied vector. In the support order of the order-one owner the values are

```text
(-4992/67, 4992/1055, -14976/47, 7296/7,
 1872, 16768/13, 49920/67, -99840/427).
```

For each support, `[H_Theta | J_Theta v]` has rank 7, against rank 6 for
`H_Theta`. The scale pairing also equals `2 d_v S_star`, checked separately
by the link Euler owner and quadratic homogeneity in `Theta`. In particular,
for the selected support it is `16768/13`. No first solder correction cancels
that particular amplitude direction.

For general amplitudes in the selected seven-support, projection to the
solder cokernel has rank 4 and kernel dimension 3. In zero-based support
coordinates its exact necessary and sufficient first-order range conditions
are

```text
x0 + 4*x6 = 0;  x2 + x6 = 0;  x3 - x4 = 0;  x5 = 0.
x = (-4*z3, z1, -z3, z2, z2, 0, z3).
```

The certificate constructs an exact solder lift for these three kernel
vectors. The selected Newton vector violates the four displayed conditions
by `(-368/13,-310/13,-253/13,-24/13)`.

This is a range obstruction to the eight supplied star-only missing-Euler
corrections, with free first-order solder included. It does not identify those
vectors with Newton corrections of the full coupled system, whose variables
include solder and translations. It is not a finite no-go for all points on
any seven-support. The nonstationary base already precludes the proposed
base-anchored stationary germ at order zero. A finite reduction must keep the
actual nonlinear solder equations and the full link/affine equations; the
three-dimensional tangent kernel alone is not such a reduction. Task and PR
remain `IN_PROGRESS` / Draft.

### 9.9 Exact finite obstruction on the Newton correction line at fixed solder

The standalone certificate
`a4d_resolved_curved_stationary_e2_support7_finite_solder_check.py`
evaluates the exact Cayley path of §9.4 over `QQ(t)`, without truncating it.
For the stored absolute solder `Theta = eta`, the numerator gcd of all 16
homogeneous solder Euler components is exactly `t`. Two components suffice:

```text
(grad_Theta S_star)[1,2] =
  -16*t*P(t) / (13*(11*t-52)^2*(11*t+52)^2*(173*t-13)),
(grad_Theta S_star)[1,3] =
   16*t*Q(t) / ((173*t-13)*(372817*t^2-4992*t-2704)^2),

P(t) = 787729723*t^5 + 11910201168580*t^4 + 57328162663980*t^3
       - 4300465765648*t^2 - 5810906816*t + 29560863488,
Q(t) = 32783181538633*t^4 + 468038424932*t^3
       - 1604236731760*t^2 + 56982657472*t + 3772793856.
```

The certificate computes exact Bezout coefficients of degrees 3 and 4 and
checks `u*P + v*Q = 1`. Therefore both displayed components can vanish only
at `t=0` on the open Cayley chart. The four chart determinants are

```text
D0 = -2*(173*t-13)*(173*t+13)/169;
D1 = 2;
D2 = -(372817*t^2-4992*t-2704)/2704;
D3 = -(11*t-52)*(11*t+52)/2704.
```

Every reduced solder-gradient denominator divides `(D0*D1*D2*D3)^2` up to a
nonzero rational factor. Thus the argument removes only declared chart units.
At `t=0`, every face has `det(I-P)=adj(I-P)=0`, so every joint residual is
zero for arbitrary affine translations and the four quadratic channels have
zero first variation. The nonzero Lorentz Euler vector in §9.4 consequently
persists for any four-channel coefficients. Together these checks prove:

> On this one-dimensional Newton correction line, at the fixed nondegenerate
> solder `Theta=eta` and inside its open Cayley chart, no value of `t` is a
> full stationary configuration, for any of the selected four-channel
> coefficients or affine translations.

An independent hostile extension tests all free solder entries at the unit
iterate `t=1`: its symmetric `16 x 16` solder Hessian has exact rank 16. Its
solder Euler equations therefore force `Theta=0`, so this particular iterate
cannot acquire a nondegenerate stationary solder. The Hessian-gradient
identity is checked directly; no fixed-solder assumption is used for this
unit-point extension. The path also reproduces
`d_t S_star|0=8384/13` and the scale obstruction `16768/13` of §9.8.

This is a finite **line-specific** no-go and a free-solder **unit-point**
no-go. It does not settle the seven independent amplitudes, free solder at
other finite points, or the full coupled residual equation `R=R_*(C)`. It
therefore does not justify either requested support-wide negative terminal.
The task remains `IN_PROGRESS`, and L=3 remains gated on an exact active-
residual L=2 witness.
