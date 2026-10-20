# Retained stopping time recovers the native spectrum and its paid source

20 October 2026. Existing Draft #334, native-programme-v1,
EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE. Phase: native realization.
Input checkpoint: f569c786730301e1603ee64062beccc6b20d05e7.

**Parent substitution.** The original all128 instrument has an exact
complete-record stopping transform, not an arbitrary Bellman objective.
Its retained waiting time determines the entire blank operator and its
noncommuting first source. The actual original port-price transform is
derived on that same tape. Sending the stopping horizon to infinity and
reading only eventual exit instead produces a support projector: its
fixed-rank determinant source vanishes, while its projector, preparation,
clock and price sources need not vanish. Thus intrinsic completion alone
cannot replace the HJR clock while preserving its spectral source.
No full Book Info, physical halting-controller admission or global D_min
selection is asserted.

## 1. Owned inputs and exact scope of the change

The [complete-exit owner](https://github.com/gvakhrushev/d0_15/blob/f569c786730301e1603ee64062beccc6b20d05e7/02_REGISTRY/research/A4D_COMPLETE_EXIT_ACTION_AND_SECOND_SOURCE.md)
already proves the finite effect I−B^(2n), its finite-clock inverse and
the source of the supplied v8 action. The
[actual all128 paid-port owner](../../d0_same_history_price_composition_2026-10-20/paid_port_history.md)
already derives the one-round weighted instrument from all 128 Kraus
rows. The
[previous return/stopping synthesis](../../d0_native_gr_completion_synthesis_2026-10-20/execution/return_cost_and_stopping.md)
already proves the scalar-shell first-exit price, finite cap and L^4
scale. Those results are consumed, not claimed again. The new object here
is the operator-valued stopped-tape transform, its inverse/source, and the
precise loss at the unlimited unmarked boundary.

Let H contain every original site and all CAR16 grades, and let R be the
unchanged oldRIGHT space, of dimension d_R=128 in the parent application.
Use the actual original outcomes alpha=(k,b), k=0,...,63, b=0,1, with
blank alpha=0=(0,0). With p=phi^(-1), p+p²=1,

\[
 B=K_0=I-\frac{\epsilon}{2}\Delta,\qquad
 \Delta=D^2\ge0,\qquad \epsilon=p^2h^2/64.
 \tag{1}
\]

All K_alpha act as identity on R. On the actual admitted Julia window,
||A_native=hD/16||≤1, so B=I−2p²A_native² satisfies
p³I=(1−2p²)I≤B≤I. The owned exact identities are

\[
 \sum_\alpha K_\alpha^*K_\alpha=I,\quad
 E_1:=\sum_kK_{(k,1)}^*K_{(k,1)}=p\epsilon\Delta,\quad
 C:=\sum_\alpha(1+b_\alpha)K_\alpha^*K_\alpha=I+E_1 .
 \tag{2}
\]

Write Q=B² and E=I−Q. Every port1 outcome is nonblank, including
blank-label/port1; hence 0≤E_1≤E. The remaining nonblank port0 effect is
E−E_1. No rare row, dark output, work record or reference component is
discarded. Only the port price c_alpha=1+b_alpha is identified by (2);
other actual prices and Info are not set to zero.

## 2. The complete finite task and its retained isometry

Fix the complete initial state and this instrument before execution.
The task considered here is: report the first nonblank native outcome,
or report unresolved after N native rounds, while retaining every
executed prefix and its fine terminal label. This is a different task
from executing all N rounds after a successful event. It is not a
retrospective replacement of an already executed longer tape.

The mathematical stopped-record isometry is

\[
 V_{\mathrm{stop},N}
 =\sum_{\substack{0\le j<N\\\alpha\ne0}}
 |0^j\alpha\rangle(K_\alpha B^j\otimes I_R)
 +|0^N,\mathrm{unresolved}\rangle(B^N\otimes I_R).
 \tag{3}
\]

The orthogonal record labels are literal complete prefixes, not a
compression of their memory algebra. Telescoping gives
V_stop,N* V_stop,N=I and

\[
 V_{\mathrm{stop},N}^*Q_{\rm exit}V_{\mathrm{stop},N}
 =(I-Q^N)\otimes I_R.
 \tag{4}
\]

Equation (4) consumes the owned finite-exit identity. Equality of this
event effect with the fixed-N unmeasured full tape does not equate the
two complete programmes or their prices. Here N counts actual native
rounds; in the HJR convention m=2N and B^(2N)=Q^N.
Implementing the conditional continuation in (3) within the original
primitive/controller palette is a separate admission obligation.

## 3. New exact stopped-tape transforms and full first jets

Let x=e^(−t), 0<x<1, be an analysis variable marking the actual port
price. A stopped leaf 0^j alpha has price j+c_alpha. The owned one-round
weighted sum, with the unique blank removed, gives exactly

\[
 G_x:=\sum_{\alpha\ne0}x^{c_\alpha}K_\alpha^*K_\alpha
 =x(E-E_1)+x^2E_1
 =x[E+p\epsilon(x-1)\Delta].
 \tag{5}
\]

Consequently the infinite sum over every finite stopped record is

\[
 \boxed{\displaystyle
 F_x^{\rm cost}
 =\sum_{j\ge0}x^j B^jG_xB^j
 =G_x(I-xQ)^{-1}.}
 \tag{6}
\]

This is a genuine generating operator of the original known price.
The simplification uses only that G_x,Q are functions of the same
Delta; individual nonblank K_alpha need not commute with Delta or with
each other. The source is therefore not restricted to a commuting
physical variation. Multiplying each retained amplitude by
x^((j+c_alpha)/2) represents (6) as a Gram operator; it does not assert
an admitted free filter, assign Info or insert an additional physical
charge.

Put R_x=(I−xQ)^(-1). For any admitted smooth field/observer/clock
variation on a fixed Hilbert fiber, including variation of epsilon,

\[
 \begin{split}
 dB&=-\tfrac12[(d\epsilon)\Delta+\epsilon\,d\Delta],\\
 dQ&=(dB)B+B(dB),\\
 dE_1&=p[(d\epsilon)\Delta+\epsilon\,d\Delta],\\
 dG_x&=(dx)(E-E_1+2xE_1)
               +x\,dE+x(x-1)dE_1,\\
 \boxed{dF_x^{\rm cost}
       &=(dG_x)R_x+G_xR_x[(dx)Q+x\,dQ]R_x.}
 \end{split}
 \tag{7}
\]

The displayed order of noncommuting factors is part of the statement.
The original pairing/adjoint and any admissible observer trivialization
must be differentiated in dDelta. Integer N is held fixed in a smooth
finite-clock jet. For a normalized joint input rho_HR the prepared
source is always

\[
 d\,\operatorname{Tr}\rho_{HR}(F_x^{\rm cost}\otimes I_R)
 =\operatorname{Tr}(d\rho_{HR})(F_x^{\rm cost}\otimes I_R)
  +\operatorname{Tr}\rho_{HR}(dF_x^{\rm cost}\otimes I_R).
 \tag{8}
\]

If this same operator is consumed by a supplied closed determinant,
its full, unnormalized trace source is

\[
 dJ_x=d_R\operatorname{Tr}_H
 (I-zF_x^{\rm cost})^{-1}
       [z\,dF_x^{\rm cost}+F_x^{\rm cost}\,dz],
 \quad J_x=-\log\det_{H\otimes R}(I-zF_x^{\rm cost}\otimes I_R).
 \tag{9}
\]

Neither (9) nor the marker fixes z or identifies the complete Book
action. A normalized preparation expectation (8) is a different
contraction of the same actual records.

The fully finite version retains the cap failure:

\[
 \begin{split}
 F_{N,x}^{\rm cost}&=F_x^{\rm cost}[I-(xQ)^N],\\
 Z_{N,x}^{\rm stop}
 &=F_{N,x}^{\rm cost}+(xQ)^N\\
 &=F_x^{\rm cost}+(I-F_x^{\rm cost})(xQ)^N.
 \end{split}
 \tag{10}
\]

Thus the exact exit-tail residual is F_x^cost(xQ)^N, and the complete
finite-cap residual is (I−F_x^cost)(xQ)^N. Since
0≤F_x^cost≤xI and 0≤Q≤I, their operator norms are at most x^(N+1)
and x^N respectively. Their full sources follow by the finite ordered
product rule

\[
 d(A^N)=\sum_{j=0}^{N-1}A^j(dA)A^{N-1-j},\qquad A=xQ.
 \tag{11}
\]

In particular the exit-tail source has norm at most
x^N(||dF_x^cost||+N||dA||). This is a fixed x<1 statement and does not
hide a uniform limit at x=1 or a closing spectral gap.

## 4. New inverse: the retained clock is sufficient, eventual exit is not

Mark only the actual number of executed rounds, without the extra
terminal port1 charge. For 0<s<1 the retained stopping-time operator is

\[
 \boxed{\displaystyle
 F_s^{\rm clock}=s(I-Q)(I-sQ)^{-1}
              =I-(1-s)(I-sQ)^{-1}.}
 \tag{12}
\]

This is the diagonal statistic s^T on the same stopped tape, including
all terminal outcomes. It requires no extra state preparation or
eigenbasis oracle. It is not a different physical objective.
Since I−F_s^clock≥(1−s)I>0, it has the exact inverse

\[
 \boxed{\displaystyle
 Q=\frac1s(sI-F_s^{\rm clock})(I-F_s^{\rm clock})^{-1},
 \qquad \Delta=\frac2\epsilon(I-\sqrt Q).}
 \tag{13}
\]

The positive B window fixes the square root. This statement includes
dark vectors: on ker Delta, F_s^clock=0 and (13) returns Q=I.
Differentiating before taking any stopping limit gives

\[
 \boxed{\displaystyle
 dF_s^{\rm clock}
 =(ds)E(I-sQ)^{-2}
 -s(1-s)(I-sQ)^{-1}(dQ)(I-sQ)^{-1}.}
 \tag{14}
\]

At fixed s this is an invertible linear map on the entire Hermitian
operator space; its inverse is
−(I−sQ)(dF_s^clock)(I−sQ)/(s(1−s)).
The native bound B≥p³I then makes the Sylvester equation
B(dB)+(dB)B=dQ uniquely invertible, with Hilbert–Schmidt inverse norm
at most 1/(2p³). Thus
dDelta=−2(dB)/epsilon−(d epsilon)Delta/epsilon recovers the full source
when the actual epsilon jet is retained. If one assumed only an
abstract B≥0, this last differentiable inverse would not follow at a
zero eigenvalue of B. This is full operator/source recovery from the
retained time statistic, not recovery from one prepared scalar
expectation or free tomography.

Now let P_0 project onto ker Delta and P_+=I−P_0. At fixed finite h,

\[
 \lim_{N\to\infty}F_{\rm exit,N}=P_+,\qquad
 \lim_{s\uparrow1}F_s^{\rm clock}
 =\lim_{x\uparrow1}F_x^{\rm cost}=P_+.
 \tag{15}
\]

The finite stopped leaves define an isometry only on P_+H.
Appending the mathematical nonhalting label with operator P_0 completes
the infinite direct sum to an isometry on H⊗R; this is not a finite
observable halt on a dark state. Exit is almost sure exactly when the
input has no P_0 weight. In (10), Z_N,1^stop=I for every finite N,
whereas lim_(x↑1) lim_(N→∞) Z_N,x^stop=P_+. The missing dark mass is
not a normalization convention and cannot be deleted.

On any smooth fixed-rank chart, r=rank Delta is constant, so at fixed z

\[
 J_\infty=-d_Rr\log(1-z),\qquad d_{\rm fields}J_\infty=0.
 \tag{16}
\]

If z moves, the remaining derivative is d_R r dz/(1−z). The projector
itself can move: P_+(dP_+)P_+=P_0(dP_+)P_0=0, but its off-diagonal
blocks need not vanish. In particular

\[
 d\,\operatorname{Tr}\rho_{HR}(P_+\otimes I_R)
 =\operatorname{Tr}(d\rho_{HR})(P_+\otimes I_R)
 +\operatorname{Tr}\rho_{HR}(dP_+\otimes I_R)
 \tag{17}
\]

need not be zero. Equation (16) follows from the full resolvent trace
of this off-diagonal derivative, not by freezing the kernel.
Rank changes are outside this differentiable statement.

The distinction is quantitative. On a fixed-rank neighborhood with
Q restricted to P_+ bounded above by q_*<1, the exact unmarked tail is
Q^N−P_0. In a local horizontal unitary frame carrying P_0, its norm is
at most q_*^N and its derivative norm is at most

\[
 2\|dP_0\|q_*^N+
 Nq_*^{N-1}\|P_+(dQ)P_+\|.
 \tag{18}
\]

The frame is an analytical comparison of fibers, not a physical
actuator. Neither q_* nor this bound is asserted uniform under mesh
refinement. In particular the N→infinity stopping limit at fixed h is
not the finite-beta HJR refinement limit.

The owned finite-clock inverse therefore cannot be continued to the
unmarked boundary: every positive spectrum with the same support has
the same P_+. The full tape does not lose that spectrum; (12)–(14)
recover it. Replacing the full stopping record by eventual yes/no
is a lossy readout. It is not a permitted future-equivalence or an
automatic D_min compression.

## 5. Whole-operator paid moment and precise attainment

The port price of the capped task is the sum of actual prices on the
rounds that occur. Occupation of round j+1 has incoming amplitude B^j.
Equivalently differentiate the COMPLETE transform (10) at x=1:

\[
 \boxed{\displaystyle
 C_{\mathrm{stop},N}
 =\partial_x Z_{N,x}^{\rm stop}\big|_{1}
 =\sum_{j=0}^{N-1}B^j C B^j.}
 \tag{19}
\]

This is the whole-operator version of the owned scalar-shell price.
Let E^dagger be the Moore–Penrose inverse on P_+, zero on P_0, and set
C_+=C E^dagger. Then exactly

\[
 C_{\mathrm{stop},N}=NP_0+C_+(I-Q^N),\qquad
 \partial_xF_x^{\rm cost}\big|_{1}=C_+.
 \tag{20}
\]

The second identity counts only finite exiting histories. The actual
unlimited expected cost is Tr rho_HR(C_+⊗I_R) only on preparations
supported in P_+⊗R; it is infinite for any positive dark mass.
There is no free deletion of the NP_0 cost in the first identity.

All moving-kernel source terms can be retained explicitly. At fixed
rank, with dE=−dQ,

\[
 \begin{split}
 dE^\dagger={}&-E^\dagger(dE)E^\dagger
 +(E^\dagger)^2(dE)P_0+P_0(dE)(E^\dagger)^2,\\
 dC_+={}&(dC)E^\dagger+C\,dE^\dagger,\qquad dC=dE_1.
 \end{split}
 \tag{21}
\]

These identities follow by differentiating EE^dagger=P_+ and
P_0E^dagger=0 in its support/kernel blocks. The prepared source is
Tr(d rho_HR)(C_+⊗I_R)+Tr rho_HR(dC_+⊗I_R), provided the entire
prepared family stays on the positive support. Otherwise the finite
formula (19), including NP_0 and its source, must be used.
Merely holding one base preparation in P_+ does not justify dropping
its ambient preparation or kernel terms.

There is also a direct prospective lower bound in a precisely defined
class. Keep the same initial state, same native round instrument, same
first-event-or-cap decision task and no erasure of executed records.
For any adapted policy that only continues these rounds and cannot
certify the task before sigma=T∧N, its reporting time tau satisfies
tau≥sigma. On the common underlying record process,

\[
 C_{\rm port,\tau}-C_{\rm port,\sigma}
 =\sum_{j=\sigma+1}^{\tau}(1+b_j)\ge\tau-\sigma\ge0.
 \tag{22}
\]

Thus the earliest reporting policy attains the lower bound (19) within
this stopping-policy class, without an assumed optimal flag, a
catalogue of paths or replacement of a realized record.
It is a mathematical port-cost attainment statement. It neither
proves that the task is compulsory nor supplies native controlled-halt
implementation and its price. Different allowed controls, archive/
controller/work prices, or genuine additional Info can change the
complete prospective objective; (22) is not a minimum of full Cost−Info.

## 6. Consequence for the same native GR parent

The actual original blank-return carrier and every oldRIGHT component
are retained throughout. An intrinsic event-completion rule supplies
a real stopping-time/port-price source through (6)–(8), (14), and (19)–(21).
Its unmarked eventual-exit determinant (16) has no fixed-rank spectral
source. Replacing the original finite HJR clock by that completion
rule therefore cannot preserve the HJR first source automatically.
Conversely, the exact marked inverse shows how the retained clock
preserves the missing spectral information, so this is not a
nonexistence claim for a native closed-loop action.

The remaining parent premise is the original admitted task/controller
and complete Book amplitude/Info/work valuation of these same records,
including its absolute normalization. A supplied closed-record
ensemble may consume the marked operator (6); its actual admission,
measure and price must be demonstrated. No parameter x,s,z is chosen
to fit the configured all40+2 Einstein family, and no new source is
silently subtracted. The scalar Golden p³ regret, finite-future Bellman
lemma and old scalar stopping price are not re-proved here.

The accompanying bounded check verifies the new marked identities,
their full noncommuting jets and moving-kernel controls, and the
all-mode flat original CAR16 specialization. It consumes the pinned
literal-instrument owner and does not replay the old all128 Kraus suite
or infer native admission from an abstract small-matrix fixture.
