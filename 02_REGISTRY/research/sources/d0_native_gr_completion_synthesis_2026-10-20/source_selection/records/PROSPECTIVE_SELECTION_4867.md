# Prospective selection of the already constructed whole-J2 reporter

20 October 2026. Baseline `4867b6d4`, existing PR #334. This note consumes `book_source/MINIMAL_GOLDEN_COMPLETE_SOURCE.md`, especially sections 4–7, and supplies an exact conditional prospective selection theorem. It does not invent a compulsory future task, select a compensation, or assert physical closure.

## 1. What the new baseline already supplies

The whole-J2 coherent scalar is already constructed:

```
t=Tr[C(F-F*)]/(2N_h),
dt|Sigma=gamma_h dJ2,        gamma_h>0.
```

Its three-query output has nonclean probability `4t^4(1-t^2)`. Both geometry and matter are combined before reporting, with the original coupling preserved. Constructing a combined query is therefore not the next task. The earlier additive pointer rank-birth obstruction explains the value of this construction; it does not apply to its quartic cleanup.

The remaining concrete obstruction is already calculated by the owner. At the same initial condition and terminal task, the postrotations `G^k` have prices, for one tick per G,

```
S_coh,k = T0 + k + 1 + q_k - I_R,
S_ptr,k = T0 + k + D_phi((1-q_k,q_k)||(p,p^2)) - I_R,
q_k=sin^2(k theta_G).
```

Set

```
p=phi^-1,
q_0=0,       q_1=p^2,       q_2=4p^3,
L=log_phi(4),       A=4+L,
D2=D_phi((p^6,4p^3)||(p,p^2))=q_2 A-5.
```

The terminal minima select zero-source k=0 (coherent), or k=0,1 (pointer). The source-preserving k=2 loses. A future continuation must overcome these actual gaps; merely requiring signed distinguishability does not exclude k=1.

## 2. Necessary comparison for an arbitrary actual prospective ledger

Let `V_k(y)` denote the **actual** remaining full prospective price after the specified terminal contribution for programme k. If information is not additive, this remainder includes its real conditional/correlation terms. It is not a function chosen to cancel a residual.

At Sigma, k=2 beats both k=0 and k=1 precisely when

```
V_0-V_2 > Delta_20,
V_1-V_2 > Delta_21.
```

Use non-strict inequalities to allow ties. For a primitive G cost `ell_G>0`, the exact gaps are

| Declared information cut | Delta_20 | Delta_21 |
|---|---:|---:|
| coherent | 2 ell_G+q_2 | ell_G+q_2-q_1 |
| pointer | 2 ell_G+D2-1 | ell_G+D2 |

For `ell_G=1`,

```
coherent: Delta_20=2.944271909999159,
          Delta_21=1.562305898749054;
pointer:  Delta_20=Delta_21=2.497384099946687.
```

These are necessary tests for any claimed native continuation. A common extra price, independent of k, cannot change the comparison. Comparison with other k or programmes remains necessary; the following theorem solves every k within a useful specified continuation class.

## 3. A real bit-dependent obligation: exact source accounting

Suppose an independently required future task has the same field-independent conditional remaining prices `v_0,v_1` for each programme, determined solely by the reported bit. Then

```
V_k=(1-q_k)v_0+q_k v_1=v_0-delta q_k,
delta=v_0-v_1.
```

A concrete sufficient accounting contract is a deterministic, fully retained future computation of actual cost `v_b` conditional on b, with no additional branch-conditional entropy. Full copied clocks do not add independent Shannon entropy, and the complete coherent output remains coherently retained. More general tasks must establish their own exact `V_k`; the formula cannot be assumed from an informal decoder description.

The future branch dependence contributes a first source. For the chosen k=2, writing the existing `kappa=8p^(9/2)>0`,

```
d(S_coh,2+V_2) = kappa(1-delta) dt,
d(S_ptr,2+V_2) = kappa(A-delta) dt.
```

One cannot use the continuation to pay the selection gap and then omit this derivative. If the actual `v_b` depend on fields, the additional term `(1-q_2)dv_0+q_2 dv_1` must also be retained.

## 4. Sharp pointer selection window: every integer k, positive same-source coefficient

Define

```
delta_*=(1+D2)/(q_2-q_1)=4.441326519075378...,
A=4+log_phi4=6.880840180825113....
```

**Theorem.** Under the preceding actual continuation contract and an actual
unit primitive price `ell_G=1`, within all admitted postrotations `G^k`,
`k>=0`, the conditions

1. k=2 is the unique prospective price minimum;
2. its source is a **positive** constant multiple of its original terminal source,

hold simultaneously **if and only if**

```
delta_* < delta < A.                                  (1)
```

“If and only if” concerns these two properties together within the stated G^k family and continuation contract. It does not compare unrelated programmes.

