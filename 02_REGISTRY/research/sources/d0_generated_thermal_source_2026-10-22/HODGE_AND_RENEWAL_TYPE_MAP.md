# Same-carrier logarithmic Hodge map and the actual sequential renewal source

22 October 2026. Bounded composition inside existing PR #334. The constructive
result is an explicit **same-cochain-space** map from a genuine Hodge heat to
its logarithmic survival heat, with its whole variation and paired trace.
Two exact controls on the original CAR16 constructor specify why its blank
Dirac and its CP nonmatch transfer cannot silently supply that map's inputs.
No new physical price, incidence, cut, clock, field equation or admission is
postulated. `GR_closed=false`.

Section 6 strengthens the application: the **literal** cut amplitude `C=QUP`
itself is a differential on the already existing active/archive carrier. Its
paired Hodge candidate and the original feedback have one explicit common
source, without choosing a new square root or an independent heat spectrum.

## 0. Literal inputs and their types

The attached `project_sources/01-d0_tome_3_geometry_phi_graph_qft_qg.md` is a
different Tome III: its 861 lines contain sections 1–10, including the sketch
of a graph wave equation at lines 686–694. It has no §§03.25–03.26. The literal
bootstrap input used here is the repository Book03 below.

| Input | Exact location consumed |
|---|---|
| Book03 master `B=beta^-1 log Tr exp(-beta Delta)-log det(I-zeta F)` | `01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md`, lines 1127–1137 |
| Actual equal-rank Golden active/archive block | Same Book03, lines 1139–1159 |
| `P,Q=I-P`, `F=(QUP)^*(QUP)`; separate Hodge spectrum | `01_BOOKS/BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md`, lines 142–158 and 175–190 |
| Fixed incidence nilpotency | `03_FORMALIZATION/D0/Topology/GradedIncidenceComplex.lean`, lines 10–21, 27–41 |
| A literal fixed-degree Hodge matrix | `03_FORMALIZATION/D0/Topology/GenericTripartiteTopHodgeSpectrum.lean`, lines 259–261 |
| Iid pointer survival logarithm | `A4D_RENEWAL_GIBBS_HEAT_AND_NATIVE_NONLINEAR_ENTROPY_BRIDGE_2026_10_22.md`, lines 367–397 |
| Already-owned inverse-square/modular heat and correlated predictive source | `A4D_NATIVE_CORRELATED_RETURN_MODULAR_HEAT_COMPATIBILITY_2026_10_22.md`, lines 70–132 and 230–285 |
| Actual no-reset nonmatch CP maps and their first jets | `sources/d0_first_match_wald_2026-10-22/SEQUENTIAL_FULL128_BOOK_RETURN.md`, lines 70–122 |
| Actual clean return, full clock and marked-source formula | Same sequential note, lines 214–322 |
| Original CAR, boost, Walsh and Golden constructor | `sources/d0_book_uniform_source_2026-10-21/check_uniform_book_source.py`, lines 51–100; unchanged blob `ee8de4635d24c668949ac9a0186616ab7d59f2ed` |

Paths in this table are relative to `02_REGISTRY/research/`, except those
beginning `01_BOOKS/` or `03_FORMALIZATION/`, which are repository-relative.
The previous algebraic Gibbs obstruction and modular logarithm are consumed;
neither is reproved here.

## 1. A positive exact construction on the SAME graded Hilbert space

Let the **actual admitted** finite Hilbert cochain complex be
`C=direct_sum C^q`, with degree-one differential `d`, `d^2=0`, fixed
inner products, and

\[
 L=dd^*+d^*d\ge0.
\]

Suppose a real spectral function satisfies `f(0)=0`, `f(lambda)>0` on the
positive spectrum, with a positive continuous choice of `f(lambda)/lambda`
at zero. Define on this very space

\[
 k(L)=\frac{f(L)}L,\qquad
 d_f=d\sqrt{k(L)}=\sqrt{k(L)}d.                         \tag{1}
\]

The quotient means spectral functional calculus, not inversion on harmonic
modes. Since `dL=Ld` and `d^*L=Ld^*`,

\[
 \boxed{d_f^2=0,\qquad
 d_fd_f^*+d_f^*d_f=k(L)L=f(L).}                          \tag{2}
\]

All cochain spaces and their dimensions stay fixed. Invertibility of `k(L)`
also preserves every cohomology dimension. This is a genuine finite Hodge
realization, rather than only the factorization of a positive matrix.

