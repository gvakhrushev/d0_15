"""Exact finite linear algebra for the H.1 physical volume quotient."""
from fractions import Fraction as F
import json


def dot(a,b):
    return sum(x*y for x,y in zip(a,b))


def rational_sqrt(x):
    from math import isqrt
    n,d=isqrt(x.numerator),isqrt(x.denominator)
    assert n*n==x.numerator and d*d==x.denominator
    return F(n,d)


def run():
    volumes=list(map(F,[4,9,7,5]))
    n=len(volumes)
    total=sum(volumes)
    # Per site: fifteen unrestricted coframe shape slots, 24 link and 2 matter,
    # followed by one physical cell-volume slot.
    size=42*n
    radial=[F(0)]*size
    dv=[F(0)]*size
    for i,v in enumerate(volumes):
        radial[42*i+41]=v/total
        dv[42*i+41]=F(1)
    assert dot(radial,dv)==1
    probes=[]
    for i in range(size):
        if i%42!=41:
            u=[F(0)]*size
            u[i]=1
            probes.append(u)
    for i in range(1,n):
        u=[F(0)]*size
        u[42*i+41],u[42*(i-1)+41]=1,-1
        probes.append(u)
    assert len(probes)==size-1 and all(dot(dv,u)==0 for u in probes)
    # Reconstruct arbitrary zero-volume vector from shape vectors and tree exchanges.
    vector=[F(i%11-5,7) for i in range(size)]
    vector[-1]-=dot(vector,dv)
    coeff=[x for i,x in enumerate(vector) if i%42!=41]
    coeff += [sum(vector[j*42+41] for j in range(i,n)) for i in range(1,n)]
    assert [sum(c*u[j] for c,u in zip(coeff,probes)) for j in range(size)]==vector

    local=[F(2), F(-5), F(13), F(11)]
    source=[F((7*i+3)%19-9,13) for i in range(size)]
    for i,v in enumerate(volumes):
        source[i*42+41]=local[i]/(2*v)
    chi=sum(local)/(2*total)
    assert dot(source,radial)==chi
    # Each true matched-volume transfer changes its coefficient by exactly this amount.
    probes_tail=probes[-(n-1):]
    for i,u in enumerate(probes_tail,1):
        assert dot(source,u)==local[i]/(2*volumes[i])-local[i-1]/(2*volumes[i-1])
    t=F(5)
    after=volumes[:]
    after[0]+=t
    after[1]-=t
    assert sum(after)==total
    gained=local[0]*(rational_sqrt(after[0]/volumes[0])-1)
    gained+=local[1]*(rational_sqrt(after[1]/volumes[1])-1)
    assert gained==F(8,3)
    K=lambda v:v*v+3*v+4
    assert K(sum(after))-K(total)==0
    assert (after[0]**2-volumes[0]**2)!=0  # local reference is visible

    # Wrong cosmological term passes all restricted tests, and is read from the scalar.
    shift=F(7,5)
    shifted=[shift*a for a in dv]
    L=[2*shift*v for v in volumes]
    assert all(dot(shifted,u)==0 for u in probes)
    assert sum(L)/(2*total)==shift!=0
    assert all(x==0 for x in [a-sum(L)/(2*total)*b for a,b in zip(shifted,dv)])
    # Scalar SC7 ideal affine calibration with exact nonzero offsets and Taylor/reading error.
    # Coefficients here exercise the bound; they do not simulate the geometric bank.
    qbase,gain,error=F(2,5),F(1,2000),F(1,100000)
    qhat=qbase+gain*sum(L)-error
    assert abs(shift-(qhat-qbase)/(2*gain*total))==error/(2*gain*total)
    return {"status":"PASS","cells":n,"dimensions":size,"independent_zero_volume_tests":len(probes),
            "free_volume":str(total),"marked_trace_multiplier_control":str(shift),
            "mark_error_in_multiplier":str(error/(2*gain*total)),
            "finite_transfer_target_change":str(gained),"physical_C_selected":False,
            "scope":"exact homogeneity, tree basis, projection, finite nonzero cosmological control and error transport; no geometric H.1 execution replay"}


if __name__=="__main__":
    print(json.dumps(run(),sort_keys=True,indent=2))
