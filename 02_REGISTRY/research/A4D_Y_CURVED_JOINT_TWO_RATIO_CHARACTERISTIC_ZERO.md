# Curved Y joint symbol: exact characteristic-zero two-ratio elimination

Status: exact research theorem with a reproducible finite certificate.
Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, PR #310.
Input branch tip: `2877d6b780d3631bd110acbfd11a04acff449713`.
No Lean, public-claim, or task-terminal promotion.

On the representative ratio plane

\[
\rho_0=1,\qquad\rho_1=x,\qquad\rho_2=y,\qquad\rho_3=1,
\]

the 68-row phase-1/phase-2 interior joint operator has rank 68 at every
point of `(C*)^2` except `(1,1)`, where its exact rank is 65. The common
zero-set of the four fixed chart minors is exactly `(1,1)` in
characteristic zero. This closes the characteristic-zero lift of this plane.
It does not classify the genuine three-ratio interior locus, the remaining
boundary equations, the full Bloch locus, or nonlinear physical response.

## 1. Exact inputs and polynomial convention

Use the same literal rational stencil and four 68-column charts as
`a4d_y_curved_joint_two_ratio_modular_check.py`. Multiply each selected
matrix entry by `14*x*y`. The integer-minors owner reconstructs the four
determinants `D_i in Z[x,y]` by coefficientwise finite-field DFT and CRT.
For each chart, 15 reconstruction primes give a modulus greater than twice
the exact product-of-row-l1 coefficient bound. A distinct prime replays
every coefficient. The full coefficient ledgers, bounds, CRT moduli, and
hashes are now saved in
`certificates/a4d_y_curved_joint_two_ratio_integer_minors_results.json`.

Write

\[
D_i=c_i x^{a_i}y^{b_i}P_i,\qquad P_i\in\mathbb Z[x,y]
\]

with `P_i` primitive and its coordinate monomial removed. All discarded
factors are nonzero on the complex algebraic torus, so this preserves the
common zero-set there.

| Chart | `(a_i,b_i)` | Bidegree of `P_i` | Nonzero coefficients |
|---|---:|---:|---:|
| 0 | `(54,47)` | `(40,34)` | 1184 |
| 1 | `(47,58)` | `(38,38)` | 1271 |
| 2 | `(49,50)` | `(43,40)` | 1448 |
| 3 | `(62,49)` | `(37,36)` | 1174 |

Set `R_01=Res_y(P_0,P_1)` and `R_23=Res_y(P_2,P_3)`. Each resultant
is the determinant of its **fixed-degree** Sylvester matrix over `Z[x]`.
The new certificate computes the modular resultants directly as polynomial
resultants; it does not change the Sylvester dimensions at special x-values.

## 2. Primitive-gcd reduction lemma

Let `A,B in Z[x]` be nonzero and let a monic `D in Z[x]` divide both
over `Z[x]`. Suppose, for a prime p:

1. `deg(A mod p)=deg A`;
2. the monic gcd of `A mod p` and `B mod p` has degree `deg D`.

Then the monic gcd of A and B over `Q[x]` is D.

Proof: choose the primitive integer gcd G over `Z[x]`. Gauss's lemma gives
integer cofactor factorizations of A and B through G. Since the leading
coefficient of A is nonzero mod p, the leading coefficient of G is also
nonzero mod p. Thus `deg(G mod p)=deg G`, and `G mod p` divides both
reductions. Consequently `deg G <= deg D`. The exact common divisor D gives
the opposite inequality; equal degrees and the monic normalization identify
the gcd with D. Degree preservation is needed for only one input.

Agreement of several modular gcds, even with degree preservation, cannot
replace the exact common divisor hypothesis. For

\[
N=664448401\cdot996672601\cdot1328896801,
\quad A=x-1-N,\quad B=A(x+2),
\]

all three modular gcds are `x-1`, with preserved degrees, whereas the exact
gcd is `x-1-N`. A second hostile control is `p*x+1`: its nonconstant factor
reduces to a unit when degree preservation is omitted. Both controls execute
inside the new certificate.

## 3. Exact common structural divisor

For each Sylvester entry, record the least x-exponent. Integer Hungarian
duals u and v satisfy `u_i+v_j <= valuation_x(entry_ij)`; every inequality
is checked directly. Their sum bounds the x-valuation of every determinant
term and gives

\[
\operatorname{ord}_{x=0}R_{01}\ge229,\qquad
\operatorname{ord}_{x=0}R_{23}\ge259.
\]

At `x=1+t`, take a constant invertible block of the exact rational
Sylvester matrix and form its Schur complement in `Q[[t]]`. The constant
block is a unit, so its determinant does not change the local order.
Compute the complement through `t^8` by recursively solving
`A(t)X(t)=B(t)`; each coefficient equation is independently replayed.
Minimum-valuation Gaussian elimination on the small complement gives:

