# Full-Lorentz balanced memory path has no q3300 crossing

Date: 2026-10-16. Exact finite-dimensional continuation of the existing
[full-Lorentz matrix interface](A4D_NATIVE_FULL_LORENTZ_ADJOINT_SOURCE.md).
Replay and outward interval output are in
[`sources/d0_full_lorentz_balanced_memory_path_2026-10-16/`](sources/d0_full_lorentz_balanced_memory_path_2026-10-16/README.md).

## Result

The earlier q3300 spectral-flow certificate belongs to the old pure state
`(|mask1>+|mask15>)/sqrt(2)`. The exact full-Lorentz source owner shows that
this state fails the new boost Euler rows: its occupation numbers are
`(1,1/2,1/2,1/2)`. It is therefore not a stationary preparation in the
enlarged interface, and its crossing cannot be transferred to the
full-Lorentz problem.

For the full-Lorentz-balanced witness

```text
chi_bal=(|mask0>+|mask1>+|mask14>+|mask15>)/2,
sigma_t=(1-t) I16/16 + t |chi_bal><chi_bal|,  0 <= t <= 1,
```

the full16 CAR calculation gives all four occupation numbers `1/2`. The
pinned full-Lorentz owner proves that the balanced endpoint has the same
homogeneous field sources as the faithful endpoint, that all twelve boost
equations vanish, and that the Dirac square is scalar on all16 Fock
components. The field source is affine in the reduced state. Each `sigma_t`
is a density matrix. A concrete purification uses 17 orthogonal reference
slots:

```text
Psi_t=sqrt(1-t)*(1/4) sum_{a=0}^{15}|a>|a> + sqrt(t)|chi_bal>|r_16>.
```

Its partial trace is exactly `sigma_t`, and the retained reference has
dimension128. Since the Dirac square is scalar on the full carrier, every
such purification satisfies the matter Euler equation. The remaining field
rows are affine in `sigma` at this fixed root, so the shared zero-source
endpoints imply zero source all along the segment. Thus this specified
segment consists of stationary points of the declared full-Lorentz matrix
interface at the same owned root. This does not establish admission by the
original D0 primitives.

The mode is evaluated directly at `q=(3,3,0,0)` on the complete
13-coordinate native mean slice. A pinned finite-decimal matrix is used only
as a coordinate preconditioner; its interval-certified left inverse proves
it is nonsingular, and no Fourier or field direction is removed. No
spatial-permutation reduction proved only for the old state is used. Since
this q lies outside `Omega-Omega`, the complete reduced Hessian is exactly affine:
`H_t=H_0+t Delta`. The balanced memory-minus-trace operator is recomputed
from the actual full16 CAR with exact Gaussian-integer arithmetic; it is not
reused from the old witness. All4096 thermal modes, the full16 Fock carrier,
and reference128 are retained through the pinned scalar and finite-shell
owners.

One fixed basis, selected numerically at `t=1/2` and then treated as exact
finite decimals inside outward interval arithmetic, proves the whole path.
At each endpoint its first direction has negative quadratic form, while the
fixed12-dimensional complement is positive definite:

| Endpoint | Upper bound on negative direction | Positive-complement lower margin |
|---:|---:|---:|
| `t=0` | `-0.02534642` | `0.03129354` |
| `t=1` | `-0.01546123` | `0.12203369` |

Both forms depend affinely on `t`, so their strict signs hold throughout the
segment. The basis is invertible; the Schur complement then gives inertia
`12 positive, 1 negative, 0 zero` for every `t` and every point of the owned
`(d,o)` enclosure. In particular there is no q3300 crossing on this
full-Lorentz-balanced path. This is an interval statement, not a floating
eigenvalue scan.

## What this changes

Stop treating the old q3300 crossing as a candidate full-Lorentz nonlinear
branch. It is a valid obstruction inside its old stored-source domain, but
that domain excludes the new balanced endpoint. The balanced branch has no
linear q3300 kernel anywhere along the tested stationary preparation
segment, so a q3300 nonlinear bifurcation cannot be obtained from this
memory interpolation.

The result leaves the real continuation problem sharply scoped: other field
modes, coupled modes outside `Omega-Omega`, other stationary preparations,
and nonlinear branches are not classified here. Nor does this prove native
gate admission, a physical preparation law, refinement recovery, or Einstein
dynamics. The next useful spectral test must consume the balanced full-
Lorentz owner directly and search for a kernel that survives the actual
source constraints; repeating the old-state q3300 calculation is closed.
