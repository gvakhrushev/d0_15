#!/usr/bin/env python3
"""New narrow entropy-adjoint/source control on the literal original 8D query.

The prefix refinement/costs are a diagnostic, not the enormous native retry
transcript. The real alpha/beta and original two-query/coin/OR maps are used.
Quantum work basis labels are kept coherently, never charged as Shannon data.
No repository writes by default; no historical checker or root census runs.
"""
import argparse
import hashlib
import json
from pathlib import Path
import time
import mpmath as mp


mp.mp.dps = 80
p = (mp.sqrt(5)-1)/2
z = mp.mpf(2)**-20
logphi = mp.log(1/p)
alpha = (1-(1-2*p**3)**9)**128
beta = ((1-p**120)**4*(1-(1-16*p**9)**20))**43
checks = []


def require(label, test):
    if not bool(test):
        raise RuntimeError(label)
    checks.append(label)


def mul(a, b):
    return [[mp.fsum(a[i][k]*b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def kron(a, b):
    return [[a[i][j]*b[k][l] for j in range(len(a[0])) for l in range(len(b[0]))]
            for i in range(len(a)) for k in range(len(b))]


def unitary(x, y):
    # The actual 4-tail x 2-scene definition of the owned native 8D block.
    e = p*p*(1+x)
    st, ct = mp.sqrt(e), mp.sqrt(1-e)
    ss = p+p*p*y
    cs = mp.sqrt(1-ss*ss)
    tail = [[ct, 0, -st, 0], [0, ct, 0, -st],
            [0, st, 0, ct], [st, 0, ct, 0]]
    scene = [[cs, -ss], [ss, cs]]
    step = kron(tail, scene)
    return mul(step, step)


def native_output(x, y, prep_shift=mp.mpf(0), prep_direction=None):
    u = unitary(x, y)
    plus = [mp.mpf(0)]*8
    minus = [mp.mpf(0)]*8
    plus[0] = plus[2] = 1/mp.sqrt(2)
    minus[0], minus[2] = 1/mp.sqrt(2), -1/mp.sqrt(2)
    if prep_direction is not None:
        plus = [a+prep_shift*b for a, b in zip(plus, prep_direction)]
        norm = mp.sqrt(mp.fsum(a*a for a in plus))
        plus = [a/norm for a in plus]
    outputs = []
    raw_outputs = []
    for psi in [plus, minus]:
        raw = [mp.fsum(row[k]*psi[k] for k in range(8)) for row in u]
        raw_outputs.append(raw)
        # The two-dimensional invariant span of the actual known efficiency
        # register: |all enabled> and the normalized coherent other component.
        # Orthogonal unused modes have zero amplitude, not discarded records.
        out = {}
        for pos in range(8):
            for coin in [0, 1]:
                flag = int(coin == 1 and pos not in [0, 2])
                out[pos, coin, flag] = raw[pos]*mp.sqrt(z if coin else 1-z)
        outputs.append(out)
    v = {a+b: va*vb for a, va in outputs[0].items() for b, vb in outputs[1].items()}
    parts = [{k: a for k, a in v.items() if int(bool(k[2] or k[5])) == report}
             for report in [0, 1]]
    return v, parts, raw_outputs[0]


def norm2(vector):
    return mp.fsum(a*a for a in vector.values())


def entropy(probs):
    return -mp.fsum(q*mp.log(q)/logphi for q in probs if q)


# A finite field-independent refinement tests the universal chain/adjoint.
# These four costs are explicitly not claimed to be the original mu or H_T.
transcripts = [(beta/3, 53, True), (2*beta/3, 71, True),
               ((1-beta)/4, 13, False), (3*(1-beta)/4, 29, False)]


def leaves(x, y, prep_shift=mp.mpf(0), prep_direction=None):
    v, parts, abort_state = native_output(x, y, prep_shift, prep_direction)
    terminal = [('bank_abort', {0: mp.sqrt(1-alpha)}, mp.mpf(11))]
    for j, (mass, cost, ready) in enumerate(transcripts):
        scale = mp.sqrt(alpha*mass)
        if ready:
            for report in [0, 1]:
                terminal.append(((j, report), {k: scale*a for k, a in parts[report].items()}, mp.mpf(19+cost)))
        else:
            terminal.append(((j, 'abort'), {k: scale*a for k, a in enumerate(abort_state)}, mp.mpf(19+cost)))
    return v, parts, terminal


def value(terminal):
    probs = [norm2(vec) for _, vec, _ in terminal]
    return mp.fsum(q*c for q, (_, _, c) in zip(probs, terminal))-entropy(probs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    start = time.perf_counter()
    v, parts, base = leaves(0, 0)
    r = norm2(parts[1])
    l = 4*p**3
    q0, r0 = 1-z*l, 1-z*l*(1+p**6)
    d0 = q0*r0
    require('complete original query/efficiency/OR norm', abs(norm2(v)-1) < mp.mpf('1e-70'))
    require('literal two-band determinant at primary', abs(r-(1-d0)) < mp.mpf('1e-70'))
    require('all complete prefix/abort/report probability', abs(mp.fsum(norm2(a) for _, a, _ in base)-1) < mp.mpf('1e-70'))
    cpre = 11*(1-alpha)+19*alpha
    mu = mp.fsum(t*c for t, c, _ in transcripts)
    ht = entropy([t for t, _, _ in transcripts])
    closed = cpre-entropy([alpha, 1-alpha])+alpha*(mu-ht-beta*entropy([r, 1-r]))
    require('complete finite leaf price equals retained ledger', abs(value(base)-closed) < mp.mpf('1e-65'))
    dx, dy = mp.mpf(3)/7, -mp.mpf(1)/5
    delta = mp.mpf('1e-20')
    vp, _, plus = leaves(delta*dx, delta*dy)
    vm, _, minus = leaves(-delta*dx, -delta*dy)
    by_label_plus = {label: vec for label, vec, _ in plus}
    by_label_minus = {label: vec for label, vec, _ in minus}
    adjoint = mp.mpf(0)
    root = {k: mp.mpf(0) for k in v}
    for label, vec, cost in base:
        probability = norm2(vec)
        factor = cost+(mp.log(probability)+1)/logphi
        derivative = {k: (by_label_plus[label][k]-by_label_minus[label][k])/(2*delta) for k in vec}
        adjoint += 2*mp.fsum(factor*a*derivative[k] for k, a in vec.items())
        if isinstance(label, tuple) and label[1] in [0, 1]:
            mass = transcripts[label[0]][0]
            for k, a in vec.items():
                root[k] += mp.sqrt(alpha*mass)*factor*a
    query_adjoint = 2*mp.fsum(root[k]*(vp[k]-vm[k])/(2*delta) for k in v)
    finite = (value(plus)-value(minus))/(2*delta)
    rx = 4*z*q0*p**11
    ry = 8*z*p**6*(r0+q0*p**6)
    rprime = rx*dx+ry*dy
    hp = mp.log((1-r)/r)/logphi
    gamma = -alpha*beta*d0*hp
    expected = gamma*rprime/d0
    for label, result in [('full entropy terminal gradient', adjoint),
                          ('backward projection/query adjoint', query_adjoint),
                          ('direct full price finite difference', finite)]:
        require(label, abs(result-expected) < mp.mpf('1e-33'))
    # Exact full8D preparation boundary, at the SAME held query and price.
    u = unitary(0, 0)
    projector = [[mp.fsum(u[k][i]*u[k][j] for k in range(8) if k not in [0, 2])
                  for j in range(8)] for i in range(8)]
    psi = [1/mp.sqrt(2) if k in [0, 2] else mp.mpf(0) for k in range(8)]
    a = l*(1+p**6)
    direction = [mp.fsum(projector[i][j]*psi[j] for j in range(8))-a*psi[i] for i in range(8)]
    require('full query preparation leakage norm', abs(mp.fsum(t*t for t in direction)-a*(1-a)) < mp.mpf('1e-70'))
    require('generated retained input has no false free tangent', abs(direction[0])+abs(direction[2]) < mp.mpf('1e-70'))
    _, _, prep_plus = leaves(0, 0, delta, direction)
    _, _, prep_minus = leaves(0, 0, -delta, direction)
    prep_source = (value(prep_plus)-value(prep_minus))/(2*delta)
    prep_expected = -2*alpha*beta*z*q0*hp*a*(1-a)
    require('independent full8D prep source is nonzero if admitted', prep_expected < 0 and abs(prep_source-prep_expected) < mp.mpf('1e-33'))
    result = {'status': 'PASS_N1_COMPLETE_ENTROPY_ADJOINT', 'checks': checks,
              'precision_digits': mp.mp.dps, 'complete_classical_terminal_labels': len(base),
              'coherent_query_work_components': len(v), 'full_price': mp.nstr(value(base), 35),
              'gamma1': mp.nstr(gamma, 35), 'source': mp.nstr(expected, 35),
              'max_source_discrepancy': mp.nstr(max(abs(t-expected) for t in [adjoint, query_adjoint, finite]), 15),
              'conditional_independent_preparation_source': mp.nstr(prep_source, 35),
              'scope': 'New source/adjoint control with literal native8D queries and actual alpha/beta; finite prefix refinement/costs are diagnostic, not historical native retry receipts; no native admission or Book03 selection.',
              'elapsed_seconds': time.perf_counter()-start,
              'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    payload = json.dumps(result, indent=2)+'\n'
    if args.output:
        args.output.write_text(payload)
    print(payload, end='')


if __name__ == '__main__':
    main()
