# D0→GR physical clock information: exact native time-slot entropy and nonconcentration of Book-MDL history

2026-10-19. **RESEARCH / exact full128 original finite-record consequence / no new detector, clock, action, selector or GR promotion.** Consume PR #334 native full16/128 owner [complete record and code source](A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md) §§1,5,6,7,9, specifically its original exactly CP/TP 128-outcome instrument, flat first-shell `Delta_h=lambda_h I`, `K_blank0=I−epsilon Delta_h/2`, `epsilon=p²h²/64`, exact IID Bernoulli EXIT indicator, and regular trace code source. Consume [Book03 §§03.3.0–03.3.0b](../../01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md): pathwise MDL minimizes the code price of one history while full algebra-valued `Z_D=sum phi^(-S_gamma)[q_gamma]` keeps memory classes. Distinguish the conditional identification `w_gamma=Born(gamma)` from native forcing; see [same-history cocycle](A4D_NATIVE_BRANCH_INFORMATION_COCYCLE.md). Companion research [global modal blank certificate](A4D_NATIVE_FULL128_GLOBAL_MODAL_HISTORY_MDLCLOCK_AND_SOURCE_2026_10_19.md), included in #384, is reused.

## 1. Exact nonconcentration even though one all-blank history has strictly the largest probability

On the genuine unchanged original 128-branch round, `blank0` means the single original blank-label/port0 outcome. Its complement consists of all 127 other full physical outcomes (including blank-label/port1 and EVERY other label/port). Let
```text
e_h=Pr(not blank0)=epsilon_h lambda_h − (epsilon_h lambda_h)^2/4,
q0_h=1−e_h=(1−epsilon_h lambda_h/2)^2.
```
The flat first-shell owner proves that these complete **exit indicators** are IID Bernoulli even though the further labelled Kraus outcomes need not be independent and the original full register/reference is retained. For `n=n_h` actual fresh rounds,
```text
K=# nonblank0∼Bin(n,e_h),
Pr(the whole 128-letter word is blank0^n)=q0_h^n.
```
The existing exact modal theorem shows `blank0^n` is the UNIQUE individual maximum if `q0_h^n>1−q0_h`. On every strict compact positive flat chart with `epsilon_h→0`, `n_h epsilon_h→beta∈(0,∞)`, `lambda_h→lambda∈(0,∞)`,
```text
q0_h^n→exp(−beta lambda)∈(0,1),
Pr(any other complete history)→1−exp(−beta lambda)>0.
```
The modal strict inequality holds for all sufficiently fine h, because the left side tends to a positive constant and the right side tends to0. **Thus a unique maximally likely word does not dominate in total Born mass**. The other 128^n−1 words carry a strictly nonzero aggregate weight and may carry almost all of it. On the already pinned L=4,h=1/4,n=1024,lambda=288/25 sample the modal word is `0.012216322302382` while the other aggregate is `0.987783677697618`; each competing full word individually has smaller probability.

**Conditional no-go:** a claim that the original positive full128 Born weights `w=q` themselves concentrate all measure on their unique MDL-optimal full recorded history at fixed nonzero beta lambda is false. This does NOT preclude algebra-valued interference/cancellation between role-memory classes, a differently admitted path space, a physical postselection/cut, or a Book history action not equal to the literal full128 Born weight. If a supposed classical-limit theorem merely asserts selection of the maximum of individually weighted paths, it is still a true maximum; it cannot automatically deduce measure concentration from it.

## 2. The native clock's time positions are an exact additional physical information carrier

For the original complete **binary coarse view** of the full128 record, retain an indicator at EVERY original record tick (blank0 vs any other). This is a deterministic readout of a physical complete history, not an independently granted new instrument. Its length-n law on flat shell is IID Bernoulli `e_h`. Conditioned on the total event count `K=k`, every ordered pattern of k time positions has the same probability and there are exactly `choose(n,k)` patterns.

The original Shannon chain rule therefore yields **at every finite n, exact**:
```text
H_phi(I_1,…,I_n)
 = n h_phi(e_h)
 = H_phi(K) + E_{K~Bin(n,e_h)} log_phi choose(n,K).       (1)
```
This consumes the full original clock and keeps all failures; it does not confuse one first-return probability with total counts. The extra `H_pos:=E log_phi choose(n,K)` is the true conditional information of **event positions in the registered time word** that is LOST if the historian stores only a count, a single success, or an all-blank MDL word.

