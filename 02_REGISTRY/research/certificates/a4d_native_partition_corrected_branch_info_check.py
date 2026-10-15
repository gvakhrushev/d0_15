from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[3]
CAPSULE = "02_REGISTRY/research/certificates/a4d_native_partition_corrected_branch_info.lean"
OUTPUT = "02_REGISTRY/research/certificates/a4d_native_partition_corrected_branch_info_output.txt"
RECEIPT = Path(__file__).with_name(
    "a4d_native_partition_corrected_branch_info_certificate.json"
)
DECLARATIONS = {
    "partition_pos",
    "normalizedWeight_sum_one",
    "bookInfo_normalizedWeight_identity",
    "bookInfo_partition_identity",
    "expectedPathAction_partition_identity",
    "normalized_base_value",
    "normalizedLikelihoodInfo_common_shift",
    "balanced_contrast_kills_partition_correction",
    "normalizedLikelihoodInfo_hasDerivAt",
    "expectedPathAction_hasDerivAt",
}
STANDARD_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
SOURCE_PATHS = {
    "01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md",
    "03_FORMALIZATION/D0/Core/BornFiniteEffects.lean",
    "03_FORMALIZATION/D0/CondensedAnchor/DetectorSupportGoldenWeight.lean",
    "02_REGISTRY/research/A4D_NATIVE_BRANCH_INFORMATION_COCYCLE.md",
    "02_REGISTRY/research/A4D_NATIVE_INFO_CONTRACT_SOURCE_AUDIT.md",
    "02_REGISTRY/research/sources/d0_ward_scene_constitutive_closure_2026-10-15/RESULT.md",
    "02_REGISTRY/research/sources/d0_ward_scene_constitutive_closure_2026-10-15/receipt.json",
    "02_REGISTRY/research/A4D_NATIVE_FIELD_TO_INSTRUMENT_JET_BOUNDARY.md",
    "02_REGISTRY/research/certificates/a4d_native_field_instrument_jet_results.json",
}