### The same incidence differential with a changed Hodge metric

There is an equivalent coordinate description which keeps the **matrix d**:
on degree `q`, use the positive Gram matrix

\[
 G_q=k(L|_{C^q})^q.                                     \tag{3}
\]

Then `d^{*G}=k(L)d^*`, so its Hodge operator is again `f(L)`.
The isometry `G_q^(1/2)` to the original orthonormal coordinates transforms
`d` into (1). Thus the precise new physical input would be the metric (3),
not an added Hilbert sector. In general `G_q` is dense: permission to vary
local scalar edge weights or local coframes does not automatically permit
these nonlocal Gram matrices.

This metric description is not automatically an unchanged physical cut and
tick. If the **literal old matrices** `P,U` are kept while their Hilbert metric
is changed to `G=direct_sum G_q`, one needs `[P,G]=0` and `U^*GU=G` for the
same orthogonal projector and unitary tick. Otherwise they must be transported
with the actual metric/cut implementation. A moving Riesz map `R=G^(1/2)`
has the exact coordinate-source rule
`D(RXR^(-1))=R(DX)R^(-1)+[Omega,RXR^(-1)]`,
`Omega=(DR)R^(-1)`. It applies to both cut and tick, including their own
input variations. The fixed-inner-product construction (1) avoids this
coordinate change, but then the changed differential `d_f` itself requires
native admission.

### Actual log-of-positive-survival specialization

For an admitted positive contraction `B_L=I-alpha L>0` and an actual fixed
tick unit `tau>0`, put

\[
 f(L)=-\tau^{-1}\log(I-\alpha L),\qquad
 k(0)=\alpha/\tau.                                     \tag{4}
\]

Equations (1)–(3) realize this logarithm exactly as a Hodge operator on the
same complex. The parameters `alpha,tau` must be the source programme's
existing parameters; this theorem does not calibrate them. The more general
modular `log L` from the owned preparation theorem has a different spectral
function. In particular subtracting its smallest positive eigenvalue to
create a new zero mode cannot be implemented by a strictly positive metric
(3) on a complex with fixed cohomology. Harmonic multiplicity is part of the
Hodge contract.

### Full noncommuting source

Let `X=DL` include every admitted incidence and metric input derivative.
For fixed orthonormal coordinates,

\[
 X=(Dd)d^*+d(Dd)^*+(Dd)^*d+d^*(Dd).
\]

With `R_u=(I-u alpha L)^(-1)`, the full derivative of (4) is

\[
 \boxed{
 Df(L)=\frac1\tau\int_0^1
 R_u[\alpha X+(D\alpha)L]R_u\,du
 -\frac{D\tau}{\tau}f(L).}                              \tag{5}
\]

No commutation of `X` with `L` is assumed. The differential itself obeys
`Dd_f=(Dd)sqrt(k(L))+d D(sqrt(k(L)))`, using the actual Fréchet derivative.
Consequently (5) is also the full derivative of the two sides of (2), not a
scalar-eigenvalue approximation. Moving original inner products must first
be included in their actual adjoint/Riesz-coordinate derivative.

## 2. Paired heat modes and the original active/archive carrier

Every positive singular value squared `lambda_(q,j)` of `d:C^q->C^(q+1)`
appears in both adjacent Hodge degrees. Therefore the full trace is

\[
 \boxed{Z_f(\beta)=b_{\rm tot}
       +2\sum_{q,j}\exp[-\beta f(\lambda_{q,j})],\qquad
 b_{\rm tot}=\sum_q\dim H^q.}                           \tag{6}
\]

Dropping one partner changes Book03's thermal trace. The construction does
not authorize such a compression or a change of `P`.

The equal-rank active/archive block of Book03 §03.26 provides a useful
**explicit algebraic embedding on an already doubled carrier**. If its
actual copy identification is `J:P H -> Q H` and `M>=0` is an operator on
`P H`, define

\[
 d_M=J\sqrt M\,P,\qquad
 \widehat L_M=d_M^*d_M+d_Md_M^*=M\oplus JMJ^*.            \tag{7}
\]

Here `d_M^2=0`. This uses the same two Hilbert blocks and the same `P`, not
new states. It is a two-term Hilbert complex. To use it as the original
**incidence** complex requires a physical identification of its degrees,
boundary map and metric; relabeling an archive as an edge space is not that
identification. For `M=-log B/tau`, (7) gives an exact positive paired Hodge
representative of the original positive blank logarithm.

