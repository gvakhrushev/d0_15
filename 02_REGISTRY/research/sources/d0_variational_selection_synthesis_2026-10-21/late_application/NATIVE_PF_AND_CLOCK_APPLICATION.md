# Actual Golden PF weights: weak material and finite clock application

21 October 2026. Bounded analytical composition in existing PR #334,
EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE, native-programme-v1.
Phase: native realization and source/refinement composition. This note
consumes the concurrent PF owner frozen from `c7e0c3d2` and the packet's
previously reviewed material and clock lemmas. It changes no native price,
primitive, field equation or historical numerical receipt.

**Exact parent substitution:** the actual original count-density sequence
below supplies the lower/weighted bound in `paid_source/PROOF.md` (8), and
the actual stored-edge perturbation supplies an `O(h)` transfer of the
finite clock commutator. Admission and payment of that sequence as one
physical process remain separate. `GR_closed=false`.

## 1. Inputs, carrier and normalization

The new inputs are the frozen
[original Golden PF regularity theorem](../late_inputs/02_REGISTRY/research/A4D_ORIGINAL_GOLDEN_PF_DISCRETE_C2_REGULARITY_AND_RANK2_MATERIAL_SOURCE_2026_10_21.md),
especially (1), (6)–(9), (13) and (16), and its consumed
[exact original-cell discrepancy theorem](../late_inputs/02_REGISTRY/gr_assembly/sources/d0_original_golden_moving_mean_j2_2026-10-19/theorem.md),
§§1–2. The consumers are the [weak material lemma](../paid_source/PROOF.md),
§2, and the [native clock bracket](../clock_bracket/PROOF.md), §§2–5.

Keep the literal original four-dimensional Golden box addresses, their
actual exact-cost counts `N_(n,z)`, and full CAR16 at every site. Let
`L>=4`, `h=1/L`, `p=phi^(-1)` and

\[
s(L)=\min\{s\in\mathbb N:\varphi^s\ge L\},\qquad
n_L=64s(L)+128,\qquad
\rho_{h,z}=\frac{L^4N_{n_L,z}}{F_{n_L+1}}.                 \tag{1}
\]

The `n_L` here is Golden address cost depth, not the attempted-round
horizon in the separate coherent-record input comparison. At each fixed
resolution the native counts and the common regular-trace level are fixed
on this field chart. They are not independently assigned site priors.

The consumed all-scale inequality is
`||rho_h-1||_infinity<9h^3`. Since `h<=1/4`,

\[
\boxed{\frac{55}{64}<\rho_{h,z}<\frac{73}{64},\qquad
\|\rho_h^{-1}\|_\infty<\frac{64}{55},\qquad
\|\rho_h^{-1}-1\|_\infty<18h^3.}                         \tag{2}
\]

The last bound uses `rho>1/2`; its slightly weaker constant is convenient
for the exact material estimate below. The same owner proves
`||nabla_h log rho||_infinity<36h^2` and
`||nabla_h^2 log rho||_infinity<72h`, but (2) alone suffices for our
weak material application and stored-edge perturbation.

### A density bound, not an absolute site-probability bound

The original regular weights have

\[
w_{h,z}=\omega_{N,n_L}N_{n_L,z},\qquad
\bar w_h=\frac{\omega_{N,n_L}F_{n_L+1}}{L^4},\qquad
\rho_{h,z}=w_{h,z}/\bar w_h.
\]

Their inverse-PF factor satisfies exactly `w_(h,z)/rho_(h,z)=bar w_h`.
This is the old source normalization, not a new division chosen to suppress
a source. The conditional Golden site probabilities are
`N_(n_L,z)/F_(n_L+1)=h^4 rho_(h,z)`; they have no positive lower bound
independent of resolution. Nor does (2) bound the absolute common regular
factor `bar w_h` from below. It bounds precisely the dimensionless density
appearing in the existing operands `f_h/rho_h` and `q_h/rho_h`.

These fixed count weights must not be identified with an arbitrary moving
input's Born probabilities, the full128 DATA invariant density, or a
field-dependent physical volume. Derivatives of those different objects
retain their actual preparation and transport terms.

The earlier discrepancy theorem (8)–(10) already gave `rho>=1/2`
eventually for a chosen schedule
`n(L)>=(16+gamma) log_phi L+C`, `gamma>0`. Thus the weak-bound premise
was already available for such a sequence. The original packet checker
did not consume that theorem. The present application supplies the missing
composition, with the new explicit all-`L` schedule and stronger bounds.

## 2. Actual weighted condition and the material estimate

Use exactly the same sigma-minus N=1 GoldenMaster after the required
canonical/null pullback. With its existing `tau>0` and `a=F_x(0,0)!=0`, put

\[
k_{\rho,z}=-\frac{F_y(-\tau f_{h,z}/\rho_{h,z},0)}a,
\qquad k_0=-\frac{F_y(0,0)}a,\qquad
\mathcal L=\sup\left|\frac{F_{yx}(x,0)}a\right|<\infty.   \tag{3}
\]

