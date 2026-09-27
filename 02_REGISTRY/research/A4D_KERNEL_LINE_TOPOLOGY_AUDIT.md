# A4D — kernel-line topology audit after FUGU synthesis v8

Status: CONTROL synthesis / topology audit. No claim or BOOK promotion.

## 1. Exact algebraic frame

Let

\[
d_r(z)=z_r^{-1}-1,\qquad q_0(z)=\operatorname{vec}_{sym}(d(z)d(z)^T),
\qquad C(z)=H_{AQ}(z).
\]

Merged owner #270 proves, pointwise for every nontrivial character d != 0,

\[
\ker C(z)=\mathbb C\,q_0(z),\qquad \operatorname{rank}C(z)=9.
\]

The proof is not generic-rank sampling: it covers projective d-space by four
charts and certifies 9x9 minors whose ideal is the unit ideal. Therefore there
is no exceptional nonzero rank-drop stratum of C.

At the trivial character z=(1,1,1,1), d=0 and C=0 exactly.

Open PR #282 supplies stronger exact-unmerged evidence:
\[
C(d)=\sum_{r=0}^3 d_r C_r
\]
over Q, with zero constant/higher coefficients and all 480 cubic scalar
coefficients of C(d)q_0(d) equal to zero. Until #282 merges, this coefficient
ledger is not main owner truth.

## 2. Relative-character reading

Per role,

\[
d_r=\chi_{-1}(z_r)-\chi_0(z_r)=z_r^{-1}-1.
\]

On the unit torus z_r=e^{i\theta_r},

\[
d_r=-2i\,e^{-i\theta_r/2}\sin(\theta_r/2).
\]

This is a useful half-angle factorization, but d_r is single-valued on the
original torus: both half-angle factors change sign under theta -> theta+2pi.

Thus q_0 is the symmetric square of the relative-character vector d. This is
an algebraic statement; it does not by itself establish a physical spin
structure.

## 3. The actual line-bundle theorem

Define the nontrivial-character base

\[
X=\{z\in(\mathbb C^\times)^4:\ d(z)\neq0\}.
\]

Because #270 gives constant kernel dimension one on X, the kernels define a
holomorphic line subbundle

\[
L=\ker C\longrightarrow X.
\]

The section q_0 is holomorphic and nowhere zero on X. Hence

\[
\boxed{L\cong X\times\mathbb C}
\]

as a holomorphic line bundle, with q_0 as a global frame. In particular,

\[
c_1(L)=0.
\]

This conclusion is stronger than an orbit-by-orbit statement and is already
supported by merged #270; it does not require the coefficient ledger of #282.

## 4. What triviality does NOT imply

The following implications are invalid without additional structure:

1. c_1(L)=0 does not imply that every connection on L has zero curvature.
   A trivial line bundle can carry nonflat connections.

2. A global frame does not make the trivialization unique up to sign.
   Any nowhere-zero holomorphic scalar function f(z) gives another frame
   f(z)q_0(z).

3. Triviality of L does not prove equality of metric response on different
   stationary connection branches. That is an envelope / reduced-action
   statement, not a line-bundle theorem.

4. A Berry-type connection obtained by normalizing q_0 requires an additional
   Hermitian structure and a specified projection rule. Its curvature, if
   nonzero, is connection-dependent even though c_1(L)=0.

Therefore frozen G is not declared a gauge artifact merely from c_1(L)=0.
Merged #270/#278 instead close the specific frozen-detune interpretation by
the exact moving-section product rule / same-carrier transport.

## 5. Coordinate hyperplanes are not a discriminant of C

Let

\[
D_r=\{z\in X:\ d_r=0\}=\{z\in X:\ z_r=1\}.
\]

Because #270 proves rank C=9 for every d != 0, L extends smoothly and
holomorphically across every D_r. q_0 may lose some coordinate entries there,
but q_0 itself remains nonzero whenever at least one other d_s is nonzero.

Hence

\[
\bigcup_r D_r
\]

is NOT the rank-jump divisor of C.

The only degeneration of the metric-null line owned by #270 occurs at d=0,
where all four components vanish simultaneously and C=0.

This corrects the earlier candidate-divisor language in the FUGU synthesis.

## 6. Consequence for monodromy proposals

A loop encircling one coordinate hypersurface D_r while the other d_s stay
nonzero is not encircling a singularity of L. The loop can be contracted
through D_r inside X because the bundle and its global frame extend there.

Therefore there is no topologically forced monodromy of the kernel line around
a single z_r=1 hypersurface.

A connection-dependent holonomy can still be defined after choosing an
actual connection on L, but:
- it is not determined by c_1(L)=0;
- it is not quantized merely by winding around D_r;
- it cannot be called physical stress until its relation to the Euler system
  is proved.

