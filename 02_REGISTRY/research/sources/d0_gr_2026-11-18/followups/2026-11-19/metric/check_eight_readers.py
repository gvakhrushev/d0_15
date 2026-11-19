"""Exact interpolation of the primary SC1 polynomial and finite Golden grouping."""
from fractions import Fraction as F
from math import comb,lcm
import json

from check_boundary_experiment import Golden as G
from check_shared_site_union import sci


def inv(x):
    # p and -1-p are conjugates; norm of a+b p is a²-ab-b².
    norm=x.a*x.a-x.a*x.b-x.b*x.b
    return G(F(x.a-x.b,norm),F(-x.b,norm))


def main():
    O,I,D,H=G(0),G(1),G(2),G(4)
    p,z=G(0,1),G(F(1,2**20))
    def report(x,y):
        E=p**2*(I+x)
        L=H*E*(I-E)
        u=p+p**2*y
        B=H*u**2*(I-u**2)
        A=L+(I-L)*B
        return z*(A+B)-z**2*A*B
    L0=B0=H*p**3
    rf=H*p**2*(I-D*p**2)*z*(I-z*B0)*(I-B0)
    ry=G(8)*p**3*(I-D*p**2)*(z*(D-L0)-z**2*(L0+D*(I-L0)*B0))
    k=ry*inv(rf)
    assert k*rf==ry
    slope=inv(D*k)
    h=G(F(1,256))
    ready=G(2*10946)*p**23
    cos2=I-D*p**2
    for _ in range(9):
        cos2=D*cos2**2-I
    vis=(I-cos2)*G(F(1,2))*p**7
    base=p**2+H*p**3*vis
    factor=p**3*vis*ready**2
    gain=D*slope*factor*rf*ry
    weights=[F((-1)**(j-1)*comb(8,j),j*j) for j in range(1,9)]
    common=lcm(*(w.denominator for w in weights))
    allocation=[int(abs(w)*common) for w in weights]
    assert all(sum((-1)**(j-1)*comb(8,j)*j**n for j in range(1,9))==(n==0)
               for n in range(8))
    def mark(e,parts):
        d=slope*e
        dy=report(O,d)-report(O,O-d)
        dx=report(k*d,O)-report(O-k*d,O)
        value=O
        for volume,rho,f,m in parts:
            u=e*inv(rho)
            value+=volume*rho*(dy*(report(u*f,O)-report(O,O))+
                               dx*(report(O,O-u*m)-report(O,O)))
        return base+factor*value

    hit=[1,1]
    for _ in range(2,37):
        hit.append(hit[-1]+hit[-2])
    count=sum(allocation)
    assert hit[36]==24157817 and hit[35]==14930352 and count==20316969
    assert G(hit[36])*p**36+G(hit[35])*p**37==I
    neg=sum(n for w,n in zip(weights,allocation) if w<0)
    offset=p**36*(G(neg)+G(common*sum(weights))*base)
    physical_gain=p**36*G(common)*h**2*gain
    datasets=[
        [(I,p,G(F(2,9)),G(F(1,7))),(I,p**2,G(F(3,11)),G(F(-1,8)))],
        [(I,p,G(F(3,11)),G(F(-1,8))),(I,p**2,G(F(2,9)),G(F(1,7)))],
        [(G(F(1,2)),G(F(4,3)),G(F(-1,7)),G(F(2,9))),
         (G(F(1,3)),I,G(F(1,8)),G(F(1,12)))],
        [(I,I,O,O)]]
    readings=[]
    for parts in datasets:
        assert sum((v*rho for v,rho,_,_ in parts),O)==I
        target=sum((v*(f-k*m) for v,_,f,m in parts),O)
        qs=[mark(G(j)*h,parts) for j in range(1,9)]
        lifted=sum((G(w)*(q-base) for w,q in zip(weights,qs)),O)
        assert lifted==h**2*gain*target
        actual=p**36*sum((G(n)*(q if w>0 else I-q)
                            for w,n,q in zip(weights,allocation,qs)),O)
        assert actual==offset+physical_gain*target
        readings.append(actual)
    assert readings[0]==readings[1]
    print(json.dumps({"status":"PASS","source":"SC1, SC4, SC7, NPS10",
         "positive_attenuations":8,"max_degree_after_division":7,
         "Golden_price_cut":36,"selector_total_exact_level":hit[-1],
         "selector_participating_paths":count,"allocations":allocation,
         "selector_active_Born_mass":sci(G(count)*p**36),
         "raw_positive_mark_gain_SC2":sci(physical_gain),
         "exact_full_matter_geometry_cases":len(datasets),
         "true_full_price_bound":False,"large_native_words_replayed":False},
         sort_keys=True,indent=2))


if __name__=='__main__':
    main()
