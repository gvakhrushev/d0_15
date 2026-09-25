# EXP-A4D-ROLE-BIVECTOR-INSERTION-UNIQUENESS

Class: `EXPENSIVE`
Parent: `CTRL-A4D-VARIATIONAL-FRONTIER`
Mode: research-only, theory-first.

## Mission

Close exactly one remaining A4D interface:

\[
\boxed{
\text{classify and, if possible, uniquely select the finite Role-typed insertion }
e\wedge e\wedge F.
}
\]

Do not reopen curvature-carrier construction, affine 2-cocycles, general \(F^2\) action families, continuum Einstein equations, or time evolution.

The audited starting point is:

`02_REGISTRY/research/MEMO_A4D_AFFINE_CONJUGACY_ROLE_BIVECTOR_INSERTION_AUDIT.md`.

## Frozen inputs

1. Independent affine links already carry exact even linear holonomy \(\Lambda_{rs}\).
2. Shared-F mixed letters do not carry independent even curvature.
3. The affine translation datum is stratified by
   \[
   [t]\in\operatorname{coker}(I-P),
   \]
   and is a separate channel from the even insertion problem.
4. On the Role bivector carrier, exact rational control calculation gives
   \[
   \dim\operatorname{End}_{\mathfrak{so}(1,3)}(\Lambda^2V)=2,
   \]
   with basis \(I,J\), \(J^2=-I\).
5. Adding the odd spacelike Role swap \(B\leftrightarrow C\) reduces the commutant to dimension 1, because \(J\mapsto-J\).
6. Existing repository work warns that simultaneous Role relabeling is not automatically the same statement as local Lorentz covariance.
7. The old fake `HomDimension` enumeration and any proof containing `sorry` are rejected.

## A. Exact owned carrier audit

Work on the actual repository types:

- `Role`;
- `RoleSpace`;
- `archiveRoleBasis`;
- `roleLorentzMetric`;
- `IsRoleLorentz`;
- `IsRoleLorentzTangent`;
- `solderLegVector`;
- Role exterior degree-two carrier;
- `occupationComplement`;
- `complementOrientation`;
- located primal/dual star;
- flat Lorentz star coefficient;
- Lorentz-restricted affine exterior connection.

Do not replace this by an abstract `Matrix 4 4` problem except as a derived coordinate certificate.

Classify every map used as one of:

- `OWNED`;
- `DERIVED-CANONICALLY`;
- `CONDITIONAL`;
- `MISSING`.

## B. Lorentz tangent to Role bivector weld

Construct the exact typed map

\[
\mathfrak{so}(\eta)\longrightarrow\Lambda^2V
\]

on the Role carrier.

The expected coordinate relation is that for Lorentz tangent \(X\),

\[
\omega_X:=\eta X
\]

is antisymmetric, hence determines a bivector/two-form coefficient set.

You must prove:

1. antisymmetry from the owned tangent condition;
2. basis independence/naturality under the owned Lorentz action;
3. compatibility with the existing exterior-frame lift;
4. no hidden Euclidean metric or arbitrary complement is introduced.

If this weld cannot be typed with current owners, return the obstruction immediately.

## C. Exact finite curvature extraction

Test the candidate

\[
\mathcal R(\Lambda)
=
\frac12(\Lambda-\Lambda^{-1}).
\]

For owned `IsRoleLorentz`, prove:

\[
\Lambda^{-1}=\eta\Lambda^T\eta,
\]

\[
\mathcal R(\Lambda)^T\eta+\eta\mathcal R(\Lambda)=0,
\]

and exact conjugation covariance

\[
\mathcal R(E\Lambda E^{-1})
=
E\mathcal R(\Lambda)E^{-1}.
\]

Near identity verify

\[
\Lambda=e^X
\quad\Rightarrow\quad
\mathcal R(\Lambda)=X+O(X^3).
\]

Compare against \(P-I\), local logarithm and other obvious extractions, but do not broaden the task once one exact global equivariant extraction is established.

## D. Complementary-face coframe bivector

For a curvature face \(S=\{r,s\}\), let \(S^c=\{u,v\}\).

Using the owned solder legs, construct

\[
B_{S^c}(x)
=
v_u(x)\wedge v_v(x).
\]

The two coframe legs must come from the complementary face needed for the four-dimensional top-cell contraction.

Mandatory hostile control:

- show that the naive same-face \(v_r\wedge v_s\) contraction has the wrong base-degree/top-cell typing for the intended \(e\wedge e\wedge F\) density.

