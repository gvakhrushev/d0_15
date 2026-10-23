# Exact cross-owner preparation/engine-admission test

Status: exact finite cross-owner result for one controlled-price fixture; not a physical-admission theorem.

## Question

Does the unique faithful density minimizing the complete coherent AF preparation price in the two-sector fixture have a square-GNS amplitude representative in the support domain of the named AF-to-CAR engine interface?

This is a deliberately narrow pair test. The preparation owner and the AF/CAR engine owner remain separately authoritative. The result does not select the fixture physically, establish primitive admission, classify the newer retained-controller carrier, or close a global native/GR question.

## Exact inputs and derivation

The preparation owner is [`A4D_NATIVE_PREPARATION_STATIONARY_SOURCE.md`](A4D_NATIVE_PREPARATION_STATIONARY_SOURCE.md), whose §9 defines the complete coherent minimum. Its checker pins its underlying preparation and controlled-record sources. The engine owner is [`A4D_NATIVE_AF_ROLE_ORBIT_CAR_GEOMETRY_2026-10-16.md`](A4D_NATIVE_AF_ROLE_ORBIT_CAR_GEOMETRY_2026-10-16.md), with the exact AF/CAR receipt and source hashes checked by `a4d_native_af_role_orbit_metric_check.py`.

For the fixture effect spectrum in the `M2` block, `E_0=(9/25,16/25)`, the owner-defined conditional prices are the actual relative-entropy prices. The unique minimizing density therefore has eigenvalues proportional to

```text
q_e = exp(-log(phi) * f_0(e)),  e in {9/25,16/25}.
```

The cross-owner checker recomputes both literal owner probabilities and prices, then verifies strict outward interval bounds:

```text
1.08684529796154 < f_0(9/25) < 1.08684529796155,
1.15165203585467 < f_0(16/25) < 1.15165203585469,
1.03167713932214 < q_(9/25)/q_(16/25) < 1.03167713932215.
```

Thus every square-GNS amplitude lifting that minimizing `M2` density has unequal singular values, with ratio

```text
1.01571508767082 < sqrt(q_(9/25)/q_(16/25)) < 1.01571508767084.
```

The owned AF-to-CAR map has rank four; its engine-support equations have rank three and their input preimage is exactly

```text
span{(1,0,0,1,0), (0,0,0,0,1)}.
```

In that preimage the `M2` amplitude is a scalar multiple of `I2`, so its singular values are equal. Right-unitary square-GNS freedom preserves singular values. The remaining `M1` scalar coordinate maps to zero and cannot cancel the `M2` support defect. The minimizing density consequently has no amplitude lift in this named engine-support domain.

## Reproduction and scope

Run, in order:

```sh
python3 02_REGISTRY/research/certificates/a4d_native_af_role_orbit_metric_check.py
python3 02_REGISTRY/research/certificates/a4d_native_preparation_and_clock_binding_check.py
python3 02_REGISTRY/research/certificates/a4d_native_preparation_engine_admission_check.py
```

The new cross-owner checker pins the preparation/controlled-record files and the AF/engine checker, receipt, and owner note; it verifies the receipt's source hashes and checks 35 exact conditions. Its output is compared with the committed [result JSON](certificates/a4d_native_preparation_engine_admission_results.json) in both ordinary and optimized runs. This establishes incompatibility only for this optimizer and this named direct AF-to-CAR support interface. It does not establish that another preparation, expanded interface, or native dynamics is impossible. In particular, the retained-controller coherent completion has an expanded carrier; its image against this support and primitive admission remain unclassified.
