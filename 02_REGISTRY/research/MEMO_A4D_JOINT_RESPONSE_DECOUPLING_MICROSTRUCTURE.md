# A4D — joint response decoupling modulo microstructure

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`  
Execution: PR #240  
Launch baseline: `83a18af7c08c998ffd7d5bf5209aabaee74a390f`  
Status: IN_PROGRESS; neither requested terminal is claimed.

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
prescribed independently of the geometric response and converging to a fixed
smooth covector field. Vacuum tau_h=0 is included. K_h^sm is the designated
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

## 4. Response-defect reduction under development

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

The intended finite criterion is
\[
 v^*D_QH_Q(z)[q]v=0
 \quad\text{for all }v\in\ker H_Q(z)\cap\ker C_Q(z),
\]
with the physical Fourier polarization used consistently. H is the Hermitian
connection Euler symbol and C is the linear metric-response symbol.
No uniform inverse or positive spectral gap is part of this criterion.
The diagonal certificate proves a required canonical special case; the
all-background, all-phase condition and its localization proof are being
audited. Neither requested terminal follows yet.

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

## 6. Current disposition

The new result is exact diagonal mean-quadratic response cancellation.
The target remains open. The first candidate missing identity is the
all-background joint-kernel quadratic annihilation condition in Section 4,
together with its explicitly stated localization hypotheses. Further results
and validation are recorded in subsequent revisions of this memo.
