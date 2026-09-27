# A4D — joint response decoupling modulo microstructure

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`  
Execution: PR #240  
Launch baseline: `83a18af7c08c998ffd7d5bf5209aabaee74a390f`  
Status: IN PROGRESS. Global (NF) is refuted. The moving metric germ is now an exact all-phase identity; response closure still requires control on nonlinear realizable defects. Neither final terminal is claimed.

Synthesis update:
[Moving germ and stationary-sheet response](MEMO_A4D_RESPONSE_STATIONARY_SHEET_SYNTHESIS.md)
proves the Laurent identity \(H_{AQ}(z)\operatorname{vec}_{sym}(dd^T)=0\),
\(d_r=z_r^{-1}-1\), and its differentiated joint continuation. It also gives
an exact stationary-sheet envelope theorem and a quantitative horizontal-lift
criterion for response decoupling. The accompanying exact certificate corrects
the FUGU v7 physical ranks at orbits 5 and 7 from 24 to 23. A zero obstruction
class is distinct from a zero cokernel, and moving-germ absorption does not
annihilate the separate quadratic metric-response defect.

Quadratic slots at the shear witness, from one symbol
`a4d_joint_response_shear_reduced_quadratic_check.py`:
on \(z=(-1,1,-1,1)\) the moving germ is \(q_0=4E_{00}+4E_{02}+4E_{22}\) and has no \(q_{11}\) entry.
\(\Phi=\tfrac12 u^2 v^*H(Q)v\) has \(\partial_u\Phi=0\) for every \(u\), while
\(\partial_{q_{11}}\Phi=-u^2\). The germ direction itself has witness stress 0.
Modulation by any of the four neighboring L=2 characters stays outside this action through order \(u^5\): on the corrected jet whose resonant projection is \(-432\), those projections vanish. A longer envelope is still open. The period-2 joint-critical amplitude is therefore not rescued by an L=2 sideband, and the quadratic stress \(-u^2\) is not attained on that critical set.

## 0. Typed target and source contract

On the unit four-torus let h=1/L and Q_h(x)=g(hx), for one fixed smooth
nondegenerate Lorentz Gram field. Work in a fixed analytic solder section on
a compact chart; patch only with the actual Lorentz quotient. Link coordinates
are dimensionless logarithms A=log K in that section.

E_Q(x) is the ten-component covector obtained by differentiating the literal
counting-sum naked-star action with respect to the symmetric Gram at x,
holding the dressed links fixed. Components pair with E_ii and E_ij+E_ji
(i<j); no extra off-diagonal factor is inserted. At the standard solder the
row-leg lift is H(q)=q eta/2, or delta E=eta q/2 for column solder.

The primary topology investigated here is weak testing on the physical torus:
for every smooth symmetric test field phi,
\[
 \langle D_h,\phi\rangle_h
 =h^4\sum_x h^{-2}
 [E_Q(Q_h,K_h)-E_Q(Q_h,K_h^{sm})](x)[\phi(hx)]\longrightarrow0.
\]
The h^-2 normalization occurs once. This is distinct from pointwise,
unweighted sum, or volume-weighted strong convergence.

The substantive source convention is E_K=0 and E_Q=h^2 tau_h, with tau_h
prescribed independently of the geometric response and converging uniformly
to a fixed smooth covector field. Vacuum tau_h=0 is included. K_h^sm is the designated
smooth approximate connection of #216, with E_K=O(h^infinity); it is NOT
assumed to satisfy the metric-source equation. Its reconstructed response is
-1/2 G[g]+O(h) under the actual #216/#223 realization hypotheses. If both
comparators instead satisfy the identical metric source, equality is exact by
substitution and proves no Einstein consistency.

The new bounded-amplitude reduction below assumes ||A_h||_infinity <= C h
and the corresponding smooth bound for A_h^sm. This includes #232 at z=h
and z=h^2, without precompactness of A_h/h. It is a declared scope assumption,
not a consequence of the joint equations. All constants are uniform in L on
the specified compact chart.

## 1. Input ledger

All six mandatory inputs were merged at launch; heads and merge commits:

| PR | Head | Merge |
|---|---|---|
| #216 | 794ec0da4657375ccf03273b37a80d12fbdeed95 | 5523d8f679c1ea02f9b73d757c81649740010d0a |
| #223 | 9068cd44e7010ea7a3c89aa7cc2c4a7e11c32716 | 25de48600cbc7c06e233d7b8f886f89566bdd6a4 |
| #226 | 56a62f7468b2e2db4f9ca7f95bc9de4c3dfc6c42 | 4b145afe33b2fb7381615199167608b71457d01d |
| #227 | 2ff59e4d803268cc682a2a1bd0f241e1f7717438 | 245095f941a047dec95877ef03996742f37cb429 |
| #232 | 94375cc0bd1194faa2d5219008b77f700fd29ded | caa1e65087ddf15cda35325189ebfcbf51a56592 |
| #237 | 5d8196f3874dc72ae0c76ea54307679f09e0dd88 | 7d7ad1ba561dc1fb1d726a8158e8ddfe0c001794 |

#241 subsequently merged at 9f9a4da468f89eea4becd931f15c3814b009babd,
head e19de6b12d6cc4e99b3227a9c3ec3a363a38964c. Its finite mixed response is
consumed in Section 5. The four diagonal generator weights are recorded in
live #235 at 66bff2e3bc80de4534089e228a93aea406eaffa8; the present narrow
certificate independently checks their direct all-edge linear Euler and
metric constraints, so no unmerged orbit census is assumed.

## 2. Exact response quotient

At fixed Q the finite response factors through the based plaquette-curvature
array:
\[
 E_Q(Q,K)(x)[q]
 =\sum_{r<s}\epsilon_{rsuv}
 D_Q(v_u\wedge v_v)[q]^T G_2\star\mathfrak b(\mathcal R(P_{rs}(x))).
\]
Thus it is a linear map L_Q from six Lorentz-curvature matrices to a metric
covector. Define response equivalence by L_Q(C-C')=0. This quotient retains
physical nongauge fibres. It is not itself a convergence theorem.

For #232, Y=J12-J13+J23 and all three (0,s) curvatures equal
sigma(p) 4z/(4+3z^2) Y. The exact all-edge and metric equations at Q=eta are
zero, while curvature is nonzero for z!=0. Its response class is the identity
class at eta, and its connection gauge class is different.

#226 gives raw exponent zero in its actual unweighted sum norm, and exponent
two after h^-2. It does not turn O(h) or O(h^2) microstructure into negligible
response. Multiplication by h^4 transfers the same bound to the corresponding
volume-weighted sum norm. Wiener estimates require a bounded algebra norm,
not merely a pointwise chart bound. #223 applies to smooth analytic vertices;
it does not control a grid-scale defect measure.

## 3. New exact diagonal quadratic-moment cancellation

Let p=sum x_r mod 4, c=(1,0,-1,0), s=(0,1,0,-1), and
\[
 a_r(p)=(x_r c_p+y_r s_p)Z_r,
\]
where the generator weights in (K1,K2,K3,J12,J13,J23) are
\[
 Z_0=(0,0,0,1,-1,1),\quad Z_1=(0,1,-1,0,0,1),
\]
\[
 Z_2=(1,0,-1,0,1,0),\quad Z_3=(1,-1,0,1,0,0).
\]
All eight real coefficients are free. Every basis field satisfies the direct
linear connection equation at all 4*4*6 phase/role/generator slots and the ten
linear metric equations at every phase.

Write K_r(p,t)=exp(t a_r(p)) and
E_Q(eta,K(t))=t E_1(p)+t^2 E_2(p)+O(t^3). Exact arithmetic gives
\[
 E_1(p)=0,\qquad \frac14\sum_{p=0}^3 E_2(p)=0
\]
as polynomial identities in all eight coefficients and all ten Gram slots.
This extends the mean quadratic cancellation beyond the single #232 ray.
It does not assert nonlinear joint stationarity of arbitrary superpositions.

The cancellation is genuinely averaged. For x0=x1=1 and the other six
coefficients zero, in component order
(00,01,02,03,11,12,13,22,23,33),
\[
 E_2(p)=\frac{(-1)^p}{4}(0,0,-1,-1,0,1,1,2,0,2).
\]
Consequently a raw superposition can have nonzero order-h^2 pointwise response
while its quadratic phase mean vanishes. Joint metric equations with a smooth
source must also handle these nonzero phase components.

The certificate uses the exact BCH coefficient
\[
 \mathcal R(e^{tX_1}e^{tX_2}e^{tX_3}e^{tX_4})
 =t\sum_iX_i+\frac{t^2}{2}\sum_{i<j}[X_i,X_j]+O(t^3).
\]
It extracts every square and cross coefficient of the known homogeneous
quadratic polynomial using integer arithmetic; it is not a floating-point
sample or a claim that a finite Taylor jet proves an exact nonlinear family.

## 4. Response-defect reduction: overview

Set b_h=(A_h-A_h^sm)/h. Expansion of the literal finite stencil identifies
three possible weak contributions: a discrete curl linear in b_h, a cross
term between the smooth connection and b_h, and a quadratic correlation of
neighboring b_h values. The first two can be tested by discrete summation by
parts once the mean of b_h is shown to vanish. The third is the potential
effective metric defect.

A one-site Young measure does not encode this correlation: each plaquette
uses four differently shifted link values. The relevant quadratic observable
is the Gram derivative of the frozen connection Hessian, contracted with a
joint stencil/frequency correlation measure.

The sufficient finite criterion is
\[
 v^*D_QH_Q(z)[q]v=0
 \quad\text{for all }v\in\ker H_Q(z)\cap\ker C_Q(z),
\]
with the physical Fourier polarization used consistently. H is the Hermitian
connection Euler symbol and C is the linear metric-response symbol.
No uniform inverse or positive spectral gap is part of this criterion.
The diagonal certificate proves a canonical special case. Section 7 proves
the conditional localization theorem, and Section 8 proves the diagonal
condition for every nondegenerate constant solder. The global identity is
refuted by Section 8.3. Its conditional theorem remains valid, while the
stationary-sheet synthesis gives a replacement research route. Neither
requested terminal follows yet.

## 5. Consumption and scope audit of #241

#241 finds the mixed coefficient -sigma(p)/4 in the (01) component at h z
for its valued profile, identity comparator, and original #232 connection.
At z=h its normalized phase-0 value tends to -1/4; at z=h^2 it tends to zero.
The leading four-phase mean is zero.

This is a useful hostile pointwise off-shell control. It is not yet the
counterexample required by this EXP task:

1. The worker does not check E_K on the varying solder or an exact joint
   prescribed-source equation.
2. The identity comparator is not established as the #216 smooth approximate
   solution on that profile.
3. The declared profile has h-dependent value eta+h alpha and is not itself
   one fixed smooth metric sampled at a fixed observation point.
4. The code uses affine solder legs and the flat Gram lift away from eta.
   The displayed rational expression is exact for that solder directional
   derivative. Its leading h z coefficient survives conversion to a smooth
   genuine Gram chart because the full solder gradient at eta is zero;
   exact higher coefficients require the nonlinear section and actual Gram.

These facts preserve the leading hostile calculation and prevent an
unsupported promotion to A4D-JOINT-MICROSTRUCTURE-METRIC-RESPONSE-NOGO.

#227 is separately exact E_K-critical but metric-source-visible at flat Q.
Its z=h^2 normalized response has a nonzero phase component and vanishing
phase mean. Defining a source after inspecting that response is not a
counterexample with a prescribed smooth source or vacuum.

## 6. Scope of the partial result

The results are an exact diagonal mean-quadratic cancellation, its all-solder
extension, and a conditional compensated response theorem. The global linear
identity is refuted. The target remains open on nonlinear realizable response
defects, as formulated in the linked stationary-sheet synthesis. Sections
7-10 retain the proofs, finite controls, and validation.


## 7. Conditional compensated response theorem (proved reduction)

This section proves the implication summarized in Section 4. The argument
is self-contained and uses no external homogenization theorem.

### 7.1 Frozen operators and the single algebraic condition

Let H_Q(z) be the physical connection Euler symbol at the constant Gram Q
and identity links. Since it is the Fourier transform of a real Hessian,
H_Q(z) is Hermitian on |z_r|=1. Let C_Q(z) be the linear metric response to
a connection amplitude at the SAME physical character. In the #216 code
the physical H at character chi is connection_symbol(E,chi^-1); changing
the polarization without changing C would invalidate the condition below.

For a symmetric Gram direction q put J_Q(q,z)=D_Q H_Q(z)[q]. The finite
condition to be proved or refuted is
\[
 \tag{NF}
 v^*J_Q(q,z)v=0\quad\text{whenever}\quad
 H_Q(z)v=0,\quad C_Q(z)v=0 .
\]
It must hold for every Q in a neighborhood of the compact image of the fixed
smooth metric, every unit-torus character z, every Gram direction q, and
every complex amplitude v. This is a joint-kernel quadratic identity, not
a lower bound for H, a connection selector, or a claim of constant nullity.

**Conditional theorem.** Assume (NF), the compact analytic finite-stencil
chart, fixed smooth Q_h, ||A_h||_infinity+||A_h^sm||_infinity <= C h,
the #216 smooth residual E_K(Q_h,A_h^sm)=O(h^infinity), exact E_K(Q_h,A_h)=0,
and ||h^-2 E_Q(Q_h,A_h)||_infinity bounded. Assume also the stated smooth
comparison response is uniformly bounded. Then D_h converges to zero against
every fixed smooth test field.

If, in addition, E_Q(Q_h,A_h)=h^2 tau_h with tau_h converging uniformly to
a prescribed smooth tau, and h^-2 E_Q(Q_h,A_h^sm) converges uniformly to
rho[g] in the SAME component/reconstruction convention, then
\[
 \|D_h\|_{\infty}\longrightarrow0,\qquad \tau=\rho[g].
\]
Under the #216/#223 physical reconstruction rho[g]=-G[g]/2. Thus uniform
smooth-source control upgrades the weak result to the requested strong
response comparison. Existence of a joint sequence is not asserted.

### 7.2 What the finite joint equations actually control

Use the physical norm ||f||_{2,h}^2=h^4 sum_x |f(x)|^2 and set
b_h=(A_h-A_h^sm)/h. This field is uniformly bounded in infinity and L2.

Taylor expansion of E_K in the links, followed by freezing the smooth
metric coefficients over one finite stencil, gives
\[
 \tag{7.1}
 H_{Q_h(x)}(T)b_h=O(h)
\]
uniformly. Here T denotes the four lattice shifts. The smooth comparator
residual divided by h remains superalgebraic. The nonlinear Taylor remainder
before division is O(h^2), and the frozen/variable-coefficient error is O(h^2).

The metric equation, the bounded h^-2 source, and the bounded smooth response
similarly give
\[
 \tag{7.2}
 C_{Q_h(x)}(T)b_h=O(h).
\]
These estimates use both finite Euler slots. They do not say b_h is small.

Every weak L2 subsequential limit b satisfies
H_{Q(x)}(1)b=0: test (7.1) against a smooth function and move each finite
shift onto the smooth coefficient/test. The shifted test converges strongly
to the unshifted test. The zero-phase congruence in #216 makes H_Q(1)
invertible uniformly on this compact nondegenerate image. Hence b=0.
All weak subsequential limits are zero, so b_h converges weakly to zero.
This is weak mean identification, not C1 or strong connection compactness.

### 7.3 Exact remaining moment

For each face the four signed link amplitudes X_i give
\[
 \mathcal R(P)=\sum_i X_i+
 \frac12\sum_{i<j}[X_i,X_j]+O(\max_i|X_i|^3).
\]
With A_h=h(a_h^sm+b_h), the h^-2 response difference has:

1. the tested linear term h^-1 C_Q(T)b_h;
2. the quadratic cross term between a_h^sm=A_h^sm/h and b_h;
3. the pure quadratic metric response of b_h;
4. an O(h) remainder in the volume-weighted L1 norm.

The first term tends to zero by summation by parts: C_Q(1)=0, and its
adjoint on a fixed smooth test is h times a smoothly convergent field.
The second tends to zero because a_h^sm converges smoothly and every fixed
shift of b_h has the same zero weak limit.

For a frozen Q and constant test q, the third term is exactly
\[
 \tag{7.3}
 \frac12\langle b,D_QH_Q(T)[q]\,b\rangle .
\]
This follows by differentiating the quadratic action
(1/2)<b,H_Q(T)b> in its constant metric coefficient. Formula (7.3) identifies
the actual nonlinear metric-variation moment. One-site weak convergence
does not control it.

### 7.4 Uniform epsilon estimate without a spectral gap

On the compact set of Q, z, unit q and unit v, (NF) and continuity imply:
for every epsilon>0 there is a finite C_epsilon such that
\[
 \tag{7.4}
 |v^*J_Q(q,z)v|
 \le \epsilon |v|^2+
 C_\epsilon\bigl(|H_Q(z)v|^2+|C_Q(z)v|^2\bigr).
\]
Proof: otherwise there is a sequence of unit v with both constraint images
tending to zero and the quadratic form bounded away from zero. A convergent
subsequence contradicts (NF). Away from a sufficiently small constraint
image, a bound for J divided by that threshold squared gives C_epsilon.
Homogeneity extends the inequality to every v.

Constants may deteriorate arbitrarily as epsilon tends to zero. No lower
bound on nonzero singular values, inverse at nearby phases, or fixed
resonance rank is required.

### 7.5 Localization closes the weak passage

Take a smooth square partition of unity sum_j psi_j^2=1 at physical length
ell_h, with bounded overlap and |grad psi_j|=O(ell_h^-1). Freeze Q and the test
q in each support, and apply discrete Fourier Parseval and (7.4) to
psi_j b_h. Finite-stencil commutators satisfy
\[
 \|[H_Q(T),\psi_j]b_h\|_{2,h}
 +\|[C_Q(T),\psi_j]b_h\|_{2,h}
 \le O(h/\ell_h)\|b_h\|_{2,h;\,expanded\ support}.
\]
Coefficient freezing adds O(ell_h), and (7.1)-(7.2) add O(h).
The square sums over j stay bounded because overlap is bounded. Replacing
the quadratic form by its localized and frozen versions has error
O(ell_h+h/ell_h).

Choose ell_h=sqrt(h), take h to zero at fixed epsilon, and then take
epsilon to zero. Equation (7.4) makes the sum of (7.3) vanish. Sections
7.2-7.3 now prove the weak response comparison.

This is also a correlation-measure description: any limiting frequency
covariance has range in ker H intersect ker C, and its tested response
moment is annihilated by (NF). The proof above constructs the passage
directly, including the commutators; invoking a Young measure by name is
unnecessary. It neither identifies the microstructure as gauge nor controls
the connection in a strong topology.

### 7.6 Why smooth sources recover a strong response statement

Under the final hypotheses of the theorem,
D_h=tau_h-rho_h converges uniformly to tau-rho[g]. The weak theorem forces
that continuous limiting field to be zero, so ||D_h||_infinity tends to zero.
This step concerns the response alone. Oscillatory connections such as #232
can remain noncompact in their physical derivatives.

If only bounded or weakly converging sources are permitted, this upgrade
does not follow. #227 and the nonzero phase witness in Section 3 demonstrate
why phase averaging and pointwise response must stay distinct.

## 8. All-solder diagonal annihilation theorem

The canonical certificate in Section 3 has an analytic extension:
(NF) holds at z=(i,i,i,i) and z=(-i,-i,-i,-i) for every real nondegenerate
constant solder, even on the full connection kernel before imposing C.

Here is a direct proof using the merged #216 BCH formula. For a face r<s,
the polarized role coefficient matrix at z=(i,i,i,i) has only two nonzero
entries: +i at (r,r) and -i at (s,s). Passing to the physical Euler transpose
reverses both signs and does not change rank or kernel. Thus H_E(i) is a
direct sum of four
6-by-6 matrices of the form i times a real Kirillov form
\[
 (X,Y)\longmapsto \ell_r([X,Y]).
\]
Up to the fixed nondegenerate bivector pairing, ell_r is the sum of the
three oriented complementary solder bivectors. This is the exterior-square
image under the invertible solder E of a fixed NONZERO bivector on the
three-dimensional complementary role space. Hence ell_r is never zero.

For completeness, every nonzero real Lorentz-algebra element has a
two-dimensional real centralizer. Identify boost and rotation components
with a complex three-vector w; the bracket is the complex cross product.
For w!=0, w cross u=0 if and only if u=lambda w, lambda complex. Viewed
over the reals this kernel has dimension two. The invariant nondegenerate
trace pairing identifies this centralizer with the kernel of the Kirillov
form. Thus every block has rank four, and
\[
 \operatorname{rank}H_E(i)=16
\]
for EVERY nondegenerate real solder. The inverse character has the same rank.

A smooth Hermitian matrix of locally constant rank has
\[
 u^* (D H) v=0\qquad (u,v\in\ker H).
\]
Indeed extend v smoothly inside the kernel, differentiate H v=0, and
left-multiply by u*. The preceding constant-rank calculation applies on the
whole nondegenerate solder domain. Therefore (NF) follows at both diagonal
quarter characters for arbitrary Gram variations and arbitrary section
tangents.

This argument covers the mean quadratic channel of the mandatory #232
microstructure on frozen smooth backgrounds. It does not cover every other
character, correlations across general resonant sets, or amplitudes larger
than O(h). The localization theorem accounts for these first two issues
only if (NF) is established on their entire possible frequency support.

### 8.1 Exact L=4 flat-solder response-moment census

The supplemental exact certificate
`certificates/a4d_joint_response_nf_l4_check.py` exhausts all
\(4^4=256\) table characters at the standard solder. For each character it
compares the complete direct \(24\times24\) connection symbol and
\(10\times24\) metric symbol against the merged #216 owner matrices, with
the reciprocal convention
\[
 H_\eta(\zeta)=H_{AA}(\zeta),\qquad
 C_\eta(\zeta^{-1})=H_{AQ}(\zeta)^T.
\]
All 256 full-matrix comparisons pass exactly over \(\mathbb Q(i)\).

The joint kernel is nonzero on exactly 20 characters: eighteen one-dimensional
carriers with \(\operatorname{rank}H=22\) on 12 characters or
\(\operatorname{rank}H=20\) on 6, and the two diagonal quarter-wave
characters with joint dimension four and \(\operatorname{rank}H=16\). The
total joint-null dimension is 26. On every one of these 20 exact kernels, all
ten Gram directions satisfy
\[
N^*D_QH_\eta(\zeta)[q]N=0.
\]
This is 200 exact matrix identities, including all three curved nongauge
one-dimensional carriers of #234 and the full diagonal kernel. No #231/#234
kernel table is imported for the census; the symbols are rebuilt and scanned
directly.

As a finite background stress test, each of the eighteen one-dimensional
carriers has zero joint kernel at three exact nonstandard constant-solder
samples: \(E=\operatorname{diag}(2,3,5,7)\), one upper shear, and one rational
off-diagonal solder. The all-solder diagonal theorem in Section 8 covers the
two diagonal quarter-wave families. These samples show that the other flat
resonances lift at the tested backgrounds; they do not classify the resonance
set for general \(Q\).

The result closes the complete L=4 flat-solder finite-frequency test only.
### 8.3 Exact shear witness, reproduced

On the upper shear solder \(E=I+E_{01}+E_{12}\),

\[
E=\begin{pmatrix}1&1&0&0\\0&1&1&0\\0&0&1&0\\0&0&0&1\end{pmatrix},
\]

at the self-inverse character \(z=(-1,1,-1,1)\), the literal #216 maps give

\[
\operatorname{rank}H=20,\quad\operatorname{rank}C=9,\quad\operatorname{rank}(H,C)=23.
\]

The joint kernel is one-dimensional. Its content-one integer generator, in role blocks \((K_1,K_2,K_3,J_{12},J_{13},J_{23})\), is

\[
\begin{aligned}
v_0&=J_{23},\\
v_1&=0,\\
v_2&=-K_3-J_{13}+J_{23},\\
v_3&=2K_1+K_2+J_{12}.
\end{aligned}
\]

The ten quadratic moments in the order \((00,01,02,03,11,12,13,22,23,33)\) are

\[
(0,0,0,0,-2,0,0,0,0,0).
\]

In particular \(v^*D_QH_Q(z)[q_{11}]v=-2\). The same character is jointly invertible at the flat solder, so this kernel is created by the shear. Because \(z^2=(1,1,1,1)\), the quadratic self-interaction of this carrier lands in the zero-frequency channel. This is a finite failure of (NF). It is not a smooth-background NOGO.

### 8.4 Period-2 Lyapunov–Schmidt step

The real carrier is the period-2 field \(\sigma(x)=(-1)^{x_0+x_2}\). Translation by \(e_0\) flips \(\sigma\) and sends the amplitude \(u\) to \(-u\). On a constant solder the action is even, so the reduced connection equation is odd and the metric Euler is even.

Quadratic sampling of two copies of this character is spatially constant, because
\(\sigma(x)\sigma(x+a)=(-1)^{a_0+a_2}\). The first connection correction is therefore a constant, zero-frequency link shift \(u^2\zeta\). On the period-2 cell the literal plaquette Euler of the pure ray, summed over all 16 sites and all 24 constant generator directions, has vanishing orders \(u^0\) and \(u^1\) and integer order-\(u^2\) source

\[
s=(0,24,16,-24,-16,0,\ -8,0,-24,16,-8,-16,\ 0,-24,-16,24,16,0,\ 0,0,0,0,0,0).
\]

The same summed Euler, linearized in a constant shift, is an invertible \(24\times 24\) matrix. Its solution is

\[
\begin{aligned}
\zeta_0&=\tfrac12(-1,1,1,1,1,0),\\
\zeta_1&=0,\\
\zeta_2&=\tfrac12(-1,-2,-1,-2,-1,0),\\
\zeta_3&=(-2,-1,1,-1,1,-2).
\end{aligned}
\]

After this elimination the order-\(u^2\) connection Euler is identically zero. The order-\(u^2\) metric Euler on the cell does not move. In the ten-component order it remains

\[
E_Q^{(2)}=u^2(0,0,0,0,-16,0,0,0,0,0).
\]

The pure ray without \(\zeta\) has the same metric jet. Solving \(E_K\) at this order does not cancel the \(q_{11}\) defect.

Vacuum \(\tau=0\) therefore forces \(u=0\). The constant source frozen from the component order already written in §3 is \(\tau=e_{00}\). Its \(00\)-slot is unmatched, so that predeclared source has no quadratic joint branch either. A source supported only on \(q_{11}\) would fit this jet, but it was not fixed in advance and is not used.

On this constant background the identity connection has vanishing curvature, hence \(E_Q=0\), and the Einstein tensor of a constant metric vanishes. That is the #216 comparator at this order. No joint-critical sequence with a nonzero normalized gap is obtained. The metric-response NOGO stays unclaimed. The exact obstruction is the surviving cell equation \(E_Q[q_{11}]=-16u^2\).

### 8.6 What the next Euler orders do

With that constant correction kept, the resonant projection of the cell connection Euler vanishes through order \(u^5\). The range does not. The odd sector at order \(u^3\) is nonzero; one recorded component is \(32\). The even sector at order \(u^4\) is nonzero; one recorded component is \(-\tfrac43\). So the ansatz is an exact connection solution only through order \(u^2\).

A link correction of order \(u^3\) or \(u^4\) changes the metric Euler only at order \(u^4\) and higher. It cannot cancel \(-16u^2\). Therefore every constant source with a component outside the \(q_{11}\) line fails the leading joint balance, including vacuum and the predeclared \(\tau=e_{00}\). The line \(\tau\parallel e_{11}\) is the only quadratic opening. It was read off the moment, so it is not used as a predeclared source. Section 8.7 solves the order-\(u^3\) and order-\(u^4\) range; the resonant projection above was computed before that elimination.

### 8.5 Flat L=8 census

The merged #216 owner symbols \(H_{AA}(z)\) and \(H_{AQ}(z)\) are compiled
once as rational Laurent polynomials in the four table phases and specialized
to \(\mathbb F_{17}\), with \(\omega=9\) of order eight, \(\sqrt2\mapsto 11\) and
\(i\mapsto 13\). Every Laurent coefficient denominator is checked nonzero mod
17, so the specialization is sound. A full-rank modular minor certifies full
rank over \(K=\mathbb Q(\sqrt2,i)\); modularly singular points are then
verified exactly in \(K\).

This census was first reported in session logs only. It has been re-run here
from scratch against the committed certificate
`certificates/a4d_joint_response_nf_l8_check.py` and reproduces exactly, with
zero failures:

| quantity | value |
|---|---|
| characters scanned | \(8^4 = 4096\) |
| modular rank profile | \(\{24: 4052,\ 23: 42,\ 20: 2\}\) |
| candidates after the modular screen | 44 |
| exact joint ranks on survivors | \(\{23: 42,\ 20: 2\}\) |
| \((\mathrm{rank}\,H_{AA},\ \mathrm{nullity})\) distribution | \((22,1)\times 36,\ (20,1)\times 6,\ (16,4)\times 2\) |
| exact response-moment tests | \(44\times 10 = 440\), all zero |

Every candidate is additionally checked against the #216 owner symbols \(H\)
and \(C=H_{AQ}^{\mathsf T}\) in the documented inverse-polarization
convention, so the census is convention-controlled and not a re-derivation.
This is a finite flat-solder stress test. It does not restore global (NF): the
shear witness of \S 8.3 remains a counterexample on a non-flat solder.

It does not establish (NF) on the continuous unit torus away from this finite
grid, nor at every Gram in the compact chart. The conditional homogenization
argument therefore remains conditional.

### 8.7 The metric image is a point, and order \(u^5\) cuts the amplitude

The order-\(u^2\) metric jet is affine in a constant link correction. Its
derivative vanishes on all 24 basis directions and on a mixed direction, so
the value does not move:

\[
E_Q^{(2)}=u^2(0,0,0,0,-16,0,0,0,0,0).
\]

The image is that single point. An earlier draft described a free block
\(Z\) and a rank-one image \(\operatorname{span}(e_{q_{11}})\). That
description is withdrawn: the connection equation fixes the correction, and
the metric value is not a line that a correction can travel. Vacuum, the
predeclared source \(\tau=e_{00}\), and the constant profile \(e_{01}\) all
miss the point. The certificate is
`a4d_joint_response_shear_source_reachability_check.py`.

The odd connection linearization at the shear character has rank 20 and a
four-dimensional kernel. The resonant witness is \(2K_0+K_1\) in that
kernel, and it also lies in the left kernel. The order-\(u^3\) source is in
the column space. One witness-orthogonal solution is recorded in
`a4d_joint_response_shear_order5_check.py`. The order-\(u^4\) constant
correction is then fixed by the even operator, which has rank 24 and agrees
with the committed quadratic source on the committed \(\zeta\).

On that solution, and on the same solution plus each of the three
witness-orthogonal kernel directions, the witness projection of the
order-\(u^5\) connection Euler equals \(-432\). The fourth kernel direction is
the witness itself. It is exactly the leading amplitude direction of the
period-2 branch, so it is not an independent reduced modulus: the change

\[
 \eta\mapsto\eta+tW
\]

is generated through order four by the amplitude reparameterization

\[
 u=v+t v^3,
 \qquad
 \xi\mapsto\xi+2t\zeta.
\]

The checker verifies this coefficient-by-coefficient in the actual 24 link
coordinates. Under the same substitution

\[
 -432u^5=-432v^5+O(v^7),
\]

so the first nonzero resonant coefficient is invariant. The reparameterization
also induces an order-\(v^5\) link correction; it enters through the odd
linearized operator and has zero witness projection because the witness is an
exact left-kernel vector. Thus the previously open WITNESS-kernel modulus is
closed: all four order-\(u^3\) kernel directions either leave the coefficient
unchanged or are amplitude reparameterization.

No further odd correction cancels that component. The reduced connection
equation on this period-2 ansatz is therefore \(-432u^5=0\), so \(u=0\).
This cuts every constant metric source on this ansatz, including a profile
parallel to \(q_{11}\). That profile was read off the quadratic jet and is not
used as a predeclared source.

The order-\(u^4\) metric jet on these solutions stays supported on \(q_{11}\).
One kernel direction changes its coefficient, from \(-7040/177\) to
\(55264/177\). An order-\(u^4\) constant correction does not move that jet.
None of these changes touches the order-\(u^2\) point.

This is not the smooth-background metric-response NOGO. The connection
equation removes the amplitude, so there is no nonzero joint-critical
sequence and no normalized gap against the #216 sheet.

### 8.8 The rest of the L=4 grid on this solder

The same upper shear was screened at all \(4^4=256\) characters. The
bracket forms are computed once from the solder; each character only
enters the role matrix. At \(z=(-1,1,-1,1)\) the assembled joint symbol
matches the #216 owner matrices. Exactly three characters are singular:

| character | joint rank | nullity | moments |
|---|---|---|---|
| \((i,i,i,i)\) | 20 | 4 | all ten blocks zero |
| \((-i,-i,-i,-i)\) | 20 | 4 | all ten blocks zero |
| \((-1,1,-1,1)\) | 23 | 1 | \((0,0,0,0,-2,0,0,0,0,0)\) |

The two diagonal characters are the quarter-wave kernels of the all-solder
identity in §8. Their moments vanish, so they are not NF defects. The only
nonzero moment on this solder and this grid is the carrier already cut in
§8.7. The certificate is
`a4d_joint_response_shear_l4_support_check.py`. This is one solder and one
finite grid. It does not restore global (NF).

### 8.9 A second defect in a fixed solder family

The same L=4 screen was run on a family fixed before the ranks were read:
the six pure shears \(I+E_{ab}\), the upper shear, the two length-two chains
\(I+E_{12}+E_{23}\) and \(I+E_{01}+E_{13}\), \(\operatorname{diag}(2,3,5,7)\),
and the curved rational sample of §8.1. Every Gram in the family is
nondegenerate. The only nonzero moments are

| solder | character | moment |
|---|---|---|
| \(I+E_{01}+E_{12}\) | \((-1,1,-1,1)\) | \((0,0,0,0,-2,0,0,0,0,0)\) |
| \(I+E_{01}+E_{13}\) | \((-1,1,1,-1)\) | \((0,0,0,0,-2,0,0,0,0,0)\) |

The second witness, in the same generator order, is
\(J_{23}\) on role 0, zero on role 1, \(-2K_1-K_3-J_{13}\) on role 2, and
\(K_2+J_{12}+J_{23}\) on role 3. Its square is again the zero frequency.
The pure shear \(I+E_{01}\) has a kernel at the first character, and that
moment vanishes, so the double step is essential.

On the chain, the period-2 ray has vanishing connection Euler through order
\(u\). The order-\(u^2\) source has a unique constant solution, and the cell
metric jet on that solution is
\(u^2(0,0,0,0,-16,0,0,0,0,0)\). Vacuum forces \(u=0\) at this order. The
certificate is `a4d_joint_response_solder_family_check.py`. The \(q_{11}\)
line is not a predeclared source.

### 8.10 The chain is cut at order \(u^5\)

The same elimination used for the upper shear applies to the chain. The odd
linearization has rank 20. The witness lies in its left kernel. The
order-\(u^3\) source is solvable. After the unique order-\(u^4\) correction,
the witness projection at order \(u^5\) equals \(-432\) on the
witness-orthogonal solution and on a basis of the remaining kernel
complement. The reduced connection equation is \(-432u^5=0\), so \(u=0\).
The certificate is `a4d_joint_response_chain_order5_check.py`.

Both finite NF defects of §8.9 are therefore absent from every formal
period-2 joint solution. This still does not restore (NF) on other
characters or other solders, and it does not produce a joint-critical
sequence.

### 8.11 Sampled unipotent shear slice and the exact sign partner

Section 9 of this memo left "NF defects on other solders" open. A previous
revision overclaimed that a finite positive-\(a\) sample closed the rational
unipotent slice and isolated the defect at \(a=1\). That statement is
withdrawn.

Parameterise the solder by
\[
S(a)=I+a\bigl(E_{01}+E_{12}\bigr),\qquad a\in\mathbb Q,\ a\neq 0.
\]
The whole \(L=4\) grid is now checked at
\[
a\in\{-1,\tfrac12,\tfrac23,1,\tfrac32,2,3\}.
\]
Every numerically scouted singular character is verified exactly over
\(\mathbb Q(i)\) with all ten Gram-direction moment blocks. The certificate is
\`a4d_joint_response_shear_family_support_check.py\`.

| \(a\) | singular characters | nullity | nonzero moments |
|---|---|---|---|
| \(1/2,\,2/3,\,3/2,\,2,\,3\) | \((i,i,i,i)\), \((-i,-i,-i,-i)\) only | 4 each | 0 |
| \(+1\) | the two diagonals, **plus** \((-1,1,-1,1)\) | 4, 4, **1** | 0, 0, **1** |
| \(-1\) | the two diagonals, **plus** \((-1,1,-1,1)\) | 4, 4, **1** | 0, 0, **1** |

At both \(a=1\) and \(a=-1\), the content-one carrier has the same exact
moment
\[
(0,0,0,0,-2,0,0,0,0,0).
\]
The \(a=-1\) point is the signature-preserving sign partner of the committed
upper shear. A nonzero \(24\times24\) joint minor on this carrier factors as
\[
256(a-1)^4(a+1)^4(a^2+1)^4,
\]
which exposes both rational candidates \(a=\pm1\).

The two diagonal quarter-wave kernels remain moment-free in the sampled
controls. No exhaustive rational-\(a\) classification is claimed here:
one nonzero minor only supplies a finite candidate set for its own row choice,
and a complete minor/gcd cover is still required before promoting
"\(|a|=1\) only" to a theorem.

\[
\boxed{\texttt{SHEAR-SAMPLED-SIGN-PARTNER-DEFECTS-CERTIFIED}}
\]

Scope: finite \(L=4\) grid and the displayed rational sample. Global (NF)
remains refuted, while the all-rational unipotent-slice classification remains
open.

### 8.12 L=8 grid on the two defect solders

The same two solders were screened at all \(8^4=4096\) characters. Bracket
forms are reduced in \(\mathbb F_{17}\) with the L=8 specialization
\(\omega=9\), \(\sqrt2\mapsto 11\), \(i\mapsto 13\). One mixed 8th root was
compared entrywise with the exact symbol. Full modular rank certifies full
rank over \(\mathbb Q(\sqrt2,i)\). The four modularly singular characters on
each solder were checked exactly.

On both solders the modular rank counts are
\(\{24:4092,\ 20:2,\ 23:2\}\). The rank-20 characters are the diagonal
quarter-waves, with vanishing moments. One rank-23 character is a modular
false positive and is exactly full rank. The remaining character is the cut
carrier: \((-1,1,-1,1)\) on the upper shear and \((-1,1,1,-1)\) on the chain,
each with content-one moment \((0,0,0,0,-2,0,0,0,0,0)\). The certificate is
`a4d_joint_response_defect_l8_check.py`.

Thus on these two solders no 8th-root character other than the cut carriers
is an NF defect.

### 8.13 Sixteenth roots on the same solders

All \(16^4=65536\) characters were ranked in \(\mathbb F_{17}\), where \(3\)
has order 16. Full modular rank certifies full rank. The characters that
remain singular in \(\mathbb F_{97}\) were checked exactly. On each solder
there are three: the diagonal quarter-waves, with vanishing moments, and the
carrier already cut at order \(u^5\). The modular counts are
\(\{24:65459,\ 23:69,\ 22:6,\ 20:2\}\). The certificate is
`a4d_joint_response_defect_l16_check.py`.

Characters outside this grid remain open, so (7.4) is still not restored on
the whole torus.

### 8.14 The reciprocal is defined on every root of unity

An earlier draft of this section treated \(\gcd(k,L)=1\) as the condition for
\(\chi=\zeta^{-1}\) to exist, and it called the complementary rows of the
\(L=4\), \(L=8\), and \(L=16\) censuses a convention gap. That reading is
withdrawn. The terminal name attached to it is not a result of this task.

The metric block uses the owned reciprocal of each phase component. On a
cyclic grid the component is \(\omega^{k}\) with \(\omega^{L}=1\). Its
reciprocal is \(\omega^{-k}\), the grid point of exponent \((-k)\bmod L\).
This holds for every exponent, including those that are not primitive. The
count \(\varphi(L)\) is the number of primitive \(L\)-th roots. It does not
decide invertibility. In particular the phases \(1\) (exponent \(0\)) and
\(-1\) (exponent \(L/2\) when \(L\) is even) are invertible.

Both defect characters are fixed by the reciprocal:
\[
(-1,1,-1,1)^{-1}=(-1,1,-1,1),\qquad
(-1,1,1,-1)^{-1}=(-1,1,1,-1).
\]
On \(L\in\{4,8,16\}\) every exponent of either character fails
\(\gcd(k,L)=1\). The withdrawn reading would therefore have placed the
certified counterexamples to (NF) outside the domain. Section 8.1 already
compares all \(256\) flat characters, including those non-primitive phases,
with the #216 owner matrices.

The certificate
`a4d_joint_response_phase_invertibility_check.py` calls the owned
`inverse_character` on every root for
\(L\in\{4,6,8,9,10,12,15,16\}\) and checks the two defect characters. It
does not restore (NF), and it does not change the moment census.

Characters that are not 16th roots remain inside the domain of the
reciprocal, and they remain open for the moment identity.

### 8.15 Connection determinant on four lines through the defects

The four lines are fixed before the determinant is read. On the upper shear
they are the phases \((z,1,-1,1)\) and \((-1,1,z,1)\). On the chain
\(I+E_{01}+E_{13}\) they are \((z,1,1,-1)\) and \((-1,1,1,z)\).

The varying component enters a connection entry only as \(z\) or as \(z^{-1}\).
The cleared matrix \(zH(z)\) has entries in \(\mathbb Q[z]\) of degree at most
2, so \(\det(zH(z))\) has degree at most 48. Exact rational values at 49
integers determine that polynomial, and the determinant at the next six
integers agrees with it. All four lines produce the same element of
\(\mathbb Q[z]\),
\[
\frac{1}{16}z^{18}(z+1)^{8}(z^{2}-2z+5)(5z^{2}-2z+1).
\]
Its value at \(z=2\) is \(9137111040\). It vanishes at the defect \(z=-1\) and
not at \(z=1\).

Both quadratics are irreducible, with discriminant \(-16\). A root of modulus
1 would have real part \(1/3\) and imaginary part \(0\), which does not lie on
the circle. The four roots are \(1\pm 2i\), of squared modulus \(5\), and
\((1\pm 2i)/5\), of squared modulus \(1/5\).

On the unit circle the only zero is therefore \(z=-1\). At every other unitary
point of these four lines the connection block is invertible, so the joint
kernel is trivial and the tested moment is vacuous. The order-8 zero at
\(z=-1\) is the order of this determinant, not a corank; the rank at that
carrier remains the rank already certified in §§8.3 and 8.9.

The four algebraic roots lie off the unit circle. Section 8.16 ranks the
joint symbol there: it is full. Unitary characters off these lines and away
from the defects remain open. Neither final terminal follows.

The certificate is `a4d_joint_response_defect_line_minor_check.py`.

### 8.16 The joint corank locus is isolated at each defect

The joint symbol is a holomorphic \(34\times 24\) matrix on \((\mathbb C^\times)^4\).
At each defect its rank is 23, the right kernel has dimension 1, and the left
kernel has dimension 11. Pairing the left kernel with the four phase
derivatives of the symbol on the right kernel produces an \(11\times 4\) matrix.
On the upper shear that matrix has rank 3 and kernel spanned by
\((11,0,8,9)\). On the chain the kernel is spanned by \((11,0,9,8)\).

Any holomorphic curve of joint corank through the defect would have its leading
tangent on that line. Along the line, the order-\(t\) equation for a kernel
correction is solvable, and the order-\(t^{2}\) pairing does not lie in the
column space of the \(11\times 4\) matrix. The same quadratic obstruction
appears at order \(t^{2k}\) for a branch of contact \(k\), and a higher jet can
cancel only the part already in that column space. Therefore no holomorphic
curve of joint corank passes through either defect. Each defect is an isolated
point of the corank locus in \((\mathbb C^\times)^4\).

In a neighborhood of either defect every other character, unitary or not, has
joint rank 24. The tested moment is vacuous pointwise there. This does not
supply a uniform constant in (7.4) near the puncture: its constants may
diverge as the character approaches the certified NF defect. The order-8 zero of one connection
determinant and the order-\(u^5\) amplitude cut are separate statements. The
diagonal quarter-waves remain other corank points, with vanishing moments, and
they do not lie in this neighborhood.

The sixteen points where the connection determinant of §8.15 vanishes off the
unit circle were ranked directly. On every one of them the joint symbol has
rank 24, so the metric rows restore the column rank. They are not further
corank points.

Characters at a finite distance from these two defects, and solders outside
the certified families, remain open. Neither final terminal follows.

The certificate is `a4d_joint_response_defect_isolation_check.py`.

### 8.17 Linear joint-kernel bookkeeping; nonlinear orders kept distinct

A direction \(b\in\ker[H;C]\) satisfies \(Hb=Cb=0\) by construction.
The certificate `a4d_joint_response_joint_critical_check.py` checks this
linear identity. It does not compute a nonlinear obstruction.

The previous interpretation of an order-\(u^5\) reduced coefficient as a
quadratic coefficient is withdrawn. For a corrected path
\(a(u)=u b+u^2a_2+\cdots\), the actual second-order connection equation is
\[
H a_2+N_2(b,b)=0.
\]
A nonzero bare self-interaction can therefore be absorbed by \(a_2\).
The separate order-five certificates explicitly use such lower-order
corrections. Their reported \(-432u^5\) term must retain its fifth order and
its period-two ansatz scope; it cannot certify \(u^2S=0\).

The prior terminal `JOINT-CRITICAL-OBSTRUCTION-IS-QUADRATIC-NOT-LINEAR`
does not follow from this calculation and is not claimed. The stationary-sheet
synthesis explains why even a valid fixed-cell fifth-order cutoff still
requires uniform control of sidebands and slow-background terms before
excluding general joint-critical sequences.

### 8.2 Amplitude boundary

The O(h) log-link bound in Section 7 is essential to this quadratic proof:
it makes the normalized cubic remainder O(h). For larger amplitudes merely
tending to zero, h^-2 ||A_h||_infinity^3 need not vanish; additional moments
may survive. The exact flat #232 identity still holds at those amplitudes,
but this proof does not extend it to a varying background.

## 9. Kill-first audit and current exact frontier

**Abstract hostile control; not a D0 action or counterexample.** Smooth
prescribed sources, weak mean zero and a regular zero-phase connection block
do not make (NF) automatic. On a periodic scalar lattice take
B=T_0+T_0^-1 and the test functional
S(q,a)=(1/2) sum_x [(Ba)_x^2+q_x a_x^2]. At q=0, its connection Hessian has
H(1)=4 and H(i)=0. For a_h=h sigma(sum x_r mod 4) with
sigma=(1,1,-1,-1), B a_h=0 and sigma^2=1. Thus
E_a=0 and E_q=h^2/2 exactly, with the prescribed smooth normalized source
tau=1/2. The smooth comparator a^sm=0 has zero response, so the normalized
response gap is 1/2. Here C=0 and D_q H=1 on the resonant kernel, violating
(NF). This checks the logical role of the missing identity and does not
modify the naked star or certify its NOGO.


The following routes have been decided:

| Route | Verdict |
|---|---|
| Equal prescribed source on both exact comparators | Exact tautology; no Einstein identification |
| #226 Lipschitz bound applied to O(h) microstructure | Insufficient: h^-2 loss remains |
| #223 applied to grid oscillations | Hypotheses absent |
| #227 used as vacuum joint counterexample | Invalid: its metric equation is nonzero |
| #241 promoted to smooth-background joint NOGO | Invalid: joint equation, comparator, and fixed-background contracts unproved |
| One-site Young measure alone | Insufficient: shifted quadratic correlations are missing |
| Phase average substituted for a pointwise limit | Invalid without the strong-source upgrade |
| Diagonal joint carrier mean quadratic stress | Exactly zero; finite certificate |
| Frozen diagonal characters at arbitrary solder | (NF) proved analytically |
| Entire L=4 grid at the flat solder | (NF) exact on all 20 nonzero joint kernels |
| Global all-background joint-kernel (NF) | **REFUTED** by the exact shear witness in §8.3 |
| Period-2 shear carrier under the joint equations | Connection equation forces \(u=0\) at order \(u^5\); no nonzero joint-critical sequence |
| Other L=4 characters on this upper shear | Only the cut character has a nonzero moment |
| Both finite defects of the eleven-solder family | Absent from formal period-2 joint solutions: each reduced connection coefficient is \(-432u^5\) |
| Characters outside the 16th-root grid | OPEN away from the two defects. Each defect is isolated in \((\mathbb C^\times)^4\) (§8.16); distant characters remain open |
| Unitary points of the four lines through the two defects | Connection determinant vanishes only at the known carrier; the joint kernel is trivial at every other unitary point (§8.15) |
| Off-circle zeros of that connection determinant | Joint rank 24 at all sixteen points (§8.16) |
| Joint corank locus through either defect | Isolated point. Tangent line blocked at second order (§8.16) |
| Joint-critical replacement for (NF) on the whole smooth image | MISSING |
| Strong connection compactness or uniqueness | Not used or requested |

The previous “prove all-phase NF” route is closed: §8.3 gives an exact finite
counterexample to the algebraic identity. The conditional theorem in §§7.1–7.6
therefore remains a valid implication but is not a global closure theorem for
the naked-star system.

Both finite NF defects of the fixed family are absent from formal period-2
joint solutions. The conditional theorem of §7 still assumes (NF) at every
character of every solder in the smooth image. Inequality (7.4) fails at
the two certified defects. Each of those points is isolated in
\((\mathbb C^\times)^4\), so every nearby character has full joint rank and
pointwise constraint estimates hold there because there is no kernel. Their
constants are not uniform toward the defect, and an isolated frequency can
carry a full quadratic correlation measure. Distant characters remain open, and the order-\(u^5\) cut does not by itself classify them. No certified joint-critical sequence
has a nonzero normalized gap against the #216 sheet: the flat #232 family
is response-null, and the #259 lift tends to zero without being joint.

The missing global statement is that (7.3) vanishes on every correlation
measure realizable by the full nonlinear equations \(E_K=0\) and
\(E_Q=h^2\tau_h\) under the fixed smooth-background/source contract. This
includes coupled carriers and correctors, not only isolated plane-wave
amplitudes. The linked synthesis gives the exact defect functional and an
alternative quantitative horizontal-lift criterion.
Neither requested terminal follows from the finite cuts above.

A finite-frequency census may stress-test which resonances satisfy the moment
identity, but no finite grid can restore a global NF theorem once the shear
counterexample exists. Conversely, a finite NF failure alone is not the
requested NOGO.

Current verdict: IN PROGRESS. The L=8 grids of the two defect solders add no
further NF defect. Neither
A4D-JOINT-PALATINI-RESPONSE-DECOUPLING-CLOSED nor
A4D-JOINT-MICROSTRUCTURE-METRIC-RESPONSE-NOGO is claimed.

## 10. Validation

The task-specific integer certificate is
`certificates/a4d_joint_response_decoupling_microstructure_check.py`; the
supplemental exact symbol/moment certificate is
`certificates/a4d_joint_response_nf_l4_check.py`.

- All eight direct joint-linear basis tests: PASS.
- 8 times 96 connection Euler coefficient identities: PASS.
- Every linear metric slot at all four phases: PASS.
- All eight square and 28 cross quadratic mean coefficients: PASS.
- Alternating pointwise witness and #232 ray guard: PASS.
- All 256 flat-solder H/C characters match the #216 owner symbols exactly.
- All 20 nonzero L=4 joint kernels pass all ten response-moment identities
  (200 exact matrix tests); total joint-null dimension is 26.
- All eighteen one-dimensional carriers lift at three exact nonstandard
  constant-solder samples.
- The owned #232 exact rational all-edge certificate and #241 mixed-response
  certificate: PASS as narrow input controls; no symbol census is redone.

The analytic localization and all-solder diagonal proofs are research proofs,
not Lean theorems. D0 guards run #2045 at 6d2637dc passed all applicable
steps. The final synchronized-head guard result is recorded in the PR.
