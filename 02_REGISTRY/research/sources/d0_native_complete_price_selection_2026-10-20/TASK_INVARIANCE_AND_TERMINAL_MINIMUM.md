# Complete Golden readout: task invariance, exact information efficiency, and the actual terminal minimum

Bounded continuation of #334 at `c7a2e7c39fab6b60fa70a553998e9aa2ccc89f3f`.
Input owner:
`02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/MINIMAL_GOLDEN_COMPLETE_SOURCE.md`.
This note strengthens its §§5–7. It does not add an obligatory task, price,
primitive compilation, decoder, or physical action. It changes the use of the
postrotation construction in the native-selection route.

## 1. One retained process and its complete output

Reuse the owner's supplied coherent query, clean embedding `J`, complement
`Q=I-JJ*`, real scalar `t`, and finite cleanup isometry. Its COMPLETE output is

\[
X(y)J=(1-2t^2)|0\rangle J+2t(1-t^2)|1\rangle J
-2t^2|1\rangle QW(y)J,
\qquad (QWJ)^*(QWJ)=(1-t^2)I.                 \tag{1}
\]

The nonclean probability is exactly `r=4t^4(1-t^2)`. Let
`G=[[sqrt(p),-p],[p,sqrt(p)]]`, `p=phi^-1`, and write
`G^k=[[c_k,-s_k],[s_k,c_k]]`. The SAME reporter is the isometry

\[
R:|b,w\rangle\longmapsto|b,w,c(b),1+b\rangle,
\qquad c(0)=0,\quad c(1)=10.                 \tag{2}
\]

The logical input and oldRIGHT are retained, not replaced with a pure input.
All output operators below are tensored with identity on them. Each actual
prefix has a known retained clock value `T_k=T_0+k ell_G`; both signs of a
computational inverse still advance the paid physical clock. The word price
is `T_0+k ell_G`, with `ell_G>0`. The source owner's canonical primitive
comparison has the integer `ell_G>=1`.

## 2. Exact full-quantum experiment equivalence, with the price boundary retained

Ignoring only the KNOWN deterministic clock offset (an explicit labelled
isometry, not an erasure), the complete output family is

\[
V_k(y)=R(G^k\otimes I)X(y)J.
\]

Put `P_R=RR*`. For any integers k,l the field-independent unitary

\[
U_{lk}=R(G^{l-k}\otimes I)R^*+(I-P_R)          \tag{3}
\]

satisfies `U_lk V_k(y)=V_l(y)` for every y and every correlated logical/
oldRIGHT input. On a common clock-labelled space an additional fixed unitary
maps the known prefix clock labels. Orthogonality of the reporter subspace
and its complement proves `U_lk* U_lk=I` directly.

Thus the full coherent statistical experiments are isomorphic: for every
POVM `{M_z}` on output l, `{U_lk* M_z U_lk}` on output k has exactly the same
outcome law for EVERY field y. This preserves all finite-hypothesis testing
risks, estimation risks with fixed loss, pairwise trace distances/fidelities,
and quantum Fisher information. No near-flat expansion is needed for (3).

**Task theorem.** A nonempty admissibility requirement stated solely in
terms of the complete quantum statistical experiment and invariant under
known output isometries cannot exclude k=0 while admitting k=2. Thus such a
requirement, however stringent, cannot force the extra source-bearing
postrotation.

**Essential boundary.** Equation (3) is not a free native decoder. Physical
admission of its uncomputation, inverse rotation, clock routing, and its
actual paid cost are separate requirements. A task requiring a specified
fixed code word, basis, clock value, or a restricted physically paid decoder
need not be invariant. The theorem does not identify those tasks. In
particular the dephased fixed-basis output laws are not generally isomorphic
for all k. All complete output registers must remain available in (3).

## 3. The fixed reporter already attains the complete local information at k=1

On the original common-null stratum Sigma, `t=0` and, for every tangent v,

\[
V_kJ=R[(c_k|0\rangle+s_k|1\rangle)J],\quad
D_vV_kJ=2D_vt\,R[(-s_k|0\rangle+c_k|1\rangle)J]. \tag{4}
\]