With the original oldRIGHT dimension `d_R` retained and no additional
moving factors, the trace is exactly

\[
 \operatorname{Tr}_{P\oplus Q,\mathrm{oldRIGHT}}
 e^{-\beta\widehat L_M}=2d_R\operatorname{Tr}_{P H}e^{-\beta M}.
 \tag{8}
\]

Thus at fixed beta the induced heat source along the coupled two-block
variation is `-Tr(sigma_M DM)`, where
`sigma_M=exp(-beta M)/Tr exp(-beta M)`. The factor in (8) remains in the
absolute action. For the general full heat `Lhat`, including moving beta,

\[
 D\left[\beta^{-1}\log Z\right]
 =-\operatorname{Tr}(\sigma D\widehat L)
 -(D\beta)\left[\frac{\log Z}{\beta^2}
       +\frac{\operatorname{Tr}(\sigma\widehat L)}\beta\right].
 \tag{9}
\]

If an **already paid** energy expectation is present, its coupled
energy-plus-heat source is

\[
 D(R+H)=\operatorname{Tr}[(D\widehat\rho)\widehat L]
       +\operatorname{Tr}[(\widehat\rho-\sigma)D\widehat L]
 \quad\text{at fixed beta}.                            \tag{10}
\]

This does not insert `R` into the bare Book03 master. For a density supported
on the active copy, cancellation on variations `DM direct_sum J DM J^*`
does not imply cancellation under independently allowed variations of the
two copies. Which of these are admissible is fixed by the actual incidence
and controller constraints. Equation (7) couples the paired spectra; a
larger independently varied physical carrier must retain its extra rows.

## 3. Concrete original-CAR obstruction to the direct untwisted input

The original constructor itself allows a short exact test of the proposed
input `d=A_+`, the number-raising part of the blank Walsh row. It is not a
replay of the owned inverse-square or Gibbs calculation.

Write `c_r` for its creators, `n_r=c_r c_r^*`, `h=cosh(theta)-1`,
`s=sinh(theta)`. The word average at the pinned phases is exactly

\[
 A=d_++d_+^*,\qquad
 d_+=\frac\nu{16}\left[
 (i-1)(c_0+c_1)-2c_2+(-i-1)c_3
       +ih\,n_0c_1-is\,n_1c_0\right].                 \tag{11}
\]

The CAR relations give the precise defect

\[
 \boxed{d_+^2=\frac{\nu^2}{256}(1+i)(e^\theta-1)c_0c_1.} \tag{12}
\]

Consequently `A^2` has a degree-zero to degree-two entry

\[
 \langle 11|A^2|00\rangle
 =\frac{\nu^2}{256}(1+i)(e^\theta-1),\qquad
 \left.\partial_\theta\langle11|A^2|00\rangle\right|_0
 =\frac{\nu^2}{256}(1+i).                               \tag{13}
\]

The other two CAR modes are empty in this displayed matrix entry. A literal
untwisted Hodge operator `dd^*+d^*d` preserves the original degrees. Thus
(12) prevents using this `d_+` in (1), and (13) already prevents equality of
the first sources on the unchanged degree decomposition. At the flat point
`A^2=(9/640)I`, the derivative of any smooth spectral function is
`Df(A^2)[X]=f'(9/640)X`; the nonzero off-degree source survives the positive
blank logarithm.

This excludes the **literal untwisted, fixed-degree Hodge identification**.
It does not exclude a covariant differential: `d_A^2=curvature` is allowed
for a connection, and its twisted Dirac square can contain these degree-two
terms. A physical twisted-Dirac heat must keep that curvature and its source.
Replacing `A^2` by `d_+d_+^*+d_+^*d_+` would delete precisely
`d_+^2+(d_+^*)^2`, including the nonzero source (13).

## 4. The actual sequential renewal/Schur source without an iid replacement

For an original anchor label `a`, let

\[
 \mathcal Q_a^*(X)=\sum_{b\ne a}K_b^*XK_b,
 \qquad R_a(u)=(I-u\mathcal Q_a^*)^{-1}.
\]

On an actual uniformly transient chart, the complete harmonic mismatch
effect on DATA is

\[
 \boxed{E_a^{\rm harm}=
 \sum_{n\ge1}\frac{(\mathcal Q_a^*)^n(I)}n
 =\int_0^1\mathcal Q_a^*R_a(u)(I)\,du,\qquad
 DE_a^{\rm harm}=\int_0^1
 R_a(u)(D\mathcal Q_a^*)R_a(u)(I)\,du.}                  \tag{14}
\]

