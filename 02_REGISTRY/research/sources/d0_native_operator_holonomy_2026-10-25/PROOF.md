# Full operator holonomy and the original finite polynomial heat source

25 October 2026. Same PR #334 and native-realization/source-composition
owner. This is a bounded mathematical application to a full clock
operator, not a report-channel construction, a new geometric root, or
selection of a physical action. The exact finite heat of the old owner
is consumed below. The new clock feedback is computed separately and
is not declared equal to the old feedback or Rayleigh terms.

## 1. Owners, parameters and the actual comparison boundary

The original full positive-frame spatial operator and scalar are
[paid writer §12.3, (55)–(56)](../../A4D_PAID_MOMENT_FIELD_WRITER_2026_10_21.md#123-applying-the-original-spatial-hjr-instead-of-substituting-the-clock):

\[
 \Delta=D^2,\quad B=I-\alpha D^2>0,\quad m=2n,\quad
 \beta=m\alpha,\quad Z_{55}=\operatorname{Tr}B^m,
\]
\[
 S_{55}={\log(C_{55}Z_{55})\over\beta}
 -128\operatorname{Tr}\log[(1-z)I+zB^m]
 +\operatorname{Tr}(\sigma D^2),\qquad
 C_{55}=128\,128^n.                                    (H1)
\]

The same owner's [§14.3a, (82a)](../../A4D_PAID_MOMENT_FIELD_WRITER_2026_10_21.md#143a-spatial-heat-complete-cq-information-and-the-actual-recycling-defect)
already gives the stopped-log generator `Λ=-α^-1 log B`. No Gibbs
preparation was inferred there, and none is inferred here. In this
packet `D` is its entire real symmetric spatial matrix, with every
site/CAR mode and the existing signed field-to-operator dictionary.
Restrict to the owner's strict real positive-frame chart; no Lorentzian
metric is substituted for its positive Hilbert norm.

The literal clock uses the owned unitary stage shift and paired Hodge
of [primary memo §7k, (101)–(102)](../../A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md#7k-recover-the-original-spatial-operator-from-the-same-complete-recorded-clock)
and [the executable Book map, full carrier and closing return](../d0_native_execution_domain_2026-10-24/BOOK_MAP.md).
For a complete `N≥1`-stage word, its holonomy is `U`,

\[
 T(|j\rangle v)=|j+1\bmod N\rangle g_jv,\quad
 d=(I-T)/\sqrt2,\quad
 \Delta_{\rm clk}=d^\dagger d\oplus dd^\dagger.          (H2)
\]

All primitive preparation, inverse, routing, programme and closing
stages count in `N`; a macro is not a single stage. Both Hodge grades
are traced. The transported prefix cut has one endpoint feedback block
`E_U=P_0 U†(I-P_0)U P_0`, rather than `N` copies of that block.

Fix a finite matrix size, `α>0`, integer `m≥1`, `β=mα>0`, and a bound
`||D||≤L_D` with `ρ=α L_D²<1` on the whole comparison chart. Hold these
parameters, all actual register dimensions, the input cut and `z∈(0,1)`
fixed in each field partial. The scaling below also holds `δ>0` and
the actual common integer `N` fixed within each compared stencil.
Field-dependent calibration parameters would add their genuine sources.

## 2. An invertible signed map consumes (55)'s finite heat exactly

Define the positive matrix function and the real symmetric operator

\[
 A_\alpha(D)=\int_0^1(I-t\alpha D^2)^{-1}\,dt,
 \qquad K_\alpha(D)=D\sqrt{A_\alpha(D)}.                 (H3)
\]

The removable zero value of the integrand function is one. Spectral
calculus gives

\[
 K_\alpha(D)^2=-\alpha^{-1}\log(I-\alpha D^2),
 \qquad e^{-\beta K_\alpha(D)^2}=(I-\alpha D^2)^m.      (H4)
\]

This is exact for the original finite `α,m`; there is no `α→0`
replacement of the old heat by a different exponential. Its signed
inverse is

\[
 D=K\left[{I-e^{-\alpha K^2}\over\alpha K^2}\right]^{1/2},             (H5)
\]

again with removable value one. The scalar function
`k(x)=sign(x) sqrt(-log(1-αx²)/α)` is strictly increasing, odd and
analytic on the strict interval. Thus the matrix, signed eigenvalues
and eigenspaces are preserved; neither just `D²` nor a trace is used
as a replacement for the original operator. Its Fréchet derivative in
an eigenbasis of `D` is

\[
 [DK_\alpha(D)[V]]_{ij}=k^{[1]}(\lambda_i,\lambda_j)V_{ij},            (H6)
\]

where the diagonal divided difference is `k'(λ)` and `k'(0)=1`.
Every divided difference is positive. The self-adjoint derivative map
is invertible, so this change creates no new kernel in the existing
16-coframe/24-link or matter-to-`D` map. Any original gauge kernel or
independent Gram/preparation source remains its original one.

Here is an explicit operator-norm bound without assuming `[D,V]=0`.
Set `g(ρ)=-log(1-ρ)/ρ`, with `g(0)=1`. Then

\[
 I\le A_\alpha\le g(\rho)I,\qquad
 \|K_\alpha\|\le L_D\sqrt{g(\rho)}=:L.                 (H7)
\]

Writing `R_t=(I-tαD²)^-1`, differentiation gives

\[
 DA_\alpha[V]=\int_0^1t\alpha R_t(DV+VD)R_t\,dt,
 \qquad \|DA_\alpha[V]\|\le
 {\alpha L_D\over(1-\rho)^2}\|V\|.
\]

If `S=sqrt(A_α)≥I`, its derivative solves
`S DS+DS S=DA_α`; the integral solution bounds `||DS||≤||DA_α||/2`.
Consequently

\[
 \|DK_\alpha(D)[V]\|\le C_\rho\|V\|,\qquad
 C_\rho=\sqrt{g(\rho)}+{\rho\over2(1-\rho)^2}.          (H8)
\]

The actual field derivative below is `Kdot=DK_α(D)[Ddot]`, not `Ddot`.
Equation (H4) and trace differentiation give the exact old heat source

\[
 D H_{55,\rm heat}[V]
 =-{2\operatorname{Tr}[D(I-\alpha D^2)^{m-1}V]\over Z_{55}}
 =-{2\operatorname{Tr}[K e^{-\beta K^2}DK_\alpha[V]]\over Z_{55}}.    (H9)
\]

No commutativity of `V`, the positive Gram or the independent density
`σ` is assumed. Sources from varying those independent data are not
contained in this fixed-data heat partial.

## 3. A literal clock holonomy retains the full transformed operator

Let `J=[[0,-1],[1,0]]` on one realification rebit and target

\[
 U_\delta(K)=\exp(\delta J\otimes K)\otimes I_{\rm aux}.             (H10)
\]

It is a real special-orthogonal **full-column** operator. It is not the
reduced channel of a regenerated programme and does not involve a
conjugate-fixed middle with constant spectrum. For `δ||K||<π`, the
principal logarithm is exactly `δ J⊗K`; its off-diagonal rebit block
recovers the signed `K`, and (H5) then recovers `D`. The entire original
operator is present in the holonomy.

The signed readout can be written without choosing an eigenbasis.
In (H10a)–(H10c), identity auxiliary extensions are understood: on the
full carrier the extracted matrix is `K⊗I_aux`, with unchanged operator
norm. No auxiliary column or normalized auxiliary trace is selected.

\[
 K=-{1\over2\delta}\operatorname{Tr}_{\rm rebit}
            [(J\otimes I)\log U_\delta].               (H10a)
\]

This preserves the sign and zero eigenspaces before applying (H5).
There is also an actual full-operator approximation bound. Let a real
orthogonal hardwired holonomy `V` obey `||V-U_δ||≤ε`, and assume both
principal phase arcs lie in `[-2π/3,2π/3]`. The target already has its
arc in `[-π/2,π/2]` under the later small-angle hypothesis; a sufficiently
small certified approximation gives the stated common strict log domain.
Define its observed operator by the same extraction,

\[
 \widehat K=-{1\over2\delta}\operatorname{Tr}_{\rm rebit}
            [(J\otimes I)\log V].                     (H10b)
\]

The principal logarithm is real skew symmetric. If its rebit blocks are
`[[A,B],[-B^T,C]]`, this extraction is `-(B+B^T)/(2δ)`, hence is real
**symmetric**; it is not a fitted `D` or an assumed exact tensor factor.
For completeness put `R(V)=(V-I)(V+I)^-1`. On the common phase arc,
`||R||≤sqrt(3)`, `||(V+I)^-1||≤1` and
`||R(V)-R(U_δ)||≤2ε`. The identity

\[
 \log V=2\int_0^1R(V)[I-t^2R(V)^2]^{-1}\,dt
\]

has resolvents of norm at most one. The resolvent identity therefore
bounds its difference by
`[2+4(sqrt(3))²/3] ||ΔR||≤12ε`. Since the extraction
`X↦-(1/2)Tr_rebit[(J⊗I)X]` has operator norm at most one,

\[
 \|\widehat K-K\|_{op}\le12\varepsilon/\delta.          (H10c)
\]

Apply the explicit signed inverse (H5) to this observed symmetric matrix
to read out `D`; its local Fréchet continuity supplies the corresponding
`D` error. The other blocks of `log V` have **not** disappeared from
the physical execution. In particular `V` is not replaced by
`exp(δ J⊗Khat)` in its heat or feedback trace; the complete operator
error and all residual blocks remain in that comparison. This is a
classical/operator readout of the compiled matrix, not a free logarithm
gate or a one-copy reconstruction of an unknown quantum state.

Let the full passive auxiliary dimension be `c_H`, and let its actual
initial projector have rank `r_P`. These are distinct multiplicities.
For example one may retain the original `(55)` carrier dimensions
`c_H=C_55` and initial protected rank `r_P=128` when its actual auxiliary
placement has those identity factors. This must be a real counted
carrier, not a multiplicity selected after the run. A spin/reference
already included in `D` is not multiplied in again. If all auxiliaries
are protected spin copies only, `c_H=r_P`.

For each actual eigenvalue `λ_i` of `K`, with its full multiplicity,
the rebit contributes holonomy phases `±δλ_i`. The actual clock phases
are `(2πk±δλ_i)/N`, `k=0,...,N-1`; (H2)'s eigenvalues are therefore

\[
 1-\cos((2\pi k\pm\delta\lambda_i)/N),                (H11)
\]

with the additional paired-Hodge and auxiliary multiplicities.
This follows directly by gauging primitive prefixes to one closing
holonomy and solving the cyclic shift equation. It is also the clock
phase formula in the [recorded-clock theorem §2](../d0_recorded_scene_clock_heat_2026-10-22/THEOREM.md).
No primitive is executed for free by this spectral gauge change.

Choose the explicit comparison temperature and gain

\[
 \beta_c={2N^2\beta\over\delta^2},\qquad
 \Gamma={\beta\over\beta_c}={\delta^2\over2N^2}.         (H12)
\]

For `K_N(t)=Σ_(k=0)^(N-1) exp[-β_c(1-cos((2πk+t)/N))]`, parity and
cyclic reindexing give `K_N(-t)=K_N(t)`. The **full** clock heat trace is

\[
 Z_c=4c_H\sum_i K_N(\delta\lambda_i).                  (H13)
\]

The factor four is Hodge degree two times rebit two. It is not an extra
factor of `N`, a normalization by input rank, or removal of half of the
signed spatial spectrum. The number of actual modes remains
`4 N c_H dim(D)`, even though high branches will have small weights.

## 4. All-mode heat and first-source estimates uniform in actual N

Assume `δ L≤π/2`. Define

\[
 \eta_N={\beta\delta^2L^4\over12N^2},\qquad
 T_0={2e^{-9\beta/\delta^2}\over1-e^{-27\beta/\delta^2}},\qquad
 T_1={10\pi\beta\over\delta}
 {e^{-9\beta/\delta^2}\over(1-e^{-27\beta/\delta^2})^2}.              (H14)
\]

The `k=0` branch has exponent `β φ_N(λ)`, where

\[
 \phi_N(\lambda)={2N^2\over\delta^2}
       [1-\cos(\delta\lambda/N)],
\]
\[
 0\le\lambda^2-\phi_N(\lambda)
       \le{\delta^2L^4\over12N^2},\qquad
 |\phi'_N(\lambda)-2\lambda|
       \le{\delta^2L^3\over3N^2}.                     (H15)
\]

For every other branch put `j=min(k,N-k)≥1`. Its wrapped clock angle
has magnitude at least `(2πj-|δλ|)/N`. The inequality
`1-cos x≥2x²/π²` on `|x|≤π` gives its exponent at least
`9βj²/δ²`. There are at most two such branches for each `j`, not
`N` branches with a common loose bound. Thus, for the sum `f_hi(λ)`
of the nonzero-clock branches,

\[
 0\le f_{\rm hi}(\lambda)\le T_0,\qquad
 |f'_{\rm hi}(\lambda)|\le T_1.                        (H16)
\]

For the derivative bound use `N|sin θ|≤|2πj±δλ|≤(5π/2)j` and sum
`j exp(-9βj²/δ²)`. Both geometric estimates in (H14) follow from
`j²≥1+3(j-1)`. They include `N=1`, when the high sum is simply empty,
and the single even-`N` endpoint branch. No alias or multiplicity is
omitted at a zero or repeated spatial eigenvalue.

Write `H_c=β_c^-1 log Z_c` and `Z=Tr exp(-βK²)=Z_55`. Then

\[
 0\le{H_c\over\Gamma}-{\log(4c_H Z)\over\beta}
 \le{1\over\beta}\log[e^{\eta_N}+e^{\beta L^2}T_0].   (H17)
\]

In particular the difference from the old heat in (H1) includes the
actual constant `β^-1 log(4c_H/C_55)`. If the old auxiliary carrier
is retained exactly this is `β^-1 log4`. It is not subtracted from the
physical price. Its field derivative is zero only in the stated fixed
parameter/dimension partial; a moving `β` retains its own derivative.

For any real symmetric variation `V_K`, put

\[
 \mathcal E_N=
 {\delta^2L^3\over3N^2}+2L(e^{\eta_N}-1)
       +e^{\beta L^2}(T_1/\beta+2LT_0).                (H18)
\]

The complete first-source estimate is

\[
 \left|D(H_c/\Gamma)[V_K]
       -D\{\beta^{-1}\log\operatorname{Tr}e^{-\beta K^2}\}[V_K]\right|
       \le\mathcal E_N\|V_K\|_{op}.                   (H19)
\]

Proof: the low-branch normalized weights differ from the target weights
by an `l1` amount at most `e^η_N-1`, since their unnormalized ratios
lie in `[1,e^η_N]`. Their logarithmic derivative is `-φ'_N`; (H15)
gives the first two terms of (H18). For the high branches use
`Z_low≥Z≥dim(D)e^-βL²`, (H16), and the low normalized source bound
`2L||V_K||`; this gives the last two terms. Multiplicities cancel in
this normalized trace comparison, without dropping them from (H13).

For clarity, at no point is a derivative of eigenvectors or a spectral
gap assumed. In an eigenbasis, a smooth spectral function satisfies
`[Df(K)[V_K]]_ij=f^[1](λ_i,λ_j)(V_K)_ij`; in its trace only the
diagonal divided differences `f'(λ_i)` remain. This proves (H19) for
noncommuting `K,V_K`, including repeated eigenvalues. It is not the
generally unjustified assertion that every operator-function Fréchet
norm equals the supremum of a scalar derivative.

Replace `V_K` by `DK_α(D)[Ddot]` and use (H8) to obtain the original
finite-heat source with error at most `E_N C_ρ ||Ddot||`. The estimate
is uniform for **every actual integer N≥1**: one may replace `N` by one
in the first two error terms. For fixed `β,L` it tends to zero as
`δ→0`, independently of how large the actual compiled clock becomes.
For a refining family with growing `L_D`, all displayed constants and
the real norm of `Ddot` must be budgeted again; this is not an automatic
mesh-uniform estimate.

## 5. True return feedback on the same declared cut

Take the actual input projector

\[
 P_0=|0\rangle\langle0|_{\rm rebit}\otimes I_{\rm scene}
                   \otimes P_{\rm aux},\qquad
 \operatorname{rank}P_{\rm aux}=r_P.                   (H20)
\]

From (H10), its return corner is `cos(δK)⊗P_aux` and its endpoint
leakage is exactly

\[
 E_U=\sin^2(\delta K)\otimes P_{\rm aux}.
\]

The owned one-return feedback determinant therefore gives

\[
 J_c=-r_P\operatorname{Tr}\log[I-z\sin^2(\delta K)],
\]
\[
 {DJ_c[V_K]\over\Gamma}
 ={2r_P z N^2\over\delta}
 \operatorname{Tr}\left[
 {\sin(2\delta K)\over I-z\sin^2(\delta K)}V_K\right].              (H21)
\]

There is no extra Hodge or clock-stage multiplier in `J_c`: only the
actual protected input rank contributes. This follows from the endpoint
cut, not from a normalization of the heat. Trace divided differences
again prove the formula for noncommuting `K,V_K`.

For `d=dim(D)` and `d_min=1-z sin²(δL)>0`, (H21) has the explicit
small-`δ` comparison

\[
 {DJ_c[V_K]\over\Gamma}
       =4r_P zN^2\operatorname{Tr}(K V_K)+\mathcal R,
\]
\[
 |\mathcal R|\le
 {2r_P z dN^2\delta^2L^3\over d_{\min}}
                  (4/3+2z)\|V_K\|_{op}.              (H22)
\]

Use `|sin(2x)-2x|≤4|x|³/3` and `sin²x≤x²` to verify this bound.
For fixed `z`, the normalized feedback source is generically of order
`N²`, **not** a vanishing term. If an actual operator family has constant
`Tr K²`, its leading trace source vanishes; that is a separate identity
to prove, and the remainder still contains `N²δ²`. No such cancellation
is assumed here.

In particular (H21) is not the original feedback
`-128 Tr log[(1-z)I+z(I-αD²)^m]` in (H1). The old Rayleigh source
`D Tr(σD²)` and its independent preparation equation are also not
provided by the clock heat theorem. Changing `z` with `N`, declaring a
different input projector, or subtracting (H21) would change the physical
comparison and must carry its real source. The complete clock Book
source is the heat source in (H19) **plus (H21)** and any actually
selected additional terms.

## 6. Native codes, padding and source norms

The exact statements above are mathematical comparisons of full finite
operators. A finite target exponential usually is not an exact word in
the algebraic raw alphabet. Application to independently hardwired
native words requires the root's separate all-column compiler argument,
its actual integer stage count and its error budget. A prepared-column
or reduced-channel approximation does not control this heat trace.
Compiler workspace must be included on all columns: the target on it
is the declared identity extension, not an unexamined garbage channel.

For orientation, the target family has the Duhamel norm bound
`||D U_δ||≤δ ||DK_α[Ddot]||`. A smooth comparison of an actual primitive
word instead has `||D U_word||≤Σ_j ||K_j||` for its real skew-adjoint
stage generators. These are different norms and are not identified for
free. The field-source theorem does not assert a continuously adjustable
native pulse or a differentiable selector of hardwired code words.

There is a safe finite-endpoint compiler bound even without such a
selector. On common `N`, fibre and input cut, gauge both history clocks
to their closing holonomies. If `||U_word-U_δ||≤ε`, their paired
Laplacians differ by at most `ε`, and the normalized heat values differ
by at most `ε/Γ`, by the owned log-heat Lipschitz inequality. For two
actual endpoints add both errors, then divide by their actual endpoint
separation and calibration. This conservative bound depends on the
true `N`. The following stronger full-spectrum estimate removes that
`N` dependence for the heat value. Neither estimate identifies
independent code histories by a small endpoint error.

### An N-uniform full-spectrum endpoint value bound

Use the actual logical hardwired operator `V` and the target `U_δ`,
with the same counted identity auxiliary extension. Assume
`||V-U_δ||≤ε`, the common principal-log phase arcs of (H10b), and put

\[
 \rho_e=12\varepsilon,\qquad
 L'=L+\rho_e/\delta,\qquad \delta L'\le\pi/2,
 \qquad q_\delta=e^{-9\beta/\delta^2}.                 (H23)
\]

By (H10c), the Hermitian matrices `-i log V` and `-i log U_δ` differ
in norm by at most `ρ_e`. The min-max principle matches their sorted
phase eigenvalues with maximum difference at most `ρ_e`, including
degeneracies. Interpolate these paired **phase numbers** linearly.
Every interpolated phase lies in `[-δL',δL']`. This is a proof device
for endpoint values, not an actual operator/compiler trajectory and
does not require differentiable eigenvectors or a native word curve.

For the scalar full-branch kernel `f_N(t)=K_N(t)`, the low branch obeys
`|∂_t f_low|≤(2βL'/δ) f_low`. The same wrapped-angle argument as
(H16) gives

\[
 |\partial_t f_{\rm hi}|\le
 {10\pi\beta\over\delta^2}
 {q_\delta\over(1-q_\delta^3)^2}.
\]

If `d_phase` is the actual number of logical phase eigenvalues, the
denominator along this numerical interpolation is at least
`d_phase exp(-βL'²)`. The common Hodge and auxiliary mode factors
multiply both numerator and denominator; all are retained and cancel
only in this logarithmic derivative bound. Integrating the scalar
derivative proves, for `H_rec=H_c/Γ`,

\[
 |H_{\rm rec}(V)-H_{\rm rec}(U_\delta)|
 \le\rho_e\left[
 {2L'\over\delta}
 +{10\pi e^{\beta L'^2}\over\delta^2}
       {q_\delta\over(1-q_\delta^3)^2}\right].          (H24)
\]

This estimate is independent of the actual integer `N`. For fixed
`β>0` and bounded `L'`, as `δ` tends to zero it gives the
claimed `O(ε/δ)` heat endpoint error; the exponentially small second
term has its explicit coefficient. It uses every actual phase of `V`,
including contributions from the other logarithm blocks, not only the
extracted `Khat`. Actual source secants add the two endpoint errors in
(H24) and divide by their real separation and calibration.

Feedback has a different error scale and is not absorbed in (H24).
For `C_U=(I-P_0)U_δP_0` and `C_V=(I-P_0)VP_0`,
`||C_U||≤δL` and `||C_V-C_U||≤ε`. Hence

\[
 \|E_V-E_{U_\delta}\|\le2\delta L\varepsilon+\varepsilon^2,
 \qquad \|E_V\|,\|E_{U_\delta}\|
       \le b_E:=\min\{1,(\delta L+\varepsilon)^2\}.
\]

On the fixed rank-`r_0=rank(P_0)` input space, the positive logdet
resolvent along the straight effect segment consequently gives

\[
 |J(V)-J(U_\delta)|
 \le{r_0z(2\delta L\varepsilon+\varepsilon^2)\over1-zb_E}.            (H25)
\]

Its gain-normalized error is the right side of (H25) divided by the
actual `Γ=δ²/(2N²)`. Thus the genuine `N²` feedback precision debt
remains. Equations (H24)–(H25) compare endpoint **values**; no compiler
C1 theorem or free derivative of independently hardwired words follows.

An actual non-power-of-two spatial carrier cannot be silently truncated
from qubits. If `D` is zero-padded by `q` modes, the low-branch partition
in (H17) is **`Z_55+q`**, not `Z_55`. Its source is the old heat source
times `Z_55/(Z_55+q)`. Any use of that factor as a gain must be explicit;
the padding modes stay in the full trace. They give zero return defect
for this zero-padding choice, not negative feedback. A nonzero fixed
padding block instead contributes its actual heat and feedback. Other
retained ancillas multiply the full trace by their real dimensions;
their preparation/protection ranks enter (H20) separately.

## 7. The different original 33-scene incidence and remaining obligations

The [recorded-clock theorem §§1–2](../d0_recorded_scene_clock_heat_2026-10-22/THEOREM.md)
and [paid writer §13.3](../../A4D_PAID_MOMENT_FIELD_WRITER_2026_10_21.md#133-all-33-scene-modes-the-literal-cyclic-clock-and-their-source)
also own a **different** full operator

\[
 \mathcal L=I-B_S\otimes I-C_S\otimes(T+T^\dagger)
\]

on the original 33-vertex scene times clock. Its heat kernel is
`Tr_33 exp[β(B_S+2C_S cos θ)]`, at its specified original temperature.
It is not `exp[-β_c(1-cos θ)]`. The present theorem neither replaces
that incidence heat by the paired clock nor adds their prices together.
Extracting the same chronological shift from that incidence operator,
as in primary memo (102), is an operator readout, not an equality of
their whole heat functionals.

The positive result is precise: a full signed spatial operator has an
invertible target holonomy, and the **whole** paired primitive-clock heat
recovers the original finite polynomial heat source with explicit bounds
uniform in the actual clock length. All Hodge/rebit/auxiliary modes and
all padding remain present. The true feedback is a potentially large
additional source. The original complete H+J+Rayleigh identity, selected
clock/temperature/cut parameters, local physical carrier realization,
independent internal controller/preparation equations and stationary
refinement are not thereby proved. `GR_closed=false`.
