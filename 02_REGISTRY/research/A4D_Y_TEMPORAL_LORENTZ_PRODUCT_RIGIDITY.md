# A4D-Y temporal Lorentz product rigidity audit

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`  
PR: #310  
Status: exact scoped advances; global terminal not reached.

## 1. Scope correction for the submitted extra-boost factor

The current owner convention in
`a4d_y_two_center_cartan_transport_check.py` is

[
B=K_1+K_2+K_3.
]

The submitted follow-up also names its added generator
(W=K_1+K_2+K_3). Under those definitions the product

[
C_B(-d)C_W(kappa)
]

does not add an independent boost direction. Exact Cayley composition gives

[
C_B(-d)C_B(kappa)=C_B(t),
qquad
t=rac{4(kappa-d)}{4-3dkappa}.
]

Moreover the submitted coefficient is exactly

[
c(d,kappa)=rac{3t^2+4}{3t^2-4}.
]

Its discriminant
(-48(3d^2-4)^2) is correct, but in the current owner notation this is a
reparameterization of the existing one-dimensional (B) subgroup. If a
different generator was intended, it must be specified explicitly.

Owner:
`a4d_y_boost_cayley_composition_check.py`.

## 2. Exact full temporal boost rigidity

Let

[
V=u_1K_1+u_2K_2+u_3K_3,qquad
r^2=u_1^2+u_2^2+u_3^2,qquad
s=u_1+u_2+u_3,
]

and use the temporal link

[
K_0=C_Y(1)C_V
]

on the product-plane solder (S_f=I+(f-1)P_perp).

A polynomial combination of the three literal role-0 boost Euler rows is

[
P_1E_{K_1}+P_2E_{K_2}+P_3E_{K_3}
=
rac{(r^2+4)(s^2r^2+64)}{r^2-4}
left(3f_0^2-f_1^2-f_2^2-f_3^2ight).
]

On the real Cayley chart (r^2
e4),

[
r^2+4>0,qquad s^2r^2+64ge64,
]

so stationarity forces the backward-harmonic product equation. On a connected
periodic spatial carrier the finite maximum principle makes (f) constant.

Thus all three real temporal boost directions, including the two directions
transverse to (K_1+K_2+K_3), are excluded as a product-profile rescue in this
ansatz.

Owner:
`a4d_y_full_boost_product_rigidity_check.py`.

## 3. Exact full temporal SO(3) spin rigidity

Let

[
R=aJ_{12}+bJ_{13}+cJ_{23}
]

and use

[
K_0=C_Y(1)C_B(-d)C_R.
]

Three literal role-0 boost rows have a polynomial combination

[
C_1E_{K_1}+C_2E_{K_2}+C_3E_{K_3}
=
-rac{2(3d^2+4)}{3d^2-4}
M_{m spin}
left(3f_0^2-f_1^2-f_2^2-f_3^2ight),
]

with

[
M_{m spin}
=
3d^4(a-b+c+3)^2+4(a-b+c-4)^2.
]

For real parameters the multiplier can vanish only on

[
d=0,qquad a-b+c=4.
]

On that complete exceptional plane the nine spatial-role rotation rows are
linear in ((f_0,f_1,f_2,f_3)), have rank three, and have kernel exactly

[
operatorname{span}(1,1,1,1).
]

Hence the exceptional plane also forces
(f_1=f_2=f_3=f_0).

The exceptional transport rows are unchanged under the two phase-2
conventions checked explicitly:

1. reciprocal completion ([K,I,K^{-1},I]);
2. same-spin ordering (C_Y^{-1}C_R) on phase 2.

Therefore the result is not a phase-order artifact.

Owner:
`a4d_y_full_spin_product_rigidity_check.py`.

## 4. What is now excluded

For the (z=1) product-plane background, nonconstant (f) cannot be rescued
by either of the following temporal-only correction classes:

- an arbitrary real pure boost Cayley factor;
- an arbitrary real spatial (SO(3)) rotation Cayley factor together with
  the owned boost-dual (B) factor.

This strictly strengthens the earlier commuting (Y/B) necessary-row no-go.

## 5. Remaining temporal question: noncommuting boost + rotation

The genuinely new six-parameter factor is

[
K_0=C_Y(1)C_VC_R
]

with arbitrary (V) and (R).

A direct exact six-parameter SymPy factorization exceeded the current symbolic
runtime. A numerical coefficient-level scout was therefore used only to choose
the next exact target:

- 500 initial random real points and 5000 wider samples were checked;
- at every checked point the three boost Euler rows possessed a one-dimensional
  left-null combination cancelling all terms linear in the neighbouring
  (f_i);
- the remaining quadratic coefficients had the Laplacian ratio
  (3:-1:-1:-1) to numerical precision;
- no counterexample to that structure was observed.

This is diagnostic only. It is not promoted to an exact theorem.

The exact missing object is the rational multiplier of that six-parameter
combination and its real zero locus. The likely first hostile control is the
known spin exceptional locus (V=0, a-b+c=4), but no claim that it is the
complete zero set is made.

## 6. Global boundary

Even a full temporal-Lorentz product rigidity theorem would not close PR #310.
Still open are:

- arbitrary transverse corrections on spatial links;
- exact all-Bloch classification of the full (136	imes96) joint symbol;
- a refinement-uniform range estimate in the declared owner topology;
- nonlinear reduced center/range control or a genuine joint-critical
  countersequence.

The connection-only quantity (minlambda(H_{AA})) is not accepted as a
uniform inverse certificate. The required linear object is a smallest
singular-value/lower-bound statement for the correctly projected full joint
operator, or an exact Laurent-minor equivalent.

No task-level terminal is claimed here.