The supremum is over one compact strict operand interval containing all
arguments used below. This is the previous source-chart hypothesis; (2)
does not by itself certify a finite coarse mesh's operand admission.
Keep the same rank-two geometric representative and its actual scalar
current `V_A^r=g_h^{rs}D_s^+psi_A` in the source-compatible chart. Assume
the owned compact-slab bounds

\[
\|f_h\|_\infty\le C_fh,\qquad \|V_A\|_{2,h}\le C_V.       \tag{4}
\]

Here the positive auxiliary norm uses `h^d sum_z` and the Euclidean sum
over current components. The negative norm is dual to the forward-gradient
seminorm on variations vanishing on the full common collar; for a periodic
regulator use mean-zero tests, equivalently the quotient by constants.
These are not indefinite Lorentzian energy norms or a new raw216 norm.

The existing normalized nonlinear-minus-affine source, including its sign
and factor two, is

\[
R_A(\rho)=-2\sum_rD_r^-[(k_\rho-k_0)V_A^r],\qquad
\langle R_A(\rho),v\rangle_h
=2\langle(k_\rho-k_0)V_A,\nabla_h^+v\rangle_h.            \tag{5}
\]

There are no boundary terms under the stated test contract. Equations
(2)–(4) give the actual weighted estimate

\[
\|(f_h/\rho_h)V_A\|_{2,h}\le\frac{64}{55}C_fC_Vh.
\]

Substitution in the previously proved weak lemma yields

\[
\boxed{\|R_A(\rho)\|_{-1,h}
\le\frac{128}{55}\mathcal L\tau C_fC_Vh.}                \tag{6}
\]

This is an application to the actual original count-density sequence,
not a hypothetical smooth replacement of its generally unequal weights.
Any separate affine material error still has to be added to (5).

### The PF-only correction is smaller

For this comparison keep `f_h` and `V_A` fixed in the same transported
source chart, and define `k_1` by (3) with `rho=1`. Then

\[
|k_{\rho,z}-k_{1,z}|
\le\mathcal L\tau|f_{h,z}|\,|\rho_{h,z}^{-1}-1|
\le18\mathcal L\tau C_fh^4.
\]

Applying the identical summation-by-parts estimate to the difference gives

\[
\boxed{\|R_A(\rho)-R_A(1)\|_{-1,h}
\le36\mathcal L\tau C_fC_Vh^4.}                         \tag{7}
\]

This compares the PF part of the same source law; it is not a physical
replacement of the true weights by a uniform prior. If other fields,
currents or preparations change, their actual source differences must be
included. With a uniform componentwise current bound, the elementary
`||D_r^-||_(infinity->infinity)<=2/h` also gives a strong PF-only error
`O(h^3)`. For the original smooth rank-two current the consumed owner has
`R_A(1)=O(h)` for the corresponding nonlinear material row, hence its
native weighted row remains `O(h)`. This is not an exact finite root.

The former alternating `rho=1,2` fixture remains a valid warning about
positivity alone. It is incompatible with (2) along this particular
refining sequence and is not an obstruction to (6) or to this owner's
strong material consistency. No full42 stability/inverse follows.

## 3. Finite weighted-clock commutator bound

Consume the new PF owner's stored-edge estimate (16). On one fixed compact
family with uniformly bounded full CAR16 coefficients, proper exterior
edge maps and the required true adjoints, the original first-order edge
scaling and bounded number of neighbors give, in a common representation,

\[
E_h=D_{\rho,h}-D_{1,h},\qquad
\|E_h\|\le C_Eh^2,\qquad \|D_{1,h}\|\le C_Dh^{-1}.        \tag{8}
\]

The norm may be the positive `ell^2_h` operator norm. The same estimates
hold in the induced site-block infinity norm: each row has only a fixed
number of bounded CAR16 edge blocks. The finite density factors in (2)
also give uniform equivalence of the correctly transported weighted norms.
No growing trace multiplicity enters these operator-norm estimates.

Let `N,M` be bounded real scalar multiplication profiles on the same
spatial slice. The restriction of (2) to that slice preserves its bounds.
For the same finite matrix expression used by the clock lemma, set

\[
H_{\rho,N}=\tfrac12\{N,D_{\rho,h}\},\qquad
H_{1,N}=\tfrac12\{N,D_{1,h}\},\qquad
e_N=H_{\rho,N}-H_{1,N}.
\]

Then `||e_N||<=||N||_infinity C_Eh^2` and
`||H_(1,N)||<=||N||_infinity C_D/h`. The exact matrix identity

\[
[H_{\rho,N},H_{\rho,M}]-[H_{1,N},H_{1,M}]
=[e_N,H_{1,M}]+[H_{1,N},e_M]+[e_N,e_M]
\]

and `||[A,B]||<=2||A||||B||` prove

