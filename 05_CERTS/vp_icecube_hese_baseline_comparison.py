#!/usr/bin/env python3
"""D0-PASSPORT-ICECUBE-HESE-001 - IceCube HESE baseline comparison.

Registry: lean_status OPEN, release_status PROOF-TARGET (empirical passport pending external
data). This certificate does NOT assert a physics result and CANNOT promote the claim to core.
It is a *propagator/verifier* of the pre-registered IceCube HESE baseline-comparison analysis:
it loads the recorded summary artifacts, cross-checks that the external HESE data backing them
is actually pinned (every manifest cache file present AND sha256-matching), and emits the honest
PASS/FAIL/SKIP token that matches the recorded analysis. It can FAIL: a FAIL verdict or a
corrupt/over-claiming artifact returns a non-zero exit.

FORM vs VALUE (house style):
  FORM  = selftest(): always-run, data-independent assertions that the can-FAIL machinery is
          sound (the PASS gate rejects no-data, rejects a recorded FAIL, rejects a no-improvement
          PASS). selftest() RAISES on any regression, so the cert can never silently rot.
  VALUE = main(): data-gated. Readiness is derived from the REAL cache (re-hash of local_path vs
          the pinned sha256 + file presence), NEVER from the manifest's hand-set status field.
          No-data ⇒ SKIP_*_EXTERNAL_DATA_REQUIRED; PASS is reserved for a real data run.

================  PRE-REGISTRATION  (per 08_PASSPORTS/IceCube/icecube_baseline_protocol.md)

STATISTIC (primary, frozen BEFORE the result):
  Energy-binned HESE high-energy-bin event count compared against two curves:
    - the no-decoherence baseline null (empirical no-deco energy shape; low+mid log10(E)
      bins power-law extrapolated to the high bin), and
    - the FROZEN D0 Hurwitz phason-damping curve emitted by
      vp_neutrino_phason_decoherence_passport.py --mode hese12 (no refit, no free exponent).
  Test statistics on the high bin:
    delta_loglik = poisson_loglik_d0 - poisson_loglik_null     (D0 better iff > 0)
    delta_chi2   = chi2_d0          - chi2_null                (D0 better iff < 0)
  Secondary (must NOT alter the primary event set): track/cascade topology ratio vs energy.

WINDOW (frozen BEFORE the result):
  IceCube HESE 12-year public event table, pinned by icecube_manifest.json, partitioned into
  3 log10(energy) bins; the comparison is scored on the TOP (high-energy) bin only
  (recorded edges 1.97e4 .. 4.80e6, high_bin_obs = 4). Events are frozen before the result.
  Forbidden (protocol): free damping exponent as core; energy threshold tuned after HESE;
  post-hoc topology selection; discarding events after seeing the result.

FALSIFIER (the can-FAIL contract; the verdict is PROPAGATED from the recorded summary, never
re-judged here, then GATED on the data actually being pinned):
  PASS  (PASS_ICECUBE_HESE_D0_BASELINE_COMPARISON): allowed ONLY when the external data are
        pinned/hash-verified AND the recorded summary status is PASS AND the frozen D0 curve
        strictly improves the declared statistic (delta_loglik > 0 AND delta_chi2 < 0) with no
        retuning. Exit 0.
  FAIL  (FAIL_ICECUBE_HESE_D0_BASELINE_COMPARISON): REQUIRED when the data are pinned and the
        no-deco baseline matches or beats the frozen D0 curve under the declared statistic
        (recorded status FAIL). Exit 1.
  SKIP  (SKIP_NEUTRINO_PHASON_DECOHERENCE_EXTERNAL_DATA_REQUIRED): REQUIRED when the pinned
        external HESE data are NOT present / NOT sha256-verified on disk: the live comparison
        cannot be reproduced and is NOT promotable, regardless of any stale recorded verdict.
        Exit 0. (SKIP_NEUTRINO_PHASON_DECOHERENCE_BASELINE_REQUIRED is used when the data are
        present but no recorded baseline summary exists yet.)

RECORDED ANALYSIS (as of this cert's authorship - reported, not trusted blindly):
  icecube_hese_baseline_summary.json status = FAIL_ICECUBE_HESE_D0_BASELINE_COMPARISON
  (delta_loglik = +0.00308, delta_chi2 = -0.00451, avg_damping_high = 0.99934 ~ no damping:
  "no-deco null describes the high-energy bin as well or better than tiny D0 damping").
  The two pinned cache files (hese12_events, hese12_license) are ABSENT on disk (the cache
  dir does not exist) -> the live verdict is SKIP (external data required), and the recorded
  FAIL is reported only as stale, un-reproducible context. This cert gates on ACTUAL file
  presence + sha256, never on the manifest's self-declared status field, and additionally
  flags the inconsistency where the manifest claims READY while the cache is absent.

HONESTY BOUNDARY:
  EXACT here: sha256 hex equality of each cache file vs the manifest; presence on disk;
    propagation (not re-derivation) of the recorded status token.
  POSTULATED / EXTERNAL: the no-deco baseline and the recorded Poisson/chi2 numbers come from
    vp_neutrino_phason_decoherence_passport.py over external HESE data; this cert does NOT
    recompute the physics and NEVER widens a margin to manufacture a PASS.

Run: exit 0 + SKIP/PASS token, or exit 1 + FAIL token (or traceback on a corrupt/over-claiming
artifact). A runner that token-matches PASS must NOT see PASS here while the data are unpinned.
"""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Windows consoles default to a non-UTF8 codepage; reconfigure so prints never crash.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
PASSPORT_DIR = ROOT / "08_PASSPORTS" / "IceCube"
MANIFEST_PATH = PASSPORT_DIR / "icecube_manifest.json"
BASELINE_SUMMARY_PATH = PASSPORT_DIR / "icecube_hese_baseline_summary.json"
PHASON_SUMMARY_PATH = PASSPORT_DIR / "icecube_phason_decoherence_summary.json"

