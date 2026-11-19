# D0 -> GR: original Book03 clock can move without creating any Book source; an internal record-sensitive cut is necessary

22 October 2026 · current Draft PR #334 / `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, `constitutive/native-programme-v1`. **New exact finite operator theorem** for the ORIGINAL Book03 §03.26.1 sixteen-stage reversible apparatus, an EXACT Golden/Q8 selective-cut consumer, and a CONDITIONAL original n20/cost-clock anti-shortcut. This does **not** modify Book03, admit a new physical projector/Info law, identify Golden code cost with the physical elapsed clock, or assert physical GR closure. `GR_closed=false`.

## 1. A strictly stronger clock blindness theorem

The original source is the actual 16-clock `ZMod 16`:

* `01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md`, §03.26.1: 14 comparison operations, one retained registration, sixteen stages, completion after 15 transitions before clock wrap.
* `03_FORMALIZATION/D0/Representation/FiniteProtocolClock.lean`: `step U (c,s)=(c+1,U_c s)`, `stage_is_internal`, `completed_stage`, `first_sixteen_labels_distinct`, retained program.
* `04_CERTIFICATES/order_memory_control_verify.py`: actual original two Q8 words, all 15 chronological operations, all four spin columns, exact positive Golden output. Original owner already validates the 512-dimensional two-program apparatus; it is not re-proved or silently claimed to be physically M1-admitted here.

Let \(M=16\), \(\mathscr K\) be the **complete internal reference/scene/record/work** space, and

\[
\mathcal U(y)=\sum_{c\in\mathbb Z_{16}}|c+1\rangle\langle c|\otimes V_c(y),
\qquad V_c(y)^*V_c(y)=I_{\mathscr K}.                 \tag{1}
\]

Any differentiable field changes all \(V_c(y)\) freely; the stage advance remains the ORIGINAL fixed reversible clock. This is the exact type of §03.26.1, not an invented reset or field-dependent clock. For arbitrary \(1\le j\le15\), \(\mathcal U(y)^j\) maps an entire stage \(c\) to exactly stage \(c+j\), with an internal unitary product \(V^{(j)}_c(y)\). In particular, with *any* constant-rank internal initialized projector \(Q_0(y)\),

\[
P_{\rm init}(y)=|0\rangle\langle0|\otimes Q_0(y),\quad
\boxed{P_{\rm init}(y)\mathcal U(y)^jP_{\rm init}(y)=0}
\quad(1\le j\le15).                               \tag{2}
\]

This is EXACT on all components and all field derivatives, including moving coframe/links, paid programme preparations and oldRIGHT, provided they stay within the stated stage factor. The clock cannot be rotated away by an internal gate. The usual ORIGINAL full complementary feedback

\[
F_P=P\mathcal U^{j*}(I-P)\mathcal U^jP
   =P-(P\mathcal U^jP)^*(P\mathcal U^jP)        \tag{3}
\]

therefore obeys \(F_{P_{\rm init}}=P_{\rm init}\), and on its rank-\(d\) range:

\[
\boxed{J_{\rm init}(y)=-d\log(1-\zeta),\quad
D_yJ_{\rm init}=D_y^2J_{\rm init}=0}
\quad (\zeta=2^{-20}).                            \tag{4}
\]

This is an **original native stage** result, not the previously used abstract mathematical counterexample in which the early return was merely assumed zero.

### Even stronger: every clock-only Book cut is source-blind

For any subset \(S\subset\mathbb Z_{16}\), take the entire internal fibre at each selected stage:

\[
P_S=\sum_{c\in S}|c\rangle\langle c|\otimes I_{\mathscr K}.
\]

On the input block \(c\in S\), the compression \((P_S\mathcal U^jP_S)^*(P_S\mathcal U^jP_S)\) is **exactly** \(I_{\mathscr K}\) if \(c+j\in S\), and zero otherwise. Consequently

\[
F_{P_S}^{(j)}
=\sum_{\substack{c\in S\\c+j\notin S}}|c\rangle\langle c|\otimes I_{\mathscr K},
\qquad
\boxed{J_S^{(j)}=-d\,b_j(S)\log(1-\zeta),}
\tag{5}
\]

