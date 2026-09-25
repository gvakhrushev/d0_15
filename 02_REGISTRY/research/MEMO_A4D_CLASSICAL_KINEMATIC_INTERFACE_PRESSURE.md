# A4D classical kinematic interface under pressure

**Task:** `EXP-A4D-CLASSICAL-KINEMATIC-INTERFACE-PRESSURE`

**Research PR:** #128

**Start baseline:** `bfc90bff3c176ee998562dbaf7821b41858388bc`

**Terminal:** `CLASSICAL-KINEMATIC-INTERFACE-PASSPORT-CONSTRUCTED`

**Strength:** theorem-ready finite kinematics and exact counterexamples; no new Lean source.

## 0. Verdict

The proposed three-stage picture needs correction before it is used downstream.

1. Graphification and vanishing of **all** canonical Role residuals are the same
   condition, including every degenerate rank stratum:
   \[
   M=\operatorname{im}(\mathcal SP_K)
     =\operatorname{span}\{R_r:r\in\mathrm{Role}\}.
   \]
2. Full affine-increment rank is an identifiability condition. It is sufficient
   for graphification, but unnecessary for every formula in the audited
   sourced-diagonal chain. It is not sufficient for endpoint descent.
3. Endpoint independence is equivalent to trivial labelled holonomy **of the
   specified transport representation**. Linear, affine, and a supplied generic
   labelled family must not be substituted for one another.
4. A graph gives a function in one direction. It need not give an inverse,
   a gauge-orbit identification, or a stable field under background variation.
5. There is an exact finite periodic counterexample in which the relation has a
   continuous constant-dimensional limit, the raw solder stays invertible, all
   affine holonomies are trivial, yet the PR #120/#123 selected mismatch jumps
   at a rank drop. The singularity is therefore **not always confined to the
   normalized graph operator**.

The minimal **pointwise active-graph plus endpoint-transport passport** is
\[
\boxed{\bigl(\forall y\;M_y=0\bigr)\ \land\ D_{\ell},}
\tag{0.1}
\]
where the positive family \(\ell\), its carrier, and the quantifiers in
\(D_{\ell}\) are supplied explicitly. This is an exact iff for the two
properties named in the passport. It is not an iff for an ordinary continuum
geometry, an intrinsic matter letter, a local action, or a stable classical
limit. Those stronger readings fail the controls below.

## 1. Provenance and ownership boundary