Necessity: positive source requires `delta<A`. Beating k=1 requires

```
delta(q_2-q_1)>1+D2,
```

which is exactly `delta>delta_*`.

For sufficiency, k=1 loses by that inequality. k=0 loses because `q_2>q_2-q_1` and its terminal gap is also `1+D2`. It remains to exclude **every** k>=3; no finite path census is needed.

The exact binary Gibbs variational identity gives, for every probability q,

```
D_phi((1-q,q)||(p,p^2))-delta q
 >= -log_phi Z_delta,
Z_delta=p+p^2 phi^delta.
```

Consequently every k>=3 loses to k=2 by at least

```
g(delta)=1-log_phi Z_delta-D2+delta q_2.               (2)
```

Let `q_*(delta)=p^2 phi^delta/Z_delta`. It is increasing, and

```
q_*(A)=q_2,
g'(delta)=q_2-q_*(delta)>=0       for delta<=A.
```

Moreover `delta_*>4`, while

```
Z_4=2 phi,
g(4)=5-(2q_2+1)log_phi2 > 1/2.                       (3)
```

The strict bound follows from `q_2<1` and `log_phi2<3/2`, since `phi^3>4`. Thus throughout (1) **all k>=3 lose by more than half a tick**.

For completeness the threshold bounds require no numerical acceptance:

```
delta_*>4  <=>  p^2 log_phi4>1.
```

Here `p^2>3/8` and `log_phi4>8/3`, the latter because `phi^8=21phi+13<64`. Also `delta_*<5`, since the k=1 gap at delta=5 is

```
5(q_2-q_1)-(1+D2)
 =4-5p^2+q_2(1-log_phi4)
 >7-11p>0.
```

Finally `6<A<7` follows from `phi^2<4<phi^3`. These establish the integer opportunities without relying on rounded logarithms.

**Integer-cost consequence:** if conditional costs are integer ticks and
the actual primitive price is `ell_G=1`, the only integer differences in
the sharp positive-source window are

```
delta=5 or delta=6.
```

Both select k=2 globally within G^k. Their full source coefficients are respectively

```
delta=5: kappa(log_phi4-1) dt >0,
delta=6: kappa(log_phi4-2) dt >0.
```

Numerically the all-k>=3 lower margins from (2) are respectively
`0.940963621459827` and `0.988838643784572` ticks.
At `delta=delta_*`, k=1 and k=2 tie. At `delta=A`, k=2 still wins but its full first source vanishes. The upper endpoint is therefore physically significant, not an arbitrary safety margin.

This theorem identifies what would need to be found in the actual future task: a branch-dependent continuation advantage in the stated range, with the prescribed field dependence and accounting. It does **not** supply or authorize that advantage.

## 5. Coherent cut: selection forces a source-sign reversal

Beating k=0 and k=1 requires

```
delta > max(1+2/q_2, 1+1/(q_2-q_1))
      = 1+2/q_2
      = 3.118033988749895... .
```

The first bound dominates because `q_2>2q_1`. Therefore no such continuation can both select k=2 and retain a **positive** coherent source coefficient `1-delta`: that coefficient is necessarily negative.

For the smallest integer possibility `delta=4`, k=2 is the global minimum within all G^k. For k>=3,

```
[S_coh,k+V_k]-[S_coh,2+V_2]
 =(k-2)-3(q_k-q_2)
 >=1-3(1-q_2)=1-3p^6>0.
```

The margin is at least `0.832815729997476` ticks. Its full first source is `-3kappa dt`. This preserves first-order stationarity zeros, including the original all40+matter roots under their remaining hypotheses, but reverses the source sign. It does not preserve positive normalization or local minimum properties in the physical fields.

More generally `1+2/q_2<delta<1+1/p^6` is a sufficient global selection interval by the same bound. No complete classification outside this sufficient interval is claimed.

## 6. Next consuming premise

The known full-J2 trace query and quartic cleanup have removed the need to construct another matter/geometric reporter. The next experimental or mathematical target is an actual compulsory continuation with:

- an independently specified task/output, not a requirement to produce Einstein's source;
- exact conditional full prices or a proved lower bound meeting section 2;
- all work, clock and information correlations retained;
- source derivatives of the continuation included;
- a comparison with other admitted programmes beyond G^k before any global D_min claim.

Under the pointer branch-only contract, the five-or-six-tick window is a precise search criterion. An unrelated fitted penalty cannot satisfy this premise. If the original physical task instead fixes a coherent cut, its sign reversal must be carried through the stationary/minimum distinction.

`check_prospective_selection.py` verifies the Golden identities, gaps, Gibbs margins and finite diagnostic examples. The all-k conclusion rests on the analytical bound (2), not on a sampled maximum k.
