#!/usr/bin/env python3
"""First-label return of one sequential instrument, without iid reset.

Exact stopped-tree/clock fixtures use Fraction. The original full128 consumer
uses NumPy/SciPy, selecting unchanged matrix constructors from a pinned blob;
it does not replay that source's unrelated SymPy/old scientific certificates.
All checks are explicit and remain active under python -O.
"""
from __future__ import annotations

import ast
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path


CHECKS: list[str] = []


def require(ok, name):
    if not bool(ok):
        raise ArithmeticError(name)
    CHECKS.append(name)


def zero(n=2, m=None):
    return tuple(tuple(Q(0) for _ in range(n if m is None else m)) for _ in range(n))


def eye(n=2):
    return tuple(tuple(Q(i == j) for j in range(n)) for i in range(n))


def add(a, b):
    return tuple(tuple(x+y for x, y in zip(ar, br)) for ar, br in zip(a, b))


def scale(c, a):
    return tuple(tuple(c*x for x in row) for row in a)


def trans(a):
    return tuple(zip(*a))


def mul(a, b):
    return tuple(tuple(sum((x*y for x, y in zip(row, col)), Q(0))
                       for col in zip(*b)) for row in a)


def total(xs, n=2):
    out = zero(n)
    for x in xs:
        out = add(out, x)
    return out


def pull(k, x):
    return mul(mul(trans(k), x), k)


def pull_jet(k, dk, x, dx):
    return total((mul(mul(trans(dk), x), k), pull(k, dx),
                  mul(mul(trans(k), x), dk)), len(x))


def det(a):
    b = [list(row) for row in a]
    result = Q(1)
    for j in range(len(b)):
        candidates = [i for i in range(j, len(b)) if b[i][j]]
        if not candidates:
            return Q(0)
        i = candidates[0]
        if i != j:
            b[i], b[j] = b[j], b[i]
            result = -result
        pivot = b[j][j]
        result *= pivot
        for i in range(j+1, len(b)):
            factor = b[i][j]/pivot
            for h in range(j+1, len(b)):
                b[i][h] -= factor*b[j][h]
    return result


def inv2(a):
    d = det(a)
    return scale(1/d, ((a[1][1], -a[0][1]), (-a[1][0], a[0][0])))


def trace(a):
    return sum((a[i][i] for i in range(len(a))), Q(0))


def exact_instrument(m):
    b = ((Q(3, 5), Q(0)), (Q(0), Q(4, 5)))
    db = ((Q(1), Q(0)), (Q(0), Q(-1, 2)))
    d = ((Q(4, 5), Q(0)), (Q(0), Q(3, 5)))
    dd = ((Q(-3, 4), Q(0)), (Q(0), Q(2, 3)))
    u = ((Q(3, 5), Q(-4, 5)), (Q(4, 5), Q(3, 5)))
    if m == 2:
        return [b, mul(u, d)], [db, mul(u, dd)]
    return [b, scale(Q(3, 5), mul(u, d)), scale(Q(4, 5), d)], [
        db, scale(Q(3, 5), mul(u, dd)), scale(Q(4, 5), dd)]


def exact_renew(k, dk, cap, x, costs, charges):
    m = len(k)
    rs, drs = [eye() for _ in k], [zero() for _ in k]
    for _ in range(cap):
        new, dnew = [], []
        for a in range(m):
            w = x**(costs[a]+charges[a][a])
            r = scale(w, pull(k[a], eye()))
            dr = scale(w, pull_jet(k[a], dk[a], eye(), zero()))
            for b in range(m):
                if b != a:
                    w = x**(costs[b]+charges[a][b])
                    r = add(r, scale(w, pull(k[b], rs[a])))
                    dr = add(dr, scale(w, pull_jet(k[b], dk[b], rs[a], drs[a])))
            new.append(r)
            dnew.append(dr)
        rs, drs = new, dnew
    n = total(scale(x**costs[a], pull(k[a], rs[a])) for a in range(m))
    dn = total(scale(x**costs[a], pull_jet(k[a], dk[a], rs[a], drs[a])) for a in range(m))
    return n, dn


