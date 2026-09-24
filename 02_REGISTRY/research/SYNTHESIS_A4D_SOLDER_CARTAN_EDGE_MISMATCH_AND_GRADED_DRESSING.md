# SYNTHESIS_A4D_SOLDER_CARTAN_EDGE_MISMATCH_AND_GRADED_DRESSING

## Status

DURABLE SYNTHESIS / POST-PR-109 FRONTIER.

Audited baseline: merged PR #109/#110/#111 on main.

This packet sharpens the fixed-N matter frontier after the affine-sensitive site-letter research. It does not introduce a new theorem owner.

## 0. What is no longer missing

The frontier is no longer "three channels" in the old sense.

The following pieces are now explicit:

### Linear exterior channel

PR #103 plus PR #110 own the 16-state exterior transport of the linear affine Cartan part and Lean-own its blindness to a pure affine translation.

### Labelled path skeleton

PR #111 Lean-owns the literal List ChainStep evaluator, shifted inverse, append/reverse/inverse, endpoint descent iff trivial labelled holonomy, and the exact L=2 positive-positive period forced by descent.

### Affine translation response

PR #109 constructs research-theorem-ready

\[
N_b=C^\dagger(b)P_0,\qquad
T_b=I+N_b,
\]

and

\[
R_{\rm nil}(L,b)=T_b\rho(L),
\]

with the exact affine semidirect law

\[
R_{\rm nil}(L,b)R_{\rm nil}(M,c)
=
R_{\rm nil}(LM,b+Lc).
\]

The site-aware weighted shift

\[
\mathscr L_r^{\rm nil}
=
M_{R_{\rm nil}(A(x,r))}U_r
\]

therefore provides an exact L+B control on the existing 16-state physical carrier.

Finite representability and archive/site support are no longer the missing primitive.

### Raw coframe first jet

PR #75 owns the independently defined flux energy and

\[
W_{\rm flux}(e)=I+H(e),
\]

with the complete uncentered first derivative.

### Pure-gauge finite chart

PR #101 owns the exact graded background trivialization

\[
\mathcal F_\phi
\]

and pure-gauge horizontal letter

\[
\ell_{d_f\phi,r}
=
\mathcal F_\phi U_r\mathcal F_\phi^{-1}.
\]

Its constitutive form is a distinct object:

\[
W_{d_f\phi}^{\rm gr}
=
\mathcal F_\phi^{-T}\mathcal F_\phi^{-1}.
\]

## 1. The actual missing seam

The first unresolved seam is the comparison between the already-constructed affine translation datum \(b_{x,r}\) and the already-owned raw solder/coframe datum on the same Role edge.

On the joint pure-gauge orbit, PR #70 and PR #101 require the extra degree-mixing affine response to disappear relative to the graded pure-gauge chart.

Off that orbit, in particular at

\[
e=0,\qquad (L,b)=(I,b),\qquad b\ne0,
\]

the affine response must remain visible.

The missing datum is therefore a **covariant edge mismatch/comparison**, not a new affine representation.

Write its desired output schematically as

\[
\kappa_N(A,e;x,r)\in V_x.
\]

The notation \(\kappa\) is a candidate packaging. Current ownership forces the need for a covariant B/E comparison, but does not yet prove that every successful finite matter letter must factor through one uniquely defined vector \(\kappa\).

## 2. Four target properties of a candidate mismatch

A candidate must at minimum realize the following exact controls:

\[
\kappa(A_{\rm flat},0;x,r)=0,
\]

\[
\kappa(A_\phi,d_f\phi;x,r)=0
\]

on the exact joint pure-gauge orbit,

\[
\kappa((I,b),0;x,r)\ne0
\]

for a nonzero pure affine shift, and a target-fibre frame law

\[
\kappa(A^h,e^h;x,r)
=
h_x^{\rm lin}\kappa(A,e;x,r)
\]

in the literal frame convention actually derived from the repository.

The last equation must not be asserted before resolving the row/vector convention between raw solder data and affine RoleSpace vectors.

## 3. Reference-leg hypothesis to test

The raw solder already supplies an internal target-site leg

\[
v_r(e,x)=\operatorname{solderLegVector}(e,x,r),
\]

with

\[
v_r(0,x)=\eta_r.
\]

The affine Cartan link supplies

\[
L_{x,r}:V_{x+r}\to V_x
\]

and translation \(b_{x,r}\in V_x\).

A natural candidate geometric ingredient is therefore a transported reference leg from the source site:

\[
L_{x,r}\,q_r(x+r),
\]

where \(q_r\) is a reference-leg field transforming in the source fibre.

The corresponding solder displacement candidate is

\[
\sigma_q(A,e;x,r)
=
v_r(e,x)-L_{x,r}q_r(x+r).
\]

This has the correct target-fibre typing and, if

\[
q'_r(y)=h_y^{\rm lin}q_r(y),
\]

has the expected homogeneous frame behavior under the linear gauge law.

But this is only a hypothesis to test.

At flat one wants \(q_r=\eta_r\), giving \(\sigma_q=0\). On the translation pure-gauge orbit one must check in the repository's literal index conventions whether \(\sigma_q\) equals the affine shift \(b\), or whether an additional metric raise/lower or row-to-vector comparison is required.

