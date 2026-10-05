# Repository claim-scope and CI audit — 2026-10-05

Repository: `gvakhrushev/d0_15`
Task: `CONTROL-PLANE`
Base: `e80a3b1ccf615fb4f70bf5900181592604928497`
Status: implementation pending in the associated Draft PR.

## Bounded acceptance scope

This control change repairs concrete inconsistencies found by the repository audit:

- align the README's Yukawa selector, Pisot/time and determinant descriptions with their actual owners;
- accept explicitly open and unproved registry targets without permitting them to masquerade as core proofs;
- preserve both proof status and release status in generated claim metadata;
- run the existing claim-coverage and no-shortcuts checks in CI, with narrow hostile regression controls.

Scientific claim and release labels remain governed by the existing registry. This work does not supply a missing physical selector, prove a continuum bridge, or retire any active research task. Exact declaration binding is a separate obligation if the heterogeneous registry cannot support it without a broader schema migration.

## Validation record

To be completed with the implementation, local checks and current-head CI evidence.
