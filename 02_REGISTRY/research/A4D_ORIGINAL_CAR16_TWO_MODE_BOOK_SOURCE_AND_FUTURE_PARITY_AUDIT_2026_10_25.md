# D0 → GR: original CAR16/Julia128 Book prepared return collapses EXACTLY 16→4→2, but the 128-label future memory does NOT

25 October 2026. New analytic, native-original-carrier result in the same scientific Draft #334. Original sources: \`A4D_ORIGINAL_FULL128_THREE_TICK_CANONICAL_FUTURE_EVEN_ALGEBRA_2026_10_22.md\` (all genuine future effects span \(M_8(\mathbb C)\oplus M_8(\mathbb C)\)); \`A4D_ORIGINAL_GOLDEN_HALMOS_NAIMARK_ALL128_CAUSAL_BOOK_WELD_2026_10_22.md\` (exact original first-blank \(K_0\), prepared \(F_{\rm pre}\), full 128 fine outcome/archive retention); \`A4D_CLOSED_FEEDBACK_NO_RETURN_PROBABILITY_AND_CANONICAL_RECIPROCAL_DUALITY_2026_10_25.md\` (exact closed P/Q no-return Born/Slater representation). **This result is stronger than the previous fixture-only nonprojector witness: the original FULL 16×16 prepared feedback determinant and its genuine Lorentz source reduce to one RADICAL-FREE rational function on the ENTIRE ORIGINAL PROPER-BOOST FAMILY.**

