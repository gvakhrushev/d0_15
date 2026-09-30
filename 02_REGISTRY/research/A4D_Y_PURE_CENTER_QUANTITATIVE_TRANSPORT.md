# Pure Y center: exact nonlinear gradient control and a derivative remainder

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, PR #310.
Input tip: `f12527c2b463ef31edb8216e6cb791355ea7b245`.
Status: exact finite-stencil theorem and an analytic estimate with constants
independent of lattice cardinality. This is a flat-metric pure-Y theorem,
not the task-level curved-background response theorem. PR stays Draft /
`IN_PROGRESS`.

The earlier sign-free transport owner proves that a stationary pure-Y
amplitude is constant. The new result makes that rigidity quantitative and
identifies the nonlinear remainder in every one of the 136 joint Euler
components. The remainder contains an amplitude difference. Consequently
the generic estimate `O(||c||^2)` is unnecessarily large for the pure-Y
interaction of a slowly varying small center amplitude.

## 1. Actual finite fields and exact all-row reduction

Let `V_L=(Z/LZ)^4`, `L in 4N`, and `p(x)=sum_j x_j mod 4`. Let
`E_L={x:p(x) in {0,2}}` be the even-phase carrier. At the standard solder
put all spatial links equal to identity and define

\[
K_0(x)=\begin{cases}
 C_Y(a(x)),&p(x)=0,\\
 C_Y(a(x))^{-1},&p(x)=2,\\
 I,&p(x)=1,3,
\end{cases}\qquad a:E_L\longrightarrow\mathbb R.
\]

Here `Y=J12-J13+J23`, `Y^3=-3Y`, and

\[
C_Y(a)=I+u(a)Y+v(a)Y^2,\qquad
u(a)=\frac{4a}{4+3a^2},\quad v(a)=\frac{2a^2}{4+3a^2}.
\]

No stationarity or smoothness of a is assumed in the identities below.
`E_Y(a)` consists of the 96 right-trivialized connection coordinates and
the 40 phase-resolved Gram metric coordinates in the owned order
`(00,01,02,03,11,12,13,22,23,33)`.

There are fixed rational finite-shift operators such that, **exactly**,

\[
\boxed{E_Y(a)=T_u u(a)+T_v v(a),\qquad T_u1=T_v1=0.}
\]

Every temporal face has precisely one nonidentity even-phase temporal
factor. On Lorentz links the differentiated inverse is the Lorentz transpose
of the differentiated plaquette. Thus its Euler variation is linear in that
factor's u and v. Spatial faces contribute only a constant part, which
cancels in the edge variation. The actual incoming and outgoing placements
are retained; this is not a derivative of a period-restricted action.

The new certificate independently assembles all rows by literal face
variation. `T_u` has 84 nonzero coefficients with total absolute sum 42;
`T_v` has 108 with total absolute sum 72. Their full rational coefficient
ledgers are saved in the result JSON. The metric rows of `T_v` vanish and
the total absolute sum in the metric rows of `T_u` is 6.

Two independent controls check the placement and nonlinear identity:

- at a=1, `u'=4/49`, `v'=16/49`, and the derivative agrees coefficient by
  coefficient with the literal `136 x 96` Bloch stencil applied to the
  Cayley family tangent `(4/7)Y` on phase 0 and `-(4/7)Y` on phase 2;
- on a nonconstant rational amplitude field, all 136 components agree with
  the separate owner's inverse-plaquette derivative and its unrestricted
  16-coordinate solder variation, converted to the ten Gram coordinates.

## 2. A quantitative nonlinear transport inequality

Consider a spatial role s=1,2,3 at a physical edge base x. Two incident
even-site amplitudes, called a,b here, enter the owned primary and secondary
boost rows. With the ordering saved in the certificate, put
`du=u(a)-u(b)`, `dv=v(a)-v(b)`. Exactly,

\[
e_P=dv,\qquad e_S=\frac{\epsilon_p}{2}du-\frac12dv,
\qquad (\epsilon_0,\epsilon_1,\epsilon_2,\epsilon_3)=(-1,-1,1,1).
\]

