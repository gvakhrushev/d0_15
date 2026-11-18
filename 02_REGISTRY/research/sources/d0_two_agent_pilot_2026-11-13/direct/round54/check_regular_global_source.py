#!/usr/bin/env python3
"""Changed integration: field routing, literal order, uniform costs and cuts.

Fixtures execute chronology only. Actual interval/power proofs are pinned
A53/B103/B104; selected real native trees exercise the G/CX replacement.
No giant production SOURCE or exact unpadded total is evaluated.
"""
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
from itertools import islice, zip_longest
from hashlib import sha256
from unittest.mock import patch
import json
import regular_global_source as g

P = Path(__file__).resolve().parent
s = g.s
old = s.old
nb = s.nb
local = s.local
zero = s.t.FieldCentre()
offsets = tuple(F((j % 13)-6, 1 << 36) for j in range(2688))
field = s.t.FieldCentre(offsets)
native = s.Sources(field)
source = g.GlobalSource(field)
assert source.field is field and source.sources.components.field is field

# Original DATA/private and CODE binding for EVERY actual source copy.
plan = g.namespace()
lay = plan['layout']
assert plan == g.previous.namespace()
assert g.birth_blocks() == g.previous.birth_blocks()
assert plan['SC6_local_to_global'] == g.previous.previous.namespace()['SC6_local_to_global']
assert sum(b['stop']-b['start'] for b in g.birth_blocks()) == 11893774624
seen = set(lay['SAM'])
kinds = Counter()
route = []

class RouteProbe:
    def choi_blocks(self, bank, bound, depth):
        route.append(('Choi', bank, bound, depth)); return iter(())

    def car_blocks(self, bank, bound, depth):
        route.append(('CAR', bank, bound, depth)); return iter(())

probe = g.GlobalSource(field)
probe.sources = RouteProbe()
for i, slot in enumerate(plan['source_slots']):
    kinds[slot['kind']] += 1
    if slot['kind'] == 'Choi':
        bound = g.ns.choi_layout(plan, slot)
        old.validate_choi(bound)
        wires = old.data(bound)+old.private(bound)
    else:
        bound = g.ns.car_layout(plan, slot)
        pv = [bound['predicate_flag'], *bound['predicate_work']]
        old.vac.validate(bound, [*pv, bound['native_aux_arbitrary']])
        wires = bound['internal_SITE']+bound['grade']+bound['RIGHT']+pv
    assert not seen.intersection(wires)
    assert plan['old_compiler_helper'] not in wires
    assert bound['SAM'] == lay['SAM']
    seen.update(wires)
    for depth in (0, 1, 2):
        list(probe.stage_blocks({'kind': 'SOURCE', 'slot': i}, depth))
        assert route[-1] == (slot['kind'], slot['bank'], bound, depth)
assert kinds == {'Choi': 1440, 'CAR': 128}
assert len(route) == 4704

# No fixed and variable link address overlap. All six offsets, not an xy
# family cache, are selected independently for every variable f group.
_, cat = old.link.fixed_and_catalogue()
variable_groups = cat['f']['variable']
assert len(variable_groups) == 256
for bank, section in cat.items():
    fixed_addresses = [e['address'] for e in section['fixed']]
    variable_addresses = [e['address'] for e in section['variable']]
    assert len(set(fixed_addresses)) == len(fixed_addresses)
    assert len(set(variable_addresses)) == len(variable_addresses)
    assert not set(fixed_addresses).intersection(variable_addresses)
    assert not variable_addresses or bank == 'f'
for group in variable_groups:
    selected = field.selected(group['indices_by_generator'])
    assert selected == tuple(offsets[j] for j in group['indices_by_generator'])
    for digits in ((0,)*6, (3,)*6, (0, 1, 2, 3, 0, 1)):
        entry = s.link.variable_entry(group, digits)
        for j, index in enumerate(group['indices_by_generator']):
            assert entry['SAM_indices'][j] == index
            assert entry['SAM_indices'][6+j] == 2688+index
            assert entry['SAM_pattern'][j]+2*entry['SAM_pattern'][6+j] == digits[j]

# Exercise the actual fixed/new bank splice with finite noncommuting
# fixtures; outer inverse depths remain literal, including depth 2/3.
toy = {'port': 90, 'spin': [91, 92]}
fixed_word = nb.seq(nb.gate('G', 4), nb.gate('CX', 4, 5))
variable_word = nb.seq(nb.gate('G', 6), nb.gate('CX', 6, 7))
fixture_cat = {'f': {'fixed': [{'address': 1}, {'address': 2}], 'variable': [{}]}}
calls = []

def fixed_provider(bound, entry, reverse=False):
    calls.append(('fixed', entry['address'], reverse))
    yield local.invert(fixed_word, int(reverse), toy)

def variable_provider(actual_field, bound, reverse=False):
    assert actual_field is field
    calls.append(('variable', reverse))
    yield local.invert(variable_word, int(reverse), toy)

