#!/usr/bin/env python3
"""Narrow consumers of generated thermal, causal and native port sources.

Exact rational finite histories and Hodge identities are distinguished from
Decimal transcendental evaluations and the original CAR16 floating consumer.
No old suite is imported or replayed. All checks survive Python -O.
"""
from __future__ import annotations

import ast
from decimal import Decimal as D, localcontext
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path

CHECKS = []


def require(ok, label):
    if not bool(ok):
        raise ArithmeticError(label)
    CHECKS.append(label)


def dec(x):
    return D(x.numerator)/D(x.denominator) if isinstance(x, Q) else D(x)


def eye(n, kind=Q):
    return tuple(tuple(kind(i == j) for j in range(n)) for i in range(n))


def zero(n, kind=Q):
    return tuple(tuple(kind(0) for _ in range(n)) for _ in range(n))


def add(a, b):
    return tuple(tuple(x+y for x, y in zip(ar, br)) for ar, br in zip(a, b))


def sc(c, a):
    return tuple(tuple(c*x for x in row) for row in a)


def trp(a):
    return tuple(zip(*a))


def mm(a, b):
    return tuple(tuple(sum(x*y for x, y in zip(row, col)) for col in zip(*b)) for row in a)


def trace(a):
    return sum(a[i][i] for i in range(len(a)))


def total(xs, n=2, kind=Q):
    out = zero(n, kind)
    for a in xs:
        out = add(out, a)
    return out


def dm(a):
    return tuple(tuple(dec(x) for x in row) for row in a)


def push(k, x):
    return mm(mm(k, x), trp(k))


def pull(k, x):
    return mm(mm(trp(k), x), k)


def gate_jet(k, dk, x):
    return add(mm(mm(dk, x), trp(k)), mm(mm(k, x), trp(dk)))


def rot(t):
    den = 1+t*t
    c, s = (1-t*t)/den, 2*t/den
    dc, ds = -4*t/den**2, 2*(1-t*t)/den**2
    return ((c, -s), (s, c)), ((dc, -ds), (ds, dc))


def rational_input(t):
    r, dr = rot(t)
    ri, dri0 = rot(-t)
    dri = sc(Q(-1), dri0)
    a = ((Q(3, 5), Q(0)), (Q(0), Q(4, 5)))
    b = ((Q(4, 5), Q(0)), (Q(0), Q(3, 5)))
    br, dbr = mm(b, r), mm(b, dr)
    k = [mm(a, r), sc(Q(3, 5), mm(ri, br)), sc(Q(4, 5), br)]
    dk = [mm(a, dr), sc(Q(3, 5), add(mm(dri, br), mm(ri, dbr))), sc(Q(4, 5), dbr)]
    rp, drp = rot(t/2)
    drp = sc(Q(1, 2), drp)
    base = ((Q(2, 3), Q(1, 12)), (Q(1, 12), Q(1, 3)))
    return k, dk, push(rp, base), gate_jet(rp, drp, base)


def finite_tree(k, dk, rho, drho, cap, prewarm=0):
    nodes = {(): (rho, drho)}
    leaves = {}
    live = []

    def visit(w):
        s, ds = nodes[w]
        if len(w) >= prewarm+2 and (w[-1] == w[prewarm] or len(w) == prewarm+cap+1):
            leaves[w] = (trace(s), trace(ds))
            return
        live.append(w)
        for b, (kb, dkb) in enumerate(zip(k, dk)):
            nodes[w+(b,)] = (push(kb, s), add(gate_jet(kb, dkb, s), push(kb, ds)))
            visit(w+(b,))

    visit(())
    return nodes, leaves, live


def log_positive_2(a):
    """Decimal spectral logarithm of a positive real symmetric 2x2 block."""
    av = (a[0][0]+a[1][1])/2
    gap = ((a[0][0]-a[1][1])**2+4*a[0][1]**2).sqrt()
    hi, lo = av+gap/2, av-gap/2
    if lo <= 0:
        raise ArithmeticError('strictly positive retained conditional DATA block required')
    if not gap:
        return sc(av.ln(), eye(2, D))
    mean, slope = (hi.ln()+lo.ln())/2, (hi.ln()-lo.ln())/gap
    return add(sc(mean, eye(2, D)), sc(slope, add(a, sc(-av, eye(2, D)))))


