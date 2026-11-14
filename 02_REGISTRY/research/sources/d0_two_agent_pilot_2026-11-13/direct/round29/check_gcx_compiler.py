#!/usr/bin/env python3
"""Bounded tests of actual matcher, parity transducer and new gate words.

Matrix fixtures set theta=pi/8, k=1 to test the exact gadget algebra on all
columns, with floating tolerance. B57, separately, certifies ACTUAL golden
angle powers by integer intervals. These tests do not execute giant W.
"""
from pathlib import Path
from collections import Counter
from functools import lru_cache
import hashlib, json, random
import numpy as np
import gcx_compiler as c

P = Path(__file__).resolve().parent
nb = c.nb
port, spin, helper = 2, (3, 4), 5
compiler = c.Compiler(port, spin, helper, 1)
src = nb.source(port, spin)


def cz(a, b):
    return nb.seq(*(nb.gate(z.op, *z.wires) for z in c.old.report.s.cz.cz_word(a, b, port, spin)))


def inv(t, depth):
    for _ in range(depth):
        t = nb.inverse_literal(t, port, spin)
    return t


def reference_tokens(t):
    macro = c.exact_cz(t, port, spin)
    if macro is not None:
        yield ('CZ', macro['old_SourceI'], macro['old_CX'])
    elif t['op'] == 'seq':
        for x in t['children']:
            yield from reference_tokens(x)
    elif t['op'] == 'repeat':
        for _ in range(int(t['count'])):
            yield from reference_tokens(t['child'])
    else:
        yield (t['op'],)


def check_counts(t):
    out, pending, stats = compiler.transform(t)
    assert pending == 0
    raw, expected = Counter(), Counter()
    for token in reference_tokens(t):
        if token[0] == 'CZ':
            expected['CZ'] += 1
            expected['CZ_old_SourceI'] += token[1]
            expected['CZ_old_CX'] += token[2]
        else:
            raw[token[0]] += 1
    assert raw['SourceI'] % 2 == 0
    expected['Z'] = raw['SourceI'] // 2
    for key in expected:
        assert stats[key] == expected[key], (key, stats, expected)
    actual = Counter(nb.counts(out))
    assert actual == Counter({'G': raw['G'] + 32 * expected['CZ'] + 16 * expected['Z'],
                              'CX': raw['CX'] + 8 * expected['CZ'] + 2 * expected['Z']})
    assert all(z['op'] in ('G', 'CX') and not set(z['wires']).intersection(spin)
               for z in nb.leaves(out))
    return out


def mul(a, b):
    return np.einsum('ij,jk->ik', a, b, optimize=False)


def power(a, n):
    r = np.eye(len(a))
    while n:
        if n & 1:
            r = mul(r, a)
        n //= 2
        if n:
            a = mul(a, a)
    return r


@lru_cache(None)
def leaf_matrix(op, wires):
    if op == 'G':
        t = np.pi / 8
        local = np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])
    elif op == 'CX':
        local = np.eye(4)[[0, 1, 3, 2]]
    else:
        assert op == 'SourceI'
        # Independent real quaternion block, including both Spin factors.
        Li = np.array([[0, -1, 0, 0], [1, 0, 0, 0],
                       [0, 0, 0, -1], [0, 0, 1, 0]])
        local = np.zeros((8, 8)); local[:4, :4] = np.eye(4); local[4:, 4:] = Li
    result = np.zeros((64, 64))
    for j in range(64):
        col = sum(((j >> (5-q)) & 1) << (len(wires)-1-i) for i, q in enumerate(wires))
        for row in range(len(local)):
            i = j
            for k, q in enumerate(wires):
                bit = (row >> (len(wires)-1-k)) & 1
                i = (i & ~(1 << (5-q))) | (bit << (5-q))
            result[i, j] = local[row, col]
    return result


def matrix(t):
    if t['op'] == 'seq':
        r = np.eye(64)
        for x in t['children']:
            r = mul(matrix(x), r)
        return r
    if t['op'] == 'repeat':
        return power(matrix(t['child']), int(t['count']))
    return leaf_matrix(t['op'], tuple(t['wires']))


