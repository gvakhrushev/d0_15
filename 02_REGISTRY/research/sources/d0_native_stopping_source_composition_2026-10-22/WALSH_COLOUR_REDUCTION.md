# Original Walsh colours: an exact all-K source reduction

22 October 2026. Same original CAR16/full128 programme, existing #334,
`constitutive/native-programme-v1`. This consumes the already-owned literal
PORT reduction. It removes another explicit long-history information term
without changing a tariff, preparing a new DATA state, resetting DATA, or
selecting a heat. `GR_closed=false`.

## 1. New parent substitution

After the exact PORT refinement is removed, the 65-label readout has 33
live Kraus outcomes. Seven of its actual Julia rows are the same Kraus
operator up to sign; another four are the same up to sign. Their complete
retained label entropy is therefore an **exact additive count source**.
The remaining calculation uses 24 live computational branches. All 128
physical fine slots and their costs remain in the actual execution; the
new readout has 56 classes including 32 dark classes.

Let `Gamma_M,K` be the existing port-merged CQ record and `Gamma_C,K` the
same record with only these seven/four row colours grouped. The new identity is

\[
 S(\Gamma_{M,K})-S(\Gamma_{C,K})
 =\log7\,\mathbb E N_7+\log4\,\mathbb E N_4.              \tag{1}
\]

It holds for every finite K and every retained input, including a
correlated reference, on the original open one-boost `(r,nu)` chart.
At the original anchor its **entire first source** also transports for
arbitrary smooth amplitude/preparation jets that break the row equality;
the required averaged Kraus jet is given in section 5. No second-source
or whole-neighbourhood identity for such symmetry-breaking jets is claimed.

In the existing literal port-price formula the net paired coefficient
was `p^3`, with `p=phi^-1` and `ell=log(phi)`. Equation (1) gives the exact
further substitution

\[
\begin{aligned}
 C_{\rm port}-[S(\Gamma_F)-S(\Omega)]/\ell
 ={}&\mathbb E\left[N_0+2N_{\rm orphan}
       +p^3N_{\rm pair}
       -\frac{\log7}{\ell}N_7
       -\frac{\log4}{\ell}N_4\right]\\
 &-[S(\Gamma_C)-S(\Omega)]/\ell .                         \tag{2}
\end{aligned}
\]

Here `N_pair` still counts **every** paired event, including the seven/four
classes. Thus the effective contributions for these two classes are
`p^3-log(7)/ell` and `p^3-log(4)/ell`. These are computed components of
Cost-minus-Info, not new physical code lengths or a declaration that
SELECT/clock/preparation work is free. All charges outside the already
bound `c_b=1+b` port component remain in the same places on both sides.

## 2. Original inputs and exact Walsh identity

The immutable constructor is
`sources/d0_book_uniform_source_2026-10-21/check_uniform_book_source.py`,
Git blob `ee8de4635d24c668949ac9a0186616ab7d59f2ed`. The existing analytic
entropy/source owner is
`sources/d0_native_complete_cq_source_2026-10-22/check_complete_history_source.py`,
Git blob `c133c6aec28e2a4068b36a6d9646bc8fb04fc2a4`. The parent literal
charge identity is `d0_native_stationary_memory_composition_2026-10-22/LITERAL_PORT_PRICE_REDUCTION.md`.
The new checker imports only the necessary definitions from the pinned
original files and verifies their bytes.

Keep the original ordering `(0,2,3,1)`, phases `(i,i,-1,-i)`, boost
`U=exp(theta G)` in role 1, `theta=2atanh(r)`, and contraction `nu`.
Write `L,R` for the two boosted Julia roots, `L0,R0` for the unboosted
roots of that role, and

\[
 D_+=(L-L_0)+(R-R_0),\qquad
 D_-=(L-L_0)-(R-R_0).                                    \tag{3}
\]

The original 64 Walsh row slots are `N_j`. The actual equalities are

| Class | Original SELECT rows j | Signs relative to first row | Representative |
|---|---|---|---|
| seven colours | 1,17,25,33,41,49,57 | +,−,−,+,+,−,− | `N_1=D_+/16` |
| four colours | 5,21,37,53 | +,−,+,− | `N_5=D_-/16` |

These are matrix equalities, not equality of row spectra. To prove them,
write each duplicated word index as `2(4d+k)+epsilon`. Odd Walsh labels
cancel between the duplicates. For even labels `2m`, write
`m=4a+2c+b`. Its Julia row is

\[
 \frac1{16}\sum_{d=0}^3(-1)^{a\cdot d}
 \left[L_d-(-1)^cL_{0d}
       +(-1)^b(R_d-(-1)^cR_{0d})\right].                  \tag{4}
\]

