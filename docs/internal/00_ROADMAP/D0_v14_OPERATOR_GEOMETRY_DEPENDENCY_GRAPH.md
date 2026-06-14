# D0 v14 Operator-Geometry Dependency Graph

This graph records the active dependency order after the Torus/Core-13 and Golden Pass30 PDG integration.

```text
BornQuadraticOrigin
  -> finite detector response discipline

TorusCore13GeometryOrigin
  -> three shell carrier
  -> radial hopping / phase drift noncommutator

TorusCore13GeometryOrigin
  -> GenerationSelectorOrigin
  -> GenerationOverlapResponseOrigin
  -> CKMNontrivialFlavourAlgebra
  -> MesonDefectTransferOrigin

TorusShell / Fin 3
  -> BaryonS3Symmetrizer
  -> symmetric triple shell carrier
  -> decuplet transfer admissibility

HiggsScalarProjectorConstructive
  -> SMScalarActionCompletion
  -> Yukawa/scalar promotion boundary

TickGaugeLorentz
  -> FiniteSpin2WaveOperator
  -> SpectralActionA2/EH bridge

Frozen D0 operator/geometry owners
  -> PDGStrictPassportV14
  -> Core13ShellGeometryPassport
```

## Active passport rule

```text
operator first
passport second
no PDG tuning
no geometry diagnostic as core source
```

## Preserved legacy source

The legacy `99_PRESERVED_SOURCE/D0_MAIN_GOLDEN_PASS30/` tree was removed in the Iteration-1
cleanup (it duplicated `add/d0-main/`, itself later removed); git history retains both for
audit/reproducibility. It was never an active theorem layer.