Use the existing `occupationComplement` / `complementOrientation` machinery rather than importing a continuum epsilon tensor.

## E. Classify the insertion Hom-space

Classify the exact space of local Lorentz-equivariant maps between the coframe bivector carrier and curvature bivector carrier.

The control calculation predicts two proper-oriented Lorentz intertwiners:

\[
I,\qquad J\equiv\star.
\]

Confirm this on the actual Role/exterior types.

Then determine whether the physical D0 symmetry requirements include an orientation-reversing Role operation that must leave the action density invariant.

This is the central selector question.

Do not silently equate:

- local Lorentz covariance;
- archive Role relabeling;
- base-cell orientation reversal;
- internal Role orientation reversal.

Give an exact implication diagram among them.

## F. Build the two candidate linear-curvature densities

If both proper-oriented intertwiners are typable, construct the finite candidates

\[
\mathcal L_0(S)
=
\epsilon_{\rm base}(S)
\langle
B_{S^c},
\mathcal R_S
\rangle,
\]

and

\[
\mathcal L_\star(S)
=
\epsilon_{\rm base}(S)
\langle
B_{S^c},
\star\mathcal R_S
\rangle.
\]

Names such as Palatini/Holst may be used only as comparison labels after the finite formulas are complete.

For each candidate prove or disprove:

- local Lorentz/frame invariance;
- base-face orientation consistency;
- Role relabel covariance;
- odd Role swap parity;
- locality;
- flat-connection vanishing.

## G. Flat constitutive compatibility

Set

\[
\Lambda=I,\qquad b=0,\qquad\Omega=0.
\]

The even linear-curvature density must vanish exactly.

Verify that no additional coframe constitutive first jet is generated and that the already-owned matter/flux first jet remains \(H(e)\).

Important: this is only a compatibility test. Because both candidate insertions may vanish at \(\Lambda=I\), it does not by itself prove uniqueness.

## H. Uniqueness decision

Return exactly one principal verdict:

### `ROLE-BIVECTOR-INSERTION-UNIQUE-UP-TO-SCALE`

Use only if the actual mandatory owned symmetry group removes one of the two Lorentz intertwiners and the surviving cell density is fully typed.

### `ROLE-BIVECTOR-INSERTION-TWO-DIMENSIONAL`

Use if both \(I\) and \(\star\) remain admissible under every genuinely mandatory owned symmetry.

Give the exact two-dimensional basis.

### `ROLE-RELABEL-SELECTOR-NOT-PHYSICAL`

Use if an odd Role relabel would reduce the space to one dimension but the repository does not justify imposing that relabeling as a physical invariance of the action.

### `ROLE-EXTERIOR-WELD-MISSING`

Use if the required Lorentz-tangent-to-degree-two Role map or complementary-face contraction cannot be typed from current owners.

## I. Required outputs

1. Verdict.
2. Owned carrier/type table.
3. Exact Lorentz tangent -> Role bivector map.
4. Exact finite curvature extraction.
5. Complementary-face solder bivector.
6. Two-dimensional proper-Lorentz commutant proof/check.
7. Symmetry-status table: local Lorentz vs Role relabel vs orientation.
8. Explicit candidate density/densities.
9. Flat \(H(e)\) compatibility.
10. At least 10 theorem-ready propositions.
11. Exactly one remaining missing principle if verdict is negative.
12. Next calculation only if insertion uniqueness is actually closed.

## Mandatory negative controls

- fake `Finset.univ` enumeration of Role-valued functions;
- zero-coframe tautology;
- same-face instead of complementary-face solder legs;
- `tr(X eta Y eta)` as a false Lorentz invariant;
- proper Lorentz only, showing dimension 2;
- odd spacelike Role swap, showing algebraic dimension 1;
- explicit statement that the last reduction is conditional on that swap being a mandatory physical symmetry;
- flat connection, showing both candidate densities vanish;
- no `sorry`, no unproved `HomDimension = 1`.

## Forbidden scope

No Lean.
No GitHub mutation.
No continuum Einstein equation.
No time interpretation of Role A.
No \(L=3\) wave claim before insertion uniqueness.
No new 2-cocycle.
No fitted coefficient.
No golden-ratio phenomenology.
No action claim built solely from quadratic curvature \(F^2\).

## Exit condition

The Role-typed finite linear-curvature insertion is either uniquely selected up to scale, exactly classified as a two-dimensional family, or shown to require one precisely identified missing weld/symmetry principle.
