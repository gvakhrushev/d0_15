#!/usr/bin/env python3
"""Finite field requests, actual family binding and literal marked prefixes."""
from pathlib import Path
from fractions import Fraction as F
from itertools import islice
from types import SimpleNamespace
from unittest.mock import patch
from hashlib import sha256
import json
import regular_comparison_task as task

P = Path(__file__).resolve().parent
nb = task.paid.paid.native
fields = [task.FieldCentre(), task.FieldCentre(tuple(F((j % 13)-6, 1 << 36) for j in range(2688)))]
labels = [task.Label()]
labels += [task.Label(arm, sign, axis) for arm in task.original.ARMS
           for sign in (-1, 1) for axis in (0, 2687)]
labels += [task.Label('post_probe', sign, plane=(0, (1 << 5376)-1)) for sign in (-1, 1)]
assert len(labels) == 23
packets = set()
for field in fields:
    for label in labels:
        request = task.Request(field, label)
        packet = request.encode()
        assert packet not in packets
        packets.add(packet)
        assert task.Request.decode(packet) == request
assert len(packets) == 46

base = json.loads(task.Request(fields[0]).encode())
bad = []
v = dict(base); v['hidden_program'] = 'another source'; bad.append(v)
v = dict(base); v['field'] = [[0, 1]]; bad.append(v)
v = json.loads(json.dumps(base)); v['field'][0] = [1, 1 << 32]; bad.append(v)
v = json.loads(json.dumps(base)); v['field'][0] = [True, 1]; bad.append(v)
v = json.loads(json.dumps(base)); v['field'][0] = [0, 2]; bad.append(v)
v = json.loads(json.dumps(base)); v['label']['field'] = 1; bad.append(v)
v = json.loads(json.dumps(base)); v['label']['arm'] = 'free_physical_source'; bad.append(v)
v = json.loads(json.dumps(base)); v['label']['sign'] = True; bad.append(v)
for value in bad:
    try:
        task.Request.decode(json.dumps(value, sort_keys=True, separators=(',', ':')).encode())
    except (ValueError, TypeError):
        pass
    else:
        raise AssertionError('invalid or hidden request accepted')
try:
    task.Request.decode(json.dumps(base, indent=2).encode())
except ValueError:
    pass
else:
    raise AssertionError('noncanonical encoding accepted')

# Actual source/post and new clock ownership, separate per field. No
# gigantic path-sum is run merely to check a bound-method identity.
tasks = [task.FieldTask(f) for f in fields]
for current in tasks:
    request = task.Request(current.field, task.Label('Pf', 1, 0))
    current.validate(task.Request.decode(request.encode()))
    target = current.family.actual_core_target()
    assert target.factory.__self__ is current.family.source
    assert current.family.source.field is current.field
    assert current.family.source.sources.components.field is current.field
    record = current.packet(request)
    assert record['actual_padded_lengths_hex']['Nbase'] == hex(current.family.cfg['Nbase'])
    assert record['late_retention_pairs'] == 175604
    calls = []

    def block_probe(**kwargs):
        calls.append(kwargs); return iter(())

    with patch.object(current.family, 'blocks', block_probe):
        list(current.word_blocks(request, keep_marks=True))
    assert calls == [dict(task.asdict(request.label), keep_marks=True)]
assert tasks[0].family.actual_core_target() is not tasks[1].family.actual_core_target()
assert tasks[0].packet(task.Request(fields[0]))['actual_padded_lengths_hex'] == (
       tasks[1].packet(task.Request(fields[1]))['actual_padded_lengths_hex'])
try:
    next(tasks[0].word_blocks(task.Request(fields[1])))
except ValueError:
    pass
else:
    raise AssertionError('foreign field silently accepted by bound family')

