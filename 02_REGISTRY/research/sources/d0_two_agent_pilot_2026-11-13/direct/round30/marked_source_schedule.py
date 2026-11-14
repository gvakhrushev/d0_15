#!/usr/bin/env python3
"""New schedule: prepare all sources, paid RAW frame, then seven reports.

At the common marked checkpoint the f and q banks are both untouched by
REPORT. The actual old-profile bridge B_R and its literal inverse are
counted, then the complete NEW word is compiled by the A29 transducer.
No equality of old/new clocks, internal marked histories or prices.
"""
from pathlib import Path
from collections import Counter
from fractions import Fraction
from functools import lru_cache
import hashlib, json, sys
P = Path(__file__).resolve().parent
D = P.parent
sys.path.insert(0, str(D/'round29'))
import gcx_birth_clock as b
c, g = b.c, b.c.old


@lru_cache(None)
def resource_wires():
    wires = []
    for slot in g.namespace()['source_slots']:
        wires.extend(slot['source'])
        if slot['kind'] == 'CAR':
            wires.extend(slot['RIGHT'])
    assert len(wires) == len(set(wires)) == 29848
    l = g.namespace()['layout']
    excluded = set(l['SAM']+l['SITE']+l['SC6_selectors']+[l['port'], l['aux_arbitrary'], 0, 1, 3, l['qubits']])
    assert not set(wires).intersection(excluded)
    assert not set(wires).intersection(q for s in g.namespace()['source_slots'] for q in s['private'])
    return tuple(wires)


def stages():
    plan = g.namespace()
    out = [{'kind': 'SITE'}]
    for ri, report in enumerate(plan['reports']):
        out.append({'kind': 'SIGMA', 'report': ri})
        out.extend({'kind': 'SOURCE', 'slot': si} for si in report['source_slots'])
    out.extend([{'kind': 'RAW_RESOURCE_FRAME', 'intrinsic_inverse_depth': 0},
                {'kind': 'RAW_RESOURCE_FRAME', 'intrinsic_inverse_depth': 1}])
    out.extend({'kind': 'REPORT', 'report': ri} for ri in range(7))
    out.extend([{'kind': 'PORT_ZERO'}, {'kind': 'SC6'}])
    return out


def stage_blocks(stage, depth=0):
    assert type(depth) is int and depth >= 0
    if stage['kind'] != 'RAW_RESOURCE_FRAME':
        yield from g.stage_blocks(stage, g.namespace(), depth)
        return
    actual_depth = depth+stage['intrinsic_inverse_depth']
    wires = resource_wires()
    for q in (reversed(wires) if actual_depth % 2 else wires):
        yield g.invert(c.nb.gate('G', q), actual_depth, g.namespace())


def A_profile_blocks(depth=0):
    schedule = stages()
    for stage in (reversed(schedule) if depth % 2 else schedule):
        yield from stage_blocks(stage, depth)


def W_profile_blocks():
    """Intermediate G/CX/SourceI description, before the actual replacement."""
    yield from A_profile_blocks()
    l = g.namespace()['layout']
    yield c.nb.z_word(l['port'], l['port'], tuple(l['spin']))
    yield from A_profile_blocks(1)


def W_blocks():
    yield from c.production_compiler().stream(W_profile_blocks())


def source_checkpoint_blocks():
    """Exact new G/CX prefix ending after the forward paid B_R bridge."""
    def profile():
        for stage in stages():
            yield from stage_blocks(stage)
            if stage == {'kind': 'RAW_RESOURCE_FRAME', 'intrinsic_inverse_depth': 0}:
                return
        raise AssertionError('missing checkpoint')
    yield from c.production_compiler().stream(profile())


def execution_stages(initial_raw_bits=0):
    next_wire = initial_raw_bits
    for block in b.birth_blocks():
        for q in range(block['start'], block['stop']):
            wire = b.physical_wire(q, initial_raw_bits)
            assert wire == next_wire
            next_wire += 1
            yield {'kind': 'canonical_RAW_birth', 'wire': wire, 'logical_wire': q,
                   'role': block['role'], 'carrier_qubits_after': next_wire,
                   'isometry': 'psi -> psi tensor (sqrt(p),p)'}
    def primitives():
        for block in W_blocks():
            yield from b.old_birth.primitive_leaves(b.physical_tree(block, initial_raw_bits))
    it = iter(primitives()); previous = next(it)
    for gate in it:
        yield {'kind': 'square_unitary_edge', 'gate': previous}
        previous = gate
    yield {'kind': 'final_unitary_g', 'gate': previous}


def fraction(encoded):
    return Fraction(int(encoded['numerator_hex'], 16), int(encoded['denominator_hex'], 16))


def translate_counts(old, cz_count, cz_source_count):
    assert (old['SourceI']-cz_source_count) % 2 == 0
    pairs = (old['SourceI']-cz_source_count)//2
    assert pairs >= 0
    k = c.production_compiler().k
    new = Counter({'G': old['G_port']+old['G_other']+16*k*pairs+32*k*cz_count,
                   'CX': old['CX']-6*cz_count+2*pairs})
    return new, 2*pairs+4*cz_count


