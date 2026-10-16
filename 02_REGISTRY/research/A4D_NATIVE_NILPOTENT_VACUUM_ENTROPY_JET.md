# The nilpotent vacuum lift has no linear occupation-entropy source

**Status:** exact conditional obstruction for one natural finite readout. The
probabilistic readout and its identification with `Info(v)` are not selected by
the native core. This does not close the native source problem or GR.

## Result

The existing affine matter lift has the exact vacuum response

\[
T_b|0\rangle=|0\rangle+|b\rangle,
\]

with degree-zero and degree-one terms. If this output is read by the finite
occupation measurement that distinguishes vacuum from the four-dimensional
one-particle sector, and the degree-one sector is equipped with any smooth
positive metric \(G\), its normalized probabilities are

\[
x=b^TGb,\qquad p_0=\frac1{1+x},\qquad
p_{\mathrm{exc}}=\frac{x}{1+x}.
\]

The resulting binary Shannon entropy is

\[
H_2(x)=\log(1+x)-\frac{x}{1+x}\log x,
\qquad H_2(0):=0.
\]

Along every smooth variation through the flat vacuum, \(b(0)=0\), one has
\(x(t)=O(t^2)\). Since \(H_2(x)=O(x(1+|\log x|))\) as \(x\downarrow0\),

\[
H_2(x(t))=O(t^2|\log|t||),\qquad
\left.\frac{d}{dt}H_2(x(t))\right|_{t=0}=0.
\]

The result is unchanged when the four orthonormal degree-one outcomes are
recorded separately: for probabilities \(p_r=\beta_r^2/(1+x)\), where
\(\sum_r\beta_r^2=x\),

\[
H_{\rm occ}=H_2(x)+\frac{x}{1+x}
H\!\left(\frac{\beta_1^2}{x},\ldots,\frac{\beta_4^2}{x}\right).
\]

The conditional four-outcome entropy is bounded by \(\log4\); hence the added
term is \(O(x)\) and the full occupation entropy still has zero first jet.

## Connection to the open gravitational comparison

The already checked factor-imbalance result gives, on its specified
trace-free factor probe,

\[
\mathcal B'_{\rm tf}=2(E_1-E_2)+C_\varphi\sigma_{\rm tf},\qquad
2(E_1-E_2)>1/10000,
\]

while the flat Einstein covector \(\rho_0\) is zero in all ten slots. A
remainder supplied only by the occupation entropy above has
\(\sigma_{\rm tf}=0\) at this vacuum. It therefore cannot cancel the positive
first term. This is a concrete negative result for the direct proposal
“the vacuum output of the existing nilpotent lift supplies the missing linear
source through its finite occupation entropy.” It does not rule out another
owned term or a non-vacuum preparation.

## Proof and ownership boundary

The Lean owner
`03_FORMALIZATION/D0/Geometry/A4DNilpotentAffineMatterLift.lean`
proves the algebraic identity above through
`nilpotentAffineTranslation_vacuum`. The transported-reference owner
`A4DTransportedReferenceMismatch.lean` proves that a supplied constant
role-basis reference on a pure affine shift gives \(\kappa_q=b\), but explicitly
does not select that reference. The norm, normalization, occupation
measurement, and entropy are additional candidate readout choices; neither
Lean owner asserts them as physical D0 laws.

For a smooth curve write \(b(t)=t v+O(t^2)\) and
\(G(t)=G_0+O(t)\). Then \(x(t)=b(t)^TG(t)b(t)=O(t^2)\). For
\(0<x<1\), \(\log(1+x)\le x\) gives
\(-p_0\log p_0=O(x)\); also
\(-p_{\rm exc}\log p_{\rm exc}=O(x(1+|\log x|))\). Dividing by \(|t|\)
proves the zero directional derivative. The same estimate applies to any
finite refinement of the degree-one outcomes because its conditional entropy
is bounded by the logarithm of the number of outcomes.

Book III defines the graph action using the vertex term `Info(v)` as a
distinguishability gain that lowers uncertainty. It does not identify that
term with the occupation entropy of this affine-lift output. Thus the
calculation tests a plausible existing-channel readout; it does not add an
entropy term to the native action.

The existing v9 four-outcome QND instrument is also a real recording
construction: it retains every \(4^n\) history and proves conservation of its
specified geometric operator. Its own result explicitly leaves an independent
energy law for the persistent outcome tape open, and it does not bind the
instrument's input preparation to \(T_b|0\rangle\). Therefore it supplies a
candidate record channel, but does not remove the missing joint
state/record/action arrow. That boundary is pinned in the exact receipt.

