#!/usr/bin/env python3
"""Guard that v14 P6 SM-facing gauge decomposition is theory/book synchronized."""
from __future__ import annotations
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "09_LEAN_FORMALIZATION" / "D0"
BOOKS = ROOT / "01_BOOKS"

checks: list[tuple[Path, list[str]]] = [
    (LEAN / "Gauge" / "SMGaugeDecomposition.lean", [
        "FrozenSMGaugeDecomposition",
        "frozenSMGaugeDecomposition",
        "frozen_sm_gauge_factors_closed",
        "frozen_sm_generation_ledger_closed",
        "frozen_sm_generation_anomaly_free",
        "no_alternative_sm_factors_at_frozen_ledger",
        "no_alternative_sm_generation_ledger_at_frozen_decomposition",
        "sm_eft_bridge_requires_frozen_decomposition",
        "frozen_sm_eft_bridge_boundary_closed",
    ]),
    (LEAN / "Bridge" / "FinalBridgeIndex.lean", [
        "import D0.Gauge.SMGaugeDecomposition",
        "smGaugeFactorsClosed",
        "smGenerationLedgerClosed",
        "smGenerationAnomalyFree",
        "smNoAlternativeGaugeFactors",
        "smEftBridgeRequiresFrozenDecomposition",
    ]),
    (LEAN / "TheoremLedger" / "HardClosureTheoremIndex.lean", [
        "D0.Gauge.frozen_sm_gauge_factors_closed",
        "D0.Gauge.frozen_sm_generation_anomaly_free",
        "D0.Gauge.no_alternative_sm_factors_at_frozen_ledger",
        "D0.Gauge.sm_eft_bridge_requires_frozen_decomposition",
    ]),
    (ROOT / "03_THEORY_MAP" / "BOOK_REFACTOR_AUDIT.md", [
        "SM-facing finite gauge decomposition",
        "D0.Gauge.FrozenSMGaugeDecomposition",
        "SM-looking dimensions therefore the SM Lagrangian is derived",
    ]),
    (BOOKS / "BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md", [
        "02.36.6 SM-facing gauge decomposition",
        "D0.Gauge.SMGaugeDecomposition",
        "no alternate factor/representation ledger",
    ]),
    (BOOKS / "BOOK_04_SPECTRUM_MATTER_AND_FINITE_SELECTOR_THEORY.md", [
        "04.11 SM-facing finite gauge decomposition",
        "D0.Gauge.FrozenSMGaugeDecomposition",
        "no-free-decomposition owners",
        "not a fitted Standard-Model import",
    ]),
    (BOOKS / "BOOK_05_VERIFICATION_STATUS_AND_CERTIFICATE_DISCIPLINE.md", [
        "## 05.13 Current inherited priority gates",
        "D0.Gauge.SMGaugeDecomposition",
        "sm_eft_bridge_requires_frozen_decomposition",
    ]),
]

failures: list[str] = []
for path, needles in checks:
    if not path.exists():
        failures.append(f"missing {path.relative_to(ROOT)}")
        continue
    text = path.read_text(encoding="utf-8")
    for needle in needles:
        if needle not in text:
            failures.append(f"{path.relative_to(ROOT)} missing {needle!r}")

# The active Book 04 must not promote the full SM Lagrangian as already derived.
book04 = (BOOKS / "BOOK_04_SPECTRUM_MATTER_AND_FINITE_SELECTOR_THEORY.md").read_text(encoding="utf-8")
for forbidden in [
    "the full Standard-Model Lagrangian is derived",
    "SM Lagrangian is core-closed",
    "running couplings are core theorems",
]:
    if forbidden in book04:
        failures.append(f"Book 04 contains forbidden overclaim {forbidden!r}")

if failures:
    print("FAIL_V14_SM_GAUGE_SYNC")
    for f in failures:
        print(" -", f)
    sys.exit(1)

print("PASS_V14_SM_GAUGE_SYNC")