PASS_TOKEN = "PASS_ICECUBE_HESE_D0_BASELINE_COMPARISON"
FAIL_TOKEN = "FAIL_ICECUBE_HESE_D0_BASELINE_COMPARISON"
SKIP_DATA_TOKEN = "SKIP_NEUTRINO_PHASON_DECOHERENCE_EXTERNAL_DATA_REQUIRED"
SKIP_BASELINE_TOKEN = "SKIP_NEUTRINO_PHASON_DECOHERENCE_BASELINE_REQUIRED"
RECOGNIZED_RECORDED = {PASS_TOKEN, FAIL_TOKEN}

# Keys the recorded baseline summary MUST carry; a malformed artifact is a hard failure
# (the guillotine: a summary that omits its own statistic cannot be honoured).
REQUIRED_BASELINE_KEYS = (
    "status",
    "high_bin_obs",
    "delta_loglik",
    "delta_chi2",
    "poisson_loglik_null",
    "poisson_loglik_d0",
    "chi2_null_high",
    "chi2_d0_high",
)


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def would_pass(baseline: dict[str, Any] | None, data_present: bool) -> bool:
    """The single PASS gate. PASS requires: data pinned AND recorded status PASS AND the
    frozen D0 curve strictly improves BOTH declared statistics. Anything else is not a PASS."""
    if not data_present or not baseline:
        return False
    if baseline.get("status") != PASS_TOKEN:
        return False
    return float(baseline["delta_loglik"]) > 0.0 and float(baseline["delta_chi2"]) < 0.0


def check_cache_files(manifest: dict[str, Any]) -> tuple[bool, list[dict[str, Any]]]:
    """Return (data_present, per-file report). data_present is True ONLY when every declared
    cache file exists AND its sha256 matches the manifest. Missing manifest['files'] => not
    present (we never treat an unpinned dataset as available)."""
    files = manifest.get("files") or []
    assert isinstance(files, list), "manifest 'files' must be a list"
    report: list[dict[str, Any]] = []
    all_ok = bool(files)
    for item in files:
        label = item.get("label", "")
        local = item.get("local_path", "")
        expected = (item.get("sha256") or "").lower()
        path = ROOT / local if local else None
        exists = bool(path and path.exists())
        actual = sha256_of(path) if exists else None
        match = bool(exists and expected and actual == expected)
        all_ok = all_ok and match
        report.append(
            {
                "label": label,
                "local_path": local,
                "exists": exists,
                "sha256_expected": expected or None,
                "sha256_actual": actual,
                "sha256_match": match,
            }
        )
    return all_ok, report


def selftest() -> None:
    """FORM gate (always run, data-independent): the can-FAIL machinery itself must be sound.
    Raises AssertionError on any regression so the cert can never silently rot into a stub."""
    assert PASS_TOKEN.startswith("PASS_") and FAIL_TOKEN.startswith("FAIL_")
    assert SKIP_DATA_TOKEN.startswith("SKIP_") and SKIP_BASELINE_TOKEN.startswith("SKIP_")
    assert len({PASS_TOKEN, FAIL_TOKEN, SKIP_DATA_TOKEN, SKIP_BASELINE_TOKEN}) == 4, "tokens must be distinct"
    # synthetic fixtures exercise every edge of the PASS gate (no external data needed):
    rec_pass = {"status": PASS_TOKEN, "delta_loglik": 0.5, "delta_chi2": -0.5}
    rec_pass_no_gain = {"status": PASS_TOKEN, "delta_loglik": -0.5, "delta_chi2": 0.5}
    rec_fail = {"status": FAIL_TOKEN, "delta_loglik": 0.003, "delta_chi2": -0.004}
    assert would_pass(rec_pass, True) is True, "FORM: a genuine improvement with pinned data must PASS"
    assert would_pass(rec_pass, False) is False, "FORM control A: PASS may never be claimed without data"
    assert would_pass(rec_fail, True) is False, "FORM control C: a recorded FAIL must never upgrade to PASS"
    assert would_pass(rec_pass_no_gain, True) is False, "FORM: a PASS status with no improvement must be rejected"
    assert would_pass(None, True) is False, "FORM: a missing summary cannot PASS"