def leaves(k, dk, cap, costs, charges):
    out = []

    def extend(word, v, dv, c):
        a = word[0]
        for b in range(len(k)):
            nv = mul(k[b], v)
            ndv = add(mul(dk[b], v), mul(k[b], dv))
            nc = c+costs[b]+charges[a][b]
            nw = word+(b,)
            if b == a or len(nw)-1 == cap:
                out.append((nw, nv, ndv, nc, b != a))
            else:
                extend(nw, nv, ndv, nc)

    for a in range(len(k)):
        extend((a,), k[a], dk[a], costs[a])
    return out


def direct_tree(records, x):
    n = total(scale(x**c, pull(v, eye())) for _, v, _, c, _ in records)
    dn = total(scale(x**c, pull_jet(v, dv, eye(), zero()))
               for _, v, dv, c, _ in records)
    return n, dn


def exact_charge_effect(k, dk, cap, costs, charges):
    reward, dreward = [], []
    for a in range(len(k)):
        reward.append(total(scale(Q(costs[b]+charges[a][b]), pull(k[b], eye())) for b in range(len(k))))
        dreward.append(total(scale(Q(costs[b]+charges[a][b]), pull_jet(k[b], dk[b], eye(), zero()))
                             for b in range(len(k))))
    q, dq = [zero() for _ in k], [zero() for _ in k]
    for _ in range(cap):
        nq, ndq = [], []
        for a in range(len(k)):
            nq.append(add(reward[a], total(pull(k[b], q[a]) for b in range(len(k)) if b != a)))
            ndq.append(add(dreward[a], total(pull_jet(k[b], dk[b], q[a], dq[a])
                                            for b in range(len(k)) if b != a)))
        q, dq = nq, ndq
    value = total(add(scale(Q(costs[a]), pull(k[a], eye())), pull(k[a], q[a])) for a in range(len(k)))
    source = total(add(scale(Q(costs[a]), pull_jet(k[a], dk[a], eye(), zero())),
                       pull_jet(k[a], dk[a], q[a], dq[a])) for a in range(len(k)))
    return value, source


