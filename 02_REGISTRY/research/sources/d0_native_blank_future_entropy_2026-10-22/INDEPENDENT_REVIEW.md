# Independent review: original stopped futures and the marginal source

22 October 2026. Existing Draft #334, `constitutive/native-programme-v1`.
Independent proof/code review and read-only replay; **PASS**.

## Exact reviewed version

| File | Git blob |
|---|---|
| [Proof](PROOF.md) | `4d86f94ce6cdbf00123c1466ebd54cb8f17a4ba2` |
| [Checker](check_blank_future_entropy.py) | `6c33f0c76794b3b24f0e7d31b40fd0c25f474fb7` |
| [Frozen result](RESULT.json) | `10e4be9b19bcb1a4e454a8235547c410701a29ee` |

All nine input blobs in [README](README.md) were independently matched
against their local bytes. In particular the actual constructor remains
`ee8de4635d24c668949ac9a0186616ab7d59f2ed`, and the consumed original
stopped execution is `2d5f49cf9c6c72f4da3bc5f587a3827eb30992c4`.

## Strongest consumer checked

The original instrument's two fine outcomes are the single ordinary
blank `K_0=B` and `K_1=-2p sqrt(p) Delta`. The selfadjoint contraction
`A` gives `0<Delta<=I` and `B>=(sqrt(5)-2)I>0`; the squared blank
eigenvalues therefore distinguish the distinct Delta blocks.

The original seven-bit first-match rule includes the port bit. Hence
`(1,0^n)` has only mismatches, and the complete remaining matched/aborted
subtree has effect `R_{1,K-n}(0)=I`. Its unconditioned prefix effect is
exactly `F_n=4p^3 Delta^2 B^(2n)`. No anchor is postselected away.
For the declared `K>=d-1`, the weighted Vandermonde determines every
block weight, and `log(rho_*)` lies in the real span of these actual
effects. The quantum KL identity proves the unique entropy maximizer,
including noncommuting competitors, on this same stopped execution.

The blockwise-uniform conditional expectation and its Pythagorean
identity correctly give `0<=I_F<=I_blank<=D(rho||rho_*)`. The local
quadratic bound proves a zero full first differential at the invariant
input even at spectral collisions. The pulled-back scalar is identically
zero, so all its total section jets vanish. Its canonical Poisson adjoint
is zero on the previously proved primitive DATA carrier.

## Actual replay

Executed the final strengthened checker once, without `--write-result`:

```bash
python3 -B 02_REGISTRY/research/sources/d0_native_blank_future_entropy_2026-10-22/check_blank_future_entropy.py
```

**27 checks passed**, including the six stopped-consumer additions.
Every field of the parsed output equals the frozen result. SHA256 checks
before and after execution confirm that proof, checker and result bytes
were unchanged. This is a replay of the strengthened final version, not
the earlier 21-check receipt. No previous scientific suite was rerun.

The maximum stopped-effect/source discrepancies were
`6.172872027514056e-18` / `2.719506629813157e-18`. The retained cap-abort
leaf `(1,0^15)` has positive probability `0.00013085709789574973`.
These are bounded numerical diagnostics; the general theorem follows
from the analytical interpolation/KL argument.

## Scope and resolved corrections

The complete stopped charged operator, comparison/factory charges,
finite preparation source and full history CQ information remain.
The anchor-one charge in the receipt is explicitly only one part of
the stopped charge. Independent RIGHT equations and zero modes remain;
the DATA result does not select a joint preparation or compulsory Info.
Normal input Hessians need not vanish or remain smooth at changing
constraint rank. No mesh-uniform conditioning or full physical GR
closure is asserted.

The final text correctly distinguishes `K=15` (at most sixteen rounds)
from a larger cap (at most `K+1` rounds); increasing a smaller cap is
still paid. README now names the blockwise-uniform conditional
expectation, rather than ordinary pinching. No required corrections
remain. `GR_closed=false`.
