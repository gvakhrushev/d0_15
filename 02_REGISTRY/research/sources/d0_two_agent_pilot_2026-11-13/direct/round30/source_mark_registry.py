#!/usr/bin/env python3
"""Explicit original Choi/CAR source moments at the new paid RAW checkpoint.

Descriptors specify bounded full-carrier observables, not an executed
detector, joint projective measurement or a replacement physical price.
The original periodic leaf catalogue supplies actual addresses/conventions.
"""
from pathlib import Path
from functools import lru_cache
from fractions import Fraction
import hashlib, json
import marked_source_schedule as s
P = Path(__file__).resolve().parent


@lru_cache(None)
def original_binding():
    return json.loads((s.D/'round11/PERIODIC_SOURCE_BINDING.json').read_text())


def choose_slot(bank, kind, walk=None):
    for i, slot in enumerate(s.g.namespace()['source_slots']):
        if slot['bank'] == bank and slot['kind'] == kind and slot['copy'] == 0 and (walk is None or slot['walk'] == walk):
            return i
    raise AssertionError((bank, kind, walk))


def raw_rank_two(slot_id, labels, coefficient, norm_upper, initial_raw_bits=0):
    slot = s.g.namespace()['source_slots'][slot_id]
    data = slot['source']
    a, z = labels
    assert 0 <= a < 1 << len(data) and 0 <= z < 1 << len(data) and a != z
    return {'source_slot': slot_id, 'bank': slot['bank'], 'kind': slot['kind'],
            'checkpoint': 'COMMON_SOURCE_RAW_FRAME_BEFORE_ANY_REPORT',
            'operator': 'coefficient*(|B r><B t|+|B t><B r|) tensor I_other',
            'coefficient': coefficient, 'operator_norm_upper': norm_upper,
            'logical_support_wires_LE': data,
            'physical_support_wires_LE': [s.b.physical_wire(q, initial_raw_bits) for q in data],
            'r_computational_label': a, 't_computational_label': z,
            'r_G_columns_LE': [(a >> i) & 1 for i in range(len(data))],
            't_G_columns_LE': [(z >> i) & 1 for i in range(len(data))],
            'B_on_support': 'tensor of actual G=[[sqrt(p),-p],[p,sqrt(p)]]',
            'fresh_CAR_RIGHT_identity_wires': slot.get('RIGHT', []),
            'fresh_CAR_RIGHT_physical_identity_wires': [s.b.physical_wire(q, initial_raw_bits) for q in slot.get('RIGHT', [])],
            'unknown_old_factor': 'exact identity, distinct from every fresh CAR RIGHT',
            'measurement_or_reader_executed': False}


def leaf_mark(site_index, template_index, choi_bank='f', initial_raw_bits=0):
    binding = original_binding()
    assert type(site_index) is int and 0 <= site_index < len(binding['site_bindings'])
    assert type(template_index) is int and 0 <= template_index < len(binding['leaf_templates'])
    assert choi_bank in ('f', 'q')
    row = binding['site_bindings'][site_index]
    template = binding['leaf_templates'][template_index]
    address = row['leaf_addresses_in_template_order'][template_index]
    if template['kind'] == 'Choi':
        slot = choose_slot(choi_bank, 'Choi', 'S1' if choi_bank == 'f' else 'T1')
        label = (address << 10) | (template['input'] << 5) | template['output']
        coefficient = 32784*template['anchor_moment_multiplier']
        out = raw_rank_two(slot, (0, label), {'integer': coefficient}, {'integer': coefficient}, initial_raw_bits)
        out['original_family'] = template['catalogue_kind']
        out['original_Julia_address_input_output'] = [address, template['input'], template['output']]
    else:
        assert template['kind'] == 'CAR' and template['cross_masks'][0] == 1
        grade = template['cross_masks'][1]
        assert grade in (0, 15)
        slot = choose_slot('q', 'CAR', 'T1')
        out = raw_rank_two(slot, ((address << 4)|1, (address << 4)|grade),
                          {'expression': '128/sqrt(p)'}, {'strict_lt_integer': 256}, initial_raw_bits)
        out['original_family'] = 'material_Psi'
        out['original_CAR_internal_site_and_grade'] = [address, grade]
    out.update({'external_SITE_index_used_only_to_resolve_original_catalogue': site_index,
                'field_leaf_name': template['name'], 'source_DAG_node': template['node'],
                'moment_is_unweighted_original_field_coordinate': True,
                'PF_or_inverse_PF_factor_inserted': False})
    return out