| Resultant | Sylvester size | Constant rank | Schur pivot orders | Exact order at x=1 |
|---|---:|---:|---|---:|
| `R_01` | 72 | 68 | `1,2,3,5` | 11 |
| `R_23` | 76 | 73 | `3,5,7` | 15 |

The finite precision is sufficient: every pivot valuation is less than 9.
For a pivot `t^v U`, the elimination ratio is known modulo `t^(9-v)`;
every pivot-row entry has valuation at least v, so multiplying the ratio
preserves each updated entry modulo `t^9`. Each recorded leading pivot
coefficient is therefore exact and nonzero. The determinant valuation is
the sum of the pivot valuations.

It follows over `Z[x]` that both resultants are divisible by the monic
polynomial

\[
D=x^{229}(x-1)^{11}.
\]

This structural divisor is established in characteristic zero before any
modular gcd is used.

## 4. Degree preservation without reconstructing the large integer resultants

The assignment-only upper degree bound for `R_01` is 2578, whereas its
modular degree is 2576. Consequently the assignment bounds alone do not
prove degree preservation. The following exact infinity correction closes
that discrepancy.

For `R_01`, reverse x by `x=1/t`, multiplying each of the 38 first
Sylvester rows by `t^40` and each of the 34 second rows by `t^38`.
The row degree sum is

\[
38\cdot40+34\cdot38=2812.
\]

Checked integer assignment duals remove total t-valuation 234, leaving a
polynomial matrix `M(t)` with

\[
\det M(t)=t^{2578}R_{01}(1/t).
\]

Exact rational arithmetic gives `rank M(0)=71`. Nonzero left and right
null vectors l and r are replayed, and

\[
\ell^T M'(0)r=0.
\]

For a 72-by-72 matrix of rank 71, its nonzero adjugate is proportional to
`r*l^T`. The determinant derivative is therefore zero, as is its constant
term. Hence `ord_t det M(t)>=2`, proving `deg R_01<=2576` over Z.

At `p=664448401`, all four integer contents are units and all chart
y-degrees are preserved. The polynomial Sylvester-resultant construction
therefore commutes with reduction. Direct exact finite-field calculation gives

\[
\deg\overline R_{01}=2576,\qquad
\deg\overline R_{23}=2742,\qquad
\gcd(\overline R_{01},\overline R_{23})=x^{229}(x-1)^{11}.
\]

The first degree matches its exact upper bound, so `deg R_01=2576` and
its leading coefficient survives reduction. The reduction lemma now yields

\[
\boxed{\gcd_{\mathbb Q[x]}(R_{01},R_{23})=x^{229}(x-1)^{11}}
\]

with monic normalization. Only one prime is needed at this last step. The
integer CRT reconstruction and the exact local/infinity calculations are the
additional hypotheses that make the lift valid.

## 5. Complex-torus zero-set and rank theorem

At any common zero of all four minors, both resultants vanish. On the
torus, `x!=0`, so their exact gcd forces `x=1`. Independent integer
univariate arithmetic gives

\[
\gcd_i P_i(1,y)=(y-1)^3.
\]

Thus `y=1`; conversely this common gcd shows that all four minors vanish
there. The independent y=1 control similarly gives `(x-1)^3`.
Therefore

\[
\boxed{V(P_0,P_1,P_2,P_3)\cap(\mathbb C^*)^2=\{(1,1)\}.}
\]

Away from that point, at least one chart has a nonzero 68-by-68 determinant,
so the interior operator has full row rank 68. At the point itself the
literal 68-by-96 rational matrix has exact rank 65. This checks that the
surviving zero is a genuine interior rank drop.

## 6. Replay and frontier

From the repository root, after installing `requirements.txt`:

```bash
python 02_REGISTRY/research/certificates/a4d_y_curved_joint_two_ratio_integer_minors_check.py
python 02_REGISTRY/research/certificates/a4d_y_curved_joint_two_ratio_charzero_check.py
```

The second certificate consumes the first owner's pinned full ledgers and
replays the exact local, infinity, finite-field, fiber, and rank checks.
The reconstruction owner also calls the same verifier on its freshly
computed ledgers in memory. Its former two-pair selection is diagnostic:
only pair `(0,3)` attains both assignment degree edges, so that selection
criterion cannot supply the required two resultants on this input.
Its terminal is
`A4D-Y-CURVED-JOINT-TWO-RATIO-CHARACTERISTIC-ZERO-ELIMINATION-CERTIFIED`.

The next linear algebraic frontier is the genuine three-ratio interior
locus together with the remaining boundary rows. A proof there must still
be converted into the relevant quantitative transverse bound. The physical
reduced Y-center equation on curved sampled metrics and the uniform relative
remainder after `h^-2` normalization remain separate open obligations.
PR #310 remains Draft / IN_PROGRESS.