def exact_tests():
    cases = []
    for m in (2, 3):
        k, dk = exact_instrument(m)
        require(total(pull(v, eye()) for v in k) == eye(), f'exact complete instrument m={m}')
        require(total(pull_jet(v, dv, eye(), zero()) for v, dv in zip(k, dk)) == zero(),
                f'exact complete instrument jet m={m}')
        costs = [1+(b % 2) for b in range(m)]
        charges = [[1 if a == b else 2 for b in range(m)] for a in range(m)]
        for cap in (1, 2, 3, 5):
            records = leaves(k, dk, cap, costs, charges)
            words = [row[0] for row in records]
            require(all(not (len(a) < len(b) and b[:len(a)] == a)
                        for a in words for b in words), f'prefix-free retained leaves m={m} K={cap}')
            clean = [row for row in records if all(b == 0 for b in row[0])]
            require(len(clean) == 1 and clean[0][0] == (0, 0) and not clean[0][4],
                    f'unique clean 00 return m={m} K={cap}')
            charge, dcharge = exact_charge_effect(k, dk, cap, costs, charges)
            charged_tree = total(scale(Q(c), pull(v, eye())) for _, v, _, c, _ in records)
            dcharged_tree = total(scale(Q(c), pull_jet(v, dv, eye(), zero())) for _, v, dv, c, _ in records)
            require(charge == charged_tree and dcharge == dcharged_tree,
                    f'complete additive charge and field source m={m} K={cap}')
            for x in (Q(1), Q(9, 16)):
                n, dn = exact_renew(k, dk, cap, x, costs, charges)
                nt, dnt = direct_tree(records, x)
                require(n == nt and dn == dnt, f'independent complete tree and source m={m} K={cap} x={x}')
                require(det(n) > 0 and n[0][0] > 0, f'positive marked Gram m={m} K={cap} x={x}')
                if x == 1:
                    require(n == eye() and dn == zero(), f'no-reset complete unmarked isometry m={m} K={cap}')
            cases.append({'labels': m, 'cap': cap, 'retained_leaves': len(records)})

    # Genuine noncommuting marked source and a frozen-normalizer negative control.
    k, dk = exact_instrument(3)
    c, kap = [1, 2, 1], [[1 if a == b else 2 for b in range(3)] for a in range(3)]
    x, z = Q(9, 16), Q(1, 5)
    n, dn = exact_renew(k, dk, 3, x, c, kap)
    a = scale(Q(3, 4)**3, mul(k[0], k[0]))
    da = scale(Q(3, 4)**3, add(mul(dk[0], k[0]), mul(k[0], dk[0])))
    g, dg = pull(a, eye()), pull_jet(a, da, eye(), zero())
    require(mul(n, g) != mul(g, n), 'exact noncommuting renewal Gram and clean corner')
    h = add(scale(1-z, n), scale(z, g))
    ni, hi = inv2(n), inv2(h)
    ds = trace(add(mul(ni, dn), scale(-1, mul(hi, add(scale(1-z, dn), scale(z, dg))))))
    stable = z*trace(add(mul(mul(mul(ni, g), hi), dn), scale(-1, mul(hi, dg))))
    frozen = -z*trace(mul(hi, dg))
    require(ds == stable, 'noncommuting full source equals stable cotangent')
    require(ds != frozen, 'freezing the actual normalizer changes the source')

    # Independent sparse retained-history/forward-clock column, not a tensor assertion.
    records = leaves(k, dk, 2, c, kap)
    rho, x, active = Q(3, 4), Q(9, 16), 4
    clean_index = next(i for i, row in enumerate(records) if row[0] == (0, 0))
    cols, dcols = [], []
    for start in range(active):
        for input_grade in range(2):
            col, dcol = {}, {}
            for leaf, (_, v, dv, charge, _) in enumerate(records):
                for output_grade in range(2):
                    key = (start+charge, leaf, output_grade)
                    col[key] = rho**charge*v[output_grade][input_grade]
                    dcol[key] = rho**charge*dv[output_grade][input_grade]
            cols.append(col)
            dcols.append(dcol)
    def gram(left, right):
        return tuple(tuple(sum((v*right[j].get(key, Q(0)) for key, v in col.items()), Q(0))
                           for j in range(len(right))) for col in left)
    full_n = gram(cols, cols)
    full_dn = add(gram(dcols, cols), gram(cols, dcols))
    corner_cols = [{key: value for key, value in col.items()
                    if key[0] < active and key[1] == clean_index} for col in cols]
    full_g = gram(corner_cols, corner_cols)
    n2, dn2 = exact_renew(k, dk, 2, x, c, kap)
    block = lambda mat: tuple(tuple(mat[i % 2][j % 2] if i//2 == j//2 else Q(0)
                                    for j in range(2*active)) for i in range(2*active))
    require(full_n == block(n2) and full_dn == block(dn2), 'open full-output clock gives identical Gram per input tick')
    g2 = scale(x**3, mul(mul(k[0], k[0]), mul(k[0], k[0])))
    direct_h = add(scale(1-z, full_n), scale(z, full_g))
    small_h = add(scale(1-z, n2), scale(z, g2))
    overlap = active-3
    ratio = det(direct_h)/det(full_n)
    predicted = (det(small_h)/det(n2))**overlap*(1-z)**(2*(active-overlap))
    require(ratio == predicted, 'direct full forward-clock determinant equals overlap formula')
    clock_only_cols = [{key: value for key, value in col.items() if key[0] < active}
                       for col in cols]
    truncated = gram(clock_only_cols, clock_only_cols)
    require(truncated != full_n, 'compressing entire output would change the normalization')

    # Exact reset counterexample: both first labels have positive probability.
    projectors = [((Q(1), Q(0)), (Q(0), Q(0))), ((Q(0), Q(0)), (Q(0), Q(1)))]
    records = leaves(projectors, [zero(), zero()], 5, [1, 1], [[0, 0], [0, 0]])
    mean = total(scale(Q(len(word)), pull(v, eye())) for word, v, _, _, _ in records)
    require(mean == scale(Q(2), eye()) and mean != scale(Q(3), eye()), 'sequential projection T=2, not iid m+1=3')
    return {'status': 'EXACT_PASS', 'tree_cases': cases,
            'source': str(ds), 'frozen_normalizer_source': str(frozen),
            'reset_counterexample': 'T=2 for every positive two-label input law; iid prediction 3 is false',
            'direct_clock_active_ticks': active, 'direct_clock_clean_duration': 3}


