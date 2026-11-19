#!/usr/bin/env python3
"""Original D0 primary null family: curvature-source protection + Green filters.

Known pp-wave tensor-reduction theorem is CONSUMED, not proved by tests.
Checks its exact D0 inputs, the unchanged finite stencil, and a class of
positive-resolvent corrections. No native Book metric descent, full price,
connection/internal stationarity, minimum, or generic GR is claimed.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from functools import lru_cache
import sympy as s
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import splu, expm_multiply

PIN='c49ebdb12244943d1ec45ef6d148a0432481141e'

def require(test, name):
    if not bool(test):
        raise AssertionError(name)


def exact_geometry():
    u,v,x,y=s.symbols('u v x y', real=True)
    q=(u,v,x,y)
    H=s.Function('H')(u,x,y)
    g=s.Matrix([[H,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]])
    gi=g.inv()
    @lru_cache(None)
    def G(a,b,c):
        return s.simplify(sum(gi[a,d]*(s.diff(g[d,b],q[c])+s.diff(g[d,c],q[b])-s.diff(g[b,c],q[d])) for d in range(4))/2)
    @lru_cache(None)
    def R(a,b,c,d):
        return s.simplify(s.diff(G(a,d,b),q[c])-s.diff(G(a,c,b),q[d])+
          sum(G(a,c,e)*G(e,d,b)-G(a,d,e)*G(e,c,b) for e in range(4)))
    Ric=s.Matrix(4,4,lambda a,b:s.simplify(sum(R(c,a,c,b) for c in range(4))))
    expected=s.zeros(4); expected[0,0]=(s.diff(H,x,2)+s.diff(H,y,2))/2
    require(Ric==expected, 'actual +--- null Ricci convention')
    scalar=s.simplify(sum(gi[a,b]*Ric[a,b] for a in range(4) for b in range(4)))
    require(scalar==0, 'Ricci scalar zero is not assumed sufficient')
    require(all(G(0,a,b)==0 for a in range(4) for b in range(4)), 'du covariantly constant')
    f=s.Function('f')(u,x,y)
    boxf=s.simplify(sum(gi[a,b]*(s.diff(f,q[a],q[b])-sum(G(c,a,b)*s.diff(f,q[c]) for c in range(4))) for a in range(4) for b in range(4)))
    require(s.expand(boxf+s.diff(f,x,2)+s.diff(f,y,2))==0, 'box on v independent scalar is minus transverse Laplacian')
    # Since du is parallel, box(f du du)=(box f) du du exactly.
    lap=lambda z:s.diff(z,x,2)+s.diff(z,y,2)
    boxRic=-(lap(lap(H)))/2
    lam=s.symbols('lambda',nonzero=True,real=True)
    amp=s.Function('j')(u)
    A2,B2,A3,B3=[s.Function(z)(u) for z in ('A2','B2','A3','B3')]
    W=A2*(x*x-y*y)+2*B2*x*y+A3*(x**3-3*x*y*y)+B3*(3*x*x*y-y**3)
    primary=-lam*amp*(x*x+y*y)+W
    require(s.expand(lap(primary)+4*lam*amp)==0, 'original primary nonvacuum Einstein source')
    require(s.expand(lap(lap(primary)))==0, 'box Ricci zero on WHOLE primary polynomial family')
    # Null source/matter conservation and wave equation, with arbitrary time profile.
    psi=s.Function('Psi')(u)
    wave=s.simplify(sum(gi[a,b]*(s.diff(psi,q[a],q[b])-sum(G(c,a,b)*s.diff(psi,q[c]) for c in range(4))) for a in range(4) for b in range(4)))
    require(wave==0, 'unchanged null material wave equation')
    # Covariant divergence of f(u,x,y) du du is identically zero for v-independent f.
    T=s.zeros(4);T[0,0]=f
    div=[]
    for b in range(4):
        val=0
        for a in range(4):
            for c in range(4):
                val+=gi[a,c]*(s.diff(T[a,b],q[c])-sum(G(d,c,a)*T[d,b]+G(d,c,b)*T[a,d] for d in range(4)))
        div.append(s.simplify(val))
    require(div==[0]*4, 'null normal-source divergence')
    # Tensor nonlinear contraction, distinct from scalar invariant.
    require(Ric*gi*Ric==s.zeros(4), 'Ricci squared rank-two source annihilates')
    # Hostile: VSI alone does NOT kill derivative field equations.
    hostile=s.simplify(boxRic.subs(H,x**4).doit())
    require(hostile==-12, 'VSI quartic nonharmonic correction is nonzero')
    # A scalar-dependent coefficient is excluded; it produces an extra null source.
    coupling=s.Function('F')(u)
    normal_nonminimal=-s.diff(coupling,u,2)
    require(normal_nonminimal!=0, 'nonminimal matter coefficient not silently absorbed')
    return {'ricci_uu':str(expected[0,0]),'box_Ricci_uu':str(boxRic),
            'primary_Ricci_uu':str(-2*lam*amp),'primary_box_Ricci':'0',
            'parallel_null_covector':True,'material_wave_equation':'0',
            'normal_source_divergence':list(map(str,div)),
            'VSI_alone_counterexample_box_Ricci_uu':str(hostile),
            'scalar_dependent_coupling_counterexample':str(normal_nonminimal)}


def exact_discrete():
    x,y,h,lam,j=s.symbols('x y h lambda j',real=True,nonzero=True)
    a,b,c,d=s.symbols('a b c d',real=True)
    H=-lam*j*(x*x+y*y)+a*(x*x-y*y)+2*b*x*y+c*(x**3-3*x*y*y)+d*(3*x*x*y-y**3)
    def lap(f):
        return s.expand((f.subs(x,x+h)+f.subs(x,x-h)+f.subs(y,y+h)+f.subs(y,y-h)-4*f)/h**2)
    ric=lap(H)/2
    require(ric==-2*lam*j,'same primary exact five-point Ricci')
    higher=-lap(ric)
    require(higher==0,'all powers annihilate by first exact zero')
    coeffs=s.symbols('b0:7')
    source=coeffs[0]*ric
    cur=ric
    for k in range(1,len(coeffs)):
        cur=-lap(cur);source+=coeffs[k]*cur
    require(s.expand(source-coeffs[0]*ric)==0,'arbitrary derivative coefficients on actual stencil')
    # General all orders follow by induction from L ric=0; finite test not proof.
    hostile=s.expand(-lap(lap(x**4))/2)
    require(hostile==-12,'same finite quartic hostile source')
    harmonic4=x**4-6*x*x*y*y+y**4
    require(lap(harmonic4)==4*h*h,'harmonic quartic is NOT exact same mesh solution')
    # Do NOT act with a homogeneous Dirichlet matrix on an extended constant source.
    D=s.Matrix([[2,-1,0],[-1,2,-1],[0,-1,2]])
    I=s.eye(3);L=16*(s.kronecker_product(D,I)+s.kronecker_product(I,D))
    ones=s.ones(9,1)
    require(L*ones!=s.zeros(9,1),'boundary-collar control: Dirichlet constant is not extended constant')
    A=s.eye(9)+s.Rational(7,3)*L
    B=s.eye(9)+s.Rational(100,1)*L
    inv_filter=A.inv()*B.inv()
    require(all(t>=0 for t in inv_filter),'exact positive resolvent filter')
    require(max(sum(inv_filter[i,k] for k in range(9)) for i in range(9))<=1,'exact filter contraction')
    full=L.inv()*inv_filter
    norm=max(sum(full[i,k] for k in range(9)) for i in range(9))
    require(norm<=s.Rational(1,8),'normal recovery constant survives large compatible corrections')
    # Same negative-sign filter has a resonance. Never claim ALL coefficients stable.
    singular=s.eye(9)-L/64
    require(singular.det()==0,'resonant negative filter must be excluded')
    return {'original_stencil_protection':'EXACT_FOR_ALL_h',
            'arbitrary_order_proof':'L_h Ric_h=0 implies L_h^k Ric_h=0 for k>=1, on complete stencil collars',
            'verified_symbolic_orders':6,'negative_quartic_boxRicci':str(hostile),
            'quartic_harmonic_finite_error':str(lap(harmonic4)),
            'Dirichlet_constant_boundary_control':True,
            'rational_large_filter_green_norm':str(norm),'uniform_bound':'1/8',
            'negative_filter_resonance':True}


def numerical_filters():
    out=[]
    for n_interval in (8,16,32):
        n=n_interval-1;h=1/n_interval
        D=sparse.diags([-np.ones(n-1),2*np.ones(n),-np.ones(n-1)],[-1,0,1],format='csc')/h**2
        I=sparse.eye(n,format='csc');L=sparse.kron(D,I,format='csc')+sparse.kron(I,D,format='csc')
        eye=sparse.eye(n*n,format='csc');lu=splu(L)
        ones=np.ones(n*n)
        base=float(lu.solve(ones).max())
        filters=[]
        for strengths in ((0.0,),(.3,),(.3,10.),(10.,100.)):
            v=ones.copy()
            for z in strengths:
                v=splu(eye+z*L).solve(v)
            ans=lu.solve(v)
            require(v.min()>-1e-12 and v.max()<=1+1e-12,'numerical positive contraction')
            require(ans.max()<=base+1e-12 and ans.max()<=.125+1e-12,'same mesh uniform norm bound')
            filters.append({'strengths':list(strengths),'green_norm_inf':float(ans.max())})
        # Heat-memory inverse, a representative Laplace-transform filter.
        heat=expm_multiply(-.02*L,ones)
        ans=lu.solve(heat)
        require(heat.min()>-1e-12 and heat.max()<=1+1e-12,'heat sub-Markov contraction')
        require(ans.max()<=.125+1e-12,'heat-filtered Green bound')
        out.append({'intervals':n_interval,'sites':n*n,'unfiltered_green_norm_inf':base,
                    'resolvent_filters':filters,'heat_filter_green_norm_inf':float(ans.max())})
    return out


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--json',type=Path);args=ap.parse_args()
    obj={'status':'PASS_PRIMARY_NULL_SOURCE_PROTECTION_AND_FILTERED_RECOVERY',
         'input_ref':PIN,'geometry':exact_geometry(),'discrete':exact_discrete(),
         'filter_checks':numerical_filters(),
         'scope':{'pp_wave_tensor_reduction':'CONSUMED_KNOWN_THEOREM_1407.5301_SECT_II',
                  'D0_primary_application':True,
                  'finite_filter_law_is_actual_Book_source':False,
                  'native_metric_only_covariant_descent_proved':False,
                  'independent_24_link_and_internal_Euler_elimination_proved':False,
                  'new_matter_law':False,'native_price_selection_proved':False,
                  'stationary_solution_is_minimum':False,'generic_GR_or_raw216_closed':False}}
    text=json.dumps(obj,ensure_ascii=False,indent=2)
    print(text)
    if args.json:args.json.write_text(text+'\n',encoding='utf-8')

if __name__=='__main__':main()
