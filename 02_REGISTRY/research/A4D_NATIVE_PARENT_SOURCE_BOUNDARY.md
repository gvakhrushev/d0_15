# Existing mixed parent: full source, indefinite radical and approximate roots

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, PR #310.
Input: `8b96338505395dabf509e13422089d89685483b8`.
Status: **scoped owner/source classification; physical matter, positive GR
and global closure remain OPEN**. No native action or constraint is added.

The earlier [homogeneous-parent result](A4D_NATIVE_AFFINE_PROBE_NOGO.md#8-a-second-existing-owner-homogeneous-mixed-parent-stationary-values)
proved zero stationary action values, while retaining a genuine nonzero
pointwise-source counterexample. This continuation resolves that distinction
for the actual supplied linear pairing: a positive scalar form annihilates
the entire pointwise source at every full field root. For invertible
indefinite forms, the remaining field roots and their source relation are
classified by an explicit image radical. Small full Euler residuals give a
quantitative source bound under stated uniform hypotheses; those hypotheses
are not inferred from a Hodge name or a native preparation not yet built.

## 1. Literal owner and independently defined field equations

The actual definition in
[`FinitePrimalDualHodgeParent.lean`](../../03_FORMALIZATION/D0/Geometry/FinitePrimalDualHodgeParent.lean)
is

\[
 B(\psi,\chi,\lambda)=\tfrac12\langle\chi,S_0\chi\rangle
        +\langle\lambda,S_0\chi-d_D S_1d_P\psi\rangle.
\]

Its supplied pairing is a function; bilinearity is not enforced by its type.
Here the declared class is a real bilinear pairing
\(\langle x,y\rangle=x^T R y\), with no injectivity assumed for the
possibly rectangular matrix \(R\). Set

\[
 M=R S_0,\qquad K=R d_D S_1d_P,
 \qquad F=\tfrac12\chi^T M\chi+\lambda^T(M\chi-K\psi).       \tag{1}
\]

This is an exact rewriting of the existing action for every choice of the
four supplied operators and the pairing, proved by `literal_owner_binding`.
All three fields belong to the same finite primal scalar space. The geometry
dependence of all inputs may be nonlinear. No physical metric law is selected.

For the class **\(M=M^T\)**, actual independent field differentiation gives

\[
 r_\psi=-K^T\lambda,\qquad r_\chi=M(\chi+\lambda),
 \qquad r_\lambda=M\chi-K\psi.                              \tag{2}
\]

`FullFieldGate` is defined by vanishing derivatives of (1) in every direction
of each of the three fields. The Lean capsule proves the exact affine or
quadratic variation polynomials, their `HasDerivAt` statements and equivalence
with (2). It does not put the desired constitutive response into the gate.

The last equation enforces the **visible** constraint
\(R(S_0\chi-d_D S_1d_P\psi)=0\). Injectivity of \(R\) implies the raw
constraint; that additional implication is separately compiled. Without it,
\(R=(1,0),S_0=(1,0)^T,d_DS_1d_P=(0,1)^T\) and
\((\psi,\chi,\lambda)=(1,0,0)\) satisfy the full visible gate but have
nonzero raw constraint. A degenerate pairing cannot be silently repaired.

## 2. Complete positive-form source theorem

For any positive definite symmetric \(M\) and any \(K\), in any finite
dimension,

\[
 (r_\psi,r_\chi,r_\lambda)=0
 \quad\Longleftrightarrow\quad
 \chi=\lambda=0,\quad K\psi=0.                              \tag{3}
\]

Indeed, \(r_\chi=0\) gives \(\lambda=-\chi\). The other two equations
then give \(\chi^TM\chi=\chi^TK\psi=0\), hence \(\chi=0\);
the converse follows by substitution. No inverse of \(K\), uniqueness of
\(\psi\), ellipticity of \(K\), or gauge interpretation of its kernel is
used. Nonzero kernel fields remain allowed.

For arbitrary constitutive variations \(U=\delta M,V=\delta K\), the
literal fixed-field derivative of (1) is

\[
 \sigma(U,V)=\tfrac12\chi^TU\chi+\lambda^T(U\chi-V\psi).
                                                                    \tag{4}
\]

Thus **every full root in (3) has \(\sigma(U,V)=0\) for all \(U,V\)**.
This is the pointwise covector, not an inference from zero stationary values
or from a differentiable choice of roots. Changes of the pairing, both
stars, and both differentials are included by their actual contributions to
\(U,V\). Pullback by any differentiable proposed geometry map is also zero.
A positive normalization of the counting pairing changes none of this.

The actual scalar formula
[`hodgeMetricMeasureWeight 0 mu 1 = mu`](../../03_FORMALIZATION/D0/Geometry/ArchiveMetricMeasureHodgeLift.lean)
gives a positive diagonal form when \(\mu>0\); its positivity is compiled.
It meets (3) **if the supplied composition \(R S_0\) is that form**.
This conditional binding is not an already constructed physical star.
In particular, `archive_weighted_hodge_dirac_owner` currently states only
the degree count, cell-type count, `DegreePreservingLaplacian true` and Role
count. Its printed proposition does not construct a weighted operator.

Negative definite symmetric \(M\) gives the same root conclusion by replacing
\((M,K,F)\) with \((-M,-K,-F)\). Indefinite and semidefinite forms require
separate analysis. Adding a field constraint or another coupled action changes
(2); neither is installed by this theorem.

## 3. Invertible indefinite form: exact kernel and source relation

For arbitrary invertible symmetric \(M\), define
\(Q=K^T M^{-1}K\). The complete full root set is

\[
 \psi\in\ker Q,\qquad \chi=M^{-1}K\psi,\qquad\lambda=-\chi,
 \qquad \sigma(U,V)=-\tfrac12\chi^TU\chi+\chi^TV\psi.       \tag{5}
\]

The capsule proves both the root equivalence and the response formula for
all finite dimensions. The reduced condition is expressed there as its
pairing with every test vector, so it does not assume an inverse of \(Q\).

The full Hessian in the ordered variables \((\psi,\chi,\lambda)\) is

\[
 H=\begin{pmatrix}0&0&-K^T\\0&M&M\\-K&M&0\end{pmatrix},
 \qquad\operatorname{rank}H=2n+\operatorname{rank}Q.          \tag{6}
\]

To verify completeness, substitute the invertible change of coordinates
\(\chi=M^{-1}K\psi+u,\lambda=-M^{-1}K\psi+v\) into (1):

\[
 F=\tfrac12\psi^TQ\psi+\tfrac12u^TMu+v^TMu.                \tag{7}
\]

The last two fields have an invertible \(2n\)-dimensional block, proving
(6) as well as (5). This is algebraic elimination of existing variables,
not a new action principle.

Let \(S=\operatorname{im}K\), with restricted symmetric form
\(b(s,t)=s^TM^{-1}t\). The map \([\psi]\mapsto K\psi\) gives

\[
 \ker Q/\ker K\simeq\operatorname{rad}(b|_S),\qquad
 \dim\operatorname{rad}(b|_S)=\operatorname{rank}K-
                                      \operatorname{rank}Q.           \tag{8}
\]

Proof: \(Q\psi=0\) is exactly \(b(K\psi,Kv)=0\) for all \(v\).
Every element of the radical has a preimage under \(K\), and the kernel
of this restricted map is \(\ker K\). Rank-nullity proves the dimension
formula. This is an all-size analytic proof, with six exact finite strata
as controls; the quotient-dimension formula itself is not claimed as compiled.

Fields in \(\ker K\) always have zero source. A nonzero quotient class has
\(\chi\ne0\) and can be detected by the independent direction
\(U=I,V=0\), whose response is \(-\|\chi\|^2/2\). This detection
equivalence is compiled. Whether a physical metric map admits that independent
direction is a separate obligation. A radical direction is not called gauge.

## 4. Nonzero source and continuation are distinct

Retain the earlier exact counterexample:

\[
 M=\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad
 K(q)=\begin{pmatrix}0&q\\q&1\end{pmatrix},\quad
 \psi=e_1,\ \chi=e_0,\ \lambda=-e_0.
\]

At \(q=0\) all three Euler vectors vanish, \(F=0\), but
\(\partial_q F=1\). Direct calculation gives

\[
 Q(q)=\begin{pmatrix}0&q^2\\q^2&2q\end{pmatrix},
 \qquad\det Q(q)=-q^4.                                    \tag{9}
\]

For every \(q\ne0\) the only full root is the zero triple. Thus this
nonzero-source root has no continuous full-root continuation to neighboring
backgrounds. In contrast, \(K(q)=\operatorname{diag}(0,1+q)\) with the same
\(M\) has roots \(\psi=e_1,\chi=(1+q)e_0,\lambda=-\chi\), and its
tangential constitutive response vanishes identically.

There is a useful general analytic reason. Let a finite symmetric quadratic
Hessian \(H(q)\) be differentiable at zero, and suppose exact critical
roots \(z(q)\to z_0\) exist along nonzero \(q\to0\), with
\(H(0)z_0=H(q)z(q)=0\). Then

\[
 0=z_0^T\frac{H(q)-H(0)}qz(q)\longrightarrow z_0^TH'(0)z_0.
                                                                    \tag{10}
\]

The equality uses symmetry of \(H(0)\); no derivative of \(z(q)\) is
needed. `continuous_critical_root_source` compiles this argument for a
continuous root family on a punctured neighborhood, using the actual
entrywise `HasDerivAt` hypotheses, symmetry and kernel equations. The
displayed elementary limit also applies along a convergent root sequence.
Consequently the fixed-field quadratic source in that direction is
zero. This proves an obstruction to continuous transport of a given
nonzero-source root, not the absence of every indefinite root. It applies
to the full Hessian (6) at fixed finite size. It does not imply a uniform
refinement estimate or exclude roots that escape to infinity. Restricting
the admitted background directions also restricts what (10) tests.

For a differentiable symmetric finite Hessian with locally constant rank,
every kernel vector has such a continuous continuation. An explicit local
proof chooses an invertible principal block \(A\) of size equal to the
rank and writes \(H=\left(\begin{smallmatrix}A&B\\B^T&D\end{smallmatrix}\right)\).
Such a block exists by symmetric elimination: use a nonzero diagonal pivot,
or, if all diagonal entries vanish, a nonzero off-diagonal two-by-two pivot,
then continue on the symmetric Schur complement.
Constant rank forces \(D-B^TA^{-1}B=0\). Keeping the lower coordinates
\(v\) fixed gives the continuous kernel vector
\((-A^{-1}Bv,v)\) through any prescribed root. Rank zero is immediate.
Thus a nonzero source of a full homogeneous quadratic root requires failure
of locally constant Hessian rank in a detecting background direction. For
(6) this is a rank-change obstruction in \(Q\). This corollary is finite
linear algebra, not a uniform range estimate. A joint physical system could
still live on a lower-dimensional background locus, or have rank-change loci
that depend on refinement; neither possibility is excluded here.

## 5. Quantitative source bound for approximate full roots

Use matching Euclidean block norms and suppose

\[
 M\ge mI>0,\quad \|(\psi,\chi,\lambda)\|\le Z,
 \quad\|(r_\psi,r_\chi,r_\lambda)\|\le R.
\]

The exact Euler balance, compiled before imposing any gate, is

\[
 \chi^TM\chi=\chi^Tr_\chi-\lambda^Tr_\lambda+\psi^Tr_\psi.
                                                                    \tag{11}
\]

Cauchy--Schwarz and \(M(\chi+\lambda)=r_\chi\) imply

\[
 \|\chi\|\le a:=\sqrt{ZR/m},\qquad
 \|\lambda\|\le b:=a+R/m,
\]

and (4) gives the dimension-independent estimate

\[
 |\sigma(U,V)|\le (a^2/2+ab)\|U\|+bZ\|V\|.               \tag{12}
\]

For uniformly positive \(m\), bounded \(Z,\|U\|,\|V\|\) and
\(R\to0\), this is \(O(\sqrt R)\). No range inverse of \(K\) is
needed. Matching normalized lattice inner products work as well, after the
same normalization is applied to the action, residuals and dual norms.
The actual native preparation must supply these uniform bounds. A scaled
differential can make \(\|V\|\) grow, so a pointwise residual assertion
alone is insufficient.

The exponent is sharp in this declared class: in dimension one take
\(M=1,K=h,\psi=1,\chi=h,\lambda=-h\). Then
\(r=(h^2,0,0)\), \(\sigma(0,1)=h\), with uniformly bounded fields.
The exact controls also retain three failures:

| Missing uniform hypothesis | Data as \(h\to0\) | Residual / response |
|---|---|---|
| Coercivity | \(M=K=h^2,(\psi,\chi,\lambda)=(1,1,-1)\) | \(r=(h^2,0,0),\ \sigma(0,1)=1\) |
| Field bound | \(M=1,K=h^2,(\psi,\chi,\lambda)=(h^{-2},1,-1)\) | \(r=(h^2,0,0),\ \sigma(0,1)=h^{-2}\) |
| Variation bound | Sharp example above, \(V=h^{-1}\) | \(r=(h^2,0,0),\ \sigma(0,V)=1\) |

The older homogeneous identity still independently bounds
\(|F|\le ZR/2\), even for indefinite forms. Its completed-contrast error
and the pointwise source error (12) are different estimates. Neither proves
the requested native-to-Einstein contrast transfer.

## 6. Verification and remaining physical arrow

The [Lean capsule](certificates/a4d_native_parent_source.lean) prints 16
propositions' transitive axioms and seven actual types, with only `propext`,
`Classical.choice`, `Quot.sound`. Its
[output](certificates/a4d_native_parent_source_output.txt) and
[receipt](certificates/a4d_native_parent_source_results.json) pin 12 D0
source files plus the toolchain inputs. Generic statements are separated
above from the all-size manual linear algebra and analytic estimate (12).

The [checker](certificates/a4d_native_parent_source_check.py) and
[immutable ledger](certificates/a4d_native_parent_source_certificate.json)
have 45 grouped exact controls: all three field gradients, full constitutive
variation, symmetric off-diagonal packing, literal rectangular pairing,
elimination, six complete Hessian/radical strata, both indefinite transport
examples, the sharp exponent and missing-hypothesis controls. They also
protect semidefinite forms, normalized constraints, degenerate pairing and
auxiliary-only gates. The default replay does not rewrite expected output:

```bash
python3 02_REGISTRY/research/certificates/a4d_native_parent_source_check.py
```

Changing the ledger's zero positive-form source or its residual exponent is
rejected. These controls do not certify all 24 A4D connection equations or
ten physical metric equations for an unspecified map. Those equations still
belong to the existing finite-probe construction and the open realization
arrow. A real source for GR must be derived from an independently owned
physical sector and its full coupled variations, with a same-carrier metric
map, Ward identity and refining solutions. The present theorem closes this
parent's declared source cases and retains its genuine indefinite exception;
it does not close that physical arrow or the original #310 terminal.
