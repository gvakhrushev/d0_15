# Two candidate AF-to-metric bridges fail; a fixed-lift extension also exits the chart

2026-10-16. Exact cross-owner results for the named `lambda=1` matter-clock
readout and the existing full16 adaptive AF/CAR engine.

The chart stores rest coordinates `m0` and defines raw native matter by
`m=rho(F)m0`. The current engine instead stores its CAR vector directly in
`Z[a]^16` and applies its gate to that raw vector. This note records four
scoped outcomes: (i) applying the gate directly to `m0` leaves the comparator
probability domain after one step; (ii) at the chart's curved base point, no
coframe `O` in the owned equality lift makes raw `m` belong to `Z[a]^16`;
(iii) for one proper future-preserving coframe, the scalar extension of the
raw gate followed by readout with the same fixed lift leaves that probability
domain; and (iv) this fixed-lift failure persists for actual exact engine-ring
states in an open neighborhood. The scalar-extension calculation at the
center is not itself an engine transition; the nearby-state result uses
admitted ring states but does not assert metric matching there. These results
exclude only the tested direct bridges, not a variable native transition,
other chart points, or global physical dynamics.

Inputs are pinned at `dfaf7c8df509d5abd83fa60a185ad530feadc9b5`:

| owner | SHA-256 |
|---|---|
| Full16 literal AF/CAR gate | `a4d_native_af_role_orbit_metric_check.py`: `b718a3ea3e3f47087b664cc9bb194e0e09c5ae818836efdba3e63b9c11e4f2d5` |
| Adaptive engine | `adaptive_engine.py`: `1eaf0ed625c78d2779da83cf85e65bf1c1e797a3719da3b786c46cd16733b402` |
| Matter-clock equality chart | `matter_clock_binding.py`: `1b2c668bca6c99ca84a4be513274fddc2c9a82a832368abc4a75ee24f58fbb71` |

## A genuinely curved input in the same full16 chart

Use the chart's actual full16 rest-coordinate vector at the owner's `s=1` reference,

\[
m_*=-2ap\,e_{\mathrm{mask}\,0}+(2p-1)e_{\mathrm{mask}\,1}
    +e_{\mathrm{mask}\,13}+e_{\mathrm{mask}\,14},\qquad
a^2=p,\quad p^2+p=1,\quad a,p>0.
\]

The complete 16-coordinate wiring is `w_i=p^2+(m_0-m_*)_i` for
`i=0,...,11` and `X_A=(m_0-m_*)_(12+A)` for `A=0,...,3`. Choose
\(\epsilon=p^{20}\), which is nonzero, belongs to the exact engine ring
\(\mathbb Z[a]\), and is small. On a local spacetime chart take

\[
w_{01,+}(x)=p^2+\kappa x_0^2,\qquad
w_i(x)=p^2\ (i\ne(01,+)),\qquad
X(x)=x+\epsilon e_3,
\qquad \kappa=1/1000.
\tag{1}
\]

This is the same owned full 12-channel comparator, with every outcome
retained. Since its metric depends on `dX` and `dw`, not on a constant phase
offset in `X`, the clock translation leaves the metric germ unchanged.
The existing exact calculation gives

\[
q(0)=\frac{p^3}{2}I_4,\qquad Dq(0)=0,\qquad
R_q(0)=-\frac{2\kappa}{3p^3}=-\frac{1}{1500p^3}\ne0.
\tag{2}
\]

At the origin all twelve effects equal `p^2`, the current is timelike, and
the top-grade coordinate is `epsilon`. In a sufficiently small open
neighborhood, the effects remain in `(0,1/2)`, `X` remains a local coordinate,
the current remains timelike, and `X_3` stays nonzero. The input therefore
lies on a genuinely curved, oriented part of the named equality chart, not
only at its flat center.

## Raw native state is outside the engine coefficient lattice for every coframe

Use the unshifted center `m0=m*` of the curved germ, so its complete
12-channel record still has

\[
q(0)=\frac{s}{2}I_4,\quad s=p^3,\qquad
j=(1,-2/3,0,0).
\]

The actual positive root of the observer pairing is

\[
B=H(j)^{1/2}=\begin{pmatrix}3&2\\2&3\end{pmatrix}/\sqrt5\oplus I_2.
\]

The owned native lift (with every allowed `O` retained) is

\[
F=\sqrt{2/s}\,O B,\qquad m=\rho(F)m_0,\qquad O^TO=I.
\]

