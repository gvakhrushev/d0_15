# MEMO_A4D_GOLDEN_ROLE_PHASE_CARRIER_OPERATOR_WELD

**Baseline:** `main = fa4af53bed53a693efbd1db832ae092c51eb5536`.
**Branch start:** `4ffc910` (lifecycle `IN_PROGRESS`).
**Brief:** `00_WORK/tasks/EXP-A4D-GOLDEN-ROLE-PHASE-CARRIER-OPERATOR-WELD.md`.
**Consumed:** PR #86 `MEMO_A4D_GOLDEN_ROLE_PHASE_REFINEMENT_WELD.md`, `ROADMAP_A4D_RELATIONAL_REFINEMENT_SYNTHESIS.md`, PR #99 `A4DGoldenRolePhaseRGDefect` and `A4DGoldenCarrierWeldBoundary`.
**Review repair:** incorporated before Ready; terminal and positive leftover preserved with corrected no-go scope.
**No Lean source. No physical time. No `J` / `D_H` / `H(e)` inter-level naturality.**

## 0. Terminal verdict

**GOLDEN-ROLE-PHASE-WELD-NEW-PRIMITIVE-REQUIRED**

The first comparison class not excluded by the repaired boundary is a finite-dimensional
`A_k`–`C(B_n)` Hilbert correspondence / bimodule together with two further pieces of
structure that are not currently owned:

1. an index rule relating Bratteli depth `k` to Role-phase period `n`;
2. enough Role action data to state an actual equivariance law on both sides.

A trivial `S_4` action on the Tower-C side is a useful control, but by itself it only says
that the Tower-C data are Role-blind. It is not the desired weld.

The index rule may not be inserted as `k = n`, and the Role-phase modulus may not be set
by hand to `L = F_m`. Either relation must come from a commuting/refinement law or another
owned structural invariant.

Repaired scoped boundary:

1. **finite point carriers:** exact enumeration finds no cardinality equality between the
   tested Tower-C path/AF carriers and `B_n` in the stated finite range; no global
   perfect-power/Fibonacci theorem is claimed;
2. **group refinement:** a surjective hom
   `(Z/L'Z)^4 -> (Z/LZ)^4` requires `L | L'`; if `gcd(L,L')=1`, every hom is zero.
   Hence the owned consecutive `L+1 -> L` Role-phase step admits no nontrivial group
   refinement hom, although the zero hom always exists;
