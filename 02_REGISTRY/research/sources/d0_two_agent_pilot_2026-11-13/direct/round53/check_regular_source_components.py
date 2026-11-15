#!/usr/bin/env python3
"""Verify the new parameter interface, uniform margins and actual powers.

Only finite local components are sampled; no huge SOURCE stream is run.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from hashlib import sha256
from itertools import islice
import json
import regular_field_targets as t
import regular_source_components as c

P = Path(__file__).resolve().parent


def validate_fields():
    centre = t.FieldCentre()
    assert t.FieldCentre.decode(centre.encode()) == centre
    near = t.RADIUS*(1-F(1, 1 << 20))
    other = t.FieldCentre(tuple(near if j % 2 else -near for j in range(t.M)))
    assert t.FieldCentre.decode(other.encode()) == other
    invalid = [(F(0),)*(t.M-1), (t.RADIUS,)+(F(0),)*(t.M-1),
               (0.0,)+(F(0),)*(t.M-1), (True,)+(F(0),)*(t.M-1)]
    for values in invalid:
        try:
            t.FieldCentre(values)
        except ValueError:
            continue
        raise AssertionError(values[:1])
    counts = Counter(x['kind'] for x in t.COORD)
    assert counts == Counter(coframe=1024, proper_link=1536, matter=128)
    b = t.chart_bounds()
    assert b['old_cube_margin_lower'] > 0
    assert F(9, 4)**2 > 5 and 2**2 < 5
    assert 2688 < 52**2 and 1748*52 < 2**17 and 3233036*52 < 2**28
    return centre, other, dict(counts)


def uniform_geometry_margins():
    iv, constants, _ = c.context(256)
    radius = t.chart_bounds()['maximum_total_coordinate_displacement']
    r = iv.rational(radius.numerator, radius.denominator)[1]
    current_checks = reference_checks = 0
    for bank in t.old.loc.BANKS:
        for row in t.coframe_rows(bank):
            _, spec = t.old.coframe_spec(row, (0,)*len(row['coordinates']))
            if spec['family'] == 'current':
                original = dict(spec)
                original.pop('digits')
                original['bits'] = None
                vector = t.old.cf.vector(iv, constants, original)
                if row['coordinates']:
                    vector = [(x[0]-r, x[1]+r) for x in vector]
                current_checks += 1
            else:
                vector = t.old.coframe_vector(iv, constants, spec)
                reference_checks += 1
            # These wide intervals cover the entire open centre box AND all
            # CODE digits, not just the test centres used in angle selection.
            factors = t.old.cf.factors(iv, vector, spec)
            assert factors['norm'][0] > 0 and factors['norm'][1] < iv.scale
            assert all(2*x['radius'][0] >= factors['norm'][1]
                       for x in factors['mode_rotations'])
    # All q base time-slices; reference y vectors are unchanged and fixed.
    for x0 in range(4):
        _, psi = t.old.mat.half_vector(iv, constants, {'kind': 'q', 'x0': x0, 'bits': None})
        psi = [(x[0]-r, x[1]+r) for x in psi]
        norm = sum(max(abs(x[0]), abs(x[1]))**2 for x in psi)
        assert 15*norm < iv.scale**2
        slack_lower = iv.scale-constants['p'][1]-(-(-norm//iv.scale))
        assert 3*slack_lower > iv.scale
    return {'all_coframe_template_boxes': current_checks+reference_checks,
            'current_templates': current_checks, 'fixed_reference_templates': reference_checks,
            'all_q_time_slice_boxes': 4,
            'covers_whole_centre_box_and_all_CODE_digits': True}


def point_semantics(centre, other):
    iv, constants, _ = c.context(512)
    checks = 0
    for bank in ('f', 'q', '0', 'x+', 'y-'):
        rows = t.coframe_rows(bank)
        chosen = [next(r for r in rows if r['direction'] == role and
                       (bool(r['coordinates']) == (bank in ('f', 'q')))) for role in range(4)]
        for row in chosen:
            digits = (0, 1, 2, 3) if row['coordinates'] else ()
            v0, _ = t.coframe_vector(centre, row, digits, iv, constants)
            vo, _ = t.coframe_vector(other, row, digits, iv, constants)
            for j in range(4):
                off = other.offsets[row['coordinates'][j]] if row['coordinates'] else F(0)
                shift = iv.rational(off.numerator, off.denominator)
                assert vo[j] == iv.add(v0[j], shift)
            checks += 1
    for bank in ('q', 'y+', 'y-'):
        rows = t.material_rows(bank)
        chosen = [rows[0], rows[-1]]
        if bank == 'q':
            chosen += [next(r for r in rows if r['SAM_indices'])]
        for row in chosen:
            _, psi0 = t.material_half_vector(centre, bank, row, iv, constants)
            _, psio = t.material_half_vector(other, bank, row, iv, constants)
            ids = row['SAM_indices'][::2] if bank == 'q' else []
            for j in range(2):
                off = other.offsets[ids[j]] if ids else F(0)
                assert psio[j] == iv.add(psi0[j], iv.rational(off.numerator, off.denominator))
            checks += 1
    return checks


def local_native(centre, other):
    # Independent actual-power arithmetic: recompute G^n in complex balls,
    # not by trusting the angle-selector's modular-grid conclusion.
    balls = c.arithmetic.Certifier(24, bits=3460, precision=8192)
    checked = 0
    def verify(record, cosine, sine, bits):
        nonlocal checked
        n = int(record['k'])*record['native_exponent_multiplier']
        a, b = balls.power(n)
        shift = balls.precision-bits
        assert shift >= 0
        cosine = tuple(int(x) << shift for x in cosine)
        sine = tuple(int(x) << shift for x in sine)
        error = max(abs(a[0]-cosine[1]), abs(a[1]-cosine[0]))
        error += max(abs(b[0]-sine[1]), abs(b[1]-sine[0]))
        assert error < balls.S >> 3460
        checked += 1

    upper = c.componentwise_upper()
    unit_checks = support_checks = 0
    for field in (centre, other):
        components = c.Components(field)
        for bank in ('f', 'q', 'x-'):
            rows = t.coframe_rows(bank)
            row = next(r for r in rows if r['direction'] == 1
                       and (bool(r['coordinates']) == (bank in ('f', 'q'))))
            digits = (3, 2, 1, 0) if row['coordinates'] else ()
            lib = components.coframe_library(row, digits)
            iv, const, _ = c.context(4096)
            factors = t.coframe_factors(field, row, digits, iv, const)
            for key, cosine, sine in t.old.cf.native_angle_targets(iv, factors):
                verify(lib['angles'][str(key)], cosine, sine, 4096)
            units = components.coframe_units(row, digits)
            assert len(units) == 27
            for depth in range(3):
                actual = Counter()
                for bound, invdepth in components.coframe_units(row, digits, depth=depth):
                    actual.update(c.local.cf.unit_counts(bound, invdepth))
                bound = upper['coframe_per_sector']
                for _ in range(depth):
                    bound = c.local.prep.raw_inverse_counts(bound)
                assert all(actual[k] <= bound[k] for k in actual)
                unit_checks += 1
            # Walk emitted DAG structure without expanding repetitions/masks.
            lay = c.local.coframe_layout()
            for bound, depth in units[:2]:
                for tree in islice(c.local.cf.unit_blocks(bound, depth, lay), 4):
                    assert_tree(tree, lay['qubits'])
                    support_checks += 1
        for bank in ('q', 'y+'):
            row = next(r for r in t.material_rows(bank) if r['SAM_indices']) if bank == 'q' else t.material_rows(bank)[0]
            lib = components.material_library(bank, row)
            iv, const, _ = c.context(4096)
            vector, _ = t.material_half_vector(field, bank, row, iv, const)
            for rotation in t.old.mat.rotations(iv, vector):
                sine = rotation['sin']
                if c.local.prep.plane_geometry(rotation['other'])['orientation'] == -1:
                    sine = iv.neg(sine)
                verify(lib['angles'][str(rotation['other'])], rotation['cos'], sine, 4096)
            for depth in range(3):
                actual = Counter()
                for bound, invdepth in components.material_units(bank, row, depth=depth):
                    actual.update(c.local.cf.unit_counts(bound, invdepth))
                bound = upper['material_per_sector']
                for _ in range(depth):
                    bound = c.local.prep.raw_inverse_counts(bound)
                assert all(actual[k] <= bound[k] for k in actual)
                unit_checks += 1
    # Every quadrant, including exact zero sine and negative cosine, halts.
    for controls in (15, 24):
        selector = c.UniformAngles(controls)
        for cv, sv in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            records, _ = selector.select(lambda iv, cc: ([('t', iv.rational(cv), iv.rational(sv))], None))
            verify(records['t'], (cv*(1 << 4096),)*2, (sv*(1 << 4096),)*2, 4096)
    return {'independent_actual_G_power_checks': checked,
            'component_inverse_inventory_checks': unit_checks,
            'actual_native_DAG_trees_inspected': support_checks,
            'whole_SOURCE_or_global_G_CX_words_executed': False}


def assert_tree(tree, qubits):
    if tree['op'] == 'seq':
        for child in tree['children']:
            assert_tree(child, qubits)
    elif tree['op'] == 'repeat':
        assert int(tree['count']) > 0
        assert_tree(tree['child'], qubits)
    else:
        assert tree['op'] in ('G', 'CX', 'SourceI')
        assert all(type(q) is int and 0 <= q < qubits for q in tree['wires'])


def main():
    plan = c.build_plan()
    assert plan == json.loads((P/'REGULAR_SOURCE_COMPONENT_PLAN.json').read_text())
    centre, other, counts = validate_fields()
    result = {'status': 'PASS_PARAMETERIZED_COFRAME_CAR_COMPONENTS_WITH_UNIFORM_CHART_AND_GRID',
              'coordinate_kinds': counts, 'uniform_geometry': uniform_geometry_margins(),
              'new_field_semantic_cases': point_semantics(centre, other),
              'native_component_checks': local_native(centre, other),
              'full_global_source_and_physical_price_integrated': False,
              'production_words_executed': False, 'physical_C_closed': False, 'GR_closed': False,
              'source_sha256': {str(f): sha256(f.read_bytes()).hexdigest() for f in
                                [Path(__file__), P/'regular_field_targets.py',
                                 P/'regular_source_components.py', P/'REGULAR_SOURCE_COMPONENT_PLAN.json']}}
    (P/'REGULAR_SOURCE_COMPONENT_CHECK.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({key: value for key, value in result.items() if key != 'source_sha256'}))


if __name__ == '__main__':
    main()
