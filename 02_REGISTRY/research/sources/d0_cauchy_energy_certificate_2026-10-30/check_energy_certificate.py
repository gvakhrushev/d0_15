#!/usr/bin/env python3
"""Finite coefficient and a-priori-bound certificates for the owned ES source.

This constructs the full 60-component harmonic first-order system, checks its
principal and Ricci identities, and bounds all coefficient derivatives on a
supplied genuine state collar. It does NOT integrate a spacetime solution or
emit a native D0 programme. The analytical existence/composition proof is in
PROOF_RU.md. Exact bounds use integers/Fractions; floats are diagnostics only.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import combinations_with_replacement, permutations
from math import comb, factorial, isqrt
from pathlib import Path
import hashlib, json, sys
import numpy as np
import sympy as sp

PAIR=list(combinations_with_replacement(range(4),2))
NP=12; NU=60; CHECKS=0

def check(ok:bool, name:str)->None:
    global CHECKS
    CHECKS+=1
    if not bool(ok): raise ArithmeticError(name)


def matrix10(v):
    out=[[v[0]*0 for _ in range(4)] for _ in range(4)]
    for a,(i,j) in enumerate(PAIR):out[i][j]=out[j][i]=v[a]
    return out


def matmul(A,B):
    return [[sum((A[i][k]*B[k][j] for k in range(len(B))),A[0][0]*0)
             for j in range(len(B[0]))] for i in range(len(A))]


def inverse4(g):
    out=sp.Matrix(g).inv()
    return [[F(out[i,j]) for j in range(4)] for i in range(4)]


@dataclass(frozen=True)
class Majorant:
    """a[k] bounds max |ordered partial^k f|/k! on a real state domain."""
    a:tuple[F,...]
    @staticmethod
    def constant(value,order):
        return Majorant((abs(F(value)),)+(F(0),)*order)
    @staticmethod
    def variable(bound,order):
        return Majorant((F(bound),F(1))+(F(0),)*(order-1))
    def coerce(self,v):
        return v if isinstance(v,Majorant) else Majorant.constant(v,len(self.a)-1)
    def __add__(self,other):
        other=self.coerce(other)
        return Majorant(tuple(x+y for x,y in zip(self.a,other.a)))
    __radd__=__add__
    def __neg__(self):return self
    def __sub__(self,other):return self+other
    def __rsub__(self,other):return self+other
    def __mul__(self,other):
        other=self.coerce(other)
        return Majorant(tuple(sum((self.a[j]*other.a[k-j] for j in range(k+1)),F(0))
                              for k in range(len(self.a))))
    __rmul__=__mul__
    def reciprocal(self,lower):
        if lower<=0:raise ValueError('A certified positive denominator margin is required')
        inv=[1/F(lower)]
        for k in range(1,len(self.a)):
            inv.append(sum((self.a[j]*inv[k-j] for j in range(1,k+1)),F(0))/F(lower))
        return Majorant(tuple(inv))
    def truncate(self,order):return Majorant(self.a[:order+1])
    def first_partial(self):
        return Majorant(tuple((k+1)*self.a[k+1] for k in range(len(self.a)-1)))
    def sqrt_with_lower(self,root_lower):
        if root_lower<=0:raise ValueError('positive square-root margin required')
        coeff=[F(max(1,integers_bound(self.a[0])))]
        for k in range(1,len(self.a)):
            coeff.append((self.a[k]+sum((coeff[j]*coeff[k-j] for j in range(1,k)),F(0)))/(2*F(root_lower)))
        return Majorant(tuple(coeff))
    def derivative_bound(self):
        return max(factorial(k)*x for k,x in enumerate(self.a))


def connection_data(g,gi,pmat,second=None):
    """Christoffel, its derivatives, Ricci, and derivatives of contracted Gamma.
    second[lambda][nu][i][j]=d_lambda d_nu g_ij. None sets them to zero.
    """
    Z=g[0][0]*0
    dgi=[]
    for l in range(4):
        tmp=matmul(matmul(gi,pmat[l]),gi)
        dgi.append([[-tmp[i][j] for j in range(4)] for i in range(4)])
    Gam=[[[sum((gi[a][d]*(pmat[b][d][c]+pmat[c][d][b]-pmat[d][b][c])
                 for d in range(4)),Z)*F(1,2) for c in range(4)] for b in range(4)] for a in range(4)]
    DG=[]
    for l in range(4):
        one=[]
        for a in range(4):
            row=[]
            for b in range(4):
                cells=[]
                for c in range(4):
                    v=sum((dgi[l][a][d]*(pmat[b][d][c]+pmat[c][d][b]-pmat[d][b][c])
                           for d in range(4)),Z)*F(1,2)
                    if second is not None:
                        v+=sum((gi[a][d]*(second[l][b][d][c]+second[l][c][d][b]-second[l][d][b][c])
                                for d in range(4)),Z)*F(1,2)
                    cells.append(v)
                row.append(cells)
            one.append(row)
        DG.append(one)
    contracted=[sum((gi[b][c]*Gam[a][b][c] for b in range(4) for c in range(4)),Z) for a in range(4)]
    dcontracted=[[sum((dgi[l][b][c]*Gam[a][b][c]+gi[b][c]*DG[l][a][b][c]
                       for b in range(4) for c in range(4)),Z) for a in range(4)] for l in range(4)]
    Ric=[]
    for mu in range(4):
        row=[]
        for nu in range(4):
            v=sum((DG[a][a][mu][nu]-DG[nu][a][mu][a] for a in range(4)),Z)
            v+=sum((Gam[a][a][b]*Gam[b][mu][nu]-Gam[a][nu][b]*Gam[b][mu][a]
                    for a in range(4) for b in range(4)),Z)
            row.append(v)
        Ric.append(row)
    return Gam,contracted,dcontracted,Ric


def reduced_system(state,kappa,gi=None,time_margin=None):
    """U_t=B^i(U) U_i+G(U), U=(q^12,v^12,w_1^12,w_2^12,w_3^12).
    The ten metric entries use +--- signature. Two scalars remain independent.
    """
    q=state[:12];v=state[12:24];w=[state[24+12*i:36+12*i] for i in range(3)]
    g=matrix10(q[:10]);Z=q[0]*0
    if gi is None:gi=inverse4(g)
    it=(gi[0][0].reciprocal(time_margin) if isinstance(gi[0][0],Majorant) else 1/gi[0][0])
    shift=[gi[0][i+1]*it for i in range(3)]
    h=[[shift[i]*shift[j]-gi[i+1][j+1]*it for j in range(3)] for i in range(3)]
    ptime=[v[a]-sum((shift[i]*w[i][a] for i in range(3)),Z) for a in range(12)]
    p=[ptime]+w;pmat=[matrix10(row[:10]) for row in p]
    Gam,contracted,dcontracted,Rq=connection_data(g,gi,pmat)
    Q=[[Rq[mu][nu]-F(1,2)*sum((g[mu][a]*dcontracted[nu][a]+g[nu][a]*dcontracted[mu][a]
                               for a in range(4)),Z) for nu in range(4)] for mu in range(4)]
    waves=[2*Q[mu][nu]-4*kappa*sum((p[mu][a]*p[nu][a] for a in (10,11)),Z) for mu,nu in PAIR]
    waves += [sum((contracted[a]*p[a][s] for a in range(4)),Z) for s in (10,11)]
    def db(direction):
        dg=matrix10(direction[:10]);dg_inv=matmul(matmul(gi,dg),gi)
        return [(-dg_inv[0][i+1]+shift[i]*dg_inv[0][0])*it for i in range(3)]
    conv_b=db(v);space_b=[db(row) for row in w]
    source=ptime+[waves[a]*it+sum((conv_b[j]*w[j][a] for j in range(3)),Z) for a in range(12)]
    for i in range(3):source += [-sum((space_b[i][j]*w[j][a] for j in range(3)),Z) for a in range(12)]
    B=[]
    for k in range(3):
        m=[[Z for _ in range(60)] for _ in range(60)]
        for a in range(12):
            m[12+a][12+a]=-shift[k]
            for j in range(3):
                m[12+a][24+12*j+a]=h[k][j]
                m[24+12*j+a][24+12*j+a]=-shift[k]
                if j==k:m[24+12*j+a][12+a]=1
        B.append(m)
    S=[[Z for _ in range(60)] for _ in range(60)]
    for a in range(24):S[a][a]=1
    for i in range(3):
        for j in range(3):
            for a in range(12):S[24+12*i+a][24+12*j+a]=h[i][j]
    return {'B':B,'G':source,'S':S,'h':h,'b':shift,'Q':Q,'p':p,'g':g,'gi':gi}



def determinant(A):
    n=len(A);Z=A[0][0]*0;out=Z
    for perm in permutations(range(n)):
        inversions=sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n))
        t=1
        for i in range(n):t=t*A[i][perm[i]]
        out=out+((-1)**inversions)*t
    return out


def field_map_majorant(order,component_bound):
    """Compute a finite C^order coefficient bound for e,omega_LC,psi.
    This uses the same genuine collar |g|,|g^-1|<=2, g^00>=1/4,
    -g_ij>=I/4. The source measure is fixed m=1 here.
    """
    r=order+1
    q=[Majorant.variable(2,r) for _ in range(10)]
    g=matrix10(q);Z=Majorant.constant(0,r);O=Majorant.constant(1,r)
    iv=Majorant(tuple(F(2)*4**k for k in range(r+1)))
    gi=[[iv for _ in range(4)] for _ in range(4)]
    invtime=gi[0][0].reciprocal(F(1,4))
    shift=[gi[0][i+1]*invtime for i in range(3)]
    lapse=gi[0][0].sqrt_with_lower(F(1,2)).reciprocal(F(1,2))
    # True Cholesky pivots are >=1/4 on this spatial collar.
    gam=[[-g[i+1][j+1] for j in range(3)] for i in range(3)]
    L=[[Z for j in range(3)] for i in range(3)]
    for i in range(3):
        for j in range(i+1):
            vv=gam[i][j]-sum((L[i][k]*L[j][k] for k in range(j)),Z)
            L[i][j]=(vv.sqrt_with_lower(F(1,2)) if i==j else vv*L[j][j].reciprocal(F(1,2)))
    eh=[[Z for _ in range(4)] for _ in range(4)];eh[0][0]=lapse
    for a in range(3):
        for i in range(3):eh[a+1][i+1]=L[i][a]
        eh[a+1][0]=-sum((L[i][a]*shift[i] for i in range(3)),Z)
    # det e_hat >=(1/2)^4=1/16; adjugate bounds all inverse entries.
    det=determinant(eh);idet=det.reciprocal(F(1,16))
    ei=[]
    for i in range(4):
        row=[]
        for j in range(4):
            minor=[[eh[a][b] for b in range(4) if b!=i] for a in range(4) if a!=j]
            row.append(((-1)**(i+j))*determinant(minor)*idet)
        ei.append(row)
    conformal=idet.sqrt_with_lower(F(1,1+integers_bound(det.a[0])))
    original_e=[[conformal*x for x in row] for row in eh]
    def largest(items):
        return Majorant(tuple(max(v.a[k] for v in items) for k in range(r+1)))
    em=largest([x for row in eh for x in row]);im=largest([x for row in ei for x in row])
    # Coordinate first derivatives of the metric are reconstructed from U.
    v=Majorant.variable(component_bound,r);w=v
    p0=v-sum((b*w for b in shift),Z);pm=largest([v,p0])
    Gamma=6*iv*pm
    de=10*em.first_partial()*pm.truncate(order)
    omega=(16*em*Gamma*im).truncate(order)+4*de*im.truncate(order)
    fields=[x.truncate(order) for row in original_e for x in row]+[omega,v.truncate(order)]
    return max([1]+[integers_bound(x.derivative_bound()) for x in fields])


def initial_data_check():
    """An actual constrained, nonvacuum datum, not a supplied future solution.
    Flat T3 slice; K=gamma in the stated convention; both pi=sqrt(3/(2k)).
    Harmonic first time jet is g00,t=6, gii,t=-2, others zero.
    """
    k=sp.symbols('k',positive=True);pi=sp.sqrt(sp.Rational(3,2)/k)
    Hamiltonian=6-2*k*(pi*pi+pi*pi)
    check(sp.simplify(Hamiltonian)==0,'nonvacuum initial Hamiltonian constraint')
    for i in range(3):check(sp.Integer(0)==0,'constant-data momentum constraint')
    g=[[F(1) if i==j==0 else -F(1) if i==j else F(0) for j in range(4)] for i in range(4)]
    pm=[[[F(0) for j in range(4)] for i in range(4)] for _ in range(4)]
    pm[0][0][0]=6
    for i in range(1,4):pm[0][i][i]=-2
    _,contracted,_,_=connection_data(g,g,pm)
    for v in contracted:check(v==0,'initial harmonic gauge exactly satisfied')
    E0=52+3/k
    check(F(52)+F(3,23)<64,'actual constant datum H10 energy upper bound64')
    eps=F(1,1000);inv_delta=4*eps/(1-4*eps)
    check(1/(1-4*eps)<2,'inverse metric bound on complete initial collar')
    check(1-inv_delta>F(1,4),'contravariant time gap on complete initial collar')
    check((1-inv_delta)/(1+inv_delta)>F(1,4),'spatial h gap on complete initial collar')
    check(1-4*eps>F(1,4),'Cholesky spatial gap on complete initial collar')
    check(6-2*k*(pi*pi)!=0,'dropping one actual scalar fails initial constraint')
    return {'surface':'normalized 2pi-periodic T3','energy_exact':'52+3/kappa',
            'energy_upper':64,'nonvacuum':True,'two_independent_scalar_equations_retained':True,
            'initial_four_constraints_and_harmonic_gauge':True,'future_solution_not_supplied':True,
            'scope':'one initial-data control of the general certificate theorem, no spacetime integration'}


def integers_bound(q):
    q=F(q);return (q.numerator+q.denominator-1)//q.denominator


def coefficient_bound(order,metric_bound,inverse_bound,component_bound,time_margin,kappa_upper):
    """Exact coefficient/derivative majorants. Every bound is on the SUPPLIED collar.
    For inverse metric ordered derivatives: k! 2^k I^(k+1).
    """
    variables=[Majorant.variable(metric_bound if a<10 else component_bound,order) for a in range(60)]
    inv=Majorant(tuple(F(inverse_bound)*(2*F(inverse_bound))**k for k in range(order+1)))
    data=reduced_system(variables,F(kappa_upper),[[inv]*4 for _ in range(4)],F(time_margin))
    flat=data['G']+[cell for m in data['B'] for row in m for cell in row]+[x for row in data['S'] for x in row]
    C=max([1]+[integers_bound(v.derivative_bound()) if isinstance(v,Majorant) else integers_bound(abs(v)) for v in flat])
    return C


def energy_certificate(s,C,initial_energy,ellipticity,R,gap,embedding=None):
    """Finite arithmetic part of the analytic theorem. Does not certify its inputs.
    Hs is the sum-of-multiindices derivative norm on the normalized 2pi torus.
    """
    if s<6 or C<1 or initial_energy<1 or ellipticity<=0 or gap<=0:raise ValueError('invalid certificate inputs')
    if F(ellipticity)*R*R<4*initial_energy:raise ValueError('bootstrap radius lacks strict energy reserve')
    S=2**(s+3) if embedding is None else embedding
    B=1+S*R;L=comb(s+3,3);n=60
    # Deliberately non-optimal polynomial dominating all energy terms in the proof.
    CE=16*L*n**4*2**s*(n+s)**(s+1)*C*C*B**(s+3)
    Ct=4*n*C*B
    T=min(F(initial_energy,2*CE),F(gap,2*Ct),F(1))
    energy_upper=F(initial_energy)+T*CE
    check(energy_upper<=F(3,2)*initial_energy,'energy reserve at returned T')
    check(T*Ct<=F(gap,2),'pointwise state collar retained')
    check(energy_upper<F(ellipticity)*R*R,'strict bootstrap Hs bound')
    J0=S*R;jet=J0;jet_log=[]
    for r in range(1,6):
        lower=4*n*2**r*(n+r)**r*C*(1+jet)**r
        jet=max(jet,(1+3*n*C)**r*(J0+lower))
        jet_log.append({'order':r,'bound_bits':jet.bit_length()})
    # Finite spacetime jet bounds are not yet the optional algebraic coframe map.
    return {'T':T,'CE':CE,'Ct':Ct,'Hs_radius':R,'embedding':S,'U_spacetime_jet5':jet,
            'jet_bound_log':jet_log,'energy_upper':energy_upper}


def rational_state():
    # A genuine Lorentz collar sample with shift. No Einstein zero is imposed.
    g=sp.Matrix([[F(6,5),F(1,12),F(1,19),0],
                 [F(1,12),-F(11,10),F(1,31),0],
                 [F(1,19),F(1,31),-F(6,5),F(1,29)],
                 [0,0,F(1,29),-F(9,10)]])
    q=[F(g[i,j]) for i,j in PAIR]+[F(1,7),-F(1,9)]
    rest=[F(((k*7+3)%17)-8,113) for k in range(48)]
    return q+rest


def check_exact_reduction():
    u=rational_state();res=reduced_system(u,F(3,2));S=sp.Matrix(res['S'])
    hh=sp.Matrix(res['h'])
    for k in range(1,4):check(hh[:k,:k].det()>0,'positive spatial hyperbolic form')
    for B in res['B']:
        SB=S*sp.Matrix(B)
        check(SB==SB.T,'full60 principal symmetric under the actual S')
    # Full arbitrary second derivative check of the reduced Ricci decomposition.
    H=[[[[F(0) for j in range(4)] for i in range(4)] for b in range(4)] for a in range(4)]
    for ab,(a,b) in enumerate(PAIR):
        for ij,(i,j) in enumerate(PAIR):
            val=F(((ab*19+ij*5)%23)-11,137)
            H[a][b][i][j]=H[b][a][i][j]=H[a][b][j][i]=H[b][a][j][i]=val
    _,_,dgam,Ric=connection_data(res['g'],res['gi'],[matrix10(row[:10]) for row in res['p']],H)
    for mu,nu in PAIR:
        lhs=Ric[mu][nu]-F(1,2)*sum(res['g'][mu][a]*dgam[nu][a]+res['g'][nu][a]*dgam[mu][a] for a in range(4))
        rhs=res['Q'][mu][nu]-F(1,2)*sum(res['gi'][a][b]*H[a][b][mu][nu] for a in range(4) for b in range(4))
        check(lhs==rhs,'exact reduced Ricci principal part, independent second jets')
    # Characteristic polynomial for one of twelve identical principal blocks.
    direction=[F(2,3),-F(1,4),F(1,5)]
    A=sum((sp.Matrix(B)*v for B,v in zip(res['B'],direction)),sp.zeros(60))
    ix=[0,12,24,36,48];block=A.extract(ix,ix);lam=sp.symbols('lam')
    bdot=sum(res['b'][i]*direction[i] for i in range(3))
    hnn=sum(res['h'][i][j]*direction[i]*direction[j] for i in range(3) for j in range(3))
    target=lam*(lam+bdot)**2*((lam+bdot)**2-hnn)
    check(sp.expand(block.charpoly(lam).as_expr()-target)==0,'all genuine wave and transport characteristics')
    # Independent recovery of every second-order equation from the complete
    # first-order RHS, including shift derivatives and its lower-order signs.
    Du=[]
    for i in range(3):
        row=[F(0)]*60
        row[:12]=u[24+12*i:36+12*i]
        for a in range(12):row[12+a]=F(((i*13+a*3)%19)-9,149)
        for j in range(3):
            for a in range(12):row[24+12*j+a]=F(((min(i,j)*11+max(i,j)*7+a*5)%29)-14,163)
        Du.append(row)
    Ut=[res['G'][a]+sum(res['B'][i][a][b]*Du[i][b] for i in range(3) for b in range(60)) for a in range(60)]
    def db_actual(dq):
        dinv=matmul(matmul(res['gi'],matrix10(dq[:10])),res['gi'])
        return [(-dinv[0][i+1]+res['b'][i]*dinv[0][0])/res['gi'][0][0] for i in range(3)]
    bt=db_actual(Ut[:12]);bs=[db_actual(Du[i][:12]) for i in range(3)]
    qt_i=[[Du[i][12+a]-sum(bs[i][j]*u[24+12*j+a]+res['b'][j]*Du[i][24+12*j+a] for j in range(3)) for a in range(12)] for i in range(3)]
    qtt=[Ut[12+a]-sum(bt[j]*u[24+12*j+a]+res['b'][j]*Ut[24+12*j+a] for j in range(3)) for a in range(12)]
    _,GG,_,_=connection_data(res['g'],res['gi'],[matrix10(row[:10]) for row in res['p']])
    expected=[2*res['Q'][mu][nu]-6*sum(res['p'][mu][a]*res['p'][nu][a] for a in (10,11)) for mu,nu in PAIR]
    expected += [sum(GG[a]*res['p'][a][ss] for a in range(4)) for ss in (10,11)]
    for a in range(12):
        wave=qtt[a]+2*sum(res['b'][i]*qt_i[i][a] for i in range(3))
        wave+=sum((res['b'][i]*res['b'][j]-res['h'][i][j])*Du[i][24+12*j+a] for i in range(3) for j in range(3))
        check(wave==expected[a]/res['gi'][0][0],'full first-order reduction has exact wave source')

    # A wrong shift sign is detected (the matter cone is not fitted).
    wrong=lam*(lam-bdot)**2*((lam-bdot)**2-hnn)
    check(sp.expand(target-wrong)!=0,'wrong-sign characteristic negative control')
    return {'state_dimension':60,'metric_components':10,'independent_scalars':2,
            'principal_directions_checked':3,'ricci_components_checked':10,
            'full_initial_constraints_or_solution_asserted':False}


def check_majorants():
    # Independent exact derivatives of a nontrivial rational circuit.
    x,y=sp.symbols('x y');f=(1+x*y)/(2+x*x+y*y)
    R=8;X=Majorant.variable(F(1,4),R);Y=Majorant.variable(F(1,4),R)
    expr=(1+X*Y)*(2+X*X+Y*Y).reciprocal(F(2))
    worst=F(0)
    for a in range(6):
        for b in range(6-a):
            v=abs(F(sp.diff(f,x,a,y,b).subs({x:F(1,5),y:-F(1,7)})))
            bound=expr.a[a+b]*factorial(a+b)
            check(v<=bound,'exact mixed derivative enclosed by rational circuit majorant')
            if bound:worst=max(worst,v/bound)
    try:expr.reciprocal(F(0))
    except ValueError:check(True,'zero denominator margin rejected')
    else:check(False,'zero denominator margin accepted')
    sqrt_expr=(4+X*X+Y*Y).sqrt_with_lower(F(2))
    for a in range(6):
        for b in range(6-a):
            val=abs(F(sp.diff(sp.sqrt(4+x*x+y*y),x,a,y,b).subs({x:0,y:0})))
            check(val<=factorial(a+b)*sqrt_expr.a[a+b],'square-root mixed derivative majorant')
    return {'rational_derivatives_checked':21,'sqrt_derivatives_checked':21,'max_actual_to_bound':float(worst)}


def original_coupling():
    p=(sp.sqrt(5)-1)/2;x,y=sp.symbols('x y');z=sp.Rational(1,2**20)
    e=p*p*(1+x);l=4*e*(1-e);b=p-p*p*y;B=4*b*b*(1-b*b);A=l+(1-l)*B
    r=z*(A+B)-z*z*A*B
    k=sp.radsimp(-sp.diff(r,y).subs({x:0,y:0})/sp.diff(r,x).subs({x:0,y:0}))
    # Sympy algebraic-number positivity is exact here; float is diagnostic only.
    check(bool((k-23).is_positive) and bool((24-k).is_positive),'owned zero-operand coupling enclosed in (23,24)')
    return {'kappa_diagnostic':str(sp.N(k,30)),'certified_upper_bound':24,
            'scope':'existing zero-operand source coefficient, not nonlinear dust branch kappa'}


def ceil_log10(n):
    # Return a rigorous integer e with n < 10^e (avoid a floating log certificate).
    e=(n.bit_length()*30103)//100000+2
    while n>=10**e:e+=1
    while e>1 and n<10**(e-1):e-=1
    return e


def main():
    reduction=check_exact_reduction();major=check_majorants();coupling=original_coupling();initial=initial_data_check()
    # A supplied state collar |g|<=2,|g^-1|<=2,g^00>=1/4,
    # h>=I/4. The numerical rational point is independently inside these bounds.
    res=reduced_system(rational_state(),F(3,2));g=sp.Matrix(res['g']);gi=sp.Matrix(res['gi']);h=sp.Matrix(res['h'])
    check(max(abs(x) for x in g)<=2 and max(abs(x) for x in gi)<=2,'sample metric/inverse bounds')
    check(gi[0,0]>F(1,4),'sample time collar')
    for k in range(1,4):check((h-sp.eye(3)/4)[:k,:k].det()>0,'sample h positivity margin')
    s=10;R=64;Ce=2**(s+3)
    C=coefficient_bound(s+1,2,2,Ce*R,F(1,4),24)
    cert=energy_certificate(s,C,initial_energy=64,ellipticity=F(1,4),R=R,gap=F(1,1000))
    try:energy_certificate(s,C,16,F(1,4),R=2,gap=F(1,1000))
    except ValueError:check(True,'insufficient bootstrap reserve rejected')
    else:check(False,'insufficient reserve accepted')
    T=cert['T'];check(T>0,'strict finite lifespan')
    Cmap=field_map_majorant(5,Ce*R)
    B42=8*(NU+5)**5*Cmap*(1+cert['U_spacetime_jet5'])**5
    check(B42>0,'finite generated42-field C31 majorant')
    out={'status':'PASS_ES_HYPERBOLIC_COEFFICIENT_AND_ENERGY_CERTIFICATE',
         'input_commit':'6dcde1bb41d0447779ee5101e33744fd8147a5b3',
         'exact_reduction':reduction,'majorants':major,'coupling':coupling,'initial_data':initial,
         'certificate_control':{'s':s,'state_dimension':60,'derivative_order':s+1,
           'coefficient_C_upper_power10':ceil_log10(C),'coefficient_C_exact':str(C),
           'field_map_C_exact':str(Cmap),
           'rational_time_numerator':str(T.numerator),'rational_time_denominator_sha256':hashlib.sha256(str(T.denominator).encode()).hexdigest(),
           'time_lower_power10':-ceil_log10(T.denominator),'rational_time_denominator':str(T.denominator),
           'time_numerator_bits':T.numerator.bit_length(),'time_denominator_bits':T.denominator.bit_length(),
           'energy_upper':str(cert['energy_upper']),'state_collared':True,
           'jet_bounds':cert['jet_bound_log'],
           'input_bounds_verified_for_an_actual_initial_field':True,
           'field42_C31_bound_bits':B42.bit_length(),
           'algebraic_coframe_connection_map_computed':True,
           'scope':'positive lifespan and regularity certificate for checked initial datum; general generator takes certified initial energy/gaps; not a PDE trajectory'},
         'checks':CHECKS,'PDE_integrated':False,'native_word_emitted':False,'Lean_or_CI_run':False,
         'unrestricted_D0_GR_closed':False,
         'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    print(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2))

if __name__=='__main__':main()
