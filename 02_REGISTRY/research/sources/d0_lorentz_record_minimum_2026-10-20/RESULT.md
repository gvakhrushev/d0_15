# GR-specialized verification: six Lorentz phase statistics are a MINIMAL complete record

20 October 2026. **Bounded theorem in existing research Draft #334**, task
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`. Phase:
verification kernel → actual native readout → GR operational realization.
Reuse the accepted main
[`VerificationCore.lean`](../../../../03_FORMALIZATION/D0/Foundation/VerificationCore.lean)
and [`TheoryTransfer.lean`](../../../../03_FORMALIZATION/D0/Foundation/TheoryTransfer.lean);
do not re-prove their generic results.

**Owner and exact scope.** The
[two-record full-CAR16 original Golden phase atlas](../../A4D_TWO_RECORD_PHASE_ATLAS_AND_AUTOMATIC_PREPARATION_SOURCE_2026_10_19.md),
§5.2, already supplies six *smooth scalar phase functions* of the actual
locally completed two-density GOOD/BAD CAR readout, with original
`p=phi^-1`, `g=p²`, moving preparation and positive anchor effects.
The scalar expectation `Z_j=Tr[A_j sigma_j(0) sigma_j(P)]` is complex and
is not itself a Born probability; its real and imaginary parts are
mathematically observable through the owner's full flag and CAR comparison.
The physical source/Cost-Info/admission of that comparison is still OPEN.

This document **does not invent a seventh detector, choose six new probes,
or assert that G0 physically executes them**. It derives an *operational
necessity and quantitative recovery law* from the existing EXACT atlas.

## 1. Exact original Golden Jacobian and an explicit inverse

In the original ordered six-generator coordinates
`xi=(N2,N3,barN2,barN3,J23,B)`, the older auxiliary
`g0=1/4` full two-record atlas has the exact first-jet matrix

\[
A_0=\frac1{240}
\begin{pmatrix}
0&7&0&5&4&0\\
0&-2&0&2&-2&0\\
2&0&6&0&0&0\\
-4&0&4&0&0&8\\
0&5&0&7&4&0\\
-6&0&-2&0&0&0
\end{pmatrix}.
\tag{1}
\]

This is an already-owned original-CAR source, **not** a new calculated
physical coefficient. Decompose the existing generators into compact
and boost parts, `N_j=(K_j+H_j)/2`,
`barN_j=(H_j-K_j)/2`, `J23=K` and `B=H`.
The published native source identity is

\[
D_X\Phi_g=\frac{g^2}{g^2+(1-g)^2}L_K(X)
 +\frac{g(2g-1)}{g^2+(1-g)^2}L_H(X).
\tag{2}
\]

At `g0=1/4` the two coefficients are `1/10` and `-1/5`.
At the ACTUAL original Golden `g=p²=(3-sqrt5)/2`, their ratios
to those coefficients are respectively

\[
a_K=5-\sqrt5,\qquad
a_H=(3\sqrt5-5)/2.
\tag{3}
\]

Decompose `A0=A0_K+A0_H` by sum/difference of its (N2,barN2)
and (N3,barN3) columns, placing the J column in K and B in H.
Then the native six-by-six Jacobian is EXACTLY

\[
 A= D\Phi_{p^2}(I) = a_K A_{0,K}+a_H A_{0,H}.
\tag{4}
\]

Its determinant reproduces the independently owned native value
\[
\det A=\frac{p^9}{15552000}>0.
\tag{5}
\]

**New explicit exact inversion.** Write `r=sqrt5`. The inverse of
the REAL Golden six-by-six matrix (4) is

\[
A^{-1}=\begin{pmatrix}
0&0&3r&0&0&-15-6r\\
40+18r&20+12r&0&0&-30-12r&0\\
0&0&15+6r&0&0&-3r\\
10+12r&20+12r&0&0&-6r&0\\
-30-6r&-30-6r&0&0&30+6r&0\\
0&0&-15-9r&15+9r&0&-15-9r
\end{pmatrix}.
\tag{6}
\]

Exact `Q(sqrt5)` multiplication (checker below) verifies `AA^-1=I`.
All six row-sums are explicit; the maximum is the second row:

\[
\boxed{\|A^{-1}\|_\infty=90+42\sqrt5<185.}
\tag{7}
\]

This is the native original-p conditioning margin, not the earlier
auxiliary 1/4 result and not a fitted physical gravity coupling.
The balanced `g=1/2` anchor has boost rank loss, exactly as the
existing owner proved; the actual Golden `g=p²` avoids that failure.

## 2. Six smooth real statistics are necessary, and the existing atlas attains six

Let `P=exp(sum_i xi_i G_i)` vary in a genuine open six-dimensional
proper-Lorentz neighborhood, and suppose a proposed native smooth
readout `R(P)\in R^m` admits a `C^1` local reconstruction map
`Q` of **all six** xi coordinates, so `Q(R(P(xi)))=xi`.
Differentiating at identity gives

\[
 DQ_{R(I)}\,DR_I=I_6.
\tag{8}
\]

Thus `rank DR_I=6`, hence necessarily `m>=6`.
This is a chain-rule theorem, not a heuristic statement about information
or a rank census. It applies wherever local smooth recovery and its
source jets are claimed, including a full six-direction physical source
comparison. A physical sector known independently to be lower
dimensional has a different bound; no six-direction admission is
silently assumed.

The existing two-density original-Golden phase atlas supplies **exactly
six** smooth scalars with invertible (5), so it saturates this necessary
local smooth-readout count. No additional independent local readout
channel is mathematically required for *information sufficiency*.
This does not establish the compulsory native action that uses it.

## 3. Quantitative h-refinement recovery (exact leading source map)

Let `G(F)=sum_i F_i G_i`, `F in [-r0,r0]^6`, with fixed small
`r0>0`, and take an original controlled smooth-lattice plaquette
`P_h(F)=exp(h²G(F))`. The entire six-phase statistic uses the SAME
prepared instrument; define the mathematically calibrated readout

\[
Y_h(F)=h^{-2}A^{-1}
 [\Phi_{p^2}(P_h(F))-\Phi_{p^2}(I)].
\tag{9}
\]

This merely applies a fixed linear decoding matrix to the original
six readouts. It does not add an actuator or postulate a physical price.
The analyticity and (4) give

\[
Y_h(F)=F+O(h^2\|F\|^2),\quad
DY_h(F)=I_6+O(h^2\|F\|),
\tag{10}
\]

uniformly on the fixed compact cube. Shrink its chart and choose
`h0>0` so `\sup_F \|DY_h(F)-I\|_\infty<=1/2` for all
`0<h<=h0`. The fundamental theorem of calculus along segments gives

\[
\frac12\|F-F'\|_\infty\le
 \|Y_h(F)-Y_h(F')\|_\infty\le
\frac32\|F-F'\|_\infty.
\tag{11}
\]

Therefore the six original scalar expectations locally recover ALL
six oriented Lorentz curvature components with a **uniform** inverse
after their necessary `h^-2` normalization. If the actual measured
phase vector has error `\|e_h\|_\infty`, any local reconstruction
satisfies the rigorous error propagation

\[
\|\widehat F-F\|_\infty\le
 2(90+42\sqrt5)\frac{\|e_h\|_\infty}{h^2}
 <370\frac{\|e_h\|_\infty}{h^2}.
\tag{12}
\]

For a general `P_h=I+h²G(F)+O(h³)`, an additional `O(h)`
geometric discretization error survives in (10)-(12).
Thus the required physical readout error for `O(h^a)` curvature
recovery is `O(h^{2+a})` (plus any independent geometric error).
A source-comparison claim must retain that amplification when mapping
the original complete-record errors into the geometric Euler response.
The existing exponentially controlled compact flag source is a
different instrument/result until its actual carrier/source map is
proved; do not apply its bounds to the full128 by name alone.

## 4. Minimum retained record information and a forced non-idle task

This section supplies a **conditional physical verification task** to
the existing `ProspectiveExecution` interface. It is not the missing
unconditional D0 prospective `optimal` theorem.

Fix a positive `r0`, target curvature accuracy `delta>0`, and
the full six-dimensional admitted test cube above. Consider the
`M=N_delta^6` equally weighted hypotheses obtained from a grid
of spacing `3delta` in every coordinate, with

\[
N_\delta=\left\lfloor\frac{2r_0}{3\delta}\right\rfloor+1.
\tag{13}
\]

Any final retained record that reconstructs the original curvature
to coordinate error at most `delta` with ZERO error on every grid
candidate must distinguish all `M` hypotheses: two different points
have separation `>=3delta>2delta`.
Thus the final code has `>=M` distinguishable codewords, and its
**worst** binary code length satisfies

\[
\ell_{\max}\ge\left\lceil\log_2 M\right\rceil.
\tag{14}
\]

For a prefix-free binary archive and a uniform grid prior, Kraft's
inequality plus Jensen gives
`E ell >= log2 M` as well. If one charged primitive produces at most
`b>=2` distinguishable terminal symbols and codes are prefix-free
with no unpriced side channel, its expected number of such symbols
is bounded below by `log_b M`. Variable stop times must themselves
be retained as part of the code. For nonzero average classification
error `epsilon`, the elementary Fano error-indicator argument yields

\[
E[\text{record symbols}]\log_2 b\ \ge\
 \log_2 M-h_2(\epsilon)
 -\epsilon\log_2(M-1).
\tag{15}
\]

This bound conditions on a common initially retained archive that
does **not** already encode the particular unknown grid point.
If the input/archive already supplies the distinctions, idle is not
excluded. If the native output alphabet or allowed initial memory
grows with h, their actual capacity and price must be included rather
than assuming one bit per physical gate.

**Conditional native unit-price consequence.** If every emitted b-ary
symbol is produced by an original nonidentity complete-state transition
and that *actual* transition is subject to the existing ActionProtocol
unit floor (Cost >= 1), then on the same uniformly distributed grid

\\[
 \\mathbb E\\sum_{\\text{executed primitives}}\\mathrm{Cost}
 \\ge\\mathbb E[\\text{emitted b-ary symbols}]
 \\ge\\log_b M.
\\tag{15a}
\\]

This is a **genuine but scoped prospective lower bound** from required
future distinctions. It does not identify generator description length,
physical work, record entropy and complete Cost-Info; it does not prove
an admitted execution ATTAINS the floor, or choose the selected physical
dynamics. If one primitive emits a larger alphabet, records a collective
outcome at one price, or reuses previously known input distinctions,
its actual b and resource/admission semantics must be used instead.

The lower bound is SHARP as a representation law. By (11) the six
calibrated coordinates `Y_h(F)` range in a fixed cube, and uniform
scalar binning at step `delta/4` gives a finite six-coordinate code
with at most `O(delta^-6)` possible words; inverse recovery has error
`<=delta`. Therefore the minimum **ideal encoded statistic** size is

\[
\boxed{
  \log_2 M=6\log_2(1/\delta)+O(1)
  \quad\text{bits,}\quad\delta\downarrow0.
}
\tag{16}
\]

For continuum accuracy `delta_h=h^a`, the necessary archive content
is `6a log2(1/h)+O(1)` bits in this six-parameter local test family.
This is a **description-length bound**, NOT a proof that the physical
native device acquires exact real phase expectations in `O(log(1/h))`
gates. Statistical shot noise, reference alignment, controller,
preparation, outcome histories, and the actual Cost−Info can demand
substantially more work. The theorem never identifies these costs.

**Prospective requirement actually supplied:** If the GR physical
specialization demands a yet-unrecorded `delta`-distinction between
all admitted local curvature hypotheses, a final idle record cannot
fulfil that task. The actual verification programme must execute
something and retain enough information by (14)-(16). This provides
a nonarbitrary *GR-specialized required-distinction* input to the
existing prospective theorem, **not** a derivation of its `optimal`
premise or of the exact Einstein-source generating action.

## 5. Consumption and limitations

Reuse `A`, not a new detector: the smallest next native task is to
identify the original fully **paid** complete programme producing
these two-density CAR/Golden comparisons, including all BAD leaves,
oldRIGHT, reference, moving preparation and observer, its true clock,
controller and work. Then evaluate the SAME programme's first source
and second variation against the already owned full HJR flat-source,
curved saddle and boundary-traction gates. Only an actual total-source
equivalence can feed `gr_operational_realization`.

The positive results here are (i) exact native inverse and conditioning,
(ii) six-scalar smooth-readout minimum, (iii) uniform local
`h^-2` curvature reconstruction, and (iv) sharp conditional
minimal retained information for a specified full six-dimensional
GR-verification task. They do not select the complete Book03 price,
admit physical six settings, solve matter Ward/Einstein joint dynamics,
or provide uniform recovery of the original raw216 response.
`GR_closed=false`.

## 6. Verification

[`check_native_golden_minimal_readout.py`](check_native_golden_minimal_readout.py)
verifies (1)-(7) by exact `Q(sqrt5)` matrix arithmetic using SymPy
and the existing CAR16 atlas matrix, including every inverse entry,
determinant and the claimed infinity-norm maximum. The abstract
chain-rule and packing/Fano arguments above are analytical and not
substituted by numerical samples.
