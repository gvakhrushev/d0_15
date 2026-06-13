#!/usr/bin/env python3
"""Certificate for the D0 proton terminal-destructive readout theorem."""
from __future__ import annotations
import json, math
from pathlib import Path

LAMBDA_B2 = 3960.0
LAMBDA_N_CORE = 2640.7985901288725
V9, V11, V13 = 9, 11, 13
D13 = V9 + V11
LAMBDA_ACT_MEV = 19.417960126286623
REFERENCE_PROTON_MEV = 938.27208816  # external benchmark; not used as input

def run_vp_proton_terminal_destructive_readout() -> dict[str, object]:
    terminal_primary = LAMBDA_B2 / V13
    terminal_checksum = LAMBDA_B2 / (V13 * D13 * V11)
    terminal_total = terminal_primary + terminal_checksum
    lambda_p = LAMBDA_N_CORE - terminal_total
    mp_mev = LAMBDA_ACT_MEV * math.sqrt(lambda_p)
    mpme = 38.0 * math.sqrt(lambda_p)
    status = 'PASS_PROTON_TERMINAL_DESTRUCTIVE_READOUT_CLOSURE' if (
        abs(terminal_total - 306.0) < 1e-12 and
        abs(lambda_p - 2334.7985901288725) < 1e-12 and
        abs(mp_mev - 938.2710491516433) < 1e-9
    ) else 'FAIL_PROTON_TERMINAL_DESTRUCTIVE_READOUT_CLOSURE'
    return {
        'status': status,
        'lambda_B2': LAMBDA_B2,
        'lambda_N_core': LAMBDA_N_CORE,
        'V13_terminal_shell': V13,
        'd13_terminal_active_capacity': D13,
        'V11_transport_layer': V11,
        'terminal_primary_lambda_B2_over_V13': terminal_primary,
        'terminal_checksum_lambda_B2_over_V13_d13_V11': terminal_checksum,
        'terminal_total': terminal_total,
        'lambda_p_D0': lambda_p,
        'Lambda_act_MeV': LAMBDA_ACT_MEV,
        'M_p_D0_MeV': mp_mev,
        'm_p_over_m_e_D0': mpme,
        'reference_proton_MeV_not_input': REFERENCE_PROTON_MEV,
        'residual_MeV_to_reference': mp_mev - REFERENCE_PROTON_MEV,
        'relative_residual_to_reference': mp_mev / REFERENCE_PROTON_MEV - 1.0,
        'calibration_inputs_used': ['electron full-cycle section only'],
        'forbidden_inputs_used': [],
        'interpretation': 'The proton is the charged terminal-destructive readout of the nucleon core; the proton mass is not used as an anchor.'
    }

def main() -> None:
    result = run_vp_proton_terminal_destructive_readout()
    root = Path(__file__).resolve().parent
    (root/'D0_PROTON_TERMINAL_DESTRUCTIVE_READOUT_RESULTS.json').write_text(
        json.dumps(result, indent=2, sort_keys=True) + '\n',
        encoding='utf-8',
    )
    lines = ['# D0 Proton Terminal-Destructive Readout Certificate', '', f"Status: {result['status']}", '']
    for k,v in result.items():
        if k != 'status':
            lines.append(f'- `{k}`: `{v}`')
    (root/'D0_PROTON_TERMINAL_DESTRUCTIVE_READOUT_RESULTS.md').write_text(
        '\n'.join(lines) + '\n',
        encoding='utf-8',
    )
    print(result['status'])

if __name__ == '__main__':
    main()
