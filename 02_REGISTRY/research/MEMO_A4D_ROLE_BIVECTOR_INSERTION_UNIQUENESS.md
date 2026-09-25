# MEMO A4D — Role-bivector insertion uniqueness

**Task:** `EXP-A4D-ROLE-BIVECTOR-INSERTION-UNIQUENESS`  
**Status:** terminal research classification  
**Principal verdict:** `ROLE-BIVECTOR-INSERTION-TWO-DIMENSIONAL`

## 1. Verdict

The finite Role-typed linear-curvature insertion is constructible on the owned
carrier. There is no `ROLE-EXTERIOR-WELD-MISSING` obstruction.

For the orientation-preserving Lorentz component the insertion space is exactly

\[
\boxed{
\operatorname{span}_{\mathbb R}\{I,\star\},
\qquad \dim=2.
}
\]

The exact audited six-dimensional middle-degree calculation is therefore a
coordinate certificate for the actual owned carrier
\(\bigwedge^2\operatorname{RoleSpace}\), not a surrogate.

A fixed-base internal orientation-reversing Lorentz transformation does reduce
the commutant to one dimension, but it keeps the identity channel and removes
the Hodge-star channel. With the finite densities of Section 8, the identity
channel is the Holst-like contraction and the star channel is the
Palatini-like/internal-epsilon contraction (up to the stated sign convention).
Therefore the disconnected internal component is not an already-owned route to
the Einstein/Palatini-like branch; it selects the other linear-curvature
channel.

The owned simultaneous Role/site relabeling is a different operation. Its base
orientation sign can compensate an internal Hodge-star pseudo-sign, so it must
be tested at the **complete action-density level** rather than replaced by a
fixed-base internal reflection. Current owners prove the required
pseudoequivariance ingredients, but not yet the transformation theorem of the
new density itself or a physical action-selector principle.

Accordingly, under the symmetries actually established for this insertion, the
correct terminal classification is

\[
\boxed{\texttt{ROLE-BIVECTOR-INSERTION-TWO-DIMENSIONAL}.}
\]

This closes the typing/Hom-space problem without inventing a selector.

---

## 2. Owned carrier/type table

| Object / map | Status | Repository owner / derivation |
|---|---|---|
| `Role` | OWNED | finite four-role carrier |
| `RoleSpace = Role → ℝ` | OWNED | `ArchiveExteriorFrameLift.lean` |
| `archiveRoleBasis` | OWNED | `ArchiveExteriorFrameLift.lean` |
| `RoleExterior = ExteriorAlgebra ℝ RoleSpace` | OWNED | `ArchiveExteriorFrameLift.lean` |
| homogeneous \(\Lambda^2V\) / exterior-power carrier | OWNED | Mathlib exterior power used by the archive exterior frame lift |
| `roleLorentzMetric = diag(+---)` | OWNED | `A4DSolderMetricCompletion.lean` |
| `IsRoleLorentz` | OWNED | \(L\eta L^T=\eta\) |
| `IsRoleLorentzTangent` | OWNED | \(X^T\eta+\eta X=0\) |
| `solderLegVector` | OWNED | \(v_r=\eta E_r^T\), `ArchiveAffineExteriorLink.lean` |
| `occupationComplement` | OWNED | `A4DPrimalDualCellPairing.lean` |
| `complementOrientation` | OWNED | same owner |
| `flatLorentzStarCoeff` | OWNED | one-fibre Lorentz star coefficient, `A4DMetricStarSignatureBoundary.lean` |
| located primal/dual star | OWNED | `A4DLocatedTopologicalStar.lean`; separate from the one-fibre metric star |
| Lorentz-restricted affine exterior connection | OWNED | `LorentzAffineExteriorConnection` |
| tangent \(X\mapsto\Lambda^2V\) weld | DERIVED-CANONICALLY | Sections 3–4 below; uses only \(\eta\) and exterior power |
| finite curvature extraction \(\mathcal R(L)\) | DERIVED-CANONICALLY | Section 4 |
| Lorentz bivector pairing \(G_2\) | DERIVED-CANONICALLY | `exteriorPairingFromBilin 2 roleLorentzMetric.toBilin'` |
| complementary solder bivector | DERIVED-CANONICALLY | Section 5 |
| proper-Lorentz Hom-space basis \(I,\star\) | DERIVED-CANONICALLY | exact-rational audited commutant + owned degree-two representation |
| action-level requirement of fixed-base \(\det=-1\) internal-frame invariance | MISSING | the single selector blocker |

