# D0 → GR: a SHARP original full128 two-tick clock is necessary and sufficient to distinguish parity MIXED states — positive native history (9,91), not a new historical primitive

26 October 2026, same active research Draft PR #334. This is a NEW source-specific theorem for the actual original CAR16/Julia/Walsh/Golden128 finite instrument and genuine no-reset two-tick memory. Consume, DO NOT REPROVE, the previously exact original future-effect algebra theorem [A4D_ORIGINAL_FULL128_THREE_TICK_CANONICAL_FUTURE_EVEN_ALGEBRA_2026_10_22.md](A4D_ORIGINAL_FULL128_THREE_TICK_CANONICAL_FUTURE_EVEN_ALGEBRA_2026_10_22.md), with its exact algebraic field and certified split-prime embedding. Consume also the original parity/four-CAR decomposition [A4D_ORIGINAL_CAR16_TWO_MODE_BOOK_SOURCE_AND_FUTURE_PARITY_AUDIT_2026_10_25.md](A4D_ORIGINAL_CAR16_TWO_MODE_BOOK_SOURCE_AND_FUTURE_PARITY_AUDIT_2026_10_25.md), which proves the zero Walsh source is odd Hermitian and its square is independent of the spectator mode operators. **This identifies a minimal PHYSICAL clock depth for one CONCRETE pair of states, not the minimal clock depth for all future-state tomography or the compulsory D0 action.**

Original r=1/9, nu=3/5, original phases (i,i,-1,-i), fixed original parity Π=(-1)^number and parity projectors P±=(I±Π)/2, rank8 each. Define the two legitimate normalized initial DATA density operators
\[
\boxed{\rho_+=P_+/8,\quad \rho_-=P_-/8.}\tag{1}
\]
These are distinct source states, but are NOT assumed to be physically prepared for free; the result is an original input-state discrimination theorem on an honestly supplied oldRIGHT/blank apparatus. It does NOT discard the original 128 labelled outcomes, dark rows, work, Hodge, cost or future records.

## 1. THEOREM A — the ENTIRE original one-tick 128-label Born record is parity BLIND for (1)

Let original \(N_j\), j=0,...,63 denote the ORIGINAL 32-pair Walsh rows, including endpoint b=0 (odd) and b=1 (even). Let the actual \(a=N_0\), which on this unchanged family satisfies
\[
a=a^\dagger,\quad\{a,\Pi\}=0,\quad
\Delta=a^2=\Delta_{01}\otimes I_{23},
\quad\operatorname{Tr}_{01}(\Pi_{01}\Delta_{01})=0
\tag{2}
\]
under the existing CAR-graded 01/23 tensor isomorphism; \(\Delta_{01}=A_{01}^2+3\nu^2I_4/128\), where \(A_{01}\) is odd. Because A01 maps the 2-dimensional even and odd 01 grades into one another, their squares have identical trace; the scalar part also has zero parity-supertrace.

The actual original fine Kraus are
\[
K_{2j}=\delta_{j0}I-2p^2N_j^\dagger a,\quad
K_{2j+1}=-2p\sqrt p\,N_j^\dagger a,\quad
p=\varphi^{-1}.
\tag{3}
\]
For j>0 every nonzero one-tick effect is a positive scalar multiple of \(a N_jN_j^\dagger a\). Write \(\operatorname{Str}X=\operatorname{Tr}(\Pi X)\). By cyclicity and odd a,
\[
\operatorname{Str}(aN_jN_j^\dagger a)
=-\operatorname{Str}(\Delta N_jN_j^\dagger).
\tag{4}
\]
The right side is EXACTLY zero for all original 64 Walsh rows:

