# A4D free-path/groupoid crossed matter lift: response and descent boundary

**Task:** `EXP-A4D-PATH-GROUPOID-CROSSED-MATTER-LIFT`  
**Baseline:** `cc63bee5da782245a1f29eeca54e0e2f1ca6e666` (current `main` after merged #101/#102)  
**Terminal:** `PATH-GROUPOID-LIFT-REQUIRES-NEW-AFFINE-PATH-RESPONSE-PRIMITIVE`  
**Status:** theorem-ready research classification, no new Lean source and no general-background matter lift claimed.

## 1. Inputs and ownership

Read fully: `MEMO_A4D_CROSSED_CONSTITUTIVE_REPRESENTATION.md`;
`MEMO_A4D_PATH_RESOLVED_MATTER_WORD_ACTION.md`; PR #70 owners
`ArchiveChainConnection.lean`, `ArchiveChainCurvature.lean`,
`ArchiveAffineCartanConnection.lean` and `ArchivePathWordAlgebra.lean`;
merged #102 owners `A4DScalarBackgroundWordMixing.lean`,
`A4DStaggeredFirstJetPathExpansion.lean`,
`A4DHorizontalDressingSecondJetFreedom.lean` and
`A4DCrossedPathAlgebraBoundary.lean`; and the located placement/star
owners `A4DLocatedPrimalDualCell.lean` and
`A4DLocatedTopologicalStar.lean`. PR #103 and parallel integrability
worker #108 remain unmerged; no statement from either branch is used.

Here \(A\) is an independently specified affine Cartan connection,
\(e\) a raw coframe, \(n\) an observer, \(p\) a *literal* oriented archive
path. None determines another. A relation between \(A\) and \(e\)
appears only on the explicitly marked *joint pure-gauge orbit*.

The main outcome has two parts. Given an admissible invertible
elementary matter link, PR #70 supplies the free-path representation
and a sharp holonomy descent theorem. The landed owners do **not**
supply the affine-sensitive elementary response for independent
\((A,e,n)\). Moreover their pure-gauge derivative excludes a
fiber-only, fixed-site one-edge letter. Free-path composition cannot
manufacture the missing response.

## 2. Literal paths and a typed conditional target

Set \(L=N+2\ge2\), \(X=(\mathbb Z/L)^4\),
\(\mathcal F=\Lambda^*\mathbb R^4\), and
\(\Gamma_N=\operatorname{Fun}(X,\mathcal F)\).
PR #70's `ChainStep` is `.fwd r` or `.bwd r`, and
`pathEnd N p x` transports a base point through a `List ChainStep`.
The negative letter is the inverse of the positive link at the
**shifted** starting point. The two labels remain distinct even when
\(L=2\) and their endpoints coincide.

`ArchivePathWordAlgebra.lean` also defines `ChainPath E x y`,
`pathAppend`, `pathReverse` and pull-order `pathEval`. Since its \(E\)
has type `X → X → Prop`, simple adjacency does not store two parallel
slot labels at \(L=2\). Use the *existing* slot-faithful
`List ChainStep` with starting point and `pathEnd`, and transfer the
inductive `ChainPath` proofs to it. Any subsequent proof-relevant
edge typing must preserve these labels. `PathExpr α` is existing syntax
for word, sum, product, bracket and `rev`; formal `rev` of a sum is
not automatically a multiplicative inverse of its evaluated operator.

For a genuine local transport, conditionally choose coefficient
modules \(V_x\) and positive isomorphisms
\(\ell^+_{A,e,n}(x,r):V_{x+r}\to V_x\); put
\(\ell^-_{A,e,n}(x,r)=\ell^+_{A,e,n}(x-r,r)^{-1}\).
For the pure-gauge package below, the useful coefficients instead
live in moving corners of \(\operatorname{End}(\Gamma_N)\). These are
typed paths in local coefficient isomorphisms, *conditional* on a
positive link actually existing. Arbitrary inverses of sums of finite
words need not lie in the inverse-free syntactic `PathExpr` algebra.

For either typed family, with \(x_0=x\) and
\(x_i=\operatorname{pathEnd}(x;[s_1,\ldots,s_i])\), define

\[
\Pi_{A,e,n}(x;[s_1,\ldots,s_j])
 =\ell(x_0,s_1)\cdots\ell(x_{j-1},s_j).
\]

Empty words evaluate to \(1_{V_x}\). Associativity and the shifted
inverse prove the exact pull laws

\[
\Pi(x;p{+\!\!+}q)=\Pi(x;p)\Pi(\operatorname{end}(x;p);q),\qquad
\Pi(\operatorname{end}(x;p);p^{-1})=\Pi(x;p)^{-1}.                 \tag{2.1}
\]

No flatness is used. These are the `affinePath` and
`pathEval_append`/`pathEval_reverse` laws of PR #70. The honest target
for the present conditional statement is local isomorphisms or
appropriate invertible corners of the finite global endomorphism
algebra, *retaining the free path as a label* of evaluation.

## 3. Independent affine path data

The literal affine link is \(A(x,r)=(L_{x,r},b_{x,r})\), a pull
\(V_{x+r}\to V_x\), with \((L,b)(M,c)=(LM,b+Lc)\).
Reverse is the shifted inverse. If same-endpoint paths \(p,q\)
give \((P,a),(Q,b)\), their based relative holonomy is

\[
(P,a)(Q,b)^{-1}=(PQ^{-1},a-PQ^{-1}b).                           \tag{3.1}
\]

The open affine torsion in `ArchiveAffineCartanConnection.lean` is
\(a-b\); the based shift is \((a-b)+(I-PQ^{-1})b\). These are
different on a curved linear background. A node gauge gives
\(A'_{x,r}=h_xA_{x,r}h_{x+r}^{-1}\), and path transport transforms at
the two endpoints. For the flat translation orbit
\(h_x=(I,-L\xi(x))\), the affine shift is
\(L(\xi(x+r)-\xi(x))=d_f\xi\) **exactly**. That checks the joint
pure-gauge \((A,e)\) orbit; it is no formula for independent \(A,e\).
The homogeneous exterior/Lorentz link is required only in the
zero-shift, flat-coframe *linear* limit.

## 4. Complete landed jet and pure-gauge link derivative

Write \((U_rf)(x)=f(x+r)\),
\(D_r=\frac L2(U_r-U_r^{-1})\),
\(B_r=\frac12(I+U_r^{-1})\) (backward average, not affine \(A\)),
\(E_{sr}=c_s^\dagger c_r\), and \(M_f\) for site multiplication.
The entire owned degree- and parity-preserving first jet is

\[
K(e)=\sum_{s,r}M_{e_s{}^r}U_sB_rE_{sr},\quad
H(e)=\sum_r\tfrac12(M_{e_r{}^r}U_r+U_r^{-1}M_{e_r{}^r})
       -K(e)-K(e)^T.                                           \tag{4.1}
\]

\(U_sB_r=\tfrac12(U_s+U_sU_r^{-1})\) retains the length-two
distinct-role corner and same-role onsite contribution. For
\(h=d_f\xi\), the exact first-jet Ward owner is

\[
G_\xi=\sum_aM_{\xi^a}D_a+K(h),\qquad H(h)=-(G_\xi+G_\xi^T).        \tag{4.2}
\]

In the already owned open invertible pure-gauge chart, denote by
\(F_\phi\) the #101 dressing
\((I+K(d_f\phi))(F^{\rm sc}_\phi\otimes I_{\mathcal F})\),
where its **normal-ordered row convention** is
\(F^{\rm sc}_\phi(x,y)=
[\exp(\sum_a\phi^a(x)D_a)]_{xy}\).
In particular this is generally **not**
\(\exp(\sum_a M_{\phi^a}D_a)\).
Its exact identities include
\(F_{\phi+c}=F_\phi\exp(\sum_a c^aD_a)\). Thus the *constructed*
global pure-gauge bisection letter is

\[
\mathscr L_t(\phi)=F_\phi U_tF_\phi^{-1}.                        \tag{4.3}
\]

It is invariant under \(\phi\mapsto\phi+c\), since the constant
exponential commutes with \(U_t\); the moved-background cocycle
\(R_\xi(\phi)=F_{\phi+\xi}F_\phi^{-1}\) is exact on the common
chart. The bisections commute, have exact inverses and satisfy
all period relations. This constructs the *joint pure-gauge
subpackage*, not a link for arbitrary \(A,e,n\).

At the flat point, any family agreeing on this orbit must have

\[
\dot{\mathscr L}_t(d_f\xi)=[G_\xi,U_t]
=-\frac1L\sum_a M_{h_t{}^a}D_aU_t+[K(h),U_t].                 \tag{4.4}
\]

Here
\([K(h),U_t]=\sum_{s,r}M_{h_s{}^r-U_th_s{}^r}
U_sB_rU_tE_{sr}\), retaining \(U_sU_t\),
\(U_sU_r^{-1}U_t\), and CAR sectors. The scalar one-cycle
sector includes \(-\tfrac12M_h(U_t^2-I)\). Thus the
**full landed jet** constrains the operator's spatial support,
not only its fiber matrix.

**Scoped fixed-site obstruction.** At \(L=5\), take
\(\xi=\delta_0\) along a one-coordinate scalar cycle. Then
\([M_\xi D,U]_{0,0}=-5/2\) and
\([M_\xi D,U]_{0,2}=+5/2\). The derivative of any family
of fixed-site one-edge letters \(M_{C_t(e)(x)}U_t\), with
fiber size 16 or 32, has only one-edge spatial support and cannot
match both entries. This excludes *that ansatz*, not a larger
path/CAR target. At \(L=2\), \(U=U^{-1}\), \(D=0\);
the scalar obstruction vanishes but occupied CAR sectors retain
the Nyquist first jet. Neither (4.1) nor (4.4) assigns an affine
response for general independent \(A,e,n\).

### Diagnostic first-order extension, with explicit nonselection

The following is a **chosen diagnostic**, not a physical/link primitive
selected by the landed owners:

\[
Q_t(e):=-\frac1L\sum_aM_{e_t{}^a}D_aU_t+[K(e),U_t],
\quad B_t(e):=Q_t(e)U_t^{-1}
=-\frac1L\sum_aM_{e_t{}^a}D_a+
K(e)-\operatorname{Ad}_{U_t}K(e).                              \tag{4.5}
\]

It agrees with the forced commutator (4.4) on exact coframes.
Over dual numbers \(\varepsilon^2=0\), the units
\(U_t+\varepsilon Q_t\) have exact inverse
\(U_t^{-1}-\varepsilon U_t^{-1}Q_tU_t^{-1}\), hence exact
append/reverse in that infinitesimal ring. The block-matrix
realization is just dual-number bookkeeping, unrelated to
homogeneous 32-state affine fiber homogenization. No real finite
background link or second jet is selected. Any independent
curl/period response vanishing on exact \(e\) changes the unknown
general link while leaving (4.4) unchanged.

For this diagnostic, direct substitution gives

\[
\Omega_{rs}^{(1)}
=B_r+\operatorname{Ad}_{U_r}B_s-\operatorname{Ad}_{U_s}B_r-B_s
=-\frac1L\sum_aM_{c_{rs}{}^a}D_a,\quad
c_{rs}{}^a=e_r{}^a+U_re_s{}^a-U_se_r{}^a-e_s{}^a.              \tag{4.6}
\]

The \(K\) coboundary cancels even with its CAR corners. For a
length-\(L\) cycle in direction \(t\),

\[
\Omega_t^{(1)}
=\sum_{j=0}^{L-1}\operatorname{Ad}_{U_t}^{j}B_t
=-\frac1L\sum_aM_{\sum_jU_t^je_t{}^a}D_a.                    \tag{4.7}
\]

Equations (4.6)–(4.7) are **only** about the diagnostic (4.5).
They do not prescribe the holonomy of every possible
affine-sensitive response.

## 5. Holonomy, exact descent and compressed crossed product

For paths \(p,q:x\to y\), if positive letters have been supplied,
the matter comparison is
\(\mathcal H_{A,e,n}(x;p,q)=\Pi(x;p)\Pi(x;q)^{-1}\).
The structural model is the exact #70 theorem
`pathEval_factors_pairGroupoid_iff_trivial_holonomy`, but its literal
Lean type is `ChainPath E` with `E : X → X → Prop`. Therefore that
owned theorem does **not by itself** retain two parallel edge labels
when distinct slots have the same ordered endpoints, as happens for
`.fwd r` and `.bwd r` at \(L=2\).

For the slot-faithful parent used here, define a labelled path by a
starting site together with `p : List ChainStep`, with endpoint
`pathEnd N p x`, and evaluate it by the shifted positive/inverse
letters of §2. The theorem-ready labelled analogue is

\[
[\forall x,y,p,q,\ 
  \operatorname{end}(x;p)=y=
  \operatorname{end}(x;q)\Rightarrow
  \Pi(x;p)=\Pi(x;q)]
\ \Longleftrightarrow\
[\forall x,p,\ 
  \operatorname{end}(x;p)=x\Rightarrow
  \Pi(x;p)=1_{V_x}].                                           \tag{5.1}
\]

This labelled statement is **research-derived here, not yet a Lean
owner**. Its proof is the same cancellation argument as #70:
the forward direction compares a labelled loop with `nil`; the
reverse compares \(p{+\!\!+}q^{-1}\) with `nil` and cancels
\(\Pi(q)\) using (2.1). No quotient of edge labels is used.

At \(L=2\), (5.1) has a necessary visible collision test:
`.fwd r` and `.bwd r` from the same site have the same endpoint,
so labelled endpoint descent forces their transports to agree.
With the shifted-inverse convention this is exactly the local
length-two period relation
\[
\ell^+(x,r)\,\ell^+(x+r,r)=1.
\tag{5.1a}
\]
Thus the labelled criterion keeps the two slots distinct until
descent is proved; it does not silently identify them through the
Prop-valued adjacency relation.

For the periodic four-dimensional cubical graph with positive and
shifted inverse letters, the corresponding theorem-ready finite
presentation checks all **labelled** oriented elementary plaquette
relations plus one length-\(L\) period in each of four independent
directions at a root, transported by paths to other sites. Backtracks
cancel by construction; plaquettes commute neighboring labelled
steps; periods reduce coordinate winding. At \(L=2\) the period
relation additionally resolves the parallel `.fwd/.bwd` endpoint
collision as in (5.1a). Hence these relations reduce every labelled
loop to the identity. Conversely the labelled iff (5.1) forces every
listed relation. This finite presentation is theorem-ready research
content, not a claim that #70 already formalizes the labelled
\(L=2\) version. Plaquette flatness alone still permits nontrivial
harmonic cycles.

**Membership versus descent.** PR #101's finite algebra is
\(\mathcal A_N=(\operatorname{Fun}(X,E_{\rm deg}))\rtimes X\),
where \(E_{\rm deg}=\bigoplus_k\operatorname{End}
(\Lambda^k\mathbb R^4)\), evaluated as
\(\bigoplus_k\operatorname{End}(\Gamma_{N,k})\).
An individual grade-preserving *global evaluated path operator*
can already be a matrix in this algebra with nontrivial loop
holonomy. Membership does **not** imply that its labelled path
representation factors through canonical endpoint identification.
Equation (5.1) characterizes the latter stronger property.
Conversely endpoint independence of path maps alone does not give
a covariant representation of *site and CAR coefficients*: their
idempotents and corners must satisfy the covariance relations.

For a connected graph with trivial matter loops, pick root paths
and identify all fibers. Their transports give
\(T_{xy}T_{yz}=T_{xz}\), hence a choice of \(Q_x\) with
\(T_{xy}=Q_xQ_y^{-1}\) (in pull order) and
covariant shifts \(T_{x,x+r}=Q_xQ_{x+r}^{-1}\).
Transport compatible site/degree coefficients by \(Q_x\);
matrix units then recover the finite crossed product, using
`crossedEval` of #70 and the degree boundary of #101/#102.
If original fixed \(M_f\) and constant CAR blocks are required,
compatibility of \(Q_x\) with *those* coefficients is an extra
hypothesis. No theorem from unmerged #108 upgrades this claim.

**Constructed pure-gauge endpoint corners.** Let \(P_x\) be
the flat site projector. On the common invertible chart,
\(q_x(\phi)=F_\phi P_xF_\phi^{-1}\) are orthogonal idempotents
with sum one. The arrow

\[
q_xF_\phi U_{y-x}F_\phi^{-1}q_y
=F_\phi P_xU_{y-x}P_yF_\phi^{-1}                         \tag{5.2}
\]

multiplies as a matrix unit and is endpoint dependent.
Summing edge corners reproduces (4.3). Despite invariance
of the **global** (4.3) under \(\phi\mapsto\phi+c\),
individual \(q_x\) can move, because
\(\exp(\sum c^aD_a)\) does not generally commute with \(P_x\).
An \(e=d_f\phi\)-only localization needs a chosen potential chart
or explicit constant-potential isotropy action. This cannot be
replaced by a background-independent fixed-site CAR assumption.

## 6. Exact hostile controls, independently varied backgrounds

All computations below use rationals. In affine tests \(A\)
is independent and \(e\) may be zero; diagnostic matter tests
choose raw \(e\) independently and do **not** set \(A=A(e)\).
Two-role tests embed in four roles by holding spectator
coordinates invariant and retaining all 16 CAR states.

| Control | Exact data and outcome | Scope |
| --- | --- | --- |
| \(L=3\) affine curl | Linear parts \(I\), shift \(b_B(0,0)=v\ne0\), other shifts zero. Paths \(p=(A,B)\), \(q=(B,A)\) from zero to \((1,1)\) have shifts \(0,v\), relative based shift \(-v\). | Same endpoints lose actual affine information. Faithful matter response would detect it; general response is still missing. |
| \(L=3\) diagnostic curl | \(e_B{}^A(0,0)=1\). In (4.6), \(c_{AB}{}^A(0,0)=-1\) and vacuum entry from site zero to \(\hat A\) equals \(+1/2\). | Diagnostic matter plaquette, independently of periods. |
| \(L=5\) affine harmonic cycle | Constant \(b_A=v/5\). Every plaquette compares equally; the \(A^5\) loop shifts by \(v\ne0\). | Plaquette flatness does not imply endpoint descent. |
| \(L=5\) diagnostic harmonic cycle | Constant \(e_A{}^A=1\). Formula (4.6) vanishes, while (4.7) is \(-D_A\ne0\); vacuum \(H(e)\) acts as 1 on constants. | Period and curl are separate tests. |
| Affine exact descent | \(b_r(x)=3(\phi(x+r)-\phi(x))\) at \(L=3\), linear \(I\). Every path shift telescopes; both plaquette and cycle holonomy vanish. | Actual affine endpoint comparison succeeds. |
| Exact pure-gauge matter | (4.3), with inverse in the invertible chart. All shifts commute and their powers satisfy the period relations; (5.2) provides endpoint corners. | Constructed **joint pure-gauge** matter descent. |
| \(L=2\) Nyquist | Occupied one-role invariant block: \(h=(-2,+2)=d_f\xi\), \(D=0\), \(K=\begin{psmallmatrix}-1&-1\\1&1\end{psmallmatrix}\), \(K^2=0\), \(H(h)=\operatorname{diag}(2,-2)\). | Centered scalar derivative vanishes, full CAR jet does not. Preserve both oriented slots. |
| \(L=3\) CAR corner | \(e_A{}^B(0,0)=3\): \(H(e)\) matrix entry from \((0,\lvert A\rangle)\) to \(((1,2),\lvert B\rangle)\) is \(-3/2\). | Distinct-role length-two \(U_AU_B^{-1}c_A^\dagger c_B\) corner of #102. |
| \(L=5\) site-support obstruction | Entries \(-5/2,+5/2\) in (4.4) share output 0 and have inputs 0 and 2. | No fixed-site \(M_CU\) family with fiber dimension 16 or 32 has this derivative. |

Two *hostile*, exact affine fiber lifts cannot substitute for
the missing spatial/constitutive response:

* On 16 Fock states set \(P_0\) to the vacuum projector,
  \(N_b=c^\dagger(b)P_0\), \(T_b=I+N_b\),
  \(\widehat\rho(L,b)=T_b\rho(L)\).
  \(N_bN_c=0\) and
  \(\rho(L)N_b\rho(L)^{-1}=N_{Lb}\), so this is a
  faithful affine representation (linear part visible on
  degree one, translation on vacuum) and distinguishes the
  above affine holonomies. It mixes degree and parity,
  does not normalize \(E_{\rm deg}\), and misses the
  spatial support of (4.4).
* Homogenize \((L,b)\) as
  \(\begin{psmallmatrix}L&b\\0&1\end{psmallmatrix}\)
  on \(\mathbb R^4\oplus\mathbb R\), then use its
  32-dimensional exterior representation.
  It preserves the *new* total degree and faithfully
  retains the affine group law. Translations fix the
  old \(\Lambda^*\mathbb R^4\) sector; the new degree is
  not the archived 16-state CAR grading. The construction
  supplies no required spatial words or located current law.

Affine holonomy is not automatically matter holonomy. An
exterior representation of *only* the linear part misses
translations; the faithful 16/32 controls detect them but
fail the other requirements. Equation (5.1) always evaluates
loops in the **actually selected** matter target.

## 7. Observer/frame, fixed located J and constitutive boundary

Conditionally, if a matter endpoint frame map
\(S_x(g,n)\) is supplied and a link transforms by
\(\ell'_{x,r}=S_x\ell_{x,r}S_{x+r}^{-1}\), then (2.1)
gives \(\Pi'(x;p)=S_x\Pi(x;p)S_y^{-1}\);
based holonomy is conjugated at \(x\). On the already
owned linear exterior sector, \(\rho(g)\) supplies the frame
map; a moving observer Gram satisfies
\(B_{gn}=\rho(g)^{-T}B_n\rho(g)^{-1}\).
A rational \(5/4,3/4\) Lorentz boost verifies this
*transported Gram* choice. A general \((A,e,n)\) endpoint
frame map cannot be inferred from unmerged #103.

The fixed located placement sends a primal basis
\((x,S)\) to \((x-\mathbf1_{S^c},S^c)\), with
archived orientation sign; its inverse sends
\((y,T)\) to \((y+\mathbf1_T,T^c)\).
Let \(J_N\) be the corresponding signed permutation.
Using the pairing \(\psi^TJ_N^T\chi\), for an
actually invertible primal operator \(R_p\) the
forced dual transport in these basis conventions is

\[
R_p^\vee=J_NR_p^{-T}J_N^T,\qquad
R_p^TJ_N^TR_p^\vee=J_N^T.                                  \tag{7.1}
\]

It composes in pull order. A rational exterior boost
with this exact signed permutation preserves (7.1)
and produces offsite dual entries: \(\lvert A\rangle\)
and \(\lvert B\rangle\) have different complementary
corner displacements. This preserves shifted dual
anchors rather than replacing fixed \(J_N\) with
same-site complement. It remains conditional for
the general primal link.

The independently owned constitutive seed is
\(W_{\rm flux}(e)=I+H(e)\).
Because the general-background lift is missing, no
general constitutive compatibility follows. A finite
**pure-gauge subcase** check needs no new second jet:
in the \(L=2\) occupied block above, \(F(t)=I+tK\),
\(F(t)^{-1}=I-tK\), and
\(\mathscr L(t)=F(t)UF(t)^{-1}=U+2tK\)
has \(\mathscr L(t)^2=I\). At \(t=1/4\)

\[
F(t)^TW_{\rm flux}(th)F(t)-I
=-t^2K^TK=-\frac18
\begin{pmatrix}1&1\\1&1\end{pmatrix}\ne0.                 \tag{7.2}
\]

Thus the independently linear \(W_{\rm flux}\) does
not satisfy the finite congruence of *this specific
pure-gauge dressing*. Its first derivative matches
(4.2). Equation (7.2) neither selects nonlinear
information nor rules out a different constitutive
groupoid action; quadratic endpoint dressing
nonselection from #101/#102 remains in force.

## 8. Terminal classification and theorem-ready handoff

The earliest undefined datum is an **affine-sensitive,
site-aware positive path-response map**

\[
(A,e,n;x,r)\longmapsto
\ell_N^+(A,e,n;x,r):
\mathcal V_{x+r}(A,e,n)\xrightarrow{\cong}
\mathcal V_x(A,e,n),                                      \tag{8.1}
\]

with a specified coefficient/site-idempotent action.
Its target must admit the spatial support in (4.4),
distinguish \(L=2\) parallel slots, and keep \(A\)
independent of \(e,n\). It must specify the
zero-shift flat-coframe exterior limit; equality
with (4.3)/(5.2) on the *joint* pure-gauge orbit;
the full CAR jet (4.1) and forced exact-direction
derivative (4.4); independent affine sensitivity;
and claimed frame/located-dual laws. Invertible
positive links force shifted negatives. No landed
owner selects (8.1) on general raw backgrounds,
even at first order in *all* independent \(A,e\)
directions. Calling the product of unspecified
links \(\Pi\) a solution would conceal this gap.

Once (8.1) is supplied, (2.1) proves append/reverse.
The first formal follow-up is the labelled `List ChainStep`
analogue (5.1), using the cancellation proof pattern of the owned
#70 `ChainPath E` theorem without conflating their edge types.
Together with the labelled plaquette relations and four periods
(including the explicit \(L=2\) slot-collision consequence (5.1a)),
that yields the finite-torus endpoint descent criterion.

An evaluated operator may already lie in the compressed matrix
algebra while its *path-labelled* evaluation fails endpoint descent;
this corrects the overly strong initial hypothesis. Transporting
compatible site/degree coefficients is additionally needed for the
full crossed product.

**Terminal verdict:**
`PATH-GROUPOID-LIFT-REQUIRES-NEW-AFFINE-PATH-RESPONSE-PRIMITIVE`.
This is a scoped missing-definition result, not
a universal no-go for every conceivable path/CAR
target and not a selected second jet.

**Exactly one recommended next step:** define the
affine-sensitive, site-aware positive link (8.1), including the joint
pure-gauge chart and independent \(A,e,n\) covariance/first-jet
requirements; in the same formalization, first add the slot-faithful
`List ChainStep` endpoint-independence iff trivial labelled holonomy
lemma using the #70 proof pattern, so the \(L=2\) parallel-slot
boundary is explicit rather than inherited from a Prop-valued edge
relation.

## 9. Reproduction

The self-contained Python 3 checker below uses only
`fractions.Fraction` and sparse dictionaries. Copy
the following fenced block into `check_path_lift.py`
and run `python3 check_path_lift.py`. Its 53 rational
assertions cover the named \(L=2,3,5\) controls,
affine 16/32 group laws, append/reverse, dual-number
inverse, rational observer boost and located dual
pairing. Diagnostic curl/cycle assertions concern
*only* (4.5); no assertion constructs the missing
general-background link.

```python
from fractions import Fraction as F
from itertools import product

checks = []
def ck(name, value):
    assert value, name
    checks.append(name)
def eye(n): return {(i,i): F(1) for i in range(n)}
def add(*aa):
    z = {}
    for a in aa:
        for ij,v in a.items(): z[ij] = z.get(ij,F(0)) + v
    return {ij:v for ij,v in z.items() if v}
def sc(c,a): return {ij:c*v for ij,v in a.items() if c*v}
def tr(a): return {(j,i):v for (i,j),v in a.items()}
def mm(a,b):
    rows,z = {},{}
    for (i,j),v in b.items(): rows.setdefault(i,[]).append((j,v))
    for (i,k),v in a.items():
        for j,w in rows.get(k,[]): z[i,j] = z.get((i,j),F(0)) + v*w
    return {ij:v for ij,v in z.items() if v}
def comm(a,b): return add(mm(a,b),sc(-1,mm(b,a)))
def diag(v): return {(i,i):F(x) for i,x in enumerate(v) if x}
def power(a,k,n):
    out=eye(n)
    for _ in range(k): out=mm(out,a)
    return out
def creator(d,r):
    return {(m|(1<<r),m):F((-1)**((m&((1<<r)-1)).bit_count()))
            for m in range(1<<d) if not m&(1<<r)}

# Exact affine translation controls: 16-state and homogeneous 32-state.
C4=[creator(4,r) for r in range(4)]
P0={(0,0):F(1)}
def T16(b): return add(eye(16),*(sc(b[r],mm(C4[r],P0)) for r in range(4)))
C5=[creator(5,r) for r in range(5)]
def T32(b): return add(eye(32),*(sc(b[r],mm(C5[r],tr(C5[4]))) for r in range(4)))
b=[F(1),F(2),F(0),F(-1)]; c=[F(2),F(-1),F(1),F(0)]
bc=[x+y for x,y in zip(b,c)]
for d,T in [(16,T16),(32,T32)]:
    ck(f'affine-{d}-add',mm(T(b),T(c))==T(bc))
    ck(f'affine-{d}-inverse',mm(T(b),T([-x for x in b]))==eye(d))
ck('16-does-not-normalize-vacuum',
   mm(mm(T16(b),P0),T16([-x for x in b]))==add(P0,mm(add(T16(b),sc(-1,eye(16))),P0)))
ck('16-mixes-parity',T16(b).get((1,0))==1)
ck('32-preserves-degree',all(i.bit_count()==j.bit_count() for i,j in T32(b)))
ck('32-old-sector-translation-fixed',all(T32(b).get((i,j),0)==F(i==j)
   for i in range(32) for j in range(16)))

def path_shift(L,links,word,x):
    x=list(x); v=[F(0)]*4
    for r,sgn in word:
        if sgn<0: x[r]=(x[r]-1)%L
        a=links(tuple(x),r)
        v=[u+sgn*w for u,w in zip(v,a)]
        if sgn>0: x[r]=(x[r]+1)%L
    return tuple(x),v
zero=[F(0)]*4; v=[F(1),F(0),F(0),F(0)]
def curl_links(x,r): return v if x==(0,0) and r==1 else zero
p=[(0,1),(1,1)];q=[(1,1),(0,1)]
yp,bp=path_shift(3,curl_links,p,(0,0));yq,bq=path_shift(3,curl_links,q,(0,0))
ck('L3-curl-same-endpoint',yp==yq==(1,1))
ck('L3-curl-affine-relative', [a-b for a,b in zip(bp,bq)]==[-x for x in v])
ck('L3-curl-matter-control',mm(T16(bp),T16([-x for x in bq]))!=eye(16))
def harmonic_links(x,r): return [a/F(5) for a in v] if r==0 else zero
_,hp=path_shift(5,harmonic_links,p,(0,0));_,hq=path_shift(5,harmonic_links,q,(0,0))
yc,hc=path_shift(5,harmonic_links,[(0,1)]*5,(0,0))
ck('L5-harmonic-plaquette-flat',hp==hq)
ck('L5-harmonic-cycle',yc==(0,0) and hc==v and T16(hc)!=eye(16))
rev=[(r,-s) for r,s in reversed(p)]
_,back=path_shift(3,curl_links,rev,yp)
ck('affine-path-reverse',back==[-x for x in bp])
def phi(x): return [F(x[0]==0),F(x[1]==1),F(0),F(0)]
def exact_links(x,r):
    y=list(x);y[r]=(y[r]+1)%3
    return [3*(b-a) for a,b in zip(phi(x),phi(tuple(y)))]
_,ep=path_shift(3,exact_links,p,(0,0));_,eq=path_shift(3,exact_links,q,(0,0))
ck('exact-affine-descent',ep==eq and mm(T16(ep),T16([-x for x in eq]))==eye(16))
_,ec=path_shift(3,exact_links,[(0,1)]*3,(0,0))
ck('exact-affine-cycle',ec==zero)

def archive(L):
    sites=list(product(range(L),repeat=2)); ids={x:i for i,x in enumerate(sites)}
    n=len(sites)*16; I=eye(n)
    def ix(x,m):return ids[x]*16+m
    def step(x,r):return tuple((v+(i==r))%L for i,v in enumerate(x))
    U=[{(ix(x,m),ix(step(x,r),m)):F(1) for x in sites for m in range(16)} for r in range(2)]
    D=[sc(F(L,2),add(a,sc(-1,tr(a)))) for a in U]
    Av=[sc(F(1,2),add(I,tr(a))) for a in U]
    E={(s,r):{(ix(x,i),ix(x,j)):v for x in sites for (i,j),v in mm(C4[s],tr(C4[r])).items()}
       for s in range(2) for r in range(2)}
    def M(f):return diag([f[x] for x in sites for _ in range(16)])
    def gauge(phi):return {(s,r):{x:L*(phi[r][step(x,s)]-phi[r][x]) for x in sites}
                               for s in range(2) for r in range(2)}
    def K(e):return add(*(mm(M(e[s,r]),mm(U[s],mm(Av[r],E[s,r])))
                         for s in range(2) for r in range(2)))
    def H(e):
        k=K(e)
        return add(*(sc(F(1,2),add(mm(M(e[r,r]),U[r]),mm(tr(U[r]),M(e[r,r]))))
                     for r in range(2)),sc(-1,k),sc(-1,tr(k)))
    def G(phi):return add(*(mm(M(phi[r]),D[r]) for r in range(2)),K(gauge(phi)))
    def Q(e,t):
        return add(sc(-F(1,L),add(*(mm(M(e[t,r]),mm(D[r],U[t])) for r in range(2)))),comm(K(e),U[t]))
    return sites,n,I,ix,step,U,D,E,M,gauge,K,H,G,Q

for L in (2,3,5):
    sites,n,I,ix,step,U,D,E,M,gauge,K,H,G,Q=archive(L)
    phi0=[{x:F(x==(0,0)) for x in sites},{x:F(2*(x==(1,0))-(x==(0,1))) for x in sites}]
    h=gauge(phi0);g=G(phi0)
    ck(f'L{L}-full-H-Ward',add(H(h),g,tr(g))=={})
    for t in range(2):ck(f'L{L}-full-link-jet-{t}',Q(h,t)==comm(g,U[t]))
    ck(f'L{L}-degree-parity',all((i%16).bit_count()==(j%16).bit_count() for i,j in H(h)))
    if L==3:
        e={(s,r):{x:F(s==0 and r==1 and x==(0,0))*3 for x in sites}
           for s in range(2) for r in range(2)}
        ck('L3-CAR-corner',H(e).get((ix((0,0),1),ix((1,2),2)))==-F(3,2))
        ec={(s,r):{x:F(s==1 and r==0 and x==(0,0)) for x in sites}
            for s in range(2) for r in range(2)}
        B=[mm(Q(ec,t),tr(U[t])) for t in range(2)]
        ad=lambda t,b:mm(U[t],mm(b,tr(U[t])))
        omega=add(B[0],ad(0,B[1]),sc(-1,ad(1,B[0])),sc(-1,B[1]))
        curl={x:ec[0,0][x]+ec[1,0][step(x,0)]-ec[0,0][step(x,1)]-ec[1,0][x] for x in sites}
        expected=sc(-F(1,L),mm(M(curl),D[0]))
        ck('L3-tangent-plaquette-curl',omega==expected and bool(omega))
        ck('L3-tangent-curl-entry',omega.get((ix((0,0),0),ix((1,0),0)))==F(1,2))
    if L==5:
        eh={(s,r):{x:F(s==0 and r==0) for x in sites} for s in range(2) for r in range(2)}
        B=mm(Q(eh,0),tr(U[0]));cy={};u=I
        for j in range(L):cy=add(cy,mm(u,mm(B,tr(u))));u=mm(u,U[0])
        ck('L5-tangent-harmonic-cycle',cy==sc(-1,D[0]) and bool(cy))
        ck('L5-harmonic-H-scalar',all(sum(v for (i,j),v in H(eh).items() if i==ix(x,0) and j%16==0)==1 for x in sites))

# Full finite pure-gauge specialization at L=2 uses the existing benchmark,
# where the scalar D is zero and F_phi=I+K(d_f phi), no new second jet.
U={(0,1):F(1),(1,0):F(1)}; I=eye(2)
K={(0,0):F(-1),(0,1):F(-1),(1,0):F(1),(1,1):F(1)}
t=F(1,4);f=add(I,sc(t,K));fi=add(I,sc(-t,K));h=sc(-1,add(K,tr(K)))
ell=mm(f,mm(U,fi))
ck('L2-pure-gauge-inverse',mm(f,fi)==I)
ck('L2-Nyquist-H',h==diag([2,-2]))
ck('L2-Nyquist-centered-zero',F(-2+2,2)==0)
ck('L2-exact-letter',ell==add(U,sc(2*t,K)))
ck('L2-exact-reverse-cycle',mm(ell,ell)==I)
ck('L2-exact-endpoint-gauge',power(ell,3,2)==ell)
W=add(I,sc(t,h)); defect=add(mm(tr(f),mm(W,f)),sc(-1,I))
ck('L2-flux-finite-congruence-defect',defect==sc(-t*t,mm(tr(K),K)) and bool(defect))
print('L2 W_flux congruence defect:',defect)

# Fixed-site-support obstruction and constant-isotropy movement of projectors.
L=5; U={(i,(i+1)%L):F(1) for i in range(L)};I=eye(L)
D=sc(F(L,2),add(U,sc(-1,tr(U))));p0={(0,0):F(1)};g=mm(p0,D)
c=comm(g,U)
ck('L5-fixed-site-link-obstructed',c.get((0,0))==-F(5,2) and c.get((0,2))==F(5,2))
ck('constant-isotropy-site-projector-moves',bool(comm(D,p0)))

# Noncommuting pull-order append/reverse, including exact first-jet units.
aa=add(eye(2),{(0,1):F(2)}); ai=add(eye(2),{(0,1):F(-2)})
bb=add(eye(2),{(1,0):F(3)}); bi=add(eye(2),{(1,0):F(-3)})
def ev(word,n):
    z=eye(n)
    for a in word:z=mm(z,a)
    return z
ck('noncommuting-append',ev([aa,bb,aa],2)==mm(ev([aa,bb],2),aa))
ck('noncommuting-reverse',mm(ev([aa,bb],2),ev([bi,ai],2))==eye(2))
ck('noncommuting-relative-holonomy',ev([aa,bb,ai,bi],2)!=eye(2))
def dm(a,b):return (mm(a[0],b[0]),add(mm(a[0],b[1]),mm(a[1],b[0])))
jet=(aa,bb);jeti=(ai,sc(-1,mm(ai,mm(bb,ai))))
ck('dual-number-exact-inverse',dm(jet,jeti)==(eye(2),{}))

# Located J at all four coordinates, with full 16-state exterior boost.
from itertools import combinations, permutations
def det(a):
    n=len(a);out=F(0)
    for p in permutations(range(n)):
        v=F((-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n)))
        for i in range(n):v*=a[i][p[i]]
        out+=v
    return out
def exterior(g):
    z={}
    for i,j in product(range(16),repeat=2):
        si=[r for r in range(4) if i&(1<<r)];sj=[r for r in range(4) if j&(1<<r)]
        if len(si)==len(sj):
            v=det([[g[r][s] for s in sj] for r in si])
            if v:z[i,j]=v
    return z
g=[[F(i==j) for j in range(4)] for i in range(4)]
g[0][0]=g[1][1]=F(5,4);g[0][1]=g[1][0]=F(3,4)
gi=[row[:] for row in g];gi[0][1]=gi[1][0]=-F(3,4)
rho=exterior(g);rhoi=exterior(gi)
ck('exterior-boost-inverse',mm(rho,rhoi)==eye(16))
eta=diag([1,-1,-1,-1]);gm={(i,j):g[i][j] for i in range(4) for j in range(4) if g[i][j]}
ck('rational-boost-Lorentz',mm(tr(gm),mm(eta,gm))==eta)
Bn=mm(tr(rhoi),rhoi)
ck('moving-observer-Gram',mm(tr(rho),mm(Bn,rho))==eye(16))
sites=list(product(range(3),repeat=4));ids={x:i for i,x in enumerate(sites)}
ix=lambda x,m:16*ids[x]+m
def anchor(x,m):return tuple((x[r]-(1-((m>>r)&1)))%3 for r in range(4))
J={}
for x in sites:
    for m in range(16):
        sign=(-1)**sum(bool(m&(1<<r)) and not bool(m&(1<<s)) for r in range(4) for s in range(r))
        J[ix(anchor(x,m),15^m),ix(x,m)]=F(sign)
n=len(sites)*16
R={(ix(x,i),ix(x,j)):v for x in sites for (i,j),v in rho.items()}
Ri={(ix(x,i),ix(x,j)):v for x in sites for (i,j),v in rhoi.items()}
Rd=mm(J,mm(tr(Ri),tr(J))) # J^-T = J for this signed permutation
ck('located-J-inverse',mm(tr(J),J)==eye(n))
ck('located-J-pairing',mm(tr(R),mm(tr(J),Rd))==tr(J))
ck('located-J-shifted-anchors',anchor((0,0,0,0),1)!=anchor((0,0,0,0),2))
ck('located-dual-boost-nonlocal',any(i//16!=j//16 for i,j in Rd))

print(f'PASS {len(checks)}/{len(checks)} exact rational controls')
for x in checks:print(x)

```
