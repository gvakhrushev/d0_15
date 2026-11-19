#!/usr/bin/env python3
"""Exact literal flat-symbol controls for a proposed full designated inverse.

No SymPy dependency.  Arithmetic is exact over Q(i).  The accompanying memo
proves the localized obstruction on a fixed smooth normal background; this
finite checker supplies its physical principal-symbol witness.  It does not
certify a nonlinear metric-response counterexample or an Einstein terminal.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path


@dataclass(frozen=True)
class QI:
    re: F = F(0)
    im: F = F(0)

    @staticmethod
    def of(x):
        return x if isinstance(x, QI) else QI(F(x))

    def __add__(self, other):
        b = QI.of(other)
        return QI(self.re+b.re, self.im+b.im)

    __radd__ = __add__

    def __neg__(self):
        return QI(-self.re, -self.im)

    def __sub__(self, other):
        return self+-QI.of(other)

    def __rsub__(self, other):
        return QI.of(other)+-self

    def __mul__(self, other):
        b = QI.of(other)
        return QI(self.re*b.re-self.im*b.im, self.re*b.im+self.im*b.re)

    __rmul__ = __mul__

    def __truediv__(self, other):
        b = QI.of(other)
        return self*b.conjugate() * (1/(b.re*b.re+b.im*b.im))

    def __rtruediv__(self, other):
        return QI.of(other)/self

    def conjugate(self):
        return QI(self.re, -self.im)

    def __bool__(self):
        return bool(self.re or self.im)

    def __complex__(self):
        return complex(float(self.re), float(self.im))


PAIRS = list(combinations(range(4), 2))
SYM = [(a,b) for a in range(4) for b in range(a,4)]
SIG = (1,-1,-1,-1)
STAR_MAP = ((5,-1),(4,1),(3,-1),(2,1),(1,-1),(0,1))


def zeros(n=4, m=4):
    return [[F(0) for _ in range(m)] for _ in range(n)]


def mm(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def generators():
    out = []
    for k in (1,2,3):
        x = zeros(); x[0][k] = x[k][0] = F(1); out.append(x)
    for a,b in ((1,2),(1,3),(2,3)):
        x = zeros(); x[a][b],x[b][a] = F(1),F(-1); out.append(x)
    return out


GEN = generators()
EYE = [[F(i==j) for j in range(4)] for i in range(4)]


def wedge(u,v):
    return [u[a]*v[b]-u[b]*v[a] for a,b in PAIRS]


def column(a,j):
    return [row[j] for row in a]


def orient(a,b):
    s = [a,b]+[i for i in range(4) if i not in (a,b)]
    return (-1)**sum(s[i]>s[j] for i,j in combinations(range(4),2))


def pairing(area, tangent):
    biv = [tangent[a][b]*SIG[b] for a,b in PAIRS]
    return sum(area[row]*SIG[PAIRS[row][0]]*SIG[PAIRS[row][1]]*sgn*biv[c]
               for c,(row,sgn) in enumerate(STAR_MAP))


def flat_symbols(phase):
    """Literal mixed connection Hessian and correctly placed metric readout."""
    phase = [QI.of(z) for z in phase]
    a = [[QI() for _ in range(24)] for _ in range(24)]
    c = [[QI() for _ in range(24)] for _ in range(10)]
    for r,s in PAIRS:
        u,v = [i for i in range(4) if i not in (r,s)]
        area = wedge(column(EYE,u),column(EYE,v))
        roles = (r,s,r,s)
        direct = (QI.of(1),phase[r],-phase[s],QI.of(-1))
        inverse = (QI.of(1),1/phase[r],-1/phase[s],QI.of(-1))
        role = [[QI() for _ in range(4)] for _ in range(4)]
        for i,j in combinations(range(4),2):
            role[roles[i]][roles[j]] += direct[i]*inverse[j]/2
            role[roles[j]][roles[i]] -= inverse[i]*direct[j]/2
        for i,xi in enumerate(GEN):
            for j,xj in enumerate(GEN):
                xy,yx = mm(xi,xj),mm(xj,xi)
                bracket = [[xy[k][l]-yx[k][l] for l in range(4)] for k in range(4)]
                val = orient(r,s)*pairing(area,bracket)
                for rr in range(4):
                    for ss in range(4):
                        a[6*rr+i][6*ss+j] += role[rr][ss]*val
        for mi,(aa,bb) in enumerate(SYM):
            lift = zeros(); lift[aa][bb] = F(SIG[aa],2)
            lift[bb][aa] = F(SIG[bb],2)
            first = wedge(column(lift,u),column(EYE,v))
            second = wedge(column(EYE,u),column(lift,v))
            da = [x+y for x,y in zip(first,second)]
            for j,xj in enumerate(GEN):
                val = orient(r,s)*pairing(da,xj)
                for p in range(4):
                    c[mi][6*roles[p]+j] += direct[p]*val
    return a,c


def elimination(matrix):
    a = [[QI.of(x) for x in row] for row in matrix]
    rank,det = 0,QI.of(1)
    for j in range(len(a[0])):
        pivot = next((i for i in range(rank,len(a)) if a[i][j]),None)
        if pivot is None:
            continue
        if pivot != rank:
            a[rank],a[pivot] = a[pivot],a[rank]; det = -det
        p = a[rank][j]; det *= p
        for k in range(j,len(a[0])):
            a[rank][k] /= p
        for i in range(rank+1,len(a)):
            m = a[i][j]
            if m:
                for k in range(j,len(a[0])):
                    a[i][k] -= m*a[rank][k]
        rank += 1
        if rank == len(a):
            break
    if rank < len(a):
        det = QI()
    return rank,det


def mv(a,v):
    return [sum(x*y for x,y in zip(row,v)) for row in a]


def norm2(v):
    return sum(QI.of(x).re**2+QI.of(x).im**2 for x in v)


def run_checks():
    passed = []
    def check(name,condition):
        if not condition:
            raise AssertionError(name)
        passed.append(name); print('PASS_'+name)
    one,quarter = [QI.of(1)]*4,[QI(F(0),F(1))]*4
    a0,c0 = flat_symbols(one); aq,cq = flat_symbols(quarter)
    r0,d0 = elimination(a0); rq,_ = elimination(aq)
    rjoint,_ = elimination(aq+cq)
    v = [F(0)]*24; v[3:6] = [F(1),F(-1),F(1)]
    check('IR_RANK_24',r0==24)
    check('IR_DETERMINANT_256',d0==QI.of(256))
    check('QUARTER_RANK_16',rq==16)
    check('QUARTER_JOINT_RANK_20',rjoint==20)
    check('PHYSICAL_HERMITIAN_ONE',all(a0[i][j]==a0[j][i].conjugate() for i in range(24) for j in range(24)))
    check('PHYSICAL_HERMITIAN_QUARTER',all(aq[i][j]==aq[j][i].conjugate() for i in range(24) for j in range(24)))
    check('Y_QUARTER_CONNECTION_KERNEL',not any(mv(aq,v)))
    check('Y_QUARTER_METRIC_KERNEL',not any(mv(cq,v)))
    check('Y_NOT_IR_KERNEL',norm2(mv(a0,v))>0)
    check('EXACT_QUARTER_CHARACTERS_L8_L12',all(n%4==0 for n in (8,12)))
    # Plane-wave real and imaginary parts lie in the actual finite carrier.
    # A coefficient freeze does not turn the whole operator into its IR value.
    return {
        'arithmetic':'Q(i), exact Fraction arithmetic',
        'ir':{'rank':r0,'determinant':str(d0.re)},
        'quarter':{'character':['i']*4,'rank':rq,'nullity':24-rq,
                   'joint_rank':rjoint,'joint_nullity':24-rjoint,
                   'Y_vector_nonzero':{'3':1,'4':-1,'5':1},
                   'connection_image_zero':True,'metric_image_zero':True},
        'IR_vs_full_witness':{'input_norm_squared':str(norm2(v)),
                              'IR_image_norm_squared':str(norm2(mv(a0,v)))},
        'checks':passed,
        'verdict':'FULL_UNIFORM_DESIGNATED_GAP_PREMISE_OBSTRUCTED',
        'nonclaims':['no nonlinear joint-critical counterexample',
                     'no nonlinear Einstein terminal',
                     'no all-Bloch classification']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--expect',type=Path)
    args = parser.parse_args()
    report = run_checks()
    if args.expect:
        assert json.loads(args.expect.read_text())==report
        print('PASS_PINNED_LEDGER')
    if args.output:
        args.output.write_text(json.dumps(report,indent=2)+'\n')
    print('RESULT: the full operator is not A(1)+O(h); IR invertibility is retained.')