* Each endpoint b=0 row N_j is odd; from the literal four-mode Julia construction, it is a sum of a mode01-supported odd word and terms linear in ONE of spectator modes2 or3. In \(N_jN_j^\dagger\), at least one of the two spectator single-mode parity supertraces therefore vanishes. Multiplication by spectator-independent \(\Delta\) cannot change this.
* Each endpoint b=1 row N_j is even; its spectator terms are a scalar plus terms EVEN and confined to a SINGLE spectator mode2 or3 (the unchanged static Julia positive root is \(I-\text{const}\,cc^\dagger\) or \(I-\text{const}\,c^\dagger c\)). The only products in \(N_jN_j^\dagger\) that can have nonzero parity-supertrace on BOTH spectator modes are the **cross product** of its mode2 and mode3 components. Both act as the identity on mode01, so their remaining trace factor is precisely \(\operatorname{Tr}_{01}(\Pi_{01}\Delta_{01})=0\) by (2). Every remaining term misses at least one spectator's parity support.

For j=0, \(K_0=I-2p^2\Delta\), \(K_1=-2p\sqrt p\,\Delta\); their effects are polynomials in \(\Delta\) and have zero parity-supertrace because (2) and the identity spectator both hold. Every original dark row has zero effect. Consequently, with NO hidden field-dependent detector, numerical-eigenspace assumption or cost,
\[
\boxed{
\operatorname{Tr}(\Pi K_\alpha^\dagger K_\alpha)=0
\quad\forall\alpha=0,\ldots,127,
\qquad
\Pr_{\rho_+}(\alpha)=\Pr_{\rho_-}(\alpha).
}\tag{5}
\]
Indeed the probability difference is \(\operatorname{Tr}(\Pi E_\alpha)/8\). ANY classical random/deterministic postprocessing of the ONE actual original recorded fine tick is equally blind to (1); no extra outcome table can rescue a one-tick current-address parity comparator on this fixed instrument. The CAR proof applies through the fixed original-phase regular two-parameter proper-boost family wherever the original Julia roots are defined. It is not asserted for arbitrary other D0 test alphabets that may directly measure parity.

## 2. THEOREM B — EXACT ORIGINAL two-tick positive outcome (9,91) breaks that blindness

Keep SAME ORIGINAL finite full128 instrument, its full CP map and NO DATA RESET. For the chronological ACTUAL fine history \(\gamma=(9,91)\), put
\[
K_\gamma=K_{91}K_9,\quad
E_\gamma=K_9^\dagger K_{91}^\dagger K_{91}K_9\succeq0.
\tag{6}
\]
The original source-owned finite-field constructor [check_future_even_algebra_modprime.py](sources/d0_original_full128_future_even_algebra_2026-10-22/check_future_even_algebra_modprime.py) builds ALL 128 true K from CAR creators, original Walsh duplicates, fixed Lorentz boost and the ORIGINAL positive Julia square roots in the characteristic-zero algebraic field
\[
\mathbb F=\mathbb Q\bigl(\sqrt p,\sqrt{12071/20000},i\bigr).
\]
Its eight verified *good split reductions* are already owned; no new prime or physical Golden coefficient is chosen here.

**NEW EXPLICIT certified witness.** Reduce the REAL algebraic element \(\operatorname{Str}E_\gamma\) via those original actual field-ring embeddings. The exact integer modular residues are
\[
\begin{array}{c|rrrrrrrr}
\mathfrak p&229&401&521&709&761&809&941&1009\\ \hline
\operatorname{Tr}(\Pi E_{9,91})\bmod\mathfrak p
&115&83&353&31&380&504&256&593
\end{array}\tag{7}
\]
Every entry is NONZERO; one nonzero good reduction already proves that the original complex characteristic-zero algebraic value is nonzero. There is no assertion that the reduced residuals approximate the tiny real number: only nonzero algebraicity is certified. Hence
\[
\boxed{
\Pr_{\rho_+}(9,91)-\Pr_{\rho_-}(9,91)
=\tfrac18\operatorname{Tr}(\Pi E_{9,91})\ne0.
}\tag{8}
\]