def thermal(q, dq, cap, beta, dbeta=D(0)):
    if any(x == 0 and dx != 0 for x, dx in zip(q, dq)):
        raise ArithmeticError('entropy/KL boundary derivative needs the actual zero-amplitude tangent')
    f, df = [], []
    for x in q:
        r = 1-x
        f.append(sum((r**n/D(n) for n in range(1, cap+1)), D(0)))
        df.append(-D(1)-sum((r**n for n in range(1, cap)), D(0)))
    ew = [(-x).exp() for x in f]
    z = sum(ew)
    sig = [x/z for x in ew]
    val = (sum(x*y for x, y in zip(q, f))+z.ln())/beta
    chi = [(y+(x-s)*dy)/beta for x, s, y, dy in zip(q, sig, f, df)]
    source = sum(x*y for x, y in zip(chi, dq))-val*dbeta/beta
    avg = sum(s*dy*dx for s, dy, dx in zip(sig, df, dq))
    dsig = [s*(-dy*dx+avg) for s, dy, dx in zip(sig, df, dq)]
    entropy = -sum(x*x.ln() for x in q if x)
    dentropy = -sum(dx*x.ln() for x, dx in zip(q, dq) if x)
    kl = sum(x*(x.ln()-s.ln()) for x, s in zip(q, sig) if x)
    dkl = sum(dx*(x.ln()-s.ln())-x*ds/s for x, dx, s, ds in zip(q, dq, sig, dsig) if x)
    return dict(value=val, source=source, chi=chi, sigma=sig, f=f, df=df,
                entropy=entropy, dentropy=dentropy, kl=kl, dkl=dkl)