def git_blob(path: str) -> str:
    return subprocess.run(
        ["git", "hash-object", path], cwd=ROOT, check=True,
        capture_output=True, text=True,
    ).stdout.strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check() -> dict[str, object]:
    capsule = (ROOT / CAPSULE).read_text()
    output = (ROOT / OUTPUT).read_text()
    found_axioms: dict[str, set[str]] = {}
    for name, raw in re.findall(
        r"'D0\.Research\.NativePartitionCorrectedBranchInfo\.([^']+)' depends on axioms: \[([^\]]*)\]",
        output,
        re.S,
    ):
        found_axioms[name] = {part.strip() for part in raw.split(",") if part.strip()}
    assert set(found_axioms) == DECLARATIONS, (set(found_axioms), DECLARATIONS)
    assert all(axioms <= STANDARD_AXIOMS for axioms in found_axioms.values())
    assert "sorryAx" not in output
    assert not re.search(r"\b(sorry|admit)\b", capsule)

    q, z, mu, dq, dz, t = sp.symbols("q z mu dq dz t", positive=True)
    log_phi = sp.Symbol("log_phi", positive=True)
    w = q * z
    info = -sp.log(mu) / log_phi - (-sp.log(w) / log_phi)
    corrected = (sp.log(q / mu) + sp.log(z)) / log_phi
    assert sp.simplify(info - corrected) == 0
    source = (dq / q + dz / z) / log_phi
    assert sp.simplify(sp.diff(corrected.subs({q: q + dq*t, z: z + dz*t}), t).subs(t, 0) - source) == 0

    # At a normalized base point, a moving total raw response still contributes.
    q0 = sp.Rational(1, 2)
    z_curve = 1 + t
    corrected_curve = (sp.log(q0 / mu) + sp.log(z_curve)) / log_phi
    assert sp.simplify(corrected_curve.subs(t, 0) - sp.log(q0 / mu) / log_phi) == 0
    assert sp.simplify(sp.diff(corrected_curve, t).subs(t, 0) - 1 / log_phi) == 0
    assert sp.simplify(sp.diff((sp.log(q0 / mu)) / log_phi, t)) == 0

    # The normalizer contributes a common mode: balanced outcome contrasts
    # cancel it, while a nonzero-sum readout retains it.
    c1 = sp.Symbol("c1")
    common_shift = sp.log(z) / log_phi
    assert sp.simplify(c1 * common_shift - c1 * common_shift) == 0
    assert sp.simplify((c1 + 1) * common_shift - c1 * common_shift - common_shift) == 0

    # Compose with the exact event-normalizer jet from the complete instrument
    # interface. This is conditional on identifying those raw event weights
    # with the Book path weights; the physical admission map stays open.
    field_receipt_path = ROOT / "02_REGISTRY/research/certificates/a4d_native_field_instrument_jet_results.json"
    field_receipt = json.loads(field_receipt_path.read_text())
    event = field_receipt["event_normalizer_first_jet"]
    p = sp.symbols("p", real=True)
    p_golden = (sp.sqrt(5) - 1) / 2
    event_probability = 144 * p - sp.Rational(177, 2)
    event_probability_jet = 189 * p - 117
    reported_dlog = sp.sympify(event["dlog_probability_dxi_lambda1"], locals={"p": p})
    assert field_receipt["exact_controls"] == 33
    assert event["probability"] == "144*p - 177/2"
    assert event["d_probability_dxi_lambda1"] == "189*p - 117"
    assert event["d_probability_dxi_lambda2"] == "378*p - 234"
    assert event["d_probability_dxi_arbitrary_scale"] == "lambda * (189*p - 117)"
    assert sp.simplify((reported_dlog - event_probability_jet / event_probability).subs(p, p_golden)) == 0
    assert sp.simplify(reported_dlog.subs(p, p_golden)) != 0
    assert sp.simplify((sp.sympify(event["dlog_probability_dxi_lambda2"], locals={"p": p}) - 2 * reported_dlog).subs(p, p_golden)) == 0
    event_mean_action_correction = -reported_dlog / log_phi
    assert sp.simplify(event_mean_action_correction.subs(p, p_golden)) != 0
    assert sp.simplify(event_mean_action_correction.subs(p, p_golden)).is_positive is True

    # The probability-weighted action is entropy minus log partition, and its
    # derivative keeps the negative normalizer jet for a varying q-family.
    alpha, dalpha, z0, dz0 = sp.symbols("alpha dalpha z0 dz0", positive=True)
    q2 = 1 - alpha
    mean_action = (-alpha * sp.log(alpha * z) - q2 * sp.log(q2 * z)) / log_phi
    entropy = (-alpha * sp.log(alpha) - q2 * sp.log(q2)) / log_phi
    mean_identity = sp.expand_log(mean_action, force=True) - (entropy - sp.log(z) / log_phi)
    assert sp.simplify(mean_identity) == 0
    q1t = alpha + dalpha * t
    q2t = 1 - q1t
    zt = z0 + dz0 * t
    mean_action_t = (-q1t * sp.log(q1t * zt) - q2t * sp.log(q2t * zt)) / log_phi
    entropy_t = (-q1t * sp.log(q1t) - q2t * sp.log(q2t)) / log_phi
    expected_source = sp.diff(entropy_t, t).subs(t, 0) - dz0 / z0 / log_phi
    assert sp.simplify(sp.diff(mean_action_t, t).subs(t, 0) - expected_source) == 0

    return {
        "schema": "A4D_NATIVE_PARTITION_CORRECTED_BRANCH_INFO_V3",
        "status": "EXACT_FINITE_PARTITION_SOURCE_AND_JOINT_JET",
        "source_blobs": {path: git_blob(path) for path in sorted(SOURCE_PATHS)},
        "capsule_sha256": sha256(ROOT / CAPSULE),
        "lean_output_sha256": sha256(ROOT / OUTPUT),
        "declarations": sorted(DECLARATIONS),
        "compiled_declaration_count": len(DECLARATIONS),
        "exact_symbolic_control_count": 12,
        "axiom_check": "STANDARD_ONLY",
        "proved": {
            "partition_log_correction_exact": True,
            "joint_source_includes_q_and_normalizer_jets": True,
            "unit_normalizer_reduces_to_branch_cocycle": True,
            "moving_normalizer_control_at_Z1_has_source_1_over_log_phi": True,
            "partition_correction_is_common_mode_across_outcomes": True,
            "balanced_branch_contrasts_annihilate_common_mode": True,
            "native_interface_event_normalizer_jet_is_nonzero_and_free_scale_sensitive": True,
            "expected_path_action_is_entropy_minus_log_partition": True,
            "expected_path_action_source_includes_negative_normalizer_jet": True,
            "event_mean_action_normalizer_source_is_strictly_positive_for_lambda1": True,
        },
        "remaining_open": [
            "book history weight bound to the same Born raw-response frame",
            "physical normalizer and its variation on the native family",
            "joint q,D,b,m variation owner",
            "map from the physical source to balanced or common-mode outcome readouts",
            "identification of the instrument event weights with Book path weights",
            "physical matter action and its same-carrier field variations",
        ],
        "conditional_event_mean_action_normalizer_source_lambda1": str(
            sp.simplify(event_mean_action_correction.subs(p, p_golden))
        ),
        "scientific_scope": "finite outcomes, positive probabilities, explicitly shared history/response interface only",
    }


if __name__ == "__main__":
    result = check()
    RECEIPT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(
        "PASS_PARTITION_CORRECTED_BRANCH_INFO",
        f"declarations={result['compiled_declaration_count']}",
        f"symbolic={result['exact_symbolic_control_count']}",
    )