There is a useful conditional strengthening if that instrument is composed
with the nilpotent lift on the same graded carrier. In its two-projection
decomposition, each one-tick branch on a principal two-plane is
\(K_j=A_j I+B_jJ\), where \(J^*=-J\) and \(J^*J=I\); hence
\(K_j^*K_j=(A_j^2+B_j^2)I\). On the common one-dimensional sectors the
effects are scalar as well. Thus the outcome effects are functions of the
instrument's geometric operator. If that operator is the actual Hodge-Dirac
square \(\mathcal D_W^2\), it preserves Fock parity: \(d+\delta_W\) is odd,
so its square is even, whether or not curved-link \(d^2\) vanishes. For
\(\Psi_b=(|0\rangle+|b\rangle)/\sqrt{1+x}\), the vacuum is even and the
created degree-one vector is odd. Therefore \(\langle0|E_j|b\rangle=0\) and

\[
\pi_j(b)=\frac{\langle0|E_j|0\rangle+\langle b|E_j|b\rangle}{1+x}
             =\pi_j(0)+O(\|b\|^2).
\]

For outcomes with \(\pi_j(0)>0\), their Shannon contribution changes by
\(O(\|b\|^2)\). If \(\pi_j(0)=0\), positivity of \(E_j\) forces
\(E_j|0\rangle=0\), so that contribution is
\(O(\|b\|^2|\log\|b\||)\). With four outcomes, the complete tape Shannon
entropy therefore has zero first derivative in the affine-shift direction
at fixed geometry. This does **not** erase the geometric source: when the
metric varies, \(E_j(q)\) itself varies, and

\[
D H_{\rm tape}[V]=-\sum_{j:\pi_j>0}(1+\log\pi_j)D\pi_j[V],\qquad
D\pi_j[V]=\langle0|D E_j[V]|0\rangle+\text{state-preparation terms}.
\]

The displayed derivative is for positive base probabilities; zero-probability
branches use the quadratic/logarithmic estimate above.

The actual finite Hodge owner defines \(\mathcal D_W=d+\delta_W\) with
\(d\) raising degree and \(\delta_W\) lowering degree; consequently
\(\mathcal D_W^2\) preserves parity without assuming \(d^2=0\). The next
section calculates one concrete metric-direction candidate from the actual
v9 instrument. It is a one-tick, trace-prepared scalar test, not the complete
ten-slot derivative on the joint \((q,D,b,m)\) tangent. That full source must
still be compared with \(\rho_0\) and all components of the factor-imbalance
contrast. No tape entropy coefficient may be fitted to the target.

If the native action identifies `Info(v)` with this expected tape information,
its action contribution is \(-D H_{\rm tape}\), because Book III fixes
\(S=\sum\operatorname{Cost}-\sum\operatorname{Info}\). That identification
still has to come from the native record owner.

## Actual v9 one-tick record entropy on the factor probe

This is a sharply specified conditional test of the missing metric term. Use
the actual v9 four-label preparation and words `(I,I,V,V*)`, the flat
trace-prepared carrier `j I_H j*/dim(H)`, and the existing positive pairing

\[
Q(s)=\operatorname{diag}(4e^{2s},e^{-2s}/4,1,1),\qquad L=4.
\]

The v9 owner has `Khat=(I-V)*(I-V)/4`, `kappa=1/(256L^2)` when `ell=1/L`,
and the input compression `j*Khat*j=kappa Delta`. On a principal two-plane
with eigenvalue `t=kappa lambda`, the literal four Kraus branches have scalar
effects

\[
\pi_0(t)=(1-2p^2t)^2,\quad
\pi_1(t)=4p^4t(1-t),\quad
\pi_2(t)=4p^3t^2,\quad
\pi_3(t)=4p^3t(1-t),
\]

where `p=phi^{-1}`, `p+p^2=1`. These follow from the recorded label
preparation and SELECT branches, rather than a fitted probability law. The
sixteen cochain grades have equal multiplicity and are all retained; their
factor cancels only in the normalized trace. Summing all 256 Fourier modes at
`L=4`, retaining all sixteen grades per mode, then differentiating `t` along `Q(s)`, gives
the exact one-tick marginal probabilities and derivatives

\[
\begin{aligned}
\Pi_0&=54275/65536+20983p/131072,&
\dot\Pi_0&=4665p/32768-2835/16384,\\
\Pi_1&=24061/65536-72183p/131072,&
\dot\Pi_1&=6675/16384-20025p/32768,\\
\Pi_2&=1539p/65536-1539/131072,&
\dot\Pi_2&=1005p/16384-1005/32768,\\
\Pi_3&=24061p/65536-24061/131072,&
\dot\Pi_3&=6675p/16384-6675/32768.
\end{aligned}
\]