All nonclean amplitude derivatives vanish, including directions where the
unseen blocks of W vary. For fixed oldRIGHT marginal the fresh coherent
record has pure first jet, so its quantum Fisher tensor is exactly

\[
\mathcal F_Q=16\,dt\otimes dt                 \tag{5}
\]

for EVERY k, including 0. This remains true if one retains oldRIGHT: its
fixed marginal is a tensor spectator to this first jet. If an independent
oldRIGHT marginal is varied, its genuine source/information is additional
and is not covered by the fixed-marginal statement.

For the complete fine-pointer law, its only positive clean categories at
Sigma have probabilities `(c_k^2,s_k^2)` and derivatives
`(-4c_ks_k dt,4c_ks_k dt)`. Every nonclean probability is O(t^4), hence its
square-root amplitude is O(t^2) and contributes zero Fisher first jet.
Whenever `c_ks_k!=0`, the full classical Fisher tensor is

\[
\mathcal F_{\mathrm{ptr},k}
=(4c_ks_k)^2\left(c_k^{-2}+s_k^{-2}\right)dt\otimes dt
=16\,dt\otimes dt=\mathcal F_Q.                \tag{6}
\]

In particular BOTH original G and G^2 attain the entire scalar first-jet
information. For the owner's field query `dt=gamma_h dJ_2`, this is the
rank-one field tensor `16 gamma_h^2 dJ_2 tensor dJ_2`; this statement does
not falsely claim observability of all 42 independent directions. At an
actual stationary point where `dJ_2=0`, this tensor is zero for EVERY k.

At k=0 the pointer family is rank-singular: its fresh bright probability
is quadratic, and its leading pointer law does not identify the sign of t.
One must not substitute zeros into the positive-support Fisher formula.
The coherent family still has (5). A valid compulsory local task is the
regular signed scalar test `dq_1/dt!=0` with maximal Fisher 16. The actual
unchanged G reporter already fulfills it; G^2 adds no local information.

## 4. Such tasks select a zero-source readout even when continuation is required

At Sigma all work is clean. With the SAME fixed oldRIGHT baseline I_R,
the two actual complete terminal prices are

\[
S_{\rm coh}^{(k)}=T_0+k\ell_G+1+s_k^2-I_R,
\qquad
S_{\rm ptr}^{(k)}=T_0+k\ell_G+
D_\varphi((c_k^2,s_k^2)\Vert(p,p^2))-I_R.       \tag{7}
\]

For an isometry-invariant quantum task, all k remain feasible. The coherent
price has the unique minimum k=0, for every positive ell_G. Its complete
field first source is zero on Sigma.

For a compulsory REGULAR SIGNED first-jet pointer task satisfying (6),
k=0 may be excluded; k=1 is admissible and has zero relative entropy in
(7). For every integer k>=2, its price is at least `T_0+k ell_G-I_R`,
strictly larger than `T_0+ell_G-I_R`. Therefore k=1 is the unique minimum
within all k>=1 for EVERY positive ell_G. This is a genuinely nonempty
measurement task; the conclusion does not rely on allowing idle.

At k=1 the exact native code match gives

\[
dS_{\rm ptr}^{(1)}
=\{1-\log_\varphi(p/p^2)\}\,dq_1=0.          \tag{8}
\]

Complete nonclean entropy and coherent oldRIGHT correlation terms have
zero first derivative by the owned quartic bound. Thus requiring an
actual signed, locally information-optimal readout still selects a
ZERO-source programme. The clause “M1 requires a distinguishable future
test” cannot by itself rescue G^2, even strengthened to optimal local
information extraction.

Under the canonical ell_G>=1 and a task admitting all k, (7) also gives
the known pointer minima: k=0,1 for ell_G=1, otherwise uniquely k=0.
Both have zero first source. The locally minimized terminal value has
zero first derivative on Sigma: the active C1 branches have the SAME
zero derivative. Large k cannot accumulate below them because their
clock cost grows linearly and the complete finite-dimensional record
entropy is uniformly bounded. This is an optimized terminal-value result,
not an assertion about the as-yet unbound whole Book03 action.

