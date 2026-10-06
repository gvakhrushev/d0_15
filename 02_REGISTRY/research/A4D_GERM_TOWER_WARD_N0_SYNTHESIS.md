# A4D germ-tower / physical-cokernel / N0 odd-gate synthesis

**Execution:** CONTROL intake, 2026-09-27  
**Parent:** `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`  
**Status:** roadmap/control synthesis; no ClaimMap/BOOK promotion  
**Baseline:** main after merged #297

## 0. Carrier separation

Four nearby objects must stay distinct:

1. the moving metric-null section `q0(d)=vec_sym(dd^T)`;
2. the frozen/cross-character source carrying the historical `8/5` residual;
3. the bare harmonic operator `B_n=C(d(z^n)) q0(d)`;
4. the nonlinear connection-amplitude sector
   `N0=span{lambda1,lambda3,lambda4,lambda6}`.

There is also a fifth object that caused a naming collision in the supplied
synthesis: the **full Gram-lift amplitude coefficient** from merged #296.
It is not equal to the bare harmonic operator `B_n`.

## 1. Repository-owned boundaries

### 1.1 Metric-null and physical transport

Merged exact owners give

```text
C(d) = sum_r d_r K_r
C(d) q0(d) = 0.
```

Merged #290 owns the physical conjugate-paired map on orbit types 5 and 7.
Its frozen/cross-character source can have a nonzero cokernel component,
whereas the actual same-carrier moving-germ source has an explicit image
witness and zero class.

Therefore `8/5` remains a carrier-mismatch/frozen-source diagnostic. It is
not a moving-germ stress coefficient.

### 1.2 Fixed-link Gram lift

Merged #296 owns the analytic frame-lift coefficient

```text
G_n =
  2 * binom(1/2,n) * sigma^(n-1)
    * C(d(z^n)) q0(d),
sigma = d^T eta d.
```

This extra factor `sigma^(n-1)` is load-bearing. Since `sigma=O(h^2)`,
the small-h order of `G_n` is different from the order of the bare
`B_n=C(d(z^n))q0`.

This resolves the apparent conflict between the supplied harmonic-collapse
calculation and the #296 scaling calculation: they were using the same
symbol `F_n` for two different objects.

## 2. Bare harmonic tower: algebra to certify

Write `x_r=d_r` and

```text
M_k(x) = sum_r x_r^k K_r q0(x).
```

Then `M_1=C(x)q0(x)=0`. Since

```text
d_r(z^n) = (1+x_r)^n - 1,
```

the **bare** harmonic operator satisfies

```text
B_n = C(d(z^n)) q0(x)
    = sum_{k>=2} binom(n,k) M_k.
```

Hence for every fixed `n>=2` its first possible homogeneous term is

```text
B_n = binom(n,2) M_2 + O(||x||^5),
```

and `M_2` has degree four. Thus `B_n=O(h^4)` for `x=O(h)`. The scalar
leading-weight generating function is

```text
sum_{n>=2} binom(n,2) s^(n-1) = s/(1-s)^3.
```

But the **full #296 coefficient**

```text
G_n = 2 * binom(1/2,n) * sigma^(n-1) * B_n
```

therefore scales generically as

```text
G_n = O(h^(2n+2)).
```

Both statements can be true simultaneously. The worker registered below
must certify this two-level factorization explicitly and prohibit future
reuse of one name for both towers.

## 3. Current N0 gate: latest #260 result

The earlier execution map saying “degree-7 odd only” is superseded by the
latest exact #260 head.

Current exact status on #260:

- the corrected **resonant** weight is zero through degree 6;
- its degree-7 connection Euler is nonzero;
- however an **orthogonal odd weight is already nonzero at degree 3**
  (COS and SIN differ by sign);
- the next required identity is therefore the **degree-3 orthogonal
  correction**;
- only after inserting that correction is it meaningful to re-evaluate the
  downstream degree-5/7 odd terms and classify the final resonant source.

So #260 remains the unique nonlinear N0 owner, but its earliest live gate is
now degree 3, not degree 7.

## 4. What is closed for execution planning

Do not:

- re-run the old FUGU rank census;
- normalize `8/5` again as candidate moving-germ stress;
- ask #260 to prove the q0 harmonic algebra;
- import #202's Newton component into N0;
- compare `B_n=O(h^4)` directly with `G_n=O(h^(2n+2))` without the
  `sigma^(n-1)` factor.

Any all-`k` physical-cokernel statement about the homogeneous `M_k` still
requires an exact owner; it is not inferred from a few sampled powers.

## 5. Registered bounded worker

`WRK-A4D-Q0-GERM-TOWER-COLLAPSE-CERT` owns only the harmonic naming and
factorization seam:

1. exact `M_1=0`;
2. exact binomial decomposition of `B_n`;
3. universal `M_2` leading term and generating function;
4. exact reconciliation with merged #296 by restoring
   `2 binom(1/2,n) sigma^(n-1)`;
5. maximal justified orbit-5/7 physical-cokernel statement;
6. hostile controls separating frozen/cross-character forcing from the
   moving carrier.

It is independent of the nonlinear N0 calculation.

## 6. Parallel execution map

- **#260:** degree-3 orthogonal odd correction first; then propagate that
  corrected jet to the downstream odd degree-5/7 resonant test.
- **#275:** build the slow same-source response pipeline in parallel; block
  only substitutions that genuinely require the corrected #260 odd chain.
- **#240:** consume #275/#260 terminals; the old “degree-6 even gate” is
  retired.
- **#299:** proof-cost/heartbeat refactor only; no scientific expansion.
- **new harmonic worker:** certify `B_n` versus full `G_n`.
- **#202:** stay on the untruncated stationary witness/no-go; do not use either
  harmonic scaling as a nonlinear bridge.

The intended result is a dependency graph with one owner per unknown, not a
new physical promotion.
