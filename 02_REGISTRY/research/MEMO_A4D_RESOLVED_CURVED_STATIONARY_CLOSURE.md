# MEMO A4D -- resolved curved stationary closure (F4 / lower wall)

**Task:** `EXP-A4D-RESOLVED-CURVED-STATIONARY-CLOSURE`
**Execution:** PR #202
**Status:** IN_PROGRESS / durable checkpoint (restructured F4 attack)
**Baseline:** `d65d826793cf39a9dba7ab390e27dd4e465d2f00`

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
\mathrm{curv}^2=\frac{64j^2(\gamma^2+\delta^2)}{j^2+4}
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
\qquad
det(I-P_{rs})approx0,
\qquad
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
\qquad
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
\boxed{\operatorname{rank}J=14},
\qquad
\boxed{\operatorname{nullity}=13}.
]

Thus exactification can be organized as a square transverse solve rather than a
27-variable blind reconstruction.

A rank-revealing QR decomposition selects 14 pivot variables. The remaining 13
coordinates were fixed to the following low-denominator rationals:

[
-\frac13, 0, -\frac13, \frac12, \frac12, -\frac12, -\frac12,
\frac43, \frac32, \frac12, \frac23, -\frac13, -1.
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
\boxed{8}.
]

The Jacobian of the literal full Euler residual restricted to those 27
variables has rank 14. Therefore only six additional independent conditions
come from Lorentz variations transverse to the (E(2)) little-group
subalgebra:

[
\boxed{14=8_{
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
(`eta,opp`), `8` (`n,adj`), and `7` (`n,opp`). This is only the
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
(`eta,adj`), `4` (`eta,opp`), `8` (`n,adj`), and `8` (`n,opp`); the sum of
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

### 9.10 Nonlinear split of the fixed-solder necessary subsystem

The seven independent amplitudes of the selected support are `x0,...,x6` in
the owner order

```text
(K1_0,K1_2,N2_2,N3_0,N3_1,N3_2,N3_3).
```
The exact multivariate certificate
`a4d_resolved_curved_stationary_e2_support7_independent_solder_check.py`
constructs each role's actual Cayley matrix and Lorentz inverse over
`QQ[x0,...,x6]`. Its chart factors are

```text
D0 = 2 - x0^2/2;  D1 = 2;
D2 = 1 - x5 - (x1^2+x2^2)/4;  D3 = 1 - x6^2/4.
```
It forms the full symmetric polynomial solder Hessian `H_num(x)` with a
single cleared product of squared chart factors and verifies
`H_num(x) vec(eta)` against all 16 fixed-solder Euler numerators. All 16
polynomial equations for the fixed-solder necessary subsystem are available
from that certificate; the four row-major entries with column index 2 are
stored in
`a4d_resolved_curved_stationary_e2_support7_solder_reduced4.json`.
Their degrees are `(8,6,9,8)` in `(x0,x3,x4,x6)`, independent of the other
three amplitudes. Their `4 x 4` tangent Jacobian in those variables at the
base has determinant `-131072`, consistent with the full seven-column
fixed-solder Jacobian rank 7.

One equation in this subsystem is linear in `x0`, say `a*x0+b=0`, and the
certificate checks the exact factorization

```text
b - 2*a = 2*x4*(x6^2-4)^2,
a(x4=0) = 32*x6^2.
```
The chart excludes `x6^2=4`. In the exceptional case `a=0`, the equation
forces `b=0`, whence `x4=x6=0`; the other two equations reduce to a small
exact two-variable ideal and imply `x0=x3=0` on the chart. With these four
amplitudes zero, the remaining exact solder equations in `(x1,x2,x5)` have
a lexicographic Groebner basis containing `x2^2+x5^2` and
`x5^2*(x1-x5+2)`. Over the reals, `x2=x5=0`; the other basis factor and
`D2 != 0` force `x1=0`. Thus the whole exceptional branch is the original
seven-amplitude base, where the full Lorentz Euler defect is nonzero.

For `a != 0`, homogeneous substitution `x0=-b/a` gives a necessary
three-variable polynomial system `F_0=F_2=F_3=0` in `(x3,x4,x6)` of exact
degrees `(19,25,24)`. The chart conditions `x6^2 != 4`, `b^2-4*a^2 != 0`
(equivalently `x0^2 != 4`), and `D2 != 0` remain explicit.

### 9.11 The main branch is empty in the open Cayley chart

`a4d_resolved_curved_stationary_e2_support7_main_branch_check.py` eliminates
`x3` from `F_0` and `F_2`, and from `F_0` and `F_3`. The gcd of those two
resultants has radical

```text
x4 * (x6-2) * (x6+2) * Q1 * Q2,
```

with the explicit degree-5 factors

```text
Q1 = 2*x4^3*x6 - 4*x4^3 + 8*x4^2*x6 - x4*x6^4 + 2*x4*x6^3
     + 12*x4*x6^2 + 8*x4*x6 + 32*x6^2,
Q2 = 4*x4^3*x6 - 8*x4^3 + 16*x4^2*x6 - x4*x6^4 + 4*x4*x6^3
     + 16*x4*x6^2 + 16*x4*x6 + 16*x4 + 64*x6^2.
```

Every common zero therefore lies on one of these factors. The certificate
then checks:

- `b-2*a = 2*x4*(x6^2-4)^2`, so `x4=0` forces `b=2*a` and, when `a != 0`,
  `x0=-2`. The whole plane `x4=0` is the Cayley wall `x0^2=4`.
- The ideal `(F_0,F_2,F_3,Q1)` contains `x6*(x6^2-4)`. Thus `x6=±2`, or
  `x6=0`, which with `Q1` forces `x4=0` and returns to `a=0`.
- The ideal `(F_0,F_2,F_3,Q2)` contains
  `x6*(x3^2-8*x6)*(x6^2-4)`. The slice `x6=0`, `x4^2=2` gives `x0=2`.
  On `x6=x3^2/8`, `b^2-4*a^2` reduces to zero, so again `x0^2=4`.

Hence `F_0=F_2=F_3=0` has no point with `a != 0`, `x6^2 != 4`, and
`x0^2 != 4`. The open main branch is empty. Combined with the exceptional
branch of §9.10, the only solution of this fixed-`eta` necessary subsystem
inside the open Cayley chart is the seven-amplitude origin, where the full
Lorentz defect remains nonzero.

This closes the fixed-solder seven-support gate. It does not solve free
solder away from `eta`, the full link/affine Euler system, or
`R=R_*(C) != 0`. No L=2 active-residual witness is obtained, so L=3 stays
unopened. The task remains `IN_PROGRESS`.

### 9.12 Frozen base link: joint linear gate and absolute solder

The next exact object keeps the selected support and the base link of §9.4,
and lets the absolute solder move. One absolute coframe is copied at every
site. Site-dependent solder is not in this gate. The certificate is
`a4d_resolved_curved_stationary_e2_support7_joint_linear_gate_check.py`.

The star density is bilinear in the two complementary solder legs, so at
this fixed link the absolute-solder gradient is exactly the constant
symmetric Hessian `H` of §9.8. That Hessian has rank 6. Its kernel is the
full solder-critical set and has the coordinate form

```text
[ z0+z1-z2 , z0 , z3 , z4 ]
[ z1       , z2 , z3 , z4 ]
[ z5       , z5 , z6+z8+z9 , z6 ]
[ z7       , z7 , z8 , z9 ].
```

`eta` is the point `z2=z9=-1` and the rest zero. The six test matrices
`{M2,M3,-J23,K1,N2,N3}` are a basis of `so(1,3)`, so the 24 link components
are the full homogeneous link Euler. On this kernel those components are
quadratic. In test order `(M2,M3,-J23,K1,N2,N3)`,

```text
(E_{role 2, N3} + E_{role 3, N2}) / 64 = (z0-z2)(z1-z2).
```

The same coordinates give

```text
det theta = (z0-z2)(z1-z2)(z6*z8 - z6*z9 - z8*z9 - z9^2).
```

Every common zero of the link Euler on the solder-critical set therefore
has determinant zero. The base point `eta` is the control that criticality
alone is not the cause: `det eta = -1`, and its link Euler is the nonzero
defect of §9.3. The pure scale `theta = t*eta` has Euler `t^2 E_0`, hence
exact link stationarity only at `t=0`, where the solder is degenerate.
The Newton prediction `t=1/2` remains critical and has determinant
`-1/16`, but its exact Euler is `E_0/4`. A second control,

```text
[[2, 1, 0, 0], [1, 0, 0, 0], [0, 0, 2, 1], [0, 0, 1, 0]],
```

is solder-critical with determinant 1 and nonzero link Euler.

The joint linearization of `S_star` at `(x, theta) = (0, eta)` uses the seven support
amplitudes and all 16 solder entries. The system is `40 x 23` of rank 19
and is consistent. One particular solution is the pure scale
`Y = -eta/2` with every amplitude zero. The homogeneous kernel has
dimension 4, and its amplitude block is zero. An explicit basis of that
solder kernel is

```text
[[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
[[0, 0, 2, 1], [0, 0, 2, 1], [1, 1, 0, 0], [0, 0, 0, 0]]
[[0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 0, 0], [1, 1, 0, 0]]
[[0, -1, -3, -1], [1, 0, -3, -1], [0, 0, 1, 0], [0, 0, 0, 1]].
```

Thus every first-order solution has `N2` on role 2 and `N3` on role 3
equal to zero. Those are the only two support directions whose first
adjugate variation is nonzero: rank 2 on faces `(0,2),(1,2)` and
`(0,3),(1,3)` respectively. Every other support direction, and every
joint solution, has vanishing first adjugate variation on the four curved
faces. All six faces already have `det(I-P)=adj(I-P)=0`, while exactly
four curvature bivectors are nonzero.

The owned channel integrand is the quadratic form of
`R = det(I-P_1) t_2 - (I-P_2) adj(I-P_1) t_1`, with no solder argument.
At this frozen link `R` vanishes for every translation, so each channel
value and each first link or translation derivative of a channel vanishes.
Translations do not repair the link. The full four-channel action
therefore has no nondegenerate stationary point at this one homogeneous
link, for any channel coefficients and any translations. Curvature is
present and the residual stays zero, so this is not an active-residual
witness.

Zero amplitudes in the linearization are not a finite no-go for the
seven-amplitude family away from this link. No L=2 witness with
`R != 0` is obtained, and L=3 stays unopened. The task remains
`IN_PROGRESS`.


### 9.13 Observer-form audit of the affine jets

The first versions of the order-two/order-three affine-jet certificates
used the null-vector outer product `n n^T`, `n=(1,1,0,0)`, for the observer
channel. That is not the selected form `h_n=I4` of the F4 owner. The
certificates now use `I4` and check the actual `H_N` declaration in
`a4d_resolved_curved_stationary_f4_check.py`. No extra channel is retained.

With the selected observer form the exact order-four ranks in §9.5 are
`(7,3,8,7)`, and the exact order-six ranks on `V2` in §9.7 are `(8,4,8,8)`.
These replace the earlier `(7,3,8,4)` and `(8,4,8,4)` channel-rank claims.
The residual maps themselves are unchanged: `rank R2=8`, `dim V2=8`,
`rank R3=16`, and `rank(R3|V2)=8`. The positive-semidefinite order-four
observer sum still has kernel `V2`, and its order-six restriction remains
positive definite. The finite-jet activation and common-kernel conclusions
of §§9.5–9.7 therefore survive for the actual four-channel action.

This audit does not solve the affine Euler equations or select coefficients.
The task remains `IN_PROGRESS`.

### 9.14 All eight supports: the joint linear gate with all four channels

The exact certificate
`a4d_resolved_curved_stationary_e2_all_supports_joint_channel_check.py`
keeps the same frozen link and one homogeneous absolute solder. It widens
translations to arbitrary values on all 64 edges of the L=2 torus. The 24
link rows are homogeneous Lorentz variations, hence necessary rows of the
full sitewise Euler system; no sufficiency for that full system is asserted.

Let `n=(1,1,0,0)^T`, `m=(1,-1,0,0)`, and `beta(x,r)=m*b(x,r)`.
Every base link fixes `m`. The exact affine face translation therefore has

```text
m*t_rs(x) = beta(x,r) + beta(x+r,s) - beta(x,s) - beta(x+s,r)
          = curl_rs beta(x).
```

All determinant first derivatives vanish. Among the twelve normal and
twelve internal homogeneous directions, the first residual can be nonzero
only in `N2_2` and `N3_3`. Their eight nonzero ordered-pair products are

```text
M_second * d adj(M_first) = -8*n*m,

N2_2: first=(r,2), second=(s,3), r,s in {0,1};
N3_3: first=(r,3), second=(s,2), r,s in {0,1}.
```

Thus `dR=8*n*active_amplitude*curl_first beta` on these pairs and zero on
all others. Constant rolewise translations have zero curl, explaining their
vanishing first residual jet without confusing it with vanishing adjugate.
For arbitrary site-dependent translations that cancellation does not hold.
The exact hostile control `b(origin,0)=e0`, all other edges zero, gives
`dR_{(0,3)|(0,2)}(origin)=8*n` in direction `N2_2`. A direct untruncated
Cayley calculation independently checks this derivative.

Write `alpha=x(N2_2)`, `gamma=x(N3_3)`, and

```text
C2 = sum_{x,r=0,1} (curl_{r,2} beta(x))^2,
C3 = sum_{x,r=0,1} (curl_{r,3} beta(x))^2.
```

Since `n^T eta n=0` and `n^T h_n n=2` for the selected `h_n=I4`, the
literal order-two coefficients of the four channels are

```text
[eps^2] I_eta_adj = [eps^2] I_eta_opp = 0,
[eps^2] I_n_adj   = [eps^2] I_n_opp
                 = 128*(alpha^2*C2 + gamma^2*C3).
```

Consequently the four-channel contribution to the joint linearized Euler
matrix is supported only on the two matching link rows and amplitude
columns. Its diagonal entries are
`lambda2=256*C2*(c_n_adj+c_n_opp)` and
`lambda3=256*C3*(c_n_adj+c_n_opp)`. Translation and solder rows have zero
channel contribution at this order because the base residual vanishes for
every translation and the channels have no solder argument.

The star joint matrix for all twelve normal amplitudes and 16 solder entries
is `40 x 28` of rank 23. Its five-dimensional kernel has amplitude projection
of dimension one, exactly the common `K1_0=K1_1` direction. Its particular
solution is again `x=0, Y=-eta/2`. Crucially, even after deleting both
channel-active link rows, the resulting rank-22 matrix still forces
`alpha=gamma=0`. The certificate checks that a symbolic channel shift with
*independent arbitrary* `lambda2,lambda3` annihilates the entire kernel of
this row-deleted matrix and the particular solution. Therefore adding the
four channels cannot change the solution set of this joint linear gate;
no coefficient division, coefficient grid, or positivity assumption is used.

Restriction to each of the eight owned minimum supports gives:

| Support indices in §9.4 owner order | Joint rank | Kernel dimension | Amplitude projection dimension |
|---|---|---|---|
| 0–4 | 18 | 5 | 1 (common `K1_0=K1_1`) |
| 5–7 | 19 | 4 | 0 |

For every support, deleting the channel-active rows still forces every
present active amplitude to zero. The symbolic-shift identity consequently
proves the same channel-independent solution-set statement on all eight.
Every solution has zero first adjugate and residual variation, including
arbitrary site-dependent translations. The nonzero residual hostile control
shows that this conclusion comes from the joint equations, not from a
structural assertion that all translations are blind.

These are **unit-linear correction** facts at a nonstationary seed. The
original base-anchored stationary formal germ remains obstructed at order
zero by `E0 != 0`; `Y=-eta/2` is not an exact stationary solder (§9.12).
Finite deformations away from this link, with free solder and the actual
finite affine Euler equations, remain open. None of the eight supports is
retired as a finite nonlinear support-wide no-go by this calculation. No
active-residual L=2 witness is obtained, and L=3 remains unopened. The task
and PR stay `IN_PROGRESS` / Draft.


### 9.15 Finite Newton line with all 16 free solder entries

The exact certificate
`a4d_resolved_curved_stationary_e2_support7_free_solder_line_check.py`
replaces fixed-solder sampling on the selected support-5 line `x=t*v`
by classification of every homogeneous absolute solder-critical point.
It reconstructs the Cayley matrices from the owner and verifies the stored
polynomial inverse column in
`a4d_resolved_curved_stationary_e2_support7_free_solder_root_data.json`.
No floating root approximation is used.

Let `D_r` be the four chart determinants in §9.8, `C=prod_r D_r^2`, and
let `Q` multiply solder column `r` by `D_r^2`. The exact solder Hessian is

```text
H_theta = Q H_norm Q / C,
```

where `H_norm` is a symmetric polynomial matrix of degree at most 8.
Its determinant is a nonzero rational constant times

```text
t^12 (173*t-13)^2 (173*t+13)^2 P_78(t).
```

`P_78` is squarefree and coprime to `t` and every Cayley chart factor.
Exact real isolating intervals give 22 simple real roots. Away from `t=0`
and these roots, solder stationarity forces `Theta=0`. At every root the
normalized Hessian has rank 15: a corank of at least two would make the
first derivative of its determinant vanish.

The checked polynomial identity is `H_norm V=d*e0`, where
`d` is a nonzero constant times `t^2 P_78`.
Both `V_0` and `det reshape(V)` are coprime to `P_78`.
Thus each of the 22 roots has a one-dimensional critical solder space,
spanned by `Q^-1 V`, and every nonzero member is nondegenerate.
One curvature component is coprime to `P_78` too, so all these links are
curved. Solder criticality has therefore not been mistaken for a vacuum.

Differentiating the inverse-column identity and using symmetry gives
`V^T H_norm' V=d' V_0` at a root. The derivatives of `Q` and `C` drop out
at criticality. Consequently the literal partial link derivative along the
line is `d' V_0/(2*C)` times the square of the solder scale; it is nonzero
at every root with nondegenerate solder.

For the matched homogeneous translation ray
`b_0=s*e0`, `b_1=b_2=b_3=0`, four actual affine Euler rows form a `4 x 4`
coefficient-response matrix. Its reduced determinant has numerator degree
125 and denominator degree 120. Both are coprime to `P_78`. For `s != 0`,
these necessary affine equations force all four channel coefficients to
zero. For `s=0`, every channel link derivative already vanishes. In either
case the nonzero star path derivative excludes full stationarity at all
22 roots. The frozen `t=0` point is excluded for every nondegenerate
critical solder by §9.12.

**Exact scope:** the entire open Newton line, every free homogeneous
absolute solder, every four-channel coefficient choice, and the stated
translation ray. This does not classify arbitrary translations or seven
independent amplitudes. It is not a support-wide terminal and supplies no
active-residual witness. L=3 remains unopened.


### 9.16 Genuine degenerate-seed germs: the eta-leading lift is obstructed

`a4d_resolved_curved_stationary_e2_eta_leading_seed_jet_check.py`
checks a genuine stationary seed: the frozen links, `Theta=0`, and arbitrary
L=2 edge translations. All base residuals vanish, and the star density is
quadratic in solder. Consider

```text
A = A0 + eps*v + O(eps^2),
Theta = eps*eta + O(eps^2),
b = b0 + O(eps),
```

with constant arbitrary coefficients of the four selected channels.
This explicitly differs from the nonstationary `Theta=eta` unit correction
in §9.14. A nonzero leading solder determinant would make this a potentially
nondegenerate punctured germ if the equations survived.

The first solder equation is `H0*eta=0`. At order two, range elimination
of `H0*Y + H1(v)*eta=0` gives a six-dimensional tangent kernel in the
union of twelve normal amplitudes. The eight support kernel dimensions
are `(2,1,1,2,2,3,1,1)`. Seven supports force both present first-residual
amplitudes to zero. Support 5 has exactly

```text
v = (-4*z3, z1, -z3, z2, z2, 0, z3)
```

in its declared seven-amplitude order. These relations are necessary solder
Euler conditions; they are not imposed as an arbitrary finite ansatz.

The role-0 homogeneous Lorentz variation
`w=(9/2)*J23-(3/2)*N2+N3` has `R1(w)=0` and star source
`[eps^2] EL_w=24`. If `R1(v)=0`, all channel terms in this row vanish at
that order, killing the other seven supports and the blind part of support 5.
If `R1(v)!=0`, the order-one link equations force
`c_n_adj+c_n_opp=0`; the positive curl-square identity of §9.14 proves this
without selecting a coefficient value.

On support 5's tangent, the eta channels have `Q3=0`. The observer-channel
difference has only a `z3^3` cubic monomial. Its affine Euler equation at
order three is therefore a homogeneous quadratic-form kernel condition
for each of the 16 real L=2 Fourier modes. Their exact Hessian ranks are
`0,2,2,2,4,4,4,4,4,4,4,4,0,2,2,2` in lexicographic parity order.
The complete Walsh matrix is checked to have Gram matrix `16*I`.
This modewise calculation includes every translation field, not only
single-mode examples.

If `c_n_adj-c_n_opp=0`, the universal eta-channel cokernel row `w` already
leaves source 24. Otherwise impose the actual affine order-three equations.
On their kernel, the two necessary link rows `N2@role2` and `N2@role3`
have the following exact properties in every mode:

- all channel terms except `z3^2` vanish;
- the eta-adjacent and eta-opposite forms agree;
- the observer-difference form vanishes;
- the `N2@role3` eta form is positive semidefinite, of rank zero or one;
- its kernel kills the quadratic form for `N2@role2`.

The star sources in these rows are respectively `-32` and `0`.
Write `Gamma=c_eta_adj+c_eta_opp`. If `Gamma=0`, the first row remains
`-32`. If `Gamma!=0`, the second row forces a sum of nonnegative Fourier
quadratic forms to vanish. Each mode lies in that form's kernel, so every
channel term in the first row also vanishes. Again `-32=0` is impossible.
No sign assumption on `Gamma`, observer-difference coefficient, or
individual channel coefficient is used. Second amplitude/solder/translation
coefficients cannot repair these leading equations: star starts at solder
order two, and the entire channel quadratic jet is zero once the necessary
observer-sum relation is imposed.

**Exact scoped verdict:** all eight germs with this prescribed
`Theta=eps*eta+...` leading solder are obstructed through coupled order
three (link/solder order two and affine order three). This is a nonlinear
compatibility obstruction at an actual stationary seed, rather than a
rank argument at a nonstationary one. It is not a classification of general
nondegenerate leading solder or finite seven-amplitude configurations.
Those remain live; no support-wide finite terminal or L=2 witness is claimed,
and L=3 stays unopened.


### 9.17 General critical leading solder: seven supports die, one locus remains

`a4d_resolved_curved_stationary_e2_critical_solder_range_check.py`
removes the prescribed eta leading solder in §9.16. Keep homogeneous links
and one homogeneous absolute solder, with `Theta=eps*T+...`, where
`H0*T=0` and `det T!=0`. The ten critical coordinates in §9.12 are used
literally. Define

```text
A=z0-z2, B=z1-z2,
C=z6*z8-z6*z9-z8*z9-z9^2.
```

The exact determinant is `det T=A*B*C`, so all three factors are units.
The order-two solder range condition is `L*H1(v)*vec(T)=0`, with `L`
a basis of the full H0 cokernel. Every entry is reconstructed from the
actual Cayley directional curvature derivative. Its eta specialization is
checked against the owned mixed-partial matrix.

In the twelve-normal union, write `dk=K1_0-K1_1`,
`d2=N2_0-N2_1`, `d3=N3_0-N3_1`, `alpha=N2_2`, `gamma=N3_3`,
`u=N2_3`, and `w=N3_2`. A two-row `d2,d3` minor is exactly `2*C`,
hence `d2=d3=0`. Further literal row identities give

```text
alpha=-gamma,
dk=-4*(B/A)*gamma,
u=w=0,
(z6+z8)*gamma=0.
```

No generic-rank sampling or polynomial-system solver is used in this
classification. The common K1, N2 and N3 role-0/1 directions and K1 on
roles 2/3 are blind kernel moduli.

Every support except index 5 lacks one member of the required pair
`N2_2,N3_3`, and therefore has `R1(v)=0`. Two inactive link tests,
`N3@role2` and `N2@role3`, have first determinant and adjugate variation
zero; this is independently checked for every face. Their channel Euler
terms at order two vanish when `R1(v)=0`, whereas their exact star-source
sum is `64*A*B!=0`. Thus all seven supports are obstructed for *every*
nondegenerate critical leading solder and arbitrary translations/coefficients
in this specified germ class.

The only residual-active survivor is support 5 on `z8=-z6`. Its lower
critical solder block is `[[z9,z6],[-z6,z9]]` and
`det T=-A*B*(z6^2+z9^2)`. Its tangent must be

```text
(-4*(B/A)*gamma, q1, -gamma, q2, q2, 0, gamma).
```

This is an explicit conformal critical-solder locus, not a preferred
nonlinear completion or a coefficient selector. The remaining locus needs
higher coupled equations. These germ exclusions do not exclude arbitrary
finite points of the seven-amplitude supports, and no L=2 witness or L=3
result is claimed.


### 9.18 Conformal critical-solder subfamily: exact order-three obstruction

`a4d_resolved_curved_stationary_e2_conformal_solder_order3_check.py`
pressure-tests a one-parameter family inside the surviving locus of §9.17.
Here `A=B=1`, the active tangent scale is one, and both blind tangent
moduli remain free:

```text
v=(-4, q1, -1, q2, q2, 0, 1).
s=(r^2-1)/(r^2+1), h=6*r/(r^2+1),
c=(s+h)/2, d=(s-h)/2.
```

For `r!=0`, let `(p3,p4)` solve the literal two-row system

```text
[[1+2*d,1+2*c],[1-2*c,-1+2*d]] * [p3,p4]^T = [d,c]^T,
T=[[1,0,p3,p4],[0,-1,p3,p4],[0,0,d,c],[0,0,-c,d]].
```

Its determinant is `-(r^4+34*r^2+1)/(2*(r^2+1)^2)`, nonzero for every
real r. This is a family of critical leading solders, not a finite vacuum.
The small leading-link balance motivated this family; the certificate's
owned conclusion is the following stronger solder-only exclusion,
independent of every translation and channel coefficient.

At order two `H0*Y=-H1(v)*T` is exactly solvable. At order three eliminate
the next solder coefficient Z with the full H0 cokernel. Keep all ten
Y-kernel variables and all seven second amplitude coefficients: the
necessary system has shape `10 x 17`. Its polynomial cokernel identities
hold for both free tangent moduli. The first identity forces `q2=0`.
Two others eliminate q1 without division by a potentially vanishing
coefficient. Their exact one-variable polynomial gcd leaves only `r=1/3`.
All denominator factors are r or the strictly positive `r^2+1`.

At `r=1/3`, generic cokernel vectors lose independence, so the certificate
recomputes the actual kernel. Two literal obstruction rows are
`-256*q2/5` and `-32*(29*q2+644)/45`; a rational linear combination is
`-20608/45`, contradicting compatibility. Thus no real r in the declared
family survives the third solder order. The r=1 member, even allowing
both tangent moduli, already requires `q2=0` and `q2=10` simultaneously.

The singular r=0 construction is not treated as a limit of the inverse
matrix. A separate explicit critical solder is tested:

```text
T0=[[1,0,0,0],[0,-1,0,0],[0,0,-1/2,-1/2],[0,0,1/2,-1/2]].
```

Its three exact order-three compatibility rows force `q2=-3`, `q1=9/2`,
and then leave a nonzero residual 64. This explicit zero-ratio leading
balance is excluded too.

**Scoped verdict:** these conformal leading-solder families are blocked
at nonlinear solder order three, including all second amplitude/solder
corrections and both tangent moduli. Arbitrary affine fields or channel
coefficients cannot repair a solder equation. The *entire* conformal
critical-solder locus in §9.17 is broader and is not retired by this result;
finite seven-amplitude equations remain open. No positive L=2 witness and
no L=3 result follow.


### 9.19 General conformal locus: an exact mixed-order compatible candidate

`a4d_resolved_curved_stationary_e2_conformal_candidate_jet_check.py`
checks a different leading solder, outside §9.18's zero lower-left-block
family. Its rational data are

```text
T=[[1,0,-53/20,-13/20],
   [0,-1,-53/20,-13/20],
   [-14/5,-14/5,-3/2,3/2],
   [-7/5,-7/5,-3/2,-3/2]],
v=(-4,-4/5,-1,0,0,0,1),
c=(c_eta_adj,c_eta_opp,c_n_adj,c_n_opp)=(-1/1024,0,1,-1).
```

The role translations have the real L=2 Fourier character `(-1)^(x0+x1)`:
`b0=e0/256`, `b1=0`, `b2=b3=e0`. These are supplied candidate parameters,
not a selection principle for the action coefficients.

At `Theta=eps*T+...`, `A=A0+eps*v+...`, all 24 literal homogeneous
Lorentz link Euler rows have zero coefficient at order two. They are also
all sitewise rows at that order: a site translation multiplies the entire
b field by one common character sign, while its contribution is quadratic.
The complete affine mode forms at orders two and three are zero matrices,
so all affine components in the occupied mode vanish at those orders.
The first residual is nonzero on eight ordered face pairs, exactly `+/-16*n`.
The leading solder determinant is `-9/2`, and the frozen curvature is
nonzero on four faces.

The actual solder order-three system, including all ten free second-solder
entries and all seven second amplitudes, has rank 5 and augmented rank 5.
Its kernel dimension is 12; the amplitude projection has dimension 4.
One exact second-amplitude particular solution is
`(0,0,18/5,56/5,0,196/25,0)`. The certificate reconstructs both the second
and third solder coefficients and substitutes them into the literal solder
Euler coefficients, rather than treating range consistency as sufficient.

**Owned status:** a mixed-order compatible truncation: link EL2, affine
EL2/EL3, and solder EL1/EL2/EL3 vanish exactly, with nonzero R1 and a
nondegenerate leading solder. Link EL3 and affine EL4 are still required.
This is not a finite witness, an all-orders formal branch, or a completed
support. In particular no hostile L=3 work is opened by these data.


### 9.20 The compatible candidate dies at actual affine order four

`a4d_resolved_curved_stationary_e2_conformal_candidate_affine4_check.py`
continues §9.19 with the full action-coefficient freedom left by its leading
balance. Define `Gamma=-1/1024` and use

```text
(c_eta_adj,c_eta_opp,c_n_adj,c_n_opp)
  = (Gamma/2+p,Gamma/2-p,q,-q),
b0=e0/(256*q), b1=0, b2=b3=e0, parity=(1,1,0,0), q!=0.
```

Here q is literally the observer-adjacent coefficient, not the difference
of the two observer coefficients. Both p and q remain free. The certificate
rechecks every leading link row for this entire family and recomputes the
actual affine forms at the next order. Third-jet functions are reused
from the existing owner and checked against the owned two-jet functions.
No alternate channel or generator convention is introduced.

All solder-compatible second-amplitude freedoms have four-dimensional
projection. Their exact matrix contribution to affine EL4 is zero, for
every p and q. Next translations in the occupied mode act through the
zero Q3 matrix, while other Fourier modes cannot repair this mode of a
translation-invariant affine operator. Higher amplitudes enter the
identically zero combined Q2 and do not repair it either. Solder corrections
are absent from the channel argument.

After multiplication by the declared unit q, the two actual affine rows
for role 0, components 2 and 3, are

```text
32*q*(1024*q-1),
-32*q*(25600*q-1)/5.
```

Their literal polynomial combination `-25*row2-5*row3` is `768*q`,
nonzero on this leading-balance chart. Thus the same branch would require
both `1024*q=1` and `25600*q=1`. No value of p, q, second amplitude,
next solder, or next translation repairs these necessary equations.
This excludes the fixed coefficient point of §9.19 as well as its entire
two-coefficient family.

**Exact scoped verdict:** the declared conformal reconstruction is blocked
by necessary affine order four. Link EL3 could impose an earlier
obstruction and is not claimed to pass; affine EL4 already excludes a
full stationary germ, so solving further rows of this reconstruction is
unnecessary. This does not classify other leading solders/tangent moduli
on §9.17's surviving locus or arbitrary finite points of support 5.
Those remain live. No L=2 finite witness, whole-support terminal, or L=3
result is claimed.

### 9.21 Free tangent modulus: both observer charts fail affine order four

`a4d_resolved_curved_stationary_e2_conformal_free_tangent_affine4_check.py`
removes the fixed tangent-modulus assumption from §§9.19–9.20. This is a
whole rational family, not a coefficient grid. Keep the declared occupied
Fourier mode 1100, `b1=0`, `b2=b3=e0`, and normalize the active tangent to
one. Write its two blind tangent coefficients as `q1,t`. For every real
`t!=2`, the following critical leading solder is nondegenerate:

```text
p3=-(13*t^2+144*t-212)/(40*(t-2)),
p4=(7*t^2-24*t+52)/(40*(t-2)),
p5=(t^2-62*t+56)/(10*(t-2)),
p7=-(9*t^2+42*t-56)/(20*(t-2)),
T=[[1,0,p3,p4],[0,-1,p3,p4],
   [p5,p5,-3/2,3/2],[p7,p7,-3/2,-3/2]],
q1=(-9*t^2+58*t+16)/(10*(t-2)),
v=(-4,q1,-1,t,t,0,1), det(T)=-9/2.
```

The exact solder range is recomputed from the owned generic Hessian jets,
keeping all ten second-solder freedoms and seven second amplitudes. A
literal constant minor is `-268435456`; rank is uniformly 5. Its kernel has
dimension 12 and amplitude projection dimension 4. Every matrix, particular
solution and kernel denominator has only powers of the declared unit `t-2`.
Thus special real values inside this chart are retained. The excluded
`t=2` is not covered by taking a rational limit.

Use `Gamma=-1/1024` and the full coefficient family
`(Gamma/2+p,Gamma/2-p,q,-q)`. Here q remains the observer-adjacent coefficient.
For `q!=0`, the leading role-0 N3 balance fixes

```text
b0=-(t^2-42*t+16)/(2048*q*(t-2))*e0.
```

Actual affine order-four matrices are recomputed over `QQ(t)` using the
existing rational matrix owner. Every solder-compatible second-amplitude
freedom drops out. The full mode matrices Q2 and Q3 have zero eta channels
and equal observer channels; next translations cannot repair this mode.
The sum of the actual role-2/component-2 and role-3/component-3 Euler rows,
after multiplying by the declared unit q, is exactly `-128*q`. This
contradicts stationarity for every t, p and nonzero q in the chart.

The zero-observer seam is checked separately, with arbitrary `b0=z*e0`.
Literal cubic polarization gives zero eta contribution to the leading
role-0 N3 row for every z. Its star source is
`-4*(t^2-42*t+16)/(t-2)`, while the observer contribution is `-8192*q*z`.
Therefore q=0 requires `P(t)=t^2-42*t+16=0`, which has two real roots and
is coprime to `t-2`. Rational-field identities show both eta contributions
from b0 vanish in the affine row sum. At P=0, the observer-b0 term vanishes
without dividing by q, and the actual eta-only affine order-four sum is
`-128`. All response/kernel denominators are regular on this seam. No
second correction, next translation or remaining coefficient p repairs it.

**Exact scoped verdict:** this entire free-tangent conformal/translation
family fails a necessary affine-order-four equation in both observer
charts. This neither declares link order three consistent nor classifies
other conformal lower blocks, independent translation ratios, other modes,
or finite seven-amplitude configurations. Those remain open; task stays
`IN_PROGRESS`, PR Draft, and L=3 remains unopened.

### 9.22 Independent translation ratio: necessary leading balance and affine no-go

`a4d_resolved_curved_stationary_e2_conformal_translation_ratio_affine4_check.py`
removes the equal-translation restriction from §9.21. The declared class
has homogeneous support-5 tangent `v=(-4,u,-1,t,t,0,1)`, real mode 1100,
`b0=z*e0`, `b1=0`, `b2=r*e0`, `b3=e0`, and critical leading solder

```text
T=[[1,0,p3,p4],[0,-1,p3,p4],
   [p5,p5,d,c],[p7,p7,-c,d]].
```

The six solder entries, the translation ratio r, both blind tangent
coefficients u,t, and all four action coefficients initially remain free.
This is a necessary-equation classification, not a chosen action selector.
The leading observer quadratic form is a strictly positive rational
multiple of `r^2+1`; the eta leading forms vanish. Affine stationarity thus
requires the observer sum to vanish. Write the remaining coefficients as
`(Gamma/2+p,Gamma/2-p,q,-q)`.

Four literal leading normal-link channel responses are

```text
role2,N2: -98304*r*Gamma,
role2,N3:  32768*Gamma,
role3,N2:  32768*r^2*Gamma,
role3,N3: -98304*r*Gamma.
```

Together with the actual star rows, a uniformly invertible three-variable
linear system forces

```text
Gamma=-1/(512*(r^2+1)),
c+d=(r^2-1)/(r^2+1),
c-d=6*r/(r^2+1).
```

No blind tangent or coefficient-difference freedom is dropped in this
calculation. Rational-field Cayley jets then give an actual affine-order-four
row sum, independent of all seven second amplitude coefficients:
`EL_b[role2,component2]+EL_b[role3,component3]=-128*(r+1)/(r^2+1)`.
Every real stationary germ in the declared class therefore requires r=-1.
If q=0, another row simultaneously requires r=1, a contradiction.

At r=-1 and q!=0, two further actual affine rows require `z=-4` and
`q*(u-2)=1/512`. The full order-three solder range is classified again,
including all ten free second-solder entries and all seven second amplitudes.
Eliminating the complete rank-two solder image leaves eight equations in
the three-dimensional second-amplitude quotient. Four independent equations
solve all p3,p4,p5,p7; the remaining range equation plus the necessary
leading role-0 N3 row give

```text
u=-(5*t^2-90*t+32)/(6*(t-2)),
p3=(5*t^2-84*t+20)/(24*(t-2)),
p4=-(13*t^2-96*t-20)/(24*(t-2)),
p5=-(t^2+18*t-8)/(12*(t-2)),
p7=(5*t^2-30*t+8)/(6*(t-2)).
```

The exceptional t=2 is excluded by the actual un-divided range equation,
which is 512 there. This is not a rational-limit argument. Nondegeneracy
is `det(T)=-9/2`. The remaining order-three matrix has a constant nonzero
rank-five minor, kernel dimension 12, and amplitude projection dimension 4.
The particular solution is substituted into all ten range equations.

All permitted second-amplitude freedoms drop from the necessary affine
rows. Put `D=5*t^2-78*t+8`; it is a unit because u=2 has already been
excluded. Two literal affine order-four rows are

```text
384*(t-2)*(t+4)/D,
-64*(5*t^2-102*t+56)/D.
```

Their numerator polynomials are coprime. They cannot both vanish, for any
remaining coefficient p or any next solder/translation. Complete occupied
mode Q2/Q3 forms vanish for both free tangent moduli; other next-translation
modes cannot cancel this mode of the homogeneous affine operator.

**Exact scoped verdict:** all independent translation ratios and all
critical solder moduli in this declared common-upper-block class are
obstructed by necessary coupled equations through affine order four.
Unequal upper solder scales, its unfixed common block, translations with
other vector components/modes, and finite off-seed amplitudes are not
retired. Task remains `IN_PROGRESS`/Draft; no finite L=2 witness or L=3.

### 9.23 Unequal upper scales and unfixed common solder block

The same ratio certificate is extended over `QQ(rho,u,t)`, without fixing
the second upper scale or the common upper-block modulus. The leading solder
is now the full normalized conformal critical form

```text
T=[[1+rho+lambda,1+lambda,p3,p4],
   [rho+lambda,lambda,p3,p4],
   [p5,p5,d,c],[p7,p7,-c,d]], rho!=0.
```

The support-5 tangent is `v=(-4*rho,u,-1,t,t,0,1)`. All lower solder
moduli, lambda, rho, both blind tangent coefficients, translations
`b0=z*e0,b1=0,b2=r*e0,b3=e0` in mode 1100, and all four coefficients remain
free before the necessary equations. No arbitrary-background construction
or extra action channel is used.

The literal normal channel responses of §9.22 remain unchanged; the star
pair source becomes `64*rho`. The necessary leading linear system is
uniformly invertible for real r and rho!=0 and fixes

```text
Gamma=-rho/(512*(r^2+1)),
c+d=(r^2-1)/(r^2+1), c-d=6*r/(r^2+1).
```

The necessary affine row sum is now `-128*rho*(r+1)/(r^2+1)`, independent of
all seven second amplitudes. It still forces r=-1. The q=0 chart remains
inconsistent. At r=-1, two actual rows force `z=-4` and
`q*(u-2)=rho/512`.

The complete solder-order-three range is recomputed with this unfixed
upper block and its actual tangent, not imported by specializing a
rho=1 result. The common modulus lambda cancels from the reduced necessary
system. Eliminating the rank-two solder image and all second-amplitude
quotient variables gives the same u(t) and p3,p4,p5,p7(t) of §9.22; the
second role-0 N3 amplitude is multiplied by rho. The un-divided t=2 range
obstruction remains 512. The uniform rank-five minor is
`536870912*rho^4`, and the determinant of leading solder is `-9*rho/2`.
All nonzero real upper scale ratios, including both signs, are retained.

For `D=5*t^2-78*t+8`, three literal necessary affine-order-four rows are

```text
row2=384*rho*(t-2)*(t+5*rho-1)/D,
row3=-64*rho*(5*t^2-6*t*rho-96*t+12*rho+44)/D,
row1=64*rho*(8*t^2*rho-t^2-132*t*rho-54*t+104*rho-16)/D.
```

Every solder-compatible second-amplitude freedom drops from these three
rows. D is a genuine unit because u=2 is already excluded. The first row
forces `t=1-5*rho`. The other two then require

```text
P=155*rho^2+436*rho-47=0,
Q=200*rho^3+555*rho^2+260*rho-71=0.
```

Their exact Bezout identity is

```text
(2738600*rho^2+8186615*rho+4368345)*P
 -(2122415*rho+6425073)*Q = 250867968.
```

Hence no real (or complex characteristic-zero) rho satisfies both.
The certificate checks the three literal response formulas, the final
polynomial substitutions and Bezout identity, all range dimensions, the
full lower affine mode forms, and all second corrections. This removes the
two apparent unequal-scale seams without a numerical reconstruction.

**Exact scoped verdict:** the entire normalized homogeneous critical-leading
solder class is excluded for the declared collinear mode-1100 translation
family, with all coefficients and both tangent moduli. Arbitrary vector
components of the translations, mixtures of modes, and finite amplitudes
away from this degenerate seed remain open. In particular this is still
not the broad finite-carrier terminal. Task `IN_PROGRESS`, PR Draft; L=3
remains unopened.


### 9.24 One e2/e3 component on role 0 or role 1

`a4d_resolved_curved_stationary_e2_role01_transverse_axis_check.py`
adds one translation coordinate to the §9.23 family, in the same occupied
mode 1100. The coordinate is `b0·e2`, `b0·e3`, `b1·e2`, or `b1·e3`.
Role 1's affine column is the negative of role 0's on all 16 rows, so
each role-1 axis repeats the corresponding role-0 axis with `sigma` flipped.
No new Fourier mode, no new channel, and no new solder modulus are
introduced. This section does not classify `e1` on roles 1, 2 or 3, nor
`e2`/`e3` on roles 2 and 3, nor `b1·e0`.

The owned polarization is recomputed for the five leading normal-link
generators. On indices `(2,3,6,7)`, every channel has zero pure square and
zero symmetric coupling to the collinear slots `b0·e0`, `b2·e0`, `b3·e0`,
identically in `(rho,u,t)`. The order-two channel form has the same zero
symmetric coupling, so the positive collinear observer norm still forces
the two observer coefficients to be opposite. Affine order-four columns
on these four indices vanish on rows 10, 11, 14 and 15. Section 9.23
reads `r=-1` from the sum of rows 10 and 15, `z=-4` from row 10 at
`r=-1`, and `q(u-2)=rho/512` from row 11 at that point. Those three
inputs are unchanged, and the reduced critical solder comes with them.
A direct collinear row-sum control reproduces
`-128*rho*(r+1)/(r^2+1)` before the new component is added. Role 0's `e1`
component, index 1, moves at least one of the five link responses. That
is a boundary check for one index, not a classification of every `e1`
component.

Write `den=5*t^2-78*t+8` and
`N1=8*rho*t^2-132*rho*t+104*rho-t^2-54*t-16`.
On the surviving reduction, rows 1 and 2 of the `e2` extension are cleared
for every tangent by

```text
sigma=-2*N1/(3*(t-2)*(t-1)),
```

together with an explicit rational `p(rho,t)` recorded in the certificate.
Row 3 does not see this component, so it remains the §9.23 numerator
`N3=5*t^2-6*rho*t-96*t+12*rho+44`. The `e2` chart is the locus `N3=0`,
outside `t=2`, `t=1`, `den=0` and `N1=0`.

The `e3` extension is rational in one modulus. Rows 1, 2 and 3 of the
actual jet vanish at

```text
t=1-5*rho,
sigma=4*(200*rho^3+555*rho^2+260*rho-71)/(125*rho^2+430*rho-47),
```

with `p` the explicit degree-five rational in the certificate. The
numerator of `sigma` is the §9.23 polynomial `Q`, so `sigma=0` is exactly
the already excluded collinear point. `Q` and the denominator are coprime.
The identity is the zero rational function on the chart `rho!=0`,
`rho!=-1/5`, `den!=0`, and both denominator factors nonzero.

Rows outside `{1,2,3,10,11,14,15}` are not evaluated in this
certificate. An order-1 shift of `K1` is not a column of the §9.23
second-amplitude quotient `Ka`, so no span in that quotient is claimed.
Whether `Ka` cancels those rows is untested. Link order three is untested.

**Exact scoped opening:** on this four-index extension, the §9.23 link
reduction survives and rows 1–3 have the explicit charts above. No finite
nondegenerate curved stationary witness is claimed, no L=3 control is
opened, and the task stays `IN_PROGRESS`. Directions not listed above stay
unclassified by this section.


### 9.25 The e3 chart dies in the Ka quotient

`a4d_resolved_curved_stationary_e2_role01_e3_ka_affine4_check.py`
takes the `e3` chart of §9.24,
`t=1-5*rho`, `sigma=4*Q/Dsig`, and the recorded `p`, with `r=-1` and
`z=-4`. The new translation slot is index 3, `b0·e3`. The weighted
column of `b1·e3` is the negative, so the opposite sign of `sigma` is
the same chart. No new Fourier mode and no new channel are added.

The second-amplitude columns are the owned finite differences
`resp(generator)-resp(0)` of §9.23, restricted to

```text
Ka = columns (1,0,0,0,0,0,0), (0,1,0,0,0,0,0),
      (0,0,0,1,1,0,0), (0,0,-1,0,0,0,1)
```

in the order `K1_0, K1_2, N2_2, N3_0, N3_1, N3_2, N3_3`.
On this chart that linear map is the zero 16×4 matrix. Rows 1, 2, 3,
5, 6, 7, 10, 11, 14 and 15 of the inhomogeneous term vanish. Row 4 is
minus row 0, row 9 is minus row 8, and row 13 is minus row 12.

The remaining numerators, after removing the chart factor `rho`, are
coprime: row 0 against row 8, and row 0 against row 12. The primitive
row-0 numerator is

```text
76625*rho^4 + 164450*rho^3 + 3760*rho^2 + 31582*rho - 9025.
```

It shares no factor with the chart denominators
`25*rho^2+68*rho-13`, `Q`, `5*rho+1`, or `125*rho^2+430*rho-47`.

The amplitude dependence at this jet order is quadratic, because the
order-4 contraction multiplies two order-2 jets. On the four `Ka`
directions the quadratic form has one nonzero piece: the square of the
last direction, raw value `32768` on observer channels of rows 8 and 12
and the opposite sign on rows 9 and 13. The two observer channels are
equal, so the opposite-observer weight `q` and `-q` cancels that piece.
Every cross term among the four directions is zero, and the other three
squares are zero. The weighted quadratic correction therefore vanishes
on rows 0, 8 and 12. The same weighted vanishing holds for the quadratic
self-energy of the solder particular amplitude and for its cross terms
with each of the four `Ka` directions.

Thus every amplitude of the form particular solution plus `Ka*y` leaves
rows 0 and 8 at their inhomogeneous values. Those two numerators have no
common zero on the chart. The `e3` extension has no affine order-4
solution in this quadratic calculus.

This no-go does not cover the `e2` axis, `e1`, role-2/3 transverse
components, `b1·e0`, other modes, or finite off-seed points. No
stationary witness and no L=3 result are claimed.


### 9.26 The owned e2 component dies on N3

`a4d_resolved_curved_stationary_e2_role01_e2_owned_affine4_check.py`
uses the same owned `resp` as §9.25, now on slots `b0·e2` and `b1·e2`.
The weighted `b1·e2` column is the negative of `b0·e2`. No new Fourier
mode and no new channel are added. The §9.24 expressions for `p` and
`sigma` are checked here rather than imported as a solution of a second
jet.

The transverse column of row 3 is identically zero. Rows 1 and 2 are
cleared by

```text
N1=8*rho*t^2-132*rho*t+104*rho-t^2-54*t-16,
sigma=-2*N1/(3*(t-2)*(t-1)),
```

with the same rational `p` recorded in the certificate. Row 3 remains
`-64*rho*N3/den`, where

```text
den=5*t^2-78*t+8,
N3=5*t^2-6*rho*t-96*t+12*rho+44.
```

At that `(p,sigma)` the linear map `(Cp+sigma*Ct)*Ka` is the zero 16×4
matrix, so the four `Ka` coordinates do not move row 3, row 0, or row 8.
Clearing row 3 on the finite-q chart therefore requires `N3=0`.

After the chart units `t-2`, `den`, `N1` and `rho` are removed, the
resultants in `rho` of the row-0 and row-8 numerators against `N3` have
gcd 1. The locus `N3=0` does not make those two rows vanish together.
`N3` at `t=2` is `-128`. At `t=1` the transverse row 1 vanishes, and
`N3(1)=0` forces `rho=47/6`, where the source row 1 is still nonzero.
The resultant of `N1` and `N3` shares no root with the collinear factor
`t+5*rho-1`, whose own resultant against `N3` is the §9.23 polynomial
`155*rho^2+436*rho-47`. On that seam `sigma` cannot clear row 1 unless
it is zero, and `sigma=0` then leaves row 2 nonzero. Also
`N3-den=6*(rho+3)*(2-t)`, so `rho=-3` makes the row-3 denominator the
same zero as `N3` and forces `u=2`, outside the finite-q chart.

The square of the last `Ka` direction does not meet the `e2` slot, and
its nonzero raw entries are equal on the two observer channels. It does
not restore row 0. Squares of the other three `Ka` directions, their
crosses on the `e2` slot, and the particular-amplitude self-energy on
`N3=0` are not remeasured here.

**Exact scoped no-go:** in the amplitude-linear `Ka` calculus, with this
one quadratic piece included, the role-0/1 `e2` extension has no affine
order-4 solution on the finite-q chart. `e1`, role-2/3 transverse
components, `b1·e0`, other modes, and finite off-seed points stay
unclassified. No stationary witness and no L=3 result. Task stays
`IN_PROGRESS`.


### 9.27 One-component openings off the four closed axes

`a4d_resolved_curved_stationary_e2_remaining_slots_affine4_check.py`
evaluates every mode-1100 component other than the collinear inputs
`b0·e0`, `b2·e0`, and `b3·e0`, on the §9.23 reduction
`r=-1`, `z=-4`, `u=ut(t)`, `q=qt(t)`, at the particular solder
amplitude. The thirteen components are `b0·e1`, `b0·e2`, `b0·e3`,
`b1·e0`, `b1·e1`, `b1·e2`, `b1·e3`, `b2·e1`, `b2·e2`, `b2·e3`,
`b3·e1`, `b3·e2`, and `b3·e3`. No new Fourier mode, no new channel,
and no new solder modulus are added. The owned affine row stays the
linear contraction of those components: `resp` does not take the
translation amplitude, and `response` multiplies each raw slot by
that amplitude once.

On this reduction the source vanishes on rows 10, 11, 14, and 15.
Row 14 is not an input to `r`, `z`, or `q(u-2)`; it vanishes after
that substitution. The source also satisfies row 4 = -row 0, row 5 =
-row 1, row 6 = -row 2, row 7 = -row 3, row 9 = -row 8, and row 13 =
-row 12.

For each of the thirteen components, `Ct*Ka` is the zero 16×4 matrix.
In this amplitude-linear calculus the solder quotient does not move
any affine row through these components. The four role-0/1 components
`b0·e2`, `b0·e3`, `b1·e2`, and `b1·e3` have zero columns on rows 10,
11, 14, and 15.

Each of the other nine has a witness row in {10, 11, 15} equal to a
nonzero integer times the chart unit `rho*(t-2)/den`, with
`den=5*t^2-78*t+8`:

```text
b0·e1 row 10 = -384,   b1·e0 row 10 = 384,   b1·e1 row 10 = -384,
b2·e1 row 15 = -768,   b2·e2 row 11 = 768,   b2·e3 row 10 = 768,
b3·e1 row 15 = 768,    b3·e2 row 10 = 768,   b3·e3 row 11 = -768.
```

The source of that row is zero and the `Ka` derivative in that
component is zero, so a one-component amplitude `sigma` leaves the
witness row equal to `sigma` times the unit. On the finite-q chart
`rho!=0`, `t!=2`, `den!=0`, the unit is nonzero, so `sigma=0`.

**Exact scoped no-go:** one component at a time, any of those nine
slots has no nonzero amplitude on the §9.23 finite-q reduction in the
amplitude-linear calculus.

The rational 4×13 matrix of those source-zero rows has rank 3 over the
function field. The denominator lcm of each row is `den`, and `den`
times the matrix has the same rank and nullity 10 over that field. The
ten vectors below are linearly independent for every `t!=2`, so on the
finite-q chart the kernel dimension is at least 10, and it equals 10
wherever the specialized rank remains 3. One basis of the function-field
kernel, checked
as rational products `A*v=0`, is the four pure axes `b0·e2`, `b0·e3`,
`b1·e2`, `b1·e3`, the mixtures `b0·e1+b1·e0`, `-b0·e1+b1·e1`,
`-4*b0·e1-b2·e1+b3·e1`, `4*b0·e1-b2·e2+b3·e3`, and

```text
Q4/(72*(t-2)^2) b0·e1 - ut*b2·e1 + (ut/2)*b2·e2 + b2·e3,
R4/(72*(t-2)^2) b0·e1 + ut*b2·e1 - (ut/2)*b2·e2 + b3·e2,
```

where `ut=-(5*t^2-90*t+32)/(6*(t-2))` is the owned tangent,
`Q4=25*t^4-660*t^3+3764*t^2+3840*t-1472`, and
`R4=-(25*t^4-660*t^3+3476*t^2+4992*t-2624)`. The four pure role-0/1
axes of §§9.24–9.26 sit in this kernel. Rows 1, 2, and 3 do not see
`Ka`, either through the owned collinear block or through these
thirteen components. The image of this kernel on those three rows has
rank 3, the full codomain over the function field, so the source is
hit and the solution space has dimension 7 over that field. That family is not
constructed here. Rows 0, 8, and 12, where `Ka` still acts, are not
solved over the function field. Section 9.28 tests those rows together
with their sign partners at three chart points.

Quadratic solder self-energy in these thirteen slots is not
remeasured. Other Fourier modes and finite off-seed points stay open.
No stationary witness and no L=3 result. Task stays `IN_PROGRESS`.


### 9.28 The kernel is consistent at three chart points

`a4d_resolved_curved_stationary_e2_kernel_rows0812_affine4_check.py`
keeps the §9.27 reduction, the thirteen mode-1100 components, and the
ten-dimensional function-field kernel of rows 10, 11, 14, and 15. The
four `Ka` coordinates are added. No new Fourier mode, no new channel,
and no new solder modulus are added. The tested system is the twelve
affine rows that are not those four source-zero rows, so the matrix is
12×14.

Every one of the thirteen translation columns satisfies row 6 = -row 2,
row 7 = -row 3, row 9 = -row 8, and row 13 = -row 12. The four closed
axes `b0·e2`, `b0·e3`, `b1·e2`, and `b1·e3` also satisfy row 4 = -row 0
and row 5 = -row 1. The other nine columns do not. Collinear `Ka` is
zero on rows 1, 2, 3, 10, 11, 14, and 15, and it satisfies row 4 =
-row 0, row 9 = -row 8, and row 13 = -row 12. Those sign facts stay in
the certificate; the twelve rows are still all present in the rank.

At the three finite-q points `(rho,t,p)=(1,0,0)`, `(1,3,1)`, and
`(2,4,0)`, the specialized system has rank 6 and the augmented matrix
has the same rank. At `(1,0,0)` there is an exact rational particular
solution, and the nullspace has eight independent vectors. At the other
two points the same count, fourteen columns and rank 6, gives solution
dimension 8.

These are three rational points. A specialization can drop rank, so
they do not prove that the generic rank is 6. They do prove that the
generic rank is at least 6, and that the amplitude-linear system is
consistent at these three points. The §9.27 count of seven kernel
parameters was the kernel alone after rows 1, 2, and 3, before these
twelve rows and before `Ka`.

Quadratic solder self-energy is not remeasured. The full Euler is not
tested. No stationary witness and no L=3 result. Task stays
`IN_PROGRESS`.


### 9.29 The line rho=1, p=0 has rank 6

`a4d_resolved_curved_stationary_e2_kernel_field_rank_affine4_check.py`
uses the same 12×14 matrix. Four sign identities hold over the whole
function field, including the right-hand side and collinear `Ka`:
row 6 = -row 2, row 7 = -row 3, row 9 = -row 8, and row 13 = -row 12.
Collinear `Ka` also satisfies row 5 = -row 1, row 6 = -row 2, and
row 7 = -row 3. The twelve rows therefore repeat eight rows:
0, 1, 2, 3, 4, 5, 8, and 12.

On the line `rho=1`, `p=0`, rows 0, 1, 2, 3, 8, and 12, in the six
kernel columns

```text
b0·e2, b0·e3, b0·e1+b1·e0, -b0·e1+b1·e1,
-4*b0·e1-b2·e1+b3·e1,
Q4/(72*(t-2)^2) b0·e1 - ut*b2·e1 + (ut/2)*b2·e2 + b2·e3,
```

have a minor which is not identically zero. At `t=0` the minor is
nonzero. As a function of `t` it is a degree-22 numerator over
`81*(t-2)^5*den^6`, with `den=5*t^2-78*t+8`. Rows 4 and 5 lie in the
span of those six rows. A particular solution supported on those six
columns, with the four `Ka` coordinates equal to zero, clears all
twelve rows identically in `t`. Where the minor is nonzero the rank is
6, so the solution dimension is 8. The same rank and consistency hold
at the further points `(1,6,0)` and `(3,6,4)`.

The degree-22 factor is not solved. This particular solution is not
claimed at those roots. The identity is on `rho=1`, `p=0`, not on the
whole `(rho,t,p)` field. `Ka` is zero in this particular solution; the
homogeneous solution was not computed. Quadratic solder self-energy
and the full Euler are not tested. No stationary witness and no L=3
result. Task stays `IN_PROGRESS`.


### 9.30 Six rows remain over the function field

`a4d_resolved_curved_stationary_e2_kernel_field_span_affine4_check.py`
uses the same 12×14 matrix. The raw nine slots still break
row 4 = -row 0 and row 5 = -row 1. After projection onto the
ten-dimensional kernel, and after adding collinear `Ka`, those two
signs are restored, and the right-hand side follows them. Together
with the four signs of §9.29, every one of the twelve rows is plus or
minus one of

```text
0, 1, 2, 3, 8, 12.
```

Those six rows meet the six kernel columns of §9.29 in a minor that is
not the zero rational function: its value at `(rho,t,p)=(1,0,0)` is
nonzero. Where this 12×14 matrix is defined and the minor is nonzero,
its rank is 6. The square subsystem on those columns is then
invertible, so setting the other eight coordinates to zero, including
all four `Ka` coordinates, solves it. The matching signs carry that
solution onto the other six rows. The solution dimension of this
12×14 system is then 8. That count keeps the ten kernel coordinates
independent, so it does not cover the locus where rows 10, 11, 14,
and 15 drop rank. The zero locus of the minor is not factored. The homogeneous
solution, which may use `Ka`, is not computed. Quadratic solder
self-energy and the full Euler are not tested. No stationary witness
and no L=3 result. Task stays `IN_PROGRESS`.


### 9.31 The quadratic jet vanishes at (1,0,0)

`a4d_resolved_curved_stationary_e2_kernel_quadratic_point_affine4_check.py`
specializes §9.30 at `(rho,t,p)=(1,0,0)`. The six pivot coordinates are

```text
(0, 0, -4, -4, 1, 0)
```

on the kernel columns `b0·e2`, `b0·e3`, `b0·e1+b1·e0`,
`-b0·e1+b1·e1`, `-4*b0·e1-b2·e1+b3·e1`, and the `Q4` column. The other
eight coordinates are zero. The particular solder amplitude is

```text
(0, 0, -10/3, -8/3, 0, 4/9, 0).
```

`resp` at that amplitude, minus `resp(0)` and minus the linear column
sum, weights to zero on rows 0, 1, 2, 3, 8, and 12 under this
translation. The same remainder stays zero along the four free `Ka=0`
translation directions. Each of the four `Ka` directions has zero
cross with the particular amplitude and zero square on those rows, and
every pairwise `Ka` cross is zero, all weighted by this same
translation. The quadratic polynomial in the four `Ka` coordinates
therefore vanishes on the six rows at this translation and this
modulus point.

Crosses between the four free translations and the `Ka` directions are
not remeasured. The test is one modulus point, not the function field.
The untruncated Euler is not evaluated. No stationary witness and no
L=3 result. Task stays `IN_PROGRESS`.


### 9.32 Free-translation polarizations of the quadratic jet

The §9.31 certificate now also contracts every quadratic polarization with
each of the four free `Ka=0` translation vectors, the columns 4, 5, 7, and 9
of `BK` at `(rho,t,p)=(1,0,0)`. Their 13-component matrix has exact rank 4.
The particular amplitude, pivot translation, four `Ka` directions, channel
coefficients and six projected rows are unchanged.

For each free translation the additional checks are:

- four particular-amplitude / `Ka` cross terms;
- four `Ka` squares;
- six pairwise `Ka` cross terms.

Thus 56 additional six-component contractions vanish exactly. The square
and pair contractions are needed as well as the 16 particular/`Ka` cross
terms: those 16 alone would not establish the polynomial statement.
Together with §9.31, the amplitude-quadratic remainder is zero on these six
rows for the particular translation plus an arbitrary linear combination
of the four free translation vectors, and for arbitrary coefficients of
the four `Ka` directions, at this one modulus point. Translation enters
linearly. The order-four affine Euler used by `resp` is at most quadratic
in the order-two amplitude: its products are of jet degrees `(1,3)`,
`(2,2)` and `(3,1)`. The constant remainder and all its quadratic
polarizations therefore cover the whole stated polynomial.

This describes the projected quadratic remainder, not a solution of the
complete Euler system for eight arbitrary parameters. It adds neither an
untruncated Euler evaluation nor a function-field identity. The solder
self-energy and missing orders must still be included before claiming
stationarity. No finite curved stationary witness, broad L=2 no-go or L=3
result is obtained. Task remains `IN_PROGRESS`.

Validation: the extended exact checker completed with exit 0 in 504.86 s.
All 56 new six-component contractions and the rank-4 coverage assertion
passed. The CI timeout is explicitly bounded at 1200 s.

### 9.33 Conditional effective-response bridge and its missing hypotheses

The supplied D0-to-GR blueprint is retained here as a conditional bridge,
not as three established continuum theorems. This section does not change
#202's action, carrier, terminal criterion or task state. Its scope is the
relation between finite stationary certificates and a possible effective
metric response.

#### Fixed-metric stationary homotopy, rather than total connectedness

On a finite carrier write `E_Q=partial_Q S`, `E_Y=partial_Y S`. If a
C1 section `Y(Q)` is exactly connection-stationary, the chain rule gives

\[
D_Q S(Q,Y(Q))=E_Q(Q,Y(Q))+(D_QY)^*E_Y(Q,Y(Q))
                =E_Q(Q,Y(Q)).
\]

This identity does not by itself make the response independent of the
chosen stationary section. A sufficient additional hypothesis is a C1
family `Y_s(Q)`, `s in [0,1]`, on one open set of metric data, such that
`E_Y(Q,Y_s(Q))=0` for every fixed `Q` and every `s`, with the two sections
as endpoints. Then

\[
\partial_s S(Q,Y_s(Q))=E_Y(Q,Y_s(Q))\cdot\partial_sY_s(Q)=0.
\]

The two effective actions are equal for every `Q` in that open set.
Differentiating that equality and using the chain rule proves equality of
their metric responses. This conditional finite-dimensional lemma requires
no uniqueness of `Y` and no inverse Hessian. Neither a fixed-flat-metric
path alone nor connectedness of the total set `{(Q,Y):E_Y=0}` supplies its
hypotheses.

An explicit algebraic control is

\[
S(q,y)=(y^2-q)^2,\qquad E_y=4y(y^2-q),\qquad E_q=2(q-y^2).
\]

The stationary set `y=0` together with `q=y^2` is connected through the
origin. For any `q>0`, the two smooth stationary sections `y=0` and
`y=sqrt(q)` have responses `2q` and `0`, respectively. They cannot be
joined inside the stationary fibre at that fixed `q`. Thus total
connectedness cannot replace the fixed-metric homotopy hypothesis.

For an approximate section, the term `(D_QY)^*E_Y` remains. To discard it
after `h^-2` normalization one must bound that product in the chosen norm;
a high-order Euler residual without control of `D_QY` is insufficient.
This is particularly relevant to the resonant/degenerate charts of #202.

#### Owned inputs and live gates, pinned 2026-09-27

Canonical main at this audit is
`12d10427e3ba81e5c8acfbd5a6fc47f0a2c6d428`. Live PR results below are
checkpoints, not merged owners.

| Input / execution | Established scope | Remaining bridge |
| --- | --- | --- |
| Merged [#273](https://github.com/gvakhrushev/d0_15/pull/273) and [#298](https://github.com/gvakhrushev/d0_15/pull/298) | `K_Schur=-1/2 K_G^(1)` coefficientwise in all 100 flat-symbol entries; polynomial Bianchi; direct `D0.All` Lean import. PR #298 merged at main `12d10427e3ba81e5c8acfbd5a6fc47f0a2c6d428` after Lean build and guards passed. | Nonlinear variable-metric identification and controlled limit remain open. This is the exact flat linear-symbol theorem only. |
| Merged [#270](https://github.com/gvakhrushev/d0_15/pull/270) and [#296](https://github.com/gvakhrushev/d0_15/pull/296) | `C(1)=0`; for nonzero complex `d`, rank `C=9`, kernel `span(dd^T)`; raw second forcing `F2=-(d^T eta d)/4 C(d odot d) vec_sym(dd^T)` | `dd^T` is Veronese; null/Kerr–Schild interpretation requires the additional null condition. Raw `d=O(h)` scaling is not a normalized field-response estimate. |
| Live [#299](https://github.com/gvakhrushev/d0_15/pull/299), head `c791b051f0e36ff615d74a30dd20b50a7f60a901` | The physical orbit-5/7 matrices have rank 23 and a genuine one-dimensional cross-character cokernel; raw residual squares are `(8/5,8/5,0,0)` and `(2,0,0,2)`. Unit-`q0` squares are `(1/25,1/25,0,0)` and `(1/46,0,0,1/46)`. All eight same-carrier moving-germ classes have explicit image witnesses. | The nonzero class freezes the metric section while changing the character. It is a carrier-mismatch diagnostic, not a stationary-sheet stress. The PR is open in REVIEW; GitHub currently reports no checks on this head. Its body records a prior Lean timeout in the large inverse reductions, so do not call this module Lean-validated. No square-root-of-13 monodromy follows from a raw basis pairing. |
| Live [#285](https://github.com/gvakhrushev/d0_15/pull/285), head `ea8aeb4910b2726f7cab84f31115a5311a50fb1b` | Mode B `(-1,1,-1,1)` is an exact identity-link joint vacuum for every real epsilon. On the selected mode-A branch `(i,i,-i,-i)`, the second forcing is solved; with zero order-epsilon link tangent, the order-epsilon-cubed connection forcing lies outside the rank-20 vacuum Hessian. | This stops that selected branch at the stated order; other initial kernel tangents remain open. It is not a metric-stress result, physical no-go, or closure of the mode family. No slow-packet estimate follows from these two characters. |
| Live [#240](https://github.com/gvakhrushev/d0_15/pull/240), `2c98fbed57976c749d7374af13352cabb0003270` | Partial terminal `SHEAR-PERIOD-2-SLOW-ENVELOPE-KILLS-AMPLITUDE-GAP-ZERO`: `-432u^5` cuts the period-2 amplitude; the bounded periodic slow envelope is zero | Other admissible microstructures remain open. The unattained stress is not an owned curvature-squared term. |
| Merged [#232](https://github.com/gvakhrushev/d0_15/pull/232), [#241](https://github.com/gvakhrushev/d0_15/pull/241), [#259](https://github.com/gvakhrushev/d0_15/pull/259); live [#275](https://github.com/gvakhrushev/d0_15/pull/275), `663292f88e6107a6566cf93ecd76f61ad113c176` | Explicit curved Y family and slow profile; corrected connection-stationary response through the claimed orders; next range correction reduces the residual freedom to the real COS/SIN shell of `N0=span(lambda1,lambda3,lambda4,lambda6)` | The selected #260 degree-6 even correction below is a quarter-wave amplitude jet, not the #275 `z=h` response. The slow-profile nonlinear cross term and same-source ten-slot comparison remain uncomputed. No exact same-source joint solution is asserted. |
| Live [#260](https://github.com/gvakhrushev/d0_15/pull/260), head `13c78b7d758da48723328ba3f45d9e4ec1a083c3` | On the selected line `u=(0,0,1,1)` in `N0`, corrected COS/SIN rays have all scalar, connection, and metric Euler terms zero through degree 5. Both degree-6 even forcing blocks have rank-24 Hessians and exact regular corrections; the corrected degree-6 metric Euler vanishes in all ten slots. | This is one line in the four-dimensional `N0`, not a classification of `F6[N0]`. The degree-7 odd resonant connection Euler is missing. The worker remains BLOCKED/Draft. Degree 5 or 6 does not establish torsion freedom or a slow-limit theorem. |
| This [#202](https://github.com/gvakhrushev/d0_15/pull/202), §§9.30–9.32 | Six projected affine rows, function-field rank-6 chart and the enlarged quadratic-remainder cancellation at one point | Full solder self-energy, untruncated joint Euler, minor zero locus and other admissible deformations. No curved stationary witness. |

#### A response gap must be computed in its own variables

The finite quarter-wave coefficient below and the slow-background response
are different maps. To close #275, evaluate the corrected Y profile on its
pinned `z=h` background, differentiate the same fixed-source action in the
ten metric slots, and compare against the independently fixed #216 response.
The degree-six calculation only reduces one candidate correction; it is not
a substitute for that comparison.

##### Degree 6 on the selected real line: a solved image, not a stress

PR #260 now supplies the exact degree-6 coefficient on the selected quarter-
wave line `u=(0,0,1,1)` of the four-dimensional `N0`, with its real COS and
SIN dressings. This supersedes the earlier statement that degree 6 was
uncomputed on these two rays. It does not classify arbitrary `u` in `N0`.

For COS, the 24-component character-`(-1)` forcing, grouped by Role in six
Lorentz-generator coordinates, is

```text
(0,-20/3,-20/3,-4,-4,0),
(0,  4/3, 4/3,-4/3,-4/3,0),
(0,0,0,0,0,0),
(0,0,0,0,0,0).
```

The zero-character forcing is its negative. Both 24x24 even Hessians have
rank 24, so these forcings lie in their regular images, with no cokernel.
The exact corrections for both characters are

```text
Role 0: (0,-1/96,-1/96, 1/96, 1/96,0)
Role 1: (0,-1/96,-1/96, 1/96, 1/96,0)
Role 2: (1/192,0,0,0,0, 1/64)
Role 3: (1/192,0,0,0,0,-1/64).
```

For SIN, both forcing blocks are the negative of the COS character-`(-1)`
forcing. Its character-`(-1)` correction is the negative of the four vectors
above; its zero-character correction is the same four-vector profile.
Substitution into the same finite action's constant-solder metric variation
gives, for each real dressing,

\[
E_Q^{(6)}=(0,0,0,0,0,0,0,0,0,0)\in\mathbb Q^{10}.
\]

This is the requested concrete reduced-response substitution at order six
on those two rays. If `Phi` denotes the regular-harmonic-eliminated action
jet, its metric derivative on the checked rays is this zero vector. This
notation names only that coefficient calculation; no repository owner yet
defines an all-orders `Phi` on a slow continuum background. The first result
is a regular-image connection lift whose metric coefficient cancels, not a
nonzero stress and not a proof for all of `N0`.

The first next coefficient on this selected ray is the degree-7 odd resonant
connection Euler. It is not computed in the current certificate. The zero
metric vector at degree six does not show that this next equation is
solvable. The full four-coordinate germ, any other resonant harmonics, and
finite-curvature continuation remain open.

The #260 germ amplitude `epsilon` and #275's slow scale `h`/valued parameter
`z_h=h` are different variables. Their matching, and any singular amplitude
or inverse growth, must be derived before assigning a power of `h` to a
coefficient. Even if a bounded metric coefficient genuinely occurred as
`h^6 F6`, its normalized contribution would be `h^4 F6 -> 0`; a nonzero
coefficient alone would not prove a finite response gap. Merged #296 owns the
specified second-order Gram-slice forcing; it does not by itself establish a
universal recurrence `F_n proportional to C(d(z^n)) vec_sym(dd^T)` or its
claimed power counting for every harmonic and smooth packet.

For the selected slow background and the designated comparator with its
realization and source prescription fixed independently, define the target
comparison explicitly:

\[
\mathcal R_h=h^{-2}\bigl(E_Q(Q_h,Y_h)-E_Q^{\rm des}(Q_h)\bigr),
\qquad Q_h=\eta+h\alpha+h^2x_0\beta.
\]

The connection-stationary candidate must first be constructed, with the
same fixed data as the comparator. Choosing a source after the candidate
is built would make a joint-response test tautological. The #216
parametrix has a super-algebraic full Euler residual; it is not yet an
exact full stationary section. Its designated coefficient remains
conditional on the stated coupled normal-rescue and response estimates.

No additive decomposition into independent `R_sm`, `R_q0`, `R_sh` and
`R_Y` is claimed: mixed nonlinear terms and completeness of the admissible
class have not been controlled. Vanishing of this one Y comparison would
close a scoped bridge, not exhaust all stationary leaves. A nonlinear GR
limit still needs existence/refinement control, the response norm and
uniform remainder bound, and the nonlinear designated identification.
The present memo proves neither `Y=Gamma_LC` nor
`S_eff=int sqrt(-g) R+O(h^4)`.

#### Execution order, without duplicate branches

1. Continue #260 from the solved degree-6 even corrections on its selected
   line: compute the degree-7 odd resonant connection Euler, then extend to
   the other coordinates of `N0` if the worker's full four-space objective
   is retained.
2. #275 must separately substitute its corrected #232 Y profile on the
   pinned `z=h` slow background, against the fixed #216 comparator. The
   quarter-wave epsilon jet supplies no amplitude-to-`h` map by itself.
3. Keep #240's shear partial terminal and #285's selected-branch cubic
   obstruction in their declared carriers. Neither exhausts other channels.
4. #202's full-Euler finite-carrier gate remains separate. #267's
   executable `E_sp` owner must be accepted and merged before #265's
   dependency gate opens.

This is a dependency map for existing tasks, not registration of new work
or a retirement of any still-open task.


### 9.34 Two distinct cokernel questions and the updated degree-six result

The latest controlled checks separate two objects that the proposed synthesis
had called one germ stress.

First, on the physical unit torus in live PR #299, the matrix pairs `A(z)`
with `C(conj(z))`. On the declared orbit types 5 and 7 its rank is 23 and its
one-dimensional cokernel is real algebra. Frozen-section cross-character
residual squares are exactly `(8/5,8/5,0,0)` and `(2,0,0,2)`; after unit-`q0`
normalization they are `(1/25,1/25,0,0)` and `(1/46,0,0,1/46)`. The same PR
constructs image witnesses for all eight same-carrier transported classes.
Thus these nonzero norms measure the frozen-section / moving-character
mismatch. They are not the source-fixed metric Euler of a stationary-sheet
continuation. The raw `l^T w` and basis norm `|3+2i|^2` are not invariants of
the normalized cokernel class. PR #299 remains an open REVIEW execution, and
its reported Lean proof timed out in the large inverse reductions; treat the
exact equations and witnesses as a live research result, not a validated
formal module.

Second, the #260 quarter-wave test uses the connection amplitudes in
`N0=span{lambda1,lambda3,lambda4,lambda6}`. For the particular direction
`u=(0,0,1,1)`, its COS and SIN dressings have the degree-six even connection
forcing in two regular 24-component character blocks. Each Hessian has rank
24, the exact corrections solve both systems, and the resulting ten-component
metric Euler is zero. This is a different calculation from the physical
orbit-5/7 cokernel. It supplies no all-orders stress theorem and no response
on the slow profile.

For this selected line, therefore, the proposed three-way classification of
the measured degree-six connection forcing is settled: it is a nonzero
regular image (in both even channels), not a cokernel class. The associated
metric coefficient, after the solved correction, is zero. The classification
has **not** been proved for every vector or every combination in the full
four-dimensional `N0`; nor does the degree-six result solve the degree-seven
odd equation. This partial positive result narrows the remaining test. It
does not justify the proposed exhaustive three-channel decomposition,
`h^{-2}E_Q + 1/2 G = R_Y + o(1)` for all realizable sequences, or the claim
that every continuum stress has been assigned.

The only justified substitution into a reduced response at this checkpoint
is the literal finite one in §9.34's degree-six calculation:

\[
D_Q\Phi^{[6]}\big|_{u=(0,0,1,1),\,COS}=0_{10},\qquad
D_Q\Phi^{[6]}\big|_{u=(0,0,1,1),\,SIN}=0_{10},
\]

where `Phi^[6]` denotes only the regular-harmonic-eliminated coefficient of
the owned finite action on these rays. No all-orders slow-background
functional \(\Phi\) is owned, so this equality cannot be substituted into
#275's \(z_h=h\) response. The requisite amplitude/scale map and same-source
comparison still have to be computed there.