def build():
    plan = s.build(); stages = s.stages(); rows = []
    completions = {x['slot']: i for i, x in enumerate(stages) if x['kind'] == 'SOURCE'}
    common_index = plan['joint_RAW_source_checkpoint_after_stage_index']
    for i, slot in enumerate(s.g.namespace()['source_slots']):
        all_data = slot['source']+slot.get('RIGHT', [])
        row = {'slot': i, 'bank': slot['bank'], 'walk': slot['walk'], 'copy': slot['copy'],
               'kind': slot['kind'], 'source_completion_stage_index': completions[i],
               'source_completion_frame': 'computational; RAW marks require the later paid frame bridge',
               'original_RAW_mark_checkpoint_after_stage_index': common_index,
               'logical_resource_frame_wires': all_data,
               'physical_resource_frame_wires_at_m0': [s.b.physical_wire(q) for q in all_data],
               'physical_address_for_old_prefix_m': 'add m to each listed physical resource wire',
               'private_helpers_excluded_from_original_resource_frame': slot['private']}
        if slot['kind'] == 'Choi':
            row['basis_encoding'] = '(a<<10)|(i<<5)|j in source wire order, little endian'
            row['roles'] = {k: slot[k] for k in ('address', 'choi_input', 'choi_output')}
        else:
            row['basis_encoding'] = '(internal_site<<4)|grade on source, independent fresh RIGHT7'
            row['roles'] = {k: slot[k] for k in ('internal_SITE', 'grade', 'RIGHT')}
        rows.append(row)
    error = s.inventory()['common_mark_error_per_unit_norm']
    assert 32784*error < Fraction(1, 2**3215)
    assert 65568*error < Fraction(1, 2**3214)
    assert 256*error < Fraction(1, 2**3223)
    selected = {'f_Choi': choose_slot('f', 'Choi', 'S1'), 'q_Choi': choose_slot('q', 'Choi', 'T1'),
                'q_CAR': choose_slot('q', 'CAR', 'T1')}
    examples = []
    templates = original_binding()['leaf_templates']
    for wanted in ('u/', 'M/', 'Psi/'):
        # The original material leaf prefix is kept rather than invented.
        indices = [i for i, t in enumerate(templates) if t['name'].startswith(wanted)]
        if not indices and wanted == 'Psi/':
            indices = [i for i, t in enumerate(templates) if t['kind'] == 'CAR']
        assert indices
        examples.append(leaf_mark(0, indices[0]))
    pins = [Path(__file__), P/'marked_source_schedule.py', P/'COMMON_SOURCE_MARKED_PLAN.json',
            s.D/'round11/PERIODIC_SOURCE_BINDING.json', s.D/'round25/H1_NAMESPACE_PLAN.json',
            s.D/'round27/PREPARED_SOURCE_MOMENT_LAW_RU.md']
    return {'status': 'EXPLICIT_ORIGINAL_SOURCE_RAW_MARK_REGISTRY_ON_CANONICAL_CHECKPOINT',
            'source_slots': rows, 'selected_common_f_q_slots': selected,
            'original_leaf_templates': len(templates), 'original_external_SITE_addresses': len(original_binding()['site_bindings']),
            'original_leaf_bindings_resolved_by_API': len(templates)*len(original_binding()['site_bindings']),
            'example_original_marks': examples,
            'uniform_canonical_mark_error_per_unit_norm': s.g.encode_error(error),
            'original_mark_error_bounds': {'inverse_coframe_u': '2^-3215', 'proper_link_U': '2^-3214', 'material_Psi': '2^-3223'},
            'norms_retained': {'inverse_coframe_u': 32784, 'proper_link_U': 65568, 'material_Psi': '128/sqrt(p)<256'},
            'input_domain': 'arbitrary incoming SAM tensor old, including coherent entanglement; every fresh WORK remains at its declared generated checkpoint',
            'bound_type': 'operator norm of pulled-back effect; any bounded checkpoint O has <=2*eta_prefix*||O||',
            'original_readers_executed_or_retained_records_created': False,
            'same_checkpoint_does_not_imply_joint_projective_measurability_of_all_marks': True,
            'all_dirty_WORK_columns_or_internal_report_marks_identified': False,
            'unsplit_current_source_bank_identified': False,
            'source_sha256': {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in pins},
            'physical_C_closed': False, 'GR_closed': False}


def main():
    out = build()
    (P/'SOURCE_RAW_MARK_REGISTRY.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({'status': out['status'], 'slots': len(out['source_slots']),
                      'original_leaf_bindings': out['original_leaf_bindings_resolved_by_API'],
                      'selected_common_slots': out['selected_common_f_q_slots']}))


if __name__ == '__main__':
    main()
