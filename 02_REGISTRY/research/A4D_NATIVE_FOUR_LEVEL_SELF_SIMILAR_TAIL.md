# Four-level activation and the self-similar Fibonacci tail

Research synthesis, 2026-10-14. Source: #310 at
`1018e73be589ddff07dace06d8872caa54b689be`.
This note tests the supplied older `phi`/`delta` notes against the owned
Fibonacci AF record and Jones transport constructions. It derives an exact
recursive state-space tail. It does not claim a physical spatial expansion,
clock, matter source, or GR realization.

## What the old algebra does and does not force

Let `phi=(1+sqrt(5))/2`, `psi=(1-sqrt(5))/2`, and `p=phi^(-1)`. The four
relations `phi+psi=1`, `phi*psi=-1`, `phi^2=phi+1`, and `psi^2=psi+1` are
consistent, but they are not four independent invariants. The two Vieta
relations imply the two quadratic relations, by

```text
phi^2 - phi - 1 = phi*(phi+psi-1) - (phi*psi+1),
psi^2 - psi - 1 = psi*(phi+psi-1) - (phi*psi+1).
```

The sign `phi-psi=sqrt(5)` uses the ordering of the roots. Thus the four
identities are an exact algebraic package, not four separately necessary
physical mechanisms.

The split in the notes is nevertheless useful. With

```text
a0 = phi-1 = p,       b0 = 2-phi = p^2,
delta0 = (a0-b0)/2 = p^3/2,
```

we have `a0+b0=1`. If the same split is applied again to a scalar `s`, its
half-difference is exactly `delta0*s`; repeating that *chosen scalar
operation* gives powers of `delta0`. The native AF state recursion below is a
different map. `Q(D)=2*delta0*phi^(D-1)=phi^(D-4)` is an exact scalar
identity, so `Q(4)=1` is its normalization; it does not derive four
spacetime dimensions. Likewise, the half-difference convention alone does
not prove a universal physical factor of two.

## The special four-level activation

The owned [record activation construction](A4D_NATIVE_FIBONACCI_RECORD_ACTIVATION.md)
proves that three literal AF inclusions (four levels including the input) are
necessary and sufficient for its specified covariant four-copy full-record
class. Necessity comes from the conjugation-fixed subspace dimensions
`2,3,7,18`: the input has eight fixed directions across four copies, so the
first two target levels cannot contain an equivariant isometric image; the
third can and has an explicit construction. This is a precise startup
threshold for that apparatus, not a general minimum depth for every physical
system.

## The tail forced by the same AF incidence

The two AF summands follow the deterministic substitution/count recursion

```text
A -> AB,    B -> A,
(A_(n+1),B_(n+1)) = (A_n+B_n,A_n),   (A_0,B_0)=(1,1).
```

Its incidence matrix has Perron factor `phi`. The forced normalized trace
weights of the two summands are

```text
u_n = p^(n+1) A_n,       v_n = p^(n+2) B_n,       u_n+v_n=1.
```

Using `p+p^2=1`, their exact one-step evolution is

```text
(u_(n+1),v_(n+1))^T = M (u_n,v_n)^T,
M = [[p,1],[p^2,0]].
```

The eigenvalues of `M` are `1` and `-p^2`. Its normalized fixed point is
`(u_*,v_*)=(1,p^2)/(1+p^2)`. The initial weights are `(p,p^2)`, hence for
every `n >= 0`

```text
(u_n,v_n) = (u_*,v_*) + (-p^2)^n * (-p^4,p^4)/(1+p^2).
```

This proves a genuine, forced self-similar tail in the owned AF state tower:
block counts grow with Fibonacci factor `phi`, while the two normalized
sector weights approach their fixed proportions with alternating contraction
factor `p^2`. The half-difference `eta_n=(u_n-v_n)/2` obeys

```text
eta_(n+1) = p/2 - p^2*eta_n,       eta_0=delta0.
```

It therefore does **not** follow the pure scalar rule
`eta_(n+1)=delta0*eta_n`. The supplied scalar recursion and the native AF
refinement share exact golden constants, but their transition laws differ.
The summands `A,B` are mathematical AF sectors; identifying them with archive
and visible matter, or with dark and light sectors, is still an extra physical
map that the current owners do not supply.

## An actual all-level record transition

The finite frames at separate levels do not become coherent under the passive
AF inclusion. The scoped analytic result
[A4D_NATIVE_FIBONACCI_LIMIT_FRAME_OBSTRUCTION.md](A4D_NATIVE_FIBONACCI_LIMIT_FRAME_OBSTRUCTION.md)
shows that no four mutually orthogonal copies of the full old bimodule can be
made exactly natural under those ordinary bonds in the multiplicity-one
standard AF GNS limit.

There is, however, a concrete route for the *prepared record corner*. The
[all-level Jones transport](A4D_NATIVE_JONES_RECORD_TRANSPORT.md) constructs
the level-dependent composite
`widehat_alpha_n = Ad_(R_n) after alpha`. It exactly transports the old
corner, every corner matrix outcome including off-diagonal records, its
conditional vector, and the full orthogonal complement across adjacent
levels. This is an owned internal recursive transition, not a passive
inclusion. The no-go result for ordinary bonds does not rule it out.

## The next decisive bridge

The strategic hypothesis now has a finite mathematical core: a four-level
activation threshold, followed by an exact Fibonacci recursion and a
corner-record transport that works at every level. The high-value next test
is whether the existing native preparation and action *admit this Jones
composite* and bind its full state, readout, and variation to the constrained
`(q,D,b,m)` carrier. In particular, derive how its level growth changes a
physical metric/volume readout and its tangent; do not identify AF block count
with spatial expansion by analogy alone. If that binding is derived, it is a
candidate engine to test against curved roots and the source/Ward identities.
If it is not, classify the obstruction for the complete owned class. The
parent #310 terminal and the physical GR claims remain open either way.
