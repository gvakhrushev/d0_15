#!/usr/bin/env python3
"""Literal quadratic/cubic gates at three physical resonance-circle carriers.

All coefficients are independently reconstructed from shared plaquette
links over Q/Q(i). Analytic local isolation is proved in the accompanying
memo; this finite certificate supplies its normal charts and nonzero gates.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import argparse
import json
import numpy as np
import a4d_identity_quarter_nonlinear_response_check as N
import a4d_identity_physical_resonance_circles_check as P
from a4d_warped_quarter_regular_response_check import qi_inverse, independent_rows
I, G = N.I, N.G

def euler(logs, increments):
    d = logs.shape[2]-1
    links = np.array([[N.jexp(logs[p,r]) for r in range(4)] for p in range(4)])
    return euler_links(links, increments)

def euler_links(links, increments):
    d = links.shape[2]-1
    ek = np.zeros((d+1,4,4,6),dtype=object)
    eq = np.zeros((d+1,4,10),dtype=object)
    for p in range(4):
        for face,(r,s) in enumerate(N.PAIRS):
            loc = [(p,r,False),((p+increments[r])%4,s,False),
                   ((p+increments[s])%4,r,True),(p,s,True)]
            fac = [N.jinv(links[x,y]) if inv else links[x,y] for x,y,inv in loc]
            prefix = [N.jconst(I,d)]
            for f in fac: prefix.append(N.jmul(prefix[-1],f))
            suffix = [None]*5; suffix[4]=N.jconst(I,d)
            for i in range(3,-1,-1): suffix[i]=N.jmul(fac[i],suffix[i+1])
            prod = prefix[4]
            for m in range(10):
                for n in range(d+1): eq[n,p,m]+=np.sum(N.DWEIGHT[face][m]*prod[n])
            for i,(x,y,inv) in enumerate(loc):
                co=N.jmul(suffix[i+1],N.WEIGHT[face].T@prefix[i])
                jet=-N.jmul(fac[i],co) if inv else N.jmul(co,fac[i])
                for n in range(d+1):
                    for g in range(6): ek[n,x,y,g]+=np.sum(jet[n].T*G[g])
    return ek.reshape(d+1,4,24),eq


class Sector:
    def __init__(self, first_phase, increments):
        self.first_phase = P.QI.of(first_phase)
        self.increments = increments
        self.point = [self.first_phase]*2+[P.Q]*2
        constant, linear, self.coordinate = P.circle_kernel(1)
        self.vector = (constant+linear*self.first_phase)/constant[self.coordinate]
        self.joint = P.joint(self.point)
        assert not np.any(self.joint@self.vector)
        self.columns = [j for j in range(24) if j != self.coordinate]
        self.rows = independent_rows(self.joint[:, self.columns])
        assert len(self.rows) == 23
        self.rest = [r for r in range(34) if r not in self.rows]
        self.inverse = qi_inverse(self.joint[np.ix_(self.rows, self.columns)])
        a0, c0 = N.flat_symbols([1]*4)
        a2, c2 = N.flat_symbols([x*x for x in self.point])
        self.h0inv = N.inverse(N.real_matrix(a0).T)
        self.h2inv = N.inverse(N.real_matrix(a2).T)
        self.c2 = N.real_matrix(c2)
        assert not any(x for row in c0 for x in row)

    def logs(self, a, b, degree=2, correction=None):
        logs = np.zeros((4, 4, degree+1, 4, 4), dtype=object)
        amplitude = P.QI(F(a, 2), F(-b, 2))
        phase = P.QI.of(1)
        for p in range(4):
            for r in range(4):
                logs[p, r, 1] = sum((G[j]*(2*(self.vector[6*r+j]*amplitude*phase).re)
                                      for j in range(6)), np.zeros((4, 4), dtype=object))
                if correction is not None:
                    logs[p, r, 2] = sum((G[j]*correction[p, 6*r+j] for j in range(6)),
                                        np.zeros((4, 4), dtype=object))
            phase *= P.Q
        return logs

    def quadratic(self, a, b):
        ek, eq = euler(self.logs(a, b), self.increments)
        assert not np.any(ek[:2]) and not np.any(eq[:2])
        fk, fq = ek[2], eq[2]
        assert not np.any(fk[0]-fk[2]) and not np.any(fk[1]-fk[3])
        k0 = sum(fk)*F(1, 4)
        k2 = (fk[0]-fk[1]+fk[2]-fk[3])*F(1, 4)
        w0, w2 = -self.h0inv@k0, -self.h2inv@k2
        w = np.array([w0+(-1)**p*w2 for p in range(4)])
        q0 = sum(fq)*F(1, 4)
        q2 = (fq[0]-fq[1]+fq[2]-fq[3])*F(1, 4)+self.c2@w2
        assert not np.any(q0)
        check_k, check_q = euler(self.logs(a, b, correction=w), self.increments)
        assert not np.any(check_k[:3])
        assert np.array_equal(check_q[2], np.array([q0+(-1)**p*q2 for p in range(4)]))
        return w, q2

    def cubic(self, a, b, correction):
        ek, eq = euler(self.logs(a, b, 3, correction), self.increments)
        assert not np.any(ek[:3])
        source = np.concatenate([ek[3], eq[3]], axis=1)
        assert not np.any(source[0]+source[2]) and not np.any(source[1]+source[3])
        fourier = np.array([P.QI(F(source[0, j]-source[2, j], 4),
                                F(source[3, j]-source[1, j], 4)) for j in range(34)], dtype=object)
        return (fourier-self.joint[:, self.columns]@self.inverse@fourier[self.rows])[self.rest]

    def check_literal_linear(self):
        # Independent readout checks every role/generator and both real
        # parts of the quarter mode, including all incident face bases.
        for j in range(24):
            for quadrature in (P.QI.of(1), P.Q):
                logs = np.zeros((4, 4, 2, 4, 4), dtype=object)
                phase = quadrature
                for p in range(4):
                    logs[p, j//6, 1] = G[j % 6]*phase.re
                    phase *= P.Q
                ek, eq = euler(logs, self.increments)
                phase = quadrature
                for p in range(4):
                    actual = np.concatenate([ek[1, p], eq[1, p]])
                    expected = np.array([(x*phase).re for x in self.joint[:, j]], dtype=object)
                    assert np.array_equal(actual, expected)
                    phase *= P.Q


def run_checks():
    results = []
    for first, shifts in ((1, (0, 0, 1, 1)), (-1, (2, 2, 1, 1)),
                           (-P.Q, (3, 3, 1, 1))):
        sector = Sector(first, shifts)
        sector.check_literal_linear()
        print('PASS_LITERAL_LINEAR_ALL48_INPUTS_'+str(shifts), flush=True)
        values = [sector.quadratic(a, b) for a, b in ((1, 0), (0, 1), (1, 1))]
        coefficients = [values[0], values[1],
                        (values[2][0]-values[0][0]-values[1][0],
                         values[2][1]-values[0][1]-values[1][1])]
        w, q2 = sector.quadratic(2, -3)
        assert np.array_equal(w, 4*coefficients[0][0]+9*coefficients[1][0]-6*coefficients[2][0])
        assert np.array_equal(q2, 4*coefficients[0][1]+9*coefficients[1][1]-6*coefficients[2][1])
        if sector.first_phase in (P.QI.of(1), P.QI.of(-1)):
            factor = 1 if sector.first_phase == P.QI.of(1) else 3
            expected = np.zeros((3, 10), dtype=object)
            expected[0, [0, 1, 4]] = [F(factor, 2), -factor, F(factor, 2)]
            expected[1] = -expected[0]
            expected[2, [0, 4]] = [1, -1]
            assert np.array_equal(np.array([x[1] for x in coefficients]), expected)
            # Complete coefficient identity: 2(q00^2+q04^2)
            # = (a^2+b^2)^2+(factor^2-1)(a^2-b^2)^2.
            rows = [expected[:, j] for j in (0, 4)]
            polynomial = {}
            exponents = [(2, 0), (0, 2), (1, 1)]
            for row in rows:
                for i, x in enumerate(row):
                    for j, y in enumerate(row):
                        key = tuple(a+b for a, b in zip(exponents[i], exponents[j]))
                        polynomial[key] = polynomial.get(key, F(0))+2*x*y
            assert polynomial == {(4, 0): factor*factor, (0, 4): factor*factor,
                                  (2, 2): 4-2*factor*factor, (3, 1): 0, (1, 3): 0}
            cubic_data = None
            bound = '||Q2(a,b)||_infinity >= (a^2+b^2)/2'
        else:
            expected = np.zeros((3, 10), dtype=object)
            expected[2] = [0, 2, -1, -1, -2, 1, 1, 0, 0, 0]
            assert np.array_equal(np.array([x[1] for x in coefficients]), expected)
            cubic_a = sector.cubic(1, 0, coefficients[0][0])
            cubic_b = sector.cubic(0, 1, coefficients[1][0])
            assert cubic_a[0] == P.QI(F(-1, 8), F(1, 8))
            assert cubic_b[0] == P.QI(F(1, 8), F(1, 8))
            plus = sector.cubic(1, 1, values[2][0])-cubic_a-cubic_b
            wm, _ = sector.quadratic(1, -1)
            minus = sector.cubic(1, -1, wm)-cubic_a+cubic_b
            mixed_a = (plus-minus)/2
            mixed_b = (plus+minus)/2
            held = sector.cubic(2, -3, w)
            assert np.array_equal(held, 8*cubic_a-27*cubic_b-12*mixed_a+18*mixed_b)
            cubic_data = {'monomials': ['a^3', 'b^3', 'a^2*b', 'a*b^2'],
                          'coefficients': [P.exact_strings(v) for v in (cubic_a, cubic_b, mixed_a, mixed_b)],
                          'quadratic_zero_cone': 'a*b=0',
                          'first_reduced_row_on_axes': ['(-1+i)*a^3/8', '(1+i)*b^3/8'],
                          'common_quadratic_cubic_real_zero': 'only a=b=0'}
            bound = 'quadratic ab gate and nonzero cubic residual on both axes'
        results.append({'point': P.exact_strings(sector.point), 'increments_mod4': list(shifts),
                        'complex_kernel': P.exact_strings(sector.vector),
                        'joint_rank': 23, 'real_period4_center_dimension': 2,
                        'range_rows': sector.rows, 'complement_columns': sector.columns,
                        'reduced_rows': sector.rest,
                        'quadratic_monomials': ['a^2', 'b^2', 'a*b'],
                        'even_connection_corrections': [N.exact_strings(x[0]) for x in coefficients],
                        'alternating_metric_quadratic': [N.exact_strings(x[1]) for x in coefficients],
                        'common_metric_quadratic': 'identically zero', 'gate': bound,
                        'cubic_reduction': cubic_data})
        print('PASS_COMPLETE_NONLINEAR_GATE_'+str(shifts), flush=True)
    return {'schema': 'a4d-identity-resonance-circle-nonlinear-gates-v1',
            'input_head': 'de71bf30e9cfd34614fc8178255d456c49ebb8b1',
            'arithmetic': 'exact Q/Q(i) literal shared-link jets; no coefficient oracle',
            'sectors': results,
            'analytic_consequence': 'in each fixed period4 invariant sector, I is the only sufficiently small exact field with EK=0 and all nonconstant-phase EQ=0',
            'nonclaims': ['does not control arbitrary longitudinal envelopes along a continuous circle',
                          'does not construct a full4D curved designated continuation',
                          'does not prove unrestricted response universality'],
            'verdict': 'THREE_CIRCLE_CARRIER_NONLINEAR_GATES_CERTIFIED; TASK_TERMINAL_OPEN'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--expect', type=Path)
    args = parser.parse_args()
    report = run_checks()
    expected = args.expect or (Path(__file__).with_name('a4d_identity_resonance_circle_nonlinear_gates_results.json') if args.output is None else None)
    if expected:
        assert json.loads(expected.read_text()) == report
        print('PASS_PINNED_LEDGER', flush=True)
    if args.output:
        args.output.write_text(json.dumps(report, indent=2)+'\n')
    print('VERDICT', report['verdict'])
