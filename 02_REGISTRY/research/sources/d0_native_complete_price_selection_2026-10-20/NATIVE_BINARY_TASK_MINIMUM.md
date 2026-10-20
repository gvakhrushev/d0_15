# An exact native paid horizon for a declared binary verification task

Bounded application within #334, input `c7a2e7c3`.
Reuse, without rebuilding, the all128 same-tape scalar cross in
`A4D_NATIVE_FULL128_RELATIVE_TRANSFER_AND_CONDENSED_DESCENT.md`, and its
physical-clock application in
`sources/d0_native_relative_history_first_jet_2026-10-20/RESULT.md` §§1–2,6.1.
This is a constructive counterpart to the postrotation task obstruction.

## 1. Native input, no independent data resets

For one fixed physical mesh h and two supplied positive coframe amplitudes
a!=b with ha,hb<1, execute the SAME admitted instrument for n rounds on
the same initial DATA/oldRIGHT state. Retain its entire coherent output.
The owned sequential isometries satisfy the exact operator identity

\[
V_n(hb)^*V_n(ha)=c_h(ha,hb)^n I,
\quad c_h(x,y)=1-\frac{p^2w_h}{128} f(x,y),
\quad w_h=4\sin^2(\pi h),\quad p=\varphi^{-1},             \tag{1}
\]
\[
f(x,y)=x^2+y^2-xy[1+xy+\sqrt{1-x^2}\sqrt{1-y^2}].          \tag{2}
\]

No iid-copy interpretation of the data is needed: (1) already belongs
to the sequential original instrument with changing data and fresh
retained outcome registers. The reference tensor does not change it.
For x,y>0, x!=y, the stable equivalent formula

\[
f(x,y)=(x-y)^2\left(1+
\frac{xy}{1-xy+\sqrt{1-x^2}\sqrt{1-y^2}}\right)>0          \tag{3}
\]

proves `0<c_h<1` on the stated native chart (the owned bound f<=2
also bounds c_h away from zero).

The DECLARED task is to distinguish these two supplied rival field
configurations with worst-case error at most delta, where
`0<delta<1/2`. Every candidate n uses the same hypothesis pair,
same physical initial input, same instrument and same error requirement.
The task and delta are not claimed to follow from M1.

## 2. Exact optimal error, uniformly over mixed and entangled inputs

Set `s=c_h^n`. For n>=1 define

\[
J_0=V_n(ha),\qquad
J_1=\frac{V_n(hb)-sV_n(ha)}{\sqrt{1-s^2}}.                \tag{4}
\]

Equation (1) gives `J_i*J_j=delta_ij I`. Hence the map
`|0> tensor u -> J_0 u`, `|1> tensor u -> J_1 u` is an isometry,
under which the two complete output density operators for ANY fixed
normalized input rho become

\[
\rho_a=|0\rangle\langle0|\otimes\rho,\qquad
\rho_b=|v_s\rangle\langle v_s|\otimes\rho,
\quad |v_s\rangle=s|0\rangle+\sqrt{1-s^2}|1\rangle.       \tag{5}
\]

This includes mixed DATA and arbitrary entanglement with oldRIGHT.
The difference of the two rank-one qubit projectors has eigenvalues
`+sqrt(1-s^2),-sqrt(1-s^2)`. Tensoring a positive trace-one rho
does not change its trace norm. Therefore

\[
\tfrac12\|\rho_a-\rho_b\|_1=\sqrt{1-c_h^{2n}},\qquad
e_n=\frac{1-\sqrt{1-c_h^{2n}}}{2}.                       \tag{6}
\]

The trace-norm variational bound gives the smallest equal-prior
binary error e_n. Its positive/negative spectral test in the qubit
factor has EQUAL conditional errors under a and b, each equal to e_n.
Thus it also attains the minimum worst-case error: no test can have
maximum error below the equal-prior optimum, and this one saturates it.
The optimal measurement is uniform in rho; knowing or purifying the
logical input is unnecessary.

This is the elementary two-dimensional application of the
Holevo–Helstrom theorem, Theorem 3.4 in the author's online chapter:
https://cs.uwaterloo.ca/~watrous/TQI/TQI.3.pdf . The all-input
normal-form reduction (4)–(5) is supplied here for the native scalar
cross, rather than postulating two independently prepared pure states.

