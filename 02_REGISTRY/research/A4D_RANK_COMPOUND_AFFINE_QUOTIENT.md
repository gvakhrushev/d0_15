# A4D rank-compound affine quotient

Task: `WRK-A4D-RANK-COMPOUND-AFFINE-QUOTIENT`  
Lean owner: `D0.Geometry.A4DRankCompoundAffineQuotient`  
Terminal: `FIXED-RANK-AFFINE-COKERNEL-COMPOUND-COORDINATE-CERTIFIED`

## Result

Let $V$ be a finite-dimensional real vector space, $M:V\to V$, and
assume `finrank (range M) = r`. The Lean definition is

\[
\Psi_r(M,t)=(\omega\mapsto t\wedge (\Lambda^rM)(\omega)):
\Lambda^rV\longrightarrow\Lambda^{r+1}V.
\]

The owner proves

\[
\Psi_r(M,t+Mc)=\Psi_r(M,t),\qquad
\Psi_r(M,t)=0\iff t\in\operatorname{im}M,
\]

and the complete equality criterion

\[
\Psi_r(M,t)=\Psi_r(M,t')\iff t-t'\in\operatorname{im}M.
\]

Thus $t\mapsto\Psi_r(M,t)$ descends to an injective coordinate on the
translation quotient $V/\operatorname{im}M$, with no quotient basis chosen.
The statement is rank-stratified: the rank equality is a hypothesis of the
kernel and completeness theorems.

For any linear equivalence $g:V\simeq V$, the owner proves naturality under
conjugation $M'=gMg^{-1}$:

\[
\Psi_r(M',gt)=(\Lambda^{r+1}g)\,\Psi_r(M,t)\,(\Lambda^rg^{-1}).
\]

On the fixed-rank stratum it also proves the affine version

\[
\Psi_r(M',gt+M'c)=(\Lambda^{r+1}g)\,\Psi_r(M,t)\,(\Lambda^rg^{-1}).
\]

This is stronger than Lorentz covariance as a change-of-frame identity: every
Lorentz transformation is a linear equivalence to which it applies. The
explicit parabolic representative below is separately proved to preserve its
Lorentz bilinear form.

## Rank-two null flag

Use coordinates $(u,v,x,y)\in\mathbb R^4$ and bilinear form

\[
B(z,z')=uv'+vu'-xx'-yy'.
\]

For $a\ne0$, the Lean model has

\[
P_a=\begin{pmatrix}
1&a^2/2&a&0\\
0&1&0&0\\
0&a&1&0\\
0&0&0&1
\end{pmatrix},\qquad N_a=P_a-I,\qquad N_a^3=0,
\]

and proves $P_a=I+N_a+N_a^2/2$, $P_aP_{-a}=I=P_{-a}P_a$, and

\[
B(P_az,P_az')=B(z,z').
\]

Writing $D_a=I-P_a$, its image and squared image are

\[
\Pi=\operatorname{im}D_a=\operatorname{span}(e_0,e_2),\qquad
\ell=\operatorname{im}D_a^2=\operatorname{span}(e_0),
\]

with $\dim\Pi=2$, $\dim\ell=1$, and

\[
\ell=\Pi\cap\Pi^{\perp_B}=\operatorname{rad}(B|_\Pi).
\]

The nonzero top compound is certified by
`parabolic_top_compound_ne_zero`. More generally, if `M` also has rank two and
$\Lambda^2D_a=q\,\Lambda^2M$ for any $q\ne0$, then
`projective_compound_recovers_parabolic_flag` proves

\[
\operatorname{im}M=\Pi,\qquad
\operatorname{im}D_a^2=\operatorname{im}M\cap(\operatorname{im}M)^{\perp_B}.
\]

So the projective class \([\Lambda^2(I-P_a)]\) recovers the plane and its
radical null line. The proof uses `Psi` to recover the image plane from the
translation-kernel locus, then the explicit Lorentz form to recover its
radical.

## Relation to existing owners

In dimension four, the $r=3$ exterior compound is the cofactor (adjugate,
up to basis and volume-form conventions) representation. In particular,
$\Lambda^3 M$ corresponds to $\det(M)M^{-T}$ when $M$ is invertible,
and extends as the third compound when it is singular. With the standard
oriented basis, $t\wedge\Lambda^3M$, after identifying its target with a
vector, has coordinates $\operatorname{adj}(M)t$. This is the cofactor
term in the existing paired residual

$$
R_{2|1}=\det(M_1)t_2-M_2\operatorname{adj}(M_1)t_1,
$$

owned by `D0.Geometry.A4DJointHolonomyResidual`. This worker makes the
single-map carrier rank-adapted and proves its exact quotient kernel; it does
not replace that two-map residual or establish an action-level invariance.

The existing `A4DRelativeAEGraphificationClosure` and
`A4DRelativeAEGraphificationClosureRank` owners compute vertical defect and
graphification from a pair-synthesis map and its residual range/rank. They are
complementary rank/quotient tools, not dependencies of this theorem: the new
owner instead uses the top exterior compound to determine `range M` and its
affine translation quotient. Its `map_ne_zero_of_finrank_range_eq` and
`range_eq_of_projectively_equal_compounds` provide the top-nonzero-compound
and projective image-recovery statements for this rank-two application.

## Exact rank boundary and claim fence

For `finrank (range M) < r`, `Lambda^r M=0`, hence `Psi_r(M,t)=0` for every
$t$; below the selected rank this coordinate carries no quotient
information. At rank $r$, the exact invariance and equality criterion above
hold. Above that stratum, `Psi_r` need not be translation-invariant. The
formal rank-four witness is

\[
\Psi_2(I,e_0)\ne\Psi_2(I,0)=0
\]

on \(\mathbb R^4\): although \(I\) has rank four, not rank two, the
three-vector \(e_0\wedge e_1\wedge e_2\) is nonzero. This is a concrete
failure of global rank-independent invariance, not a claim that every
higher-rank input fails.

The result is a finite-dimensional kinematic resolution diagnostic. It adds
no action term, no I-channel, and no replacement for the selected physical
residual.
