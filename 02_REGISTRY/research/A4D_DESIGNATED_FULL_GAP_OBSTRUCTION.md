# Designated smooth sheet: the full uniform inverse premise is false

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #310.
Calculated response input: `c724c48e25564d7aab4e39ba3976546db9c9a86a`.
Integration base refreshed to `b0ee482ace5ad829c2b91a6b1a5ab1a747af8449`.
Smooth-owner input: merged #216, `5523d8f679c1ea02f9b73d757c81649740010d0a`.
Independent sparse-symbol cross-check: #317, `3e5b5a873002a7dc52565b2bad343f5591384088`.

Status: exact flat principal-symbol certificate and an analytic localized
obstruction to a full refinement-uniform inverse about a smooth connection.
The curved calculation below is numerical. Neither task-level physical
terminal is reached. The IR theorem of #216 is preserved.

## 1. Correct recentering and the incorrect operator replacement

For a designated branch it is appropriate to write

\[
K=K_h^{\rm sm}(g)\exp\delta.
\]

This removes the inappropriate global `||g-eta||` forcing from a rescue
equation about a flat Y vacuum. It does not eliminate the high-frequency
variables in the actual finite connection Euler equation.

The symbol `A(1)` is the zero-phase value of the flat 24-by-24 polarized
connection block. #216 proves its determinant is 256 and proves an IR gap.
The full flat Euler operator is a finite convolution `H_eta(T)` with
symbol `A(lambda)^T` in the owner's placement, not multiplication by `A(1)`.
Freezing the link/solder coefficients does not freeze the input frequency.
Consequently

\[
D E_K|_{K_h^{\rm sm}}=A(1)+O(h)
\]

is not an operator-norm statement on unrestricted physical link fields.
On macroscopic bounded frequencies the IR expansion is valid. #216,
Sections 4.1--4.2, already distinguishes that expansion from a full solve.

## 2. Exact physical witness at the identity sheet

The [stdlib exact checker](certificates/a4d_designated_full_gap_check.py)
reconstructs the literal BCH face Hessian and metric readout over Q(i).
It does not import a rank table. Its
[ledger](certificates/a4d_designated_full_gap_results.json) gives

\[
\operatorname{rank}A(1)=24,\quad \det A(1)=256,
\qquad \operatorname{rank}A(i,i,i,i)=16.
\]

The full 34-by-24 stack `(A;C)` has exact rank 20 there: four physical
linear directions survive the joint derivative.

In role-major `(K1,K2,K3,J12,J13,J23)` coordinates let v have only
role-zero rotation entries `(1,-1,1)`. Exactly,

\[
A(i,i,i,i)v=0,\qquad C(i,i,i,i)v=0,
\qquad \|v\|_2^2=3,\quad\|A(1)v\|_2^2=6.
\]

Here C is the connection-to-metric readout with the actual opposite mixed
phase placement. A is Hermitian at the quarter character, and v is real;
hence `A(i)^T v=0` as well. The four-quarter character is present at every
period divisible by four, including 8 and 12. Its real/conjugate pair is an
actual real physical field, not an off-unit analytic probe.

These 24 coordinates are the fixed nondegenerate Gram-section/dressed-link
coordinates of #216. The site Lorentz verticals have already been removed.
The witness is not a remaining gauge zero. The exact small-amplitude Y
family through the identity also prevents treating all Y fields as a remote
sheet near only the finite-amplitude `K_Y(1)` vacuum.

In particular, even at constant eta the proposed full replacement by A(1)
has an order-one error on this mode. Removing the finite-amplitude Y seed
from a numerical search does not remove this physical principal kernel.

## 3. Fixed curved background: a localized obstruction in every l^p norm

The flat control is not the sole argument. Fix a smooth nondegenerate
metric realization with a normal coordinate/Gram section at a point y=0:

\[
S(y)=I+O(|y|^2).
\]

