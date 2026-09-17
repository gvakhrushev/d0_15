# NO-GO: Pi0 Branch-Defect Generation

Lean modules: `D0.Spectrum.Pi0BranchDefectGeneration`, `D0.Spectrum.Pi0BranchDefectControls`

The current D0 Lean core does not determine a fundamental defect generation theorem.

## Exact Reasons

1. No canonical action is defined on the defect vector: `¬ ExistsCanonicalPi0DefectAction`.
2. The phase defect relies on comparison with the transcendental constant `Real.pi`, which is not part of the exact finite core algebra.
3. Extra physical inputs are required to resolve a finite 3-generation orbit structure.
