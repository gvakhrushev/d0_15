# D0 interpretation spine

This file is not a release report. It is the working synthesis contract for the
D0 physical interpretation layer.

## Spine

```text
finite D0 core
  -> dimensionless observables
  -> InterpretationPackage
  -> one ExternalSICalibration
  -> SI readout
  -> empirical passports
```

## Contract

- The finite core owns the internal invariants, operators, combinatorics,
  spectral proxies, cosmology shape statements, and no-go boundaries.
- The `InterpretationPackage` owns coherence across RG, spectral action,
  cosmology, and gauge readouts. These are explicit package conditions, not
  hidden promotions of physical meaning into the core. **They are a contract to
  be discharged per sector, not a proven core property.** Each coherence
  condition is conditional on its own sector's bridge/passport owner; no
  book-level bridge is promoted to core by being bundled here; and aggregating
  the sectors into one package adds no claim the individual books did not
  already make. Cross-sector coherence is a working conjecture of the
  interpretation layer, not a theorem of the finite core.
- `ExternalSICalibration` is the single SI transition. It declares units and
  macroscopic constants for readout; it does not mutate core trace shapes.
- Empirical passports compare calibrated readouts to external data. They can
  falsify or constrain a readout package, but they do not add missing core
  theorems.

## Lean anchors

- `D0.Bridge.InterpretationSpine`
- `Bridge.interpretation_package_keeps_core_dimensionless`
- `Bridge.interpretation_package_does_not_mutate_core_shape`
- `Bridge.si_readout_uses_single_external_calibration`
- `Bridge.interpretation_spine_has_single_si_readout`
- `Bridge.empirical_comparison_is_after_si_readout`
- `Bridge.interpretation_package_rg_readout_coherent`
- `Bridge.interpretation_package_spectral_action_readout_coherent`
- `Bridge.interpretation_package_cosmology_shape_readout_coherent`
- `Bridge.interpretation_package_gauge_readout_coherent`
- `Bridge.interpretation_package_passports_external`
- `Bridge.interpretation_spine_coherence_contract`
- `Bridge.interpretation_package_from_existing_anchors_coherent`

## Typed readout package

### RGReadoutCoherence

Tracks finite scale algebra and RG residual/curvature obstruction as package
conditions. Lean constructor: `Bridge.rgReadoutFromAnchors`, using
`Bridge.phi_scale_step`, `D0.archiveRGPhaseProjection_surjective`, and the
conditional smooth interpolation bridge.

### SpectralActionReadoutCoherence

Tracks finite heat-trace/spectral-action proxy status and blocks continuum
promotion unless an explicit bridge theorem is added. Lean constructor:
`Bridge.spectralActionReadoutFromAnchors`, using the finite `a0/a2` proxy
theorems and an explicit no-continuum-promotion obligation.

### CosmologyShapeReadout

Tracks dimensionless cosmology-shape statements and keeps empirical parameters
outside the core generator. Lean constructor:
`Bridge.cosmologyShapeReadoutFromAnchors`, using the core-shape/passport
boundary theorem.

### GaugeReadoutCoherence

Tracks the finite gauge layer and nonabelian boundary/no-go conditions as part
of the package. Lean constructor: `Bridge.gaugeReadoutFromAnchors`, using
gauge-curvature origin and nonabelian boundary anchors.

### PassportExternality

Tracks declared external data and enforces that passports constrain calibrated
readouts without mutating the D0 core. Lean constructor:
`Bridge.passportExternalityFromAnchors`, using traceability status no-promotion
anchors.

## Anchor constructors

### rgReadoutFromAnchors

Builds `RGReadoutCoherence` from phi scale algebra, archive RG projection, and
the smooth interpolation bridge assumption.

### spectralActionReadoutFromAnchors

Builds `SpectralActionReadoutCoherence` from finite `a0/a2` proxy theorems and
an explicit no-continuum-promotion obligation.

### cosmologyShapeReadoutFromAnchors

Builds `CosmologyShapeReadout` from core-shape independence and empirical
passport non-promotion theorems.

### gaugeReadoutFromAnchors

Builds `GaugeReadoutCoherence` from gauge-curvature origin and nonabelian
boundary anchors.

### passportExternalityFromAnchors

Builds `PassportExternality` from traceability status no-promotion anchors.

### interpretationPackageFromAnchors

Assembles the full typed readout package from the five anchor constructors.

### interpretation_package_from_existing_anchors_coherent

Proves that the assembled package satisfies the full D0 interpretation spine
coherence contract.

## Development rule

New physical claims should strengthen one of three things:

- a core invariant or finite theorem;
- an `InterpretationPackage` coherence condition;
- the single calibrated readout and its empirical passport.

Claims that do not strengthen one of these layers should stay out of the active
theory map.
