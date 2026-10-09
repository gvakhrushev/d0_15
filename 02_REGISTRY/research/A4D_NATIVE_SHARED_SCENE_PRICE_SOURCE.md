# Native price: the shared scene first jet and the least-price test

Research continuation of #310, input SOURCE
`b236ad0f4c0ff2efd6d5d446c4a03ca091b33ee4`; main
`fa2b04b9c8aae5a0b8470322d6091712ce56567a`. This is a companion to
[the intrinsic constrained-source calculation](A4D_NATIVE_CONSTRAINED_PRICE_SOURCE.md),
within the same execution. No parent terminal or public claim changes.

## 1. Result and exact scope

At the existing unweighted `K(9,11,13)` scene, the first derivative of the
normalized scene heat price **plus the full-history return price** factors
through one explicit covector on **all 359 independent edge variations**.
The degree normalization and archive pairing vary together. This removes
independent heat/return jets from this declared interface.

For each fixed inverse temperature `beta > 0`, exactly two fugacities
`0 < z < 1` make the canonical scene stationary with respect to these weights.
The upper branch has a negative definite second variation on a 296-dimensional
space and therefore cannot be a local minimum in this class. Neither branch
is asserted to solve equations for variations of beta or z themselves.
The lower branch has not been proved to minimize the price.

**Admission boundary.** The class below is a completely specified mathematical
positive-conductance extension of the existing scene. The frozen scene and
its normalized operator have primary owners; the assertion that every such
weight variation is a physical native variation is NOT supplied by them.
`ArchiveWeightedGraph` permits weighted graphs but does not establish that
physical admission. In particular, this result does not choose weights as
functions of `(q,D,b,m)`, nor a temperature/fugacity law. It does not derive
a matter action, Ward identity, metric source, rho0, curved roots or GR.

## 2. Common carrier, including the archive pairing

Let the fixed 33 vertices have zones of sizes 9, 11 and 13. Give every
cross-zone unordered edge a positive conductance `w_ij = w_ji`; all other
entries, including diagonal entries, remain zero. Write

\[
A=A(w),\quad d_i=\sum_j A_{ij},\quad D_d=\operatorname{diag}(d_i),
\quad T=D_d^{-1}A,\quad\Delta=I-T.
\]

`D_d` is the scene degree, not the dressed physical link `D_e`.
At `w=1`, the degrees are 24, 22 and 20 and their sum is 718.
The combinatorial heat polynomial in `SceneHeatKernel.lean` belongs to
`D_d-A`; it is not substituted for the normalized heat operator here.
The [existing composed-price report](A4D_NATIVE_COMPOSED_FEEDBACK_DYNAMICS.md)
already distinguishes those routes and leaves a heat law on all 718 histories
unselected. This result uses the stated 33-vertex normalized route.

On all 718 ordered histories let `J` copy a vertex value to histories with
that target, `W_H` be the diagonal matrix of history conductances and `R`
reverse each history. Set

\[
C=D_d^{-1}J^T W_H,\qquad P=JC.
\]

Then `J^T W_H J=D_d`, `CJ=I`, and `P` is the `W_H`-orthogonal projection.
Reversal preserves `W_H` and `R^2=I`. In particular `CRJ=T`. The full
feedback of **one application of R**, including every history row, satisfies

\[
F_H=PR(I-P)RP=J(I-T^2)C,\qquad
\det(I_{718}-zF_H)=\det(I_{33}-z(I-T^2)). \tag{1}
\]

The first identity is direct multiplication, using `CJ=I` and `R^2=I`.
The second is Sylvester's determinant identity. Both identities are
kernel-checked for arbitrary finite dimensions. The archive's complementary
identity block is retained; no reduced determinant or memory reset is used.
Equation (1) holds for every positive `w`, so differentiating it includes the
changes of degree, `C`, `P` and the history pairing. Reversal is not asserted
to be the complete physical tick. For two successive retained reversals
the actual operator is `R^2=I` and its feedback is zero. Equation (1) is
not that two-tick price, nor a replacement of `R^2` by the coarse `T^2`.
The preceding golden two-tick calculation remains a separate contribution
with its own word and admission hypotheses.

## 3. Full price and its common first derivative

For fixed `beta > 0` and `0 < z < 1`, use the existing price formula

\[
\mathcal B_{\beta,z}(w)=\beta^{-1}\log Z
 -\log\det Q,\quad
Z=\operatorname{Tr}e^{-\beta(I-T)},\quad
Q=I-z(I-T^2). \tag{2}
\]

`T` is similar to the real symmetric matrix `D_d^{-1/2} A D_d^{-1/2}`,
with spectrum in `[-1,1]`. Thus `Z>0` and all eigenvalues of `Q` are at
least `1-z>0`; the real log and inverse used here exist.
For a symmetric edge-supported adjacency jet `E`, set
`dot D_d=diag(E 1)`. Differentiating `D_d T=A` gives

\[
V=\dot T=D_d^{-1}(E-\dot D_d T),\quad V1=0. \tag{3}
\]

