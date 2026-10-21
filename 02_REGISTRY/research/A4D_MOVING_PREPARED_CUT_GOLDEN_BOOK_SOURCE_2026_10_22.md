# D0 → Book03: fixed Golden comparator, moving native prepared cut, exact marked feedback and unavoidable input reaction

**Date:** 22 October 2026. Existing Draft [#334](https://github.com/gvakhrushev/d0_15/pull/334), `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`. **Scope:** exact finite operator theorem plus a rigorous application to the original all128 native isometry and conditional full42 source. No new D0 action, primitive, claimed physical selection, Book03 Info law, M1/G0 admission or GR acceptance. `GR_closed=false`.

## Executive theorem: a third route that avoids both previously discovered bottlenecks

Two already published mathematical device-to-Book bridges are (A) a rank-one fixed input cut with `V† CZ V`, requiring coherent *reverse* reporter execution, and (B) a universal fixed Bell two-copy return, whose source gain is bounded by `2 sqrt(2)/D` where D is full output dimension. We construct a different route on the existing operator type:

- **One actual forward isometry** `W(y)` prepares the protected input into the full work/record space.
- The **Book active cut is the projector onto the image of that prepared isometry**, transported with the actual preparation. This is the new, explicitly declared *physical premise*; it is not inferred from Book03 §03.25.
- A **fixed** `Golden-reflection–controlled-Z–Golden-reflection` operation (or the already-owned H version) reads an already native projective binary flag, on all columns. No inverse `W†`, no controlled moving gate, no new continuous rotation, and no discarded work occur in the mathematical feedback circuit.
- The whole true complementary Book response is a spectral polynomial of the **actual native prepared POVM effect**. It remains exact when the latter is a noncentral noncommuting operator:

\[
\boxed{\qquad F_{\rm Golden,post}\simeq 4pE(I-pE),\qquad
F_{\rm H,post}\simeq 2E-E^2,\quad E=W^\dagger\Pi W.\qquad}\tag{A}
\]

The strength does not decay like `1/D`: on a scalar effect `E=r I_d`, the Book gain grows with the actual protected subspace rank `d`. In the Golden option it reproduces **exactly** the preceding fixed-cut `V†CZV` Book source, while requiring no coherent `V†`. The price is a **moving prepared active cut** and its genuine independent-preparation Euler equation. Those are substantial physical obligations, not bookkeeping conventions.

## 1. Complete and exact operator construction

Let `H_in` be a d-dimensional input space, `K` the *complete* retained native work/history output space, `W(y):H_in→K` an isometry (`W†W=I_d`) with the actual oldRIGHT attached as a protected factor, and `Π` an **existing** orthogonal projection representing one complete recorded binary event on `K`. `Π` may be a complex multi-record Boolean projection, not only one output qubit. All complementary outcomes remain orthogonal inside `K`.

Set `Q_y=W_y W_y†` and `E_y=W_y†Π W_y`. Positivity gives `0≤E≤I`. Add a comparator qubit with fixed Hadamard `H`. Its *fixed* unitary is

\[
U=(H\otimes I_K)\{\,|0\rangle\langle0|\otimes I_K+|1\rangle\langle1|\otimes(I_K-2\Pi)\,\}(H\otimes I_K)
=I_2\otimes(I_K-\Pi)+X\otimes\Pi.\tag{1}
\]

This is an ordinary controlled Boolean phase on an **already available** event flag, synthesizable at fixed finite register size from paid H/CNOT/Toffoli if their actual address/factory/clock costs are included. Its physical implementation is not assumed free; it does not require `W†`.

Define the **post-preparation active cut**

\[
P_y=|0\rangle\langle0|\otimes Q_y.\tag{2}
\]

On its range, using the input coordinates provided by `W`,

\[
W^\dagger\langle0|P_y U P_y|0\rangle W
=W^\dagger(I-\Pi)W=I-E.\tag{3}
\]

Since `U` is unitary, the literal, *whole-output* Book03 complement is `F=P U†(I-P)UP=P-(PUP)†(PUP)` on `ran P`, so (3) proves (A) exactly, with no commutativity or probability-only substitution.

Its complete Book03 §03.25 feedback and its exact first jet at fixed `z` are therefore

\[
\boxed{J_{\rm post}(y)=-\operatorname{Tr}_{H_{in}}\log[I-z(2E_y-E_y^2)],}\tag{4}
\]
\[
\boxed{D J_{\rm post}=2z\operatorname{Tr}\!\left[(I-E)(I-z(2E-E^2))^{-1}DE\right],}\tag{5}
\]

including every `DW` and `DΠ`. `E` commutes with its polynomial and resolvent, but **`E` need not commute with `DE`**; (5) is valid under the trace without asserting that false commutativity. If `z` moves, add `Tr[(I-z(2E-E²))^-1(2E-E²)]Dz`.

For a **scalar** prepared effect `E_y=r(y) I_d` on a connected chart,

\[
\boxed{J_{\rm post}=-d\log[1-z(2r-r^2)],\qquad
DJ_{\rm post}=\frac{2dz(1-r)}{1-z(2r-r^2)}\,Dr.}\tag{6}
\]

At the fair binary root `r=1/2`, the full protected-rank source gain is `d z/(1-3z/4)>0`, not `O(1/D)`.

### Native Golden-reflection version: same prior Book source, **without** native reverse reporter

The historical Book03 comparator already has a native Golden reflection

\[
R_G=XG=\begin{pmatrix}p&\sqrt p\\\sqrt p&-p\end{pmatrix},
\quad R_G^\dagger R_G=R_G^2=I.
\]

Replace the fixed H's in (1) by the fixed R_G, leaving the same already-recorded binary projector Π and the SAME post-preparation cut (2). The physical middle operation is still just a fixed phase controlled by Π, with no V(y)†. Exact multiplication gives on the prepared input range

\[
A_\varphi=W^\dagger\langle0|R_G\mathrm{CZ}_{\Pi}R_G|0\rangle W
=p^2I+p(I-2E)=I-2pE.
\]

Consequently the genuine Book03 complement and all complex-Hermitian jets are

\[
\boxed{F_{\varphi,\rm post}=4p E(I-pE),\quad
J_{\varphi,\rm post}=-\operatorname{Tr}_d\log[I-z4p E(I-pE)],}\tag{6a}
\]
\[
\boxed{DJ_{\varphi,\rm post}
=4pz\operatorname{Tr}_d[(I-2pE)(I-z4pE(I-pE))^{-1}DE].}\tag{6b}
\]

At scalar `E=rI_d` its exact derivative is `4dpz(1-2pr)/[1-z4pr(1-pr)] Dr`. For the fair root r=1/2, the return value F is **exactly the old reflected-reporter value** `3p−1` and

\[
\boxed{DJ_{\varphi,\rm post}
=\frac{4dp^3z}{1-z(3p-1)}\,Dr.}\tag{6c}
\]

The earlier fixed-cut reflected construction used a paid `V†CZV` and had (6c) with rank d=1. Here the same source is obtained by a **fixed** Golden/CZ/Golden device, replacing the reverse by a field-dependent *prepared active projector* and preserving the true input multiplicity d. This is an operator-source identity, not a claim that D0 chooses the required moving active cut. Unlike the H variant, the Golden spectral response is not globally monotone on [0,1]; its derivative changes sign above r=1/(2p), a crucial input-stationarity distinction established below.


### What the moving cut means physically

`P_y` is the *range of a genuinely prepared state/subspace*, not the initialized blank projector and not a mere passive change of a fixed coordinate system. The physical Book03/observer owner must independently establish that this **specific** prepared projection is its active cut. Holding `P` fixed while holding the fixed unitary (1) fixed would instead give **zero field source**. Transporting `Π` simultaneously with `Q` as a mere coordinate conjugation also leaves the source unchanged. No algebraic identity can turn the choice of an active physical cut into a free primitive.

## 2. A direct original all128 full-history calculation — exact doubling of blank-return time

Use the literal existing original native `full128` sequential isometry, *without* a Golden cost mark,

\[
V_n(y)=\sum_{|\omega|=n}|\omega\rangle K_\omega(y),\quad V_n^\dagger V_n=I.
\]

Every original report label, including both Golden ports, all blank/nonblank coefficients, physical DATA and oldRIGHT, is retained in the output. Let `Π_nonblank=I-|0^n><0^n|` on the **complete** ordered history. The actual allblank Kraus is the owned positive selfadjoint `B(y)=I-α(y)Δ(y)>0`; the only allblank n-word is `B^n`. Therefore the prepared event effect is **exact on arbitrary original moving coframes and links**:

\[
E_n=V_n^\dagger\Pi_{nonblank}V_n=I-B^{2n}.\tag{7}
\]

Apply the post-preparation theorem with `W=V_n` and *the same native full record*:

\[
\boxed{F_{\rm post,n}=2E_n-E_n^2=I-B^{4n}.}\tag{8}
\]

Thus the new feedback coincides **as an operator-valued function and in its whole noncommuting first jet** with the original blank-return complement for a separately executed `2n`-round native tape:

\[
\boxed{J_{\rm post,n}(B)=J_{\rm blank,2n}(B)
=-r_R\operatorname{Tr}_{DATA}\log[(1-z)I+zB^{4n}].}\tag{9}
\]

Here `r_R=128` is the original oldRIGHT counting multiplicity. `D(B^{4n})=Σ_{k=0}^{4n-1}B^k(DB)B^{4n-1-k}` retains all noncommuting cross terms. 

For the **fixed Golden comparator** on the SAME native V_n prepared cut, the exact alternative polynomial is instead

\[
\boxed{F_{\varphi,\rm post,n}=4p(I-B^{2n})[I-p(I-B^{2n})],}\tag{9a}
\]

which does **not** equal I−B^{4n} in general and has a genuine sign flip of its first spectral source when an eigen-event probability crosses 1/(2p). The two-clock relation (9) belongs specifically to the original H/CZ/H comparator, while (9a) belongs to the original Golden reflection and reproduces the old reflected Book map without V†. Both retain all128 native outcomes and actual shared-link jets mathematically.

The identity is **not** a free 2n-run protocol or equal paid history: the actual *prepared-cut n-tape*, its additional comparator/flag computation and the independent physical `2n`-tape have different work, timestamps, stopping decisions and Book03 Info. Their absolute costs must not be identified by (9).

### Exact marked full128 normalizer: a new root-free noncommuting source

The owned analytical port-cost marker defines `W_n,t=Σ exp(-t C_ω/2)|ω>K_ω`, with genuine positive operator normalizer `N=W_n,t†W_n,t=(Φ_t*)^n(I)`. Let `C=e^{-tn}B^{2n}` be the exactly marked allblank Gram. On the strict positive finite chart, normalize *mathematically* to `Vhat=W N^-1/2` (which is not automatically a native executed isometry). For the same **postprepared** image cut of `Vhat`,

\[
E=I-N^{-1/2}CN^{-1/2},\qquad F=I-(N^{-1/2}CN^{-1/2})^2.
\]

The determinant can be evaluated **without differentiating a square root**, and without falsely commuting `N,C`:

\[
\boxed{J_{\mathrm{post},n,t}=r_R\{\log\det N-
\log\det[(1-z)N+z C N^{-1}C]\}.}\tag{10}
\]

Put `K=(1-z)N+z C N^-1 C` and hold z fixed. Then

\[
\boxed{DJ=r_R\operatorname{Tr}[N^{-1}DN-K^{-1}DK],}\tag{11}
\]
\[
DK=(1-z)DN+z\{(DC)N^{-1}C+C N^{-1}(DC)
-C N^{-1}(DN)N^{-1}C\}.\tag{12}
\]



For the fixed **Golden** primitive an equally root-free and genuinely noncommutative formula follows. Define `D_p=(1−2p)N+2pC` and `K_p=(1−z)N+zD_p N^-1 D_p`. Then

\[
\boxed{J_{\varphi,\rm post,n,t}
=r_R\{\log\det N-\log\det K_p\}.}\tag{12a}
\]

The full differential is `DJ=r_R Tr[N^-1 DN−K_p^-1 DK_p]` with

\[
DK_p=(1-z)DN+z\{(DD_p)N^{-1}D_p+D_p N^{-1}(DD_p)
-D_pN^{-1}(DN)N^{-1}D_p\},
\quad DD_p=(1-2p)DN+2pDC,\tag{12b}
\]

at the fixed primitive p and z; moving-z produces `(D_p N^-1 D_p−N)Dz`. This is exact even when N and C do not commute. H is the special case with coefficient b=1/2, so D_b=C. Neither analytic polar normalization is a free native changed-clock execution.

Moving z adds `(CN^-1C-N)Dz` to DK. The *whole* Marked-source jets `DN` are already computed by the original exact noncommuting transfer recursion; they cannot be replaced by `n d log scalar`. The physically changed filtered-failure isometry is a different execution, as proved in the prior normalization owner. At `t=0`, `N=I`, `C=B^{2n}`, and (10) reduces exactly to (9).

### First-shell continuum consumer, no new limit theorem

The owned original physical first-shell source result has `n_h=128h^-4`, `ν_h=ha`, and complete blank survival `B_h^{2n_h}→exp[-τ(a)]I` in `C¹` with `τ=8π²p²a²` on compact positive-a charts. Consequently the new post-cut Book value/source obeys

\[
\boxed{J_{\rm post}\longrightarrow
-d\log[1-z+z e^{-2τ(a)}],\qquad
D_aJ_{\rm post}\longrightarrow
\frac{2dz e^{-2τ(a)}τ'(a)}{1-z+z e^{-2τ(a)}}.}\tag{13}
\]

Here `d=128×128=16384` counts the real original DATA128 and oldRIGHT128, and the old shell theorem supplies convergence. This statement concerns the post-cut mathematical action, not a new paid clock or the complete Info/heat action.

## 3. One conditional full42 first-source application to the original paid moment reporter

The existing moment-writer offers a complete binary report with full original field source on a declared code/positive-density interface. On the original common-null family, its local real probabilities are all `r_i(y*)=r_0`, positive weights `w_i` sum to `W>0`, and its entire *specified counted-CQ* price is

\[
S_{CQ}=B_m-\gamma_m\sum_i w_i h_\varphi(r_i),\quad
D S_{CQ}|_*= -\gamma_m h_\varphi'(r_0)\sum_iw_iDr_i.\tag{14}
\]

Use the **same already-published** four-slot fixed rational Golden reference-coin aggregation (one complemented indexed site result and three equal known reference slots), giving

\[
r_{\rm fair}=(2+r_0-\bar r)/4,\qquad
\bar r=\sum_iw_i r_i/W.\tag{15}
\]

At the Einstein–CAR null roots, `r_fair=1/2` and `Dr_fair=-(1/(4W)) Σ w_i Dr_i`. Suppose that the actual complete coherent prepared reporter admits an isometry `W_y` into the retained output, with the same physical binary projection Π and protected rank `d`, satisfying the **whole-subspace condition** `W_y†ΠW_y=r_fair(y)I_d` on an open field chart; this holds on a fixed oldRIGHT spectator for a prepared clean known-input reporter, but it has **not** been established as the compulsory D0 execution and cut. Then the **literal fixed-unitary post-preparation Book feedback** (6) has

\[
\boxed{D_{42}J_{\rm post}|_*
=g_{\rm post/CQ}D_{42}S_{CQ}|_*,\quad
 g_{\rm post/CQ}=
\frac{dz}{4W\gamma_m h_\varphi'(r_0)(1-3z/4)}>0.}\tag{16}
\]



For the fixed **Golden** comparator the same conditional chart gives the *previous* reflected-reporter factor, now with full prepared input multiplicity d and no V†:

\[
\boxed{D_{42}J_{\varphi,\rm post}|_*
=g_{\varphi,\rm post/CQ}\,D_{42}S_{CQ}|_*,\quad
 g_{\varphi,\rm post/CQ}
=\frac{dp^3 z}{W\gamma_m h'_\varphi(r_0)[1-z(3p-1)]}>0.}\tag{16a}
\]

No new coefficient has been chosen: compare with the previous one-rank result and set d=1. On the whole original oldRIGHT-preserving rank-d supported subspace the actual Book trace contributes multiplicity d; that extension is valid only when the prepared report effect is truly scalar on those d columns.

This gain is determined by `d,z`, original site-copy counts and real factory readiness, with no fitted continuous Einstein source. Every original 16+24+2 field direction is included **on the exact named common reporter chart**. It is only a first-jet identity. The same negative-semidefinite Hessian defect of the previous aggregated-reporter construction remains, from collapsing many local outcomes to one mean; no second-order inertia, minimizer selection or native all42 physical admission follows.

## 4. Strict free-preparation no-go: the difficulty cannot be moved into an unpriced cut

The moving cut is not magically stationary under an independent free input. Treat the prepared `d`-plane `Q=WW†` as an arbitrary Grassmann variable with fixed U and Π, and assume no genuine independently charged upstream preparation/clock/Info reaction. For `J(Q)` in (4), define the strictly nonnegative spectral derivative

\[
K(E)=2z(I-E)[I-z(2E-E^2)]^{-1}.\tag{17}
\]

For any tangent `δW` with `W†δW+δW†W=0`, its only source is the transverse component: 

\[
DJ[δW]=2\operatorname{ReTr}[K(E)W†Π(I-Q)δW].\tag{18}
\]

All vertical gauge/coordinate rotations `δW=WX` with `X†=-X` disappear because `K(E)` commutes with E. Its exact horizontal Hilbert–Schmidt gradient is

\[
\boxed{\nabla_W^{\rm hor}J=2(I-Q)Π W K(E).}\tag{19}
\]

By the isometry and Π²=Π,

\[
\boxed{\|(I-Q)ΠW\|_{HS}^2=\operatorname{Tr}(E-E^2).}\tag{20}
\]

If the gradient (19) vanishes, its action on all eigenspaces of E with `e<1` vanishes since K(e)>0 there; the e=1 eigenspace already has `(I-Q)ΠW=0`. Thus `(I-Q)ΠW=0`, which is equivalent to 

\[
\boxed{DJ\equiv0\text{ for every free prepared-cut tangent}
\quad\Longleftrightarrow\quad [Q,\Pi]=0.}\tag{21}
\]

At such a point E has only eigenvalues 0 and 1 and cannot encode a fractional 0<r<1 field-sensitive binary signal.

### Sharp Golden exception — a fractional *stationary* principal angle, but zero field source

For the Golden comparator replace K(E) in (17)–(19) by

\[
K_\varphi(E)=4pz(I-2pE)[I-z4pE(I-pE)]^{-1}.
\]

The same exact Grassmann variation proof applies, but `K_φ` has one interior zero at

\[
\boxed{r_\bullet=\frac{1}{2p}=\frac\varphi2\in(0,1),\qquad
F_\varphi(r_\bullet)=1.}\tag{22a}
\]

Using the identity `||(I-Q)ΠWv||²=e(1-e)` for a normalized eigenvector of E with eigenvalue e, the **entire** unconstrained input critical set is classified:

\[
\boxed{DJ_{\varphi,\rm post}=0\ \forall\ \delta Q
\iff\ \operatorname{spec}(E)\subseteq\{0,1,1/(2p)\}.}\tag{22b}
\]

For e=0 or1, transverse projector leakage vanishes; for e=1/(2p) the scalar source multiplier itself vanishes. Conversely every fractional eigenvalue other than r_bullet has nonzero gradient and can be varied through a genuine output-subspace tangent. At the extra Golden point the Book feedback is saturated, `F=1`, its first field/source derivative vanishes and its scalar second derivative is negative: it is not a hidden Einstein selection mechanism. In particular the actual root reporter r=1/2 is NOT r_bullet; it retains the nonzero independent preparation Euler.

For the scalar Golden effect `E=rI_d` its exact horizontal preparation-gradient norm (away from the sign change, with absolute value) is

\[
\boxed{\|\nabla_W^{\rm hor}J_\varphi\|_{HS}
=\frac{8p z|1-2pr|\sqrt{d r(1-r)}}{1-z4pr(1-pr)}.}\tag{22c}
\]

At r=1/2 this equals `4p³ z sqrt(d)/[1−z(3p−1)]>0`. The Golden fixed-comparator route therefore trades physical *inverse* access for a *constrained/paid moving prepared cut*, **not** for a free joint stationary controller. The H comparator has no interior fractional exceptional eigenvalue, hence the stronger iff [Q,Π]=0 classification (21) specific to its source.
 In particular for `E=r I_d` with `0<r<1`, **the free-preparation gradient is strictly nonzero** with exact norm

\[
\boxed{\|\nabla_W^{\rm hor}J\|_{HS}
=\frac{4z(1-r)\sqrt{d r(1-r)}}{1-z(2r-r^2)}.}\tag{22}
\]

At the fair source root `r=1/2` this is `z sqrt(d)/(1-3z/4)>0`. At the original DATA128×oldRIGHT128 `d=16384`, it is approximately `0.0001220704` for `z=2^-20` (compute exact expression before quoting digits). If the **actual** writer constrains Q as a generated state, those free normal variations are NOT admitted, and the real causal adjoint and paid initial/controller Euler replace (21). If they are admitted, its **actual** preparation-price first jet must cancel (19) or produce a genuine constraint reaction. Neither cancellation is supplied by this theorem.

This exactly exposes the tradeoff with the old two source bridges: fixed initialized-cut Route A needs a *coherent reverse*; fixed universal rank-one Bell Route B has an `O(1/D)` signal; the NEW native-Golden forward-only route has the *identical prior Golden feedback source*, now with full protected rank d and **without V†**, but it needs a *moving, physically justified, upstream-stationary prepared cut*. No route automatically closes the simultaneous physical requirements.

## 5. Type/physical acceptance gate

A physical D0→GR theorem using (16) must still independently establish:

1. A single M1/G0-admitted, paid, field-dependent coherent preparation **from the common initial state**, its actual factory/abort/clock and all original oldRIGHT modes. A positive *finite code catalogue* and controlled field-price differences do not alone produce a smooth physical field writer or a unique field selection.
2. Book03's active projector at the scene0 detector **is the prepared image projector (2)**, or an actually source-preserving native identification of that projector with the original Book03 P_N. This cannot be assumed by calling both objects "active"; the original fixed-scene default projector and the original full128 pre-blank cut are separate physical sections.

   There is also an exact type check against the previously owned fixed-initial-cut Golden bridge: its [proof](sources/d0_native_book_reflection_bridge_2026-10-21/PROOF.md) sets `P_Ω=|χ><χ|`, rank one, and counts the complete initial purification once; an oldRIGHT128 factor contained in the complete workspace does not multiply that determinant. The moving cut here has `rank(P_y)=d`; on the advertised protected `DATA128×oldRIGHT128` subspace, `d=16384`. Therefore this full-rank `P_y` cannot be identified with that specific rank-one `P_Ω`, and its factor `d` cannot be transferred to that fixed-cut source. This rejects only reuse of that mathematical bridge as the same cut. It does not identify the compulsory Book03 `P_N`/`J_loc` with `P_Ω` or rule out a separately selected moving cut; that requires the literal same-tape projector and its preparation/source equations.
3. One complete real Book03 Info and memory-algebra readout on that SAME tape, with coherent-vs-measured flags and the true heat/feedback cut typed. A fixed-CQ or terminal-only Shannon entropy is not automatically compulsory Book03 Info.
4. Genuine **independent** preparation/controller/observer/clock Euler equations; (21) prohibits the shortcut that makes all prepared cuts free, while finite moment writer cost neutrality does not imply physical selection of a geometry code.
5. For physical GR, the original full 42-field source, exact root and common refinement/recovery with genuine native time/cost and raw216. The current already-owned positive root/capstone may be consumed only once the above same-execution identification succeeds.

`GR_closed=false`. The Golden-sweet-spot classification is a scoped input-stationarity theorem for the fixed original splitter, not a compulsory physical preparation. The theorem adds no primitive, new field, fitted coupling, counterterm, alternative metric, chosen Info law or declared physical selection.
