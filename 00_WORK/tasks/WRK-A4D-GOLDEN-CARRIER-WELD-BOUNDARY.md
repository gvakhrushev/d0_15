# WRK-A4D-GOLDEN-CARRIER-WELD-BOUNDARY

## Class

WORKER / FORMALIZATION

## Parent

`CTRL-GRAVITY-DYNAMICS-CLOSURE`

## State

PLANNED

## Start gate

SATISFIED once PR #104 lands on `main`.

Primary durable input:

`02_REGISTRY/research/MEMO_A4D_GOLDEN_ROLE_PHASE_CARRIER_OPERATOR_WELD.md`.

Required existing owners:

- `D0.Geometry.A4DGoldenCarrierWeldBoundary`;
- `D0.Geometry.A4DGoldenRolePhaseRGDefect`;
- `D0.Algebra.FibonacciAFTower`;
- Role-phase product carrier and projection owners.

This worker formalizes only the repaired truth boundary from PR #104.

It must **not** construct the surviving Hilbert correspondence, choose an index rule, or
touch `J`, `D_H`, `H(e)`, physical time, stress, or Einstein dynamics.

## Objective

Lean-own the exact boundary:

```text
owned consecutive Role-phase set bonding
  != nontrivial group refinement;

AF stage -> commutative Role algebra
  has exact early-stage character exceptions
  and no unital map from k >= 2;

trivial-source Role equivariance
  lands in the invariant sector;

finite cardinality/GNS mismatch
  is owned only on the enumerated range.
```

Target terminal:

`GOLDEN-CARRIER-WELD-BOUNDARY-LEAN-OWNED-CORRESPONDENCE-INDEX-RULE-RESEARCH-REQUIRED`.

## Mandatory packages

### 1. Group-refinement boundary

Prefer a small general algebraic lemma reusable by the Role product.

Prove a theorem of the form:

```text
gcd(L,L') = 1
->
every additive/group hom
  (Role -> ZMod L') ->+ (Role -> ZMod L)
is zero
```

for positive moduli in the actual repository types.

Then specialize to the owned consecutive moduli:

```text
L = n+2
L' = n+3
gcd(L,L') = 1
```

and conclude:

- every group hom is trivial;
- therefore there is no nontrivial/surjective group refinement hom;
- the existing `archiveRolePhaseProjection` remains a finite-set map, not a group map.

Also prove the necessary divisibility boundary for a surjective product-cyclic refinement,
either at the full Role-product level or through a precise cyclic/exponent lemma:

```text
surjective ((Z/L'Z)^4 -> (Z/LZ)^4) -> L | L'.
```

Do not state “no group homomorphism”: the zero hom exists.

### 2. AF-to-commutative algebra boundary

Do **not** use normalized traces as multiplicative maps.

Prove an algebraic matrix-unit theorem strong enough to imply:

```text
m >= 2
D nonzero commutative unital algebra
->
no unital algebra hom M_m(C) -> D.
```

A ring/algebra-hom theorem is sufficient; a C*-specific theorem is optional if it follows
cleanly from existing Mathlib APIs.

Then connect it to the Fibonacci stage shape.

Required exact stage classification:

- `k=0`: two scalar blocks; characters exist;
- `k=1`: `M_2(C) oplus C`; a scalar-summand character exists;
- `k>=2`: both path-count blocks have size at least two; hence no unital
  `A_k -> C(B_n)` hom in the formalized stage model.

If the repository does not yet have a literal finite-stage algebra type for `A_k`,
introduce the smallest theorem-local/type alias needed to express the two matrix blocks.
Do not build an AF-limit replacement.

Also retain the weaker all-stage fact:

```text
k >= 1 -> no injective unital map A_k -> commutative target
```

when convenient.

### 3. Reverse-direction truth firewall

Do not prove a false no-go for

```text
C(B_n) -> A_k.
```

Document or formalize only the safe boundary:

- commutative finite-dimensional algebras have noninjective matrix representations;
- the missing datum is a canonical Role/Bratteli/refinement-compatible spectral
  decomposition, not bare existence.

No placeholder canonical map.

### 4. Trivial-source Role equivariance control

Formalize an abstract action lemma:

```text
source action trivial
f equivariant
->
f(v) is fixed by every group element
```

for each source vector `v`.

Specialize only as far as the current Role permutation action makes natural.

Do not claim `Hom_{S4}` is empty.
Do not invent a Tower-C `S_4` action.

### 5. Finite-range arithmetic boundary

Using exact arithmetic, own the **bounded** checks from the memo.

For `0 <= k,n <= 11`, prove the required non-equalities between:

- Tower-C path count and `|B_n|=(n+2)^4`;
- `dimA k` and `|B_n|`;
- `dimA k` and `16|B_n|`.

Use `native_decide` only under the repository's accepted exact finite certificate pattern.

Also own the explicit adjacent divisibility failures for the five hostile period names:

- Fibonacci;
- Fibonacci + 1;
- Fibonacci + 2;
- `floor(phi^j)` for the explicitly rationalized initial controls;
- Lucas.

It is enough to exhibit one adjacent failure per proposed **full consecutive surjective
tower**.

Do not infer a global perfect-power/Fibonacci theorem.

## Suggested module layout

Either strengthen:

`D0/Geometry/A4DGoldenCarrierWeldBoundary.lean`

or add narrowly imported helpers such as:

- `A4DGoldenGroupRefinementBoundary.lean`;
- `A4DGoldenAFCommutativeTargetBoundary.lean`.

Keep the capstone in `A4DGoldenCarrierWeldBoundary`.

## Exact capstones

At minimum expose named theorems equivalent to:

- consecutive coprime Role-product homs are zero;
- nontrivial/surjective consecutive group refinement is impossible;
- surjective product-cyclic refinement requires modulus divisibility;
- matrix block `m>=2` has no unital map to a nonzero commutative target;
- exact AF early-stage character exceptions;
- `k>=2` AF stage has no unital map to `C(B_n)`;
- trivial-source equivariant image lies in invariants;
- bounded `k,n<=11` cardinality/GNS non-equalities;
- hostile named full consecutive towers fail necessary divisibility.

Add `#print axioms` for principal capstones or repository-equivalent checks.

## Registry

Register only bounded claims actually proved.

Do not promote the surviving correspondence/index rule to a claim of existence or no-go.

## GitHub-first flow

1. fresh branch from current `main`;
2. `python tools/task_lifecycle.py start WRK-A4D-GOLDEN-CARRIER-WELD-BOUNDARY`;
3. immediately open Draft PR before Lean edits;
4. narrow builds during iteration;
5. one final `python tools/lean_task_build.py final`;
6. no-sorry, repo/work validators, generated views, `git diff --check`;
7. self-retire in the same PR;
8. Ready / `Lifecycle: REVIEW`;
9. do not self-merge.

No `lake clean`, `sorry`, `sorryAx`, or new axioms.

## Truth firewall

Do not:

- say the zero group hom does not exist;
- use traces as algebra homomorphisms;
- erase the `k=0,1` scalar-summand exceptions;
- turn bounded enumeration into an all-stage theorem;
- claim reverse maps `C(B_n)->A_k` are impossible;
- define the missing correspondence;
- set `k=n` or `n+2=F_m`;
- touch `J`, `D_H`, `H(e)`, physical time, stress, or Einstein closure.

## Exit condition

The repaired PR #104 carrier/group/algebra/equivariance/arithmetic boundary is Lean-owned
with exact scope, while the Role-equivariant correspondence and index rule remain
explicit research work.
