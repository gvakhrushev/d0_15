# Remote intake of the three previously local scientific packets

22 October 2026. Repository `gvakhrushev/d0_15`. Existing scientific owner: Draft PR #334, branch `exp/a4d-joint-response-continuation-2026-10-16`.

## Delivery completed by this commit

The 29 text files from the previously supplied `D0_global_spectral_closure_2026-10-22.patch` are imported at their original repository paths, byte-for-byte. The original local delivery root commit `5ab5340eb9a211ff642faec3182829f57f073608` is provenance, not a parent substituted for the remote branch. This intake preserves the latest inspected remote head `f9d47475cceaebbba481bfb979be006fcef687a1`, including all eleven concurrent commits since `31d174bbf39a6d055ee3a1369b254f400b4f8952`. No source, Book, existing research owner, or acceptance flag is overwritten.

Imported inventory: one routing note, eighteen files in `sources/d0_global_spectral_closure_2026-10-22/`, and ten files in `sources/d0_native65_causal_source_2026-10-22/`; total 186095 bytes. All 29 Git blob hashes agree with the local delivery inventory. The global packet's `previous/` directory preserves the earlier paired spectral synthesis; these are three scientific packets, not 29 new theorems.

## Entry points

- [Global thermal Schur/Ward and scene-source synthesis](A4D_GLOBAL_THERMAL_SCHUR_WARD_AND_SCENE_SOURCE_LIMIT_2026_10_22.md).
- [Complete spectral proof](sources/d0_global_spectral_closure_2026-10-22/THEOREM.md).
- [Earlier paired Hodge/full heat exact null-family composition](sources/d0_global_spectral_closure_2026-10-22/previous/GLOBAL_SYNTHESIS.md).
- [Native65 complete-history causal price and source](sources/d0_native65_causal_source_2026-10-22/THEOREM.md).

## Fresh replay performed for this intake

`OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python run_validation.py` ran successfully in the extracted global packet before upload. Its read-only wrapper checked all sixteen pins before and after, and reproduced all four frozen outputs:

| Command | Exact stdout SHA-256 |
|---|---|
| `python check_spectral_closure.py` | `c215ce4d8a8cb34db64204656c86ddfab6e22f40d9cada01901ee469e1f3bc3f` |
| `python -O check_spectral_closure.py` | `c215ce4d8a8cb34db64204656c86ddfab6e22f40d9cada01901ee469e1f3bc3f` |
| `python inputs/check_all40_arbitrary_brinkmann.py` | `09570bf30707b6f25ad2e38b7b6be3474e0ff3c15b7e857327ebce07502b9db1` |
| `python previous/check_global_spectral.py` | `a71c4fbf00c350e8c483b8aaece8325182addc3788bb048e9f9e2ffc5c23768e` |

The new spectral checker has 190 active checks per run. The inherited symbolic all40 checker was executed with its assertions enabled. The native65 packet is an unchanged archival import; its numerical suite is not claimed rerun for this intake. No new Lean build, independent review, remote CI pass, or main merge is asserted.

## Historical metadata versus current publication

The original manifests, receipts and prose explicitly record their earlier local-only transport state (`remote_published=false`, `remote_repository_modified=false`, or equivalent). Those bytes are retained deliberately so that their hashes and original provenance remain valid. This intake note supersedes only their old delivery status: the files are now tracked by this remote research-branch commit. It does not revise their scientific claims or turn an old receipt into a new remote CI result.

## Scientific boundary

These are scoped mathematical results: the paired spectral field model and its regular continuum sectors, true-scene heat source bounds, and a distinct measured native65 history. No equality of those executions, compulsory physical Book03 selection, complete independent-apparatus stationarity, generic finite-grid recovery, or universal D0-to-GR closure is inferred from importing them. `GR_closed=false` remains unchanged.
