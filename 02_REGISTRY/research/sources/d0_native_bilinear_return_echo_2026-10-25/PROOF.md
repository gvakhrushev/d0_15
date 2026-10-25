# Exact native bilinear return echo

25 October 2026. Same PR #334, constitutive/native-programme-v1.
One fixed processor and two native product-programme bits implement
the ORIGINAL rank2 RETURN, not its full8D channel or a continuous
physical field-to-programme map. Free programme controls retain their
equations. No Cost/Info tariff, action or GR closure is introduced.

## 1. Original return and the exact fixed processor

The original [two-native-8D determinant owner §1](../d0_native_gr_completion_synthesis_2026-10-20/book_source/TWO_NATIVE_8D_DETERMINANT_SOURCE.md)
and [local LEFT-controlled source (5)–(11)](../../A4D_LOCAL_LEFT_CODED_CAR_NULL_MATTER_EINSTEIN_2026_10_18.md)
give, on the retained basis indexed by `(0,2)`,

\[
 C_2(E,b)=(1-2b)[(1-E)I_2-EX],\quad
 F_2=I_2-C_2^\dagger C_2,\quad
 j=-\log\det[(1-\zeta)I_2+\zeta C_2^\dagger C_2],
 \qquad\zeta=2^{-20}.                                (1)
\]

Here X is the data-bit swap. The original effect eigenvalues are
`B=4b(1-b)` and `A=B+(1-B)4E(1-E)`, so
`j=-log(1-zeta A)-log(1-zeta B)`: the genuine complementary determinant.

Use programme bits `e=0,B=1`, unknown DATA `d=2`, source-spin
`s=(3,4)`, and source port0. Let

\[
 V=Z_e Z_B CX(e,d)\otimes I_{\rm spin}.                (2)
\]

These three logical operations commute. Their four programme blocks
on DATA are

\[
 D_{00}=I,\quad D_{01}=-I,\quad
 D_{10}=-X,\quad D_{11}=X.                            (3)
\]

For normalized pure programme bits
`chi_E=sqrt(1-E)|0>+sqrt(E)|1>` and similarly `chi_b`, let
`A=A_programme tensor I_DATA,spin` prepare their PRODUCT from00. Then

\[
 \langle00|A^\dagger VA|00\rangle
  =\sum_{r,t}\Pr(r,t)D_{rt}
  =(1-2b)[(1-E)I-EX]\otimes I_{\rm spin}.              (4)
\]

This holds on EVERY DATA/spin input, with entanglement and untouched
oldRIGHT. Phases cancel since V is programme-diagonal; PRODUCT
probabilities are essential (§6). No measurement, fair factory,
Bernstein table or moving target is used.

The true input isometry inserts only the two programme blanks,

\[
 i:\mathcal H_{d,\rm spin}\longrightarrow
          |00\rangle_{e,B}\otimes\mathcal H_{d,\rm spin},\quad
 \dim\mathcal H=32,\quad\operatorname{rank}i=8.
\]

Writing `Y=A†VA`, its actual input return and feedback are

\[
 i^\dagger Yi=C_2\otimes I_4,\qquad
 F_Y=I_8-(i^\dagger Yi)^\dagger(i^\dagger Yi)=F_2\otimes I_4,
 \qquad J_Y=4j.                                      (5)
\]

The complement retains ALL programme/DATA leakage. The factor4 is
the actual protected-spin input rank; failed returns are not discarded.

## 2. Literal native implementation on all32 columns

Consume [Book03 §03.26.1–2](../../../../01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md)
and [the all-column inverse/routing of §7j](../../A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md).
In the declared source-I profile, `S=diag(I4,L_i)` satisfies

\[
 S^2=Z_e\otimes I_4,\qquad
 G_e^\dagger=S S G_e S S.                             (6)
\]

Thus `Z_e` is TWO actual SourceI stages. To implement `Z_B`, execute
`SWAP(e,B); S; S; SWAP(e,B)`, each SWAP being three native CX.
Append the actual `CX(e,d)`. The complete fixed V word has

