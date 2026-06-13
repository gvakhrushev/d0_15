# NO-GO: Generation Spectral Rays Undefined

Lean module: `D0.Spectrum.GenerationSpectralRays`

The current D0 Lean core does not determine a fundamental theorem
`exactly_three_generation_clusters`.

## Exact Reasons

1. No canonical finite generation operator is selected by the current D0 core:
   `canonicalGenerationOperator = none`.

2. No exact rational/integer spectrum is available from such an operator:
   `K913Spectrum = none`.

3. The generation ray theorem is not derivable from the current objects:
   `¬ GenerationRayTheoremDerivableFromCurrentObjects`.

## Lean Theorem

```lean
theorem NO_GO_GENERATION_RAYS_UNDEFINED :
    GenerationSpectralRayNoGo
```

## Consequence

The three-generation statement is not a closed core theorem in the current D0
formalization. It must either receive a new canonical finite operator and
tolerance-free clustering definition, or move to a model/passport layer.