At finite cap use the polynomial sum through `n=K`; its exact derivative
is `sum_(n=1)^K (1/n) sum_(j=0)^(n-1) Q^j (DQ) Q^(n-1-j)(I)`.
Each term in the effect is positive because `Q_a^*` is CP. Its Fréchet
derivative includes every `DK_b`, and the original scalar charge derivatives
if the marked maps of the sequential owner are used.

For the actual first outcome, the unconditioned effect and scalar source are

\[
 E^{\rm harm}=\sum_a K_a^*E_a^{\rm harm}K_a,\qquad
 D\langle H_N\rangle
 =\operatorname{Tr}[(D\rho)E^{\rm harm}]
  +\operatorname{Tr}[\rho\,DE^{\rm harm}].               \tag{15}
\]

This has no iid or order-one classical Markov hypothesis. Equivalently use
the actual conditional `rho_a=K_a rho K_a^*/Pr(a)` and retain its quotient
derivative. OldRIGHT is kept by tensoring the maps with its identity; taking
the DATA marginal here computes this stated additive observable only.

The resolvent is a literal algebraic Schur elimination: on the doubled
**operator space**, the lower-right Schur complement of

\[
 \begin{pmatrix}I&-u\mathcal Q_a^*\\-I&I\end{pmatrix}
\]

is `I-u Q_a^*`. This block is not asserted Hermitian or an incidence
Laplacian. The effect in (14) is the superoperator logarithm **applied to I**;
it is not a logarithm of `I-Q_a^*(I)`, nor a positive heat matrix on DATA.

### Exact native negative level of the superoperator logarithm

This type distinction is already visible in the original flat CAR16 input.
Use the owned `A^2=h_0I`, `h_0=9/640`, and put `e=4p^2h_0=9p^2/160`.
The original recycling map is the paired-Julia map of
`A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md` §1, equation (3).
For `X=eta_2=i(c_2-c_2^*)`, the literal flat roots `sqrt(1-nu^2)=4/5`
give

\[
 \mathcal T(X)=\frac{(4/5)+3(4/5)^2}{4}X
 =\frac{17}{25}X,\qquad AX=-XA.
\]

The actual blank-removed channel therefore satisfies

\[
 \boxed{\mathcal Q_0^*(X)
 =\bigl(\Phi^*-B(\,\cdot\,)B\bigr)(X)
 =-\left(\frac{17e}{25}+\frac{e^2}{4}\right)X.}         \tag{16}
\]

Hence `-log(I-Q_0^*)` has the strictly negative eigenvalue
`-log(1+17e/25+e^2/4)`. Complete positivity of a survival **map** does not
make it a positive heat **matrix** on the 256-dimensional Liouville space.
This logarithm is well defined: `Q_0^*(I)=(e-e^2/4)I` with `0<e-e^2/4<1`,
so CP positivity bounds its operator norm by that strict contraction factor.
The effect (14) remains positive on the original 16-dimensional DATA space.
An identification of these two objects would change both type and trace.

## 5. Exact criterion for using the construction in the original master

Equations (1)–(10) give a concrete source map to test against the **actual**
programme, instead of assigning its thermal spectrum after the fact. For a
fixed original incidence family the proposed map is legal precisely when
its admitted Hodge metric is the derived family (3), or a proved equivalent
metric with the same full operator and tangent map. This requires the
actual metric constraints, locality, grading, boundary domain and positive
rank to admit that family. Equality of a heat trace at one field is weaker
than this operator/source identity. A two-term use of (7) additionally needs
the existing archive/degree identification and retains both heat partners.
The cut/tick compatibility or common transport stated after (3) is part of
this criterion, rather than a change in arbitrary trace dimension.

For that identified family, the literal full Book03 first source at fixed
beta and zeta is then

\[
 \boxed{D\mathcal B_N
 =-\operatorname{Tr}(\sigma_{\widehat L}D\widehat L)
 +\zeta\operatorname{Tr}[(I-\zeta F_N)^{-1}DF_N].}       \tag{17}
\]

Use (5) for the first term and the unchanged sequential-return equations
(11)–(14) for the second, with the actual common `P`, retained preparation
prefix and open clock. Moving beta, zeta and actual clock/cut sources are
added by their product rules; a change of rank uses Book03's discrete rank
comparison. If an additional genuine paid `R` is present, add its whole
source, with (10) applicable only to an actually supplied energy expectation.

