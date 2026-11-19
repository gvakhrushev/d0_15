"""Certify an unheralded finite key and a uniform bound on every positive binary history."""
from fractions import Fraction
from itertools import product
from math import cos, sin, asin, log, sqrt
from pathlib import Path
import json
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[4]/"d0_native_readiness_amplification_2026-10-24"))
from native_phase import native_rotation_intervals

p=(sqrt(5)-1)/2
ell=-log(p)
theta=asin(p)


def run():
    n=6
    # Seed both complementary names on identical golden births with the same
    # total length. Integer search proposes m; the native interval certifies it.
    _,m=min((abs(cos(j*theta)),j) for j in range(1,4097))
    cb,sb=native_rotation_intervals(m,bits=140)
    cerr=max(abs(Fraction(int(v.p),int(v.q))) for v in cb)
    assert cerr<1 and min(abs(float(v)) for v in sb)>.999
    delta=float(cerr**2)
    ideal=(.665,.785)
    # Bad name 00 in a two-lane circuit can produce an arbitrary joint law.
    # Deliberately put all bad mass on the least likely good word.
    for s in ideal:
        P=[s**sum(w)*(1-s)**(n-sum(w)) for w in product((0,1),repeat=n)]
        bad=[float(i==P.index(min(P))) for i in range(len(P))]
        Q=[(1-delta)*v+delta*b for v,b in zip(P,bad)]
        bound=max(-log(1-delta),log(1+delta*5**n))/ell
        assert all(abs(log(q/v)/ell)<=bound+1e-13 for q,v in zip(Q,P))
        ent=lambda probs:-sum(v*log(v)/ell for v in probs if v)
        assert abs(ent(P)-ent(Q))<=ent((delta,1-delta))+delta*n*log(2)/ell
        for a in (0,.4,1):
            def price(probs):
                S=[(9*(n-sum(w))+2*sum(w))-a*ent(probs)+(1-a)*log(pr)/ell
                   for w,pr in zip(product((0,1),repeat=n),probs)]
                lo=min(S)
                return lo,lo-log(sum(p**(x-lo) for x in S))/ell
            assert max(abs(l-r) for l,r in zip(price(P),price(Q)))<=(
                    a*(ent((delta,1-delta))+delta*n*log(2)/ell)+(1-a)*bound+1e-12)
    print(json.dumps(dict(two_rail_one_rotation=m,bad_label_mass_upper=delta,
                          copies=n,word_relative_contamination_upper=delta*5**n,
                          geometric_all_column_precision_proven=False,GR_closed=False),indent=2))


if __name__=="__main__":
    run()