\[
\boxed{\|[H_{\rho,N},H_{\rho,M}]-[H_{1,N},H_{1,M}]\|
\le\|N\|_\infty\|M\|_\infty
       (4C_EC_Dh+2C_E^2h^4).}                           \tag{9}
\]

For fixed count weights and fixed lapse profiles, the new owner's
additional bounds `||D_yE_h||=O(h^2)` and
`||D_yD_(1,h)||=O(h^-1)` imply `O(h)` for the first field derivative
of this difference by differentiating the displayed identity. Moving
preparations, volume maps or lapse profiles need their own chain rule;
spatial difference bounds for the fixed counts do not control those jets.

### The true adjoint is part of the operator contract

Inequality (9) is an algebraic perturbation estimate. Calling these
matrices self-adjoint clock generators additionally requires the true
adjoint in the actual Hilbert/Gram representation. The literal weighted
stored shift can satisfy `S*!=S^-1` in counting coordinates; its positive
form `D*D` is not thereby `D^2`. The new positive-form estimate does not
prove self-adjointness of that literal stored `D` or select it as a clock.

When the actual representation is the already-owned passive transport
`D_rho=U_rho^-1 D_1 U_rho`, the states, inner product and adjoint must all
be transported together. Lapse multiplication commutes with `U_rho`, so
both the anticommutators and their bracket conjugate exactly. This exact
case is consistent with (9), but the general stored-edge bound does not
assert that every physical density variation is such a passive change.

## 4. What transfers to the continuum clock formula

On the previous flat identity-link/constant-spatial-frame chart, keep its
actual one-sided native stencil, full CAR16 and
`{alpha^i,alpha^j}=2q^{ij}I`. The owned smooth bracket limit is

\[
\mathcal B_{N,M}
=-\left(V^j\partial_j+\tfrac12\partial_jV^j+\Omega\right),
\quad V^j=q^{ij}(N\partial_iM-M\partial_iN),\quad
\Omega=\tfrac14[\alpha^i,\alpha^j](\partial_iN)(\partial_jM).
\]

For bounded `C^4` profiles and spinors on a compact region with the
larger common collar, the prior theorem gives
`||([H_(1,N),H_(1,M)]-B_(N,M))f_h||<=C h||f||_(C^4)`.
Combining it with (9) proves the same `O(h)` estimate for the actual
weighted stencil on schedule (1). In `ell^2_h` this follows also by
integrating the previous uniform estimate over the fixed finite volume;
the bounded-degree estimate above preserves its block-infinity version.

The two scopes are different: (9) compares two finite lattice matrices
uniformly over their grid modes, whereas their continuum differential
comparison still requires smooth test data. It does not give uniform
continuum operator convergence at Nyquist frequency. The original
one-sided `O(h)` defect and its spin term are retained.

The actual PF weights are spatially unequal, so this application is not
a replacement by one translation-invariant Fourier block. Conversely,
the separate coherent-input Fourier calculation does not prove an
all-space price or variable-frame clock identity. The estimate (9)
continues to compare the two operators on a bounded variable-frame/link
family, but the unweighted continuum comparator there must retain its
own frame and connection terms. The constant-frame formula above cannot
be silently reused on that different chart. No canonical gravity
constraint algebra or dynamical metric is obtained from this estimate.

## 5. Paid depth, remaining application and author scope

The depth (1) is a specific finite schedule of original Golden histories.
It is not a newly varied continuous coupling or a proof that the native
physical choice law selects that schedule. The constants `C_f,C_V`,
`mathcal L,C_E,C_D` are uniform bounds on the stated compact charts, not
adjustable source-cancellation terms. The source's existing `p,tau`,
normalizations and clock convention remain fixed. Its real address cost,
trace-level enlargement, preparation, retained histories, routing and
work must be admitted and paid; a measured prefix Cost-minus-entropy
identity does not price the entire apparatus.

Likewise, an unnormalized full Book trace can amplify a small operator
error by its growing dimension. The new PF owner's separate trace-source
estimate and deeper schedules retain that factor. Equation (9) alone
does not prove a vanishing complete Book price/source defect.

This application discharges the specific normalized-PF/weighted-flux
premise for this native sequence and the finite weighted-clock
perturbation estimate. The complete selected Book03 process, independent
input/writer/clock equations, actual coupled gauge/collar inverse and
physical field refinement remain open.

**Author scope note.** This is a direct analytical composition of frozen
owned inequalities with the existing summation-by-parts lemma and an
exact three-term matrix commutator identity. No new numerical suite,
history enumeration or factory replay was run. Historical `RESULT.json`
files and pinned reviews are unchanged and are not presented as checks
of this newly added consumer. Independent review of this application is
separate. Write paths for this subtask are this note and the historical
PF-premise clarification in `../paid_source/PROOF.md`; integration and
frozen-source manifests remain with the packet owner. `GR_closed=false`.
