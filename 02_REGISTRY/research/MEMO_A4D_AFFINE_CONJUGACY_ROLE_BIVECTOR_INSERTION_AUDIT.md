# MEMO A4D — affine conjugacy audit and Role-bivector insertion gate

Status: **CONTROL-ACCEPTED-WITH-REPAIRS / INSERTION-GATE-NARROWED**

This memo records the control audit of the post-curvature researcher packet. It is not a claim-registry owner and does not promote Einstein/Cartan dynamics.

## 1. Accepted affine-conjugacy result

For an exact based affine holonomy
\[ H=(P,t) \]
and a node affine gauge
\[ g=(E,c), \]
the owned conjugation law is
\[ P' = EPE^{-1}, \qquad t' = Et + (I-P')c. \]

At fixed representative P, pure origin shifts give
\[ t\sim t+(I-P)c. \]
Hence the translation conjugacy datum is
\[ [t]\in\operatorname{coker}(I-P)=V/\operatorname{im}(I-P). \]

Exactly:
\[ t\sim0 \iff t\in\operatorname{im}(I-P), \]
and all translation shifts are removable iff I-P is invertible.

Therefore the discarded binary rule
\[ P\neq I\Rightarrow t\sim0 \]
is false.

For a full conjugacy classification one must also quotient by the residual centralizer action. A fixed-P slice is described by
\[ (P,[t]), \]
while the invariant affine datum is more precisely the conjugacy class of P together with the Z(P)-orbit of [t].

## 2. Representative Lorentz strata

With
\[ \eta=\operatorname{diag}(1,-1,-1,-1), \qquad P^T\eta P=\eta, \]
the residual translation sector is stratified by I-P:

- P=I: all of t survives.
- I-P invertible: t is completely removable.
- I-P singular and P≠I: only [t] in coker(I-P) survives.

Exact rational examples include a spatial half-turn, a rational boost, a loxodromic representative, and a parabolic/null representative. The first two have nonzero residual quotients, the loxodromic example has zero residual quotient, and the parabolic example has nonzero residual quotient with degenerate induced Lorentz geometry.

The relation
\[ (\operatorname{im}(I-P))^{\perp_\eta}=\ker(I-P^{-1}) \]
is the correct dual description of the quotient. It does not imply that every residual quotient carries a canonical nondegenerate quadratic norm.

## 3. Rejected overclaim

The claim that every P≠I translation block can be removed by
\[ c=-(I-P)^{-1}t \]
is valid only when I-P is invertible. Rotation, boost and parabolic Lorentz holonomies provide explicit hostile controls with P≠I and non-removable translation classes.

## 4. Rotational quadratic germ

Let
\[ P(\epsilon)=\exp(\epsilon X+\cdots), \qquad X\in\mathfrak{so}(1,3). \]

The candidate
\[ \operatorname{tr}(X\eta Y\eta) \]
is not invariant under general Lorentz conjugation and must not be used as a second invariant.

For the proper oriented Lorentz group the quadratic invariant space is two-dimensional. At the level of the Role bivector carrier this is the statement that the commutant of the infinitesimal so(1,3) action on Λ²V is two-dimensional.

## 5. Independent exact commutant check

CONTROL repeated this as an exact rational linear-algebra calculation rather than relying on the researcher narrative.

Use the ordered bivector basis
\[ (AB,AC,AD,BC,BD,CD). \]

Let T in M6(Q) be an unknown intertwiner, giving 36 scalar unknowns. Impose
\[ T\rho_2(X_i)=\rho_2(X_i)T \]
for the three boost and three spatial-rotation generators of so(1,3).

The resulting rational linear system has rank 34, hence
\[ \boxed{\dim\operatorname{End}_{\mathfrak{so}(1,3)}(\Lambda^2V)=2.} \]

A basis is I and
\[
J=
\begin{pmatrix}
0&0&0&0&0&-1\\
0&0&0&0&1&0\\
0&0&0&-1&0&0\\
0&0&1&0&0&0\\
0&-1&0&0&0&0\\
1&0&0&0&0&0
\end{pmatrix},
\]
with
\[ J^2=-I. \]

This is the finite Role-bivector Hodge complex structure in the chosen orientation convention.

Now impose the odd spacelike Role swap B↔C, which preserves η but reverses orientation. The augmented rational system has rank 35, so its commutant is one-dimensional:
\[ \boxed{\dim=1.} \]

Moreover
\[ \rho_2(B\leftrightarrow C)J\rho_2(B\leftrightarrow C)^{-1}=-J. \]

This is an exact algebraic result. What is not yet established is whether that odd Role relabeling is a mandatory physical symmetry of the A4D insertion problem. Existing repository work explicitly warns that simultaneous Role relabeling is not the same statement as local Lorentz covariance.

## 6. Spectrum repairs

### Pure-translation RoleSpace action

The scalar two-direction L=3 curl operator has
\[ \operatorname{spec}K_{\rm scalar}=\{0^{10},3^4,6^4\}. \]

Tensoring with η=(+---) gives total dimension 4·18=72, hence
\[ \boxed{\operatorname{spec}K_{\rm full}=\{0^{40},+3^4,+6^4,-3^{12},-6^{12}\}.} \]

The previously stated multiplicities +3^8,+6^8,-3^24,-6^24 are rejected because they sum to the wrong total dimension.

### Rotational B1 action

For six Lie-algebra components, the total L=3 link space has dimension 6·18=108. With Lie-algebra signature (3,3), the corrected spectrum is
\[ \boxed{\{0^{60},+3^{12},-3^{12},+6^{12},-6^{12}\}.} \]

The previously stated nullity 54 is rejected; it misses the six harmonic zero modes.

## 7. Why the quadratic F² classification does not close the live gap

The rotational commutant/class-function calculation concerns quadratic curvature germs such as F². The active A4D frontier is narrower and different: a finite action density linear in even curvature and quadratic in the solder/coframe, schematically
\[ e\wedge e\wedge F. \]

The quadratic-curvature family does not decide whether this linear-curvature insertion is unique.

## 8. Existing owned ingredients for the linear-curvature insertion

The repository already owns the relevant typed ingredients separately:

- RoleSpace = Role → R;
- roleLorentzMetric;
- IsRoleLorentz;
- solderLegVector, with flat value equal to the corresponding archiveRoleBasis vector;
- the exterior-algebra Role carrier;
- occupationComplement and complementOrientation;
- the located primal/dual star and its Role-permutation pseudoequivariance;
- the flat Lorentz exterior-star coefficient with the correct Lorentzian middle-degree sign;
- independent affine link transport with a Lorentz-restricted .lin sector.

The remaining task is the weld among them, not the invention of a new carrier.

## 9. Candidate exact finite curvature extraction

For a Lorentz plaquette linear holonomy Λ, define the candidate
\[ \mathcal R(\Lambda)=\frac12(\Lambda-\Lambda^{-1}). \]

Under the owned convention
\[ \Lambda\eta\Lambda^T=\eta, \]
one has
\[ \Lambda^{-1}=\eta\Lambda^T\eta. \]

Therefore
\[ \mathcal R(\Lambda)^T\eta+\eta\mathcal R(\Lambda)=0, \]
so R(Λ) lies exactly in the Lorentz tangent algebra, without a matrix logarithm.

It is conjugation equivariant:
\[ \mathcal R(E\Lambda E^{-1})=E\mathcal R(\Lambda)E^{-1}. \]

Near the identity,
\[ \Lambda=e^X \Rightarrow \mathcal R(\Lambda)=X+O(X^3). \]

This is a candidate research extraction, not yet a Lean-owned action primitive.

## 10. Correct cell-level shape of the insertion

For curvature on a base face S={r,s}, the two solder legs required for a four-dimensional top-cell contraction should be taken from the complementary face
\[ S^c=\{u,v\}, \]
not from the same r,s face.

Let v_u(x),v_v(x) be the owned solder-leg vectors and
\[ B_{S^c}(x)=v_u(x)\wedge v_v(x). \]

A typed curvature bivector must be obtained from R(Λ_S) using η, since η R(Λ_S) is antisymmetric.

The two natural proper-oriented Lorentz insertions are represented by the two commutant directions:
\[ \mathcal L_0(S)\sim\epsilon_{\rm base}(S)\langle B_{S^c},\mathcal R_S\rangle, \]
and
\[ \mathcal L_\star(S)\sim\epsilon_{\rm base}(S)\langle B_{S^c},\star\mathcal R_S\rangle. \]

The exact repository-level map from the Lorentz tangent matrix to the degree-two Role exterior carrier is still to be written and proved natural. These formulas are the target shape, not yet ownership.

## 11. Flat constitutive compatibility does not select between the two insertions

At Λ=I, the extraction satisfies R(Λ)=0. Hence both linear-curvature candidates vanish on the flat connection. They therefore do not add a new constitutive first jet there; the already-owned matter/flux response H(e) remains separate.

Consequently the test R=0, c=0, Λ=I is necessary for compatibility but does not distinguish the identity and Hodge-star insertion directions.

## 12. Live selector question

The exact local algebra now leaves only one sharp selector question:
\[ \boxed{\dim\{\text{owned-equivariant linear-curvature Role insertions}\}=1\text{ or }2?} \]

Lorentz covariance alone gives dimension 2.

If an orientation-reversing Role relabeling is a mandatory symmetry of the physical insertion, the exact commutant calculation gives dimension 1.

The repository already owns odd-Role pseudoequivariance of the located star, but it also explicitly states that simultaneous Role relabeling is not identical to local Lorentz covariance. Therefore the symmetry status must be decided rather than silently imposed.

## 13. Control disposition

Accepted:

- affine residual datum [t] in coker(I-P);
- stratification by rank of I-P;
- rejection of tr(XηYη) as a Lorentz invariant;
- two-dimensional proper-Lorentz bivector commutant;
- one-dimensional commutant after an odd Role swap;
- separation of quadratic-curvature action germs from the linear-curvature insertion problem.

Repaired:

- full pure-translation and rotational L=3 spectral multiplicities.

Rejected:

- P≠I implies t pure gauge;
- a fake Finset.univ enumeration of Role-valued functions as an insertion Hom-space;
- any HomDimension = 1 theorem containing sorry;
- testing Lorentz invariance only at zero coframe.

Next research target:

EXP-A4D-ROLE-BIVECTOR-INSERTION-UNIQUENESS
