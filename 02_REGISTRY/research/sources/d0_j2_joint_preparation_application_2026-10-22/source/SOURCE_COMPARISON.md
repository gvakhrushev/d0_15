# Same original all42 carrier: addressed Book J2 source, corrected field point, and the remaining full-source equation

22 October 2026. Read-only repository inputs pinned to
`af6e7eb8952564d86ddbfe910eb5f41d4a1b4e4b`, existing Draft #334,
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`.
Isolated practical calculation; no repository, Book, physical action selection,
or acceptance flag was changed. `GR_closed=false`.

## 1. Which actual operator component is being continued

The source carrier is exactly the original two-cell/three-node rational collar
at

`h=0.183801524658179446663931692878752644250497528167344843803260291378571211`.

All 16 coframe, 24 proper Lorentz-link and two real CAR coordinates are varied.
The unchanged six based G2STAR plaquettes, the original sigma-minus reporter,
tau=1/20, fixed positive PF weights (1,1), and both temporal matter differences
are retained. This is neither the separate h=1/4 root nor the n20/256-address
coherent READY execution nor the sequential CAR16/full128 boost fixture.

The exact original source files and Git blobs are:

| Source | Git blob |
|---|---|
| `sources/d0_full42_interval_banach_2026-10-22/certified_model.py` | `6d5b41ce11a941fde95e722e708ebb02d689985c` |
| Same directory `inputs.py`, with hash-verified exact rational collar | `2c12d84fb3454dbf3cda6d71852d0cd4e57e1f65` |
| `sources/d0_original_unpadded42_2026-10-22/certified_unpadded.py` | `a8bcb1a32be09d1b45b8626278e014e7288bce2f` |
| Same directory `center_new.json` | `6b520fbd6218444601d90d7e30b738f8c828bd22` |
| `A4D_ORIGINAL_UNPADDED_N1_J2_ALL42_BRINKMANN_WELD_2026_10_22.md` | `3750cc13e7a82b75bd6a65c15994b96b38476182` |

The last owner, Section 2, already identifies the original displayed two-tick
Book feedback block with the SAME two native reporter operands. With
`p=phi^-1`, `zeta=2^-20`, and cell index j,

\[
E_j=p^2(1+x_j),\quad L_j=4E_j(1-E_j),\quad
b_j=p-p^2y_j,\quad B_j=4b_j^2(1-b_j^2),\quad
A_j=L_j+(1-L_j)B_j,
\]
\[
r_j=\zeta(A_j+B_j)-\zeta^2A_jB_j,
\qquad
J_2=-528\sum_{j=0}^1[\log(1-\zeta A_j)+\log(1-\zeta B_j)].
\]

Consequently

\[
\boxed{(1-\zeta A_j)(1-\zeta B_j)=1-r_j,
\qquad J_2=-528\sum_j\log(1-r_j).}
\tag{1}
\]

The two eigenbands A and B each remain in [0,1] on the native chart.
The combined click r can exceed zeta: it is the OR probability of TWO
zeta-thinned queries. No identification `r=zeta*f` with one complementary
eigenvalue f is being made, and no fugacity was changed to one. The original
528 multiplicity is consumed from the displayed two-band operator owner.
This owner does not identify its configured local feedback with every term
of the complete physically selected Book03 price.

## 2. Source units and exact residual on the original chart

Let `h_phi(r)=-[r log r+(1-r)log(1-r)]/log(phi)` and let nu be the ORIGINAL
fixed normalization in `certified_model.py`. The unpadded source is

\[
S_0=\nu\sum_j[h_\varphi(r_j)-h_\varphi(r_{\rm ref})
                         -(r_j-r_{\rm ref})].
\]

To express the two Euler covectors in the same source unit use the single
constant derived at the already owned common-null report:

\[
\boxed{
a_J=\frac{\nu[h'_\varphi(r_{\rm ref})-1](1-r_{\rm ref})}{528}
=-1904017.7665841860862614934962084559607001092852336835\ldots .}
\tag{2}
\]

This is a constant normalization for comparison of equations, not a new
physical coupling fitted at the new point. Multiplication by this nonzero
constant does not change the zeros of the genuine J2 source.

At arbitrary fields on this SAME chart, the entire additional feedback
covector relative to the original unpadded source is explicitly

\[
\boxed{
R^{J}_y=a_Jd_yJ_2-d_yS_0
=\sum_j\left[
\frac{528a_J}{1-r_j}-\nu(h'_\varphi(r_j)-1)
\right]d_yr_j.}
\tag{3}
\]

No projection to one material component, averaging of the two addresses,
or freezing of 41 other equations occurs. Equation (3) is evaluated as a
42-component covector in `J2_SOURCE_AT_UNPADDED.json`.

The high-precision initial values are approximately

\[
(r_0,r_1)=(1.851273046769266,\ 1.851234682506386)10^{-6},
\]
\[
\partial_{40}r_0=-3.522176118223356\ldots\,10^{-8},\qquad
\partial_{40}r_1=+3.52217037918975\ldots\,10^{-8},
\]
\[
\|dJ_2\|_\infty\simeq3.0302867\,10^{-11},\qquad
\|R^J_y\|_\infty\simeq5.7697197\,10^{-5}.
\tag{4}
\]

The maximum occurs at zero-based coordinate 40, the first freely varied CAR
amplitude. The original unpadded center is stationary to its already
certified precision; its nonzero J2 residual is not a rounding artifact.
The earlier strict h0 Book mismatch owner also encloses this raw component
between `-3.779e-11` and `-2.282e-11` at the exact original root.

Thus the 1e-22 sufficient additional-source budget around the old root does
not apply to this source replacement. It does not follow that the new
equations have no root.

## 3. Actual all42 continuation to a different nonflat field point

Use a homotopy only as a numerical construction:

\[
S_\lambda=(1-\lambda)S_0+\lambda a_J(J_2-J_{2,\rm ref}),
\qquad 0\le\lambda\le1.
\tag{5}
\]

Ten successive all42 solves at lambda=0.1,...,1 converged. The source
normalization is fixed throughout. At lambda=1 the unpadded functional
disappears entirely and the solved equations are exactly `d_42 J2=0`.
No half-measured or modified information rule is asserted by this homotopy.

High-precision refinement evaluates the UNCHANGED original scalar constructor
to recover both clicks, replacing only its final scalar consumer by (1).
At 100 decimal digits the refined numerical gradient in the comparison units
is `1.06462919160356e-69`. The separate
[endpoint proof](../certificate/ENDPOINT_PROOF.md) then establishes existence
by outward interval arithmetic on every one of the 1764 Hessian entries.
Its full first-source upper bound is below `8.011e-67`, contraction is below
`0.000143095`, and center drift is below `2.402e-65`. Banach therefore proves
a unique exact real zero of all 42 literal J2 equations in the radius `1e-30`
ball about the proposed rational center. This does not certify the whole
numerical continuation path, which is unnecessary for endpoint existence.

The new 90-digit rational candidate is in
[`J2_CENTER_HIGH_PRECISION.json`](../certificate/J2_CENTER_HIGH_PRECISION.json).
Its displacement from the original unpadded center is

\[
\boxed{\|y_{J,c}-y_{0,c}\|_\infty
=8.6411107401628749306947521526\ldots\,10^{-7}.}
\tag{6}
\]

At that candidate,

\[
r_0=1.8512730484670064507467187053674003\ldots\,10^{-6},
\quad
r_1=1.8512346808086468142566117359975115\ldots\,10^{-6}.
\]

The unchanged actual field geometry gives

| Geometric or matter quantity | Numerical value |
|---|---:|
| det(e) | 1.5256645603816626752 |
| Actual based plaquette `(P12)[1,2]` | 0.00202101740548772637 |
| First-cell temporal derivative of psi1 | 0.0881179660940935337 |
| Original transverse psi2 derivative | 0.1461251182078218756 |
| r0-r1 | 3.83676583596364901e-11 |

These are actual coframe/holonomy/CAR quantities from the same original
constructor. The new solution is not obtained by changing the collar,
zeroing the matter, or restricting to the old one-parameter pure-boost
subspace. Its original six-face/source geometry is fully retained.

The independent interval congruence check proves inertia 16 negative/26
positive for the constant-normalized feedback throughout the new root ball.
Its signed diagonal-dominance margin exceeds 0.04308485257 after allowing
the entire Hessian variation on the ball. Raw J2 has 26 negative/16 positive
directions because a_J<0. In particular the new field root is a strict
nondegenerate saddle and the local degree of its gradient is +1.
No proof on an unexamined box covering the entire continuation path is used.

## 4. What remains in the true complete Book03 covector

The new point closes the displayed feedback equations. It must not be
promoted to a complete H+J+R root without computing the remaining source.
On ONE genuinely identified finite execution let

\[
\mathscr B_{\rm actual}=H_{\rm actual}+J_{\rm actual}+P_{\rm rest},
\quad
H_{\rm actual}=\beta^{-1}\log\operatorname{Tr}e^{-\beta\Delta_N},
\quad
J_{\rm actual}=-\log\det(I-\zeta F_N).
\]

Here `P_rest` denotes only the additional contributions actually required
by that execution's already selected full price. It is not a new price
term to choose. For the bare Section 03.25 bootstrap it is absent. If a
complete paid-history binding supplies additional Info/work/clock/input
terms, those terms and their overlaps must be identified before addition.
In particular the native 0/10 expected charge cannot be counted a second
time by appending S0 to the feedback.

For fixed beta,zeta and constant finite ranks put
`sigma_beta=e^(-beta Delta_N)/Tr e^(-beta Delta_N)` and
`J_extra=J_actual-J2`. The exact full42 comparison is

\[
\boxed{
a_Jd_y\mathscr B_{\rm actual}-d_yS_0
=R^J_y+a_J\left[
-\operatorname{Tr}(\sigma_\beta\,d_y\Delta_N)
+d_yJ_{\rm extra}+d_yP_{\rm rest}\right].}
\tag{7}
\]

At a verified new J2 critical point, the remaining complete equation is

\[
\boxed{
d_y\mathscr B_{\rm actual}
=-\operatorname{Tr}(\sigma_\beta\,d_y\Delta_N)
 +d_yJ_{\rm extra}+d_yP_{\rm rest}=0.}
\tag{8}
\]

For every independently admitted preparation/controller/clock coordinate u,
the separate equation is still

\[
-\operatorname{Tr}(\sigma_\beta\,d_u\Delta_N)
+d_uJ_{\rm actual}+d_uP_{\rm rest}=0.
\tag{9}
\]

For moving beta,zeta add the actual terms
`-S(sigma_beta) d beta/beta^2` and
`Tr[(I-zeta F_N)^(-1) F_N] d zeta`. Fixed integer caps and ranks do
not generate fictitious continuous Euler rows.

Equations (7)-(9) identify the still missing data precisely: the actual
same-run maps `Delta_N(y,u)` and `F_N(y,u)`, including all field-dependent
complement blocks, the selected retained information algebra and complete
paid leaf costs, and their actual field/preparation writer. A value of a
different boost-only instrument source supplies none of these 42
Jacobian columns by itself.

## 5. The new stopped-quantum and one-mean owners do not fill those rows by substitution

The stopped full128 source owner has a complete finite-cap identity on ITS
actual retained CAR16 tape,

\[
\mathscr S_K=(m+1)[C_1-H(q)/\ell]
 +\mathfrak D_K/\ell-\operatorname{Tr}(GV_K)
 +\operatorname{Tr}(\widehat B_K\delta),
\quad \delta=(\Phi-I)\rho.
\tag{10}
\]

It retains all cap-aborts, conditional quantum DATA and preparation source.
At a stationary base the final term still has derivative
`Tr Bhat_K[(dPhi)rho+(Phi-I)d rho]` for independent variations; finite
preparation is not replaced by an infinite invariant state. This is an
exact finite formula, but its Kraus/input/cost map has not been identified
with the original h0 two-cell all42 map. Therefore (10) is not added to
(1), nor are its r/nu boost derivatives relabeled as the 42 field rows.

The coherent READY one-mean owner has an actual paired-cut heat satisfying
`d(H_C+J)=R(f)dJ`, with `34165/50549<=R(f)<1`. That identity includes its
own admitted preparation directions. It is a source reduction on the
rank-one coherent n20/256-site cut, and does not turn that cut into the
two-band addressed J2 operator used in (1). The one-mean obstruction at
the separate h=1/4 root likewise does not prohibit the different
critical point constructed here.

An open chronological unitary path has a constant heat spectrum after
cumulative-unitary gauge trivialization. The actual 16-stage Book clock
owner instead defines a cyclic ZMod16 apparatus, even though its
15-operation execution finishes before wrap. Its full scene/cut Hodge
has not been identified with the open path incidence. Thus that correct
conditional heat theorem cannot presently set the Delta row in (8) to
zero. The forward-clock HJR owner also retains any nonseparable thermal
interaction source explicitly.

## 6. Preparation typing and verification scope

The separate preparation calculation establishes fixed query eigeninputs
psi+ and psi- on `span{|0>,|2>}` and vanishing eight real CP1 first rows
for the actual N1 Born-score extension. Those rows also vanish for a
scalar feedback extended through the same Born reports. However a
literal full rank-two operator determinant can be independent of the
chosen input rays; then its preparation Hessian is zero rather than
the nondegenerate Born-score Hessian. Identifying these two functions
requires the actual operator/preparation map. This note therefore
claims the same-variable **42-field J2 endpoint** only, and does not
declare a 50-variable physically selected Book root.

Completed here: exact same-operand feedback factorization, entire initial
42-covector, all42 continuation, high-precision new candidate, and its
nonflat geometry. The independent interval certificate supplies exact
existence at its own stated scope. Uncomputed: the complete actual
Delta/Info/work/clock residual (8), all additional physically admitted
internal equations, and uniform physical continuum/refinement.

### Reproduction

`compare_sources.py --repo .` imports the unchanged original model and
rational inputs at their actual repository paths, checks all three input
Git blobs, and reproduces `J2_SOURCE_AT_UNPADDED.json` with mpmath 1.3.0.
The default command compares every computed value with the frozen receipt;
`--write-result` is the explicit receipt-authoring option. A local replay
through this portable entrypoint passed. The proof in `../certificate/`
independently consumes the proposed center and rational preconditioner;
its validation does not require trusting the numerical trajectory or
reproducing its floating-point proposal generation. No GitHub CI, Lean,
whole physical HJR or previous all-stack suite is claimed rerun here.
