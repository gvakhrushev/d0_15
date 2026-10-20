# Recorded state to observer form: a concrete component and its full heat derivative

Parent: existing #310, `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`.
Input SOURCE: `80462afde4668fc822a01a70c2e571ce36ecd64e`.
Date: 11 October 2026. **Finite preparation component; native T0 remains open.**

The existing recording gate supplies a nonempty faithful reduced-state sector.
In an explicitly specified density-to-Role readout, that state determines the
argument of the existing positive observer form. Its variation is computed
from a normalized input curve of the same gate. This removes a freely supplied
observer *inside this mathematical component*. It does not derive physical
admission of the readout, choose this pairing as native heat, or complete the
joint preparation on `(q,D,b,m)`.

The full heat-price check is essential. Substituting this form into the
already studied positive Hodge binding produces a strictly nonzero thermal
derivative on a precise finite high-temperature range. A state-dependent
formula alone therefore does not solve stationarity. No compensator,
temperature, action, or source is selected to make it vanish.

## 1. The full retained state and the exact faithful domain

Use the literal `GoldenCoherentMemory.fullStep`, with `a>0`, `a²=p`,
`p+p²=1`, `p>0`. Its actual `blank_record_evolution` is

\[
 U(a,p)(u,0,v,0)^T=(au-pv,0,0,pu+av)^T.                 \tag{1}
\]

For any real full output `psi=(alpha,beta,gamma,delta)`, define the amplitude
matrix `Psi=[[alpha,beta],[gamma,delta]]`. The declared readout is the genuine
system-factor partial trace `rho=Psi Psi^T`; all four full-state coordinates
remain in the domain. In the explicit order **A,B,C,D**, set

\[
 j=(\rho_{00}+\rho_{11},\;2\rho_{01},\;0,\;
       \rho_{00}-\rho_{11}),\qquad \eta=\mathrm{diag}(1,-1,-1,-1).
\]

This is a specified Pauli coordinate map, not the enumeration order of `Role`:
the actual owner has A=(0,0), B=(1,1), C=(0,1), D=(1,0). For a general Hermitian
matrix `[[x,z+iw],[z-iw,y]]`, the same convention gives `(x+y,2z,-2w,x-y)`.
The exact determinant identity is

\[
 k:=j^T\eta j=4\det\rho
   =4(\alpha\delta-\beta\gamma)^2.                    \tag{2}
\]

On precisely the real sector `det Psi != 0`, put `n=j/sqrt(k)`. Then
`n^T eta n=1`, and `n_A>0`. The existing owner yields

\[
 h(j)=-\eta+\frac{2}{k}(\eta j)(\eta j)^T
     =\operatorname{observerMetric}(n)>0.             \tag{3}
\]

Its existing exterior Gram positivity applies in every degree. The supplied
unit-observer premise is now proved from this full state and readout, rather
than assumed independently. The companion Lean capsule proves the generic
determinant identity, unit normalization, equality with the actual owner and
positive definiteness. The extension of the coordinate identity to complex
densities does not assert native admission of complex gate inputs.

For the blank input of (1), the prior modular-preparation packet already
established `rho=diag(p,p²)`. Here its previously uncomputed observer output is

\[
 j=(1,0,0,p^3),\quad k=4p^3,\quad
 h_\varphi=\begin{pmatrix}
 p+\tfrac12&0&0&-\tfrac12\\
 0&1&0&0\\0&0&1&0\\-\tfrac12&0&0&p+\tfrac12
 \end{pmatrix}.                                      \tag{4}
\]

Its eigenvalues are `(1/p,1,1,p)` and determinant one. These follow from the
actual state; no spectrum is fitted. This is a positive pairing, not a newly
proved physical Lorentz metric or causal clock.

## 2. An actual full-state curve and its differentiated pairing

Keep the same gate and use the exact normalized input curve

\[
 u(t)=\frac{1-t^2}{1+t^2},\quad v(t)=\frac{2t}{1+t^2},\quad
 A(t)=au(t)-pv(t),\quad B(t)=pu(t)+av(t).              \tag{5}
\]