def main():
    # Every orientation, one/two routed controls, integer depths through 6.
    matcher_cases = 0
    for a, b in [(0, 1), (1, 0), (0, port), (port, 1)]:
        for depth in range(7):
            t = inv(cz(a, b), depth)
            m = c.exact_cz(t, port, spin)
            assert m and m['inverse_depth'] == depth and m['old_SourceI'] == 5 * 3**depth
            check_counts(t); matcher_cases += 1
    # Whole macro recognition must not reduce merely from inventory.
    broken = cz(0, 1)
    broken['children'][0] = nb.gate('CX', 0, 1)
    assert c.exact_cz(broken, port, spin) is None
    rejected = 0
    for t in [src, nb.seq(src, nb.gate('G', 0)), nb.seq(src, cz(0, 1)), broken]:
        try:
            list(compiler.stream([t]))
        except AssertionError:
            rejected += 1
        else:
            raise AssertionError('malformed input accepted')
    # State cycles of period one and two, including split block boundaries.
    for n in range(1, 11):
        t = nb.seq(nb.repeat(n, src), nb.repeat(n, src))
        check_counts(t)
        assert Counter(nb.counts(nb.seq(*compiler.stream([nb.repeat(n, src), nb.repeat(n, src)])))) == {'G': 16*n, 'CX': 2*n}
    huge = (1 << 10000) + 7
    t, p, count = compiler.transform(nb.repeat(huge, nb.seq(src)))
    assert p == 1 and count['Z'] == huge // 2
    assert Counter(nb.counts(t)) == {'G': 16*(huge//2), 'CX': 2*(huge//2)}
    # Boundary-state transient: repeated S;G;S starts valid only after an S.
    t = nb.seq(src, nb.repeat(7, nb.seq(src, nb.gate('G', 0), src)), src)
    check_counts(t)
    seeds = [nb.z_word(0, port, spin), nb.z_word(port, port, spin),
             nb.rotation_power(0, -3, port, spin), nb.rotation_power(port, -2, port, spin),
             nb.boolean_word('X', 1, target=0, port=port, spin=spin),
             nb.boolean_word('H', 1, target=1, port=port, spin=spin), cz(0, 1)]
    fixtures = [inv(t, depth) for t in seeds for depth in range(4)]
    rng = random.Random(2901)
    for _ in range(32):
        fixtures.append(nb.seq(*(nb.repeat(rng.randrange(1, 4), rng.choice(fixtures[:28])) for _ in range(3))))
    max_error = 0.0
    for t in fixtures:
        out = check_counts(t)
        error = float(np.max(np.abs(matrix(t) - matrix(out))))
        assert error < 2e-10, error
        max_error = max(max_error, error)
    # Production k is used symbolically, not expanded, in actual emitted DAGs.
    production = c.production_compiler()
    out, p, count = production.transform(nb.seq(nb.source(production.port, production.spin), nb.source(production.port, production.spin)))
    assert p == 0 and count['Z'] == 1
    assert Counter(nb.counts(out)) == {'G': 16*production.k, 'CX': 2}
    pins = [Path(__file__), P/'gcx_compiler.py', c.D/'round13/compile_native_cz.py',
            c.D/'round14/native_boolean.py', c.old.B/'round57/GADGET_G_POWER_CERTIFICATE.json']
    result = {'status': 'PASS_BOUNDED_COMPILER_AND_ALL_COLUMN_IDEAL_GADGET_FIXTURES',
              'exact_matcher_cases': matcher_cases, 'malformed_cases_rejected': rejected,
              'matrix_fixtures': len(fixtures), 'matrix_dimension': 64,
              'matrix_fixture_theta': 'pi/8, k=1; not actual golden angle',
              'matrix_max_abs_error': max_error, 'matrix_tolerance': 2e-10,
              'repeat_test_exponent_bit_length': huge.bit_length(),
              'production_k_bit_length': production.k.bit_length(),
              'giant_W_expanded': False, 'complete_provider_coverage_is_separate': True,
              'source_sha256': {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in pins},
              'physical_C_closed': False, 'GR_closed': False}
    (P/'GCX_COMPILER_CHECK.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ('status', 'exact_matcher_cases', 'matrix_fixtures', 'matrix_max_abs_error')}))


if __name__ == '__main__':
    main()
