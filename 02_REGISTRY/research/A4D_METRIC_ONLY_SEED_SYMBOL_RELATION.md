# A4D: metric-only plane versus the E-LIN response symbol pair

Task: `WRK-A4D-METRIC-ONLY-SEED-SYMBOL-RELATION`
Class: `WORKER`
Terminal: `J2-METRIC-ONLY-SEED-SYMBOL-RELATION-CERTIFIED`

## 1. Question

#264 established that on two of the nine owned L=4 singular orbit types the
forward-coframe/joint-kernel intersection equals the complete two-real-dimensional
#262 metric-only plane. E-LIN owns a two-dimensional Lorentz response-operator
family `span{E_eta, E_sp}`.

Both "twos" are numerically equal. That is not a typed statement. This task puts
the amplitude plane and the operator symbols in one real carrier and decides
whether the plane has an exact operator-theoretic characterization from the seed
pair.

## 2. Sources, all merged on main

| Input | Provenance | Role |
|---|---|---|
| `a4d_affine_coframe_joint_carrier_check.py` | merged #264 | metric Euler block `C`, real carrier ordering, the nine L=4 orbit ids |
| `A4D_METRIC_NULL_HESSIAN_COMPLEX.md` | merged #270 | `rank C = 9`, `ker C = span(dd^T)`, orbit split 0 and 4 |
| `a4d_elin_esp_executable_owner_check.py` | merged #267 | executable `esp_fourier_symbol`, `eeta_fourier_symbol`, `ESP` owner |

No new operator was defined. The brief forbids inventing an operator to fit the
#262 plane, and none was: `E_eta` and `E_sp` are the merged #267 owners, called
through their published API.

The prior blocker `E_SP-EXECUTABLE-SYMBOL-OWNER-MISSING` is resolved by #267.
The task could only resume after that merge, as its brief required.

## 3. The common carrier

The #264 carrier is 20-dimensional with ordering

```
[Re q, Im q]
```

over the ten `SYM` symmetric metric-amplitude components. The #267 response
symbol is a 10x10 complex object indexed by the same `SYM` order, so it is
realified once, directly, into the same ordering. No extra block, no gauge
direction, and no additional component is appended to either side.

Both objects therefore live in $\mathbb{R}^{20}$, and they live there *by
construction from their own owners*, not by choosing a convenient basis.

## 4. Exact nine-orbit relation table

`plane` is $\dim\ker C_{\mathrm{real}}$ at that character. `image` is
$\operatorname{rank}$ of the operator applied to the plane. `inv` is exact
invariance of the plane under the operator. `ann` is exact annihilation.
`inter` is $\dim\bigl(\operatorname{im}(\text{plane})\cap\text{plane}\bigr)$.

| orbit | character | operator | plane | image | inv | ann | inter |
|---|---|---|---|---|---|---|---|
| 0 | (0,0,1,1) | `E_sp` | 2 | 2 | 0 | 0 | 2 |
| 0 | (0,0,1,1) | `E_eta` | 2 | 2 | 0 | 0 | 2 |
| 1 | (0,0,1,3) | `E_sp` | 2 | 2 | 0 | 0 | 2 |
| 1 | (0,0,1,3) | `E_eta` | 2 | 2 | 0 | 0 | 2 |
| 2 | (0,1,1,2) | `E_sp` | 2 | 2 | 0 | 0 | 2 |
| 2 | (0,1,1,2) | `E_eta` | 2 | 2 | 0 | 0 | 2 |
| 3 | (1,0,1,2) | `E_sp` | 2 | 2 | 0 | 0 | 2 |
| 3 | (1,0,1,2) | `E_eta` | 2 | 2 | 0 | 0 | 2 |
| 4 | (1,1,1,1) | `E_sp` | 2 | 0 | 0 | **1** | 0 |
| 4 | (1,1,1,1) | `E_eta` | 2 | 0 | 0 | **1** | 0 |
| 5 | (1,1,3,3) | `E_sp` | 2 | 2 | 0 | 0 | 2 |
| 5 | (1,1,3,3) | `E_eta` | 2 | 2 | 0 | 0 | 2 |
| 6 | (2,0,1,1) | `E_sp` | 2 | 2 | 0 | 0 | 2 |
| 6 | (2,0,1,1) | `E_eta` | 2 | 2 | 0 | 0 | 2 |
| 7 | (2,1,1,2) | `E_sp` | 2 | 2 | 0 | 0 | 2 |
| 7 | (2,1,1,2) | `E_eta` | 2 | 2 | 0 | 0 | 2 |
| 8 | (2,1,2,3) | `E_sp` | 2 | 2 | 0 | 0 | 2 |
| 8 | (2,1,2,3) | `E_eta` | 2 | 2 | 0 | 0 | 2 |