def rational_and_decimal_checks():
    with localcontext() as ctx:
        ctx.prec = 85
        beta = D(2)*((D(5).sqrt()-1)/2)**2
        ell = ((D(5).sqrt()+1)/2).ln()
        cases = []
        for cap in (1, 2, 3):
            k, dk, rho0, drho0 = rational_input(Q(1, 5))
            require(total(pull(x, eye(2)) for x in k) == eye(2), 'exact instrument completeness')
            require(total(add(mm(trp(dx), x), mm(trp(x), dx)) for x, dx in zip(k, dk)) == zero(2),
                    'exact differentiated completeness')
            prep = [(rho0, drho0)]
            for _ in range(2):
                r, dr = prep[-1]
                prep.append((total(push(x, r) for x in k),
                             total(add(gate_jet(x, dx, r), push(x, dr)) for x, dx in zip(k, dk))))
            nodes, leaves, live = finite_tree(k, dk, *prep[-1], cap)
            words = sorted(leaves)
            q = [dec(leaves[w][0]) for w in words]
            dq = [dec(leaves[w][1]) for w in words]
            require(sum(v[0] for v in leaves.values()) == 1 and sum(v[1] for v in leaves.values()) == 0,
                    'exact full stopped mass and source')
            out = thermal(q, dq, 7, beta, D(1)/19)
            require(abs(beta*out['value']-out['entropy']-out['kl']) < D('1e-80'),
                    'finite generated thermal value = entropy plus KL')
            require(abs(beta*out['source']+out['value']/19-out['dentropy']-out['dkl']) < D('1e-79'),
                    'whole moving-beta generated source identity')

            # True reverse adjoint of the complete stopped execution, then of
            # its two actually generated prewarm steps; input remains upstream.
            adjoints = {w: sc(c, eye(2, D)) for w, c in zip(words, out['chi'])}
            gate_source = D(0)
            for w in sorted(live, key=len, reverse=True):
                sigma = nodes[w][0]
                children = [adjoints[w+(b,)] for b in range(len(k))]
                for kb, dkb, h in zip(k, dk, children):
                    gate_source += trace(mm(h, dm(gate_jet(kb, dkb, sigma))))
                adjoints[w] = total((pull(dm(kb), h) for kb, h in zip(k, children)), kind=D)
            h = adjoints[()]
            prep_source = D(0)
            for j in range(1, -1, -1):
                dz = total(gate_jet(kb, dkb, prep[j][0]) for kb, dkb in zip(k, dk))
                prep_source += trace(mm(h, dm(dz)))
                h = total((pull(dm(kb), h) for kb in k), kind=D)
            boundary = trace(mm(h, dm(drho0)))
            reverse = gate_source+prep_source+boundary-out['value']/(19*beta)
            require(abs(reverse-out['source']) < D('1e-78'), 'complete finite-tree causal adjoint source')
            require(abs(boundary) > D('1e-8'), 'independent input reaction is not deleted')
            require(abs(prep_source) > D('1e-8'), 'generated prewarm gate price reaction is retained')

            # Literal elapsed trials and labelled stage charges, no iid reset.
            nt = sum(leaves[w][0]*len(w) for w in words)
            dnt = sum(leaves[w][1]*len(w) for w in words)
            omega = total(nodes[w][0] for w in live)
            domega = total(nodes[w][1] for w in live)
            require(trace(omega) == nt and trace(domega) == dnt, 'exact elapsed-clock occupation and source')
            charges = [Q(1), Q(2), Q(1)]
            g = total(sc(c, pull(kb, eye(2))) for c, kb in zip(charges, k))
            dg = total(sc(c, add(mm(trp(dkb), kb), mm(trp(kb), dkb)))
                       for c, kb, dkb in zip(charges, k, dk))
            costs = {w: sum(charges[b] for b in w) for w in words}
            c = sum(leaves[w][0]*costs[w] for w in words)
            dc = sum(leaves[w][1]*costs[w] for w in words)
            require(c == trace(mm(g, omega)), 'exact complete charge occupation')
            require(dc == trace(mm(dg, omega))+trace(mm(g, domega)), 'exact complete charge source')

            # Coarse first anchor versus the complete measured stopped word.
            qa = [sum(leaves[w][0] for w in words if w[0] == a) for a in range(3)]
            dqa = [sum(leaves[w][1] for w in words if w[0] == a) for a in range(3)]
            aout = thermal(list(map(dec, qa)), list(map(dec, dqa)), 7, beta, D(1)/19)
            baseline = dec(c)-(out['entropy']-aout['entropy'])/ell
            dbaseline = dec(dc)-(out['dentropy']-aout['dentropy'])/ell
            price = dec(c)-out['entropy']/ell
            dprice = dec(dc)-out['dentropy']/ell
            rebuilt = baseline-beta*aout['value']/ell+aout['kl']/ell
            drebuild = dbaseline-(beta*aout['source']+aout['value']/19)/ell+aout['dkl']/ell
            require(abs(price-rebuilt) < D('1e-79'), 'full fine-history price from generated coarse thermal graph')
            require(abs(dprice-drebuild) < D('1e-77'), 'full fine-history source with real baseline and KL reaction')
            require(abs(dbaseline) > D('1e-7'), 'fine-history baseline is source-visible')

            # Now retain both preparation labels AND conditional quantum DATA.
            # This is the complete CQ tape, not only its future-report marginal.
            all_nodes, all_leaves, all_live = finite_tree(k, dk, rho0, drho0, cap, prewarm=2)
            all_words = sorted(all_leaves)
            for w in words:
                sub = [v for v in all_words if v[2:] == w]
                if sum(all_leaves[v][0] for v in sub) != leaves[w][0]:
                    raise ArithmeticError('retained preparation gives the same future marginal')
                if sum(all_leaves[v][1] for v in sub) != leaves[w][1]:
                    raise ArithmeticError('retained preparation gives the same future source')
            require(sum(all_leaves[v][0] for v in all_words) == 1,
                    'all preparation labels and all future branches retained')
            cfull = sum(all_leaves[v][0]*sum(charges[b] for b in v) for v in all_words)
            dcfull = sum(all_leaves[v][1]*sum(charges[b] for b in v) for v in all_words)
            oprep = total(s for s, _ in prep[:-1])
            doprep = total(ds for _, ds in prep[:-1])
            require(cfull == c+trace(mm(g, oprep)), 'all preparation port charges paid exactly')
            require(dcfull == dc+trace(mm(dg, oprep))+trace(mm(g, doprep)),
                    'all preparation port-charge sources retained exactly')

            hcq, dhcq, hrecord = D(0), D(0), D(0)
            full_adjoints = {}
            for v in all_words:
                sv, dsv = map(dm, all_nodes[v])
                logs = log_positive_2(sv)
                logplus = add(logs, eye(2, D))
                hcq -= trace(mm(sv, logs))
                dhcq -= trace(mm(dsv, logplus))
                pv = dec(all_leaves[v][0])
                hrecord -= pv*pv.ln()
                full_adjoints[v] = add(sc(dec(sum(charges[b] for b in v)), eye(2, D)),
                                       sc(1/ell, logplus))
            require(hcq-hrecord > D('1e-5'), 'retained conditional quantum work has nonzero entropy')
            full_baseline = dec(cfull)-(hcq-aout['entropy'])/ell
            dfull_baseline = dec(dcfull)-(dhcq-aout['dentropy'])/ell
            full_price = dec(cfull)-hcq/ell
            dfull_price = dec(dcfull)-dhcq/ell
            rebuilt_full = full_baseline-beta*aout['value']/ell+aout['kl']/ell
            drebuilt_full = dfull_baseline-(beta*aout['source']+aout['value']/19)/ell+aout['dkl']/ell
            require(abs(full_price-rebuilt_full) < D('1e-77'),
                    'complete preparation-record-work CQ price identity')
            require(abs(dfull_price-drebuilt_full) < D('1e-76'),
                    'complete preparation-record-work CQ source identity')
            # Independently backpropagate that full CQ objective through every
            # actual preparation and stopped gate, then its moving input.
            full_gate_source = D(0)
            for v in sorted(all_live, key=len, reverse=True):
                sv = all_nodes[v][0]
                children = [full_adjoints[v+(b,)] for b in range(len(k))]
                for kb, dkb, h in zip(k, dk, children):
                    full_gate_source += trace(mm(h, dm(gate_jet(kb, dkb, sv))))
                full_adjoints[v] = total((pull(dm(kb), h) for kb, h in zip(k, children)), kind=D)
            full_input = trace(mm(full_adjoints[()], dm(drho0)))
            require(abs(full_gate_source+full_input-dfull_price) < D('1e-75'),
                    'independent full CQ adjoint with paid preparation and retained work')
            cases.append({'comparison_cap': cap, 'leaf_count': len(words),
                          'clock': str(nt), 'thermal_source': str(out['source']),
                          'input_reaction': str(boundary), 'prewarm_reaction': str(prep_source),
                          'fine_baseline_source': str(dbaseline),
                          'full_retained_preparation_leaf_count': len(all_words),
                          'complete_CQ_price': str(full_price),
                          'complete_CQ_source': str(dfull_price),
                          'complete_baseline_source': str(dfull_baseline),
                          'conditional_quantum_work_entropy': str(hcq-hrecord),
                          'complete_input_reaction': str(full_input)})

        # A symmetric genuine q-tangent is stationary although the partial
        # thermal gradient is nonzero. An independent heat tangent detects it.
        q, dq = [D(2)/5, D(2)/5, D(1)/5], [D(1), D(-1), D(0)]
        o = thermal(q, dq, 4, beta)
        residual_sq = sum((x-y)**2 for x, y in zip(q, o['sigma']))
        require(o['source'] == 0 and residual_sq > D('1e-6'), 'generated tangent vs independent-heat control')
        dark = thermal([D(1), D(0), D(0)], [D(0)]*3, 7, beta)
        harmonic = sum(D(1)/j for j in range(1, 8))
        require(dark['f'] == [D(0), harmonic, harmonic] and dark['df'] == [D(-1), D(-7), D(-7)],
                'finite polynomial includes bright and dark support endpoints')
        require(abs(beta*dark['chi'][1]-harmonic-7*dark['sigma'][1]) < D('1e-82'),
                'dark-label thermal cotangent and full finite trace retained')
        return {'status': 'PASS', 'rational_scope': 'exact probabilities, jets, clock and charge identities',
                'transcendental_scope': '85-digit Decimal checks, not interval certificates',
                'cases': cases, 'independent_heat_direction_source': str(residual_sq)}


