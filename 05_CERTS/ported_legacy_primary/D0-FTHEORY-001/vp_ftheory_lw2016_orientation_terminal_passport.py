#!/usr/bin/env python3
"""Orientation and terminal-lift passport for Lin-Weigand 2016.

This certificate consumes the already generated D0/LW2016 layers:

- D0_FTHEORY_LW2016_D0_FILTER_NUMBERS.json
- D0_FTHEORY_LW2016_CHIRAL_RECOMBINATION_NUMBERS.json
- D0_FTHEORY_LW2016_INTERSECTION_RECOMPUTE_NUMBERS.json

It closes two defects left open by the intersection recompute layer:

1. orientation_sign_passport, via sign(chi_R)=sign(B-L)_R;
2. F_terminal, via the 1(6) lifting sector with chi=-ABCD=-4.

No D0 parameter is fitted here.  The only remaining open defect after this
passport is F_scale.
"""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
D0_FILTER_JSON = ROOT / "D0_FTHEORY_LW2016_D0_FILTER_NUMBERS.json"
RECOMBINATION_JSON = ROOT / "D0_FTHEORY_LW2016_CHIRAL_RECOMBINATION_NUMBERS.json"
INTERSECTION_JSON = ROOT / "D0_FTHEORY_LW2016_INTERSECTION_RECOMPUTE_NUMBERS.json"
OUT_JSON = ROOT / "D0_FTHEORY_LW2016_ORIENTATION_TERMINAL_NUMBERS.json"
OUT_REPORT = ROOT / "D0_FTHEORY_LW2016_ORIENTATION_TERMINAL_RESULTS.md"

D0_GENERATIONS = 3
D0_LIGHT_GAUGE_RANK = 4
D0_READOUT_ROLES = 4
D0_TERMINAL_SINGLET_CHI = -D0_READOUT_ROLES

B_MINUS_L = {
    "Q": Fraction(1, 3),
    "u^c": Fraction(-1, 3),
    "d^c": Fraction(-1, 3),
    "L+Hu+Hd": Fraction(-1, 1),
    "e^c": Fraction(1, 1),
}


def sign(value: int | Fraction) -> int:
    if value > 0:
        return 1
    if value < 0:
        return -1
    return 0


def sign_label(value: int) -> str:
    return "+" if value > 0 else "-" if value < 0 else "0"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def result_by_name(d0_filter: dict[str, Any], needle: str) -> dict[str, Any]:
    for result in d0_filter["results"]:
        if needle in result["name"]:
            return result
    raise KeyError(f"No D0 filter result matching {needle!r}")