Let the smooth approximate comparison connection satisfy the owned bound
`||log K_h^sm||_infinity <= C h`. It need not be exactly stationary for this
argument. Let H_h be its literal connection Hessian in the exponential
increment chart. On sites within distance ell of the normal center,
finite-stencil analyticity and the fixed finite set of shifts imply that
each coefficient differs from the flat coefficient by at most

\[
C\bigl((h\ell)^2+h\bigr).
\]

Take a nonzero smooth compactly supported cutoff chi and the physical
quarter packet

\[
u_h(x)=\chi(x/\ell)\,i^{x_0+x_1+x_2+x_3}\,v,
\]

periodized on the carrier, with support inside the normal chart. On the
uncut plane wave H_eta(T) vanishes by Section 2. The commutator with the
cutoff contains finitely many differences `chi((x+r)/ell)-chi(x/ell)`.
For each fixed shift r and every `1<=p<=infinity`, scaling the cutoff gives

\[
\|\chi((\cdot+r)/\ell)-\chi(\cdot/\ell)\|_p
\le C\ell^{-1}\|\chi(\cdot/\ell)\|_p.
\]

The lower bound on the cutoff norm follows from a smaller region where
chi is bounded away from zero. For finite p both sides carry the same
factor `ell^(4/p)`; at p=1 this is the actual unweighted component sum.
Translations and the finite fibre conversions introduce no L-dependent
factor. Combining the coefficient perturbation and commutator bounds,

\[
\boxed{\frac{\|H_hu_h\|_p}{\|u_h\|_p}
\le C\bigl(\ell^{-1}+(h\ell)^2+h\bigr).}
\]

Choose `ell=floor(h^(-2/3))` on `L in 4N`, for sufficiently small h. Then
`ell -> infinity`, `h ell -> 0`, and the support fits the fixed normal
chart. Therefore

\[
\boxed{\inf_{u\ne0}\frac{\|H_hu\|_p}{\|u\|_p}
\le C h^{2/3}.}
\]

At p=2 this is `sigma_min(H_h) <= C h^(2/3)`. At p=1 it directly excludes
the proposed refinement-uniform owner-sum inverse. If H_h is invertible,
its inverse norm is at least `c h^(-2/3)`; otherwise there is no full
inverse. This is an upper bound on the gap, not a sharp asymptotic rate.

The same argument applies to the full joint derivative `(H_h,C_h)`:
the packet's constant principal metric output also vanishes. An independently
prescribed metric source has no derivative with respect to these increments.
The argument excludes a full linear lower bound, not a reduced nonlinear
estimate on a correctly proved stationary center/normal correspondence.

Complexification loses no conclusion: the real coefficient operator acts
on the real and imaginary parts, and their norms have fixed comparison
constants. The packet does not assert a nonlinear stationary branch.

## 4. Actual curved numerical probe at L=8,12

The [probe](experiments/a4d_designated_curved_hessian_probe.py) uses the fixed
C-infinity periodic metric

\[
g=\operatorname{diag}(1,-1,-f(x_1)^2,-f(x_1)^2),\qquad
f=1+0.02(1-\cos(2\pi x_1)).
\]

The metric is independent of h. At x1=0 its value is eta, its first
derivatives vanish, and `f''(0)=0.08*pi^2 != 0`, so its warped spatial
curvature is nonzero. This is a metric-normal center, not a varying frame
for a flat metric.

Translation symmetry in x0,x2,x3 reduces the smooth background solve to
24L unrestricted link coordinates. Numerical continuation starts at the
identity at zero metric amplitude and increases that amplitude to 0.02.
The action is the literal plaquette product with inverse links and actual
star/solder pairing. The Hessian contains all first, same-factor second,
and distinct-factor second derivatives. The transverse quarter Bloch fibre
keeps phase i in x0,x2,x3 and all L x1 variables; it is not an IR projection.

The [numerical ledger](experiments/a4d_designated_curved_hessian_results.json)
records:

| L | connection residual infinity | smooth translation fibre sigma_min | quarter fibre sigma_min | quarter inverse l1 norm |
|---:|---:|---:|---:|---:|
| 8 | 8.69e-16 | 0.284547 | 7.840802e-6 | 192550.3 |
| 12 | 6.66e-16 | 0.284385 | 7.158566e-7 | 2152216.4 |

The link-log bounds divided by h are respectively 0.11394 and 0.12060.
The background translation fibre remains well conditioned in this probe;
the unrestricted quarter fibre is a different block. Two grids do not
prove an asymptotic rate or the minimum over every transverse character.
The analytic result in Section 3 supplies the refinement obstruction.

Flat Hessian comparison with the independently reconstructed mixed symbol
has maximum error 2.23e-16. Curved directional gradient and Hessian finite
differences have errors below 2.70e-11 and 1.01e-10.

These are floating-point connection-stationary continuations, not validated
exact roots. No independent metric source is imposed. The probe does not
identify its finite-L branch with #216's specific cutoff parametrix, prove
the joint equations, or construct a normalized response counterexample.

## 5. Why neither a tail nor a gap collapse closes the physical theorem

Smoothness bounds the prescribed metric/comparator forcing; it does not
bound arbitrary stationary connection amplitudes in a resonant kernel.
A small Fourier tail cannot be multiplied by an inverse at an exact zero.
It also does not establish solvability of the resulting cokernel equation.

#216 actually proves a super-algebraic residual for its fixed C-infinity
realization, with its stated Wiener assumptions. Replacing those hypotheses
by C4 does not preserve that conclusion. In four dimensions the elementary
H4/Cauchy--Schwarz bound is

\[
\sum_{|n|>M}|\widehat q(n)|
\le\Big(\sum_{|n|>M}|n|^{-8}\Big)^{1/2}\|q\|_{H^4}
\le C M^{-2}\|q\|_{H^4}.
\]

An individual coefficient bound is not a bound of the whole tail in the
task norm. Even an invertible operator with a uniform l2 spectral gap need
not have a refinement-uniform l1 inverse; the requested norm has to be
proved directly.

There is a separate rate issue. A sitewise O(h2) residual summed over L4
sites is O(h^-2), not O(h2). Even a true sum-norm correction `delta=O(h2)`
and a raw Lipschitz readout give only an O(1) normalized difference. A
little-o conclusion needs `delta=o(h2)` in that norm or a stronger proved
response cancellation. The super-algebraic #216 residual would be enough
under an appropriate polynomial normal-rescue bound; the full uniform
linear gap proposed here is stronger than necessary and is false.

Conversely, a falling spectral gap is not a nonlinear Einstein counterexample.
The metric equations may obstruct a mode or its allowed stationary response
may agree with the comparator. #227 does not supply the required exact
joint-critical/source-compatible sequence on this curved metric.

## 6. Current proof obligation and replay

The first missing designated object is the full nonlinear range-reduced
stationary correspondence after actual IR elimination, retaining the
physical resonant center equations and a metric-response estimate uniform
in refinement. A polynomial inverse loss on a genuine normal quotient,
together with controlled center response and #216's super-algebraic residual,
can suffice. The full spectral inverse excluding only gauge cannot supply
that quotient because the physical principal kernel survives.

For the broader #310 terminal the declared class must also cover the owned
Y microstructure; merely choosing a smooth connection neighborhood cannot
prove response universality over the other admissible stationary sheets.

```bash
python 02_REGISTRY/research/certificates/a4d_designated_full_gap_check.py \
  --expect 02_REGISTRY/research/certificates/a4d_designated_full_gap_results.json
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python \
  02_REGISTRY/research/experiments/a4d_designated_curved_hessian_probe.py \
  --periods 8 12 --output /tmp/a4d_designated_probe.json
```

No action, selector, source contract, or physical terminal is changed.
The failed full-gap route is now decided; the Einstein/response bridge
remains open at the retained nonlinear stationary correspondence.
