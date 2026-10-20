"""Replay the AF coupling comparison and reject a forged identification."""

from check_af_cost_info_coupling import run


def main() -> None:
    receipt = run()
    assert receipt["status"] == "PASS"
    assert receipt["coupling_holds"] is False
    assert receipt["sources_coincide"] is False
    assert receipt["gr_derived"] is False
    assert receipt["equation_20_closed"] is False
    assert receipt["constant_chosen_to_match_einstein"] is False
    assert receipt["mixed_length_operator_identity_checked"] is False
    assert receipt["observer_argument_present"] is False
    assert receipt["matter_argument_present"] is False
    assert receipt["blank_volume_law_cancels"] is False
    assert receipt["check_count"] >= 49
    assert receipt["lapse_einstein_contraction"] == "-2/(N*a**2)"
    assert "epsilon" in receipt["shift_einstein_contraction"]
    print(f"PASS {receipt['check_count']} {receipt['coupling_holds']}")


if __name__ == "__main__":
    main()