The corresponding graph moves are

\[
\mathcal G=\{e_s-e_0,e_s+e_0:s=1,2,3\}.
\]

These two Euler rows control the entire real Cayley chord, including sign
changes and the turning point of either scalar function separately:

\[
du^2+3dv^2
=\frac{16(a-b)^2}{(4+3a^2)(4+3b^2)}
\le6(e_P^2+e_S^2).
\]

The last inequality follows from
`6(e_P^2+e_S^2)-[(2e_S+e_P)^2+3e_P^2]=2(e_P-e_S)^2`.
Therefore for `|a|,|b|<=M`,

\[
|a-b|\le\frac{\sqrt6}{4}(4+3M^2)\sqrt{e_P^2+e_S^2}.
\]

On the fixed compact interval `[-3/2,3/2]` this gives the convenient
rational bound

\[
\boxed{|a-b|\le7\sqrt{e_P^2+e_S^2}.}
\]

It holds edge by edge on every finite carrier, so it also holds in the
corresponding edge counting norms for every `1<=p<=infinity`, with no
lattice-size constant. The primary row alone fails at `a=1,b=-1`;
discarding the compact amplitude hypothesis also invalidates the constant 7.
Both are executed hostile controls. The earlier unrestricted real
stationary-rigidity theorem remains valid; this compactness condition is
needed for its quantitative constant, not its zero-residual conclusion.

The moves generate the complete even-sum lattice, as certified by the
existing transport owner. A direct path bound also gives a quantitative
periodic consequence. Represent the difference between two even sites by
integers `d_j in [-L/2,L/2]`, with even coordinate sum. Then

\[
d=\sum_{s=1}^3d_s(e_s-e_0)
  +\frac{d_0+d_1+d_2+d_3}{2}\,2e_0,
\quad 2e_0=(e_1+e_0)-(e_1-e_0).
\]

Its word length is at most
`sum_s |d_s|+|sum_j d_j| <= 7L/2 <=4L`. Hence

\[
\boxed{\operatorname{osc}a
 \le28L\max_{\text{selected boost pairs}}\sqrt{e_P^2+e_S^2}.}
\]

In particular, a pure-Y sequence in this chart with a sitewise connection
residual `O(h^2)`, `h=1/L`, has amplitude oscillation `O(h)`. This follows
from the literal nonlinear equations; no envelope smoothness is imposed.
At zero connection residual, a is constant and the full joint metric
response vanishes. Transverse corrections can cancel these rows and are
not excluded by this theorem.

## 3. Exact derivative factor in the nonlinear remainder

For a scalar field on `E_L` set

\[
\|D_{\mathcal G}c\|_p
 =\max_{m\in\mathcal G}\|c(\cdot+m)-c\|_{\ell^p(E_L)}.
\]

For the 34 output coordinates at each physical site use the component-sum
norm `||F||_(p,comp)=sum_nu ||F_nu||_lp(V_L)`. The metric-only version has
ten components. A constant site weight may be inserted into both norms;
all estimates below retain the same constants. For p=1 the unweighted
norm is the raw coordinate sum norm. Its relation to the declared owner
Frobenius sum norm uses only fixed fibre-dimension constants.

Let z0 be constant, `a=z0+c`, and assume both z0 and all values of a lie
in `[-3/2,3/2]`. Put `rho=||c||_infinity`. Define

\[
r_\phi(t)=\phi(z_0+t)-\phi(z_0)-\phi'(z_0)t.
\]

On this interval the exact derivatives satisfy

\[
u''(z)=\frac{72z(z^2-4)}{(4+3z^2)^3},\quad |u''|\le27/4;
\qquad
v''(z)=\frac{16(4-9z^2)}{(4+3z^2)^3},\quad |v''|\le65/16.
\]