`INVARIANT_PAIRS=0`, `ANNIHILATING_PAIRS=2`, total 18 (orbit, operator) pairs.

## 5. What the table does and does not establish

The plane is two-dimensional on **all nine** orbits, reproducing the #262
statement on orbits 0 and 4 exactly as merged.

The relation is **not uniform**. It is degenerate at exactly one character:

- at orbit 4 `(1,1,1,1)` the character is the trivial one, so `zeta = 1` on
  every role. The merged #267 `E_sp` owner is the **purely spatial** three
  dimensional response: its 21 nonzero coefficients carry no constant
  (diagonal role-pair) term that survives at `zeta = 1`. The `E_sp` symbol is
  therefore identically zero at that character even though it is non-zero
  elsewhere, and it annihilates the whole metric-only plane. The same holds for
  `E_eta` here. This is a **degenerate** relation: a vanishing symbol
  annihilates everything and says nothing about the plane's position in the
  carrier;
- on the other eight orbits both operators are non-degenerate on the plane
  (`image = 2`) but the image is **not** equal to the plane: the exact
  intersection has full dimension 2 while
  $\operatorname{rank}[\,\text{plane}\ \mid\ \operatorname{im}(\text{plane})\,]=4$.

Consequently the plane is **not** an invariant plane, **not** a common kernel,
and **not** an eigenspace for either operator, at any of the nine orbits. There
is no exact operator-theoretic characterization of the metric-only plane from
the seed pair `E_eta`, `E_sp`.

`inter = 2` with `rank[plane | image] = 4` is the decisive pair of numbers: the
image of the plane is a distinct complementary 2-plane meeting the original in
the full 2 dimensions.

## 6. Hostile controls

- **Dimension match is not equality.** The plane has dimension 2 on every orbit
  and the operator acts on a 20-dimensional carrier. The certificate asserts
  this distinction explicitly per orbit (`*_PLANE_IS_NOT_OPERATOR_SPAN`) rather
  than inferring anything from the shared "two".
- **A vanishing symbol cannot certify annihilation.** The orbit-4 annihilation is
  reported as a separate, degenerate case and is explicitly excluded from being
  read as a structural relation. The eight non-degenerate orbits are the ones
  that decide the question.
- **Symbol non-degeneracy is verified, not assumed.** At orbit 0 the `E_sp`
  symbol has rank 6 of 20 with 42 nonzero entries and `E_eta` has rank 12 with
  114 nonzero entries, so the non-zero images on the eight non-degenerate
  orbits are real statements rather than artifacts of a zero operator. On
  orbit 4 the same operators are evaluated at `zeta = 1`; the `E_sp` symbol
  vanishes there while `E_eta` has rank 12 yet still annihilates the plane,
  which is the substantive orbit-4 statement.
- **No fitting.** The plane comes from `ker C_real` of the merged #264 block and
  the symbols from the merged #267 owners. The certificate reads no #262 census
  artifact and normalizes from no J2 orbit.

## 7. Reproduction

```bash
python3 02_REGISTRY/research/certificates/a4d_metric_only_seed_symbol_relation_check.py
```

All arithmetic is exact over the complex symbolic ring; no floating tolerance is
used. The terminal line is `J2-METRIC-ONLY-SEED-SYMBOL-RELATION-CERTIFIED`.

## 8. Scientific status

This is an **exact finite classification** of the relation between one owned
amplitude plane and one owned operator pair on a specified finite carrier. It is
not a physical identification, not a gauge statement, and not a claim release.

The negative outcome is the substantive result: the apparent dimensional
coincidence between the #262 metric-only plane and `span{E_eta, E_sp}` carries
**no exact operator-theoretic structure** in this carrier. Any downstream use of
that "two equals two" as evidence must cite this certificate as its refutation.

## 9. Scope

No gauge map, no nonlinear germ search, no edits to #202/#240/#259/#260, no
Einstein promotion, no beta/phi/remnant interpretation, no claim or BOOK edits,
and no child tasks.
