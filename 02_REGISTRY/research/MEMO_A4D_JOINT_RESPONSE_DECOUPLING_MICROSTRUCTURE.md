# A4D — joint response decoupling modulo microstructure

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`  
Execution: PR #240  
Launch baseline: `83a18af7c08c998ffd7d5bf5209aabaee74a390f`  
Status: PARTIAL / BLOCKED on the all-phase identity (NF); neither requested terminal is claimed.

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
condition for every nondegenerate constant solder. The remaining all-phase
identity is open. Neither requested terminal follows yet.

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
extension, and a conditional compensated response theorem. The target remains
open on the all-phase joint-kernel identity. Sections 7-10 provide the proofs,
precise remaining condition, and validation.


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

### 8.1 Amplitude boundary

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
| All-phase, all-background joint-kernel (NF) | OPEN |
| Strong connection compactness or uniqueness | Not used or requested |

The **single first missing identity on this route** is (NF) on the remaining
unit-torus characters and the declared compact metric chart. Sections
7.1-7.6 prove that this finite identity would suffice for the stated O(h)
joint-critical class, including #232 at both required scalings, without a
uniform inverse or strong connection compactness.

Failure of (NF) at a finite carrier would identify a possible quadratic
defect, not by itself an exact smooth-background NOGO. A negative terminal
would still require solving the nonlinear joint equations with the declared
prescribed source and #216 comparator. The exact diagonal and #241 controls
do not supply such a counterexample.

Current verdict: PARTIAL / BLOCKED ON (NF). Neither
A4D-JOINT-PALATINI-RESPONSE-DECOUPLING-CLOSED nor
A4D-JOINT-MICROSTRUCTURE-METRIC-RESPONSE-NOGO is claimed.

## 10. Validation

The task-specific certificate is
certificates/a4d_joint_response_decoupling_microstructure_check.py.

- All eight direct joint-linear basis tests: PASS.
- 8 times 96 connection Euler coefficient identities: PASS.
- Every linear metric slot at all four phases: PASS.
- All eight square and 28 cross quadratic mean coefficients: PASS.
- Alternating pointwise witness and #232 ray guard: PASS.
- The owned #232 exact rational all-edge certificate and #241 mixed-response
  certificate: PASS as narrow input controls; no symbol census is redone.

The analytic localization and all-solder diagonal proofs are research proofs,
not Lean theorems. D0 guards run #2045 at 6d2637dc passed all applicable
steps. The final synchronized-head guard result is recorded in the PR.
