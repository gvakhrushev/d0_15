#!/usr/bin/env python3
"""Native six-face Lorentz star: exact continuum-normalization seam and
two-field rank-two local finite 40-direction first-source control.

Scope: positive-oriented Cartesian +--- chart, homogeneous local interior
stencil, original sigma +/- coefficient options. NOT an exact finite root
or a compulsory native Book03 physical/clock/preparation selection.
"""
from itertools import combinations
import json
import numpy as np
import sympy as sp
from scipy.linalg import expm
from scipy.optimize import brentq
from scipy.special import erfi

ETA=np.diag([1.,-1.,-1.,-1.])
PAIRS=list(combinations(range(4),2))
G2=np.array([ETA[a,a]*ETA[b,b] for a,b in PAIRS])
STARMAP={(0,1):((2,3),-1),(0,2):((1,3),1),(0,3):((1,2),-1),
         (1,2):((0,3),1),(1,3):((0,2),-1),(2,3):((0,1),1)}
STAR=np.zeros((6,6))
for a,(b,sgn) in STARMAP.items():
    STAR[PAIRS.index(b),PAIRS.index(a)]=sgn
I=np.eye(4); LORENTZ=[]
for i in (1,2,3):
    X=np.zeros((4,4));X[0,i]=X[i,0]=1
    LORENTZ.append(X)
for i,j in ((1,2),(1,3),(2,3)):
    X=np.zeros((4,4));X[i,j]=1;X[j,i]=-1
    LORENTZ.append(X)

KAPPA=23.41640675188407497289558 # original finite z=2^-20, not fitted

def verify_exact():
    es=[sp.eye(4),
        sp.diag(sp.Rational(7,5),sp.Rational(9,4),
                sp.Rational(11,8),sp.Rational(13,9)),
        sp.Matrix([[2,sp.Rational(1,4),0,0],
                   [sp.Rational(1,3),3,sp.Rational(1,5),0],
                   [0,0,2,sp.Rational(1,7)],
                   [sp.Rational(1,8),0,0,2]])]
    eta=sp.diag(1,-1,-1,-1)
    st=sp.Matrix(STAR.astype(int).tolist())
    g2=sp.Matrix(np.diag(G2).astype(int).tolist())
    G=[]
    for i in (1,2,3):
        X=sp.zeros(4);X[0,i]=X[i,0]=1;G.append(X)
    for i,j in ((1,2),(1,3),(2,3)):
        X=sp.zeros(4);X[i,j]=1;X[j,i]=-1;G.append(X)
    for e in es:
        assert e.det()>0
        inv=e.inv()
        for r,s in PAIRS:
            u,v=[i for i in range(4) if i not in (r,s)]
            seq=[r,s,u,v]
            eps=(-1)**sum(seq[i]>seq[j] for i in range(4) for j in range(i+1,4))
            B=sp.Matrix([e[i,u]*e[j,v]-e[j,u]*e[i,v] for i,j in PAIRS])
            for X in G:
                T=X*eta
                b=sp.Matrix([T[i,j] for i,j in PAIRS])
                star=(eps*B.T*g2*st*b)[0]
                scalar=2*(inv[r,:]*T*inv[s,:].T)[0]*e.det()
                assert sp.factor(star+scalar/2)==0
    return 108

def time_to_radius(t):
    coeff=np.sqrt(np.pi/2.)
    return brentq(lambda r:coeff*
                  (erfi(r/np.sqrt(2))-erfi(1/np.sqrt(2)))-t,
                  .6,1.5,xtol=1e-14)

def cell(t,h,amplitude):
    r=time_to_radius(t)
    A=np.exp(-r*r/4)*np.sqrt(r)
    B=np.exp(r*r/4)/np.sqrt(r)
    e=np.diag([A,B,r,r]).astype(complex)
    spin=(0.,.5-.5/r**2,
          np.exp(-r*r/4)/np.sqrt(r),
          np.exp(-r*r/4)/np.sqrt(r))
    u=np.array([I if j==0 else expm(h*spin[j]*LORENTZ[j-1])
                for j in range(4)],dtype=complex)
    v=np.zeros((2,4),complex)
    # Literally retained forward-difference CAR history on each interior cell.
    v[0,0]=amplitude*r*np.exp(-r*r/2)
    v[1,1]=amplitude
    return dict(e=e,u=u,v=v,r=r)

