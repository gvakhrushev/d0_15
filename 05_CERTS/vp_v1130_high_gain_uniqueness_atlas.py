#!/usr/bin/env python3
import json, math

results = {}

# 306 destructive terminal readout
V9 = 9
m_dest = 2 * V9
readout306 = m_dest * (m_dest - 1)
results['306'] = {
    'm_dest': m_dest,
    'value': readout306,
    'expected': 306,
    'pass': readout306 == 306,
    'negative_controls': {
        '305': 'missing one off-diagonal destructive channel',
        '307': 'adds one ambient/external destructive sink',
        '324': 'includes self-loops; not destructive readout'
    }
}

# 38 single action section
V_total = 9 + 11 + 13
rank_A = 3
nullity = V_total - rank_A
gamma = nullity // rank_A
assert nullity % rank_A == 0
N_unlock = 2 * gamma - 1
N_act = 2 * N_unlock
results['38'] = {
    'V_total': V_total,
    'rank_A': rank_A,
    'nullity': nullity,
    'gamma': gamma,
    'N_unlock': N_unlock,
    'value': N_act,
    'expected': 38,
    'pass': N_act == 38,
    'negative_controls': {
        '37': 'unclosed half-cycle',
        '39': 'extra non-D0 channel',
        '40': 'witness endpoint double-counted'
    }
}

# 99 gravity active covariance depth
V11 = 11
active_line_depth = V9 * V11
results['99'] = {
    'H_line_dimension': [V9, V11],
    'value': active_line_depth,
    'expected': 99,
    'pass': active_line_depth == 99,
    'negative_controls': {
        '98': 'one active line-covariance channel removed',
        '100': 'one ambient covariance state added',
        '117': 'uses V13 terminal shell as active propagation shell'
    }
}

results['overall_pass'] = all(v['pass'] for v in results.values() if isinstance(v, dict) and 'pass' in v)
print(json.dumps(results, indent=2, ensure_ascii=False))
if not results['overall_pass']:
    raise SystemExit(1)
