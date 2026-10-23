# Complete Perron transfer and the finite marked price source

20 October 2026. Existing draft PR #334,
EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE, native-programme-v1.

**Result.** The owned full 718-edge scalar/CAR instrument has an exact
completely positive Perron similarity. Summing every flag at a fixed
transition depth removes conditional quantum probabilities from the raw
scalar partition, even when the preparation moves. The full paid source
is preserved by a finite marked generating function: its derivative
retains the conditional record, actual Cost/Info, moving endpoint and
stopping clock. Applied to the existing complete compiler ledger, this
gives an explicit internal baseline covector \(DB\). It does not identify
an unmarked pressure, a chosen entropy cut and the compulsory Book price.

## 1. Input and scope

Use the original directed \(K(9,11,13)\) support: 33 vertices and
\(2(9\cdot11+9\cdot13+11\cdot13)=718\) directed edges. Let
\(K(y)\) be strictly positive on those edges, with
\[
Kr=\lambda r,\qquad r_u>0,\qquad \sum_u r_u=1,\qquad
P_{uv}=\frac{K_{uv}r_v}{\lambda r_u}.
\tag{1}
\]
The actual one-sided initial scene law is \(r\), not the stationary
distribution. No uniformization of the Perron weights is made.

On each edge use the complete finite instrument already supplied by the
full scalar/CAR owner:
\[
\sum_b M_{uv,b}^{\dagger}M_{uv,b}=I.
\tag{2}
\]
Its Julia example has \(M_G=p\Lambda(L_{uv})\) and
\(M_B=(I-p^2\Lambda(L_{uv})^\dagger\Lambda(L_{uv}))^{1/2}\),
with \(p=\varphi^{-1}\) on the owner's strict contraction chart.
Every failure, edge label and fresh flag is retained. Operators act as
the identity on oldRIGHT. The proofs below allow a general complete
instrument, and do not replace the actual instrument by its good branch.

The original owner calls this a native-type scalar/CAR lift, not a
gate-by-gate realization of the literal original full128 programme.
It also distinguishes scene edges from spacetime Role links. These
qualifications remain. The new transfer identities supply no missing
physical address map, gate price or Info law.

## 2. Full completely positive Perron similarity

For a fixed finite active fibre, write an observable as \(A=(A_u)_u\).
Define
\[
(\mathcal K^*A)_u
 =\sum_v K_{uv}\sum_b M_{uv,b}^{\dagger}A_vM_{uv,b},
\qquad
(S_rA)_u=r_uA_u.
\]
Direct substitution of (1) gives the operator identity
\[
\boxed{S_r^{-1}\mathcal K^*S_r=\lambda\mathcal T^*},
\qquad
(\mathcal T^*A)_u
 =\sum_vP_{uv}\sum_bM_{uv,b}^{\dagger}A_vM_{uv,b}.
\tag{3}
\]
This is a similarity of the complete transfer, including both Julia
outcomes, not a comparison of a single matrix element or trace.

For each \(u\), the stacked map
\[
V_u\psi=\bigoplus_{v,b}\sqrt{P_{uv}}\,M_{uv,b}\psi
\]
is an isometry by (2). Hence
\((\mathcal T^*A)_u=V_u^\dagger(\bigoplus_{v,b}A_v)V_u\),
so \(\|\mathcal T^*A\|\le\max_v\|A_v\|\).
Also \(\mathcal T^*\mathbf I=\mathbf I\). Its spectral radius is therefore
exactly one, and similarity proves
\[
\boxed{\operatorname{spr}(\mathcal K^*)=\lambda(K).}
\tag{4}
\]
This requires neither a stationary CAR density nor a frozen preparation.
It holds pointwise for moving complete instruments and for non-symmetric
\(K\).

The finite active transfer is not asserted to be a faithful representation
of the algebra of all unbounded histories. Fresh archives can continue to
grow. Taking their complete trace to compute a statistic is not a physical
erasure or permission to omit their prices. The finite path identities
below also hold for successive instruments with different finite work
spaces; a spectral radius is asserted only for the fixed-fibre
endomorphism in (3).

