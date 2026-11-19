"""Exact check of geometric reference, two attenuations and compensated field maps."""
from fractions import Fraction as F
from math import comb,lcm
import json

from check_boundary_experiment import Golden as G
from check_shared_site_union import sci
from check_eight_readers import inv


def main():
    zero,one,two,four=map(G,(0,1,2,4))
    p=G(0,1)
    z=G(F(1,2**20))
    def r(x,y):
        e=p**2*(one+x)
        l=four*e*(one-e)
        u=p+p**2*y
        b=four*u**2*(one-u**2)
        a=l+(one-l)*b
        return z*(a+b)-z**2*a*b
    l0=b0=four*p**3
    rf=four*p**2*(one-two*p**2)*z*(one-z*b0)*(one-b0)
    rq=G(8)*p**3*(one-two*p**2)*(z*(two-l0)-z**2*(l0+two*(one-l0)*b0))
    k=rq*inv(rf)
    mesh=F(1,4); s_ref=F(4)
    t,v=mesh/2,mesh/20
    ca,sa=(1+t*t)/(1-t*t),2*t/(1-t*t)
    cb,sb=(1-v*v)/(1+v*v),2*v/(1+v*v)
    F_grid=sa*sb*(2+(ca-1)*(1-cb))/(2*mesh**2)
    assert 0<F_grid<F(1,8)<s_ref**2/2
    b_ref=G(F_grid/s_ref**2)*inv(k)
    assert b_ref*k*G(s_ref**2)==G(F_grid)
    # Numerical fixture only; full generator norm for an actual chart is not measured.
    physical_eps=G(F(1,4096))
    h=physical_eps*G(F(1,8))
    delta=physical_eps*b_ref
    dy=r(zero,delta)-r(zero,zero-delta)
    dx=r(k*delta,zero)-r(zero-k*delta,zero)
    assert dx==two*delta*rq
    lam=dy*inv(dx)
    assert lam*rq*dx==dy*rf*k
    assert lam!=one
    f,m=G(F(13,17)),G(F(2,9))
    target=f-k*m
    def mark(e,d,x,y):
        return ((r(zero,d)-r(zero,zero-d))*(r(e*x,zero)-r(zero,zero))+
                (r(k*d,zero)-r(zero-k*d,zero))*(r(zero,zero-e*y)-r(zero,zero)))
    field=zero
    published=zero
    wrong=zero
    independent_d=G(F(1,2048))
    independent_steps=zero
    for j in range(1,9):
        J=G(j)
        signed=(-1)**(j-1)*comb(8,j)
        tau=J*G(F(1,8))
        actual=mark(physical_eps,delta,tau*f,tau*lam*m)
        assert actual==mark(J*h,delta,f,lam*m)
        field+=G(F(signed,j))*actual
        wrong+=G(F(signed,j))*mark(physical_eps,delta,tau*f,tau*m)
        published+=G(F(signed,j*j))*mark(J*h,J*h*b_ref,f,m)
        independent_steps+=G(F(signed,j*j))*mark(J*h,J*independent_d,f,m)
    assert field==h*dy*rf*target
    assert published==two*b_ref*h**2*rf*rq*target
    assert independent_steps==two*independent_d*h*rf*rq*target
    assert wrong!=field
    weights=[F((-1)**(j-1)*comb(8,j),j) for j in range(1,9)]
    common=lcm(*(w.denominator for w in weights))
    sizes=[int(common*abs(w)) for w in weights]
    counts=[1,1]
    while counts[-1]<sum(sizes):
        counts.append(counts[-1]+counts[-2])
    price=len(counts)-1
    assert common==840 and sum(sizes)==63253 and price==24
    assert G(counts[-1])*p**price+G(counts[-2])*p**(price+1)==one
    print(json.dumps({"status":"PASS","reference_mesh":"1/4","s_ref":"4",
        "F_grid":str(F_grid),"b_geometric":sci(b_ref),"published_scalar_b":sci(inv(two*k)),
        "delta_for_material_map":sci(delta),"lambda_minus_one":sci(lam-one),
        "legal_input_formulas_checked":"original source moment identities; full hardware norm not computed",
        "two_exact_interpolations":"two-step linear reference and unchanged reference with field map",
        "uncorrected_material_coefficient_rejected":True,
        "fixed_reference_selector":{"price_cut":price,"word_count":sum(sizes),
        "bins":sizes,"active_Born_mass":sci(G(sum(sizes))*p**price)},
        "physical_ledger_identified":False,"full_clock_replayed":False},
        indent=2,sort_keys=True))


if __name__=='__main__':
    main()
