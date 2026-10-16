# Directly evolving rest coordinates leaves the metric-binding chart

2026-10-16. Exact cross-owner one-step result for the named `lambda=1`
matter-clock readout. The checker applies the actual full16 gate directly to
the chart's rest-coordinate vector `m0` and proves that this direct update
leaves the probability domain on a curved germ.

The AF/CAR engine owner defines its gate on the raw CAR vector `m`, while the
matter-clock chart reads `m0=rho(F)^-1 m`. No owner currently identifies the
gate on `m0` with the raw native transition or derives the simultaneous
`(F,m)->(F',m')` map. Thus this result rejects the direct rest-coordinate
update `m0 -> U_+ m0`; it does not yet show that the actual coupled native
process fails. It is not a no-go for simultaneous coframe motion or all
native physics.

Inputs are pinned at `dfaf7c8df509d5abd83fa60a185ad530feadc9b5`:

| owner | SHA-256 |
|---|---|
| Full16 literal AF/CAR gate | `a4d_native_af_role_orbit_metric_check.py`: `b718a3ea3e3f47087b664cc9bb194e0e09c5ae818836efdba3e63b9c11e4f2d5` |
| Adaptive engine | `adaptive_engine.py`: `1eaf0ed625c78d2779da83cf85e65bf1c1e797a3719da3b786c46cd16733b402` |
| Matter-clock equality chart | `matter_clock_binding.py`: `1b2c668bca6c99ca84a4be513274fddc2c9a82a832368abc4a75ee24f58fbb71` |

## A genuinely curved input in the same full16 chart

Use the chart's actual full16 rest-coordinate vector at the owner's `s=1` reference,

\[
m_*=-2ap\,e_0+(2p-1)e_1+e_{13}+e_{14},\qquad
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

Replay the 37 exact controls in ordinary or optimized mode:

```sh
python3 02_REGISTRY/research/certificates/a4d_native_common_process_domain_check.py
python3 -O 02_REGISTRY/research/certificates/a4d_native_common_process_domain_check.py
```

Both modes agree with the pinned
[`results JSON`](certificates/a4d_native_common_process_domain_results.json).
The finite AF image and primitive-admission boundary remains explicit. The
certificate's selector is computed from `m0[1]`; the raw engine selector is
computed from the raw CAR vector `m[1]`, and their identification is unproved.
The next scientific target is now the missing coordinate bridge: derive the
raw branch selector and the coupled `F,m -> F',m'` transition, then test
`m'=U_s m`, `m0'=rho(F')^-1m'`, the twelve probability-domain conditions,
all ten metric matching rows, all sixteen matter components, and the full
action derivative together.