## 3. Finite raw partition with moving preparation

Fix a transition depth \(n\). For a scalar path
\(\gamma=(u_0,\ldots,u_n)\), let
\[
W_K(\gamma)=\prod_{j<n}K_{u_ju_{j+1}},\qquad
c_y(\mathbf b\mid\gamma)
 =\operatorname{Tr}\bigl(
 M_{\gamma,\mathbf b}\sigma_{u_0}
 M_{\gamma,\mathbf b}^{\dagger}\bigr).
\]
Here \(\sigma_u(y)\) is any normalized conditional full input density.
It may be correlated with a protected oldRIGHT and may move inside its
actual admissible preparation domain. Completeness in chronological
order gives \(\sum_{\mathbf b}c_y(\mathbf b\mid\gamma)=1\).

For any normalized starting weights \(\mu(y)\), the complete raw
partition and its derivative are consequently
\[
\boxed{\widehat Z_n^\mu
 =\sum_{\gamma,\mathbf b}\mu_{u_0}W_K(\gamma)
       c_y(\mathbf b\mid\gamma)
 =\mu^\top K^n\mathbf1,}
\tag{5}
\]
\[
D\widehat Z_n^\mu
 =(D\mu)^\top K^n\mathbf1
 +\sum_{j=0}^{n-1}\mu^\top K^j(DK)K^{n-1-j}\mathbf1.
\tag{6}
\]
All \(DM\) and \(D\sigma\) contributions cancel through the complete
trace-preserving identity, not by deleting failed branches or fixing
the preparation. With held \(K,\mu\), the unmarked raw statistic has no
conditional-instrument or normalized-input source, to every order for
which the data are differentiable.

**Fixed depth is essential.** A flag-dependent stopping rule weights
different numbers of \(K\)-transitions; then (5) cannot be substituted
with one common \(n\). The next section keeps the actual stopped clock.

## 4. Marking the actual price preserves the complete finite source

Use now the owned initial scene law \(r\). Telescoping (1) gives the
actual normalized full event law
\[
q_y(\gamma,\mathbf b)
 =r_{u_0}\prod_{j<n}P_{u_ju_{j+1}}\,
       c_y(\mathbf b\mid\gamma)
 =\lambda^{-n}r_{u_n}W_K(\gamma)c_y(\mathbf b\mid\gamma).
\tag{7}
\]
Let \(s_\omega(y)=C_\omega(y)-I_\omega(y)\) be the **actual supplied**
complete leaf price, with every paid preparation, reference, clock and
work term assigned once. It can depend explicitly on the preparation and
record law. The following real variable \(t\) is an analytic mark, not a
new physical gate, price or freely chosen Info table:
\[
Z_n(t;y)=
 \sum_{\omega=(\gamma,\mathbf b)}
 r_{u_n}W_K(\gamma)c_y(\mathbf b\mid\gamma)
 \varphi^{-t s_\omega(y)}.
\]
At \(t=0\), completeness and \(K^nr=\lambda^nr\) give
\(Z_n(0;y)=\lambda^n\). Thus
\[
\boxed{
-\left.\partial_t\log_\varphi Z_n(t;y)\right|_{t=0}
 =\mathbb E_{q_y}s,\qquad
D\mathbb E_qs
 =\mathbb E_q[Ds]+\mathbb E_q[s\,D\log q].
}
\tag{8}
\]
Unsubscripted log in the score formula is the natural logarithm.
The complete score is
\[
D\log q_\omega
 =D\log c_y(\mathbf b\mid\gamma)
 +\sum_{j<n}D\log K_{u_ju_{j+1}}
 +D\log r_{u_n}-nD\log\lambda.
\tag{9}
\]
It has mean zero. Equations (8)-(9) retain the moving final preparation,
conditional quantum record and actual Cost/Info derivative. In
particular \(\mathbb E_q[Ds]\) alone is generally not the derivative
of the mean price.

