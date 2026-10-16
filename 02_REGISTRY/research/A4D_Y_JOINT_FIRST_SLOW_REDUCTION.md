# Y continuation: the joint center is constrained before its wave equation

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`

Input: #310 `1d257c9902168a0631b6ac601c532e0de1800379`; main
`e80a3b1ccf615fb4f70bf5900181592604928497`. The corrected finite owners are
consumed, not replaced. No global terminal is claimed. PR remains Draft /
`IN_PROGRESS`.

## 1. Result and scope

The two connection-center hyperbolic symbols are correct. They are not two
free envelopes of the **full fixed-metric joint/source system**. The metric
equations impose a full-rank first-slow constraint before the second-order
connection-center equation. At the flat Y vacuum with `z=1`, this constraint
forces all four derivatives of the leading Y amplitude to vanish and removes
the order-h boost-dual correction, when the raw prescribed source is O(h^2).

This gives an injective first-order center symbol for the stacked joint
operator, in every nonzero real slow covector. It supplies a local
low-frequency inverse estimate without assuming an elliptic connection
Hessian. It does not establish a global Bloch gap, an exact curved branch,
or a bound uniform as z tends to zero.

There is also an explicit nonlinear curved seed with exact sitewise metric
response erasure. One exact connection row shows why that seed itself cannot
be the nonlinear stationary branch. The required transverse corrections
cannot be omitted.

The owned quadratic symbols have exact characteristic polynomials. Their
null lines are `(16/25,1,1,1)` for Y and `(16/7,1,1,1)` for the boost-dual
mode, so neither null line lies in the stationary sector `t0=0`. On that
stationary sector the eigenvalues are `{-1024/26901,37439/3087,37439/3087}`
and `{-64/267,2261/48,2261/48}`, respectively. The spatial plane
`t1+t2+t3=0` is positive for both symbols; this covers the product seed's
covector `(1,-1,0)`, but is a restricted-sector fact and gives no full
elliptic gap. The exact characteristic polynomials and null vectors are
checked by `a4d_y_center_envelope_symbol_check.py`.

## 2. Five-column constraint, including the visible center

Use the owned literal blocks with connection test phase lambda^(-s) and
metric readout lambda^(+s). At zero slow momentum write

\[
H=A_0,\quad N=(n_Y,n_D),\quad C=C_0,
\qquad HN=0,\quad Cn_Y=0,\quad Cn_D\ne0.
\]

The owned ranks are `rank H=94`, `rank[H;C]=95`. Let G be the bordered
range inverse of H and put `Y_i=-G A_i n_Y`. All four equations
`H Y_i+A_i n_Y=0` and their left-cokernel conditions hold exactly.

For a flat metric and a regular slowly modulated Y amplitude c(X), the
order-h connection correction has the form

\[
a_1=\sum_iY_i\partial_i c+n_Y b_Y+n_D b_D.
\]

The order-h metric/source equation is therefore

\[
\mathcal M\binom{\nabla c}{b_D}=0,\qquad
\mathcal M=[CY_0+C_0^{[1]}n_Y\mid\cdots\mid
CY_3+C_3^{[1]}n_Y\mid Cn_D]\in\mathbb Q^{40\times5}.
\]

Here `C_i^[1]` denotes the first shift moment in direction i, not the
zero-momentum block C. The free b_Y is invisible at this order. An arbitrary
smooth source first enters at order h^2; it cannot cancel the displayed rows.

Select zero-based rows `(0,1,2,4,14)`. Their five-by-five minor T is

\[
\begin{pmatrix}
625/1281&-400/3843&-400/3843&-400/3843&0\\
-200/1281&-9941/1281&15731/1098&-49703/7686&0\\
-200/1281&-49703/7686&-9941/1281&15731/1098&0\\
-191/1281&-3407/26901&71805/23912&-91115/30744&1\\
191/1281&3407/26901&116003/30744&-273487/71736&1
\end{pmatrix}.
\]

The exact identities are

\[
\det T=-\frac{975737200}{35590023},\qquad
\|T^{-1}\|_F^2=
\frac{22658595092811829982361}{373208728717825280000}<64.
\]

Consequently, for real or complex v,

\[
\boxed{\|\mathcal Mv\|_2\ge\|v\|_2/8.}
\]

This is a certified inequality on all phase-resolved metric rows. It is
lost by taking the four-phase average. It gives `dc=0`, `b_D=0` in the
homogeneous leading joint problem, rather than a free Y wave.

## 3. A joint low-frequency estimate, derived rather than assumed

At fixed metric define the rectangular Bloch derivative

\[
\mathcal J(t)=\binom{A(t)}{C(t)},\qquad
\mathcal J_0=\mathcal J(0),\qquad\ker\mathcal J_0=\mathbb R n_Y.
\]

Let G_J be its Moore-Penrose range inverse and
`Pi=I-J_0 G_J` the orthogonal left-cokernel projection. Define

\[
\Gamma_i=\Pi\mathcal J_i n_Y,
\qquad\Gamma=[\Gamma_0|\Gamma_1|\Gamma_2|\Gamma_3].
\]

Then Gamma has rank four. Indeed, if `sum_i Gamma_i xi_i=0`, a transverse
connection correction can cancel the corresponding first-slow joint
forcing. Its connection part must equal `sum_i Y_i xi_i+N b`. The metric
part then says `M(xi,b_D)=0`. The preceding minor forces `xi=0`.
This proves the assertion over both R and C.

Finite-dimensional analytic range elimination for J(t) now gives the
one-column reduced symbol `sum_i t_i Gamma_i+O(|t|^2)`. For physical
`t=i k`, injectivity and compactness of the real unit sphere give constants
`c,delta>0` such that

\[
\boxed{\sigma_{\min}(\mathcal J(ik))\ge c|k|\quad
       (0<|k|<\delta).}
\]

For completeness, the 95-dimensional range block of J_0 stays boundedly
invertible onto its image near zero. Eliminating that block is a uniformly
bounded triangular change of variables. On the remaining one-dimensional
domain the squared first-order norm is `k^T Gamma^T Gamma k`, a positive
definite quadratic form. The quadratic Taylor remainder is absorbed by
decreasing delta. This proves the stated singular-value estimate for the
full rectangular operator, not merely for a selected row.

On a periodic lattice of side L, the low-frequency complement of the
constant Y mode therefore has inverse loss at most `C L`, in normalized
Fourier l2 or Fourier l1 norms. This is a decomposition used in an estimate,
not a spectral filter added to the equations. Other Bloch strata and the
owner physical-space sum norm are not controlled by this local estimate.

## 4. Nonlinear first-slow reduction is a constrained first-order system

The constant-coframe owner supplies an analytic family `chi(Q,z)` of exact
joint Y vacua for constant Q near eta. Work in its nondegenerate Gram chart.
The frozen joint derivative has rank exactly 95 near `(eta,1)`: a nonzero
95-minor persists, and the exact Y tangent remains a null vector. Its range
inverse, left projection, and first shift moments are analytic there.
The rank-four Gamma condition also persists in a sufficiently small fixed
neighborhood. This statement does not extend to z=0.

Here is an explicit definition of the nonlinear leading equation. Write
the literal local Euler map as a function of the finitely many shifted
metric and link values. Its first shift moments are

\[
\mathcal J_i=\sum_\delta\delta_i D_{K_\delta}\mathscr E,
\qquad \mathcal B_i=\sum_\delta\delta_i D_{Q_\delta}\mathscr E,
\]

evaluated on chi, with all fast-phase incidences retained. Right-trivialize
link variations in the same chart as the owners. For slowly varying Q,z,
the full order-h equation is

\[
\mathcal J_0 w_1+
\sum_i(\mathcal J_i\chi_Q+\mathcal B_i)\partial_iQ+
\sum_i\mathcal J_i\chi_z\partial_i z=0.
\]

Set `b=Pi sum_i(J_i chi_Q+B_i) partial_i Q` and
`L_Gamma=(Gamma^T Gamma)^(-1) Gamma^T`. Exact elimination yields

\[
\boxed{\nabla z=-L_\Gamma b,\qquad
 (I-\Gamma L_\Gamma)b=0.}
\]

These coefficients are analytic in Q,z. This is a nonlinear constrained
first-order system for the center; its differential compatibility must
also be imposed. The two connection-only wave symbols may enter higher
compatibility equations, but are not a substitute for this system. At a
normal point the derivative of these first-slow constraints is part of
the owned 20-curvature compatibility calculation. No existence theorem
for this nonlinear first-order system is being inferred from its linearization.

## 5. A genuinely curved nonlinear seed and why it is not stationary

Let `n=(1,1,1)`, `P_perp=I_3-n n^T/3`, extended by zero in the time slot,
and choose a positive smooth f with `partial_0 f=0`, `n.grad f=0`. Put

\[
S_f=I+(f-1)P_\perp,\qquad
Q_f=\eta+(1-f^2)P_\perp.
\]

This is a product of a flat Lorentzian two-plane and a conformal spatial
surface. Nonconstant f generally gives nonzero curvature. Let Y be the
owned rotation, B its commuting boost dual, and choose

\[
L_0(x)=W_{p(x)}(z),\qquad
L_i(x)=\exp(h\alpha_i(x)Y),\qquad
\alpha=Y_{spatial}\nabla\log f/3.
\]

For any h and z in the Cayley chart, all spatial plaquettes are unchanged
when W is removed. Time independence and commutation give
`P_0i=W_p W_(p+1)^(-1)`, independently of the spatial links. Its odd
curvature is the same scalar multiple of Y for all i at a given phase.
The sum of all 16 unrestricted solder derivatives of these temporal faces
vanishes for S_f. Therefore the exact, unaveraged identity is

\[
\boxed{E_Q(Q_f,K_{seed}(z))=E_Q(Q_f,K_{seed}(0)).}
\]

It is not a same-prescribed-source tautology: it is a direct action identity.
It is also not on-shell. In fact `YB=BY=0`; rotations generated by Y fix B
on both sides. The six literal occurrences of a temporal B edge give

\[
\boxed{E_{K_0,B}(x)=3f(x)^2-\sum_{i=1}^3f(x-he_i)^2.}
\]

Each positive temporal-face contribution is f(x)^2 and each incoming
one is minus f(x-he_i)^2. This identity is independent of z and of the
spatial rotation angles. On a connected periodic spatial lattice its
vanishing at every site forces f^2 constant by the maximum principle.
Hence the commuting seed ansatz cannot be the required nonflat exact branch.

For `f^2=1+epsilon cos(omega(x1-x2))`, the Gaussian curvature at its peak
is `epsilon omega^2/(1+epsilon)^2`, while the exact connection residual is
`2 epsilon(1-cos(omega h))`; its h^-2 limit is `epsilon omega^2`.
The residual is genuine, despite exact metric-response invisibility.
This obstruction neither excludes corrections in the full connection
space nor forces z to shrink.

For this Fourier mode alone, with `u=x1-x2`, the shift operator
`L_h=3I-sum_i S_i` obeys
`L_h cos(omega*u)=2(1-cos(omega*h))*cos(omega*u)`. Hence the displayed
residual is exactly `L_h(epsilon*cos(omega*u))`, and on a nonconstant
mean-zero periodic mode the required correction is `epsilon*cos(omega*u)`.
More generally, on the first Brillouin zone,
`Re m(k)=2 sum_i sin^2(k_i*h/2) >= 2 h^2 |k|^2/pi^2`; thus the mean-zero
operator inverse has norm at most `pi^2/(2 h^2 k_min^2)`, not an h-uniform
bound. The mode-specific O(1) correction uses the smooth fixed-frequency
forcing and does not prove uniform control for arbitrary h-dependent data.
The product-seed certificate checks the exact cosine identity.

The companion small certificate verifies all 96 coefficients of E_K at
orders h^0 and h^1 for arbitrary f and its two independent spatial-plane
gradients at z=1. Thus the nonlinear seed is first-slow compatible and
fails at order h^2, precisely where transverse corrections become necessary.
The linear conformal control also solves the new first-order constraints
with constant Y amplitude; the injectivity result does not exclude the
owned surviving curved sector.

## 6. Exact finite-lattice nonlinear reduction and its first obstruction

For a fixed finite lattice let
`F_h(a;p)=(E_K(Q,K_Y exp(a)), E_Q(Q,K_Y exp(a))-j)`, where p=(Q,j) and
j is specified before solving. Include the entire lattice kernel, not
only the two zero-momentum connection vectors. Let J_h be the fixed-metric
joint derivative, G_h its range pseudoinverse, and `Pi_h=I-J_h G_h`.
Write `a=c+w`, `c in ker J_h`, `w in im J_h^*`.

There is a rigorous local analytic range reduction. To see its quantitative
content, set `kappa_h=||G_h||`, `d=||F_h(c;p)||`, `r=2 kappa_h d`.
If the radius-r chart ball is valid and

\[
\kappa_h\sup_{\|w\|\le r}
\|D_aF_h(c+w;p)-J_h\|\le\tfrac12,
\]

the map `w -> -G_h(F_h(c+w;p)-J_h w)` maps that ball to itself and contracts
by at most one half. Its unique analytic fixed point W_h solves the range
equation. The full equation is then exactly equivalent to

\[
\boxed{\Phi_h(c;p)=\Pi_hF_h(c+W_h(c;p);p)=0.}
\]

This is an exact nonlinear Kuranishi map for each finite lattice, with
the complete metric/source rows kept. The displayed inequalities state
the constants that would have to be uniform; no uniform claim is implicit.

For an independently fixed parameter curve `p(epsilon)`, a compatible
first tangent v obeys `J_h v+B_h p_1=0`. The first nonlinear necessary
equation is explicitly

\[
\boxed{\mathcal O_{2,h}=
\Pi_h\{B_h p_2+D^2F_h[(v,p_1),(v,p_1)]\}=0.}
\]

If it holds, the second derivative of the range correction is its
negative G_h image, up to the retained kernel. If it fails, no C2 branch
with that prescribed metric/source curve has the specified tangent.
This is an actual reduced equation, not an off-shell response pairing.

## 7. First nonlinear curved gate; one exact metric readout slice is obstructed

The nonlinear curved forcing on the surviving local normal-jet sector has
now been evaluated exactly on the normalized curvature slice below. Let beta be the
spatial Y two-form and choose a constant-curvature surface product with
`R=-kappa beta tensor beta`. Its Gaussian curvature is `3 kappa`. For a
dimensionless lattice offset xi, put `x=P_perp xi`, `r^2=x.x`,
`T=r^2 P_perp-x x^T`, and `delta=kappa h^2`. Then
its exact geodesic-normal Taylor data are

\[
Q=\eta+\delta T-\tfrac25\delta^2r^2T+O(\delta^3),\qquad
S=I-\tfrac12\delta T+\tfrac3{40}\delta^2r^2T+O(\delta^3),
\]

with the spatial matrices extended by zero in the time slot. These follow
from `sin(sqrt(3 kappa) r)/(sqrt(3 kappa) r)` and are rational Taylor inputs.

The replay uses the following exact setup:

1. Extract the already-certified phase-polynomial first connection
   tangent `a^[1]_p(xi)`, now checked to have degree one, from the
   normal-jet solve. Keep its constant Y freedom as a parameter or fix
   the parameterization z, not a selector.
2. Substitute `K=K_Y exp(delta a^[1]+delta^2 a^[2])` into the literal
   Euler map, with all 96 components of `a^[2]_p(n)` allowed and all
   monomials in four coordinates through degree four. Every incoming
   shift changes both xi and p. Retain the conjugate real phase pairs.
3. At delta^2 solve the full connection equations and all fast-phase
   metric differences. A common metric coefficient is allowed during
   this necessary-compatibility test, then compared with the independent
   Einstein expansion; it is not adopted afterwards as a physical source.
4. Eliminate the 95 frozen joint range variables degree by degree. Return
   the exact remaining cokernel map, its rational forcing, and either a
   left obstruction or a full solution. A direct unreduced layout has
   70 monomials, 6720 connection coefficients and 700 common-source
   coefficients; the triangular elimination avoids a blind large census.

For general Gram variations use the actual analytic coframe derivative
(the Sylvester equation for the square root), not the identity-frame
lift eta*q/2 away from Q=eta. Report the common response at the normal
point only after compatibility. The calculation below is a formal local
connection continuation and metric phase-readout test on one normalized
curvature slice; it is not a global or refinement-uniform theorem.

### 7.1 Exact connection jet and metric phase defect

The normal-jet owner now verifies exactly that the normalized surviving
first connection tangent has no quadratic term in `xi`, so it is linear in
the normal coordinate. At order `delta^2`, its products with the quadratic
first metric jet have degree at most three. The homogeneous degree-four
forcing therefore comes only from the exact second-order Gram coframe
displayed above.

`a4d_y_curved_normaljet_degree2_obstruction_check.py` assembles the full
136-row order-`delta^2` Euler polynomial with the pinned first connection
tangent, exact Gram coframe, and right-trivialized inverse-link variation.
It includes all common phase-metric source coefficients. The homogeneous
degree-four forcing vanishes identically. The exact triangular cokernel
reduction gives:

| reduced map | rank | consequence |
|---|---:|---|
| frozen connection Hessian `H` | 94 | connection kernel dimension 2 |
| frozen joint derivative `[H; C0]` | 95 | fixed-metric joint kernel dimension 1 |
| joint derivative plus ten phase-common metric-source columns | 105 | 31-dimensional remaining cokernel |
| connection-only jet through degree four, 140 center coefficients | 140 x 140, rank 30 / 30 augmented | all 96 connection rows have an exact solution |
| joint degree-three reduced system, 35 degree-four center coefficients | 35 / 35 augmented | degree-four center correction is zero |
| joint degree-two system, 20 free degree-three center coefficients | 20 / 21 augmented | exact phase-common metric readout fails |

The connection-only elimination has a rational solution through normal
degree four; its 140-row cokernel system has rank and augmented rank 30, and
the certificate verifies all 96 Taylor equations exactly. The separate
degree-two joint defect is supported on `xi3^2`. After range elimination
and allowing every free degree-three center coefficient, a primitive
integer combination of the 31 joint cokernel coordinates has pairing
`-22209`; its primitive lift to the 136 Euler rows has pairing `-166034484`.
It proves that the order-`delta^2` metric readout cannot be made exactly
phase-common, even after the connection equation is solved. For the exact
rational connection solution, the full phase-resolved metric coefficient
has a componentwise coefficient-sum bound below `11000` on
`|xi_i|<=1`; therefore its phase defect is at most
`11000*delta^2 = 11000*kappa^2*h^4` on this local cell. After normalization
by `h^2`, this single coefficient contributes at most
`11000*kappa^2*h^2`, which tends to zero for bounded curvature. This is a
finite leading-order estimate, not a bound on the higher-order remainder or
on a complete exact branch. The certificate records the connection
solution, metric coefficient bound, both witnesses, row order, and all
annihilation checks. The two-dimensional kernel of `H` is not the joint
cokernel. Reproduce with:

The same replay now also extracts the zero-normal-momentum **connection**
cokernel equation before allowing a spatially varying center. In the
recorded exact basis of the two rows of `ker(H^T)`, the normalized curvature
slice has projected source

\[
\mathcal C_{2,\mathrm{const}}=
\left(\frac{351402359}{2108160},
      \frac{21506403637}{154949760}\right)\ne0.
\]

Both columns for a constant shift of the two center amplitudes vanish in this
equation, as they must since those shifts lie in `ker(H)`. Thus a stationary
seed with spatially constant center amplitudes cannot solve the connection
Euler equation at this order. The exact degree-four normal-jet solution
instead uses a nonconstant center profile: its transported contribution is
the negative of the vector above, and all 96 connection rows then vanish.
This is an actual quadratic Lyapunov--Schmidt coefficient for this one
normalized curvature germ, not a no-go for spatially varying centers, other
curvature germs, or the finite-lattice branch. It also does not remove the
separate phase-resolved metric defect, whose normalized size is subleading
at this order. The coefficient is unchanged if the first-order connection
tangent is shifted by an arbitrary constant multiple of the exact flat Y
tangent is shifted by an arbitrary constant multiple of the exact flat Y
family tangent, and the curvature amplitude is made symbolic at the same
time. The exact replay gives the connection vector
`kappa^2*(351402359/2108160, 21506403637/154949760)` and the joint
`xi3^2` phase-common witness `-22209*kappa^2`, both independent of the
retuning parameter `s`. Thus the nonzero obstruction covers the full
`kappa != 0` ray and cannot be tuned away by a first-order constant Y
retuning. The degree-four spatial center profile still cancels the
connection-only zero mode locally. The joint phase-common defect remains a
finite normal-jet obstruction; it does not turn the `O(h^4)` response defect
into an `O(h^2)` normalized gap.

```sh
python3 02_REGISTRY/research/certificates/a4d_y_curved_normaljet_compatibility_check.py
python3 02_REGISTRY/research/certificates/a4d_y_curved_normaljet_degree4_gate_check.py
python3 02_REGISTRY/research/certificates/a4d_y_curved_normaljet_degree2_obstruction_check.py
python3 02_REGISTRY/research/certificates/a4d_y_stationary_center_family_coker_check.py
```

The regular formal connection branch survives this order; the residual
phase-dependent metric term is of order `h^4` and is subleading to the
requested `h^2` normalization. The remaining theory is to continue the
connection solution to all required orders and prove a refinement-uniform
remainder in the owner topology; neither the connection-only hyperbolic
symbol nor an elliptic inverse assumption settles those questions.

## 8. Replay and claim boundaries

```sh
python3 02_REGISTRY/research/certificates/a4d_y_joint_first_slow_injectivity_check.py
python3 02_REGISTRY/research/certificates/a4d_y_product_plane_seed_check.py
```

The first reuses a single owned face assembly and a four-column range solve;
it does not rerun the 20-curvature or small-amplitude pipelines. The second
uses small matrix identities, first-order dual-number arithmetic, and the
exact Fourier-mode shift-row identity. The center-symbol certificate also
checks exact full and stationary characteristic polynomials.

The validated norms are finite Euclidean coefficient norms and the stated
local frozen-symbol Fourier estimates. There is no owner-sum-norm nonlinear
response theorem, no all-Bloch uniformity, no z-to-zero uniformity, no new
source or selector, no action change, and no promotion of either global
terminal. The pure-rotation seed obstruction is explicitly not a no-go
for the full connection space.

The submitted scratch `a4d_y_joint_stationary_correction_check.py` was also
replayed. Its exact T identities are independently owned by the 40-by-5
certificate above; its center spectra and the seed's particular cosine-mode
correction are now checked by the two owner scripts. Its `sigma_min` assertion
uses a floating root (the exact inverse-Frobenius bound is the retained proof),
and its claimed shift-symbol zero set is only tested by substituting the zero
frequency. The Fourier identity and Brillouin-zone inequality stated above
give the valid analytic argument. The new exact obstruction certificate
evaluates the selected order-`delta^2` normal jet through its decisive
degree-two cokernel equation. It does not establish a uniform nonlinear
inverse or classify all curved branches, so those remain open beyond this
finite slice.
