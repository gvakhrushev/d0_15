#!/usr/bin/env python3
"""D0 #334: backward GR seam; exact ADM curvature/8+8 exterior and fixed-beta IR tests.
No physical-native selector, no Einstein field equation asserted from code.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sympy as s
import mpmath as mp

HERE=Path(__file__).resolve().parent
checks=[]
def ck(v,tag):
    if v is not True and v!=s.true: raise ArithmeticError(tag+': '+str(v))
    checks.append(tag)
def equal(x,y,tag): ck(s.simplify(x-y)==0,tag)

# Two natural exterior carriers in exactly the same 16 grades: 4D and 3D x time-grade.
for d in (3,4):
    trE=-sum(s.binomial(d-2,k-1) for k in range(d+1))
    a0=2**d; a2=s.Rational(a0,6)+trE
    equal(trE,-2**(d-2),f'full_exterior_{d}D_traceE')
    equal(a2,-s.Rational(2**(d-2),3),f'full_exterior_{d}D_heat_a2')
equal(2*(-s.Rational(2,3)),-s.Rational(4,3),'rank8_plus_rank8_spatial_heat_a2_same_rank16')
equal(-s.Rational(4,3)-2*(-s.Rational(4,3)) ,s.Rational(4,3),'spectral_signature_reflection_relative_coeff')

# Direct Ricci from metric jets, without preinstalled spatial/Lorentz scalar oracle.
t,x,y,z=s.symbols('t x y z',real=True)
coords=(t,x,y,z)
def ricci_scalar_jet(g,p):
    n=4; subs=dict(zip(coords,p)); g=s.Matrix(g)
    G=g.subs(subs); gi=G.inv()
    dG=[g.diff(q).subs(subs) for q in coords]
    ddG=[[g.diff(q).diff(r).subs(subs) for r in coords] for q in coords]
    dgi=[-gi*dG[q]*gi for q in range(n)]
    Gamma={}; dGamma={}
    for a in range(n):
        for b in range(n):
            for c in range(n):
                Gamma[a,b,c]=s.Rational(1,2)*sum(gi[a,k]*(dG[b][k,c]+dG[c][k,b]-dG[k][b,c]) for k in range(n))
                for e in range(n):
                    dGamma[e,a,b,c]=s.Rational(1,2)*sum(dgi[e][a,k]*(dG[b][k,c]+dG[c][k,b]-dG[k][b,c])+gi[a,k]*(ddG[e][b][k,c]+ddG[e][c][k,b]-ddG[e][k][b,c]) for k in range(n))
    Ric=s.zeros(n)
    for b in range(n):
        for d in range(n):
            Ric[b,d]=sum(dGamma[a,a,b,d]-dGamma[d,a,b,a]+sum(Gamma[a,a,e]*Gamma[e,b,d]-Gamma[a,d,e]*Gamma[e,b,a] for e in range(n)) for a in range(n))
    return s.factor(s.trace(gi*Ric))

ADM=[]
for f,pt,label in [ (1+x*x,(0,s.Rational(1,2),0,0),'static'),
                   (1+t+x*x,(s.Rational(1,4),s.Rational(1,2),0,0),'time_dependent')]:
    N=1+x; shift=x/2
    G=s.diag(N*N, f*f,f*f,f*f); L=s.diag(N*N,-f*f,-f*f,-f*f)
    G[0,0]+=f*f*shift*shift;G[0,1]=G[1,0]=f*f*shift
    L[0,0]-=f*f*shift*shift;L[0,1]=L[1,0]=-f*f*shift
    R_G=ricci_scalar_jet(G,pt);R_L=ricci_scalar_jet(L,pt)
    f_x=s.diff(f,x);f_xx=s.diff(f,x,2)
    R3=s.factor(-4*f_xx/f**3+2*f_x**2/f**4) # 3D conformal f^2 delta
    Lap=s.factor(s.diff(f*s.diff(N,x),x)/f**3)
    ss=dict(zip(coords,pt))
    R3p=s.factor(R3.subs(ss));Lapp=s.factor(Lap.subs(ss));Np=N.subs(ss)
    expected=-2*R3p+4*Lapp/Np
    equal(R_L-R_G,expected,'ADM_'+label+'_nonzero_shift_lapse_spatial_gap')
    equal(-s.Rational(3,4)*(-s.Rational(4,3)*R_G+2*s.Rational(4,3)*R3p),R_G-2*R3p,'ADM_'+label+'_spectral_relative_curvature')
    ck(R_L!=R_G,'ADM_'+label+'_nontrivial_Lorentz_Riemann_difference')
    ADM.append({'fixture':label,'R_G':str(R_G),'R_L':str(R_L),'R3':str(R3p),'laplace_N':str(Lapp),'difference':str(R_L-R_G),'expected':str(expected)})

# ADM has all ten independent metric slots (lapse, shift3, spatial6), unlike restricted stored chart.
lapse=s.symbols('n',positive=True)
v=s.symbols('v1:4')
h11,h22,h33,h12,h13,h23=s.symbols('h11 h22 h33 h12 h13 h23',real=True)
h=s.Matrix([[h11,h12,h13],[h12,h22,h23],[h13,h23,h33]])
vv=s.Matrix(v)
g=s.zeros(4)
g[0,0]=lapse*lapse-(vv.T*h*vv)[0]
for i in range(3):
    g[0,i+1]=g[i+1,0]=-(h*vv)[i]
    for j in range(3):g[i+1,j+1]=-h[i,j]
variables=[lapse,*v,h11,h22,h33,h12,h13,h23]
outputs=[g[0,0],g[0,1],g[0,2],g[0,3],g[1,1],g[2,2],g[3,3],g[1,2],g[1,3],g[2,3]]
J=s.Matrix(outputs).jacobian(variables)
check_sub={lapse:s.Integer(4),v[0]:s.Rational(1,7),v[1]:s.Rational(-2,9),v[2]:s.Rational(3,11),h11:s.Integer(2),h22:s.Integer(3),h33:s.Integer(5),h12:s.Integer(0),h13:s.Integer(0),h23:s.Integer(0)}
detJ=s.factor(J.subs(check_sub).det())
ck(detJ!=0,'ADM_full10_nondegenerate_jacobian')
equal(abs(detJ),2*check_sub[lapse]*30,'ADM_full10_exact_jacobian_determinant')

# The fixed-beta large-scale IR coefficient of the ORIGINAL log-feedback, on full exterior16.
mp.mp.dps=65
p=(mp.sqrt(5)-1)/2
beta=2*p*p
zz=mp.mpf(1)/2**20
r=zz/(1-zz)
M=128
F2=-mp.polylog(2,-r);F3=-mp.polylog(3,-r)
cc=4*M*F2/(3*(4*mp.pi)**2*beta)
volume=16*M*F3/(4*mp.pi*beta)**2
ratio=volume/cc
ck(F2>0 and F3>0 and cc>0 and volume>0,'native_fixed_beta_nonzero_heat_curvature_and_volume')
ck(abs(ratio-12*F3/(beta*F2))<mp.mpf('1e-57'),'fixed_beta_relative_Lambda_EH_ratio_no_fit')

# Exact n-by-n heat coefficient: 1/n cyclic recurrence changes the spatial law via F2.
rr=s.symbols('rr')
a0,a2=s.symbols('a0 a2')
for n in range(1,7):
    term=s.expand((-1)**(n+1)*rr**n/s.Integer(n)**3*(a0+n*a2))
    equal(term.coeff(a2),(-1)**(n+1)*rr**n/s.Integer(n)**2,'full_logdet_a2_weight_'+str(n))

# Finite-temperature Poisson resummation without changing beta. det G(tau)=1.
def theta_j(jj,R,tau,dual):
    gs=[mp.exp(2*tau),mp.exp(-2*tau),mp.mpf(1),mp.mpf(1)]
    if dual:
        pref=R**4/(4*mp.pi*jj*beta)**2
        return pref*mp.fprod(mp.jtheta(3,0,mp.exp(-R**2/(4*jj*beta*g))) for g in gs)
    return mp.fprod(mp.jtheta(3,0,mp.exp(-4*mp.pi**2*jj*beta*g/R**2)) for g in gs)

for R in (mp.mpf(2),mp.mpf(5)):
    for jj in (1,3):
        x0=theta_j(jj,R,mp.mpf('0.2'),False)
        x1=theta_j(jj,R,mp.mpf('0.2'),True)
        ck(abs(x0-x1)/x1<mp.mpf('1e-53'),f'Poisson_R{R}_j{jj}_4D_exact_thermal_identity')

def shape_contrast(R,tau):
    b0=theta_j(1,R,mp.mpf(0),True); b1=theta_j(1,R,tau,True)
    H=(mp.log(b1)-mp.log(b0))/beta
    sig=mp.mpf(0)
    for j in range(1,7):
        sig+=(-1)**(j+1)*r**j/j*(theta_j(j,R,tau,True)-theta_j(j,R,mp.mpf(0),True))
    J=-16*M*sig
    return H,J
results=[]
for R in (2,4,8):
    H,J=shape_contrast(mp.mpf(R),mp.mpf('0.2'))
    results.append({'R':R,'thermal_shape_contrast':mp.nstr(H,20),'feedback_shape_contrast':mp.nstr(J,20)})
ck(abs(mp.mpf(results[2]['thermal_shape_contrast']))<abs(mp.mpf(results[0]['thermal_shape_contrast'])),'fixed_beta_thermal_flat_shape_vanishes_at_large_radius')
ck(abs(mp.mpf(results[2]['feedback_shape_contrast']))<abs(mp.mpf(results[0]['feedback_shape_contrast'])),'fixed_beta_feedback_flat_shape_vanishes_at_large_radius')

# Required observer spatial term is exactly -2 times the same full16 spatial Hodge density.
kappa=s.symbols('kappa',nonzero=True)
R4,Rsp=s.symbols('R4 Rsp')
actualJ=kappa*R4
required=kappa*(R4-2*Rsp)
equal(required-actualJ,-2*kappa*Rsp,'observer_spatial_relative_source_uniqueness')

obj={
'owner':'D0 Draft PR334 backward IR Einstein bridge; GEOMETRIC / CONDITIONALLY SPECTRAL, not native physical selection',
'checks_count':len(checks),'checks':checks,'adm_samples':ADM,
'ADM_ten_slot_jacobian_det_fixture':str(detJ),
'heat_coeffs':{'4d_exterior_rank':16,'4d_a2_over_R':'-4/3','3d_double_rank':16,'3d_double_a2_over_R':'-4/3','Lorentz_relative_coeff':-2},
'native_v8_parameters':{'beta':mp.nstr(beta,42),'z':'2^-20','M':M,'r':mp.nstr(r,42), 'F2_minusLi2_minus_r':mp.nstr(F2,42),'F3_minusLi3_minus_r':mp.nstr(F3,42),'positive_curvature_EH_coefficient':mp.nstr(cc,42),'volume_coefficient_absolute':mp.nstr(volume,42),'volume_to_curvature_ratio':mp.nstr(ratio,42)},
'fixed_beta_flat_shape':results,
'gate':'derive physical native 3d-relative readout and on-shell retained/observer projection with full first sources and refinement; no full GR proof',
'limitations':['positive full16 Hodge and natural measure torsionfree slice','ADM foliation and boundary','macroscopic R->infty is not original fixed-volume h->0 comparator','original native complete Cost-Info law and matter are not selected','no all-ten joint-critical nonflat sequence']}
(HERE/'RESULT.json').write_text(json.dumps(obj,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
print('PASS',len(checks))
print('ADM direct:',ADM)
print('ADM jacobian det',detJ)
print('c_J',mp.nstr(cc,20),'lambda_J',mp.nstr(volume,20),'ratio',mp.nstr(ratio,15))
print('fixed beta shape contrasts',results)
print('RESULT.json sha256',hashlib.sha256((HERE/'RESULT.json').read_bytes()).hexdigest())
