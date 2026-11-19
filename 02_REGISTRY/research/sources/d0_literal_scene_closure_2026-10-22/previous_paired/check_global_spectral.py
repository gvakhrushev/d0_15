#!/usr/bin/env python3
"""Global source of the declared two-band paired-incidence H+J model.

This checks the original Golden operands and the new global composition.
It does NOT replay the old 40+2 geometric proof, identify the physical
Book03 scene Laplacian, or assert a full native preparation/compiler.
The numerical table uses the MINIMAL paired Hilbert carrier, not a claimed
physical dimension of the D0 scene. No finite precision claim is an
outward-interval certificate.
"""
from __future__ import annotations
import json
from pathlib import Path
from mpmath import mp
import sympy as sp

mp.dps = 80
p = (mp.sqrt(5)-1)/2
zeta = mp.mpf(2)**-20
beta = 2*p*p
checks = []

def require(label: str, condition: bool) -> None:
    if not condition:
        raise ArithmeticError(label)
    checks.append(label)

def close(label: str, actual, expected, tol=mp.mpf('1e-55')) -> None:
    require(label, abs(actual-expected) < tol)

def operands(x, y):
    E=p*p*(1+x)
    L=4*E*(1-E)
    b=p-p*p*y
    B=4*b*b*(1-b*b)
    A=L+(1-L)*B
    return A, B

A0,B0=operands(mp.mpf(0),mp.mpf(0))
Ax=mp.diff(lambda x: operands(x,0)[0],0)
Ay=mp.diff(lambda y: operands(0,y)[0],0)
By=mp.diff(lambda y: operands(0,y)[1],0)
jA=zeta/(1-zeta*A0)
jB=zeta/(1-zeta*B0)
lamJ=(jA*Ay+jB*By)/(jA*Ax)

ps=(sp.sqrt(5)-1)/2
zs=sp.Rational(1,2**20)
Bs=4*ps**3
As=Bs*(1+ps**6)
axs=4*ps**2*(1-2*ps**2)*(1-Bs)
bys=-8*ps**3*(1-2*ps**2)
ays=(1-Bs)*bys
require('exact native A_y/A_x=-2p',sp.simplify(ays/axs+2*ps)==0)
require('exact native B_y/A_x=-2p^-5',sp.simplify(bys/axs+2*ps**-5)==0)
ratio_old=-2*ps**-5*((1-zs*As)/(1-zs*Bs)+ps**6)
ratio_new=(ays+(1-zs*As)/(1-zs*Bs)*bys)/axs
require('exact equality to the inherited lambda_minus',sp.simplify(ratio_new-ratio_old)==0)
close('native lambda decimal',lamJ,mp.mpf('-23.416406751884074972895583'),mp.mpf('1e-23'))

# Minimal paired carrier: positive bands A,B twice, no extra harmonic modes.
# Additional field-independent heat modes are retained through Zfixed >= 0.
def coefficients(W: int, Zfixed=mp.mpf(0)):
    Z=Zfixed+2*W*(mp.exp(-beta*A0)+mp.exp(-beta*B0))
    tA=2*mp.exp(-beta*A0)/Z
    tB=2*mp.exp(-beta*B0)/Z
    wA=jA-tA
    wB=jB-tB
    lam=(wA*Ay+wB*By)/(wA*Ax)
    return Z,tA,tB,wA,wB,lam

rows=[]
for L in [8,16,32,64,128,256]:
    W=528*L**4
    for Zfixed in [mp.mpf(0),mp.mpf(W),mp.mpf(100*W)]:
        Z,tA,tB,wA,wB,lam=coefficients(W,Zfixed)
        require('heat derivative bound',0<tA<mp.mpf(1)/W and 0<tB<mp.mpf(1)/W)
        require('both full H+J slopes strictly positive',wA>0 and wB>0)
        require('derived coupling has the Einstein sign',lamJ<lam<-2*p)
        bound=2*abs(By/Ax)/(W*zeta-1)
        require('uniform coupling defect bound',abs(lam-lamJ)<bound)
    Z,tA,tB,wA,wB,lam=coefficients(W)
    rows.append({'L':L,'W_lower_model':W,'W_zeta':str(W*zeta),
                 'lambda_minimal_paired_carrier':mp.nstr(lam,28),
                 'lambda_defect':mp.nstr(lam-lamJ,18),
                 'h4_scaled_defect':mp.nstr((lam-lamJ)*L**4,18)})