That exact index comparison is part of the missing seam.

Do not silently equate the raw coframe row \(e_r{}^a\), the solder leg perturbation, and the affine RoleSpace shift.

## 4. The commutator shortcut is false as a closure argument

The post-PR-109 synthesis suggested studying

\[
[H(e),C^\dagger(b)P_0].
\]

This mixed commutator is a legitimate diagnostic once both tangent directions are typed on the same global carrier.

It is **not** the mechanism that makes the affine response disappear on the pure-gauge diagonal.

First,

\[
[I,T_b]=0,
\]

not \(T_b\).

Second, if \(F\) is invertible and degree preserving while

\[
T_b=I+N_b,\qquad N_b\ne0
\]

raises degree \(0\to1\), then

\[
F T_bF^{-1}
=
I+F N_bF^{-1}
\ne I.
\]

Degree-preserving conjugation cannot erase a nonzero degree-mixing translation response.

Thus the diagonal disappearance must occur before such dressing, through

\[
\kappa=0
\]

or an equivalent covariant mismatch law.

The mixed commutator may later measure B/E interaction, but it cannot replace the edge comparison.

## 5. \(\mathcal F_\phi\) and \(W_{\rm flux}\) are different objects

Another required firewall:

\[
\mathcal F_\phi
\]

is an invertible background trivialization/action object.

\[
W_{\rm flux}(e)=I+H(e)
\]

is a symmetric constitutive/Riesz section derived from an independently defined finite energy.

The statement

\[
D_eW_0=H
\]

does not imply

\[
D_e\mathcal F_0=H.
\]

On the pure-gauge orbit the actual relation is

\[
W_{d_f\phi}^{\rm gr}
=
\mathcal F_\phi^{-T}\mathcal F_\phi^{-1}.
\]

Any arbitrary-background finite E dressing must respect this typing.

## 6. First-jet freedom of a finite graded dressing

Suppose, only after the edge comparison is solved, one seeks an arbitrary-background invertible graded dressing

\[
\mathcal F_e
=
I+\varepsilon G(e)+O(\varepsilon^2)
\]

with induced constitutive form

\[
W_e
=
\mathcal F_e^{-T}\mathcal F_e^{-1}.
\]

Then at flat

\[
D_eW_0[e]
=
-\bigl(G(e)^T+G(e)\bigr).
\]

Hence the owned \(H(e)\) fixes only the symmetric part of the tangent generator:

\[
G(e)^T+G(e)=-H(e).
\]

Its skew part is not selected by \(H\) alone.

The exact pure-gauge chart \(\mathcal F_\phi\) fixes the tangent on exact directions \(e=d_f\phi\), but raw harmonic/curl/transverse coframe directions remain a finite integration/classification problem.

Therefore there is currently no theorem of a unique finite graded \(\mathcal F_e\) from \(H\) plus the pure-gauge chart.

## 7. Correct order of the next frontier

The fixed-N path now has no useful branch before these steps:

1. Lean-own the exact nilpotent affine response and its grading boundary, so the new B construction is no longer research-only.
2. Construct or terminally classify the solder–Cartan edge mismatch/comparison, including the transported reference-leg/index issue.
3. Only after step 2, construct or classify an arbitrary-background finite graded E dressing whose pure-gauge restriction is \(\mathcal F_\phi\) and whose induced constitutive form has first derivative \(H\).
4. Only after such a finite dressing exists, study its mixed B/E commutator and second jet as consequences.

## 8. What not to reopen

Do not reopen:

- finite affine representability;
- Channel-L blindness;
- labelled-path descent;
- \(Q\), \(\mathcal S\), or a universal \(K\) as independent selectors;
- physical time;
- stress or Einstein equations;
- golden/AF/\(\phi\) refinement;
- \(A=A(e)\).

## 9. Exactly one current research step

Construct or terminally classify the target-fibre solder–Cartan edge mismatch, beginning with the transported-reference-leg hypothesis and auditing the literal row/vector/index conventions on the exact pure-gauge orbit.

The finite E dressing remains downstream and must not be started until that comparison is resolved.
## 10. Post-PR-112 refinement

PR #112 closes the row/vector ambiguity and sharpens the mismatch layer.

The owned `solderLegVector` already converts the raw right-transforming solder row into a target-fibre vector. For a supplied source reference leg

\[
q_r(y)\in V_y,
\]

the exact transported-reference mismatch is

\[
\kappa_q(A,e;x,r)=A_{x,r}(q_r(x+r))-v_r(e,x).
\]

It has exact pure-linear frame covariance and preserves the raw Nyquist/corner controls.

The new terminal is narrower: current D0 does not select the source reference/origin section \(q\). A fixed flat reference and the natural source solder leg both fail the exact pure-gauge diagonal, while the tautological \(q=A^{-1}v\) would erase every pure affine shift and is therefore inadmissible.

The next research step is consequently `EXP-A4D-SOLDER-REFERENCE-LEG-SECTION`.

The finite graded E dressing remains blocked. PR #112 alone does not make \(\kappa(A,e)\) intrinsic; it only constructs the conditional family \(\kappa_q\).

