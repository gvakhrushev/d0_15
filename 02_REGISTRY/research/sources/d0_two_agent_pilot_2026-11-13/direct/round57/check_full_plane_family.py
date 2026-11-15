#!/usr/bin/env python3
"""Check the new finite request, actual factory, padding and source budget."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from hashlib import sha256
from itertools import islice
from types import SimpleNamespace
from unittest.mock import patch
import json
import full_plane_family as a

P = Path(__file__).resolve().parent
native = a.paid.native
leaves = lambda stream: [g for tree in stream for g in a.paid.target.e.leaves(tree)]


def main():
    fields = [a.FieldCentre(), a.FieldCentre(tuple(F((j % 5)-2, 1 << 36) for j in range(2688)))]
    planes = [(0, 1), (1, 6), (0, (1 << 5376)-1), ((1 << 5376)-2, (1 << 5376)-1)]
    labels = [a.LegacyLabel()]
    labels += [a.LegacyLabel(arm, sign, axis) for arm in a.prior.original.ARMS
               for sign in (-1, 1) for axis in (0, 2687)]
    labels += [a.LegacyLabel('post_probe', sign, plane=planes[-1]) for sign in (-1, 1)]
    labels += [a.PlaneLabel(arm, sign, plane) for arm in a.ARMS
               for sign in (-1, 1) for plane in planes]
    assert len(labels) == 55
    encoded = set()
    for field in fields:
        for label in labels:
            request = a.Request(field, label)
            packet = request.encode()
            assert a.Request.decode(packet) == request
            assert packet not in encoded
            encoded.add(packet)
    assert len(encoded) == 110

    base = json.loads(a.Request(fields[0], a.PlaneLabel('Pf', 1, (0, 1))).encode())
    bad = []
    v = json.loads(json.dumps(base)); v['external_program'] = 'different'; bad.append(v)
    v = json.loads(json.dumps(base)); v['family'] = 'arbitrary_skew'; bad.append(v)
    v = json.loads(json.dumps(base)); v['label']['sign'] = True; bad.append(v)
    v = json.loads(json.dumps(base)); v['label']['plane'] = [0, 1 << 5376]; bad.append(v)
    v = json.loads(json.dumps(base)); v['label']['plane'] = [1, 0]; bad.append(v)
    v = json.loads(json.dumps(base)); v['label']['axis'] = 0; bad.append(v)
    v = json.loads(json.dumps(base)); v['field'][0] = [1, 1 << 32]; bad.append(v)
    for value in bad:
        try: a.Request.decode(json.dumps(value, sort_keys=True, separators=(',', ':')).encode())
        except (ValueError, TypeError): pass
        else: raise AssertionError('invalid or hidden datum accepted')
    try: a.Request.decode(json.dumps(base, indent=2).encode())
    except ValueError: pass
    else: raise AssertionError('noncanonical packet accepted')

    instances = [a.FullPlaneTask(field) for field in fields]
    _, q, cert = a.grid.uniform_grid()
    k8 = a.grid.Macros().ks['pi8']
    for instance in instances:
        c = instance.cfg
        old = instance.bound.family.cfg
        assert c['coreL'] == old['coreL'] and c['postL'] == old['postL'] and c['probeL'] == old['probeL']
        assert c['controlL'] == max(old['controlL'], sum(a.paid.old.plane_upper(5376, q, k8).values())+4)
        assert c['Lbase'] == old['coreL']+old['postL']+old['probeL']+4*c['controlL']
        assert c['Nbase'] == c['n']+c['Lbase'] and c['Nbase'] > old['Nbase']
        assert c['K'] == 4*(c['Nbase'].bit_length()+17375) > old['K']
        assert c['Nbase'].bit_length() == 38150 and c['K'] == 222100
        target = instance.bound.family.actual_core_target()
        assert target.factory.__self__ is instance.bound.family.source
        assert target is instance.bound.family.actual_core_target()
        packet = instance.packet(a.Request(instance.field, a.PlaneLabel('Qb', -1, planes[-1])))
        assert packet['actual_padded_lengths_hex']['Nbase'] == hex(c['Nbase'])
        assert packet['late_retention_pairs'] == c['K']
        assert not list(instance.native_plane_blocks((0, 1), 0))
    assert instances[0].cfg == instances[1].cfg
    assert instances[0].bound.family.actual_core_target() is not instances[1].bound.family.actual_core_target()
    try: next(instances[0].word_blocks(a.Request(fields[1])))
    except ValueError: pass
    else: raise AssertionError('foreign field accepted')

    # Exercise actual production selector and plane-factory dispatch, without
    # expanding the 2^5375 parity catalogue or the high positive G powers.
    powers = {s: a.plane_power(s) for s in (-1, 1)}
    assert all(1 <= k <= q for k in powers.values()) and powers[-1]+powers[1] == q
    dispatch = []
    def plane_stub(x, y, k, sam, macro):
        dispatch.append((x, y, k, tuple(sam), macro.ks['pi8']))
        yield native.gate('G', sam[0])
    with patch.object(a.paid.old, 'plane_blocks', plane_stub):
        for plane in planes:
            for sign in (-1, 1):
                assert len(list(instances[0].native_plane_blocks(plane, sign))) == 1
                assert dispatch[-1] == (*plane, powers[sign], tuple(instances[0].cfg['sam']), k8)
    assert len(dispatch) == 8

    # A genuinely complete small emitted word for every kind of label,
    # both fields and all thirteen retained prefix frontiers. Replace only
    # the huge component providers by explicit literal native words.
    marks = ['SOURCE_before_Qf']+[x['name'] for x in a.prior.prefixes.registry()]
    fixture_labels = [x for x in labels if type(x) is not a.PlaneLabel or x.plane in planes[:2]]
    prefix_cases = 0
    slot_cases = 0
    for field_index, field in enumerate(fields):
        before = [native.gate('G', 3+field_index), native.gate('CX', 0, 3+field_index)]
        middle = [[native.gate('CX', 3, 4), native.gate('G', 4)] if j % 2
                  else [native.gate('G', 3)] for j in range(len(a.prior.prefixes.processor_stages()))]
        returned = [native.gate('CX', 1, 4), native.gate('G', 3)]
        def source():
            yield from before
            yield {'op': 'B82_CUT', 'name': a.paid.CUTS[0]}
            for group in middle: yield from group
            yield {'op': 'B82_CUT', 'name': a.paid.CUTS[1]}
            yield from returned
        def post(): yield native.gate('G', 0)
        def old_control(axis, sign):
            if sign: yield native.repeat(1 if sign > 0 else 2, native.gate('G', axis % 3))
        def plane_control(plane, sign):
            if sign: yield native.repeat(1 if sign > 0 else 3, native.gate('G', (plane[0]+plane[1]) % 3))
        def probe(plane, sign): yield from old_control(1, sign)
        def processor(name):
            for group in middle[:a.prior.prefixes.descriptor(name)['processor_stage_count']]: yield from group
        c = {'n': 5, 'sam': (0, 1, 2), 'K': 3, 'controlL': 9,
             'coreL': len(before)+sum(map(len, middle))+len(returned)+4,
             'postL': 5, 'probeL': 6}
        c['Lbase'] = c['coreL']+c['postL']+c['probeL']+4*c['controlL']
        c['Nbase'] = c['n']+c['Lbase']
        fixture = a.FullPlaneTask.__new__(a.FullPlaneTask)
        fixture.field, fixture.cfg = field, c
        fixture.native_plane_blocks = plane_control
        fixture.bound = SimpleNamespace(processor_native_blocks=processor,
            family=SimpleNamespace(_guard=lambda: None,
                source=SimpleNamespace(compiled_core_with_cuts=source, source_prefix_blocks=lambda: iter(before)),
                actual_post_blocks=post, actual_probe_blocks=probe))
        with patch.object(a.paid, 'raw_control_factory', old_control):
            for label in fixture_labels:
                request = a.Request(field, label)
                emitted = leaves(fixture.word_blocks(request))
                assert len(emitted) == c['Lbase']
                sign_map = a.paid.slot_signs(label.arm, label.sign)
                if type(label) is a.PlaneLabel:
                    ctr = lambda axis, sign: plane_control(label.plane, sign)
                else: ctr = old_control
                expected = leaves(a.paid.family_blocks(c, source, post, ctr, probe,
                                    **asdict_label(label)))
                assert emitted == expected
                slot_cases += 1
                for name in marks:
                    part = leaves(fixture.prefix_blocks(request, name))
                    length = c['controlL']+len(before)
                    if name != 'SOURCE_before_Qf':
                        length += c['controlL']+sum(map(len, middle[:a.prior.prefixes.descriptor(name)['processor_stage_count']]))
                    assert part == emitted[:length] and len(part) == length
                    prefix_cases += 1
                stages = list(fixture.stages(request))
                assert len(stages) == c['Nbase']+2*c['K']
                assert stages[-1]['kind'] == 'final_unitary_g'
                assert stages[-1]['gate'] == native.gate('G', c['n']+c['K']-1)
    assert slot_cases == 78 and prefix_cases == 1014

    # Independent new clock/precision algebra. Full SOURCE/post errors are
    # inherited in the analytic norm, never multiplied by the plane count.
    cfg = instances[0].cfg
    t, gs, z = (F(1, 1 << k) for k in (6000, 3208, 20))
    gamma0 = F(8, 3)*z*gs
    m = 5376
    mu = F((1 << 5375)+40*m, 1 << 32768)
    bracket = 8/(1-z)+24*z/(1-z)**2+16*z*z/(1-z)**3
    taylor = t*t*(bracket/16+F(1, 6))/gs
    control = 2*mu/(t*gs)
    heat = F(6*cfg['Nbase'], 359)/(t*gamma0)*F(1, 1 << (cfg['K']//4))
    ah = F(6, 359)/gamma0*F(1, 1 << (cfg['K']//4))
    extra = 208*(1 << 8064)*(taylor+control+heat+ah+F(1, 1 << 8150))
    got = a.bounds(cfg, normalized_reading_error=F(1, 1 << 8150))
    assert got['finite_vs_analytic_full_raw_dual'] == extra < F(1, 1 << 75)
    assert got['finite_full_raw_target_error'] < F(1, 1 << 34)
    assert a.bounds(cfg)['finite_vs_analytic_full_raw_dual'] < extra
    assert got['full_analytic_target_error'] == a.analytic.bounds()['feedback_full_raw_dual']+208*ah
    for e in (F(-1), 0.0):
        try: a.bounds(cfg, normalized_reading_error=e)
        except ValueError: pass
        else: raise AssertionError('invalid reading bound accepted')

    plan = a.build()
    for name, digest in plan['source_sha256'].items():
        assert sha256(Path(name).read_bytes()).hexdigest() == digest
    out = {'status': 'PASS_FULL_PLANE_REQUESTS_FACTORIES_PREFIXES_CLOCK_AND_DUAL_BUDGET',
           'canonical_request_roundtrips': len(encoded), 'invalid_request_rejections': 8,
           'actual_production_plane_selector_dispatches': len(dispatch),
           'full_small_native_word_and_clock_cases': slot_cases,
           'complete_small_literal_prefix_cases': prefix_cases,
           'new_Nbase_bits': cfg['Nbase'].bit_length(), 'new_K': cfg['K'],
           'all_four_plane_interpolant_extra_raw_dual_lt': '2^-75',
           'all_four_plane_interpolant_target_raw_dual_lt': '2^-34',
           'arbitrary_X_compiled_finite_theorem_claimed': False,
           'production_giant_word_or_price_evaluated': False,
           'physical_C_closed': False, 'GR_closed': False,
           'source_sha256': {**plan['source_sha256'], str(Path(__file__)): sha256(Path(__file__).read_bytes()).hexdigest()}}
    (P/'FULL_PLANE_FAMILY_CHECK.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k != 'source_sha256'}, indent=2))


def asdict_label(label):
    return a.asdict(a.FullPlaneTask.legacy_shape(label))


if __name__ == '__main__':
    main()