At fixed integer n, h and epsilon, differentiating along a legitimate scalar-shell chart `Delta_h=lambda_h I` (e.g. varying the owned compact strict flat coframe scale), the exact **finite source** follows directly from the binomial score:
```text
D_lambda e_h = epsilon_h(1−epsilon_h lambda_h/2),
d/de E[f(K)]=n E_{J~Bin(n−1,e)}[f(J+1)−f(J)].
```
With `f(k)=log_phi choose(n,k)`,
```text
boxed: D_lambda H_pos
   = [n epsilon_h(1−epsilon_h lambda_h/2)/ln(phi)]
       E_{J~Bin(n−1,e_h)} ln[(n−J)/(J+1)].                (2)
```
The binomial score formula is an exact identity (no numerical approximation). Moving clock, controller, preparation and off-scalar link tangent must be differentiated in the ORIGINAL full channel recursion separately. In particular the original J23 field direction in the companion first-source receipt does **NOT** preserve `Delta_h=lambda I` off the base, so equation (2) may NOT be applied to its full tape source without that extra operator calculation.

## 3. Controlled refinement and source: missing clock positions carry a growing first derivative

Suppose `n_h epsilon_h=beta_h` lies in a fixed compact strict interval `0<beta_min≤beta_h≤beta_max`, and `lambda_h` lies in `[lambda_min,lambda_max]` with `lambda_min>0`. The binomial count K has uniformly bounded factorial moments and converges to Poisson(`beta lambda`) if `beta_h→beta`, `lambda_h→lambda`.

For K=O(1), `ln choose(n,K)=K ln n−ln K!+O(K²/n)`. Uniform moment bounds and exponential binomial tails make this valid in expectation and after one differentiation with respect to lambda (for fixed n,epsilon). Since `n=beta_h/epsilon_h`, the exact controlled expansion is
```text
H_pos = (beta_h lambda_h/ln phi) ln(1/epsilon_h)+O(1),
D_lambda H_pos = (beta_h/ln phi) ln(1/epsilon_h)+O(1).      (3)
```
The `O(1)` here is UNIFORM on the stated positive compact beta/lambda chart. The exact coefficient is `beta_h lambda_h` rather than `beta lambda` without an independently given rate for `beta_h→beta`, `lambda_h→lambda`: replacing it by its limit inside `+O(1)` would be unjustified.

Meanwhile
```text
H_phi(K)→H_phi(Poisson(beta lambda))<∞,
S_MDL=−n log_phi(q0_h)→beta lambda/ln phi,
Pr(MDL blank0^n)→e^(−beta lambda)∈(0,1).
```
Thus the **native time-slot Shannon source diverges logarithmically**, although the SOURCE of the selected single modal path has a finite nontrivial limit; a count-only coarse-grained source also has a finite limit. Their mismatch is the price of preserving actual record time labels. These are different original READOUTS, not two equivalent normalizations of one field action. No new parameter is being fitted.

## 4. One pinned numerical check (not a surrogate for original 128×16 parent replay)

Original native input `L=4,h=1/4,n=1024,lambda=288/25` with its original p:
```text
Pr(all blank0) = 0.012216322302382...
E K              = 4.395521353308...
H_phi(I_1...I_n) = 58.904533846304...
H_phi(K)         = 4.436275996782...
H_pos            = 54.468257849523...
D_lambda H_phi(I_1...I_n) = 4.313983868261...
D_lambda H_phi(K)         = 0.094773097984...
D_lambda H_pos            = 4.219210770277...
S_MDL            = 9.153936163646...
```
The [checker](sources/d0_physical_binary_return_2026-10-19/check_native_full128_clock_slot_entropy.py) replays exact finite binomial chain/score identities and verifies the source against symmetric finite differences. All physical events are the original 128-round words; only their event indicator is read out for this specific identity. The external finite KL/entropy price or a complete signed Lorentz/Einstein action is NOT chosen.

## 5. A precise physical closure decision rather than another geometric jet

