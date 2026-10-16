# Exact fixed-source existence audit: null shear and temporal Y

Task: EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE, Draft PR #310.
Input: f4f88161325574e4c5750e0af4a8cc14a2f4b48e.
Status: two exact scoped existence obstructions; parent PARTIAL / OPEN.
The action, metric sampling, source convention and admission domain are
unchanged. No source is assigned from a candidate after construction.

The proposed nilpotent reduction does not give a linear joint system.
Its restricted action is identically telescopic, while variations outside
the subgroup impose nonlinear equations. Full stationarity excludes every
nonconstant sampled null shear in the entire eight-coefficient
one-coordinate subgroup. A separate complete current identity excludes
temporal curved deformations of the displayed Y vacuum.
Neither statement supplies or excludes every possible original joint root.

## 1. Which existence statement is needed

The [all-warp fixed-source theorem](A4D_FIXED_SOURCE_ALGEBRAIC_COMPATIBILITY.md#51-every-nonconstant-positive-warp-forbids-the-positive-conjunction)
already determines the raw gap from the source equation alone. A terminal
counterexample still requires one fixed smooth nondegenerate curved metric,
one fixed smooth source and exact full joint roots on an unbounded
refinement sequence, inside the original small chart.

[H-DOMAIN](A4D_J2_METRIC_RESPONSE_SENSITIVITY.md#1-chart-response-and-norm)
fixes a sufficiently small log radius independently of the mesh.
The log-O(h) hypotheses of later stationary-action and homogenization
lemmas are additional scoped assumptions, rather than the definition of
that original chart. Accordingly the tests below allow arbitrary real
coefficients, including fixed-small UV amplitudes. They do not cut out
the #232 response-null family by requiring smooth unknown links.

Only full Euler equations are used: all six Lorentz generators on all
four independent link directions. Stationarity of an action restricted
to a chosen subgroup does not imply those equations.

## 2. Nondegenerate null shear and the complete subgroup

Let $\eta=\operatorname{diag}(1,-1,-1,-1)$, $k=(1,1,0,0)^T$ and
$k^\flat=k^T\eta=(1,-1,0,0)$. For an arbitrary real periodic sequence
$H_n$, $n=x_2\bmod L$, set
\[
 E_n=I+\tfrac12H_n k k^\flat,\qquad
 Q_n=\eta+H_n(k^\flat)^Tk^\flat,\qquad
 \det E_n=1,\quad\det Q_n=-1.                         \tag{1}
\]
These metrics never become degenerate. A fixed nonconstant smooth
$H(y_2)$ gives a curved example in an arbitrarily small metric chart.

For transverse internal directions $i=2,3$, define
\[
 N_i=k e_i^T\eta-e_i k^\flat .
\]
They are Lorentz generators, commute, and every $V=aN_2+eN_3$
satisfies $V^3=0$. Thus
\[
 \exp V=I+V+\tfrac12V^2,\qquad
 (\exp V)^{-1}=I-V+\tfrac12V^2                        \tag{2}
\]
exactly. Allow every role:
\[
 V_0=aN_2+eN_3,\quad V_1=bN_2+fN_3,\quad
 V_2=cN_2+gN_3,\quad V_3=dN_2+jN_3.                  \tag{3}
\]
All eight coefficients are arbitrary periodic lattice sequences in $n$.
They need no expansion, regular interpolant, or size assumption.
Role 2 shifts $n$; the other three role shifts leave it unchanged.

The [literal checker](certificates/a4d_null_shear_full_euler_check.py)
assembles all 24 shared-link rows and all ten packed Gram slots.
Writing $\Delta u_n=u_n-u_{n+1}$, the metric response is exactly
\[
 \Xi_n=\left(
 -\tfrac12\Delta b,\tfrac12(\Delta a-\Delta b),
 \tfrac12\Delta j,-\tfrac12\Delta d,\tfrac12\Delta a,
 \tfrac12\Delta j,-\tfrac12\Delta d,0,
 -\tfrac12(\Delta e+\Delta f),\tfrac12(\Delta a+\Delta b)
 \right).                                           \tag{4}
\]
Slots are $(00,01,02,03,11,12,13,22,23,33)$, with the existing
off-diagonal dual weights. The cell action is
$-(\Delta a+\Delta b)$, so the restricted periodic action is zero for
every choice of (3). Every restricted null-generator Euler pairing
therefore vanishes identically.

The curvature pairing is also checked on the full Lorentz domain:
$\eta W^T\eta=-W$ for each face and Gram-derivative weight gives
$\langle W,(P-P^{-1})/2\rangle=\langle W,P\rangle$.
This identity preserves every full Lorentz variation. The checker
compares both versions of the action, all ten Gram slots and all
144 local generator incidences producing the 24 shared-link rows.

The full equations do not vanish: for $H=0$, $a=1/10$, $b=-1/10$,
and all other coefficients zero, the full row
$E_{K,\mathrm{Role}\,3,J_{03}}=1/100$.
This exact hostile control exposes the invalid linearization step.

## 3. Full rows force the null shear to be constant

The following identities are extracted from the complete polynomial
rows and checked identically, not by mesh extrapolation.

Four linear rows first give $b_n=-a_n$ and $f_n=-e_n$.
Sums and differences of Role 0 and Role 1 rows then give
\[
 a_{n-1}=a_{n+1},\quad e_{n-1}=e_{n+1},\quad
 c_{n-1}=-j_n,\quad g_{n-1}=d_n.                      \tag{5}
\]
The two Role 2 quadratic rows impose
\[
 j_{n+1}=-a_na_{n+1}+e_ne_{n+1},\qquad
 d_{n+1}=a_ne_{n+1}+a_{n+1}e_n.                       \tag{6}
\]
By (5) their right sides are independent of $n$. Hence $j,d,c,g$
are constant, with $C=c=-j$ and $G=g=d$. Two Role 3 rows now imply
\[
 C=a_n^2-e_n^2,\qquad G=2a_ne_n.
\]
Use $z_n=a_n+i e_n$ only as an algebraic abbreviation for these real
equations. Equations (6) and the last display say
\[
 z_n^2=C+iG=z_nz_{n+1}.
\]
If $z_n\ne0$, the neighboring value equals it. If $z_n=0$, the
common-square identity makes $z_{n+1}=0$ as well. All eight
coefficients are constant, and (4) is identically zero.

Put $a=A$, $e=B$. Another full row is
\[
 E_{K,\mathrm{Role}\,0,J_{02}}
 =\tfrac12\{P(A,B)-2A-H_n+H_{n-1}\},\quad
 P=A^4-4A^3B-6A^2B^2+4AB^3+B^4.                     \tag{7}
\]
Its vanishing forces $\Delta H$ to be constant. Periodic summation
forces that constant to be zero. Thus, for every $L\ge3$,
\[
 \boxed{E_K=0\ \Longrightarrow\ H_n=\mathrm{constant},
                         \quad \Xi_n=0.}             \tag{8}
\]
A fixed nonconstant smooth $H$ cannot be constant on arbitrarily fine
sample sets; their density and continuity exclude a refining sequence
of roots in this subgroup, for any predeclared source.

For constant $H$, the remaining polynomial row has
$Q=A^4+4A^3B-6A^2B^2-4AB^3+B^4$ and imposes $Q=2B$.
Together with (7), it gives $(A+iB)^4=(1-i)(A+iB)$.
Nonzero constant solutions have $|A+iB|=2^{1/6}>1$ and lie outside
a sufficiently small chart. This finite stratum is distinct from
the full-field #232 vacuum.

## 4. The temporal Y deformation: the missing current is a matrix

Consider the separate phase-rotation construction with
$n=x_0\bmod L$ and $p=\sum_r x_r\bmod4$.
The three spatial columns of the solder have zero time components and
form an arbitrary invertible real matrix $M_n$.
The time column may vary with $n$.
Take temporal phase links $(R_n,I,R_n^{-1},I)$ and all spatial links
equal to identity, where $R_n$ is a proper spatial Y rotation.

At each cell the Y curvature can have zero solder current on a large
linear solder kernel. In particular, with axis
$\nu=(1,1,1)/\sqrt3$ and $P_\parallel=\nu\nu^T$,
$M_n=P_\parallel+f_nP_\perp$ lies in that kernel.
This is a local response statement, not shared-link stationarity.

Set $C_n=\operatorname{cof}M_n=\det(M_n)M_n^{-T}$.
The complete spatial-link boost rows compare
\[
 J_\pm(n)=(I+R_n^{\pm1})C_n:
\qquad
 E_{i,\mathrm{boost}}(n,p)
 =\begin{cases}
  \tfrac12[J_-(n-1)-J_-(n)]e_i,&p=0,1,\\
  \tfrac12[J_+(n-1)-J_+(n)]e_i,&p=2,3 .
 \end{cases}                                        \tag{9}
\]
The spatial-link spin rows vanish. The temporal-link rows are
additional constraints and cannot weaken (9).
Spatial faces cancel in these rows because their weights vary only
with time and their shifts are spatial.
The [cofactor-current checker](certificates/a4d_y_temporal_cofactor_current_check.py)
retains every row, checks the cofactor weight identity for nonsymmetric
$M$, and replays both signs of (9).

Full stationarity forces both $J_+$ and $J_-$ to be constant.
In the small chart $I+R_n$ is invertible, and $C_n$ is invertible.
The exact identity
\[
 J_-(n)=R_n^{-1}J_+(n)
\]
gives $R_n=J_+J_-^{-1}$, independent of $n$.
It then fixes $C_n$ and $M_n$ on the chosen orientation component.
For the transverse scale, the axial current is already
$2f_n^2P_\parallel$, independent of rotation angle, and forces $f_n$
constant when $f_n>0$.
Conservation of a selected scalar such as $f\cos\theta$ misses this
axial entry and the independent opposite-phase current.

The hostile replay has $f=(1,2)$ and Cayley amplitude $1/10$:
all $\Xi$ slots vanish while 72 connection entries are nonzero.
One is the rational number $2009/1209$.
Thus response-null local data do not provide a curved vacuum root.

With constant spatial columns and an arbitrary smooth time column,
the coframe is closed and gives a flat coordinate metric.
Identity links are then also exactly stationary. The unique smooth
formal comparator germ has zero response to all orders, so this
nonconstant-coordinate control gives no curved response gap.

## 5. What has been settled and what is still required

Nilpotence truncates the link exponential and makes (4) linear, but
full link variations leave the subgroup and retain nonlinear products.
The promised reduction to a linear fixed-source joint system fails
at that exact step. The temporal Y alternative fails at the complete
matrix current (9).

The [multidimensional extension](A4D_NULL_MULTIDIMENSIONAL_FIXED_SOURCE_OBSTRUCTION.md)
now treats arbitrary four-coordinate null-subgroup fields over a fixed
pp profile $H(y_2,y_3)$ in the explicit coefficient chart $\delta\le1/288$.
Its full finite Laurent inverse derives $O(h)$ and rules out nonconstant
profiles on unbounded refinements. That extension needs no smoothness
of unknown links.

These proofs do not address links in additional Lorentz directions,
a larger unspecified chart in the multidimensional extension, or the full
noncommuting source image. They do not construct the original rooted
counterexample. The remaining terminal obligation is still one
exact curved fixed-source sequence in the original chart, or the
original owner estimate on the full realizable source image.
No task retirement, Ready transition or public/Lean claim follows.

## 6. Replay and validation boundary

Both checkers default to verifying their immutable JSON ledgers.
The null-shear checker requires --write to replace its explicit output;
the Y checker writes only when --output PATH is supplied.
Both support --repo for replay outside the repository.
The checks certify the literal polynomial identities and hostile
controls above. The all-period consequences (5)--(9) are the analytic
proofs, rather than conclusions inferred from a few periods.

The imported finite face owners are pinned by SHA256 in each ledger.
The mandatory #232 null and #227 visible controls retain their existing
source and curvature interpretations. The general parent status
remains PARTIAL / OPEN.
