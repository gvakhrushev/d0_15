# Exact alignment of the golden scale and native memory source

Date: 16 October 2026. Consumer: the G0 question whether the golden parameter
has a response-visible role in the actual retained-memory sector. This note
combines the user-supplied four-level scale formulas with two pinned native
owners. It adds no state, action, selector, time variable, or refinement rule.

Inputs at published checkpoint `b1283e9659ae2c4a9855e7b1200c40163eb83481`:

| Input | SHA-256 |
|---|---|
| `A4D_NATIVE_CLOSED_RECORD_ENGINE.md` | `36eaeb8617630acaeace297fa64e7b8c33b92fc4824133a2b8e3515c4c79520a` |
| `A4D_NATIVE_MEMORY_SOURCE_FIBRE.md` | `37d31c0e3ab9ebfd4e60a105913f46b1c959f97e1be9b0c339a12dc8ce31b014` |
| memory-source `result.json` | `51c2e602f6915df1726eb108b3b22f11745d097ed6e4b7dcf09294573d561e5d` |

## One exact parameter appears in three roles

Set

\[
\phi=\frac{1+\sqrt5}{2},\qquad p=\phi-1=\phi^{-1},\qquad
r=2p-1=\sqrt5-2=\phi^{-3},\qquad \delta_0=\frac r2.
\]

The user-supplied split is `a0 = phi - 1` and `b0 = 2 - phi`. Since
`p + p^2 = 1`, these are exactly `a0=p`, `b0=p^2`; hence
`delta0=(a0-b0)/2`. The proposed dimension scale therefore simplifies,
for every integer D, to

\[
Q(D)=2\delta_0\phi^{D-1}=\phi^{D-4}.
\]

Its four distinguished values are

\[
(Q(1),Q(2),Q(3),Q(4))=(\phi^{-3},\phi^{-2},\phi^{-1},1)
=(r,p^2,p,1).
\]

The native record engine independently has the two-tick return
\[
R=\begin{pmatrix}r&-s\\s&r\end{pmatrix},\qquad
r=2p-1,\quad s=2ap,\quad a^2=p,
\]
so the same `r` is its cosine coordinate and half its trace. More sharply,
the native memory-source owner computes two full-CAR orderings with the same
affine endpoint and the same action value, but their complete link sources
obey

\[
f_{01}=K_0p\,v_0,\qquad f_{10}=K_0(2-3p)\,v_0=p^3f_{01}=r f_{01},
\]
where `K0 > 0` and `v0 != 0` are the already owned geometry-dependent
factor and source vector. The ratio cancels both: it is dimensionless and is
unchanged by a common calibration or geometry scale. Thus the user’s
`Q(1)` equals both the memory-return cosine and the exact attenuation of the
connection source when the two same-endpoint histories are reversed. The
identity is specific to the golden equation: `p^3-(2p-1)=(p-1)(p^2+p-1)`.

This establishes response-visible significance of `p` in the declared
conditional v8 memory/source family. It does not show that this v8 action,
the preparation rule, or the link probe is physically admitted by all of D0.
The dimension label D in `Q(D)` remains the user’s algebraic scale index; no
D0 theorem identifies it with a spacetime dimension or a refinement level.

## The entire memory-source orbit is recurrent and bounded

For the actual whole-blank record orbit, the same source owner gives, after
the one fixed spatial CAR probe,

\[
f_k=-K_0p\,T_{k+1}(r)\,v_0,
\]
with `T_n` the Chebyshev polynomial. Consequently

\[
f_{k+2}=2r f_{k+1}-f_k=4\delta_0 f_{k+1}-f_k.
\]

The closed-record owner proves that R has infinite order. Writing
`r=cos(theta)`, this means `theta/(2 pi)` is irrational. The circle orbit is
therefore dense, and `T_{k+1}(r)=cos((k+1)theta)` is dense in `[-1,1]`.
For fixed `K0,p,v0`, the source readouts are bounded and dense on the segment
`{t v0 : -K0 p <= t <= K0 p}`; they do not grow monotonically or converge.
This gives an exact distinction between the engine’s unbounded symbolic
record complexity and this bounded physical source readout.

The result supports an endless internally changing memory trajectory and
shows that its current source can vary densely. It does not produce growing
spatial volume, an endogenous refinement trigger, or accelerated expansion.
Those require a native transition from retained distinctions to new
admissible child degrees; the owned weighted pullback only copies inherited
values, and its physical pairing remains conditional. The memory-source
owner’s `published_to_GitHub=false` records its original execution-time state;
the source packet is now included in Draft PR #334.

## Exact check

`certificates/a4d_golden_memory_source_alignment_check.py` checks the pinned
input hashes, the golden identities, the path-source ratio, the four-level
normalization, and the Chebyshev source recurrence using exact algebraic
arithmetic. It includes a non-golden rational mutation that must fail the
shared-parameter identity. These checks verify the algebraic bridge above;
they do not replace the owners’ physical-admission or source derivations.

On Python 3.9.6, both the ordinary and optimized runs pass all 38 checks
and emit byte-identical JSON. The non-golden mutation is rejected.

```sh
python3 02_REGISTRY/research/certificates/a4d_golden_memory_source_alignment_check.py
python3 -O 02_REGISTRY/research/certificates/a4d_golden_memory_source_alignment_check.py
```
