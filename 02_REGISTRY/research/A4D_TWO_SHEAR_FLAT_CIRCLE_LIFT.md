# Two-shear coframe lifts the six flat resonance circles

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #310.
Status: exact frozen-symbol theorem. It is a test of full-carrier curved
compatibility, not a response-decoupling terminal.

The corrected physical identity-link symbol is `(A^T; C)`. At the standard
coframe it has six continuous rank-23 joint-kernel circles, three of the form
`lambda_0=lambda_r=a`, with the two other phases `i`, and three real conjugates.
The [circle owner](A4D_IDENTITY_PHYSICAL_RESONANCE_CIRCLES.md) gives their
exact kernel. A fixed **nonorthogonal** coframe destroys those old circles
away from their common quarter points already in the connection block:

\[
S_* = I+\tfrac12 E_{10}+\tfrac12 E_{21},\qquad \det S_*=1,
\quad Q_*=S_*^T\eta S_*.
\]

For each `r=1,2,3`, write `H_r(a)` for the literal `24 x 24` connection
Hessian at the identity links and phases `(a,a,i,i)`, with the second `a`
in role `r`. For every `|a|=1`:

\[
\boxed{a\ne i\ \Longrightarrow\ \operatorname{rank} H_r(a)=24.}
\tag{1}
\]

At `a=i`, each `H_r` has rank 16 and the physical joint stack has rank 20.
Complex conjugation proves the analogous statement for the three circles
with fixed phase `-i`. Thus all six **old flat circles** lift on this
frozen nonorthogonal coframe, leaving their universal diagonal-quarter
points. A spatially constant `Q_*` itself has zero macroscopic curvature;
this is a frozen-coefficient input for, not a proof about, a varying metric.

The certificate derives `H_r` directly from the four factors of every
based plaquette and the complementary coframe areas. The optional Gram rows
use the true lift `dS=S Q^{-1}dQ/2`. At `S=I` their physical placement
matches `(A^T;C)` coefficientwise on every line: Laurent radius one and
three exact interpolation nodes suffice, with a fourth unit-circle node
held out. This avoids the historical `(A;C)` placement error.

After clearing the explicit coefficient denominator `d_r` and one negative
Laurent power in each row, fraction-free polynomial elimination gives

\[
\det[d_r a H_r(a)]=a^{14}(a-i)^8 P_r(a),\qquad
(d_1,d_2,d_3)=(4,8,8),\quad \deg P_r=12.
\tag{2}
\]

Every coefficient of `P_r` is pinned in the JSON ledger. Over `Q(i)` its
irreducible factor degrees are `(3,3,3,3)` for `r=1` and `(6,6)` for
`r=2,3`. For each factor `p`, the certificate computes the reverse conjugate
`p^*(a)=a^deg(p) conjugate(p(1/conjugate(a)))` and verifies
`gcd(p,p^*)=1` exactly. A unit-modulus root of `p` would also be a root of
`p^*`, so no factor of `P_r` has a unit-modulus root. The exact determinant
at `(3+4i)/5` is independently checked against direct matrix elimination.
The `a^14` factor is irrelevant on the character torus. Equation (1)
follows for the entire continuous circle, not just sampled characters.

This is a nontrivial **coframe-coupling** result: a single shear or a
diagonal warp leaves connection rank 22 on the role-1 circle at the held-out
character, while the two-shear coframe raises it to 24. It explains why a
single metric component cannot stand in for a general curved background.
On every compact subarc separated from `a=i`, continuity supplies a positive
singular-value bound for all coframes in some neighborhood of `S_*`; the
bound is not uniform as the subarc approaches the quarter point.

This theorem does not classify new zeros off those six old circles, provide
a whole-torus inverse, treat shared links on a varying coframe, or control
the nonlinear projected plaquette current in the owner sum. In particular,
lifting old circles does not prove the stationary-response quotient image
is one class. Those are the remaining task-level obligations.

Replay:

```sh
python3 02_REGISTRY/research/certificates/a4d_generic_coframe_circle_lift_check.py
```
