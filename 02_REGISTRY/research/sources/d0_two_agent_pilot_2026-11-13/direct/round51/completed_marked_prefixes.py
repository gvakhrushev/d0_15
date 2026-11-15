#!/usr/bin/env python3
"""Actual A49 forward prefixes at completed CODE-disjoint processor stages.

The pre-Qf original SOURCE mark is kept separately. Its derivative is not
renamed the matched geometric jet. This supplies a declared finite list
of full retained prefixes, not admission of all original descriptor marks.
"""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json, sys

sys.dont_write_bytecode = True
P = Path(__file__).resolve().parent
D = P.parent
sys.path.insert(0, str(D/'round49'))
import two_bit_paid_family as paid
g = paid.source


def processor_stages():
    schedule = g.previous.stages()
    boundary = schedule.index({'kind': 'RAW_RESOURCE_FRAME', 'intrinsic_inverse_depth': 0})
    return schedule[boundary+1:]


def registry():
    out = [{'name': 'SOURCE_after_Qf', 'processor_stage_count': 0,
            'frame': 'RAW resource frame, after independently paid Qf control'}]
    for index, stage in enumerate(processor_stages(), 1):
        kind = stage['kind']
        name = ('REPORT_%d_complete' % stage['report'] if kind == 'REPORT'
                else 'RAW_frame_return' if kind == 'RAW_RESOURCE_FRAME' else kind)
        out.append({'name': name, 'processor_stage_count': index,
                    'last_completed_stage': stage})
    assert len(out) == 12 and out[-1]['name'] == 'SC6'
    return out


def descriptor(name):
    found = [x for x in registry() if x['name'] == name]
    assert len(found) == 1, name
    return found[0]


def processor_profile_blocks(name):
    for stage in processor_stages()[:descriptor(name)['processor_stage_count']]:
        yield from g.stage_blocks(stage)


def processor_native_blocks(name):
    # A49's first Q cut has pending=0. Each selected completed prefix must
    # also close that same transducer; unfinished internal marks are rejected.
    for tree in g.compiler().stream(processor_profile_blocks(name)):
        yield g.physical_tree(tree)


def assembled_prefix(core_factory, processor_factory, control_factory, cfg,
                     *,axis, sign, name):
    """Literal prefix of matched A49 history through the requested frontier.

    All initial births and the rest of the same A49 clock remain in its
    parent execution. This iterator contains square native gates only.
    """
    assert sign in (-1, 0, 1)
    yield from paid.pad.counted_pad(lambda:control_factory(axis, sign),
                                   cfg['controlL'], cfg['sam'])
    # No core padding is due here: that identity is emitted after the
    # whole return branch, later in A49. Do not move it to this mark.
    yield from core_factory()
    if name == 'SOURCE_before_Qf':
        return
    yield from paid.pad.counted_pad(lambda:control_factory(axis, -sign),
                                   cfg['controlL'], cfg['sam'])
    yield from processor_factory(name)


def native_prefix_blocks(name, axis=0, sign=0):
    assert name == 'SOURCE_before_Qf' or name in [x['name'] for x in registry()]
    yield from assembled_prefix(g.source_prefix_blocks, processor_native_blocks,
                                paid.raw_control_factory, paid.production_configuration(),
                                axis=axis, sign=sign, name=name)


def decode(x):
    return F(int(x['numerator_hex'], 16), int(x['denominator_hex'], 16))


