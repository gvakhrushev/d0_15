# EXP-LORENTZ-CONTINUUM-TYPED-OWNER

## Class
EXPENSIVE

## Parent
CTRL-GRAVITY-DYNAMICS-CLOSURE

## Objective

Turn the current proposition-level smooth/Rieffel/Connes/Lorentz passport stack into an exact typed research contract suitable for downstream tensor/operator convergence.

The target is not to claim the continuum as CORE. Determine whether the existing explicit bridge assumptions are sufficient to construct, conditionally, an actual object ((M,g)) with (M) a smooth connected 4-manifold and (g) a smooth Lorentz metric of signature ((1,3)), together with comparison data from the D0 refinement tower.

Repository edits: **none**.

## Required reading

- `02_REGISTRY/research/EINSTEIN_ALLY_CHARACTERIZATION_BRIDGE.md`
- `02_REGISTRY/CLOSURE_CONTRACT.md`
- `03_FORMALIZATION/D0/Bridge/RieffelGHPBridge.lean`
- `03_FORMALIZATION/D0/Bridge/ConnesReconstructionBridge.lean`
- `03_FORMALIZATION/D0/Bridge/SmoothMetricBridge.lean`
- `03_FORMALIZATION/D0/Bridge/LorentzBridge.lean`
- `03_FORMALIZATION/D0/Bridge/Assumptions/HeatTraceWeyl.lean`
- all smooth-manifold/Lorentz claim and assumption rows.

## Required audit

1. List the exact types exported by each bridge module.
2. Separate proposition-only assumptions from constructed objects.
3. Determine whether a real smooth manifold object is already available anywhere.
4. Determine whether a real Lorentz metric object is available anywhere.
5. Determine whether dimension four and signature ((1,3)) are properties of that same typed object.
6. Determine what comparison maps or convergence morphisms from the finite tower exist.
7. State the minimum additional bridge assumptions needed to formulate convergence of finite edge/matrix responses to continuum tensor operators.

## Positive target

A theorem-ready conditional owner:

`D0-LORENTZ-CONTINUUM-TYPED-OWNER-001`

with output schematically
[
(M,g,\Phi_N,\text{comparison/convergence data}),
]
under explicitly named bridge assumptions only.

## Firewalls

Do not infer Lorentz covariance from finite permutation symmetry.
Do not infer smooth tensors from scalar heat-trace limits.
Do not hide missing comparison maps inside the word reconstruction.
Do not promote bridge assumptions to CORE.

## Terminal verdict

Return exactly one:

- `TYPED-LORENTZ-CONTINUUM-PASSPORT-REACHED`
- `PROP-BUNDLE-NOT-OBJECT-BRIDGE-OPEN`
- `CONTINUUM-COMPARISON-MAPS-MISSING`
- `LORENTZ-REIFICATION-REQUIRES-NEW-ASSUMPTION`

## Deliverable

`MEMO_21_LORENTZ_CONTINUUM_TYPED_OWNER.md`
