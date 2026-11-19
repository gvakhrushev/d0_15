"""Certify the closest integer tariff on the pinned 128-outcome coframe row."""
from fractions import Fraction as F
from math import isqrt
from decimal import Decimal, localcontext
from pathlib import Path
import argparse
import json
import runpy
_shared = runpy.run_path(str(Path(__file__).with_name("check_constraints.py")))
check, load_table = _shared["check"], _shared["load_table"]

Q = 10**56

def ceil_div(x,y):
    return -((-x)//y)

def mul(x,y):
    products=[i*j for i in x for j in y]
    return min(products)//Q, ceil_div(max(products),Q)

def add(x,y):
    return x[0]+y[0],x[1]+y[1]

def scale(x,n):
    a,b=x[0]*n,x[1]*n
    return min(a,b),max(a,b)

def ratio(x,y):
    check(x[0]>=0 and y[0]>0,"positive quotient")
    return x[0]*Q//y[1],ceil_div(x[1]*Q,y[0])

def ln_interval(y):
    """Return proven integer brackets for Q ln(y/Q), 1 <= y/Q <= 5."""
    z=ratio((y[0]-Q,y[1]-Q),(y[0]+Q,y[1]+Q))
    check(3*z[1]<=2*Q+3,"atanh argument <= 2/3 plus grid rounding")
    zz=mul(z,z)
    power=z
    acc=(0,0)
    for j in range(200):
        k=2*j+1
        acc=add(acc,(power[0]//k,ceil_div(power[1],k)))
        power=mul(power,zz)
    # 2 * z^401/[401 (1-z²)] is an upper bound on the positive tail.
    return 2*acc[0], 2*acc[1]+ceil_div(2*power[1]*Q,401*(Q-zz[1]))

def abs_interval(x):
    return max(x[0],-x[1],0),max(x[1],-x[0])

def display(interval):
    with localcontext() as ctx:
        ctx.prec=70
        return [str(Decimal(t)/Decimal(Q)) for t in interval]

def nearest(p,p2,t,c,R):
    M=36*R
    possibilities=[]
    for i in range(-M,M+1):
        base=add(scale(p2,i),scale(t,-1))
        # Only these two candidates can minimize |base+j p| for fixed i.
        approx=(-(base[0]+base[1]))//(p[0]+p[1])
        jlist=sorted(set(min(M,max(-M,j)) for j in (approx,approx+1)))
        if jlist[0]>-M:
            check(add(base,scale(p,jlist[0]))[1]<=0,"left monotonicity")
        if jlist[-1]<M:
            check(add(base,scale(p,jlist[-1]))[0]>=0,"right monotonicity")
        for j in jlist:
            err=abs_interval(add(base,scale(p,j)))
            possibilities.append((err[0],err[1],i,j))
    possibilities.sort()
    lo,hi,i,j=possibilities[0]
    check(lo>0 and hi<possibilities[1][0],"unique certified minimum")
    return {"N0":i,"N1":j,"scaled_residual_bounds":display((lo,hi)),
            "source_residual_bounds":display(mul(c,(lo,hi)))}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",type=Path,default=None)
    args=ap.parse_args()
    rows=load_table(args.repo)
    weights=[F(x["D_Tr_M"])*F(40,3) for x in rows]
    check(sorted(weights)==[-36]+[1]*4+[4]*8,"pinned actual row")
    root=isqrt(5*Q**2)
    p=((root-Q)//2, ceil_div(root+1-Q,2))
    phi=add((Q,Q),p)
    p2=add((Q,Q),scale(p,-1))
    p3=add(scale(p,2),(-Q,-Q))
    c=ratio(scale(p2,27),(102400*Q,102400*Q))
    logphi=ln_interval(phi)
    logs={d:ln_interval((d*Q,d*Q)) for d in (2,3,5)}
    result={}
    for n in (41,42):
        ell=add(add(scale(logs[2],n),scale(logs[3],16)),scale(logs[5],-4))
        target=add(ratio(scale(ell,4),logphi),scale(p3,-24))
        result[str(n)]={str(r):nearest(p,p2,target,c,r) for r in (1,6,8,9,10,16,32,64,128)}
    print(json.dumps({"status":"PASS","convention":"target=4*L_k/ln(phi)-24*p^3; k=41 (CQ),42 (fine); source residual = scaled residual * 27*p^2/102400","cases":result},indent=2))

if __name__=="__main__":
    main()
