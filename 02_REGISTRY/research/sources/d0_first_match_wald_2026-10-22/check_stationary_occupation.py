#!/usr/bin/env python3
"""Exact bounded no-reset first-match occupation/source diagnostics.

Stdlib only. Two genuinely correlated rational Kraus instruments are checked
against every complete stopped word through K=5, including cap aborts. This
does not rerun the native full128 suites or certify a physical Info/Book map.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json


def mat(rows):
    return tuple(tuple(F(x) for x in row) for row in rows)


I = mat([[1, 0], [0, 1]])
O = mat([[0, 0], [0, 0]])


def add(*xs):
    return tuple(tuple(sum((x[i][j] for x in xs), F(0))
                       for j in range(2)) for i in range(2))


def scale(c, x):
    return tuple(tuple(c * v for v in row) for row in x)


def mul(a, b):
    return tuple(tuple(sum((a[i][k] * b[k][j] for k in range(2)), F(0))
                       for j in range(2)) for i in range(2))


def adj(x):
    # These fixtures are real; every independent real matrix unit is kept.
    return tuple(zip(*x))


def tr(x):
    return x[0][0] + x[1][1]


def branch(k, x):
    return mul(mul(k, x), adj(k))


def branch_jet(k, dk, x):
    return add(mul(mul(dk, x), adj(k)), mul(mul(k, x), adj(dk)))


def effect(k):
    return mul(adj(k), k)


def effect_jet(k, dk):
    return add(mul(adj(dk), k), mul(adj(k), dk))


def channel(ks, x, omit=None):
    return add(*(branch(k, x) for b, k in enumerate(ks) if b != omit))


def channel_jet(ks, dks, x, omit=None):
    return add(*(branch_jet(k, dk, x)
                 for b, (k, dk) in enumerate(zip(ks, dks)) if b != omit))


def dual(ks, x, omit=None):
    return add(*(mul(mul(adj(k), x), k)
                 for b, k in enumerate(ks) if b != omit))


def dual_jet(ks, dks, x, omit=None):
    return add(*(add(mul(mul(adj(dk), x), k), mul(mul(adj(k), x), dk))
                 for b, (k, dk) in enumerate(zip(ks, dks)) if b != omit))


def flat(x):
    return [v for row in x for v in row]


def unflat(x):
    return mat([x[:2], x[2:]])


def solve(a, b):
    n = len(b)
    a = [list(row) + [rhs] for row, rhs in zip(a, b)]
    for col in range(n):
        pivot = next(j for j in range(col, n) if a[j][col])
        a[col], a[pivot] = a[pivot], a[col]
        v = a[col][col]
        a[col] = [z / v for z in a[col]]
        for j in range(n):
            if j != col:
                v = a[j][col]
                a[j] = [x - v * y for x, y in zip(a[j], a[col])]
    return [row[-1] for row in a]


def one_minus_channel(ks, omit=None):
    cols = []
    for j in range(4):
        basis = unflat([F(i == j) for i in range(4)])
        cols.append(flat(add(basis, scale(-1, channel(ks, basis, omit)))))
    return [list(row) for row in zip(*cols)]


def resolvent(ks, omit, x):
    return unflat(solve(one_minus_channel(ks, omit), flat(x)))


def stationary(ks, forcing=None):
    a = one_minus_channel(ks)
    a[-1] = [F(1), F(0), F(0), F(1)]
    rhs = [F(0)] * 4 if forcing is None else flat(forcing)
    rhs[-1] = F(1) if forcing is None else F(0)
    return unflat(solve(a, rhs))


CHECKS = 0


def require(value, label):
    global CHECKS
    CHECKS += 1
    if not value:
        raise AssertionError(label)


def occupations(ks, dks, rho, drho, cap):
    out = []
    for a, (ka, dka) in enumerate(zip(ks, dks)):
        state = branch(ka, rho)
        dstate = add(branch_jet(ka, dka, rho), branch(ka, drho))
        x = dx = O
        for _ in range(cap):
            x, dx = add(x, state), add(dx, dstate)
            state, dstate = channel(ks, state, a), add(
                channel_jet(ks, dks, state, a), channel(ks, dstate, a))
        out.append((x, dx))
    return out


def tree(ks, dks, rho, drho, c, dc, fee, dfee, cap):
    """Keep every terminal match and every terminal cap-abort word."""
    leaves = []

    def finish(word, amp, damp, cost, dcost, aborted):
        e = effect(amp)
        de = effect_jet(amp, damp)
        prob = tr(mul(rho, e))
        dprob = tr(add(mul(drho, e), mul(rho, de)))
        leaves.append(dict(word=word, e=e, de=de, p=prob, dp=dprob,
                           c=cost, dc=dcost, abort=aborted))

    def visit(a, word, amp, damp, cost, dcost):
        if len(word) == cap + 1:
            finish(word, amp, damp, cost, dcost, True)
            return
        for b, (kb, dkb) in enumerate(zip(ks, dks)):
            new = mul(kb, amp)
            dnew = add(mul(dkb, amp), mul(kb, damp))
            nc, ndc = cost + c[b] + fee[a][b], dcost + dc[b] + dfee[a][b]
            if a == b:
                finish(word + (b,), new, dnew, nc, ndc, False)
            else:
                visit(a, word + (b,), new, dnew, nc, ndc)

    for a, (ka, dka) in enumerate(zip(ks, dks)):
        visit(a, (a,), ka, dka, c[a], dc[a])
    return leaves


def charge_effect(ks, dks, c, dc, fee, dfee, cap):
    es = [effect(k) for k in ks]
    des = [effect_jet(k, dk) for k, dk in zip(ks, dks)]
    one = add(*(scale(cb, eb) for cb, eb in zip(c, es)))
    done = add(*(add(scale(dcb, eb), scale(cb, deb))
                 for cb, dcb, eb, deb in zip(c, dc, es, des)))
    total, dtotal = one, done
    for a, (ka, dka) in enumerate(zip(ks, dks)):
        la = add(one, *(scale(fee[a][b], es[b]) for b in range(len(ks))))
        dla = add(done, *(add(scale(dfee[a][b], es[b]),
                             scale(fee[a][b], des[b])) for b in range(len(ks))))
        bk = dbk = O
        for _ in range(cap):
            bk, dbk = add(la, dual(ks, bk, a)), add(
                dla, dual_jet(ks, dks, bk, a), dual(ks, dbk, a))
        total = add(total, mul(mul(adj(ka), bk), ka))
        dtotal = add(dtotal, mul(mul(adj(dka), bk), ka),
                     mul(mul(adj(ka), dbk), ka), mul(mul(adj(ka), bk), dka))
    return total, dtotal


def marked_gram(ks, c, fee, cap, x):
    total = O
    for a, ka in enumerate(ks):
        terminal = scale(x ** (c[a] + fee[a][a]), effect(ka))
        rk = I
        for _ in range(cap):
            rk = add(terminal, *(scale(x ** (c[b] + fee[a][b]),
                                       mul(mul(adj(kb), rk), kb))
                                  for b, kb in enumerate(ks) if b != a))
        total = add(total, scale(x ** c[a], mul(mul(adj(ka), rk), ka)))
    return total


def run_fixture(name, ks, dks):
    m = len(ks)
    require(add(*(effect(k) for k in ks)) == I, name + ' completeness')
    require(add(*(effect_jet(k, dk) for k, dk in zip(ks, dks))) == O,
            name + ' differentiated completeness')
    rho = stationary(ks)
    require(channel(ks, rho) == rho and tr(rho) == 1, name + ' stationary')
    require(rho == adj(rho) and rho[0][0] > 0 and
            rho[0][0] * rho[1][1] - rho[0][1] ** 2 > 0, name + ' faithful')
    q = [tr(branch(k, rho)) for k in ks]
    require(all(x > 0 for x in q), name + ' active outcomes')
    p00 = tr(branch(ks[0], branch(ks[0], rho)))
    require(p00 != q[0] ** 2, name + ' genuinely noniid')
    drho_star = stationary(ks, channel_jet(ks, dks, rho))
    require(add(channel_jet(ks, dks, rho), channel(ks, drho_star),
                scale(-1, drho_star)) == O, name + ' moving stationary source')

    c = [b + 1 for b in range(m)]
    dc = [F(2 * b - 1, 7) for b in range(m)]
    fee = [[1 + (2 * a + b) % 3 for b in range(m)] for a in range(m)]
    dfee = [[F(a - b, 11) + F(a == b, 13) for b in range(m)] for a in range(m)]
    drho_free = mat([[F(1, 7), F(1, 11)], [F(1, 11), F(-1, 7)]])
    cases = [('fixed_stationary_base', rho, O),
             ('moving_stationary', rho, drho_star),
             ('independent_preparation', scale(F(1, 2), I), drho_free)]
    max_leaves = 0
    for case, r, dr in cases:
        delta = add(channel(ks, r), scale(-1, r))
        ddelta = add(channel_jet(ks, dks, r), channel(ks, dr), scale(-1, dr))
        for cap in range(1, 6):
            label = name + '/' + case + '/K=' + str(cap)
            occ = occupations(ks, dks, r, dr, cap)
            leaves = tree(ks, dks, r, dr, c, dc, fee, dfee, cap)
            max_leaves = max(max_leaves, len(leaves))
            require(sum(v['p'] for v in leaves) == 1 and
                    sum(v['dp'] for v in leaves) == 0, label + ' full normalization/source')
            require(add(*(v['e'] for v in leaves)) == I and
                    add(*(v['de'] for v in leaves)) == O, label + ' operator normalization/source')
            count = 1 + sum(tr(x) for x, dx in occ)
            dcount = sum(tr(dx) for x, dx in occ)
            require(count == sum(len(v['word']) * v['p'] for v in leaves) and
                    dcount == sum(len(v['word']) * v['dp'] for v in leaves),
                    label + ' stopped trial count/source')
            for a, (xa, dxa) in enumerate(occ):
                power, dpower = r, dr
                defect_sum = ddefect_sum = O
                defect, ddefect = delta, ddelta
                for _ in range(cap):
                    defect_sum, ddefect_sum = add(defect_sum, defect), add(ddefect_sum, ddefect)
                    power, dpower = channel(ks, power, a), add(
                        channel_jet(ks, dks, power, a), channel(ks, dpower, a))
                    defect, ddefect = channel(ks, defect, a), add(
                        channel_jet(ks, dks, defect, a), channel(ks, ddefect, a))
                require(xa == add(r, scale(-1, power), defect_sum) and
                        dxa == add(dr, scale(-1, dpower), ddefect_sum),
                        label + ' finite stationarity defect and source a=' + str(a))
                for b, (kb, dkb) in enumerate(zip(ks, dks)):
                    nb = tr(branch(kb, xa))
                    dnb = tr(add(branch_jet(kb, dkb, xa), branch(kb, dxa)))
                    nt = dnt = F(0)
                    for v in leaves:
                        number = v['word'][1:].count(b) if v['word'][0] == a else 0
                        nt += number * v['p']
                        dnt += number * v['dp']
                    require((nb, dnb) == (nt, dnt), label + ' cell occupation/source')
            ce, dce = charge_effect(ks, dks, c, dc, fee, dfee, cap)
            ct = add(*(scale(v['c'], v['e']) for v in leaves))
            dct = add(*(add(scale(v['dc'], v['e']), scale(v['c'], v['de']))
                        for v in leaves))
            require((ce, dce) == (ct, dct), label + ' charge operator/full source')
            mean = tr(mul(r, ce))
            dmean = tr(add(mul(dr, ce), mul(r, dce)))
            require(mean == sum(v['p'] * v['c'] for v in leaves) and
                    dmean == sum(v['dp'] * v['c'] + v['p'] * v['dc'] for v in leaves),
                    label + ' actual moving scalar-ledger mean/source')
            for x in (F(2, 3), F(3, 4)):
                mg = marked_gram(ks, c, fee, cap, x)
                require(mg == add(*(scale(x ** v['c'], v['e']) for v in leaves)),
                        label + ' complete marked Gram')
                require(mg != I, label + ' positive mark is not physical normalization')

    # Exact resolvent identities, including a nonzero off-stationary first source.
    ddelta_fixed = channel_jet(ks, dks, rho)
    dcount_fixed = F(0)
    for a, ka in enumerate(ks):
        xa = resolvent(ks, a, branch(ka, rho))
        require(xa == rho, name + ' stationary full occupation a=' + str(a))
        dxa = resolvent(ks, a, add(branch_jet(ka, dks[a], rho),
                                  channel_jet(ks, dks, xa, a)))
        require(dxa == resolvent(ks, a, ddelta_fixed), name + ' stationary-base defect source')
        dcount_fixed += tr(dxa)
        dxmoving = add(drho_star, resolvent(ks, a, add(
            channel_jet(ks, dks, rho), channel(ks, drho_star), scale(-1, drho_star))))
        require(dxmoving == drho_star, name + ' moving stationary occupation source')
        for b, kb in enumerate(ks):
            require(tr(branch(kb, xa)) == q[b], name + ' correlated cell law')
        r = scale(F(1, 2), I)
        delta = add(channel(ks, r), scale(-1, r))
        require(resolvent(ks, a, branch(ka, r)) == add(r, resolvent(ks, a, delta)),
                name + ' arbitrary-preparation exact defect')
    require(dcount_fixed != 0, name + ' freezing preparation changes first-count source')
    require(sum(q[b] * sum(F(1 if a == b else 2) for a in range(m))
                for b in range(m)) == 2 * m - 1, name + ' conditional balanced fee')

    # A retained finite preparation prefix: exact defect and its full derivative.
    r, dr = scale(F(1, 2), I), drho_free
    delta, ddelta = add(channel(ks, r), scale(-1, r)), add(
        channel_jet(ks, dks, r), channel(ks, dr), scale(-1, dr))
    evolved_delta, evolved_ddelta = delta, ddelta
    for length in range(6):
        require(add(channel(ks, r), scale(-1, r)) == evolved_delta and
                add(channel_jet(ks, dks, r), channel(ks, dr), scale(-1, dr)) == evolved_ddelta,
                name + ' finite paid prefix defect/source L=' + str(length))
        r, dr = channel(ks, r), add(channel_jet(ks, dks, r), channel(ks, dr))
        evolved_delta, evolved_ddelta = channel(ks, evolved_delta), add(
            channel_jet(ks, dks, evolved_delta), channel(ks, evolved_ddelta))

    return {'name': name, 'outcomes': m, 'stationary_density': [[str(v) for v in row] for row in rho],
            'one_label_probabilities': [str(v) for v in q],
            'non_iid_joint00_minus_product': str(p00 - q[0] ** 2),
            'uncapped_stationary_mean_trials': m + 1,
            'frozen_preparation_mean_trial_first_source': str(dcount_fixed),
            'largest_complete_tree_leaves': max_leaves}


def main():
    base = [mat([[F(3, 5), 0], [0, F(4, 5)]]),
            mat([[0, F(3, 5)], [F(4, 5), 0]])]
    dbase = [mat([[F(4, 5), 0], [0, 0]]),
             mat([[0, 0], [F(-3, 5), 0]])]
    rotation = mat([[F(3, 5), F(-4, 5)], [F(4, 5), F(3, 5)]])
    three = [scale(F(3, 5), k) for k in base] + [scale(F(4, 5), rotation)]
    dthree = [scale(F(3, 5), k) for k in dbase] + [O]
    fixtures = [run_fixture('nonunital_two_kraus', base, dbase),
                run_fixture('rotated_three_kraus', three, dthree)]
    # Unique stationarity is essential: projective readout returns immediately.
    projection = [mat([[1, 0], [0, 0]]), mat([[0, 0], [0, 1]])]
    for cap in range(1, 6):
        occ = occupations(projection, [O, O], scale(F(1, 2), I), O, cap)
        require(1 + sum(tr(x) for x, dx in occ) == 2,
                'projective hostile control gives 2 trials, not iid 3')

    result = {'status': 'PASS', 'exact_checks': CHECKS, 'arithmetic': 'stdlib Fraction',
              'finite_caps': [1, 2, 3, 4, 5], 'preparation_prefix_lengths': [0, 1, 2, 3, 4, 5],
              'fixtures': fixtures, 'projective_counterexample_trials': 2,
              'native_full128_suite_rerun': False, 'iid_information_inferred': False,
              'selected_physical_preparation_claimed': False,
              'full_book_source_closed': False,
              'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
