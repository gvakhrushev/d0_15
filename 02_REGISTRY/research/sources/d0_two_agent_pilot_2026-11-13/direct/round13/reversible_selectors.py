#!/usr/bin/env python3
"""Fixed reversible selector circuits in the explicit X/CX/CCX basis.

All inputs are read-only, even at intermediate gates. Work is computational
zero at entry and restored on exit. These are logical circuits, not native
Golden factory admissions. The iterator expands every macro into named gates.
"""
from collections import Counter
from itertools import product


def cc_signed(a, positive_a, b, positive_b, target):
    """target ^= literal(a) & literal(b), without changing either input."""
    assert len({a, b, target}) == 3
    if not positive_a and not positive_b:
        yield ('X', target)
    if not positive_a:
        yield ('CX', b, target)
    if not positive_b:
        yield ('CX', a, target)
    yield ('CCX', a, b, target)


def pattern_gate(controls, pattern, target, work):
    """Clean multi-literal toggle, explicitly expanded into <=2-control gates."""
    k = len(controls)
    assert len(set(controls+[target]+work)) == len(controls)+1+len(work)
    assert 0 <= pattern < 2**k
    if not k:
        yield ('X', target)
    elif k == 1:
        if not pattern:
            yield ('X', target)
        yield ('CX', controls[0], target)
    elif k == 2:
        yield from cc_signed(controls[0], bool(pattern&1), controls[1], bool(pattern&2), target)
    else:
        assert len(work) >= k-2
        forward = list(cc_signed(controls[0], bool(pattern&1), controls[1], bool(pattern&2), work[0]))
        for i in range(2, k-1):
            forward.extend(cc_signed(work[i-2], True, controls[i], bool((pattern>>i)&1), work[i-1]))
        yield from forward
        yield from cc_signed(work[k-3], True, controls[-1], bool((pattern>>(k-1))&1), target)
        yield from reversed(forward)


def compare_compute(register, threshold, borrows):
    """Compute all subtraction borrows for x-threshold, LSB first."""
    assert 0 < threshold < 2**len(register)
    assert len(borrows) == len(register)+1
    for i, x in enumerate(register):
        old, new = borrows[i:i+2]
        if (threshold>>i)&1:
            # b' = 1-x+x*b, exact on Boolean inputs.
            yield ('X', new)
            yield ('CX', x, new)
            yield ('CCX', x, old, new)
        else:
            # b' = b-x*b.
            yield ('CX', old, new)
            yield ('CCX', x, old, new)


def compare_xor(register, threshold, target, borrows):
    """target ^= [unsigned(register) < threshold]; clean borrowed workspace."""
    assert 0 <= threshold <= 2**len(register)
    if threshold == 0:
        return
    if threshold == 2**len(register):
        yield ('X', target)
        return
    forward = list(compare_compute(register, threshold, borrows))
    yield from forward
    yield ('CX', borrows[-1], target)
    yield from reversed(forward)


def prefix_codes(n):
    """Raw n-bit Golden word -> kind and lexicographic rank of stopped prefix."""
    prefixes = [set(), set()]
    raw = []
    for bits in product((0, 1), repeat=n):
        total = 0
        prefix = []
        for bit in bits:
            if total >= n:
                break
            total += 1+bit
            prefix.append(bit)
        kind = total-n
        assert kind in (0, 1)
        prefixes[kind].add(tuple(prefix))
        raw.append((bits, kind, tuple(prefix)))
    ranks = [{pre: i for i, pre in enumerate(sorted(rows))} for rows in prefixes]
    codes = []
    for bits, kind, prefix in raw:
        word = sum(b<<i for i, b in enumerate(bits))
        codes.append([word, kind, ranks[kind][prefix]])
    return sorted(codes)


