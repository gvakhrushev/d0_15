# No-reset first-match occupation: stationary native input, exact defect, and paid preparation

22 October 2026. Existing Draft #334 / native-programme-v1. This is a bounded
extension of the same first-match owner. It changes no task, acceptance flag,
physical primitive, Info definition, or selected Book action.

**New substitution.** Independent fresh trials are unnecessary for the
first-match **additive occupation/charge law** when the actual sequential
instrument starts in its stationary marginal and every relevant killed
channel is transient. The complete records may remain correlated. The exact
nonstationary correction and its first source are explicit, including at a
stationary base with a moving instrument. Finite preparation by the original
channel gives a controlled approximation with its full prefix still paid and
retained. This does not extend the iid Shannon/CQ entropy theorem by analogy.

The original inverse-square preparation, its uniqueness and its paid prefix
are **consumed owned results**, not new stationary-state claims:

- [original preparation owner](../../A4D_NATIVE_PREPARATION_AND_GOLDEN_OFFSHELL_SOURCE_2026_10_21.md)
  and [its proof §§1–6](../d0_native_preparation_closure_2026-10-21/PROOF.md);
- [literal full128 channel](../../A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md)
  and [actual paid-port history](../d0_same_history_price_composition_2026-10-20/paid_port_history.md);
- [sequential native Book-return companion](SEQUENTIAL_FULL128_BOOK_RETURN.md)
  and [active-label support companion](NATIVE_ACTIVE_LABEL_SUPPORT.md).

## 1. Exact finite no-reset recurrence and charge source

Let the complete instrument on the fixed DATA carrier have branches
\(\mathcal I_a(X)=K_aXK_a^\dagger\) and trace-preserving sum \(\Phi\).
Every oldRIGHT component is kept: tensor these maps with its identity.
In the additive formulas, \(\rho\) denotes the DATA marginal; stationarity
of that marginal does not assert joint factorization, erase DATA–oldRIGHT
correlations, or determine their information price.
The first outcome \(a\) is retained as the anchor. Execute at most \(K\)
later comparisons, stop at the first later outcome equal to \(a\), and keep
the full unmatched terminal word as the cap-abort output. Thus a programme
has at most \(K+1\) native rounds, with no reset of DATA. Integer \(K\) is
held fixed in every smooth source below.

Let \(c_b\) be the actual additive round charge and \(k_{ab}\) an additional
specified additive comparison charge. Both may move. This notation does not
certify a comparator's physical cost or identify its Shannon entropy. A
random comparison factory can be included in the branches on an enlarged
carrier; replacing it by a conditional mean is valid only for an already
justified additive ledger that does not alter the subsequent dynamics.

For an analytical marker \(t\), define

\[
 E_a(t)=e^{-t(c_a+k_{aa})}K_a^\dagger K_a,\qquad
 \mathcal T_a^*(t)(X)=\sum_{b\ne a}e^{-t(c_b+k_{ab})}K_b^\dagger X K_b,
\]
\[
 R_{a,0}(t)=I,\quad R_{a,j}(t)=E_a(t)+\mathcal T_a^*(t)(R_{a,j-1}(t)),
 \qquad N_K(t)=\sum_a e^{-tc_a}K_a^\dagger R_{a,K}(t)K_a.       \tag{1}
\]

Expanding (1) retains every complete stopped word \(\omega\), including its
cap abort:
\(N_K(t)=\sum_\omega e^{-tC_\omega}K_\omega^\dagger K_\omega\).
Completeness gives \(R_{a,j}(0)=I\) and \(N_K(0)=I\). At positive \(t\),
\(N_K(t)\) is a generating Gram, generally neither \(I\) nor a scalar.
Normalizing marked amplitudes by \(N_K(t)^{-1/2}\) would construct a different
instrument; it is not free normalization of this physical programme.

Write \(E_b=K_b^\dagger K_b\),
\(\mathcal T_a^*=\mathcal T_a^*(0)\), and

\[
 C=\sum_b c_bE_b,\qquad L_a=C+\sum_b k_{ab}E_b.
\]

The exact charge effect is