No Euclidean inner product, continuum epsilon tensor, matrix logarithm, arbitrary
complement, or new exterior carrier is needed.

---

## 3. Lorentz tangent → Role bivector map

Put \(V=\operatorname{RoleSpace}\) and \(\eta=\operatorname{roleLorentzMetric}\).
For an owned Lorentz tangent \(X\),

\[
X^T\eta+\eta X=0.
\tag{3.1}
\]

The brief's natural lowered object is

\[
\omega_X:=\eta X.
\tag{3.2}
\]

The already-owned theorem `lorentzTangent_flat_solder_skew` is exactly

\[
\omega_X+\omega_X^T=0.
\tag{3.3}
\]

Thus \(\omega_X\) is a canonical covariant Role two-form. The crucial typing
point is that the actual archive degree-two carrier is a **bivector** carrier.
Because \(\eta^2=I\) is owned, raise both indices canonically:

\[
\beta_X:=\eta\omega_X\eta=X\eta.
\tag{3.4}
\]

The owned theorem `lorentzTangent_right_condition` gives

\[
X\eta+(X\eta)^T=0,
\tag{3.5}
\]

so \(\beta_X\) is antisymmetric as well. In the ordered archive Role basis it
defines

\[
\mathfrak b(X)
  :=\sum_{a<b}(X\eta)_{ab},e_a\wedge e_b
  \in\Lambda^2V.
\tag{3.6}
\]

The basis in (3.6) is only a coordinate certificate. Intrinsically the map is
the metric musical identification of the antisymmetric two-form \(\eta X\)
with the degree-two exterior vector carrier.

