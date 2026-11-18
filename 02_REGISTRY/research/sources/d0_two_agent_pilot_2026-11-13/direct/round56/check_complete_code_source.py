#!/usr/bin/env python3
"""Changed application checks; not a replay of the giant native history."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json
import sys
import complete_code_source as a

sys.dont_write_bytecode = True
P = Path(__file__).resolve().parent
sys.path.insert(0, str(a.D/'round47'))
import full_vector_controls as mg


def main():
    Q, p = mg.e.Q4, mg.e.SIN
    beta = 2*p*p
    assert p+p*p == Q(1)
    assert beta-Q(1) == -p**3
    assert (2*F(309, 500))**4 > 2
    assert 4*2688 < 104**2

    # Exact coefficient identities, including independent-beta and
    # source orientation controls. H/J here are algebraic test operands,
    # not claimed to be production graph values.
    cases = 0
    for dH in (Q(0), Q(1), p, Q(F(-7, 3))):
        for dJ in (Q(0), Q(1), p*p, Q(F(11, 7))):
            master = dH+dJ
            oriented_stat = beta*dH+dJ
            assert oriented_stat == master-p**3*dH
            for H in (Q(1), p):
                dbeta = Q(F(2, 7))
                moving = oriented_stat+H*dbeta
                assert moving-oriented_stat == H*dbeta != Q(0)
                cases += 1
    assert beta*Q(1) != Q(1)  # det^-beta incorrectly rescales the J row.
    assert -(beta+Q(1)) != beta+Q(1)  # opposite global orientation.
    assert beta != Q(1)  # throwing away the heat correction is not exact.
    B, dB, gain, dgain = F(3), F(5), F(2), F(7)
    assert dB/gain != dB/gain-B*dgain/gain**2

    zero = a.task.FieldCentre()
    shifted_values = [F(0)]*2688
    shifted_values[0] = F(1, 1 << 34)
    shifted_values[-1] = -F(1, 1 << 35)
    shifted = a.task.FieldCentre(tuple(shifted_values))
    packets = []
    for field in (zero, shifted):
        for arm in ('Pf', 'Qf', 'Qb', 'Pb'):
            pair = [a.section_packet(a.task.Request(field, a.task.Label(arm=arm, sign=s, axis=17)))
                    for s in (-1, 1)]
            assert pair[0]['request_sha256'] != pair[1]['request_sha256']
            for key in ('field_name_sha256', 'actual_padded_lengths_hex', 'clock_layers_N_hex',
                        'late_retention_pairs', 'clock_dimension_formula'):
                assert pair[0][key] == pair[1][key]
            assert all(x['determinant_power'] == -1 and x['full_graded_heat_modes'] == '425*D'
                       and x['input_rank'] == 1 and not x['whole_physical_Cost_Info_identified']
                       for x in pair)
            packets.extend(pair)
    assert packets[0]['field_name_sha256'] != packets[8]['field_name_sha256']

    # Recompute the heat factor independently from the clock dimension
    # inequality, retaining all four n-qubit stage ranks.
    b = a.bounds()
    fam = a.task.FieldTask(zero).family
    cfg = fam.cfg
    gamma0 = F(8, 3)*F(1, 1 << (20+3208))
    heat = F(1248, 359)*F(1, 1 << (cfg['K']//4))/gamma0
    assert heat == b['analytic_heat_full_raw_dual'] < F(1, 1 << 40672)
    assert cfg['Nbase'] != a.task.paid.paid.production_configuration()['Nbase']
    assert cfg['K'] == 175604 and cfg['Nbase'].bit_length() == 30833
    finite = F(6*cfg['Nbase'], 359)*F(1, 1 << (cfg['K']//4))/(F(1, 1 << 1700)*gamma0)
    assert finite == b['finite_native_heat_per_axis']
    assert b['master_full_raw_dual'] < F(1, 1 << 34)
    assert b['finite_native_statistical_four_axis_l2'] < F(1, 1 << 101)

    # Small exact layout algebra: every prefix square stage contributes
    # 2^n, with all n early births and K actual retention pairs present.
    for n in range(1, 6):
        for body in (4, 11, 23):
            for K in range(1, 6):
                stages = [1 << j for j in range(n)]
                stages += [1 << n]*body
                for j in range(K):
                    stages += [1 << (n+j), 1 << (n+j+1)]
                D = sum(stages)
                assert D == (1 << n)*(body-2+3*(1 << K))-1
                assert D >= 1 << (n+K)

    source = a.build()
    for name, digest in source['source_sha256'].items():
        assert sha256(Path(name).read_bytes()).hexdigest() == digest
    out = {'status': 'PASS_A56_ACTUAL_GRAPH_STATISTICAL_ORIENTATION_AND_DISTINCT_SOURCE_BUDGETS',
           'exact_source_coefficient_cases': cases, 'actual_bound_native_pair_packets': len(packets),
           'small_exact_clock_dimension_checks': 75,
           'new_Nbase_and_full_heat_modes_retained': True,
           'free_beta_wrong_determinant_power_wrong_orientation_and_moving_gain_controls': True,
           'analytic_master_and_oriented_statistical_full_raw_dual_lt': '2^-34',
           'analytic_heat_full_raw_dual_lt': '2^-40672',
           'finite_native_MG2_statistical_four_axis_l2_lt': '2^-101',
           'full_native_skew_or_physical_C_binding_claimed': False,
           'physical_C_closed': False, 'GR_closed': False,
           'source_sha256': {**source['source_sha256'], str(Path(__file__)): sha256(Path(__file__).read_bytes()).hexdigest()}}
    (P/'COMPLETE_CODE_SOURCE_CHECK.json').write_text(json.dumps(out, indent=2)+'\n')
    print(out['status'])


if __name__ == '__main__':
    main()