It is NOT a GR-source theorem for arbitrary all42 coframe/link/matter changes: the 2-parameter physical chart here has the original proper-boost parameter \(r=\tanh(\theta/2)\), original common scalar \(\nu\), and FIXED original phases \((i,i,-1,-i)\); all other field variables are outside its claims. Nor does scalar reduction authorize discarding original original128 fine Kraus, future tests, WORK, oldRIGHT, clock, Info, HJR or field-source roles. \`GR_closed=false; native_full_action_selected=false\`.

## 1. THEOREM A — exact original Walsh row0 is an ODD Hermitian CAR word whose square eliminates the spectator modes

Keep the native original four-fermion CAR16 with creator ordering \((0,2,3,1)\) and \(\{c_a,c_b^\dagger\}=\delta_{ab}\). Write
\[
G=c_0c_1^\dagger+c_1c_0^\dagger=G^\dagger,\quad G^3=G,\qquad
U_r=e^{2\,\operatorname{artanh}(r)G}
=I+\frac{2r}{1-r^2}G+\frac{2r^2}{1-r^2}G^2,\quad |r|<1.
\tag{1}
\]
This is the ORIGINAL proper Lorentz boost, not a newly selected unitary. It is positive and even; no imaginary Euclidean rotation is substituted.

Let \(a=N_0\) be the ORIGINAL zero Walsh label, endpoint b=0, from the frozen 32-pair Walsh/Julia source with original duplicated slots. Directly summing the actual \((-1)^{\operatorname{popcount}(0\&j)}=1\) row gives
\[
\boxed{
\begin{aligned}
a=A_{01}+b_2+b_3,\quad&
A_{01}=\frac{\nu}{16}
[(i-1)c_0+(-i-1)c_0^\dagger
 +i c_1U_r-iU_rc_1^\dagger-c_1-c_1^\dagger],\\
&b_2=-\frac{\nu}{8}(c_2+c_2^\dagger),\\
&b_3=\frac{\nu}{16}[(-1-i)c_3+(-1+i)c_3^\dagger].
\end{aligned}}\tag{2}
\]
All three summands are selfadjoint/odd; distinct mode supports CAR-anticommute. Because \(A_{01}\) is odd and supported only on modes 0,1, the EVEN cross anticommutators are zero, and
\[
b_2^2=\frac{4\nu^2}{256}I,\qquad b_3^2=\frac{2\nu^2}{256}I.
\]
Thus the original positive full native CAR16 Kraus response is
\[
\boxed{
\Delta=a^\dagger a=a^2=A_{01}^2+\frac{3\nu^2}{128}I_{16}.
}\tag{3}
\]
**This is an exact full16 identity for ALL real \(r\in(-1,1)\), \(\nu>0\)** with original phases, not a spectrum tolerance at \(r=1/9\). It implies \(\Delta\ge3\nu^2/128\,I\). The upper strict bound \(\Delta<I\) is asserted only on original admitted regular chart (at \(r=1/9,\nu=3/5\) it holds). Changing the original phases or admitting independent arbitrary Lorentz links changes the theorem's input and cannot inherit (3) for free.

Let \(H_{01}\cong\mathbb C^4\) be the two-mode CAR Fock state, \(H_{23}\cong\mathbb C^4\) the spectator modes. The canonical graded CAR tensor relabelling reorders occupied basis bits \((0,2,3,1)\to(0,1,2,3)\) with sign \((-1)^{n_1(n_2+n_3)}\). Under that explicit unitary \(W_{\rm graded}\), the original matrix becomes
\[
\boxed{
W_{\rm graded}^\dagger\Delta W_{\rm graded}
=\Delta_{01}\otimes I_4,\quad
\Delta_{01}=A_{01,4}^2+\frac{3\nu^2}{128}I_4.
}\tag{4}
\]
Hence all original prepared Book source and value depend on the 4×4 **ACTIVE** CAR operator, multiplied by the exactly REQUIRED untouched spectator dimension four. They are not allowed to be calculated on an unpaid 4D replacement process instead of the original actual carrier.

## 2. THEOREM B — the 4×4 characteristic polynomial is the square of ONE quadratic with known rational coefficients

The two-mode \(A_{01,4}\) is selfadjoint and ODD for \(\Pi_{01}=(-1)^{N_0+N_1}\). Its matrix in the even and odd 2-dimensional blocks is
\[
A_{01,4}\cong
\begin{pmatrix}0&T^\dagger\\T&0\end{pmatrix},\quad T\in M_2(\mathbb C).
\]
Consequently \(\Delta_{01}\) is the direct sum of \(T^\dagger T+cI_2\) and \(TT^\dagger+cI_2\), \(c=3\nu^2/128\). They have the SAME characteristic polynomial even when T is singular (a finite square matrix always has equal eigenvalue lists for \(T^\dagger T,TT^\dagger\)). Define the exact two invariants
\[
\boxed{
\begin{aligned}
s(r,\nu)&=\frac{\nu^2(5r^4+r^3-8r^2-r+5)}{64(1-r^2)^2},\\[1mm]
t(r,\nu)&=\frac{\nu^4(23r^4+6r^3-32r^2-10r+25)}
{16384(1-r^2)^2}.
\end{aligned}}\tag{5}
\]
Direct 2×2 CAR multiplication (derived from (1)–(3); executable symbolic checker below) proves
\(\operatorname{tr}(T^\dagger T+cI_2)=s\) and
\(\det(T^\dagger T+cI_2)=t\). Therefore
\[
\boxed{
\chi_{\Delta_{01}}(x)=(x^2-sx+t)^2,\qquad
\chi_{\Delta}(x)=(x^2-sx+t)^8.
}\tag{6}
\]
These are **exact symbolic rational-function identities**. The parent full16 algebra has at most two distinct eigenvalues \(\lambda_\pm\), EACH with exactly multiplicity 8, on the ORIGINAL full CAR16 space. They may coincide at isolated boosts; the invariant formula continues analytically with NO eigenvector gauge.

At the ACTUAL physical native \(r=1/9,\nu=3/5\):
\[
\boxed{
\lambda_\pm=\frac{141489\pm 9\sqrt{397841}}{10240000},\quad
\lambda_-\simeq0.0132629182178348,\quad
\lambda_+\simeq0.0143716520946652.
}\tag{7}
\]
At \(r=0\), \(\lambda_+=\lambda_-=5\nu^2/128\), an exact crossing explicitly included.

## 3. THEOREM C — ORIGINAL full16 Book return and source are ONE radical-free Golden rational function

Let \(p=\varphi^{-1}\), \(z=\zeta=2^{-20}\), and retain the original ORIGINAL blank Kraus
\[
K_0=I-2p^2\Delta,\qquad
F_{\rm pre}=I-K_0^\dagger K_0=4p^2\Delta(I-p^2\Delta).
\tag{8}
\]
On the unchanged 16D DATA return input (multiply by genuine oldRIGHT rank \(d_R\) in a protected spectator model), define
\[
u=4zp^2,\qquad v=4zp^4,\qquad
\mathfrak d(s,t)=
1-us+v(s^2-2t)+u^2t-uvst+v^2t^2.
\tag{9}
\]
This is the PRODUCT of the two actual positive survival eigenvalues \(1-z4p^2\lambda_\pm(1-p^2\lambda_\pm)\) WITHOUT introducing \(\sqrt{s^2-4t}\). From (6),(8):
\[
\boxed{
\det_{16}(I-zF_{\rm pre})=\mathfrak d(s(r,\nu),t(r,\nu))^8,\quad
J_{\rm pre}=-8\log\mathfrak d(s(r,\nu),t(r,\nu)).
}\tag{10}
\]
**All radical/spectral-basis choices disappear.** Since \(s,t\in\mathbb Q(r,\nu)\), \(\mathfrak d\in\mathbb Q(\sqrt5)(r,\nu)\) with the already fixed original \(p,z\). On any regular chart (where its value is positive) its genuine original CAR source in the proper-boost coordinate \(\theta=2\operatorname{artanh}r\) is the EXACT rational logarithmic derivative
\[
\boxed{
D_\theta J_{\rm pre}=-4(1-r^2)\,
\frac{\partial_r\mathfrak d(s(r,\nu),t(r,\nu))}
{\mathfrak d(s(r,\nu),t(r,\nu))}.
}\tag{11}
\]
No commuting \(D\Delta\) assumption is used: (10) is the determinant of the WHOLE field-dependent operator, so differentiating that scalar function automatically includes all noncommuting matrix entries. At the fixture,
\[
\boxed{
J_{\rm pre}=3.2042444113482065\cdot10^{-7},\quad
D_\theta J_{\rm pre}=-1.8312595190037388\cdot10^{-8}.
}\tag{12}
\]
These precisely reproduce the ORIGINAL previously owned full128 computation with moving Lorentz source. The correct physical right-archive multiplicity \(d_R\) multiplies both.

A complete field source in arbitrary coframe/link/material directions is NOT recovered from two original \((r,\nu)\) derivatives. The exact calculation is a very strong *native same-source closed formula* on the actual original proper-boost family, not a claim to have solved GR by dimensional counting.

## 4. THEOREM D — a parity-switching ORIGINAL CAR operator preserves the Book return, while ORIGINAL future tests still distinguish the two parity sectors

Let \(\Pi=(-1)^{N_0+N_1+N_2+N_3}\), \(P_\pm=(I\pm\Pi)/2\). The odd Majorana \(\Gamma_2=c_2+c_2^\dagger\) is a selfadjoint unitary with
\[
\boxed{\Gamma_2^2=I,\quad\{\Gamma_2,\Pi\}=0,\quad
[\Gamma_2,\Delta]=[\Gamma_2,F_{\rm pre}]=0.}\tag{13}
\]
Therefore \(\Gamma_2:P_+H\to P_-H\) is an EXACT unitary equivalence of the two parity restrictions of the prepared Book feedback, for EVERY \(r,\nu\) in this original chart. The two 8×8 feedback determinants are identical:
\[
\boxed{
\det_{P_+H}(I-zF_{\rm pre})=\det_{P_-H}(I-zF_{\rm pre}),\quad
J_{\rm pre}=J_++J_-=2J_+.
}\tag{14}
\]
This parity equivalence is a property of THE PREPARED Book effect only; \(\Gamma_2\) need NOT intertwine all original 128 Kraus/future histories. On the exact original THREE-TICK instrument, the effects span \(M_8\oplus M_8\), so \(P_\pm\) are both fully observable within the authentic future-test algebra. **Deleting one parity sector and multiplying its scalar \(J\) by 2 preserves one Book number but LOSES genuine available future distinctions**, and is therefore NOT a future-faithful D0 code/task reduction. This is the exact physical memory firewall for the otherwise dramatic 16→2 calculation.

## 5. THEOREM E — conditional UNIQUENESS of the filled Slater audit from the authentic future algebra, not an invented U(16) symmetry

The earlier closed no-return probability is realized by a pure \(\Lambda^d H_P\) filled input. Instead of arbitrarily assuming all \(U(16)\) act as D0 physical gates, consume the ORIGINAL already proved **future-observation algebra**
\[
\mathcal A_{\rm future}=M_8(\mathbb C)\oplus M_8(\mathbb C).
\]
Its changes of orthonormal representation frames on the TWO irreducible sectors form \(U(H_+)\times U(H_-)\). These are BASIS changes of the existing observable algebra, not new native physical actuation gates.

**Exact representation theorem.** In the finite fermionic CAR/exterior representation of \(H_+\oplus H_-\), any PURE FIXED-NUMBER state ray \(\Psi\in\Lambda^k(H_+\oplus H_-)\) that is invariant **up to global phase** under EVERY independent such basis change must be one of FOUR occupation classes:
\[
\boxed{(k_+,k_-)\in\{(0,0),(8,0),(0,8),(8,8)\}.}\tag{15}
\]
**Proof:** diagonal unitaries with independently varying phases force any invariant ray to have just ONE joint occupation-index weight; otherwise relative phases change the ray. Internal two-coordinate swaps, which belong to each \(U(8)\), then force that one occupied index subset in EACH block to be either EMPTY or FULL (if it is nonempty proper, swap an occupied and unoccupied index to give an orthogonal ray). Conversely empty and filled top wedges are one-dimensional determinant representations, so each of the four possibilities is invariant up to phase.

If the audit task is required to use a PURE basis-independent INPUT, is NONTRIVIAL on **both** independently future-accessible parity sectors, and must use NO extra mode orientation or asymmetrical parity catalogue, only the \((8,8)\) fully occupied input survives. Thus
\[
\boxed{
\Psi_{\rm future\text{-}complete}
=\Omega_{+}^{(8)}\wedge\Omega_-^{(8)}
\in\Lambda^{16}H_{\rm CAR16}\quad\text{unique up to a phase}.
}\tag{16}
\]
Its exact closed no-return Born probability is the original complete 16D \(\det(I-zF_{\rm pre})\), as in the existing Slater theorem; both parity sectors are counted with the correct protected rank.

**Precisely conditional part (DO NOT PROMOTE):** an ORIGINAL four-mode CAR Fock *state* is not itself a newly available **16-fermion exterior-power** state on the 16-dimensional CAR4 state space. The PURE/BASIS-INDEPENDENT/FUTURE-FAITHFUL no-return auditing TASK is not yet proved obligatory from M1; other instrument-dependent pure or mixed input preparations exist, and the allowed full physical native action alphabet can break the abstract U8×U8 covariance. This is **uniqueness within the defined closed, symmetric, pure all-sector audit** — it removes an arbitrary *mathematical selection* in the prior Slater proposal, not the actual physical price/admission of the newly required exterior-power register. Its real compiler, work, future tests, SourceI/Golden field map and complete clock remain open.

**Positive architectural implication:** the same native CAR16 supplies both:
1. the COMPLETE basis-free, two-branch canonical mathematical audit, and
2. the actual 128 fine record/future algebra that forbids discarding either parity sector, even though both contribute exactly equal Book scalar values.

This is a strong source-specific bridge between closed memory, CAR superselection, positive Book feedback and the proof architecture. But it does NOT derive the compulsory H+J+R or selected Palatini–CAR action from shortest physical code. Full D0→GR still needs the actual M1/B00–03 choice of the self-audit task and admissible native variation domain on one real full history. \`GR_closed=false\`.

## 6. Independent reproducibility and physical scope

The checker \`sources/d0_original_car16_two_mode_book_2026-10-25/check_two_mode_original.py\` rebuilds the ORIGINAL 32 duplicated Walsh row0 through the CAR creators, exact proper Lorentz boost \(U_r\) (not an imported quadratic model), and canonical 16D graded basis. It compares original 16D \(\Delta=a^\dagger a\) with (3)/(4) at several exact rational \(r,\nu\), checks both spectator CAR commutators, the 2×2 odd-block characteristic polynomial against BOTH rational functions (5), parity-switch \(\Gamma_2\), strict 16D 8+8 determinant/trace multiplicity, the radical-free Book source and its ORIGINAL first \(\theta\)-jet at \(r=1/9,\nu=3/5\).

Analytic §1–5 supplies the all-parameter proof; finite samples are regression controls, not the sole proof for the infinite family. No actual original 128 fine history or field-direction not in this proper-boost chart is erased/claimed covered.


## 7. THEOREM F — original prepared Book alone has a STRICT proper-boost source on the whole canonical positive interval

The radical-free formula (9)–(11) permits an exact sign theorem, with NO numerical eigenvector tracking or Newton root finder. Keep the original fixed phases, \(p=\varphi^{-1}\), \(\zeta=2^{-20}\), and the compact physical test chart
\[
\boxed{0\le r\le1/9,\qquad 0<\nu\le3/5.}\tag{17}
\]
Here \(s,t>0\) and the CAR contraction is strictly positive; the original \(r=1/9,\nu=3/5\) sits at its endpoint. The two rational invariants of (5) obey EXACTLY
\[
\boxed{
\begin{aligned}
\partial_rs&=\frac{\nu^2(1+r^2)(r^2+4r-1)}
{64(1-r^2)^3}<0,\\
\partial_rt&=\frac{2\nu^4(3r^4+14r^3-6r^2+18r-5)}
{16384(1-r^2)^3}<0.
\end{aligned}}\tag{18}
\]
The inequalities have elementary *rational interval proofs*: \(r^2+4r-1\le1/81+4/9-1<0\), and the second numerator bracket is at most \(3/6561+14/729+2-5<0\) after deleting the nonpositive \(-6r^2\). The invariants themselves satisfy
\(0<s<1/4\) and \(0<t<1\) throughout the chart, since
\[
s\le\frac{(9/25)\,6}{64(80/81)^2}
=\frac{177147}{5120000}<\frac14,\quad
t\le\frac{(81/625)\,26}{16384(80/81)^2}
=\frac{6908733}{32768000000}<1.
\tag{19}
\]
Put \(u=4\zeta p^2,v=4\zeta p^4\). The exact survival polynomial has derivatives
\[
\partial_s\mathfrak d=-u+2vs-uvt<0,\qquad
\partial_t\mathfrak d=-2v+u^2-uvs+2v^2t<0.
\tag{20}
\]
Indeed \(2vs=2up^2s<u/2\); moreover
\(\partial_t\mathfrak d\le v(-2+4\zeta+2v)<0\)
because \(v<4\zeta\) and \(12\zeta<2\).
Therefore
\[
\boxed{
\partial_r\mathfrak d
=(\partial_s\mathfrak d)(\partial_rs)
+(\partial_t\mathfrak d)(\partial_rt)>0,
\quad
D_\theta J_{\rm pre}
=-4(1-r^2)\frac{\partial_r\mathfrak d}{\mathfrak d}<0.
}\tag{21}
\]
Every inequality is strict for \(\nu>0\); at \(r=0\) all formulas have a regular one-sided derivative. This is a precise non-perturbative, all-boost **NO-GO for stationarity of the ISOLATED prepared full128 Book feedback** when this Lorentz direction is physically admitted. Neither a numerical fixture, a Dirac eigengap, the field source's sign, nor a scalar row fit is needed.

**Physical reading:** the authentic original closed memory's positive Book return gives a genuine source. To obtain an admissible D0→Einstein stationary action on a physical chart that permits this boost, other ACTUAL paid terms or derived physical constraints must account for that source. A matching-reference second arm MAY supply an opposite source, but doing so from a supplied reference choice is not yet forced by M1; genuine independent arm/controller rows must still close. Conversely, if the physical task does not admit this boost as an independent variation, (21) is not a failure of its own stationarity. It is a sharp guard against promoting the nice Slater no-return representation itself to the WHOLE selected D0 action.

The checker below verifies the exact analytic derivatives (18), rational bounds (19) and original source sign on multiple rational points. Its finite tests are supporting controls; the proof above covers the continuum interval.
