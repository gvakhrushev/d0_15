# Actual addressed J₂ root and fixed-P N1 preparation application

Supporting packet for [the parent synthesis](../../A4D_ORIGINAL_J2_FULL42_AND_N1_PREPARATION_JOINT_ROOT_2026_10_22.md), existing Draft PR #334. Scientific inputs: `af6e7eb8952564d86ddbfe910eb5f41d4a1b4e4b`. `GR_closed=false`.

The packet proves two distinct results:

1. A new exact nonflat stationary root of all 42 field equations for the literal original addressed two-tick J₂, with an outward interval Banach certificate and rigorous full saddle inertia.
2. An exact 50-variable lift of the original unpadded N1 root on the declared independent fixed-P product-input domain, with eight preparation equations, an invertible preparation Hessian and explicit normal constraint reactions.

The preparation extension of the literal determinant, complete physical heat/return/Info/work source, actual upstream/writer admission and uniform physical GR limit remain at their explicit scopes. The two roots are not identified.

| Subdirectory | Proof and evidence |
|---|---|
| [source](source/SOURCE_COMPARISON.md) | Exact two-factor feedback identity, all 42 initial source components, complete remaining-source equations |
| [certificate](certificate/ENDPOINT_PROOF.md) | New rational center, preconditioner, all outward Hessian endpoints, interval existence and inertia |
| [preparation](preparation/PROOF.md) | Original N1 joint-input theorem, all eight preparation Hessian rows and normal reactions |

[REVIEW.md](REVIEW.md) records the independent mathematical, literal-operator and scope checks. [MANIFEST.json](MANIFEST.json) freezes the new packet and parent synthesis; unchanged original dependencies are consumed from their existing repository paths and are not duplicated here.

## Read-only reproduction

Python 3 with mpmath 1.3.0 is sufficient. From the repository root:

```bash
python3 02_REGISTRY/research/sources/d0_j2_joint_preparation_application_2026-10-22/source/compare_sources.py --repo .
python3 02_REGISTRY/research/sources/d0_j2_joint_preparation_application_2026-10-22/certificate/check_feedback_interval42.py --audit
python3 02_REGISTRY/research/sources/d0_j2_joint_preparation_application_2026-10-22/certificate/check_feedback_inertia.py --audit
python3 02_REGISTRY/research/sources/d0_j2_joint_preparation_application_2026-10-22/preparation/check_joint_input_lift.py --repo .
```

The source and preparation consumers recompute their new quantities and compare the frozen receipts. The certificate audits verify the saved interval matrix, rational data, strict Banach and inertia bounds, and geometry; they explicitly do not claim a fresh reconstruction of all second derivatives. The original expensive J₂ endpoint calculation was performed successfully. Its proof describes the explicit fresh full-recompute command with separate output paths. The prior unpadded field-root proof is consumed, not replayed.
