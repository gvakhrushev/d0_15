# Affine native profiles cannot realize the completed Einstein contrasts

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #310.
Input research head: `af221e2fed92821c52afc88a5500774de8cd9a93`.
Control baseline inspected: `fa2b04b9c8aae5a0b8470322d6091712ce56567a`.
Status: **proved analytic obstruction for the explicit class below**, with
exact algebraic controls. No new Lean owner or registry promotion.

The [earlier seam audit](https://github.com/gvakhrushev/d0_15/blob/af221e2fed92821c52afc88a5500774de8cd9a93/02_REGISTRY/research/A4D_NATIVE_SEAM_ACTION_GATE_BOUNDARY.md) excludes
a direct fixed-fine action-preserving stationary map. That argument alone
does not exclude a weak prepared metric-contrast transfer. The present
theorem addresses the weak transfer separately. It includes simultaneous
affine fine/coarse variations at fixed lift, affine metric fibers, arbitrary
finite refinement dimensions, and auxiliary null directions. It requires
neither equality of action values nor convergence of native Hessians.

It does **not** establish completeness of this class in the D0 core. A
nonlinear metric readout, nonlinear native constraint, moving lift, metric
dependent norm, or independently owned signed action is outside the class.
Such a mechanism must be derived from its own core owner; naming it does not
construct it. The original #310 fixed-source/raw-owner terminal remains OPEN.

## 1. Independently defined native class

At each mesh $h=1/L$, $L\in4\mathbb N$, let $Z_h,Q_h,H_h$ be finite
dimensional real spaces. A native state is $z\in Z_h$, its metric data are
$q\in Q_h$, and its allowed metric fiber is

\[
 C_hz=q+b_h.                                                   \tag{1}
\]

Here $C_h$ and $b_h$ are fixed before the experiment. The fiber is nonempty
on every metric pencil used below. The sampling $g\mapsto q_h(g)$ is affine
in the actual covariant metric components, including all ten symmetric
slots; it is not an arbitrary nonlinear relabeling of native coordinates.
Allowed auxiliary variations are **all** $v\in\ker C_h$. The gate is the
Euler equation of the native action on those variations, defined independently
of the desired contrast:

\[
 S_h(z,q)=\gamma_h\|d_h+D_hz\|_{W_h}^{2}+\ell_h(q),\quad
 \gamma_h>0,\quad W_h>0,\quad
 D_zS_h(z,q)[v]=0\quad(v\in\ker C_h).                         \tag{2}
\]

$D_h,d_h,W_h,\gamma_h,C_h$ may depend on $h$, but not on the metric or
which probe is selected. $\ell_h$ is affine. A fixed independently specified
source contributes such a term. No matter action or dynamical source is
inferred from $\ell_h$. There is no uniform spectral gap hypothesis and no
uniqueness or removal of a nongauge auxiliary kernel.

This class contains the fixed-$J$ seam extension
$D=L_fJ-JL_c$ with both $L_f,L_c$ affine variables, any affine symmetry,
row-sum and support constraints, and a fixed positive counting norm. Indeed

\[
 S(D+t\delta D)-S(D)-DS(D)[t\delta D]
       =t^2\|\delta L_fJ-J\delta L_c\|^2\ge0.                 \tag{3}
\]

This extension is an analyzed class, not a claim that `ArchiveVariation`
already owns joint fine/coarse variations. Its actual owner freezes the
fine Laplacian and lift and varies only the coarse Laplacian.

## 2. The full gate gives a convex profile, even with null directions

On the finite affine image of (1), choose an affine section $z_0(q)$.
Write every state as $z_0(q)+v$, $v\in\ker C_h$. Then the seam residual is
$r_h(q)+K_hv$, with $r_h$ affine. Let $P_h$ be the $W_h$-orthogonal
projection onto $\operatorname{range}K_h$. This range is closed because
the spaces are finite dimensional. Its orthogonal projection exists without
an inverse on the auxiliary kernel.

The gate is

\[
 K_h^*W_h(r_h(q)+K_hv)=0.                                    \tag{4}
\]

It is solvable: take $K_hv=-P_hr_h(q)$. Every solution has the same residual
$(1-P_h)r_h(q)$ and value

\[
 F_h(q)=\gamma_h\|(1-P_h)r_h(q)\|_{W_h}^{2}+\ell_h(q).       \tag{5}
\]

For any other state, orthogonality gives its action minus $F_h$ as
$\gamma_h\|K_h(v-v_*)\|_{W_h}^{2}\ge0$. Thus **every stationary
preparation is a global fiber minimum**. Null directions remain in the
fiber and do not affect this value.

Equation (5) proves that $F_h(q_h(g))$ is a convex quadratic in actual
metric data. On any fixed affine metric pencil $g_s=g_*+sV$, its centered
secant, for any admitted $\epsilon>0$, is exactly its derivative:

\[
 d_h(s)=\frac{F_h(q_h(g_{s+\epsilon}))-
                     F_h(q_h(g_{s-\epsilon}))}{2\epsilon}.
 \qquad d_h(s_2)-d_h(s_1)\ge0\quad(s_2>s_1).                 \tag{6}
\]

Affine source terms change the intercept, never this inequality. There
is no estimate on the $h$ dependent quadratic coefficients in this proof.

## 3. The quantitatively specified transfer would preserve monotonicity

Use the [owned finite-probe experiment](https://github.com/gvakhrushev/d0_15/blob/af221e2fed92821c52afc88a5500774de8cd9a93/02_REGISTRY/research/A4D_NATIVE_FINITE_PROBE_COMPLETION.md)
without changing its full 24-row preparation or ten-slot metric convention.
To fix the meaning of the contrast, define the unnormalized half differences

\[
 \Delta I_h(s,V)=\tfrac12[I_h(g_{s+\epsilon},A_+)
                              -I_h(g_{s-\epsilon},A_-)],
 \quad
 \Delta I_h^N(s,V)=\tfrac12[S_h(z_+,q_+)-S_h(z_-,q_-)].       \tag{7}
\]

$A_\pm$ are admitted preparations in that experiment; $z_\pm$ satisfy
the independently defined full auxiliary gate (4) at the corresponding
metric fibers. Require one fixed calibration $a\ne0$, the same for every
probe and mesh, and the proposed bound

\[
 |a^{-1}\Delta I_h^N(s,V)-\Delta I_h(s,V)|\le C_{s,V}h.       \tag{8}
\]

The probe theorem gives
$\Delta I_h/\epsilon=DI(g_s)[V]+O_{s,V}(h/\epsilon+\epsilon^2)$.
Consequently, for $\epsilon_h=h^{1/3}$,

\[
 |a^{-1}d_h(s)-DI(g_s)[V]|\le C'_{s,V}h^{2/3}.              \tag{9}
\]

Pointwise convergence for every fixed $s$ is enough. Uniform convergence
in $s$ and differentiation of an asymptotic error are not needed. From (6),
the limiting derivative must be nondecreasing when $a>0$, nonincreasing
when $a<0$. The same conclusion holds for the source-subtracted target
$I-\ell$, since a fixed source functional is affine in $g$.

If native record and refinement errors perturb each value in (7) by at
most $B_{s,V}h$, their combined half-difference error is at most $B_{s,V}h$
and is included in (8). More generally their error must be $o(\epsilon_h)$
for this monotonicity conclusion. This is a **conditional error-composition
lemma**, not a derivation of physical native recording/refinement maps.

## 4. Two opposite curvatures at the same genuinely curved metric

The literal curvature sign is $R_{\rm owner}=-R_{\rm standard}$, including
Ricci and Einstein tensors, as pinned in the probe owner. Take
$\eta=\operatorname{diag}(1,-1,-1,-1)$ and a positive smooth periodic
function $q$ on $\mathbb T^4$. The conformal metric $g=q\eta$ has

\[
 I(q\eta)=-\tfrac12\int\sqrt{|g|}R_{\rm standard}
        =-\tfrac34\int q^{-1}\eta^{\mu\nu}
                               \partial_\mu q\partial_\nu q. \tag{10}
\]

For completeness, write $q=\Omega^2$. The Christoffel formula gives
$R_{\rm standard}=-6\Omega^{-3}\Box_\eta\Omega$ in dimension four;
$\sqrt{|g|}=\Omega^4$. Periodic integration by parts then gives
$3\int\Omega\Box_\eta\Omega=-3\int\eta(d\Omega,d\Omega)$,
which is (10). The checker independently constructs every Christoffel
and Ricci component for each one-coordinate conformal jet. In particular
$R_{\rm standard}=\eta^{kk}(-3q''/q^2+3(q')^2/(2q^3))$;
the density's $3\eta^{kk}q''/2$ term is a periodic divergence.

For an affine scalar variation $q+sv$, direct differentiation of (10) gives

\[
 D^2I(q\eta)[v\eta,v\eta]
   =-\tfrac32\int q^{-1}
       \eta(dv-v\,dq/q,dv-v\,dq/q).                         \tag{11}
\]

Choose the explicit curved base and two **fixed** metric probes

\[
 q_*(y)=1+\tfrac1{10}\cos(2\pi y_1),\quad g_*=q_*\eta,
 \quad u_0=\cos(2\pi y_0),\quad u_1=\cos(2\pi y_1),
 \quad V_k=2q_*u_k\eta.                                    \tag{12}
\]

Here $9/10\le q_*\le11/10$; both pencils
$g_{k,s}=q_*(1+2su_k)\eta$ are smooth, oriented, time oriented and
nondegenerate for $|s|<1/4$. At $y_1=0$,
$R_{\rm owner}(g_*)=120\pi^2/121\ne0$. This is a geometric curved
base for the probe test, **not** an asserted native on-shell solution.

Substitute $q=q_*(1+2su_k)$ and $v=2q_*u_k$ in (11). The derivatives
of the curved base cancel exactly, leaving

\[
 \frac{d^2}{ds^2}I(g_{k,s})
      =-6\eta^{kk}\int\frac{q_*(\partial_k u_k)^2}
                                  {(1+2su_k)^3}.             \tag{13}
\]

The integral is strictly positive. The time pencil has strictly negative
second derivative, the spatial pencil strictly positive, throughout the
declared interval. At zero they are exactly

\[
 I''(g_{0,s})|_{s=0}=-12\pi^2,\qquad
 I''(g_{1,s})|_{s=0}=+12\pi^2.                               \tag{14}
\]

The packed half-standard-Einstein response independently checks this
normalization in all ten slots. The conformal probe has nonzero response;
it is not one of the four genuine linearized metric gauge directions.

## 5. Obstruction theorem and its exact quantifiers

**Theorem.** No native family of class (1)--(2), with fibers on both
pencils (12) and their admitted probe endpoints, can satisfy (8) for every
fixed $s$ in $(-1/4,1/4)$ with one nonzero calibration $a$ and
$\epsilon_h=h^{1/3}$. This remains true for any fixed affine source term
and for recording/refinement errors covered by Section 3.

**Proof.** When $a>0$, (6) and (9) require $I'(g_{0,s})$ to be
nondecreasing, contradicting (13) for any two distinct $s$. When $a<0$,
they require $I'(g_{1,s})$ to be nonincreasing, contradicting its strictly
positive derivative. Affine source subtraction does not change either
second derivative. Both fibers were assumed and are inhabited by (4);
the argument does not use empty native preparations. This proves the
whole stated refining class, not an extrapolation from finite fixtures.

The theorem does not prohibit a bridge on a smaller probe class that
omits one pencil, at only a single metric/first derivative, or by nonlinear
native preparation whose values differ by a macroscopic amount from (5).
Those are different hypotheses and do not supply the all-probe transfer
requested here. It also does not exclude the nonlinear coframe Gram map
or a core-owned moving-lift sector. No completeness theorem is supplied
for those alternatives.

The [subsequent signed-quadratic/Gram theorem](A4D_NATIVE_QUADRATIC_GRAM_FLUX_BOUNDARY.md)
removes positivity and supplies an exactly affine coframe/metric Gram
pencil with a nonzero Einstein third variation. Its explicit affine-fiber
scope includes that Gram mechanism; it still does not cover arbitrary
nonlinear constraints or moving-lift couplings.

## 6. Hostile controls and stationarity boundary

* **Gate substitution:** choosing off-shell auxiliary data $y=g^2$ for
  the affine residual $1-y$ produces $(1-g^2)^2$, with a negative second
  derivative at zero. The actual auxiliary equation is $y=1$. The
  off-shell preparation cannot be called its stationary profile.
* **Nonlinear readout/constraint:** the same polynomial can result from
  a nonlinear metric readout or constraint. This demonstrates why the
  affine-fiber restriction is load bearing; it is not a no-go for every
  positive native action.
* **Small residual:** $(h^2y-1)^2$ has Euler residual $-2h^2$ at $y=0$
  but action gap one above its minimum. An $O(h^2)$ residual alone does
  not justify an $O(h)$ profile-value error without a range estimate.
* **Source fitting:** a fixed source is affine in the metric and cannot
  repair (14). Assigning a different source to each endpoint changes the
  experiment. No such fitting occurs here.
* **Null directions:** the exact profile fixture retains an auxiliary
  kernel. Eliminating that kernel or declaring it gauge is unnecessary.
* **Calibration:** negative calibration reverses both signs, preserving
  their incompatibility. A separate calibration per probe is forbidden.

The independent stationarity implication required for positive GR remains
unproved: native on-shell equations must annihilate the source-subtracted
physical contrast for **all** smooth symmetric probes. Auxiliary gate (4)
only makes its own fiber variations stationary. It is not defined by the
desired annihilation and does not prove that implication.

## 7. Replay and next missing arrow

The [checker](certificates/a4d_native_affine_probe_nogo_check.py) and its
[immutable ledger](certificates/a4d_native_affine_probe_nogo_results.json)
check 71 exact controls: generic square/Jensen identities, simultaneous
fine/coarse seams, a rank-deficient full stationary profile, packed
metric responses, nonlinear conformal Hessians, the two periodic signs,
curvature nonemptiness and the hostile controls. The general analytic
proof is Sections 1--5. The consumed
[Palatini checker](https://github.com/gvakhrushev/d0_15/blob/af221e2fed92821c52afc88a5500774de8cd9a93/02_REGISTRY/research/certificates/a4d_finite_probe_palatini_check.py) checks
all 24 connection rows on arbitrary 64 first-jet coefficients and all
ten metric response slots including a sheared off-diagonal control.

```sh
python3 02_REGISTRY/research/certificates/a4d_native_affine_probe_nogo_check.py
python3 02_REGISTRY/research/certificates/a4d_finite_probe_palatini_check.py
```

The next arrow is an independently core-owned **non-affine physical
state/variation/action realization** with quantitative record/refinement
compatibility, or a completeness obstruction for every remaining such
owner. The existing archive number-record section is not that arrow.
No new action, selector, source prescription or physical postulate has
been introduced by this result.

## 8. A second existing owner: homogeneous mixed-parent stationary values

The [actual mixed-parent action](../../03_FORMALIZATION/D0/Geometry/FinitePrimalDualHodgeParent.lean)
is a different mechanism, with auxiliary multiplier fields and supplied
stars/differentials. It is not assumed to be a positive seam norm. Its
literal formula, writing $K=d_D S_1d_P$, is

\[
 B_g(\psi,\chi,\lambda)=\tfrac12\langle\chi,S_0(g)\chi\rangle
           +\langle\lambda,S_0(g)\chi-K(g)\psi\rangle.       \tag{15}
\]

The following class restrictions are explicit: the supplied pairing is
bilinear; the displayed operators are linear **in the fields** at fixed
metric; all three fields admit simultaneous rescaling as an allowed
auxiliary variation; the native field gate is their full Euler equation.
The geometry-dependent operators and pairing may depend arbitrarily
nonlinearly on $g$, including moving-lift realizations. The action has no
additional metric-only or inhomogeneous field term. Fixed affine source
terms in $g$ are allowed as before.

These are not hidden properties of a function's name: the Lean definition
accepts `pairing` as a function, so bilinearity must be supplied or proved
for its actual instantiation. The existing perfect-pairing construction
does give bilinear pairings, but does not select a physical metric law.
Likewise the scalar Ward theorem alone is not the full field Euler gate.

**Homogeneous-parent theorem.** Every stationary preparation in this class
has $B_g=0$. Consequently it cannot satisfy the completed contrast transfer
(8) on either of the strictly curved action pencils (13), even when the
operator dependence on the actual metric is nonlinear.

**Proof.** At fixed geometry,
$B_g(t\psi,t\chi,t\lambda)=t^2B_g(\psi,\chi,\lambda)$.
The independently defined full field gate annihilates the simultaneous
field variation. Differentiating at $t=1$ gives $2B_g=0$. In coordinates
this is the exact identity

\[
 \langle\psi,E_\psi\rangle+\langle\chi,E_\chi\rangle
                  +\langle\lambda,E_\lambda\rangle=2B_g.    \tag{16}
\]

No inverse, positivity, self-adjointness or removal of a kernel is used.
The zero triple gives a genuine stationary preparation at every metric;
nonzero kernel fields can also remain. Every full-field stationary value
is zero regardless of which preparation is used. Native secants therefore
contain only the derivative of an affine source functional, which is
constant along each affine metric pencil. The limit (9) would require
$I'(g_{k,s})$ to be constant in $s$, contradicting (13). This proves the
declared class for arbitrary refinement dimensions and nonlinear operators.

For approximate Euler preparations, (16) gives the quantitative bound
$|B_g|\le\|z\|\|E_z\|/2$ in a fixed coordinate dual norm, where
$z=(\psi,\chi,\lambda)$. An $O(h)$ bound for this product suffices to
include their action error in Section 3. It must be proved from the native
preparation; it is not inferred from an Euler residual alone.

**Source control.** Zero stationary values do not imply that the pointwise
metric Euler covector of every root vanishes at a singular metric
projection. The exact checker instantiates (15) with
$S_0=\left(\begin{smallmatrix}0&1\\1&0\end{smallmatrix}\right)$,
$K(q)=\left(\begin{smallmatrix}0&q\\q&1\end{smallmatrix}\right)$.
At $q=0$, $\psi=e_1$, $\chi=e_0$, $\lambda=-e_0$ solve every field row
and have $B=0$, but $\partial_qB=1$. This is a finite supplied-data
counterexample, not a physical Lorentz-Hodge realization. It protects the
distinction between completed values and the full stationary source
relation. No local matter stress theorem follows from (16).

Nonlinear or inhomogeneous native constraints that exclude rescaling,
fixed nonzero field boundary data, a non-bilinear supplied function, an
additional metric-only action, or a genuinely nonquadratic field action
are outside this second theorem. They require their own core owners.
This result therefore investigates one more existing candidate, rather
than claiming that the whole non-affine native frontier is exhausted.
