# All-period cubic barrier on a pure physical resonance circle

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #310.
Input head: `909ad048d25de2def8875290c41bf9475e9180e6`.
Status: exact all-period cubic compatibility gate and fixed-period tangent
isolation. Coupled circles, a uniform nonlinear radius, and curved transfer
are not claimed.

The [full quadratic envelope gate]
(A4D_IDENTITY_RESONANCE_CIRCLE_NONLINEAR_GATES.md) on `(a,a,i,i)` leaves
`Z_n=t epsilon_n i^n` and its i multiple, with arbitrary signs. The following
literal identities remove the apparent need to inspect every sign period.

Set `n=x0+x1`, `q=sum x mod4`, and let T shift n by one at fixed q. Normalize
`t=1/2`. The leading real log U has

\[
U_{n,q,2/3}=\epsilon_n(1,0,-1,0)_q T_{2/3},\qquad
U_{n,q,0/1}=\tfrac12(\epsilon_{n+1}-\epsilon_n)
(1,1,-1,-1)_q K_1.
\tag{1}
\]

The second cone is a q translation of this field. Both the common and
alternating even connection blocks have exact finite Laurent inverses. The
new common block at `(b,b,1,1)` has radius four and row/column coefficient
envelopes `9/2`; the earlier alternating output inverse at `(b,b,-1,-1)` has
radius three and the same bound. Their two-sided coefficient identities give
period-independent inverses on every lp space, including unweighted owner1.

In the Boolean group algebra `Q[epsilon_j]/(epsilon_j^2-1)`, all signs are
independent. Literal incident faces fix the unique even quadratic log W:

\[
W_{q,0}=W_{q,1}=\tfrac12 K_1\quad(q=0,2),
\qquad W=0\text{ on all other entries}.
\tag{2}
\]

For `log L=alpha U+alpha^2 W`, every connection and every metric coefficient
through degree two vanishes, including the common metric readout. At degree
three every metric row still vanishes. The positive q Fourier coefficient
of the 34-row joint source is exactly `s_3=S(T)epsilon`. In zero-based owner
row numbering its only entries are

\[
(s_3)_{1,2,9,10}=-\tfrac i8\epsilon_n,
\qquad
(s_3)_{13,15,20,22}
=\frac{\epsilon_n-\epsilon_{n-1}
+i(\epsilon_n+\epsilon_{n-1})}{16}.
\tag{3}
\]

All cubic Boolean monomials cancel to these linear expressions. This is
computed from actual four-link plaquette products and right-trivialized Euler
variations, not fitted from sign sequences.

The pinned witness is a row Laurent polynomial `L(z)` of powers 0,1,2 with
58 nonzero rational-complex entries and coefficient envelope 36. Every
coefficient of both identities is verified:

\[
\boxed{L(z)J(iz,iz,i,i)=0,\qquad L(z)S(z)=\tfrac i4 z.}
\tag{4}
\]

Here `J=(A^T;C)` is the independently audited physical symbol. Thus **any**
odd cubic normal correction V gives

\[
L(T)(s_3+J(T)V)=\tfrac i4 T\epsilon\ne0.
\tag{5}
\]

Identifying Boolean indices modulo an arbitrary period preserves all
identities. For the original amplitude `Z=t epsilon i^n`, U scales by 2t
and the cubic source by `(2t)^3`. The finite convolution bound therefore gives

\[
\boxed{\|s_3+J V\|_p\ge\tfrac{t^3}{18}\|\epsilon\|_p,
\qquad1\le p\le\infty.}
\tag{6}
\]

There is no period normalization. Lifting the phase projection and shifts to
the full torus preserves their finite-convolution bounds and multiplicities;
in owner1 a unit-modulus sign field has norm `L^4`. Conjugation and spatial
permutation give the other pure circles.

## Analytic consequence and its exact scope

No C3 exact joint branch through I can have a nonzero tangent solely in the
pure-circle quadratic cone. Even quadratic corrections are unique by the
connection inverse. Additional odd second-order kernel coordinates cannot
change the odd cubic equation: odd times odd has even q parity. Arbitrary
third-order normal coordinates lie in the range killed by (4). Thus (5)
contradicts the remaining noncommon metric/connection equations.

At each fixed L, the joint kernel in the full `(n,q)` invariant sector has
complex dimension `L+3`: one circle direction at every n frequency and three
additional quarter directions at z=1. A finite-dimensional normal chart
exists. If exact nonzero roots approach I with their normalized center tending
to a pure-circle direction, the even equations force the limit into the
classified quadratic cone. Dividing the odd equations by the cubed center
norm and applying (4) contradicts (5). This excludes that tangent accumulation
without assuming an analytic branch parameterization.

The normal-chart constants may depend on L. This argument does **not** supply
a uniform radius for arbitrary refinement sequences, and it does not handle
limits containing comparable additional quarter coordinates or coupled-circle
directions. On a varying fixed coframe the flat witness is not automatically
an exact annihilator. No full curved Target D/U terminal follows.

## Replay

```sh
python3 02_REGISTRY/research/certificates/a4d_identity_circle_sign_cubic_gate_check.py
```

The checker pins all literal Boolean sources, the common even inverse, and the
left witness. A changed witness sign and the wrong `(A;C)` placement both fail
the coefficient identity. The result is
`ALL_PERIOD_PURE_CIRCLE_SIGN_CUBIC_GATE_CERTIFIED; TASK_TERMINAL_OPEN`.
It is now an input to the response-memory program, not a new main spectral
classification target.
