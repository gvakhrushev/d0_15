# Sequential first-label return on the original full128 instrument

Date: 2026-10-22. Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`.
Assembly carrier/slot: `native-programme-v1` / `constitutive`. Supporting
application in existing Draft #334; `GR_closed=false`.

## 1. The premise replaced, and the input actually consumed

The [first-match owner](../../A4D_FIRST_MATCH_WALD_NATIVE_INFORMATION_FULL_SOURCE_2026_10_22.md)
proves its complete CQ price and information identities for independently
prepared complete trials. Those identities cannot be applied to repeated use
of the original instrument on its previous output DATA. Here the same DATA
continues after each outcome. The stopping rule is compiled at finite cap,
and its complete marked Gram and actual clean-return corner are calculated
from the original Kraus matrices, rather than from an iid outcome law.

The native matrix input is the unchanged constructor in
[`../d0_book_uniform_source_2026-10-21/check_uniform_book_source.py`](../d0_book_uniform_source_2026-10-21/check_uniform_book_source.py),
git blob `ee8de4635d24c668949ac9a0186616ab7d59f2ed`. It supplies the original
Walsh/Julia/Golden 128-outcome instrument on all 16 CAR grades and its proper
role-1 boost derivative in one Fourier block. Its first, allblank Kraus matrix
is

\[
B=K_0=I-2p^2 a^\dagger a,
\qquad p=\varphi^{-1},\qquad 0\le a^\dagger a\le I.
\tag{1}
\]

Thus \(B=B^\dagger\ge(1-2p^2)I=(2p-1)I>0\). This is the original matrix,
not a newly supplied query amplitude. The current numerical consumer retains
all 128 outcomes and all 16 grades, including dark outcomes. It does not infer
positive iid support size 128 and does not claim a full spatial/all42 result.

The finite forward-clock determinant is consumed from
[`A4D_FULL_HJR_FORWARD_CLOCK_TRANSPORT_2026_10_21.md`](../../A4D_FULL_HJR_FORWARD_CLOCK_TRANSPORT_2026_10_21.md).
The new application is its explicit first-label stopped corner and complete
noncommuting normalizer on this instrument. Book03 already specifies the
master scalar and stationarity; choosing another aggregation scalar is not
an outstanding task.

## 2. Complete stopped execution without a reset

Let \(K_a(y)\), \(0\le a<m\), be a differentiable finite instrument,
\(\sum_a K_a^\dagger K_a=I\). Retain the first outcome \(a\). Produce further
outcomes on the previous output state, until the first later occurrence of
the same \(a\), or until \(K\ge1\) later comparisons have completed. Retain
every mismatch, the final match or cap-abort, and every actual factory record.
No postselection or reset occurs.

For a retained word \(w=(a,b_1,\ldots,b_j)\), its operator is
\(L_w=K_{b_j}\cdots K_{b_1}K_a\). For a matched leaf, \(b_j=a\) and every
earlier \(b_i\ne a\). For an aborted leaf, \(j=K\) and every \(b_i\ne a\).
These words are prefix-free: no terminated word is an allowed initial
segment of a longer leaf. Consequently, writing them in separate outcome
slots padded with zero does not identify two allowed leaves. In particular,
the allzero word is the unique leaf \(00\), and it is matched, never aborted.

Let \(c_b\) be the actual charged component of one outcome and
\(\kappa_{ab}\) that of its comparison with anchor \(a\). The simple formulas
below assume these charges are scalars for the specified complete branch.
If factories have more outcomes, retain their raw records and use the grouped
instrument \(\mathcal I_a(X)=\sum_v K_{a,v}XK_{a,v}^\dagger\), with the actual
factory marks inside each matched/mismatched sum. Equality must remain on the
specified original labels \(a\); comparing the refined pairs \((a,v)\) instead
would change the stopping task. If factories or controllers retain memory,
use the enlarged state and its actual CP map. A cap in the number of
comparisons is not an arbitrary deadline in physical time.

For fixed nonnegative charges, define

\[
\begin{aligned}
E_{a,t}&=e^{-t(c_a+\kappa_{aa})}K_a^\dagger K_a,\\
\mathcal T_{a,t}^{*}(X)
 &=\sum_{b\ne a}e^{-t(c_b+\kappa_{ab})}K_b^\dagger X K_b,\\
R_{a,0}(t)&=I,\qquad
R_{a,k}(t)=E_{a,t}+\mathcal T_{a,t}^{*}(R_{a,k-1}(t)),\\
N_K(t)&=\sum_a e^{-tc_a}K_a^\dagger R_{a,K}(t)K_a.
\end{aligned}
\tag{2}
\]

Unrolling gives

\[
R_{a,K}=
\sum_{j=0}^{K-1}(\mathcal T_{a,t}^{*})^j(E_{a,t})
+(\mathcal T_{a,t}^{*})^K(I).
\tag{3}
\]

The last term is exactly the retained abort sector. Multiplying each leaf
operator by \(e^{-t C_w/2}\), including both the initial trial and subsequent
comparisons, gives a marked column \(W_t\). Direct expansion proves
\(N_K=W_t^\dagger W_t\). This is an operator identity on DATA, not a scalar
average computed in a chosen input state.

At zero mark,

\[
E_{a,0}+\mathcal T_{a,0}^{*}(I)=I,
\qquad R_{a,K}(0)=I,\qquad N_K(0)=I,\qquad DN_K(0)=0.
\tag{4}
\]

Thus the unmarked complete stopped column is an isometry for every finite
cap without iid assumptions. At nonzero mark, neither \(N_K\) nor its source
can be dropped or assumed to commute with the clean corner.

The exact field derivative follows the ordered recursion

\[
DR_{a,k}=DE_{a,t}+(D\mathcal T_{a,t}^{*})(R_{a,k-1})
+\mathcal T_{a,t}^{*}(DR_{a,k-1}),
\tag{5}
\]

followed by the product rule in the last line of (2). Moving charge fields
contribute \(D e^{-tc}=-t e^{-tc}Dc\); they are not excluded by notation.
Initial-state source \(D\rho\) must also be included when evaluating a scalar
\(\operatorname{Tr}(\rho N_K)\).

## 3. What a constant comparison charge does and does not remove

For unmarked CP maps, put

\[
L_a=\sum_b(c_b+\kappa_{ab})K_b^\dagger K_b,
\qquad
Q_{a,0}=0,\quad Q_{a,k}=L_a+\mathcal T_{a,0}^{*}(Q_{a,k-1}).
\]

Then the complete charged-effect operator is

\[
\mathcal C_K=-\partial_t N_K(0)
=\sum_a\left(c_a K_a^\dagger K_a+K_a^\dagger Q_{a,K}K_a\right).
\tag{6}
\]

For the number of trials, take one charge per trial and zero comparison
charge. Equivalently set \(Q_{a,0}=0\) and
\(Q_{a,k}=I+\mathcal T_{a,0}^{*}(Q_{a,k-1})\), then
\(\mathcal L_K=I+\sum_a K_a^\dagger Q_{a,K}K_a\).
All fixed per-comparison charges multiply the actual number of comparisons.
That number can vary with the field even when the price of each comparison
is fixed. The marked normalizer (2) retains this source.

For example, \(K_0=|0\rangle\langle0|\) and
\(K_1=|1\rangle\langle1|\), with any initial diagonal state whose two entries
are positive, produce two identical consecutive outcomes. There are exactly
two trials for every cap \(K\ge1\), not the iid value \(m+1=3\). The retained
label entropy is the entropy of the first label, not three times it.

Even eventual return needs an actual hypothesis for an uncapped process.
For \(K_0=|1\rangle\langle0|\), \(K_1=|1\rangle\langle1|\), and \(\rho=I/2\),
both first labels have probability \(1/2\), yet first label 0 never recurs.
This is a general-instrument control, not a statement about the original
full128 instrument. Equations (2)–(6) require no infinite-horizon assumption.

The complementary stationary-input occupation theorem is developed in
[`SEQUENTIAL_STATIONARY_OCCUPATION.md`](SEQUENTIAL_STATIONARY_OCCUPATION.md).
It recovers an additive-cost occupation identity under an actual stationary
input and return hypothesis, with a separate stationarity-defect source.
It does not import iid entropy or supply a physical input selection.

## 4. A concrete clean comparison word

For \(n\ge2\)-bit labels, preserve both labels. In \(n\) blank difference
bits compute their XOR using \(2n\) CNOT gates. Apply X to all difference
bits. Compute their AND into a flag using \(n-2\) chain ancillas and
\(2n-3\) Toffoli gates, including cleanup of that chain. Apply X to all
difference bits again and X once to the flag. Reverse the original XOR
computation using another \(2n\) CNOT gates.

This acts on blank scratch as

\[
|a,b,0_{\rm scratch},f\rangle\longmapsto
|a,b,0_{\rm scratch},f\mathbin\oplus[a\ne b]\rangle.
\tag{7}
\]

Every gate is a permutation on its full space, so the word is unitary for
arbitrary ancillas as well. The intended clean action (7) is checked on all
16,384 seven-bit label pairs and both initial flag values; the two-bit word
also has an explicit all-128-column census. Gate counts are

\[
4n\ {m CNOT}+(2n+1)\ X+(2n-3)\ {m Toffoli}=8n-2.
\tag{8}
\]

For full128 labels this is 28 CNOT, 15 X, and 11 Toffoli: 54 logical gates.
The physical price is
\(28c_{\rm CNOT}+15c_X+11c_{\rm Toffoli}\), with the actual factory and
controller contributions added. The integer 54 is a unit-logical-gate
convention, not a derivation of native physical price or clock time.

The output polarity matters. The 13-gate two-bit equality skeleton in the
iid appendix leaves MATCH equal to 1. It needs an extra X, making 14 gates,
to have the clean MATCH-zero convention used here. Retaining a MATCH-one
flag would make the proposed blank return vanish. Our word includes this X.

Scratch is clean at completion, but becomes nonblank during the X layers.
If the actual execution separately archives intermediate work states or
factory outcomes, those records must enter the return calculation. The
word alone does not prove that every native retained factory record is blank.
A stop-stage register can be uncomputed from the prefix-free retained label
array, which determines the first matching index or the cap. That decoder
has its own actual gate price and duration; neither is supplied for free.

## 5. The true corner and the open forward clock

Assume precisely the following return interface for the execution under
consideration: the allblank \(00\) leaf has clean comparison scratch,
MATCH-zero and ABORT-zero flags, a restored controller stage, and the actual
factory-work return amplitude already included in its specified Kraus word.
All other retained leaves are orthogonal to the initialized work vector.
No extra permanent nonempty-history bit is written. Under the ideal clean
comparison interface (7), with no additional return factor, the unique
work-clean operator is

\[
A_{00,t}=e^{-t C_{00}/2}B^2,
\qquad C_{00}=2c_0+\kappa_{00},
\qquad G_t=A_{00,t}^\dagger A_{00,t}=e^{-t C_{00}}B^4.
\tag{9}
\]

If a real factory has a nontrivial clean amplitude, replace (9) with that
actual ordered operator. If every leaf is orthogonal to initialized work,
the already-owned zero-corner result still applies. A different record
encoding does not repair that result without changing its actual corner.

Let the clean word take actual elapsed duration \(d_{00}\) and let the active
input/output window contain \(M\) counter positions. Use a larger padded
counter containing every shifted output, with no wrap on any admitted path.
The full output is retained. Only the complementary-return corner is tested
against the active window. Orthogonal histories then give

\[
W_{M,t}^\dagger W_{M,t}=I_M\otimes N_K(t),\qquad
A_{M,t}=(P_M S^{d_{00}}P_M)\otimes A_{00,t}.
\tag{10}
\]

Compressing the entire output of \(W\) to that same window would discard
histories and change the Gram; it is a different map. The direct rational
clock fixture tests this distinction explicitly.

Put \(r=\max(M-d_{00},0)\), \(d_H=\dim\mathrm{DATA}\), and retain the original
oldRIGHT spectator of dimension \(d_R=128\). For the normalized column
\(V_t=W_tN_K^{-1/2}\), the literal complementary-return determinant is

\[
\begin{aligned}
H_K(t)&=(1-\zeta)N_K(t)+\zeta G_t,\\
J_{M,K}(t)
&=d_R\{r[\log\det N_K(t)-\log\det H_K(t)]
 -(M-r)d_H\log(1-\zeta)\}.
\end{aligned}
\tag{11}
\]

The full unmarked instrument has \(N_K(0)=I\); its physical clean-return
feedback on this specified interface is therefore exactly the two-round
\(B^4\) feedback, independent of the larger stopping cap. All later leaves
remain in the complete isometry but are orthogonal to this particular
initialized-work corner. This does not equate their information or cost.

For nonnegative marked charges, the clean leaf is a positive summand in
the Gram. Equation (1) gives, for every finite cap,

\[
I\succeq N_K(t)\succeq G_t
\succeq e^{-t C_{00}}(2p-1)^4 I>0,\qquad t\ge0.
\tag{12}
\]

Thus the normalization and return in (11) are well defined uniformly in
the cap under the stated clean interface, even without commutation.

At fixed \(t,\zeta\), fixed admitted clock window, and fixed elapsed duration,

\[
\begin{aligned}
DJ_{M,K}
&=d_R r\operatorname{Tr}\left[N_K^{-1}DN_K
 -H_K^{-1}((1-\zeta)DN_K+\zeta DG_t)\right]\\
&=d_R r\zeta\operatorname{Tr}\left[
 N_K^{-1}G_tH_K^{-1}DN_K-H_K^{-1}DG_t\right].
\end{aligned}
\tag{13}
\]

The second expression avoids subtracting two order-one traces when
\(\zeta=2^{-20}\). It is an exact ordered matrix identity, not a commuting
approximation. For moving clean charge,

\[
DG_t=e^{-t C_{00}}\left[
\sum_{j=0}^{3}B^j(DB)B^{3-j}-t(DC_{00})B^4\right].
\tag{14}
\]

Moving clock/cut variables require their actual additional source. Common
right changes of coordinates in both Gram and corner cancel as in the
existing normalized determinant owner; a common scalar factor alone does
not create a new feedback source.

### Physical typing of the mark

At \(t=0\), the raw complete column is the stopped compiled isometry, subject
to the stated primitive/preparation/controller/clock interfaces. At \(t>0\),
\(W_t\) is its exact charge-generating column. Its polar normalization
\(W_tN_K^{-1/2}\) is a declared normalized marked Book diagnostic. It is not
automatically the output of the unchanged gates. A physical attenuation or
normalization construction must retain its own failures and work, and
recompute their true corner. Equations (11)–(14) do not identify this marked
diagnostic with the compulsory native master merely by definition.

### Retaining the actual preparation prefix

The stationary occupation application consumes the already-owned inverse-
square invariant DATA density from
[`A4D_NATIVE_PREPARATION_AND_GOLDEN_OFFSHELL_SOURCE_2026_10_21.md`](../../A4D_NATIVE_PREPARATION_AND_GOLDEN_OFFSHELL_SOURCE_2026_10_21.md).
A physical finite preparation by \(L\) unobserved original rounds has marginal
\(\Phi^L(\rho_0)\), while every earlier outcome and oldRIGHT remain globally
retained. Replacing that whole state by its reduced stationary marginal is
not an identity of coherent prepared inputs or Book return corners.

For example, retaining that prefix at the same initial blank cut in the
ideal clean interface of §5 gives the unique clean word \(0^L00\). At zero
mark its return and Gram are

\[
A_{\rm prefix,00}=B^{L+2},\qquad
G_{\rm prefix,00}=B^{2L+4},\qquad N_{\rm complete}=I.
\tag{15}
\]

The true prefix duration must enter (10). On an invertible positive-energy
carrier, \(0<B<I\), so the clean return tends to zero with long preparation,
even as the reduced DATA approaches its invariant density. A cut after the
preparation or a coherent inverse is a separately specified execution/cut
whose full source must be calculated. Equation (15) consumes the existing
fixed-round blank-return identity; it is not a new all-history certificate.
The finite preparation also retains the owned actual port-price boundary
term. Stationary occupation removes the reset premise in its additive
calculation; it does not remove this prefix from the Book03 master.

## 6. Decisive checks and remaining consuming premise

[`check_sequential_native_return.py`](check_sequential_native_return.py) and
[`SEQUENTIAL_RETURN_RESULT.json`](SEQUENTIAL_RETURN_RESULT.json) provide:

- Exact rational two- and three-label instruments, with a complete field
  jet; all stopped match/abort leaves at caps 1, 2, 3, and 5 independently
  reproduce the Gram and its first derivative.
- An exact noncommuting fixture in which freezing the actual normalizer
  changes the feedback source, and a direct retained-history/open-clock
  determinant check, including the incorrect output-compression control.
- The reset counterexample and the clean 54-gate comparison word, including
  all seven-bit label pairs and both flag values.
- The unchanged original full128 Fourier matrices and their actual boost
  jet at caps 1, 2, and 4. Mark-zero normalization, the clean corner,
  marked source, and sequential trial counts are evaluated. Independent
  five-point matrix-family differences test the analytic first source.

The checker selects only the unchanged matrix-constructor AST nodes from
the pinned source; this permits its NumPy/SciPy consumer without importing
unrelated SymPy certificates. The source blob and selected definitions are
recorded. It does not claim that the older whole suite was rerun. Exact
rational checks and floating-point original-block checks have separate
statuses. The logical-charge/clock example uses \(c_b=1+(b\bmod2)\),
\(\kappa=54\), and \(M=d_{00}+1=57\); this is a declared component/convention,
not the complete physical cost of all query, stage, and factory operations.

At the literal original boost \(\theta=0.08,\nu=0.6\), the unmarked feedback
source for one overlapping clock return is
\(-6.853707110464\cdot10^{-6}\) at all three caps. For the declared mark
\(t=0.02\), the cap-two full source is
\(-2.415820548363\cdot10^{-6}\), while freezing its normalizer gives
\(-7.045923091317\cdot10^{-6}\). The five-point discrepancy from the full
analytic source is below \(4\cdot10^{-15}\) in the six tested cases. These
are floating-point diagnostic values, not interval enclosures. For fixed
maximally mixed initial DATA, cap two has mean trial count
\(2.041819022446\) and derivative \(-0.003481387471\); a constant comparison
price consequently has a nonzero complete stopping source on this input.
The exact stationary-input application uses its own actual moving density,
not this fixed mixed diagnostic state.

This replaces a reset assumption with the actual finite sequential
operator calculation. The remaining consuming premise is specific: join
the admitted full field/preparation map, native heat operator, actual
retained factory/stage/clock corner, and complete price to the same Book03
variation. In particular, the clean comparator word does not fix the heat
term or make independent inputs stationary, and the marked diagnostic does
not select its own physical implementation. No BOOK, claim, lifecycle,
`positive_gr`, raw216 or full-GR acceptance state is changed.
