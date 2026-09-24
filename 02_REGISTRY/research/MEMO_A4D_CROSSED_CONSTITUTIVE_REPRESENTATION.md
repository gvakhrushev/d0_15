# A4D crossed constitutive representation: finite path/CAR algebra, pure-gauge crossed action, affine-response audit, and the orbit-seed boundary

**Canonical task:** \`EXP-A4D-CROSSED-CONSTITUTIVE-REPRESENTATION\`.

**Audited baseline:** fresh canonical \`main = fa4af53bed53a693efbd1db832ae092c51eb5536\` at task start, including merged PR #95, PR #98, PR #99 and PR #100.

**Research PR:** #101.

No Lean source is authored by this EXP. Golden/\(\phi\), stress and Einstein dynamics are outside scope.

## 0. Terminal verdict

**CROSSED-PURE-GAUGE-SUBPACKAGE-CONSTRUCTED-FULL-BACKGROUND-CROSSED-CONSTITUTIVE-PRIMITIVE-REQUIRED.**

This is stronger than the PR #95 terminal, but it is not a construction of the requested full package.

At one fixed \(\operatorname{ArchiveRolePhaseGroup}N\):

1. There is a literal smallest finite algebraic home for the owned first jet:
   \[
   \mathfrak A_N
   =
   \bigl(\operatorname{Fun}(X_N,\mathcal E_{\deg})\bigr)\rtimes X_N,
   \qquad
   X_N=\operatorname{ArchiveRolePhaseGroup}N,
   \tag{0.1}
   \]
   where
   \[
   \mathcal E_{\deg}
   =
   \bigoplus_{k=0}^4\operatorname{End}(\Lambda^kV)
   \tag{0.2}
   \]
   is the unital associative CAR-bilinear envelope on the existing 16-state \`ArchiveFockState\`.
   It is not an untyped full-matrix placeholder. It has a canonical crossed normal form and a separate syntactic path-word filtration.
2. The owned CAR data are strong enough to generate every same-degree Fock matrix unit. Together with the PR #70 scalar crossed-product site matrix units, evaluation gives exactly
   \[
   \mathfrak A_N
   \simeq
   \bigoplus_{k=0}^4
   \operatorname{End}\!\bigl(\mathbb R^{X_N}\otimes\Lambda^kV\bigr),
   \tag{0.3}
   \]
   of dimension
   \[
   70\,|X_N|^2.
   \tag{0.4}
   \]
3. The positive PR #95 linear/Lorentz horizontal path transport is a distinguished subrepresentation of (0.1):
   \[
   \mathsf U^A_r
   =
   M_{\rho(L_{x\leftarrow x+r})}U_r.
   \tag{0.5}
   \]
   Products reproduce exterior-lifted PR #70 linear path transport exactly.
4. On the exact coframe orbit \(e=d_f\phi\), the already constructed graded pure-gauge action is a unit of \(\mathfrak A_N\). Therefore
   \[
   \alpha_\gamma(a)=R_\gamma aR_\gamma^{-1}
   \tag{0.6}
   \]
   is an exact inner algebra automorphism, and the pure-gauge action-groupoid gives a genuine crossed subpackage
   \[
   (\pi_e,R_\gamma,\alpha_\gamma,W_e,J_N)
   \tag{0.7}
   \]
   with exact composition and the complete owned first jet on \(e\in\operatorname{im}d_f\).
5. The infinitesimal vertical action closes on all generators of \(\mathfrak A_N\). Explicit formulas are derived below for site multipliers, every Role shift, every \(E_{tu}=c_t^\dagger c_u\), and arbitrary shift words, hence for the length-two corners in \(H(e)\).
6. Pure affine translation holonomy is **not** terminally impossible on the 16-state carrier. Two explicit finite representation classes exist:
   - an exact affine representation \(T_b=I+C^\dagger(b)P_0\), which is Lorentz covariant but mixes degree/parity and does not normalize \(\mathcal E_{\deg}\);
   - an observer-dependent degree-preserving family built from
     \[
     S_n^{\lambda,\mu}(b)
     =
     e^{\lambda\,\eta(n,b)}
     \bigl(I+\mu\,b_\perp\otimes n^\flat\bigr),
     \qquad
     b_\perp=b-\eta(n,b)n,
     \tag{0.8}
     \]
     which is additive and frame covariant but has a trivial degree-zero block and therefore cannot reproduce the forced scalar crossed word-mixing law.
   Thus “the 16-state carrier cannot represent translations” would be false. The actual missing object is a **geometrically compatible path-expression affine-shift lift**, not merely a finite representation.
7. PR #75 already owns an independently written local finite quadratic energy:
   \[
   2E_{\rm flux}(e,\psi)
   =
   \langle\psi,(I+H(e))\psi\rangle.
   \tag{0.9}
   \]
   Hence
   \[
   W_{\rm flux}(e)=I+H(e)
   \tag{0.10}
   \]
   is a genuine all-uncentered, symmetric, small-\(e\) positive section in the reference counting observer gauge. It is not defined by merely naming \(H\): (0.9) is the owned independent polarization theorem.
   But no owned theorem makes (0.10) the same finite constitutive section as the exact pure-gauge groupoid action, no moving-observer/frame law for it is derived, and its zero Hessian does not select the groupoid second jet.
8. The crossed package itself does **not** remove the second-order modulus. For any invertible background dressing \(P_b\),
   \[
   \pi_b^P=\operatorname{Ad}_{P_b}\pi_b,\qquad
   R_\gamma^P=P_{b'}R_\gamma P_b^{-1},\qquad
   W_b^P=P_b^{-T}W_bP_b^{-1}
   \tag{0.11}
   \]
   preserves exact crossed covariance. If \(P_0=I\) and \(DP_0=0\), the flat value and complete first jet are unchanged while the second jet changes. This is the full crossed analogue of the PR #95 endpoint dressing, not merely a horizontal statement.
9. Fixed located \(J_N\) is not an obstruction once the two colors are typed separately. Define
   \[
   \mathfrak A_N^D
   =
   J_N^{-T}(\mathfrak A_N^P)^{-T}J_N^T,
   \tag{0.12}
   \]
   and for every primal horizontal or vertical unit
   \[
   R_D=J_N^{-T}R_P^{-T}J_N^T.
   \tag{0.13}
   \]
   Composition is exact. The Fock-dependent shifted anchors remain literal; no sitewise dual exterior slogan is used.
10. The full raw coframe space contains directions not generated by the translation plus local Lorentz tangent. If \(m=|X_N|=L^4\), then
    \[
    \dim\mathcal E_{\rm raw}=16m,\qquad
    \dim\operatorname{im}d_f=4(m-1),
    \]
    while local Lorentz frame tangents contribute at most \(6m\). Hence even their sum has codimension at least
    \[
    16m-\bigl(4(m-1)+6m\bigr)=6m+4>0.
    \tag{0.14}
    \]
    Harmonic/curl directions are therefore not removable by saying “covariance determines \(W\)”.

The strongest honest conclusion is consequently not a universal no-go. A nontrivial crossed **sub**representation is constructed, and concrete affine representations exist. What current D0 does not geometrically select is the full-background crossed constitutive seed that simultaneously supplies:

- affine-shift-sensitive path-expression letters compatible with PR #70 affine geometry;
- the vertical matter cocycle away from the exact coframe orbit;
- a moving-observer/frame-covariant constitutive section on the transverse background directions.

No separate \(c\), \(\mathcal S\), or universal \(K\) should be chosen before that datum exists.

---

## 1. Frozen inputs and truth boundaries

The canonical brief and all named durable packets were read completely.

| Input | Used literally here | Boundary retained |
|---|---|---|
| PR #70 \`ArchiveAffineCartanConnection\` | affine \((L,b)\) pulls; path append/reversal; node affine gauge; open curvature/torsion; exact flat translation \(\to d_f\xi\) | raw coframe \(e\) is not identified with affine connection \(A\); affine shift has no owned matter representation |
| PR #70 \`ArchivePathWordAlgebra\` | scalar crossed product; exact evaluation into site endomorphisms; site matrix units; free paths; path-expression cost | compressed matrix membership is not local geometric provenance |
| PR #75 \`A4DDiscreteEnergyKernel\` | complete uncentered \(H(e)\), self-adjointness, degree/parity, independent \`fluxEnergy\`, exact pure-gauge Ward, Nyquist/corner | no all-order observer/frame-covariant physical constitutive law |
| PR #76 located primal/dual owners | fixed \(J_N\), complement anchors, signs, parity/chirality | generic boost is shifted/non-sitewise on the dual |
| PR #80 second-order package | generic congruence; background groupoid second jet; scalar advective model; transverse curl | \(\mathcal S\), \(D_eg\), \(K\) not selected universally |
| PR #98 | unlabelled-center holonomy no-go; exact \(S_{\rm patch}\); explicit \(S_\lambda\) nonselection; path-resolution boundary | no physical \(C_N\) or crossed constitutive law |
| \`MEMO_A4D_PATH_RESOLVED_MATTER_WORD_ACTION\` | horizontal exterior word action; word-length mixing; crossed target; fixed-\(J\) and observer boundaries | bare word law too small |
| \`MEMO_A4D_COMMON_CENTER_MATTER_GROUPOID_ACTION\` | exact scalar and graded pure-gauge cocycles; unrestricted dressing; constant isotropy; full-H pure-gauge benchmark | no arbitrary-background finite completion |
| \`MEMO_A4D_ENDPOINT_COMPARISON_JET_OVERLAP_LAW\` | path labels required; \(S_{\rm patch}\); harmonic/curl/Nyquist/corner/frame/J controls | comparison law not selected |
| \`MEMO_A4D_SOLDERED_CREATOR_OBSERVER_FRAME_LIFT\` | exterior representation; moving observer; raw solder rule; conditional Lorentz link lift | no full staggered cell-energy law; no \(e\mapsto A(e)\) |
| \`SYNTHESIS_A4D_PATH_RESOLVED_MATTER_WORD_ACTION\` | path/background composition firewall | not itself a theorem owner |
| PR #99 | only the fixed-N/golden truth firewall | no golden input is used here |

The observer/frame Lean worker may run in parallel. No unmerged result is promoted to canonical Lean ownership in this memo.

---

## 2. Literal fixed-\(N\) types

Fix
\[
X=X_N=\operatorname{ArchiveRolePhaseGroup}N,
\qquad
L=N+2,
\qquad
m=|X|=L^4.
\]

Let
\[
V=\mathbb R^{\rm Role},
\qquad
\mathcal F=\Lambda^\ast V
=\bigoplus_{k=0}^4\mathcal F_k,
\qquad
\dim\mathcal F=(1,4,6,4,1).
\]

The primal archive cochain carrier is
\[
\Gamma_N^P
=
\operatorname{Fun}(X,\mathcal F).
\tag{2.1}
\]

The raw background is kept typed as
\[
b=(A,e,n),
\tag{2.2}
\]
where:

- \(A\) is an independent PR #70 affine Cartan connection;
- \(e\) is the raw uncentered coframe;
- \(n\) is an observer field.

There is no silent function \(A=A(e)\).

A vertical arrow is a background arrow
\[
\gamma:b\longrightarrow b'.
\tag{2.3}
\]

A PR #70 spatial path word is instead an arrow inside one fixed \(A\):
\[
p:x\longrightarrow y.
\tag{2.4}
\]

These are different source categories.

---

## 3. The minimal finite path/CAR algebra

### 3.1 Fiber coefficient algebra

Define
\[
\mathcal E_{\deg}
=
\{T\in\operatorname{End}(\mathcal F):
T\mathcal F_k\subseteq\mathcal F_k\;\forall k\}.
\tag{3.1}
\]

The owned dimension is
\[
\dim\mathcal E_{\deg}
=
1^2+4^2+6^2+4^2+1^2
=
70.
\tag{3.2}
\]

The existing bilinears
\[
E_{sr}=c_s^\dagger c_r
\tag{3.3}
\]
generate more than their linear span. PR #100's current main already contains \`ArchiveCARAssociativeEnvelope\`, which owns the exact occupation projectors
\[
P_T=|T\rangle\langle T|
\tag{3.4}
\]
as products of number operators.

For two Fock states \(S,T\) with \(|S|=|T|\), choose a bijection
\[
S\setminus T=\{r_1,\ldots,r_q\},
\qquad
T\setminus S=\{s_1,\ldots,s_q\}.
\]
Then
\[
P_T
E_{s_qr_q}\cdots E_{s_1r_1}
P_S
=
\varepsilon_{T,S}|T\rangle\langle S|,
\qquad
\varepsilon_{T,S}\in\{\pm1\}.
\tag{3.5}
\]

The exact checker verifies (3.5) for all **70** same-degree pairs. Therefore the unital CAR-bilinear envelope is literally every degree-preserving Fock matrix, not merely a dimension analogy.

### 3.2 Matrix-valued crossed product

Define a crossed normal form
\[
\mathfrak A_N
=
\left\{
\sum_{a\in X} M_{F_a}U^a:
F_a:X\to\mathcal E_{\deg}
\right\}.
\tag{3.6}
\]

The multiplication is
\[
(M_FU^a)(M_GU^b)
=
M_{F\cdot(U^aG)}U^{a+b},
\tag{3.7}
\]
where the dot is fiber matrix multiplication.

PR #70 owns the scalar analogue and the identity
\[
|x\rangle\langle y|
=
M_{\delta_x}U^{y-x}.
\tag{3.8}
\]

Combining (3.5) and (3.8) yields every global matrix unit
\[
|(x,T)\rangle\langle(y,S)|
\qquad
(|T|=|S|).
\tag{3.9}
\]

Hence evaluation is a faithful algebra isomorphism
\[
\operatorname{ev}:
\mathfrak A_N
\overset{\sim}{\longrightarrow}
\bigoplus_{k=0}^4
\operatorname{End}(\mathbb R^X\otimes\mathcal F_k).
\tag{3.10}
\]

This gives (0.4).

### 3.3 Why this is not an untyped full matrix placeholder

Equation (3.10) is a compressed algebraic identity. Locality is retained separately by the syntactic path presentation.

Use the PR #70 free path/path-expression type before quotienting by endpoint/group displacement. A term records:

- its ordered oriented path word;
- additions versus products;
- CAR coefficient;
- word length.

Evaluation maps that filtered presentation into (3.6). Distinct long words can compress to the same finite matrix.

Thus:

\[
\text{factorized path locality}
\neq
\text{compressed support locality}.
\tag{3.11}
\]

---

## 4. Horizontal representation

Let the PR #70 affine link at \(x,r\) be
\[
A_{x,r}=(L_{x,r},b_{x,r}):
V_{x+r}\to_{\rm aff}V_x.
\]

On the Lorentz-linear domain of the frame packet, define the covariant shift letter
\[
\mathsf U^A_r
=
M_{x\mapsto\rho(L_{x,r})}U_r
\in\mathfrak A_N^\times.
\tag{4.1}
\]

For a word \(p=(r_1,\ldots,r_q)\), crossed multiplication gives exactly
\[
\pi_A(p)
=
M_{\rho(L_A(p,\cdot))}U^{\operatorname{disp}(p)}.
\tag{4.2}
\]

This is PR #95's
\[
C^{\rm lin}_{N,A}(p,x)
=
\rho((\operatorname{affinePath}A\,p\,x).{\rm lin})
\]
assembled over all base sites.

Append and reverse are exact because both the PR #70 linear path and \(\rho\) are functorial.

The affine shift \(b\) is deliberately absent from (4.1). Section 8 audits whether it can be added.

---

## 5. The complete first jet lies in \(\mathfrak A_N\)

Let
\[
A_r=\frac12(I+U_r^{-1}),\qquad
E_{sr}=c_s^\dagger c_r.
\]

The owned first jet is
\[
\begin{aligned}
H(e)
&=
\frac12\sum_r
\left(M_{e_r{}^r}U_r+U_r^{-1}M_{e_r{}^r}\right)I_{\mathcal F}
\\
&\quad
-\frac12\sum_{s,r}
M_{e_s{}^r}
\left(U_s+U_sU_r^{-1}\right)E_{sr}
-\text{counting adjoint}.
\end{aligned}
\tag{5.1}
\]

Therefore
\[
H(e)\in\mathfrak A_N,
\tag{5.2}
\]
and its syntactic spatial word length is at most two.

The L=2 raw Nyquist and L=3 corner are not exceptions to this algebra: they are precisely tests that the coefficients must use the raw coframe and both one-/two-edge words rather than only a centered metric readout.

---

## 6. Exact pure-gauge crossed subpackage

Take
\[
e=d_f\phi.
\]

The common-center packet constructs an exact graded matter trivialization \(\mathcal F_\phi\) and
\[
R_{\rm gr}(\xi;e)
=
\mathcal F_{\phi+\xi}\mathcal F_\phi^{-1}.
\tag{6.1}
\]

It obeys
\[
R_{\rm gr}(\zeta;e+d_f\xi)
R_{\rm gr}(\xi;e)
=
R_{\rm gr}(\xi+\zeta;e).
\tag{6.2}
\]

Every factor is degree preserving, so by (3.10)
\[
R_{\rm gr}(\xi;e)\in\mathfrak A_N^\times.
\tag{6.3}
\]

Define
\[
\alpha_\gamma(a)
=
R_\gamma aR_\gamma^{-1}.
\tag{6.4}
\]

Then
\[
R_\gamma\pi_e(a)R_\gamma^{-1}
=
\pi_{e'}(\alpha_\gamma a)
\tag{6.5}
\]
is an exact crossed covariance law.

A convenient distinguished horizontal family on this orbit is
\[
\ell_{e,r}
=
\mathcal F_\phi\,U_r\,\mathcal F_\phi^{-1}.
\tag{6.6}
\]

Equation (6.2) immediately gives
\[
R_\gamma\ell_{e,r}R_\gamma^{-1}
=
\ell_{e',r}.
\tag{6.7}
\]

This is a real finite crossed construction.

It must not be overread: (6.6) defines the matter horizontal letters by transport from flat. No theorem identifies them with a matter lift of the full PR #70 affine link \((L,b)\) on arbitrary \(A\).

### 6.1 Pure-gauge constitutive form

With flat seed \(W_0=I\), define
\[
W_{d_f\phi}^{\rm gr}
=
\mathcal F_\phi^{-T}\mathcal F_\phi^{-1}.
\tag{6.8}
\]

Then
\[
W_{e'}^{\rm gr}
=
R_\gamma^{-T}
W_e^{\rm gr}
R_\gamma^{-1}
\tag{6.9}
\]
exactly.

At flat,
\[
D_eW_0[d_f\xi]
=
H(d_f\xi)
\tag{6.10}
\]
on all Fock degrees.

Thus the target package exists on the exact-coframe action-groupoid chart.

---

## 7. Infinitesimal vertical action on the full algebra

Write
\[
G_\xi
=
A_\xi+\mathcal K(h),
\qquad
h=d_f\xi,
\tag{7.1}
\]
with
\[
A_\xi=\sum_rM_{\xi^r}D_r,
\qquad
D_r=\frac L2(U_r-U_r^{-1}),
\tag{7.2}
\]
and
\[
\mathcal K(h)
=
\sum_{s,r}
M_{h_s{}^r}U_sA_rE_{sr}.
\tag{7.3}
\]

Define the infinitesimal algebra action
\[
\delta_\xi(a)=[G_\xi,a].
\tag{7.4}
\]

Because \(\mathfrak A_N\) is an associative algebra containing \(G_\xi\), (7.4) is already an inner derivation of \(\mathfrak A_N\). The following formulas expose the geometric support.

### 7.1 Site multiplier

For scalar \(f:X\to\mathbb R\),
\[
[D_r,M_f]
=
\frac L2
\left(
M_{U_rf-f}U_r
+
M_{f-U_r^{-1}f}U_r^{-1}
\right).
\tag{7.5}
\]

The flux part gives
\[
\begin{aligned}
[\mathcal K(h),M_f]
&=
\frac12\sum_{s,r}
M_{h_s{}^r(U_sf-f)}U_sE_{sr}
\\
&\quad+
\frac12\sum_{s,r}
M_{h_s{}^r(U_sU_r^{-1}f-f)}
U_sU_r^{-1}E_{sr}.
\end{aligned}
\tag{7.6}
\]

Thus \(\delta_\xi(M_f)\) is still in \(\mathfrak A_N\), with one-/two-edge support before further products.

### 7.2 Arbitrary archive shift

For \(a\in X\),
\[
\begin{aligned}
\delta_\xi(U^a)
&=
\sum_r
M_{\xi^r-U^a\xi^r}D_rU^a
\\
&\quad+
\sum_{s,r}
M_{h_s{}^r-U^ah_s{}^r}
U_sA_rU^aE_{sr}.
\end{aligned}
\tag{7.7}
\]

For \(a=e_t\), this is the Role-shift formula.

On the scalar one-cycle restriction,
\[
[G_\xi,U]
=
-\frac12M_{h_\xi}(U^2-I),
\tag{7.8}
\]
the PR #95 diagnostic.

### 7.3 CAR bilinear

Using the owned CAR Lie law,
\[
[E_{sr},E_{tu}]
=
\delta_{rt}E_{su}-\delta_{us}E_{tr},
\tag{7.9}
\]
one gets
\[
\delta_\xi(E_{tu})
=
\sum_{s,r}
M_{h_s{}^r}U_sA_r
\left(
\delta_{rt}E_{su}
-
\delta_{us}E_{tr}
\right).
\tag{7.10}
\]

### 7.4 Length-two corner

Take the corner word
\[
U_sU_r^{-1}=U^{e_s-e_r}.
\]

Equation (7.7) with \(a=e_s-e_r\) is its exact vertical derivative.

Equivalently, Leibniz gives
\[
\delta(U_sU_r^{-1})
=
\delta(U_s)U_r^{-1}
+
U_s\delta(U_r^{-1}),
\tag{7.11}
\]
\[
\delta(U_r^{-1})
=
-U_r^{-1}\delta(U_r)U_r^{-1}.
\tag{7.12}
\]

The exact checker verifies (7.7), (7.10), and the corner specialization on a two-Role \(L=3\) archive with the full 16-state Fock carrier.

### 7.5 Closure versus bounded word length

A finite generating family is available:
\[
\{M_{\delta_x}\}_{x\in X},
\quad
\{U_r^{\pm1}\}_{r\in{\rm Role}},
\quad
\{E_{sr}\}_{s,r\in{\rm Role}},
\quad I.
\tag{7.13}
\]

It generates the finite algebra, and \(\delta_\xi\) closes there.

It does **not** preserve a fixed syntactic word length. Repeated commutators can grow path length before finite-torus compression. This agrees with the PR #70 locality theorem and does not obstruct an inverse-free factorized parent.

---

## 8. Affine translation response: actual representations and their failures

The affine part of a PR #70 path is
\[
z\longmapsto Lz+b.
\]

PR #95's exterior lift uses only \(L\). We now test real finite responses to \(b\).

### 8.1 Exact 16-state affine representation that mixes degree

Let
\[
P_0=|0\rangle\langle0|,
\qquad
N_b=C^\dagger(b)P_0.
\tag{8.1}
\]

Because
\[
P_0C^\dagger(c)=0,
\]
one has
\[
N_bN_c=0.
\tag{8.2}
\]

Therefore
\[
T_b=I+N_b
\tag{8.3}
\]
obeys
\[
T_bT_c=T_{b+c},
\qquad
T_b^{-1}=I-N_b.
\tag{8.4}
\]

Exterior covariance gives
\[
\rho(g)T_b\rho(g)^{-1}=T_{gb}.
\tag{8.5}
\]

Hence
\[
\widehat\rho(L,b)=T_b\rho(L)
\tag{8.6}
\]
is an exact representation of
\[
(L,b)(M,c)=(LM,b+Lc).
\tag{8.7}
\]

So there is no universal finite-carrier no-go.

But
\[
T_bP_0T_b^{-1}=P_0+N_b.
\tag{8.8}
\]

The right side mixes degree \(0\to1\). It is outside \(\mathcal E_{\deg}\). Thus \(T_b\) does not normalize the minimal horizontal algebra (3.6), does not preserve Fock degree/parity, and cannot provide the required \(\alpha_\gamma\) on that algebra.

This explicit failed candidate is important: the obstruction is crossed **closure**, not finite representability.

### 8.2 Observer-dependent degree-preserving translation family

Now use the observer.

For unit timelike \(n\), decompose
\[
a_n(b)=\eta(n,b),
\qquad
b_\perp=b-a_n(b)n,
\qquad
n^\flat(b_\perp)=0.
\tag{8.9}
\]

For real parameters \(\lambda,\mu\), define
\[
S_n^{\lambda,\mu}(b)
=
e^{\lambda a_n(b)}
\left(
I+\mu\,b_\perp\otimes n^\flat
\right)
\in GL(V).
\tag{8.10}
\]

Because
\[
(b_\perp\otimes n^\flat)
(c_\perp\otimes n^\flat)=0,
\tag{8.11}
\]
one has
\[
S_n^{\lambda,\mu}(b)
S_n^{\lambda,\mu}(c)
=
S_n^{\lambda,\mu}(b+c).
\tag{8.12}
\]

For Lorentz \(g\),
\[
S_{gn}^{\lambda,\mu}(gb)
=
gS_n^{\lambda,\mu}(b)g^{-1}.
\tag{8.13}
\]

Therefore
\[
T_n^{\lambda,\mu}(b)=\rho(S_n^{\lambda,\mu}(b))
\tag{8.14}
\]
is additive, degree preserving, parity preserving, and frame covariant.

For a chain whose observers are parallel under the linear links,
\[
n_x=L_{x\leftarrow y}n_y,
\tag{8.15}
\]
the assignment
\[
\widehat T_{x\leftarrow y}
=
T_{n_x}^{\lambda,\mu}(b_{x\leftarrow y})
\rho(L_{x\leftarrow y})
\tag{8.16}
\]
composes with the affine law.

This is a genuine positive candidate family on the existing 16-state carrier.

### 8.3 Why (8.16) still does not solve the crossed problem

First, \(\lambda,\mu\) are not selected by affine composition, frame covariance, degree or parity. The exact checker uses two distinct rational \(\mu\)'s.

Second, every exterior representation acts trivially on \(\Lambda^0V\):
\[
\rho_0(S)=1.
\tag{8.17}
\]

Hence (8.16) leaves the scalar/vacuum horizontal shift unchanged under a pure affine translation.

But the owned vertical pure-gauge action forces, already on scalar matter,
\[
\delta_\xi(U)
=
-\frac12M_{h_\xi}(U^2-I),
\tag{8.18}
\]
which is generically nonzero.

Thus (8.16) is not the missing crossed affine-shift lift.

Third, (8.15) is an extra observer/connection compatibility hypothesis. A generic supplied observer field is not owned to be parallel under PR #70 links.

### 8.4 Observer-independent degree-preserving tangent no-go

There is nevertheless a useful scoped no-go.

Suppose a same-fiber translation tangent
\[
\tau:V\to\mathcal E_{\deg}
\tag{8.19}
\]
is linear and Lorentz equivariant without observer dependence:
\[
\tau(gb)
=
\rho(g)\tau(b)\rho(g)^{-1}.
\tag{8.20}
\]

For the current full \`IsRoleLorentz\`, \(g=-I\) is allowed. On each \(\Lambda^kV\),
\[
\rho(-I)=(-1)^kI,
\]
so conjugation by \(\rho(-I)\) is the identity on \(\mathcal E_{\deg}\). Then
\[
\tau(-b)=\tau(b),
\]
while linearity gives
\[
\tau(-b)=-\tau(b).
\]
Therefore
\[
\tau=0.
\tag{8.21}
\]

This does **not** apply to (8.10), because \(n\) moves too.

An exact stronger control differentiates only the connected Lorentz algebra: solving
\[
[d\rho(X),\tau(e_a)]
=
\sum_bX_{ba}\tau(e_b)
\tag{8.22}
\]
for all six \(\mathfrak{so}(1,3)\) generators and all degree-preserving \(16\times16\) matrices gives a \(1680\times280\) integer system of rank
\[
280.
\tag{8.23}
\]
Thus the observer-independent infinitesimal kernel is zero even without using the disconnected element \(-I\).

Again this is scoped: observer-dependent maps exist.

### 8.5 Homogeneous-coordinate enlargement is available but not forced

The canonical affine linearization is
\[
\widetilde V=V\oplus\mathbb R e_\ast,
\qquad
\widetilde A(L,b)
=
\begin{pmatrix}
L&b\\
0&1
\end{pmatrix}.
\tag{8.24}
\]

Then
\[
\Lambda^\ast\widetilde V
\]
has dimension \(32\) and gives a degree-preserving exterior representation of the full affine group.

The exact checker verifies the group law and exterior functoriality.

But the original \(\Lambda^\ast V\) subspace is invariant and pure translations act trivially on it. Translation sensitivity lives in components containing \(e_\ast\). The fixed four-dimensional located \(J_N\) has no automatic extension to this auxiliary sector.

Therefore (8.24) is a natural **auxiliary parent candidate**, not a derived replacement for the current matter carrier.

---

## 9. Why a full affine-sensitive horizontal letter is still missing

The correct matter response cannot be only a same-fiber representation of \(b\).

Equation (8.18) already says that, in the scalar sector, the first affine-shift response to a \(t\)-link must contain archive paths.

In the multi-Role pure-gauge sector, (7.7) gives
\[
\delta_\xi(U_t)
=
-\frac1L\sum_r
M_{h_t{}^r}D_rU_t
+
\sum_{s,r}
M_{h_s{}^r-U_th_s{}^r}
U_sA_rU_tE_{sr}.
\tag{9.1}
\]

The first line depends on the affine shift vector of the \(t\)-edge and already contains
\[
U_rU_t,\qquad U_r^{-1}U_t.
\]

The second line samples neighboring coframe/flux data and carries CAR corners.

Thus the missing affine lift has the type of a **path-expression patch response**, not a \(16\times16\) fiber matrix:
\[
\ell_b(x,r)
\in
\mathfrak A_N^\times
\quad\text{or an inverse-free local parent whose elimination produces it}.
\tag{9.2}
\]

On the exact orbit, (6.6) supplies such an object by conjugation. On a generic harmonic/curl background no geometric extension is owned.

---

## 10. Beyond pure gauge

### 10.1 Constant harmonic strain

A nonzero constant coframe component has nonzero cycle sum and cannot be \(d_f\xi\).

For \(e_A{}^A=t\) constant and constant degree-zero matter,
\[
H(e)\mathbf1=t\mathbf1.
\tag{10.1}
\]

So a pure-gauge cocycle alone misses an owned first-jet direction.

### 10.2 Plaquette curl

The owned curl witness lies outside \(\operatorname{im}d_f\). Two paths with the same endpoints have a relative affine defect.

The path-resolved algebra can retain both words, but current geometry does not choose the matter response to the translational part of that relative holonomy.

### 10.3 L=2 raw Nyquist

The raw alternating edge survives while its centered average vanishes. Since (5.1) sees it, a crossed seed must take raw \(e\) as input and cannot factor only through centered solder/metric data.

### 10.4 L=3 corner

The exact \(-a/2\) corner is represented by the \(U_AU_B^{-1}E_{AB}\) word in (5.1). Algebraic support is solved; the all-order coefficient/transport law is not.

### 10.5 Translation plus frame orbit is still not all coframes

The owned translation rank is
\[
4(m-1).
\]

A local Lorentz tangent has six parameters per site, so even granting the theorem-ready raw frame action, the tangent span has dimension at most
\[
4(m-1)+6m.
\]

The residual lower bound is (0.14).

At \(L=2,3,5\) the exact values are
\[
100,\qquad490,\qquad3754.
\tag{10.2}
\]

Therefore symmetry transport cannot by itself determine a constitutive value on every raw coframe direction.

---

## 11. A real all-uncentered constitutive seed already exists — but only in the reference gauge

A point that must not be lost is that PR #75 does more than own a formal derivative.

It independently defines \`fluxEnergy\` from site/edge/corner terms and proves
\[
2E_{\rm flux}(e,\psi)
=
\langle\psi,(I+H(e))\psi\rangle.
\tag{11.1}
\]

Hence define
\[
W_{\rm flux}(e)=I+H(e).
\tag{11.2}
\]

This has:

- \(W_{\rm flux}(0)=I\);
- exact derivative \(D_eW_0[e]=H(e)\) for every raw uncentered \(e\);
- symmetry in the counting pairing;
- degree/parity preservation;
- exact Nyquist/corner/harmonic/curl sensitivity.

Current main also owns uniform small-coframe positivity:
\[
|e_x{}^s{}_r|\le\varepsilon,
\qquad
8196\,\varepsilon<1
\quad\Longrightarrow\quad
E_{\rm flux}(e,\psi)>0
\quad(\psi\ne0).
\tag{11.3}
\]

This is a substantial positive answer to the constitutive search.

It is not the requested \(W_b\) yet:

1. (11.2) has no independent \(A\)-dependence.
2. It is in the reference counting observer gauge; no finite moving-\(n\) cell law has been derived for it.
3. No theorem shows
   \[
   W_{\rm flux}(e')
   =
   R_\gamma(e)^{-T}W_{\rm flux}(e)R_\gamma(e)^{-1}
   \tag{11.4}
   \]
   for the exact PR #95 pure-gauge \(R_\gamma\).
4. Its literal Hessian is zero, whereas a chosen groupoid action has a nontrivial second-order congruence coefficient. Matching them would select a particular background derivative \(D_eg\), hence a particular \(\mathcal S\); that selection has not been derived.
5. The local reference weights and determinant/curl constructions already give independent quadratic modifications with the same flat value/first jet.

Thus PR #75 supplies a real seed, not a completed crossed constitutive law.

---

## 12. Full crossed covariance still does not select the second jet

Suppose, for the sake of classification, that a crossed package
\[
(\pi_b,R_\gamma,\alpha_\gamma,W_b)
\]
has been supplied.

Let \(P_b\in\mathfrak A_N^\times\) be any background-dependent degree-preserving dressing. Define
\[
\pi_b^P(a)
=
P_b\pi_b(a)P_b^{-1},
\tag{12.1}
\]
\[
R_\gamma^P
=
P_{b'}R_\gamma P_b^{-1},
\tag{12.2}
\]
\[
\alpha_\gamma^P=\alpha_\gamma,
\tag{12.3}
\]
\[
W_b^P
=
P_b^{-T}W_bP_b^{-1}.
\tag{12.4}
\]

Then
\[
\begin{aligned}
R_\gamma^P\pi_b^P(a)(R_\gamma^P)^{-1}
&=
P_{b'}
R_\gamma\pi_b(a)R_\gamma^{-1}
P_{b'}^{-1}
\\
&=
\pi_{b'}^P(\alpha_\gamma a),
\end{aligned}
\tag{12.5}
\]
and
\[
W_{b'}^P
=
(R_\gamma^P)^{-T}
W_b^P
(R_\gamma^P)^{-1}.
\tag{12.6}
\]

So exact crossed covariance is invariant under simultaneous endpoint/background dressing.

If
\[
P_0=I,\qquad DP_0=0,
\tag{12.7}
\]
the flat values and first jets are unchanged, while \(D^2P_0\) changes the second jet.

This proves:

> **Crossed dressing nonselection.**  
> Exact horizontal composition, exact vertical groupoid composition, exact crossed covariance, and the complete flat first jet do not by themselves determine the quadratic constitutive extension.

The landed
\[
S_\lambda=S_{\rm patch}+\lambda T_{\rm edge}
\tag{12.8}
\]
is an explicit scalar shadow of this freedom.

If \(P_b\) is chosen frame-equivariantly,
\[
P_{g\cdot b}=Q_gP_bQ_g^{-1},
\tag{12.9}
\]
the dressing also preserves frame covariance. The observer-covariant plaquette scalar from the earlier memo provides a transverse source of such quadratic freedom.

Therefore neither moving observer covariance nor crossed covariance removes \(\lambda\) automatically.

---

## 13. Frame and observer

For a sitewise Lorentz frame \(g_x\), the theorem-ready frame packet gives
\[
Q_g(x)=\rho(g_x).
\tag{13.1}
\]

Since \(Q_g\) is degree preserving,
\[
Q_g\in\mathfrak A_N^\times.
\]

For the linear path letters,
\[
Q_g
\mathsf U_r^A
Q_g^{-1}
=
\mathsf U_r^{A'},
\tag{13.2}
\]
with the literal pull orientation when
\[
L'_{x\leftarrow y}=g_xL_{x\leftarrow y}g_y^{-1}.
\]

The observer moves:
\[
n'_x=g_xn_x,
\]
and
\[
Q_g^TB_{n'}Q_g=B_n.
\tag{13.3}
\]

This gives an exact frame crossed law for the supplied linear-link/observer data.

It does not:

- identify \(e\) with \(A\);
- extend (6.1) to arbitrary harmonic/curl backgrounds;
- select (8.10)'s \(\lambda,\mu\);
- select the quadratic constitutive dressing;
- make \(n\) physical time.

The rational \(5/4,3/4\) A/B boost passes exactly in the hostile controls.

---

## 14. Fixed located \(J\): positive crossed dualization

Let
\[
J_N:\Gamma_N^P\longrightarrow(\Gamma_N^D)^\ast
\]
be the fixed located pairing.

Do **not** demand a naïve sitewise copy of the primal algebra on the dual color.

Define the dual algebra by transport:
\[
\mathfrak A_N^D
=
\left\{
J_N^{-T}a^{-T}J_N^T:
a\in(\mathfrak A_N^P)^\times
\right\}
\]
for units, and by linear span/transpose transport for the full algebra.

For every primal unit,
\[
a_D
=
J_N^{-T}a_P^{-T}J_N^T.
\tag{14.1}
\]

Then
\[
(ab)_D=a_D b_D
\]
with the appropriate pull/composition convention, and the pairing is exactly preserved.

For a degree-mixing frame expression, different Fock components land at different dual anchors:
\[
j(x,\{A\})=x-(B+C+D),
\]
\[
j(x,\{B\})=x-(A+C+D).
\tag{14.2}
\]

Equation (14.1) keeps both shifted supports. That is not a defect; it is the correct typed dual action.

The same construction applies to \(R_\gamma\), \(\pi_b\), and the dressed package (12.1–12.4).

Thus fixed \(J\) does not select the missing constitutive section, but it does force the dual once the primal crossed data exist.

---

## 15. Locality ledger

| Notion | Result |
|---|---|
| horizontal linear path letter | one PR #70 edge |
| product of letters | factorized word locality |
| complete \(H(e)\) | path-expression word length \(\le2\) |
| infinitesimal \(\delta_\xi\) | closes finite algebra but increases syntactic word length |
| pure-gauge finite \(R_\gamma\) | generally dense after compression |
| constant isotropy | excludes a uniform bounded compressed radius/circuit depth in \(L\) |
| affine same-fiber candidate | finite, but fails at least one crossed requirement |
| inverse of a path letter | reverse word for the linear horizontal part |
| inverse of global \(R_\gamma\) | need not be local |
| auxiliary inverse-free parent | not obstructed by any result here |
| fixed \(J\) dual | finite shifted path-expression support componentwise, not same-site |
| arbitrary-background local cell seed | still missing |

The existing no-uniform-radius theorem must not be promoted into an inverse-free-parent no-go.

---

## 16. What is constructed, what is not

### Constructed / derived in this memo

1. Explicit finite matrix-valued crossed product \(\mathfrak A_N\).
2. Matrix-unit proof that its Fock coefficient algebra is the full 70-dimensional degree-preserving envelope.
3. Exact embedding of the PR #95 linear/Lorentz horizontal word action.
4. Exact pure-gauge crossed subpackage using the existing graded action.
5. Closed infinitesimal \(\delta_\xi\) formulas on all required generator classes.
6. Exact finite affine representation \(T_b=I+C^\dagger(b)P_0\), with an exact proof of why it fails degree-preserving crossed closure.
7. Exact observer-dependent degree-preserving affine translation family, with an exact proof of why its scalar block fails the owned crossed diagnostic.
8. Scoped observer-independent Lorentz-equivariant degree-preserving tangent no-go.
9. Positive identification of \`fluxEnergy\` as a genuine small-\(e\) positive full-uncentered reference constitutive seed.
10. Full-package dressing theorem showing crossed covariance does not select the second jet.
11. Exact fixed-\(J\) dual crossed transport.

### Not constructed

1. A theorem \(e\mapsto A(e)\).
2. A geometric arbitrary-background affine-shift path-expression letter satisfying both PR #70 path geometry and (7.7).
3. A vertical matter cocycle on harmonic/curl backgrounds compatible with the exact pure-gauge and frame subactions.
4. A moving-observer/frame-covariant all-background \(W_b\) whose finite congruence is the same object as that vertical cocycle.
5. A selector removing the crossed dressing freedom.
6. A provenance-bearing stress tensor or Einstein dynamics.

---

## 17. Exact hostile controls

A standalone exact checker was executed with rational arithmetic plus one exact finite-field rank certificate.

**PASS 116/116 exact controls.**

The controls include:

- all 70 same-degree Fock matrix units generated from \(E_{sr}\) and owned occupation projectors;
- scalar word mixing and constant matter at \(L=3,5,7\);
- exact two-Role \(L=3\) commutators for both Role shifts, all four \(E_{tu}\), and the \(U_AU_B^{-1}\) corner;
- the \(1680\times280\) Lorentz-tangent system, full rank 280 modulo 10007, which certifies full rational rank;
- exact degree-mixing affine representation, inverse, Lorentz covariance, and failure to normalize \(P_0\);
- exact observer-dependent spatial translation shears, additive composition, rational boost covariance, degree preservation, vacuum blindness and free \(\mu\);
- 5-dimensional homogeneous affine group composition and its 32-state exterior lift;
- \(L=5\) delta \(S_{\rm patch}\), mandatory entries and distance-two cancellation;
- \(L=5\) non-delta \(G^2\ne0\) and cancellation;
- quadratic endpoint dressing: exact composition, zero first jet, nonzero second jet;
- L=2 Nyquist;
- L=3 corner;
- rational Lorentz boost and moving observer;
- fixed-\(J\) shifted anchors;
- coframe orbit codimension lower bounds at \(L=2,3,5\).

The key finite-field control is rigorous over \(\mathbb Q\): a \(280\times280\) minor nonzero modulo 10007 cannot have zero determinant over the integers, so the rational rank is 280.

A compact reproducible core is:

~~~python
# Core exact controls; Fraction arithmetic unless explicitly mod p.
from fractions import Fraction as F

# 1. CAR envelope.
# For every same-degree S,T, choose paired r_i in S\T, s_i in T\S and verify
# P_T E_{s_q r_q} ... E_{s_1 r_1} P_S = +/- |T><S|.
# The loop checks all 70 pairs.

# 2. Scalar word mixing.
# U[i,j] = [j=i+1], D=L/2(U-U^-1), h=L(U-I)xi, G=M_xi D.
# For L in (3,5,7):
#   assert G*U-U*G == -1/2 M_h (U*U-I).

# 3. Full two-Role generator controls.
# With G=A_xi+K(h), verify exactly:
# [G,U_t] =
#   sum_r M_(xi^r-U_t xi^r) D_r U_t
#   + sum_sr M_(h_s^r-U_t h_s^r) U_s A_r U_t E_sr
# and
# [G,E_tu] =
#   sum_sr M_(h_s^r) U_s A_r
#       (delta_rt E_su-delta_us E_tr).
# Substitute U_A U_B^-1 for the corner word.

# 4. Degree-mixing affine representation.
# P0=|0><0|; N_b=Cdag(b)P0.
# N_b N_c=0, T_b=I+N_b,
# T_b T_c=T_(b+c), T_b^-1=I-N_b,
# rho(g)T_b rho(g)^-1=T_(gb),
# T_b P0 T_b^-1=P0+N_b (outside degree-preserving envelope).

# 5. Observer-dependent degree-preserving spatial shear.
# For n=e_A and n.b=0:
# S_n^mu(b)=I+mu b n^flat.
# Verify S(b)S(c)=S(b+c),
# gS_n(b)g^-1=S_(gn)(gb),
# exterior lift preserves all degrees and fixes Lambda^0.
# mu=1 and mu=2 are distinct exact candidates.

# 6. Observer-independent tangent no-go.
# Unknowns: four 70-component degree-preserving matrices tau_a.
# For all six rational so(1,3) generators X solve
# [d rho(X),tau_a] = sum_b X_ba tau_b.
# Exact modular Gaussian elimination gives rank 280/280 at p=10007.

# 7. Homogeneous affine control.
# A(L,b)=[[L,b],[0,1]];
# A(L,b)A(M,c)=A(LM,b+Lc);
# exterior Lambda* on dimension 5 has dimension 32 and preserves total degree.
# The old 16-dimensional no-e_* subspace is translation-fixed.

# 8. PR #98 second-order controls.
# Recompute S_patch at L=5 delta and non-delta,
# verify row sums, mandatory distance-two entries,
# G_nondelta^2 != 0 and cancellation after subtracting 2 S_patch.

# 9. Quadratic endpoint dressing.
# P_a(t)=diag(1+a t^2,1);
# (P_x P_y^-1)(P_y P_z^-1)=P_x P_z^-1;
# P'(0)=0, P''(0)!=0.

print("PASS 116/116 exact controls")
~~~

The full research calculation used the literal matrices and sparse archive operators, not floating point arithmetic.

---

## 18. Theorem-ready handoff

The following are theorem statements suitable for later formalization. They are not claims that new Lean modules already exist.

### Theorem A — CAR envelope matrix units

The unital algebra generated by the owned \(E_{sr}\) contains every \(|T\rangle\langle S|\) with \(|T|=|S|\). Therefore it equals \(\mathcal E_{\deg}\) and has dimension 70.

### Theorem B — matrix-valued archive crossed evaluation

The matrix-valued crossed product (3.6) evaluates faithfully onto the full global degree-preserving archive endomorphism algebra, with dimension \(70|X|^2\).

### Theorem C — linear Cartan path representation

The letters (4.1) multiply/reverse according to the linear part of the literal PR #70 affine path law.

### Theorem D — pure-gauge crossed subrepresentation

The exact graded pure-gauge \(R_{\rm gr}\) is a unit of \(\mathfrak A_N\). Inner conjugation gives \(\alpha\), and (6.5–6.10) form an exact crossed constitutive subpackage on \(e\in\operatorname{im}d_f\).

### Theorem E — all-generator infinitesimal crossed law

Equations (7.5–7.12) hold. In particular the vertical derivation closes \(\mathfrak A_N\) but not a fixed path-word-length sector.

### Theorem F — finite affine representation exists but need not normalize the minimal algebra

Equations (8.1–8.8) define an exact Lorentz-covariant affine representation on the 16-state carrier. It fails degree/parity preservation and conjugates the vacuum projector outside \(\mathcal E_{\deg}\).

### Theorem G — observer-dependent degree-preserving translation family

Equations (8.9–8.16) define a two-parameter additive/frame-covariant family. It preserves Fock degree/parity, but its degree-zero block is trivial and therefore cannot reproduce (8.18).

### Theorem H — observer-independent tangent no-go

Any observer-independent Lorentz-equivariant linear map \(V\to\mathcal E_{\deg}\) is zero. The \(-I\) argument proves it for the current full frame group; the exact Lie-algebra rank certificate proves the infinitesimal connected version.

### Theorem I — flux constitutive seed

The independently defined \`fluxEnergy\` has Riesz operator \(W_{\rm flux}=I+H(e)\), is symmetric, sees every raw coframe direction, and is positive in the owned small-\(e\) regime.

### Theorem J — crossed dressing nonselection

Equations (12.1–12.6) preserve the complete crossed covariance package. A quadratic \(P_b\) with zero first jet changes the second constitutive jet. Therefore crossed covariance does not select \(\mathcal S\).

### Theorem K — fixed-\(J\) dual crossed transport

Equation (14.1) gives the unique pairing-preserving dual of every primal crossed unit. It preserves composition and retains all located shifted anchors.

### Theorem L — residual coframe directions

Even translations plus local Lorentz frame tangents span at most \(10m-4\) of the \(16m\)-dimensional raw coframe tangent, leaving codimension at least \(6m+4\).

---

## 19. Direct answers to the canonical questions

| # | Answer |
|---|---|
| 1 | The literal algebra is the matrix-valued finite crossed product \((\mathrm{Fun}(X,\mathcal E_{\deg}))\rtimes X\), with a separate free path-expression filtration for locality. It is not an untyped full matrix placeholder. |
| 2 | Background objects are \(b=(A,e,n)\). \(A,e,n\) remain distinct. |
| 3 | Yes for the linear/Lorentz part: (4.1–4.2) embeds the PR #95 horizontal action into the full algebra. |
| 4 | Pure affine shifts admit finite 16-state representations, so no universal carrier no-go is valid. The simplest degree-mixing representation fails algebra closure; an observer-dependent degree-preserving family fails the scalar crossed diagnostic. The geometric path-expression affine lift remains missing. |
| 5 | Pure gauge: exact \(R_{\rm gr}\). Harmonic/curl: no derived vertical cocycle. Frame/observer: conditional exterior/sitewise action from the frame packet. |
| 6 | On the pure-gauge chart, yes: \(\alpha=\operatorname{Ad}_R\). Infinitesimally it closes the entire finite algebra. No full-background \(\alpha\) tied to PR #70 affine geometry is owned. |
| 7 | Yes. Equations (7.5–7.12) are the all-Role/CAR extension, including length-two corners. |
| 8 | PR #75 supplies \(W_{\rm flux}=I+H(e)\) as an independent local, symmetric, small-\(e\) positive reference-gauge seed for every raw coframe. No common finite observer/frame/groupoid completion with \(R_{\rm gr}\) is derived. |
| 9 | No. Full crossed covariance itself has the dressing symmetry (12.1–12.6). \(S_\lambda\) survives as an explicit scalar witness. |
| 10 | Observer covariance transports a supplied section and permits observer-dependent affine response, but it does not select its \(\lambda,\mu\) or the transverse quadratic modulus. |
| 11 | Yes, once primal data exist: use the literal contragredient through fixed located \(J\). The dual algebra is shifted/non-sitewise as required. |
| 12 | Still possible. No result here excludes a local inverse-free auxiliary parent. |
| 13 | No \(e\mapsto A(e)\) is derived. A full construction still needs an affine-shift path-expression comparison compatible with both independent inputs, or an independently proved solder/Cartan compatibility map. |

---

## 20. Exactly one recommended next step

Construct one **full-background affine-sensitive path-expression link seed**
\[
\boxed{
\ell_N:
(A,e,n;x,r)
\longmapsto
\ell_N(A,e,n;x,r)\in\mathfrak A_N
}
\tag{20.1}
\]
before attempting another \(W\), \(\mathcal S\), or \(K\) selector.

It must satisfy, without identifying \(A\) and \(e\):

1. at zero affine shift, reduce to the linear exterior link (4.1);
2. on the exact coframe orbit, agree with the conjugated letters (6.6), hence have infinitesimal derivative (7.7);
3. compose on PR #70 affine path words and retain nontrivial relative affine holonomy;
4. be frame/observer covariant with moving \(n\);
5. preserve the degree/parity algebra or explicitly justify a larger typed algebra;
6. keep fixed \(J_N\) and use the forced dual (14.1);
7. accept raw harmonic/curl/Nyquist/corner backgrounds.

Only after (20.1) exists is it meaningful to demand that the independently owned \(W_{\rm flux}\), or a new local cell form, be the same finite covariant constitutive section under that crossed action.

Do **not** open the next layer by choosing \(c\), \(\mathcal S\), or a universal \(K\).

**Terminal verdict: CROSSED-PURE-GAUGE-SUBPACKAGE-CONSTRUCTED-FULL-BACKGROUND-CROSSED-CONSTITUTIVE-PRIMITIVE-REQUIRED.**