Since `rho` is the full exterior representation, its grade-one block is
exactly `F`. Let `u0` denote the degree-one basis vector at mask 1. The grade-one part
of `m*` is `(2p-1)u0=p^3 u0`, hence for
**every** `O` the raw grade-one matter has the same Euclidean squared norm

\[
\|m_{[1]}\|^2
=\frac{2}{p^3}(p^3)^2\|B u_0\|^2
=\frac{26}{5}p^3.
\tag{5}
\]

This number is not an algebraic integer. The element `a` satisfies the
monic polynomial `a^4+a^2-1=0`; `p=a^2` has conjugates `p` and `-1-p`, whose
product is `-1` and whose cubes sum to `-4`. The negative norm shows `p` is
not a square in `Q(p)`, so `[Q(a):Q(p)]=2`; therefore the field trace of (5)
from `Q(a)` to `Q` is `-208/5`, not an integer. Every coordinate in the
engine's exact ring `Z[a]` is an algebraic integer, and a sum of their
squares would also be an algebraic integer. Thus (5) contradicts
`m_[1] in Z[a]^4`.

The result is independent of the orthogonal-frame choice and even holds if
`O` is restricted to proper, future-axis-preserving rotations. It means the
literal current ring engine has no raw input at this named chart base under
the direct identification `m_engine=m_native`. A separate engine-on-rest
adapter would need its own owner and variation law; it is not supplied by
this calculation. The check also verifies two such proper coframes give the
same matched curved metric and rest readout.

## Fixed-lift raw-gate extension leaves the comparator domain

The lattice obstruction above means no actual raw engine step exists at this
base point. To test what a fixed-lift identification would do even after
temporarily extending the gate by scalars beyond its owned coefficient domain,
choose the proper, future-axis-preserving rotation

\[
O=\begin{pmatrix}3&2\\-2&3\end{pmatrix}/\sqrt{13}\oplus I_2,
\qquad F=\sqrt{2/p^3}\,OB.
\]

It sends the grade-one raw vector onto the first coordinate and keeps all six
engine guard coordinates zero both before and after the extended positive
gate. Extend the owner's matrix `U_+` from `Q(a)` to
`Q(a,sqrt(2),sqrt(13))`, apply it to `rho(F)m*`, then read back with the same
`rho(F)^{-1}`. The first comparator effect becomes

\[
w'_0=-\frac{2N}{5(\sqrt5-1)^{3/2}},
\quad
N=-15\sqrt{13}-10\sqrt{10}-10\sqrt{\sqrt5-1}
+5\sqrt5\sqrt{\sqrt5-1}+20\sqrt2+7\sqrt{65}.
\]

The sign is exact. Rational square bounds give
\[
\begin{aligned}
\sqrt{65}&>4031/500,& \sqrt2&>707/500,& \sqrt5&>559/250,&
\sqrt{\sqrt5-1}&>1111/1000,\\
\sqrt{13}&<1803/500,& \sqrt{10}&<3163/1000,&
\sqrt{\sqrt5-1}&<139/125.
\end{aligned}
\]
Each bound follows by squaring positive rationals; for the nested radical,
square once more after adding one. Substitution yields
\[
N>7(4031/500)+20(707/500)+5(559/250)(1111/1000)
-15(1803/500)-10(3163/1000)-10(139/125)
=14749/50000>0.
\]
The denominator is positive, hence `w'_0<0`. Thus even the fixed-lift
linear extension cannot preserve the named comparator chart at this frame.
This supplements the arithmetic exclusion: it still does not describe an
admitted raw transition or rule out a variable lift `F'`.

## The fixed-lift failure persists for nearby exact engine states

The center raw vector is outside `Z[a]^16`, but this does not make the
fixed-lift test an artifact of a point outside the engine domain. The
coefficient ring `Z[a]` is dense in `R`: since `a` is irrational,
`Z[a]` contains `Z+aZ`; for every `epsilon>0`, the pigeonhole principle gives
integers `q != 0` and `k` with `0<|qa-k|<epsilon`, and integer multiples of
`qa-k` approximate any real number. Coordinatewise, the product lattice
remains dense in the subspace where the six guard coordinates are exactly
zero.

For the chosen coframe, the scalar row of `rho(F)^-1` is the scalar identity.
The first fixed-lift effect after the positive raw gate is therefore an
affine functional whose linear row is exactly `(a,-p,0,...,0)`, with
`l1` norm `a+p<2`. At the center its value is `-kappa_F`, where the exact
radical bounds above and `5*(sqrt(5)-1)^(3/2)<225/32` give
`kappa_F>943936/11250000>2/25`. Consequently every raw perturbation with
`||delta m||_infinity<1/50` satisfies

