#!/usr/bin/env python3
"""Exact native full128 J23 Fisher coarsening witness from pinned original Q(sqrt5) receipt.

Consumes #334 ORIGINAL file:
sources/d0_native_full128_order_readout_2026-10-19/COMPLETE_SHANNON_SOURCE.json.
Does not rerun the 16x16x128 Kraus or infer native Book Cost-Info selection.
"""
import json
from pathlib import Path
import sympy as s

here=Path(__file__).resolve().parent
receipt=here.parent/"d0_native_full128_order_readout_2026-10-19"/"COMPLETE_SHANNON_SOURCE.json"
data=json.loads(receipt.read_text())
assert data["status"]=="PASS_SCOPED_COMPLETE_FULL128_SHANNON_FIRST_SOURCE"
rows=data["probability_law"]["groups"]
R=s.sqrt(5)
groups=[]
for row in rows:
    q=s.sympify(row["probability"],locals={"sqrt":s.sqrt})
    dq=s.sympify(row["source_sum"],locals={"sqrt":s.sqrt})
    groups.append((int(row["multiplicity"]),q,dq))
assert sum(m for m,q,dq in groups)==128
assert s.simplify(sum(m*q for m,q,dq in groups)-1)==0
assert s.simplify(sum(dq for m,q,dq in groups))==0
assert sum(m for m,q,dq in groups if q==0)==86
zero=[(m,q,dq) for m,q,dq in groups if q==0]
assert all(dq==0 for _,_,dq in zero)

blank=[g for g in groups if s.N(g[1])>s.Rational(1,2)]
special=[g for g in groups if g[0]==7]
assert len(blank)==len(special)==1
m0,q0,dq0=blank[0]
mx,qper,dqx=special[0]
assert m0==1 and mx==7
assert s.simplify(q0-(5034167+28557*R)/5120000)==0
assert s.simplify(dq0-(42633-14157*R)/5120000)==0
assert s.simplify(qper-(567-243*R)/5120000)==0
assert s.simplify(dqx-(-1701+729*R)/5120000)==0

Qx=s.simplify(mx*qper)
Qr=s.simplify(1-q0-Qx)
dQr=s.simplify(-dq0-dqx)
assert s.simplify(dqx/Qx+s.Rational(3,7))==0
assert s.simplify(dQr/Qr+s.Rational(1,2))==0
assert Qx.is_positive and Qr.is_positive

Ibinary=s.simplify(dq0**2/(q0*(1-q0)))
Ithree=s.simplify(dq0**2/q0+dqx**2/Qx+dQr**2/Qr)
# First (untruncated) original 128-outcome Fisher >= Cauchy grouped bound
# because within each equal-probability group we know only the SUM of dq.
Igroup=s.simplify(sum(dq**2/(m*q) for m,q,dq in groups if q!=0))
assert s.simplify(Igroup-Ithree)==0
gap=s.simplify(Ithree-Ibinary)
assert s.simplify(gap-Qx*Qr/(196*(Qx+Qr)))==0
assert gap.is_positive

print("PASS original native 128=42 positive +86 dark, all first jets normalized")
print("PASS special 7-outcome Lorentz J23 score=-3/7; other exits=-1/2")
print("PASS full Fisher >= exactly calculable three-group Fisher > binary blank/exit")
print("Iblank   =",s.N(Ibinary,23))
print("I3 lower =",s.N(Ithree,23))
print("extra    =",s.N(gap,23))
print("ratio    =",s.N(Ithree/Ibinary,23))
print("SCOPE native J23 readout; original full Book Cost-Info and GR not selected")