For an actually stopped complete record, let \(\tau(\omega)\le n_{\max}\)
be its number of counted \(K\)-transitions. All aborts and cap outcomes
are retained. Whenever its actual law has the same chronological
factorization,
\[
q_\omega=\lambda^{-\tau(\omega)}
 r_{u_{\tau(\omega)}}W_K(\gamma)c_y(\omega\mid\gamma),
\]
use
\[
Z_{\rm stop}(t;y)=
 \sum_\omega
 \lambda^{-\tau(\omega)}r_{u_{\tau(\omega)}}W_K(\gamma)
 c_y(\omega\mid\gamma)\varphi^{-t s_\omega(y)}.
\tag{10}
\]
Then \(Z_{\rm stop}(0)=1\), (8) still holds, and the last term of (9) is
\(-\tau(\omega)D\log\lambda\). Pulling one common
\(\lambda^{-n_{\max}}\) outside this sum is incorrect. The counted scene
transition length is not automatically the compiler's full primitive
tick count; that real cost remains in \(C_\omega\). Caps and literal
words are discrete held data when taking a differential.

These formulas use the actual complete positive record law. They do not
replace a coherent algebra-valued Book sum by a measured law. On a fixed
positive support they follow by differentiating finite sums. At branches
whose probabilities vanish, the formulas apply only where the actual
mean has the required differentiable extension; no general smoothness
of rank-birth entropy is assumed.

For the already-owned residual decomposition
\(s_\omega=s_c+\delta_s1_M+\xi_\omega\), let
\[
R=\sum_\omega \xi_\omega A_\omega^\dagger A_\omega
\]
for the full normalized instrument and prepared density \(\rho\).
Marking \(\xi\) in (8) gives exactly
\[
\mathbb E_q\xi=\operatorname{Tr}(\rho R),\qquad
D\mathbb E_q\xi
 =\operatorname{Tr}((D\rho)R)+\operatorname{Tr}(\rho\,DR).
\tag{11}
\]
Here \(DR\) includes the derivatives of \(\xi\) and of the actual Kraus
operators. Thus the marked identity preserves the remaining absolute
residual when its true prices are supplied. It does not set it to zero.
A genuine endpoint coboundary likewise retains its finite initial/final
expectation; stationary endpoint cancellation cannot be substituted for
the one-sided finite execution.

## 5. The actual complete compiler baseline and its source

Consume the existing complete all-launch compiler ledger. For one
independently implemented local block, let \(R_{\rm pre}\) be the whole
preparation transcript; let \(\alpha\) be bank readiness. Let \(T\)
contain every reached-stage retry, X sign, abort location, correction,
clock and retained work label; let \(\beta\) be stage readiness,
\(H_T=H_\varphi(T)\), and \(\mu\) the actual expected paid stage cost.
A ready click of ideal probability \(q\) continues; all other outcomes
stop. At cap \(N\ge1\), set
\[
E_N(x)=\sum_{k=0}^{N-1}x^k,\qquad x=\beta q.
\]
On the owner's complete CQ cut and pure-input/reference convention,
the exact ledger is
\[
C_{\rm full}=C_{\rm pre}+\alpha\mu E_N(x),\qquad
H_{\rm full}=H_{\rm pre}+\alpha[H_T+\beta h_\varphi(q)]E_N(x).
\tag{12}
\]
No primitive tick, failure or aborted prefix is removed by (12).

For the fixed original vacuum query, write
\[
p=\varphi^{-1},\quad z_0=2^{-20},\quad L=4p^3,\quad
Q_\star=1-z_0L,\quad
R_\star=1-z_0L(1+p^6),\quad q_\star=1-Q_\star R_\star.
\]
The symbols \(R_\star\) and \(z_0\) are fixed query constants, distinct
from the operator \(R\) in (11) and from internal parameters \(\zeta\).
The baseline at zero geometric query is
\[
\boxed{
B_{\rm CQ}(\zeta)
 =C_{\rm pre}-H_{\rm pre}
 +\alpha[\mu-H_T-\beta h_\star]E_N(\beta q_\star),
\qquad h_\star=h_\varphi(q_\star).
}
\tag{13}
\]
All quantities on the right come from actual finite transcript laws and
paid costs. They are not freely chosen counterterms.

