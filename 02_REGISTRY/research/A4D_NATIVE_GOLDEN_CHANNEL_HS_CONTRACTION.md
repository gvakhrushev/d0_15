# Equal-weight Hilbert–Schmidt contraction of the golden CAR channel

**Status:** Conditional candidate. Skeptic #1 wounded the strict lower endpoint, because failure of positive-definiteness does not separate a zero pivot from a negative one. The repair demands a negative leading pivot; that pass survived. Skeptic #3 survived the citation rebase onto `681a631c`. The preparation memo, its checker and its receipt have the same bytes at `7a188938`. The gravity-gate sentence moved on that later tip and is quoted below from it. No registry row. Not a physical admission and not GR. Pre-flight on
`finite-time mixing`, `Hilbert-Schmidt contraction`, `49/50`, and
`spectral gap` inside `02_REGISTRY`: the only owner of a mixing rate for
this channel is the explicit absence recorded below. The Fiedler value 20,
the Lyapunov gap assumption, the Bellissard gap label, and the 2×2 golden
readout kernel are different carriers.

## Claim

On the sixteen-component CAR carrier, let \(U_r=\operatorname{record}(I_4,e_r)\)
for \(r=0,1,2,3\) and let \(a^2=p\), \(p^2+p=1\), with the positive roots.
The equal-weight nonselective channel
\[
\Phi(X)=pX+\frac{p^2}{4}\sum_{r=0}^{3}U_rXU_r^{T}
\]
fixes \(I_{16}\) and preserves trace. For every nonzero traceless Hermitian
\(16\times 16\) matrix \(\delta\),
\[
\frac{9442}{10000}<\|\Phi\|^2_{\mathrm{HS}}<\frac{9443}{10000}<\left(\frac{49}{50}\right)^2,
\]
where \(\|\Phi\|_{\mathrm{HS}}\) is the operator norm of \(\Phi\) on that
real-linear space for the Frobenius norm. Hence
\(\|\Phi(\delta)\|_F<(49/50)\|\delta\|_F\), and the same strict factor
powers to \(\Phi^n\). The constant is not an upper bound for every positive
weight vector \((\pi_r)\).

## Owned pre-facts

The preparation note at `681a631c` still records the missing rate, and the
gate this rate does not close now includes the same-edge affine-shift readout
(`A4D_NATIVE_GOLDEN_CHANNEL_ENDOGENOUS_PREPARATION.md:221-228`):

> There is no exact finite-time mixing-rate bound here; turning the asymptotic
> preparation into a finite-depth error estimate needs a quantitative spectral
> gap or contraction bound. More fundamentally, the core still owes the
> physical map that admits the same-edge affine-shift readout and golden
> transition on this full-support family, and binds its preparation to the
> counted dynamics on the complete
> \((q,D,b,m)\) state. The own action, full metric and matter variations, Ward
> identity, refinement transfer, curved roots, soundness/recovery, G0, and the
> existing parent terminals remain open.

The same note separates the attractor from equal weights. That separation is
conditioned on admitting the same-edge shift readout (`:210-216`):

> Conditioned on admitting the same-edge shift readout, the golden two-outcome
> rule, and full support on these four native returns, repeated unobserved
> internal ticks prepare the state used by the existing v3 event-conditioned
> source calculation as the channel's unique long-time equilibrium. The
> preparation does not require the core to select equal probabilities for the
> unobserved preparation. The counted v3 source instrument still uses its own
> equal-weight return rule, which remains unselected by the core.

Its hostile control for one return is the rank of a single commutant, together
with the fixed-basis rotation failure (`:203-205`):

> As hostile
> controls, one return alone has rank 192 and a 64-dimensional commutant, and
> the fixed-basis channel fails SO(3) covariance at zero shift.

The displayed unscaled sum is the equal-weight channel. Positive weights enter
by scaling both Kraus operators of return \(r\) by \(\sqrt{4\pi_r}\), so
\(\pi_r=1/4\) leaves those operators unchanged (`:32-36`).

`03_FORMALIZATION/D0/Representation/GoldenRelativeChannel.lean:6-9` is a
different operator:

> The kernel below is the squared-entry response of the existing golden gate.
> It propagates diagonal input weights; coherent evolution is still the gate itself.
> Iterating this kernel therefore requires diagonalization between stages and is not
> identified with coherent ticks or spatial dimension.

`02_REGISTRY/claims.csv:369`, claim `D0-CONNECTIVITY-SPECTRAL-GAP-SPEED-001`,
is the graph Laplacian gap, not this channel:

> Connectivity spectral gap: K(9,11,13) Fiedler value (smallest nonzero Laplacian eigenvalue) = 20 > 0 (connected); edgeless = 0.

## The contraction