\[
 N_V=11,\qquad (n_G,n_{CX},n_S)=(0,7,4).              (7)
\]

Both phase blocks return arbitrary spin on ALL columns. Intermediate
S interactions remain in the clock; no individual spin G/CX or
eigenstate is assumed. Selective source-I availability remains the
existing apparatus-profile premise.

Let `p=(sqrt(5)-1)/2`, `G=[[sqrt(p),-p],[p,sqrt(p)]]=R(theta)`.
For positive integer native codes `(k_E,k_B)`, prepare

\[
 A=G_e^{k_E}G_B^{k_B},\quad
 E=\sin^2(k_E\theta),\quad b=\sin^2(k_B\theta).        (8)
\]

Execute A, the literal V, and the actual raw inverse of A. An inverse
G on port e uses five stages (6). An inverse G on B uses the owned
SWAP route around that five-stage word, hence eleven stages. The
complete echo body therefore has

\[
 n_G=2(k_E+k_B),\quad n_S=4(k_E+k_B+1),\quad
 n_{CX}=7+6k_B,\quad N_{\rm body}=6k_E+12k_B+11.       (9)
\]

For `(1,1),(2,1),(1,2),(2,2)` these lengths are29,35,41,47.
Append respectively22,16,10,4 actual CX stages as cancelling pairs
on ordinary active wires. All four complete words then have the
SAME actual clock `N=51`, with no unpaid idle or inverse shorthand.
Every matrix remains unitary on32 columns. Source-spin is restored
by each completed inverse block.

Programmes stay coherent until the echo ends. OldRIGHT is never
target, control or scratch. Seal outputs only AFTER completion;
no later inverse may touch them. No measured history is reversed.

## 3. The entire native heat is exactly constant

On32 columns V is a real symmetric involution. The B-programme sign
pairs every positive eigenvector with a negative one, so its exact
spectrum is `+1` multiplicity16 and `-1` multiplicity16. Every echo
Y is conjugate to V on ALL unprepared programme/dirty-spin columns.

Use the owned full cyclic primitive clock and transported prefix
cuts, with actual N, fixed beta>0 and the original zeta. For

\[
 K_N(t)=\sum_{k\bmod N}
       e^{-\beta[1-\cos((2\pi k+t)/N)]},
\]

the COMPLETE paired Hodge partition and Book scalar are

\[
 Z_N=32[K_N(0)+K_N(\pi)],\qquad
 \mathcal B_Y=\beta^{-1}\log Z_N+4j(E,b).              (10)
\]

At beta0 this counts `64N` modes, or3264 at N51. All actual stages
enter N; no extra N/Hodge factor multiplies J. Prefix-gauge
commutators cancel in the full heat trace.

The fixed-N heat source is EXACTLY zero. The prefix adjoint of
[paid writer §10.5](../../A4D_PAID_MOMENT_FIELD_WRITER_2026_10_21.md)
eliminates generated rows of this expanded word, not independent
programme or moving-cut sources.

## 4. Original source reproduced, with its exact scope

At `k_E=k_B=1`, ordinary G from blanks gives `E=b=p²`: BOTH original
bands and the whole returned matrix are exact native values, with
no READY condition or approximate forward gate.

For the OPERATOR comparison use `R(arcsin sqrt(E))` and
`R(arcsin sqrt(b))`, without claiming a continuous native primitive.
On original operands `E=p²(1+x)`, `b=(p+sigma p²y)²`, (5) gives

\[
 D\mathcal B_Y|_\Sigma=4Dj
       =4(a_0Dx+b_0Dy),\qquad
 {b_0\over a_0}={2\sigma\over p^5}(R_0/Q_0+p^6),       (11)
\]

Here `R0=1-zeta+zeta p12`, `Q0=1-zeta+zeta p6`,
`a0=4zeta p11/R0`. Sigma− gives the original finite-zeta
`lambda_minus`. Physical use of the inverse-PF source still needs
the SAME coframe/link/CAR code to generate the product biases and
satisfy independent equations; finite endpoints are not that map.

