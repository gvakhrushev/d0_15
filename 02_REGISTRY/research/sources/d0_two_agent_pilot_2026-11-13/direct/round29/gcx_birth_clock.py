#!/usr/bin/env python3
"""New G/CX-only RAW construction with one fresh helper and explicit clock.

The old symbolic 0,1,3 factors are nowhere addressed by the new word.
Omitting these placeholders from its definition is not a reset, partial
trace or a claimed physical equivalence of the two histories/prices.
An actual old RAW prefix/cut can be retained unchanged for any m>=0.
"""
from pathlib import Path
from collections import Counter
from fractions import Fraction
import hashlib, json, sys
import gcx_compiler as c
P = Path(__file__).resolve().parent
sys.path.insert(0, str(c.D/'round28'))
import fresh_aux_birth_clock as old_birth


def birth_blocks():
    blocks = old_birth.birth_blocks(c.old.namespace())
    h = c.old.namespace()['layout']['qubits']
    return blocks + [{'role': 'new_G_CX_gadget_helper_WORK', 'start': h, 'stop': h+1}]


def physical_wire(q, initial_raw_bits=0):
    """Actual append-order address, with all existing m wires unaddressed."""
    m = initial_raw_bits
    N = c.old.namespace()['layout']['qubits']
    assert type(m) is int and m >= 0
    assert type(q) is int and 0 <= q <= N and q not in (0, 1, 3)
    if q == 2705:
        return m
    if q == 2:
        return m+1
    if 4 <= q <= 2704:
        return m+q-2
    assert q >= 2706
    return m+q-3


def logical_wire(q, initial_raw_bits=0):
    m = initial_raw_bits
    N = c.old.namespace()['layout']['qubits']
    assert type(q) is int and type(m) is int and m >= 0 and 0 <= q < m+N-2
    if q < m:
        return None
    r = q-m
    if r == 0:
        return 2705
    if r == 1:
        return 2
    if 2 <= r <= 2702:
        return r+2
    return r+3


def physical_tree(tree, initial_raw_bits=0):
    op = tree['op']
    if op == 'seq':
        return c.nb.seq(*(physical_tree(x, initial_raw_bits) for x in tree['children']))
    if op == 'repeat':
        return c.nb.repeat(int(tree['count']), physical_tree(tree['child'], initial_raw_bits))
    assert op in ('G', 'CX')
    return c.nb.gate(op, *(physical_wire(q, initial_raw_bits) for q in tree['wires']))


def physical_blocks(initial_raw_bits=0):
    for tree in c.W_blocks():
        yield physical_tree(tree, initial_raw_bits)


def execution_stages(initial_raw_bits=0):
    """Complete finite iterator, not an execution of the giant program."""
    next_wire = initial_raw_bits
    for block in birth_blocks():
        for q in range(block['start'], block['stop']):
            wire = physical_wire(q, initial_raw_bits)
            assert wire == next_wire
            next_wire += 1
            yield {'kind': 'canonical_RAW_birth', 'wire': wire, 'logical_wire': q,
                   'role': block['role'], 'carrier_qubits_after': next_wire,
                   'isometry': 'psi -> psi tensor (sqrt(p),p)'}
    def primitives():
        for block in physical_blocks(initial_raw_bits):
            yield from old_birth.primitive_leaves(block)
    it = iter(primitives())
    previous = next(it)
    for gate in it:
        yield {'kind': 'square_unitary_edge', 'gate': previous}
        previous = gate
    yield {'kind': 'final_unitary_g', 'gate': previous}


def inventory():
    old = json.loads((c.D/'round25/GLOBAL_H1_PLAN.json').read_text())
    census = json.loads((c.old.B/'round58/CZ_EXACT_OCCURRENCES.json').read_text())
    assert census['status'] == 'PASS_A25_COMPLETE_LOGICAL_CZ_CENSUS'
    C = census['W_CZ_total']
    S_cz = census['W_CZ_old_SourceI_count']
    X_cz = census['W_CZ_old_CX_count']
    w = {k: int(v) for k, v in old['global_native_counts']['W_literal_echo'].items()}
    assert C == 1052744 and S_cz == 10527440 and X_cz == 14*C
    assert w['SourceI'] >= S_cz and (w['SourceI']-S_cz) % 2 == 0
    pairs = (w['SourceI']-S_cz)//2
    assert pairs == int(census['W_nonCZ_SourceI_pair_count'])
    k = c.production_compiler().k
    new = Counter({'G': w['G_port']+w['G_other']+32*k*C+16*k*pairs,
                   'CX': w['CX']-X_cz+8*C+2*pairs})
    rotations = 4*C+2*pairs
    e_replace = Fraction(rotations, 2**7432)
    e_old = old['compressed_reflection_error_bound']
    e_old = Fraction(int(e_old['numerator_hex'], 16), int(e_old['denominator_hex'], 16))
    return new, C, pairs, rotations, e_replace, e_old+e_replace


