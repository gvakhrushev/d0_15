# Identity quarter center: nonlinear classification and response suppression

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #310.
Input head: `3b0430770f717c222caf7dbbe6b0080f2843a94f`.
Action and Gram-section metric coordinates: unchanged.

Status: exact finite algebra plus an analytic local theorem on the real
four-phase identity chart. This closes its entire nonlinear stationary
center, including mixed center directions. The theorem concerns fields
depending only on `p=(x0+x1+x2+x3) mod 4` at constant `eta`. It does not
assert a varying-envelope, arbitrary-Bloch or fixed-curved theorem.

The [certificate](certificates/a4d_identity_quarter_nonlinear_response_check.py)
reconstructs the literal Euler jets over Q and Q(i), all 36 quadratic and
120 cubic coefficients, and exact all-amplitude vacuum identities. Its
[ledger](certificates/a4d_identity_quarter_nonlinear_response_results.json)
contains every range-correction and reduced-equation coefficient.

## 1. The closed statement

Write `l=log K` in the 96-dimensional real four-phase link chart. Let

\[
F(l)=\bigl(E_K(\eta,e^l),\Pi_{\ne0}E_Q(\eta,e^l)\bigr),\qquad
M(l)=\tfrac14\sum_{p=0}^3 E_Q(\eta,e^l)(p).
\]

Here `Pi_ne0` removes only the four-phase average: it retains 30 metric
equations, and F has 126 real rows. In particular, `F=0` permits an
initially unspecified phase-common metric response; it does not set that
response to zero by definition. Metric components are the owner's ten
Gram coordinates, not variations restricted to the center ansatz.

There are a radius epsilon and a constant C such that:

1. All `F(l)=0` with `||l||<epsilon` are precisely eight one-parameter
   families described below. All have the full metric response `E_Q=0`.
2. For the union V of these exact vacua,
   `dist(l,V) <= C ||F(l)||^(1/3)`.
3. The phase-common readout has the stronger estimate

\[
\boxed{\|M(l)\|\le C\|l\|\,\|F(l)\|.} \tag{1}
\]

These are local analytic conclusions, not merely statements about the
leading jets. Constants refer to this fixed four-phase problem. Section 7
states exactly which repeated-cell refinement estimate follows.

## 2. Center coordinates and exact axes

Use generator order `(K1,K2,K3,J12,J13,J23)`. Define

\[
\begin{aligned}
T_0&=J_{12}-J_{13}+J_{23},&T_1&=K_2-K_3+J_{23},\\
T_2&=K_1-K_3+J_{13},&T_3&=K_1-K_2+J_{12}.
\end{aligned}
\]

The four-phase linear joint kernel has real dimension eight:

\[
V(c)_{p,r}=\begin{cases}
a_rT_r,&p=0,\\ b_rT_r,&p=1,\\-a_rT_r,&p=2,\\-b_rT_r,&p=3,
\end{cases}\qquad c=(a_0,a_1,a_2,a_3,b_0,b_1,b_2,b_3).
\]

The literal derivative has rank 88. The `z=1,-1` connection blocks are
invertible. At `z=i`, the joint 34-by-24 block has rank 20 and kernel
spanned by the four role-supported T_r; `z=-i` is its real conjugate.
These are physical dressed-link coordinates after the Gram-section
gauge quotient.

For any role r and either parity s=0,1, set

\[
K_r(s)=U_r(t),\quad K_r(s+2)=U_r(t)^{-1},\quad
U_r(t)=(I-tT_r/2)^{-1}(I+tT_r/2),
\]

and set every other link to I. These are eight exact families. Indeed,

\[
T_r^3=\kappa_rT_r,\quad(\kappa_0,\kappa_1,\kappa_2,\kappa_3)=(-3,1,1,1),
\qquad U_r(t)=I+\frac{4tT_r+2t^2T_r^2}{4-\kappa_rt^2}.
\]

The checker puts every link over the common denominator
`D=4-kappa_r*t^2`, including the inactive identities. Each literal
right-trivialized Euler term has four factors. Its complete cleared
numerator has degree at most eight. All coefficients of all 136 rows
vanish for every role and both parities. This proves identities where
`D!=0`, rather than sampling amplitudes or truncating an infinite series.
Near zero the Cayley family reparametrizes `exp(u T_r)`, so its logarithm
is exactly one of the eight straight axes `V(u e_j)`.

## 3. Analytic range elimination and the quadratic gate

Choose all connection coordinates at `z=1,-1` as normal variables. At
`z=i`, delete columns `(5,11,16,21)` and retain the other 20 as normal
columns. Exact row elimination of the joint block gives a transform B
with `B Q_normal = (I_20;0_14)`. Use all even-frequency connection rows
and the first 20 complex transformed quarter rows as the 88 range
equations. Their normal derivative is invertible. The analytic implicit
function theorem gives a unique normal graph `w=W(c)=O(|c|^2)` on which
these range equations vanish.