def comparison_gates(n):
    a, b = list(range(n)), list(range(n, 2*n))
    d = list(range(2*n, 3*n))
    chain = list(range(3*n, 4*n-2))
    flag = 4*n-2
    gates = []
    for i in range(n):
        gates.extend([('CX', a[i], d[i]), ('CX', b[i], d[i])])
    gates.extend(('X', v) for v in d)
    if n == 2:
        gates.append(('CCX', d[0], d[1], flag))
    else:
        compute = [('CCX', d[0], d[1], chain[0])]
        compute.extend(('CCX', chain[i-2], d[i], chain[i-1]) for i in range(2, n-1))
        gates.extend(compute)
        gates.append(('CCX', chain[-1], d[-1], flag))
        gates.extend(reversed(compute))
    gates.extend(('X', v) for v in d)
    gates.append(('X', flag))
    for i in reversed(range(n)):
        gates.extend([('CX', b[i], d[i]), ('CX', a[i], d[i])])
    return gates, flag


def apply_bits(state, gates):
    for gate in gates:
        if gate[0] == 'X' or all((state >> i) & 1 for i in gate[1:-1]):
            state ^= 1 << gate[-1]
    return state


def comparator_tests():
    result = {}
    for n in (2, 3, 7):
        gates, flag = comparison_gates(n)
        counts = {name: sum(g[0] == name for g in gates) for name in ('X', 'CX', 'CCX')}
        require(counts == {'X': 2*n+1, 'CX': 4*n, 'CCX': 2*n-3}, f'exact clean comparator gate counts n={n}')
        for a in range(1 << n):
            for b in range(1 << n):
                raw = a | (b << n)
                for initial_flag in (0, 1):
                    value = apply_bits(raw | (initial_flag << flag), gates)
                    expected = raw | ((initial_flag ^ (a != b)) << flag)
                    if value != expected:
                        raise ArithmeticError(f'unclean comparator n={n}, a={a}, b={b}')
        require(True, f'all clean label pairs and both flags n={n}')
        # The smallest compiler permits an independent full arbitrary-ancilla census.
        if n == 2:
            outputs = {apply_bits(v, gates) for v in range(1 << (flag+1))}
            require(len(outputs) == 1 << (flag+1), 'all128 arbitrary-ancilla comparator columns are distinct')
        result[str(n)] = {'counts': counts, 'total_gates': len(gates),
                           'all_clean_label_pairs': 1 << (2*n), 'both_initial_flags': True}
    return {'status': 'EXACT_PASS', 'words': result,
            'physical_price': '28 c_CNOT + 15 c_X + 11 c_Toffoli; 54 only for unit logical charging',
            'archive_scope': 'ancillas are finally clean; intermediate X-layer states are not erased from any separately archived trace'}