def orientation(r,s):
    seq=[r,s]+[i for i in range(4) if i not in (r,s)]
    return (-1)**sum(seq[i]>seq[j] for i in range(4)
                     for j in range(i+1,4))

def star_density(curr,nxt,h):
    e,U,V=curr['e'],curr['u'],nxt['u']
    total=0j
    for r,s in PAIRS:
        P=U[r]@(V[s] if r==0 else U[s])@np.linalg.inv(U[r])@np.linalg.inv(U[s])
        F=(P-np.linalg.inv(P))/2
        T=F@ETA
        b=np.array([T[i,j] for i,j in PAIRS])
        u,v=[i for i in range(4) if i not in (r,s)]
        B=np.array([e[i,u]*e[j,v]-e[j,u]*e[i,v] for i,j in PAIRS])
        total+=orientation(r,s)*(B*G2)@(STAR@b)
    return total/h**2 # original h^-4 density with two h-scaled solder legs

def matter_query(c):
    ginv=np.linalg.inv(c['e'].T@ETA@c['e'])
    return sum(v@ginv@v for v in c['v'])

def native_first_source(h,sigma):
    # sigma-minus reproduces the prior continuum seed, with epsilon²=1/kappa.
    # sigma-plus is the ORIGINAL alternative, with epsilon²=1/(2kappa).
    amplitude=np.sqrt(1/(KAPPA if sigma==-1 else 2*KAPPA))
    slope=sigma*KAPPA
    prev,cur,nxt=[cell(t,h,amplitude) for t in (-h,0,h)]
    def action():
        return star_density(prev,cur,h)+star_density(cur,nxt,h)+slope*matter_query(cur)
    tiny=1e-20
    eco=np.zeros((4,4));link=np.zeros((4,6))
    for i in range(4):
        for j in range(4):
            old=cur['e'][i,j]
            cur['e'][i,j]=old+1j*tiny
            eco[i,j]=action().imag/tiny
            cur['e'][i,j]=old
    for r in range(4):
        for j,X in enumerate(LORENTZ):
            old=cur['u'][r].copy()
            cur['u'][r]=expm(1j*tiny*X)@old
            link[r,j]=action().imag/tiny
            cur['u'][r]=old
    return {'h':h,'sigma':sigma,'f':float(star_density(cur,nxt,h).real),
            'q':float(matter_query(cur).real),
            'coframe00':float(eco[0,0]),'coframe11':float(eco[1,1]),
            'max_coframe':float(np.max(abs(eco))),
            'max_physical_link':float(h*np.max(abs(link))),
            'max_offdiagonal_coframe':float(
                np.max(abs(eco-np.diag(np.diag(eco))))),
            'material_amplitude':float(amplitude)}

def run():
    import math
    assert verify_exact()==108
    rows=[]
    for sigma in (-1,1):
        for n in (8,16,32,64,128):
            row=native_first_source(1/n,sigma)
            rows.append(row)
            assert abs(row['q'])<1e-12
            if sigma==1:
                assert row['max_coframe']<.8/n
                assert row['max_physical_link']<.5/n
            else:
                assert abs(row['coframe00']-3*math.exp(-.25))<.3/n
                assert abs(row['coframe11']+3*math.exp(-.75))<.7/n
    assert rows[-1]['max_coframe']<rows[5]['max_coframe']
    assert rows[4]['max_coframe']>2
    return {'status':'PASS_SCOPED_STAR_TO_CONTINUUM_NORMALIZATION',
            'exact_face_tests':108,
            'face_relation':'S_star_cell = -det(e)*R_standard_cell/2 (positive Cartesian orientation)',
            'rank2_sigma_minus_limit':{'E_coframe00':'3 exp(-1/4)',
                                        'E_coframe11':'-3 exp(-3/4)'},
            'rank2_sigma_plus':{'volume_relation':'e*mu=2*kappa',
                                'tested_full40_first_source':'O(h) observed'},
            'rows':rows,
            'scope':{'finite_exact_all42_root':False,
                     'uniform_analytic_refinement_bound_proved':False,
                     'material_rows_zero_by_constant_finite_currents':True,
                     'full_nonlinear_CQ_price_source_replayed':False,
                     'native_sigma_plus_book_choice_proved':False,
                     'spatial_homogeneous_interior_stencil':True,
                     'GR_closed':False}}
if __name__=='__main__':
    print(json.dumps(run(),indent=2))