There are now two precise constructive continuations. An untwisted
incidence route must supply the admitted metric (3) for its existing
nilpotent `d`, without replacing it by the curved `d_+` of (11). A
twisted-Dirac route can retain the original `A` and the explicit positive
blank logarithm, but must identify that twisted heat in the master while
keeping the curvature terms (12)–(13). The no-reset waiting observable is
already computed by (14)–(15); it supplies neither identification by itself.
This removes an unspecified functional-calculus step and leaves a concrete
incidence/metric or twisted-heat source equality to establish on the same
execution. No old suite or new numerical test was run for this note.

## 6. Literal cut differential: ONE explicit coupled heat/feedback candidate

This application uses the already owned Gram identity and full moving-cut
variation, rather than re-certifying them:
`03_FORMALIZATION/D0/CVFT/BoundaryRankLocalization.lean`, lines 44–65 and
79–85, owns `rank(C^*C)=rank C` and Gram positivity; and
`A4D_NATIVE_BOOK03_OPERATOR_VARIATION_BOUNDARY.md` §§1–2 owns the admissible
fixed-rank projector/unitary tangents and all outer/inner cut legs of `DF`.
The new composition below uses those inputs to compute the paired heat and
its source from the same **actual** `P,U`.

### 6.1 The actual cut amplitude is already nilpotent

On the full original finite execution space, write
`M=dim H`, `r=rank P`, `Q=I-P`, and use its literal unitary `U`. Define

\[
 \boxed{C=QUP,\qquad C^2=QU(PQ)UP=0,\qquad
 L_C=C^*C+CC^*.}                                        \tag{18}
\]

Thus the same active/archive decomposition is a two-term Hilbert complex,
with `C:P H -> Q H`. Its active Hodge block is **exactly** the owned feedback
operator, not a fitted spectrum:

\[
 \boxed{L_C|_{P H}=F=C^*C|_{P H},\qquad
 L_C|_{Q H}=CC^*|_{Q H},\qquad 0\le L_C\le I.}          \tag{19}
\]

There is no new state space, chosen `J`, matrix square root, gate angle or
choice of unitary completion in (18): `C` is determined by the existing
output column `UP` and its existing output cut. In particular `CC^*` here
uses `QUPU^*Q`; it is not silently identified with the distinct reverse-tick
emission operator `QU^*PUQ`.

### 6.2 All harmonic modes remain in the trace

Let `k=rank C`, only for this proof. The `k` positive eigenvalues of `F`
also occur in `CC^*`. Therefore

\[
 \begin{aligned}
 \dim\ker L_C&=M-2k\ge |M-2r|,\\
 Z_C(\beta)&=\operatorname{Tr}_{\mathcal H}e^{-\beta L_C}
       =M-2k+2\sum_{j=1}^k e^{-\beta\lambda_j}\\
       &=\boxed{M-2r+2\operatorname{Tr}_{P\mathcal H}e^{-\beta F}}.
 \end{aligned}                                          \tag{20}
\]

No full-rank assumption on `C` is required. Even if `M-2r` is negative,
the last expression equals the positive full heat trace in the preceding
line. Its form in terms of fixed `M,r` is smooth through a rank change of
`C`; no derivative of `k` or deletion of a newly dark mode is taken.
The many unused archive/work directions contribute genuine zero modes.
They remain in `Z_C`, including its thermal source denominator. Padding
the carrier with extra dormant states would change that denominator and is
not part of this construction.

### 6.3 Exact common source, including a moving original cut

The concrete coupled candidate is the literal Book03 scalar evaluated on
this candidate heat and the same feedback:

\[
 \mathcal B_C=\beta^{-1}\log Z_C
       -\log\det_{P\mathcal H}(I-\zeta F).
\]

On the original admissible determinant chart `I-zeta F>0`, for fixed finite
`M,r,beta,zeta`, equations (19)–(20) give

\[
 \boxed{D\mathcal B_C
  =\operatorname{Tr}_{P\mathcal H}\left[
   \left\{\zeta(I-\zeta F)^{-1}
           -\frac{2e^{-\beta F}}{Z_C}\right\}D_cF\right].}
                                                               \tag{21}
\]

`D_cF` is the full derivative in a co-moving orthonormal frame for the
original retained space. There is no commuting-tangent assumption: inside
the trace the Fréchet derivative of the exponential is exactly
`-beta Tr(exp(-beta F) D_cF)`.

