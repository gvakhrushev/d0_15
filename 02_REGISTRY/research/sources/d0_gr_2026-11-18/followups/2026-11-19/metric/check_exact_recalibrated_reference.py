"""Exact k=89 Golden CAR loader and recalibrated 24-price reference."""
from fractions import Fraction
from math import comb
import json
import math
import mpmath as mp
import numpy as np
import sympy as sp
from sympy.polys.matrices import DomainMatrix

import check_dyadic_car_loader as old
from check_source_price import load_control, need


def main():
    ne,digest=load_control()
    mp.mp.dps=300
    p=(mp.sqrt(5)-1)/2; a=mp.sqrt(p); theta=mp.asin(p)
    cos=mp.cos(712*theta); sin=mp.sin(712*theta)
    amp=p*sin; filler=-p*cos
    need(amp>0 and filler>0, 'no additional sign-correcting CZ')
    need(abs(a*a+amp*amp+filler*filler-1)<mp.mpf('1e-290'),
         'exact reference state is normalized')

    # The native G^712 is an exact algebraic-field matrix. Evaluation needs
    # substantial guard precision because the exact coefficients are large.
    g=DomainMatrix.from_Matrix(ne.G_LOCAL).convert_to(ne.GOLDEN_FIELD)
    power=g**712
    need(power.transpose().matmul(power)==DomainMatrix.eye((2,2),ne.GOLDEN_FIELD),
         'exact full-column Golden power')
    evaluated=power.to_Matrix().evalf(260)
    cex=mp.mpf(str(evaluated[0,0])); sex=mp.mpf(str(evaluated[1,0]))
    need(abs(cex-cos)<mp.mpf('1e-60') and abs(sex-sin)<mp.mpf('1e-60'),
         'exact algebraic 712-power and independent high-precision trigonometry')

    # Every address/control column follows the previously certified Gray
    # identity; the selected angle is exactly 8*89*theta, not an approximation.
    old.gray_checks(3)
    old.gray_checks(4)
    old.verify_routed_rotations()
    old.verify_exact_site_phases()
    for u,v in ((14,6),(6,2),(0,1),(1,3),(3,7)):
        old.verify_adjacent_swap(u,v)
    pp=float(p); aa=float(a)
    gg=np.array([[aa,-pp],[pp,aa]])
    xx=np.array([[0.,1.],[1.,0.]])
    W=old.mat_one(0,gg)
    for bit in (1,2,3):W=old.mm(old.mat_one(bit,xx),W)
    for bit in (1,2,3):W=old.mm(old.mat_cx(0,bit),W)
    base=old.mm(old.rotation(14,0,-float(712*theta)),W)
    pairs=((1.,0.),(0.,1.),(-1.,0.),(0.,-1.))
    errors=[]
    for n,(cn,sn) in enumerate(pairs):
        U=old.mm(old.rotation(0,15,n*math.pi/2),base)
        expected=np.zeros(16);expected[1]=aa;expected[14]=float(filler)
        expected[0]=float(amp)*cn;expected[15]=float(amp)*sn
        errors.append(float(np.linalg.norm(U[:,1]-expected)))
        need(np.linalg.norm(old.mm(U.T,U)-np.eye(16))<1e-12, 'all 16 CAR columns')
    need(max(errors)<1e-12,'correct exact L=4 site vectors')

    z=mp.mpf(1)/2**20
    def report(x,y):
        E=p*p*(1+x); L=4*E*(1-E); u=p+p*p*y
        B=4*u*u*(1-u*u); A=L+(1-L)*B
        return z*(A+B)-z*z*A*B
    rf=mp.diff(lambda x:report(x,0),0)
    rq=mp.diff(lambda y:report(0,y),0)
    k0=rq/rf
    F=mp.mpf(16517734400)/162621047169
    H=mp.mpf(1)/4
    ideal_amp=H*mp.sqrt(F/k0)/(2*mp.sin(mp.pi*H))
    ratio=(amp/ideal_amp)**2
    bref=F/(16*k0)
    epsilon=mp.mpf(1)/4096
    h=epsilon/8
    dg=epsilon*bref
    dm=dg*ratio
    dy=report(0,dm)-report(0,-dm)
    dx=report(k0*dg,0)-report(-k0*dg,0)
    scale=dy/dx
    need(abs(dx-2*dg*rq)<mp.mpf('1e-280'), 'geometric denominator stays original')
    need(0<scale<1, 'finite L=4 matter contraction')

    weights=[Fraction((-1)**(j-1)*comb(8,j),j) for j in range(1,9)]
    for degree in range(1,9):
        need(sum(weights[j-1]*j**degree for j in range(1,9))==(1 if degree==1 else 0),
             'eight-point exact interpolation identity')
    mu=[mp.mpf('0.4'),mp.mpf('0.6')]
    ff=[mp.mpf('0.03'),mp.mpf('-0.02')]
    mm=[mp.mpf('0.01'),mp.mpf('0.025')]
    r0=report(0,0)
    values=[]
    for j in range(1,9):
        t=j*h
        values.append(sum(w*(dy*(report(t*x,0)-r0)+dx*(report(0,-scale*t*y)-r0))
                          for w,x,y in zip(mu,ff,mm)))
    lhs=sum(mp.mpf(w.numerator)/w.denominator*v for w,v in zip(weights,values))
    rhs=h*dy*rf*sum(w*(x-k0*y) for w,x,y in zip(mu,ff,mm))
    need(abs(lhs-rhs)<mp.mpf('1e-260'), 'unequal exact reference interpolation')
    b2=1-p**(6*64); b3=1-(1-16*p**9)**64
    selector_ready=(1-p**40)*(b2**6*b3)**1452
    visibility=p**7*mp.sin(512*theta)**2
    gain=selector_ready*p**24*840*h*p**3*visibility*rf*dy
    b0=1-(1-2*p**3)**16; b2load=1-(1-4*p**3)**32
    b3load=1-(1-16*p**9)**32
    loader_ready=b0**86*(b2load**4*b3load)**43*b3load**3

    # Directed intervals for signs, common finite reference and a coarse
    # uniform-in-H coefficient bound. Geometry, alpha and phases remain open.
    iv=mp.iv;iv.dps=70
    ip=(iv.sqrt(5)-1)/2;ia=iv.sqrt(ip);it=iv.atan2(ip,ia)
    iamp=ip*iv.sin(712*it);ifiller=-ip*iv.cos(712*it)
    need(iamp.a>iv.mpf('0.01113313') and iamp.b<iv.mpf('0.01113314'), 'positive exact amplitude interval')
    need(ifiller.a>iv.mpf('0.61793') and ifiller.b<iv.mpf('0.61794'), 'positive exact filler interval')
    ir=iv.mpf(4)*iv.pi**2*iamp**2*24*1601/160
    delta_max=iv.mpf(4)*iv.pi**2*iamp**2/4096
    need(ir.b<iv.mpf('1.176') and delta_max.b<iv.mpf('0.0000013'),
         'uniform H amplitude ratio and material perturbation bounds')
    iz=iv.mpf(1)/2**20; L0=4*ip**2*(1-ip**2)
    iy=iv.mpf(['-0.0000013','0.0000013']); iu=ip+ip**2*iy
    B=4*iu**2*(1-iu**2); dB=8*ip**2*iu*(1-2*iu**2)
    derivative=(iz*(2-L0)-iz**2*(L0+2*(1-L0)*B))*dB
    B0=4*ip**2*(1-ip**2); dB0=8*ip**3*(1-2*ip**2)
    reference=(iz*(2-L0)-iz**2*(L0+2*(1-L0)*B0))*dB0
    derivative_ratio=derivative/reference
    need(derivative_ratio.a>iv.mpf('0.999993') and derivative_ratio.b<iv.mpf('1.000007'),
         'uniform material finite-difference derivative bounds')
    need(ir.b*derivative_ratio.b<iv.mpf('1.177'), 'uniform current-field scale bound')

    # The algebraic obstruction uses only exact rational norm identities.
    root2,root5=sp.sqrt(2),sp.sqrt(5)
    ss=2+root2; ps=(root5-1)/2; ps_conj=(-root5-1)/2
    need(sp.simplify(ss*(2-root2))==2, 'norm of 2+sqrt2 is nonsquare rational')
    need(sp.simplify((ss/5)*((2-root2)/5))==sp.Rational(2,25),
         'norm after possible sqrt5 division is nonsquare rational')
    need(sp.simplify(ps*ps_conj)==-1, 'golden p has negative quadratic norm')
    print(json.dumps({
       'status':'PASS','native_source_sha256':digest,
       'L':4,'gray_exponent_k':89,'gray_G_calls':712,
       'G_calls_outside_factories_including_prep':719,
       'CX_calls_outside_factories_including_prep':71,
       'Toffoli_calls':43,'CCZ_calls':3,'direct_CZ_calls':0,
       'exact_G_power_verified':True,'exact_full_column_sites':4,
       'max_fresh_car_vector_error':max(errors),
       'material_amplitude':mp.nstr(amp,24),'positive_filler':mp.nstr(filler,24),
       'amplitude_squared':mp.nstr(amp*amp,24),
       'common_material_to_geometric_ratio':mp.nstr(ratio,24),
       'geometric_delta':mp.nstr(dg,24),'material_delta':mp.nstr(dm,24),
       'current_matter_scale':mp.nstr(scale,24),
       'current_matter_amplitude_scale':mp.nstr(mp.sqrt(scale),24),
       'selector24_gain_per_actual_alpha_squared':mp.nstr(gain,24),
       'loader_success_probability_conditional_on_factory_interface':mp.nstr(loader_ready,24),
       'coefficient_bound_if_exact_phase_H_family':1.177,
       'amplitude_scale_bound_if_exact_phase_H_family':1.085,
       'uniform_native_site_phase_realized':False,
       'L16_exact_common_success_phase_in_allowed_field':False,
       'actual_full_bank_alpha_known':False,'current_loader_compiled':False,
       'full_book_cost_info_identified':False,'GR_closed':False,
    },sort_keys=True,indent=2))


if __name__=='__main__':
    main()
