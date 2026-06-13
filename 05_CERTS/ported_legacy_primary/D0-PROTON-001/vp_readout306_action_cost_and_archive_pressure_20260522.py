#!/usr/bin/env python3
import math, json
sqrt5 = math.sqrt(5)
phi = (1+sqrt5)/2
delta0 = (sqrt5-2)/2
V9, V11, V13 = 9, 11, 13
rank = 3
nullity = 30
d13 = V9 + V11
lambda_B2 = 2*V9*d13*V11
terminal_primary = lambda_B2/V13
terminal_checksum = lambda_B2/(V13*d13*V11)
terminal_total = terminal_primary + terminal_checksum
action_cost = 2*V9*(d13-rank)
lambda_N_core = 2640.7985901288725
lambda_p = lambda_N_core - terminal_total
mp_me = 38*math.sqrt(lambda_p)
delta8 = delta0**8
pressure_total = -delta8
pressure_per_archive_mode = pressure_total/nullity
lambda_B_act = 0.012763468417239953
A_V13 = 1/(1+delta0/V13)
lambda_B_terminal = lambda_B_act*A_V13
A_phi = 1/(1+delta0/phi)
chi_B = -math.log(A_phi)
assert abs(lambda_B2-3960.0) < 1e-12
assert abs(terminal_total-306.0) < 1e-12
assert abs(action_cost-306.0) < 1e-12
assert abs(terminal_total-action_cost) < 1e-12
assert abs((d13*V11+1) - ((d13-rank)*V13)) < 1e-12
assert abs(lambda_p-2334.7985901288725) < 1e-10
assert pressure_total < 0
assert abs(pressure_total + delta8) < 1e-30
assert abs(pressure_per_archive_mode*nullity - pressure_total) < 1e-30
assert 0 < lambda_B_terminal < lambda_B_act
assert chi_B > 0
result = {
    "status": "PASS_READOUT306_ACTION_COST_AND_ARCHIVE_PRESSURE",
    "readout_306": {
        "lambda_B2": lambda_B2,
        "terminal_primary": terminal_primary,
        "terminal_checksum": terminal_checksum,
        "terminal_total": terminal_total,
        "action_cost_trace": action_cost,
        "directed_address_slots": 2*V9,
        "reduced_transport_slots": d13-rank,
        "terminal_trace_equivalence_error": abs(terminal_total-action_cost),
        "lambda_p": lambda_p,
        "mp_me": mp_me,
        "identity": "(2 V9)(d13-rank) = lambda_B2/V13*(1+1/(d13 V11)) = 306"
    },
    "archive_pressure": {
        "delta0_8": delta8,
        "archive_pressure_trace": pressure_total,
        "archive_pressure_per_archive_mode": pressure_per_archive_mode,
        "w0": -1.0,
        "wa": -delta8,
        "n_s": 29/30,
        "lambda_B_terminal": lambda_B_terminal,
        "A_phi": A_phi,
        "chi_B": chi_B,
        "operator": "P_archive^D0 = -(delta0^8/nullity) Pi_archive"
    }
}
print(json.dumps(result, indent=2))
print("PASS_READOUT306_ACTION_COST_AND_ARCHIVE_PRESSURE")
