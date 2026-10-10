# Existing mixed parent: full source, field-frame universality and transverse seed boundary

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, PR #310.
Initial source classification: `8b96338505395dabf509e13422089d89685483b8`.
Field-frame continuation input: `41ae2916bd1676c45209ea7f347e084c31ae7f09`.
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

## 6. Complete field-frame class: full background source and joint roots

This section resolves a physical-consumer question left by the complete
[flat transport classification](A4D_NATIVE_DYNAMICAL_OWNERSHIP.md#6-complete-flat-translation-lift-family-including-its-stabilizer):
when does changing the representation of the fields change the background
equations? The result applies on **any differentiable background domain**,
including independent coframe and link directions. It does not require that
the background lie on the flat translation orbit. Its complete declared
class consists of invertible linear reparametrizations of one fixed family
of the existing mixed-parent action. It does not classify all D0 actions.

### 6.1 Literal transport of every supplied owner slot

Let the background be \(b\), and let \(Q_0(b),Q_1(b),T_3(b),T_4(b)\)
be invertible maps on the four finite owner slots. Write \(Q=Q_0\),
\(P=Q^{-1}\). Transform the existing data by

\[
\begin{aligned}
 d'_P&=Q_1d_PP,&d'_D&=T_4d_DT_3^{-1},\\
 S'_0&=T_4S_0P,&S'_1&=T_3S_1Q_1^{-1},&R'&=P^TRT_4^{-1}.
\end{aligned}                                                       \tag{13}
\]

Multiplying the actual owner compositions gives, with no inverse of a star,
no positive-definiteness assumption, and possibly rectangular \(R\),

\[
 M'=R'S'_0=P^TMP,\qquad
 K'=R'd'_DS'_1d'_P=P^TKP.                                      \tag{14}
\]

Thus all intermediate frame choices cancel. The Lean definitions
`reframeData`, `reframePairing` and theorem `reframed_visible_operators`
establish (13)–(14) for the literal `FinitePrimalDualHodgeData` in every
finite dimension. `literal_reframed_owner` proves

\[
 F(M',K';Q\psi,Q\chi,Q\lambda)=F(M,K;\psi,\chi,\lambda).       \tag{15}
\]

This is a change of coordinates in an existing action. It does not install
(13) as a new native transport or assert its physical admissibility. If a
native pairing is fixed, (13) is admissible only when its transformed
pairing coincides with that fixed pairing, or an existing rule admits its
transformation. Holding an arbitrary \(R\) fixed can break (15).

### 6.2 Complete field roots and the off-shell source defect

At corresponding field states \(z'=(Q\psi,Q\chi,Q\lambda)\), the three
actual Euler covectors obey \(r'_i=P^T r_i\). Equivalently, their values on
an arbitrary test \(v'\) equal the old covectors on \(Pv'\). Invertibility
therefore gives a bijection of **all full field roots**. This is compiled
as `full_gate_congruence` using `FullFieldGate`, which was defined by the
three independent derivatives before any source assertion. Symmetric
\(M\) may be positive, indefinite or singular.

For any background tangent \(v\), put

\[
 U=D_bM[v],\quad V=D_bK[v],\quad A=P\,D_bQ[v].
\]

Differentiating \(QP=1\) gives \(D_bP[v]=-AP\), so the actual fixed-new-field
operator derivatives are

\[
 D_bM'[v]=P^T(U-A^TM-MA)P,\quad
 D_bK'[v]=P^T(V-A^TK-KA)P.                                    \tag{16}
\]

Substitution into (4), retaining all three field residuals, gives the exact
off-shell identity

\[
 \boxed{\sigma'_v(z')-\sigma_v(z)=
   -r_\psi^TA\psi-r_\chi^TA\chi-r_\lambda^TA\lambda.}          \tag{17}
\]

Proof: the first new kinetic term is
\(-\tfrac12\chi^T(A^TM+MA)\chi=-(A\chi)^TM\chi\), since \(M\)
is symmetric. The remaining terms are
\(-\lambda^TA^TM\chi-\lambda^TMA\chi+
\lambda^TA^TK\psi+\lambda^TKA\psi\). Grouping them with (2)
gives exactly (17), including its minus signs. The generic Lean theorem
`frame_off_shell_defect` proves this equality; `response_congruence`
handles arbitrary frame values, not only \(Q=1\).

The source is an actual background derivative. In addition to the earlier
`constitutive_first_variation`, `simultaneous_background_first_variation`
compiles the derivative of the literal parent under simultaneous operator
and field variations. In (16), taking the old-coordinate field variation
\((-A\psi,-A\chi,-A\lambda)\) recovers (17). General differentiable
\(Q(b)\) uses the ordinary finite-dimensional chain rule and the explicitly
derived inverse derivative above; that analytic passage is not claimed as
a separately compiled global calculus theorem.

### 6.3 All background equations, not only a Ward direction

On the full field gate, (17) implies

\[
                     \sigma'_v(z')=\sigma_v(z)\quad\text{for every }v.\tag{18}
\]

The quantifier includes all independent admitted coframe, connection and
other background variations. It does not come from a divergence identity
or from checking only gauge directions. `full_gate_background_source`
is the compiled pointwise statement. Thus no extra contribution to the
source can be obtained solely from the background derivative of a field
frame. No smooth choice of roots as \(b\) varies is needed for this result;
isolated indefinite full roots are included.

For the **same** geometric action \(G(b)\), combine the full matter gate
with the independently derived equations
\(D_bG[v]+\sigma_v=0\) for every admitted \(v\). The map
\((b,z)\mapsto(b,Q(b)z)\) bijects the complete joint root sets. Its
projection to background states is identical. This is the content of
`joint_gate_frame_equivalence`, which takes the actual geometric derivative
as a fixed input; it neither assumes matter-response vanishing nor invents
a native gate. If the metric readout is an unchanged function of \(b\),
the projected metric solution set and its source are the same.

**Complete fixed-seed corollary.** If the seed operators \(M,K\) are
independent of the background and all its dependence is the field-frame
transport (13), then \(U=V=0\). Equation (18) gives zero source in **every**
background direction at every full field root. This is compiled as
`transported_fixed_seed_source_zero`, with no positivity or invertibility
of \(M\). The full matter gate therefore contributes no background Euler
condition beyond those of the unchanged geometric action. In the standalone
parent, every admitted background has at least its zero-field joint root;
this family cannot select Einstein backgrounds. This is a complete conclusion
for the fixed-seed field-frame class, not all nonlinear constitutive laws,
additional action terms or constrained native matter sectors.

Equation (15) also makes the action difference between any two corresponding
endpoint states exactly equal, even off shell and even with different
frames at the endpoints. `corresponding_endpoint_contrast` proves this
finite identity. A probe with fields held fixed in the new coordinates
need not hold them fixed in the old coordinates. Equality for corresponding
states does not prove the native-to-Einstein contrast estimate or manufacture
an admitted probe/refinement map.

For two transport presentations with a common seed action and corresponding
isotropy data, an intertwiner which reparametrizes **all** fields, four
operators, pairing and constraints as above contributes no new background
Euler equation on the full matter gate. Hence this frame freedom in the
action presentation disappears from the joint background equations. It is
not a proof that every transport/intertwiner is an owned physical gauge or
that all free native actions have the same physical operators.

### 6.4 Approximate roots and the required uniform estimate

In matching Euclidean block norms, (17) gives

\[
 |\sigma'_v-\sigma_v|
 \le \|r\|\,\|\operatorname{diag}(A,A,A)z\|
 \le \|A\|\,\|r\|\,\|z\|.                                  \tag{19}
\]

This is Cauchy–Schwarz and the operator norm inequality; positivity and an
inverse of \(M\) are unnecessary. Normalized lattice norms require the
same normalization on action and residual covectors. To replace the norms
in (19) by new-frame norms uniformly in \(h\), bounds on \(Q_h,P_h\)
are also needed. None is supplied by pointwise invertibility.

The missing logarithmic-derivative bound is a real obstruction: take
\(M=1,K=h,z=(1,h,-h)\), and the smooth everywhere invertible scalar frame
\(Q_h(q)=\exp(q/h^2)\). At \(q=0\), \(Q_h=1\),
\(r=(h^2,0,0)\to0\), fields are bounded, and \(A_h=h^{-2}\).
With seed background derivatives zero, (17) gives
\(\sigma'_q-\sigma_q=-1\). Thus vanishing residuals and bounded frame
values at a point do not imply convergence of the source. The exact checker
reproduces the sign and the sharp contraction in (19). This bound is an
analytic finite-dimensional estimate, not a compiled uniform refinement
theorem.

### 6.5 What remains physically significant, with an exact control

A transverse constitutive law is not determined by (13). Two fixed seed
families can have the same values and the same complete field root at one
background while having distinct background Euler covectors there. Take

\[
 M=\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad
 K_a(q)=\begin{pmatrix}0&0\\0&1\end{pmatrix},\quad
 K_b(q)=\begin{pmatrix}0&q\\q&1\end{pmatrix},\quad
 \psi=(0,1)^T,\quad\chi=(1,0)^T,\quad\lambda=-\chi.
\]

At \(q=0\), both actions have exactly the same \(M,K,z\) and all three
field residuals vanish. But \(\sigma_a(\partial_q)=0\) and
\(\sigma_b(\partial_q)=1\). Every smooth invertible field frame leaves
this difference equal to one, by (18). For a common geometric derivative
zero, this particular full matter root is a joint background root only in
the first family. The second family has the rank-change feature already
classified in Section 4; no smooth family of its nonzero roots is assumed.

These are realizations of the **supplied-data parent interface**, for example
\(R=d_P=d_D=1,S_0=M,S_1=K\) on equal two-dimensional slots. They are exact
controls on input sufficiency, not two asserted physical D0 matter theories.
The parameter \(q\) has not been identified with an owned transverse metric
variation. If one wants that physical identification, its native map and
admission theorem must first be supplied. Consequently this result distinguishes
Euler families at the interface and does not assert physical D0 nonuniqueness.

The controls additionally retain:

* A noninvertible frame can create spurious full roots.
* Omitting the field equation leaves a nonzero defect even if both auxiliary
  equations hold.
* An external term \(-J^T\psi\) must become \(-(P^TJ)^T\psi'\);
  keeping the same numerical \(J\) is generally a different problem. Its
  background variation must also be included when \(P\) varies.
* A norm constraint must become \(\|P\psi'\|=1\), including its background
  derivative and multiplier terms; it cannot silently remain \(\|\psi'\|=1\).
* A physical field readout and a refinement map require their own commuting
  diagrams. Replacing a refinement map by \(Q_H R_{hH}P_h\) gives algebraic
  conjugacy, but does not prove that this replacement is native-admissible.

**Next unresolved proposition:** derive the transverse seed operators,
geometric action, full independent variations and admissible refinement from
native ownership, or classify a complete native family and test its remaining
Euler/physical parameters. Repeating the choice of \(U\) or its Hessian as
a field-frame representation cannot supply that missing law. The positive
form source theorem, the indefinite rank-change exception, the original
fixed-source/raw-owner #310 problem, and the independent #202/#317 terminals
all retain their stated scope and status.

## 7. Verification and remaining physical arrow

The [Lean capsule](certificates/a4d_native_parent_source.lean) prints 32
propositions' transitive axioms and 18 actual types, with only `propext`,
`Classical.choice`, `Quot.sound`. Its
[output](certificates/a4d_native_parent_source_output.txt) and
[receipt](certificates/a4d_native_parent_source_results.json) pin 12 D0
source files plus the toolchain inputs. Generic statements are separated
above from the all-size manual linear algebra and analytic estimate (12).

The [checker](certificates/a4d_native_parent_source_check.py) and
[immutable ledger](certificates/a4d_native_parent_source_certificate.json)
have 75 grouped exact controls: all three field gradients, full constitutive
variation, symmetric off-diagonal packing, literal rectangular pairing,
elimination, six complete Hessian/radical strata, both indefinite transport
examples, the sharp exponent and missing-hypothesis controls. They also
protect semidefinite forms, normalized constraints, degenerate pairing and
auxiliary-only gates. The 30 new controls bind arbitrary frame values, all
four owner slots, every field equation, the source defect, endpoint contrasts,
34 independent background jets (10 plus 24 abstract coordinates), the mesh
counterexample and transformed constraints. These coordinate controls do not
assert a constructed physical metric/connection map. The default replay does not rewrite expected output:

```bash
python3 02_REGISTRY/research/certificates/a4d_native_parent_source_check.py
```

Seventeen hostile ledger changes are rejected: the two earlier source/exponent
controls plus fifteen changes erasing the full gate, frame scope, constraint
transformation, residual bound hypotheses or open physical obligations. These controls do not certify all 24 A4D connection equations or
ten physical metric equations for an unspecified map. Those equations still
belong to the existing finite-probe construction and the open realization
arrow. A real source for GR must be derived from an independently owned
physical sector and its full coupled variations, with a same-carrier metric
map, Ward identity and refining solutions. The present theorem closes this
parent's declared source cases and retains its genuine indefinite exception;
it does not close that physical arrow or the original #310 terminal.