The remaining equations are an even-frequency metric vector R_e of
dimension ten at z=-1 and a quarter vector R_o of dimension 28 over R.
Translation by two phases acts as `c -> -c`. Our range splitting commutes
with that translation, so uniqueness gives the exact parity laws

\[
R_e(c)=Q_2(c)+O(|c|^4),\qquad
R_o(c)=Q_3(c)+O(|c|^5). \tag{2}
\]

This separation matters: an even quadratic obstruction cannot cancel an
odd cubic obstruction along a shrinking sequence.

If f_K^(2) is the literal quadratic connection forcing, the quadratic
normal correction is determined uniquely by

\[
w_0=-H(1)^{-1}\widehat f_K^{(2)}(1),\qquad
w_2=-H(-1)^{-1}\widehat f_K^{(2)}(-1).
\]

Here `H(z)=A(z)^T` in the owner's placement. The checker independently
matches every literal Euler derivative column at z=1,-1,i to H and C.
The alternating metric gate is
`Q_2=hat f_Q^(2)(-1)+C(-1)w_2`. The mean metric quadratic coefficient
vanishes identically on all eight center coordinates; `C(1)=0` as well.

The exact ten-vector Q_2 is `M_2 t`, where M_2 has rank seven and kernel
spanned by `(3,1,1,1,1,1,-1,1)`, and

\[
\begin{aligned}
t_0&=a_0(a_1-a_2+a_3)-b_0(b_1-b_2+b_3),\\
t_1&=a_0b_0,&t_2&=a_1b_1,&t_3&=a_2b_2,&t_4&=a_3b_3,\\
t_5&=a_0b_1+a_1b_0,&t_6&=a_0b_2+a_2b_0,&t_7&=a_0b_3+a_3b_0.
\end{aligned}
\]

Over the reals, `Q_2=0` implies `t=s(3,1,1,1,1,1,-1,1)` and hence

\[
(a_0b_1-a_1b_0)^2=t_5^2-4t_1t_2=-3s^2.
\]

Therefore s=0 and all eight t_i vanish. The real quadratic zero cone is
exactly the union of ten three-dimensional planes:

- `b=0`, `a=(u,v,w,-v+w)`;
- `a=0`, `b=(u,v,w,-v+w)`;
- eight planes with `a0=b0=0` and, independently for each spatial role,
  either a_r or b_r free, with its opposite parity set to zero.

For completeness, if a0 is nonzero the product and cross equations force
every b_r to zero, then t0 gives the first plane. Nonzero b0 gives the
second. If both vanish, `a_r*b_r=0` gives the eight spatial planes.

## 4. Cubic gate and transverse isolation

Insert `V(c)+W_2(c)` into the exact exponential-link Euler series to degree
three. Project its quarter coefficient by the last 14 complex rows of B.
Any third-order normal correction is killed by this projection. Thus the
result is precisely Q_3 in (2), without having to solve for W_3.

The certificate reconstructs every cubic coefficient by polarization. It
also evaluates a separate dense rational amplitude vector to check the
reconstruction. On each quadratic plane the row space of Q_3 is exactly:

| Plane | Rank | Monomials spanning the row space |
|---|---:|---|
| either temporal plane | 9 | u^2 v, u^2 w, u v^2, u v w, u w^2, v^3, v^2 w, v w^2, w^3 |
| any spatial plane | 7 | u^2 v, u^2 w, u v^2, u v w, u w^2, v^2 w, v w^2 |

On a temporal plane these equations force v=w=0. On a spatial plane at
most one of u,v,w can be nonzero. Consequently

\[
\{c\in\mathbb R^8:Q_2(c)=Q_3(c)=0\}
=\bigcup_{j=0}^7\mathbb R e_j. \tag{3}
\]

At every e_j the stacked derivative `D(Q_2,Q_3)` has exact rank seven.
Its radial column vanishes, so it is injective on the seven-dimensional
normal space to that axis. These eight ranks are also certified exactly.

Hostile controls include `a1=a2=1` with other coordinates zero: its
quadratic gate vanishes but its cubic gate does not. Keeping only the
quadratic calculation would therefore retain false mixed branches.
The simultaneous temporal cosine/sine vector `a0=b0=1` already fails
the quadratic gate.

## 5. Why these finite jets prove a nonlinear classification

Let r=|c| and v=c/r on the unit sphere. By (2) the scaled analytic map

\[
\mathcal B(r,v)=\left(r^{-2}R_e(rv),r^{-3}R_o(rv)\right)
\]

extends to r=0 with value `(Q_2(v),Q_3(v))`. Its only zeros on that
sphere at r=0 are the sixteen signed axis points. Away from small
neighborhoods of those points, compactness gives a positive lower bound
for its norm, retained for all sufficiently small r.

Near a signed axis its derivative on the sphere has rank seven. Select
seven independent output rows there. The inverse function theorem and
continuity give a uniform local lower Lipschitz bound in v. The exact
axis identities imply `B(r,+/-e_j)=0` for every sufficiently small r;
therefore there is no displaced zero near that axis. Combining the
finitely many neighborhoods with the compact complement gives

