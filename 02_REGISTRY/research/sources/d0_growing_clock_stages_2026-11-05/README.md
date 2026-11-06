# Clock frames from finite stages: Lean receipt

Implementation commit `02bfcd183382f2668620c8333fb7d7dd3ca0a1c4`, file
`03_FORMALIZATION/D0/Algebra/GrowingClockStages.lean`, SHA-256
`deb74a3113b72a2812f7ed5b44d55cd14ebe701a45c795b052a6b38ac4773373`.
The owner is #334 `afd99daf54d26ef7e1b47a94f380557213e9c6d5`,
`02_REGISTRY/research/sources/d0_retained_response_concentration_2026-10-28/GROWING_CLOCK_RU.md`
§§1–3, Git blob `370e8fb572e85fedeebe2e72531c01d5b68b0a91`.

For potentially different finite coordinate types `H j`, the sigma type
`Σ j, H j` provides the coordinates of their direct sum. The matrix `stageFrame`
places an individual map in its stage and zero in all others. The Lean theorem
`stageFrame_orthogonal` derives `(J i)† J j = if i=j then 1 else 0` solely
from the isometry of each stage map. Given isometries `A j : h0 → H j` and
an initial isometric frame `V : r → h0`, `transported_isometry` supplies that
premise for `A j * V`. `stage_clock_determinant` passes the resulting derived
frames directly to the previously proved `clock_cut_determinant`; it still
requires `T†T=1` and actual stage advances of these frames. A finite zero-frame
control demonstrates failure of the diagonal equality without isometry.

The owner's concrete spaces, basis identifications, isometries and clock have
not been built here. Owner application needs, among other things, the initial
cut identification `P₀ = V V†`, the correct initial identification and
`A₀V = V`, the actual `A j`, and proofs of clock isometry and stage advance.
No 425D lift, field map, physical admission, Cost−Info selection or GR closure
is claimed. Neither the desired frame orthogonality nor the target determinant
is assumed in the new consumer.

## Verification and provenance

`python3 tools/lean_task_build.py narrow D0.Algebra.GrowingClockStages` returned
0 in an isolated sparse checkout and independently cloned existing `.lake`
cache; [narrow.log](narrow.log) records its full output, including the two
pre-existing unused-section warnings in the imported GrowingClockFrame module.
This is a targeted cached build, not a full clean build nor a `D0.All` build;
`D0.All` gained an import. The build receipt source/dependency/environment
SHA-256 values are `8f24421c46cf8632efbfcce4735d54ca66cd261218914776393317d44b58285e`,
`a9c8ceda6f52dd316f754d8c403f904416325f31740783f8e183ee0d235ec58e`, and
`ee0e17d653f3cfc96784755a17c136c4b26ac9864b67f7a3303e63043d528411`.

From `03_FORMALIZATION`, `lake env lean` applied to [check.lean](check.lean)
returned 0; [check.log](check.log) records the exact types and axiom reports.
The three declarations depend on `propext`, `Classical.choice`, `Quot.sound`.
The generated `.olean`, not included in Git, had SHA-256
`2afaa21e3ce46c1d7dcf2fd0db86ad55855a812b0abafae15b9f2a485734de06`.

## Historical six-module inventory

The saved collector output on the original stage checkpoint contains the same 482
declaration records, byte-for-byte, as the [existing frame inventory](../d0_proof_architecture_formalization_2026-10-24/reports/c0_growing_frame_inventory_d9eb_2026-11-05/declarations.json).
To reconstruct that historical output, replace the single values of
`snapshot_commit` and `lean_source_digest` in those bytes with
`aa5626f53bc6b250d6b2feef098d222883e0886a` and
`8f24421c46cf8632efbfcce4735d54ca66cd261218914776393317d44b58285e`, respectively.
The reconstruction was byte-compared with the saved output; its SHA-256 is
`2c8ba2bc5a12cc3dbf63ead7bf045bb11cb35dcd8ca64b1e01e8de8445dae978`. This observation concerns the six inventoried modules on the old stage checkpoint.
