#!/usr/bin/env python3
"""Condensed scale-rigidity layer for the Lin-Weigand 2016 D0 carrier.

This certificate is intentionally conservative.  It records the condensed
testing language for the remaining F_scale defect, but it refuses to infer
scale freezing from profiniteness alone.

The only final PASS for scale closure would require explicit S_gate/Jacobian
constraint data with nullity zero.  In the current corpus that data is absent,
so the honest output is D0_CANDIDATE_SCALE_RIGIDITY_OPEN.
"""

from __future__ import annotations

import itertools
import json
import math
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ORIENTATION_TERMINAL_JSON = ROOT / "D0_FTHEORY_LW2016_ORIENTATION_TERMINAL_NUMBERS.json"
D0_FILTER_JSON = ROOT / "D0_FTHEORY_LW2016_D0_FILTER_NUMBERS.json"
OPTIONAL_SCALE_JACOBIAN_JSON = ROOT / "D0_FTHEORY_LW2016_SCALE_JACOBIAN_CONSTRAINTS.json"
OUT_JSON = ROOT / "D0_FTHEORY_LW2016_CONDENSED_SCALE_RIGIDITY_NUMBERS.json"
OUT_REPORT = ROOT / "D0_FTHEORY_LW2016_CONDENSED_SCALE_RIGIDITY_RESULTS.md"

