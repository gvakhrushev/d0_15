#!/usr/bin/env python3
"""Check all original leaf addresses, scopes and actual inserted bridge DAGs."""
from pathlib import Path
from collections import Counter
from fractions import Fraction
import hashlib, json
import sympy as sp
import source_mark_registry as r
s = r.s
P = Path(__file__).resolve().parent


def main():
    plan = s.build(); registry = r.build(); binding = r.original_binding()
    kinds = Counter(); old = s.g.namespace(); selected = registry['selected_common_f_q_slots']
    assert len(set(selected.values())) == 3
    selected_supports = [set(old['source_slots'][i]['source']+old['source_slots'][i].get('RIGHT', [])) for i in selected.values()]
    assert sum(map(len, selected_supports)) == len(set.union(*selected_supports))
    max_physical = old['layout']['qubits']-2
    for x, row in enumerate(binding['site_bindings']):
        for i, template in enumerate(binding['leaf_templates']):
            mark = r.leaf_mark(x, i)
            data = mark['logical_support_wires_LE']
            physical = mark['physical_support_wires_LE']
            assert all(0 <= q < max_physical for q in physical)
            assert [s.b.logical_wire(q) for q in physical] == data
            t = sum(bit << j for j, bit in enumerate(mark['t_G_columns_LE']))
            a = sum(bit << j for j, bit in enumerate(mark['r_G_columns_LE']))
            assert (a, t) == (mark['r_computational_label'], mark['t_computational_label'])
            address = row['leaf_addresses_in_template_order'][i]
            if template['kind'] == 'Choi':
                assert a == 0 and (t >> 10) == address
                assert ((t >> 5) & 31) == template['input'] and (t & 31) == template['output']
                assert mark['coefficient']['integer'] == 32784*template['anchor_moment_multiplier']
                assert address > 0 and len(data) == 22
            else:
                assert (a >> 4) == (t >> 4) == address
                assert a & 15 == 1 and t & 15 == template['cross_masks'][1]
                assert len(data) == 12 and len(mark['fresh_CAR_RIGHT_identity_wires']) == 7
            kinds[mark['original_family']] += 1
    assert sum(kinds.values()) == 72192
    # All copies bind to the same paid checkpoint while their completion
    # times remain explicit and do not masquerade as RAW-frame checkpoints.
    assert len(registry['source_slots']) == 1372
    all_resource = []
    for row in registry['source_slots']:
        assert row['source_completion_stage_index'] < plan['joint_RAW_source_checkpoint_after_stage_index']
        assert row['original_RAW_mark_checkpoint_after_stage_index'] == 1380
        all_resource.extend(row['logical_resource_frame_wires'])
    assert tuple(all_resource) == s.resource_wires()
    # Test the four ACTUAL integer inverse depths, not ideal sign cancellation.
    compiler = s.c.production_compiler(); width = len(s.resource_wires()); per_wire = Counter()
    q = s.resource_wires()[0]
    for depth in (0, 1, 2, 1):
        tree = s.g.invert(s.c.nb.gate('G', q), depth, old)
        out, pending, counts = compiler.transform(tree)
        assert pending == 0 and counts['CZ'] == 0
        per_wire.update(s.c.nb.counts(out))
    assert per_wire == {'G': 4+192*compiler.k, 'CX': 42}
    old_counts = {k: int(v) for k, v in json.loads((s.D/'round29/GCX_BIRTH_CLOCK_PLAN.json').read_text())['native_counts'].items()}
    assert int(plan['new_native_counts']['G'])-old_counts['G'] == width*per_wire['G']
    assert int(plan['new_native_counts']['CX'])-old_counts['CX'] == width*per_wire['CX']
    # Exact one-factor unitary / orthogonality supplies all tensor powers.
    p = (sp.sqrt(5)-1)/2
    G = sp.Matrix([[sp.sqrt(p), -p], [p, sp.sqrt(p)]])
    assert sp.simplify(G.T*G-sp.eye(2)) == sp.zeros(2)
    assert sp.simplify(G[:,0].dot(G[:,1])) == 0
    # A representative two-bit RAW conjugation; no free physical gate implied.
    B = sp.kronecker_product(G, G)
    O = sp.zeros(4); O[0,3] = O[3,0] = 1
    Oraw = B*O*B.T
    assert sp.simplify(B.T*Oraw*B-O) == sp.zeros(4)
    error = s.inventory()['common_mark_error_per_unit_norm']
    assert error < Fraction(1, 2**3231)
    assert 32784*error < Fraction(1, 2**3215) and 65568*error < Fraction(1, 2**3214)
    # p>3/5 implies sqrt(p)>1/2, so 128/sqrt(p)<256.
    assert p > sp.Rational(3,5) and Fraction(256)*error < Fraction(1, 2**3223)
    pins = [Path(__file__), P/'marked_source_schedule.py', P/'source_mark_registry.py',
            P/'COMMON_SOURCE_MARKED_PLAN.json', P/'SOURCE_RAW_MARK_REGISTRY.json',
            s.D/'round11/PERIODIC_SOURCE_BINDING.json', s.D/'round29/GCX_BIRTH_CLOCK_PLAN.json']
    out = {'status': 'PASS_ORIGINAL_LEAF_MARKS_COMMON_RAW_FRAME_AND_PAID_BRIDGE',
           'all_original_leaf_bindings_checked': dict(kinds), 'total_leaf_bindings': sum(kinds.values()),
           'source_slot_checkpoints_checked': 1372, 'resource_bridge_wires': width,
           'selected_f_q_supports_pairwise_disjoint': True,
           'actual_bridge_inverse_depths': [0,1,2,1],
           'exact_RAW_frame_conjugation_fixture': True,
           'original_norm_weighted_mark_budgets_checked': True,
           'complete_giant_program_or_detector_executed': False,
           'source_sha256': {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in pins},
           'physical_C_closed': False, 'GR_closed': False}
    (P/'MARKED_SOURCE_CHECK.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({k: out[k] for k in ('status','total_leaf_bindings','resource_bridge_wires')}))


if __name__ == '__main__':
    main()