\[
 \boxed{\mathcal C_K=-\partial_tN_K(0)
 =C+\sum_a K_a^\dagger B_{a,K}K_a,\quad
 B_{a,0}=0,\quad B_{a,j}=L_a+\mathcal T_a^*(B_{a,j-1}).}       \tag{2}
\]

For any normalized actual input \(\rho\), the full first source is

\[
 D\mathbb E C_K=\operatorname{Tr}(D\rho)\mathcal C_K
                +\operatorname{Tr}\rho\,D\mathcal C_K,       \tag{3}
\]
\[
 DB_{a,j}=DL_a+(D\mathcal T_a^*)(B_{a,j-1})
                       +\mathcal T_a^*(DB_{a,j-1}),          \tag{4}
\]
\[
 D\mathcal C_K=DC+\sum_a\big[(DK_a^\dagger)B_{a,K}K_a
          +K_a^\dagger(DB_{a,K})K_a+K_a^\dagger B_{a,K}DK_a\big].
                                                               \tag{5}
\]

Here \(DC=\sum_b[(Dc_b)E_b+c_bDE_b]\) and
\(DL_a=DC+\sum_b[(Dk_{ab})E_b+k_{ab}DE_b]\). All original adjoint,
observer and field variations enter the actual \(DK_a\). No commuting
replacement of the ordered products in (4)–(5) is made.

## 2. Finite occupation and the exact stationarity defect

Use Schrödinger maps
\(\mathcal T_a=\Phi-\mathcal I_a\), and define

\[
 \sigma_a=\mathcal I_a(\rho),\qquad
 \delta=(\Phi-I)\rho,\qquad
 \mathcal R_{a,K}=\sum_{j=0}^{K-1}\mathcal T_a^j.
\]

The unnormalized expected incoming DATA state before comparisons with anchor
\(a\) is \(X_{a,K}=\mathcal R_{a,K}\sigma_a\). The identity
\(\sigma_a=(I-\mathcal T_a)\rho+\delta\) telescopes to

\[
 \boxed{X_{a,K}=(I-\mathcal T_a^K)\rho+\mathcal R_{a,K}\delta.} \tag{6}
\]

Consequently the mean number of comparisons of type \((a,b)\), the mean
number of native rounds, and the complete mean charge are respectively

\[
 n_{ab,K}=\operatorname{Tr}\mathcal I_b(X_{a,K}),\qquad
 \mathbb E T_K=1+\sum_a\operatorname{Tr}X_{a,K},               \tag{7}
\]
\[
 \mathbb E C_K=\operatorname{Tr}\rho C
                         +\sum_a\operatorname{Tr}L_aX_{a,K}.\tag{8}
\]

This includes the last unsuccessful comparison on every cap-abort word.
There is no IID probability \(q_b\) substituted for a conditioned branch.
For every finite \(K\), including at zero-probability labels, the full jet is

\[
 D\delta=(D\Phi)\rho+(\Phi-I)D\rho,                         \tag{9}
\]
\[
 \boxed{DX_{a,K}=(I-\mathcal T_a^K)D\rho
 -(D\mathcal T_a^K)\rho+(D\mathcal R_{a,K})\delta
                                      +\mathcal R_{a,K}D\delta,} \tag{10}
\]
\[
 D\mathcal T_a^j=\sum_{i=0}^{j-1}\mathcal T_a^i
                      (D\mathcal T_a)\mathcal T_a^{j-1-i}.
\]

Differentiate (7)–(8), including \(D\mathcal I_b\), \(DC\), \(DL_a\),
and \(D\rho\). Equations (3)–(5) and (8)–(10) are two equal exact
contractions of the same complete finite tree.

## 3. Stationary correlated records: the non-IID occupation theorem

Assume \(\Phi(\rho_*)=\rho_*\), \(\operatorname{Tr}\rho_*=1\), and
that for each active anchor \(a\), the spectral radius of \(\mathcal T_a\)
is strictly less than one. Put \(q_b=\operatorname{Tr}\mathcal I_b(\rho_*)\)
and let \(m\) count the active anchor labels \(\{a:q_a>0\}\). With
\(\mathcal R_a=(I-\mathcal T_a)^{-1}\), (6) gives