\[
w'_0(m+\delta m)<-\frac{2}{25}+2\|\delta m\|_\infty< -\frac{1}{25}.
\]

The input selector and the post-gate selector are both strictly positive at
the center; the owner gate preserves the exact guard-zero subspace and
`Z[a]^16`. Thus sufficiently close points of the dense guard-zero engine
domain execute the actual `U_+` step. The input probability inequalities,
timelike current and nonzero curvature are open at the base, and one may
choose the approximant off the zero top-grade hyperplane. Therefore the same
fixed-readout chart failure occurs for exact engine-domain inputs that are
initially inside a nearby genuinely curved chart. This is stronger than the
single non-admitted scalar-extension probe, but it remains a fixed-F chart
result: it does not show the perturbed states lie on the ten-row matching
graph, and it does not rule out a variable `F'` or a different native law.

## One literal rest-coordinate step fails the same readout

For this candidate coordinate update, the chart vector `m0` has first-grade
selector `2p-1>0`, so the literal gate uses its positive branch `U_+`. The
checker executes the coefficient-stored engine state and verifies that this
is its literal first transition;
the next state has a nonzero negative selector, so the actual adaptive
engine's `U_-` step is defined as well.

Reusing the same `lambda=1` comparator wiring on the output gives the exact
second effect

\[
w'_1=p^2+(U_+m_0-m_*)_1
    =2-3p+a(4p-3).
\tag{3}
\]

Its sign is proved with rational bounds, not floating point. From
\(p=(\sqrt5-1)/2\), squaring positive rational bounds gives
\(3/5<p<5/8\); hence \(a=\sqrt p>3/4\), \(4p-3<-1/2\), and
\(2-3p<1/5\). Thus

\[
\boxed{w'_1<-\frac38+\frac15=-\frac7{40}<0.}
\tag{4}
\]

The output of this candidate rest-coordinate step is still a real full16
engine state in the guard sector. Its chart current remains timelike,

\[
J'=(1,2/(3+p^{40}),0,0),\qquad
J'^T\eta J'=1-4/(3+p^{40})^2>5/9,
\]

and its top-grade coordinate is `-a p^20-p`, which is nonzero. The failure
is specifically that the named fixed comparator can no longer form a real
channel from the evolved matter: its required effect weight is negative.
The current and orientation did not disappear.

**Scoped verdict:** the candidate direct rest-coordinate update
`m0 -> U_+ m0` does not close on the existing `lambda=1` curved
metric-binding chart, even for one step. The unresolved raw-state transition
has the form `m=rho(F)m0`, `m'=U_s m`, `m0'=rho(F')^-1 m'`, with the branch
selected from the raw engine coordinate and `F'` determined by the common
process. The repository has not derived or admitted this map, nor checked
its all-ten metric matching, all-sixteen matter components, AF image, or
complete differentiated action. No global selector or parent NO-GO follows.

Replay the 93 exact controls in ordinary or optimized mode:

```sh
python3 02_REGISTRY/research/certificates/a4d_native_common_process_domain_check.py
python3 -O 02_REGISTRY/research/certificates/a4d_native_common_process_domain_check.py
```

Both modes agree with the pinned
[`results JSON`](certificates/a4d_native_common_process_domain_results.json).
The 93-check result concerns the named unshifted chart base, the distinct
rest-coordinate candidate, and the fixed-lift neighborhood; it does not
cover another chart point.

The existence target has since been met at a different point. The separate
[498-check complete-field owner](certificates/a4d_native_complete_field_source_check.py)
contains a literal `Z[a]^16` matching input and its actual engine step; for
that output, every Lorentz frame at fixed `q=eta` misses the same comparator
probability interval. See [Section 3.1](A4D_NATIVE_COMPLETE_FIELD_SOURCE_AND_TRANSPORT.md).
This does not contradict the base-point ring obstruction above. The open
critical step is now a native joint `q,m` transition (or an independently
owned change of readout) that follows from the full source/action; `q'` may
not be chosen to repair the channel by hand. Its moving reference, all
sixteen matter components, ten metric rows, AF admission and full action
derivative must be checked together. This is a fixed-`q` obstruction for a
specific actual input, not a global no-go; other processes, variable `q'`,
primitive AF admission and the full GR/root tasks remain open.
