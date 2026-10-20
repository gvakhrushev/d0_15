# The same native history: full return, marked price and prospective stopping

20 October 2026. Bounded composition for existing PR #334 and
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`; input commit
`acfe3e19ecda5f2dbc678ec52e2f7cd0f3e639a1`.

**Parent use.** The original full128 history already gives the HJR feedback
operator on the full data carrier. A physically filled Fock preparation is
not necessary for this operator identity or for Book03's closed-loop trace.
The new composition below carries the actual port-cost marker through that
SAME return, including every outcome, and applies it on the exact physical
coframe-scale family used by the primary GR comparison. It also computes a
prospective event-stopping task on that family. These maps locate the
remaining choice of complete Book history valuation and task; they do not
select a replacement physical action or declare the full Book logdet invalid.

## 1. Owned inputs and a positive return identity

Use the original all128 Kraus rows in
[`paid_port_history.md`](../../d0_same_history_price_composition_2026-10-20/paid_port_history.md):

\[
K_{0k}=\delta_{k0}I-2p^2N_k^*A,\qquad
K_{1k}=-2p\sqrt p\,N_k^*A,
\quad p+p^2=1,
\]
\[
A=hD/16=A^*,\quad N_0=A,\quad\sum_kN_kN_k^*=I,
\quad \epsilon=p^2h^2/64,\quad\alpha=\epsilon/2.
\tag{1}
\]

The single blank outcome means **port0, label0, coefficient0**. Its operator
is \(B=I-\alpha\Delta\), where \(\Delta=D^2\). Its complement includes the
blank-label port1 and all other 126 outcomes. In particular, neither EXIT
nor the paid port1 is substituted for this complement.

Let \(V_n\colon H\otimes R\to H\otimes R\otimes T_n\) be the actual
retained-history isometry

\[
V_n=\sum_{\omega\in\{1,\ldots,128\}^n}
 (K_\omega\otimes I_R)\otimes|\omega\rangle,
\qquad T_n=(\mathbb C^{128})^{\otimes n},\quad \dim R=128.
\tag{2}
\]

All oldRIGHT columns and all fresh records remain. Set

\[
P_0=I_{H\otimes R}\otimes|0^n\rangle\langle0^n|,
\qquad Q_0=I-P_0.
\]

Completeness and the literal blank word give

\[
V_n^*V_n=I,\qquad
P_0V_n=(B^n\otimes I_R)\otimes|0^n\rangle,
\]
\[
\boxed{F_n=V_n^*Q_0V_n=(I-B^{2n})\otimes I_R.}
\tag{3}
\]

For the original full unitary implementation \(W_n\), with the original
blank-tape injection \(i\), \(V_n=W_ni\). Thus (3) is the active block of
the Book feedback \(P_0W_n^*Q_0W_nP_0\), not a new fitted effect.
The Gram adjoint in this formula does not by itself charge a second executed
inverse; any physically executed return operation retains its actual charge.

This positive identity is already owned by the
[v8 construction, §§3–4](../inputs/02_REGISTRY/research/sources/d0_record_generated_heat_v8_2026-10-14/RESULT.md)
and the [full-Lorentz owner, §2](../inputs/02_REGISTRY/research/A4D_NATIVE_FULL_LORENTZ_ADJOINT_SOURCE.md).
Its use here fixes the common clock, rather than reproving a missing theorem:

\[
n=128L^2=m/2,\quad m=256L^2,\quad
\alpha=p^2h^2/128,\quad n\epsilon=m\alpha=\beta=2p^2.
\tag{4}
\]

Consequently the **full** Book feedback component is exactly

\[
-\log\det_{H\otimes R}(I-zF_n)
=-128\operatorname{Tr}_H\log[(1-z)I+zB^m].
\tag{5}
\]

There is no claim that every data mode is simultaneously physically occupied.
The active cut itself contains all of \(H\otimes R\). Book03 §03.3.2 allows
a closed-history trace over that carrier. Its native admission and complete
valuation must be established as such; the Slater probability realization is
a separate sufficient interpretation, not a necessity for (5).

For fixed \(n,h,p,z\), all noncommuting field variations are retained:

\[
dF_n=-\sum_{j=0}^{m-1}B^j(dB)B^{m-1-j}\otimes I_R,
\quad dB=-\alpha\,d\Delta,
\]
\[
dJ=128z\operatorname{Tr}_H[(I-z(I-B^m))^{-1}d(I-B^m)].
\tag{6}
\]

Moving \(z,\alpha\), observer pairing or cut requires their derivatives.
The fixed chart here includes the full observer whitening of the owned
instrument. Integer \(n\) changes compare different programmes, not a
smooth field derivative.

## 2. Open and closed boundaries are exact, different contractions

The owned [clock-source identity](../../d0_same_history_price_composition_2026-10-20/clock_source_reduction.md)
applied to the actual cost-tilted CP map gives a nilpotent clock \(\mathcal A_t\)
with the \(n\) successive transfers. An initial density column \(r_\rho\)
and final trace row \(\ell\) give

\[
Z_n(t)=\ell(I-\mathcal A_t)^{-1}r_\rho,
\quad\det(I-\mathcal A_t-u r_\rho\ell)=1-uZ_n(t).
\tag{7}
\]

The determinant lemma with matrix-valued boundaries \(R,L\) instead gives

\[
\det(I-\mathcal A-RL)
=\det(I-\mathcal A)\det(I-L(I-\mathcal A)^{-1}R).
\tag{8}
\]

Choosing the complete return boundary for (3) yields (5). Choosing a
prepared scalar boundary yields one prepared return. Equation (8) is an
identity of generating objects, not a free physical reset or a proof that
the Book price of these different closures is identical.
For (5), the clock and matrix boundary are those of the underlying
amplitude/isometry return (3); they are not the Liouville clock
\(\mathcal A_t\) of (7). No equality of these two transfer carriers is assumed.

In particular, replacing the full return by a chosen prepared expectation
is not a representation change preserving (5). On an invariant decomposition

\[
H=S\oplus S^\perp,\qquad F_n=F_S\oplus F_{S^\perp},
\]

the exact source omitted by such a compression is

\[
dJ-dJ_S=128z\operatorname{Tr}_{S^\perp}
 [(I-zF_{S^\perp})^{-1}dF_{S^\perp}].
\tag{9}
\]

It vanishes only under an actual condition on the complementary source.
This states what a source-preserving task/representation map must retain;
it does not deny the original full closed ensemble.

## 3. NEW: the original cost marker through the same full return

The actual known port code has \(C_{\rm port}(\omega)=n+N_1(\omega)\),
so \(n\le C_{\rm port}\le2n\). It does not include all unknown controller,
label, preparation, archive or work charges. With analysis parameter

\[
x=e^{-t}>0,\qquad E_t=\sum_\omega x^{C_{\rm port}(\omega)}
 |\omega\rangle\langle\omega|,
\]

define the **marked generating effect**, without asserting a physical
filter or a new action,

\[
F_{n,t}=V_n^*Q_0E_tQ_0V_n.
\]

The marker commutes with the fixed blank cut. The one blank word has exactly
cost \(n\). Expansion into the full retained record therefore proves

\[
\boxed{
 F_{n,t}=
 \big[(\Phi_t^*)^n(I)-x^n B^{2n}\big]\otimes I_R,
}\tag{10}
\]

where the **actual all128** transfer, not a scalar clock substitute, is

\[
\Phi_t(X)=x\left[X+\epsilon\left((p^2+px)\mathcal T(DXD)
 -\tfrac12\{\Delta,X\}\right)\right],
\quad \mathcal T(X)=\sum_kN_k^*XN_k.
\tag{11}
\]

Thus \(F_{n,0}=F_n\) exactly. At fixed \(t\), put \(A_t=\Phi_t^*\). Then

\[
d[(A_t)^n(I)]=\sum_{j=0}^{n-1}
 A_t^j\big[(dA_t)A_t^{n-1-j}(I)\big],
\]
\[
dF_{n,t}=\left[d(A_t^n(I))-x^n d(B^{2n})\right]\otimes I_R.
\tag{12}
\]

All field derivatives of \(D,N_k,\epsilon\) in (11) are included as in
the owned paid-port source. If \(t\) moves, differentiate both \(A_t\) and
\(x^n\); the latter contributes \(-n x^nB^{2n}dt\) to \(d(x^n B^{2n})\).
Whenever \(I-zF_{n,t}>0\), the marked closed generating source is

\[
dJ_t=128\operatorname{Tr}_H
 [(I-zF_{n,t}^{H})^{-1}(z\,dF_{n,t}^{H}+F_{n,t}^{H}\,dz)].
\tag{13}
\]

Here \(F_{n,t}^{H}\) is the data factor of (10). Formula (13) is not the
logdet of the scalar open partition (7).

The exact first cost insertion also has a direct positive meaning:

\[
-\left.\partial_tF_{n,t}^{H}\right|_0
=C_{n,\mathrm{exit}}
=\sum_{\omega\ne0^n}C_{\rm port}(\omega)K_\omega^*K_\omega,
\]
\[
C_{n,\mathrm{exit}}=C_n^{\mathrm{op}}-nB^{2n},
\quad C_n^{\mathrm{op}}=nI+p\epsilon\sum_{j=0}^{n-1}(\Phi^*)^j(\Delta),
\]
\[
\boxed{nF_n^H\le C_{n,\mathrm{exit}}\le2nF_n^H.}
\tag{14}
\]

Thus closed-return marking does not make the executed clock disappear.
For example, \(-\partial_tJ_t|_0=128z\operatorname{Tr}[(I-zF_n^H)^{-1}
C_{n,\mathrm{exit}}]\). Both the baseline \(n\) and the extra return-port
charge are present.

This differs from the earlier prepared-price echo
\(I-(V^*\sqrt{I-E}V)^2=V^*EV+L\). That construction introduced a new
marker coupling, then compressed its output against the prepared work cut;
its work-complement \(L\ge0\) remains real. Here the physical fixed cut is
the **original nonblank tape**, and \(E_t\) is merely the diagonal cost
generating mark on that tape. At \(t=0\) there is no added marker gate,
so the original identity (3) has no such extra term. The two results agree
on their respective operator definitions.

## 4. Application to the exact common physical coframe scale

Consume the [same-carrier scale theorem](../inputs/02_REGISTRY/research/A4D_EXACT_GR_COMMON_CARRIER_HJR_SCALE_SOURCE_GAP_2026_10_20.md).
For \(h=1/L\), \(v_r=h\sqrt\rho\,e_r\), identity proper links and the
constant whitened observer,

\[
\Delta(\rho,k)=\lambda_k I_{16},\quad
\lambda_k=\rho\mu_L(k),\quad
\mu_L(k)=\sum_r(2-2\cos(2\pi k_r/L)),
\]
\[
0\le\mu_L\le16,\quad\sum_k\mu_L(k)=8L^4.
\tag{15}
\]

Every original Kraus row preserves momentum. Consequently
\(\Delta\) commutes with every row, not only with the summed channel. On
each whole CAR16 block, (11) has dual trace multiplier

\[
g_{n,t}(\lambda)=x^n a_x(\lambda)^n,
\quad a_x(\lambda)=1+p\epsilon\lambda(x-1),
\quad b(\lambda)=1-\epsilon\lambda/2.
\]

Therefore the **entire** same-instrument marked return is diagonal by
momentum with exact scalar

\[
\boxed{f_{n,t}(\lambda)=x^n[a_x(\lambda)^n-b(\lambda)^{2n}].}
\tag{16}
\]

With the original clock (4), its genuine scale derivative is

\[
\boxed{\partial_\rho f_{n,t}(\rho\mu)
=\beta\mu x^n\left[b^{m-1}-p(1-x)a_x^{n-1}\right].}
\tag{17}
\]

This gives a complete full-carrier source with no dropped band:

\[
\partial_\rho J_t
=2048z\beta x^n\sum_k
\frac{\mu_L(k)[b_k^{m-1}-p(1-x)a_{x,k}^{n-1}]}
 {1-zx^n(a_{x,k}^n-b_k^m)}.
\tag{18}
\]

At \(t=0\), (18) is exactly the positive HJR feedback part of the owned
common-carrier scale source. The fixed oldRIGHT multiplicity 128 and CAR16
multiplicity 16 have not become 128 physical copies or one normalized
prepared trace. The heat and Riesz terms remain their separate owned terms.

For any fixed \(t>0\), \(x<1\). On each sufficiently fine member of the
strict chart, \(0\le a_x,b\le1\). More generally, (10) gives

\[
x^{2n}F_n^H\le F_{n,t}^{H}\le x^nF_n^H\le x^nI.
\tag{19}
\]

Combining (15), (17) and (19), for the original fixed \(0<z<1\),

\[
\boxed{L^{-4}|\partial_\rho J_t|
\le\frac{16384z\beta[1+p(1-x)]x^n}{1-zx^n}
\longrightarrow0.}
\tag{20}
\]

Thus the **cost-marked** return cannot be substituted for the unmarked
HJR return while silently keeping its extensive scale source. This is an
exact statement about the same operator and actual port marker, not a
conclusion that the full Book action must use the marked return as its law.

The allblank heat marker is instead \(x^nB^m\). Its fixed-\(t,n\) logarithmic
heat source is unchanged because \(\log\operatorname{Tr}(x^nB^m)
=n\log x+\log\operatorname{Tr}B^m\). This illustrates why removing a
normalization common to a fixed-length open experiment need not preserve
a closed-loop source: different loop repetitions contain different numbers
of complete \(n\)-round words, so the same constant changes their fugacity.

## 5. What (20) does and does not require of complete Info

The original \(K_\omega\) already contains Golden amplitudes. Equation
(10) is a generating mark that reads their known port cost. It does not
assert that the actual physical law must multiply those amplitudes by the
same price again. Book03 uses an algebra-valued amplitude sum before its
quadratic readout; identifying its scalar weight with a native probability,
an absolute normalized-branch amplitude, or an additional multiplier of
\(K_\omega\psi\) are different maps.
The companion [Book source binding](../book_source/BOOK_SOURCE_BINDING.md)
spells out those maps on the very same nonblank Golden port pair; its
normalization factor must be carried through the closed boundary here.

For example, **if** a proposed complete valuation is an additional
nonnegative outcome weight \(w_\omega=p^{C_\omega-I_\omega}\) in the
return Gram, preserving the same unmarked return requires

\[
\sum_{\omega\ne0^n}(w_\omega-1)K_\omega^*K_\omega=0.
\tag{21}
\]

Equation (21), including its field derivative, is the exact missing
transport condition for that specified interpretation. Uniformly
\(I_\omega\le n-a\) with \(a>0\), and \(C_\omega\ge C_{\rm port}\ge n\),
would imply \(F_{\rm net}\le p^aF_n^H\ne F_n^H\) whenever the return is
nonzero. Thus that interpretation needs at least some supported information
gain at the executed-clock scale, or a different explicitly derived cycle
valuation. A Shannon entropy of the observed tape is not silently used as
that gain. If the weight multiplies amplitudes, the Gram weight is its
square; the same transport test uses \(w_\omega^2\), not \(w_\omega\).

For an actual admitted complete code, (21) might follow from a Book memory
cocycle or a derived normalization. No such formula is proved here. Nor
does this restriction establish physical nonuniqueness: it identifies the
application required by this specific same-history representation.

## 6. The actual fixed preparation: sparse records without deleting outcomes

The same scale owner uses the entire lowest positive momentum shell
\(S_L\subset H\), dimension \(8\cdot16=128\), with the unchanged oldRIGHT
Gram \(I_{128}/128\). Its eigenvalue is

\[
\lambda_1=\rho\mu_{1,L},\quad
\mu_{1,L}=2-2\cos(2\pi/L)=O(h^2).
\]

The Riesz subspace and a fixed purification do not move under pure scale.
Every conditional Kraus outcome stays in this shell. Both the blank effect
and the port1 effect are scalar there:

\[
q_0=(1-\epsilon\lambda_1/2)^2,\quad
e=1-q_0,\quad r=p\epsilon\lambda_1.
\tag{22}
\]

Thus blank/nonblank flags are IID Bernoulli((e)); the port bits are
separately IID Bernoulli((r)). This does not assert that fine labels or
the conditional quantum states are independent. For fixed \(n=m/2\),

\[
\mathbb E C_{\rm port}=n(1+r)=n+p\beta\rho\mu_{1,L},
\quad\partial_\rho\mathbb E C_{\rm port}=p\beta\mu_{1,L}=O(h^2),
\]
\[
\delta_n=1-q_0^n=O(h^2),\quad e=O(h^4).
\tag{23}
\]

Chain entropy, conditional on the actual preceding fine record, gives the
useful sparse bound

\[
H(\text{entire pointer tape})
\le nH_2(e)+ne\log127=O(h^2\log(1/h)).
\tag{24}
\]

No fine outcome is discarded. This is not the loose bound \(n\log128\).
For the coherent unmeasured record, the final pure state has data shell128
and oldRIGHT128 on its other side, hence its record density has rank at
most \(128^2\). The allblank record expectation is \(q_0^n=1-\delta_n\),
so its largest eigenvalue is at least that number. Consequently

\[
S(\text{coherent record})
\le H_2(\delta_n)+\delta_n\log(128^2-1)
=O(h^2\log(1/h)).
\tag{25}
\]

These are entropy **values**. They are not first-source bounds and are
not definitions of Book Info. The prepared low-shell facts do not refute
the full closed trace (5): the latter uses a different, explicitly full
return boundary. Conversely they cannot justify compressing that boundary
without the complementary source (9), which is nonzero and extensive on
this family.

## 7. A constructive prospective stopping task on the SAME instrument

Suppose a complete task explicitly requires the first nonblank outcome of
these original identical rounds. Continue retaining every record, and let

\[
T=\min\{j\ge1:\omega_j\ne0\}.
\]

On the shell (22), every preceding outcome is blank and leaves the
normalized state unchanged. The exact first-event law and known price are

\[
\Pr(T=j)=q_0^{j-1}e,\qquad
\mathbb E T=1/e,
\]
\[
\boxed{\mathbb E C_{{\rm port},T}=(1+r)/e.}
\tag{26}
\]

To prove the price formula, every nonterminal port is 0, and the final
port1 probability is \(r/e\). Thus \(C_{{\rm port},T}=T+\mathbf1_{
\text{terminal port1}}\). All failures to stop at earlier rounds remain
recorded. With the actual physical coframe scaling,

\[
\mathbb E T\sim\frac{16}{p^2\pi^2\rho}\,L^4,
\qquad
\mathbb E C_{{\rm port},T}\sim\frac{16}{p^2\pi^2\rho}\,L^4.
\tag{27}
\]

This provides a concrete extensive execution cost for one prepared
carrier without assuming full band occupation. It is NOT an identification
with the HJR source, an admitted infinite protocol, or a derivation that
this stopping task is physically compulsory.

Every actual check may instead have a finite horizon. If the specified
task is to see an event by that horizon with failure at most \(\eta\in(0,1)\),
the unique least horizon among **these fixed-round repetition programmes** is

\[
N_\eta=\left\lceil\frac{\log\eta}{\log q_0}\right\rceil
=\Theta(L^4)
\tag{28}
\]

for fixed \(\eta\). This is a prospective monotonicity certificate for a
specified task, not an enumeration of all possible native controls or a
claim of global D_min optimality. The original HJR horizon \(n=128L^2\)
has event probability \(O(h^2)\), so cannot meet this fixed-success task
at fine meshes. Independent duplicate checks repeat the paid task; their
mere existence does not determine its event, error criterion or horizon.

The fully finite version, stopped at the event or the fixed cap \(N\), is
also exact:

\[
\mathbb E C_{{\rm port},T\wedge N}
=(1+r)\sum_{j=0}^{N-1}q_0^j
=\frac{(1+r)(1-q_0^N)}{e}.
\tag{29}
\]

Its genuine field source differentiates (29) at fixed \(N\); varying the
integer horizon or the task's failure criterion is a different comparison.
For the unbounded expectation used only to state (27), this derivative has
the explicit asymptotic
\(L^{-4}\partial_\rho\mathbb E C_{{\rm port},T}
\to-16/(p^2\pi^2\rho^2)\).
No equality with the HJR coefficient is asserted. The finite formula (29)
keeps both the earlier no-event records and the capped failure record.

Book03 §03.23.2 forces distinct write/read roles. Book06 §06.6.B fixes an
inward distinguishability ladder cutoff from the observer floor. Neither
quoted rule identifies that inward depth with (28), with \(m/2\), or with
the repetition index of the closed return expansion. That native map must
be supplied; choosing it to fit the gravity source would be circular.

## 8. Exact parent substitution and remaining premise

The positive operator map in (3)–(6) is an owned input and is valid on the
whole original data/oldRIGHT carrier. It prevents rejecting HJR merely
because the actual preparation occupies one shell. The new (10)–(18)
compose that map with the actual known full-tape port-price transform,
including its noncommuting source and its common-family scale source.
Equations (26)–(28) show concretely how a different, explicitly required
future distinction changes the paid clock scale before execution.

The missing parent is now stated on one set of objects: derive the
original native admission and complete Book valuation of this same
\(V_n,P_0,Q_0\), with all record/controller/preparation/work prices and
the correct amplitude/Info normalization, and derive the task/clock
that D_min optimizes. Then its full first source must be compared to the
configured all40+2 GR family. Bare HJR fails the already owned flat source
test; no term here is fitted to cancel that mismatch. Bellman/no-detour
can be consumed after its complete task and objective are identified.
The existing exact geometry and verification foundations need no restart.

The local checker is a bounded new composition check, not a replay of the
old suite. It evaluates the marked return and its genuine scale jet from
all128 original CAR16 Kraus rows at two rounds; checks the two-round
all-record cost insertion, and rejects erasing the recycling term or
using the wrong blank/port cut. The all-\(n,L\) statements above are
proved by composition and the explicit inequalities, not extrapolated
from those two rounds.
