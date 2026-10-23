# The whole owned blank family misses the canonical Jones conditional corner

15 October 2026. Exact extension of the existing level-three AF/CAR state
test. This closes the fixed-path whole-blank family only; it is not a no-go
for other AF paths, other owned preparations, physical admission, or the D0
core.

## Exact result

The earlier level-three test showed that the golden seed
\(m_0=B(a,p)\), \(a^2=p\), \(p^2+p=1\), has nonzero mass outside the canonical
Jones conditional corner. I extended that computation over the **entire
already-owned real whole-blank family**

\[
m_0=B(x,y),\qquad x^2+y^2=1,
\]

without changing the level-three same-simple path identification. I carried
each seed through the literal full record step, the existing 32-dimensional
AF/CAR weld, the native (A_3\to A_9) right-module path frame, and the
canonical Jones corner projection (e).

Let \(v(x,y)\in\mathbb R^{89}\) be the resulting normalized source row and
\(H=I-e). The exact off-corner Gram matrix is diagonal:

\[
\begin{aligned}
M_{xx}={}&8\sqrt2 ap+16ap-10a-5\sqrt2 a-5\sqrt2 p
           +\tfrac{27}{2}p-\tfrac{15}{2}+3\sqrt2,\\
M_{yy}={}&-26ap-8\sqrt2 ap+5\sqrt2 a+16a-\tfrac{49}{2}p
           +5\sqrt2 p-3\sqrt2+16,\\
M_{xy}={}&0,
\end{aligned}
\qquad
v(x,y)^T H v(x,y)=M_{xx}x^2+M_{yy}y^2.
\]

Exact rational interval arithmetic, using squared rational brackets for
\(p=\varphi^{-1}\), \(a=\sqrt p\), and \(\sqrt2\), certifies

\[
0.5663<M_{xx}<0.5664,
\qquad
0.9934<M_{yy}<0.9936.
\]

Consequently every normalized state in this whole-blank family has more
than (0.5663) of its norm outside the canonical Jones conditional corner.
No choice of (x,y) in this existing preparation family binds to the
canonical conditional vector under this path identification. The fixed golden
seed's value (0.7295098\ldots) is one point of a uniform family obstruction,
not a special numerical accident.

The result also explains why discarding the off-corner part is not harmless:
the owned source-active odd-tick current is \(J=e_0+2xy e_1\), with
\(\ell(J,J)=(x^2-y^2)^2\). At the golden seed the recorded current is
\((1,2ap,0,0)\), with Lorentz norm \(p^6\). The same prepared states
necessarily retain a large component outside the canonical conditional
corner. This is an algebraic fact about the fixed AF path, not a physical
light/dark assignment.

## What survives and what does not

The calculation rules out repairing the canonical-state mismatch by adjusting
the two amplitudes in the already-owned blank preparation. It does not show
that the native state is invalid. The actual recorded CAR vector remains a
normalized vector state in the (A_9) GNS space, and the owned Jones
homomorphisms transport its operator corner to later levels. The
[positive-state refinement](A4D_NATIVE_AFCAR_POSITIVE_STATE_REFINEMENT.md)
now constructs its compatible positive extension by composing with the
already-owned trace-adjoint conditional expectation; it preserves every
polynomial readout in the transported record/current algebra. Thus forcing
equality with (e/p^3) is unnecessary and is no longer a viable route within
this blank family. The joint ((q,D,b,m)) pullback and its physical admission
remain open.

No new state selector, physical postulate, action, or claim status is added.
The test uses the actual CAR gate, blank isometry, AF/CAR weld and Jones path
frames already owned by #310.

## Reproduction and source pins

From the repository root:

```sh
python3 02_REGISTRY/research/certificates/a4d_native_afcar_blank_family_state_check.py
```

The checker reconstructs the full (x,y)-dependent state and the Gram matrix
from the pinned source owners. It also proves its strict positive bounds with
outward rational intervals; it does not rely on a floating-point sign test.

| Input | SHA-256 |
|---|---|
| `A4D_NATIVE_AFCAR_CURRENT_COMMUTANT_BOUNDARY.md` | recorded in certificate |
| `A4D_NATIVE_CORRELATED_CURRENT_TRANSITION.md` | recorded in certificate |
| `a4d_native_afcar_current_commutant.py` | recorded in certificate |
| `a4d_native_correlated_current_transition.py` | recorded in certificate |
| AF activation and Jones transport owners | recorded in certificate |

No CORE theorem is promoted, no existing parent terminal is closed, and the
physical admission, source/Ward identity, curved root and GR remain open.
