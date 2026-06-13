#!/usr/bin/env python3
"""D0 filter for the Lin-Weigand 2016 F-theory Standard-Model vacuum class.

This is a structural certificate, not a full intersection-tensor recomputation.
The fixture records the published-level data needed for the first D0 vacuum
filter: internal real dimension, light gauge rank, absolute chiral generation
count, light exotics, free low-energy scales, and terminal shell status.

Full matter-surface intersections can be plugged in later by replacing the
listed chiral indices with computed int_{S_R} G4 values.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
import re
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "D0_FTHEORY_LW2016_D0_FILTER_NUMBERS.json"
OUT_REPORT = ROOT / "D0_FTHEORY_LW2016_D0_FILTER_RESULTS.md"

D0_INTERNAL_REAL_DIM = 8
D0_LIGHT_GAUGE_RANK = 4
D0_GENERATIONS = 3
D0_TERMINAL_DIM = 13

SM_REPS = (
    "Q",
    "u^c",
    "d^c",
    "L",
    "e^c",
)


@dataclass(frozen=True)
class VacuumData:
    name: str
    source: str
    gauge_factors: list[str]
    real_internal_dim: int
    chiral_indices: dict[str, int]
    exotics: list[str]
    free_mass_scales: int | None
    terminal_dim: int | None
    notes: list[str]


@dataclass(frozen=True)
class D0FilterResult:
    name: str
    gauge_rank: int
    F_omega: int
    F_rank: int
    F_chi_abs: dict[str, int]
    F_exotic: int
    F_scale: int | None
    F_terminal: int | None
    hard_failures: list[str]
    unknowns: list[str]
    status: str
    notes: list[str]


def gauge_rank(gauge_factors: list[str]) -> int:
    rank = 0
    for factor in gauge_factors:
        token = factor.strip().replace(" ", "")
        su = re.fullmatch(r"SU\((\d+)\)", token)
        u = re.fullmatch(r"U\((\d+)\)", token)
        if su:
            rank += int(su.group(1)) - 1
        elif u:
            rank += int(u.group(1))
        else:
            raise ValueError(f"Unsupported gauge factor: {factor!r}")
    return rank


def d0_filter(vac: VacuumData) -> D0FilterResult:
    rank = gauge_rank(vac.gauge_factors)
    f_omega = vac.real_internal_dim - D0_INTERNAL_REAL_DIM
    f_rank = rank - D0_LIGHT_GAUGE_RANK
    f_chi_abs = {
        rep: abs(vac.chiral_indices[rep]) - D0_GENERATIONS
        for rep in SM_REPS
        if rep in vac.chiral_indices
    }
    missing_reps = [rep for rep in SM_REPS if rep not in vac.chiral_indices]
    f_exotic = len(vac.exotics)
    f_scale = None if vac.free_mass_scales is None else vac.free_mass_scales
    f_terminal = None if vac.terminal_dim is None else vac.terminal_dim - D0_TERMINAL_DIM

    hard_failures: list[str] = []
    unknowns: list[str] = []
    if f_omega != 0:
        hard_failures.append("F_omega")
    if f_rank != 0:
        hard_failures.append("F_rank")
    if missing_reps:
        hard_failures.append("F_chi_missing_reps")
    if any(value != 0 for value in f_chi_abs.values()):
        hard_failures.append("F_chi_abs")
    if f_exotic != 0:
        hard_failures.append("F_exotic")
    if f_scale is None:
        unknowns.append("F_scale")
    elif f_scale != 0:
        hard_failures.append("F_scale")
    if f_terminal is None:
        unknowns.append("F_terminal")
    elif f_terminal != 0:
        hard_failures.append("F_terminal")

    if hard_failures:
        status = "D0_PREVACUUM_NOT_FINAL"
    elif unknowns:
        status = "D0_CANDIDATE_NOT_FINAL"
    else:
        status = "D0_FINAL_ADMISSIBLE"

    notes = list(vac.notes)
    if missing_reps:
        notes.append(f"Missing SM chiral reps in fixture: {missing_reps}")
    return D0FilterResult(
        name=vac.name,
        gauge_rank=rank,
        F_omega=f_omega,
        F_rank=f_rank,
        F_chi_abs=f_chi_abs,
        F_exotic=f_exotic,
        F_scale=f_scale,
        F_terminal=f_terminal,
        hard_failures=hard_failures,
        unknowns=unknowns,
        status=status,
        notes=notes,
    )


def lin_weigand_fixtures() -> list[VacuumData]:
    source = "Lin-Weigand 2016, arXiv:1604.04292"
    sm_chiral_abs_three = {
        "Q": 3,
        "u^c": 3,
        "d^c": 3,
        "L": 3,
        "e^c": 3,
    }
    return [
        VacuumData(
            name="Lin-Weigand published SM-like model before lifting",
            source=source,
            gauge_factors=["SU(3)", "SU(2)", "U(1)", "U(1)"],
            real_internal_dim=8,
            chiral_indices=sm_chiral_abs_three,
            exotics=["vectorlike color triplet pair", "1(6) recombination singlet sector"],
            free_mass_scales=None,
            terminal_dim=None,
            notes=[
                "F-theory Calabi-Yau fourfold gives real internal dimension 8.",
                "Published gauge group has two U(1) factors before D0 light-rank filtering.",
                "Fixture uses absolute SM chiral index = 3; sign passport is a later orientation layer.",
                "The triplet pair and the 1(6) singlet sector are treated as light until recombination/lifting is supplied.",
            ],
        ),
        VacuumData(
            name="Lin-Weigand after U(1)' lift and triplet recombination",
            source=source,
            gauge_factors=["SU(3)", "SU(2)", "U(1)"],
            real_internal_dim=8,
            chiral_indices=sm_chiral_abs_three,
            exotics=[],
            free_mass_scales=None,
            terminal_dim=None,
            notes=[
                "This is a D0 candidate carrier geometry after the two required light-sector lifts.",
                "It is still not final because mass-scale and terminal-shell closure are not supplied by the F-theory fixture.",
            ],
        ),
        VacuumData(
            name="D0 final-vacuum target sanity row",
            source="D0 target, not a Lin-Weigand claim",
            gauge_factors=["SU(3)", "SU(2)", "U(1)"],
            real_internal_dim=8,
            chiral_indices=sm_chiral_abs_three,
            exotics=[],
            free_mass_scales=0,
            terminal_dim=13,
            notes=[
                "Sanity row showing the exact zero vector required for a final D0 vacuum.",
                "This row is not asserted to be produced by the published Lin-Weigand model.",
            ],
        ),
    ]


def run_vp_ftheory_lw2016_d0_filter() -> dict[str, Any]:
    fixtures = lin_weigand_fixtures()
    results = [d0_filter(vac) for vac in fixtures]
    published = results[0]
    lifted = results[1]
    target = results[2]

    if published.status != "D0_PREVACUUM_NOT_FINAL":
        raise AssertionError("Published Lin-Weigand row must be rejected as final D0 vacuum.")
    if published.F_rank != 1:
        raise AssertionError("Published Lin-Weigand rank defect must be +1.")
    if published.F_exotic <= 0:
        raise AssertionError("Published Lin-Weigand row must retain an exotic defect before lifting.")
    if lifted.status != "D0_CANDIDATE_NOT_FINAL":
        raise AssertionError("Lifted row must be a D0 candidate, not final, while scale/terminal are unknown.")
    if target.status != "D0_FINAL_ADMISSIBLE":
        raise AssertionError("D0 target sanity row must pass all filter components.")

    return {
        "status": "PASS_FTHEORY_LW2016_D0_FILTER",
        "constants": {
            "D0_INTERNAL_REAL_DIM": D0_INTERNAL_REAL_DIM,
            "D0_LIGHT_GAUGE_RANK": D0_LIGHT_GAUGE_RANK,
            "D0_GENERATIONS": D0_GENERATIONS,
            "D0_TERMINAL_DIM": D0_TERMINAL_DIM,
        },
        "fixtures": [asdict(vac) for vac in fixtures],
        "results": [asdict(result) for result in results],
        "decision": {
            "published_lw2016": published.status,
            "published_rank_defect": published.F_rank,
            "published_exotic_defect": published.F_exotic,
            "after_lifting": lifted.status,
            "final_target": target.status,
            "hidden_fit": False,
        },
        "guardrails": [
            "This certificate does not recompute Lin-Weigand intersection numbers.",
            "F_chi uses abs(chi_R)=3 pending an orientation/sign passport.",
            "A geometric U(1) is allowed only if it is not light after Stueckelberg/Higgs/archive lifting.",
            "F_scale=0 requires a D0 readout/moduli projection not supplied by the published fixture.",
        ],
    }


def _write_report(result: dict[str, Any]) -> None:
    lines = [
        "# D0 F-theory Lin-Weigand 2016 Vacuum Filter",
        "",
        f"- `{result['status']}`",
        "",
        "Sources:",
        "",
        "- Lin and Weigand, `G4-Flux and Standard Model Vacua in F-theory`, arXiv:1604.04292.",
        "",
        "## D0 Filter",
        "",
        "The implemented D0 vector is:",
        "",
        "```text",
        "F_D0 = (dim_R(Y4)-8, rank(G_light)-4, {|chi_R|-3}_R, n_light_exotics, n_free_scales, D_terminal-13)",
        "```",
        "",
        "A final D0 vacuum requires every known component to vanish and no unknown component to remain.",
        "",
        "## Results",
        "",
        "| fixture | gauge rank | F_omega | F_rank | F_chi_abs | F_exotic | F_scale | F_terminal | status |",
        "| --- | ---: | ---: | ---: | --- | ---: | --- | --- | --- |",
    ]
    for row in result["results"]:
        lines.append(
            f"| `{row['name']}` | `{row['gauge_rank']}` | `{row['F_omega']}` | `{row['F_rank']}` | "
            f"`{row['F_chi_abs']}` | `{row['F_exotic']}` | `{row['F_scale']}` | `{row['F_terminal']}` | `{row['status']}` |"
        )
    lines.extend(
        [
            "",
            "## Decision",
            "",
            "- Published Lin-Weigand before lifting is not a final D0 vacuum: `F_rank=+1` and `F_exotic>0`.",
            "- After `U(1)'` lifting and triplet recombination it becomes a D0 candidate carrier geometry.",
            "- It is still not final until `F_scale=0` and `F_terminal=0` are supplied by a D0 projection.",
            "",
            "## Guardrails",
            "",
        ]
    )
    for item in result["guardrails"]:
        lines.append(f"- {item}")
    OUT_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    result = run_vp_ftheory_lw2016_d0_filter()
    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _write_report(result)
    print(f"VP F-theory LW2016 D0 filter: [{result['status']}]")
    print(json.dumps(result["decision"], indent=2, sort_keys=True))
    if result["status"].startswith("FAIL"):
        sys.exit(1)


if __name__ == "__main__":
    main()