Only role 1 is boosted. For every other role the differences vanish.
Also `L0d+R0d=(1+s)I`, `s=sqrt(1-nu^2)`, independently of d. Formula
(4) immediately gives four signed copies of `D_+` when `(c,b)=(0,0)`,
four copies of `D_-` when `(c,b)=(0,1)`, and three further signed copies
of `D_+` when `(c,b)=(1,0)` with nontrivial role character. The remaining
trivial character has an additional scalar term and is not grouped.
This proof applies on the open contraction chart; differentiating it
retains all its r/nu jets. The checker verifies it with exact Fraction
coefficients of formal Julia-root and number-operator symbols.

The existing port-merged Kraus matrices are

\[
 M_0=B,\quad M_1=K_{0,1},\quad
 M_{j+1}=-\sqrt{2t}\,N_j^*A\quad(j\ne0),
 \qquad A=N_0,\ t=2p^2.                                 \tag{5}
\]

Thus the merged labels are `{2,18,26,34,42,50,58}` and
`{6,22,38,54}`, with the same displayed signs. Blank and orphan stay
separate. Replace each class of size m by `C=sqrt(m) M_rep`; leave all
other readout classes unchanged. The unconditional DATA channel Phi is
identical. There are 24 live branches, not eight: the prior eight
row-Gram spectral classes do not identify channels.

## 3. Every finite word and full preparation

For a fixed colour-grouped chronological word z, every original colour
refinement multiplies the whole operator product by a scalar sign and
`product m_j^(-1/2)`. These scalars commute with all intervening
noncommuting operations. All refinements consequently have the same
normalized final DATA-reference state and equal probabilities within
their fibre. The fibre entropy is `N_7(z) log7+N_4(z) log4`.
Summing proves (1), with no reset or independence assumption about DATA.

The actual colour count effects are

\[
 C_7=\sum_{a\in\mathcal C_7}M_a^*M_a,
 \quad C_4=\sum_{a\in\mathcal C_4}M_a^*M_a,
 \quad D=\log7\,C_7+\log4\,C_4.                           \tag{6}
\]

For an arbitrary input, the removed information is exactly

\[
 I_{\rm colour,K}=\operatorname{Tr}(\Omega F_K),\qquad
 F_K=\sum_{n=0}^{K-1}(\Phi^*)^nD.                         \tag{7}
\]

With a retained reference, `F_K` is tensored with its identity. This is
the full preparation score, not `K D` with a frozen stationary input.
The same finite recursion gives every field source without enumerating
the history tree:

\[
 F_{k+1}=D+\Phi^*F_k,\qquad
 \dot F_{k+1}=\dot D+\dot\Phi^*F_k+\Phi^*\dot F_k,
 \qquad F_0=\dot F_0=0.                                  \tag{8}
\]

Thus `dot I=Tr(dot Omega F_K)+Tr(Omega dot F_K)` includes the actual
incoming preparation and every intervening field variation. Existing
Poisson/Fredholm machinery can evaluate the same finite sum; a new
controller or stopping price is not introduced.

## 4. Closed native scalar source, including K4096

On the existing stationary section `rho=Delta^-1/Z`, `Delta=A* A`,
`h=16/Z`, every individual colour in the two classes has the same
probability q. There is a closed two-mode expression. Put

\[
 c=\cosh(2\theta),\quad s=\sqrt{1-\nu^2},\quad
 u=\sqrt{1-\nu^2c},\quad \chi=\frac{c+1}{2c},
\]

\[
 f=(u-1)^2+(s-1)^2-(u-1)(s-1)(1+\chi).
\]

Then

\[
 \boxed{q=\frac{t h}{256}f,\qquad
 I_{\rm colour,K}=Kq(7\log7+4\log4).}                    \tag{9}
\]

For the proof, `L-L0` is supported on the fully occupied 0/1 sector and
`R-R0` on the one-particle 0/1 sector. These supports are orthogonal, so
`D_+^2=D_-^2`. In each spectator sector, the right-root rank-one projector
has overlap chi with its unboosted projector. Hence
`Tr D_+^2=Tr D_-^2=8f` on the full 16-dimensional DATA space.
Using `N_1=D_+/16` and the existing stationary identity
`M rho M*=2t N_j* N_j/Z` gives (9). Spectator parity only changes an
off-diagonal sign in the one-particle block and leaves this trace unchanged.

The first source is obtained by differentiating the displayed elementary
formula. Explicitly, if `a=u-1`, `b=s-1`,

\[
 \dot f=2a\dot u+2b\dot s
 -(b\dot u+a\dot s)(1+\chi)-ab\dot\chi,
 \quad\dot q=\frac t{256}(\dot h f+h\dot f).               \tag{10}
\]

On the native point `r=1/9,nu=3/5`, with the existing boost direction r
and one-port-null direction `v=partial_r-nu h_r/(2h) partial_nu`, the
closed formula and the unchanged Kraus/source matrices agree:

| Quantity | Per tick | K=4096 |
|---|---:|---:|
| Colour entropy, nats | 0.0000020401040956228075 | 0.00835626637567102 |
| r-source | +0.00004574389219266401 | +0.1873669824211518 |
| v-source | +0.00004674489475961614 | +0.19146708893538772 |

