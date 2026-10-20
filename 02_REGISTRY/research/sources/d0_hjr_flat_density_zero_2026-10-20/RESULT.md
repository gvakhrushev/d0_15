# Original H+J+R: flat-holonomy coframe source outside the pure Palatini-density ideal

20 October 2026. **Bounded research subresult inside existing Draft #334**, task
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`.
Consumer: the existing `constitutive` / `native_sector` / `contrast_refinement_transfer`
application of the nonseparable density-pullback theorem
[`d0_native_gr_universality_2026-10-20/RESULT.md`](../d0_native_gr_universality_2026-10-20/RESULT.md).
There is no new action, task, claim/status promotion, physical selector or GR terminal.

## Question and exact answer

The recently proved local coframe-change theorem states that an *already
identified* geometric full action of the form `F(f_1,...,f_m)`, with the original
homogeneous six-face Palatini site densities `f_i` and nonzero first derivatives,
is locally exactly equivalent to a weighted Palatini star. **Does the original
conditional full `H+J+R` spectral price automatically have that form?**

**No**, even on a legitimate nondegenerate constant-coframe, flat-proper-link
chart. The *whole* original `H+J+R` has a nonzero coframe derivative on a
curve where *every* `f_i=0` identically. This is an obstruction to applying the
density-only factorization theorem to the bare complete conditional `H+J+R`
off shell, not a no-go for the theorem, for the original D0 programme, for
additional genuinely paid native work, or for positive GR.

## Original finite carrier and unchanged action

Take the maintained whole-price owner
[`A4D_EXACT_CURVED_WHOLE_HJR_FIXED_COLLAR_ROOT_2026_10_20.md`](../../A4D_EXACT_CURVED_WHOLE_HJR_FIXED_COLLAR_ROOT_2026_10_20.md),
equation (1), including its original true positive adjoint and *all* site/CAR
modes. Fix its unmodified constants

\[
L=8,\quad h=\ell=1/8,\quad p=(\sqrt5-1)/2,\quad
\alpha=p^2h^2/128,\quad M=16384,\quad
\beta=M\alpha=2p^2,\quad z=2^{-20}.
\]

Use every `L^4=4096` site and all 16 CAR modes: `N=65536`. Keep the
original complete positive action, original normalizer, and a field-independent
workspace factor `C` in the declared experiment:

\[
d=h^{-1}\sum_{r=0}^3 C(v_r)(\Lambda(U_r)S_r-I),\quad
\widehat D=d+d^\dagger,\quad \Delta=\widehat D^2,
\]
\[
B=I-\alpha\Delta,\quad Z=\operatorname{Tr}_{H}B^M,\quad
F=1-z+zB^M,
\]
\[
S={\log(CZ)\over\beta}
 -128\operatorname{Tr}_{H}\log F
 +\operatorname{Tr}(P^*\Delta P).
\tag{1}
\]

Set **all actual proper Lorentz links** `U_r=I`. Choose the invertible
constant frame and fixed rest observer

\[
v_r(s)={s\over4}e_r,\qquad 0<s<s_*.
\tag{2}
\]

The CAR realization stays full and the true shifted adjoint is used.
Sufficiently small `s>0` respects the strict positivity and Julia window.
The eight minimal nonzero momenta (`q=±e_r`) and all 16 CAR grades form
the **complete isolated rank-128 spectral shell** for each `s>0`.
Taking `P` to be its original rank-128 Riesz preparation normalized so
`P^*P=I_{128}/128` gives exactly the fixed-right preparation Euler
condition; no spectral complement is deleted. (No full geometric Euler
or prospective optimality is imposed.)

All based plaquettes equal identity at `U=I`. Therefore

\[
f_i(v(s),U=I)=0
\qquad\text{for every original site }i
\quad\text{and every }s>0.
\tag{3}
\]

## Exact full spectrum and the transverse first jet

Let `u=s^2`. On the original entire CAR/site space,

\[
\Delta(s)=u\Delta_0,\qquad
\lambda_0(q)=4\sum_{r=0}^3(2-2\cos(2\pi q_r/8)).
\tag{4}
\]

The entries `2-2cos(2*pi*k/8)` for `k=0,...,7` are exactly
`0, 2-sqrt(2), 2, 2+sqrt(2), 4, 2+sqrt(2), 2, 2-sqrt(2)`.
Their direct fourfold convolution with multiplicity 16 proves

\[
\operatorname{Tr}\Delta_0=2,097,152,\qquad
{\operatorname{Tr}\Delta_0\over65536}=32,\qquad
\lambda_{\rm occ}=8-4\sqrt2,\qquad
\operatorname{rank}P=128.
\tag{5}
\]

The original preparation term on this **actual** stationary fixed-right
spectral shell is `R(u)=u lambda_occ`. Inserting (4) into the *entire*
action (1) yields an analytic function for `u>0`, with a one-sided
analytic extension to `u=0` (which is used only to compute a derivative,
**not** as an admitted invertible coframe or an occupied separated shell):

\[
S(u)=
{\log\!\left(C\sum_\lambda(1-\alpha u\lambda)^M\right)\over\beta}
-128\sum_\lambda\log\!\left(1-z+z(1-\alpha u\lambda)^M\right)
+u(8-4\sqrt2),
\tag{6}
\]
where both sums retain all 65,536 eigenvalues with multiplicity.
Differentiating the true `log Z`, `log F`, and original `R`, with
`M\alpha=\beta`, gives

\[
\begin{aligned}
\lim_{u\downarrow0}S'(u)
 &= -{\operatorname{Tr}\Delta_0\over65536}
  +128z\beta\operatorname{Tr}\Delta_0+(8-4\sqrt2)\\
 &= -32+256(3-\sqrt5)+8-4\sqrt2\\
 &=\boxed{744-256\sqrt5-4\sqrt2>162>0}.
\end{aligned}
\tag{7}
\]

The final strict bound uses only `sqrt(5)<9/4` and `sqrt(2)<3/2`.
Continuity now proves `dS/ds=2sS'(s^2) != 0` for an open interval of
strictly **positive**, invertible coframes. This is not merely a spurious
derivative at the singular `s=0` chart boundary.