\[
 \boxed{X_{a,\infty}=\rho_*,\qquad
       \mathbb E N_{ab}=q_b,\qquad \mathbb E T_\infty=m+1.}    \tag{11}
\]

No equality of conditional next-outcome probabilities is needed. If
\(s=\operatorname{Tr}\rho_* C\) and \(\kappa_b=\sum_a k_{ab}\), then

\[
 \boxed{\mathbb E C_\infty=(m+1)s+\sum_bq_b\kappa_b.}        \tag{12}
\]

Thus the unequal-comparator **column-sum** criterion in the existing owner
also works for these correlated stationary executions. The scope is still
the specified additive charge. A conditional status-code example with
\(k_{aa}=1\), \(k_{ab}=2\) for \(a\ne b\) has mean \(2m-1\); this
does not turn that deterministic encoding into an original stochastic
Golden primitive or price the actual equality circuit.

The same proof applies to CP outcome maps with several Kraus operators.
In particular a coarse anchor can control stopping while all fine labels
remain retained and charged. The number \(m\) then counts **anchor classes**,
not discarded fine records. A three-class READY task would have multiplier
four under these actual stationarity/transience hypotheses; it is a different
stopping rule from equality of the native full128 fine labels.

### A sufficient transience condition with an elementary proof

If \(\Phi\) has a unique normalized stationary density \(\rho_*\), then
every branch with \(q_a>0\) is transient. In particular a faithful unique
stationary density suffices for every nonzero Kraus branch.

Indeed \(F_n=(\mathcal T_a^*)^n(I)\) decreases to \(F\ge0\). If
\(F\ne0\), choose a density \(\eta\) with
\(s=\operatorname{Tr}F\eta>0\). The positive Cesàro sequence
\(Y_N=N^{-1}\sum_{j<N}\mathcal T_a^j\eta\) has a convergent subsequence
with limit \(Y\ge0\), \(\operatorname{Tr}Y=s\), and
\(\mathcal T_aY=Y\). Trace preservation of \(\Phi\) implies
\(\operatorname{Tr}\mathcal I_aY=0\), hence \(\mathcal I_aY=0\) by
positivity. Therefore \(\Phi Y=Y\). Uniqueness gives \(Y=s\rho_*\),
contradicting \(q_a>0\). Thus \(F=0\). In finite dimension this implies
\(\mathcal T_a^n\to0\) as a linear map and its spectral radius is below
one. No separate large spectral computation is needed.

Uniqueness cannot be omitted. For an orthogonal projective instrument
\(K_a=P_a\), the next outcome after anchor \(a\) is already \(a\).
For every cap \(K\ge1\), exactly **two** rounds are executed. In the binary
case the IID answer three is false, despite stationary input \(I/2\).

## 4. First source: stationarity at one point is insufficient

On a fixed-support chart where every active \(\mathcal T_a\) stays
transient, an arbitrary input has the exact uncapped identity

\[
 X_a=\rho+\mathcal R_a\delta,\qquad
 DX_a=D\rho+\mathcal R_a(D\mathcal T_a)\mathcal R_a\delta
                                               +\mathcal R_aD\delta. \tag{13}
\]

At a stationary base \(\delta=0\), this reduces to

\[
 \boxed{DX_a=D\rho+\mathcal R_aD\delta,\qquad
 D n_{ab}=Dq_b+\operatorname{Tr}\mathcal I_b(\mathcal R_aD\delta).} \tag{14}
\]

The exact charge source there is

\[
 \boxed{D\mathbb E C_\infty=(m+1)Ds+
 \sum_b\kappa_bDq_b+\sum_bq_bD\kappa_b
                     +\sum_a\operatorname{Tr}L_a\mathcal R_aD\delta.} \tag{15}
\]

For a **moving stationary family**, \(D\delta=0\), so the last term
vanishes. For a physically fixed preparation with a moving instrument it
is generally nonzero. Likewise a common column sum \(\kappa_b=\kappa\)
cancels the probability tangent, but leaves \(D\kappa\). Independent
preparation, factory and comparator sources are not set to zero.