The output is `(A(t),0,0,B(t))`, its squared norm is one, and its reduced
density is `diag(A(t)²,B(t)²)`. This is a variation of the declared apparatus
interface, not a proof of M1 physical preparation of every input. It is
nonempty and faithful on the explicit interval `|t|<=1/10`: the exact bounds
`3/5<p<5/8`, `3/4<a<4/5` give `A>=247/404>0`, `B>=217/505>0`.
Here `u>=99/101` and `|v|<=20/101`. With `ell=217/505`, the whole interval
satisfies `ell² I <= h(t) <= ell^{-2} I`: its two nontrivial eigenvalues
are `A(t)²/B(t)²` and the reciprocal, and `ell<=A,B<=1`.
Thus local positivity is quantitative, without a boundary regularization.

At zero, `A'=-2p`, `B'=2a`, `rho'=diag(-4ap,4ap)` and `j'=(0,0,0,-8ap)`.
For any variation `v=delta j`, differentiation of (3) gives

\[
 \delta h=\frac2k[(\eta v)(\eta j)^T+(\eta j)(\eta v)^T]
    -\frac{4j^T\eta v}{k^2}(\eta j)(\eta j)^T.        \tag{6}
\]

The denominator derivative is compulsory. On (5) the only nonzero entries at
zero are

\[
 h'_{AA}=h'_{DD}=d'=-\frac{2a}{p^2},\qquad
 h'_{AD}=h'_{DA}=c'=\frac{2a(1+p^2)}{p^3}.            \tag{7}
\]

The whole curve has `det h=1`; in particular `Tr(h^{-1}h')=0`, while `h'!=0`.
This is a nonzero shape variation of the pairing, **not** ten metric-source
components and not a proof that the observer direction is physical.
The capsule proves genuine `HasDerivAt` statements for (5), its retained
contrast, the rational diagonal/mixed coefficients and their actual composition
with the gate curve. The complete matrix
substitution and (6)--(7) are checked by exact symbolic algebra.

## 3. The retained heat price, not just a varying matrix

The previously proved positive Hodge binding on the full periodic carrier has
`delta_W=W^{-1}d^*W`, `D_W=d+delta_W`. For a constant positive pairing metric
Q, its full Fourier symbol is

\[
 \Delta_Q(k)=z(k)^*Q^{-1}z(k)I_{16},\qquad
 z_r(k)=L(e^{2\pi i k_r/L}-1).                         \tag{8}
\]

All sites, conjugate modes, zero modes and all sixteen exterior grades remain.
In this *explicit binding test*, substitute `Q(t)^{-1}=h(t)` from (3)--(5).
It is an instance of the already stated compound law; it is not declared the
native heat owner. At a fixed coframe this is a matter/readout variation of
the positive pairing. It is not silently substituted for a physical q probe.

With the original ordinary finite trace and fixed beta>0,

\[
 H(t)=\beta^{-1}\log\left(16\sum_k e^{-\beta\lambda_k(t)}\right),
 \quad \lambda_k(t)=z(k)^*h(t)z(k),\qquad
 H'(0)=-\frac{\sum_k\lambda'_k(0)e^{-\beta\lambda_k(0)}}
                    {\sum_k e^{-\beta\lambda_k(0)}}. \tag{9}
\]

The factor sixteen cancels from the derivative, not from the price. Formula
(9) differentiates the entire coupled pairing, including (6). It follows
from the previously checked finite thermal derivative and the actual full
symbol (8). This packet's spectral argument is analytic, not a new compiled
heat theorem.

There is an explicit nonzero range, for every finite `L>=2` (hence for `L in
4N`). Uniform averaging over the whole Fourier grid gives
`mean |z_r|²=2L²` and `mean Re(conj(z_r)z_s)=L²` for r!=s. Consequently (7)
gives

\[
 \operatorname{mean}_k\lambda'_k(0)
   =L^2(4d'+2c')=4apL^2>0.                           \tag{10}
\]

