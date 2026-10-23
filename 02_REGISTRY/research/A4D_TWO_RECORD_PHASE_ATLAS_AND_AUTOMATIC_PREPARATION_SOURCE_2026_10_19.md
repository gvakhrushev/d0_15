# Two independent retained records: a full Lorentz scalar-phase atlas and the preparation source already inside the comparison

19 October 2026. Same scientific execution and Draft #334,
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`.
Input `90fc38d972cc8538ce6fff2912906a496733c097`.

**20 October integration:** latest consumed source
`d533539ba87aaddb567efa84beba765f608af296`. Its
[native-Golden three-density owner](A4D_NATIVE_GOLDEN_P_COMPLETE_CAR_CLOSED_HISTORY_SIX_PHASE_AND_PREPARATION_2026_10_19.md)
has ALREADY proved six scalar phases, moving preparation and no
interhistory/flag coherence requirement at the original primitive p.
Those are consumed results, not claimed as new here. The additional
theorem below uses TWO output densities and a fixed CAR effect, derives
the general flag-probability determinant and its exact balanced-flag
failure, and specializes to original p without an auxiliary normalization.
Sections 2–6 preserve the original 1/2-scale control; §§5.1–5.2 and 7.1
state the current native and cross-front consumers.

**Positive correction of the parent criterion.** The previous
[phase-integrability theorem](A4D_TWO_HISTORY_PHASE_HELMHOLTZ_AND_NATIVE_ACTION_GATE_2026_10_19.md)
correctly excludes replacing a scalar-action differential by a curved
diagonal one-arm Berry covector. It does not exclude the differential of
the COMPLETE closed comparison. We now construct that differential on the
same CAR16 and the already-owned Julia instrument. The missing preparation
component appears automatically. More strongly, the construction survives
complete GOOD/BAD dephasing and gives six locally independent SCALAR phase
coordinates from the same two native probe preparations and six existing
CAR anchor operators. Neither relative global-phase coherence between whole
histories nor an integrable one-arm connection is necessary for this readout.

This is an observable/source-composition theorem, not selection of the
physical Book price. The relevant measuring criterion changes; the full
D0-to-GR theorem remains open.

## 1. Which condition was too strong?

Book03 §§03.3.0–03.3.2 starts with the complete weighted history/memory sum
and its finite action. It does not identify its differential with
`alpha=-i<chi,dchi>` for one output family. That alpha is a connection
one-form, and its curvature can be nonzero. Its nonclosure is an obstruction
ONLY to the specific substitution `alpha=dS`.

For three normalized rays with nonzero pair overlaps, the existing
closed comparison is instead

\[
 B=\langle\chi_0,\chi_1\rangle
   \langle\chi_1,\chi_2\rangle
   \langle\chi_2,\chi_0\rangle,
 \qquad S=\operatorname{Im}\log B.
 \tag{1}
\]

On any nonzero branch its WHOLE source is

\[
 dS=\operatorname{Im}\sum_{(i,j)=(0,1),(1,2),(2,0)}
 \frac{\langle d\chi_i,\chi_j\rangle+
       \langle\chi_i,d\chi_j\rangle}
      {\langle\chi_i,\chi_j\rangle}.
 \tag{2}
\]

Both endpoint derivatives matter. Independent field-dependent ray phases
cancel in (1), and therefore in all its source jets. Equation (2) is closed
because it is the differential of an actual scalar, not because each ray's
Berry curvature vanishes. The following exact construction demonstrates
the distinction on the original carrier, rather than invoking it abstractly.

## 2. The complete original Julia comparison supplies the preparation term

Keep all exterior grades of CAR16 and the original grade-one vectors

\[
 a=e_+,\qquad b=(e_2+i e_3)/\sqrt2,\qquad
 \psi_w=\sqrt{1-w}\,a+\sqrt w\,b,\quad 0<w<1.
 \tag{3}
\]

Both components have odd parity. For the original spatial generator
`J=J23`, `Ja=0`, `Jb=ib`. Put `U(t)=Lambda(exp(tJ))`. On this compact
subgroup the ALREADY OWNED Julia scale and full complement are

\[
 T=U/2,\quad F=\sqrt3 I/2,\quad
 V_t\psi=\tfrac12|G\rangle U(t)\psi
              +\tfrac{\sqrt3}{2}|B\rangle\psi.
 \tag{4}
\]

`V_t^dagger V_t=I16` exactly; no outcome is discarded. Define three full
32-component normalized outputs
`A=V_0 a`, `B_0=V_0 psi_w`, `C=V_t psi_w`. Their closed product is exactly

\[
 \boxed{B_{\rm coh}=(1-w)
       [1-w/4+(w/4)e^{it}].}
 \tag{5}
\]

GOOD and BAD both contribute: the central overlap is
`(1/4)<psi_w,U psi_w>+3/4`. Its BAD term is not removed by normalization.
The output Berry connection is still `alpha_C=(w/4)dt`, with curvature
`dw wedge dt/4`. Yet the scalar phase of (5), including moving preparation
in all three factors, has the mixed preparation derivative needed for a
closed source. There is no contradiction and no inserted counterterm.

This coherent witness is mathematically sufficient to refute a general
`F=0` gate. It is NOT necessary to assume physically coherent access to
three whole histories: the next construction is stronger operationally.

## 3. Two independent outputs with COMPLETELY CLASSICAL flags suffice

Fully dephase GOOD/BAD, preserving both records. With `gamma=1/4`,
`rho_w=|psi_w><psi_w|` and `rho_t=U rho_w U^dagger`, the actual normalized
output densities are

\[
 \sigma_0=\gamma|G\rangle\langle G|\otimes\rho_w
 +(1-\gamma)|B\rangle\langle B|\otimes\rho_w,
\]
\[
 \sigma_t=\gamma|G\rangle\langle G|\otimes\rho_t
 +(1-\gamma)|B\rangle\langle B|\otimes\rho_w.
 \tag{6}
\]

Use the original CAR number operator `n_+=c_+^dagger c_+`, on ALL16 grades,
and the fixed anchor `A_+=I_flag tensor n_+`. It is a positive effect, not
an additional prepared state or a freely assigned relative phase. The
ordered two-record scalar is

\[
 Z_2=\operatorname{Tr}(A_+\sigma_0\sigma_t).
 \tag{7}
\]

It is complex and is NOT a probability. Direct multiplication gives

\[
 \begin{split}
 Z_2&=(1-w)[\gamma^2+(1-\gamma)^2
                  -\gamma^2w+\gamma^2w e^{it}]\\
 &=\boxed{\frac58(1-w)
                  [1-w/10+(w/10)e^{it}].}
 \end{split}\tag{8}
\]

The BAD–BAD contribution is `(9/16)(1-w)` and remains present. The result
uses unconditional full densities, with no division by a successful
probability. Dephasing the flags does NOT erase the relational CAR phase.
Within-CAR coherence in (3) remains required; classical states diagonal in
one common CAR basis would not give this signal.

### 3.1. A concrete readout, without a coherent superposition of histories

Let `W_swap` exchange the two complete output Hilbert factors and let
`O=(I tensor A_+) W_swap`. The elementary trace identity is

\[
 \operatorname{Tr}[(\sigma_0\otimes\sigma_t)O]
 =\operatorname{Tr}(A_+\sigma_0\sigma_t)=Z_2.
 \tag{9}
\]

The Hermitian operators `(O+O^dagger)/2` and `(O-O^dagger)/(2i)` measure
its real and imaginary parts. To make unmatched classical flags receive
literally zero score, use `P_match O P_match` and its Hermitian parts;
this has the same mean on (6). Mismatches are retained records with zero
estimator score, not discarded trials. Native implementation of this
two-copy operator is not presumed.

There is also a direct TOMOGRAPHIC alternative with no inter-history
coherent gate. In this invariant grade-one sector,

\[
 Z_2=\sum_{f=G,B}\sum_{k=+, -,2,3}
       (\sigma_0^{f})_{+k}(\sigma_t^{f})_{k+}.
 \tag{10}
\]

Each complex matrix element is reconstructed from unconditional joint
flag-and-CAR number/real-coherence/imaginary-coherence expectations.
These are standard one-body CAR bilinears, all number/parity preserving.
Products can be estimated from independent samples of the two processes;
the corresponding settings, repetitions, reference alignment and work
remain part of an actual programme's price. Formula (10) does not claim
that a single run reveals a density matrix or that the native apparatus
already measures every bilinear. It proves that coherent global phases of
separately prepared whole histories are unnecessary for this invariant.

`Z2` is unchanged under independent overall phases of either preparation
and under simultaneous unitary changes of the anchor and output frame.
Independent unaligned CAR frames still require their genuine comparison
map. This is not a blanket Lorentz-gauge or reference-erasure claim.

Measuring density-product invariants by copy permutations is established
quantum-information machinery; see [Ekert et al. (2002)](https://arxiv.org/abs/quant-ph/0203016)
and [Oszmaniec, Brod and Galvao (2021)](https://arxiv.org/abs/2109.10006).
The result here is its exact composition with the original D0 CAR/Julia
carrier and its full preparation/flag source, not invention of the general
measurement method.

## 4. Exact source, visibility and leading preparation completion

For `k=1/4` in (5) or `k=1/10` in (8), the real prefactor does not affect
the phase. Write `p=kw`, `D=1-2p(1-p)(1-cos t)`. Since `p<1/4`, the
bracket `1-p+p exp(it)` stays in the right half-plane. The exact source is

\[
 \boxed{dS_k=\frac{k\sin t}{D}\,dw
       +\frac{p[p+(1-p)\cos t]}{D}\,dt.}
 \tag{11}
\]

Its mixed partial derivatives agree identically. In particular

\[
 S_k=p t-\frac{p(1-p)(1-2p)}6t^3+O(t^5),
\]
\[
 \partial_wS_k=kt+O(t^3),\qquad
 \partial_tS_k=kw+O(t^2).
 \tag{12}
\]

At `t=h^2 theta`, on a fixed compact `(w,theta)` chart inside `0<w<1`,

\[
 \boxed{h^{-2}d_{w,\theta}S_k
       =d(kw\theta)+O_{C^1}(h^4).}
 \tag{13}
\]

Thus the dephased comparison gives `theta dw/10` together with `w dtheta/10`
at leading order. The earlier one-arm connection missed this component
because it differentiated a different comparison protocol. The component
is supplied by (7) itself; it is not fitted to restore exactness.

There is a genuine visibility condition. The phase of (8) is analytically
well-defined for every `0<w<1`, but `Z2` tends to zero as `w→1`. On
`w≤1-delta`, `|Z2|≥delta/2`. Error estimates from noisy observed real and
imaginary parts need this bound; the phase coordinate is not free signal
amplification. A moving Julia scale would also contribute its derivative:
the leading factor would be `w gamma²/[gamma²+(1-gamma)²]`. Here the scale
is the existing fixed `gamma=1/4`, not a tunable gravity normalization.

## 5. All SIX Lorentz directions have genuine scalar phase coordinates

The one-rotation example extends to a full analytic Lorentz chart, using
EXACTLY the existing two probe preparations and six anchor observables of
the [complete two-line owner](A4D_TWO_LINE_CAR_PROJECTIVE_LORENTZ_BARGMANN_GAUGE_FREE_2026_10_19.md),
§§4–5. In native null order `(+,−,2,3)`, keep

\[
 \psi_+=(e_++e_2+i e_3)/\sqrt3,\qquad
 \psi_-=(e_-+e_2+i e_3)/\sqrt3,
\]
\[
 (O_j,\rho_j)=(n_+,\rho_+),(n_2,\rho_+),
 (I_{+,-},\rho_+),(I_{+,2},\rho_+),
 (n_-,\rho_-),(I_{+,-},\rho_-),
 \tag{14}
\]

where `I_ij=(c_j^dagger c_i-c_i^dagger c_j)/(2i)`. Set
`A_j=I_flag tensor (I16+O_j)/2`. On full CAR16, number anchors have
spectrum in `[1/2,1]`, coherence anchors in `[1/4,3/4]`.

For a small ORIGINAL proper-Lorentz `U(xi)`, use the genuine full
instrument `T=Lambda(U)/2`, `F=sqrt(I16-T^dagger T)`, and DEPHASE its flags:

\[
 \sigma_j(\xi)=\operatorname{diag}
       (T\rho_jT^\dagger,F\rho_jF),\qquad
 Z_j(\xi)=\operatorname{Tr}[A_j\sigma_j(0)\sigma_j(\xi)],
 \quad S_j=\arg Z_j.
 \tag{15}
\]

The strict identity gap `I-T^dagger T=3I/4` provides a genuine open
analytic chart, including boosts. At identity, `sigma_j(0)=diag(rho_j/4,3rho_j/4)`.
For the full exterior Lie generator `X`, differentiation of the positive
square root gives the complete density source

\[
 \boxed{D_X\sigma_j=\operatorname{diag}
 \left(\frac{X\rho_j+\rho_jX^\dagger}{4},
 -\frac{(X+X^\dagger)\rho_j+\rho_j(X+X^\dagger)}8\right).}
 \tag{16}
\]

BAD is essential for boost derivatives. Its trace cancels the trace of
GOOD, so the entire output remains normalized. The positive visibilities
are `5/12` for the three number anchors and `5/16` for the three coherence
anchors. In the already-owned Lie order `(N2,N3,barN2,barN3,J23,B)`, exact
full-CAR algebra yields

\[
 \boxed{240\,DS(0)=
 \begin{pmatrix}
 0&7&0&5&4&0\\
 0&-2&0&2&-2&0\\
 2&0&6&0&0&0\\
 -4&0&4&0&0&8\\
 0&5&0&7&4&0\\
 -6&0&-2&0&0&0
 \end{pmatrix},}
\]
\[
 \boxed{\det(240DS)=12288,\qquad
        \det DS=1/15552000000\ne0.}\tag{17}
\]

The inverse-function theorem therefore gives a LOCAL ANALYTIC inverse of
six gauge-independent SCALAR phase coordinates on all six Lorentz
directions, with both Julia outcomes retained and classical. This is not
the earlier collection of curved one-arm Berry covectors. Each row is the
differential of its actual scalar (15), so its full Hessian is symmetric
when all preparation/reference/anchor derivatives are retained.

For arbitrary moving native variables the correct formula is simply

\[
 dS_j=\operatorname{Im}\frac{
 \operatorname{Tr}[(dA_j)\sigma_{j0}\sigma_j+
 A_j(d\sigma_{j0})\sigma_j+A_j\sigma_{j0}d\sigma_j]}{Z_j}.
 \tag{18}
\]

No new connection gauge, fitted coefficient, omitted failure or success
renormalization is used. The full grades are retained; the selected inputs
and their derivatives lie in the invariant grade-one block. Physical
implementation/choice and its work cost are still not implied by the
existence of these operators or by the inverse-function theorem.

### 5.1. General flag imbalance: why balanced flags erase the boost phases

Let `0<g<1` be the fixed GOOD probability at identity and replace the
auxiliary contraction by `T=sqrt(g) Lambda(U)`, `F=sqrt(I-T^dagger T)`.
Set `s2=g²+(1-g)²`. The original complete-density derivative becomes

\[
 D_X\sigma=\operatorname{diag}\left(
 g(X\rho+\rho X^\dagger),
 -\frac g2\{X+X^\dagger,\rho\}\right).
 \tag{18a}
\]

Keep EXACTLY the six preparations/effects in (14)–(15); no probe search
is performed. If `X=K+H`, `K^dagger=-K`, `H^dagger=H`, define

\[
 L_K=\frac{\Im\operatorname{Tr}(A\rho[K,\rho])}{\operatorname{Tr}(A\rho)},
 \qquad
 L_H=\frac{\Im\operatorname{Tr}(A\rho\{H,\rho\})}{\operatorname{Tr}(A\rho)}.
\]

The pair-phase derivative is exactly

\[
 \boxed{D_XS=\frac{g^2}{s_2}L_K+
                 \frac{g(2g-1)}{s_2}L_H.}\tag{18b}
\]

The observer-compact directions are
`N2-barN2,N3-barN3,J23`; the Hermitian boost directions are
`N2+barN2,N3+barN3,B`. There are three of each. Exact multiplication of
the same six anchor rows gives

\[
 \boxed{\det DS_g=
 \frac{g^9(1-2g)^3}{124416\,[g^2+(1-g)^2]^6}.}\tag{18c}
\]

At `g=1/2`, ALL three boost derivatives cancel between GOOD and BAD,
and the rank is exactly THREE. For every other `0<g<1` the rank is SIX.
This is a failure of this particular phase statistic, not loss of boost
information from the full output density or the original six CAR readout.
A balanced calibration would therefore produce a false three-direction
obstruction if used to judge the whole programme. Retaining BAD alone is
not enough: the actual branch weights and chosen statistic matter.

The factorization in (18c) follows structurally from three compact and
three boost directions, and is independently checked as an exact rational
identity. It is not evidence that only the Golden probability is possible.

### 5.2. Original Golden p: TWO densities, no third prepared reference

The latest native owner identifies the original contraction as
`T=p Lambda(U)`, `p=phi^-1`, so `g=p²`, `1-g=p`. The TWO-density statistic
still uses the original fixed positive CAR effects, not a third prepared
anchor density. Since `1-2p²=p³` and `s2=sqrt(5)p³`, (18c) gives

\[
 \boxed{\det DS_{\rm Golden}=\frac{p^9}{15552000}>0.}\tag{18d}
\]

This is different from the already-published THREE-density native atlas
with determinant `p^9/1152` and different anchors. Neither determinant is
a physical action coefficient. The pair construction reduces the required
dynamic density records to baseline and transformed output, at the price
of a fixed CAR effect and a smaller conditioning margin.

For the exact compact preparation family (3), the full native pair trace is

\[
 Z_{2,g}=s_2(1-w)
 [1-\kappa w+\kappa w e^{it}],\qquad
 \kappa=g^2/s_2.
\]
\[
 \boxed{\kappa_{\rm Golden}=
 \frac1{\varphi+2}=\frac{5-\sqrt5}{10},\qquad
 h^{-2}d\arg Z_{2,g}=d(\kappa w\theta)+O_{C^1}(h^4).}\tag{18e}
\]

The native preparation component is `kappa theta dw`, not `theta dw/10`.
For native p, `kappa<1/2`, so the rotation bracket stays in the right
half-plane. On `w≤1-delta`, `|Z_{2,g}|≥delta p³`. For arbitrary `g>1/2`
there can instead be zeros at `kappa w=1/2,t=pi`; the general phase atlas
is only asserted locally near identity with its positive visibility.

The null-word and owned plaquette readings in §6 likewise become
`[ab]arg Z= kappa w` and `h² Omega kappa w/4`. All preparation, anchor,
reference and any actually moving g derivatives belong to the complete
differential. The original g=1/4 values are retained as controls, not
silently substituted for native p.

## 6. The same crossed-Weyl signal, with its actual flag factor

For the original null word
`W(a,b)=exp(aN2)exp(b barN3)exp(-aN2)exp(-b barN3)`,
its two first derivatives vanish and `[ab]W=J23`. Hence
`[ab](W^dagger W)=0`. The complete Julia failure square root has ZERO
`[ab]` derivative, even though the full finite word is not unitary.
Applying (7) on the same state (3) gives the exact mixed coefficient

\[
 \boxed{[ab]\arg Z_2(W)=w/10.}\tag{19}
\]

On the already-owned corrected orthogonal six-face finite Cartan jet,
`[ab]P_uv=(h² Omega/4)J23` and both first derivatives of this plaquette
vanish. Therefore its full dephased reading is

\[
 \boxed{[ab]\arg Z_2(P_{uv})=h^2\Omega w/40.}\tag{20}
\]

Here `Omega` is the transverse wedge of the two wave gradients; it is
distinct from the preparation weight w. If it moves, its derivative must
also be included. In (19), at fixed `0<w<1`, the `(a,b)` phase Hessian is
`[[0,w/10],[w/10,0]]`, with both signs. Positive normalized Born records
therefore do not force the Hessian of their relational phase to be positive.
This is not an identification with the full Palatini `(12,12)` block.

The vacuum all40 rows of the geometric owner still vanish at this mixed
order while Weyl remains nonzero. A nonzero measured Weyl phase is not
itself an Einstein Euler equation. The new result supplies its correctly
typed full comparison source and eliminates the extra whole-history
coherence requirement for this readout.

## 7. Archive, price and the corrected consuming test

For an independent retained archive factor, even an arbitrary mixed one,
`sigma_i_total=tau_i tensor sigma_i`, and anchor `I_archive tensor A`,

\[
 Z_{\rm total}=\operatorname{Tr}(\tau_0\tau_1)\,Z_2.
 \tag{21}
\]

The archive multiplier is real and nonnegative for positive densities.
Where it is positive, all phase jets are unchanged even if it moves.
It changes visibility and can vanish; correlations between CAR and archive
invalidate this factorization and require the actual joint density.
No archive entropy, preparation or work term is removed from the full price.

Three distinctions change the parent route:

1. Test the COMPLETE comparison differential (18), not `d alpha=0` for a
   constituent ray. The previous contact/curl theorem remains correct only
   for its stated one-arm substitution.
2. Whole-history phase coherence is not a necessary readout premise for
   (7)/(15). Paid CAR density comparisons of independent complete records
   suffice mathematically, with the common operator reference retained.
3. A faithful six-coordinate observable atlas is not a selected action.
   Expressing Palatini as an arbitrary fitted function of these coordinates
   would still import the desired law and is not a proof.

The next exact physical composition is thus the binding of the ACTUAL
admitted Cost-Info/Book price to the full retained density comparison and
its full source, including preparation, clock, work, correlated oldRIGHT
and reference. If the physical action uses a different statistic, vary that
statistic. Only then apply the existing same-action connection/history
Schur and its joint-root/refinement theorem. No universal `F=0` gate or
new graviton-vertex search is needed before this comparison.

### 7.1. The latest six-triangle bridge: quotient descriptions, not extra physical selectors

The latest [six-original-triangle owner](A4D_MINIMAL_SIX_ORIGINAL_SCENE_TRIANGLES_REPRODUCE_FULL_ROLE40_PALATINI_2026_10_20.md)
already proves the entire offshell 40-source identity when each scene
chord is the ORIGINAL four-shared-link Role plaquette. The
[Aut(K913) naturality owner](A4D_AUTOMORPHISM_NATURAL_SIX_FACE_ROLE_EMBEDDING_AND_ORDERED_MEMORY_TWIRL_2026_10_20.md)
proves `F_iota(y)=F_star(y)` for every embedding in its transitive orbit;
it explicitly says that 122316480 is a counting orbit, not a physical
register. The following sharpens its consumer without adding an apparatus:

\[
 \boxed{\sum_\iota q_\iota(y)F_\iota(y)=F_\star(y)
 \quad\text{for ANY normalized field-dependent }q_\iota(y),\qquad
 D^k\sum_\iota q_\iota F_\iota=D^kF_\star.}\tag{22}
\]

The proof is substitution followed by `sum q=1`; all distribution-source
terms cancel BEFORE a limit. More basically, for the geometric scene
connection, `Phi_(g iota)(y)=g Phi_iota(y)`, so its quotient class
`[Phi_iota(y)]` is independent of iota. For the FULL decorated scene the
same statement uses the orbit `g Phi_iota0^all(y)`, with ALL data
relabelled together; it is not the fixed-Cost family of SO placements.
The quotient needs no invariant choice of a
numbered root, random uniform orbit preparation or paid gauge-label
register when a label is merely a coordinate representative. If a label
is physically prepared/stored or selects different operations, its entropy
and work remain actual costs; (22) removes none of those prices.

This is exact geometric SOURCE descent, not an action selector. Holding
arbitrary scalar Book costs fixed while changing only the SO placement
is NOT a full-scene gauge transformation. An extra positive cost on the
original edge `9↔20` distinguishes a triangle using C20 from one using
C26; only simultaneous permutation of costs, preparation, reference and
records gives the gauge equivalence. Similarly cross-site transition
maps must transform as `W_yx -> P_y W_yx P_x^-1`; their path products
then telescope. Independent unaligned chart forgetting or averaging
primitive transports is not quotient descent.

The latest [4D Bianchi/Wilson replay](sources/d0_native_role_face_integrability_2026-10-20/check_six_scene_triangles_role_bianchi_harmonic_wilson.mjs)
supplies the second necessary distinction: six scene chord matrices are
derived FUNCTIONS of shared Role links, not six independent new Euler
coordinates. Imposing independent face-chord Euler would already reject
the periodic flat Palatini vacuum, whereas the true link Euler is zero
by the coboundary adjoint. This is a variational-domain error, not a new
obstruction to the original four-dimensional geometric action.

Thus the shortest consuming test keeps the existing Golden LEFT Role
addresses, composes the actual four-link face word before quotienting
pure scene relabeling, and reads the same full native-p records. It needs
neither all327-scene tomography nor a physical random orbit merely to
name six triangles. A real site-conditioned field programme, full paid
Cost-Info binding, matter/internal stationarity and refinement still need
their own positive theorem. The new pair atlas addresses the readout
interface of this SAME programme, not those remaining obligations.

## 8. Verification and status

The [exact checker](sources/d0_two_record_phase_atlas_2026-10-19/check_two_record_phase.py)
constructs all16 exterior generators, full32 Julia outputs, the dephased
densities, number/coherence anchors, scalar phases and their source jets.
It checks the full flag derivative, all36 entries of (17), its exact
determinant, the two-copy trace identity, the missing preparation component,
the original commutator coefficient and the visibility/source distinctions.
Independent read-only derivation verified (5), (8), (11), (17), (19) and
the original plaquette's absence of first-order contamination before
publication. This is not registry acceptance or a full Lean/GR replay.

The coefficients `1/4` (coherent three-ray), `1/10` (dephased two-density
with a number anchor) and `1/28` (three dephased DENSITIES instead of a
number anchor) describe DIFFERENT complete comparisons. They must not be
silently identified as one physical Book source. `GR_closed=false`;
full native price selection, joint recovery and raw216 remain open.
