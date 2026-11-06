# Growing-clock frame: bounded Lean receipt

Source implementation: commit `93efff4896df8c399f24ea6e5492e56d01480dea`,
`03_FORMALIZATION/D0/Algebra/GrowingClockFrame.lean`, SHA-256
`057de430a54f95a98bed1baf393caca5b2339bd010df2b8177bc645dce89ade2`.
The intended owner is #334 commit `afd99daf54d26ef7e1b47a94f380557213e9c6d5`,
`02_REGISTRY/research/sources/d0_retained_response_concentration_2026-10-28/GROWING_CLOCK_RU.md`
§§1–3, Git blob `370e8fb572e85fedeebe2e72531c01d5b68b0a91`.
The determinant consumer `D0.Algebra.IsometricClockDeterminant.det_clock_defect`
is an existing theorem; no new Gram-complement theorem is claimed.

For finite complex matrix carriers, orthogonal isometric frames `J_i`, an
isometry `T†T=1` and every internal stage advance `T J_i = J_(i+1)` imply
that the sum of frame projections is a self-adjoint projector and that
`L=(1-P)TP` obeys `L†L=J_f(1-C†C)J_f†`, with
`C=J_0† T J_f`. The existing rectangular determinant theorem then gives the
recorded equality for all complex `z`. Neither the final leakage factorization
nor the determinant equality is assumed. The compiled finite control takes
`J_0=e_0`, `J_1=e_1`, `T=I`; orthogonal frames and isometry hold, stage
advance fails and so does the asserted factorization.

The concrete owner's stage spaces and operators have not been constructed or
identified with these parameters. The 425D lift, field variation and full
physical source, admission, Cost−Info selection and GR recovery remain open.
This is a conditional algebraic bridge, not physical closure.

## Verification

`python3 tools/lean_task_build.py narrow D0.Algebra.GrowingClockFrame` returned
0 in an isolated sparse worktree and isolated reused `.lake` cache; the full
output and environment/dependency receipt are in [narrow.log](narrow.log).
This is a targeted cached build, not a full clean build or a build of `D0.All`
(the latter only gained the import). Initial preflight found a missing tracked
symlink target in the sparse checkout; that exact tracked target was restored
before the recorded successful run. The output contains two unused-section
linter warnings. Build receipt source/dependency/environment SHA-256 values are
`7547c3c3b789e9a20029d5c7c2ef4ce653e608f000412091cf2c38162aaa9188`,
`a9c8ceda6f52dd316f754d8c403f904416325f31740783f8e183ee0d235ec58e`, and
`ee0e17d653f3cfc96784755a17c136c4b26ac9864b67f7a3303e63043d528411`.

From `03_FORMALIZATION`, `lake env lean <absolute-path-to-check.lean>` returned
0 against that built module; [check.lean](check.lean) and [check.log](check.log)
record the declarations and axiom reports. The two final theorems use
`propext`, `Classical.choice`, and `Quot.sound`. The generated `.olean` SHA-256
was `bee0a6d24f4c6ee0c9230a000046d16a2d71b47f60ec7a2f579f282ce4bc72ff`;
it is a local build artifact, not included here.