def exact_hodge_checks():
    t = Q(1, 3)
    d = ((Q(0), Q(0), Q(0), Q(0)), (Q(0), Q(0), Q(0), Q(0)),
         (Q(1), t, Q(0), Q(0)), (Q(0), Q(2), Q(0), Q(0)))
    dd = ((Q(0),)*4, (Q(0),)*4, (Q(0), Q(1), Q(0), Q(0)), (Q(0),)*4)
    l = add(mm(d, trp(d)), mm(trp(d), d))
    dl = total((mm(dd, trp(d)), mm(d, trp(dd)), mm(trp(dd), d), mm(trp(d), dd)), 4)
    k = add(eye(4), l)  # f(L)=L+L^2, positive k=I+L
    g = tuple(tuple((Q(i == j) if i < 2 else k[i][j]) for j in range(4)) for i in range(4))
    dg = tuple(tuple((Q(0) if i < 2 else dl[i][j]) for j in range(4)) for i in range(4))
    # G0=I and G1=k1; d has only degree-zero -> degree-one entries.
    dadj = mm(trp(d), g)
    ddadj = add(mm(trp(dd), g), mm(trp(d), dg))
    lf = add(mm(d, dadj), mm(dadj, d))
    dlf = total((mm(dd, dadj), mm(d, ddadj), mm(ddadj, d), mm(dadj, dd)), 4)
    require(mm(d, d) == zero(4), 'exact genuine incidence nilpotency')
    require(lf == add(l, mm(l, l)), 'same-incidence Hodge metric realizes f(L) exactly')
    target = total((dl, mm(l, dl), mm(dl, l)), 4)
    require(dlf == target, 'full moving Hodge metric source including noncommuting jet')
    require(mm(l, dl) != mm(dl, l), 'Hodge source control is noncommuting')
    r = tuple(tuple(Q((i+1)*(j+1), 19) for j in range(4)) for i in range(4))
    cot = total((r, mm(l, r), mm(r, l)), 4)
    require(trace(mm(r, dlf)) == trace(mm(cot, dl)), 'exact Frechet cotangent pullback')
    require(trace(lf) == 2*sum(lf[i][i] for i in range(2)), 'both Hodge spectral partners retained')
    return {'status': 'EXACT_PASS', 'spectrum_function': 'f(lambda)=lambda+lambda^2',
            'trace': str(trace(lf)), 'source_pairing': str(trace(mm(r, dlf))),
            'native_incidence_admission': False}