The derivative of a matrix exponential under the trace is valid without a
commuting jet: differentiate its power series and use cyclicity of trace.
Jacobi's determinant formula then gives

\[
\dot{\mathcal B}=\operatorname{Tr}(MV),\quad
M=\rho-2zTQ^{-1},\quad \rho=e^{-\beta(I-T)}/Z. \tag{4}
\]

This is an analytic finite-dimensional proof of the matrix derivative;
the capsule proves the trace identities, not a general matrix `HasFDerivAt`.
For a single unordered edge the coefficient in (4) is

\[
\omega_{ij}=M_{ji}/d_i+M_{ij}/d_j
 -(TM)_{ii}/d_i-(TM)_{jj}/d_j. \tag{5}
\]

Uniform rescaling of all conductances leaves `T` unchanged and gives
`sum w_ij omega_ij=0`. Freezing the degree would lose both (3) and this
check. Heat and feedback now have the same jet `V`.

## 4. Exact first-jet quotient on all 359 edges

At `w=1` the characteristic polynomial is

\[
\chi_T(t)=t^{30}(t-1)(t^2+t+\kappa_0),\qquad
\kappa_0=39/160,\quad r=\sqrt{10}/40.
\]

The two remaining eigenvalues are `r_+=-1/2+r` and `r_-=-1/2-r`.
Let `P_c(i,j)=d_j/718` project onto constants, and let `P_d` subtract
the mean within each zone. The latter has rank 30 and `T P_d=P_d T=0`.
For **every** edge-supported `E`, (3) satisfies

\[
\operatorname{Tr}V=\operatorname{Tr}(P_cV)
 =\operatorname{Tr}(P_dV)=0. \tag{6}
\]

Indeed the diagonal of `T(w)` is zero, `V1=0`, and `P_d D_d^{-1}E`
has zero trace because `E` has no within-zone entries; the degree term
has zero trace by cycling `T` next to `P_d`. The exact checker verifies
(6) on the full 359-element edge basis, as well as the native spectrum.

Define the scalar invariant `kappa(w)=1-Tr(T(w)^2)/2`, so
`kappa(1)=kappa_0` and `dot kappa=-Tr(TV)`. For any spectral function
`M=m(T)` with values `m_+`, `m_-` on the two remaining eigenspaces,
the spectral decomposition and (6) give

\[
\operatorname{Tr}(MV)=\frac{m_- -m_+}{2r}\,\dot\kappa. \tag{7}
\]

This is a first-jet statement at the canonical scene, not a claim that
the full price at arbitrary non-equitable weights depends only on kappa.
The polynomial equivalent uses
`Tr(T^2 V)=-Tr(TV)` and `Tr(T^3 V)=(1-kappa_0)Tr(TV)`;
these are checked on every edge and the generic contraction is compiled.

The three per-edge coefficients of `dot kappa` are:

| Zone pair | Edges | Coefficient on each edge |
| --- | ---: | ---: |
| 9--11 | 99 | `91/278784` |
| 9--13 | 117 | `1/57600` |
| 11--13 | 143 | `-93/387200` |

Their edge-weighted sum is zero and the covector is nonzero. As an
independent equitable-family check, with pair weights `x,y,u`,

\[
\kappa(x,y,u)=\frac{2574uxy}{(11u+9y)(13u+9x)(11x+13y)}.
\]

Its three derivatives at `(1,1,1)` are `91/2816`, `13/6400`, and
`-1209/35200`, precisely the sums in the table. This check does not replace
the full-edge calculation.

## 5. Scalar coefficients and the two stationary branches

For `k<1/4` let `s(k)=sqrt(1/4-k)` and

\[
Z_\beta(k)=1+30e^{-\beta}
 +e^{-\beta(3/2-s(k))}+e^{-\beta(3/2+s(k))},
\quad Q_z(k)=(1-z)(1-2kz)+k^2z^2.
\]

At `k=kappa_0`, (4)--(7) become

\[
\dot{\mathcal B}=(c_H+c_F)\dot\kappa,\quad
c_H=-\frac{e^{-\beta(3/2-r)}-e^{-\beta(3/2+r)}}{2rZ_\beta(\kappa_0)},
\quad c_F=\frac{2z[1-(1+\kappa_0)z]}{Q_z(\kappa_0)}. \tag{8}
\]

The capsule supplies actual scalar `HasDerivAt` proofs for the heat,
feedback and their sum, including the square-root domain. The constant
feedback term `-30 log(1-z)` is retained in that scalar price.

Write `h=-c_H`. For every `beta>0`, `0<h<5/7`: set
`a=3/2-r>7/5`, `b=3/2+r` and apply the mean-value theorem to
`exp(-beta x)` on `[a,b]`. For some `xi` in `(a,b)`,
`h=beta exp(-beta xi)/Z`; `exp(beta xi)>beta xi` and `Z>1`
give `h<1/xi<5/7`.

Since `dot kappa` is nonzero, full edge stationarity is equivalent to
`c_F=h`. With positive denominator this is the quadratic