These decimals are numerical evaluations of the exact formula, not
outward interval certificates. The value is small while the derivative
is material; the value alone supplies no derivative estimate.
In particular this known positive v colour term is larger in magnitude
than the previously computed negative paired-bit v term
`-0.02440620486766245` at K4096. Their sum is another known component,
not the full remaining 24-branch history source. No conclusion about the
sign of that uncomputed remainder follows from entropy positivity.

## 5. Arbitrary ambient first-source transport at the anchor

Suppose a class has `M_a=s_a M` at the anchor, `|s_a|=1`, but its admitted
amplitude jets need not preserve that equality. The correct compressed
first jet is

\[
 C=\sqrt m\,M,\qquad
 \dot C=\frac1{\sqrt m}\sum_a\overline{s_a}\,\dot M_a.
 \tag{11}
\]

For every independently varied input, expanding products proves

\[
 \sum_a\left(\dot M_a\Omega M_a^*+M_a\dot\Omega M_a^*
                 +M_a\Omega\dot M_a^*\right)
 =\dot C\Omega C^*+C\dot\Omega C^*+C\Omega\dot C^*.
 \tag{12}
\]

It follows by chronological composition that (11) reproduces every
coarse output block and its first variation for any fixed finite K.
At the anchor the refined blocks within a fibre are `X_z/d_z`, where
`d_z=7^{N_7(z)}4^{N_4(z)}`. On their common support,
`log(X_z/d_z)=log X_z-log(d_z)`. Therefore the differentiated entropy
difference is exactly

\[
 D[S(\Gamma_M)-S(\Gamma_C)]
 =D\mathbb E[N_7\log7+N_4\log4].                         \tag{13}
\]

This proof does not assume that the individual refined probabilities
have identical derivatives. It supplies the full first covector at the
anchor, including preparations, from the actual averaged jets. Smooth
amplitude rank births have eigenvalues of order `epsilon^2` and entropy
of order `epsilon^2 |log epsilon|`; their first contribution is zero.
No unsupported C2 extension is asserted. For arbitrary independently
varied density states on a rank boundary, retain the usual existence
conditions for an ordinary entropy derivative; the original rho is
strictly positive.

Away from the one-boost chart, the actual grouped CP channel can require
multiple Kraus operators. Formula (11) is its correct first-jet
representation at the anchor, not a replacement physical execution on
an open full-field neighbourhood. In particular, an actual common
42-field writer and its physical price remain separate obligations.

The checker includes a deliberately symmetry-breaking **complete Kraus
amplitude tangent** obtained by a small unitary rotation of physical
output slots, together with an independent input perturbation. It checks
(12), (13), and the normal counter (8) at K1/K2. This is an ambient
algebra control, not a claimed native field-writing primitive.

## 6. Composition with a PORT-sensitive stopping controller

If the actual bounded stopping rule reads PORT bits but is insensitive
to these row colours, the admissible refined PORT mass `a_z` from the
same-programme stopping proof is independent of the seven/four colour
assignment. The colour fibre remains uniform. Consequently (1)–(2)
apply with the true stopped counts, and the already derived stopping
term `-E log(a_z)/ell` stays in the price unchanged. The finite counter
is evaluated on the existing controller-augmented channel and genuine
live prefixes, retaining the paid cap and terminal cases.

This does not cover a stopping rule that reads the erased row colour.
Such a rule needs its own admissible fibre weight; uniformity cannot be
imported from the fixed-window result. Likewise, colour-dependent
charges outside the literal port component must remain explicitly
priced, especially under jets that change their individual probabilities.

## 7. Genuine filter boundary and verification

The reduction is not a finite posterior-state theorem. On the actual
two-band Delta, let `0<lambda_-<lambda_+` and
`b_-=1-t lambda_->b_+=1-t lambda_+>0`. After n genuine blanks the posterior
band-weight ratio is multiplied by `(b_-/b_+)^(2n)`. These ratios are all
different, and the next-blank probabilities increase strictly to
`b_-^2`. The blank histories have positive probability. Thus even this
one actual family already gives infinitely many predictively distinct
filter states. Finite DATA dimension and the eight one-round spectral
classes do not provide a finite set of filter states. The remaining
24-branch entropy/source has not been declared closed.

`check_walsh_colour_reduction.py` emits JSON and accepts `--json PATH`.
It auto-discovers the repository root from cwd/script ancestors, accepts
`--repo-root`, or can use `--input-dir` containing the two pinned source
files. The receipt is `RESULT_WALSH_COLOUR_REDUCTION.json`.
It checks formal exact Walsh identities; unchanged native matrices and
both native jets; completeness and physical multiplicities; actual
K1/K2 colour/source identities; the hostile ambient/preparation jet;
the closed scalar native source; and the distinct actual blank filters.
The quantum entropy replay keeps every singular mode with the existing
`eta=1e-22` regularization, whose source error bound is reported separately
from ordinary floating arithmetic. No new long history enumeration,
action fit, heat selection, or physical GR closure is inferred.