def actual_cut_complex_checks():
    """Use the executing U and P themselves, retaining the whole ambient space."""
    import numpy as np
    from scipy.linalg import expm

    def plane(i, j, t, n=6):
        rr, drr = rot(t)
        a = [list(row) for row in eye(n)]
        da = [list(row) for row in zero(n)]
        for x, ix in enumerate((i, j)):
            for y, iy in enumerate((i, j)):
                a[ix][iy], da[ix][iy] = rr[x][y], drr[x][y]
        return tuple(map(tuple, a)), tuple(map(tuple, da))

    n, rank = 6, 2
    p = tuple(tuple(Q(i == j and i < rank) for j in range(n)) for i in range(n))
    q = add(eye(n), sc(Q(-1), p))
    a, da = plane(0, 2, Q(1, 5))
    b, _ = plane(1, 3, Q(1, 3))
    c, dc = plane(0, 1, Q(2, 7))
    u = mm(mm(a, b), c)
    du = add(mm(mm(da, b), c), sc(Q(1, 2), mm(mm(a, b), dc)))
    _, wdot = plane(0, 3, Q(0))
    dp = add(mm(wdot, p), sc(Q(-1), mm(p, wdot)))
    cut = mm(mm(q, u), p)
    dcut = total((sc(Q(-1), mm(mm(dp, u), p)), mm(mm(q, du), p), mm(mm(q, u), dp)), n)
    f = mm(trp(cut), cut)
    df = add(mm(trp(dcut), cut), mm(trp(cut), dcut))
    lc = add(f, mm(cut, trp(cut)))
    dlc = total((df, mm(dcut, trp(cut)), mm(cut, trp(dcut))), n)
    require(mm(trp(u), u) == eye(n), 'actual-cut rational full unitary')
    require(mm(cut, cut) == zero(n), 'actual cut differential QUP is exactly nilpotent')
    require(add(mm(cut, dcut), mm(dcut, cut)) == zero(n), 'moving-cut nilpotency source')
    require(mm(p, f) == f and mm(f, p) == f, 'actual feedback equals active cut-complex heat block')
    require(trace(lc) == 2*trace(f), 'actual cut-complex full paired trace identity')

    arr = lambda x: np.array(x, dtype=float)
    pn, fn, dfn, ln, dln = map(arr, (p, f, df, lc, dlc))
    beta, z = 3-np.sqrt(5.), 2.**-20
    boltz = expm(-beta*ln)
    zfull = float(np.trace(boltz))
    ef = expm(-beta*fn)
    zpaired = n-2*rank+2*np.trace(pn@ef)
    require(abs(zfull-zpaired) < 2e-14, 'literal heat trace retains all harmonic complement modes')
    sigma = boltz/zfull
    inv = np.linalg.inv(np.eye(n)-z*fn)
    raw_heat = -float(np.trace(sigma@dln))
    feedback = z*float(np.trace(inv@dfn))
    compact = float(np.trace((z*inv-2*ef/zfull)@dfn))
    require(abs(compact-raw_heat-feedback) < 2e-14, 'whole Book-type source through the actual moving cut')
    dropped = -2*float(np.trace(ef@dfn))/(zfull-(n-2*rank))+feedback
    require(abs(dropped-compact) > 1e-5, 'dropping harmonic complement changes the source')
    # oldRIGHT is an actual unchanged tensor multiplicity, not heat copies that
    # may be omitted from the absolute value.
    right = 3
    lbig, dlbig = np.kron(ln, np.eye(right)), np.kron(dln, np.eye(right))
    fbig, dfbig = np.kron(fn, np.eye(right)), np.kron(dfn, np.eye(right))
    ebig = expm(-beta*lbig)
    bigheat = -float(np.trace(ebig@dlbig))/float(np.trace(ebig))
    bigfb = z*float(np.trace(np.linalg.solve(np.eye(n*right)-z*fbig, dfbig)))
    require(abs(bigheat-raw_heat) < 2e-14 and abs(bigfb-right*feedback) < 2e-14,
            'actual oldRIGHT heat normalization and feedback multiplicity')
    require(abs(np.trace(ebig)-right*zfull) < 2e-13, 'oldRIGHT remains in absolute heat trace')
    return {'status': 'PASS', 'exact_scope': 'rational U,P and all moving-cut/operator identities',
            'trace_source_scope': 'floating finite exponentials; no interval claim',
            'ambient_dimension': n, 'active_rank': rank, 'oldRIGHT_control': right,
            'heat_trace': zfull, 'complete_source': compact,
            'heat_source': raw_heat, 'feedback_source': feedback,
            'incorrect_dropped_harmonic_source': dropped,
            'identification_with_selected_Book03_incidence': False}