where \(b_j(S)=\#\{c\in S:c+j\notin S\}\). This is a **finite exact rank theorem valid for every internal field-dependent unitary**. Every geometric, matter and input first/second derivative of this clock-only feedback is exactly zero. Changing which time stages are considered active is insufficient to produce Einstein source. In particular `S={0}` gives (4), and `S=all16` gives `F=0`, `J=0`.

### Exact necessary source carrier: internal, relatively anchored cuts

For the general genuine stage-diagonal but INTERNAL selective projector
\(P(y)=\bigoplus_c Q_c(y)\), the old Book operator on the stage-\(c\) active range is

\[
\boxed{F_c=I_{\operatorname{ran}Q_c}
   -Q_c V_c^{(j)*} Q_{c+j}V_c^{(j)}Q_c
   \quad\text{on }\operatorname{ran}Q_c.}                 \tag{6}
\]

Define \(T_c=Q_c V_c^{(j)*}Q_{c+j}V_c^{(j)}Q_c\), whose eigenvalues are the squared cosines of the principal angles between the transported active internal subspaces. For locally constant ranks the EXACT feedback and all noncommuting source jets are

\[
\boxed{J_P=-\sum_c \operatorname{Tr}_{\operatorname{ran}Q_c}
     \log[(1-\zeta)I+\zeta T_c],}
\quad
\boxed{D_yJ_P=-\zeta\sum_c\operatorname{Tr}
       [((1-\zeta)I+\zeta T_c)^{-1}D_yT_c].}           \tag{7}
\]

The second formula uses any local orthonormal trivialization of each variable-rank-free subbundle; traces are invariant under those changes. It DOES NOT assume \([T_c,D T_c]=0\). Relative motion of an **actually selected** internal record/reference/scene cut is mathematically necessary for a nontrivial feedback SOURCE within this stage-local, unmarked completion. Otherwise \(T_c\in\{0,I\}\) has constant multiplicities and (5) applies. A moving \(\zeta\), non-stage-local coherent \(P\), selected field-dependent spectral heat, or genuine cost-marked nonunitary execution are distinct possibilities, not ruled out by (5).

## 2. An actual original Golden/Q8 construction shows the needed type is not fictitious

Consume the UNCHANGED Book03 §03.26.1 / `GoldenOrderInterferometer.lean` **15-operation** comparison, including both original programs, all four spin inputs and reversible final record. Its EXACT registered port laws are

\[
\Pr(\text{record0}\mid\mathrm{identity})=1,
\quad \Pr(\text{record0}\mid\mathrm{order})=p^6,
\quad \Pr(\text{record1}\mid\mathrm{order})=4p^3,
\quad p=\varphi^{-1},\ p^6+4p^3=1.                        \tag{8}
\]

Do NOT add any gate. As a **mathematical Book-active-cut candidate**, take the genuine stage0 prepared 4-dimensional spin input (arm0,record0) plus the existing stage15 **record0** output projector (8-dimensional, all arms and 4 spins) on one stored-program branch. The untouched 15-transition original machine moves stage0 to stage15; it moves stage15 to stage14 and therefore outside this declared two-stage cut. Its actual compressed operator has exactly four principal-angle eigenvalues `1` for the identity word or `p^6` for the noncommuting order word, and eight terminal zero eigenvalues. The complementary Book actions of this **declared** cut are therefore

\[
J_{\rm id}=-8\log(1-\zeta),\qquad
J_{\rm order}=-4\log(1-4p^3\zeta)-8\log(1-\zeta),
\]
\[
\boxed{\Delta J=-4\log(1-4p^3\zeta)>0.}                \tag{9}
\]

This is a nonzero true Golden **program contrast** derived using the existing complete internal clock and report, while a clock-only cut on the SAME unitary is rigorously field-blind by (5). Numerical \(\Delta J=3.6021130949821424\cdot10^{-6}\) for the original \(\zeta\). The two Q8 programs are DISCRETE alternatives; (9) alone is NOT an all42 continuous gravitational source, and the particular combined active projector is NOT identified with native obligatory \(P_N\). The actual native actuation, reference preparation, physical cut selection and whole heat/Info price are STILL open. The useful positive result is that the required **type** of internal, anchored cut is already expressible on original retained records without inventing a new gate.

As a local operator derivative check (explicitly an **auxiliary** non-native continuously variable internal rotation), for rank-one \(Q_0=Q_{15}=|0\rangle\langle0|\), a relative internal angle \(\theta\) gives
\[
J(\theta)=-\log(1-\zeta\sin^2\theta)-\log(1-\zeta),\quad
J'(\theta)=\frac{\zeta\sin(2\theta)}{1-\zeta\sin^2\theta}. \tag{10}
\]
This checks the nonzero source criterion in (7) **without claiming** that arbitrary \(\theta\) is an admitted D0 primitive.

## 3. The n=20 original 72,441-label Golden cost-clock fork is now an EXACT finite support test

A distinct owner has already fixed the original complete **charged** Golden stopped code, not the Q8 stage cost. Its native prefix/suffix/final charges at `n=20`, including ALL failure branches, are:

| original leaf | number or source | full original Golden code cost |
|---|---:|---:|
| first-crossing overshoot | \(F_{20}=6765\) | 21 |
| exact-cost + `FF` | \(F_{21}=10946\) | 22 |
| exact-cost + `RR` | \(F_{21}\) | 24 |
| `FR` or `RF`, then terminal direct `0` | \(2F_{21}\) before report law | 24 |
| `FR` or `RF`, then terminal return `10` | \(2F_{21}\) before report law | 25 |

There are exactly \(6765+6(10946)=72441\) complete positive fine labels. The **unmarked** normalized probability is 1. Each of the four true charge values has **nonzero residue mod 16**:

\[
\{21,22,24,25\}\bmod16=\{5,6,8,9\};\qquad 0\notin\{5,6,8,9\}.\tag{11}
\]

**Conditional physical fork:** IF AND ONLY IF one actually admits a preserved stage register counting **each native Golden code-cost quantum** modulo16, initialized to zero, with no independent factory, elapsed-clock offset, unpriced reset or wrap-identification of old memory, then ALL complete original n20 report and abort branches end orthogonal to the initialized-stage cut. This is an EXACT conclusion for that specified clock lift, not a proof that Book03's 16-stage **per-operation** clock IS this code-cost clock. The two clocks are different native notions until a true source-preserving transport identifies them.

The difference matters even after the complete original **Cost-only analytic mark** is applied. With true Ready fraction \(a=2F_{21}p^{23}\), homogeneous original report probability \(r\), marked whole-input norm at mark \(t\) is

\[
\begin{split}
N_t(r)={}&6765p^{21}e^{-21t}+10946p^{22}e^{-22t}
 +10946p^{24}e^{-24t}\\
&+a[(1-r)e^{-24t}+r e^{-25t}],\\
\partial_r N_t={}&a(e^{-25t}-e^{-24t})\ne0\quad (t>0).   \tag{12}
\end{split}
\]

This retains the entire unready tree, both real terminal charges, and all native prefix multiplicities. At \(t=\ln\varphi\), native \(\zeta=2^{-20}\) and original \(r_0\simeq1.8512395785\cdot10^{-6}\), the exact arithmetic gives \(N_t\simeq2.2584831908890814\cdot10^{-5}\), \(\partial_r N_t\simeq-1.2586096789189258\cdot10^{-6}\), hence the analytic **cost marker sees the field**. But under (11)'s genuine clock-lift premise the entire initialized-return corner is EXACTLY \(A_{E,t}=i^*W_{E,t}=0\). In the original normalized-complement form with all positive normalization retained:

\[
\boxed{J_{\rm init,t}
 =r_R\log\det N_t-r_R\log\det[(1-\zeta)N_t+\zeta A_{E,t}^*A_{E,t}]
 =-r_Rd\log(1-\zeta),\quad D_yJ_{\rm init,t}=0.}\tag{13}
\]

Even the TRUE nonzero derivative of the full marked input norm (12) CANNOT rescue a stage-orthogonal initial-return cut. This is a stronger native code/cut **anti-shortcut** than simply setting a hypothetical early corner to zero by choice. The pre-existing positive cost-marked fixture depends on \(A_{E,t}\ne0\); it is not contradicted but its crucial physical early-return premise is now an explicit, checkable clock-alignment issue. For any truly executed factory cost/clock affecting the actual endpoint residue or initial work cut, (11) must be recomputed with the complete original ledger; our equality does NOT set any such costs to zero.

## 4. Exact consuming test for #334; what the theorem settles

* **Clock-only/no stage-conditional internal cut: FAIL** for a nonzero direct Einstein-CAR first source. Equations (2)–(5) hold for arbitrary changing internal primitives and all42 geometrical/material variations on the real clock type. Golden refinement, longer words before wrap and larger stage-only masks do not repair that source.
* **Exact original discrete Q8 witness: POSITIVE BOOK OPERATOR CONTRAST** on an already available output-bit-selective combined start/end cut (9). This is an actual register/gate calculation, NOT Book03's physically chosen \(P_N\) or a continuous 42-source theorem.
* **Original Golden n20 cost-as-stage clock: CONDITIONAL FAIL** of the initialized-cut marked mechanism, with exact native residues (11) and real full-tree cost marker (12). The actual 16-stage Q8 per-operation and Golden cost clocks have NOT been identified. Do not read an original n20 `cost` as elapsed `stage` without proving the missing transport.

**One now-constrained mandatory physical question:** on the SAME admitted original Golden READY + ten-sign CAR complete tape, read the genuinely selected Book03 \(P_N\) from its actual scene/support and clock/oldRIGHT, and determine the original stage-conditioned internal principal angles \(T_c\) in (6). Compute the actual heat \(\Delta_N\), original branch `Info(v)`, weighted early/factory charges and true independent input rows. A purely stage/cost-only scalarization cannot yield the required source; a real, nontrivial record/reference-selective cut or a separately derived heat/Info channel is required. Do not add (9) to an unchanged HJR as a fitted term. The original exact h4 all42 configured CQ root and null-family source remain witnesses, not a proof that this cut/heat/action is compulsory. Uniform raw216 refinement, M1 physical admission and GR all remain OPEN.

### Bounded independent reproduction and preserved originals

`02_REGISTRY/research/sources/d0_book03_stage_clock_selected_cut_2026-10-22/check_book03_clock_selected_cut.py` is an ordinary standalone Python/numpy bounded independent checker: **119 controls passed**. It constructs cyclic 16×2 staged orthogonal transitions, directly evaluates the original complementary logdet for internal and clock-only cuts across 1,5,15 and wrap 16, checks the exact principal-angle first source, original positive Golden prefix normalizer and charge residues, the marked book-cut zero source, and the literal existing Q8 output coefficient from original Book03. This is a **new limited check**, not a rerun of the 512-dimensional original Q8 checker, Lean, the 72,441 exact site census or the h=1/4 interval root. Original scientific source files remain unchanged. `full_D0_price_selected=false; GR_closed=false; raw216_closed=false`.
