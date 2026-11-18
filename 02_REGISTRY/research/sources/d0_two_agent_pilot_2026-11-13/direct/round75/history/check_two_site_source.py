"""Interval witness against every positive mixture of 8192 native heat depths."""
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
import sys
from unittest.mock import patch

import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parent.parent/"curvature"))
import check_local_coframe_source as heat

car=heat.car
I=heat.I
SITE_A=(1,3,2,2)
SITE_B=(2,2,1,1)


def material_coefficients():
    nums=car.actual_counts(heat.ROOT)
    f=np.array(car.fourier_numerators())
    wt={z:heat.P*heat.P*heat.P*I.rational(Fraction(256*n,sum(nums))).sqrt()
        for z,n in zip(car.SITES_LIST,nums)}
    def empty():
        return defaultdict(lambda:I(np.zeros(128)))
    local={SITE_A:empty(),SITE_B:empty()}
    full=empty()
    for i,z in enumerate(car.SITES_LIST):
        for m,amp in ((1,heat.P.sqrt()),(14,heat.P)):
            for (y,k,source),coef in car.flat_column(z,m).items():
                part=amp*wt[source]*Fraction(coef,128)*I(f[i].astype(float))
                full[y,k]=full[y,k]+part
                if source in local:
                    local[source][y,k]=local[source][y,k]+part
    # For positive covariant dilation, delta D=-S_z. Store -delta R.
    return [2*sum((heat.interval.reduce_sum(full[k]*x) for k,x in local[z].items()),I(0.))
            for z in (SITE_A,SITE_B)]


def witness():
    a,b=material_coefficients()
    assert .04352821178<a.lo<a.hi<.04352821180
    assert .09870434925<b.lo<b.hi<.09870434928
    with patch.object(car,"W",SITE_A):
        T,A=heat.operators()
    with patch.object(car,"W",SITE_B):
        _,B=heat.operators()
    ca=(a.lo+a.hi)/2
    cb=(b.lo+b.hi)/2
    # Conservative exact local rank/HS estimate for either operator.
    # For numerical-basis evaluation its off-diagonal parity block has smaller HS norm.
    assert (32*144*(heat.P*heat.P*heat.P).square()*I.rational(Fraction(256*78,10946))*16).hi<90**2
    assert 90*(a.hi+b.hi)<64
    assert 12*max(ca-a.lo,a.hi-ca)+12*max(cb-b.lo,b.hi-cb)<5e-13
    # Each full geometric block has spectral coefficient error <1e-12.
    # Multiplication by its observed coefficient and this sparse sum preserve
    # the exact model tolerance used by the one-site numerical-basis theorem.
    mix=cb*A-ca*B
    assert (ca+cb)*1e-12+5e-13+24*np.finfo(float).eps<1e-12
    assert mix.getnnz(0).max()<=12 and mix.getnnz(1).max()<=12
    heat.frobenius_over(A.data,12)
    heat.frobenius_over(B.data,12)
    heat.frobenius_over(mix.data,8)
    # The inner certificate accepts any local source whose true nuclear norm
    # is <=64 and whose sparse off-diagonal block satisfies these error bounds.
    with patch.object(heat,"operators",return_value=(T,mix)):
        s,local=heat.numerical_basis()
    return a,b,s,local


def main():
    a,b,s,local=witness()
    # The common direction is V = b d/de_A - a d/de_B. Its R row is
    # b*(-a)-a*(-b)=0 algebraically; no rounded cancellation is used.
    groups=[]
    def certify(left,right):
        try:
            row,_=heat.across_depths(s,local,left,right)
            ok=row.lo>0
        except AssertionError:
            ok=False
        if not ok:
            assert left<right, ("failed at depth",left)
            mid=(left+right)//2
            certify(left,mid)
            certify(mid+1,right)
        else:
            groups.append((left,right,row))
    start=1
    while start<=8192:
        end=min(8192,start+start//64)
        certify(start,end)
        start=end+1
    assert sum(v-u+1 for u,v,_ in groups)==8192
    lower=min(float(y.lo) for _,_,y in groups)
    normalized=lower/(float(a.hi)*float(b.hi))
    print("true -DR at A, B:",heat.interval.bounds(a),heat.interval.bounds(b))
    print("number of certified groups",len(groups),"uniform lower bound",lower,
          "normalized lower bound",normalized)
    assert lower>.00009472 and normalized>.02204
    for n in (1,424,425,8192):
        row,_=heat.across_depths(s,local,n,n)
        print(n,heat.interval.bounds(row))


if __name__=="__main__":
    main()
