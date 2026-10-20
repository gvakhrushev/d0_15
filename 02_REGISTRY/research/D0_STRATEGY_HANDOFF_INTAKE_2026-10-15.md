# D0 strategy and source preservation — reconciled with #324

15 October 2026. Repository: `gvakhrushev/d0_15`. Task: `CONTROL-PLANE`, PR #323.
Base: `fa2b04b9c8aae5a0b8470322d6091712ce56567a`.
Original proposal: `cd02a65de1c708eae113b03ca63392e1641c427c`.

## Single ownership

[#324](https://github.com/gvakhrushev/d0_15/pull/324) owns the only operational
flow: README, AGENTS, current gravity route, work guide, live task dispatcher
and CI execution. This #323 supplies strategy and preserved research inputs.
It adds no entry point, execution overlay, role dispatcher, queue row or task
brief. Neither PR merges or accepts the other automatically.

The original competing process proposals remain available in the
[immutable original proposal](https://github.com/gvakhrushev/d0_15/tree/cd02a65de1c708eae113b03ca63392e1641c427c):
`D0_START_HERE_RU.md`, `D0_GR_EXECUTION_PLAN.json`, the four proposed briefs,
`tools/d0_handoff.py`, and the former README/AGENTS rewrite. They are historical
proposals, not commands or registered work in the reconciled tree. No proposed
execution has been launched. The restored main queue retains its original
rows and WIP limits. The original source commit is an ancestor of this revision;
no force overwrite is used.

The original `README_CORPUS.md` and `AGENTS_PROTOCOL.md` were exact copies of
main blobs `4a01f69d815ad234d6010142be3c304009916de0` and
`024d2d0c2f01e25a32fd8c6f95488c73a1d849be`. Those duplicates are unnecessary;
the originals and the initial proposal remain in Git history.

## Preserved unique content

| Material | Scope | Original Git blob |
|---|---|---|
| [User strategy](D0_RESEARCH_STRATEGY_RU.md) | Full bottom-up vision, constructive synthesis, minimal closure, pi0, golden record, resonant matter, archive and moving preparation | `9c9eb4a77a68a5a631e0c902da1d744a09be7e29` |
| [18 scientific leads](D0_IDEA_REGISTER.json) | Origins, mechanisms, missing proof links and consumers; historical role tags do not dispatch agents | `27caee32a4a0fc01a83b17cdfdfe9e000f8a128c` |
| [Original source notes](D0_HANDOFF_SOURCE_NOTES_RU.md) | Selected user quotations and separately labelled historical sketches | `86951250b8c561e0a5fc15a328f1cb51d57b93bc` |
| [G0–G4 proof decomposition](D0_GR_CLOSURE_CONTRACT_RU.md) | Supporting scientific map for #324's two fronts, with common `Omega_h -> (A_h,R_h)` and no readout-completeness assumption | Original `b1963497af9e2c7d24b7e342e32f07637a4704e8`; reconciled text includes the explicit interface repair |

The first three files and the entire source capsule remain byte-identical to
the original proposal. The common proof decomposition is clarified rather than
promoted to a second current plan. #324 connects I01–I09/I11/I16 to preparation
and source, I14–I15 to joint equations/refinement, I10 to physical response
equivalence, I12–I13 to downstream calibration, and I17–I18 to work rationale.
Numerical sketches remain leads, never new physical premises.

## Lossless source capsule

[sources/d0_strategy_handoff_2026-10-15/INPUT_MANIFEST.json](sources/d0_strategy_handoff_2026-10-15/INPUT_MANIFEST.json)
records 21 UTF-8 files: 20 Ward/resonance inputs and the original strategy audit.
All six payload parts, the manifest and restoration script retain their exact
original blobs. This preserves the stated files, not the entire outer ZIP.

- Packed SHA256: `a4db16bad334bc7a6a5b28f3400adaba8ef6a718b54ce11451fc9dcf151c4f1d`.
- Decoded JSON SHA256: `6fd4d7a179ba693a7985d86fa7aa331e47b5c38a8ab95b0d2fc7050a754058cf`.
- Original audit SHA256: `d258c771a2a3a0939e4203c3018bf651309e6b36bb4cdaa130cb5ab8b4ad61ff`.

```sh
python 02_REGISTRY/research/sources/d0_strategy_handoff_2026-10-15/restore.py --check
python 02_REGISTRY/research/sources/d0_strategy_handoff_2026-10-15/restore.py --extract /tmp/d0-handoff-inputs
```

Extraction refuses differing existing files and unsafe paths; it does not
execute the scientific programs. Independent safe extraction verified every
restored file hash and the audit's equality to the user-supplied source.
Mathematical replay retains the declared upstream full4D capsule ref
`9fbc75db0a94707dc3105cdfb3f322a14e62a979`; no missing source is replaced by prose.
This preservation does not install the Ward packet into #310 or expand #322.

## Complete readable research packet, 15 October 2026

The [record-geometry research packet](sources/d0_record_geometry_2026-10-15/README.md)
now publishes the latest synthesis, full expensive-AI brief, proofs, instructions,
source programs and recorded results as directly readable text. Its manifest maps
all 150 recursive text occurrences in the supplied ZIP to 77 unique contents;
the earlier 21-file strategy capsule is also readable, bringing the combined
total to 78 unique source texts. The existing capsule and strategic originals
remain unchanged. No ZIP or base64 decoding is needed to read the evidence.

The packet pins both its historical #310 input and the newer publication-time
SOURCE, identifies already completed work to avoid repeating it, and provides
safe text-based replays without executing historical import/patch commands.
This is additional preservation in #323: #324 retains the only operational
flow, and the expensive brief continues #310 under its existing ownership.
No task row, scientific owner, acceptance or parent terminal changes here.

## Validation and acceptance boundary

The preservation workflow checks only the idea inventory and capsule integrity;
it does not inspect role/WIP/brief proposals or run scientific certificates.
Canonical structural/work/protocol/generated-view checks apply to the actual
reconciled candidate. Current PR CI, not the original failed run, establishes
its remote guard status.

No Lean, physical action/source binding, refinement-uniform nonlinear inverse,
GR closure, scientific acceptance or parent retirement is claimed by this
content intake. The distinct #202/#310/#317 obligations and #322 review remain
unchanged. Merge and scientific use remain separate decisions.
