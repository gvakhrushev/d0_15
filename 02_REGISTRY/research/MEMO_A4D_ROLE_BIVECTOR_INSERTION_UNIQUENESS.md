# MEMO A4D — Role-bivector insertion uniqueness

**Task:** `EXP-A4D-ROLE-BIVECTOR-ORIENTED-DENSITY-SELECTOR`  
**Execution:** PR #169  
**Status:** terminal research classification  
**Principal verdict:** `ROLE-BIVECTOR-INSERTION-UNIQUE-UP-TO-SCALE`

## 0. Result

The finite Role-typed linear-curvature insertion is uniquely selected up to one
overall multiplicative scale.

The proper/oriented Lorentz intertwiner space is exactly

\[
\operatorname{End}_{SO^+(1,3)}(\Lambda^2V)
=
\operatorname{span}_{\mathbb R}\{I,\star\},
\qquad \dim=2.
\]

The missing selector is already present in D0, but it is **not** the assertion
that an odd Role permutation is the same thing as an improper local Lorentz
frame change.

The selector is the independent finite spatial gauge/naturality principle:

\[
G_A
:=
\{\sigma\in\operatorname{Perm}(Role):\sigma(A)=A\}
\cong S_3,
\]

acting simultaneously on the three spatial Role directions, archive/site
coordinates and exterior fibres.

This group is not invented for this task:

- `ArchiveHodgeSpatialShellOperator` owns `SpatialRoleStabilizer`,
  preservation of the A-invariant spatial sector and equivariance of the
  spatial Laplacian/Hodge square;
- `A4DRoleSpatialRepresentationWeld` owns the exact A-stabilizer action on the
  spatial triad and its intertwining with the typed Role residual;
- `RoleFockPermutation` owns the signed Role action, including the odd spatial
  swaps \(B\leftrightarrow C\) and \(C\leftrightarrow D\);
- the D0 gauge definition identifies local gauge symmetry with
  combinatorial indistinguishability of outgoing-direction permutations;
- M1 catalogue invariance forbids a canonical action from inserting an
  additional preferred ordering/axis not present in the owned input.

The crucial orientation fact is that the insertion is a four-dimensional
**oriented top-cell density**. Under a simultaneous spatial Role/site
permutation \(\sigma\), the base orientation line contributes
\(\operatorname{sgn}(\sigma)\). Therefore the internal insertion map
\(K:\Lambda^2V\to\Lambda^2V\) must satisfy the sign-twisted condition

\[
\boxed{
K\,\rho_2(\sigma)
=
\operatorname{sgn}(\sigma)\,
\rho_2(\sigma)K.
}
\tag{0.1}
\]

This is not the ordinary commutant condition for a fixed-base internal
reflection.

For the two proper-Lorentz candidates,

\[
I\rho_2(\sigma)=\rho_2(\sigma)I,
\]

whereas the owned Lorentz middle-degree star obeys

\[
\star\rho_2(\sigma)
=
\operatorname{sgn}(\sigma)\,
\rho_2(\sigma)\star.
\tag{0.2}
\]

Hence every odd spatial permutation kills the \(I\) channel and preserves the
\(\star\) channel as an oriented density. Exact rational rank calculation
gives

\[
36-34=2
\quad\text{(proper Lorentz only)},
\]

and, after the sign-twisted \(B\leftrightarrow C\) condition,

\[
36-35=1,
\qquad
\ker=\mathbb R\star.
\]

Adding both spatial transposition generators of \(G_A\cong S_3\) leaves the
same one-dimensional line.

Thus

\[
\boxed{
\text{finite }e\wedge e\wedge F
\text{ insertion}
=
\mathbb R\,\star
\quad\text{up to overall scale}.
}
\]

No new symmetry primitive is required.

The exact checker is

`02_REGISTRY/research/certificates/a4d_role_spatial_stabilizer_selector_check.py`.

---

## 0.1 Pressure review of the merged two-dimensional boundary

Fresh main `041186361869da30fd88eca072ca36e760544cd3` terminally classified the
typed insertion as two-dimensional and named exactly one downstream question:

`ACTION-LEVEL-DIAGONAL-ROLE-ORIENTATION-SELECTOR-UNPROVED`.

That merged packet already observed the decisive possibility: the base
orientation sign can compensate the internal Hodge-star pseudo-sign under a
simultaneous odd Role/site relabel. It stopped because the **complete new
density transformation** and the **independent physical selector principle**
had not been supplied.

This packet closes exactly those two items and changes nothing upstream:

