"""Native SC1/SC7 and all 16 Fock sectors on a two-component SITE control."""
from decimal import Decimal, localcontext
from fractions import Fraction as F
from itertools import combinations, permutations
from math import prod
import json

from check_boundary_experiment import Golden as G


def eye(n):
    return [[F(i==j) for j in range(n)] for i in range(n)]


def transpose(a):
    return list(map(list,zip(*a)))


def matmul(a,b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]


def det(a):
    n=len(a)
    return sum((-1)**sum(i>j for h,i in enumerate(p) for j in p[h+1:])
               *prod(a[i][j] for i,j in enumerate(p)) for p in permutations(range(n)))


def exterior(matrix,rows,cols):
    return det([[matrix[i][j] for j in cols] for i in rows])


def dgamma(rows,cols,N):
    identity=eye(4)
    total=F(0)
    for j in cols:
        M=[r[:] for r in identity]
        for i in range(4):
            M[i][j]=N[i][j]
        total+=exterior(M,rows,cols)
    return total


def curvature(t):
    c=(1-t*t)/(1+t*t)
    s=2*t/(1+t*t)
    X,Y=eye(4),eye(4)
    X[2][2],X[2][3],X[3][2],X[3][3]=c,-s,s,c
    Y[1][1],Y[1][3],Y[3][1],Y[3][3]=c,s,-s,c
    P=matmul(matmul(Y,X),matmul(transpose(Y),transpose(X)))
    N=[[F(0)]*4 for _ in range(4)]
    N[1][2],N[2][1]=F(1),F(-1)
    trace=F(0)
    for grade in range(5):
        masks=list(combinations(range(4),grade))
        trace+=sum(dgamma(i,j,N)*exterior(P,j,i) for i in masks for j in masks)
    res=-trace/8
    formula=4*t*t*(1+2*t*t-t**4)/(1+t*t)**4
    assert res==formula
    return res


def sci(x):
    with localcontext() as ctx:
        fractions=[F(x.a),F(x.b)]
        ctx.prec=80+max(len(str(abs(v.numerator)))+len(str(v.denominator)) for v in fractions)
        a,b=[Decimal(v.numerator)/Decimal(v.denominator) for v in fractions]
        return format(a+b*(Decimal(5).sqrt()-1)/2,'.12E')


def main():
    zero,one,two,four=map(G,(0,1,2,4))
    p=G(0,1)
    phi=one+p
    tA,tB=p,p**2
    a_inv,b_inv=phi,phi**2
    assert tA*a_inv==tB*b_inv==one and b_inv-a_inv==one
    z,delta,eps=map(G,[F(1,2**20),F(1,1024),F(1,32)])
    def report(x,y):
        E=p**2*(one+x)
        L=four*E*(one-E)
        u=p+p**2*y
        B=four*u**2*(one-u**2)
        A=L+(one-L)*B
        return z*(A+B)-z**2*A*B
    cos2=one-two*p**2
    for _ in range(9):
        cos2=two*cos2**2-one
    vis=(one-cos2)*G(F(1,2))*p**7
    ready=G(2*10946)*p**23  # SC2 scalar reference only
    dy=report(zero,delta)-report(zero,zero-delta)
    B0=four*p**3
    rx=four*p**2*(one-two*p**2)*z*(one-z*B0)*(one-B0)
    gain=p**3*vis*ready**2*dy*rx
    assert Decimal(sci(gain))>0
    def F1(x):
        return p**3*vis*ready**2*dy*(report(x,zero)-report(zero,zero))
    for x in [F(-1,10),F(0),F(2,19)]:
        assert F1(G(x))==gain*G(x)*(one-phi*G(x))
    levels=[F(1,5),F(1,4)]
    f0,f1=map(curvature,levels)
    assert f1==F(18368,83521) and f1>f0>0
    for s in [F(0),F(1,9),F(2,7),F(-1,3)]:
        curvature(s)
    f0,f1=G(f0),G(f1)
    def union(fA,fB):
        return tA*F1(eps*fA*a_inv)+tB*F1(eps*fB*b_inv)
    swap=union(f1,f0)-union(f0,f1)
    assert swap==gain*phi*eps**2*(f1**2-f0**2)
    assert Decimal(sci(swap))>0
    # Equal-volume tangent, df_A=1, df_B=-1.
    tangent=gain*eps*((one-two*phi*eps*f1*a_inv)-(one-two*phi*eps*f1*b_inv))
    assert tangent==two*gain*phi*eps**2*f1
    # Genuine finite two-slot mark, applied to known (scalar READY) source.
    qbase=p**2+four*p**3*vis
    assert Decimal(sci(qbase+union(f1,f0)))<F(1,2)
    # All actual output references (7 slots) constant here except P_f,
    # so the omitted reference-x term vanishes exactly (P_q = P_0).
    print(json.dumps({
        "status":"PASS","source_head":"531f775e05b4295930fc1fadb77b1ffd97e76038",
        "Fock_dimension":16,"Fock_curvature_at_1_over_5":str(f0.a),
        "Fock_curvature_at_1_over_4":str(f1.a),
        "reporter_delta":"1/1024","field_attenuation":"1/32",
        "marked_swap_gap_SC2":sci(swap),"required_max_per_endpoint_error_SC2":sci(swap*G(F(1,2))),
        "derivative_along_dfA_plus1_dfB_minus1_SC2":sci(tangent),
        "derivative_divided_by_actual_first_amplitude":sci(two*phi*eps*f1),
        "geometric_ready_unknown":"same symbolic expression, with actual positive field-independent readiness",
        "complete_word_replayed":False,"true_economic_fixed_volume_transfer":False
    },indent=2,sort_keys=True))


if __name__=='__main__':
    main()
