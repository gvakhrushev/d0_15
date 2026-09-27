# A4D germ-tower / physical-cokernel / N0 odd-gate synthesis

**Execution:** CONTROL intake, 2026-09-27  
**Parent:** `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`  
**Status:** roadmap/control synthesis; no ClaimMap/BOOK promotion  
**Baseline:** current main after merged #265

## 0. Why this packet exists

Several nearby calculations were being conflated:

1. the moving Gram-lift null germ `q0(z)=vec_sym(d d^T)`;
2. the frozen/cross-character forcing that produces the historical residual
   `8/5`;
3. the physical conjugate-paired map `[A(z)|C(conj z)]`;
4. the independent nonlinear connection-amplitude sector
   `N0=span{lambda1,lambda3,lambda4,lambda6}`.

Main already owns enough exact structure to separate (1)-(3), while open
#260 owns (4). The remaining work should therefore be split by carrier, not
by another rank census.

## 1. Repository-owned facts

The following are already durable on main or on the named live owner and must
not be re-derived in a new lane.

### 1.1 Metric-null complex

Merged coefficient owners give

[
C(d)=sum_{r=0}^3 d_r K_r,qquad
C(d),operatorname{vec}_{sym}(dd^T)=0.
]

The rank/kernel owner proves the nonzero-character kernel line. This is a
moving null section, not a fixed-fibre stress theorem.

### 1.2 Physical carrier and frozen-source split

Merged #290 owns the physical conjugate-paired carrier on orbit types 5 and
7. The cross-character/frozen source has a one-dimensional physical cokernel
component and the historical rational residuals, while the actual
same-carrier moving-germ forcing has an explicit image witness and zero
cokernel class.

Therefore `8/5` is not a stress coefficient of the moving germ. It is a
carrier-mismatch/frozen-source diagnostic.

### 1.3 Fixed-link nonlinear harmonic forcing is a different question

Merged #296 owns the finite Gram-lift second forcing at unchanged links. Its
nonzero quarter-wave forcing is not in conflict with §1.2: fixed raw links
and a connection-stationary continuation are different partials. #285 then
showed that an order-epsilon^2 connection repair can be metric-silent on its
selected branch.

### 1.4 N0 even channel is already consumed

Open #260 records the current carrier-level state: corrected COS/SIN rays
vanish through degree 5; the degree-6 even connection forcings are solved in
rank-24 regular Hessian images, and substitution of those corrections gives
zero metric Euler in all ten Gram slots on the selected line.

The live gate is therefore the **degree-7 odd resonant connection Euler**,
not another degree-6 census.

## 2. New algebraic intake: harmonic tower collapse

The supplied synthesis proposes the following exact algebraic compression.
Write `x_r=d_r` and

[
M_k(x)=sum_r x_r^k K_r,operatorname{vec}_{sym}(xx^T).
]

Then the metric-null identity gives

[
M_1=C(x)operatorname{vec}_{sym}(xx^T)=0.
]

For the n-th character harmonic,

[
d_r(z^n)=(1+x_r)^n-1,
]

hence formally

[
F_n
=sum_r d_r(z^n)K_roperatorname{vec}_{sym}(xx^T)
=sum_{kge 2}inom{n}{k}M_k.
]

Consequently the universal leading homogeneous piece for every `n>=2` is

[
F_n=inom n2 M_2+O(|x|^5),
]

so for `x=O(h)` the raw tower starts at `O(h^4)`; after the established
`h^{-2}` response normalization its leading contribution is `O(h^2)`.
The scalar leading-weight generating function is

[
sum_{nge2}inom n2 s^{n-1}=rac{s}{(1-s)^3}.
]

This compression is elementary once the exact coefficient matrices are
owned, but **main does not yet contain a dedicated certificate for the whole
statement**. It is therefore registered below as a bounded worker instead of
being silently promoted from chat/sandbox arithmetic.

## 3. What is and is not closed

### Closed for execution planning

- Do not re-run the old FUGU rank census.
- Do not normalize `8/5` again as a candidate germ stress.
- Do not make #260 prove the Gram-lift harmonic collapse.
- Do not import #202's Newton component into the N0 odd calculation.
- Keep #275 on its same-source slow-background response lane and let it
  prepare all algebra not dependent on the missing odd-7 coefficient.

### Still theorem/certificate work

The all-harmonic algebraic collapse in §2 needs a repository certificate that
uses the merged exact `K_r` owner. In addition, any stronger assertion that
every individual `M_k` is physical-cokernel exact for all `k` must be
proved from the registered carrier, not inferred from a few sampled powers.
The existing #290 same-carrier theorem remains the authoritative physical
transport owner.

## 4. Single new worker

Register:

`WRK-A4D-Q0-GERM-TOWER-COLLAPSE-CERT`

Its job is deliberately small and independent of #260/#275/#299:

1. reconstruct the exact `K_r` from merged owners;
2. prove coefficientwise `M_1=0`;
3. certify the binomial decomposition of `F_n` and the universal `M_2`
   leading term;
4. certify the scalar generating function;
5. test the owned orbit-5/7 physical cokernel pairings for the required
   low homogeneous pieces and state exactly what general all-`k` conclusion
   is justified;
6. include hostile controls distinguishing frozen/cross-character forcing
   from same-carrier moving transport.

It must not edit #260's nonlinear germ, #275's slow-background continuation,
#202, BOOK, ClaimMap, or release statuses.

## 5. Fast execution map

The work can now run in parallel without collision:

- **#260:** only degree-7 odd COS/SIN resonant Euler + shared cokernel/rank
  verdict.
- **#275:** same-source slow-response pipeline and all substitutions that do
  not require the missing odd-7 coefficient.
- **#299:** proof-cost refactor only; no scientific scope expansion.
- **new worker:** harmonic-tower collapse certificate.
- **#202:** untruncated stationary witness/no-go on its own component.

The intended terminal is not a new physical claim. It is a smaller dependency
graph in which each remaining unknown has exactly one owner.