\[
\|R_e(c)\|+\|R_o(c)\|
\ge c_*\,|c|^2\operatorname{dist}(c,\mathcal A),\qquad
\mathcal A=\bigcup_j\mathbb R e_j. \tag{4}
\]

Indeed the original rows weigh the scaled even component by r^2 and the
odd component by r^3; for r<=1 both dominate r^3 times the scaled norm.
Distance on the sphere is comparable to `dist(c,A)/r` near each axis.
This proves exact local classification on the range graph. The normal
implicit function theorem transfers it to the full 96-variable chart.

Since `dist(c,A)<=|c|`, (4) also gives the cubic error bound. A nonzero
range residual controls distance to the range graph linearly. The graph
vanishes on each axis and is Lipschitz. These facts prove
`dist(l,V)<=C||F(l)||^(1/3)` for arbitrary sufficiently small l.

## 6. The stronger response estimate

Restrict the phase-common metric response to the range graph and write
`m(c)=M(V(c)+W(c))`. It is analytic and even under c -> -c. Its constant
and linear terms vanish, and Section 3 verifies that its complete
quadratic term vanishes. Therefore

\[
m(c)=O(|c|^4),\qquad Dm(c)=O(|c|^3).
\]

Moreover `m=0` on every axis by the exact family identities. Integrating
Dm on a segment to a closest axis point gives

\[
\|m(c)\|\le C|c|^3\operatorname{dist}(c,\mathcal A)
\le C|c|\bigl(\|R_e(c)\|+\|R_o(c)\|\bigr), \tag{5}
\]

where the last step uses (4). This is a readout estimate even though the
linear inverse has a physical kernel.

For arbitrary l, the normal implicit-function chart writes
`l=V(c)+N(c,s)`, where s is its range residual,
`N(c,0)=W(c)` and `|N(c,s)-W(c)|<=C|s|`. Thus
`|R(c)|<=C|F(l)|` and `|c|+|s|<=C|l|`. The full phase mean M has zero
derivative at l=0: the zero-frequency metric block C(1) vanishes and all
other Fourier components average to zero. Its derivative near zero is
therefore O(|l|). Moving from `N(c,s)` to `W(c)` changes M by at most
`C|l| |s|`. Together with (5) this proves (1).

No assumption that a small remainder implies a uniformly small inverse
was used. In this sector the nonlinear constraints and readout vanishing
supply the estimate which the false full-gap premise could not supply.

## 7. Refinement consequence and the remaining curved obligation

On a periodic L^4 carrier with `4|L`, restrict strictly to these repeated
four-phase fields. Each phase occurs exactly L^4/4 times. For any fixed
`1<=p<=infinity`, repeating a cell multiplies both output norms in (1)
by the same counting factor; the log factor can be taken in sup norm.
Consequently the estimate for the lifted constant phase mean is

\[
\|\overline E_Q\|_{\ell^p}
\le C_p\|\log K\|_\infty
\bigl(\|E_K\|_{\ell^p}+\|\Pi_{\ne0}E_Q\|_{\ell^p}\bigr), \tag{6}
\]

with a constant independent of L on this sector, including the actual
unweighted component sum at p=1. This counting argument is essential;
arbitrary growing-dimensional norm equivalence is not being used.

If the norm of the right-hand residual is `O(h^2)` in the declared norm
and `||log K_h||_infinity -> 0`, then
`h^-2 ||overline E_Q|| -> 0`. A sitewise O(h^2) bound alone is not the
stated unweighted sum hypothesis. The estimate suppresses the
phase-common readout; it does not give an extra small factor for a
nonzero oscillatory metric source itself.

This settles the flat four-phase stationary center through the identity
and its phase-common response, not merely the finite-amplitude Y chart.
For the requested fixed-curved theorem one must still control slowly
varying coefficients, envelopes and other physical frequencies relative
to `K_h^sm(g)`, in the owner sum norm. In particular, (6) cannot be
applied independently to adjacent cells while discarding the links and
Euler rows crossing their boundaries. A curved replacement of (6), with
an `o(h^2)` response remainder after that gluing, remains an actual proof
obligation. Existence of the required exact joint continuation with its
independently prescribed source also remains open.

The full uniform linear inverse stays refuted by the designated-gap
owner. This result supplies a proved nonlinear response mechanism on a
restricted sector; it does not reinstate that inverse, modify the action,
choose a new source, or promote an Einstein/physical task terminal.
Keep #310 Draft / IN_PROGRESS.

## Reproduction

```bash
python 02_REGISTRY/research/certificates/a4d_identity_quarter_nonlinear_response_check.py --expect 02_REGISTRY/research/certificates/a4d_identity_quarter_nonlinear_response_results.json
```

The checker needs NumPy for exact object-array operations and the sibling
`a4d_designated_full_gap_check.py` for the literal flat-symbol convention.
It uses no floating point, SymPy, rank oracle, or numerical stationary
seed. The classification, blow-up estimate and response bound are proved
above from its exact finite outputs; they are not Lean formalizations.
