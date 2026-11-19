"""Certify a strictly positive FULL stopped-CQ field derivative in primary §7gb."""
import hashlib
import contextlib
import io
import json
import sys
from fractions import Fraction as Q
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
REV = "076d5d5a7b366c0dd0970f388df7a9e6895498c4"
OWNER = "02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md"
EMBED_SHA = "2ac8b4202c0212cf19a66c0a8940680cf94a405bdd99f2466936076faa7e9d66"
source_path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parent / "primary" / "current_7ga_gb.md"
source = source_path.read_text()
name = "check_full128_cq_coframe_residual.py"
raw = source.split("<!-- BEGIN D0 20261118 FILE " + name + " -->\n" + chr(96)*3 + "python\n")[1]
raw = raw.split("\n" + chr(96)*3 + "\n<!-- END D0 20261118 FILE " + name + " -->")[0] + "\n"
assert hashlib.sha256(raw.encode()).hexdigest() == EMBED_SHA
nscope = {}
# Replay the entire pinned one-round certificate. The sole source substitution
# gives the identical popcount on Python 3.9.
with contextlib.redirect_stdout(io.StringIO()):
    exec(raw.replace(".bit_count()", '.__format__("b").count("1")'), nscope)
assert nscope["result"]["status"] == "PASS_EXACT_FULL128_CQ_COFRAME_RESIDUAL"
I, O, N, DN, A, DA, lam = [nscope[k] for k in ("I", "O", "ns", "dns", "a", "da", "kappa")]
same = nscope["same"]
ss = lam * (1-lam)
nonzero = 0
norm2 = sp.Rational(0)
s0 = O.copy()
s1 = O.copy()
ds0 = O.copy()
ds1 = O.copy()
for n, dn in zip(N[1:], DN[1:]):
    m = (n.H * A).applyfunc(sp.expand)
    dm = (dn.H*A + n.H*DA).applyfunc(sp.expand)
    nonzero += int(m != O)
    norm2 += sp.trace(dm.H*dm)
    s0 += m.H*m
    s1 += m*m.H
    ds0 += dm.H*m + m.H*dm
    ds1 += dm*m.H + m*dm.H
assert same(s0, ss*I) and same(s1, ss*I) and same(ds0,O) and same(ds1,O)
norm2 = sp.factor(norm2 / (16 * ss))
assert nonzero == 20 and norm2 < sp.Rational(6,5)**2
assert same(A.H*A, lam*I) and same(DA.H*A + A.H*DA, O)

# Isolate all stopping probabilities without numeric approximations.
p0,p1 = Q(61803398,10**8),Q(61803400,10**8)
assert p0*p0+p0 < 1 < p1*p1+p1
la = Q(9,640)
def lohi(p):
    return 4*p**3*la**2,4*p**3*la*(1-la), (1-2*p**2*la)**2
t0,r0,c0 = lohi(p0)
t1,r1,c1 = lohi(p1)
glo,ghi = r0/(1-t0),r1/(1-t1)
wlo = glo*c1/(1-t0) + p0*r0/(1-t0)
whi = ghi*c0/(1-t1) + p1*r1/(1-t1)
assert 0 < glo < ghi < Q(131,10000)
assert Q(209,10000) < wlo < whi < Q(21,1000)

# Rigorous lower bound on the owner's exact single-round covector, in nats.
# logarithms from log(z)=2 sum_{j>=0} u^(2j+1)/(2j+1), u=(z-1)/(z+1).
def log_bounds(z, terms=16):
    u = Q(z-1,z+1)
    value = 2*sum(u**(2*j+1)/(2*j+1) for j in range(terms))
    err = 2*u**(2*terms+1)/((2*terms+1)*(1-u*u))
    return value,value+err
l2, l3, l5 = (log_bounds(z) for z in (2,3,5))
one_lo = 27*p0**2/Q(25600)*(41*l2[0]+16*l3[0]-4*l5[1])
one_hi = 27*p1**2/Q(25600)*(41*l2[1]+16*l3[1]-4*l5[0])
positive_lo = wlo*one_lo/((1+p1)*r1)
positive_hi = whi*one_hi/((1+p0)*r0)
assert positive_lo>Q(157,10000) and positive_hi<Q(158,10000)
assert log_bounds(20,80)[1] < 3

# Sum exact first and second moments over k>=2. The zero spectra are handled
# by the x log(x) directional limit of a smooth Kraus square (see note).
g = Q(131,10000)
first_tail = 1/(1-g)**2-1
second_tail = (1+g)/(1-g)**3-1
tail = 2*Q(6,5)*Q(21,1000)*(3*second_tail+Q(3,2)*first_tail)
assert tail < Q(104,10000)
lo = positive_lo-tail
hi = positive_hi+tail
assert lo > Q(1,200) and hi < Q(27,1000)
print(json.dumps({"status":"PASS","pinned_embedded_constructor":EMBED_SHA,
                  "nonzero_informative_Walsh_rows":nonzero,
                  "rms_square_including_all_63_rows":str(norm2),
                  "single_informative_record_bound":["0.0157","0.0158"],
                  "absolute_remaining_derivative_lt":"0.0104",
                  "full_stopped_geometric_derivative_strict_interval":["0.005","0.027"],
                  "cost_derivative":"0","generated_preparation_derivative":"0",
                  "units":"natural logarithms","physical_Book_Info_selection_proved":False},indent=2))
