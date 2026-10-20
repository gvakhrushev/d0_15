# D0 → GR: NULL-BRINKMANN SOURCE GAP AND THE UNIQUE MATCHED-HISTORY COCYCLE

**20 October 2026. Existing parent [#334](https://github.com/gvakhrushev/d0_15/pull/334), `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`. Research synthesis / exact finite analytic theorem + a canonical conditional resolution.**
Phase: `constitutive / native_sector / gr_operational_realization`.
No new action, registered task, compulsory physical selector, BOOK/CORE/assembly promotion or `GR_closed` claim.

## The scientific decision

There is ONE fixed original geometry on which the two central D0 gravity
routes disagree: the **flat, constant-H member of the exact nonlinear
Einstein–CAR Brinkmann family already integrated to main**, with original
coframe scaling v=h e, old16 fullCAR site modes, same Lorentz null links
and independent coframe Euler directions.

The bare full conditional H+J+R carries a NONZERO source in the **same
null Brinkmann H direction**, even though the original configured
Golden-J2/Palatini/Einstein source vanishes exactly. The directional
source is extensive O(L⁴), survives mesh refinement at finite
nonzero density, and is NOT a volume-only/cosmological pressure: the
deformation fixes the full coframe and metric determinants exactly.

A reference-matched two-history scalar **cocycle** instead cancels
all coframe-only flat source rows to ALL orders at the diagonal.
If it preserves the original dynamical link derivative, that
cocycle is UNIQUE when its value is zero on every reference diagonal.
This supplies a canonical **mathematical** shape of the required
relative native source rather than a counterterm tuned to Einstein.
Actual physical execution/selection, positive records, code/clock
cost and curved source matching remain to be proved.

## 1. This is EXACTLY the original Brinkmann null deformation

Use the original physical null metric and unwrapped local coframe in
the main [exact 40→3→1 all-Euler result](../gr_assembly/sources/d0_double_null_quadratic_cartan_2026-10-19/arbitrary_brinkmann_all40.md)
and the [same fixed Einstein family](D0_GR_PRIMARY_POSITIVE_CASE.md).
For every integer L>=4, h=1/L, use the original based links U_r=I,
constant original scalar/top CAR amplitudes and a constant observer
n=(e_++e_-)/sqrt(2). The observer-induced positive fibre makes the
internal four reference vectors (e_+,e_-,e_2,e_3) orthonormal even though
the *physical Lorentz metric* has eta_(+,-)=1 and eta_22=eta_33=-1.

On ALL original finite site/coframe variables, take

\[
v_u(t)=h(e_++t e_-),\quad v_v=h e_-,\quad
v_x=h e_2,\quad v_y=h e_3,\qquad U_r=I.
\tag{1}
\]

The same ORIGINAL physical geometry has

\[
g_t=2du\,dv+2t\,du^2-dx^2-dy^2,\quad
H=2t,\quad \det e(t)=1,\quad\det g_t=-1.
\tag{2}
\]

All Christoffels vanish in these constant coordinates, so
\(\operatorname{Riem}(g_t)=0\) for EVERY real t.
On the actual original Palatini six based faces P=I and
f_i(e,U)=0. Its complete 16 coframe and 24 proper-link Euler rows
are all zero, including this variation. With constant CAR matter,
the configured Golden-J2 + star all40+2 source is zero at each h.

**This is not a new geometry.** It is precisely the *constant H*
subsector of the already main-published nonlinear GR witness.
It is also a volume-preserving, internal-null coframe shear.
At fixed lattice, the full local Diff interpretation has not
yet been proved: a shear of the physical continuum coordinates
does not automatically act on the discrete site translation algebra.
None is assumed in the source test.

## 2. Exact same-CAR full-HJR source at the physical h scale

Use the **unchanged** conditional full-Lorentz positive-adjoint
\(\mathsf H+\mathsf J+\mathsf R\) from
[A4D_EXACT_CURVED_WHOLE_HJR_FIXED_COLLAR_ROOT_2026_10_20.md](A4D_EXACT_CURVED_WHOLE_HJR_FIXED_COLLAR_ROOT_2026_10_20.md).
All 16L⁴ CAR/site modes, the entire thermal complement,
the true global normalizer, feedback multiplicity128,
all proper-link domains and the full fixed-right rank128
Riesz preparation remain in the action.

The exact full16 Clifford square on (1), with the genuine shifted
positive adjoint, is

\[
\begin{aligned}
\Delta_h(t,k)&=\mu(k)+2t\,\Re(\bar z_u z_v)
                       +t^2|z_u|^2,\quad
 z_r=e^{2\pi i k_r/L}-1,\\
\mu(k)&=\sum_r |z_r|^2
=\sum_r(2-2\cos(2\pi k_r/L)).
\end{aligned}\tag{3}
\]
Each eigenvalue has **multiplicity16**, no Fock grade discarded.
At t=0 the original isolated Riesz preparation occupies precisely
the eight first nonzero momenta times all16 CAR grades.
Its Rayleigh FIRST derivative in t vanishes, because every
occupied momentum has at most one nonzero coordinate.

Keep original p=phi^-1, zeta=2^-20,
alpha=p²/(128L²), m=256L², beta=m alpha=2p².
Write b_k=1-alpha mu(k), w_k=b_k^m,
Q_L=sum_k w_k, F_k=1-zeta+zeta w_k. Differentiate the
**complete original** action \(\log(C\,16Q_L)/\beta
-2048\sum_k\log F_k+R_{\rm Riesz}\).
The exact source is

\[
D_t S_{HJR,L}|_0
=\sum_k 2\Re(\bar z_u z_v)\,
 b_k^{m-1}\left(\frac{2048\zeta\beta}{F_k}-\frac1{Q_L}\right).
\tag{4}
\]

Because every other factor is even under each independent
k_r→−k_r, the \(\sin k_u\sin k_v\) contribution cancels
**AFTER the full momentum sum**, not by changing the Dirac
operator. Hence the exact finite formula is

\[
\boxed{
D_t S_{HJR,L}|_0
=2\sum_k (1-\cos\theta_u)(1-\cos\theta_v)\,
 b_k^{m-1}
 \left(\frac{2048\zeta\beta}{F_k}-\frac1{Q_L}\right).
}
\tag{5}
\]

The H term carries its true \(-1/Q_L\), the complete 128x16
feedback trace its positive source, and the moving
reference128 R term its real zero first shear.
This is the full conditional HJR source, NOT
a prechosen Einstein action.

### Exact all-L lower bound, including the finite chart

For EVERY L>=256, using the original calibration
3/8<p²<2/5 and 3/4<beta<4/5, the elementary estimate
\(-\log(1-x)\le x/(1-x)\) proves uniformly

\[
b_k^m >e^{-13}>1/500000,\quad Q_L>L^4/500000,
\quad b_k^{m-1}>1/500000.
\]
The last rational exponential bound follows from
\(e<68/25,\ (68/25)^{13}<500000\).
Since F_k<=1 and 2048 zeta beta>3/2048,
the entire bracket in (5) satisfies

\[
\frac{2048\zeta\beta}{F_k}-\frac1{Q_L}
>\frac3{2048}-\frac{500000}{L^4}>0.
\]
Finally \(\sum_k(1-\cos\theta_u)(1-\cos\theta_v)=L^4\)
for every L>=2. Thus

\[
\boxed{
\frac1{L^4}D_t S_{HJR,L}|_0
>\frac{2}{500000}
\left(\frac3{2048}-\frac{500000}{L^4}\right)
\ge\frac{180983}{33554432000000}
>\frac1{200000000}>0
\quad(L\ge256).
}
\tag{6}
\]

As H=2t, the ACTUAL original Brinkmann H-source per site
is \(D_H S/L^4 >1/400000000\).
Translation invariance and the Riesz envelope identity
give the SAME nonzero coframe Euler source at
**each original site** when the corresponding local H
coframe leg alone is varied. Thus the configured
Einstein vacuum and the bare HJR action do not share
even this one exact native Euler equation.

### Analytic continuum limit, independent special functions

The thermal/source H term stays O(1), the
reference128 R derivative is identically zero, and
the J source has O(L⁴) summable Bloch density.
Therefore

\[
\boxed{\displaystyle
\lim_{L\to\infty}\frac1{L^4}D_t S_{HJR,L}|_0
=
4096\zeta\beta\int_{\mathbb T^4}
\frac{(1-\cos\theta_u)(1-\cos\theta_v)
 e^{-\beta\mu(\theta)}}
{1-\zeta+\zeta e^{-\beta\mu(\theta)}}\,
\frac{d^4\theta}{(2\pi)^4}
=8.2006044369077622175\cdot10^{-6}>0.
}\tag{7}
\]

The integral is manifestly positive on an open set.
The independent exact convergent Bessel expansion uses
\(I_0,I_1\), \(c=\zeta/(1-\zeta)\):
\[
\frac{4096\zeta\beta}{1-\zeta}
\sum_{n\ge0}(-c)^n e^{-8(n+1)\beta}
 I_0(2(n+1)\beta)^2
 [I_0(2(n+1)\beta)-I_1(2(n+1)\beta)]^2.
\tag{8}
\]
No finite-L extrapolation proves the sign; (6) and
the positive integral do.

**Hard interpretation:** an arbitrary cosmological/volume-only
term \(V(\det e)\) has identically ZERO derivative along (1),
and therefore cannot cancel (5). Fixing the volume
(unimodular constraint) also does not exclude (1).
This is an **actual null-Brinkmann flat-source anomaly
of the BARE conditional price at fixed site registration**,
not only the common radial source in the previous HJR theorem.
A compensated observer/transported site/readout change is a
different physical variation and needs its actual source.

## 3. The UNIQUE source-preserving relational replacement

Let \(\mathcal A_h(e,U,\mathrm{internals})\) denote the FULL
specific one-arm price of a physically supplied native
programme, with its actual clock, preparation, reference,
history and work charged (these inputs are not defined by
the HJR spectral formula alone). Suppose a **genuinely
admitted** matched flat comparison arm \(U_0\) exists,
with the SAME e, observer and explicitly transported
oldRIGHT/preparation/clock data.

On a connected smooth chart of allowed U, define

\[
\boxed{\mathscr C_h(e;U,U_0)
=\mathcal A_h(e,U)-\mathcal A_h(e,U_0).}
\tag{9}
\]

Exact, to all orders:
\[
\begin{aligned}
&\mathscr C_h(e;U,U)=0,\qquad
\mathscr C_h(e;U,V)+\mathscr C_h(e;V,W)
=\mathscr C_h(e;U,W),\\
&D_e\mathscr C_h(e;U,U_0)|_{U=U_0}=0
\quad\text{for all 16 coframe directions},\\
&D_U\mathscr C_h=D_U\mathcal A_h,\qquad
D_eD_U\mathscr C_h=D_eD_U\mathcal A_h
\quad(U_0\text{ independently retained}).
\end{aligned}
\tag{10}
\]

**Uniqueness theorem (not a choice of counterterm):**
If any \(\widetilde{\mathscr C}_h(e;U,U_0)\) has
the SAME complete link derivative as \(\mathcal A_h(e,U)\)
for every U in that connected chart, and is exactly
zero when U=U_0 for every e,U0, then
\(\widetilde{\mathscr C}_h=\mathscr C_h\).
Proof: their difference in U is constant on each
connected chart; evaluation at U=U0 fixes that constant.
The additive identity then holds automatically.
If only coframe differential vanishing is required rather than zero value,
the general solution is (9) plus `c(U_0, held internals)`: integration in e
does not eliminate dependence on an independently retained reference.
Exact zero diagonal for every reference fixes this term to zero, as does
the full pair-cocycle identity. A globally field-independent constant
requires the corresponding reference/internal derivative conditions too.
Source preservation here is a partial derivative at independently held
reference/internals. If a physical matching map moves their preparation,
observer or clock with active U, their actual chain-rule sources remain
until joint internal stationarity or an explicit cancellation is proved.

Thus **one** relative comparison of the FULL original
price automatically cancels its entire one-arm
volume/shear/flat metric pressure at U=U0, WITHOUT
dropping even a single thermal or CAR mode, fitting
the 8.2e-6 coefficient or altering link/mixed coframe-link
variation. It supplies the precise missing
**reference-source subtraction**, conditional on its
actual operational admission and full payment.

### Gauge and probability qualifications

\(U_0\) must be a **retained flat reference connection**,
not silently reset to numerical identity after an
arbitrary local Lorentz gauge transformation. Under
a common physical frame change both U and U0 and
their coframes/observers/references transform together.
If the original complete scalar action is covariant
under that actual map, the difference is covariant.

Writing \(-\log_\varphi[w(U)/w(U_0)]\) is legitimate
as (9) only after identifying \emph{real unnormalised
original} weights \(w=\varphi^{-\mathcal A_h}\).
For separately NORMALIZED Born probabilities
\(q_U=w_U/Z_U\) the score has an additional true
\(\log_\varphi(Z_U/Z_{U_0})\) term. It cannot be discarded
by calling the readout 'relative'. Direct/return histories,
comparison attempt clocks, complement flags and oldRIGHT
remain full physical records. Reference subtraction
is NOT free work and is not proved to be the
compulsory physical selector by algebraic uniqueness.

## 4. The native signed source needed AFTER pressure removal already exists as representation

Read the existing #334
[A4D_NATIVE_JONES_CAR16_TOP_GOLDEN_RELATIVE_PALATINI_2026_10_20.md](A4D_NATIVE_JONES_CAR16_TOP_GOLDEN_RELATIVE_PALATINI_2026_10_20.md).
The original grade-four CAR saturation on one vacuum/top
pair is EXACTLY the oriented old face:
\[
C_B C_{\mathcal R(P)}
=-{\cal P}_\star(B,P)|top\rangle\langle vac|.
\tag{11}
\]
The ALREADY owned nonorthogonal Jones p³ pair
with FULL GOOD/BAD Golden flag-dephased densities
has an explicit positive two-history log-odds mixed source
equal to the literal star Palatini face (owner §7).
No external Hodge matrix or arbitrarily fitted Einstein
coefficient is required for this representation.

The earlier
[A4D_NATIVE_PAID_SOURCE_AND_PAIRED_FEEDBACK_SYNTHESIS_2026_10_20.md](A4D_NATIVE_PAID_SOURCE_AND_PAIRED_FEEDBACK_SYNTHESIS_2026_10_20.md)
also constructs the inverse-paired CAR16 positive
feedback with flat curvature-only leakage eliminated
and a concrete full six-direction \(c_{\rm pair}df_\star\)
source at leading smooth order. **Neither constructed
tester is automatically the original compulsory
full128/HJR/Book physical price**.

The genuinely new SYNTHESIS is therefore structural:

\[
\begin{array}{c}
\text{original retained verification + TWO paid histories}\\
\downarrow\quad \text{matched reference groupoid cocycle}\\
\text{automatic elimination of absolute flat
coframe pressure at ALL mesh sizes}\\
\downarrow\quad\text{native top-CAR/Jones orientation
source on same programme}\\
\text{signed }(e\wedge e)\cdot{\cal R}(P)
\text{ finite Palatini differential}\\
\downarrow\quad \text{existing original 40→3→1,
source, exact curved family and midpoint recovery}\\
\text{nonlinear Einstein–null-CAR sector, if
the complete programme actually selects the source}.
\end{array}
\tag{12}
\]

There is **no permission** to identify the two
separately constructed mathematical instruments or
to declare their source sum the full native action.
The missing source map is now one precise two-history
same-execution identification, not a new geometry
or rank study.

## 5. The single decisive same-programme condition

On the finite FULL original oldRIGHT/ref128/CAR16
Brinkmann carrier and the ACTUAL paid native
complete programme, decide whether a matched
old-archive preserving pair of reference/active
histories with one shared coframe+observer exists
whose full Cost−Info source satisfies:

1. **Full reference diagonal:** for every e,
   \(\mathscr C(e;U_0,U_0)=0\), including *all*
   recorded work and clock terms; so local H
   source on the flat null line is zero, not
   the proven bare HJR value (6).
2. **Signed source, no inserted geometry:** on
   original six based plaquettes, the actual
   coframe/link/matter preparation source of
   that SAME programme has the existing
   Jones/top-CAR \(\star\) response, with
   a real selected normalization and all
   16+24+2 independent Euler rows.
3. **Native selection and refining realization:**
   original admissibility and prospective
   Cost−Info/continuation or equation-equivalent
   law really chooses that paid paired programme,
   and its source/refinement error is controlled
   on the exact main GR solution family.

PASS would feed the existing positive GR
composition in the correct category. FAIL would
exclude this exact two-arm physical route,
not the already-proved configured geometric
Einstein solutions. **At present this
same-programme premise is UNPROVED.**

## Reproducible evidence and retained scope

`python3 02_REGISTRY/research/sources/d0_hjr_flat_density_zero_2026-10-20/check_brinkmann_reference_cocycle.py`

The checker validates the ORIGINAL physical null
coframe/metric identity symbolically, the
exact rational all-L pressure bound, independent
high-precision Bloch/Bessel continuum values,
full 16L⁴ HJR action-level directional finite
differences at seven original L, and algebraic
cocycle/source-preservation equations. It
does not pretend those finite matrices
prove physical native admission, external
review or general GR.

**Status:** source incompatibility of **BARE**
HJR with the SAME flat member of exact
Golden-J2/Einstein family PROVED for the declared
conditional operator and L>=256.
Unique comparison correction proved **inside
the declared additive link-source preserving
class**. Original native selector and full
physical D0→GR remain OPEN, as does raw216.