def make_plan(palette):
    n, r = palette['golden_coins_n'], palette['fair_bits_r']
    parts = palette['partitions']
    codes = prefix_codes(n)
    rank_width = max(row[2] for row in codes).bit_length()
    j_width = max(1, (len(parts)-1).bit_length())
    label_width = max(1, (max(len(p['weights']) for p in parts)-1).bit_length())
    cursor = 0
    layout = {}
    for name, size in [('palette',j_width), ('golden',n), ('fair',r), ('output',label_width+1),
                       ('kind',1), ('rank',rank_width), ('row_flag',1),
                       ('pattern_work',max(0,j_width-1,n-2)),
                       ('borrows',r+rank_width+1), ('less',1)]:
        layout[name] = list(range(cursor, cursor+size))
        cursor += size
    rows = []
    for j, partition in enumerate(parts):
        counts = [[int(x) for x in pair] for pair in partition['counts_ready_then_abort']]
        # Last code (abort) is zero. Remaining codes contain READY in their MSB.
        out_codes = [i | (1<<label_width) for i in range(len(counts)-1)]+[0]
        for kind in (0, 1):
            cumulative = 0
            boundaries = []
            for i, count in enumerate(counts[:-1]):
                cumulative += count[kind]
                mask = out_codes[i]^out_codes[i+1]
                if cumulative and mask:
                    boundaries.append([str(cumulative), mask])
            rows.append({'palette':j, 'kind':kind, 'boundaries':boundaries})
    return {'schema':'d0.logical.reversible.selector.v1', 'primitive_basis':['X','CX','CCX'],
            'wire_count':cursor, 'layout':layout, 'palette_count':len(parts),
            'label_width':label_width, 'prefix_codes':codes, 'rows':rows,
            'output_encoding':'low bits label index; high bit READY; all-zero on abort/invalid palette',
            'work_input':'all named kind/rank/row/pattern/borrows/less work wires are computational zero',
            'all_inputs_read_only_at_every_gate':True, 'work_restored':True,
            'native_gate_word':False, 'GR_closed':False}


def prefix_word(plan):
    q = plan['layout']
    outputs = q['kind']+q['rank']
    for raw, kind, rank in plan['prefix_codes']:
        code = kind | (rank<<1)
        for bit, target in enumerate(outputs):
            if (code>>bit)&1:
                yield from pattern_gate(q['golden'], raw, target, q['pattern_work'])


def row_word(plan, row):
    q = plan['layout']
    controls = q['palette']+q['kind']
    pattern = row['palette'] | (row['kind']<<len(q['palette']))
    flag = q['row_flag'][0]
    selector = list(pattern_gate(controls, pattern, flag, q['pattern_work']))
    yield from selector
    reg = q['fair']+q['rank']
    for threshold, mask in row['boundaries']:
        compute = list(compare_xor(reg, int(threshold), q['less'][0], q['borrows']))
        yield from compute
        for i, target in enumerate(q['output']):
            if (mask>>i)&1:
                yield ('CCX', flag, q['less'][0], target)
        yield from reversed(compute)
    yield from reversed(selector)


def selector_word(plan):
    """Expand full fixed word, with no branch on any quantum input."""
    prefix = list(prefix_word(plan))
    yield from prefix
    for row in plan['rows']:
        yield from row_word(plan, row)
    yield from reversed(prefix)


def first_success_plan(attempts, label_width):
    assert attempts >= 1 and label_width >= 1
    cursor=0
    layout={}
    for name,size in [('labels',attempts*label_width),('ready',attempts),
                      ('output',label_width),('out_ready',1),
                      ('survive',attempts+1),('chosen',attempts)]:
        layout[name]=list(range(cursor,cursor+size));cursor+=size
    return {'schema':'d0.logical.first-success-label.v1','attempts':attempts,
            'label_width':label_width,'layout':layout,'wire_count':cursor,
            'scope':'coherent labels only; not copying or routing arbitrary quantum payloads',
            'primitive_basis':['X','CX','CCX'],'native_gate_word':False,'GR_closed':False}


def first_success_word(plan):
    q=plan['layout'];cap=plan['attempts'];width=plan['label_width']
    forward=[('X',q['survive'][0])]
    for i in range(cap):
        forward.extend([('CCX',q['survive'][i],q['ready'][i],q['chosen'][i]),
                        ('CX',q['survive'][i],q['survive'][i+1]),
                        ('CX',q['chosen'][i],q['survive'][i+1])])
    yield from forward
    for i in range(cap):
        for b in range(width):
            yield ('CCX',q['chosen'][i],q['labels'][i*width+b],q['output'][b])
        yield ('CX',q['chosen'][i],q['out_ready'][0])
    yield from reversed(forward)


def apply_word(word, state):
    """Independent of compiler semantics: execute individual named gate tuples."""
    for gate in word:
        kind, *w = gate
        if kind == 'X':
            state ^= 1<<w[0]
        elif kind == 'CX':
            if (state>>w[0])&1: state ^= 1<<w[1]
        elif kind == 'CCX':
            if ((state>>w[0])&(state>>w[1]))&1: state ^= 1<<w[2]
        else:
            raise ValueError(kind)
    return state


def put(state, wires, value):
    assert 0 <= value < 2**len(wires)
    for i, wire in enumerate(wires):
        state=(state & ~(1<<wire)) | (((value>>i)&1)<<wire)
    return state


def get(state, wires):
    return sum(((state>>wire)&1)<<i for i,wire in enumerate(wires))


def counts_of(word):
    return dict(Counter(gate[0] for gate in word))