3. **AF -> commutative algebra:** for `k >= 1`, no injective unital algebra/*-algebra map
   `A_k -> C(B_n)` can exist because `A_k` is noncommutative. More sharply, for
   `k >= 2` both matrix blocks have size at least two, so there is no unital
   `*-hom A_k -> C(B_n)` at all. The early stages `k=0,1` must be treated separately:
   scalar summands give characters;
4. **commutative algebra -> AF:** unital maps `C(B_n) -> A_k` are not excluded. They are
   finite spectral decompositions / projection-valued labelings inside the two matrix
   blocks. What is missing is a canonical Role/Bratteli/refinement-compatible choice;
5. **Role equivariance:** Tower C currently has no owned `S_4` action, so
   `Hom_{S_4}` across the towers is not yet a repository-typed object. If a trivial
   action is artificially supplied on the Tower-C source, equivariant maps can exist,
   but their images lie in the `S_4`-invariant sector on the Role side;
6. **GNS dimension matching:** exact finite checks show no equality with
   `ell^2(B_n)` or `ell^2(B_n x Fock)` on the tested stages. No all-stage arithmetic
   no-go is inferred from growth alone.

The PR #99 scalar

```text
goldenScaleProbe k = phi
```

is independent of `k` and transports no Tower-C state. It remains a scalar diagnostic,
not a carrier weld.

## 1. Exact tower types

### Tower B — Role-phase / CAR

- `ArchiveRolePhasePoint n = Role -> Fin(n+2)`
- `ArchiveRolePhaseGroup n = Role -> Z/(n+2)Z`
- `archiveRolePhaseProjection n` is coordinatewise `archiveRGPhaseProjection n`
- `archiveRGPhaseProjection n x = <x.val % archiveFibers n, ...>`

With `L = n+2`:

| n | L | `|B_n| = L^4` | cochain `16 L^4` |
|---|---:|---:|---:|
| 0 | 2 | 16 | 256 |
| 1 | 3 | 81 | 1296 |
| 2 | 4 | 256 | 4096 |
| 3 | 5 | 625 | 10000 |
| 4 | 6 | 1296 | 20736 |
| 5 | 7 | 2401 | 38416 |
| 6 | 8 | 4096 | 65536 |

For positive moduli `L,L'`, a surjective hom
`(Z/L'Z)^4 -> (Z/LZ)^4` forces `L | L'`: the source exponent `L'`
annihilates every image, while the target contains elements of exact order `L`.

If `gcd(L,L') = 1`, every hom is zero. Therefore for the owned consecutive step
`L' = L+1`, every group hom is trivial. The repository projection
`archiveRolePhaseProjection n` is nevertheless a valid finite-set map; the statement
is that it is not a nontrivial group-refinement hom.

Role `S_4` acts on Tower B by permuting coordinates. PR #99 owns commutation with the
coordinatewise projection at the finite-set level.

### Tower C — golden cylinder / Bratteli / AF

The owned AF owner gives:

- incidence `M_phi = [[1,1],[1,0]]`;
- path counts `p(0)=(1,1)`, `p(k+1)=(a+b,a)`;
- stage shape `A_k = M_a(C) oplus M_b(C)`;
- algebra dimension `dim A_k = a^2+b^2`;
- Perron trace/scaling ratio `phi`;
- trace-preserving GNS refinement isometry internal to the AF tower.

Initial controls:

| k | `(a,b)` | paths `a+b` | `dim A_k` |
|---|---:|---:|---:|
| 0 | (1,1) | 2 | 2 |
| 1 | (2,1) | 3 | 5 |
| 2 | (3,2) | 5 | 13 |
| 3 | (5,3) | 8 | 34 |
| 4 | (8,5) | 13 | 89 |
| 5 | (13,8) | 21 | 233 |
| 6 | (21,13) | 34 | 610 |

Index `k` is Bratteli depth. It is not Role-phase period `n`, record depth, a history
tick, or physical time.

### Tower A — record / profinite

Tower A is not used as a substitute. The first-step `6 != 16` record/Role-phase
separation remains owned by `A4DGoldenCarrierWeldBoundary`.

## 2. Comparison classes

### 2.1 Point carrier — finite-range no-go only

Tower-B cardinalities are fourth powers `(n+2)^4`.
Tower-C finite path counts begin

```text
2, 3, 5, 8, 13, 21, 34, 55, 89, ...
```

and AF algebra dimensions begin

```text
2, 5, 13, 34, 89, 233, 610, ...
```

Exact enumeration for `0 <= k,n <= 11` finds no equality between either tested Tower-C
sequence and `|B_n|`, and no equality between `dim A_k` and the cochain dimension
`16|B_n|`.

This is deliberately a finite-range theorem target. It is not promoted to a global
statement that Fibonacci numbers or AF dimensions can never be fourth powers.

Cardinality excludes bijections only. It does not exclude injections, surjections,
relations, stochastic kernels, representations, or Hilbert correspondences.

### 2.2 Role-equivariant function maps — typing boundary

Tower C currently owns the golden shift/Bratteli structure, but no Role-permutation
`S_4` action. Therefore a repository-level object such as

```text
Hom_{S_4}(Fun(C_k), Fun(B_n))
```

is not typed until an action on the Tower-C source is supplied.

As a negative control, artificially give the source the trivial `S_4` action. Then
nonzero equivariant maps can exist, but for every source vector `v` their images satisfy

```text
sigma . f(v) = f(v)
```

for every Role permutation `sigma`. Thus the image lies in the invariant subspace.
This does not encode how Tower-C data transform as Role geometry.

### 2.3 Algebra maps `A_k -> C(B_n)` — exact stage boundary

For `k >= 1`, `A_k` has a noncommutative matrix block, while `C(B_n)` is
commutative. Hence no injective unital hom can exist.

The sharper character statement is stage-sensitive.

For a nonzero commutative unital algebra `D` and `m >= 2`, there is no nonzero
unital hom

```text
M_m(C) -> D.
```

A matrix-unit proof is enough: commutativity forces the images of distinct diagonal
matrix units to coincide, while their product is zero; unitality then contradicts the
sum of the diagonal units.

Consequences for `A_k = M_a(C) oplus M_b(C)`:

- `k=0`: `A_0 = C oplus C`; characters/unital maps to a commutative target exist;
- `k=1`: `A_1 = M_2(C) oplus C`; projection to the scalar summand gives a character,
  so unital maps still exist;
- `k>=2`: `a,b >= 2`; neither block has a character, so no unital
  `*-hom A_k -> C(B_n)` exists.

Normalized matrix traces are **not** multiplicative and are not used as algebra
homomorphisms.

### 2.4 Algebra maps `C(B_n) -> A_k` — noncanonical positive class

This direction is not ruled out by commutativity or cardinality.

A unital `*-representation`

```text
C(B_n) -> M_a(C)
```

is equivalent to a family of pairwise orthogonal projections indexed by `B_n`
whose sum is the identity; zero projections are allowed. For
`A_k = M_a(C) oplus M_b(C)`, one chooses such a spectral decomposition in each block.

Therefore many noninjective maps exist. The current repository does not supply a
canonical choice that is simultaneously:

- Role-covariant;
- Bratteli-compatible;
- compatible with the Role-phase bonding;
- derived without arbitrary labeling of matrix subspaces by Role-phase points.

This direction remains a possible ingredient of a correspondence; it is not a solved weld.

### 2.5 GNS identification — finite-range no-go only

At finite AF stages the trace GNS vector space has dimension `dim A_k`. Exact
enumeration for `0 <= k,n <= 11` shows no equality with either

```text
dim ell^2(B_n) = |B_n|
dim ell^2(B_n x Fock) = 16 |B_n|.
```

This rules out dimension-preserving identifications on that tested rectangle only.
It does not prove an all-stage perfect-power theorem and does not disturb the genuine
internal AF GNS refinement isometries already owned by `FibonacciAFTower`.

### 2.6 Reindexed group tower — scoped no-go

A full **surjective group-refinement tower** along a proposed modulus sequence
`L_0,L_1,...` would require `L_j | L_{j+1}` at every adjacent step.

The common hostile names already fail this necessary condition at an explicit early
adjacent pair:

| name | first terms | explicit failing adjacent pair |
|---|---|---|
| `F_j` | 1, 1, 2, 3, 5, 8, ... | `2 not| 3` |
| `F_j+1` | 2, 2, 3, 4, 6, 9, ... | `2 not| 3` |
| `F_j+2` | 3, 3, 4, 5, 7, ... | `3 not| 4` |
| `floor(phi^j)` | 1, 2, 4, 6, 11, ... | `4 not| 6` |
| Lucas | 1, 3, 4, 7, 11, ... | `3 not| 4` |

One failing adjacent step is enough to rule out the **full consecutive surjective tower**
for that named sequence. It does not say that every pair fails, nor that no useful
subsequence can ever have divisibility.

Subsequences such as Fibonacci divisibility subsequences are mathematically available,
but no current Tower-C theorem canonizes one as the Role-phase period law.

### 2.7 One-dimensional Zeckendorf candidate — positive control, not a weld

No-`11` words admit the standard Fibonacci coding by an initial integer interval.
Prefix restriction and reduction modulo a Fibonacci-sized interval can exhibit the same
fiber-size multiset in small exact controls; for example the `13 -> 8` control has
five fibers of size two and three of size one.

This does not identify:

- the owned `archiveRGPhaseProjection : Fin(n+3) -> Fin(n+2)` with Fibonacci restriction;
- cyclic translation `+1 mod L` with the golden shift;
- the four-fold Role product `B_n` with four word spaces;
- an `S_4` action on Tower-C words.

Promoting the observation by declaring `n+2 = F_m` would insert the missing index rule
rather than derive it.

### 2.8 Correspondence / bimodule — surviving class

A finite-dimensional Hilbert `A_k`–`C(B_n)` correspondence is not excluded by the
preceding no-gos.

Fiberwise over the finite spectrum `B_n`, such a correspondence is a family of finite
Hilbert spaces carrying representations of

```text
A_k = M_a(C) oplus M_b(C).
```

Each fiber representation is classified by a pair of nonnegative multiplicities of the
two simple AF blocks. This makes the surviving problem concrete rather than placeholder
structural data.

A genuine weld still needs:

1. an owned relation between `k` and `n`;
2. an owned or derived `S_4` action on the Tower-C/left side, or an explicit theorem
   explaining why a weaker one-sided equivariance is the intended structure;
3. a refinement law comparing Bratteli inclusion with pullback/pushforward along the
   Role-phase projection;
4. only after (1)–(3), evaluation against the PR #99 operator and energy residuals.

A trivial `S_4` action on `A_k` can be used as a control. It forces the multiplicity
data to be constant on Role orbits on the `B_n` side, but it does not by itself identify
Tower-C structure with Role geometry.

No such refinement-compatible correspondence family or index rule is currently owned.

## 3. PR #99 residual after the comparison audit

```text
goldenScaleProbe k = phi
goldenRGResidual n k P = 0
  iff RenormalizedProjectiveCompatibility n P phi
```

The energy residual is a separate Dirichlet statement.

These theorems accept a supplied finite-set comparison `P` of one-dimensional phase
indices and a scalar probe. They do not receive a Tower-C word, AF element, trace-GNS
vector, or correspondence.

Therefore the residual remains a conditional diagnostic. Setting `c = phi` does not
construct a carrier, algebra map, or correspondence.

The nearest-neighbor exact-projective failure at scale `1` remains a negative control.
It is not a theorem that the golden residual is always nonzero.

## 4. Index and Role-equivariance audit

| datum | status |
|---|---|
| `k` vs `n` | distinct; no owned relation |
| record depth | Tower A; not used |
| history tick / `U_A` / physical time | firewalled |
| Role set-equivariance of `p_n` | owned |
| Role action on Tower C | absent |
| trivial Tower-C Role action | admissible control only; images land in B-side invariants |
| nontrivial group refinement for owned consecutive `p_n` | excluded by coprime exponents |
| Fock 16-fiber identity lift | construction choice, not a Tower-C consequence |
| AF -> commutative unital map at `k>=2` | excluded |
| commutative -> AF representation | exists noncanonically |

## 5. Firewalls respected

Not inferred:

- `k = n`;
- `n+2 = F_m`;
- physical time from golden depth;
- carrier weld from `c = phi`;
- Tower A = Tower B;
- a Tower-C `S_4` action from absence of one;
- located-`J`, `D_H`, or `H(e)` inter-level naturality;
- stress or Einstein dynamics.

## 6. Exact controls

The durable finite controls are:

- `|B_n|=(n+2)^4` and `16(n+2)^4`;
- path-count and `dim A_k` recurrence from `FibonacciAFTower`;
- exact cardinality/dimension comparison on `0 <= k,n <= 11`;
- early AF algebra stages `C oplus C`, `M_2(C) oplus C`, then two nonscalar blocks;
- coprime consecutive Role-phase moduli `L,L+1`;
- explicit failing adjacent divisibility pairs for the five hostile period names;
- forbid-`11` / Zeckendorf small controls;
- PR #99 `goldenScaleProbe_eq_phi`;
- Tower-A/Tower-B first-step fibers `6 != 16`.

These controls can be invalidated only by a later owner that supplies additional structure:
for example a nontrivial Tower-C Role action, a canonically selected divisibility
subsequence/index rule, or a named refinement-compatible correspondence.

## 7. Theorem-ready handoff

The next Lean worker should strengthen `A4DGoldenCarrierWeldBoundary` without defining
the missing correspondence.

Target theorem families:

1. **group boundary**
   - coprime finite-exponent homs are zero;
   - the owned consecutive Role-phase moduli therefore admit no nontrivial group hom;
   - surjective product-cyclic refinement implies the required divisibility condition;
2. **AF/commutative target boundary**
   - no unital hom from `M_m(C)`, `m>=2`, to a nonzero commutative target;
   - exact early-stage exceptions at `k=0,1`;
   - no unital `A_k -> C(B_n)` for `k>=2`;
3. **Role trivial-action control**
   - equivariant maps from a trivial source representation land in the invariant sector;
4. **finite-range arithmetic**
   - exact `0 <= k,n <= 11` non-equalities for path/AF dimensions versus
     `|B_n|` and `16|B_n|`;
   - explicit hostile adjacent-divisibility failures.

Do not formalize a global Fibonacci perfect-power theorem unless an actual proof is added.
Do not add a placeholder `Correspondence` structure and declare the weld solved.

## 8. Exactly one next step

Formalize the repaired boundary above next to `A4DGoldenCarrierWeldBoundary`.

The surviving correspondence/index-rule problem remains research-owned and may be opened
as a separate follow-on EXP only with the repaired boundary frozen as its truth firewall.