def bounds():
    a48 = json.loads((D/'round48/ACTUAL_FULL_VECTOR_SOURCE_JET.json').read_text())
    source = g.upper_inventory_and_error()
    report = json.loads((D/'round17/GLOBAL_REPORT_COMPILATION.json').read_text())
    known = report['seven_report_all_known_approximate_macros']
    assert known % 7 == 0
    # Complete retained A17 target, including factories, failure and READY.
    # Uniform bound for all 12 declared stages; use all 8 REPORTs even for
    # an earlier mark. RAW inverse/PORT/SC6 are exact in SourceI profile.
    eD = F(8*(known//7), 1 << 4096) + source['replacement_error']
    eB = source['full_SOURCE_DATA_fibre_prefix_error']
    eP = decode(paid.control.control_plan()['control_vs_exp_tX_error'])
    jet_B = decode(a48['full_axis_jet_error'])
    sigma, t = F(1, 1 << 80), F(1, 1 << 1700)
    M1 = 1748
    # Dhat is common in both arms and exactly CODE-disjoint. Its error
    # multiplies the genuine derivative M1, never 1/(sigma*t).
    jet = jet_B + eD*M1
    centre = sigma*104*M1 + eB + eD
    # For Fbar=(Fhat+ + Fhat-)/2: analytic double commutator norm <=4,
    # midpoint displacement <=2 t², and two independent control errors.
    midpoint = centre + 2*eP + 2*t*t
    # (F+*OF+ - F-*OF-)/(2 sigma t)=Fbar*O J + J*O Fbar,
    # ||Fbar||<=1; use the full map, not success-normalized probabilities.
    effect = 2*jet + 2*M1*midpoint
    assert eD < F(1, 1 << 4058)
    assert centre < F(1, 1 << 62) and midpoint < F(1, 1 << 62)
    assert jet < F(1, 1 << 44) and effect < F(1, 1 << 43)
    return {'all_completed_processor_prefix_error': eD,
            'full_prefix_centre_error': centre,
            'full_prefix_midpoint_error': midpoint,
            'full_prefix_finite_axis_jet_error': jet,
            'norm_one_joint_effect_finite_axis_jet_error': effect}


def build():
    paths = [Path(__file__), D/'round17/report_assembly.py',
             D/'round17/GLOBAL_REPORT_COMPILATION.json',
             D/'round48/two_bit_global_source.py',
             D/'round48/ACTUAL_FULL_VECTOR_SOURCE_JET.json',
             D/'round49/two_bit_paid_family.py',
             D/'round50/INDEPENDENT_PRICE_ROWS_PLAN.json',
             g.t.loc.B/'round86/B86_ORIGINAL_MARK_ADMISSION_RU.md',
             g.t.loc.B/'round91/B91_FULL_VECTOR_JET_AND_SOURCE_FIBRE_RU.md']
    return {'status': 'CONSTRUCTED_TWELVE_COMPLETED_MATCHED_A49_PREFIXES',
            'prefixes': registry(),
            'earlier_SOURCE_before_Qf_preserved_as_distinct_prefix': True,
            'matched_geometric_jet_claim_for_SOURCE_before_Qf': False,
            'full_processor_and_fresh_source_remainder_retained': True,
            'factory_failed_READY_and_private_columns_not_discarded': True,
            'domain': 'all SOURCE DATA and SITE columns on declared SOURCE-private and processor/factory RAW fibre, with external reference; selected A23 extension',
            'production_provider_is_prefix_of_same_matched_A49_gate_history': True,
            'new_birth_gate_or_clock_change': False,
            'all_completed_processor_error_lt': '2^-4058',
            'full_prefix_centre_error_lt': '2^-62',
            'full_prefix_finite_axis_jet_error_lt': '2^-44',
            'norm_one_joint_effect_finite_axis_jet_error_lt': '2^-43',
            'norm_one_means_unconditioned_full_effect_not_success_normalization': True,
            'bounds': {k:paid.encode(v) for k,v in bounds().items()},
            'all_original_Dnu_or_early_unfinished_marks_identified': False,
            'same_FN_fibre_at_distinct_logical_controls_claimed': False,
            'original_Vh_norm_and_full_Cost_Info_closed': False,
            'production_word_or_targets_evaluated': False,
            'physical_C_closed': False, 'GR_closed': False,
            'source_sha256': {str(p):sha256(p.read_bytes()).hexdigest() for p in paths}}


if __name__ == '__main__':
    result = build()
    (P/'COMPLETED_MARKED_PREFIX_PLAN.json').write_text(json.dumps(result, indent=2)+'\n')
    print(result['status'])
