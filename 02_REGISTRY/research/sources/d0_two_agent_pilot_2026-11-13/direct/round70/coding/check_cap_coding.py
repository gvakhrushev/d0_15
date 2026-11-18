"""Enumerate the complete conditional cap-three B130 laws and their two score norms."""
from collections import defaultdict
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import sympy as s

path = Path(__file__).resolve().parents[1] / "arithmetic/coframe/check_coframe_gap.py"
spec = spec_from_file_location("cap_coframe", path)
c = module_from_spec(spec)
spec.loader.exec_module(c)
p = (s.sqrt(5)-1)/2
rare = c.RARE
qfield = lambda x: s.expand(s.radsimp(x))


def scalar(pattern, ports, lam, dlam):
    w, dw = s.Integer(1), s.Integer(0)
    for quiet, b in zip(pattern, ports):
        if quiet and not b:
            q, dq = (1-2*p**2*lam)**2, -4*p**2*(1-2*p**2*lam)*dlam
        elif quiet and b:
            q, dq = 4*p**3*lam**2, 8*p**3*lam*dlam
        else:
            q, dq = (4*p**3 if b else 4*p**4), 0
        w, dw = w*q, dw*q + w*dq
    return qfield(w), qfield(dw)


def enumerate_direction(direction):
    ds = c.constructor(direction)
    orig, deriv, lam = ds["ns"], ds["dns"], ds["kappa"]
    a, da = orig[0], deriv[0]
    dlam = s.Rational(3,64) if direction=="nu" else 0
    eye, zero = c.matrix(ds["I"]), c.matrix(ds["O"])
    ops, e, de, preparations = {}, {}, {}, {}
    norm2 = 0
    speeds = {}
    for k,(n,dn) in enumerate(zip(orig, deriv)):
        b,db = n.H*a, dn.H*a+n.H*da
        norm2 += s.expand(s.trace(db.H*db))
        if k in (0,*rare):
            gram = s.expand(s.trace(b.H*b))
            cross = s.re(s.expand(s.trace(b.H*db)))
            speeds[k] = s.factor(s.expand(s.trace(db.H*db))/gram-(cross/gram)**2)
            out, dout = c.matrix(b*b.H), c.matrix(db*b.H+b*db.H)
            preparations[k] = c.state_jet(out,dout)
        b, bh, db, dbh = (c.matrix(x) for x in (b,b.H,db,db.H))
        if k==0:
            b,bh,db,dbh = eye,eye,zero,zero
        ops[k] = b,bh,db,dbh
        e[k] = bh.matmul(b)
        de[k] = dbh.matmul(b)+bh.matmul(db)
    bound = 2*(s.sqrt(max(speeds.values()))+2*s.sqrt(4*p**2*norm2))
    assert norm2 == (s.Rational(205,256) if direction=="nu" else s.Rational(1601,5120))
    assert bound < (s.Rational(4425,1000) if direction=="nu" else s.Rational(7298,1000))
    live = [k for k in range(64) if e[k] != zero]
    dark = [k for k in range(64) if e[k] == zero]
    assert len(live) == 21 and all(de[k] == zero for k in dark)
    print(direction, "incoming derivative norm squares", speeds)
    for label,(rho,drho) in preparations.items():
        # Aggregate rationals separately from factors of p of the port choices.
        groups = defaultdict(lambda:[0,s.S.Zero,s.S.Zero,s.S.Zero])
        def add(pattern,mass,rate):
            assert mass>=0
            if mass==0:
                assert rate==0
                return
            row = groups[pattern]
            row[0] += 1
            row[1] += mass
            row[2] += rate
            row[3] += rate**2/mass
        for j in live:
            b,bh,db,dbh = ops[j]
            state = b.matmul(rho).matmul(bh)
            rate = db.matmul(rho).matmul(bh)+b.matmul(drho).matmul(bh)+b.matmul(rho).matmul(dbh)
            add((j==0,),c.tr(state),c.tr(rate))
            for k in live:
                m = c.trace_pair(e[k],state)
                dm = c.trace_pair(de[k],state)+c.trace_pair(e[k],rate)
                add((j==0,k==0),m,dm)
        total = dtotal = fisher = s.S.Zero
        bright = 0
        for pattern,(hits,m,dm,info) in groups.items():
            for ports in (((0,),) if len(pattern)==1 else ((1,0),(1,1))):
                w,dw = scalar(pattern,ports,lam,dlam)
                total += w*m
                dtotal += w*dm+dw*m
                fisher += w*info+2*dw*dm+dw**2*m/w
                bright += hits
        assert qfield(total-1)==qfield(dtotal)==0
        fisher = qfield(fisher)
        assert fisher>=0 and fisher<bound**2
        if direction == "nu":
            expected = (15621-4715*s.sqrt(5))/16384
        else:
            sig = {
                0:(739471599,32768000000,44638509,6553600000),
                13:(1022449868679,43356160000000,61903220789,8671232000000),
                29:(24793629619887,1083904000000000,1497504492717,216780800000000),
            }
            aa,bb,cc,dd = sig[{45:13,61:29}.get(label,label)]
            expected = s.Rational(aa,bb)-s.Rational(cc,dd)*s.sqrt(5)
        assert qfield(fisher-expected)==0
        assert fisher < (s.Rational(557,1000) if direction=="nu" else s.Rational(88,1000))**2
        print(direction, label, "bright", bright, "dark", 8256-bright, "Fisher", float(fisher))
        assert bright == 903
        yield label, fisher


if __name__=="__main__":
    for axis in ("v","nu"):
        print(axis, "scores squared", {j: str(x) for j,x in enumerate_direction(axis)})
    m, alphabet = 10**32, 528576
    assert sum(s.S.One/s.factorial(i) for i in range(6)) > s.Rational(27,10)
    assert s.Rational(27,10)**75 > m+1
    c_bound = 75*(alphabet-1)+3
    assert 2*s.Rational(88,1000)*c_bound/10**16 < s.Rational(7,10**10)
    assert 2*s.Rational(557,1000)*c_bound/10**16 < s.Rational(45,10**10)