The mean value theorem gives
`|r_phi(c1)-r_phi(c2)| <= sup|phi''| rho |c1-c2|`.
Since the coefficient sum in each Euler row vanishes, choose one even-site
reference for that row and subtract its value of `r_phi`. Every source
shift relative to this reference is the sum of at most two signed moves
in G. The certificate records and replays each such path. Shift isometry
and the triangle inequality now give

\[
\boxed{\|E_Y(z_0+c)-D E_Y(z_0)c\|_{p,\mathrm{comp}}
 \le1152\,\|c\|_\infty\|D_{\mathcal G}c\|_p,}
\]

because `2[42*(27/4)+72*(65/16)]=1152`. Keeping only the metric rows gives
the sharper bound

\[
\boxed{\|E_{Q,Y}(z_0+c)-D E_{Q,Y}(z_0)c\|_{p,\mathrm{comp}}
 \le81\,\|c\|_\infty\|D_{\mathcal G}c\|_p.}
\]

This proves an actual finite-stencil nonlinear cancellation, with constants
independent of L. In particular, if `||c_h||_infinity=O(h)` and its **actual
gradient norm in this inequality** is `O(h^2)`, the remainder in that norm
is `O(h^3)`. For the projected nonzero low-frequency part, the owned
`O(h^-1)` inverse loss would turn this particular forcing into `O(h^2)`,
rather than O(h). This observation is an estimate on that forcing, not a
solution or a contraction theorem: compatibility, zero modes, higher
frequencies, the curved metric and transverse corrections still have to be
controlled.

In particular, a pointwise `O(h^3)` remainder is not `O(h^3)` in the
unweighted owner sum norm. That inference would lose the growing lattice
cardinality. The sum-norm theorem above requires the stated gradient bound
in that sum norm; no response-universality limit follows by changing weights.

## 4. How this enters the full nonlinear problem

There is also a useful analytic extension of the remainder statement at the
flat metric. In a fixed compact right-exponential chart put
`K=K_Y(z0+c) exp(w)`, allowing all right-trivialized connection coordinates w,
or restricting w to a chosen transverse complement. Let `J_w w` be the
derivative in w at `(c,w)=(0,0)`. Finite-stencil
analyticity and the mean value theorem give a constant C_r, independent of L,
such that

\[
\|E(K)-D E_Y(z_0)c-J_w w\|_{p,\mathrm{comp}}
\le1152\|c\|_\infty\|D_{\mathcal G}c\|_p
 +C_r\bigl(\|c\|_\infty+\|w\|_\infty\bigr)\|w\|_{p,\mathrm{comp}}.
\]

Indeed, subtract E(K_Y) and integrate the w-derivative along t w; its
difference from the frozen derivative is bounded by the local second
derivatives times `||c||_infinity+||w||_infinity`. There are finitely many
shifts and components and shift isometry introduces no cardinality factor.
This analytic bound does not assert a numerical value for C_r or that a
solution has w of the required size. If `||c||_infinity=O(h)`,
`||D_G c||_p=O(h^2)`, and both `||w||_infinity` and
`||w||_(p,comp)` are O(h^2), the full flat-chart nonlinear remainder
is O(h^3). Obtaining those sizes on a genuinely curved sampled metric from
the range and reduced equations remains the missing continuation estimate.

Thus the norm-only quadratic scaling objection is refined for the exact
Y-family interaction. It is not removed for every interaction or every
physical sequence. The global full-joint Bloch complement and the genuinely
curved reduced center/compatibility equations remain open. Neither
`A4D-JOINT-PALATINI-RESPONSE-DECOUPLING-CLOSED` nor
`A4D-JOINT-MICROSTRUCTURE-METRIC-RESPONSE-NOGO` is asserted.

## 5. Replay

```bash
python 02_REGISTRY/research/certificates/a4d_y_pure_center_quantitative_transport_check.py
```

The script checks the exact all-row operators, the old-owner derivative and
nonconstant-field controls, every selected boost pair, the rational chord
identity, compact derivative constants, finite paths, both nonlinear
remainder constants, the hostile controls, and the pinned full-ledger JSON.
It performs no floating-point decisions and does not edit Lean or claims.