Put \(a=\mu-H_T-\beta h_\star\),
\(x_\star=\beta q_\star\), \(E=E_N(x_\star)\).
Holding the original query constants and discrete cap, the complete
internal differential is
\[
\boxed{
\begin{aligned}
DB_{\rm CQ}={}&D(C_{\rm pre}-H_{\rm pre})
 +aE\,D\alpha+\alpha E(D\mu-DH_T)\\
 &+\alpha[q_\star a E_N'(x_\star)-h_\star E]D\beta .
\end{aligned}}
\tag{14}
\]
If the actual variation also changes the baseline report probability,
add
\[
\alpha\beta[aE_N'(x_\star)-h_\varphi'(q_\star)E]Dq_\star.
\tag{15}
\]
Equations (14)-(15) follow directly by the product rule in (12).
For independent block implementations they are summed with the original
integer multiplicities. A shared prefix is counted once; correlated
factories require their actual conditional entropy law.

There is a useful precise preparation qualification. If a retained input
sector has data-independent complete branch effects
\(A_\omega^\dagger A_\omega=q_\omega I\), all its conditional maps are
scaled isometries. Its normalized logical state cannot change the record
law. On the original pure full-input/reference convention, moving that
state inside the fixed-oldRIGHT domain therefore leaves the baseline
unchanged. This is not a proof that arbitrary variations of the
detector's query preparation have scalar effects. Those genuine
preparation variations must still be evaluated in (14)-(15).
Under those same scalar-effect hypotheses, for a mixed full input the
complete CQ entropy additionally contains
\(S_\varphi(\rho)\); a moving input spectrum contributes
\(-DS_\varphi(\rho)\) to the CQ price. Fixing only the oldRIGHT marginal
does not in general fix that spectrum.

The actual expanded compiler owner proves \(\kappa=\mu-H_T>53\).
Since \(h_\varphi(q)\le\log_\varphi2<2\) and \(\beta\le1\), its
\(a>51\). For two caps using the **same retained prefix bank and same
stage interface**, with all unused bank data retained,
\[
\boxed{B_{{\rm CQ},N+1}-B_{{\rm CQ},N}
 =\alpha a(\beta q_\star)^N>0.}
\tag{16}
\]
This is an actual clock increment, not a proposed minimization over
unrequired tasks. If changing the cap changes the prepared bank,
dispatcher or transcript law, their changed terms in (13) must be
included instead of using the held-bank formula (16).

## 6. Absolute Book binding and the coframe consumer

The separately stated absolute Book binding on the same full leaf
alphabet is \(s_\omega=-\vartheta\log_\varphi q_\omega-J_{\rm abs}\).
It gives a different baseline,
\[
B_{\rm abs}
 =\vartheta\{H_{\rm pre}
   +\alpha[H_T+\beta h_\star]E_N(\beta q_\star)\}
   -J_{\rm abs}.
\tag{17}
\]
Here \(\vartheta=1/2\) for amplitude binding and \(1\) for probability
binding. Neither (3) nor (8) selects a binding. With fixed
\(\vartheta,q_\star\), put \(A=H_T+\beta h_\star\); then
\[
\begin{aligned}
DB_{\rm abs}=\vartheta\{&
DH_{\rm pre}+AE\,D\alpha+\alpha E\,DH_T\\
&+\alpha[h_\star E+q_\star A E_N'(x_\star)]D\beta\}
-DJ_{\rm abs}.
\end{aligned}
\tag{18}
\]
A moving \(q_\star\) adds
\(\vartheta\alpha\beta[h_\varphi'(q_\star)E+
A E_N'(x_\star)]Dq_\star\).
A separately priced upstream term is added only if it really lies outside
this already complete binding. There is no second free H+J+R or Info
addition. The finite mark (8) reproduces (17)-(18), including the
derivative of the sampling law, rather than deriving \(J_{\rm abs}\).

This supplies the exact remaining source to a proved coframe reduction.
Specifically, suppose an actual admitted, boundary-preserving fibre
diffeomorphism has already established
\[
S(y,\zeta)=B(\zeta)+P(\widetilde y(y,\zeta)),
\tag{19}
\]
with \(P\) independent of \(\zeta\) in these coordinates. Then the chain
rule and invertibility in geometric directions give
\[
DS=0\quad\Longleftrightarrow\quad DP=0,\quad DB=0
\tag{20}
\]
on a product variation domain. On a constrained domain, \(DB\) must
instead vanish on its actual induced internal variations. At \(DP=0\)
the derivative of the moving coframe map contributes zero, while the
baseline (14) or (18) remains exactly. This is the appropriate consumer
of the separate all-order vacuum coframe absorption result; it does not
extend that vacuum theorem to undensitized matter or silently enlarge
its free-site domain.

## 7. What canonical trace and pressure do determine

The owned AF trace preparation theorem already proves that full
nonnegative compatible Fibonacci refinement forces the normalized
tracial weights \(x_n=p^{n+1},y_n=p^{n+2}\); their parameter derivatives
vanish. It also proves that these visible traces do not uniquely fix a
density on the full GNS carrier. Its explicit faithful full-state fibre
and thermal examples are mathematical interface results, not a statement
that those alternative preparations are physically admitted. Consequently
one cannot infer \(DB=0\) in (14) merely from the uniqueness of the AF
trace, or transplant a conditional Gibbs baseline into this compiler.

Likewise the owned scalar Book Perron theorems already determine the
pressure derivative once the actual scalar Cost/Info entries are given.
The new result here is the complete CP lift and finite marked source,
not a claim that scalar Book pressure is unavailable. These formulas
preserve the actual selected value and internal source, including
endpoints and stopping, while leaving the selection of the full
physical Info, preparation and execution law at its existing scope.

## 8. Input provenance and bounded verification

Primary inputs are pinned at repository head
24eebbda2a44896970271e03bf99b9518941234b.
The following are Git blob hashes, not hashes of this companion.

| Repository path | Git blob |
|---|---|
| 02_REGISTRY/research/A4D_SINGLE_RUN_PERRON_BOOK_CAR16_FRESH_FLAG_SOURCE_WELD_2026_10_19.md | da8bb08e96de3a25b83e56d8ad0ec769a4227268 |
| 02_REGISTRY/research/A4D_SCENE_PERRON_DOOB_SINGLE_HISTORY_GOLDEN_INFO_SOURCE_2026_10_19.md | e212dfbc22007c6bafa10d80d38c35d51ce5b347 |
| 02_REGISTRY/research/A4D_NATIVE_BOOK_PATH_ARCHIVE_GROWTH_AND_PERRON_PRESSURE_FORCING_2026_10_19.md | 80b5574e1e6b3277ba0e35920cddadf1e484fb3f |
| 02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/FULL_PRICE_COMPOSITION.md | b0d4483c42e4ac8281603b1459c1f2464da1fff9 |
| 02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/BOOK_SOURCE_BINDING.md | 0fc40d94bf6db0d0be49c783c902274821af5b92 |
| 02_REGISTRY/research/A4D_NATIVE_AF_TRACE_PREPARATION.md | 3cbb805fb72b501a0eb1d7d17b9f037dff115880 |

The adjacent [CommonJS checker](check_perron_complete_marked_source.cjs)
uses only exact BigInt rational first
jets. It checks the new CP similarity on noncommuting complete Kraus
maps, a moving pure preparation with exactly fixed oldRIGHT, 192 complete
three-transition leaves, 66 flag-stopped leaves, and the scalar
terminal-weight identity on all 718 original supported edges.
It rejects omission of the explicit price derivative, the moving final
endpoint, the conditional instrument/preparation score, and substitution
of a common horizon exponent on stopped leaves. The compiler baseline
differential and held-bank increment are checked as exact polynomial
identities; a rational held entropy symbol is only an algebraic fixture,
not the actual native entropy value.

Execution: PASS, 508 exact identities. The fixtures verify the displayed
finite identities, not physical admission, an Info selector, the original
Perron spectrum, or full GR. No historical geometry, compiler or Lean
checker is rerun by this companion.