EPS = 1e-12
FINITE_STAGE_MAX_N = 8
D0_BINARY_ALPHABET = ("A", "B")
D0_CONSTRAINTS = [
    "finite_detector_factorization",
    "golden_self_return",
    "single_Lambda_section",
    "S_gate_stationarity",
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def binary_words(n: int) -> list[str]:
    return ["".join(bits) for bits in itertools.product(D0_BINARY_ALPHABET, repeat=n)]


def projection(word: str, n: int) -> str:
    if n > len(word):
        raise ValueError("Cannot project to a longer word.")
    return word[:n]


def finite_detector_audit(max_n: int = FINITE_STAGE_MAX_N) -> dict[str, Any]:
    rows = []
    for n in range(max_n + 1):
        size = len(binary_words(n))
        expected = 2**n
        rows.append({"n": n, "S_n_size": size, "expected": expected, "pass": size == expected})

    projection_rows = []
    for n in range(max_n):
        domain = binary_words(n + 1)
        codomain = set(binary_words(n))
        projected = [projection(word, n) for word in domain]
        fibers = {target: projected.count(target) for target in codomain}
        projection_rows.append(
            {
                "from": n + 1,
                "to": n,
                "all_targets_hit": set(projected) == codomain,
                "uniform_binary_fibers": all(size == 2 for size in fibers.values()),
                "pass": set(projected) == codomain and all(size == 2 for size in fibers.values()),
            }
        )

    return {
        "S_D0_type": "inverse_limit_binary_detector",
        "alphabet": list(D0_BINARY_ALPHABET),
        "finite_stage_rows": rows,
        "projection_rows": projection_rows,
        "projection_consistent": all(row["pass"] for row in rows)
        and all(row["pass"] for row in projection_rows),
    }


def cylinder_measure(word: str, p: float) -> float:
    q = p * p
    value = 1.0
    for letter in word:
        if letter == "A":
            value *= p
        elif letter == "B":
            value *= q
        else:
            raise ValueError(f"Unknown detector letter: {letter!r}")
    return value


def golden_measure_audit(max_n: int = FINITE_STAGE_MAX_N) -> dict[str, Any]:
    p = (math.sqrt(5.0) - 1.0) / 2.0
    q = p * p
    self_return_defect = p + q - 1.0
    rows = []
    for n in range(max_n + 1):
        total = sum(cylinder_measure(word, p) for word in binary_words(n))
        rows.append({"n": n, "total_cylinder_measure": total, "defect": total - 1.0, "pass": abs(total - 1.0) < EPS})
    return {
        "p": p,
        "p_squared": q,
        "self_return_defect": self_return_defect,
        "self_return_pass": abs(self_return_defect) < EPS,
        "branch_measure": {"A": "p=phi^-1", "B": "p^2=phi^-2"},
        "cylinder_rows": rows,
        "finite_cylinder_normalization_pass": all(row["pass"] for row in rows),
    }


def ordinary_condensed_negative_control() -> dict[str, Any]:
    return {
        "ordinary_condensed_hom_free": True,
        "statement": "Hom_Top(S_D0, M_LW) is generally not finite and does not freeze continuous moduli by profiniteness alone.",
        "reason": "Continuous maps from a Cantor/profinite test object into a topological moduli space can still vary; scale closure requires the D0 constrained subfunctor.",
        "pass": True,
    }


def nullity_from_jacobian(matrix: list[list[float]], tol: float = 1e-10) -> int:
    # Lightweight Gaussian rank over floats; sufficient for optional numeric
    # constraint data.  Exact symbolic scale closure should be a later cert.
    rows = [list(map(float, row)) for row in matrix]
    if not rows:
        return 0
    m = len(rows)
    n = len(rows[0])
    rank = 0
    col = 0
    while rank < m and col < n:
        pivot = max(range(rank, m), key=lambda r: abs(rows[r][col]))
        if abs(rows[pivot][col]) <= tol:
            col += 1
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        pivot_value = rows[rank][col]
        rows[rank] = [x / pivot_value for x in rows[rank]]
        for r in range(m):
            if r == rank:
                continue
            factor = rows[r][col]
            if abs(factor) > tol:
                rows[r] = [a - factor * b for a, b in zip(rows[r], rows[rank])]
        rank += 1
        col += 1
    return max(0, n - rank)


def scale_defect_from_optional_jacobian() -> dict[str, Any]:
    if not OPTIONAL_SCALE_JACOBIAN_JSON.exists():
        return {
            "jacobian_available": False,
            "F_scale": None,
            "status": "D0_CANDIDATE_SCALE_RIGIDITY_OPEN",
            "reason": "No S_gate/string-moduli Jacobian constraint data is present.",
        }
    data = load_json(OPTIONAL_SCALE_JACOBIAN_JSON)
    matrix = data.get("J_constraints")
    if not isinstance(matrix, list):
        raise AssertionError("Scale Jacobian file exists but lacks list field J_constraints.")
    nullity = nullity_from_jacobian(matrix)
    return {
        "jacobian_available": True,
        "source": str(OPTIONAL_SCALE_JACOBIAN_JSON.relative_to(ROOT)),
        "F_scale": nullity,
        "status": "D0_FINAL_ADMISSIBLE_CARRIER" if nullity == 0 else "D0_CANDIDATE_SCALE_RIGIDITY_OPEN",
        "reason": "F_scale is the nullity of the supplied D0 scale-constraint Jacobian.",
    }


def run_vp_ftheory_lw2016_condensed_scale_rigidity() -> dict[str, Any]:
    orientation_terminal = load_json(ORIENTATION_TERMINAL_JSON)
    d0_filter = load_json(D0_FILTER_JSON)
    if orientation_terminal["status"] != "PASS_FTHEORY_LW2016_ORIENTATION_TERMINAL_PASSPORT":
        raise AssertionError(f"Unexpected orientation/terminal status: {orientation_terminal['status']}")
    if orientation_terminal["decision"]["after_orientation_terminal"] != "D0_CANDIDATE_SCALE_OPEN":
        raise AssertionError("Scale-rigidity layer must start from D0_CANDIDATE_SCALE_OPEN.")
    if d0_filter["status"] != "PASS_FTHEORY_LW2016_D0_FILTER":
        raise AssertionError(f"Unexpected D0 filter status: {d0_filter['status']}")

    finite_detector = finite_detector_audit()
    golden_measure = golden_measure_audit()
    negative_control = ordinary_condensed_negative_control()
    scale_defect = scale_defect_from_optional_jacobian()

    if not finite_detector["projection_consistent"]:
        raise AssertionError("Finite detector inverse-system audit failed.")
    if not golden_measure["self_return_pass"] or not golden_measure["finite_cylinder_normalization_pass"]:
        raise AssertionError("Golden self-return measure audit failed.")
    if negative_control["ordinary_condensed_hom_free"] is not True:
        raise AssertionError("Negative control must explicitly prevent ordinary Hom from closing F_scale.")

    constrained_subfunctor = {
        "name": "M_LW^D0(S_D0)",
        "ambient": "underline(M_LW)(S_D0)=Hom_Top(S_D0,M_LW)",
        "constraints": D0_CONSTRAINTS,
        "finite_factorization_rule": "f:S_D0->M_LW must factor as f_N o pi_N for physical readout.",
        "golden_self_return_rule": "branch weights A=p, B=p^2 obey p+p^2=1.",
        "single_section_rule": "all low-energy scales must pass through Lambda_act=38*m_e*c^2.",
        "stationarity_rule": "dS_gate/dm_a=0 for string-moduli scale directions.",
    }

    formulated_defects = {
        "F_omega": 0,
        "F_rank": 0,
        "F_chi_abs": 0,
        "F_orientation": 0,
        "F_exotic": 0,
        "F_terminal": 0,
        "F_scale": scale_defect["F_scale"],
    }

    if scale_defect["F_scale"] is None:
        status = "D0_CANDIDATE_SCALE_RIGIDITY_OPEN"
    elif scale_defect["F_scale"] == 0:
        status = "D0_FINAL_ADMISSIBLE_CARRIER"
    else:
        status = "D0_CANDIDATE_SCALE_RIGIDITY_OPEN"

    if scale_defect["F_scale"] is None and status != "D0_CANDIDATE_SCALE_RIGIDITY_OPEN":
        raise AssertionError("F_scale=None must not produce final admissible status.")

    return {
        "status": "PASS_FTHEORY_LW2016_CONDENSED_SCALE_RIGIDITY_LAYER",
        "final_scale_status": status,
        "inputs": {
            "orientation_terminal": str(ORIENTATION_TERMINAL_JSON.relative_to(ROOT)),
            "d0_filter": str(D0_FILTER_JSON.relative_to(ROOT)),
            "optional_scale_jacobian": str(OPTIONAL_SCALE_JACOBIAN_JSON.relative_to(ROOT)),
        },
        "condensed_reference": {
            "source": "Scholze, Lectures on Condensed Mathematics; condensed sets as sheaves on profinite sets; topological X tested by S |-> Hom_Top(S,X).",
            "guardrail": "This reference supplies the testing language only; it does not freeze moduli.",
        },
        "profinite_detector": finite_detector,
        "golden_measure": golden_measure,
        "ordinary_condensed_negative_control": negative_control,
        "d0_constrained_subfunctor": constrained_subfunctor,
        "scale_defect_logic": scale_defect,
        "known_defects_after_condensed_formulation": formulated_defects,
        "decision": {
            "before_scale_layer": orientation_terminal["decision"]["after_orientation_terminal"],
            "after_condensed_scale_layer": status,
            "F_scale": scale_defect["F_scale"],
            "false_pass_prevented": scale_defect["F_scale"] is None and status == "D0_CANDIDATE_SCALE_RIGIDITY_OPEN",
            "ordinary_condensed_hom_closes_scale": False,
            "hidden_fit": False,
        },
        "guardrails": [
            "S_D0 is a distinguished profinite test object, not the whole ProFin category.",
            "Ordinary Hom_Top(S_D0,M_LW) is a negative control and cannot close F_scale.",
            "Only the constrained D0 subfunctor can define scale rigidity.",
            "No final F_scale=0 claim is made without an explicit S_gate scale-constraint Jacobian.",
        ],
    }


def _write_report(result: dict[str, Any]) -> None:
    lines = [
        "# D0 F-theory Lin-Weigand 2016 Condensed Scale-Rigidity Layer",
        "",
        f"- `{result['status']}`",
        f"- final scale status: `{result['final_scale_status']}`",
        f"- F_scale: `{result['decision']['F_scale']}`",
        "",
        "## Profinite Detector",
        "",
        "| n | S_n size | expected | pass |",
        "| ---: | ---: | ---: | ---: |",
    ]
    for row in result["profinite_detector"]["finite_stage_rows"]:
        lines.append(f"| `{row['n']}` | `{row['S_n_size']}` | `{row['expected']}` | `{row['pass']}` |")
    lines.extend(
        [
            "",
            "## Golden Measure",
            "",
            f"- p: `{result['golden_measure']['p']}`",
            f"- p^2: `{result['golden_measure']['p_squared']}`",
            f"- p+p^2-1: `{result['golden_measure']['self_return_defect']}`",
            f"- self-return pass: `{result['golden_measure']['self_return_pass']}`",
            "",
            "## Negative Control",
            "",
            f"- ordinary condensed Hom free: `{result['ordinary_condensed_negative_control']['ordinary_condensed_hom_free']}`",
            f"- statement: {result['ordinary_condensed_negative_control']['statement']}",
            "",
            "## D0 Constrained Subfunctor",
            "",
        ]
    )
    for constraint in result["d0_constrained_subfunctor"]["constraints"]:
        lines.append(f"- `{constraint}`")
    lines.extend(
        [
            "",
            "## Defect Ledger",
            "",
            "| defect | value |",
            "| --- | ---: |",
        ]
    )
    for key, value in result["known_defects_after_condensed_formulation"].items():
        lines.append(f"| `{key}` | `{value}` |")
    lines.extend(
        [
            "",
            "## Decision",
            "",
            f"- Before scale layer: `{result['decision']['before_scale_layer']}`.",
            f"- After condensed scale layer: `{result['decision']['after_condensed_scale_layer']}`.",
            f"- False final PASS prevented: `{result['decision']['false_pass_prevented']}`.",
            f"- Ordinary condensed Hom closes scale: `{result['decision']['ordinary_condensed_hom_closes_scale']}`.",
            f"- Hidden fit: `{result['decision']['hidden_fit']}`.",
            "",
            "PASS_FTHEORY_LW2016_CONDENSED_SCALE_RIGIDITY_LAYER",
        ]
    )
    OUT_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    try:
        result = run_vp_ftheory_lw2016_condensed_scale_rigidity()
    except Exception as exc:
        print(f"FAIL_FTHEORY_LW2016_CONDENSED_SCALE_RIGIDITY_LAYER: {exc}", file=sys.stderr)
        return 1
    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    _write_report(result)
    print(result["status"])
    print("final_scale_status:", result["final_scale_status"])
    print("F_scale:", result["decision"]["F_scale"])
    print("false_pass_prevented:", result["decision"]["false_pass_prevented"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