For completeness, choose a local unitary `V(y)` with
`P(y)=V(y)P_0V(y)^*`, put `Omega=V^*DV`, and write tildes for the co-moving
coordinates. Then

\[
 \begin{aligned}
 DP&=V[\Omega,P_0]V^*,\qquad
 \widetilde U=V^*UV,\\
 D\widetilde U&=V^*(DU)V+[\widetilde U,\Omega],\\
 \widetilde C&=Q_0\widetilde U P_0,\qquad
 D\widetilde C=Q_0(D\widetilde U)P_0,\\
 D_cF=D\widetilde F&=(D\widetilde C)^*\widetilde C
                         +\widetilde C^*D\widetilde C.
 \end{aligned}                                          \tag{22}
\]

Thus the co-moving formula includes the induced `DQ=-DP`, both outside
`P` legs, and the actual unitary/clock/preparation source. Equivalently
differentiate the ambient expression
`DC=-(DP)UP+Q(DU)P+QU(DP)` and use
`D tilde(C)=V^*(DC)V+[tilde(C),Omega]`; transporting `DC` alone would omit
the frame connection.
Changing the frame inside `P_0` and `Q_0` adds only a commutator to `D_cF`;
its contraction with the spectral function in (21) is zero. The moving-cut
source is therefore retained without a gauge-coordinate ambiguity.

If beta or zeta is an independently moving input, add

\[
 (D\zeta)\operatorname{Tr}_{P\mathcal H}[(I-\zeta F)^{-1}F]
 -(D\beta)\left[\frac{\log Z_C}{\beta^2}
    +\frac{2\operatorname{Tr}_{P\mathcal H}(F e^{-\beta F})}
                 {\beta Z_C}\right].                   \tag{23}
\]

Physical changes of window/rank use the original discrete carrier
comparison. Formula (21) holds on each fixed-rank chart, with the actual
finite window and every retained record included from the outset.

### 6.4 Original oldRIGHT multiplicity

If the original apparatus factors as `H=H_0 tensor oldRIGHT` and its actual
operators are `P=P_0 tensor I_(d_R)`, `U=U_0 tensor I_(d_R)`, then

\[
 F=F_0\otimes I_{d_R},\qquad L_C=L_{C_0}\otimes I_{d_R},
 \qquad Z_C=d_R Z_0,
 \quad Z_0=M_0-2r_0+2\operatorname{Tr}_{P_0}e^{-\beta F_0}.
\]

The complete scalar and its fixed-parameter base-space source are

\[
 \boxed{\begin{aligned}
 \mathcal B_C
 &=\beta^{-1}\log(d_R Z_0)
       -d_R\log\det_{P_0}(I-\zeta F_0),\\
 D\mathcal B_C
 &=\operatorname{Tr}_{P_0}\left[
   \left\{d_R\zeta(I-\zeta F_0)^{-1}
              -\frac{2e^{-\beta F_0}}{Z_0}\right\}D_cF_0\right].
 \end{aligned}}                                         \tag{24}
\]

In particular `d_R=128` multiplies the feedback source, while the spectator
multiplicity cancels from the normalized thermal source. It remains as
`beta^-1 log d_R` in the absolute heat value. No arbitrary trace dimension
is introduced or removed.

### 6.5 The precise remaining native incidence identification

The new result is a complete mathematical candidate
`(actual P,U) -> (C=QUP,L_C,F)` with the common source (21), rather than an
independently specified thermal spectrum. The missing application is now
the concrete equality

\[
 \Delta_N^{\rm actual}(V)
 \stackrel{?}{=}C^*C+CC^*
\]

on the original full heat carrier, or an actual admissible unitary chain
identification carrying both operators and their tangent maps to that
identity. This must identify the existing active/archive spaces with the
actual incidence degrees and their boundary operator. The exact harmonic
space in (20), complex cut coefficients, locality/metric restrictions and
all original source directions are part of this comparison. It cannot be
inferred solely from nilpotency or positivity, since Book02 treats the
Hodge geometry and feedback return as a paired input, not as this equality.

Thus `L_C` is not declared the selected physical heat. It is a stronger
same-carrier constructive candidate than an arbitrary `J sqrt(M)`: every
entry and every source in it comes from the already specified execution,
and its entire bare-master price is now calculable without a separate heat
oracle. The remaining question is that specific native incidence/source
identification, with the physical original Info/work terms still retained.
