# Scene / Riesz / M1 operator weld

## Verdicts

- Part A: `RIESZ-RESIDUAL-IS-SCENE-OPPOSITE-CUT`
- Part B: `M1-RIESZ-REPRESENTATION-PREMISE-REQUIRED`
- Part R: `ROLE-FOCK-ACTION-OWNED-ENVELOPE-PENDING`

Parts C and D were not executed.

## A. Opposite cut

The unsigned incidence operator and the opposite-cut embeddings are defined for an arbitrary complete tripartite scene. On a zone, the cut uses only the cardinalities of the other two zones. After a block-scalar metric, incidence of that cut is the product of those cardinalities times the weight difference, times the zone lift.

On `K(9,11,13)` the existing standard embeddings `A9`, `A11`, and `A13` are those cuts, and `BPlus` and `R` are the unsigned incidence and the block-scalar metric. The owned numbers are the products

- `11 * 13 = 143` on the size-9 sector,
- `9 * 13 = 117` on the size-11 sector,
- `9 * 11 = 99` on the size-13 sector.

The same theorem on `K(2,6,6)`, `K(3,3,8)`, and `K(2,3,4)` returns `36`, `12`, `24`, `9`, `12`, `8`, and `6`. The scene constants do not persist.

`dim Balanced(n) = n - 1` was already the generic kernel rank of the zone-sum map. The mismatch images of the three standard sectors are supported on different zones. Their joint rank on that span is `8`, `10`, or `12` according to which block weights differ. Because `(a-b)+(b-c)=a-c`, a single sector cannot be the only active one, so the only values are `0`, `18`, `20`, `22`, and `30`.

This rank is the rank on the standard-sector span. It does not replace a proof that the rank of the mismatch on all of `KPlus` equals that count.

## B. M1 and the uniform weight

`positive_weight_mismatch_zero_iff` remains the algebraic zero locus: for positive block weights, the bare mismatch vanishes on `KPlus` if and only if the three weights are equal.

`VerificationContract` requires two lines to return the same record comparison. It has no edge carrier and no block weights. The Boolean two-line contract is a verification contract and still coexists with weights `1,2,3`, whose mismatch does not vanish. Equality of only two blocks is a different locus from uniformity.

The missing premise is a representation that sends the two registered lines to two scene readouts, preserves line exchange, and proves that readout equality is uniform positive weight. Defining the readouts as the two sides of the mismatch would not supply that premise.

Separately, a radius-one average `α I + β U_r^{-1}` equals the owned backward average for every function if and only if `α = β = 1/2`. The pure forward coefficient `α = 1`, `β = 0` fails. Constant functions do not separate the coefficients. This classification uses the owned centered-difference identity. It is not a theorem of `VerificationContract`.

## R. Role action on Fock space

`ArchiveFockState` is `Role → Bool`. A role permutation acts by `(σ · s)(r) = s(σ⁻¹ r)`. The action sends the identity permutation to the identity, multiplies correctly, is bijective, and preserves Fock degree.

Jordan-Wigner operators use one fixed role order, so the plain occupation transport is not the conjugation operator. The signed transport multiplies by the parity of occupied order inversions. For each of the three adjacent transpositions of that order, conjugation sends `c_r` to `c_{σ r}`, sends `c_r†` to `c_{σ r}†`, and sends `c_s† c_r` to `c_{σ s}† c_{σ r}`. Number bilinears and the signed transport preserve Fock degree.

The sign cocycle that would assemble those adjacent conjugations into a general permutation, and the identification of the degree-preserving endomorphism algebra with a 70-dimensional envelope, are not proved here.

## C and D

The corrected Hodge/Dirac owner from the dispersion repair is not on this baseline as a replacement for the hopping CAR operator. The hopping operator and `A4DLinearizedMetricResponse` are not placed on one `LocalSymRoleField` carrier here, and no log-det identification is claimed. No gauge group is derived.

## Owners

- `D0.Geometry.OppositeCutPairing`
- `D0.Gravity.SceneOppositeCutIdentification`
- `D0.Foundation.M1RieszRepresentationGap`
- `D0.Geometry.RoleFockPermutation`
