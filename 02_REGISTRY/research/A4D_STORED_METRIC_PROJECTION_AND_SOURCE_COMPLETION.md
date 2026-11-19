# Full stored-adjoint metric image and the missing source equation

17 October 2026. Same Draft #334, input e397a0af. Consumer: the
[complete-exit/action source](A4D_COMPLETE_EXIT_ACTION_AND_SECOND_SOURCE.md)
must be pulled back through the **actual joint** metric image, not an
assumed ten-dimensional tangent. This strengthens the earlier
[fixture/source-image calculation](sources/d0_native_gr_source_image_2026-10-16/RESULT_RU.md)
by a nonlinear necessity/sufficiency theorem and a generic source formula.
It does not repeat its support/rank census.

## 1. Exact nonlinear metric projection

Use eta=diag(1,-1,-1,-1), Q=F eta F^T, native legs
v_r=eta F_r^T, and a future unit observer n. Set

```text
tau=F n, lambda=Q^-1 tau,
tau^T Q^-1 tau=1,
S=tau tau^T-Q=W^T W.                                  (1)
```

W contains the three spatial components of the legs in the observer's
rest frame. Therefore S is positive semidefinite, rank3, with kernel
span(lambda). We stay in a regular neighbourhood with all own-leg spatial
lengths nonzero, an invertible F and a chosen future branch.

The two stored-adjoint edge conditions imply that a proper Lorentz
transport A_xy preserves both n and its own leg:

```text
A_xy n_y=n_x, A_xy v_r(y)=v_r(x), y=x+h e_r.             (2)
```

These statements follow from the original positive observer pairing and
inverse-return/creation adjoint identities; the [joint chart](A4D_NATIVE_FULL_JOINT_KERNEL_AND_MATTER_REDUCTION.md)
retains their full observer/link solutions. They imply the exact scalar
invariants

```text
tau_r(y)=tau_r(x), Q_rr(y)=Q_rr(x).                     (3)
```

**Projection theorem.** A nearby Lorentz-signature field Q is realized by
the complete regular stored-adjoint joint class if and only if there is
a nearby tau on the selected future branch satisfying (1) and (3) on
every own edge. Thus the nonlinear remaining condition is the existence
of this line-constant observer projection. Moving n or compensating links
cannot remove it.

For sufficiency, choose a smooth rank3 Gram factor W of S. Locally choose
three columns I with S_II positive definite and factor
`S_II=L^T L`; define the fourth column by `w_j=L^-T S_Ij`.
The rank3 Schur identity gives its correct length and all Gram entries.
Set u_r=(tau_r,w_r), n=e0 and `F=[tau,-W^T]`. Then F eta F^T=Q and F
is invertible. By (3) the two w_r on each own edge have the same nonzero
length. The near-identity SO3 rotation taking w_r(y) to w_r(x) exists
smoothly; its free SO2 stabilizer gives all such edge rotations. Their
Lorentz lifts diag(1,R_r) solve (2) and both adjoint conditions.

For an arbitrary future unit field n, take the canonical proper Lorentz
whitening L(n)n=e0 and put

```text
v_r=L(n)^-1 u_r,
A_xy=L(n_x)^-1 diag(1,R_r) L(n_y).                      (4)
```

This restores the complete moving-observer freedom, not a frozen-observer
subclass. There is no flatness/torsion-free requirement on the links in
this theorem. Full16 exterior lifting preserves these pair equations.
The construction is kinematic; it does not solve the price's Euler rows.

## 2. The exact tangent and its conormal

Linearize at a constant regular background. On a Fourier mode with all
four own-direction shift factors nonzero, (3) gives

```text
delta tau=0, H_rr=0, H=delta Q,
2 lambda^T delta tau-lambda^T H lambda=0.
```

Consequently the complete metric image is

```text
H_rr=0, lambda^T H lambda=0.                            (5)
```

The converse follows by differentiating the local Gram/link construction.
All four observer/link compensations have already been allowed. The five
conditions are independent: regular own legs exclude lambda supported on
a single coordinate, so lambda lambda^T has a nonzero off-diagonal part.
The image has dimension5, with conormal

```text
E=Diag(d)+c lambda lambda^T.                            (6)
```

Pairing is Tr(E H), counting both off-diagonal entries. Since Q=g^-1,
`delta g=-g H g`, the intrinsic Einstein action has covariant source
`+G_mu,nu` against H, with its boundary convention retained.

## 3. Generic Bianchi residual and one explicit completion row

Let k be a real continuum Fourier covector, a=Qk, s=tau.k=lambda.a.
For a covariant Einstein source, Bianchi is E a=0. On the open set
where **each a_i is nonzero**, substituting (6) leaves exactly one line:

```text
E_res=lambda lambda^T-s Diag(lambda_i/a_i),
E_res a=0.                                            (7)
```

This source is nonzero because its off-diagonal part is nonzero. It is
invisible to every admitted H in (5). Bianchi alone cannot eliminate it.
For k^TQk nonzero it is also an actual linearized Einstein tensor: choose
`bar h=2E_res/(k^TQk)` and `h=bar h-(g/2)Tr(Q bar h)`.
Then k^TQ bar h=0 and the full Fierz–Pauli tensor of h exp(i k.x) is E_res.
The producing h need not lie in (5); this is not a constrained stationary
solution or an original fixed-source counterexample.

There is a simple improvement over a conformal completion. Define at the
fixed background, independently of k,

```text
P_off=lambda lambda^T-Diag(lambda_i^2).
Tr(E_res P_off)=sum_(i!=j)lambda_i^2 lambda_j^2>0.       (8)
```

Its zero diagonal kills every diagonal term in (6). Therefore a **single
additional source row** paired with P_off would remove the generic
Bianchi residual, including the earlier conformal-zero exception. This
is not a new momentum-dependent detector or an eigenbasis oracle.

However lambda^T P_off lambda is the same strictly positive number.
P_off violates (5), so it is not an existing native variation. Formula
(8) states precisely what an admitted enlargement or independent physical
source equation would have to supply; it does not add that equation.

## 4. Exceptional modes are retained

When any a_i=0 use the exact equations, without division:

```text
d_i a_i+c lambda_i s=0 for each i.                      (9)
```

For regular lambda_i nonzero on the zero set, if s is nonzero this forces
c=0 and leaves diagonal sources on that set. If s=0, the c direction and
these diagonal directions survive. P_off detects c, not those diagonal
sources. For more degenerate lambda, (9) itself is the criterion. Thus
(8) is not a claim of one-row completion for all momenta.

The bounded control includes a full-support k with one component of Qk
zero and an explicit undetected diagonal source. No exceptional mode or
matter grade is discarded to obtain a ten-row conclusion.

## 5. Consuming consequence

The complete positive E↔Delta inverse is an operator statement. Its
pullback through the stored class has the nonlinear projection (1)–(4)
and source residual (7), with exceptions (9). Reconstructing a full
Levi–Civita connection from a represented coframe does not remove these
variation constraints. A complete native GR claim needs its own admitted
source completion or a physically forced larger domain, together with
the unchanged action/matter/clock source and refinement control.

Evidence is the adjacent `sources/d0_stored_metric_projection_2026-10-17/`
packet: a rational nonconstant own-edge fixture, Gram reconstruction,
moving observer, all16 exterior intertwiners, invariant negative controls,
generic residual/completion identities and one full Einstein realization.
These checks support the stated analytic proof, not physical selection,
nonflat joint stationarity or the original raw h^-2/#216 terminal.