**Physical readout boundary.** The spectral test in (5) is a concrete
mathematical POVM on the FULL coherent output, depending on the supplied
hypotheses and n. It is not proved to have a finite native compilation
with any specified price. Tracing out data/work or dephasing the tape
can increase its error. No record or failure is silently discarded.

## 3. Exact minimum paid horizon in the unchanged fixed-horizon protocol class

Solving e_n<=delta gives the exact integer threshold

\[
\boxed{n_{\min}(h;a,b,\delta)=
\left\lceil\frac{\ln[4\delta(1-\delta)]}
{2\ln c_h(ha,hb)}\right\rceil.}                         \tag{7}
\]

The numerator and denominator are both strictly negative. Every
n<n_min fails even with an unrestricted final coherent measurement;
n=n_min attains the mathematical error bound. Empty execution has
error 1/2 and is infeasible for this genuinely nonempty task. For
delta=0 no finite n works because c_h>0. For a=b no n works for any
delta<1/2. These controls retain the distinction between operational
observability and perfect finite discrimination.

The owned original chronological port ledger, including ALL failed
outcomes, has under hypothesis a the mean price

\[
C_n(a)=n[1+p\epsilon_h a^2 w_h],\qquad
\epsilon_h=p^2h^2/64.                                  \tag{8}
\]

The same formula holds with b. Both strictly increase with n.
Therefore n_min uniquely minimizes the actual mean port price for
each hypothesis, its worst-case mean, and every fixed mixture of the
two, among these fixed-horizon same-instrument protocols. In the
equal-prior comparison,

\[
\overline C_{\min}
=n_{\min}\left[1+\frac{p\epsilon_h w_h}{2}(a^2+b^2)\right]. \tag{9}
\]

This is an actual minimum with an explicit attainable statistical
constraint. It is not a minimum of the unbound complete Cost-minus-Info
functional, nor over adaptive stopping, changed instruments, different
preparations, or unequal decoder implementations. A genuine decoder
price depending on n must be added before asserting a full programme
minimum. The increasing all-launch port price alone is what is used.

## 4. Sharp physical scale and finite retained port excess

For fixed positive a!=b,

\[
f(ha,hb)=h^2(a-b)^2+O(h^4),\quad
-\ln c_h=\frac{p^2\pi^2}{32}(a-b)^2h^4+O(h^6).           \tag{10}
\]

The ceiling contributes at most one round, hence

\[
\boxed{h^4n_{\min}\longrightarrow
\frac{-16\ln[4\delta(1-\delta)]}{p^2\pi^2(a-b)^2}.}      \tag{11}
\]

With the actual physical event-time scale `tau_h=p^2 h^4/64`,

\[
\boxed{n_{\min}\tau_h\longrightarrow
T_\delta=\frac{-\ln[4\delta(1-\delta)]}{4\pi^2(a-b)^2}.}  \tag{12}
\]

This is the exact error-dependent constant behind the owned sharp
h^-4 horizon, not merely a big-O lower bound. All native rounds stay
paid. Their equal-prior extra return-port price remains finite:

\[
\overline C_{\min}-n_{\min}\longrightarrow
-\frac{p(a^2+b^2)}{2(a-b)^2}\ln[4\delta(1-\delta)].       \tag{13}
\]

No smooth gravitational source is inferred from the integer ceiling
in (7). While comparing protocols n changes; while differentiating
the original fixed-protocol action the physical clock is held as its
actual independent variable. Interchanging those operations requires
an additional selection/clock theorem.

## 5. Exact contribution to the parent argument

The native full-tape cross now supplies an explicit, uniform-in-input,
complete-coherent binary verifier and the least native paid fixed
horizon for any DECLARED nontrivial error requirement. No additional
data copies, Born-law fit, postselection, new geometry, or hidden
price coefficient is needed for these formulas.

The remaining premises are concrete: which distinction must actually
be verified, what error/precision is native, whether the actual
readout attains the derived bound with its full paid implementation,
and what complete Cost-minus-Info is selected. This theorem computes
the consequence of such a task; it does not insert that task to force
an Einstein source. It can be composed with a genuine native task
derivation later without repeating the all128 instrument algebra.