Read completely: the canonical brief and
`SYNTHESIS_A4D_CLASSICAL_INTERFACE_PRESSURE_PROTOCOL.md`; PR #123's memo;
`MEMO_A4D_DIAGONAL_JUNCTION_OVERLAP_LAW.md` (PR #120);
`MEMO_A4D_LABELLED_REFERENCE_SELECTION_PRINCIPLE.md` (PR #117); and the six
mandatory Lean owners/candidates listed below.

At task start #123–#126 were open. They were read at these immutable heads,
without merging their branches into this research PR:

| Input | Audited head | Literal scope |
|---|---|---|
| #123 | `3613d6a75e0761112ee6b243f898883c6970dd6e` | Research construction of the counting-labelled span primitive |
| #124 | `a1bdc87afd329189109275cdec4ebab6fb738a0c` | `A4DRegularAEPassport.lean`: restricted rational matrix reconstruction |
| #125 | `c365ed3cf3677e277040022b7f4ded2c7b0376d0` | `A4DConditionalSourcedDiagonalTransport.lean`: supplied full comparison, source and parallel residual |
| #126 | `840f6a7677481e66bfaa70621c168d7415e41dfe` | `A4DRelativeAEComparisonSpan.lean`: abstract labelled coefficient maps and canonical splitting |

Main already contains:

- `A4DLabelledPathHolonomyDescent.lean`, especially
  `labelledPathEval_factors_endpoints_iff_trivial_holonomy` and
  `labelled_L2_period_of_endpoint_descent`;
- `A4DReferenceJunctionCompressionBoundary.lean`, especially
  `referenceJunction_compress_iff` and the mixed-Role flat witness;
- `A4DRoleOverlapTwistedCocycle.lean`, especially
  `transportedReferenceMismatch_diagonal_form`;
- `ArchiveAffineCartanConnection.lean`, `ArchiveAffineExteriorLink.lean`, and
  `A4DTransportedReferenceMismatch.lean` for literal pull order, solder and
  conditional mismatch.

The #126 candidate proves a generic coefficient-space construction. It does
not by itself instantiate every archive synthesis field or prove the new
rank/continuity/quotient claims here. The #125 candidate stops at the parallel
kernel; the observer-positive selection used below is the **research** rule
in PR #120, with its explicit downstream choices. No theorem below is called
newly Lean-owned by this memo.

The regular raw-solder passport of #124 has different invertibility hypotheses
from \(\operatorname{rank}\mathcal B=4\). Neither its raw solder matrix nor
its reconstruction operator is the increment synthesis map \(\mathcal B\).

## 2. Types and quantifiers

Fix one finite archive \(X=X_N\), with four Role labels and period
\(L=\operatorname{archiveFibers}N\). Work over \(\mathbb R\). At a site \(y\),
\(E_{\rm lab}=\mathbb R^{\mathrm{Role}}\) has its counting inner product;
\(V_y\) is the four-dimensional moving output fibre. Frames act on \(V_y\),
not on the coefficient label slot.

For \(x=y-r\), use the repository pull convention
\[
A_{x,r}(z)=L_{x,r}z+b_{x,r}:V_y\longrightarrow V_x,
\]
\[
\bar b_r=L_{x,r}^{-1}b_{x,r},\qquad
\Delta b_r=b_{y,r}-\bar b_r,\qquad
\Delta v_r=v_r(y)-L_{x,r}^{-1}v_r(x).
\]
The two linear maps are
\(\mathcal B\varepsilon_r=\Delta b_r\),
\(\mathcal S\varepsilon_r=\Delta v_r\). Write
\[
K=\ker\mathcal B,\quad H=K^\perp,\quad U=\operatorname{im}\mathcal B,
\quad M=\mathcal S(K),\quad
\mathscr R=\operatorname{im}(\mathcal B,\mathcal S).
\]
Let \(\sigma=(\mathcal B|_H)^{-1}:U\to H\). Then
\[
J=J^{\rm can}=\mathcal S\sigma,
\qquad C:=J\mathcal B=\mathcal SP_H,
\qquad D:=\mathcal SP_K=\mathcal S-C,
\qquad R_r=D\varepsilon_r.
\tag{2.1}
\]
Here \(D\) is a residual **map**, not the endpoint predicate \(D_\ell\).
Neither \(R_r\) nor \(M\) denotes spacetime curvature.

Define separately:

| Predicate | Exact meaning |
|---|---|
| \(G_y\) | \(\mathscr R_y\) is the graph of a linear map on \(U_y\) |
| \(G\) | \(G_y\) at every site |
| \(Z_y\) | \(R_r(y)=0\) for every Role |
| \(\mathrm{Full}_y\) | \(\operatorname{rank}\mathcal B_y=4\), equivalently \(U_y=V_y\) |
| \(D_\ell\) | All two labelled words with the same start and endpoint have equal evaluation in a specified invertible family \(\ell^+\) |
| \(D_L\) | \(D_\ell\) for \(\ell^+_{x,r}=L_{x,r}\), acting on \(V\) |
| \(D_A\) | Endpoint descent of the full affine transport; equivalently of its homogeneous \(5\times5\) linear representation |

For a **fixed label** \(r\), the pair \((\Delta b_r,\Delta v_r)\) is already
determinate. Multivaluedness appears when arbitrary labelled coefficient
combinations are identified through their common \(\mathcal Bc\). It is not
an assertion that the stored value of a given labelled edge is random.

## 3. Exact graphification theorem

**Theorem 1.** At every site, with no rank assumption,
\[
\boxed{
M=\operatorname{im}D=\operatorname{span}\{R_A,R_B,R_C,R_D\}.}
\tag{3.1}
\]
Consequently,
\[
\boxed{
G_y\iff M=0\iff K\subseteq\ker\mathcal S
\iff D=0\iff Z_y.}
\tag{3.2}
\]

**Proof.** \(P_K\) has image exactly \(K\), since it is the identity on
\(K\). Thus \(\operatorname{im}(\mathcal SP_K)=\mathcal S(K)\). The four
\(\varepsilon_r\) span \(E_{\rm lab}\), so their images span this range.
The fibre over \(u\in U\) of the generated relation is
\(J(u)+M\); it is a singleton iff \(M=0\). Finally
\(\mathcal S(K)=0\iff K\subseteq\ker\mathcal S\). This proves every
direction, including \(U=0\).

The exact dimension is
\[
\dim M=\operatorname{rank}D
=\operatorname{rank}\binom{\mathcal B}{\mathcal S}
 -\operatorname{rank}\mathcal B.
\tag{3.3}
\]
The last equality is rank-nullity for the projection
\(\mathscr R\to U\), whose kernel is \(\{0\}\oplus M\).

**Nearest negative.** Take
\(\mathcal B=(e_A,e_A,0,0)\),
\(\mathcal S=(e_B,-e_B,0,0)\). Then \(J(e_A)=0\),
\(R_A=e_B\), \(R_B=-e_B\), and \(R_C=R_D=0\), but
\(M=\mathbb Re_B\). Vanishing for one Role is strictly weaker than (3.2).
It also shows that the sum of all residuals can vanish while \(M\ne0\).

These statements transform exactly under every invertible output frame:
\(K'=K\), \(C'=gC\), \(D'=gD\), \(M'=gM\). No observer norm enters
the graphification criterion.

## 4. What a graph does not establish

### 4.1 It does not establish the gauge diagonal

The exact translation chart has \(\mathcal S=\eta\mathcal B\); hence it
satisfies \(G_y\). The converse fails. With \(\mathcal B=I\) and
\(\mathcal S=0\), the unique comparison is \(J=0\), not \(\eta\).
This is realizable on an entire periodic archive, not just in an abstract
matrix pair: take \(L_{x,r}=I\), \(e=0\), and
\(b_{x,r}=f(x_r)e_r\) with \(f=(1,2,-3)\) on each length-three cycle.
Then \(\Delta f=(4,1,-5)\), so \(\mathcal B\) is invertible at every
site and \(\mathcal S=0\). The shift has zero periods and is exact, but
\(e\ne b\). Graphification fits the increment pairs; it does not prove
membership in the prescribed paired translation-gauge orbit.

In fact, when the two dimensions are four, every \(\mathcal S\) admits
\(J=\mathcal S\mathcal B^{-1}\) wherever \(\mathcal B\) is invertible.
Thus zero canonical residual is automatic on this open algebraic branch.
It cannot alone be a test of physical classicality or a measure of distance
from the gauge chart.

### 4.2 It does not establish a reversible change of variables

Define the horizontal defect
\[
N_h:=\mathcal B(\ker\mathcal S),\qquad W:=\operatorname{im}\mathcal S.
\]
The reversed relation is a graph on \(W\) iff \(N_h=0\). Therefore
\[
\boxed{\text{both directions are functions}
\iff\ker\mathcal B=\ker\mathcal S.}
\tag{4.1}
\]
Under \(G_y\), \(\ker J=N_h\). A full-rank \(\mathcal B\) still permits
\(J=0\). A two-sided full-fibre identification requires both syntheses to
have rank four.

There is also an exact two-sided core of **every** linear relation:
\[
\boxed{U/N_h\ \simeq\ W/M,\qquad [\mathcal Bc]\mapsto[\mathcal Sc].}
\tag{4.2}
\]
For well-definedness, if \(\mathcal B(c-c')=\mathcal Bd\) with
\(\mathcal Sd=0\), then \(c-c'-d\in K\), so
\(\mathcal S(c-c')\in M\). If \(\mathcal Sc\in M\), subtract a
\(k\in K\) with \(\mathcal Sk=\mathcal Sc\); then
\(c-k\in\ker\mathcal S\), so \(\mathcal Bc\in N_h\). Surjectivity is
immediate. This quotient records exactly the information common to both
coordinates. It does not authorize discarding the two defects physically.

### 4.3 An unlabelled relation does not determine the canonical seed

For \(M\ne0\), \(J^{\rm can}\) uses the labelled presentation and its
counting product, not just the image subspace \(\mathscr R\).

In the duplicate example of §3, replace the first labelled pair
\((e_A,e_B)\) by \((2e_A,2e_B)\), leaving the second
\((e_A,-e_B)\) unchanged. The generated relation is identical. The minimum
counting representative of \(e_A\) is now \((2/5,1/5,0,0)\), giving
\[
J^{\rm can}_{\rm new}(e_A)=\tfrac35e_B,
\qquad J^{\rm can}_{\rm old}(e_A)=0.
\tag{4.3}
\]
This rescaling is not an allowed output-frame transformation or a mere Role
permutation. It is a hostile test of a proposed *forgetful map* to the bare
relation. Such forgetting loses data needed by the seed. On the graph locus,
the unique strict comparison is presentation-independent.

For a fixed \(\mathcal B\), (2.1) is a direct decomposition in coefficient
map space, according to inputs \(H\oplus K\). It does not make the output
images of \(C\) and \(D\) disjoint. For example
\(\mathcal B=(e_A,e_A,0,0)\), \(\mathcal S=(2e_B,0,0,0)\) gives
\(\operatorname{im}C=\operatorname{im}D=\mathbb Re_B\). No direct sum
between a geometric defect and an unknown graded dynamics follows.

## 5. Full rank and the entire extension-independence chain

Since \(\dim E_{\rm lab}=\dim V_y=4\), rank four gives \(K=0\),
therefore \(M=D=0\). Full rank with nonzero vertical defect is impossible.
The equal-dimension hypothesis matters: a surjection from a larger label
space would not have this consequence.

For \(r_b=\dim U\), full extensions of the partial \(J\) form an affine
space with difference space
\[
\operatorname{Hom}(V_y/U,V_y),\qquad \dim=4(4-r_b).
\tag{5.1}
\]
Extensions exist by choosing any vector-space complement. Uniqueness occurs
iff \(U=V_y\). No complement is needed to evaluate \(C\).

**Theorem 2.** Fix \(A,e\) and all downstream selection data. If
\(\widetilde J_1(y)|_{U_y}=\widetilde J_2(y)|_{U_y}\) at **every site**,
the entire audited sourced-diagonal chain is identical for the two extensions.

| Stage | Formula | Reason for independence |
|---|---|---|
| Generator action | \(C_r=\widetilde J(y)\Delta b_r\) | \(\Delta b_r\in U_y\) |
| Relative defect | \(R_r=\Delta v_r-C_r\) | Same \(C_r\) |
| Seed | \(a_r=-\bar b_r-C_r\) | Same \(C_r\) |
| Predecessor | \(\rho_r=A_{y-r,r}^{-1}v_r(y-r)-v_r(y)=a_r-R_r\) | Both summands, and their difference, agree |
| Path source | \(S_{p,r}=P_pa_r(y')-a_r(y)\) | Same seed at both endpoints; \(P_p\) depends on \(A\) |
| Solution set | \(P_p\delta_r(y')-\delta_r(y)=S_{p,r}\) for all labelled paths | Identical equations |
| Parallel kernel | \(\delta_r=a_r+h_r\), \(P_ph_r(y')=h_r(y)\) | Same affine solution space and same linear kernel |
| Post-source selection | PR #120 projection onto \(\mathcal H_o(A)\) | Same transported mean, fixed observer/basepoint/path family |
| Reference and overlap | \(q_r=v_r+\delta_r\), \(\Omega_{rs}=v_r-v_s+\delta_r\) | Identical selected or supplied \(\delta\) |
| Conditional mismatch | \(\kappa=b+Lv_r(y)-v_r(x)+L\delta_r(y)\) | No further evaluation of \(J\) |

In pull order,
\[
S_{p++q,r}=S_{p,r}+P_pS_{q,r},\qquad
S_{\bar p,r}=-P_p^{-1}S_{p,r}.
\]
These identities add no evaluations of \(J\) at transported vectors outside
the active span. In particular there is no hidden operation
\(J_yP_pu\) in the source formula.

Conversely, equality of the seeds for all Roles at a site implies equality of
\(\widetilde J_i\Delta b_r\), hence of the restrictions on their span.
The seed-containing chain therefore factors exactly through
\[
\operatorname{End}(V_y)/\{T:T|_{U_y}=0\}
\simeq\operatorname{Hom}(U_y,V_y).
\tag{5.2}
\]
This converse is not claimed from equality of the final mismatch alone.

**Exact extension control.** On the L=3 gauge witness,
\(U_y\subseteq\mathbb Re_B\). The two full maps
\(\widetilde J_1=\eta\) and
\(\widetilde J_2=\eta+e_C\otimes e_A^*\) are distinct, agree on every
\(U_y\), and produce the same \((15,-3,-12)e_B\) diagonal, all path
sources, and \(\kappa=0\). At the middle site \(U=0\), even \(0\) and
\(I\) agree on all actual increments.

The nearest negative is to change the value on the active \(e_B\) line to
zero: the gauge seed becomes \((6,-3,-3)e_B\), with nonparallel error
\((9,0,-9)e_B\). Thus the audited independence is precisely outside \(U\),
not arbitrary comparison independence.

On generic holonomy backgrounds the PR #120 selected \(\delta\) still
depends on its specified downstream basepoint/path/observer data. The theorem
holds when those data are held fixed; extension independence must not be
rewritten as independence from every auxiliary choice. No conclusion about
unconstructed future observables is made.

### 5.1 Repair of an older candidate rejection

The active-span audit also changes how PR #120's solder-conjugate candidate
must be tested. Its displayed shear \(B_e=I-3E_{B,A}\) gives
\(B_e\eta B_e^{-1}-\eta=-6E_{B,A}\). But the active increment line of that
specific gauge witness is \(\mathbb Re_B\), which this difference
annihilates. Disagreement of full matrices is not a failure at the arguments
actually used by the seed. That old calculation alone does not reject the
candidate on its stated witness.

There is a literal replacement negative on an invertible raw-solder exact
gauge chart. Take \(b_{x,A}=f(j)(e_A+e_B)\) and the coframe coordinates
\(e_A{}^A(x)=e_A{}^B(x)=f(j)\), with \(f=(1,1,-2)\) and all other
components zero. These are the chart shift/coframe gradient data of the
periodic potential \((0,1,2)(e_A+e_B)\). At source site zero,
\[
B_e|_{AB}=\begin{pmatrix}2&0\\-1&1\end{pmatrix},\quad
\Delta b_A=3(e_A+e_B),\quad \Delta v_A=3e_A-3e_B.
\]
The solder-conjugate comparison gives
\[
(B_e\eta B_e^{-1})\Delta b_A=3e_A-6e_B\ne\Delta v_A.
\tag{5.3}
\]
The raw solder determinants around the cycle are \((2,2,-1)\), all nonzero.
Thus the candidate still fails gauge calibration, but the repaired rejection
tests the active span. This is precisely the standard the extension audit
requires; a harmless off-span mismatch is not counted as a failure.

## 6. The selected mismatch has a sharper decomposition

The predecessor identity gives
\(\tau_r=-L_{x,r}\rho_r\), where
\(\tau_r=b_{x,r}+L_{x,r}v_r(y)-v_r(x)\). For any sourced solution
\(\delta_r=a_r+h_r\),
\[
\boxed{\kappa(x,r)=L_{x,r}\bigl(R_r(y)+h_r(y)\bigr).}
\tag{6.1}
\]
This follows by substituting \(\rho=a-R\); it uses no dynamics or new
selection rule. It is useful because it locates the two pieces that remain
visible in the already-defined mismatch: a local residual and a parallel
section. Their output ranges need not be complementary.

Under \(G\), \(R=0\), but \(\kappa\) can still be nonzero. Constant pure
shift has \(a=-b\), \(h=b\), \(\delta=0\), and \(\kappa=b\). Thus
\(M=0\iff R=0\) is not \(\kappa=0\), \(\delta=0\), or absence of cycle
data. Conversely \(\kappa=0\) means \(R_r(y)=-h_r(y)\), not automatically
the vanishing of either summand.

There is a useful improvement when \(D_L\) holds. All loop-fixed spaces are
the full fibre, so PR #120's projection is the identity. Its selected diagonal
can be written without an observer, a basepoint, or a path family:
\[
\boxed{
\delta_r(y)=a_r(y)-\frac1{|X|}\sum_{z\in X}Q_{y\leftarrow z}a_r(z),}
\tag{6.2}
\]
where \(Q\) is the unique endpoint linear transport. Indeed transport the
basepoint mean back to \(y\) and use composition of \(Q\). Equation (6.2)
is still a **global** mean. Endpoint-only transport is not the assertion that
the selected section is a local finite-stencil functional of the background.

For another precise cycle check, form the auxiliary affine connection
\(A^\kappa_{x,r}=(L_{x,r},\kappa(x,r))\) from the conditional mismatch.
This is a defined affine package, not a claim that it is the unknown matter
letter. Under \(G\) and \(D_L\), parallelity gives
\(\kappa(x,r)=h_r(x)\). Its positive Role period at \(x\) is exactly
\[
\operatorname{Hol}_{A^\kappa}(r^L;x)=(I,Lh_r(x)).
\tag{6.3}
\]
Every summand transported to \(x\) is the same parallel vector. Since
\(L>0\) over \(\mathbb R\), all these periods vanish iff every \(h_r=0\).
If \(h=0\), this connection is simply \((L,0)\), which descends under
\(D_L\). Hence, under the stated hypotheses,
\[
D_{A^\kappa}\iff h=0.
\tag{6.4}
\]
This identifies an actual additional cycle test; it does not count \(M=0\)
and \(R=0\) twice.

## 7. Labelled descent and its exact locality boundary

For a specified \(\ell^+_{x,r}\in\operatorname{GL}(V)\), the reverse slot is
\[
\ell^-_{x,r}=(\ell^+_{x-r,r})^{-1}.
\]
Words are literal `List ChainStep`. Evaluation obeys
\(\ell(p++q)=\ell(p)\ell(q)\) in pull order and
\(\ell(\bar p)=\ell(p)^{-1}\).

**Theorem 3 (existing owner, scoped exactly).**
\[
\boxed{D_\ell\iff
\forall x,\gamma\ (\operatorname{pathEnd}(\gamma,x)=x
\Longrightarrow\ell(\gamma,x)=I).}
\tag{7.1}
\]
The forward implication compares a loop with the empty word. For the reverse,
if \(p,q:x\to y\), use the loop \(p++\bar q\). Its value is
\(\ell(p)\ell(q)^{-1}\), so identity implies equality. This argument keeps
the labelled slots throughout.

Under (7.1), define \(Q_{x\leftarrow y}\) by any word from \(x\) to \(y\).
It is well-defined and satisfies
\[
Q_{x\leftarrow x}=I,\quad
Q_{x\leftarrow y}Q_{y\leftarrow z}=Q_{x\leftarrow z},\quad
Q_{y\leftarrow x}=Q_{x\leftarrow y}^{-1}.
\]
Existence of words follows from the connected periodic Role graph. No
physical matter family is constructed by this descent theorem.

The following distinctions are mandatory:

- A local field of edge maps is already defined when its holonomy is
  nontrivial. Erasing all path dependence of transport is a stronger condition
  than writing a local connection. The passport must not exclude every curved
  connection by definition and then call that a derivation of classicality.
- \(D_A\) implies \(D_L\) by taking linear parts; the converse fails on
  constant pure shift. All linear loops are identity, but a positive Role
  cycle has affine shift \(Lb\ne0\).
- The loop-fixed space in PR #120 belongs to \(L\). It is not silently the
  holonomy of a future graded matter representation.
- Two-link **reference-origin** compression is another operation:
  `referenceJunction_compress_iff` requires \(q_1=v_2\). At flat mixed Roles,
  \(G\), \(D_L\), and \(D_A\) all hold, and each edge mismatch is zero,
  while \(q_A-v_B=e_A-e_B\ne0\). Thus even the passport (0.1) does not
  identify every Role reference with a single common origin.

## 8. Complete logical-independence matrix

Here holonomy means **the same background's linear transport \(L\)**. Thus
the examples do not rely solely on appending an unrelated generic link family
to a matrix pair. Each rank/graph statement below holds at every site.

Let \(g\) be the exact A/B boost
\[
g=\begin{pmatrix}5/3&4/3&0&0\\4/3&5/3&0&0\\0&0&1&0\\0&0&0&1\end{pmatrix},
\qquad
w=(I-g^{-1})e_A=-\tfrac23e_A+\tfrac43e_B.
\]
For boost examples, \(L_{x,A}=g\), \(L_{x,s}=I\) for \(s\ne A\), and
\(e=0\), so \(\mathcal S\varepsilon_A=w\), others zero. The length-three
linear cycle is
\[
g^3|_{AB}=\tfrac1{27}
\begin{pmatrix}365&364\\364&365\end{pmatrix}\ne I.
\tag{8.1}
\]
All linear plaquettes are flat, because the other positive linear letters
are identity.

| Full rank everywhere | \(G\) | \(D_L\) | Exact realization |
|---|---|---|---|
| No | Yes | Yes | Flat: \(\mathcal B=\mathcal S=0\), rank zero |
| No | Yes | No | Boost background, \(b_{x,A}=e_A\), others zero: \(\mathcal B=\mathcal S=(w,0,0,0)\), rank one |
| No | No | Yes | Flat connection and L=2 Nyquist coframe: \(\mathcal B=0\), \(M=\mathbb Re_A\) everywhere |
| No | No | No | Boost background, all \(b=0\): \(\mathcal B=0\), \(M=\mathbb Rw\) everywhere |
| Yes | Yes | Yes | Length-three \(b_{x,r}=f(x_r)e_r\), \(f=(1,2,-3)\), \(L=I,e=0\): \(\mathcal B=\operatorname{diag}(\Delta f(x_r))\), \(\mathcal S=0\) |
| Yes | Yes | No | Boost background, \(b_{x,A}=e_A\), \(b_{x,s}=f(x_s)e_s\) for \(s=B,C,D\): columns \((w,\Delta f(x_B)e_B,\Delta f(x_C)e_C,\Delta f(x_D)e_D)\) |
| Yes | No | Either | Impossible: rank four implies \(K=0\), hence \(M=0\) |

In the final realized row, the determinant is
\((-2/3)\Delta f(x_B)\Delta f(x_C)\Delta f(x_D)\ne0\).
The previous full-rank row even has \(D_A\), since the shift is the gradient
of the periodic scalar profile \((0,1,3)\) in each coordinate. It is still
not the paired \(b=e\) gauge chart.

This exhausts the eight Boolean combinations: six are realized and two are
algebraically forbidden. Replacing \(M=0\) by all-Role \(R=0\) changes no
row. The separate rank-jump family in §10 supplies the required stability
separation.

For a generic family \(\ell\) supplied independently of \(A,e\), the same
Boolean separations are also available by product construction. That weaker
statement does not provide a coupling to an unconstructed finite matter link.

## 9. Mandatory finite hostile controls

### 9.1 Flat and constant pure shift

Flat has \(U=M=0\), \(a=\delta=\kappa=0\). Constant pure shift also has
\(U=M=0\), but \(a=-b\), \(h=b\), \(\delta=0\), \(\kappa=b\).
Both reject rank-four necessity for the audited formulas. Pure shift also
rejects \(R=0\Rightarrow\kappa=0\) and \(D_L\Rightarrow D_A\).

### 9.2 L=3 exact translation-gauge rank drop

For the A-edge shift cycle \(b_A=(3,3,-6)e_B\), the source-site values are

| Source coordinate | \(\Delta b_A\) | \(\Delta v_A\) | Rank | \(a_A=\delta_A\) |
|---|---|---|---|---|
| 0 | \(9e_B\) | \(-9e_B\) | 1 | \(15e_B\) |
| 1 | 0 | 0 | 0 | \(-3e_B\) |
| 2 | \(-9e_B\) | \(9e_B\) | 1 | \(-12e_B\) |

The mean is zero, \(h=0\), and \(\kappa=0\) on all edges. There is no
full-fibre ambiguity in any output despite the zero middle span. After a
pure-linear frame, comparison is \(g\eta g^{-1}\) on \(gU\), not a
fixed numerical \(\eta\). The exact A/B block is
\(\frac19\left(\begin{smallmatrix}41&-40\\40&-41\end{smallmatrix}\right)\).

### 9.3 L=2 Nyquist

At flat \(A\), use \(e_A{}^A=(-2,+2)\), hence
\(v_A=(-1,3)e_A\). Then
\[
\mathcal B=0,\quad J=0,\quad R_A(y)=(-4,+4)e_A,
\quad M=\mathbb Re_A.
\]
The source seed and selected diagonal are zero, while at the **edge start**
\[
\kappa_A(x)=(+4,-4)e_A.
\]
The opposite signs are just predecessor/source indexing. This background
has trivial linear and affine holonomy and a non-graph relation. A quotient
that kills \(M\) erases the very raw response that the task requires retained.

### 9.4 L=3 corner and curl

Set \(e_A{}^B(0)=1\) at the single origin of the four-dimensional archive,
zero elsewhere, with flat \(A\). Then
\(v_A(0)=e_A-e_B\), \(v_A(A)=e_A\), \(\mathcal B=0\), and
\(\kappa_A(0)=e_B\). At affected source sites \(M\ne0\).
The B-coordinate pattern of the solder curl along the relevant B cycle is
\((-1,0,+1)\). It is not a parallel section, so adding a nonzero multiple
violates the fixed sourced equation. This does not require inventing a new
curvature selector.

For the separate constant harmonic coframe, \(a=0\), and the source leaves
a constant parallel freedom. PR #120's positive kernel rule chooses zero.
The coframe itself is still retained in \(v\) and the Role overlaps.

### 9.5 Duplicate increments

For \(\Delta b_A=\Delta b_B=u\) and solder outputs \(v_1,v_2\),
\[
J(u)=\tfrac12(v_1+v_2),\qquad
R_A=\tfrac12(v_1-v_2),\qquad R_B=-R_A.
\]
If \(v_1\ne v_2\), the strict graph assignment is impossible. The labelled
counting split exposes this fact symmetrically. Choosing one duplicate as
the representative would change the selected seed.

### 9.6 Nontrivial holonomy and exact L=2 period

The boost (8.1) gives a nontrivial cycle even when all linear plaquettes are
flat and the relation is a graph. At period two, `.fwd r` and `.bwd r` have
the same endpoint but are distinct labels. Endpoint descent forces
\[
\boxed{\ell^+_{x,r}\ell^+_{x+r,r}=I.}
\tag{9.1}
\]
Constant boost letters violate this with \(g^2\ne I\); alternating
\(g,g^{-1}\) satisfy the period. A constant pure affine shift violates the
full affine period by \(2b\), although its linear period is identity.

Even **all Role period-two tests** do not replace full labelled holonomy:
take constant involutions \(X,Z\) on a spatial two-plane, where \(X\)
swaps the basis and \(Z=\operatorname{diag}(1,-1)\). Each squares to identity,
but \(XZ\ne ZX\), so the plaquette loop is nontrivial. Both local square
relations and global cycle relations must be checked in a generator-based
implementation of (7.1).

## 10. Stability failure: the selected mismatch can jump

### 10.1 The mandated local rank-jump relation

With all other columns zero, take
\[
\mathcal B_t\varepsilon_A=te_A,\qquad
\mathcal S_t\varepsilon_A=e_B.
\]
For \(t\ne0\), \(M_t=0\) and \(J_t(e_A)=t^{-1}e_B\). At zero,
\(U_0=0\), \(J_0=0\) on that domain, and \(M_0=\mathbb Re_B\).
The generated relation is the line \(\mathbb R(te_A,e_B)\), which has
the finite vertical limit \(\mathbb R(0,e_B)\).

However the **actual generator action**, not only its normalization, is
\[
C_t\varepsilon_A=
\begin{cases}e_B&t\ne0,\\0&t=0.\end{cases}
\tag{10.1}
\]
Thus relation continuity does not imply continuity of the counting-selected
representative used by the seed.

### 10.2 Literal periodic lift of the failure

This is an admissible fixed-L=3 background family, with all other coordinates
spectators. Let \(j=x_A\) and \(f=(1,-2,1)\). Set
\[
L_{x,r}=I,\quad b_{x,A}(t)=t f(j)e_A,\quad b_{x,s}=0\ (s\ne A),
\]
\[
v_A(x)=e_A+f(j)e_B,\qquad v_s(x)=e_s\ (s\ne A).
\tag{10.2}
\]
The raw coframe is \(e_A{}^B(x)=-f(j)\); the raw solder matrix is a shear
of determinant one. Both \(A_t\) and \(e\) depend smoothly on \(t\).
The affine shift is the exact periodic gradient of
\((0,t,-t)e_A\), so **all affine holonomies are trivial for every \(t\)**.

At source coordinate \(j\), write
\(d_j=f(j)-f(j-1)=(0,-3,3)\). Then
\[
\Delta b_A=t d_je_A,\qquad \Delta v_A=d_je_B.
\]
For \(d_j\ne0\) the relation is the same line as in §10.1, up to a
nonzero generator multiple. At the site with \(d_j=0\) it is the zero
relation for every \(t\). Thus every site's relation has a continuous
constant-dimensional family, including at zero.

For \(t\ne0\), all sites are graphs, and
\[
a_A(j)=-t f(j-1)e_A-d_je_B,\qquad
\frac13\sum_j a_A(j)=0.
\]
Therefore the unambiguous flat-pull selector (6.2) gives
\(\delta=a\), \(h=0\), and
\[
\kappa_A(t;x)=0\qquad(t\ne0).
\tag{10.3}
\]
At \(t=0\), all affine increments vanish, so \(C=a=\delta=h=0\), whereas
\[
\kappa_A(0;x)=\bigl(f(j+1)-f(j)\bigr)e_B=(-3,3,0)e_B.
\tag{10.4}
\]
In particular, \(\kappa_A(0;0)=-3e_B\), while the value is zero for every
nonzero \(t\). No basepoint choice, observer ambiguity, nontrivial holonomy,
raw-solder singularity, or floating-point tolerance explains this jump.

**Pressure verdict:** the current construction is globally defined pointwise;
it has no general continuity guarantee across graph-to-vertical transitions.
The example disproves a stronger stable-interface interpretation. It does
not contradict the pointwise claims of #123 or the conditional algebra of
#125.

### 10.3 Exact lost-direction criterion

Here is a theorem-ready way to locate the failure. Let
\(\mathcal B_t\to\mathcal B_0\), \(\mathcal S_t\to\mathcal S_0\), and
suppose along a fixed-rank approach that \(P_{H_t}\to P_*\). Orthogonal
projector limits are orthogonal projectors. Taking limits in
\(\mathcal B_tP_{H_t}=\mathcal B_t\) gives
\(\mathcal B_0P_*=\mathcal B_0\), hence
\(H_0\subseteq\operatorname{im}P_*\). Write
\[
\operatorname{im}P_*=H_0\oplus W_{\rm lost},\qquad
W_{\rm lost}\subseteq K_0.
\]
Then
\[
\boxed{
\lim C_t-C_0=\mathcal S_0P_{W_{\rm lost}}.}
\tag{10.5}
\]
Continuity of the correlated action along that approach is therefore
equivalent to \(\mathcal S_0(W_{\rm lost})=0\). In the witness,
\(W_{\rm lost}=\mathbb R\varepsilon_A\) and this image is nonzero.

For arbitrary sequences in finite dimension, projector compactness permits
the same analysis on every convergent subsequence. In particular,
\(M_0=0\) is sufficient for continuity of \(C\) and \(D\) **at that
background**, because it annihilates every possible lost subspace. It does
not bound the operator \(J_t\) on normalized active directions.

For example \(\mathcal B_t\varepsilon_A=t^2e_A\),
\(\mathcal S_t\varepsilon_A=te_B\) has \(M_t=0\) for every \(t\),
including zero, but \(J_t(e_A)=t^{-1}e_B\). Here \(C_t\to0\) is
continuous. The **image relation** drops dimension at zero; its Grassmannian
limit is not its zero fibre there. Smooth generators do not in general make
their image subspaces a smooth relation bundle. Constant pair rank is the
missing hypothesis in that overstatement.

On a constant-rank region, a quantitative sufficient bound is
\[
\|J\|\le \|\mathcal S\|/\sigma_{\min}(\mathcal B|_H),
\]
using any explicitly specified positive output norm for analysis. A uniform
nonzero lower bound and bounded \(\mathcal S\) control the gain. This norm
does not enter the definition of the source. Rank alone gives no such bound.
Similarly \(\dim M=1\) can coexist with residual magnitude tending to zero,
as \(\mathcal B=0\), \(\mathcal S\varepsilon_A=\epsilon e_B\) shows.
The dimension is an exact obstruction count, not a quantitative distance.

## 11. Further synthesis: when is forgetting actually compatible?

The next useful synthesis is a criterion for a **specified linear readout**
to forget internal data. It avoids assuming that every possible quotient is
physically admissible.

For a supplied surjective map \(q_y:V_y\to\overline V_y\) with kernel
\(W_y\), forgetting only the solder output gives a unique map
\(U_y\to\overline V_y\) iff \(M_y\subseteq W_y\). This follows from
the same kernel-inclusion proof as Theorem 1.

If **both** coordinates use the same quotient fibre, the exact condition is
stronger:
\[
\boxed{
\operatorname{im}(q_y\mathcal B_y,q_y\mathcal S_y)
\text{ is a graph}
\iff
\mathcal S_y(\mathcal B_y^{-1}W_y)\subseteq W_y.}
\tag{11.1}
\]
Indeed its coefficient kernel is
\(\ker(q_y\mathcal B_y)=\mathcal B_y^{-1}W_y\). Merely killing the old
vertical part can create new coefficient relations after the first coordinate
is also quotiented. Under an existing graph, this says
\(J_y(U_y\cap W_y)\subseteq W_y\).

For the same-fibre linear transport \(P\), quotient transport exists iff
\(P_pW_{y'}=W_y\) for all paths. It is endpoint-independent iff additionally
\[
(P_\gamma-I)V_y\subseteq W_y
\quad\text{for every labelled loop at }y.
\tag{11.2}
\]
Thus the same quotient must pass a local relation test **and** a transport
test. The choice \(W_y=M_y\) has no automatic reason to pass either
transport invariance or (11.1).

### 11.1 Constructive finite saturation theorem

There is a universal algebraic answer for the simultaneous same-fibre quotient.
Fix a basepoint \(o\) and paths to all sites, with pulls
\(T_y:V_y\to V_o\). Let
\[
H_o^{\rm coinv}:=\sum_{\gamma:o\to o}(P_\gamma-I)V_o,
\qquad B_y^o=T_y\mathcal B_y,\quad S_y^o=T_y\mathcal S_y.
\]
This is a coinvariant defect subspace, **not** PR #120's common fixed space
\(\mathcal H_o\). Define
\[
W^{(0)}=H_o^{\rm coinv},\qquad
W^{(k+1)}=W^{(k)}+
\sum_y S_y^o\bigl((B_y^o)^{-1}W^{(k)}\bigr).
\tag{11.3}
\]
The sequence is monotone and stabilizes after at most four strict dimension
increases. If one step has the same dimension, it is already a fixed point.
Call the result \(W^*\), and set \(W_y=T_y^{-1}W^*\).

**Theorem 4.** This is the smallest parallel family of subspaces for which
both the same-fibre quotient relation is a graph and the quotient linear
transport is endpoint-independent.

**Proof.** Every subspace containing \(H_o^{\rm coinv}\) is invariant under
all loop operators: \(Pv-v\in H_o^{\rm coinv}\); use inverses for equality.
Thus the construction of \(W_y\) is independent of the chosen path to \(y\),
and yields a parallel family. At the fixed point, (11.3) is exactly (11.1)
in basepoint coordinates; (11.2) holds by initialization. Conversely any
family satisfying (11.1)–(11.2) contains the initialization and each iterate,
by induction, so contains \(W^*\). Replacing \(T_y\) by a loop times
\(T_y\) changes outputs only by \(H_o^{\rm coinv}\) and preserves preimages
of every \(W^{(k)}\); hence the iterates themselves are independent of that
choice. A different basepoint transports the construction equivariantly.

This is a finite construction despite the notation summing all loops. A
spanning tree of the finite **labelled multigraph** gives finitely many
fundamental loop generators. The span of their \((P-I)V\) images suffices:
\((PQ-I)v=(P-I)Qv+(Q-I)v\), and inverses add no new image. Both L=2
parallel edges must be retained when making that graph.

### 11.2 A one-dimensional defect can force total quotient collapse

At identity transport, take the exact coefficient maps
\[
\mathcal B=(e_A,e_B,e_C,0),\qquad
\mathcal S=(e_B,e_C,e_D,e_A).
\]
Initially \(M=\mathbb Re_A\). Iteration (11.3) gives successively
\[
\mathbb Re_A,quad
\operatorname{span}(e_A,e_B),\quad
\operatorname{span}(e_A,e_B,e_C),\quad V.
\tag{11.4}
\]
The maximal simultaneous quotient is zero-dimensional. Killing a vertical
direction forces its successor to vanish, then the next, then the entire
fibre. This is an exact algebraic witness within the theorem's input type,
not a claim that a physical observer must perform this quotient.

For the Nyquist control with flat \(P\), saturation kills the \(e_A\)
direction, including the mandated \(4e_A\) response. For boost holonomy,
\(H_o^{\rm coinv}\) contains the entire A/B plane. Thus quotient existence
alone is cheap; **preserving a specified set of observable distinctions** is
the real additional requirement. A zero quotient always exists and proves
no physical classical limit.

This supplies a precise future meaning for “admissible quotient”: its kernel
must satisfy (11.1)–(11.2) and must be invisible to the chosen readouts. No
such invisibility is assumed here, especially for Nyquist and harmonic data.

## 12. Corrected interface hierarchy

| Level | Literal conclusion | Additional conclusion not established |
|---|---|---|
| K0: all labelled synthesis pairs | Relation, quotient comparison, canonical counting split are defined pointwise | Stable subspace bundle or stable selected outputs |
| K1: K0 plus \(G\) | A unique strict comparison on each actual \(U_y\) | Inverse comparison; \(J=\eta\); paired gauge exactness; vanishing \(\kappa\) |
| K2: K1 plus \(D_\ell\) for a specified family | That family's word evaluation descends to endpoints | Descent of another representation; common-origin junction compression; local action |
| K3: K2 plus \(U_y=V_y\) | The entire comparison endomorphism is identifiable | New content in the already-audited sourced chain; invertibility of \(J\); stable limiting dynamics |

Thus K3 is a strictly smaller set of backgrounds, but its extra hypothesis
buys only full-comparison identifiability in the present audit. Flat, pure
shift and the exact gauge rank drop already have well-defined downstream
outputs without it. Calling K3 *the* physical classical sector is unsupported.

The finite rank and graph conditions can be investigated before any limit in
\(L\). This does not prove that rank stabilization is a physically selected
limit, and §10 shows why pointwise graphification alone is inadequate for a
stable limiting claim. Equations (11.1)–(11.3) formulate what forgetting would
require if a concrete readout is later supplied.

The remaining finite graded coframe dressing is an independent seam. Neither
its existence, finite formula, first-jet integration, nor a direct dynamical
split follows from the coefficient decomposition (2.1). No claim about GR,
QFT, an action, stress, Einstein equations, a continuum manifold, or physical
time is made here.

## 13. Theorem-ready handoff and pressure coverage

The existing two worker briefs remain the appropriate owners of their narrow
algebraic interfaces. This research PR neither duplicates their Lean modules
nor mints new executable tasks outside CONTROL.

| Handoff statement | Existing input / remaining formal work |
|---|---|
| \(\operatorname{range}\,\mathrm{canonicalResidual}=\mathrm{verticalDefect}\) | Extend #126 using that the kernel component is identity on \(\ker B\) |
| \(M=0\iff\forall r,R_r=0\), residual rank formula | Role basis expansion and finite-dimensional rank-nullity; add all-Role converse explicitly |
| Full rank implies graph; two-sided graph iff equal kernels | Finite dimensionality plus strict-span criterion; keep inverse comparison separate |
| Every stage in §5 is extension-independent | Reuse #125 definitions in `WRK-A4D-ACTIVE-SPAN-EXTENSION-INDEPENDENCE`; quantify over all sites |
| \(\kappa=L(R+h)\) | Combine predecessor decomposition with existing diagonal mismatch identity |
| \(D_\ell\iff\) all labelled loops identity | Reuse the existing `List ChainStep` owner in `WRK-A4D-LABELLED-ENDPOINT-CLASSICAL-DESCENT` |
| Independence matrix | Exact same-background finite realizations in §8, not just unrelated product structures |
| Flat-pull selector formula and rank-jump mismatch | Research selection theorem with explicit hypotheses; not in #125's supplied-J kernel theorem |
| Lost-direction criterion (10.5) | Separate continuity theorem with projector limit hypotheses |
| Quotient graph/transport criteria and finite saturation | New theorem-ready finite linear algebra; no readout or physical quotient inferred |

Pressure coverage for the main implications is explicit:

| Claim under pressure | Positive exact witness | Nearest negative | Rank-degenerate control | Labelled-holonomy control |
|---|---|---|---|---|
| Graph iff all residuals zero | L=3 exact gauge | Duplicate unequal solder outputs; one Role still zero | Flat and gauge middle site | Both graph and vertical boost examples |
| Full rank only needed for full identifiability | Full-rank periodic example | Rank-one distinct full extensions | Flat/pure shift \(U=0\) | Full rank with boost cycle |
| Whole-chain extension independence | \(\eta\) and \(\eta+e_Ce_A^*\) on gauge spans | Changing the active \(e_B\) value changes the seed | Zero middle span | Source append/reverse checked in noncommuting pull order; no holonomy restriction in proof |
| Endpoint iff all loop holonomies trivial | Identity and exact affine gauge | Constant boost cycle | Nyquist with identity transport | L=2 positive period and noncommuting involutions |
| Graph/descent imply stable outputs | Constant-rank regular families | Periodic discontinuity (10.2) | Vertical endpoint at \(t=0\) | Counterexample has trivial **affine** holonomy throughout |
| Common quotient iff relation/transport compatible | Fixed point of (11.3) | Quotienting only the old \(M\) fails in (11.4) | Nyquist quotient loses a live direction | Boost coinvariant A/B loss; labelled loop generators retained |

These proofs and controls establish the scoped passport terminal, while
refuting the stronger stable/common-origin/classical-dynamics interpretations.

## 14. Exactly one next pressure step

**Pressure-test continuity of the selected sourced-diagonal readout across
rank transitions.** Use (10.2) as the mandatory killing witness. CONTROL
should require a theorem or a scoped no-go deciding whether the current
primitive can support a continuous selected \((\delta,\kappa)\) on a
specified admissible family while retaining exact gauge, pure-shift and raw
Nyquist/corner controls.

The input should be the already-derived comparison and source, not a new
unconstrained selector. The first criterion is (10.5): identify the lost
coefficient directions and test whether their solder images survive. Then
separate continuity of \(C=J\mathcal B\) from boundedness of normalized
\(J\), and propagate the actual result through the fixed source/kernel
selection. Any restriction of admissible rank-changing backgrounds, any
altered representative, or any observable quotient must be stated as an
additional hypothesis and tested against the mandatory raw controls.

This is the next pressure target because a concrete failure is already
present. It does not open the finite graded dressing gate by assertion.

## 15. Reproducible exact verification

The appendix is a self-contained Python standard-library checker, using
`fractions.Fraction`, row reduction and finite enumeration. It is embedded
in this memo so the research arithmetic is durable without an unregistered
certificate or a new dependency. It checks all sites and four Role slots on
the stated L=2/L=3 backgrounds, the extension control, exact noncommutative
source laws, period firewalls, the actual discontinuous selected mismatch,
and quotient saturation. Symbolic proofs above supply the general quantifiers;
finite assertions are not promoted to Lean theorems.

Execution of the exact appendix: **5822 assertions passed**, with no floating
tolerances. The many assertions include repeated per-site identities; this
is one finite hostile suite, not 5822 independent theorem proofs.

From repository root, run:

```bash
python - <<'CHECK'
from pathlib import Path
p = Path('02_REGISTRY/research/MEMO_A4D_CLASSICAL_KINEMATIC_INTERFACE_PRESSURE.md')
s = p.read_text().split('\n<!-- EXACT_CHECKER_BEGIN -->\n', 1)[1]
code = s.split('```python\n', 1)[1].split('\n```', 1)[0]
exec(compile(code, str(p) + ':exact-checker', 'exec'))
CHECK
```

## 16. Ready audit

Before Ready, `origin/main` was fetched again and remained
`bfc90bff3c176ee998562dbaf7821b41858388bc`. PRs #123–#126 were still open,
with exactly the heads in §1; the audited candidate files were unchanged.
Their provisional status is retained explicitly. No dependency branch was
self-merged or copied into this PR.

Local validation passed: canonical repository architecture (zero warnings),
claim-strength lint, generated Lean views, active work validation, and the
5822-assertion exact appendix. The task self-retired with
`tools/task_lifecycle.py retire`: its manifest row and brief were removed
and generated status views refreshed. The final PR declares
`Lifecycle: REVIEW`; merge and acceptance remain with CONTROL.

There are no Lean/formalization changes and no new claims. A new local Lean
build is therefore outside this research PR's changed surface. Ready-state
remote CI is the final repository guard; its status is reported on PR #128.

## Appendix: exact checker

<!-- EXACT_CHECKER_BEGIN -->

```python
from fractions import Fraction as Q
from itertools import product

checks = 0

def ck(ok, label):
    global checks
    checks += 1
    if not ok:
        raise AssertionError(label)

def z(m=4, n=4):
    return [[Q(0) for _ in range(n)] for _ in range(m)]

def eye(n=4):
    return [[Q(i == j) for j in range(n)] for i in range(n)]

def tr(a):
    return [list(c) for c in zip(*a)]

def add(a, b):
    return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]

def sc(t, a):
    return [[Q(t)*x for x in r] for r in a]

def sub(a, b):
    return add(a, sc(-1,b))

def mul(a, b):
    return [[sum((x*y for x,y in zip(r,c)),Q(0)) for c in tr(b)] for r in a]

def col(a,j):
    return [r[j] for r in a]

def cols(vs,n=4):
    return [[Q(v[i]) for v in vs] for i in range(n)]

def mv(a,v):
    return [sum((x*y for x,y in zip(r,v)),Q(0)) for r in a]

def va(*vs):
    return [sum(q,Q(0)) for q in zip(*vs)]

def vs(t,v):
    return [Q(t)*q for q in v]

def rr(a):
    a=[[Q(x) for x in row] for row in a]
    piv=[]
    k=0
    for j in range(len(a[0])):
        p=next((i for i in range(k,len(a)) if a[i][j]),None)
        if p is None:
            continue
        a[k],a[p]=a[p],a[k]
        t=a[k][j]
        a[k]=[x/t for x in a[k]]
        for i in range(len(a)):
            if i!=k:
                t=a[i][j]
                a[i]=[x-t*y for x,y in zip(a[i],a[k])]
        piv.append(j)
        k+=1
        if k==len(a):
            break
    return a,piv

def rank(a):
    return len(rr(a)[1])

def ker(a):
    r,piv=rr(a)
    n=len(a[0])
    out=[]
    for j in range(n):
        if j not in piv:
            v=[Q(i==j) for i in range(n)]
            for i,p in enumerate(piv):
                v[p]=-r[i][j]
            out.append(v)
    return out

def inv(a):
    n=len(a)
    r,piv=rr([x+y for x,y in zip(a,eye(n))])
    if piv[:n]!=list(range(n)):
        raise ValueError('singular')
    return [row[n:] for row in r]

def span(vs0,n=4):
    m=cols(vs0,n)
    return [col(m,j) for j in rr(m)[1]]

def projector(basis,n=4):
    if not basis:
        return z(n,n)
    c=cols(basis,n)
    return mul(mul(c,inv(mul(tr(c),c))),tr(c))

def package(b,s):
    k=ker(b)
    pk=projector(k)
    c=mul(s,sub(eye(),pk))
    d=mul(s,pk)
    m=span([mv(s,v) for v in k])
    ck(add(c,d)==s,'coefficient decomposition')
    ck(rank(d)==len(m)==rank(b+s)-rank(b),'residual image/rank formula')
    ck((d==z())==(rank(b+s)==rank(b)),'graph criterion')
    return c,d,m

I=eye()
Z=z()
e=[col(I,j) for j in range(4)]
o=[Q(0)]*4
eta=cols([e[0]]+[vs(-1,v) for v in e[1:]])
g=[[Q(5,3),Q(4,3),0,0],[Q(4,3),Q(5,3),0,0],
   [0,0,1,0],[0,0,0,1]]
gi=inv(g)
ck(mul(tr(g),mul(eta,g))==eta,'rational Lorentz boost')
ck(mul(g,gi)==I,'boost inverse')
ck(mul(g,eta)!=mul(eta,g),'fixed eta fails conjugacy')

# A full-operator mismatch must be tested on the active increment span.
raw=eye(); raw[1][0]=Q(-3)
old=mul(raw,mul(eta,inv(raw)))
ck(old!=eta and mv(old,e[1])==mv(eta,e[1]),'old shear mismatch annihilates its active line')
raw=eye(); raw[0][0]=Q(2); raw[1][0]=Q(-1)
bad=mul(raw,mul(eta,inv(raw)))
db=vs(3,va(e[0],e[1]))
ck(mv(bad,db)==va(vs(3,e[0]),vs(-6,e[1])),'repaired solder-conjugate active failure')
ck(mv(eta,db)==va(vs(3,e[0]),vs(-3,e[1])),'repaired exact gauge increment')
ck(rank(raw)==4 and mv(bad,db)!=mv(eta,db),'failure on invertible raw solder')

# Strict graph, one Role, duplicate generators, and presentation dependence.
package(Z,Z)
package(I,Z)
ck(rank(I)==4 and rank(Z)==0,'full graph need not be invertible')
b=cols([e[0],e[0],o,o]); s=cols([e[1],vs(-1,e[1]),o,o])
c,d,m=package(b,s)
ck(c==Z and d==s and len(m)==1,'duplicate symmetric split')
ck(col(d,2)==o and col(d,0)!=o,'one Role zero is insufficient')
c2,d2,_=package(mul(g,b),mul(g,s))
ck(c2==mul(g,c) and d2==mul(g,d),'output frame covariance')
tlabel=eye(); tlabel[0][0]=Q(2)
bb=mul(b,tlabel); ss=mul(s,tlabel)
cc,_,_=package(bb,ss)
ck(rank(b+s)==rank(bb+ss)==rank([r+q for r,q in zip(b+s,bb+ss)]),
   'same unlabelled relation')
ck(col(cc,1)==vs(Q(3,5),e[1]),'same relation has different canonical J(u)')

# Entire finite archive controls: all four Role slots are used.
def shift(x,r,t,L):
    y=list(x); y[r]=(y[r]+t)%L; return tuple(y)

def fields(L,lin,bfun,vfun):
    sites=list(product(range(L),repeat=4))
    out={}
    for y in sites:
        bars=[]; bs=[]; ss=[]
        for r in range(4):
            x=shift(y,r,-1,L); li=inv(lin(x,r))
            bar=mv(li,bfun(x,r)); bars.append(bar)
            bs.append(va(bfun(y,r),vs(-1,bar)))
            ss.append(va(vfun(y,r),vs(-1,mv(li,vfun(x,r)))))
        b=cols(bs); s=cols(ss); c,d,m=package(b,s)
        a=[va(vs(-1,bars[r]),vs(-1,col(c,r))) for r in range(4)]
        out[y]=(b,s,c,d,m,a)
    return sites,out

def flat_selected(L,bfun,vfun):
    sites,out=fields(L,lambda x,r:I,bfun,vfun)
    means=[vs(Q(1,len(sites)),va(*[out[y][5][r] for y in sites])) for r in range(4)]
    ds={y:[va(out[y][5][r],vs(-1,means[r])) for r in range(4)] for y in sites}
    kap={}
    for x in sites:
        for r in range(4):
            y=shift(x,r,1,L)
            kap[x,r]=va(bfun(x,r),vfun(y,r),ds[y][r],vs(-1,vfun(x,r)))
            ck(kap[x,r]==va(col(out[y][3],r),vs(-1,means[r])), 'kappa = R + h')
    return sites,out,ds,kap

zero=lambda x,r:o
flatv=lambda x,r:e[r]
origin=(0,0,0,0)
_,out,ds,kap=flat_selected(3,zero,flatv)
ck(all(v==o for v in kap.values()),'flat mismatch')
_,out,ds,kap=flat_selected(3,lambda x,r:e[1],flatv)
ck(all(rank(v[0])==0 and v[3]==Z for v in out.values()),'pure shift graph rank zero')
ck(all(v==o for row in ds.values() for v in row),'pure shift diagonal zero')
ck(all(v==e[1] for v in kap.values()),'pure shift retained')
ck(vs(3,e[1])!=o,'linear identity does not erase affine period')
f=(3,3,-6)
bg=lambda x,r:vs(f[x[0]],e[1]) if r==0 else o
vg=lambda x,r:va(e[0],vs(-f[x[0]],e[1])) if r==0 else e[r]
_,out,ds,kap=flat_selected(3,bg,vg)
for j in range(3):
    y=(j,0,0,0)
    ck(col(out[y][0],0)==vs((9,0,-9)[j],e[1]),'gauge increment')
    ck(out[y][1]==mul(eta,out[y][0]),'exact gauge chart calibration')
    ck(rank(out[y][0])==(1,0,1)[j],'gauge rank drop')
    ck(ds[y][0]==vs((15,-3,-12)[j],e[1]),'exact gauge diagonal')
ck(all(v==o for v in kap.values()),'exact gauge mismatch zero')
J2=add(eta,cols([e[2],o,o,o]))
ck(J2!=eta,'distinct full extensions')
for row in out.values():
    ck(mul(J2,row[0])==mul(eta,row[0])==row[2],'extension action equality on all sites')

vn=lambda x,r:vs((-1,3)[x[0]],e[0]) if r==0 else e[r]
_,out,ds,kap=flat_selected(2,zero,vn)
ck(kap[origin,0]==vs(4,e[0]),'Nyquist +4')
ck(kap[(1,0,0,0),0]==vs(-4,e[0]),'Nyquist -4')
ck(all(len(row[4])==1 for row in out.values()),'Nyquist everywhere vertical')
vc=lambda x,r:va(e[r],vs(-1,e[1])) if x==origin and r==0 else e[r]
_,out,ds,kap=flat_selected(3,zero,vc)
ck(kap[origin,0]==e[1],'L3 raw corner retained')
curl=[]
for j in range(3):
    x=(0,j,0,0)
    curl.append(va(vc(x,0),vs(-1,vc(shift(x,1,1,3),0))))
ck(curl==[vs(-1,e[1]),o,e[1]],'corner curl is nonparallel')

# All six possible (full rank, graph, trivial linear holonomy) combinations.
f=(1,2,-3)
bf=lambda x,r:vs(f[x[r]],e[r])
_,out=fields(3,lambda x,r:I,bf,flatv)
ck(all(rank(row[0])==4 and row[3]==Z for row in out.values()),'full graph / trivial holonomy')
lg=lambda x,r:g if r==0 else I
blo=lambda x,r:e[0] if r==0 else o
_,out=fields(3,lg,blo,flatv)
ck(all(rank(row[0])==1 and row[3]==Z for row in out.values()),'rank one graph / boost holonomy')
bh=lambda x,r:e[0] if r==0 else vs(f[x[r]],e[r])
_,out=fields(3,lg,bh,flatv)
ck(all(rank(row[0])==4 and row[3]==Z for row in out.values()),'full graph / boost holonomy')
_,out=fields(3,lg,zero,flatv)
ck(all(rank(row[0])==0 and len(row[4])==1 for row in out.values()),'vertical / boost holonomy')
g3=mul(g,mul(g,g))
ck(g3[0][:2]==[Q(365,27),Q(364,27)] and g3!=I,'nontrivial boost cycle')
ck(mul(g,I)==mul(I,g),'plaquette flatness is weaker than cycle descent')

# Noncommutative source append / reverse, with a genuine fixed vector.
p=eye(); p[0][1]=Q(2)
q=eye(); q[1][0]=Q(3)
ck(mul(p,q)!=mul(q,p),'noncommuting pulls')
a0=va(e[0],e[2]); a1=va(e[1],e[3]); a2=va(e[0],e[1])
source=lambda P,a,b:va(mv(P,b),vs(-1,a))
sp=source(p,a0,a1); sq=source(q,a1,a2)
ck(source(mul(p,q),a0,a2)==va(sp,mv(p,sq)),'sourced append order')
ck(source(inv(p),a1,a0)==vs(-1,mv(inv(p),sp)),'sourced reverse order')
h=e[2]
ck(source(p,va(a0,h),va(a1,h))==sp,'parallel residual solution')
ck(source(p,va(a0,h),va(a1,e[0]))!=sp,'nonparallel residual rejected')

# L2 labels: period necessary, but periods alone are insufficient.
ck(shift(origin,0,1,2)==shift(origin,0,-1,2),'L2 endpoints coincide')
ck(g!=gi and mul(g,g)!=I,'L2 distinct positive / inverse letters')
ck(mul(g,gi)==I,'L2 alternating boost positive period')
x=eye(); x[2][2]=0; x[3][3]=0; x[2][3]=1; x[3][2]=1
zz=eye(); zz[3][3]=-1
ck(mul(x,x)==I and mul(zz,zz)==I,'all L2 role periods can hold')
ck(mul(x,zz)!=mul(zz,x),'L2 plaquette can still fail')

# Rank-jump primitive, and a periodic downstream discontinuity with flat pulls.
for t in (Q(-2),Q(-1,3),Q(0),Q(1,5),Q(2)):
    b=cols([vs(t,e[0]),o,o,o]); s=cols([e[1],o,o,o])
    c,d,m=package(b,s)
    ck(col(c,0)==(e[1] if t else o),'rank-jump correlated action')
    ck(len(m)==(0 if t else 1),'rank-jump vertical dimension')
    if t:
        ck(vs(1/t,col(c,0))==vs(1/t,e[1]),'normalized graph gain')
f=(1,-2,1)
vr=lambda x,r:va(e[0],vs(f[x[0]],e[1])) if r==0 else e[r]
saved={}
for t in (Q(-1),Q(0),Q(1,7),Q(1)):
    br=lambda x,r:vs(t*f[x[0]],e[0]) if r==0 else o
    _,out,ds,kap=flat_selected(3,br,vr)
    ck(sum(f)==0,'exact affine period zero at every t')
    ck(all(rank(cols([vr(y,r) for r in range(4)]))==4 for y in out), 'raw solder stays invertible')
    if t:
        ck(all(row[3]==Z for row in out.values()),'rank-jump all sites graph off zero')
        ck(all(v==o for v in kap.values()),'rank-jump selected kappa zero off zero')
        ck(ds[(1,0,0,0)][0]==va(vs(-t,e[0]),vs(3,e[1])),'rank-jump diagonal formula')
    else:
        ck(kap[origin,0]==vs(-3,e[1]),'rank-jump selected kappa jumps at zero')
        ck(ds[(1,0,0,0)][0]==o,'rank-jump diagonal zero at zero')
    saved[t]=kap[origin,0]
ck(saved[Q(0)]!=saved[Q(1,7)]==saved[Q(1)],'actual downstream discontinuity')

# Finite simultaneous quotient saturation and complete-collapse control.
def preimage_images(b,s,W):
    block=[br+[-v[i] for v in W] for i,br in enumerate(b)]
    return [mv(s,c[:4]) for c in ker(block)]

b=cols([e[0],e[1],e[2],o]); s=cols([e[1],e[2],e[3],e[0]])
W=[]; dims=[]
for _ in range(5):
    W=span(W+preimage_images(b,s,W)); dims.append(len(W))
ck(dims==[1,2,3,4,4],'one vertical direction can force the zero common quotient')
H=span([col(sub(g,I),j) for j in range(4)])
ck(len(H)==2 and span(H+[e[0],e[1]])==H,'boost coinvariant loss is the AB plane')

# Flat mixed-Role junction: descent and graphification do not imply q_r=v_s.
ck(va(e[1],vs(-1,e[0]),e[0],vs(-1,e[1]))==o,'flat endpoint / junction cancellation')
ck(e[0]!=e[1],'flat common-origin compression fails')
print(f'PASS: {checks} exact rational assertions; no floating tolerances')
```
