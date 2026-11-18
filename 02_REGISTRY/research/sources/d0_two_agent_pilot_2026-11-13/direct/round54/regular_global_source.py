#!/usr/bin/env python3
"""Actual field-dependent G/CX SOURCE and retained comparator core.

The same field is used by all 1440 Choi and 128 CAR copies. The namespace,
births, eight REPORTs, original SC6 and compiler helper remain exactly A48.
The post and whole paid clock are separate consumers of this NEW core.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from functools import lru_cache
from hashlib import sha256
import json
import regular_source_native as s
import two_bit_global_source as previous

P = Path(__file__).resolve().parent
D = P.parent
t = s.t
nb = s.nb
ns = previous.ns
namespace = previous.namespace
birth_blocks = previous.birth_blocks
physical_wire = previous.physical_wire
physical_tree = previous.physical_tree
compiler = previous.compiler
schedule = previous.previous.stages


class GlobalSource:
    def __init__(self, field):
        self.sources = s.Sources(field)
        self.field = self.sources.field

    def stage_blocks(self, stage, depth=0):
        plan = namespace()
        if stage['kind'] == 'SOURCE':
            slot = plan['source_slots'][stage['slot']]
            if slot['kind'] == 'Choi':
                yield from self.sources.choi_blocks(slot['bank'], ns.choi_layout(plan, slot), depth)
            else:
                yield from self.sources.car_blocks(slot['bank'], ns.car_layout(plan, slot), depth)
        else:
            yield from previous.stage_blocks(stage, depth)

    def profile_with_cuts(self):
        stages = schedule()
        for stage in stages:
            yield from self.stage_blocks(stage)
            if stage == {'kind': 'RAW_RESOURCE_FRAME', 'intrinsic_inverse_depth': 0}:
                yield {'op': 'B82_CUT', 'name': previous.previous.p43.CUTS[0]}
        lay = namespace()['layout']
        yield nb.z_word(lay['port'], lay['port'], tuple(lay['spin']))
        for stage in reversed(stages):
            yield from self.stage_blocks(stage, 1)
            if stage == {'kind': 'RAW_RESOURCE_FRAME', 'intrinsic_inverse_depth': 1}:
                yield {'op': 'B82_CUT', 'name': previous.previous.p43.CUTS[1]}

    def compiled_core_with_cuts(self):
        yield from previous.previous.compile_tagged(self.profile_with_cuts, compiler(), physical_tree)

    def core_blocks(self):
        for tree in self.compiled_core_with_cuts():
            if tree['op'] != 'B82_CUT':
                yield tree

    def source_prefix_blocks(self):
        def profile():
            for stage in schedule():
                yield from self.stage_blocks(stage)
                if stage == {'kind': 'RAW_RESOURCE_FRAME', 'intrinsic_inverse_depth': 0}:
                    return
            raise AssertionError('missing SOURCE boundary')
        for tree in compiler().stream(profile()):
            yield physical_tree(tree)


@lru_cache(None)
def upper_inventory_and_error():
    source = s.inventory_upper()['all_SOURCE_forward_componentwise_upper']
    report = json.loads((D/'round17/GLOBAL_REPORT_COMPILATION.json').read_text())
    rp = s.old.counter(report['native_forward_resources'])
    r = len(previous.previous.resource_wires())
    assert r == 34112
    frames = Counter(G_other=r, G_port=r, CX=6*r, SourceI=4*r)
    A = source+s.old.times(rp, 8)+s.old.raw_counts(8)+frames
    A.update(G_port=5889, CX=4096, SourceI=8196)
    W = A+s.old.inv(A)+Counter(SourceI=2)
    units = 8*W['SourceI']
    replacement = F(units, 1 << 20000)
    native = Counter(G=W['G_port']+W['G_other']+compiler().k*units,
                     CX=W['CX']+W['SourceI'])
    known = report['seven_report_all_known_approximate_macros']
    assert known % 7 == 0
    source_error = s.error_bounds()['all1440Choi_128CAR_SITE']
    prefix = source+s.old.raw_counts(8)+Counter(G_other=r)
    prefix_error = source_error+F(8*prefix['SourceI'], 1 << 20000)
    eta = source_error+F(8*(known//7), 1 << 4096)
    compressed = 2*eta+replacement
    assert replacement < F(1, 1 << 15800)
    assert prefix_error < F(1, 1 << 3423)
    assert compressed < F(1, 1 << 3421)
    return {'A_profile_upper': A, 'W_profile_upper': W, 'W_G_CX_upper': native,
            'replacement_error': replacement, 'canonical_A_error_before_replacement': eta,
            'full_canonical_compressed_error': compressed, 'source_error': source_error,
            'full_SOURCE_DATA_fibre_prefix_error': prefix_error}


def encode(value):
    if isinstance(value, F):
        return s.old.encode_error(value)
    if isinstance(value, Counter):
        return {key: hex(int(v)) for key, v in value.items()}
    if isinstance(value, dict):
        return {key: encode(v) for key, v in value.items()}
    return value


def build_plan():
    u = upper_inventory_and_error()
    paths = [Path(__file__), P/'regular_source_native.py',
             D/'round53/regular_field_targets.py', D/'round53/regular_source_components.py',
             D/'round48/two_bit_source_native.py', D/'round48/two_bit_global_source.py',
             s.old.B/'round103/regular_link_julia.py',
             s.old.B/'round93/proper_link_two_bit_native.py',
             s.old.B/'round93/PROPER_LINK_RESOURCE_UPPER.json']
    return {'status': 'PARAMETERIZED_GLOBAL_SOURCE_G_CX_CORE_ON_ORIGINAL_DATA_FIBRE',
        'field_coordinates': 2688, 'field_centre_open_radius': '2^-32', 'CODE_bits': 5376,
        'same_immutable_field_in_all_source_copies': True,
        'Choi_copies': 1440, 'CAR_copies': 128, 'REPORT_banks': 8,
        'RAW_births': sum(z['stop']-z['start'] for z in birth_blocks()),
        'A48_namespace_births_old_helper_and_SC6_retained': True,
        'B103_variable_link_sectors': 256*4096,
        'old_B93_variable_link_word_removed_from_emission': True,
        'full_literal_integer_inverse_depths_retained': True,
        'finite_lazy_G_CX_providers_implemented': True,
        'uniform_SOURCE_inventory_upper': encode(s.inventory_upper()),
        'uniform_global_inventory_and_errors': encode(u),
        'uniform_component_errors': encode(s.error_bounds()),
        'core_call_upper_bit_length': sum(u['W_G_CX_upper'].values()).bit_length(),
        'SOURCE_prefix_error_lt': '2^-3423', 'compressed_core_error_lt': '2^-3421',
        'SourceI_replacement_error_lt': '2^-15800',
        'norm_scope': 'full declared DATA fibre with native RAW Choi-private24/CAR-predicate3; external entanglement allowed',
        'arbitrary_dirty_private_operator_claim': False,
        'aggregate_inventory_is_upper_not_actual': True,
        'new_paid_post_and_clock_bound_here': False,
        'compiler_differentiability_or_physical_source_claim': False,
        'production_expanded_words_executed': False,
        'physical_C_closed': False, 'GR_closed': False,
        'source_sha256': {str(p): sha256(p.read_bytes()).hexdigest() for p in paths}}


if __name__ == '__main__':
    plan = build_plan()
    (P/'REGULAR_GLOBAL_SOURCE_PLAN.json').write_text(json.dumps(plan, indent=2)+'\n')
    print(json.dumps({k: plan[k] for k in ('status', 'RAW_births', 'core_call_upper_bit_length',
                                         'SOURCE_prefix_error_lt', 'compressed_core_error_lt')}))
