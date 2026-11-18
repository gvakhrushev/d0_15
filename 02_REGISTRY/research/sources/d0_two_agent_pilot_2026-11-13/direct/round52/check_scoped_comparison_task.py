#!/usr/bin/env python3
"""Finite catalogue, independent prefix placement and full retained instrument.

The instrument check is mathematical availability, never physical registration.
"""
from pathlib import Path
from hashlib import sha256
import json
import sympy as S
import scoped_comparison_task as task

P = Path(__file__).resolve().parent
nb = task.paid.native


def labels():
    seen = set()
    for label in task.catalogue():
        packet = task.encode(label)
        assert task.decode(packet) == label and packet not in seen
        seen.add(packet)
    assert len(seen) == 26881
    for plane in ((0, 1), ((1 << task.CODE_BITS)-2, (1 << task.CODE_BITS)-1)):
        for sign in (-1, 1):
            value = task.Label('post_probe', sign, plane=plane)
            assert task.decode(task.encode(value)) == value
    invalid = [dict(arm='centre', sign=1), dict(arm='centre', axis=1),
               dict(arm='Pf', sign=True), dict(arm='Pf', sign=0),
               dict(arm='Qf', sign=1, axis=task.M),
               dict(arm='post_probe', sign=1, plane=(1, 1)),
               dict(arm='post_probe', sign=1, plane=(0, 1 << task.CODE_BITS)),
               dict(arm='free_regular_Y', sign=1)]
    for args in invalid:
        try:
            task.Label(**args)
        except ValueError:
            continue
        raise AssertionError(args)
    extra = json.loads(task.encode(task.Label()))
    extra['Y'] = [0]
    try:
        task.decode(json.dumps(extra).encode())
    except ValueError:
        pass
    else:
        raise AssertionError('unimplemented free field silently accepted')
    return {'ordinary_labels_exhausted': len(seen), 'boundary_probe_labels': 4,
            'invalid_or_hidden_field_packets_rejected': len(invalid)+1}


def placement():
    sam = (0, 1, 2)
    before = [nb.gate('G', 3), nb.gate('CX', 0, 3)]
    middle = [[nb.gate('G', 4)] if j % 2 else
              [nb.gate('CX', 3, 4), nb.gate('G', 3)]
              for j in range(len(task.prefixes.processor_stages()))]
    returned = [nb.gate('CX', 1, 4), nb.gate('G', 4)]

    def core():
        yield from before
        yield {'op': 'B82_CUT', 'name': task.paid.CUTS[0]}
        for block in middle:
            yield from block
        yield {'op': 'B82_CUT', 'name': task.paid.CUTS[1]}
        yield from returned

    def control(axis, sign):
        if sign:
            yield nb.repeat(1 if sign > 0 else 2, nb.gate('G', sam[axis]))

    def processor(name):
        for block in middle[:task.prefixes.descriptor(name)['processor_stage_count']]:
            yield from block

    def leaves(stream):
        return [gate for tree in stream for gate in task.paid.target.e.leaves(tree)]

    cfg = {'sam': sam, 'controlL': 6,
           'coreL': len(before)+sum(map(len, middle))+len(returned)+4,
           'postL': 6, 'probeL': 6}
    cases = [task.Label()]
    cases += [task.Label(arm, sign, axis) for arm in task.ARMS
              for sign in (-1, 1) for axis in (0, 2)]
    cases += [task.Label('post_probe', sign, plane=(0, 1)) for sign in (-1, 1)]
    marks = ['SOURCE_before_Qf']+[x['name'] for x in task.prefixes.registry()]
    checks = []
    for label in cases:
        full = leaves(task.paid.family_blocks(cfg, core,
                      lambda: iter([nb.gate('G', 0), nb.gate('G', 1)]), control,
                      lambda plane, sign: control(0, sign), **task.asdict(label)))
        assert len(full) == cfg['coreL']+4*cfg['controlL']+cfg['postL']+cfg['probeL']
        for name in marks:
            part = leaves(task.assembled_prefix(label, name, cfg,
                          lambda: iter(before), processor, control))
            length = cfg['controlL']+len(before)
            if name != 'SOURCE_before_Qf':
                length += cfg['controlL']+sum(map(len, middle[:task.prefixes.descriptor(name)['processor_stage_count']]))
            assert len(part) == length and part == full[:length]
            checks.append({'label': task.asdict(label), 'mark': name, 'literal_prefix_calls': length})
    assert len(checks) == 299
    return checks


