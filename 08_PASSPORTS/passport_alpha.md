# Passport — fine-structure constant α (closure-holonomy)

**Claim ids:** `D0-ALPHA-HOLONOMY-002` (9-digit match, CHK), `D0-SEAM-HOLONOMY-001` /
`D0-PI0-DISCRETE-ANGLE-001` / `D0-Q8-SIN-CHANNEL-001` (structure, THE), `D0-ALPHA-MEASUREMENT-LIMIT-001`
(measurement-limit bet, HYP). **Cert:** `05_CERTS/vp_seam_holonomy_alpha.py` (+ `vp_pi0_discrete_angle.py`,
`vp_q8_sin_channel.py`, `vp_alpha_measurement_limit.py`).

## The three layers (honest status split)

| Layer | Value | Status | Owner |
|---|---|---|---|
| 1. Structural top | `α_top⁻¹ = 359φ⁻² − φ⁻⁵ = 726 − 364φ = 137.0356281` | **THE** | `D0-XI5-TORUS-DEFECT-001`, exact ℚ(φ) |
| 2. Closure holonomy | `α⁻¹ = α_top⁻¹ + φ⁻¹⁷(1 + lnφ·sin(12/5)) = 137.035999151` | structure **THE** / 9-digit match **CHK** | this passport |
| 3. Measurement limit | last `~10⁻⁸` band | **HYP** (falsifiable bet) | `D0-ALPHA-MEASUREMENT-LIMIT-001` |

The structure of layer 2 is derived/forced (angle `12/5 = 2π₀(2−φ)` exact, `sin`-channel from `Q₈ G²=−I`,
depth `φ⁻¹⁷ = seam×EW`, `h_KS = lnφ`); only the 9-digit agreement with data is the CHK content.

## Versioned external data

| Source | α⁻¹ | date |
|---|---|---|
| CODATA-2018 | 137.035999084 (21) | 2018 recommended |
| CODATA-2022 | 137.035999177 (21) | 2022 recommended |

Structural value `137.035999151` is **straddled**: `137.035999084 < 137.035999151 < 137.035999177`.
Gap to CODATA-2018 = `6.7×10⁻⁸`, smaller than the 2018→2022 inter-edition shift `9.3×10⁻⁸`.

## Pre-registered falsifiable bet

> As α⁻¹ is measured more precisely, the recommended value converges toward **137.035999151 from below**.
> **Falsified if** a future high-precision α⁻¹ settles away from the structural value by more than the
> closure holonomy can absorb (outside the measurement band).

## Discriminating tests (in the cert, must FAIL)
`cos` instead of `sin` → explains only 48.7% of the correction (~51% miss); `exp` instead of linear →
248× worse; wrong depth `φ⁻¹⁶`/`φ⁻¹⁸` → gross miss. `π` instead of `π₀` is a **symbolic** exactness
discriminator (`2π(2−φ)=2.39996 ≠ 12/5`), not a gross-α one — not faked as such.

## Honest bounds
- The 9-digit CODATA match is **empirical (CHK)**, never registered as a THE derivation of the α value.
- The residue route to Δα (Dixmier/`D0-CVFT-F1`) is **BLOCKED** (transcendental `∝1/lnφ` vs `α_alg ∈ ℚ(φ)`);
  the closure holonomy is the working route.
- 2nd-order holonomy was checked and does **not** close the residual (it worsens it).
- The cone-angle `2π₀` micro-derivation is now **machine-checked**: `π₀=(6/5)φ²` is *forced* by the δ₀-closure
  balance (`D0.Geometry.pi0_forced_by_closure_balance`; cert `vp_pi0_discrete_angle.py`). Only the deeper origin
  of the closure ratio leans on corpus THE (`§04.6.π.4`) — a narrower named proof-target.