splice = []
with patch.object(old.link, 'fixed_and_catalogue', lambda: ({}, fixture_cat)), \
     patch.object(old.link, 'sector_blocks', fixed_provider), \
     patch.object(s.link, 'variable_bank_blocks', variable_provider):
    forward = [fixed_word, fixed_word, variable_word]
    for depth in range(4):
        calls.clear()
        actual = list(native.link_blocks('f', toy, depth))
        reference = [local.invert(x, depth, toy)
                     for x in (reversed(forward) if depth % 2 else forward)]
        # Nested exact seq syntax need not coincide; primitive streams do.
        def flatten(stream):
            for tree in stream:
                yield from nb.expand(tree, 200000)
        assert list(flatten(actual)) == list(flatten(reference))
        if depth % 2:
            assert calls == [('variable', True), ('fixed', 2, True), ('fixed', 1, True)]
        else:
            assert calls == [('fixed', 1, False), ('fixed', 2, False), ('variable', False)]
        splice.append({'depth': depth, 'blocks': len(actual)})

# Level-nine uses the owned B39 recursion. Independently compare the
# actual new recursion to its original finite DAG at small exact levels.
adapter_toy = {'SAM': [], 'address': [], 'choi_input': [], 'choi_output': [1],
    'branch': 0, 'phase_rebit': 2, 'comparator_scratch': [3], 'port': 4,
    'spin': [5, 6], 'aux_arbitrary': 7, 'oldRIGHT_witness': 8, 'qubits': 9}
V = nb.selective_rotation([0], [1], 1, 1, 4, (5, 6))

class ToySources(s.Sources):
    def omega_blocks(self, bank, bound=None, depth=0):
        for tree in reversed(V['children']) if depth % 2 else V['children']:
            yield local.invert(tree, depth, adapter_toy)

fixture = ToySources(field)
adapter_checks = []
with patch.object(old, 'inputs', lambda: {'phase': {'phase_k': '1'},
                 'level9': {'correction_l': '1'}, 'h_k': 1}):
    for levels in range(3):
        for depth in range(3):
            actual = fixture.half_blocks('f', adapter_toy, levels, depth)
            ref = old.old.adapter.adapter_blocks(old.old.adapter_layout(adapter_toy),
                                                  V, 1, 1, 1, levels, bool(depth % 2))
            ref = (local.invert(tree, depth-depth % 2, adapter_toy) for tree in ref)
            count = 0
            for a, b in zip_longest(flatten(actual), flatten(ref)):
                assert a == b
                count += 1
            adapter_checks.append({'levels': levels, 'depth': depth, 'leaves': count})

# Check global forward/inverse schedule and both literal marks without
# pretending to compile the enormous components. Marker stages are explicit.
class ScheduleProbe(g.GlobalSource):
    def stage_blocks(self, stage, depth=0):
        yield {'op': 'STAGE_FIXTURE', 'stage': stage, 'depth': depth}

stages = g.schedule()
walk = list(ScheduleProbe(field).profile_with_cuts())
stage_walk = [z for z in walk if z['op'] == 'STAGE_FIXTURE']
assert [(z['stage'], z['depth']) for z in stage_walk] == (
    [(z, 0) for z in stages]+[(z, 1) for z in reversed(stages)])
marks = [z['name'] for z in walk if z['op'] == 'B82_CUT']
assert marks == list(g.previous.previous.p43.CUTS)
for i, item in enumerate(walk):
    if item['op'] == 'B82_CUT':
        prior = walk[i-1]
        assert prior['op'] == 'STAGE_FIXTURE'
        assert prior['stage']['kind'] == 'RAW_RESOURCE_FRAME'

# Fixed B93 links use exactly the old fixed-sector bound, excluding its
# variable parts. Reconstruct the saved reference banks independently.
upper = s.inventory_upper()
fixed = s.fixed_link_sector_upper()
saved = old.inputs()['proper_upper']['bank_bounds']
for bank, section in cat.items():
    if not section['variable']:
        actual_bound = old.times(fixed, len(section['fixed']))
        assert actual_bound == old.counter(saved[bank]['forward_componentwise_upper_hex'], 16)
for bank in s.BANKS:
    for kind in ('Choi', 'CAR'):
        row = upper[kind][bank]
        assert row['source_literal_inverse_upper'] == old.inv(row['source_forward_upper'])
total = old.site.inventory(old.inputs()['site'])['SITE_forward']
for slot in plan['source_slots']:
    total.update(upper[slot['kind']][slot['bank']]['source_forward_upper'])
assert total == upper['all_SOURCE_forward_componentwise_upper']
u = g.upper_inventory_and_error()
assert u['source_error'] < F(1, 1 << 3423)
assert u['full_SOURCE_DATA_fibre_prefix_error'] < F(1, 1 << 3423)
assert u['full_canonical_compressed_error'] < F(1, 1 << 3421)
assert u['replacement_error'] < F(1, 1 << 15800)
assert all(type(v) is int and v > 0 for v in u['W_G_CX_upper'].values())

