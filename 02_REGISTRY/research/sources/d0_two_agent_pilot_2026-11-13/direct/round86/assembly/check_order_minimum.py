"""All admissible orders of two X and 2N Y commands, on the actual fresh Fourier tap."""
import itertools
import json
from decimal import Decimal, localcontext

import mpmath as mp
import numpy as np


def require(ok,msg):
    if not ok:
        raise ValueError(msg)


def flip(control,target):
    bits=np.arange(8)
    return np.eye(8,dtype=int)[:,bits^(((bits>>control)&1)<<target)]


def census(n,q):
    # Work-slot, target, known control. Old f,e supply the purification.
    X,Y=flip(2,0),flip(0,1)
    hist=[0]*(n+1)
    best=float("inf")
    for i,j in itertools.combinations(range(2*n+2),2):
        state=np.zeros((8,2))
        state[4,0],state[5,1]=np.sqrt(1-q),np.sqrt(q)
        total=0
        mat=np.eye(8,dtype=int)
        for pos in range(2*n+2):
            gate=X if pos in (i,j) else Y
            moved=np.einsum("ij,jk->ik",gate,state)
            total+=np.sqrt(max(0,1-abs(np.vdot(moved,state))**2))
            mat=gate @ mat
            state=moved
        accepted=np.array_equal(mat,np.eye(8,dtype=int))
        require(accepted==((j-i-1)%2==0),"full truth-table restoration")
        if accepted:
            k=(j-i-1)//2
            hist[k]+=1
            predicted=2+(2*n-2*k)*np.sqrt(2*q-q*q)+2*k*np.sqrt(1-q*q)
            require(abs(total-predicted)<1e-12,"motion for an arbitrary word")
            best=min(best,total)
    require(hist==[2*(n-k)+1 for k in range(n+1)],"word multiplicities")
    return best


def certified_neighbours():
    iv=mp.iv
    iv.dps=65
    p=(iv.sqrt(5)-1)/2
    b=iv.mpf(["0.01113313016680724180219075442448827511",
              "0.01113313016680724180219075442448827512"])**2
    q5,q6=2*p**3*17/16,2*p**3*(1+(1-2*b)/16)
    lp=-iv.log(p)
    def value(n,q):
        g=iv.sqrt(2*q-q*q)
        other=iv.sqrt(1-q*q)
        r=iv.exp(-2*lp*(g-other))
        a=(1-r**(n+1))/(1-r)
        b=(r-(n+1)*r**(n+1)+n*r**(n+2))/(1-r)**2
        return 2+2*n*other-iv.log(a+2*b)/lp
    for n in (1454,1455):
        diff=value(n,q6)-value(n,q5)
        require((diff.b<0) if n==1454 else (diff.a>0),"neighbouring budgets must have opposite signs")


def main():
    certified_neighbours()
    with localcontext() as ctx:
        ctx.prec=60
        p=(Decimal(5).sqrt()-1)/2
        # Intervals in the 712 G certificate enclose this rounded amplitude at >36 digits.
        b=Decimal("0.0111331301668072418021907544244882751144769")**2
        q5,q6=2*p**3*Decimal(17)/16, 2*p**3*(1+(1-2*b)/16)
        logphi=-(p.ln())
        def g(q):
            return (2*q-q*q).sqrt()
        def free(n,q):
            x=g(q)-g(1-q)
            r=(-2*logphi*x).exp()
            # s0=sum r^m, s1=sum m r^m, 0<=m<=n
            s0=(1-r**(n+1))/(1-r)
            s1=(r-(n+1)*r**(n+1)+n*r**(n+2))/(1-r)**2
            return 2+2*n*g(1-q)-(s0+2*s1).ln()/logphi
        for n in range(1,6):
            for q in (q5,q6):
                require(abs(census(n,float(q))-float(2+2*n*g(1-q)))<1e-12,"catalogue minimum")
        ds={str(n):float(free(n,q6)-free(n,q5)) for n in (1,16,1024,1454,1455,4096,10000)}
        require(ds["1"]<0<ds["10000"],"statistical sign changes with the time budget")
        r=(-2*logphi*(g(q6)-g(1-q6))).exp()
        loss=((1+r)/(1-r)**2).ln()/logphi
        safe=int(loss/(2*(g(1-q6)-g(1-q5))))+1
        require(free(safe,q6)>free(safe,q5),"conservative finite dominance bound")
        print(json.dumps({"exhaustive_max_pairs":5,"admissible_order_count":"(N+1)^2",
                          "fresh_Fourier_q5_gt_q6_gt_half":True,
                          "strict_min_F6_minus_F5_positive_for_all_positive_N":True,
                          "logsum_F6_minus_F5_at_unit_rate":ds,
                          "sufficient_pairs_from_infinite_tail_only":safe,
                          "shorter_service_admitted_eliminates_positive_identity_work":True,
                          "GR_closed":False},indent=2))


if __name__=="__main__":
    main()