1. the complete density transformation is checked over all six elements of
   `SpatialRoleStabilizer ≅ S3` and all six degree-two Role faces;
2. the mandatory symmetry source is the already-owned D0 permutation-gauge /
   catalogue-invariance principle applied to the already-owned A-stabilizer
   spatial action, not a new improper-Lorentz postulate.

The exact finite identities are

\[
\epsilon(\sigma S)\,
q_\sigma(S)\,
q_\sigma(S^c)
=
\operatorname{sgn}(\sigma)\epsilon(S),
\tag{0.3}
\]

\[
\rho_2(\sigma)^T G_2\rho_2(\sigma)=G_2,
\tag{0.4}
\]

and

\[
\star\rho_2(\sigma)
=
\operatorname{sgn}(\sigma)
\rho_2(\sigma)\star.
\tag{0.5}
\]

Consequently, for the complete scalarized cell densities,

\[
\mathcal L_I(\sigma\cdot S)
=
\operatorname{sgn}(\sigma)\mathcal L_I(S),
\qquad
\mathcal L_\star(\sigma\cdot S)
=
\mathcal L_\star(S).
\tag{0.6}
\]

Thus the merged two-dimensional boundary is not contradicted at the
proper-Lorentz Hom-space level; it is **completed** at precisely its named
action-level selector boundary.

---

## 1. Owned carrier and type audit

Let

\[
V=\operatorname{RoleSpace}=Role\to\mathbb R,
\qquad
\eta=\operatorname{roleLorentzMetric}=\operatorname{diag}(+1,-1,-1,-1).
\]

| Object / map | Status | Owner / reason |
|---|---|---|
| `Role`, `RoleSpace`, `archiveRoleBasis` | OWNED | existing Role carrier/exterior lift |
| degree-two exterior carrier \(\Lambda^2V\) | OWNED | existing exterior frame lift |
| \(\eta\), `IsRoleLorentz`, `IsRoleLorentzTangent` | OWNED | A4D solder/Lorentz owners |
| `solderLegVector` | OWNED | row-to-vector map \(v_r=\eta E_r^T\) |
| `occupationComplement`, `complementOrientation` | OWNED | primal/dual cell pairing |
| one-fibre Lorentz star coefficients | OWNED | `A4DMetricStarSignatureBoundary` |
| signed Role/site action | OWNED | `RoleFockPermutation`, `ArchiveDiagonalRoleTransport` |
| `SpatialRoleStabilizer` | OWNED | `ArchiveHodgeSpatialShellOperator` |
| A-stabilizer/spatial-triad intertwiner | OWNED | `A4DRoleSpatialRepresentationWeld` |
| tangent \(\to\Lambda^2V\) weld | DERIVED-CANONICALLY | §2 |
| finite curvature extraction | DERIVED-CANONICALLY | §3 |
| complementary solder bivector | DERIVED-CANONICALLY | §4 |
| Lorentz bivector pairing \(G_2\) | DERIVED-CANONICALLY | exterior determinant pairing induced by \(\eta\) |
| proper-Lorentz commutant \(\mathbb RI\oplus\mathbb R\star\) | DERIVED-CANONICALLY | §5 + exact checker |
| sign-twisted \(G_A\) selector | DERIVED-CANONICALLY FROM OWNED SYMMETRY | §§6–7 |
| extra preferred spatial axis/order | MISSING AND FORBIDDEN AS A SELECTOR | would be an unowned catalogue choice |

There is no `ROLE-EXTERIOR-WELD-MISSING` obstruction.

---

## 2. Lorentz tangent to Role bivector

For an owned Lorentz tangent \(X\),

\[
X^T\eta+\eta X=0.
\tag{2.1}
\]

Therefore

\[
\omega_X:=\eta X
\]

is antisymmetric:

\[
\omega_X^T
=
X^T\eta
=
-\eta X
=
-\omega_X.
\tag{2.2}
\]

This is the canonical covariant two-form coefficient matrix.

Because the owned Lorentz metric satisfies \(\eta^2=I\), raising both indices
gives

\[
\beta_X:=\eta\omega_X\eta=X\eta,
\tag{2.3}
\]

and \(\beta_X\) is likewise antisymmetric. Hence

\[
\mathfrak b(X)
=
\sum_{a<b}(X\eta)_{ab}\,e_a\wedge e_b
\in\Lambda^2V.
\tag{2.4}
\]

No Euclidean inner product or arbitrary complement enters.

