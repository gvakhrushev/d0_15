# A4D Ward locus is a divisor: det A, Smith pole, flat Q-vanishing

**Lane:** Wall B / Palatini response / Ward class localization
**Execution:** Draft research PR on `research/a4d-ward-divisor-smith-pole`
**Status:** EXACT numbers below; no BOOK/claim promotion; Res on a valued solder is OPEN
**Baseline:** `e8dcebe844a77452878e605ee4c35bdc9b43c100` (main at branch cut)
**Machine-readable:** `02_REGISTRY/research/certificates/a4d_ward_divisor_smith_pole.json`

## 0. Terminal

```text
A4D-WARD-LOCUS-IS-DIVISOR-SMITH-POLE-LEQ-2-FLAT-Q-VANISHES
```

This is not Einstein-from-E_Q and not a discrete T_μν. It localizes where a
linear Ward class *can* live, and records that the first-order metric readout
Qᵀ A⁻¹ F on the flat background is identically zero.

## 1. Closed form of det A on the diagonal family

For Z = (z, z, z, z) the connection Hessian A(z) = d²S/dc² (24×24) satisfies

```text
det A(z) = (z² + 1)¹² / (16 z¹²)
```

Certified by exact symbolic `factor(together(A.det()))` and by the identity
check against the closed form. Zero of algebraic order 12 at z = ±i.
Geometric nullity at those points is 8 (rank A₀ = 16). The discrepancy
12 vs 8 is Jordan/Smith structure, not an arithmetic error.

Consequence: on the *diagonal* family the determinant vanishes only at
z = ±i. In particular z = −1 is regular on that family
((−1)² + 1 = 2). A scan that reports rank 16 at “half-wave z=−1” while
building Z_r = i exp(i φ_r) with φ = π is actually sitting at z = −i,
not at z = −1.

## 2. The zero locus is a stratified divisor, not two points

Exact ranks of A on selected characters (same plaquette complex):

| Z | rk A | nullity |
|---|---|---|
| (i,i,i,i) and (−i,−i,−i,−i) | 16 | 8 |
| opposite-phase pairs off i, e.g. (i e^{iφ}, i e^{-iφ}, i, i) | 20 | 4 |
| same-sign two-phase, e.g. (i e^{iπ/2}, i, i e^{iπ/2}, i) | 22 | 2 |
| one phase shifted; generic including z = 1 | 24 | 0 |

Working hypothesis consistent with the sample (not a theorem):
degeneration requires even counts of +i and −i with n_{+i} + n_{-i} ≥ 2,
and then nullity = 2 · max(n_{+i}, n_{-i}). Odd counts restore full rank.
This law is OPEN as a quantified statement over the whole 4-torus.

#227 / #232 occupy the deepest stratum Σ₁₆. A new sheet would occupy Σ₂₀.
The designated IR packet of #241 / #275 lives in Σ₂₄: A is invertible there.

## 3. Local Smith data at z = i + w

Let NK (resp. NL) be a basis of the right (resp. left) kernel of A₀,
both 8-dimensional, and A₁ = ∂A/∂w at w = 0. The 8×8 degeneration matrix

```text
M = NL A₁ NK
```

has exact rank 4. So four of the eight kernel directions open at order w
and four open only at higher order. Hence A⁻¹ has poles of order at most 2.

Column-norm log-slopes of A(i(1+δ))⁻¹ for δ ∈ {1/8, 1/16, 1/32, 1/64}:

```text
histogram:  { order 1 : 6 columns,  order 2 : 18 columns }
```

This is *not* the naive split “4 simple + 4 double” of the invariant factors
read as columns of A⁻¹ in the coordinate basis. Coordinate columns mix the
Smith blocks. The invariant statement that survives is: rank M = 4 and
max pole order of A⁻¹ is 2.

## 4. What is dead, what is open

- Germ channel: dead as a Ward class (`M_1 = 0`, `M_k ∈ im C` on orbits 5/7,
  owned #270 / #303). Not reopened here.
- F7 (resonant odd Euler of the same dressing): lies in im A already on the
  spike; first-order metric readout vanishes in every tested channel.
  Connection cohomology, not a metric class.
- Orth3 (orthogonal odd Euler): outside im A on Σ₁₆ (16 → 17). That is the
  #260 connection-only no-go. Whether it produces a *metric* residue is **not**
  a first-order fact.
- Flat first-order operator R = −Qᵀ A⁻¹, with Q = d²S/dc dq evaluated at
  vanishing background connection: R F = 0 for both Orth3 and F7.
  An earlier number Res ≈ 110.85 used a Q that still depended on the background
  connection a and is **withdrawn**. Linear metric readout on η does not see
  the class. That is the same structural fact as #275: the mixed jet that can
  carry a residue is t³ h (and t² h), not Qᵀ A⁻¹ on the identity solder.

## 5. Constitutive reading

One meromorphic family A(Z) on the character 4-torus. Its determinant divisor
D = {det A = 0} is stratified with nullities {0, 2, 4, 8}. The linear Ward
class, if it exists as a metric object, is a polar current of A⁻¹ along D
with pole order ≤ 2, read by a *second-order* mixed jet on a valued solder.

Designated Einstein is the regular value of the same family at Z = (1,1,1,1),
which is off D. A C^∞ packet supported near the IR point does not occupy D.
Occupying D is a condensate (#227 on Σ₁₆, or a not-yet-built sheet on Σ₂₀).

## 6. Remaining gates (exactly two)

1. Mixed metric jet on Q_h = η + h α + h² x₀ β (the #275 / #259 owner):
   does the second-order readout of Orth3 (or of the 4-plane ker M) survive
   after the connection range correction? This is S_{t³ h} / S_{t² h}, not
   the withdrawn first-order Res.
2. Quantified divisor law on the whole torus: prove or kill
   `nullity = 2 max(n_{+i}, n_{-i})` on even-even strata.

No F9. No T_μν stamp. No identification of Λ_{±64} with E_Q.

## 7. Boundaries

No Lean promotion. No change to #202 / #240 / #260 owners. Scripts that built
the ranks and M live with the session artifacts; the numbers above are the
ones this memo is willing to keep.
