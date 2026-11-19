# Coherent AF preparation source on the flat factor shear

Status: exact cross-owner first-jet test for one corrected golden-determinant/AF-price route. It is not a native-action or GR theorem.

## Test

The existing factor-imbalance owner fixes a volume-preserving homogeneous metric tangent. In the positive orthonormal chart it is

```text
V = diag(2,-2,0,0).
```

The solder lift in the factor owner gives the corresponding physical Lorentz path; on this path the flat Einstein covector is zero in all ten metric slots. The same owner proves that, at `beta=log(2)`, the full Hodge heat source is `2*(E1-E2)>1/10000` for every `L>=2`, while the fixed-golden two-tick feedback remainder has zero first variation.

The golden-cylinder record owner supplies the flat carrier's complete 572 normal shapes: twelve active matrices

```text
A_k = -2 k k^T / sqrt(12 p^3),   k=e_i +/- e_j,
```

and 560 zero shapes. Every active matrix has rank one. For a metric deformation, the raw shape endomorphism has jet `-V A`; in the orthonormal tangent frame used by the determinant compiler the equivalent symmetric jet is

```text
dA = -(V A + A V)/2.
```

For each rank-one shape, `e2(A)=det(A)=0`. Direct differentiation gives

```text
de2 = tr(A) tr(dA) - tr(A dA) = 0,
ddet = tr(adj(A) dA) = 0.
```

The same identities hold for the 560 zero shapes. Therefore every compiled setting

```text
u_i = t^2 e2(A_i) + t^4 det(A_i)
```

has `u_i=du_i=0` on this probe. The literal golden-determinant effect
`E_eff=p^2[I+2p^6 sum_i u_i Q_i]` remains `p^2 I` to first order, with `dE_eff=0`.

The 572 geometric settings are also addressable in the existing literal AF
owner, rather than inferred from its earlier 64-setting example. Its
`same_cost_addresses` constructor supplies 715 equal-cost candidates for
`length=13, returns=4`; taking the first 572 gives 572 distinct settings.
Each setting has prefix cost 17 and active-leaf cost 20. The complete cut has
10,946 ready leaves and 6,765 pending leaves; the 1,144 active success/failure
leaves are distinct, and every other ready or pending leaf remains in the cut.
Map shape `i` to address `i`. The actual addressed-effect constructor returns
`p^2` on every leaf, and its setting parameters and first jets are all zero.
This verifies the full 572-setting effect-level composition in the finite AF
carrier. A hostile control sets one setting parameter to `1/2`; exactly its two
ready leaves change, while all other ready and every pending leaf stay blank.
This confirms the address/effect test detects a nonzero setting without
discarding any part of the carrier. Primitive admission of the complete
physical program remains open.

## The actual preparation-price derivative

The AF preparation owner gives the unique faithful density minimum and its envelope source

```text
sigma*_j = mu_j exp(-log(phi) f_j(E_j))/Z,
dA* = sum_j Tr[sigma*_j f'_j(E_j) dE_j].
```

Since this candidate has `dE=0`, its optimized AF price source is exactly zero. At the blank effect `E=p^2 I`, the minimizing `M2` amplitude is a scalar multiple of `I2`; that direction is the existing engine-support trace line. This removes the linear support obstruction at the blank direction, but it does not prove that the optimizer's coefficient or the full preparation is physically admitted by the engine.

The result is sharper than testing only a non-scalar effect. The earlier `(9/25,16/25)` fixture has an optimizer outside the named direct engine-support fiber. Here the blank-effect minimizer lies on its linear support direction, yet its source still vanishes on the factor shear. Together with the owned heat and fixed-gate feedback derivatives, this corrected candidate supplies no stress capable of canceling the heat source. It is therefore not stationary on the tested flat trace-free probe if these are the only terms in the proposed sum.

## Scope and next mathematical obligation

This is a first-jet result on one exact flat reference carrier. It does not classify the uncorrected determinant circuit's full archive action, prove primitive admission of the coherent correction, bound a refining secant for a different complete action, or rule out other native source terms. The direct fixed-gate/AF-price route is exhausted on this probe; a surviving route must derive a nonzero source from a separately owned native variation and include its complete archive and matter contributions. No source is assigned from `rho0`, and no new selector or action is introduced.

Reproduce with:

```sh
python3 02_REGISTRY/research/certificates/a4d_native_factor_imbalance_remainder_check.py
python3 02_REGISTRY/research/certificates/a4d_coherent_compilation_cost_descent_check.py
python3 02_REGISTRY/research/certificates/a4d_native_preparation_factor_shear_check.py
python3 -O 02_REGISTRY/research/certificates/a4d_native_preparation_factor_shear_check.py
```

The new exact checker pins the flat normal-volume, determinant compiler, coherent AF compilation, preparation, AF/CAR support, and factor-imbalance owners. Its exact checks include all 572 active/zero normal settings, the 572-to-572 actual AF address map, and the complete addressed effect. Ordinary and optimized Python modes compare against the committed [certificate JSON](certificates/a4d_native_preparation_factor_shear_results.json). No new Lean declaration is claimed.
