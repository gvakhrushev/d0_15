"""Real NC1 switch report, exact stopped lengths, raw pointer accounting and first jets."""
from fractions import Fraction as F
from pathlib import Path
import sys

import mpmath as mp
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "round79" / "writer"))
from check_sharp_history_writer import G, X, equal, e0, e1, expanded_reset, v


def reports(previous_B, current_B):
    current_P = 1 - current_B
    switch = previous_B ^ current_B
    # The native reset is an exact all-column addressed inverse on any old PORT/Spin.
    flip = (sp.eye(2), X)
    head = flip[current_B] * flip[previous_B] * G.T * v
    assert equal(head, (e0, e1)[switch])
    for value in (current_P, switch):
        tail = flip[value] * G * flip[value] * v
        assert equal(tail, e0 if value else G*v)
    native = ("0", "10")
    return native[current_P], native[switch]


def histories(u, m):
    # Enumerate the actual stopped branches, including the truncation bit.
    out = []
    for k in range(m+1):
        out.append(([1]*k + [0], u if k == 0 else (1-u)**2*u**(k-1)))
    out.append(([1]*(m+1), (1-u)*u**m))
    return out


def exact_check():
    expanded_reset()
    table = {(a,b): reports(a,b) for a in (0,1) for b in (0,1)}
    for m in range(8):
        for u in (F(1,17), F(3,13), F(7,24)):
            total = duration = symbols = upper = lower = F(0)
            for path, mass in histories(u,m):
                prev = 0
                letters = []
                for sector in path:
                    letters.extend(table[prev,sector])
                    prev = sector
                total += mass
                duration += mass*len(path)
                symbols += mass*sum(map(len,letters))
                upper += mass*path.count(0)
                lower += mass*path.count(1)
            assert total == 1 and duration == 2-u**m
            assert symbols == 7-2*u-2*(2-u)*u**m
            assert upper == 1-(1-u)*u**m and lower == 1-u**(m+1)
            for eta in (F(7,8),F(9,10)):
                failures = duration*(1-eta)/eta
                raw_symbols = 3*(upper+lower)+2*failures
                assert raw_symbols == (1+2/eta)*duration
    u,m=sp.symbols('u m', positive=True)
    L=7-2*u-2*(2-u)*u**m
    assert sp.simplify(sp.diff(L,u)-(-2+2*u**m-2*m*(2-u)*u**(m-1)))==0
    print("exact NC1 slots and stopped tree: caps 0 through 7, including overflow")


def certify():
    iv=mp.iv
    iv.dps=65
    p=(iv.sqrt(5)-1)/2
    base=iv.ln(1/p)
    def h(u): return -(u*iv.ln(u)+(1-u)*iv.ln(1-u))/base
    eta=(iv.mpc(iv.sqrt(p),p)**16).imag**2
    c_idle=h(eta)/eta
    assert 0.8006 < c_idle.a < c_idle.b < 0.8008
    assert (iv.ln(iv.mpf(7)/3)/base).a>1 and (iv.ln(2)/base).b<1.45
    data=[]
    for s in (2,3):
        u=p**(6*s)
        L=7-2*u
        H=2*h(u)
        raw_L=2*(1+2/eta)
        raw_H=2*c_idle
        data.append((L,H,L-H,L+raw_L-H-raw_H))
        for cap in (1,2,16):
            N=2-u**cap
            c=7-2*u-2*(2-u)*u**cap
            print(s,'cap',cap,'length',float(c.mid),'coarse entropy',float((N*h(u)).mid))
        print(s,'unbounded base %.12f, info %.12f, raw letters %.12f, raw extra info %.12f'%
              tuple(float(x.mid) for x in (L,H,raw_L,raw_H)))
    d=[y-x for x,y in zip(*data)]
    assert .00586 < d[0].a < d[0].b < .00587
    assert -.08048 < d[1].a < d[1].b < -.08046
    assert .08633 < d[2].a < d[2].b < .08635
    assert (d[2]-d[3]).a<=0<=(d[2]-d[3]).b
    print('NPS2 secants, base length/coarse entropy/net/all-pointers net:',
          *[float(x.mid) for x in d])


if __name__ == "__main__":
    exact_check()
    certify()