The Kraus pair of one return is
\(K_0=(pI+p^2U)/2\), \(K_1=ap(U-I)/2\). With
\(\alpha=p/2\), \(\beta=p^2/2\), \(\gamma=ap/2\), the field relations give
\(\alpha\beta=\gamma^2=p^3/4\), \(\alpha^2+\gamma^2=p/4\), and
\(\beta^2+\gamma^2=p^2/4\). The cross terms \(XU^T\) and \(UX\) therefore
drop, and
\[
K_0XK_0^T+K_1XK_1^T=\frac p4 X+\frac{p^2}4 UXU^T
\]
for every matrix \(X\) and every one of the four literal returns. Equal
weights sum the four copies to the displayed \(\Phi\). Swapping \(p\) with
\(p^2\) in the identity coefficient does not satisfy the same relation, and
the swapped formula differs on a concrete symmetric matrix.

Each \(U_r\) is orthogonal. Consequently \(\Phi(I)=I\) and \(\operatorname{tr}\Phi(X)=\operatorname{tr} X\). Real symmetric and real skew matrices are each invariant. They are Frobenius-orthogonal because a symmetric entry and a skew entry contribute opposite products on \((i,j)\) and \((j,i)\). A traceless Hermitian matrix is uniquely \(S+iK\) with \(S\) real symmetric traceless and \(K\) real skew, and
\[
\|\Phi(S+iK)\|_F^2=\|\Phi(S)\|_F^2+\|\Phi(K)\|_F^2.
\]
The Hilbert–Schmidt norm on traceless Hermitian matrices is the maximum of the two real norms. Skew matrices are traceless. The symmetric norm below is the traceless one: the identity direction is the eigenvalue \(1\), and it is excluded.

The six exterior transpositions of the four bits act by signed permutation matrices \(E_\pi\). Each such matrix is a symmetric involution, so conjugation by \(E_\pi\) is an orthogonal involution of the Frobenius space. The sum \(C\) of those six conjugations is therefore self-adjoint. Its kernels at eigenvalues \(6,-6,0,2,-2\) have dimensions
\[
\begin{align*}
\text{skew }&(4,8,12,42,54),\\
\text{symmetric }&(12,8,20,54,42).
\end{align*}
\]
These five kernels span each sector, intersect trivially, and are pairwise Frobenius-orthogonal. Every non-trivial symmetric kernel is traceless. The coordinate formula for conjugation matches literal matrix conjugation \(EME^T\) on a separating integer probe in each sector. The Frobenius coordinate weights are \(1\) on diagonal entries and \(2\) on off-diagonal entries, matching the entrywise sum of squares on \(E_{00}\) and on \(E_{01}+E_{10}\).

\(\Phi\) preserves every one of these kernels. On the 11-dimensional trace-zero subspace of the symmetric eigenvalue-\(6\) kernel, the squared Hilbert–Schmidt norm is strictly greater than \(9442/10000\) and strictly less than \(9443/10000\). The same kernel also contains the identity, whose squared norm is \(1\); that line is exactly the trace direction and is excluded from the traceless claim. The other nine kernels — all five skew kernels, and the symmetric kernels at eigenvalues \(-6,0,2,-2\) — each have squared norm strictly less than \(9442/10000\). Those nine kernels are traceless, orthogonal to the identity, and orthogonal to the 11-dimensional block. The global squared norm on traceless Hermitian matrices is therefore the 11-dimensional value, and it lies in \((9442/10000,9443/10000)\).

The lower endpoint is strict because the form \((9442/10000)H-A\) on that
11-dimensional block has a negative leading pivot. After the earlier pivots
are positive, that pivot is a negative leading principal minor, so the
quadratic form takes a negative value and the squared norm is strictly
greater than \(9442/10000\). A zero pivot would only show a singular leading
submatrix and would not be accepted. The same negative-pivot test puts the
skew eigenvalue-\(2\) kernel strictly above \((96/100)^2\).

The integer comparison \(9443\cdot 2500=23607500<24010000=2401\cdot 10000\) is
\((9443/10000)<(49/50)^2\). The squared norm is positive and below
\((49/50)^2\), so the norm itself is strictly below \(49/50\). The upper
bounds are all-positive pivots, which is positive-definiteness and a strict
inequality.

The winning block is not normal for its Frobenius adjoint: \(L\) and
\(H^{-1}L^TH\) do not commute. The quantity bounded here is the largest
singular value, not the spectral radius.

The skew kernel of eigenvalue \(2\), the runner-up in the exploratory
spectrum, is not bounded by \((96/100)^2\). The window above is not a bound
so loose that this runner-up fails to meet it.

## Verification

`02_REGISTRY/research/certificates/a4d_native_golden_channel_hs_contraction_check.py`
— 34/34 exact controls, status
`PASS_CONDITIONAL_EQUAL_WEIGHT_HS_CONTRACTION`.

Negative controls, each able to change the conclusion:

