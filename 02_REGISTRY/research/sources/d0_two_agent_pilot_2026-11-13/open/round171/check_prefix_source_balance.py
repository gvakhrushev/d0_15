"""Check conditional score transport on a full stopped tree and the B170 sampler."""

from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
import json
import runpy


SOURCE = Path(__file__).resolve().parents[1] / "round170/check_golden_mask_reference.py"


def require(condition, context):
    if not condition:
        raise ArithmeticError(context)


def check_prefix_identity():
    # Synthetic rational masses for the general identity. A leaf is terminal
    # exactly at its given address. Positive masses have the same support.
    leaves = {
        "00": (F(1, 7), F(2, 17), F(1, 23)),
        "01": (F(2, 7), F(1, 17), -F(2, 23)),
        "100": (F(1, 7), F(4, 17), F(3, 23)),
        "101": (F(1, 7), F(1, 17), -F(1, 23)),
        "11": (F(2, 7), F(9, 17), -F(1, 23)),
    }
    values = defaultdict(lambda: (F(0), F(0), F(0)))
    for word, row in leaves.items():
        for length in range(len(word) + 1):
            h = word[:length]
            values[h] = tuple(a + b for a, b in zip(values[h], row))
    require(values[""] == (1, 1, 0), "normalized absolute root shape")
    direct = sum(t * dq / q for q, t, dq in leaves.values())
    full_fisher = sum(dq**2 / q for q, _, dq in leaves.values())
    local, conditional_fisher = F(0), F(0)
    edge_contributions = []
    for prefix, (mass_q, mass_t, derivative) in sorted(values.items()):
        if prefix in leaves:
            continue
        stage = F(0)
        stage_fisher = F(0)
        for bit in "01":
            if prefix + bit not in values:
                continue
            next_q, next_t, next_dq = values[prefix + bit]
            q_bit = next_q / mass_q
            t_bit = next_t / mass_t
            score = next_dq / next_q - derivative / mass_q
            stage += mass_t * (t_bit - q_bit) * score
            stage_fisher += mass_q * q_bit * score**2
        local += stage
        conditional_fisher += stage_fisher
        edge_contributions.append([prefix, str(stage)])
    require(local == direct, "transport splits into visited parent scores")
    require(conditional_fisher == full_fisher, "exact conditional Fisher sum")
    return {
        "positive_terminal_addresses": list(leaves),
        "edge_score_terms": edge_contributions,
        "full_tilted_score": str(direct),
        "full_graph_fisher": str(full_fisher),
    }


def check_b170_reference():
    owner = runpy.run_path(str(SOURCE))
    target = owner["efficiency"](4)
    leaves = owner["golden_sampler"](target)
    sizes = [owner["code_length"](leaf.word) for leaf in leaves]
    require((min(sizes), max(sizes)) == (2, 16), "actual sparse Golden archive")
    count = len(leaves)
    fail_count = sum(leaf.mark == 0 for leaf in leaves)
    require((count, fail_count) == (13, 9), "actual one-cycle file")
    rows = []
    for n in (1, 2, 3, 17):
        count_0 = count**n
        count_1 = 2 * count_0 - fail_count**n
        # Mathematical calibration of the incoming old two-sector masses.
        # Born mixture q and the literal event-price example are held apart.
        q = F(1, 2)
        tilted_entry = q * count_1 / ((1 - q) * count_0 + q * count_1)
        root_score = tilted_entry / q - (1 - tilted_entry) / (1 - q)
        require(root_score == F(2 * (count_1 - count_0), count_1 + count_0),
                "only the arrival score is nonzero")
        require(0 < root_score < F(2, 3), "uniform source bound for the count model")
        if n == 1:
            require(root_score == F(4, 15), "one real sampler exact tilt")
        rows.append({
            "cycles": n,
            "selected_price_times_log_base_source_gap": str(-root_score),
            "full_defect_range_in_units_log_phi_at_least": (max(sizes) - min(sizes)) * n,
        })
    return rows


def main():
    print(json.dumps({
        "status": "PASS",
        "full_stopped_tree": check_prefix_identity(),
        "actual_B170_archives_under_declared_conditional_price": check_b170_reference(),
        "physical_price_identified": False,
        "GR_closed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
