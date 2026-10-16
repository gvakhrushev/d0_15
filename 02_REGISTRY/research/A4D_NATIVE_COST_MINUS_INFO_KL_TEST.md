# SOURCE #310: conditional Cost-minus-Info test on the actual three-round record

15 October 2026. RESEARCH / finite QND code-versus-entropy test.

## Question and scope

The native comparator already has a literal three-round record and a fixed
golden prefix code: no-error is `0`, return/error is `10`. Book III defines
the path action as `sum Cost - sum Info`, but the native owner has not yet
identified `Info(v)` with a record statistic. This note tests one concrete
candidate: the Shannon entropy of the actual three-round tape, added by the
chain rule over its three vertices. It does not install that candidate as the
native law.

The calculation is restricted to a QND eigenstate of the comparator, where
the three outcomes are iid. Let `N` be the number of errors, `T=3`, `p=phi^-1`,
and let `r` be the actual error probability per round. The actual and golden
laws on a word `omega` are

```
q_r(omega) = r^N (1-r)^(T-N),
mu(omega) = p^(T+N).
```

The reference is normalized because `p+p^2=1`. Its code length is exactly
`-log_phi mu(omega)=T+N`. If the proposed `Info` is the Shannon entropy of the
actual tape in the same `log_phi` units, then the finite-word action is exactly

```
E_q[T+N] - H_phi(q) = D_phi(q || mu)
  = T[(1-r)log_phi((1-r)/p) + r log_phi(r/p^2)].
```

This is the code-length/entropy identity for this specified instrument and
reference. It is not a proof that the native `Info(v)` owner selects that
entropy, and it does not replace the native Cost-minus-Info action map.

## Radial source on the certified v10 box

Use the already certified `L=8` v10 root box, without refitting its center:

```
d0 = 0.063635191594344535042829697433316630182693569761541 +/- 1e-12
epsilon = d0 (128 - 64 sqrt(2))
ell = 1/8,  kappa = ell^2/256 = 1/16384,  gamma = 4 p^3
r = gamma kappa epsilon.
```

Along the fixed radial path `epsilon(t)=exp(-2t) epsilon`, `r'(0)=-2r`.
The cost-only normalized source is `-2 epsilon`. The action contribution
`-H_phi` has derivative

```
2 epsilon log_phi((1-r)/r).
```

Therefore the normalized material source for this conditional `Cost-Info`
candidate is

```
-2 epsilon log_phi(r / (p(1-r)))
  in (83.39406619, 83.39406620).
```

The `-Info` term shifts the source relative to the existing cost-only v10
root by

```
2 epsilon log_phi((1-r)/r)
  in (88.16547511, 88.16547512).
```

Thus this Shannon-tape candidate does not preserve radial stationarity at the
existing v10 root of `H+J+R0`, where `R0` is the code-cost term without `Info`:
with the same heat and feedback, the additional term moves that root's
normalized source by a strictly positive amount. The finite three-round calculation is exact in `r`; the
outward intervals use the entire inherited root box. A control at `r=p^2`
recovers `q=mu` and zero KL derivative, confirming the reference convention.

## What this resolves

It closes one tempting shortcut: identifying the native information term
with Shannon entropy of the comparator's actual three-round tape does not
preserve the radial root of the existing `H+J+R0` source. This is a conditional
obstruction for that specific readout and radial direction. It is not a
no-go for other native information functionals or states, and it does not
establish the full ten-component source, the joint `(q,D,b,m)` tangent,
physical Ward identity, or GR.

The existing Lean `ActionProtocol` does not choose this candidate: its fields
are only an action assignment, zero cost for identity transitions, and a unit
lower bound for nontrivial transitions. It has no record, `Cost`, or `Info`
field. The present calculation therefore reads the Book III prose as a
conditional proposal and does not inherit an entropy law from that Lean type.

The remaining high-value proof is still the native history-to-readout map:
derive the actual `Info(v)` from the owned primitive records, including its
joint variation with `Cost`, and compare that complete derivative with the
required source. No coefficient or counterterm is fitted here.

## Reproduction

Run:

```
python 02_REGISTRY/research/certificates/a4d_native_cost_minus_info_kl_check.py
cd 03_FORMALIZATION && lake env lean ../02_REGISTRY/research/certificates/a4d_native_cost_minus_info_kl.lean
```

The Lean capsule proves the finite one-round and three-round code/entropy/KL
identity; it does not select native `Info`. The checker validates all eight
words, normalization of both measures, the symbolic KL/source identities,
the inherited v10 root receipt, outward interval separation, the compiled
Lean output, and negative controls for the golden law, root, and mixture
scope. Its receipt is
`02_REGISTRY/research/certificates/a4d_native_cost_minus_info_kl_results.json`.