# Exercise the NEW prefix wrapper against complete native padded words on
# two different source fixtures; all 13 marks and independent arms count.
marks = ['SOURCE_before_Qf']+[x['name'] for x in task.prefixes.registry()]
literal_checks = 0
for field_index, field in enumerate(fields):
    sam = (0, 1, 2)
    before = [nb.gate('G', 3+field_index), nb.gate('CX', field_index, 3+field_index)]
    middle = [[nb.gate('G', 4)] if j % 2 else [nb.gate('CX', 3, 4), nb.gate('G', 3)]
              for j in range(len(task.prefixes.processor_stages()))]
    returned = [nb.gate('CX', 1, 4), nb.gate('G', 4)]

    def core():
        yield from before
        yield {'op': 'B82_CUT', 'name': task.paid.paid.CUTS[0]}
        for block in middle:
            yield from block
        yield {'op': 'B82_CUT', 'name': task.paid.paid.CUTS[1]}
        yield from returned

    def control(axis, sign):
        if sign:
            yield nb.repeat(1 if sign > 0 else 2, nb.gate('G', sam[axis % 3]))

    def processor(name):
        for block in middle[:task.prefixes.descriptor(name)['processor_stage_count']]:
            yield from block

    def leaves(stream):
        return [gate for tree in stream for gate in task.paid.paid.target.e.leaves(tree)]

    cfg = {'sam': sam, 'controlL': 6,
           'coreL': len(before)+sum(map(len, middle))+len(returned)+4,
           'postL': 6, 'probeL': 6}
    fixture = task.FieldTask.__new__(task.FieldTask)
    fixture.field = field
    fixture.family = SimpleNamespace(cfg=cfg, _guard=lambda: None,
        source=SimpleNamespace(source_prefix_blocks=lambda: iter(before)))
    fixture.processor_native_blocks = processor
    with patch.object(task.paid.paid, 'raw_control_factory', control):
        for label in labels:
            request = task.Request(field, label)
            full = leaves(task.paid.paid.family_blocks(cfg, core,
                lambda: iter([nb.gate('G', 0), nb.gate('G', 1)]), control,
                lambda plane, sign: control(0, sign), **task.asdict(label)))
            for name in marks:
                part = leaves(fixture.prefix_blocks(request, name))
                length = cfg['controlL']+len(before)
                if name != 'SOURCE_before_Qf':
                    length += cfg['controlL']+sum(map(len,
                        middle[:task.prefixes.descriptor(name)['processor_stage_count']]))
                assert len(part) == length and part == full[:length]
                literal_checks += 1
assert literal_checks == 598

# The processor is exactly the inherited field-independent provider.
# Finite samples exercise the new wiring; the complete equality follows
# from identical schedule, stage provider, namespace and compiler.
processor_checks = 0
for current in tasks:
    for row in task.prefixes.registry():
        name = row['name']
        got = list(islice(current.processor_native_blocks(name), 3))
        expected = list(islice(task.prefixes.processor_native_blocks(name), 3))
        assert got == expected
        processor_checks += 1
    starts = list(islice(current.stages(task.Request(current.field)), 2))
    assert [z['wire'] for z in starts] == [0, 1]
    assert all(z['kind'] == 'canonical_RAW_birth' for z in starts)

# Recompute the uniform finite jet envelope from constants and NEW eB/eW,
# without importing A48's old bound as the answer at a new field.
u = task.source.upper_inventory_and_error()
c = task.paid.paid.control.control_plan()['control_vs_exp_tX_error']
eP = F(int(c['numerator_hex'], 16), int(c['denominator_hex'], 16))
sigma, step = F(1, 1 << 80), F(1, 1 << 1700)
M1, M2 = 1748, 3233036
eB = u['full_SOURCE_DATA_fibre_prefix_error']
extra = (eB+2*eP)/(sigma*step)+F(4, 3)*104*M1*step**2
report = json.loads((task.D/'round17/GLOBAL_REPORT_COMPILATION.json').read_text())
eD = F(8*(report['seven_report_all_known_approximate_macros']//7), 1 << 4096)+u['replacement_error']
jet = sigma*104**2*M2+extra+eD*M1
midpoint = sigma*104*M1+eB+eD+2*eP+2*step**2
effect = 2*jet+2*M1*midpoint
bounds = task.frontier_bounds()
assert bounds['full_prefix_finite_axis_jet_error'] == jet < F(1, 1 << 44)
assert bounds['full_prefix_midpoint_error'] == midpoint < F(1, 1 << 62)
assert bounds['norm_one_joint_effect_finite_axis_jet_error'] == effect < F(1, 1 << 43)
plan = task.build()
assert plan == json.loads((P/'REGULAR_COMPARISON_TASK.json').read_text())
for path, digest in plan['source_sha256'].items():
    assert sha256(Path(path).read_bytes()).hexdigest() == digest
assert plan['available_original_REPORT_READY_pairs'] == task.original.report_labels()
result = {'status': 'PASS_REGULAR_FIELD_REQUEST_AND_MARKED_PREFIX_BINDING',
    'field_name_label_canonical_round_trips': 46, 'invalid_packets_rejected': len(bad)+1,
    'actual_field_bound_post_factories_and_common_new_clock_checked': True,
    'literal_prefix_comparisons_two_fields_all_independent_arms': literal_checks,
    'unchanged_processor_provider_sample_comparisons': processor_checks,
    'uniform_full_vector_jet_recomputed_lt': '2^-44',
    'uniform_norm_one_effect_jet_recomputed_lt': '2^-43',
    'uniform_midpoint_error_lt': '2^-62',
    'fine_instrument_registration_or_Vh_Cost_Info_proved': False,
    'production_word_executed': False, 'physical_C_closed': False, 'GR_closed': False,
    'source_sha256': {str(p): sha256(p.read_bytes()).hexdigest() for p in
                     [Path(__file__), P/'regular_comparison_task.py', P/'REGULAR_COMPARISON_TASK.json']}}
(P/'REGULAR_COMPARISON_TASK_CHECK.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({k: result[k] for k in ('status', 'field_name_label_canonical_round_trips',
                                       'literal_prefix_comparisons_two_fields_all_independent_arms')}))