If \(E\eta E^T=\eta\) and \(X'=EXE^{-1}\), then

\[
\beta_{X'}
 =EXE^{-1}\eta
 =EX\eta E^T
 =E\beta_XE^T,
\tag{3.7}
\]

hence

\[
\boxed{
\mathfrak b(EXE^{-1})=(\wedge^2E)\mathfrak b(X).
}
\tag{3.8}
\]

This is the required representation-theoretic naturality. There is no hidden
Euclidean metric and no arbitrary basis/complement choice.

For the **physical frame/gauge covariance** one must respect the repository's
two conventions. The raw solder uses the active right action
\[
\Theta\mapsto\Theta E.
\]
Therefore its internal vector leg
\[
v_r=\eta\Theta_r^T
\]
transforms as
\[
v_r\mapsto E^{-1}v_r.
\]
The owned affine gauge law is
\[
P\mapsto hPh^{-1}.
\]
Thus the same physical local-frame change is represented on the affine gauge
side by
\[
h.\mathrm{lin}=E^{-1}.
\]
Then
\[
P\mapsto E^{-1}PE,
\qquad
\mathcal R(P)\mapsto E^{-1}\mathcal R(P)E,
\]
and the bivector weld obeys
\[
\mathfrak b(E^{-1}XE)
=
(\wedge^2E^{-1})\mathfrak b(X),
\]
exactly matching the transformation of the complementary solder bivector.
Using the same matrix direction for both the raw right frame and affine
conjugation would be a convention error.

Compatibility with the owned exterior-frame lift is immediate: that lift is
literally the exterior-algebra functor, and its homogeneous degree-two
restriction is `exteriorPower.map 2 E`.

---

## 4. Exact finite curvature extraction

For an invertible Lorentz plaquette linear holonomy \(L\), define

\[
\boxed{
\mathcal R(L):=\frac12(L-L^{-1}).
}
\tag{4.1}
\]

From \(L\eta L^T=\eta\) and \(\eta^2=I\),

\[
L^{-1}=\eta L^T\eta.
\tag{4.2}
\]

Therefore

\[
\begin{aligned}
\mathcal R(L)^T\eta+\eta\mathcal R(L)
&=\frac12
\left(L^T\eta-\eta L+\eta L-L^T\eta\right)\\
&=0.
\end{aligned}
\tag{4.3}
\]

So \(\mathcal R(L)\) lands **exactly** in the owned Lorentz tangent algebra,
and

\[
C(L):=\mathfrak b(\mathcal R(L))\in\Lambda^2V
\tag{4.4}
\]

is a fully typed finite curvature bivector.

For any Lorentz frame \(E\),

\[
\mathcal R(ELE^{-1})
 =E\mathcal R(L)E^{-1},
\tag{4.5}
\]

hence by (3.8)

\[
C(ELE^{-1})=(\wedge^2E)C(L).
\tag{4.6}
\]

Near the identity, if \(L=e^X\),

\[
\mathcal R(e^X)
 =\frac12(e^X-e^{-X})
 =\sinh X
 =X+\frac{X^3}{3!}+\cdots .
\tag{4.7}
\]

Thus its first jet is exactly \(X\) and there is no quadratic correction.

Controls:

- \(L-I\) does not lie in the Lorentz tangent algebra at finite \(L\).
- A raw coordinate antisymmetric projection is not the needed conjugation-natural
  tangent extraction unless the Lorentz metric placement is supplied explicitly.
- \(\log L\) is only local and requires branch data.
- (4.1) is global on the invertible Lorentz group, algebraic, branch-free and
  exactly conjugation-equivariant.

---

## 5. Complementary-face solder bivector

Let the curvature live on an oriented base face
\(S=\{r,s\}\). The owned occupation complement gives the two missing roles

\[
S^c=\{u,v\}.
\tag{5.1}
\]

At site \(x\), use the actual owned internal solder legs

\[
v_u(x)=\operatorname{solderLegVector}(N,e,x,u),
\qquad
v_v(x)=\operatorname{solderLegVector}(N,e,x,v).
\tag{5.2}
\]

Define

\[
B_{S^c}(e,x):=v_u(x)\wedge v_v(x)\in\Lambda^2V,
\tag{5.3}
\]

with the ordered sign fixed by `complementOrientation S`. This is local and
uses no imported continuum \(\epsilon_{\mu\nu\rho\sigma}\).

The mandatory hostile control is decisive. Using the same-face bivector
\(v_r\wedge v_s\) assigns the two coframe base legs to the same two base
directions already occupied by the curvature 2-face. The intended top-cell
product then repeats base directions instead of occupying all four roles.
Equivalently, in exterior base degree it has the wrong support for
\(2+2=4\). The complementary face occupies every Role direction exactly once
and is the finite cubical analogue required by the target
\(e\wedge e\wedge F\).

---

## 6. Proper-Lorentz Hom-space and canonical pairing

The metric-induced degree-two pairing is already canonically available from

\[
G_2
:=
\operatorname{exteriorPairingFromBilin}
\bigl(2,\eta^{\flat}\bigr).
\tag{6.1}
\]

For simple blades,

\[
G_2(u\wedge v,p\wedge q)
=
\eta(u,p)\eta(v,q)-\eta(u,q)\eta(v,p).
\tag{6.2}
\]

The generic theorem `exteriorPairingFromBilin_natural` supplies its exact
frame naturality. Hence \(G_2\) is the correct Lorentz bivector contraction;
the previously rejected
\(\operatorname{tr}(X\eta Y\eta)\) is not substituted for it.

The owned one-fibre Lorentz star is determined in the archive subset basis by

\[
\operatorname{flatLorentzStarCoeff}(S)
=
\operatorname{complementOrientation}(S)
\operatorname{flatLorentzSubsetWeight}(S).
\tag{6.3}
\]

On middle degree,

\[
\star^2=-I.
\tag{6.4}
\]

The audited exact-rational commutant calculation on the six basis blades has
rank \(34\) in \(36\) unknowns. Since the archive exterior-frame lift
restricts to precisely the same \(\wedge^2\) representation, this transports
without changing the representation:

\[
\boxed{
\operatorname{End}_{SO^+(1,3)}(\Lambda^2V)
=
\operatorname{span}_{\mathbb R}\{I,\star\}.
}
\tag{6.5}
\]

Therefore proper/oriented Lorentz covariance alone leaves exactly two insertion
directions. Any derivation returning one dimension under proper Lorentz alone
has imposed an extra symmetry.

---

## 7. Role/orientation symmetry classification

The following operations must remain distinct.

| Operation | What moves | Owned status | Effect on middle-degree \(\star\) | What it proves |
|---|---|---|---|---|
| proper local Lorentz frame | internal fibre; raw solder and affine gauge use the inverse convention of Section 3 | owned algebraically | commutes | leaves the two channels \(I,\star\) |
| fixed-base internal \(\det=-1\) Lorentz reflection | internal fibre only | algebraically admitted by `IsRoleLorentz`; not owned as mandatory action gauge symmetry | anticommutes | keeps identity/Holst-like, removes star/Palatini-like |
| simultaneous signed Role/site relabeling | fibre labels and archive/base directions together | owned | located star is pseudoequivariant with \(\operatorname{sgn}\sigma\) | distinct from local Lorentz; full new density transformation still needs an action-level theorem |
| base-cell orientation reversal | base orientation bookkeeping | owned combinatorially | not by itself an internal commutant condition | can compensate or expose an internal pseudo-sign only after the complete density is transformed |

For the explicit odd spacelike fixed-base reflection \(P_{BC}\),

\[
P_{BC}\eta P_{BC}^T=\eta,
\qquad
\det P_{BC}=-1,
\]

and the audited commutant calculation gives

\[
\operatorname{End}_{\langle SO^+(1,3),P_{BC}\rangle}(\Lambda^2V)
=
\mathbb R I,
\]

with

\[
P_{BC}^{(2)}\star=-\star P_{BC}^{(2)}.
\]

This algebraic statement is exact, but its physical interpretation is crucial:
it removes the star/Palatini-like channel rather than selecting it.

The repository separately owns, for simultaneous Role/site transport,

\[
JQ_\sigma
=
\operatorname{sgn}(\sigma)Q_\sigma J.
\]

That theorem shows why a diagonal Role/site relabel cannot be replaced by a
fixed-base reflection. For an odd spatial relabel an additional base-orientation
sign is present. Whether the complete finite density
\(\varepsilon_S G_2(B_{S^c},TC_S)\) is scalar for \(T=I\), for
\(T=\star\), or for a particular combination is therefore a separate
action-level calculation.

No such density-level selector theorem is claimed here.

---

## 8. Explicit finite densities

For an oriented curvature face \(S\) and its complementary face \(S^c\),
put

\[
C_S:=C(L_S)
=
\mathfrak b\!\left(
\frac12(L_S-L_S^{-1})
\right),
\tag{8.1}
\]

where \(L_S\) is the based linear plaquette holonomy, and let
\(B_{S^c}\) be (5.3). With the owned base complement orientation coefficient

\[
\varepsilon_S:=\operatorname{complementOrientation}(S),
\tag{8.2}
\]

the two proper-Lorentz-equivariant local finite densities are

\[
\boxed{
\mathcal L_I(S,x)
=
\varepsilon_S\,
G_2\bigl(B_{S^c}(e,x),C_S(x)\bigr)
}
\tag{8.3}
\]

and

\[
\boxed{
\mathcal L_\star(S,x)
=
\varepsilon_S\,
G_2\bigl(B_{S^c}(e,x),\star C_S(x)\bigr).
}
\tag{8.4}
\]

Both are:

- local to the face/top-cell data used to construct them;
- exactly covariant under proper local Lorentz frame transformations **after**
  the raw-frame/affine-gauge inverse convention of Section 3 is matched;
- consistently oriented by the existing complement machinery;
- zero when the linear plaquette holonomy is identity.

Up to the fixed sign convention, \(\mathcal L_I\) is the finite Holst-like
metric contraction while \(\mathcal L_\star\) is the finite
Palatini-like/internal-epsilon contraction.

Under a fixed-base internal \(\det=-1\) Lorentz transformation,
\(\mathcal L_I\) is a scalar while \(\mathcal L_\star\) carries the internal
orientation pseudo-sign. Thus imposing that disconnected internal symmetry
would delete the Palatini-like \(\star\) channel. It is therefore a
conditional algebraic reduction, not the missing Einstein selector.

The simultaneous odd Role/site relabel is a different test because the base
orientation also transforms. Its full action-density sign is left as the
single downstream selector calculation rather than guessed from the internal
commutant alone.

No claim is made here about a fitted coefficient, an \(F^2\) action, continuum
Einstein equations, or a time interpretation.

---

## 9. Flat \(H(e)\) compatibility

Set

\[
L_S=I,\qquad b=0,\qquad\Omega=0.
\tag{9.1}
\]

Then

\[
\mathcal R(I)=0,
\qquad
C_S=0,
\tag{9.2}
\]

and therefore

\[
\mathcal L_I=\mathcal L_\star=0.
\tag{9.3}
\]

Moreover, with curvature held flat, variation of either density with respect
to the coframe alone still carries the zero factor \(C_S\). Hence this new
linear-curvature sector does not create an additional flat constitutive first
variation. The already-owned matter/flux first response \(H(e)\) remains the
relevant flat response.

Consequently

\[
\boxed{
\text{flat }H(e)\text{ compatibility does not choose }I\text{ versus }\star.
}
\tag{9.4}
\]

---

## 10. Theorem-ready propositions

1. **Tangent lowering is skew.**  
   If `IsRoleLorentzTangent X`, then
   \((\eta X)^T=-\eta X\).

2. **Tangent raising is skew.**  
   If `IsRoleLorentzTangent X`, then
   \((X\eta)^T=-X\eta\).

3. **Canonical bivector landing.**  
   Every owned Lorentz tangent defines
   \(\mathfrak b(X)\in\Lambda^2V\) by the antisymmetric coefficients
   \(X\eta\), with no Euclidean metric.

4. **Bivector equivariance.**  
   For `IsRoleLorentz E`,
   \[
   \mathfrak b(EXE^{-1})=(\wedge^2E)\mathfrak b(X).
   \]
   Under the owned physical right-frame convention, taking
   \(h.\mathrm{lin}=E^{-1}\) makes both the solder bivector and based
   curvature bivector transform by \(\wedge^2E^{-1}\).

5. **Finite Lorentz inverse formula.**  
   If `IsRoleLorentz L`, then
   \[
   L^{-1}=\eta L^T\eta.
   \]

6. **Finite extraction lands in the tangent algebra.**  
   For
   \(\mathcal R(L)=\tfrac12(L-L^{-1})\),
   `IsRoleLorentzTangent (R L)`.

7. **Finite extraction is conjugation-equivariant.**  
   \[
   \mathcal R(ELE^{-1})=E\mathcal R(L)E^{-1}.
   \]

8. **Finite extraction has the correct first jet.**  
   If \(L=e^X\), then
   \[
   \mathcal R(L)=\sinh X=X+O(X^3).
   \]

9. **Complementary solder bivector has top-cell support.**  
   For a degree-two face \(S\), the two solder legs indexed by
   \(S^c\) supply the missing base degree and define
   \(B_{S^c}\in\Lambda^2V\).

10. **Same-face hostile control.**  
    Using the solder legs indexed by \(S\) repeats the curvature base
    directions and does not provide the intended degree-four
    \(e\wedge e\wedge F\) top-cell structure.

11. **Lorentz exterior pairing is canonical.**  
    `exteriorPairingFromBilin 2 roleLorentzMetric.toBilin'` is invariant
    under the corresponding Lorentz exterior action.

12. **Middle-degree star squares to minus identity.**  
    The owned flat Lorentz star coefficients give
    \(\star^2=-I\) on \(\Lambda^2V\).

13. **Proper-Lorentz insertion commutant is two-dimensional.**  
    \[
    \operatorname{End}_{SO^+(1,3)}(\Lambda^2V)
    =\mathbb RI\oplus\mathbb R\star.
    \]

14. **Odd internal reflection removes the star commutant direction.**  
    For the fixed-base internal \(B\leftrightarrow C\) reflection,
    \[
    P_{BC}^{(2)}\star=-\star P_{BC}^{(2)},
    \]
    and the augmented commutant is \(\mathbb RI\).

15. **Flat-curvature vanishing.**  
    At \(L=I\), both (8.3) and (8.4) vanish identically.

16. **Flat-coframe first-variation neutrality.**  
    At fixed \(L=I\), the first coframe variation of both
    linear-curvature densities is zero, so the test cannot select between
    the two channels.

17. **Role relabel is not a fixed-base local-frame theorem.**  
    The owned diagonal signed Role/site action and its
    \(\operatorname{sgn}(\sigma)\) star pseudoequivariance do not imply
    invariance under an internal orientation reversal with the base face held
    fixed.

18. **Disconnected fixed-base selection is branch-sensitive.**  
    Adding a fixed-base odd internal reflection leaves the identity/Holst-like
    channel and removes the star/Palatini-like channel; therefore that
    disconnected symmetry cannot be introduced merely to obtain the
    Einstein-like branch.

These propositions are research/theorem-ready statements; this task adds no
Lean.

---

## 11. Exactly one remaining selector question

The insertion classification itself is closed at dimension two. The one
remaining question before any uniqueness claim is

\[
\boxed{
\texttt{ACTION-LEVEL-DIAGONAL-ROLE-ORIENTATION-SELECTOR-UNPROVED}
}
\]

D0 must evaluate the **complete finite density** under an owned odd spatial
Role relabel acting simultaneously on

- the base face and its complement orientation,
- the solder legs,
- the curvature face,
- and the internal Hodge star.

The existing located-star theorem already supplies the internal
\(\operatorname{sgn}(\sigma)\) pseudoequivariance, but that is not yet the
transformation theorem for the new \(e\wedge e\wedge F\) density.

A fixed-base disconnected internal Lorentz gauge postulate is **not** adopted
as the missing principle: it would select the identity/Holst-like channel and
remove the star/Palatini-like channel. Any later one-dimensional selection must
therefore come from an independently justified action-orientation law.

No mathematical/type weld blocker remains.

---

## 12. Mandatory negative controls

- **Fake HomDimension:** rejected. No function-space enumeration such as a
  multi-argument `Finset.univ` is the insertion Hom-space.
- **Zero-coframe tautology:** rejected. Covariance is stated for the generic
  complementary solder bivector, not checked only at \(e=0\).
- **Same-face legs:** rejected by Proposition 10.
- **False Lorentz invariant:** the old
  \(\operatorname{tr}(X\eta Y\eta)\) expression is not used; the typed
  exterior pairing \(G_2\) is used instead.
- **Proper Lorentz only:** returns dimension two, as required.
- **Odd Role swap:** algebraically returns dimension one, but only conditionally
  as a physical selector.
- **Flat curvature:** both candidate linear-curvature densities vanish.
- **Quadratic-curvature detour:** no \(\operatorname{tr}(F^2)\),
  \(\operatorname{tr}(F\star F)\), Wilson-action, or fitted coefficient is
  introduced.

This closes the requested finite insertion classification at dimension two and leaves only the
separate action-level diagonal Role/orientation selector calculation above; no uniqueness claim is made.
