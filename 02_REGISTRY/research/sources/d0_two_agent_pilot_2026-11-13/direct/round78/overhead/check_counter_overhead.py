"""Native attempts, raw P/Q signs, ticket work and stopped Shannon on the A75 vector."""
import json
import sys
from fractions import Fraction as Q
from functools import lru_cache
from math import comb
from pathlib import Path

import numpy as np

sys.dont_write_bytecode=True
DIRECT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(DIRECT/"round75/work"))
import check_pointer_weyl as owner

I,O=owner.I,owner.O
L=12


def product(a,b):
    out=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            out[i+j]+=x*y
    return out


def solve():
    p,C,w,dw,fw,bw,_,_,_=owner.site_vector()
    phi_log=-O.logarithm(p)
    def act(v,k):
        return owner.dirac(v,k,fw,bw)
    def kernel(v,dv):
        for i in range(4):
            dv=act(dv,w)+act(v,dw)
            v=act(v,w)
            if i==1:
                v2,d2=v,dv
        return 4*p*p*(v2-p*p*v),4*p*p*(d2-p*p*dv)

    V,DV=[C],[I(np.zeros_like(C.lo))]
    for _ in range(8):
        v,dv=kernel(V[-1],DV[-1])
        V.append(v)
        DV.append(dv)
    m,dm=[I(1.)],[I(0.)]
    for k in range(1,17):
        a,b=k//2,(k+1)//2
        m.append(O.reduce_sum(V[a]*V[b]))
        dm.append(O.reduce_sum(DV[a]*V[b]+V[a]*DV[b]))
    # All remaining native powers satisfy ||K||<1/100 and ||DK||<16,
    # as certified on the full primary carrier in the companion history check.
    for k in range(17,64):
        m.append(I(0.,float(I.rational(Q(1,100**k)).hi)))
        hi=float(I.rational(Q(16*k,100**(k-1))).hi)
        dm.append(I(-hi,hi))
    def eval_poly(poly):
        return tuple(sum((c*v for c,v in zip(poly,s) if c),I(0.)) for s in (m,dm))
    def traced(j,h):
        zeta=[(-1)**k*comb(j,k) for k in range(j+1)]
        failure=[0]+[-x for x in zeta[1:]]
        @lru_cache(None)
        def row(success,fail):
            poly=[(-1)**k*comb(h+j*success,k) for k in range(h+j*success+1)]
            for _ in range(fail):
                poly=product(poly,failure)
            raw,draw=eval_poly(poly)
            mass,dmass=normalizer
            q=raw/mass
            return q,(draw-q*dmass)/mass
        normalizer=eval_poly([(-1)**k*comb(h,k) for k in range(h+1)])
        O.require(normalizer[0].lo>.97 and row(0,1)[0].lo>.001,
                  "physical lower normalization and Jensen log support")
        results={k:[I(0.),I(0.)] for k in ("attempts","ones","work","entropy","pairs")}
        def add(name,val,jet):
            results[name][0]+=val
            results[name][1]+=jet
        for f in range(L):
            for s in (0,1):
                ways=comb(f+s,s)
                total,dtotal=row(s,f)
                success,ds=row(s+1,f)
                failed,df=row(s,f+1)
                # Use the support range even when tiny mass intervals
                # would make an explicit conditional ratio ill-conditioned.
                rl,rh=.97,1.
                if total.lo>0:
                    candidate=success/total
                    rl=max(rl,float(candidate.lo))
                    rh=min(rh,float(candidate.hi))
                ratio=I(rl,rh)
                add("attempts",ways*total,ways*dtotal)
                one,done=(success,ds) if f%2==0 else (failed,df)
                add("ones",ways*one,ways*done)
                add("work",ways*(total+2*failed*ratio),
                    ways*((1+2*(I(1.)-ratio).square())*ds+(1+2*ratio.square())*df))
            g,dg=row(2,f)
            lower=I.rational(Q(97,100)**2*Q(1,1000)**f)
            logg=O.logarithm(I(max(float(g.lo),float(lower.lo)),
                                min(float(g.hi),1.)))
            add("entropy",-(f+1)*g*logg/phi_log,-(f+1)*dg*logg/phi_log)
            if f>=2:
                bits=(f-1).bit_length()
                mult=I.rational(Q(bits*2**bits,f))/(p*p*p)
                q,dq=row(0,f)
                add("pairs",mult*q,mult*dq)
        # For f>=12 both value and directional derivative, including log,
        # are dominated by 100000(f+2)^3 (.03)^(f-1); successive ratio <.04.
        tail=float(I.rational(Q(100000*(L+2)**3)*Q(3,100)**(L-1)*Q(25,24)).hi)
        for name,(amount,jet) in results.items():
            results[name]=[amount+I(-tail,tail),jet+I(-tail,tail)]
        cost=[(a+b) for a,b in zip(results["attempts"],results["ones"])]
        pair_work=2*(1+2*p*p*p)
        for key,scale in (("literal_net",I(0.)),("net_one_tick",I(1.)),
                          ("net_sqrt22",I(22.).sqrt())):
            results[key]=[cost[k]+scale*(results["work"][k]+pair_work*results["pairs"][k])
                          -results["entropy"][k] for k in (0,1)]
        if h==j:
            mass,jet=normalizer
            O.require((results["attempts"][0]*mass-2).contains(0) and
                      (results["attempts"][1]*mass+results["attempts"][0]*jet).contains(0),
                      "gated absolute attempt bill and its source equal 2 and zero")
        return results
    all_rows={}
    for prior in ("original","after_blank"):
        cases=[traced(j,0 if prior=="original" else j) for j in (1,2,3)]
        all_rows[prior]={"j_1_2_3": [{k:[O.bounds(v) for v in pair] for k,pair in row.items()}
                                     for row in cases],
                         "second_difference_source": {k:O.bounds(cases[2][k][1]-2*cases[1][k][1]+cases[0][k][1])
                                                      for k in cases[0]}}
    def control(key):
        return (I(*all_rows["after_blank"]["second_difference_source"][key])
                -I(*all_rows["original"]["second_difference_source"][key]))
    control_bounds={k:O.bounds(control(k)) for k in ("literal_net","net_one_tick","net_sqrt22")}
    O.require(control_bounds["literal_net"][0]>6.6206e-5 and
              control_bounds["net_one_tick"][0]>3.8833e-5 and
              control_bounds["net_sqrt22"][1]<-6.0439e-5,
              "preparation-dependent compulsory comparisons for both named clock scales")
    all_rows["after_minus_original_second_difference_source"]=control_bounds
    return all_rows


if __name__=="__main__":
    print(json.dumps(solve(),indent=2))
