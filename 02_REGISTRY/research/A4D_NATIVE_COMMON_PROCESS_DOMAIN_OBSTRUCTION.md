# Two candidate AF-to-metric bridges fail on the named curved chart

2026-10-16. Exact cross-owner results for the named `lambda=1` matter-clock
readout and the existing full16 adaptive AF/CAR engine.

The chart stores rest coordinates `m0` and defines raw native matter by
`m=rho(F)m0`. The current engine instead stores its CAR vector directly in
`Z[a]^16` and applies its gate to that raw vector. This note records two
separate tests: (i) applying the gate directly to `m0` leaves the comparator
probability domain after one step; (ii) at the chart's curved base point,
no coframe `O` in the owned equality lift makes raw `m` belong to `Z[a]^16`.
The second is an exact arithmetic obstruction to this direct engine/native
identification at this base point. Neither result excludes another native
transition, another admitted chart point, or global physical dynamics.

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

Replay the 64 exact controls in ordinary or optimized mode:

```sh
python3 02_REGISTRY/research/certificates/a4d_native_common_process_domain_check.py
python3 -O 02_REGISTRY/research/certificates/a4d_native_common_process_domain_check.py
```

Both modes agree with the pinned
[`results JSON`](certificates/a4d_native_common_process_domain_results.json).
The raw-engine result is limited to this equality-chart base and direct raw
identification; the rest-coordinate gate test is a distinct candidate map.
The twelve probability tests, all ten transverse equations, full action, AF
primitive admission and other possible charts remain open.
The next scientific target is to find whether any point in the owned equality
graph simultaneously satisfies the literal raw coefficient domain and has
an admitted update. If so, derive `m'=U_s m`, `m0'=rho(F')^-1m'` from that
owner and test the twelve probability-domain conditions, all ten metric
matching rows, all sixteen matter components and the full action derivative.
If not, extend the exact ring obstruction beyond this single base point.