If \(E\eta E^T=\eta\), then

\[
\begin{aligned}
\beta_{EXE^{-1}}
&=EXE^{-1}\eta\\
&=EX\eta E^T,
\end{aligned}
\]

so

\[
\boxed{
\mathfrak b(EXE^{-1})
=
(\wedge^2E)\mathfrak b(X).
}
\tag{2.5}
\]

This is exactly the homogeneous degree-two restriction of the already-owned
exterior frame lift.

---

## 3. Exact finite curvature extraction

For an invertible Lorentz plaquette holonomy \(L\), define

\[
\boxed{
\mathcal R(L)
=
\frac12(L-L^{-1}).
}
\tag{3.1}
\]

From

\[
L\eta L^T=\eta,
\qquad \eta^2=I,
\]

one gets

\[
L^{-1}=\eta L^T\eta.
\tag{3.2}
\]

Therefore

\[
\mathcal R(L)^T\eta+\eta\mathcal R(L)=0,
\tag{3.3}
\]

so \(\mathcal R(L)\in\mathfrak{so}(\eta)\) exactly, not just to first
order.

Conjugation is exact:

\[
\mathcal R(ELE^{-1})
=
E\mathcal R(L)E^{-1}.
\tag{3.4}
\]

The finite curvature bivector is

\[
C(L):=\mathfrak b(\mathcal R(L))\in\Lambda^2V.
\tag{3.5}
\]

If \(L=e^X\),

\[
\mathcal R(e^X)
=
\sinh X
=
X+\frac{X^3}{3!}+\cdots,
\tag{3.6}
\]

so the first jet is exactly \(X\) and there is no quadratic term.

This is superior for the present purpose to:

- \(L-I\), which is not exactly Lorentz-tangent at finite \(L\);
- a coordinate antisymmetric projection, which is not the intrinsic
  Lorentz-tangent projection;
- \(\log L\), which needs a local branch.

---

## 4. Complementary-face solder bivector and orientation bookkeeping

Let the curvature face be the degree-two Role occupation state

\[
S=\{r,s\},
\qquad
S^c=\{u,v\}.
\]

The internal complementary solder bivector is

\[
B_{S^c}(e,x)
=
v_u(e,x)\wedge v_v(e,x)
\in\Lambda^2V.
\tag{4.1}
\]

The order \(u<v\) here is only the fixed Role basis order used to write the
blade. The **base top-cell orientation** is a separate factor

\[
\epsilon_{\rm base}(S)
=
\operatorname{complementOrientation}(S).
\tag{4.2}
\]

It must be used exactly once.

This separation repairs a tempting double-count:

- do **not** hide `complementOrientation` inside \(B_{S^c}\) and multiply by
  it again in the density;
- \(B_{S^c}\) is an internal bivector;
- \(\epsilon_{\rm base}\) records the orientation of the base
  face-complement pair.

The same-face hostile candidate

\[
v_r\wedge v_s
\]

is wrong for the intended top-cell insertion because its base degree repeats the
same two face directions already occupied by curvature. The complementary face
is what supplies all four base directions exactly once.

---

## 5. Proper-Lorentz Hom-space

Let \(G_2\) be the degree-two bilinear form induced from \(\eta\):

\[
G_2(u\wedge v,p\wedge q)
=
\eta(u,p)\eta(v,q)-\eta(u,q)\eta(v,p).
\tag{5.1}
\]

This is the typed Lorentz exterior pairing, not the false surrogate
\(\operatorname{tr}(X\eta Y\eta)\).

On the ordered basis

\[
(AB,AC,AD,BC,BD,CD)
\]

the six boost/rotation generators of \(\mathfrak{so}(1,3)\) give a rational
linear commutant system with 36 unknowns and rank 34. Therefore

\[
\dim
\operatorname{End}_{\mathfrak{so}(1,3)}(\Lambda^2V)
=
2.
\tag{5.2}
\]

The two basis directions are

\[
I,
\qquad
\star,
\]

with

\[
\star^2=-I.
\tag{5.3}
\]

Thus proper Lorentz covariance alone **does not** give uniqueness.

---

## 6. The principle that closes the selector

### 6.1 What is forced before the insertion

D0 already owns the causal/spatial split: one distinguished A direction and a
three-dimensional spatial Role sector. On the finite archive carrier the
natural spatial symmetry is

\[
G_A
=
\operatorname{Stab}(A)
\subset\operatorname{Perm}(Role).
\]

This is not an abstract desired symmetry. The repository literally owns:

`ArchiveHodgeSpatialShellOperator`

\[
\operatorname{SpatialRoleStabilizer}
=
\{\sigma:\operatorname{Perm}(Role)\mid\sigma(A)=A\},
\]

together with preservation of the A-invariant spatial sector and commutation
with the spatial Laplacian/Hodge square.

`A4DRoleSpatialRepresentationWeld` owns the same stabilizer on the spatial
triad and proves the exact intertwining/equivariance of the typed Role-spatial
readout.

Hence \(B,C,D\) may be permuted inside the finite spatial Role carrier without
adding a new geometric datum.

### 6.2 Why this symmetry is mandatory for a canonical D0 action

D0's own gauge definition is permutation-theoretic: a local outgoing-direction
permutation that does not change the distinguishing structure is gauge
indistinguishability; the continuous gauge group is downstream packaging.

The entry contract also imposes catalogue invariance: a verdict cannot depend on
a privileged external catalogue.

Therefore an action claimed to be constructed solely from the owned A4D
spatial data must be natural under \(G_A\). Choosing one ordering or one
spatial axis to break that action without an additional owned field/section
would add exactly the missing catalogue datum the task forbids.

This is the missing physical principle from the provisional analysis:

\[
\boxed{
\texttt{SPATIAL-ROLE-GAUGE-NATURALITY}.
}
\]

It is independent of local Lorentz covariance. No identification of those two
symmetries is made.

---

## 7. Why the orientation sign selects \(\star\), not \(I\)

This is the load-bearing calculation.

For an odd spatial permutation such as

\[
\sigma=(B\ C)\in G_A,
\]

the internal bivector representation is \(\rho_2(\sigma)\). Algebraically,

\[
\rho_2(\sigma)\star
=
-\star\rho_2(\sigma).
\tag{7.1}
\]

If one incorrectly treats \(\sigma\) as a **fixed-base internal improper
Lorentz reflection**, then the required condition is the ordinary commutant

\[
K\rho_2(\sigma)=\rho_2(\sigma)K,
\tag{7.2}
\]

and the surviving line is \(\mathbb RI\).

That calculation is correct but it is **not the physical Role/site relabeling
being tested here**.

For a simultaneous Role/site relabeling, the base top-cell orientation also
moves. The owned complement/fermion-sign machinery gives the familiar
orientation pseudo-sign: odd \(\sigma\) contributes

\[
\operatorname{sgn}(\sigma)=-1
\]

to the oriented top-cell line. Therefore invariance of the scalarized oriented
cell density requires

\[
\boxed{
K\rho_2(\sigma)
=
\operatorname{sgn}(\sigma)\rho_2(\sigma)K.
}
\tag{7.3}
\]

For \(K=I\), (7.3) fails on every odd spatial permutation.

For \(K=\star\), (7.1) is exactly (7.3).

The exact rational system therefore has:

\[
\begin{array}{c|c|c}
\text{requirements} & \text{rank} & \text{solution space}\\
\hline
\mathfrak{so}(1,3) & 34 & \mathbb RI\oplus\mathbb R\star\\
\mathfrak{so}(1,3)+\text{fixed-base odd commutation} & 35 & \mathbb RI\\
\mathfrak{so}(1,3)+\text{oriented }(B\ C)\text{ twist} & 35 & \mathbb R\star\\
\mathfrak{so}(1,3)+\text{full oriented }G_A & 35 & \mathbb R\star
\end{array}
\tag{7.4}
\]

An even spatial 3-cycle alone leaves dimension 2. Thus the odd component is
genuinely load-bearing, and the exact base-orientation sign determines which
one-dimensional line survives.

The action-level transformation is also checked directly, not only through the
Hom-space equation. The exact certificate enumerates all six elements of
\(G_A\cong S_3\) and all six Role two-faces (36 explicit face/group cases).
For every \(\sigma\) and face \(S\), the complement orientation obeys the
finite identity

\[
\epsilon_{\sigma S}\,q_S(\sigma)\,q_{S^c}(\sigma)
=
\operatorname{sgn}(\sigma)\,\epsilon_S,
\tag{7.5}
\]

