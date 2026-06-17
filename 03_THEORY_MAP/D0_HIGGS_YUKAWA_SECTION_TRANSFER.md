# D0 Higgs/Yukawa Section Transfer

## Definitions

Finite block carrier: ℋ_R ⊕ (ℋ_L ⊗ ℋ_ϕ) with dims e.g. 1 + 1×2 = 3 (minimal deterministic example).

Yukawa map Y : ℋ_R → ℋ_L ⊗ ℋ_ϕ (dimensionless coefficients).

Full block operator:

𝒴 = [[0 , Y†] , [Y , 0]]

Certified scalar projector compatibility: (I_L ⊗ P_ϕ) Y = Y  (where P_ϕ = I₂ from the rank-2 closure).

## Theorem Statement

The Yukawa section is a finite off-diagonal block operator Y compatible with the certified scalar projector P_ϕ, yielding Hermitian 𝒴 on the finite carrier. No second mass anchor is introduced; Λ_act remains the sole dimensional scale.

## Proof (constructive)

Define minimal dims, construct deterministic Y (e.g. [[1],[0.5]]), build 𝒴, verify Hermitian (𝒴†=𝒴), verify projector compatibility (P_ϕ Y = Y), assert no second anchor introduced (static flag).

See executable cert for numerical verification.

## Negative Controls

- FAIL_RANK1_SCALAR_YUKAWA_LEG
- FAIL_EXTRA_SCALAR_PROJECTOR_RANK_GT2
- FAIL_SECOND_MASS_ANCHOR_FOR_YUKAWA_SECTION
- FAIL_PDG_SELECTED_YUKAWA_BEFORE_OPERATOR_FREEZE

## Cert Tokens (from 05_CERTS/vp_higgs_yukawa_section_transfer.py)

PASS_YUKAWA_BLOCK_HERMITIAN

PASS_YUKAWA_PROJECTOR_COMPATIBLE

PASS_YUKAWA_SECTION_NO_SECOND_MASS_ANCHOR

PASS_SINGLE_ACTION_SECTION_PRESERVED

(and the four FAIL_ expected negative controls)

## Book Patch Text

The Yukawa section is a finite off-diagonal block operator Y:ℋ_R→ℋ_L⊗ℋ_ϕ compatible with the certified scalar projector:

P_ϕ Y = Y .

Equivalently the full block operator 𝒴 = [[0,Y†],[Y,0]] is Hermitian on the finite left-right-scalar carrier. Yukawa coefficients are dimensionless; the only dimensional scale remains Λ_act. No second mass anchor is introduced.

In Book 05 add YUKAWA-SECTION-CERT-CLOSED (finite Yukawa block map compatible with certified scalar projector and introduces no second mass anchor).