At (4), `0<=lambda_k<=16L²/p`. The norm of (7) is `4a/p³`, so
`|lambda'_k|<=64aL²/p³`. Using `|exp(-beta lambda)-1|<=beta lambda` yields

\[
 N_\beta:=\operatorname{mean}(\lambda'_k e^{-\beta\lambda_k})
 \ge4apL^2-\frac{1024aL^4}{p^4}\beta.
\]

For the nonempty interval `0<beta<=p^5/(512L²)` this is at least `2apL²`.
The mean Boltzmann denominator is positive and at most one, hence

\[
                         H'(0)\le-2apL^2<0.          \tag{11}
\]

This is a finite binding test. The beta interval shrinks with L; (11) is not
a fixed-beta refinement theorem or a general prohibition of this pairing.
If a complete native preparation admits the same joint path and the complete
remaining price R has `R'(0)=0`, (11) excludes stationarity there. Generally
stationarity requires `R'(0)=-H'(0)`; that equality must follow from actual
equations, not be used to define R. In particular the known golden feedback
zero cannot be extended to every simultaneous matter/readout variation.

## 4. Controls and the remaining single preparation obligation

* The same gate maps the normalized input `(a,0,-p,0)` to `(1,0,0,0)`.
  Its density is rank one and k=0. Formula (3) has no normalized timelike
  observer there. The full gate interface is not globally faithful.
* Right orthogonal changes of the record coordinates preserve `Psi Psi^T`
  while changing the full state. Such readout-null directions are retained;
  this packet does not declare them gauge or discard their equations.
* There is no uniform bound on the entire faithful sector. Outputs
  `(sqrt(1-epsilon²),0,0,epsilon)` arise from normalized inverse inputs of
  the same gate. The extreme h eigenvalues are `(1-epsilon²)/epsilon²`
  and its reciprocal; they diverge/vanish near the rank-one boundary.
* The C coordinate vanishes for these real densities. This component does
  not supply arbitrary observer directions or all ten physical metric probes.
* A global pure state is distinct from its mixed tensor marginal; no archive
  direction or full-price contribution is eliminated by taking that readout.

The remaining task is still one own joint preparation, possibly relational,
on `(q,D,b,m)`, including actual admission of its state/readout and complete
allowed changes. A positive result on an independently admitted nonempty
sector need not wait for whole-core classification. If this component is
used, that preparation must supply the rest of the coupling and test all
equations; the nonzero derivative (11) cannot be omitted. Passive covariance
does not grant physical operation permission.

For the metric/link variables, the tangent remains
`D delta q_t D^T + delta D q_t D^T + D q_t delta D^T = delta q_s`.
The full-price derivative must be pulled back along the actual complete
preparation before comparison with rho0. No Einstein/pure-trace dichotomy
has been proved. T0--T3, all 44 dependency nodes, own source/Ward, curved joint
roots, soundness/recovery and the original #310/#202/#317 terminals remain open.

## 5. Replay and formal scope

Run `python 02_REGISTRY/research/certificates/a4d_native_recorded_observer_preparation_check.py`
with the repository's SymPy dependency. The checked capsule is outside the
supported D0 tree; `--compile` replays it with the pinned Lean toolchain and
available built imports. Its 22 propositions and three consumed declarations
have only `propext`, `Classical.choice`, and `Quot.sound` in their transitive
axiom reports. The output prints their actual propositions, not just names.

The exact certificate verifies the full real density identity, the literal
gate and actual curve, all sixteen pairing derivative entries, every exterior
blade principal minor at the golden state, all 256 L=4 Fourier modes and the
sixteenfold full multiplicity. Executed mutations test tensor mixing, observer
normalization, its missing derivative, off-diagonal weights, replacement by a
pure density and an incorrect input curve. Altered scope/input ledgers are
rejected before mathematical replay. Physical admission, the all-L heat bound,
and a full native source are not reported as new Lean theorems.