They satisfy `sum Pi_j=1` and `sum dot Pi_j=0`. Outward interval evaluation
of the Shannon derivative

\[
\dot H_{\rm one}=-\sum_{j=0}^3(1+\log\Pi_j)\dot\Pi_j
\]

gives

\[
0.29472132449356845780<\dot H_{\rm one}
<0.29472132449356845782.
\]

The already-owned full heat source on this same factor path is
`2(E_1-E_2)=2(16/257-256/(2^128+1))`, which lies between
`0.12451361867704280155` and `0.12451361867704280156`. Since Book III uses
`Cost-Info`, identifying this particular `Info` with the one-tick Shannon
entropy would leave the residual

\[
2(E_1-E_2)-\dot H_{\rm one}
\in(-0.170207705816526,-0.170207705816525),
\]

so this natural record entropy overcompensates the heat contrast and does not
make the flat probe stationary. This is a finite, reproducible obstruction
for the specified one-tick trace preparation. It is not a no-go for the full
core: v9 preserves the entire `4^n` tape, and its complete history entropy
and conditional entropy increments are different functionals. The native
owner still has not selected which record statistic enters `Info(v)`, nor
bound its moving preparation on the ten joint metric slots. No physical
source, Ward identity, or GR claim follows from this candidate comparison.

The persistent record has a second, more relevant entropy candidate: its
asymptotic Shannon entropy per tick. Conditional on an initial Fourier
eigenmode, the QND outcomes are iid with law `pi(t_k(s))`. The full initial
trace is a finite mixture of these laws, so its record entropy rate is

\[
h_4(s)=4^{-4}\sum_{k\in(\mathbb Z/4)^4}H_4(\pi(t_k(s))).
\]

Here `pi_2(t)=4p^3t^2` separates distinct nonnegative `t` values; the latent
mode class is observable from long outcome frequencies. Differentiating the
actual 256-mode sum, with the zero mode retained and contributing zero, gives

\[
0.2698613692846649638467< h_4'(0)
<0.2698613692846649638468.
\]

The `Cost-Info` residual against the same heat contrast is
`2(E_1-E_2)-h_4'(0) in (-0.145348,-0.145347)`. Thus even the asymptotic
per-tick Shannon rate of this persistent v9 record does not supply the
required source on this probe. The finite-`n` entropy and its first few
conditional increments remain different quantities; none is identified with
the native `Info(v)` by the current owners.

The current PR also contains v10's full record-tape two-projector energy,
all-length record intertwiners, and a re-certified large-L stationary root.
That is a stronger operator/thermal completion inside its explicitly declared
loop class. It does not identify the quadratic record-consistency energy with
Shannon `Info(v)`, derive the loop from M1, or close AF/spatial refinement,
the physical Ward identity, or GR. This one-tick calculation remains useful
as a hostile test of the simplest entropy interpretation and does not replace
the full-history v10 price.

## Hostile controls and reopening conditions

- At a non-vacuum base with \(x_0=4\),
  \(dH_2/dx=-\log(x)/(1+x)^2\) is nonzero. The vacuum hypothesis is essential.
- The surprisal of a rare excitation branch for \(b=t e_1\) diverges as
  \(-2\log|t|\). Treating that individual surprisal as a smooth source is
  invalid; its probability-weighted mean is the entropy analyzed above.
- The norm \(\|b\|_G\) has a cusp at \(b=0\). It can have a radial linear
  change, but it is not a differentiable source on the smooth variational
  domain used in this comparison.
- A different non-vacuum prepared state, a separately owned local record law,
  or another differentiable native action term remains open. No assumption
  here excludes them.

## Reproduction

The exact checker validates the finite probability identities, entropy
decomposition, vacuum and non-vacuum controls, derives the literal v9
one-tick branch effects and `L=4` marginals, interval-checks the entropy
comparison and the persistent-record entropy-rate derivative, and pins the
Lean/readout/source owners. The small-parameter limit is proved analytically
above; it is not claimed as a Lean-checked logarithmic theorem.

```sh
python3 02_REGISTRY/research/certificates/a4d_native_nilpotent_vacuum_entropy_jet_check.py \
  --output 02_REGISTRY/research/certificates/a4d_native_nilpotent_vacuum_entropy_jet_results.json
```
