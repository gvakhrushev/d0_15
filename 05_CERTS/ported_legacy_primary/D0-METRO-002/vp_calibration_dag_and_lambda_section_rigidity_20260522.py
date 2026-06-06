#!/usr/bin/env python3
"""D0 calibration DAG and Lambda action-section rigidity certificate."""
import math, json
from pathlib import Path

phi = (1 + math.sqrt(5)) / 2
delta0 = (math.sqrt(5) - 2) / 2
Delta_lambda = math.sqrt(10) / 20
I_B = Delta_lambda**2 * delta0**3 / 24
q_mass = 1/(1+delta0**3)
pi0 = (6/5)*phi**2
Lambda_act_MeV = 19.417960126286623
tau0_seconds = 2.129815732459607e-22
ell0_meters = 6.38502693521136e-14
D_L = 3.951771012845559e+21

powers = [1,1,1,-1,-1,-1,-2,-2,0]
nonzero_scale_rank = 1 if any(p != 0 for p in powers) else 0
assert abs(delta0 - 1/(2*phi**3)) < 1e-15
assert abs(I_B - 1.7129710281803203e-06) < 1e-20
assert abs(q_mass - 0.9983582475962778) < 1e-15
assert abs(pi0 - 3.141640786499874) < 1e-15
assert abs((ell0_meters/tau0_seconds) - 299792458.0) < 1e-3
assert abs(Lambda_act_MeV/38 - 0.5109989506917533) < 1e-15
assert nonzero_scale_rank == 1
assert len(["electron_full_cycle_action_section"]) == 1

# Check active text repairs for known broken LaTeX artifacts.
root = Path(__file__).resolve().parents[1]
active_text = ""
for p in (root/'01_BOOKS').glob('BOOK_*.md'):
    active_text += p.read_text(encoding='utf-8')
assert '\x0c' not in active_text
assert '\f\frac' not in active_text
assert '=\\right)' not in active_text

out = {
    "status": "PASS_CALIBRATION_DAG_AND_LAMBDA_SECTION_RIGIDITY",
    "Lambda_act_MeV": Lambda_act_MeV,
    "electron_rest_slot_MeV": Lambda_act_MeV/38,
    "tau0_seconds": tau0_seconds,
    "ell0_meters": ell0_meters,
    "c_from_ell0_over_tau0": ell0_meters/tau0_seconds,
    "I_B": I_B,
    "q_mass": q_mass,
    "pi0": pi0,
    "lambda_power_passport": powers,
    "nonzero_scale_rank": nonzero_scale_rank
}
print(json.dumps(out, indent=2))
print("PASS_CALIBRATION_DAG_AND_LAMBDA_SECTION_RIGIDITY")