- Swapped \(p\) and \(p^2\) fails the coefficient identity and fails on a matrix.
- Weights \((97,1,1,1)/100\) on the explicit traceless matrix fixed by \(U_0\) have squared Frobenius ratio strictly above \((49/50)^2\).
- The winning block's form at \(9442/10000\) has a negative leading pivot, so the squared norm is strictly greater than \(9442/10000\). A zero pivot would fail this control.
- The skew eigenvalue-\(2\) kernel is not positive definite at \((96/100)^2\).
- The winning block's adjoint commutator is nonzero.
- One sign error in the positive-square-root convention fails the controls \(\sqrt5-2>0\) and \(\sqrt5-3<0\).

Reproduce with:

```sh
python3 02_REGISTRY/research/certificates/a4d_native_golden_channel_hs_contraction_check.py
```

## Named risks and pre-registered attack surface

The strongest self-attack is to read \(49/50\) as uniform on the whole
simplex \(\pi_r>0\). The named second object is the traceless witness fixed
by the single return \(U_0\). At equal weights its norm is strictly below
\(49/50\). At \((97,1,1,1)/100\) the same vector has ratio strictly above
\(49/50\), so the operator norm on that weight exceeds the equal-weight
bound. Equal weights are an extra selection, the same unselected counted
instrument named at `:215-216` of the preparation note. They are not derived
from full support.

Next attacks, in the same order a reader is likely to make them:

- Calling the singular-value bound a spectral gap of a self-adjoint generator. The winning block is not normal.
- Importing `GoldenRelativeChannel.kernel` or claim `D0-CONNECTIVITY-SPECTRAL-GAP-SPEED-001` as this constant. One is a \(2\times 2\) diagonal-weight kernel. The other is the Fiedler value 20 of \(K(9,11,13)\).
- Dropping the off-diagonal Frobenius factor \(2\). The certificate anchors that factor to the entrywise square sum; without it the generalized eigenvalues are a different quadratic form.
- Treating a failed interval enclosure, a power iteration, or a Euclidean `eigh` of the non-symmetric matrix \(H^{-1}L^THL\) as the proof. The proof is unpivoted exact LDL on \(cH-L^THL\). A negative pivot is a negative leading minor. All-positive pivots are positive-definiteness.
- Promoting \(\|\Phi^n(\delta)\|_1\le 4(49/50)^n\|\delta\|_1\), which follows from Cauchy–Schwarz on sixteen eigenvalues, into a sharp trace-norm or diamond-norm gap. The factor \(4\) is the carrier dimension, and no diamond norm is computed.
- Reading the contraction as admission of the golden transition on \((q,D,b,m)\), as a source, or as an Einstein equation.
- Inferring \(b_e\mapsto n_e\) from this norm. The existing affine-CAR transports are already shift-blind, and this channel does not read \(b_e\).

## What this does not show

This is a conditional contraction for one already specified equal-weight
channel. It does not select those weights, admit the channel as a physical
operation, or identify \(I_{16}/16\) with native matter \(m\). It does not
read the affine shift \(b_e\), and it does not combine owned heat or action
terms with the ten-slot covector. It does not give a trace-norm or
diamond-norm rate, and it does not identify the Hilbert–Schmidt norm with
the spectral radius. A radial remainder, a shear jet, and this contraction
are not the coframe–curvature principle \(\mathfrak{V}\). The archive
remainder \(C_A\) is not a compensator for the covector or for this rate.
The own action, Ward identity, refinement, curved roots, soundness and
recovery, G0, and the parent terminals remain open.

The separate shift-blindness note already closes the direct transport route
(`A4D_NATIVE_AFFINE_LINK_SHIFT_BLINDNESS.md:50-55`):

> The two existing
> affine-CAR Dirac operators cannot derive this map: at fixed \(F,U_e,m\),
> their outputs do not respond when \(a_e\), hence \(b_e\), changes. Therefore
> the positive metric covector computed for the candidate v3 cost remains
> conditional on a separate local record/preparation owner that actually reads
> \(b_e\).

The rate does not move the live gate on `conditional_endogenous_preparation`
in `A4D_NATIVE_GRAVITY_DEPENDENCIES.json` at `7a188938`:

> The direct route through ArchiveAffineExteriorLink, archiveAffineLinkedHodgeDirac and archiveSolderedDirac is ruled out: all are invariant under changes of affine shift at fixed linear links (see conditional_archive_shift_blindness). Do not infer b_e->n_e from these transports. The next arrow is a separate already-owned local record/preparation law that reads b_e, with its action, joint variation, full-support preparation and refinement; if none exists, prove completeness of the actual interface before claiming obstruction. Then combine all owned heat/action terms with the candidate ten-slot covector and compare the total source with rho0; keep parent terminals open.

`archive_source_completion.next` on the same tip says to use the existing AF
heat transfer for that representation, and then:

> The remaining owner is the physical full generator L(q,D,b,m), its actual joint field tangent and any changing-algebra terms. Keep all price terms and the candidate metric covector; do not replace the physical archive by K or choose a cancellation.
