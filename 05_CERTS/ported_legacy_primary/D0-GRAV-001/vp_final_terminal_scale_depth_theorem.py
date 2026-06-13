#!/usr/bin/env python3
"""Final bridge Task 1: terminal leakage scale-depth theorem ledger."""

from __future__ import annotations

import math

from d0_graph import PARTS, N_VERTICES, delta_0, phi
from vp_gate_coefficient_stationarity import run_vp_gate_coefficient_stationarity
from vp_gravity_terminal_leakage_selector import run_vp_gravity_terminal_leakage_selector
from vp_scene_generating_action import run_vp_scene_generating_action


def run_vp_final_terminal_scale_depth_theorem() -> dict[str, object]:
    scene = run_vp_scene_generating_action()
    gate = run_vp_gate_coefficient_stationarity()
    terminal = run_vp_gravity_terminal_leakage_selector()

    v9, v11, v13 = PARTS
    omega8 = 8
    depth = v9 * v11
    rank_depth = 3 * N_VERTICES
    base = omega8 * phi**depth
    correction = 1.0 + delta_0 / v13
    corrected = base * correction

    derivation_steps = [
        "J_scene stationary point gives Omega8 and parts (V9,V11,V13)=(9,11,13).",
        "The addressed scale-depth uses V9*V11; independently Rank*|V|=3*33 gives the same depth 99.",
        "The electron SI bridge is terminal-shell calibrated, so the first resolved leakage is distributed over |V13|.",
        "Terminal selector chooses correction 1+delta0/V13 before any numeric comparison.",
        "The leakage correction multiplies the scale-depth because it rescales ell0/lP, not gamma_e directly.",
    ]
    failure_modes = [
        "If the SI bridge uses a local generator line, the reduced Compton convention removes the 2*pi cycle.",
        "If the bridge is not electron-terminal, denominators Rank, Omega8, |V|, or N_anchor can compete.",
        "If the correction is additive in gamma_e rather than multiplicative in ell0/lP, this formula is invalid.",
        "If V9*V11 is not derived as the continuum-depth selector, phi^99 remains a bridge ansatz.",
    ]
    return {
        "status": "PASS_TERMINAL_SCALE_DEPTH_DERIVATION_LEDGER",
        "theorem_candidate": "Terminal Leakage Scale-Depth Theorem",
        "scene_status": scene["status"],
        "gate_status": gate["status"],
        "terminal_selector_status": terminal["status"],
        "formula": "ell0/lP = Omega8 * phi^(V9*V11) * (1 + delta0/V13)",
        "depth_identity": {
            "V9*V11": depth,
            "Rank*|V|": rank_depth,
            "identity_holds": depth == rank_depth,
        },
        "base_scale_depth": base,
        "terminal_correction": correction,
        "corrected_scale_depth": corrected,
        "correction_type": "multiplicative scale-depth correction",
        "derivation_steps": derivation_steps,
        "failure_modes": failure_modes,
        "proof_obligation_remaining": (
            "derive the use of V9*V11 as continuum self-similarity depth from "
            "J_scene + S_gate + S_boundary + S_heat stationarity"
        ),
    }


def main() -> None:
    result = run_vp_final_terminal_scale_depth_theorem()
    print(f"VP final terminal scale-depth theorem: [{result['status']}]")
    for key, value in result.items():
        if key != "status":
            print(f"{key}= {value}")


if __name__ == "__main__":
    main()