def build():
    new, C, pairs, rotations, e_replace, error = inventory()
    L = sum(new.values())
    n = sum(b['stop']-b['start'] for b in birth_blocks())
    assert n == 10407050782 and L.bit_length() == 11647
    assert e_replace < Fraction(1, 2**3244)
    assert error < Fraction(1, 2**3231)
    assert Fraction(67, 100)-error > Fraction(2, 3)
    assert error*2**3158 < Fraction(1, 2**73)
    assert 55*error*2**3158 < Fraction(1, 2**67)
    assert 55*error*2**3188 < Fraction(1, 2**37)
    pins = [Path(__file__), P/'gcx_compiler.py', P/'GCX_COMPILER_CHECK.json',
            c.D/'round25/GLOBAL_H1_PLAN.json', c.D/'round28/fresh_aux_birth_clock.py',
            c.old.B/'round57/GADGET_G_POWER_CERTIFICATE.json', c.old.B/'round58/CZ_EXACT_OCCURRENCES.json']
    return {'status': 'EXPLICIT_NEW_G_CX_ONLY_WORD_BIRTH_AND_CLOCK_PLAN',
            'exact_counts_depend_on_structural_provider_coverage': True,
            'native_alphabet': ['G', 'CX'], 'SourceI_calls': 0,
            'fresh_helper_logical_wire': c.old.namespace()['layout']['qubits'],
            'new_helper_is_RAW_not_selected_zero': True,
            'fresh_aux_contract_from_A28': True,
            'old_symbolic_placeholders_omitted_from_new_definition': [0, 1, 3],
            'no_old_input_is_erased_or_reset': True,
            'initial_RAW_prefix_size': 'any m>=0; all old coordinates are unaddressed',
            'original_SourceI_profile_or_Spin_frame_required_by_new_word': False,
            'logical_birth_blocks': birth_blocks(), 'total_RAW_births': n,
            'SAM_RAW_births': 2688, 'WORK_RAW_births': n-2688,
            'all_births_are_separate_before_first_unitary': True,
            'CZ_macro_replacements': C, 'SourceI_pair_replacements': str(pairs),
            'rotation_power_blocks': str(rotations),
            'native_counts': {k: str(v) for k, v in new.items()},
            'native_call_count_L': str(L), 'native_call_count_bit_length': L.bit_length(),
            'square_unitary_edges': str(L-1), 'clock_layers_N': str(n+L),
            'last_actual_g_logical': {'op': 'CX', 'wires': [2692, 2705]},
            'last_actual_g_physical': 'CX(m+2690,m)',
            'clock_dimension_over_initial_dimension': {'coefficient': str(L+1),
                'power_of_two_exponent': n, 'additive_constant': -1,
                'formula': '(L+1)*2^n-1'},
            'all_column_replacement_error_bound': c.old.encode_error(e_replace),
            'canonical_compressed_error_bound': c.old.encode_error(error),
            'compressed_scalar_gt': '2/3',
            'normalized_native_error_lt': '2^-73', 'scaled_lift_native_error_lt': '2^-67',
            'physical_unit_lift_native_error_lt': '2^-37',
            'normalization_scope': 'same owned fixed h=1/4,m=2688 candidate and A26 gain, not a full-price source estimate',
            'scalar_reason': 'real matrices, exact SAM control-only, all WORK (including aux/helper) canonically compressed, and I_old',
            'exact_reflection_or_inverse_echo_claimed': False,
            'old_internal_marks_or_heat_price_identified': False,
            'physical_old_cut_or_selected_full_Cost_Info_binding_proved': False,
            'giant_program_executed': False,
            'source_sha256': {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in pins},
            'physical_C_closed': False, 'GR_closed': False}


def main():
    out = build()
    (P/'GCX_BIRTH_CLOCK_PLAN.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({k: out[k] for k in ('status', 'total_RAW_births', 'native_call_count_bit_length',
                                        'CZ_macro_replacements', 'compressed_scalar_gt')}))


if __name__ == '__main__':
    main()
