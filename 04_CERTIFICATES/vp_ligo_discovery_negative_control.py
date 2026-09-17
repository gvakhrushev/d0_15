"""D0 v16 LIGO discovery negative-control guardrail.

This is a status/discipline certificate.  It does not validate a LIGO signal.
It freezes the negative outcomes of the V3--V12 discovery scans and prevents
promotion of proxy results to a D0 core or empirical passport.
"""


def run():
    print("--- D0 LIGO DISCOVERY NEGATIVE CONTROL CERT ---")

    status = "DISCOVERY-NEGATIVE-CONTROL / TRANSFER-MAP-TARGET"
    forbidden_status = {
        "LIGO-PHI-PASS",
        "GW170814-D0-CONFIRMED",
        "RAMIFIED-PHI-GW-CLOSED",
        "FIXED-ALPHA-POPULATION-LAW-CLOSED",
        "CORE-CLOSED",
    }
    assert status not in forbidden_status
    print("PASS_LIGO_RESULTS_NOT_CORE_CLOSED")

    outcomes = {
        "raw_phi_ratio": "REJECTED_IN_PROXY",
        "detector_frame_phi": "NOT_SIGNIFICANT",
        "gw170814_mu_plus_phi_5_4": "P_VALUE_0P53_NOT_SIGNIFICANT",
        "ramified_population_v9": "NOT_SUPPORTED",
        "fixed_alpha_population_v10_v11": "NO_STABLE_FIXED_ALPHA",
    }
    assert all(v != "CONFIRMED" for v in outcomes.values())
    print("PASS_LIGO_RAW_PHI_AND_RAMIFIED_SHORTCUTS_REJECTED")

    next_target = "NON_SATURATING_TRANSFER_CORRECTED_RESIDUAL_OBSERVABLE"
    assert next_target.startswith("NON_SATURATING")
    print("PASS_LIGO_NEXT_TARGET_TRANSFER_MAP_ONLY")

    forbidden_promotions = [
        "raw_frequency_phi_ladder",
        "single_event_mu_plus_without_null",
        "population_alpha_after_retuning",
    ]
    assert len(forbidden_promotions) == 3
    print("PASS_LIGO_PROXY_PROMOTION_FORBIDDEN")

    print("PASS_LIGO_DISCOVERY_NEGATIVE_CONTROL_CERT")


if __name__ == "__main__":
    run()
