# Local replay of the pinned moving-cut checker

This replay uses the exact checker and stored result from #334 commit
`eebcb5e467742df3e9cf7fa9702042d7294aa742`. The checker SHA-256 is
`da4df4d9c075b9b6cc01a4c74503ea1bb379d062bdbb74e5ddb02703f2f85d2c`.

Run from the repository root:

```sh
python3 02_REGISTRY/research/sources/d0_root_moving_cut_2026-10-28/check_root_moving_cut.py > 02_REGISTRY/research/sources/d0_root_moving_cut_2026-10-28/local_replay_2026-10-28/normal.json 2> 02_REGISTRY/research/sources/d0_root_moving_cut_2026-10-28/local_replay_2026-10-28/normal.stderr
python3 -O 02_REGISTRY/research/sources/d0_root_moving_cut_2026-10-28/check_root_moving_cut.py > 02_REGISTRY/research/sources/d0_root_moving_cut_2026-10-28/local_replay_2026-10-28/optimized.json 2> 02_REGISTRY/research/sources/d0_root_moving_cut_2026-10-28/local_replay_2026-10-28/optimized.stderr
```

Both outputs are byte-identical to each other and report
`PASS_FULL_BOOTSTRAP_MOVING_CUT`, `GR_closed=false`, and moving-cut source
`0.06218198611141448`. The local environment is Python 3.9.6 / NumPy 2.0.2;
the pinned owner receipt records maximum finite-difference error
`7.698841564263148e-12`, while this local replay records
`7.00670077513621e-12`. Nine numeric result fields differ from the pinned
receipt, with maximum absolute difference `1.3507694962555661e-11` in a
finite-difference sample. This is environment-sensitive numerical output,
not a byte-identical replay of the owner's JSON.

Each mode emitted 12 NumPy `RuntimeWarning` records; both 1,493-byte stderr
files are retained and identical. The warnings are not suppressed or declared
harmless. The replay verifies this finite checker only; it does not execute
full42, Lean, CI, or a physical GR selection.

Verify the replay files and, where the Git objects are available, their source
pins:

```sh
python3 02_REGISTRY/research/sources/d0_root_moving_cut_2026-10-28/local_replay_2026-10-28/verify_local_replay.py --verify-source-objects
```