def instrument():
    # Retain the entire 8-dimensional output. Two label bits define four
    # projectors; the other output wire and arbitrary two input columns remain.
    R = S.Rational
    H = S.Matrix([[1, 1, 1, 1], [1, -1, 1, -1],
                  [1, 1, -1, -1], [1, -1, -1, 1]])/2
    rotation = S.Matrix([[R(3, 5), -R(4, 5)], [R(4, 5), R(3, 5)]])
    U = S.kronecker_product(rotation, H)
    F = U[:, [0, 5]]
    assert F.T*F == S.eye(2)
    effects, kraus = [], []
    for report, ready in ((0, 0), (0, 1), (1, 0), (1, 1)):
        Pi = S.diag(*[int((j & 1) == report and ((j >> 1) & 1) == ready) for j in range(8)])
        K = Pi*F
        E = K.T*K
        assert E == F.T*Pi*F
        assert all(x >= 0 for x in E.eigenvals())
        effects.append(E);kraus.append(K)
    assert sum(effects, S.zeros(2)) == S.eye(2)
    rho = S.Matrix([[R(1, 2), R(1, 5)], [R(1, 5), R(1, 2)]])
    retained = sum((K*rho*K.T for K in kraus), S.zeros(8))
    assert S.trace(retained) == 1
    assert S.trace((effects[0]+effects[2])*rho) > 0
    # Positive postprocessing merges both failure outcomes, without deleting.
    coarse = [effects[0]+effects[2], effects[1], effects[3]]
    assert sum(coarse, S.zeros(2)) == S.eye(2)
    # A read at an intermediate mark is not a free unchanged continuation.
    plus = S.Matrix([1, 1])/S.sqrt(2)
    coherent = plus*plus.T
    dephased = S.eye(2)/2
    effect = coherent
    assert S.trace(effect*coherent) == 1 and S.trace(effect*dephased) == R(1, 2)
    assert retained != F*rho*F.T
    return {'four_outcome_positive_normalized_full_retained_maps': True,
            'arbitrary_two_input_columns_and_positive_failure_retained': True,
            'positive_coarse_graining_preserves_total': True,
            'free_intermediate_measurement_preserves_suffix_rejected': True,
            'actual_registration_or_full_original_fine_K9_proved': False}


def main():
    plan = task.build()
    assert plan == json.loads((P/'FINITE_COMPARISON_TASK.json').read_text())
    for filename, digest in plan['source_sha256'].items():
        assert sha256(Path(filename).read_bytes()).hexdigest() == digest
    flags = plan['available_report_label_tests']
    assert len(flags) == 8
    assert flags[0]['report_wire'] == 21216958 and flags[0]['ready_wire'] == 21216959
    all_wires = [x[key] for x in flags for key in ('report_wire', 'ready_wire')]
    assert len(set(all_wires)) == 16
    assert all(0 <= q < plan['actual_early_RAW_births'] for q in all_wires)
    assert set(all_wires).isdisjoint(task.paid.production_configuration()['sam'])
    out = {'status': 'PASS_FINITE_TASK_BINDING_AND_AVAILABLE_RETAINED_LABEL_TEST',
           'label_checks': labels(), 'independent_prefix_fixtures': placement(),
           'mathematical_label_instrument': instrument(),
           'all_eight_actual_REPORT_READY_address_pairs_checked': True,
           'actual_regular_field_family_or_physical_fine_instrument_proved': False,
           'production_word_executed': False,
           'source_sha256': {str(f): sha256(f.read_bytes()).hexdigest() for f in
                             [Path(__file__), P/'scoped_comparison_task.py', P/'FINITE_COMPARISON_TASK.json']},
           'physical_C_closed': False, 'GR_closed': False}
    (P/'FINITE_COMPARISON_TASK_CHECK.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({'status': out['status'], 'ordinary_labels': 26881,
                      'literal_independent_prefix_comparisons': 299}))


if __name__ == '__main__':
    main()