For example the independent complete-trace checker evaluates
`S'(0.01^2)=165.382513783...` directly. This real-point numeric value
is diagnostic; the nonzero theorem is equation (7).

## Consequence: precise failing substitution, not a replacement theory

Any `C^1` function of **only** the original Palatini site densities,
`F(f_1,...,f_m)`, plus a *field-independent constant*, is constant on
(2) by (3). Its coframe derivative along that same path is exactly zero.
Equation (7) contradicts equality of either the full actions or their
coframe first jets there. Consequently:

* The existing nonseparable-density coframe pullback remains a valid
  **conditional** theorem; it cannot be applied **unconditionally** to
  the unchanged full conditional `H+J+R` off-shell price.
* The full spectral pressure already carries an independent native
  **flat-holonomy coframe source**. Calling the six-face readout its sole
  geometric dependence erases a real original contribution.
* The signal is not supplied by a contrived penalty, a fitted matter
  stress, a dropped CAR complement, a frozen normalizer, or a surrogate
  determinant. The true full H and J terms and original stationary
  reference128 R are all present.
* This is only a *one-direction necessary-condition counterexample* on
  the specified conditional action and source chart. It does **not**
  exclude a legitimate additional preparation/work/clock/history action,
  a specially proved on-shell source cancellation, a structural
  field-dependent native operation, or an equation-equivalent physical
  realization on a different admitted sector. It also does not assert
  the present conditional HJR is the compulsory selected D0 action.
* The newer exact curved **fixed-collar** HJR roots are unaffected: they
  are solutions of the actual full conditional source, not of the
  density-only Palatini formula. Their independent saddle/selection
  boundary also remains unchanged.

## Next physical substitution

Before the `gr_operational_realization` consumer can use the nonlinear
Palatini coframe-dressing theorem on the **same** admitted programme, it
must derive the actual full off-shell decomposition (or a proved
equation-level alternative), preserving the nonzero flat spectral source
of (7). In particular test, on one genuine common preparation and its
actual admitted tangent space,

\[
 D_eS_{\rm full}\big|_{f=0},\quad
 D_e S_{\rm prep/work/clock/history}\big|_{f=0},\quad
 D_eS_{\rm structural\ operations}\big|_{f=0},
\]

including the preparation Schur where internal variables are eliminated.
Check the complete original 16 coframe + 24 proper-link rows, source
normalization, observer equations and history/clock records. A cancellation
must follow from the same true full price and same preparation, never by
subtracting a fitted flat pressure. Alternatively prove physical equivalence
of on-shell covectors under a specified invertible map with all hypotheses.

**State:** conditional HJR density-only factorization is excluded on this
flat-holonomy chart; `constitutive`, `native_sector`, `GR`, and the original
`raw216` terminals remain OPEN.

## Reverse-synthesis: one missing native price, two independent tests

The new [complete-flag/native-minimum packet](../../A4D_COMPLETE_FLAG_SOURCE_AND_NATIVE_MINIMUM_GATE_2026_10_20.md),
section 5, proves a *different* necessary condition on the exact curved fixed-
collar critical family of the same conditional whole H+J+R. There, an
admissible nongauge bulk tangent v has

\[
D^2 S_{\mathrm{HJR}}[v,v]\in
[-2372501681/32000000000,\,-2372493199/32000000000]\subset(-.074141,-.074140).
\tag{8}
\]

To keep that same critical point as a physical local minimum for an *actually
derived* full-price completion `S_full=S_HJR+E`, **if** this same v is
physically admitted and the new action is C2, it is necessary that

\[
dE=0\ \text{at the original curved root},\qquad
D^2E[v,v]\ge 2372493199/32000000000.
\tag{9}
\]

This condition is quoted at the exact scoped fixed-L8 critical point, not
asserted uniformly in `h`, and it is distinct from the present flat test.
On the separate flat-holonomy family, if one requires the *whole completed
action itself* to be a function of Palatini densities only, the same extra
price must instead obey the first-source cancellation

\[
\lim_{u\downarrow0}\frac{dE}{du}
=-744+256\sqrt5+4\sqrt2
\tag{10}
\]
whenever this limit exists, or pointwise `E'(u)=-S_HJR'(u)` on every
included positive-`u` segment. If the actual physical target contains
other fields/terms, or only an equation-level transported equivalence is
claimed, use its **derived** source instead; (10) is not imposed on those
other hypotheses.

Equations (9) and (10) are **two separate necessary tests at two different
configurations**, not a proposed functional `E`. They make the next
`constitutive` verification finite and discriminating: derive the one
complete native preparation/controller/clock/history/work price without
post hoc tuning; evaluate its flat first jet **and** the existing curved
negative-Hessian direction, with actual admission and source maps. Only
after those gates does the existing nonlinear field/refinement argument
have a candidate to consume. No new selector or Einstein equation is
smuggled into the source.

## Smallest decisive replay

Run `python3 check_flat_source.py` in this directory. Standard-library-only
code independently enumerates the full exact `Z[sqrt(2)]` spectrum with
multiplicities, checks trace and occupied-shell rank, verifies the radical
identity (7) and its strict bound, and calculates complete unmodified
`H+J+R` action and derivative at seven genuine nonzero coframe scales.
No certificate/claim registry or source-owner theorem is modified.