If Book03's physical classical limit means **concentration in Born measure of the recorded complete history** under the same finite-record clock, it is **NOT** implied by least-code/mode selection: (1)–(3) show a positive nonmodal mass and a large missing clock-position source. The admissible theory must prove one of these native mechanisms, not assert it:

- The Book history/memory-class sum has phase/role-algebra interference genuinely changing the physical measure and its complete source; keep actual operator order, old RIGHT, controller work and normalization.
- The physical verification cut deliberately resolves only a coarse history, with a **forced** original observability/forgetting projection that prices the lost positions consistently. No post hoc event relabelling.
- A different clock/refinement regime is physically selected and controls both the modal mass and its actual source; choosing a degenerate `beta lambda→0` makes the all-blank mass concentrate but also extinguishes its positive Rayleigh signal under bounded actual source jets. This is not a new adjustable clock.

The decisive same-programme check remains full Book history weight and aggregation (NOT choosing mean vs modal to fit Einstein), actual preparation/clock/work plus all 16+24+CAR signed source rows, original microstructure/resonance/refinement, and raw #216. The result is a **scoped no-concentration theorem and exact native time-position source**, not physical GR closure. `GR_closed=false`.


## 6. NEW: native counting and full timed-history MDL pick DIFFERENT "classical" outcomes

A further, sharper theorem follows from the SAME original full128 instrument, without inventing another experiment. The original `A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md` §2 has the ACTUAL repeated total-exit counter by its tilted map `Phi_s=Bmap+e^s Jmap`, while §6 proves the indicators are iid Bernoulli `e_h` on the original strict flat scalar shell. The time-resolved indicator string `I^n=(I_1,...,I_n)` and its native count `K=Σ I_j` are TWO genuinely available deterministic observables of exactly the SAME retained complete 128-round record.

**Literal pathwise finite-source identity on the time-indicator alphabet.** For any particular indicator word `i^n` with exactly k exits,
```text
Pr(i^n)=e^k (1−e)^(n−k),
Pr(K=k)=choose(n,k) Pr(i^n),
S_phi(i^n)=−log_phi Pr(i^n),
S_phi(K=k)=−log_phi Pr(K=k).
```
Hence for EVERY individual original indicator word, with no averaging,
```text
boxed: S_phi(i^n) = S_phi(K=k)+log_phi choose(n,k).        (7)
```
This is the exact combinatorial cost of forgetting EVENT TIMES while keeping their number, **conditional on identifying cost with Born surprisal on this indicator readout**. The original FULL 128-letter word may have further label/reference relative entropy and is not falsely equated to the indicator word here. Equation (7) is the pointwise counterpart of the expectation source in (1), with the coefficient of the time-position term unambiguously fixed to 1 by the original probability law, not fitted to GR.

The two most likely outcomes are DIFFERENT at the same actual finite probe:

- Among all **full 128-letter timed histories**, the previous theorem `q0^n>1−q0` makes `blank0^n` the unique global maximum, hence count K=0.
- Among the actual **native total event counts**, `K∼Bin(n,e)`, whose unique mode is `floor((n+1)e)` when `(n+1)e` is noninteger.

For the pinned original `L=4,h=1/4,n=1024,lambda=288/25` with exact `e=1−q0`, rational-Q(sqrt5) inequalities certify
```text
4 < (1025)e < 5,
count-mode K*=4 (UNIQUE),
Pr(full timed MAP blank0^1024)=0.012216322302382...,
Pr(count K=4)=0.192174653906956... .
```
Therefore the exact native deterministic counting quotient `π(i^n)=Σ_j i_j` has
```text
boxed: argmax [π_* Pr] = 4  !=  π[argmax Pr] = 0.           (8)
```
In the full128 case `π` is the genuine original counter of blank0-complement exits. **Maximum-code selection is not stable under the physically available forgetting-to-count readout.** This is a specific counterexample to claiming that one observer-independent classical state follows solely from maximizing probabilities in whichever available readout frame is chosen. It is NOT a no-go for the Book03 memory-class history action, nor an identification of its original M1 forgetting with counting: that exact physical bridge must be proved.

The action of the most likely *count* is `S_phi(K=4)=3.427494044791...` while for any single timed indicator word with four exits the additional clock multiplicity price is exactly `log_phi choose(1024,4)=51.000341330123...` Golden units. The fine all-blank modal price remains `9.153936163646...`.