Thus the hypothesis "stress equals monodromy of normalized q_0 around
z_r=1" is rejected in this literal line-bundle form.

## 7. Re-typing the three live sectors

### Metric-null germ

This is L=ker C on X. It is globally trivial and same-carrier transport is
owned. Open #278 additionally gives exact-unmerged cross-carrier residuals
8/5 and 2, but proves that the actual same-carrier moving germ has zero class
in that physical cokernel.

These residuals are carrier-mismatch diagnostics, not monodromy of L.

### Shear / #240 / #279

The shear response defect is a defect of a JOINT symbol under a changed solder
and nonlinear realizability problem. It is not caused by a rank jump of C at
d_r=0, because no such rank jump exists.

Any relation between the shear carrier and coordinate-zero patterns must be a
separate transfer theorem in the extended joint stationary system.

### #232 / Y / N0

This is a connection-only or joint-cokernel sector. It is outside the kernel
line topology from the start. Its nonlinear response question belongs to the
reduced-action / Ward programme.

Quarter-wave points are therefore not a third stratum of L. They may be
special strata of an EXTENDED joint operator, but that discriminant must be
defined separately.

## 8. IR statement: exact-point decoupling versus leading response

At the exact trivial character,

\[
C(1,1,1,1)=0.
\]

This is merged owner truth, not merely a hypothesis.

But "C=0 at the point" must not be promoted to "no IR gravitational
response". The same #270 owner computes the leading Schur elimination near
the trivial character and obtains the Einstein seed at order h^2 after the
regular connection block is eliminated.

Thus the correct statement is:

- exact mixed metric-connection Hessian coupling vanishes at z=1;
- its first derivatives in character generate a nontrivial O(h^2) Schur
  metric operator;
- after h^-2 normalization that leading operator is the designated
  -1/2 Einstein response.

So IR safety is not absence of coupling to all orders; it is controlled
vanishing plus a certified leading Schur limit.

## 9. Where a genuine topological/holonomy obstruction could live

If a monodromy or holonomy mechanism remains desirable, the candidate bundle
must be richer than L=ker C. Possible typed objects are:

1. the solution bundle/projection of the nonlinear stationary variety
   Sigma -> (Q,z) after regular variables are eliminated;
2. a cokernel line of the PHYSICAL joint operator [A(z)|C(conj z)] on a
   constant-corank locus, after proving it forms a bundle;
3. the reduced-action variational cohomology class
   D_Q L_red modulo the Euler ideal plus lattice divergences, owned as the
   mechanism-level target by the merged reduced-action Ward synthesis.

Each candidate requires its own connection/projection before "holonomy" has a
well-defined meaning.

## 10. Updated forward programme

A. Merge/pin #282 so the affine coefficient ledger becomes main owner truth.

B. Do not spend a worker proving rank stratification of C: #270 already proves
there is NO nonzero rank-drop locus.

C. Replace the old divisor-transfer question by an EXTENDED-JOINT
stratification: determine constant-corank loci of the physical/joint operator
relevant to #240/#232/#278, with carriers kept typed.

D. Continue the merged #287 reduced-action programme: reconstruct one common
coupled action for shear u and N0/Y amplitude v, then test

\[
D_Q\mathcal L_{\rm red}
\in
\langle E_u,E_v,\ldots\rangle+\operatorname{Div}.
\]

E. Only if an extended joint cokernel/solution bundle has a canonically owned
connection should a holonomy invariant be computed.

## 11. Status firewall

OWNED on main:
- q_0=dd^T spans ker C for every d != 0;
- rank C=9 for every d != 0, with no exceptional nonzero rank-drop;
- C=0 at d=0;
- moving-section transport identity;
- leading IR Schur-Einstein weld.

EXACT but unmerged:
- #282 coefficientwise affine decomposition and 480 cubic zero checks;
- #278 raw cross-carrier residual squares 8/5 and 2 plus same-carrier
  absorption.

VALID CONSEQUENCE:
- ker C is a holomorphically trivial line bundle on X;
- c_1(ker C)=0;
- coordinate hyperplanes d_r=0 are not singular strata of this line bundle.

NOT VALID FROM THESE FACTS:
- frozen G is gauge solely because c_1=0;
- uniqueness of stationary response from line-bundle triviality;
- topologically forced monodromy around one d_r=0 hypersurface;
- stress quantization by that monodromy;
- quarter-wave/Y as a stratum of ker C.

The durable nonlinear stress target remains the reduced-action Ward/cohomology
mechanism, or an explicitly defined extended-joint cokernel/solution-bundle
obstruction.