def inventory():
    old = json.loads((D/'round25/GLOBAL_H1_PLAN.json').read_text())
    decode = lambda v: Counter({key: int(value) for key, value in v.items()})
    components = {k: decode(v) for k, v in old['global_native_counts']['components'].items()}
    r = len(resource_wires())
    # B_R;literal inverse B_R in A; each actual primitive inverted again in A^-1.
    delta_W = Counter({'G_port': 3*r, 'G_other': r, 'CX': 18*r, 'SourceI': 24*r})
    W = decode(old['global_native_counts']['W_literal_echo'])+delta_W
    new_W, rotations_W = translate_counts(W, 1052744, 10527440)
    before = sum((components[k] for k in ('SITE', 'SIGMA7', 'Choi1260', 'CAR112')), Counter())
    before.update({'G_other': r})
    new_before, rotations_before = translate_counts(before, 0, 0)
    parts = old['conditional_canonical_input_error_components']
    eta_sources = sum((fraction(parts[k]) for k in ('SITE_once', 'Choi1260', 'CAR112')), Fraction())
    eta_all = fraction(old['canonical_input_error_bound'])
    eps_W = Fraction(rotations_W, 2**7432)
    eps_before = Fraction(rotations_before, 2**7432)
    return {'W_old_profile': W, 'W_new': new_W, 'W_rotations': rotations_W,
            'checkpoint_old_profile': before, 'checkpoint_new': new_before,
            'checkpoint_rotations': rotations_before,
            'eta_common_old': eta_sources, 'eta_common_new': eta_sources+eps_before,
            'common_mark_error_per_unit_norm': 2*(eta_sources+eps_before),
            'full_compressed_error': 2*eta_all+eps_W,
            'replacement_error': eps_W, 'added_old_profile_counts': delta_W}


def build():
    inv = inventory(); schedule = stages(); n = sum(z['stop']-z['start'] for z in b.birth_blocks())
    L = sum(inv['W_new'].values()); j = sum(inv['checkpoint_new'].values())
    assert L.bit_length() == 11647 and n+L < 2**11647
    assert 0 < j < L-1
    assert inv['common_mark_error_per_unit_norm'] < Fraction(1, 2**3231)
    assert inv['full_compressed_error'] < Fraction(1, 2**3231)
    assert inv['replacement_error'] < Fraction(1, 2**3244)
    assert Fraction(67, 100)-inv['full_compressed_error'] > Fraction(2, 3)
    assert sum(s['kind'] == 'SOURCE' for s in schedule) == 1372
    frame_index = schedule.index({'kind': 'RAW_RESOURCE_FRAME', 'intrinsic_inverse_depth': 0})
    assert frame_index == 1380 and all(s['kind'] != 'REPORT' for s in schedule[:frame_index+1])
    pins = [Path(__file__), D/'round29/gcx_compiler.py', D/'round29/gcx_birth_clock.py',
            D/'round25/global_h1.py', D/'round25/GLOBAL_H1_PLAN.json', D/'round25/H1_NAMESPACE_PLAN.json',
            D/'round27/PREPARED_SOURCE_MOMENT_LAW_RU.md', c.old.B/'round57/GADGET_G_POWER_CERTIFICATE.json',
            c.old.B/'round58/CZ_EXACT_OCCURRENCES.json']
    return {'status': 'NEW_COMMON_SOURCE_RAW_FRAME_MARKED_SCHEDULE',
            'A_forward_stages': schedule, 'source_slot_count': 1372,
            'source_frame_logical_wires': list(resource_wires()),
            'source_frame_wire_count': len(resource_wires()),
            'source_frame_excludes_SAM_external_SITE_private_helpers_report_labels_old': True,
            'joint_RAW_source_checkpoint_after_stage_index': frame_index,
            'joint_RAW_source_checkpoint_native_prefix_calls': str(j),
            'joint_RAW_source_checkpoint_clock_layer': str(n+j),
            'no_REPORT_executed_at_joint_RAW_source_checkpoint': True,
            'explicit_G_frame_and_paid_literal_inverse_inserted': True,
            'total_RAW_births': n, 'new_native_counts': {k: str(v) for k, v in inv['W_new'].items()},
            'new_native_call_count': str(L), 'new_native_call_count_bit_length': L.bit_length(),
            'new_clock_layers': str(n+L),
            'clock_dimension_over_initial_dimension': {'coefficient': str(L+1), 'power_of_two_exponent': n, 'additive_constant': -1},
            'checkpoint_native_counts': {k: str(v) for k, v in inv['checkpoint_new'].items()},
            'added_W_old_profile_counts': dict(inv['added_old_profile_counts']),
            'original_source_isometry_prefix_error': g.encode_error(inv['eta_common_old']),
            'new_source_isometry_prefix_error': g.encode_error(inv['eta_common_new']),
            'common_mark_error_per_unit_operator_norm': g.encode_error(inv['common_mark_error_per_unit_norm']),
            'full_compressed_error': g.encode_error(inv['full_compressed_error']),
            'all_column_replacement_error': g.encode_error(inv['replacement_error']),
            'scalar_corner_gt': '2/3', 'old_native_words_exactly_commute_claimed': False,
            'reordering_scope': 'ideal canonical-fibre hybrid, arbitrary SAM/old coherence, exact source-only shared-register identities',
            'original_mark_frame': 'B_R O_computational B_R* on the explicitly enumerated fresh source DATA',
            'actual_reader_or_output_record_executed': False,
            'unsplit_current_bank_supplied': False,
            'full_all_dirty_column_T2_established': False,
            'old_prices_or_marked_histories_equated': False,
            'source_sha256': {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in pins},
            'physical_C_closed': False, 'GR_closed': False}


def main():
    out = build()
    (P/'COMMON_SOURCE_MARKED_PLAN.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({k: out[k] for k in ('status', 'source_slot_count', 'source_frame_wire_count',
                                        'new_native_call_count_bit_length', 'scalar_corner_gt')}))


if __name__ == '__main__':
    main()