On a genuine *flat scalar-shell family* at fixed h, n, epsilon the two strict modes have different first sources, without arbitrary normalization:
```text
D_lambda S_phi(full chronological MAP)
 = n e'(lambda)/[(1−e) ln phi] ≈ 0.795467681433,
D_lambda S_phi(MAP count K=4)
 = −[4/e−(n−4)/(1−e)] e'(lambda)/ln phi
 ≈ 0.071578415524.
```
This is a rigorous **readout-dependent first-source separator**, not merely a difference of event values. Do **NOT** multiply this scalar-shell count source by the original J23 `Dlambda_tr` as though J23 preserved the scalar-shell condition off the base; the moving full128 channel recursion is still required for that physical off-scalar variation.

The physical GR bridge must now **commute the original forgetting/verification algebra with classical MDL selection and the same-history Cost−Info source** or identify and price the exact noncommutativity. This is a focused native experimental/operational obligation and does not call for any new polynomial Cartan jet.

[Exact count-MAP and first-source checker](sources/d0_physical_binary_return_2026-10-19/check_original_count_forgetting_modal_instability.py), in addition to the existing time-slot entropy checker, verifies the Q(sqrt5) inequalities and both normalized actions. `GR_closed=false`.


## 7. Book06 consumer: unique entropy-selected forgetting on the original physical clock record

Book06 §§06.5, 06.24–06.25 ([original Book](../../01_BOOKS/BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md)) requires a TYPED finite forgetting quotient that preserves declared observed responses, with its compatible conditional kernel selected by **maximizing entropy**, not by an arbitrary discard. The original full128 native detector already keeps the FULL original chronological register and also has its own actual repeated exit-count observable from the tilted instrument.

Declare for THIS scoped physical consumer that the retained coarse response is exactly the number K of nonblank0 clock ticks. The fiber of the counting quotient on n time-indicator words has precisely M_k=binom(n,k) elements. Since the native strict flat first-shell blank0/complement indicators are IID Bernoulli with the same e, their real conditional distribution given K=k is **exactly uniform** on this fiber.

For every alternative normalized conditional kernel r_k supported on the same fiber,

\[
H_\varphi(r_k)=\log_\varphi M_k-D_\varphi(r_k\Vert U_k)
\le \log_\varphi M_k,
\qquad U_k(i)=1/M_k.
\]

Equality holds **only** for the actual native conditional kernel U_k. Thus the Book06 maximum-entropy forgetting rule, **provided its retained response is this original count**, has the UNIQUE, physically attained answer. No extra Gibbs preparation, controller, observer weighting, source coupling or erasure is inserted; original chronological archive information remains in the complete tape. The exact conditional entropy is the already proved source

\[
H_\varphi(\text{time positions}\mid K)=
\mathbb E_K\log_\varphi\binom nK,
\]

whose finite first scalar-shell variation was established in equation (2).

There is an exact compatible SCALAR probability-level Book03 exponential-weight pushforward on this particular indicator quotient IF the same-history scalar binding w_Book=q_Born is admitted:

\[
\varphi^{-S_{\rm count}(k)}
=\sum_{i^n:\,\#\mathrm{exit}(i^n)=k}
 \varphi^{-S_{\rm ordered}(i^n)},
\qquad
S_{\rm count}(k)=S_{\rm ordered}(i^n)-\log_\varphi\binom nk.
\]

This is the **unique correctly multiplicity-priced effective history cost** on the declared count readout. It does not claim that Book03's true role-memory-algebra-valued partition is scalar, that its fundamental M1 forgetting is exactly this event-count map, or that Cost−Info is experimentally selected as this Born surprisal. The earlier failure of argmax to commute with forgetting remains real, and is now accounted for by the induced binomial degeneracy information rather than by an arbitrary external counterterm.

**Physical progress:** given the original 128-channel instrument and the declared native count response, the readout quotient, full archive conservation, maximum-entropy conditional kernel and induced scalar log-weight source are mutually compatible, exact and parameter-free. **Open compulsory gate:** prove that the D0 original action/verification history actually uses this or another pinned retained-response quotient, including 128 labels, Lorentz memory classes, preparation, controller/work and clock, then replay the full Einstein–CAR source. Still GR_closed=false.