def orientation_passport(grouped_chi: dict[str, int]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    defects: dict[str, int] = {}
    generation_defects: dict[str, int] = {}
    pattern: dict[str, str] = {}
    for rep, b_minus_l in B_MINUS_L.items():
        chi = int(grouped_chi[rep])
        chi_sign = sign(chi)
        bml_sign = sign(b_minus_l)
        defect = chi_sign - bml_sign
        gen_defect = abs(chi) - D0_GENERATIONS
        defects[rep] = defect
        generation_defects[rep] = gen_defect
        pattern[rep] = sign_label(chi_sign)
        rows.append(
            {
                "field": rep,
                "chi": chi,
                "sign_chi": chi_sign,
                "B_minus_L": str(b_minus_l),
                "sign_B_minus_L": bml_sign,
                "defect": defect,
                "generation_defect": gen_defect,
            }
        )

    if any(value != 0 for value in defects.values()):
        raise AssertionError(f"Orientation defects remain: {defects}")
    if any(value != 0 for value in generation_defects.values()):
        raise AssertionError(f"Generation defects remain: {generation_defects}")

    return {
        "F_orientation": 0,
        "rule": "sign(chi_R)=sign(B-L)_R",
        "pattern": pattern,
        "defects": defects,
        "generation_defects": generation_defects,
        "rows": rows,
    }


def terminal_lift_passport(
    grouped_chi: dict[str, int],
    published_before: dict[str, Any],
    after_lifting: dict[str, Any],
) -> dict[str, Any]:
    terminal_chi = int(grouped_chi["u1_lifting_vev_sector"])
    conditions = {
        "surplus_rank_before_lifting": published_before["F_rank"] == 1,
        "exotics_before_lifting": published_before["F_exotic"] > 0,
        "terminal_singlet_chi": terminal_chi == D0_TERMINAL_SINGLET_CHI,
        "rank_closed_after_lifting": after_lifting["F_rank"] == 0,
        "exotics_closed_after_lifting": after_lifting["F_exotic"] == 0,
    }
    if not all(conditions.values()):
        raise AssertionError(f"Terminal-lift conditions failed: {conditions}")
    return {
        "F_terminal": 0,
        "sector": "1(6)",
        "grouped_sector_name": "u1_lifting_vev_sector",
        "chi": terminal_chi,
        "rule": "chi(1(6))=-ABCD and lifting closes F_rank,F_exotic",
        "conditions": conditions,
        "condition_rows": [
            {"condition": key, "value": value, "pass": bool(value)}
            for key, value in conditions.items()
        ],
    }


def run_vp_ftheory_lw2016_orientation_terminal_passport() -> dict[str, Any]:
    d0_filter = load_json(D0_FILTER_JSON)
    recombination = load_json(RECOMBINATION_JSON)
    intersection = load_json(INTERSECTION_JSON)

    if d0_filter["status"] != "PASS_FTHEORY_LW2016_D0_FILTER":
        raise AssertionError(f"Unexpected D0 filter status: {d0_filter['status']}")
    if recombination["status"] != "PASS_FTHEORY_LW2016_CHIRAL_RECOMBINATION_LAYER":
        raise AssertionError(f"Unexpected recombination status: {recombination['status']}")
    if intersection["status"] != "PASS_FTHEORY_LW2016_INTERSECTION_RECOMPUTE":
        raise AssertionError(f"Unexpected intersection status: {intersection['status']}")
    if recombination["grouped_chi"] != intersection["grouped_chi"]:
        raise AssertionError("Grouped chiral ledgers disagree between recombination and intersection layers.")

    grouped_chi = {key: int(value) for key, value in intersection["grouped_chi"].items()}
    published_before = result_by_name(d0_filter, "before lifting")
    after_lifting = result_by_name(d0_filter, "after U(1)' lift")

    orientation = orientation_passport(grouped_chi)
    terminal = terminal_lift_passport(grouped_chi, published_before, after_lifting)

    known_defects = {
        "F_omega": after_lifting["F_omega"],
        "F_rank": after_lifting["F_rank"],
        "F_chi_abs": 0 if all(v == 0 for v in after_lifting["F_chi_abs"].values()) else after_lifting["F_chi_abs"],
        "F_orientation": orientation["F_orientation"],
        "F_exotic": after_lifting["F_exotic"],
        "F_terminal": terminal["F_terminal"],
        "F_scale": after_lifting["F_scale"],
    }

    if known_defects["F_scale"] is not None:
        raise AssertionError("This passport must leave F_scale open, not silently close it.")
    non_scale = {key: value for key, value in known_defects.items() if key != "F_scale"}
    if any(value != 0 for value in non_scale.values()):
        raise AssertionError(f"Known non-scale defects remain: {non_scale}")

    return {
        "status": "PASS_FTHEORY_LW2016_ORIENTATION_TERMINAL_PASSPORT",
        "inputs": {
            "d0_filter": str(D0_FILTER_JSON.relative_to(ROOT)),
            "chiral_recombination": str(RECOMBINATION_JSON.relative_to(ROOT)),
            "intersection_recompute": str(INTERSECTION_JSON.relative_to(ROOT)),
        },
        "constants": {
            "D0_GENERATIONS": D0_GENERATIONS,
            "D0_LIGHT_GAUGE_RANK": D0_LIGHT_GAUGE_RANK,
            "D0_READOUT_ROLES": D0_READOUT_ROLES,
            "D0_TERMINAL_SINGLET_CHI": D0_TERMINAL_SINGLET_CHI,
        },
        "grouped_chi": grouped_chi,
        "orientation": orientation,
        "terminal": terminal,
        "known_defects_after_orientation_terminal": known_defects,
        "decision": {
            "before_lifting": published_before["status"],
            "after_lifting_before_passport": after_lifting["status"],
            "after_orientation_terminal": "D0_CANDIDATE_SCALE_OPEN",
            "only_remaining_defect": "F_scale",
            "hidden_fit": False,
        },
        "guardrails": [
            "B-L orientation is a fixed left-chiral SM passport, not a fitted D0 parameter.",
            "The terminal rule uses the already recomputed chi(1(6))=-4 and the already verified rank/exotic closure after lifting.",
            "F_scale is deliberately not closed by this certificate.",
        ],
    }


def _write_report(result: dict[str, Any]) -> None:
    lines = [
        "# D0 F-theory Lin-Weigand 2016 Orientation/Terminal Passport",
        "",
        f"- `{result['status']}`",
        f"- after passport: `{result['decision']['after_orientation_terminal']}`",
        f"- only remaining defect: `{result['decision']['only_remaining_defect']}`",
        "",
        "## Orientation Passport",
        "",
        f"- rule: `{result['orientation']['rule']}`",
        "",
        "| field | chi_R | sign chi_R | B-L | sign B-L | defect |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in result["orientation"]["rows"]:
        lines.append(
            f"| `{row['field']}` | `{row['chi']}` | `{row['sign_chi']}` | "
            f"`{row['B_minus_L']}` | `{row['sign_B_minus_L']}` | `{row['defect']}` |"
        )

    lines.extend(
        [
            "",
            "## Terminal-Lift Passport",
            "",
            f"- sector: `{result['terminal']['sector']}`",
            f"- chi: `{result['terminal']['chi']}`",
            f"- rule: `{result['terminal']['rule']}`",
            "",
            "| condition | value | pass |",
            "| --- | ---: | ---: |",
        ]
    )
    for row in result["terminal"]["condition_rows"]:
        lines.append(f"| `{row['condition']}` | `{row['value']}` | `{row['pass']}` |")

    lines.extend(
        [
            "",
            "## Known Defects After Passport",
            "",
            "| defect | value |",
            "| --- | ---: |",
        ]
    )
    for key, value in result["known_defects_after_orientation_terminal"].items():
        lines.append(f"| `{key}` | `{value}` |")

    lines.extend(
        [
            "",
            "## Decision",
            "",
            f"- Before lifting: `{result['decision']['before_lifting']}`.",
            f"- After lifting before passport: `{result['decision']['after_lifting_before_passport']}`.",
            f"- After orientation/terminal passport: `{result['decision']['after_orientation_terminal']}`.",
            f"- Only remaining defect: `{result['decision']['only_remaining_defect']}`.",
            f"- Hidden fit: `{result['decision']['hidden_fit']}`.",
            "",
            "PASS_FTHEORY_LW2016_ORIENTATION_TERMINAL_PASSPORT",
        ]
    )
    OUT_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    try:
        result = run_vp_ftheory_lw2016_orientation_terminal_passport()
    except Exception as exc:
        print(f"FAIL_FTHEORY_LW2016_ORIENTATION_TERMINAL_PASSPORT: {exc}", file=sys.stderr)
        return 1
    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    _write_report(result)
    print(result["status"])
    print("after_orientation_terminal:", result["decision"]["after_orientation_terminal"])
    print("only_remaining_defect:", result["decision"]["only_remaining_defect"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