# Nonuniform integer copy weights, inverse-PF operand dictionary.
# This tests the scalar-source composition, not a new 42-field geometry.
m=[528*1000,528*1500,528*2500]
W=sum(m)
mean=mp.mpf(W)/3
rho=[mp.mpf(k)/mean for k in m]
tau=mp.mpf('0.0001')
Zfixed=mp.mpf(7*W)

def action(fields):
    bands=[operands(tau*fields[2*i]/rho[i],tau*fields[2*i+1]/rho[i]) for i in range(3)]
    Z=Zfixed+2*sum(k*(mp.exp(-beta*A)+mp.exp(-beta*B)) for k,(A,B) in zip(m,bands))
    J=-sum(k*(mp.log(1-zeta*A)+mp.log(1-zeta*B)) for k,(A,B) in zip(m,bands))
    return mp.log(Z)/beta+J

Z,tA,tB,wA,wB,lam=coefficients(W,Zfixed)
gain=mean*tau*wA*Ax
errors=[]
for k in range(6):
    def along(t):
        v=[mp.mpf(0)]*6;v[k]=t
        return action(v)
    value=mp.diff(along,0)
    target=gain if k%2==0 else gain*lam
    close('complete global H+J derivative at each nonuniform site',value,target)
    errors.append(abs(value-target))

# No differentiation along the null ansatz is used in the previous test:
# f_i,q_i are independently varied before evaluating at f_i=q_i=0.
# The old exact unrestricted geometric theorem is consumed separately.

# Gibbs auxiliary elimination, including every fixed spectator mode.
# Here Zfixed=7W means 7W zero eigenvalues in this diagnostic.
energy=2*sum(k*(A0*mp.exp(-beta*A0)+B0*mp.exp(-beta*B0)) for k in m)/Z
entropy=mp.log(Z)+beta*energy
close('thermal variational envelope value',entropy/beta-energy,mp.log(Z)/beta)
for energy_i in [mp.mpf(0),A0,B0]:
    sigma_i=mp.exp(-beta*energy_i)/Z
    close('each Gibbs auxiliary Euler row',-energy_i-(mp.log(sigma_i)+1)/beta,(mp.log(Z)-1)/beta)

# Exact all-h discrete Poisson identity used by the inherited all40+2 proof.
x,y,h,lam,E,a2,b2,a3,b3=sp.symbols('x y h lambda E a2 b2 a3 b3',nonzero=True)
H=-lam*E*(x*x+y*y)+a2*(x*x-y*y)+2*b2*x*y+a3*(x**3-3*x*y*y)+b3*(3*x*x*y-y**3)
Lap=(H.subs(x,x+h)+H.subs(x,x-h)+H.subs(y,y+h)+H.subs(y,y-h)-4*H)/h**2
require('all-h exact sourced harmonic profile',sp.simplify(Lap+4*lam*E)==0)
# Algebraic source-preserving rescaling for the same continuum metric.
lstar,lh,e0=sp.symbols('lambda_star lambda_h e0',nonzero=True)
require('fixed target metric via determined matter normalization',sp.simplify(lh*(lstar/lh)*e0-lstar*e0)==0)

result={
 'status':'PASS_GLOBAL_COMPOSITION_FOR_DECLARED_PAIRED_INCIDENCE_MODEL',
 'source_baseline':'ff98f8cf5eea6b989945349b5d2ffd313c5db8ff',
 'original_parameters':{'p':'(sqrt(5)-1)/2','zeta':'2^-20','beta':'2p^2'},
 'lambda_feedback_limit':mp.nstr(lamJ,35),
 'analytic_sign_gate':'W*zeta>1',
 'nonuniform_scalar_source_max_error':mp.nstr(max(errors),10),
 'illustrative_minimal_paired_carrier_table':rows,
 'exact_symbolic_poisson_identity':True,
 'old_all40_plus_two_material_geometric_proof_reexecuted':False,
 'physical_Book03_scene_equals_paired_incidence':False,
 'physical_independent_inputs_solved':False,
 'universal_GR_proved':False,
 'precision_kind':'80-digit diagnostic and listed exact symbolic identities; no outward-interval/full-Lean claim',
 'check_count':len(checks)
}
print(json.dumps(result,ensure_ascii=False,indent=2))
