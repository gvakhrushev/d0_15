"""Marginal stopped Shannon row on the published full128 V00-V01 tangent."""
import json, math
from collections import defaultdict
from fractions import Fraction as Q
from itertools import product
from pathlib import Path

# Reuse exact integer realification and rigorous rational log enclosures.
# These are the earlier replay packages for the same unchanged primary matrices.
anchor=Path(__file__).resolve().with_name("frozen")
source=(anchor/"check_cq_bright_terms.py").read_text()
ctx={"__file__":str(anchor/"check_cq_bright_terms.py")}
exec(compile(source.split("def log_poly(signature):")[0].rsplit("@lru_cache(None)",1)[0], str(anchor/"check_cq_bright_terms.py"), "exec"),ctx)
R,DR,coeff,mm,inner,logi,iscale=[ctx[k] for k in ("R","DR","coeff","mm","inner","logi","interval_scale")]
import contextlib, io, runpy
with contextlib.redirect_stdout(io.StringIO()):
    original=runpy.run_path(str(anchor/"check_full128_cq_coframe_residual.py"))
assert all(x == y for x,y in zip(original["ns"],ctx["base"]["N"]))
assert all(x == y for x,y in zip(original["dns"],ctx["base"]["DN"]))
assert list(map(len,(original["ns"],original["dns"]))) == [64,64]
D=ctx["D"]
np=ctx["np"]
jets={}
for k in (1,2,3):
    masses=defaultdict(Q)
    total=dmass=Q(0)
    for ids in product(range(20),repeat=k):
        b,db=R[ids[0]],DR[ids[0]]
        for j in ids[1:]:
            db=mm(DR[j],b)+mm(R[j],db)
            b=mm(R[j],b)
        c=math.prod(coeff[j] for j in ids)/32
        prob=c*inner(b,b)
        dp=2*c*inner(b,db)/D
        if prob:
            masses[prob]+=dp
        else:
            assert dp==0
        total+=prob
        dmass+=dp
    assert total==1 and dmass==0
    lo=hi=Q(0)
    for prob,dp in masses.items():
        if dp==0: continue
        # Exact probability, logarithm evaluated as a rational interval.
        l,u=iscale(-dp,logi(prob))
        lo+=l
        hi+=u
    jets[k]=(lo,hi)

def iadd(a,b):
    return (a[0]+b[0],a[1]+b[1])
def imul(a,b):
    vals=[x*y for x in a for y in b]
    return (min(vals),max(vals))
def outward(a,scale=10**11):
    return [str(Q((a[0]*scale).__floor__(),scale)),str(Q((a[1]*scale).__ceil__(),scale))]
def show(a):
    return [float(y) for y in a]
u=10**40
pl=Q(math.isqrt(5*u*u)-u,2*u)
pu=pl+Q(1,2*u)
t=Q(9,640)
def rrate(p):
    q=4*p**3*t
    return q*(1-t)/(1-q*t)
gl,gu=rrate(pl),rrate(pu)
hq=(Q(0),Q(0))
for k,v in jets.items():
    wt=((1+pl)*(1-gu)*gl**k,(1+pu)*(1-gl)*gu**k)
    hq=iadd(hq,imul(wt,v))
# For probabilities p_w=||B_w||^2_HS/d, |D H_k| <= 2 k C sqrt(E(log p_w)^2).
# At most 20^k positive words, E(log p_w)^2 <= (k log20+sqrt2)^2.
s1=gu/(1-gu)**2-sum(j*gu**j for j in range(1,4))
s2=gu*(1+gu)/(1-gu)**3-sum(j*j*gu**j for j in range(1,4))
tail=2*Q(13,10)*(1+pu)*(1-gl)*(logi(Q(20))[1]*s2+Q(142,100)*s1)
full=iadd(hq,(-tail,tail))
cq_raw=json.loads((anchor/"cq_bright_terms_result.json").read_text())
cq=tuple(map(Q,cq_raw["stopped_jet_outward_rational"]))
gap=(full[0]-cq[1],full[1]-cq[0])
def rc(p):
    return 81*p**5/(12800*(1-4*p**3*t))
cost=(rc(pl),rc(pu))
lnphi=(logi(1/pu)[0],logi(1/pl)[1])
def resto(a):
    return (a[0]/lnphi[1]-cost[1],a[1]/lnphi[0]-cost[0])
assert gap[0]>0
print(json.dumps(dict(status="PASS_EXACT_STORED_ROW_JETS_RATIONAL_LOG_ENCLOSURES", n_bright=list(jets),
    marginal_single_informative_derivatives={str(k):outward(v) for k,v in jets.items()},
    common_absolute_tail_k_ge_4=outward((Q(0),tail))[1],
    stopped_joint=outward(full),stopped_data=outward(cq),stopped_gap=outward(gap),
    stopped_reader=outward(cost),residual_data=outward(resto(cq)),residual_joint=outward(resto(full)),
    display={"joint":show(full),"gap":show(gap),"reader":show(cost),
             "residual_data":show(resto(cq)),"residual_joint":show(resto(full))}),indent=2))