def main() -> int:
    print("=== D0-PASSPORT-ICECUBE-HESE-001  IceCube HESE baseline comparison ===")
    selftest()  # FORM gate first: refuse to run if the can-FAIL machinery has regressed

    # ---- load artifacts (schema guillotine) -----------------------------------------
    manifest = load_json(MANIFEST_PATH)
    assert manifest is not None, f"manifest missing: {MANIFEST_PATH}"
    baseline = load_json(BASELINE_SUMMARY_PATH)
    phason = load_json(PHASON_SUMMARY_PATH)

    if baseline is not None:
        for key in REQUIRED_BASELINE_KEYS:
            assert key in baseline, f"recorded baseline summary missing required key {key!r}"
        assert (
            baseline["status"] in RECOGNIZED_RECORDED
        ), f"unrecognized recorded baseline status {baseline['status']!r}"

    # ---- cross-check the manifest cache actually exists (never trust self-declared READY)
    data_present, file_report = check_cache_files(manifest)
    manifest_ready_declared = manifest.get("status") == "READY"
    ready_contradicted = manifest_ready_declared and not data_present
    missing = [r["label"] or r["local_path"] for r in file_report if not r["exists"]]
    hash_mismatch = [r["label"] or r["local_path"] for r in file_report if r["exists"] and not r["sha256_match"]]

    # ---- determine the honest verdict (propagate recorded status, gate on data) ------
    if not data_present:
        verdict = SKIP_DATA_TOKEN
        rc = 0
        reason = "external HESE cache not pinned (missing/hash-mismatch); comparison not reproducible"
    elif baseline is None:
        verdict = SKIP_BASELINE_TOKEN
        rc = 0
        reason = "HESE data pinned but no recorded no-deco baseline summary to compare against"
    elif would_pass(baseline, data_present):
        verdict = PASS_TOKEN
        rc = 0
        reason = "frozen D0 curve strictly improves the declared statistic over the no-deco baseline"
    elif baseline["status"] == FAIL_TOKEN:
        verdict = FAIL_TOKEN
        rc = 1
        reason = "no-deco baseline matches or beats the frozen D0 curve under the declared statistic"
    else:
        # recorded status is PASS but the strict improvement gate failed -> reject (do not honour)
        raise AssertionError(
            f"over-claim: recorded status {baseline['status']!r} but deltas do not show strict "
            f"D0 improvement (delta_loglik={baseline.get('delta_loglik')}, "
            f"delta_chi2={baseline.get('delta_chi2')})"
        )

    # ---- verdict token FIRST among PASS_/FAIL_/SKIP_ words (so the runner reads it) ---
    print(verdict)
    print(f"reason: {reason}")

    # ---- runtime negative controls (the guillotine on THIS run's actual inputs) -------
    assert (verdict != PASS_TOKEN) or data_present, "control A: PASS may never be emitted without pinned data"
    if baseline is not None and baseline["status"] == FAIL_TOKEN:
        assert not would_pass(baseline, True), "control C: a recorded FAIL must never upgrade to PASS"
    print("CONTROL_OK: FORM selftest passed; data-gate + no-FAIL-upgrade hold on this run")

    # ---- honesty / cross-checks (named boundaries; no PASS_/FAIL_/SKIP_ wordstarts) ---
    if ready_contradicted:
        print(f"HONEST_MANIFEST_READY_CONTRADICTED_BY_DISK: missing={missing} hash_mismatch={hash_mismatch}")
    print(f"HONEST_RECORDED_BASELINE_STATUS: {baseline['status'] if baseline else 'absent'} (reported, not re-derived)")
    print(
        "HONEST_PROOF_TARGET_NON_PROMOTABLE: this cert never lifts the claim to core; external "
        "data only constrain the frozen D0 phason-decoherence passport once pinned"
    )
    if phason is not None:
        print(f"HONEST_PHASON_SUMMARY_STATUS: {phason.get('status', 'unknown')}")

    # ---- results artifact (gitignored runtime output) --------------------------------
    results = {
        "claim": "D0-PASSPORT-ICECUBE-HESE-001",
        "status": verdict,
        "returncode": rc,
        "data_present": data_present,
        "manifest_ready_declared": manifest_ready_declared,
        "manifest_ready_contradicted_by_disk": ready_contradicted,
        "missing_cache_files": missing,
        "sha256_mismatch_files": hash_mismatch,
        "file_report": file_report,
        "recorded_baseline_status": baseline["status"] if baseline else None,
        "recorded_deltas": (
            {"delta_loglik": baseline["delta_loglik"], "delta_chi2": baseline["delta_chi2"]}
            if baseline
            else None
        ),
        "recorded_phason_status": phason.get("status") if phason else None,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    out = Path(__file__).with_suffix(".results.json")
    out.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"results: {out.name}  (exit {rc})")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