## 5. A stronger minimum obstruction on the actual admissible signal range

For k=0, summing ALL work rows in (1) gives the exact probability

\[
q_1(t)=4t^2(1-t^2).                              \tag{9}
\]

The source owner's actual signal is
`t=Tr[C(F-F_*)]/(2N_h)`, with `0<=F,F_*<=I` and `0<=C<=zI`,
`z=2^-20`. Since `-I<=F-F_*<=I`, positivity of C implies

\[
|t|\le \operatorname{Tr}C/(2N_h)\le z/2,
\quad 0<q_1(t)\le z^2<p\quad(t\ne0).           \tag{10}
\]

For the complete fine-pointer law pi, Shannon's chain rule gives
`H_phi(pi)>=h_phi(q_1)`. The same bound holds for the entropy INCREMENT
of the full fine-pointer/oldRIGHT cq record. Indeed each coarse port
effect is EXACTLY `q_b I`, by orthogonality of the clean and nonclean
work in (1), so the oldRIGHT state conditioned on b equals its fixed
marginal. Thus `S(BR)=h_2(q_1)+S(R)`, and, because the extra fine-work
label W is classical, `S(BWR)>=S(BR)`. Consequently
`[S(BWR)-S(R)]/ln(phi)>=h_phi(q_1)`. This retains all conditional
oldRIGHT correlations rather than assuming they vanish separately.
For `0<q<=p`, `-q log_phi(q)>=q` and the
other binary-entropy term is positive. Hence

\[
S_{\rm ptr}^{(0)}(y)
=T_0+1+q_1-H_\varphi(\pi)-I_R
\le T_0+1+q_1-h_\varphi(q_1)-I_R
<T_0+1-I_R=S_{\rm ptr}^{(0)}|_\Sigma.           \tag{11}
\]

For the cq convention, replace `H_phi(pi)+I_R` in (11) by the full
`S(BWR)/ln(phi)` and set `I_R=S(R)/ln(phi)`. The preceding exact
conditional-entropy bound proves the SAME strict inequality.

Thus ANY Sigma point with arbitrarily close admissible `t!=0` is not a
local minimum of this full classical terminal price when k=0 is feasible.
This includes a stationary Einstein point if such nearby queries exist:
the result does not require `dJ_2!=0` or a nonzero quadratic Hessian.
For a smooth path with `t=a epsilon+O(epsilon^2)`, `a!=0`, finite work
dimension gives

\[
S_{\rm ptr}^{(0)}-S_*=
-\frac{8a^2}{\ln\varphi}\epsilon^2\ln(1/|\epsilon|)
+O(\epsilon^2).                                \tag{12}
\]

The rank birth is C1 but not C2. A finite Hessian test misses this
entropy-driven decrease. Retaining nonclean outcomes strengthens, rather
than removes, the classical entropy decrease.

## 6. Exact parent substitution and next genuine premise

The postrotation construction remains a positive realization of the
configured whole-J2 first source. It is now proved impossible to select
its k=2 member by ANY complete-quantum-information-invariant task, and
also impossible by the specific strongest regular local scalar pointer
information requirement, under the stated complete terminal prices.
This is a family/task-class theorem, not a no-go for every D0 programme.

The missing application has therefore sharpened: the native task must
carry an actually sourced, paid restriction not invariant under these
known output rotations, or the genuine complete continuation/Book price
must change (7). Its decoder/reference/clock price must be derived and
compared. Naming distinguishability, adding a Fisher precision threshold,
or demanding a nonzero equation source does not supply that premise.
No new selector or task is installed here. Full native action selection,
positive_gr, and raw216 remain open.

The adjacent standard-library checker independently executes the actual
three-query circuit on complete retained 2x2 work, verifies the reporter
transport including its full code/clock output, checks the Golden algebra
and local Fisher identities exactly, and tests the strict entropy
inequality on the original z-scale. General-dimensional, all-k and
all-field conclusions are proved analytically above; finite fixtures are
not substituted for them.