\[
\left(\frac{199}{80}+\frac{14001}{25600}h\right)z^2
 -\left(2+\frac{119}{80}h\right)z+h=0. \tag{9}
\]

Its discriminant is `4(1-h)+h^2/40>0`. Its values at `0`, `1/2`,
and `160/199` are respectively

\[
h>0,\quad (40241h-38720)/102400<0,\quad 6240h/39601>0.
\]

Continuity and degree two prove exactly one root in `(0,1/2)` and
exactly one in `(1/2,160/199)`. This classifies stationary parameter
pairs; it does not select beta, either root, or a physical on-shell state.
At `z=160/199` only feedback is stationary: the heat derivative is still
nonzero. Dropping it gives the wrong stationarity equation.

## 6. A 296-dimensional second-variation obstruction

For each pair of zones choose zero-sum vectors `u`, `v`, supported in
the respective zones, and put `E=uv^T+vu^T`. Finite sums of these span
a space of dimension `8*10+8*12+10*12=296`. They preserve every degree.
Consequently the genuine positive-weight curve `A(t)=A(0)+tE` has

\[
T(t)=T_0+tV,\quad V=D_d^{-1}E,\quad
T_0V=VT_0=0,\quad \operatorname{Tr}V=0.
\]

The second variation of (2) along any of these curves is

\[
\mathcal B''(0)=
\left[\frac{\beta e^{-\beta}}{Z_\beta(\kappa_0)}
 -\frac{2z}{1-z}\right]\operatorname{Tr}(V^2). \tag{10}
\]

For the heat part the first derivative of `Z` is zero, while
`Z''(0)=beta^2 exp(-beta) Tr(V^2)`. In the balanced sector the feedback
pencil is `(1-z)I+zt^2V^2`, giving the other term. These calculations
hold for all sums of the basis directions, not just each basis separately.
Symmetric `E` gives
`Tr(V^2)=sum_ij E_ij^2/(d_i d_j)>0` for nonzero `E`.
For the basis `u=e_i-e_0`, `v=e_j-e_0`, this trace is respectively
`1/66`, `1/60`, or `1/55`. The checker certifies rank 296 over the rationals.

The heat factor is less than one, since `beta<exp(beta)` and `Z>1`.
On the upper branch `z>1/2`, the feedback factor is greater than two.
Thus (10) is negative definite on this whole 296-dimensional space;
the upper branch is not a local minimum in the admitted weight class.
The generic sign inequality is kernel-checked. The matrix Hessian formula
is analytic and independently checked on the exact rank-two curves.

These directions are invisible in (8) but are not similarity directions:
`Tr(T(t)^2)=Tr(T_0^2)+t^2 Tr(V^2)` changes. No physical gauge removal
follows from their vanishing first response. The 296-dimensional tangent
space, the 30-dimensional balanced state sector, and the existing
653-dimensional joint-history-readout kernel are different objects.

## 7. Consequence for the critical path

If an actually owned native map into this weighted scene class is derived
at the canonical scene, its price covector needs only the contraction

\[
\eta[V_s,V_t,W,\dot b,\dot m]
=(c_H+c_F)\sum_{e=1}^{359}\kappa_e\,
 Dw_e[V_s,V_t,W,\dot b,\dot m]. \tag{11}
\]

The `Dw_e` must come from the actual preparation and preserve the complete
joint tangent `D_e V_t D_e^T+W q_t D_e^T+D_e q_t W^T=V_s`.
They cannot be fitted to rho0. The preceding intrinsic-covector theorem
then handles conormal invariance, link equations and metric readout.
At a stationary pair (9) the derivative of this scene contribution
vanishes for every such pullback; this alone is neither the whole native
on-shell system nor an Einstein equation.

The next task is therefore a specific admission/pullback theorem for (11),
or a complete obstruction for the actual native interface. It is no longer
necessary to reconstruct independent operator jets merely to evaluate
this scalar contribution at this base. Completeness of native variations,
other action terms, refinement, physical metric readout, rho0 and all
G0--G4/parent #310/#202/#317 terminals remain open.

## 8. Reproduction and proof boundaries

The companion capsule and exact checker have common stem
`certificates/a4d_native_shared_scene_price_source`.
The receipt records 21 resolved Lean declarations, actual printed
propositions and transitive kernel axioms. It also pins the toolchain,
prior packets and relevant primary source files. The generic capsule
does not import a D0 owner as an unused appearance of specialization.

The exact checker reconstructs the canonical 33-vertex adjacency,
all 359 first jets, the 296-dimensional balanced space, scalar identities
and hostile controls. Primary owners and prior compiled scene/history
bindings are hash-pinned separately. Exact computations, analytic arguments,
and compiled propositions are distinguished above. The MVT/IVT existence
argument and all-size analytic matrix derivative/Hessian are not advertised
as newly compiled Lean theorems.

Run from the repository root:

```sh
python3 02_REGISTRY/research/certificates/a4d_native_shared_scene_price_source_check.py
```

Compile the capsule from `03_FORMALIZATION` using `lake env lean` and its
relative path. No public release tree, action, selector or physical postulate
is changed by this research packet.