def native_checks():
    import numpy as np
    import scipy
    from scipy.linalg import expm, solve_sylvester
    from scipy.special import logsumexp

    source = Path(__file__).resolve().parents[1]/'d0_book_uniform_source_2026-10-21'/'check_uniform_book_source.py'
    raw = source.read_bytes()
    blob = hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    require(blob == 'ee8de4635d24c668949ac9a0186616ab7d59f2ed', 'unchanged original native constructor blob')
    wanted = {'adj', 'herm', 'root', 'creators', 'native'}
    nodes = [n for n in ast.parse(raw).body if
             (isinstance(n, ast.FunctionDef) and n.name in wanted) or
             (isinstance(n, ast.Assign) and any(isinstance(v, ast.Name) and v.id in {'P', 'EYE'} for v in n.targets))]
    require(len(nodes) == 7, 'only pinned constructor definitions selected')
    env = {'np': np, 'expm': expm, 'solve_sylvester': solve_sylvester}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(source), 'exec'), env)
    native, creators, p = env['native'], env['creators'], env['P']
    n, eps, beta = 16, 4*p*p, 2*p*p
    ident = np.eye(n, dtype=complex)
    costs = 1+np.arange(128) % 2

    def adj(x):
        return x.conj().swapaxes(-1, -2)

    def rt(x):
        y = np.trace(x)
        if abs(y.imag) > 1e-10:
            raise ArithmeticError('non-real native pairing')
        return float(y.real)

    def forward(k, x):
        return np.sum(k@x@adj(k), axis=0)

    def backward(k, x):
        return np.sum(adj(k)@x@k, axis=0)

    def dforward(k, dk, x):
        return np.sum(dk@x@adj(k)+k@x@adj(dk), axis=0)

    def evaluate(theta, details=False):
        k, dk = native(theta)
        e, de = adj(k)@k, adj(dk)@k+adj(k)@dk
        delta = (2/eps)*(ident-k[0])
        ddelta = (-2/eps)*dk[0]
        g = np.sum(costs[:, None, None]*e, axis=0)
        dg = np.sum(costs[:, None, None]*de, axis=0)
        prep = [(ident/n, np.zeros_like(ident))]
        for _ in range(2):
            r, dr = prep[-1]
            prep.append((forward(k, r), dforward(k, dk, r)+forward(k, dr)))
        r, dr = prep[-1]
        sig1 = k@r@adj(k)
        dsig1 = dk@r@adj(k)+k@dr@adj(k)+k@r@adj(dk)
        q = np.einsum('bij,aji->ab', e, sig1).real
        dq = (np.einsum('bij,aji->ab', de, sig1)+np.einsum('bij,aji->ab', e, dsig1)).real
        f = sum((1-q)**j/j for j in range(1, 8))
        df = -sum((1-q)**j for j in range(7))
        logz = logsumexp(-f)
        thermal_sigma = np.exp(-f-logz)
        tv = float((np.sum(q*f)+logz)/beta)
        chi = (f+(q-thermal_sigma)*df)/beta
        tsrc = float(np.sum(chi*dq))
        cpair = costs[:, None]+costs[None, :]
        cp = sum(rt(x@g) for x, _ in prep[:-1])
        dcp = sum(rt(dx@g+x@dg) for x, dx in prep[:-1])
        cv = cp+float(np.sum(q*cpair))
        csrc = dcp+float(np.sum(dq*cpair))
        # The EXISTING one-round blank cut, not the Golden archive splitter.
        # Its unused 127 output labels remain in the full heat carrier.
        blank, dblank = k[0], dk[0]
        fb = ident-adj(blank)@blank
        dfb = -adj(dblank)@blank-adj(blank)@dblank
        mbase, oldright, zeta = 128*n, 128, 2.**-20
        efb = expm(-beta*fb)
        zcut = mbase-2*n+2*rt(efb)
        fb_source = oldright*zeta*rt(np.linalg.solve(ident-zeta*fb, dfb))
        cut_source = -2*rt(efb@dfb)/zcut+fb_source
        je = -oldright*float(np.linalg.slogdet(ident-zeta*fb)[1])
        cut_value = float(np.log(oldright*zcut)/beta+je)
        evf, uf = np.linalg.eigh(fb)
        sqrt_blank = (uf*np.sqrt(1-evf))@adj(uf)
        recovered = (2/eps)*(ident-sqrt_blank)
        drecovered = -(2/eps)*solve_sylvester(sqrt_blank, sqrt_blank, -dfb)
        enat = expm(-beta*delta)
        znat = mbase-2*n+2*rt(enat)
        recovered_source = -2*rt(enat@ddelta)/znat+fb_source
        recovered_value = float(np.log(oldright*znat)/beta+je)
        if not details:
            return tv, cv, cut_value, recovered_value
        require(np.linalg.norm(g-ident-p*eps*delta) < 2e-13, 'original 128-outcome native port effect')
        require(np.linalg.norm(dg-p*eps*ddelta) < 2e-13, 'original native port-effect derivative')
        require(abs(q.sum()-1) < 2e-13 and abs(dq.sum()) < 2e-13, 'complete native 128^2 probability and source')
        require(q.min() > -1e-15, 'full native finite probability carrier retained')
        require(np.linalg.eigvalsh(blank).min() > 0, 'actual original positive blank branch')
        require(np.linalg.norm(fb-(eps*delta-eps**2/4*delta@delta)) < 2e-13,
                'original blank feedback is the forced polynomial of native heat')
        require(np.linalg.norm(dfb-(eps*ddelta-eps**2/4*(ddelta@delta+delta@ddelta))) < 2e-13,
                'original blank coupled feedback source')
        require(np.linalg.norm(recovered-delta) < 2e-13 and np.linalg.norm(drecovered-ddelta) < 2e-13,
                'canonical same-cut inverse heat and noncommuting source')
        require(abs(cut_source) > 1e-9 and abs(recovered_source) > 1e-9,
                'original native cut candidates retain a real boost source')
        # Reverse report source, then reverse both paid preparation stages.
        h1 = np.einsum('ab,bij->aij', chi, e)
        heat1 = rt(np.sum(adj(k)@h1@k, axis=0)@dr)
        report_gate = float(np.einsum('ab,bij,aji->', chi, de, sig1).real)
        report_gate += float(np.einsum('aij,aji->', h1, dk@r@adj(k)+k@r@adj(dk)).real)
        h = np.sum(adj(k)@h1@k, axis=0)
        prewarm_source = 0.0
        for j in range(1, -1, -1):
            prewarm_source += rt(h@dforward(k, dk, prep[j][0]))
            h = backward(k, h)
        require(abs(tsrc-report_gate-prewarm_source) < 2e-12, 'native complete generated thermal adjoint')
        require(abs(prewarm_source-heat1) < 2e-12, 'native generated preparation chain-rule identity')
        require(abs(prewarm_source) > 1e-10, 'native prewarm source cannot be frozen')
        # All four actual port-costed rounds, retaining finite prewarm.
        omega = prep[0][0]+prep[1][0]+r+forward(k, r)
        domega = prep[0][1]+prep[1][1]+dr+dforward(k, dk, r)+forward(k, dr)
        cocc = rt(omega)+p*eps*rt(delta@omega)
        dcocc = rt(domega)+p*eps*rt(ddelta@omega+delta@domega)
        require(abs(cv-cocc) < 2e-12 and abs(csrc-dcocc) < 2e-12,
                'same finite native tape supplies actual occupation energy and full source')
        # Consume the owned stationary preparation, including its moving source.
        inv = np.linalg.inv(delta)
        z = rt(inv)
        dinv = -inv@ddelta@inv
        rho = inv/z
        drho = dinv/z-inv*rt(dinv)/z**2
        ev, u = np.linalg.eigh(delta)
        sg = (u*np.exp(-beta*ev-logsumexp(-beta*ev)))@adj(u)
        exact_cov = n*(inv@inv)/z**2-sg
        pulled = rt(exact_cov@ddelta)
        full = rt(drho@delta+(rho-sg)@ddelta)
        frozen = rt((rho-sg)@ddelta)
        require(abs(pulled-full) < 2e-13, 'generated inverse-square native thermal cotangent')
        require(abs(full-frozen) > 1e-9, 'fixed-rho partial gradient is not the native full source')
        return {'theta': theta, 'prewarm_rounds': 2, 'report_rounds': 2,
                'full_retained_report_labels': 128**2, 'thermal_polynomial_cap': 7,
                'thermal_value': tv, 'thermal_source': tsrc, 'prewarm_source': prewarm_source,
                'actual_port_cost': cv, 'actual_port_source': csrc,
                'inverse_square_full_source': full, 'frozen_preparation_source': frozen,
                'partial_thermal_gradient_norm': float(np.linalg.norm(q-thermal_sigma)),
                'original_blank_cut': {
                    'base_full_dimension': mbase, 'base_active_rank': n, 'oldRIGHT': oldright,
                    'retained_harmonic_complement': mbase-2*n,
                    'paired_heat_trace_without_oldRIGHT': zcut,
                    'cut_complex_source': cut_source,
                    'canonical_recovered_heat_source': recovered_source,
                    'feedback_source': fb_source,
                    'actual_native_coupling': 'F=epsilon Delta-epsilon^2 Delta^2/4; g(F)=2/epsilon (I-sqrt(I-F))',
                    'selected_Book03_incidence': False}}

    result = evaluate(.08, True)
    step = 1e-4
    values = [evaluate(.08+j*step) for j in (-2, -1, 1, 2)]
    errors = []
    sources = [result['thermal_source'], result['actual_port_source'],
               result['original_blank_cut']['cut_complex_source'],
               result['original_blank_cut']['canonical_recovered_heat_source']]
    for i, source_value in enumerate(sources):
        fd = (values[0][i]-8*values[1][i]+8*values[2][i]-values[3][i])/(12*step)
        errors.append(abs(fd-source_value))
    require(max(errors) < 2e-8, 'native full-source five-point independent control')
    result['five_point_errors'] = errors

    # Two bounded original type controls, without a new spectral census.
    cs = creators()
    theta, nu = .08, .6
    c0, c1, c2, c3 = cs
    n0, n1 = c0@adj(c0), c1@adj(c1)
    dp = nu/16*((1j-1)*(c0+c1)-2*c2+(-1j-1)*c3
                +1j*(np.cosh(theta)-1)*n0@c1-1j*np.sinh(theta)*n1@c0)
    defect = nu**2/256*(1+1j)*np.expm1(theta)*c0@c1
    require(np.linalg.norm(dp@dp-defect) < 1e-14, 'actual original CAR raising differential square')
    k, _ = native(theta)
    require(np.linalg.norm((dp+adj(dp))@(dp+adj(dp))-(2/eps)*(ident-k[0])) < 2e-13,
            'CAR degree defect belongs to the unchanged native blank heat')
    k0, _ = native(0.)
    x = 1j*(c2-adj(c2))
    qx = backward(k0, x)-adj(k0[0])@x@k0[0]
    ee = 9*p*p/160
    lam = -(17*ee/25+ee*ee/4)
    require(np.linalg.norm(qx-lam*x) < 2e-13 and lam < 0,
            'native CP survival is not a positive Hilbert-space heat contraction')
    result['native_survival_superoperator_eigenvalue'] = lam
    result['constructor_blob'] = blob
    result['numpy'] = np.__version__
    result['scipy'] = scipy.__version__
    result['scope'] = 'one original Fourier/role-1-boost consumer; no spatial all42, interval or physical-admission claim'
    return result


def main():
    result = {'rational_decimal': rational_and_decimal_checks(),
              'hodge': exact_hodge_checks(), 'actual_cut_complex': actual_cut_complex_checks(),
              'native': native_checks(),
              'GR_closed': False, 'old_suites_replayed': False,
              'physical_Book03_identification': False}
    result['status'] = 'PASS'
    result['checks'] = len(CHECKS)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
