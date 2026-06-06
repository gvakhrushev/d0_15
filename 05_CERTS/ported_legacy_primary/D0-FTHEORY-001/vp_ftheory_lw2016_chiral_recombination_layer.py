#!/usr/bin/env python3
"""Lin-Weigand 2016 chiral-index/recombination layer for the D0 filter.

This layer encodes the explicit published spectrum of section 4.1:

- base B=P3 with H^3=1,
- flux G4 fixed by equation (4.5),
- raw chiral indices listed in table 4.1,
- recombination/matching listed in table 4.2.

It does not yet derive the table 4.1 values from resolved-fourfold matter
surface intersections.  Instead it verifies the next factual layer: the
published chi_R ledger recombines to absolute three-generation SM multiplets,
while the unrecombined publication row remains non-final because it contains
the U(1)' and exotic/recombination sectors.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "D0_FTHEORY_LW2016_CHIRAL_RECOMBINATION_NUMBERS.json"
OUT_REPORT = ROOT / "D0_FTHEORY_LW2016_CHIRAL_RECOMBINATION_RESULTS.md"

D0_GENERATIONS = 3


@dataclass(frozen=True)
class FluxLedger:
    base: str
    intersection_numbers: dict[str, int]
    flux_equation: str
    flux_coefficients: dict[str, int]
    source: str


@dataclass(frozen=True)
class ChiralLedger:
    raw_chi: dict[str, int]
    recombination_groups: dict[str, list[str]]
    exotic_before_recombination: list[str]
    lifting_operations: list[str]


def lin_weigand_flux_ledger() -> FluxLedger:
    return FluxLedger(
        base="P3",
        intersection_numbers={
            "H^3": 1,
            "Hbar_Kbar^2": 16,
            "Hbar^2_Kbar": 4,
            "Kbar^3": 64,
        },
        flux_equation=(
            "G4=4Hbar^2+4Hbar*Kbar-4Hbar*S7-36Hbar*U+4Kbar^2-4Kbar*S7-36Kbar*U"
        ),
        flux_coefficients={
            "Hbar^2": 4,
            "Hbar*Kbar": 4,
            "Hbar*S7": -4,
            "Hbar*U": -36,
            "Kbar^2": 4,
            "Kbar*S7": -4,
            "Kbar*U": -36,
        },
        source="Lin-Weigand 2016 equations (4.3) and (4.5)",
    )


def lin_weigand_chiral_ledger() -> ChiralLedger:
    # Table 4.1 signs are representation-convention dependent.  D0's first
    # orientation-free filter uses absolute generation counts; a later sign
    # passport should decide which channel is called R or conjugate R.
    raw_chi = {
        "2(1)": -2,
        "2(2)": 1,
        "2(3)": -2,
        "3(1)": -2,
        "3(2)": 0,
        "3(3)": 1,
        "3(4)": -1,
        "3(5)": -4,
        "(3,2)": 3,
        "1(1)": 2,
        "1(2)": 1,
        "1(3)": 0,
        "1(4)": 0,
        "1(5)": 0,
        "1(6)": -4,
    }
    recombination_groups = {
        "Q": ["(3,2)"],
        "u^c": ["3(1)", "3(4)"],
        "d^c": ["3(3)", "3(5)"],
        "L+Hu+Hd": ["2(1)", "2(2)", "2(3)"],
        "e^c": ["1(1)", "1(2)", "1(4)"],
        "neutral_singlet_1(5)": ["1(5)"],
        "u1_lifting_vev_sector": ["1(6)"],
    }
    return ChiralLedger(
        raw_chi=raw_chi,
        recombination_groups=recombination_groups,
        exotic_before_recombination=[
            "extra vectorlike triplet pair before recombination",
            "1(6) singlet sector used to Higgs/lift U(1)'",
        ],
        lifting_operations=[
            "recombine triplet curves 3(1)+3(4) and 3(3)+3(5)",
            "recombine doublet curves 2(1)+2(2)+2(3)",
            "give vev to 1(6) singlet sector to lift U(1)'",
        ],
    )


def group_chi(raw_chi: dict[str, int], group: list[str]) -> int:
    missing = [item for item in group if item not in raw_chi]
    if missing:
        raise KeyError(f"Missing raw chiral entries: {missing}")
    return sum(raw_chi[item] for item in group)


def run_vp_ftheory_lw2016_chiral_recombination_layer() -> dict[str, Any]:
    flux = lin_weigand_flux_ledger()
    ledger = lin_weigand_chiral_ledger()

    grouped = {
        name: group_chi(ledger.raw_chi, group)
        for name, group in ledger.recombination_groups.items()
    }
    sm_abs_defects = {
        name: abs(grouped[name]) - D0_GENERATIONS
        for name in ("Q", "u^c", "d^c", "L+Hu+Hd", "e^c")
    }
    before_lifting_defects = {
        "rank_defect": 1,
        "exotic_categories": len(ledger.exotic_before_recombination),
    }
    after_recombination_known_defects = {
        "F_chi_abs": sm_abs_defects,
        "F_exotic": 0,
        "F_rank": 0,
    }
    unknown_after_recombination = ["F_scale", "F_terminal", "orientation_sign_passport"]

    if any(value != 0 for value in sm_abs_defects.values()):
        raise AssertionError(f"Recombined SM absolute chirality must be 3: {sm_abs_defects}")
    if grouped["neutral_singlet_1(5)"] != 0:
        raise AssertionError("Neutral singlet 1(5) should have zero chirality in the published ledger.")
    if grouped["u1_lifting_vev_sector"] != -4:
        raise AssertionError("1(6) lifting sector should carry the published chi=-4 ledger entry.")

    return {
        "status": "PASS_FTHEORY_LW2016_CHIRAL_RECOMBINATION_LAYER",
        "source": "Lin-Weigand 2016, arXiv:1604.04292, section 4.1, equations (4.3),(4.5), tables 4.1,4.2",
        "constants": {
            "D0_GENERATIONS": D0_GENERATIONS,
        },
        "flux_ledger": asdict(flux),
        "chiral_ledger": asdict(ledger),
        "grouped_chi": grouped,
        "sm_abs_defects_after_recombination": sm_abs_defects,
        "before_lifting_defects": before_lifting_defects,
        "after_recombination_known_defects": after_recombination_known_defects,
        "unknown_after_recombination": unknown_after_recombination,
        "decision": {
            "published_before_lifting": "D0_PREVACUUM_NOT_FINAL",
            "after_recombination": "D0_CANDIDATE_NOT_FINAL",
            "full_intersection_recompute": "CLOSED_BY_D0_FTHEORY_LW2016_INTERSECTION_RECOMPUTE",
            "hidden_fit": False,
        },
        "guardrails": [
            "This layer encodes the published chiral-index table; it does not recompute chi_R from resolved matter surfaces.",
            "Absolute chirality is used pending a D0 sign/orientation passport.",
            "The 1(6) sector is counted as a lifting/vev sector, not as an accepted light SM multiplet.",
            "After recombination the model is still not final until scale and terminal closure are supplied.",
        ],
    }


def _write_report(result: dict[str, Any]) -> None:
    lines = [
        "# D0 F-theory Lin-Weigand 2016 Chiral Recombination Layer",
        "",
        f"- `{result['status']}`",
        f"- source: `{result['source']}`",
        "",
        "## Flux Ledger",
        "",
        f"- base: `{result['flux_ledger']['base']}`",
        f"- intersections: `{result['flux_ledger']['intersection_numbers']}`",
        f"- flux: `{result['flux_ledger']['flux_equation']}`",
        "",
        "## Raw Chiral Ledger",
        "",
        "| curve | chi |",
        "| --- | ---: |",
    ]
    for name, value in result["chiral_ledger"]["raw_chi"].items():
        lines.append(f"| `{name}` | `{value}` |")
    lines.extend(
        [
            "",
            "## Recombined Groups",
            "",
            "| D0/SM group | curves | grouped chi | abs defect |",
            "| --- | --- | ---: | ---: |",
        ]
    )
    sm_defects = result["sm_abs_defects_after_recombination"]
    for name, group in result["chiral_ledger"]["recombination_groups"].items():
        defect = sm_defects.get(name, "")
        lines.append(
            f"| `{name}` | `{group}` | `{result['grouped_chi'][name]}` | `{defect}` |"
        )
    lines.extend(
        [
            "",
            "## Decision",
            "",
            "- Before lifting: `D0_PREVACUUM_NOT_FINAL` because rank defect and exotic/lifting sectors remain.",
            "- After recombination: known chiral SM defects vanish under `abs(chi)=3`.",
            "- The row remains `D0_CANDIDATE_NOT_FINAL` until `F_scale`, `F_terminal`, and the sign passport are closed.",
            "",
            "## Guardrails",
            "",
        ]
    )
    for item in result["guardrails"]:
        lines.append(f"- {item}")
    OUT_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    result = run_vp_ftheory_lw2016_chiral_recombination_layer()
    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _write_report(result)
    print(f"VP F-theory LW2016 chiral recombination layer: [{result['status']}]")
    print(json.dumps(result["decision"], indent=2, sort_keys=True))
    if result["status"].startswith("FAIL"):
        sys.exit(1)


if __name__ == "__main__":
    main()
