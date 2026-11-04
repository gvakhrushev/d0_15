# Isolated Lean build feasibility probe

Snapshot: `24363981f4d3568d92d78e6ef455e7123f88e297` (published PR #402 head at probe).
Manifest SHA-256: `4ed211000f753c64c6b1fc155970f6b28c9500763f1ad520d8762ae165ac24fa`. Toolchain pin: `leanprover/lean4:v4.30.0`.

**Outcome: no final build was run and there is no successful build receipt.** The strict dependency-source preflight failed before Lean. This is not an independent build, proof validation, C0 acceptance, or GR closure.

A separate project Git checkout was cloned from the published GitHub branch and checked out at the snapshot above. Each dependency was independently cloned from the corresponding local Git repository with `--no-hardlinks --no-checkout --local`, then checked out at its manifest revision. These source Git checkouts contain no copied `.lake/build` or shared `.olean`; this does not independently authenticate the local source Git object databases. The project status command returned no changes.

Dependency HEAD equality to manifest revisions was checked by the setup script. The full before/after byte provenance did not complete and is not asserted. The revisions were:

- `mathlib`: `6988106320cbae4bcbd5d142075946f7fe08a7b7`
- `plausible`: `a456461b368b71d2accd95234832cd9c174b5437`
- `LeanSearchClient`: `c5d5b8fe6e5158def25cd28eb94e4141ad97c843`
- `importGraph`: `515cf9d0c00ece5e661f6de4326a53dedc1e8ea1`
- `proofwidgets`: `a84b3e2475d5c5ab979567b1ad8aea21b764bcf8`
- `aesop`: `558915ae105bfd8074e22d597613d1961822adc2`
- `Qq`: `a6e6c34c4ef182f83b219a3a5a385f51f44bdc4c`
- `batteries`: `32dc18cde3684679f3c003de608743b57498c56f`
- `Cli`: `6b907cf12b2e445ccb7c24bc208ef04a1f39e84c`

Preflight ran in the isolated checkout with `LAKE_NO_CACHE=1`, `LEAN_NUM_THREADS=1`, `PYTHONDONTWRITEBYTECODE=1`, using:

```text
python -X utf8 -B -c "import json,lean_task_build as t; d=t.dependency_provenance(); print('DEPENDENCIES',json.dumps(d,sort_keys=True)); print('SOURCE_SHA256',t.source_digest()); print('ENV_SHA256',t.build_environment_digest()); print('TOOLCHAIN',json.dumps(t.toolchain_snapshot(),sort_keys=True))"
```

The strict preflight exited 1 in `dependency_provenance()` while resolving the tracked Mathlib symlink `scripts/bench/build/fake-root/bin/lean.py` to its tracked `lean` target: `Path.resolve(strict=True)` returned Windows `FileNotFoundError` / WinError 3. A separate read confirmed the target exists. Source digest, environment digest and toolchain snapshot occur after that call and therefore were not obtained in this preflight. No provenance rule or source was altered.

An independent temporary junction to an existing directory on the same extra volume allowed reading a sentinel, but strict resolution of both junction and file returned WinError 3. The test removed the junction and temporary files; no permanent mount was created. This is a platform/path limitation, not evidence of a missing dependency or of a successful build.

At inspection the original system volume had approximately 5.79 GB free; the existing project build and dependency trees contained approximately 2.79 GB and 7.17 GB respectively. The separate volume reported approximately 301 GB free. A full from-source build duration and peak resource use were not measured. No full replay was run or stopped.

The following copies redact user and volume paths and normalize textual line endings; their contents are not byte-identical to the original logs. Original SHA-256 values are retained for correlation, and sanitized hashes identify these files:

| Artifact | Original SHA-256 | Sanitized SHA-256 |
| --- | --- | --- |
| `setup.log` | `f7308addf68f298acb68b81f185cbe3e4223a4608393074a55aa7f9cc2d076d1` | `2413be861b4521de9b103e86991e91e963c60f6414c6ff930ee85ecde2fb25d9` |
| `preflight.log` | `be2d645cbfb47e161a19ff535d2b4a2093426117daf75fb678aa20a83ba12135` | `0d772750c15a416fb5f2a94ed5beccc86f0c5d6415292ed49e8b5cb5fcdaeb6b` |
| `junction-probe.json` | `d2b1c5a97549b4b823d302e203f1018568676fe24c4f22c41145496db310ef56` | `ad174ae60acc2b159f7a94044dde8ff3a409f906e720a5a423d5cc18b612e6fb` |

The runtime source checker reports generated binary build caches and dynamic libraries outside its attestation boundary. None of the checks here establishes a successful final build.
