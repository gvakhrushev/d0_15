# Full-Lorentz-balanced q3300: no crossing in the inherited 13D block

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

The mode is evaluated directly at `q=(3,3,0,0)` on the 13-coordinate
section returned by the pinned `pure_memory_interval._section` owner. That
is the complete section of that inherited stored-source chart; it is **not**
the full transverse Hessian of the enlarged full-Lorentz matrix interface.
No map or Schur elimination of the additional interface directions is
proved here, so a kernel coupled to those directions is not excluded. Within
the declared 13-coordinate section, a pinned finite-decimal matrix is used
only as a coordinate preconditioner; its interval-certified left inverse
proves it is nonsingular, and no coordinate in this section is removed. No
spatial-permutation reduction proved only for the old state is used. Since
this q lies outside `Omega-Omega`, the Hessian restricted to this section is
exactly affine: `H_t=H_0+t Delta`. The balanced memory-minus-trace operator
is recomputed from the actual full16 CAR with exact Gaussian-integer
arithmetic; it is not reused from the old witness. All4096 thermal modes,
the full16 Fock carrier, and reference128 are retained through the pinned
scalar and finite-shell owners.

One fixed basis, selected numerically at `t=1/2` and then treated as exact
finite decimals inside outward interval arithmetic, proves the whole path.
At each endpoint its first direction has negative quadratic form, while the
fixed12-dimensional complement is positive definite:

| Endpoint | Upper bound on negative direction | Positive-complement lower margin |
|---:|---:|---:|
| `t=0` | `-0.02534642` | `0.03129354` |
| `t=1` | `-0.01546123` | `0.12203369` |

Both forms depend affinely on `t`, so their strict signs hold throughout the
segment. The basis is invertible; the Schur complement within the declared
13D section then gives inertia `12 positive, 1 negative, 0 zero` for every
`t` and every point of the owned `(d,o)` enclosure. Thus this section has no
q3300 crossing along the balanced path. This is an interval statement, not a
floating eigenvalue scan; it says nothing about kernels involving omitted
full-interface directions.

## What this changes

Stop transferring the old q3300 crossing into the tested 13D section of the
balanced preparation segment. The old crossing belongs to an unbalanced
state that fails the full-Lorentz source equations; this new certificate
shows constant inertia only for the inherited 13D restriction. It does not
exclude a full-interface q3300 kernel whose vector uses additional
boost/link/observer directions or their coupling to this section.

The result leaves the real continuation problem sharply scoped: the omitted
full-Lorentz field directions and their Schur coupling, other field modes,
coupled modes outside `Omega-Omega`, other stationary preparations, and
nonlinear branches are not classified here. Nor does this prove native gate
admission, a physical preparation law, refinement recovery, or Einstein
dynamics. The next useful spectral test must construct the field map from
the full matrix interface to this 13D section, or compute the complete
q3300 Hessian and its coupled kernel, before using this restriction to
exclude a nonlinear branch.
