#!/usr/bin/env python3
"""Exact CAR/Einstein/source identities for the finite causal response proof.
No numeric root search, source fit, native admission or general-GR claim.
"""
from itertools import product
import json
import sympy as s
checks=[]
def eq(name,a,b=0):
    good=all(s.simplify(x)==0 for x in s.Matrix(a)-s.Matrix(b)) if isinstance(a,s.MatrixBase) or isinstance(b,s.MatrixBase) else s.simplify(a-b)==0
    if not good:raise ArithmeticError(name)
    checks.append(name)
def require(name,truth):
    if not truth:raise ArithmeticError(name)
    checks.append(name)
def creators():
    cc=[]
    for r in range(4):
        c=s.zeros(16)
        for mask in range(16):
            if not mask&(1<<r):c[mask|(1<<r),mask]=(-1)**((mask&((1<<r)-1)).bit_count())
        cc.append(c)
    return cc

def main():
    checks.clear();C=creators();eta=s.diag(1,-1,-1,-1)
    gam=[c-c.T for c in C]
    for i in range(4):
        for j in range(4):
            eq('CAR_%d%d'%(i,j),C[i]*C[j].T+C[j].T*C[i],s.eye(16) if i==j else s.zeros(16))
    q=s.symbols('q',positive=True);ks=s.symbols('p0:4',real=True)
    # Direct linearized LC from the actual Lorentz cone metric germ.
    wave=s.Matrix([0,q,q,0]);hh=s.zeros(4)
    hh[0,1]=hh[1,0]=hh[0,2]=hh[2,0]=2
    lift=lambda A:sum((A[i,j]*C[i]*C[j].T for i,j in product(range(4),repeat=2)),s.zeros(16))
    MM=[]
    for r in range(4):
        G=s.Matrix(4,4,lambda a,b:sum(eta[a,d]*(wave[r]*hh[d,b]+wave[b]*hh[d,r]-wave[d]*hh[r,b]) for d in range(4))/2)
        MM.append(lift(-G.T))
    A= -2*q*(C[1]+C[2])*C[0].T
    eq('actual_LC_time_component',MM[0],s.zeros(16))
    eq('actual_LC_first_spatial_component',MM[1],A)
    eq('actual_LC_second_spatial_component',MM[2],A)
    eq('actual_LC_fourth_component',MM[3],s.zeros(16))
    eq('first_torsionfree_contraction',sum((C[r]*MM[r] for r in range(4)),s.zeros(16)),s.zeros(16))
    eq('ordered_first_connection_products_nilpotent',A*A,s.zeros(16))
    # Full all-slot Einstein first variation; no restricted scalar oracle.
    raised=eta*hh
    Ric=s.Matrix(4,4,lambda i,j:(-sum(wave[a]*wave[i]*raised[a,j]+wave[a]*wave[j]*raised[a,i] for a in range(4))+(wave.T*eta*wave)[0]*hh[i,j]+wave[i]*wave[j]*s.trace(raised))/2)
    Ein=Ric-eta*s.trace(eta*Ric)/2
    eq('all_ten_Einstein_rows_vanish',Ein,s.zeros(4))
    u=s.symbols('u',real=True)
    a=s.Matrix([(1-2*u*u)/(1+2*u*u),2*u/(1+2*u*u),2*u/(1+2*u*u),0])
    gg=2*a*a.T-s.eye(4)
    eq('cone_normalized_exactly',(a.T*a)[0],1)
    eq('cone_volume_exactly_constant',s.factor(gg.det()),-1)
    # Exact all16 first-jet norm and the full squared-operator susceptibility.
    B=C[1]*C[2]*C[0].T
    eq('full_CAR_monomial_norm',s.trace(B.T*B),2)
    eq('CAR_monomial_nilpotent',B*B,s.zeros(16))
    e1=q*(ks[1]-ks[2])*(B-B.T)
    eq('actual_reverse_block_adjoint',e1.T,-e1)
    d0=s.I*sum((ks[r]*gam[r] for r in range(4)),s.zeros(16))
    dtarget=d0+s.I*q*(gam[1]+gam[2])
    delta1=dtarget*e1+e1*d0
    normE=4*q*q*(ks[1]-ks[2])**2
    Uk=ks[0]**2+ks[1]**2+ks[2]**2+q*(ks[1]+ks[2])+q*q
    eq('exact_full16_E1_norm',s.trace(e1.T*e1),normE)
    eq('exact_full16_Delta1_norm',s.trace(delta1.conjugate().T*delta1),2*Uk*normE)
    eq('no_scalar_vacuum_price_added',B*s.eye(16)[:,0],s.zeros(16,1))
    eq('no_backward_scalar_vacuum_price_added',B.T*s.eye(16)[:,0],s.zeros(16,1))
    # Exact divided-difference Hessian of the full finite logZ+logdet price.
    t=s.symbols('t',real=True);al=s.Rational(1,20);m=4;be=m*al;z=s.Rational(1,9);multi=2
    eig=[2-s.sqrt(1+t*t),2+s.sqrt(1+t*t)]
    KK=[(1-al*l)**m for l in eig];Z=s.simplify(sum(KK));FF=[1-z+z*k for k in KK]
    price=s.log(Z)/be-multi*s.log(s.simplify(FF[0]*FF[1]))
    actual=s.diff(price,t,2).subs(t,0)
    Z0=Z.subs(t,0)
    kap=lambda l:-(1-al*l)**(m-1)/Z0+multi*z*be*(1-al*l)**(m-1)/(1-z+z*(1-al*l)**m)
    eq('actual_complete_price_divided_difference',actual,kap(3)-kap(1))
    require('susceptibility_is_not_discardable',actual!=0)
    # Exact full-feedback sign identity, neither F nor the normalizer frozen.
    Ek,El,zz=s.symbols('Ek El zz',positive=True);Fk=1-zz+zz*Ek;Fl=1-zz+zz*El
    eq('full_feedback_difference_identity',Ek/Fk-El/Fl,(1-zz)*(Ek-El)/(Fk*Fl))
    n0,n1,n2=s.symbols('n0 n1 n2',integer=True)
    U=n0*n0+n1*n1+n2*n2+n1+n2+1;V=n1+n2+1;D=n1-n2
    eq('integer_gap_identity',U,(V*V+D*D+1)/2+n0*n0)
    upper=16*(1+s.Rational(2,7)/(1-s.Rational(1,343)))**4
    require('rigorous_partition_upper_bound',upper<50)
    require('fixed_v8_feedback_margin',s.Rational(128*50,2**20-1)<s.Rational(1,4))
    require('golden_beta_between_three_quarters_and_one',s.Rational(3,4)<2*((s.sqrt(5)-1)/2)**2<1)
    require('rational_tanh_lower_mechanism',s.Rational(3,2)*s.Rational(48,50)>s.Rational(4,3))
    # Standard Gaussian moment identity used only in the optional local symbol.
    x=s.symbols('x',positive=True);t=s.symbols('t',real=True)
    f=s.exp(-2*x*t*(1-t))
    eq('proper_Gaussian_integral_boundary_identity',s.diff((2*t-1)*f,t),(2+2*x*(2*t-1)**2)*f)
    return {'schema':'d0-finite-causal-exact/1','exact_group_count':len(checks),'checks':checks,
            'SOURCE':'a4f4d4e86ae63336841337e1a93cd5296eb43792',
            'proved':'specific full finite proper-link second jet and its positive h^-2 limit; pure longitudinal Einstein first jet zero',
            'general_C1_h2_remainder_proved':False,'fixed_source_exact_root_terminal_closed':False,
            'native_physical_price_admitted':False,'GR_closed':False}
if __name__=='__main__':print(json.dumps(main(),sort_keys=True,indent=2))
