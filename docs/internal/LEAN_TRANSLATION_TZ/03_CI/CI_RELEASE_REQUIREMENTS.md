# CI requirements for D0 Lean formalization

Required release commands:

```bash
lake exe cache get
lake build
python tools/check_no_sorry_in_core.py
python tools/check_claim_map_coverage.py
python 05_CERTS/run_all_core_certs.py
python 05_CERTS/run_all_bridge_certs.py
python 05_CERTS/run_all_empirical_passports.py
python tools/build_release_ledger.py
```

Release fails if:

- `Float` appears in Lean theorem definitions outside examples/tests.
- `sorry` appears in `D0/Core`, `D0/Combinatorics`, `D0/Topology`, `D0/Algebra`, `D0/Gauge`.
- `axiom` appears outside `D0/Bridge/Assumptions`.
- A bridge theorem imports assumptions silently into core.
- Any active `Claim ID` has no Lean theorem, cert, or passport mapping.
- Any empirical claim lacks data hashes and run command.
- Status database and generated `CLAIM_TO_LEAN_MAP.csv` disagree.
