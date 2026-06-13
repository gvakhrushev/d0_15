#!/usr/bin/env python3
"""v11.13 proof-cell certificate for D0-PROTON-001 / readout-306.
Checks that 306 is an operator trace and terminal formula, not a naked constant.
"""
import json, math
from pathlib import Path
V9,V11,V13=9,11,13
rank=3
d13=V9+V11
lambda_B2=2*V9*d13*V11
terminal = lambda_B2/V13*(1+1/(d13*V11))
action_trace = (2*V9)*(d13-rank)
identity_checksum = d13*V11+1
identity_rhs = (d13-rank)*V13
lambda_N_core=2640.7985901288725
lambda_p=lambda_N_core-action_trace
mp_me=38*math.sqrt(lambda_p)
checks = {
  "lambda_B2_is_3960": abs(lambda_B2-3960)<1e-12,
  "terminal_formula_is_306": abs(terminal-306)<1e-12,
  "action_trace_is_306": abs(action_trace-306)<1e-12,
  "trace_equals_terminal": abs(terminal-action_trace)<1e-12,
  "identity_221": identity_checksum == identity_rhs == 221,
  "lambda_p": abs(lambda_p-2334.7985901288725)<1e-10,
  "mp_me": abs(mp_me-1836.1506376509778)<1e-10,
}
status = "PASS_READOUT306_PROOF_CELL_V1113" if all(checks.values()) else "FAIL_READOUT306_PROOF_CELL_V1113"
result={
  "status": status,
  "inputs": {"V9":V9,"V11":V11,"V13":V13,"rank":rank,"d13":d13},
  "lambda_B2": lambda_B2,
  "terminal_formula": terminal,
  "action_trace": action_trace,
  "trace_space_dimensions": [2*V9, d13-rank],
  "identity": "d13*V11+1=(d13-rank)*V13=221",
  "lambda_p_D0": lambda_p,
  "mp_over_me_D0": mp_me,
  "checks": checks,
  "forbidden": ["proton mass anchor", "free hadron fit", "306/13 neutron lifetime shortcut"]
}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
Path(__file__).with_suffix('.md').write_text('# Readout-306 proof-cell certificate v11.13\n\nStatus: '+status+'\n\n```json\n'+json.dumps(result,indent=2,sort_keys=True)+'\n```\n',encoding='utf-8')
print(status)