The exact two-Kraus checker below has
\(\rho_*=\mathrm{diag}(9/25,16/25)\) and stationary mean three rounds.
For its stated completeness-preserving Kraus tangent while freezing this
input, \(D\mathbb E T_\infty=-7077/24050\ne0\). Including the induced
stationary preparation tangent makes that source zero. This is an explicit
counterexample to differentiating (11) at a merely stationary base.

## 5. Consumption of the actual full128 stationary preparation

The owned original channel is

\[
 \Phi(X)=X+\epsilon\{\mathcal T(DXD)-\tfrac12(\Delta X+X\Delta)\},
 \qquad \Delta=D^2,
\]

with bistochastic selfadjoint recycling \(\mathcal T\). The original
preparation owner proves: if \(D\) is invertible and \(\mathcal T\) has
a strict contraction on traceless matrices, then

\[
 \rho_*=\Delta^{-1}/Z,\qquad Z=\operatorname{Tr}\Delta^{-1},           \tag{16}
\]

is the unique stationary density, and all original sequential marginals
converge to it. The same owner proves the actual Fourier-fixture recycling
bound \(q\le39/40\) at \(\nu=3/5\), including the admitted strict-Julia
proper-boost chart. Its source, consumed unchanged, is

\[
 D\rho_*=-\Delta^{-1}(D\Delta)\Delta^{-1}/Z
             +\rho_*\operatorname{Tr}[\Delta^{-1}(D\Delta)\Delta^{-1}]/Z.
                                                                    \tag{17}
\]

Equations (11)–(15) therefore apply to this **same actual native channel**
on the owned regular chart, without resetting DATA and without another
stationary-state solve. The prior proof of (16) is the input; the new result
is its first-label return occupation and the explicit departure term (13).
The unchanged oldRIGHT tensor remains throughout. This does not replace the
actual Jones or joint CAR input by (16) without preparing and paying for it.

The literal original port charge is
\(C=I+p\epsilon\Delta\), \(p=\varphi^{-1}\). Hence its known part is

\[
 \mathbb E C_{\rm port,\infty}=(m+1)\left(1+\frac{p\epsilon d}{Z}\right),
 \quad
 D\mathbb E C_{\rm port,\infty}
 =(m+1)pd\left(\frac{D\epsilon}{Z}-\frac{\epsilon DZ}{Z^2}\right),     \tag{18}
\]

on a moving stationary fixed-support chart. The count is constant there;
the actual port charge need not be. All other price components keep their
own sources. The two calibrations \(A=hD/16\) and \(\epsilon_A=4p^2\)
give the same effect \(p\epsilon\Delta=4p^3A^2\); they are not adjustable
coefficients.

The [literal support companion](NATIVE_ACTIVE_LABEL_SUPPORT.md) determines
the active alphabet: at the specified flat phases \((i,i,-1,-i)\),
\(\nu=3/5\), there are 42 nonzero fine Kraus branches, hence stationary
mean **43** native rounds. On its nonzero proper-boost chart there are 64,
hence **65**. All 128 labels stay in the finite instrument, including dark
ones. Neither count is the three-class READY prefactor.

This support jump forbids differentiation of the uncapped count across the
flat point. A newly born branch has vanishing anchor probability but a
diverging conditional waiting time. Its uncapped occupation approaches one
whole stationary state. The limits of infinite cap and vanishing field
therefore do not commute. Equations (1)–(10) remain exact at every finite
cap and across the support birth; an uncapped source needs fixed support and
uniform transience on the chart being differentiated.

## 6. Finite actual preparation prefix, with its full retained cost

Starting from the actual \(\rho_0\), execute \(L\) original native rounds
before choosing the first-match anchor. Retain every preparation record.
Its DATA marginal is \(\rho_L=\Phi^L\rho_0\), and its exact defect is

