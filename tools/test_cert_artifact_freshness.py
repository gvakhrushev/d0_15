#!/usr/bin/env python3
"""Mutation and semantic regressions for immutable certificate artifacts."""
from __future__ import annotations

import csv
import importlib
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERTIFICATES = ROOT / "04_CERTIFICATES"
sys.path.insert(0, str(CERTIFICATES))


def check_json_numeric_contract() -> None:
    import cert_runtime

    with tempfile.TemporaryDirectory(prefix="d0-json-freshness-") as temp:
        artifact = Path(temp) / "probe.json"
        artifact.write_text(
            json.dumps({"value": 1.0, "label": "fixed", "items": [1, True]}) + "\n",
            encoding="utf-8",
        )
        cert_runtime.assert_json_artifact_matches(
            artifact, {"value": 1.0 + 5.0e-13, "label": "fixed", "items": [1, True]}
        )
        try:
            cert_runtime.assert_json_artifact_matches(
                artifact, {"value": 1.0 + 1.0e-6, "label": "fixed", "items": [1, True]}
            )
        except AssertionError:
            pass
        else:
            raise AssertionError("meaningful numeric artifact drift was accepted")
    print("PASS_JSON_ARTIFACT_NUMERIC_CONTRACT")


def check_stale_artifacts_fail() -> None:
    import cert_runtime

    cases = (
        ("vp_d0_redshift_drift_direct", "VERDICT", None),
        ("vp_feedback_partition_function", "PASSPORT", "ROOT"),
        ("vp_redshift_drift_expansion_coupled", "VERDICT", None),
    )
    with tempfile.TemporaryDirectory(prefix="d0-cert-freshness-") as temp:
        temp_root = Path(temp)
        old_runtime_root = cert_runtime.ROOT
        try:
            for module_name, target_name, runtime_root_name in cases:
                module = importlib.import_module(module_name)
                artifact_dir = temp_root / module_name
                artifact_dir.mkdir(parents=True)
                artifact_name = (
                    "feedback_partition_function_summary.json"
                    if target_name == "PASSPORT"
                    else Path(getattr(module, target_name)).name
                )
                artifact = artifact_dir / artifact_name
                stale = '{"stale": true}\n'
                artifact.write_text(stale, encoding="utf-8")
                original_target = getattr(module, target_name)
                setattr(module, target_name, artifact_dir if target_name == "PASSPORT" else artifact)
                if runtime_root_name:
                    cert_runtime.ROOT = temp_root
                try:
                    try:
                        if module_name == "vp_redshift_drift_expansion_coupled" and not (
                            module.ROOT
                            / "05_EXPERIMENTS/_EXTERNAL_DATA_CACHE/desi_bao/desi_gaussian_bao_ALL_GCcomb_mean.txt"
                        ).is_file():
                            module.assert_json_artifact_matches(artifact, {"computed": True})
                        else:
                            module.main()
                    except AssertionError as error:
                        assert "tracked canonical artifact" in str(error)
                    else:
                        raise AssertionError(f"{module_name} accepted a stale artifact")
                    assert artifact.read_text(encoding="utf-8") == stale
                    print(f"PASS_MUTATION_STALE_ARTIFACT_REJECTED {module_name}")
                finally:
                    setattr(module, target_name, original_target)
                    cert_runtime.ROOT = old_runtime_root
        finally:
            cert_runtime.ROOT = old_runtime_root


def check_gravity_core_semantics() -> None:
    claim_rows = {
        row["claim_id"]: row
        for row in csv.DictReader(
            (ROOT / "02_REGISTRY/claims.csv").open(encoding="utf-8", newline="")
        )
    }
    expected_anchors = {
        "D0-TYPED-ROLE-OPPOSITE-CUT-WELD-001": "not a physical-dynamics selection",
        "D0-DIAGONAL-ROLE-HODGE-SYMMETRY-001": "commutes with d, d dagger, D_H, and D_H squared",
        "D0-HODGE-GRADING-SYMMETRY-001": "occupation is not a symmetry of D_H",
        "D0-SPATIAL-HODGE-SHELL-OPERATOR-001": "not the BOOK finite feedback operator",
        "D0-MOVING-GRADED-DIFFERENTIAL-001": "No analytic exponential and no physical action are used",
        "D0-PRIMAL-DUAL-MOVING-ACTION-001": "not a constitutive selector",
        "D0-PATH-HODGE-STABILIZER-001": "No constitutive kernel is selected",
        "D0-MOVING-D-PARENT-WARD-001": "does not conclude divergence-free stress",
        "D0-RADIUS-ONE-WARD-KERNEL-001": "not local Lorentz covariance",
        "D0-CONSTITUTIVE-KERNEL-FAMILY-001": "no alpha is selected",
        "D0-CONSTITUTIVE-HOLONOMY-COMPATIBILITY-001": "This does not select a connection",
        "D0-AFFINE-CARTAN-PATH-CLOSURE-001": "No physical Hodge kernel or constitutive action is selected",
    }
    for claim_id, anchor in expected_anchors.items():
        row = claim_rows[claim_id]
        assert row["lean_status"] == "LEAN_PROVED", claim_id
        assert row["release_status"] == "CORE-FORMALIZED", claim_id
        assert not row["python_cert"].strip(), f"CORE owner unexpectedly cert-backed: {claim_id}"
        assert anchor in row["notes"], f"semantic boundary changed for {claim_id}: {anchor}"

    rules = json.loads(
        (ROOT / "02_REGISTRY/claim_strength_rules.json").read_text(encoding="utf-8")
    )
    by_id = {rule["id"]: rule for rule in rules["rules"]}
    shell_rule = by_id["shell-compression-is-book-feedback"]
    assert "spatialShellFluxCompression" in shell_rule["pattern"]
    assert "BOOK finite feedback operator F_N" in shell_rule["message"]
    reverse_rule = by_id["reverse-star-negates-located-j"]
    assert "located two-color J" in reverse_rule["message"]
    print(f"PASS_GRAVITY_CORE_SEMANTICS_PROTECTED claims={len(expected_anchors)}")


if __name__ == "__main__":
    check_json_numeric_contract()
    check_stale_artifacts_fail()
    check_gravity_core_semantics()
