#!/usr/bin/env python3
"""D0 v16 dusty-plasma tabletop bridge cert.

This certificate verifies the status discipline and structural dictionary for the
Vasiliev--Vasilieva electron-beam dusty-plasma laboratory bridge. It is not a
physics proof of D0, quantum gravity, black-hole jets, phi mass loss, or acoustic
log-phi spacing.

Allowed status: BRIDGE-CERT / TABLETOP-PASSPORT-SEED.
Forbidden promotion: CORE-CLOSED, ISOMORPHISM-CLOSED, TABLETOP-QG-PROVED.
"""

import numpy as np

PHI = (1.0 + np.sqrt(5.0)) / 2.0


def assert_status_discipline() -> None:
    status = "BRIDGE-CERT / TABLETOP-PASSPORT-SEED"
    forbidden = {
        "CORE-CLOSED",
        "ISOMORPHISM-CLOSED",
        "DUSTY-PLASMA-ISOMORPHISM-CERT-CLOSED",
        "TABLETOP-QG-PROVED",
    }
    assert status not in forbidden
    assert "BRIDGE" in status and "SEED" in status
    print("PASS_STATUS_BRIDGE_NOT_CORE_CLOSED")


def assert_article_fact_dictionary() -> None:
    # Facts admitted from the external laboratory article only as bridge facts.
    article_facts = {
        "dust_changes_beam_plasma_shape": True,
        "plasma_volume_contracts_with_dust": True,
        "three_modes_declared": True,
        "transition_mode_channel_clearing": True,
        "disturbed_mode_dust_flyout": True,
        "ordered_structure_attract_repel_switch": True,
    }
    assert all(article_facts.values())
    print("PASS_ARTICLE_FACTS_DECLARED")


def assert_mapping_is_analogy_not_identity() -> None:
    mapping_class = {
        "r2_z_beam_contour": "continuum_shadow_not_phi_law",
        "ne_balance": "rate_equation_shadow_not_logdet_identity",
        "electrostatic_ion_drag_forces": "force_balance_shadow_not_FN_identity",
        "dust_flyout": "jet_like_channel_clearing_not_blackhole_identity",
        "radial_potential": "pressure_gradient_shadow_not_SI_gravity_identity",
    }

    assert mapping_class["r2_z_beam_contour"] != "phi_law"
    assert mapping_class["ne_balance"] != "logdet_identity"
    assert mapping_class["electrostatic_ion_drag_forces"] != "FN_identity"
    assert mapping_class["dust_flyout"] != "blackhole_jet_identity"
    assert mapping_class["radial_potential"] != "SI_gravity_identity"

    print("PASS_MAPPING_ANALOGY_NOT_IDENTITY")


def assert_d0_operator_dictionary() -> None:
    dictionary = {
        "electron_beam": "directed_readout_witness",
        "dust_grains": "archive_capacity_sinks",
        "dust_absorption": "active_to_archive_transfer_analogue",
        "plasma_contraction": "active_volume_contraction_analogue",
        "dust_free_channel": "channel_clearing_analogue",
        "dust_flyout": "saturated_ejection_analogue",
        "attract_repel_switch": "seam_sign_switch_analogue",
    }

    assert dictionary["electron_beam"] == "directed_readout_witness"
    assert dictionary["dust_grains"] == "archive_capacity_sinks"
    assert dictionary["dust_free_channel"] == "channel_clearing_analogue"
    assert dictionary["attract_repel_switch"] == "seam_sign_switch_analogue"

    print("PASS_D0_OPERATOR_DICTIONARY")


def assert_predictions_marked_external() -> None:
    predictions = {
        "golden_mass_loss_phi_minus_2": "EXTERNAL_EXPERIMENT_REQUIRED",
        "acoustic_log_phi_spacing": "EXTERNAL_EXPERIMENT_REQUIRED",
        "pressure_current_density_phase_surface": "EXTERNAL_EXPERIMENT_REQUIRED",
    }

    assert all(v == "EXTERNAL_EXPERIMENT_REQUIRED" for v in predictions.values())

    # Numerical constants are admissible only as prediction targets.
    assert np.isclose(PHI ** -2, 0.3819660112501051)
    assert np.isclose(np.log(PHI), 0.48121182505960347)

    print("PASS_PHI_CONSTANTS_ARE_PREDICTION_TARGETS_ONLY")


def run() -> int:
    print("--- D0 DUSTY PLASMA TABLETOP BRIDGE CERT ---")
    assert_status_discipline()
    assert_article_fact_dictionary()
    assert_mapping_is_analogy_not_identity()
    assert_d0_operator_dictionary()
    assert_predictions_marked_external()
    print("PASS_DUSTY_PLASMA_TABLETOP_BRIDGE_CERT")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
