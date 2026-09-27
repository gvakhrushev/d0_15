# A4D metric-null Hessian complex

**Task:** \`WRK-A4D-METRIC-NULL-HESSIAN-COMPLEX\`  
**Status:** exact finite symbol owner  
**Terminal:** \`J2-METRIC-NULL-HESSIAN-COMPLEX-EXACT\`

## 1. Result

The universal two-real-dimensional metric-only block of the conjugate-paired
L=4 carrier is not an accidental orbit-by-orbit kernel and does not require
the missing \`E_sp\` owner to define it.

Let the accepted polarized metric-response symbol be

\[
C(z)=H_{AQ}(z):\operatorname{Sym}^2\mathbb C^4\to
\mathbb C^{24},
\]

and define the backward character difference

\[
d_r(z):=z_r^{-1}-1.
\]

For every nontrivial character \(d\neq0\),

\[
\boxed{
\ker C(z)
=
\operatorname{span}_{\mathbb C}
\left\{
q_{\rm null}(z)
\right\},
\qquad
q_{\rm null}(z)=d(z)d(z)^T.
}
\]

Equivalently, with \(\operatorname{vec}_{\rm sym}\) in the repository's ten
symmetric metric slots,

\[
\boxed{
C(z)\operatorname{vec}_{\rm sym}\!\bigl(d d^T\bigr)=0.
}
\]

Moreover \(\operatorname{rank}C(z)=9\) for every \(d\neq0\). This is
pointwise, not merely generic: the certificate covers projective \(d\)-space
by the four charts \(d_j=1\) and, on each chart, verifies explicit
\(9\times9\) minors whose ideal is the unit ideal. Hence there is no
exceptional nonzero rank-drop stratum. At the trivial character
\(z=(1,1,1,1)\), \(d=0\) and \(C=0\).

Thus the physical conjugate-paired metric-only plane of #262 is the
realification of one complex line. Its owner is the character-dependent
Hessian line above.

## 2. Exact complex

The result may be written as the exact symbol sequence

\[
0\longrightarrow\mathbb C
\xrightarrow{\ \mathsf H_d\ }
\operatorname{Sym}^2\mathbb C^4
\xrightarrow{\ C(d)\ }
\mathbb C^{24},
\]

where

\[
\mathsf H_d(\phi)=d d^T\phi.
\]

For \(d\neq0\),

\[
\operatorname{im}\mathsf H_d=\ker C(d).
\]

This is an exact statement about the polarized finite star response. It is
useful to call it the **metric-null Hessian complex**. The name records the
operator structure only. It does not declare a full diffeomorphism gauge
symmetry of the nonlinear finite action.

In position-space language, \(d_r=z_r^{-1}-1\) is the symbol of a backward
finite difference, so the null metric is a discrete scalar Hessian

\[
q_{\mu\nu}\sim \nabla^-_\mu\nabla^-_\nu\phi.
\]

The annihilation by \(C\) is therefore a finite exact
"second difference / Cartan-response" compatibility, not an orbit census.

## 3. The FUGU detune residual is transport, not a new response row

The FUGU forward scout held a metric-null vector fixed while changing one
character \(z_j\). That produces a generally nonzero raw derivative

\[
w_j=(D_j C)q,\qquad D_j=z_j\partial_{z_j}.
\]

Visibility of this fixed vector is not invariant under a change of carrier,
because the kernel line itself moves with \(z\).

Differentiate the exact identity \(C(z)q_{\rm null}(z)=0\). For every
character direction,

\[
\boxed{
(D_j C)q_{\rm null}
=
-C(D_j q_{\rm null}).
}
\]

Hence

\[
\boxed{w_j\in\operatorname{im}C}
\]

identically. The exact certificate reproduces the nine owned L=4 singular
orbit representatives and verifies all \(9\times4=36\) raw FUGU detune
vectors this way.

This supersedes the fixed-vector A/B interpretation of the FUGU v2-v4
scouts. In particular the apparent all-B orbit \((1,1,3,3)\) is not a
first-order D0-only response anomaly: its raw detune is canceled by the
metric transport \(q_1=-D_jq_{\rm null}\) before any connection correction is
needed.

The earlier tests \(w\in\operatorname{im}A\) remain legitimate linear-algebra
measurements of a frozen vector, but they are not the joint/carrier-covariant
obstruction. A character move must transport the owner of the metric-null
line.

## 4. Relation to the affine/coframe result #264

The flat forward-coframe metric shadow uses the forward character difference

\[
a_r(z):=z_r-1.
\]

For a coframe Fourier amplitude \(y\), its symmetric metric shadow is

\[
q_{\rm aff}(a,y)=a y^T+y a^T.
\]

The metric-null line uses the backward difference. With

\[
Z=\operatorname{diag}(z_0^{-1},\ldots,z_3^{-1}),
\]

there is an exact identity

\[
d=-Za,
\qquad
q_{\rm null}=d d^T
=
Z(aa^T)Z.
\]

Therefore finite forward-coframe and backward-response carriers need not
coincide even though they have the same continuum tangent.

For nonzero \(a,d\), the rank-one tensor \(dd^T\) belongs to the
forward-coframe metric image
\(\{ay^T+ya^T:y\in\mathbb C^4\}\) iff \(d\) is collinear with \(a\).
Since \(d_r=-a_r/z_r\), this occurs precisely when all nontrivial character
components \(z_r\neq1\) have the same phase.

On the nine owned L=4 singular orbit types this selects exactly

\[
(0,0,1,1),\qquad(1,1,1,1),
\]

i.e. orbits 0 and 4. That is exactly the pair on which #264 independently
found that the forward-coframe/joint-kernel intersection equals the complete
two-real-dimensional metric-only plane. Orbit 5 \((1,1,3,3)\) lies in the
same coarse square-map fibre as orbit 4 but has split \(+i/-i\) phases, so
\(d\not\parallel a\) and the affine intersection vanishes.

Thus the #264 orbit split is explained by the **forward/backward character
duality**, not by capacity, nullity, or a new even selector.

This does not promote the forward-coframe image to gauge: #264 already
forbids that inference for the selected finite star action.

## 5. Smooth-character limit

Let

\[
z_r=e^{ihk_r}.
\]

Then

\[
a_r=ihk_r-\frac12h^2k_r^2+O(h^3),
\qquad
d_r=-ihk_r-\frac12h^2k_r^2+O(h^3).
\]

Therefore

\[
aa^T=-h^2kk^T+O(h^3),
\qquad
dd^T=-h^2kk^T+O(h^3),
\]

and

\[
\boxed{
dd^T-aa^T=O(h^3).
}
\]

Equivalently, the exact identity \(dd^T=Z(aa^T)Z\) gives

\[
dd^T-aa^T
=
(Z-I)aa^T
+
aa^T(Z-I)
+
(Z-I)aa^T(Z-I).
\]

Since \(Z-I=O(h)\) and \(aa^T=O(h^2)\), the mismatch is \(O(h^3)\).
After the gravitational \(h^{-2}\) normalization,

\[
\boxed{
h^{-2}(dd^T-aa^T)=O(h)\to0.
}
\]

This gives a concrete finite-to-smooth mechanism:

> a finite-UV metric-null mode need not be an exact affine/coframe direction,
> while its normalized IR shadow becomes affine-shaped to first continuum
> order.

At leading order the null metric is the scalar-longitudinal tensor
\(-h^2 k_\mu k_\nu\). This is gauge-shaped in the continuum sense (it is the
Fourier Hessian of a scalar), but the present result proves only this scalar
subcomplex. It does not construct the full four-parameter vector
diffeomorphism image.

## 6. Operational reading

The correct lesson of the FUGU detune is the registered-carrier rule.

A metric-null vector at one character and a metric-null vector at a nearby
character are not the same primitive merely because both live in a
ten-coordinate array. The exact transport is \(q_{\rm null}(z)=dd^T\).

Holding the old \(q\) fixed while changing \(z\) changes the carrier but
refuses to move the owner. The resulting \(w=(D C)q\neq0\) is therefore a
transport defect, not by itself a physical response defect.

In the operational "cat and box" language: the character move changes the
box. The exact Hessian section tells how the box moves with the state. If the
box is transported, this particular metric germ remains null exactly.

## 7. Consequences for the active gravity front

### 7.1 #232 remains a different object

The #232 family is a **connection** microstructure with nonzero curvature and
exact flat-metric response-nullity. The Hessian line here is a **metric**
amplitude. They are not identified.

This result therefore does not solve or kill #232. It removes a false
metric-germ counterexample that could otherwise contaminate the response
decoupling question.

### 7.2 #240 becomes sharper

The live #240 question remains

\[
h^{-2}
\left[
E_Q(Q_h,K_h)-E_Q(Q_h,K_h^{\rm sm})
\right]\to0
\]

for genuinely joint-critical connection microstructure on a slowly varying
smooth background.

But character-dependent metric-null amplitudes must now be transported by
the exact Hessian complex before declaring a normalized response gap.
A fixed-\(q\) detune of the metric-only line is not a valid counterexample.

The first meaningful obstruction is therefore a response component **after**
the exact metric-null transport has been removed, together with the full
joint equations. For #232-type \(Y\), that remains a separate calculation.

### 7.3 #237 / compactness

A metric-null complex exists at every nontrivial character. Therefore a
uniform compactness or inf-sup argument on the unquotiented metric carrier
cannot treat the two-real-dimensional L4 metric-only block as a finite
accident.

Any refinement-uniform theorem must either:
- quotient/control this exact Hessian complex, or
- prove how it is fixed by the nonlinear joint equations / boundary data.

This reduces one part of the growing-kernel problem from a census to an
explicit algebraic subcomplex.

### 7.4 #265 / #267

The metric-only plane no longer needs \`E_eta/E_sp\` to define it. Its exact
owner is \(dd^T\).

#267 remains necessary for the independent executable \`E_sp\` owner.
#265 remains meaningful only as a same-carrier comparison between the
now-owned Hessian metric-null line and the realified E-LIN operator symbols.
It must not use \`E_sp\` to define the metric-only sector.

The earlier proposed four-dimensional
\(\ker C\oplus\operatorname{span}\{E_\eta,E_{sp}\}\) "even sector" should
therefore not be promoted merely from dimension and direct-sum data.

## 8. What this means for Einstein

The result does not derive Einstein's equation by itself. It supplies a
missing structural reason why finite extra metric directions need not survive
as extra continuum observables.

At finite lattice character the response-null line and the forward-coframe
image can disagree. In the smooth-character limit their scalar-longitudinal
shadows agree through the \(h^2\) order relevant to the normalized metric
response, with only an \(O(h)\) normalized mismatch.

This is the first exact mechanism in this lane of the form

\[
\text{finite non-gauge-shaped UV distinction}
\quad\longrightarrow\quad
\text{gauge-shaped IR null direction},
\]

without declaring the UV object itself gauge and without adding a selector
to the action.

The remaining Einstein problem is no longer local uniqueness. It is whether
the genuinely curved connection microstructure left after this exact metric
complex is removed is also invisible in the normalized response. That is
precisely the non-tautological content of #240.

## 9. Next primitive

The next calculation should not be another L4 census.

1. Use this exact Hessian transport as a mandatory quotient/transport in any
   slow-character response calculation.
2. For a #232-type connection microstructure on \(Q_h=g(hx)\), compute the
   first response component that survives both:
   - the connection range correction, and
   - the metric-null Hessian transport.
3. If that projected component vanishes at the first possible order, promote
   the decoupling mechanism toward #240.
4. If it does not, its exact nonzero coefficient is the correct D0-only
   response anomaly candidate.

A second, independent extension is to test whether the remaining
three vector-symmetrized coframe directions acquire their own compensated
connection lift in the smooth limit. That would be the route from the scalar
Hessian subcomplex toward a full linearized diffeomorphism complex; it is not
owned here.

## 10. Reproduction and firewall

Certificate:

\`02_REGISTRY/research/certificates/a4d_metric_null_hessian_complex_check.py\`

The certificate rebuilds the star metric-response symbol from the accepted
finite conventions and uses exact SymPy algebra. Numerical FUGU SVD data are
hostile controls only, not theorem evidence.

**Not claimed:**
- full diffeomorphism gauge;
- nonlinear gauge symmetry;
- \`metric-only = span{E_eta,E_sp}\`;
- an \`E_sp\` owner;
- #232 decoupling;
- a continuum Einstein theorem;
- BOOK or claim promotion.