# Real global coframe/CAR words, including intrinsic inverses, meet the
# closed SourceI grammar in G/CX replacement. Whole masks stay lazy.
actual_checks = []
cfslot = next(z for z in plan['source_slots'] if z['kind'] == 'Choi' and z['bank'] == 'f')
caslot = next(z for z in plan['source_slots'] if z['kind'] == 'CAR' and z['bank'] == 'q')
cfbound = g.ns.choi_layout(plan, cfslot)
cabound = g.ns.car_layout(plan, caslot)
cfrow = next(r for r in s.t.coframe_rows('f') if r['coordinates'])
carrow = next(r for r in s.t.material_rows('q') if r['SAM_indices'])
cfunits = native.components.coframe_units(cfrow, (0, 1, 2, 3), cfbound)
caunits = native.components.material_units('q', carrow, cabound)
for kind, bound, units in [('coframe', cfbound, cfunits), ('CAR', cabound, caunits)]:
    protected = set(bound['SAM'])
    protected.update(bound['address'] if kind == 'coframe' else bound['internal_SITE'])
    protected.update([bound['oldRIGHT_witness']] if kind == 'coframe' else bound['RIGHT'])
    for extra in (0, 1, 2):
        for unit, intrinsic in units:
            # A unit streams each complete Walsh term as its own tree;
            # the first two actual terms suffice to test binding/closure.
            for tree in islice(local.cf.unit_blocks(unit, intrinsic+extra, bound), 2):
                transformed, pending, census = g.compiler().transform(tree, 0)
                assert pending == 0
                for leaf in nb.leaves(transformed):
                    assert leaf['op'] in ('G', 'CX')
                    assert leaf['wires'][-1] not in protected
                    for wire in leaf['wires']:
                        g.physical_wire(wire)
            actual_checks.append({'kind': kind, 'literal_depth': intrinsic+extra})

# A newly general Julia sector is the one changed grammar that A48 could
# not cover. Compute its actual 496 angles and pass real positive/inverse
# Walsh terms through the original global compiler, with all CODE read-only.
group = variable_groups[0]
digits = (0, 1, 2, 3, 0, 1)
certificate, angles = s.link.native_rotations(field.selected(group['indices_by_generator']),
                                             digits, group['xy'])
entry = s.link.variable_entry(group, digits)
assert len(angles) == 496
protected = set(cfbound['SAM']+cfbound['address']+[cfbound['oldRIGHT_witness']])
link_trees = 0
for depth in range(3):
    for angle in angles:
        diff = angle['i'] ^ angle['j']
        flips = bin(diff).count('1')-1
        # Ignore no prefix: all leading permutations and two full Walsh
        # terms are included; the masks themselves remain production-sized.
        blocks = s.link.sector_blocks(cfbound, entry, [angle], reverse=bool(depth % 2))
        for tree in islice(blocks, flips+2):
            tree = local.invert(tree, depth-depth % 2, cfbound)
            transformed, pending, _ = g.compiler().transform(tree, 0)
            assert pending == 0
            for leaf in nb.leaves(transformed):
                assert leaf['op'] in ('G', 'CX')
                assert leaf['wires'][-1] not in protected
                for wire in leaf['wires']:
                    g.physical_wire(wire)
            link_trees += 1

result = {'status': 'PASS_PARAMETERIZED_SOURCE_GLOBAL_COMPOSITION',
    'all_source_slots': dict(kinds), 'field_bound_routing_cases': len(route),
    'independent_proper_link_groups': len(variable_groups),
    'fixed_variable_link_splice_literal_depth_cases': splice,
    'exact_small_adapter_primitive_comparisons': adapter_checks,
    'global_stage_count_each_direction': len(stages), 'original_source_marks': marks,
    'independent_slot_sum_inventory_verified': True,
    'actual_coframe_CAR_G_CX_unit_checks': len(actual_checks),
    'actual_new_Julia_angles_checked_in_global_layout': len(angles),
    'actual_new_Julia_G_CX_trees_depths_0_1_2': link_trees,
    'actual_new_Julia_angle_powers_sha256': certificate['angle_powers_sha256'],
    'SOURCE_prefix_error_lt': '2^-3423', 'compressed_core_error_lt': '2^-3421',
    'SourceI_replacement_error_lt': '2^-15800',
    'all_2688_CODE_targets_unchanged_by_SOURCE': True,
    'whole_production_stream_or_actual_unpadded_length_evaluated': False,
    'new_post_and_clock_verified_here': False, 'physical_C_closed': False, 'GR_closed': False,
    'source_sha256': {str(p): sha256(p.read_bytes()).hexdigest() for p in
                     [Path(__file__), P/'regular_source_native.py',
                      P/'regular_global_source.py', P/'REGULAR_GLOBAL_SOURCE_PLAN.json']}}
(P/'REGULAR_GLOBAL_SOURCE_CHECK.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({k: result[k] for k in ('status', 'field_bound_routing_cases',
                                       'actual_coframe_CAR_G_CX_unit_checks')}))