def native_tests():
    import numpy as np
    import scipy
    from scipy.linalg import expm, solve_sylvester

    source = Path(__file__).resolve().parents[1]/'d0_book_uniform_source_2026-10-21'/'check_uniform_book_source.py'
    raw = source.read_bytes()
    blob = hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    require(blob == 'ee8de4635d24c668949ac9a0186616ab7d59f2ed', 'unchanged original native constructor git blob')
    wanted = {'adj', 'herm', 'root', 'creators', 'native'}
    parsed = ast.parse(raw, filename=str(source))
    nodes = [node for node in parsed.body if
             (isinstance(node, ast.FunctionDef) and node.name in wanted) or
             (isinstance(node, ast.Assign) and any(isinstance(v, ast.Name) and v.id in {'P', 'EYE'} for v in node.targets))]
    require(len(nodes) == 7, 'exact constructor AST selection; no modified native matrix definitions')
    env = {'np': np, 'expm': expm, 'solve_sylvester': solve_sylvester}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(source), 'exec'), env)
    native = env['native']
    dimension, labels, right = 16, 128, 128
    ident = np.eye(dimension, dtype=complex)
    costs = 1+np.arange(labels) % 2
    theta, comparator_charge, z = .08, 54, 2.0**-20

    def adj(x):
        return x.conj().swapaxes(-1, -2)

    def real_trace(x):
        v = np.trace(x)
        if abs(v.imag) > 1e-9:
            raise ArithmeticError('complex trace in real native source')
        return float(v.real)

    def setup(k, dk, t):
        w, f = np.exp(-t*costs), np.exp(-t*comparator_charge)
        sop = np.einsum('bki,blj,b->ijkl', k.conj(), k, w, optimize=True).reshape(256, 256)
        dsop = (np.einsum('bki,blj,b->ijkl', dk.conj(), k, w, optimize=True)
                +np.einsum('bki,blj,b->ijkl', k.conj(), dk, w, optimize=True)).reshape(256, 256)
        def cp(x):
            return (x.reshape(labels, 256) @ sop.T).reshape(labels, 16, 16)
        def dcp(x):
            return (x.reshape(labels, 256) @ dsop.T).reshape(labels, 16, 16)
        def local(x):
            return adj(k) @ x @ k
        def local_jet(x, dx):
            return adj(dk) @ x @ k + adj(k) @ dx @ k + adj(k) @ x @ dk
        h, dh = adj(k) @ k, adj(dk) @ k+adj(k) @ dk
        return w, f, cp, dcp, local, local_jet, h, dh

    def renew(k, dk, cap, t):
        w, f, cp, dcp, local, local_jet, h, dh = setup(k, dk, t)
        ws = w[:, None, None]
        r = np.broadcast_to(ident, k.shape).copy()
        dr = np.zeros_like(r)
        for _ in range(cap):
            nr = f*(ws*h+cp(r)-ws*local(r))
            ndr = f*(ws*dh+dcp(r)+cp(dr)-ws*local_jet(r, dr))
            r, dr = nr, ndr
        return np.sum(ws*local(r), axis=0), np.sum(ws*local_jet(r, dr), axis=0)

    def mean_trials(k, dk, cap):
        _, _, cp, dcp, local, local_jet, _, _ = setup(k, dk, 0.)
        r, dr = np.zeros_like(k), np.zeros_like(k)
        for _ in range(cap):
            nr = ident+cp(r)-local(r)
            ndr = dcp(r)+cp(dr)-local_jet(r, dr)
            r, dr = nr, ndr
        return ident+np.sum(local(r), axis=0), np.sum(local_jet(r, dr), axis=0)

    def book(k, dk, n, dn, t):
        b, db = k[0], dk[0]
        b2, db2 = b@b, db@b+b@db
        g = np.exp(-t*(2+comparator_charge))*(b2@b2)
        dg = np.exp(-t*(2+comparator_charge))*(db2@b2+b2@db2)
        h = (1-z)*n+z*g
        ev, vec = np.linalg.eigh((n+adj(n))/2)
        require(ev.min() > 0, 'positive original first-label marked Gram')
        nr = (vec/np.sqrt(ev))@adj(vec)
        c = nr@g@nr
        cv = np.linalg.eigvalsh((c+adj(c))/2)
        require(cv.min() > -1e-12 and cv.max() < 1+1e-12, 'clean original corner is a normalized contraction')
        variable = -right*float(np.log1p(z*(cv-1)).sum())
        cot = np.linalg.solve(n, g@np.linalg.inv(h))
        source_value = right*z*real_trace(cot@dn-np.linalg.solve(h, dg))
        frozen = -right*z*real_trace(np.linalg.solve(h, dg))
        # One overlapping clean return, with a declared unit-logical-tick window.
        clean_duration, active_ticks = 56, 57
        full_value = variable-right*(active_ticks-1)*dimension*float(np.log1p(-z))
        return {'variable_J': variable, 'J_with_clock': full_value, 'field_source': source_value,
                'frozen_normalizer_source': frozen,
                'normalizer_min_eigenvalue': float(ev.min()),
                'corner_max_eigenvalue': float(cv.max()),
                'normalizer_source_norm': float(np.linalg.norm(dn)),
                'commutator_norm': float(np.linalg.norm(n@g-g@n)),
                'clean_duration': clean_duration, 'active_ticks': active_ticks}

    k, dk = native(theta)
    require(np.linalg.norm(np.sum(adj(k)@k, axis=0)-ident) < 3e-13, 'original full128 complete column')
    require(np.linalg.norm(np.sum(adj(dk)@k+adj(k)@dk, axis=0)) < 3e-13, 'original full128 complete field jet')
    require(np.linalg.norm(k[0]-adj(k[0])) < 1e-13, 'original clean Kraus B is selfadjoint')
    require(np.linalg.eigvalsh(k[0]).min() > 0, 'original clean Kraus B is positive invertible')
    outputs = {}
    unmarked_sources = []
    for t in (0., .02):
        for cap in (1, 2, 4):
            n, dn = renew(k, dk, cap, t)
            item = book(k, dk, n, dn, t)
            if t == 0:
                require(np.linalg.norm(n-ident) < 6e-13 and np.linalg.norm(dn) < 6e-13,
                        f'unmarked sequential isometry and zero normalization source K={cap}')
                unmarked_sources.append(item['field_source'])
            else:
                # The two-trial cap1 commutator is below 2e-13 on this weak
                # native chart. Record it without promoting roundoff-scale
                # evidence; caps2/4 and the rational fixture carry this test.
                if cap > 1:
                    require(item['commutator_norm'] > 1e-12, f'genuine original noncommuting marked return K={cap}')
                require(abs(item['field_source']-item['frozen_normalizer_source']) > 1e-10,
                        f'original full normalization source cannot be omitted K={cap}')
            # Independent five-point differentiation of the unchanged native matrix family.
            step = 2e-4
            values = []
            for shift in (-2, -1, 1, 2):
                kk, _ = native(theta+shift*step)
                zz = np.zeros_like(kk)
                nn, _ = renew(kk, zz, cap, t)
                values.append(book(kk, zz, nn, np.zeros_like(nn), t)['variable_J'])
            fd = (values[0]-8*values[1]+8*values[2]-values[3])/(12*step)
            error = abs(fd-item['field_source'])
            require(error < 1e-11, f'independent original field derivative K={cap} t={t}')
            item.update({'finite_difference_source': fd, 'finite_difference_error': error})
            outputs[f't={t},K={cap}'] = item
    require(max(unmarked_sources)-min(unmarked_sources) < 1e-13, 'physical clean00 feedback is cap independent at zero mark')
    trial_outputs = {}
    for cap in (1, 2, 4):
        count, dcount = mean_trials(k, dk, cap)
        mean, dmean = real_trace(count)/dimension, real_trace(dcount)/dimension
        if cap == 1:
            require(np.linalg.norm(count-2*ident) < 1e-13 and np.linalg.norm(dcount) < 1e-13,
                    'one-comparison cap has exactly two original trials')
        else:
            require(abs(dmean) > 1e-7, f'constant per-comparison charge has nonzero stopped-count source K={cap}')
        trial_outputs[str(cap)] = {'mean_trials_for_maximally_mixed_data': mean, 'field_source': dmean,
                                   'comparison_charge_source_if_unit_logical_prices': comparator_charge*dmean}
    return {'status': 'NUMERICAL_PASS', 'source_git_blob': blob,
            'source_sha256': hashlib.sha256(raw).hexdigest(),
            'selected_unchanged_definitions': sorted(wanted)+['P', 'EYE'],
            'numpy_version': np.__version__, 'scipy_version': scipy.__version__,
            'theta': theta, 'port_charges': '1+(label mod 2)',
            'comparison_charge': comparator_charge,
            'charge_and_clock_scope': 'declared unit logical-gate diagnostic; native physical factory/clock admission is not inferred',
            'marked_map_scope': 't>0: exact generating column and its declared polar-normalized Book diagnostic, not unchanged gates',
            'unmarked_map_scope': 't=0: compiled column if the stated gate, preparation, clean factory and clock interfaces are admitted',
            'corner_cases': outputs, 'sequential_trial_counts': trial_outputs,
            'spatial_scope': 'one original L4 Fourier block and role-1 boost jet; no all42/full-spatial closure claim'}


def main():
    exact = exact_tests()
    comparator = comparator_tests()
    native = native_tests()
    result = {'status': 'PASS', 'GR_closed': False, 'check_count': len(CHECKS),
              'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'exact': exact, 'comparator': comparator, 'original_full128': native,
              'checks': CHECKS}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
