#!/usr/bin/env python3
"""Replace complete native CZ macros and remaining SI pairs by G/CX.

This is a NEW word/clock. It is not a transport of the old internal marks.
Repeat DAGs are transformed with a two-state transducer, never expanded.
One fresh arbitrary helper is reused; no clean-state promise is needed.
The complete stream's coverage is a separate structural proof obligation.
"""
from pathlib import Path
from collections import Counter
import json, sys

P = Path(__file__).resolve().parent
D = P.parent
sys.path.insert(0, str(D / 'round25'))
import global_h1 as old
nb = old.nb


def seq(*children):
    children = [t for t in children if not (t['op'] == 'seq' and not t['children'])]
    return children[0] if len(children) == 1 else nb.seq(*children)


def repeat(n, child):
    assert type(n) is int and n >= 0
    if n == 0 or (child['op'] == 'seq' and not child['children']):
        return nb.seq()
    return child if n == 1 else nb.repeat(n, child)


def source_atom(tree, port, spin):
    """Only the nested-repeat form emitted by actual literal inversions."""
    n = 1
    while tree['op'] == 'repeat':
        count = int(tree['count'])
        assert str(count) == tree['count'] and count >= 1
        n *= count
        tree = tree['child']
    if tree['op'] != 'SourceI':
        return None
    assert tree['wires'] == [port, *spin]
    return n


def exact_cz(tree, port, spin):
    """Recognize A13's whole 13/19-letter CZ at any paid inverse depth.

    No identity rewrite is accepted merely from gate counts. All CX order,
    all five SI positions and every exact repeated-SI multiplicity match.
    """
    if tree['op'] != 'seq' or len(tree['children']) not in (13, 19):
        return None
    atoms = []
    controls = set()
    multiplicities = []
    for child in tree['children']:
        if child['op'] == 'CX':
            wires = tuple(child['wires'])
            if len(wires) != 2 or wires[0] == wires[1]:
                return None
            atoms.append(('CX', wires))
            controls.update(wires)
        else:
            n = source_atom(child, port, spin)
            if n is None:
                return None
            multiplicities.append(n)
            atoms.append(('SourceI', (port, *spin)))
    if len(multiplicities) != 5 or len(set(multiplicities)) != 1:
        return None
    n = multiplicities[0]
    depth, residual = 0, n
    while residual % 3 == 0:
        residual //= 3
        depth += 1
    if residual != 1:
        return None
    controls.discard(port)
    if len(controls) not in (1, 2) or controls.intersection(spin):
        return None
    c = sorted(controls)
    pairs = [(c[0], port)] if len(c) == 1 else [c, c[::-1]]
    for a, b in pairs:
        template = [(g.op, tuple(g.wires)) for g in old.report.s.cz.cz_word(a, b, port, spin)]
        if depth % 2:
            template.reverse()
        if atoms == template:
            return {'controls': (a, b), 'inverse_depth': depth,
                    'old_SourceI': 5 * n, 'old_CX': len(atoms) - 5}
    return None


class Compiler:
    def __init__(self, port, spin, helper, k):
        assert type(k) is int and k > 0
        assert len(set((port, *spin, helper))) == 4
        self.port, self.spin, self.helper, self.k = port, tuple(spin), helper, k

    def rotation(self, multiplier):
        assert multiplier in (2, 14, 4, 12)
        return nb.repeat(multiplier * self.k, nb.gate('G', self.helper))

    def z(self):
        c, h = self.port, self.helper
        return nb.seq(nb.gate('CX', c, h), self.rotation(4),
                      nb.gate('CX', c, h), self.rotation(12))

    def cz(self, a, b):
        h = self.helper
        assert len(set((a, b, h))) == 3
        pieces = []
        for controls, multiplier in [((), 2), ((a,), 14), ((b,), 14), ((a, b), 2)]:
            parity = [nb.gate('CX', c, h) for c in controls]
            pieces.append(nb.seq(*parity, self.rotation(multiplier), *reversed(parity)))
        return nb.seq(*pieces)

    def transform(self, tree, pending=0):
        """Return (new DAG, pending SI parity, exact replacement census).

        pending=1 means one trailing SI from the preceding input has not
        yet emitted an output. Encountering a non-SI before its mate fails.
        """
        assert pending in (0, 1)
        macro = exact_cz(tree, self.port, self.spin)
        if macro is not None:
            assert not pending, 'unpaired SI immediately before native CZ'
            a, b = macro['controls']
            return self.cz(a, b), 0, Counter({
                'CZ': 1, 'CZ_old_SourceI': macro['old_SourceI'],
                'CZ_old_CX': macro['old_CX'],
                'CZ_depth_' + str(macro['inverse_depth']): 1})
        op = tree['op']
        n = source_atom(tree, self.port, self.spin)
        if n is not None:
            total = n + pending
            pairs = total // 2
            return repeat(pairs, self.z()), total % 2, Counter({'Z': pairs})
        if op == 'seq':
            out, count = [], Counter()
            for child in tree['children']:
                t, pending, c = self.transform(child, pending)
                out.append(t)
                count.update(c)
            return seq(*out), pending, count
        if op == 'repeat':
            n = int(tree['count'])
            assert str(n) == tree['count'] and n >= 1
            # At most two transitions before revisiting a parity state.
            seen, words, counts, states = {}, [], [], [pending]
            while len(words) < n and pending not in seen:
                seen[pending] = len(words)
                t, pending, c = self.transform(tree['child'], pending)
                words.append(t); counts.append(c); states.append(pending)
            if len(words) == n:
                return seq(*words), pending, sum(counts, Counter())
            start = seen[pending]
            period = len(words) - start
            cycles, tail = divmod(n - start, period)
            count = sum(counts[:start], Counter())
            cycle_count = sum(counts[start:], Counter())
            count.update({k: cycles * v for k, v in cycle_count.items()})
            count.update(sum(counts[start:start + tail], Counter()))
            out = seq(*words[:start], repeat(cycles, seq(*words[start:])), *words[start:start + tail])
            return out, states[start + tail], count
        assert op in ('G', 'CX'), 'unexpected old operation: ' + op
        assert not pending, 'unpaired SI before ' + op
        wires = tree['wires']
        assert len(wires) == {'G': 1, 'CX': 2}[op] and len(set(wires)) == len(wires)
        assert all(type(q) is int and q >= 0 for q in wires)
        assert not set(wires).intersection([*self.spin, self.helper])
        return tree, 0, Counter()

    def stream(self, blocks):
        """Boundary parity is carried across blocks, including SC6 leaves."""
        pending = 0
        for block in blocks:
            tree, pending, _ = self.transform(block, pending)
            if tree['op'] != 'seq' or tree['children']:
                yield tree
        assert pending == 0, 'unpaired terminal SourceI'


def production_compiler():
    plan = old.namespace()
    cert = json.loads((old.B / 'round57/GADGET_G_POWER_CERTIFICATE.json').read_text())
    assert cert['status'] == 'PASS_CERTIFIED_FOUR_POSITIVE_G_POWERS'
    assert cert['rotation_norm_error_each_strict_lt'] == '2^-7432'
    return Compiler(plan['layout']['port'], plan['layout']['spin'],
                    plan['layout']['qubits'], int(cert['k_hex'], 16))


def W_blocks():
    """Finite lazy NEW word; never feed it to old inverse_literal."""
    compiler = production_compiler()
    yield from compiler.stream(old.W_blocks())
