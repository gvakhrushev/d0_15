#!/usr/bin/env python3
"""Check new address intervals, actual SC6 block boundaries and heat gate.

No 10-billion-birth stream, giant native word, or heat matrix is executed.
"""
from pathlib import Path
from collections import Counter
from fractions import Fraction
import hashlib, itertools, json, random
import gcx_birth_clock as b
c = b.c
P = Path(__file__).resolve().parent


def last_leaf(t):
    while t['op'] in ('seq', 'repeat'):
        t = t['children'][-1] if t['op'] == 'seq' else t['child']
    return t


def main():
    plan = b.build()
    N = c.old.namespace()['layout']['qubits']
    n = plan['total_RAW_births']
    rng = random.Random(2902)
    layouts = []
    for m in (0, 1, 3, 17, 103):
        cursor, physical = m, []
        for block in b.birth_blocks():
            a, z = block['start'], block['stop']
            start, stop = b.physical_wire(a, m), b.physical_wire(z-1, m)+1
            assert start == cursor and stop-start == z-a
            cursor = stop
            physical.append({'role': block['role'], 'start': start, 'stop': stop})
            for q in {a, z-1, (a+z-1)//2}:
                assert b.logical_wire(b.physical_wire(q, m), m) == q
        assert cursor == m+n
        assert all(b.logical_wire(q, m) is None for q in range(m))
        for q in [q for q in range(2707) if q not in (0, 1, 3)] + [N] + [rng.randrange(2706, N) for _ in range(1000)]:
            assert b.logical_wire(b.physical_wire(q, m), m) == q
        first = list(itertools.islice(b.execution_stages(m), 4))
        assert [s['wire'] for s in first] == list(range(m, m+4))
        layouts.append({'old_raw_prefix_bits': m, 'birth_intervals': physical})
    # Actual SC6 is emitted as singleton leaves, so this exercises pending
    # SI across distinct blocks rather than already paired synthetic trees.
    compiler = c.production_compiler()
    layout = c.old.namespace()
    sc6 = []
    for depth in (0, 1):
        before, after = Counter(), Counter()
        def blocks():
            for t in c.old.stage_blocks({'kind': 'SC6'}, layout, depth):
                before.update(c.nb.counts(t))
                yield t
        for t in compiler.stream(blocks()):
            after.update(c.nb.counts(t))
            for z in c.nb.leaves(b.physical_tree(t, 0)):
                assert z['op'] in ('G', 'CX') and all(0 <= q < n for q in z['wires'])
        pairs = before['SourceI']//2
        assert after == {'G': before['G']+16*compiler.k*pairs, 'CX': before['CX']+2*pairs}
        assert pairs == (4096 if depth == 0 else 24064)
        sc6.append({'depth': depth, 'SourceI_pairs': pairs, 'actual_input_singletons': 18176})
    # The first SITE RAW conversion becomes W's last converted block.
    q = c.old.ns.site_layout(layout)['SITE'][0]
    assert q == 2692
    initial = c.nb.rotation_power(q, -1, compiler.port, compiler.spin)
    inverse = c.nb.inverse_literal(initial, compiler.port, compiler.spin)
    transformed, pending, _ = compiler.transform(inverse)
    assert pending == 0
    final = last_leaf(transformed)
    assert final == {'op': 'CX', 'wires': [2692, 2705]}
    assert b.physical_tree(final, 0) == {'op': 'CX', 'wires': [2690, 0]}
    # The prior port-detail obstruction survives the all-column perturbation.
    _, _, _, _, error, _ = b.inventory()
    old_element_lower = Fraction(24, 25)*Fraction(309, 500)**7
    assert old_element_lower-error > Fraction(3, 100)
    # Prefix clock bound q is specific to this constructed segment. Actual
    # earlier history/marks/readers must be added before selecting retention K.
    layers = int(plan['clock_layers_N'])
    assert layers < 2**11647
    # Exact clock-size formula verified on small independently summed cases.
    for births in range(1, 10):
        for length in range(1, 9):
            dims = [2**j for j in range(births)] + [2**births]*length
            assert sum(dims) == (length+1)*2**births-1
    pins = [Path(__file__), P/'gcx_birth_clock.py', P/'GCX_BIRTH_CLOCK_PLAN.json',
            P/'gcx_compiler.py', c.old.B/'round45/site_native.py',
            c.old.B/'round21/SC6_FORWARD.jsonl', c.D/'round28/ROOT_REVIEW_B55.json']
    out = {'status': 'PASS_NEW_RAW_ADDRESSES_CLOCK_AND_PORT_DETAIL_OBSTRUCTION',
           'checked_layouts': layouts, 'SC6_actual_block_boundary_checks': sc6,
           'last_g_logical': final, 'last_g_physical_m0': b.physical_tree(final),
           'isolated_new_segment_clock_layers_lt': '2^11647',
           'frontloaded_port_birth_detail_commutator_norm_gt': '3/100',
           'commutator_argument': 'old exact off-diagonal witness >=(24/25)*(309/500)^7; extending helper by its canonical v preserves the birth-detail witness, and new all-column error is smaller than the margin',
           'heat_source_nonzero_inferred': False, 'heat_zero_or_ST4_inferred': False,
           'actual_retention_K_chosen': False, 'full_clock_or_heat_matrix_executed': False,
           'source_sha256': {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in pins},
           'physical_C_closed': False, 'GR_closed': False}
    (P/'GCX_BIRTH_CLOCK_CHECK.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({'status': out['status'], 'prefix_cases': len(layouts), 'SC6_depths': [0, 1],
                      'new_port_commutator_gt': '3/100'}))


if __name__ == '__main__':
    main()