while \(G_2\) is invariant and
\(\star\rho_2(\sigma)=\operatorname{sgn}(\sigma)\rho_2(\sigma)\star\).
Consequently the complete identity-channel density transforms by
\(\operatorname{sgn}(\sigma)\), whereas the complete star-channel density is
invariant in every one of the 36 cases. This discharges the exact
\`ACTION-LEVEL-DIAGONAL-ROLE-ORIENTATION-SELECTOR-UNPROVED\` boundary left by
the previous main packet.

---

## 8. Symmetry implication/status table

| Operation | Base moves? | Internal fibre moves? | Owned / mandatory? | Density condition | Consequence |
|---|---:|---:|---|---|---|
| proper local Lorentz frame | no | yes | owned | ordinary intertwiner | leaves \(I,\star\) |
| fixed-base internal \(\det=-1\) Lorentz reflection | no | yes | algebraically allowed but not independently mandatory | ordinary intertwiner | would select \(I\) |
| simultaneous spatial Role/site relabel \(G_A\) | yes | yes | owned finite symmetry; mandatory by gauge/naturality + catalogue invariance | sign-twisted intertwiner (7.3) | selects \(\star\) |
| base-cell orientation reversal alone | yes | no | orientation bookkeeping | flips base orientation line | not an internal Hom-space selector by itself |
| full arbitrary Role relabel moving A | yes | yes | owned algebraic action, but does not preserve the A-spatial sector in general | not required here | not used |

Thus:

\[
\text{spatial Role gauge}
\neq
\text{local Lorentz gauge},
\]

and

\[
\text{simultaneous odd Role/site relabel}
\neq
\text{fixed-base improper internal reflection}.
\]

The uniqueness proof relies on the first distinction, not on erasing it.

---

## 9. The two candidates and the survivor

For a face \(S\), define the finite curvature bivector

\[
C_S(x)
=
\mathfrak b
\left(
\frac12(L_S(x)-L_S(x)^{-1})
\right).
\tag{9.1}
\]

The two proper-Lorentz candidate scalarized cell densities are exactly those
required by the task:

\[
\mathcal L_0(S,x)
=
\epsilon_{\rm base}(S)
G_2\bigl(B_{S^c}(e,x),C_S(x)\bigr),
\tag{9.2}
\]

and

\[
\mathcal L_\star(S,x)
=
\epsilon_{\rm base}(S)
G_2\bigl(B_{S^c}(e,x),\star C_S(x)\bigr).
\tag{9.3}
\]

Both are local, proper-Lorentz covariant and vanish for flat linear holonomy.

Under the mandatory simultaneous spatial Role/site action:

- \(\mathcal L_0\) is odd under an odd spatial transposition and therefore
  fails scalar density invariance;
- \(\mathcal L_\star\) receives the internal \(\star\) pseudo-sign which
  cancels the base orientation pseudo-sign and is invariant.

Therefore the unique finite insertion density is

\[
\boxed{
\mathcal L_{\rm lin-curv}(S,x)
=
c\,
\epsilon_{\rm base}(S)
G_2\bigl(
B_{S^c}(e,x),
\star\mathfrak b(\mathcal R(L_S(x)))
\bigr),
}
\tag{9.4}
\]

with one undetermined overall scale \(c\).

This task does not select \(c\).

---

## 10. Flat constitutive compatibility

At

\[
L_S=I,
\qquad
b=0,
\qquad
\Omega=0,
\]

one has

\[
\mathcal R(I)=0,
\qquad
C_S=0,
\]

hence

\[
\mathcal L_0
=
\mathcal L_\star
=
0.
\tag{10.1}
\]

With curvature fixed at identity, coframe variation of either density also
contains the zero curvature factor, so no additional flat coframe constitutive
first jet is generated.

Therefore the existing matter/flux first response \(H(e)\) remains unchanged.

This compatibility test does not itself select the channel; the selector is §7.

---

## 11. Theorem-ready propositions

1. **Lorentz tangent lowering is antisymmetric.**  
   `IsRoleLorentzTangent X` implies \((\eta X)^T=-\eta X\).

2. **Canonical Role-bivector landing.**  
   Every Lorentz tangent determines \(\mathfrak b(X)\in\Lambda^2V\) using
   \(X\eta\), with no Euclidean metric.

3. **Bivector naturality.**  
   \[
   \mathfrak b(EXE^{-1})=(\wedge^2E)\mathfrak b(X).
   \]

4. **Finite Lorentz inverse.**  
   `IsRoleLorentz L` implies \(L^{-1}=\eta L^T\eta\).

5. **Finite curvature tangent landing.**  
   \(\mathcal R(L)=\tfrac12(L-L^{-1})\) is exactly Lorentz-tangent.

6. **Finite curvature conjugation covariance.**  
   \[
   \mathcal R(ELE^{-1})=E\mathcal R(L)E^{-1}.
   \]

7. **Correct first jet.**  
   \[
   \mathcal R(e^X)=X+O(X^3).
   \]

8. **Complementary solder top-cell typing.**  
   \(B_{S^c}=v_u\wedge v_v\) supplies the two base directions absent from
   the curvature face.

9. **Same-face no-go.**  
   \(v_r\wedge v_s\) repeats the curvature base directions and fails the
   four-direction top-cell typing.

10. **Proper-Lorentz commutant.**  
    \[
    \operatorname{End}_{\mathfrak{so}(1,3)}(\Lambda^2V)
    =
    \mathbb RI\oplus\mathbb R\star.
    \]

11. **Middle-degree Lorentz star.**  
    \[
    \star^2=-I.
    \]

12. **A-stabilizer is an owned spatial symmetry.**  
    `SpatialRoleStabilizer` acts on the spatial triad, preserves the
    A-invariant sector and intertwines the owned spatial Role operators.

13. **Odd spatial star pseudoequivariance.**  
    For \(\sigma\in G_A\),
    \[
    \star\rho_2(\sigma)
    =
    \operatorname{sgn}(\sigma)\rho_2(\sigma)\star.
    \]

14. **Oriented-density intertwiner law.**  
    Simultaneous Role/site relabel covariance of
    \(\epsilon_{\rm base}G_2(B,K C)\) is equivalent to
    \[
    K\rho_2(\sigma)
    =
    \operatorname{sgn}(\sigma)\rho_2(\sigma)K.
    \]

15. **One odd spatial swap is sufficient.**  
    Proper Lorentz covariance plus the oriented \(B\leftrightarrow C\)
    density law has a one-dimensional solution space.

16. **The unique line is \(\star\).**  
    That solution space equals \(\mathbb R\star\).

17. **Even spatial permutations are insufficient.**  
    Adding only the even spatial 3-cycle leaves the two-dimensional
    \(I,\star\) space.

18. **Fixed-base improper reflection is a different test.**  
    Ordinary commutation with the same odd matrix selects \(I\), proving that
    fixed-base internal reflection and simultaneous Role/site relabeling must
    not be conflated.

19. **Flat-curvature vanishing.**  
    \(L=I\Rightarrow\mathcal L_{\rm lin-curv}=0\).

20. **Flat coframe-jet neutrality.**  
    At fixed flat curvature, the first coframe variation of the selected
    linear-curvature density is zero.

---

## 12. Mandatory negative controls

The exact certificate checks all load-bearing controls:

- proper Lorentz alone gives rank 34 / dimension 2;
- odd spatial swap with **ordinary** commutation gives dimension 1 but the
  wrong line \(I\), and is retained only as a hostile distinction;
- odd spatial swap with the **orientation-twisted** density law gives rank 35 /
  dimension 1 and the line \(\star\);
- full \(G_A\) gives the same \(\star\) line;
- an even spatial 3-cycle alone leaves dimension 2;
- omitting the base orientation sign is explicitly rejected;
- \(\star^2=-I\) and its odd-swap anti-commutation are exact;
- no fake function-space enumeration is used;
- no zero-coframe covariance proof is used;
- no same-face solder replacement is used;
- no false \(\operatorname{tr}(X\eta Y\eta)\) invariant is used;
- flat connection makes both candidate densities vanish;
- no quadratic-curvature \(F^2\) action is introduced.

---

## 13. Terminal disposition

The provisional blocker

`ACTION-LEVEL-DISCONNECTED-LORENTZ-SYMMETRY-OWNER-MISSING`

is **not** needed and is retired.

The successful principle is instead the already-owned combination

\[
\boxed{
\text{forced A/spatial split}
+
\text{SpatialRoleStabilizer}
+
\text{D0 permutation-gauge definition}
+
\text{M1 catalogue invariance}
+
\text{base orientation line}.
}
\]

It independently enforces the sign-twisted spatial Role/site naturality of the
top-cell density and reduces the proper-Lorentz two-dimensional Hom-space to

\[
\boxed{\mathbb R\star.}
\]

Therefore the principal task verdict is

\[
\boxed{
\texttt{ROLE-BIVECTOR-INSERTION-UNIQUE-UP-TO-SCALE}.
}
\]

There is **no remaining selector/weld blocker inside the scope of this task**.

The only surviving freedom is the overall multiplicative normalization of the
already-selected density. Fixing that scale, varying the action, or identifying
a downstream continuum field equation are separate tasks and are not claimed
here.
