# D0 → ОТО: the ORIGINAL full128 Fourier/CAR16 is ONE logical native reflector; seven of its eight Julia controls have an EXACT H/Toffoli-only HERALDED compiler, while the eighth provably requires a field-sourced resource

22 October 2026 · EXISTING Draft PR #334, native-programme-v1 / constitutive. **New native quantum circuit / algebraic-number SOURCE-SELECTION synthesis, using the ORIGINAL old Julia CAR16 128 Kraus, no new tensor, Einstein coefficient, detector, cost reference, Golden angle or hidden prior.** It consumes the earlier canonical \`W\` reflection, \`A4D_ORIGINAL_FULL128_CANONICAL_HOUSEHOLDER_AND_MEASURED_COHERENCE_WALL_2026_10_22.md\`, and the new original exact one-reflection/128-label constructor \`sources/d0_original_full128_native_julia_reflection_2026-10-22/check_original_julia_walsh_one_reflection.py\`. The physical original Julia controlled-boost link, irreversible-versus-coherent factory and complete M1 selected Book03 \(\Delta_N/\operatorname{Info}\) are NOT assumed available. \`GR_closed=false\`.

## 0. A single real missing primitive, not 128 arbitrary Kraus inverses

The unchanged original native \`sources/d0_book_uniform_source_2026-10-21/check_uniform_book_source.py\` contains precisely 128 genuine complex CAR16 matrices \(K_\alpha(y)\), \(\alpha=0,\ldots,127\), \(\nu=3/5\), phases \((i,i,-1,-i)\) and original \(p=\varphi^{-1}\). The original register has 32 duplicated Julia word-pairs, 64 Walsh rows and two Golden return port outputs per row. For the true Fourier boost \(r=\tanh(\theta/2)=1/9\), \(\theta=\ln(5/4)\), 64 outcomes are exactly DARK and 64 bright. Every dark label remains part of the original physical 7bit outcome alphabet, not illegally renormalized away.

The prior original one-reflection identity, already checked against every old K and first jet, is
\[
 \boxed{
  K_\alpha=\delta_{\alpha0} I-2 W_\alpha W_0^\dagger,\quad
  \sum_{\alpha=0}^{127}W_\alpha^\dagger W_\alpha=I,\quad
  U_{\rm native}=I-2WW^\dagger=U_{\rm native}^\dagger
                    =U_{\rm native}^{-1}.
 }\tag{1}
\]
All original field dependence is inside the old \(\Lambda e^X\) CAR/Julia source, not an external new action. This theorem determines **one** unitary completion that also equals the actual algebraically reconstructed ORIGINAL reflection; it does not show that the primitive circuit is M1 physically compulsory.

**New question:** can \(W\), hence \(U_{\rm native}\), be compiled from the already positive paid H/CNOT/Toffoli/Q8/Golden logical action set without an arbitrary field-specific rotation table? We prove a sharp positive/negative answer for exactly this original one-dimensional proper-boost field fixture.

## 1. ORIGINAL word and flag architecture gives a SIX-bit, fully reversible prepared range

Use the unchanged original fermionic 4-creator exterior CAR16 in Jordan–Wigner order \((0,2,3,1)\), as in the old real code. The 16 distinct source word-pairs can be indexed
\[
 k=4r+2e+t,\qquad
 r\in\{0,1,2,3\},\quad e,t\in\{0,1\}.
\]
Here \(r\) selects original creator role, \(e=0\) selects the original possibly phase/boosted \(X_r=\nu c_rU_r e^{i\phi_r}\), \(e=1\) selects original \(\nu c_r\) with its known minus sign, and \(t=0,1\) selects \(X_r\) versus \(X_r^\dagger\) and left versus right Julia root. \(\phi_r=(\pi/2,\pi/2,\pi,{-}\pi/2)\) is the old exact Q8 phase word.

Write \(L_X=(I-XX^\dagger)^{1/2}\), \(R_X=(I-X^\dagger X)^{1/2}\). The source **native Julia reflection** itself is
\[
 \boxed{
 J_X=\begin{pmatrix}L_X&X\\ X^\dagger&-R_X\end{pmatrix},
 \quad J_X=J_X^\dagger,\quad J_X^2=I.
 }\tag{2}
\]
Thus \(J_X\) is its OWN inverse; no field-fitted inversion or arbitrary phase oracle is being asked for.

Define one \(\mathcal Q_y\) on the original **six variable work qubits**: the original 4-bit Walsh word \(k\), the Julia-output bit \(b\), and the Golden port bit \(t_p\). The old seventh duplicated-Walsh bit remains a fixed zero old work label (but its physical history slot and price cannot be dropped without a real compression programme). \(\mathcal Q_y\) is the COMPLETE unitary composition

1. Hadamard on the four word bits (\(H_4\)).
2. CNOT from old word tag \(t\) to initialized Julia bit \(b\).
3. The eight-way controlled \(J_{X_{r,e}}\) on \(b\otimes\text{CAR16}\).
4. Apply native \(X_b\) if \(t=0\), native \(Z_b\) if \(t=1\); apply the original \(-1\) source sign if \(e=1\).
5. Apply the SAME four-bit Walsh \(H_4\).
6. Apply ONE unchanged native Golden \(XG_\varphi\) to the terminal port, where
\[
 G_\varphi=\begin{pmatrix}\sqrt p&-p\\p&\sqrt p\end{pmatrix},\
 XG_\varphi|0\rangle=p|0\rangle+\sqrt p|1\rangle.
\]

The double occurrence of each old Julia word eliminates the fifth Walsh bit exactly:
\[
 \sum_{j=0}^{31}(-1)^{\operatorname{popcount}(\ell\& j)}
      \mathrm{word}_{\lfloor j/2\rfloor}
 =\begin{cases}
   2\sum_{k=0}^{15}(-1)^{\operatorname{popcount}((\ell/2)\&k)}
       \mathrm{word}_k,&\ell\text{ even},\\
   0,&\ell\text{ odd}.
 \end{cases}
 \tag{3}
\]

The logical K-location is exactly the ORIGINAL \(\alpha=8\ell+4d+2b+t_p\) with duplicate-Walsh \(d=0\) bright or \(d=1\) dark. Direct multiplication gives, for every \(|\psi\rangle\in\mathrm{CAR16}\),
\[
 \boxed{\mathcal Q_y\bigl(|0_{\rm work}\rangle|\psi\rangle\bigr)=W_y|\psi\rangle.}
 \tag{4}
\]
No operation on protected oldRIGHT is needed. Therefore the COMPLETE original 128 Kraus channel has this **specific** coherent unitary realization on the full old work+CAR16:
\[
 \boxed{
 U_{\rm full128,y}=
  \mathcal Q_y
   (I-2|0_{\rm work}\rangle\langle0_{\rm work}|
           \otimes I_{\rm CAR16})
  \mathcal Q_y^\dagger
 =I-2W_y W_y^\dagger .
 }\tag{5}
\]
The gate about the literal all-zero work label is an ordinary finite multi-controlled sign, constructible from owned logical Toffoli/CZ/CNOT *if physical addressability is admitted*. The true oldRIGHT128 is tensor spectator at every step.

**Independent full complex numerical control.** A locally executed separate Python reconstruction of the old full CAR16 creators and every \(K_\alpha\) gave a maximum \(\ell_\infty\) entry residual under (4) of \(4.34\times10^{-19}\), verified \(Q^\dagger Q=I\) on arbitrary 7bit-work superpositions and \(Q(I-2P_0)Q^\dagger=I-2WW^\dagger\) on random FULL 128-work×DATA vectors. The separately committed independent source-test \`check_original_julia_walsh_one_reflection.py\` compares all 128 against the old original native code rather than substituting a fitted synthetic channel. The new \`check_complete_native_reflection_compiler.py\` is a complete independent source-and-inverse consumer of THAT original legacy code.

## 2. THEOREM A — SEVEN of the ORIGINAL eight Julia blocks compile from ONLY fixed signed CAR permutations, 3 H and one honest success flag

The eight controlled \(J_{X_{r,e}}\) in (2) consist of **seven UNBOOSTED** fixed \(\nu=3/5\) creator/dagger cases, and the single true ORIGINAL \((r,e)=(1,0)\) boosted role. On each unboosted case
\[
 X=\frac35 T,\qquad
 TT^\dagger=P_{\rm out},\quad
 T^\dagger T=P_{\rm in},
\]
where \(T\) is one of the ORIGINAL fermionic creators or daggers with its fixed native sign and \(\{\pm1,\pm i\}\) Q8 phase. It is a signed monomial PARTIAL permutation of CAR16, so its bit/Jordan–Wigner basis action uses only reversible Boolean controls and already owned Q8 phases.

On the full \(2\times16\) auxiliary/CAR Hilbert space put
\[
 P_A=\operatorname{diag}(P_{\rm out},P_{\rm in}),\
 Z=\operatorname{diag}(I,-I),\
 X_A=\begin{pmatrix}0&T\\T^\dagger&0\end{pmatrix},\
 Z_I=(I-P_A)Z.
\]
Because \(X_A^2=P_A\) and \(Z_I^2=I-P_A\), the two signed **GLOBAL unitary involutive** permutations
\[
 \boxed{S_B=Z_I+X_A,\qquad S_C=-Z_I+X_A}
\]
satisfy \(S_B^\dagger S_B=S_C^\dagger S_C=I\). They are computational-basis signed permutations with fixed ±i phases, not arbitrary continuous Julia matrices. The ORIGINAL native unboosted Julia square roots reduce to
\[
 L_X=I-\tfrac15P_{\rm out},\quad
 R_X=I-\tfrac15P_{\rm in}.
\]
Consequently the entire original \(32\times32\) unitary has the exact identity
\[
 \boxed{
 5J_X=4Z+2S_B+S_C.
 }\tag{6}
\]
Unlike a two-matrix LCU pretending \(4Z+3X_A\) is unitary on the idle CAR sector, the \(S_C\) **minus sign on the idle complement** makes (6) a TRUE unitary on ALL unknown input states, not just the 16 active occupation states.

**Finite H/Toffoli compiler:** prepare three uniform Hadamard-labelled routing bits \(j\in\{0,\ldots,7\}\). The seven accepted values choose the *existing finite reversible native signed word*
\[
 j=0,1,2,3\mapsto Z,\quad
 j=4,5\mapsto S_B,\quad
 j=6\mapsto S_C.
\]
The eighth \(j=7\) enters a recorded ABORT flag. Apply \(H^{\otimes3}\) again, and select the actual observed output \((j=0,\mathrm{ABORT}=0)\); retain ALL rejected quantum/work/clock branches. The successful Kraus action is exactly
\[
 \boxed{K_{\rm fixed\ Julia,success}
 =\frac18(4Z+2S_B+S_C)
 =\frac58J_X,\qquad
 K^\dagger K=\frac{25}{64}I_{32}.}                      \tag{7}
\]
This is a **real one-attempt exact HERALDED unitary**, not postselected Born probabilities renormalized into a free physical step. No \(\frac35\) angle, normalization \(\sqrt7\), hidden simulator coupling, random field prior or resource state is needed to construct this uniform success gate. The old native \(3/5,4/5\) ratio emerges from the exact 4:2:1 signed CLASSICAL codeword multiplicities. The minimum 3 Hadamards **per executed logical MUX stage** are the true probe bits and are paid, as are all controlled CAR/Toffoli/Q8, good/fail reads and work.

Equation (7) holds tensor \(\mathrm{id}_{R}\) for an ARBITRARY unknown input entangled with protected oldRIGHT. The **success-probability marginal** has no field source even when \(\rho_{DR}(y)\) moves:
\[
 D_yP_{\rm success}=\tfrac{25}{64}D_y\operatorname{Tr}\rho(y)=0.
\]
This does NOT claim the rejected fine quantum work, complete old source preparation, control/factory/clock or compulsory Book03 pathwise Info are field neutral.

A completed exact Gaussian-INTEGER full CAR32 checker checks all seven original \((\mathrm{role},e)\), every signed permutation is selfadjoint unitary, all \(1024\) matrix entries of \(5J=4Z+2S_B+S_C\), the entire \(J^2=I\) and all 14 tag/canonical word outputs. It passed **33,628 exact assertions**:
\`sources/d0_native_julia_seven_clifford_heralded_2026-10-22/check_seven_julia_heralded_galois.mjs\`. An independent full complex Python calculation on the original CAR16 source words reproduces all unboosted Julia matrices and their uniform 25/64 success with residual <\(5\cdot10^{-16}\).

### Reassemble ALL EIGHT controlled Julia blocks while paying the SAME success probability

The eighth, genuinely boosted block \(J_{\rm boost}(y)\) is a **different** input: its physical existence as a G0 controlled unitary with full source is NOT proved by the above seven fixed circuits. If and ONLY IF that one source-coupled \(J_{\rm boost}\) is admitted, the same 3H coin can balance its success amplitude **coherently across the programme superposition**:

- for the seven fixed programme values: the native \(4Z+2S_B+S_C\) construction;
- for the one boosted programme value: the already physically supplied \(J_{\rm boost}(y)\) on coin labels \(0,\ldots,5\) and \(-J_{\rm boost}(y)\) on coin label 6;
- for coin label 7: one genuine common recorded failure.

The boosted successful coefficient is \((6-1)/8=5/8\), identical to all seven fixed ones. This realizes exactly
\[
 \boxed{
 K_{\mathrm{MUX},success}
  =\frac58\sum_{k=0}^{7}|k\rangle\langle k|
                        \otimes J_k(y),\quad
 K_{\mathrm{MUX}}^\dagger K_{\mathrm{MUX}}=\frac{25}{64}I.
 }\tag{8}
\]
All programme branches stay coherent on success, **no which-Julia-tag leak**, no oldRIGHT gate. A single field-dependent controlled \(J_{\rm boost}\) per MUX suffices (its sign for j6 is a fixed programmable phase); this is conditional on that physically ACTUATED native source. Do not reinterpret the seven fixed gates as eight completely field-independent original Julia words.

## 3. THEOREM B — exact FULL 128 Kraus reflector on success with constant \(\Gamma=625/4096\)

The complete Q in §1 uses its controlled Julia MUX exactly ONCE. Replace that MUX by the **uniform** successfully flagged (8), keeping every native H, Golden, bit copy, phase and work register. The entire heralded Q then has
\[
 \boxed{K_{Q,success}=\tfrac58Q,\quad
       P_{Q,success}=\tfrac{25}{64}}
\]
on EVERY state of the full CAR16+work carrier, not merely the originally initialized \(|0\rangle\). Because native Julia blocks are selfadjoint, the reverse Q† circuit is the old paid logical reverse of exactly those gates; the same one-shot gadget gives \(K_{Q^\dagger,success}=\frac58Q^\dagger\).

Place the old literal \(S_0=I-2P_{|0_{\rm work}\rangle}\) between them. Retaining BOTH complete success flags and ALL failed clocks/factory states gives
\[
 \boxed{
 K_{\mathrm{full128},success}
   =\underbrace{\tfrac58Q}_{\rm success\ 2}\,
          S_0\,
      \underbrace{\tfrac58Q^\dagger}_{\rm success\ 1}
   =\frac{25}{64}U_{\rm native},\qquad
 \Gamma:=P_{\rm both\ flags\ success}
   =\Big(\frac{25}{64}\Big)^2
   =\frac{625}{4096}
   \simeq0.152587890625.
 }\tag{9}
\]

**No RETRIES of an unknown quantum input are assumed.** The full additional instrument contains a 1−Γ ≈84.74% failure mass, with genuine possibly information-bearing conditional quantum work. Equation (9) is a valid mathematical high-success **one-shot heralded compiler**, not an unconditioned 128-Kraus original physical channel (which would require proving a deterministic implementation or including failures as physically required new branches).

On a genuinely successful common full input/oldRIGHT original tape, the ORIGINAL native 128 fine Kraus outputs are exactly
\[
 \boxed{K_{\alpha,\mathrm{both\ success}}
 =\tfrac{25}{64}K_{\alpha,\mathrm{original}},
 \quad q_{\alpha,\mathrm{both}}(y)=\Gamma q_{\alpha,\mathrm{original}}(y),
 \quad D_vq_{\alpha,\mathrm{both}}=\Gamma D_vq_{\alpha,\mathrm{original}},}
 \tag{10}
\]
for any physically admitted native field tangent \(v\). No retuned Einstein source or prior is inserted. The success-flag marginal alone has \(D_v\Gamma=0\), but the *complete pathwise* Info, failure conditions and absolute code/factory/stage prices must all be INCLUDED in original Book03 price, not dismissed by averaging the successful subset.

The independent \`check_complete_native_reflection_compiler.py\` recomputes the unchanged original 128-Kraus source, applies the COMPLETE 7bit work Q and Q† to arbitrary complex work vectors, checks every actual \(K_\alpha\) entry and all old field jets, and verifies (9) on multiple arbitrary inputs entangled with a protected reference. Its local independent Python prototype passed with maximum Kraus \(\ell_\infty\) residual \(4.34e{-19}\), unitary/full-reflection residuals \(\ll1e{-10}\), and exactly \(\Gamma\) on every sampled input. This is an independent finite-dimensional verification of the MATH, not a physical G0 gate enactment.

The **logical** input resources of one successful full two-MUX wrapper, NOT including Toffoli decomposition, factory retries, unknown-state failure clock, controlled field actuation or actual Book03 Info, can be counted explicitly:

- \(\mathcal Q\) and \(\mathcal Q^\dagger\): \(2\times8=16\) H on old 4bit word register;
- both 3H/abort/3H Julia gadgets: \(2\times6=12\) H on allocated fair-coin resource;
- TOTAL fixed easy H = **28**, plus exactly two original Golden \(G_\varphi,G_\varphi^{-1}\) (the inverse is the already owned \(Z G_\varphi Z\)), two coherent conditional accesses to the ONE TRUE boosted Julia source, one full-register allzero sign, native copy/sign/Jordan–Wigner CAR permutations and ALL necessarily paid controls, failures and clock stages.

This is NOT the full D0 cost of the script; only a reproducible UPPER COUNT on simple logical H/Golden/boosted calls IF those resource primitives are actually admitted and the branch controls are synthesized.

## 4. THEOREM C — WHY exactly the eighth original native Julia block cannot come from fixed Golden/H/Q8 gates, EVEN WITH POSTSELECTION

This is a new physically decisive ***necessity theorem***, not a generic finite-angle no-go. The original role-1 proper Lorentz CAR operator at \(r=1/9,\nu=3/5,\theta=\ln(5/4)\) is
\[
 U_\mathrm{boost}=I+\frac9{40}G+\frac1{40}G^2,\qquad G^3=G.
\]
Thus the original \(X_{\rm boost}=(3i/5)c_1U_{\rm boost}\) has NONZERO entries in \(\mathbb Q(i)\), i.e. no newly supplied algebraic scalar in its offdiagonal block. But the actual original Julia \(L=(I-XX^\dagger)^{1/2}\) has EXACT 16 CAR eigenvalue roots
\[
 \underbrace{1}_{8\ \text{times}},\
 \underbrace{4/5}_{4\ \text{times}},\
 \underbrace{\sqrt{24142}/200}_{4\ \text{times}}.
\]
The extra scalar is native algebra, not a fitted external angle:
\[
 \begin{split}
 \cosh(2\theta)&=\frac{881}{800},\\
 1-\tfrac9{25}\cosh2\theta
 &=1-\frac{7929}{20000}
  =\frac{12071}{20000}
  =\frac{24142}{40000}.
 \end{split}
\]
Hence
\[
 \boxed{\operatorname{Tr}_{16}L
   =\frac{56}{5}+4\frac{\sqrt{24142}}{200}.}          \tag{11}
\]

Now restrict the native **field-INDEPENDENT** gate palette explicitly to fixed
\[
 G_\varphi,\quad H,\quad
 \{\pm1,\pm i\}\ (\text{Q8}),\quad
 X,Z,\mathrm{CNOT},\mathrm{Toffoli},
\]
initialized computational states, finite ancillas, computational readouts, finite classical feedforward, accepted/rejected outcome flags and arbitrary finite circuit length. (No actual field-dependent boosted interaction, no newly supplied algebraic ancilla/matter amplitude, no imported continuous oracle.)

All its gate entries lie in the exact field
\[
 \boxed{\mathbb K=\mathbb Q\bigl(i,\sqrt2,\sqrt p\bigr),
      \quad p=(\sqrt5-1)/2.}                          \tag{12}
\]
The Golden \(\sqrt p\) satisfies \(f(x)=x^4+x^2-1\), with quartic discriminant
\(\operatorname{disc}f=-400=-2^4 5^2\). The splitting field of f is \(\mathbb Q(i,\sqrt p)\): the other roots are \(\pm i/\sqrt p\). Adding \(H\)'s \(\sqrt2\) and Q8's i can ramify this algebraic number field ONLY at the rational primes **2 and 5**.

The integer 12071 is PRIME (checked by dividing by every prime up to its square root), and \(12071\notin\{2,5\}\). The quadratic field \(\mathbb Q(\sqrt{12071})\) RAMIFIES at 12071. It cannot be a subfield of \(\mathbb K\). Since \(\sqrt2\in\mathbb K\),
\[
 \boxed{\sqrt{24142}/200\notin\mathbb K.}            \tag{13}
\]

Every unnormalized successful Kraus map produced by ANY finite branch of the declared fixed gate palette has ALL entries in \(\mathbb K\), including finite coherent controlled circuits and finite adaptively measured/postselected circuits. Suppose a purported exact uniform unknown-state heralded native compiler achieved \(K_{\rm succ}=c\,J_{\rm boost}\) with \(c\ne0\) on its entire genuine aux×CAR16 space. Pick a nonzero rational-times-i entry of the genuine BOOSTED \(X\)-offdiagonal Julia block: its resulting \(K_{\rm succ}\) entry is in \(\mathbb K\), and its Julia target entry is a nonzero element of \(\mathbb Q(i)\subset\mathbb K\). Hence necessarily \(c\in\mathbb K\). The entire upper-left \(L\) trace of \(K_{\rm succ}\) lies in \(\mathbb K\), so (11) forces \(\sqrt{24142}/200\in\mathbb K\), contradicting (13).

Therefore
\[
 \boxed{\text{NO exact finite field-independent Golden/H/Q8/Clifford
 gate circuit, EVEN WITH POSTSELECTION, supplies the true boosted Julia.}}
 \tag{14}
\]

This is **not** a no-go for approximate phase synthesis at a fixed field point, or a truly sourced field-input/programme containing the missing algebraic extension, or a physical operation on the actual CAR/Lorentz geometric state with field-dependent amplitudes. It is an exact proof that at least ONE genuine field-sourced native operation/resource must occur before the original Fourier \(r=1/9\) full128 can be **exactly** heralded, with all accepted work and oldRIGHT. It resolves the "is the last Julia gate just an unnecessary arbitrary choice?" issue: on this native chart, the extra algebraic content is NECESSARY. The physically allowed source and its cost/independent Euler remain open. For arbitrary full 42-link variations, other original Julia roles may also become field-moving: "ONE" is specifically the old one-parameter role1 boost fixture, not a 42D uniform claim.

The exact BigInt Gaussian-integer checker of all seven positive LCU Julia relations, seven 32×32 unitary involutions, \(\operatorname{Tr}L\) algebra and 12071 prime/Galois obstructions produced **33,628 PASS** in a V8-transcribed JS run; no old full128 spectrum/external field action was retuned.

## 4a. The ORIGINAL labelled instrument also excludes unbounded stopped fixed-palette work

This strengthens §4 by applying its owned number-field obstruction to
the ORIGINAL conditional process, rather than a chosen Julia completion.
The changed question is whether nonminimal rational dilation, extra paid
memory or variable stopping can avoid its genuinely sourced operand.
This excludes that realization route, not D0, approximation or a different
source-equivalent interpretation.

**Exact native witness.** Keep the original vacuum and one-particle
CAR vectors \(|b_0\rangle=|{\tt 0001}\rangle\),
\(|b_1\rangle=|{\tt 0010}\rangle\): bit values 1 and 2 in the unchanged
constructor, not relabelled Walsh outcomes. At \(\theta=\log(5/4)\),
put \(t=\sqrt{24142}/200\). The original Walsh root row restricts to

\[
 N_1|_{\{b_0,b_1\}}=
 \frac1{16}\left[(t-1)
 \frac{\begin{pmatrix}1681&369\\369&81\end{pmatrix}}{1762}
 +\frac15|b_0\rangle\langle b_0|\right].                 \tag{14a}
\]

Indeed \((c,s)=(41/40,9/40)\), and the boosted right defect has
eigenvalue \(t\) on the normalized vector proportional to \((c,s)\). The left defect
equals its unboosted value on this plane; all other unboosted
Walsh-root differences cancel. The corresponding two components of
\(A|{\rm vac}\rangle=N_0|{\rm vac}\rangle\) are both
\(\nu(i-1)/16\), with no coupling from the other one-particle
components into this plane. Thus the ACTUAL label
\(K_2=-2p^2N_1^\dagger A\) has two nonzero entries with ratio

\[
 R=\frac{(K_2)_{b_0,{\rm vac}}}{(K_2)_{b_1,{\rm vac}}}
   =\frac{41}{9}+\frac{881}{1125(t-1)}
   =\frac{209-160t}{81}\notin\mathbb K.                 \tag{14b}
\]

The exact simplification uses \(t^2=12071/20000\). If
\(R\in\mathbb K\), then \(t=(209-81R)/160\in\mathbb K\), contradicting
the OWNED (13). The obstruction is already in one original output.

**Stopped-programme lemma.** Allow finite computational ancillas at
each finite stage, coherent fixed-palette circuits, computational
readouts, classical feedforward, retained work and coarse success.
Every ACTUAL resolved primitive Kraus matrix, including measurements
and decoder, must have entries in \(\mathbb K\). Arbitrary real-basis
measurements are excluded: their effects having entries in
\(\mathbb K\) would not alone establish this Kraus invariant.

A successful output is announced after a finite transcript. No
uniform horizon, finite expected time or eventual-halting assumption
is required. Resolve all successful finite transcripts and final
traced work basis into countably many unnormalized \(L_\gamma\),
each with entries in \(\mathbb K\). If their coarse operation were
any nonzero uniform heralded multiple of original label 2, then

\[
 \sum_\gamma |L_\gamma\rangle\!\rangle
                  \langle\!\langle L_\gamma|
       =a\,|K_2\rangle\!\rangle\langle\!\langle K_2|,
       \qquad a>0.                                    \tag{14c}
\]

For every vector \(v\perp|K_2\rangle\!\rangle\), positivity gives
\(0=\sum_\gamma|\langle v,L_\gamma\rangle\!\rangle|^2\).
Every nonzero \(L_\gamma\) is a scalar multiple of \(K_2\). Its
displayed entry ratio would equal \(R\), while a ratio of nonzero
\(\mathbb K\)-entries belongs to \(\mathbb K\): contradiction.
Extra paid flags, attenuation, tracing work, scalar conditional
normalization and classical stopping do not change this argument.
Finite coherent recombination is already part of \(L_\gamma\).

Even vacuum-input output preservation suffices.
\(K_2|{\rm vac}\rangle\) is odd and pure. The owned
[canonical future algebra](A4D_ORIGINAL_FULL128_THREE_TICK_CANONICAL_FUTURE_EVEN_ALGEBRA_2026_10_22.md)
is \(M_8\oplus M_8\): its parity effect excludes even mass and its
full odd block fixes that pure conditional state. Every positive
refined vacuum output must then lie on the same forbidden ray.
This requires the SAME CAR output and original future tests;
a different encoding needs its own transport theorem.

**Parent substitution and route decision.** The
[native Julia/Walsh realization and whole paired-heat transport](A4D_NATIVE_BLOCK_REALIZATION_AND_COMPLETE_HEAT_TRANSPORT_2026_10_22.md)
at input aa559595e7b800af8217c58885a4710c16747444 already realizes the
minimal Halmos/63-row factorization inside the old register, retaining
all original labels/jets and the derived 1984-mode identity complement.
Consume this positive operator result. It does not make its moving
Julia resource a fixed-palette operation. Equations (14b)--(14c)
exclude replacing that resource by larger fixed-palette rational work
while keeping the original causal instrument. A new completion is
not needed to decide this.

A root-free replacement may retain \(K_0\), hence PRE feedback
\(F=I-K_0^\dagger K_0\), while changing the other labelled CP outputs.
It cannot thereby inherit the original fine entropy, no-reset process
or native65 full price. A different programme with the same total
Euler source is not excluded, but requires that actual complete-source
identity, including its flags, preparation, clocks and work.
Unbounded fair-extractor algorithms can produce scalar probabilities
outside a finite algebraic probability field; they do not create this
forbidden pure projective output.

The remaining ORIGINAL-instrument realization route must obtain a
genuinely source-bearing operation or input from the native physical
process, with its price and independent equations. Approximation and
unbounded coherent nonhalting limits are outside this exact
finite-success theorem and retain their source-convergence obligations.
Do not repeat exact fixed-palette full128 searches by increasing work
or the stopping horizon. Book03 medium/observer identification, full
valuation, actual 42-field pullback and refinement remain open;
GR_closed=false.

The smallest diagnostic used the unchanged native excerpt (source blob
ee8de4635d24c668949ac9a0186616ab7d59f2ed): at the original fixture
the direct \(K_2[1,0]/K_2[2,0]\) is 1.0456596447494142, differing from
(14b) by less than \(2.3\,10^{-16}\); exact symbolic simplification
is zero. The general conclusion is the algebraic proof, not a floating
field test. Old compiler/prime/CAR certificates are consumed unchanged.

## 5. Book03/Einstein and paid-time synthesis: a sharp constructive boundary, not a falsely claimed gravity closure

This result provides an explicit native original ARCHITECTURE, not another tuned finite model:
\[
 \boxed{
 \text{actual raw CAR16/real boost}
 \longrightarrow
 7\,\text{original FIXED heralded signed-permutation Julia blocks}
 +1\,\text{GENUINE SOURCED boosted Julia}
 \longrightarrow \mathcal Q
 \longrightarrow U_{\rm original\ full128}
 \longrightarrow \text{complete fine readout and OLD work}.
 }
\]

The previous \`A4D_ORIGINAL_FULL128_CANONICAL_HOUSEHOLDER_AND_MEASURED_COHERENCE_WALL_2026_10_22.md\` proves that actually irreversibly reading the original fine record BEFORE coherent return loses protected-reference information that later DATA-only deterministic correction cannot restore (\(F_{\rm ent}\) loss >7.39e−6). Thus the new \(\mathcal Q^\dagger\) MUST act BEFORE the irreversible fine record if a fully coherent operator return is desired. Our honest one-shot flags have their own earlier monitored outcomes and cannot be declared free or merged into the original unconditioned 128 Kraus.

The independent new \`A4D_NATIVE_FULL128_NEXT_TICK_THREE_MODE_BOOK_HODGE_2026_10_22.md\` proves the native second full128 fresh-work step on the first record-support cut has a completion-independent NONZERO sourced return (118,272 active modes, three native spectrum bands), whereas the **same first original reflector** is a different fixed-work operation. See the accompanying same-old-W support/no-return theorem: the first original \(\mathcal Q S_0\mathcal Q^\dagger\) COMMUTES with its own exact postrecord support \(P_{\rm rec}\); the physically genuine next DATA tick with a NEW allocated 128-ary work register does not. That clarifies the precise physical time ordering and which future action can produce Book feedback.

The concurrent \`A4D_ORIGINAL_UNPADDED_N1_J2_ALL42_BRINKMANN_WELD_2026_10_22.md\` gives an EXACT nonlinear literal \(0/10\) Golden Price−measured-Shannon all42 Brinkmann–CAR source **on its specified N1 programme**, and the exact same-event all-orders old J₂ no-click logdet identity. Those field variables and the present 1-parameter Fourier CAR16/full128 gate are NOT yet one physically selected equal-cost programme. One may NOT substitute the recovered Julia operator's field source for the fully compulsory Book03 scene \(\Delta_N(V)\), native pathwise Info, independent controller/clock/input Euler, or uniform raw216 Einstein. Their strict SAME-EXECUTION source identification is the remaining joint parent.

**New minimal physically testable interface:** supply/derive from **the old native G0 physical input**, not a new user-fitted gate, ONE controlled proper-boost Julia interaction \(J_{X_\text{role1}}(y)\) on the ACTUAL CAR16+aux register, coherent until the selected Book readout, together with priced H/Toffoli/oldRIGHT and all two-flags. Verify its operator values/jets and the 42-field geometry/CAR map. Then §2/§3 become a complete conditional original full128 coherent hardware realization from the native existing paid logic, with no generic 128-gate catalogue or arbitrary completion.

**Strict status:** \`seven_unboosted_original_Julia_heralded_native_compile_math=true\`, \`heralded_uniform_Julia_probability=25/64\`, \`original_complete_full128_conditional_Q_S0_Qdag_heralded_probability=625/4096\`, \`one_true_role1_geometric_Julia_gate_physically_admitted=false\`, \`fixed_GoldenHQ8_exact_boost_gate_forbidden_by_ramification=true\`, \`compulsory_Book03_scene_Hodge_pathInfo_selected=false\`, \`all42_G0_native_writer_proven=false\`, \`GR_closed=false\`.

## Reproducibility and immutable owner receipts

- \`sources/d0_native_julia_seven_clifford_heralded_2026-10-22/check_seven_julia_heralded_galois.mjs\`: **33,628 exact Gaussian/BigInt checks PASS** for the seven ORIGINAL unboosted \((r,e)\) Julia blocks, full 32×32 matrix/intertwining, honest native \(25/64\) success, original integer prime/discriminant/Galois source necessity. External number-field ramification lemma used at its usual theorem scope, not a numeric substitute.
- \`sources/d0_native_julia_seven_clifford_heralded_2026-10-22/check_complete_native_reflection_compiler.py\`: NEW independent full 7bit original complex CAR16 Q/Q†/full128/first-jet/oldRIGHT heralded 625/4096 test, consuming original \`sources/d0_book_uniform_source_2026-10-21/check_uniform_book_source.py\`. A LOCAL equivalent independent implementation was run; this specific committed \`.py\` file has **not** been executed on remote GitHub CI by the connector. It must be run with Python/numpy/scipy to certify its exact committed source independently. No compiled physical H factory/stage/Julia Q8 cost claim is smuggled in.
- \`sources/d0_original_full128_native_julia_reflection_2026-10-22/check_original_julia_exact_car_algebra.mjs\`: **562 exact checks PASS**, native boosted role1 \(\operatorname{spec}XX^\dagger=\{0,9/25,7929/20000\}\) 8/4/4, \(\sqrt{24142}/200\), polynomial degree 2, 512 Golden duplicate Walsh sign identities. The previous original \`check_original_julia_walsh_one_reflection.py\` is committed as an additional independently runnable 128-Kraus bridge but not marked remote CI-PASS without executing it.
