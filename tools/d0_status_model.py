#!/usr/bin/env python3
"""Shared D0 status model: the single source for the canonical release-status
enum, its collapse map, the mapping onto the Lean D0Status firewall, and the
track-fair scoring ladder.

Imported by validate_csv.py, check_firewall.py and d0_score.py so the guards and
the scorer never drift from each other. Mirrors
09_LEAN_FORMALIZATION/D0/Traceability/StatusTaxonomy.lean (D0Status + canPromoteTo).
"""
from __future__ import annotations

# --- Canonical release_status enum (Phase 3 collapses all drift into these 12) ---
CANONICAL_RELEASE_STATUS: set[str] = {
    "CORE-FORMALIZED",
    "CERT-CLOSED",
    "NO_GO_PROVED",
    "NO-GO",
    "BRIDGE-ASSUMPTIONS-EXPLICIT",
    "CORE_BRIDGE_SPLIT",
    "BRIDGE-CALIBRATION",
    "EMPIRICAL-PASSPORT",
    "EXTERNAL-BACKGROUND",
    "PROOF-TARGET",
    "DEPRECATED",
    "OPEN",
}

# Collapse map: drifted/descriptive release_status -> canonical member.
# Descriptive specificity (e.g. EDGE-ALPHA-TRACE-...) moves to the notes column.
RELEASE_STATUS_COLLAPSE: dict[str, str] = {
    "BRIDGE-ASSUMPTION": "BRIDGE-ASSUMPTIONS-EXPLICIT",
    "PROOF-OBLIGATION-EXPOSED": "PROOF-TARGET",
    "THEOREM-TARGET-SHARPENED": "PROOF-TARGET",
    "CERT-CANDIDATE": "PROOF-TARGET",
    "EMPIRICAL-PASSPORT-CANDIDATE": "PROOF-TARGET",
    "LOWER-BOUND-TARGET": "PROOF-TARGET",
    "CONDITIONAL-THEOREM-TARGET": "PROOF-TARGET",
    "METROLOGY-PREDICTION-TARGET": "PROOF-TARGET",
    "HORIZON-JET-OBSERVABLE-CERT-SCAFFOLD": "PROOF-TARGET",
    "OPERATOR-SCAFFOLD-CERTIFIED": "CERT-CLOSED",
    "SPIN-FLAVOUR-TRANSFER-CERTIFIED": "CERT-CLOSED",
    "OPERATOR-LAW-CLOSED": "CERT-CLOSED",
    "OPERATOR-LEMMA-CERT": "CERT-CLOSED",
    "CERT-SCAFFOLD-CLOSED": "CERT-CLOSED",
    "EDGE-ALPHA-TRACE-CERT-CLOSED": "CERT-CLOSED",
    "RAMIFICATION-COMPANION-COVER-CERT-CLOSED": "CERT-CLOSED",
    "BARYON-ANONYMOUS-POLE-CERT-CLOSED": "CERT-CLOSED",
    "FRACTAL-CONTINUUM-PREDICTION-CERT-CLOSED": "CERT-CLOSED",
    "RELATIVE-ARCHIVE-ACCELERATION-CERT-CLOSED": "CERT-CLOSED",
    "RELATIVE-PRESSURE-BRIDGE-LAW-CERT-CLOSED": "CERT-CLOSED",
    "LOGDET-PRESSURE-COUPLING-CERT-CLOSED": "CERT-CLOSED",
    "LOGDET-SECOND-RESPONSE-STABILITY-CERT-CLOSED": "CERT-CLOSED",
    # D0-PUB-001 publication-structure meta row; Phase 3 reviews it explicitly.
    "PUBLICATION-MONOGRAPH-STRUCTURE": "EXTERNAL-BACKGROUND",
}


def canonical_release(status: str) -> str:
    s = (status or "").strip()
    return RELEASE_STATUS_COLLAPSE.get(s, s)


VALID_LEAN_STATUS: set[str] = {
    "LEAN_PROVED",
    "LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS",
    "PYTHON_CERTIFIED",
    "OPEN",
    "DEPRECATED",
    "",
}