\[
 \delta_L=(\Phi-I)\rho_L=\Phi^L\delta_0,\qquad
 \delta_0=(\Phi-I)\rho_0,                                             \tag{19}
\]
\[
 D\delta_L=\Phi^L D\delta_0+
        \sum_{j=0}^{L-1}\Phi^j(D\Phi)\Phi^{L-1-j}\delta_0.            \tag{20}
\]

Use \(\rho_L,\delta_L\) directly in (6) or (13); no finite prefix is
declared exactly stationary. For any owned mixing bound on trace-zero
operators \(\|\Phi^j\|\le M r^j\), \(0<r<1\), one obtains

\[
 \|\delta_L\|\le Mr^L\|\delta_0\|,\qquad
 \|D\delta_L\|\le Mr^L\|D\delta_0\|
                    +LM^2r^{L-1}\|D\Phi\|\,\|\delta_0\|.           \tag{21}
\]

The extra occupation term is \(\mathcal R_a\delta_L\); its norm is at
most \(\|\mathcal R_a\|Mr^L\|\delta_0\|\). Its derivative is

\[
 D(\mathcal R_a\delta_L)=\mathcal R_a(D\mathcal T_a)\mathcal R_a\delta_L
                                        +\mathcal R_aD\delta_L.      \tag{22}
\]

No uniform bound on \(\|\mathcal R_a\|\) is asserted at a support birth,
closing gap or spatial refinement. The recycling bound \(39/40\) is not
silently substituted for a mixing bound of \(\Phi\); the preparation owner
supplies the latter only with its stated finite-chart constants.

The full mean additive price is the prefix price
\(\sum_{j<L}\operatorname{Tr}C\Phi^j\rho_0\), plus (8) or (12) with
its defect term for the following stopping stage, plus every actual
comparison/controller price. Differentiate the entire prefix as well. For
the original port part, the existing preparation proof §6 already gives its
exact Poisson boundary formula; this theorem does not charge it twice.

The retained coherent prefix contains more than its reduced marginal. In
the companion's same initialized-blank Book cut, the clean chronological
word is \(0^L00\), with native amplitude \(B^{L+2}\) and unmarked
**clean-corner Gram** \(B^{2(L+2)}\), \(B=I-\epsilon\Delta/2\). The
complete stopped column still has Gram \(I\). Replacing the complete prepared
work by \(\rho_*\) would change that Book object. The occupation reduction
is a computation of additive expectations on the retained execution, not a
deletion of its preparation tape, physical clock, or return source.

## 7. Information boundary and bounded exact receipt

The occupation theorem does not imply
\(H(\text{stopped tape})=(m+1)H(\text{one label})\) for correlated
records, nor the analogous iid product-CQ identity. Already at cap one,
stationarity gives
\(H(Y_1,Y_2)=2H(Y_1)-I(Y_1;Y_2)\). The rational two-Kraus fixture has
\(P(00)-P(0)^2=7056/390625\ne0\), so this mutual information is strictly
positive. All own code entropy must still be counted once on the actual
complete record. Full Book Info, heat, work, clock, independent inputs and
the selected \(D_{42}(H+J+R)\) are unchanged obligations.

Run [check_stationary_occupation.py](check_stationary_occupation.py).
The stdlib Fraction receipt [STATIONARY_OCCUPATION_RESULT.json](STATIONARY_OCCUPATION_RESULT.json)
records **608 exact checks**. It uses two genuinely non-IID rational Kraus
instruments with two and three outcomes, cap \(K=1,\ldots,5\), and three
independent source cases: fixed stationary input, moving stationary input,
and moving independent preparation. Every complete stopping leaf and cap
abort is enumerated separately (largest tree: 189 leaves). Checks cover
operator normalization, every comparison cell, full moving charge effects,
their first sources, two nonzero analytical marks, the exact resolvent
defect, finite retained preparation prefixes \(L=0,\ldots,5\), and the
projective counterexample. No original full128 expensive suite is rerun.

The diagnostic proves these finite algebraic identities and tests their
scope. The native application consumes the existing original preparation
theorem and the separate exact support companion. It does not claim a new
physical preparation selection, comparator-price admission, entropy law,
or closure of the selected full Book/GR source.