The original complex 16×16 K built independently at r=1/9,nu=3/5 give the DECIMAL CHECK (not proof of nonzero):
\[
\begin{aligned}
\Pr_{\rho_+}(9,91)&\approx 5.9803571740330562\cdot10^{-9},\\
\Pr_{\rho_-}(9,91)&\approx 6.0085213526075941\cdot10^{-9},\\
\Pr_{\rho_+}-\Pr_{\rho_-}
&\approx-2.8164178574538306\cdot10^{-11}.
\end{aligned}\tag{9}
\]
It is a rare event, so physically estimating its bias with finite samples requires true repetitions, fresh known preparations, retained records and their paid costs. That is not silently replaced by an exact Born mean from one finite click.

Combining (5),(8) proves the SHARP native original-FINE-history bound:
\[
\boxed{
\text{for the pair }(\rho_+,\rho_-),\quad
\text{minimal distinguishability horizon}=2\text{ ORIGINAL no-reset ticks}.
}\tag{10}
\]
This does NOT assert that 2 ticks span all 128 even-algebra directions — the already owned strong COMPLETE future-observation result uses THREE paid ticks for the whole \(M_8\oplus M_8\) operator algebra.

## 3. THEOREM C — the already established original 128→65 causal predictor preserves THIS exact two-tick parity comparator, with the genuine Golden port price

Both fine labels in (6) are j>0 odd-port labels, \(9=2\cdot4+1\) and \(91=2\cdot45+1\). The unchanged ORIGINAL twin relation \(K_{2j+1}=\sqrt p\,L_j\), j>0, gives
\[
K_{91}K_9=p\,L_{45}L_4,\quad
E^{128}_{(9,91)}=p^2E^{65}_{(5,46)}
\tag{11}
\]
with 65-predictor label indices 5 and46 under its earlier indexing (K0, K1, then L1,...,L63). Therefore
\[
\boxed{
\Pr^{128}_{\rho_\pm}(9,91)
=p^2\,\Pr^{65}_{\rho_\pm}(5,46),\qquad
\Delta_{\rm parity}^{65}=\Delta_{\rm parity}^{128}/p^2\ne0.
}\tag{12}
\]
This is genuine *no-reset* chronological Kraus scaling, not a fresh state reset or artificially chosen posterior. The independent port bits that were merged still retain their ORIGINAL Golden probabilities and positive net Cost−Info price \(p^3\mathbb E N_{\rm pair}\), as owned in the exact 65-label theorem. They are not deleted physically, and a STOP rule that uses the port b does NOT inherit the merged-label stopping tree.

**Operational use:** within ONE already existing two-tick original fine instrument, a positive actual RECORD cylinder already distinguishes the two central parity sectors. Thus parity is a real future distinction that any D_min future-complete memory must retain. No external history-comparison primitive or independently fitted parity projector was needed; the distinction was manufactured by the closed two-step composition.

## 4. Exact support/checker and scientific limitations

The companion checker [check_two_tick_parity_witness.py](sources/d0_original_full128_future_even_algebra_2026-10-22/check_two_tick_parity_witness.py) IMPORTS, without editing, the original fully authenticated modular K constructor from the pre-existing same directory. It checks ALL 128 one-tick supertraces vanish mod each original prime, the one positive original two-tick (9,91) supertrace has the eight exact nonzero residues (7), each corresponding chronological original K and 65-labelling ratio is preserved, and the two normalized sector Born probabilities are distinct in every good reduction. The analytic CAR support argument above establishes (5) in characteristic zero; a finite list of modular zero tests ALONE would NOT establish one-tick blindness, so no such invalid inference is used. No original 128-tick engine reimplementation, new source mask or extra quantum primitive has been inserted.

**Scientific scope:** mathematically exact native CAR16 future-memory horizon for TWO legitimate prepared DATA states and one original closed experiment. \`GR_closed=false; full_D0_action_selected=false; compulsory_M1_test_suite_selected=false\`. The original BOOK03 full observer, scene Hodge/cut/clock, retained fine history Cost/Info, all42 geometric fields, arbitrary additional future alphabets and physical preparation of the chosen mixed parity-block states retain their previous independent obligations.