# --- Lean D0Status firewall (mirror StatusTaxonomy.lean) ---
# canonical release_status -> D0Status (None = pre-closure, not a closure status)
RELEASE_TO_D0STATUS: dict[str, str | None] = {
    "CORE-FORMALIZED": "CORE_CLOSED",
    "CERT-CLOSED": "CERT_CLOSED",
    "NO_GO_PROVED": "NO_GO",
    "NO-GO": "NO_GO",
    "BRIDGE-ASSUMPTIONS-EXPLICIT": "BRIDGE_CALIBRATION",
    "CORE_BRIDGE_SPLIT": "BRIDGE_CALIBRATION",
    "BRIDGE-CALIBRATION": "BRIDGE_CALIBRATION",
    "EMPIRICAL-PASSPORT": "EMPIRICAL_PASSPORT",
    "EXTERNAL-BACKGROUND": "EXTERNAL_DATA_REQUIRED",
    "PROOF-TARGET": None,
    "OPEN": None,
    "DEPRECATED": None,
}

# canPromoteTo(s, CORE_CLOSED) = False for these (StatusTaxonomy.lean lines 12-17).
FORBIDDEN_PROMOTIONS_TO_CORE: set[str] = {
    "EMPIRICAL_PASSPORT",
    "EXTERNAL_DATA_REQUIRED",
    "BRIDGE_CALIBRATION",
}


def can_promote_to_core(d0status: str | None) -> bool:
    return d0status not in FORBIDDEN_PROMOTIONS_TO_CORE


# --- Track-fair scoring ladder (cumulative, increasing increments 1,1,2,3,5,8) ---
# Core spine L0..L5 cumulative score.
SPINE_CUMULATIVE = {0: 1, 1: 2, 2: 4, 3: 7, 4: 12, 5: 20}
SPINE_LEVEL_NAMES = {
    0: "UNTRACKED",
    1: "HYP",
    2: "CERT_SCAFFOLD",
    3: "PYTHON_CERTIFIED",
    4: "LEAN_PROVED",
    5: "CORE_FORMALIZED",
}
# Lateral terminal-track per-claim ceilings (firewall in points).
TRACK_CEILING = {
    "CORE": 20,
    "NO_GO": 12,
    "BRIDGE": 11,
    "PASSPORT": 7,
    "EXTERNAL": 2,
    "DEPRECATED": 0,
}

# --- Repository hygiene / refactor KPI (Iteration 2; second, independent axis) ---
# A 100-point budget scored from deterministic git+guard facts. Penalties subtract
# (each capped so one signal can't dominate), bonuses add back, result clamped to
# [0, budget]. Adding tracked junk / fake proofs / book-trash LOWERS the score;
# deleting them RAISES it — so cleanup is itself a tracked KPI next to theory
# strength. Every signal names the offending files, so the output is a worklist.
HYGIENE_BUDGET = 100
# name: (unit_penalty, max_penalty, human_label)
HYGIENE_PENALTIES: dict[str, tuple[float, float, str]] = {
    "tracked_meta_trash":   (0.3, 20.0, "tracked files under add/ + _QUARANTINE/v17_overshoots/ (vendored input, not release)"),
    "tracked_but_ignored":  (1.0, 8.0,  "tracked-but-gitignored files (scratch that should not ship)"),
    "tautology_proofs":     (1.5, 18.0, "Lean (h:stmt):stmt:=h tautologies marked leanCoreProved (prove nothing)"),
    "proof_debt":           (2.0, 10.0, "sorry/axiom inside the built D0/ tree"),
    "phantom_certs":        (3.0, 12.0, "vp_*.py cited in books but absent on disk and not OPEN/PROOF-TARGET"),
    "orphan_proof_targets": (0.1, 10.0, "PROOF-TARGET markers in book prose with no registry row"),
    "dev_comments":         (1.0, 8.0,  "developer '# ...' TODO/notes left in book prose"),
    "path_leaks":           (0.05, 12.0, "internal repo paths / vp_*.py / D0.* module names dumped in book prose"),
    "corpus_errors":        (1.0, 10.0, "check_v14_clean_corpus violations (duplicate headings, version logs)"),
    "real_in_project_lake": (5.0, 10.0, "a real .lake build tree inside the repo (must be an external junction)"),
}
# name: (unit_bonus, max_bonus, human_label)
HYGIENE_BONUSES: dict[str, tuple[float, float, str]] = {
    "files_deleted_vs_base": (0.1, 10.0, "net files removed vs base-v14 (rewards shrinking the publish tree)"),
}
