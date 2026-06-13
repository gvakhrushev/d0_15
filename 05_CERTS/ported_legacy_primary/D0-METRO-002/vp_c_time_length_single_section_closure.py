#!/usr/bin/env python3
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
nums = json.load(open(root/'00_INDEX'/'D0_C_TIME_LENGTH_SINGLE_SECTION_CLOSURE_NUMBERS.json'))

tau0 = nums['single_section_dictionary']['tau0_seconds']
ell0 = nums['single_section_dictionary']['ell0_meters']
c_exact = nums['single_section_dictionary']['c_exact_definition_m_per_s']
ratio = ell0/tau0
D_L = nums['gravity_downstream']['D_L']
ellP = nums['gravity_downstream']['ellP_D0_m']

checks = []
checks.append(('internal_c', nums['internal_units']['ell0_D0'] / nums['internal_units']['tau0_D0'] == 1))
checks.append(('si_c_ratio', abs(ratio - c_exact) < 1e-6))
checks.append(('ell0_c_tau0', abs(ell0 - c_exact*tau0)/ell0 < 5e-16))
checks.append(('ellP_depth', abs(ellP - ell0/D_L)/ellP < 5e-16))
checks.append(('no_hadron_anchor', 'not independent' in nums['neutron_proton_role']['role'] or 'not independent' in ' '.join(nums['guardrails'])))

failed = [name for name, ok in checks if not ok]
if failed:
    raise SystemExit('FAIL_C_TIME_LENGTH_SINGLE_SECTION_CLOSURE: ' + ', '.join(failed))
print('PASS_C_TIME_LENGTH_SINGLE_SECTION_CLOSURE')
print(json.dumps({
  'c_ratio': ratio,
  'tau0_seconds': tau0,
  'ell0_meters': ell0,
  'ellP_depth_check': ell0/D_L,
  'status': nums['status']
}, indent=2))