The completion differs from the original FULL8D logical channel;
other future tests do not transfer from return equality. Global
scene/AF extensions need their actual modes, predicates and ranks:
rank528 selection is not a free blank mask. A protected identity
oldRIGHT of dimension r multiplies Z and J by r; blank identity work
has a different cut rank. Neither original reference nor AF modes
are omitted or counted twice.

## 5. Independent programme equations do not vanish

For a general normalized pure programme `chi` on the four basis
labels w, let `p_w=|chi_w|²`, `C=sum_w p_w D_w` and
`Q=(1-zeta)I+zeta C†C`. The exact feedback remains
`J=-4 log det Q`. Its real probability adjoints are

\[
 o_w=-8\zeta\operatorname{ReTr}(Q^{-1}C^\dagger D_w),\quad
 DJ=\sum_w o_wDp_w.
\]

For the Euclidean unit-state tangent metric modulo global phase,
the full CP3 preparation-covector norm is

\[
 \|DJ\|=2\sqrt{\sum_wp_wo_w^2-(\sum_wp_wo_w)^2}.       (12)
\]

At the native primary programme `G|0> tensor G|0>`, all four
probabilities are positive and C has eigenvalues `p³,p6`, both
strictly positive. Hence
`o00=-8zeta Tr(Q^-1 C)<0` and `o01=-o00>0`; (12) is nonzero.
Heat cannot cancel this independent normal reaction; generated
programmes instead require their actual causal control pullback.

There is even a finite native lower-price edit at common N51.
Put `L=4p³=1-p6`. Changing `(1,1)` to `(2,1)` changes E from p²
to L while leaving b=p². The second feedback band B stays L, but

\[
 A_{11}-A_{21}=Lp^6(1-4p^6)>0.                        (13)
\]

Hence `B_echo(2,1)<B_echo(1,1)` at common N, without a gate-cost
equality or smooth native pulse. Nearer native values `k_E=67,1,1161`,
`k_B=1` have exact `E67<E1<E1161` in(.37,.4). Body lengths425,29,6989
plus6568,6964,4 real CX stages give common N6993. Exact band ordering
gives `B67<B1<B1161`, since J_E>0 here. These edits need not solve a
fixed field/query task; exclusion requires its genuine correctness
constraint, not a claim that every native word is a field variation.

## 6. Two means are not the complete programme law

Z-readability does not imply dependence only on E,b. For a general
joint programme law put `t=Pr(11)-Eb`. The true corner is

\[
 C(E,b,t)=C_2(E,b)+2t(I+X).                            (14)
\]

The product preparer fixes `t=0`. The native correlated preparer
`A_corr=G_e;CX(e,B)` instead has `Pr(00)=p,Pr(11)=p²` and SAME
`E=b=p²`, but `t=p³`. Its full echo uses19 stages
`(2G,9CX,8SourceI)`;32 real cancelling CX give common N51.
Its return and feedback bands are exactly

\[
 C_{\rm corr}=pI+p^2X,\quad
 \operatorname{spec}F_{\rm corr}=\{0,1-p^6\},\quad
 J_{\rm product}-J_{\rm corr}
       =-4\log[1-\zeta(1-p^{12})]>0.                 (15)
\]

The WHOLE heat is identical. Even the local fixed-marginal source is

\[
 \partial_tJ|_{E=b=p^2,t=0}=-32\zeta p^6/R_0\ne0.    (16)
\]

Thus a genuine native correlation edit preserves BOTH field means
but changes full Book price. The two-marginal dictionary must derive
joint independence from the actual generated preparation/constraint,
or retain this extra source. It is not enough to call V Z-readable.
Future tests can distinguish the joint laws; no equality of full
future profiles is claimed. The exact product-return operation is
proved, while physical field generation, independent joint equations
and `GR_closed`/raw216 completion remain open.
