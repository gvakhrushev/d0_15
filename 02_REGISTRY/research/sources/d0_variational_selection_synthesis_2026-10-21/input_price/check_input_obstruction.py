#!/usr/bin/env python3
"""Narrow original-native128 scalar-field/input obstruction.

Exact integer CAR and algebraic inequalities plus a floating independent
all128 check. No input optimization, history census, lattice or GR claim.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import math
import sys
import numpy as np
import sympy as sp

REPO = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('/workspace/scratch/323a1a75ae17/d0_15')
PINS = {
 '02_REGISTRY/research/sources/d0_native_preparation_closure_2026-10-21/inputs/native_input.py': 'ee8de4635d24c668949ac9a0186616ab7d59f2ed',
 '02_REGISTRY/research/A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md': 'df8611c7fa37fa71e883831b3f01f434532d99ce',
 '02_REGISTRY/research/sources/d0_retained_entropy_input_euler_2026-10-21/PROOF.md': 'cc0010752a2236fd9e504dc95d8469d82633c191',
 '02_REGISTRY/research/sources/d0_native_preparation_closure_2026-10-21/PROOF.md': '2dde923ce481a00db4928a9467819ccdb73cae5a',
}
checks = []
def require(ok, label):
    if not bool(ok):
        raise ArithmeticError(label)
    checks.append(label)

for rel, sha in PINS.items():
    raw = (REPO/rel).read_bytes()
    actual = hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    require(actual == sha, 'immutable source '+rel)

path = REPO/next(iter(PINS))
spec = importlib.util.spec_from_file_location('original_native128',path)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

# Actual signed CAR convention, using exact SymPy Gaussian integers.
order = (0,2,3,1)
cs=[]
for r in range(4):
    c=sp.zeros(16)
    before=order[:order.index(r)]
    for bits in range(16):
        if not ((bits>>r)&1):
            c[bits|(1<<r),bits]=(-1)**sum((bits>>j)&1 for j in before)
    cs.append(c)
zeta=(sp.I,sp.I,-1,-sp.I)
b=sum((c*(z-1)+c.T*sp.conjugate(z-1) for c,z in zip(cs,zeta)),sp.zeros(16))
b2=(b*b).applyfunc(sp.expand)
require(b2 == 10*sp.eye(16),'exact Gaussian-integer CAR B^2=10 I, B=16 A/nu')
require(b2 != 16*sp.eye(16),'hostile wrong Fourier energy rejected')

p=(sp.sqrt(5)-1)/2
phi=1/p
require(sp.simplify(p**2+p-1)==0,'exact Golden normalization')
require(sp.simplify(p**3-(sp.sqrt(5)-2))==0,'exact p^3 identity')
require(sp.Rational(5)>sp.Rational(11,5)**2,'sqrt5>11/5 hence p^3>1/5')
require(sp.Rational(5)>4,'sqrt5>2 hence phi>3/2')
require(sp.simplify(phi**12-144*phi-89)==0,'exact phi^12=144phi+89')
require(144*sp.Rational(3,2)+89>256,'log_phi(256)<12')
delta=sp.Rational(5,32)*p**3*(sp.Rational(3,5)**2-sp.Rational(1,2)**2)
require(sp.simplify(delta-sp.Rational(11,640)*p**3)==0,'exact all-input rate difference')
require(sp.Rational(4096)*sp.Rational(11,640)*sp.Rational(1,5)-12==sp.Rational(52,25),
        'strict finite-price gap >52/25 from exact bounds')

diag={}
eye=np.eye(16,dtype=complex)
for nu in (.5,.6):
    k,_=m.native(0.0,nu)
    total=sum((x.conj().T@x for x in k),np.zeros_like(eye))
    port=sum((x.conj().T@x for x in k[1::2]),np.zeros_like(eye))
    a2=(eye-k[0])/(2*m.P**2)
    lam=5*nu*nu/128
    e=4*m.P**3*lam
    label=eye-k[0].conj().T@k[0]-k[1].conj().T@k[1]
    label_rate=4*m.P**2*lam*(1-lam)
    errs={'completeness':float(np.linalg.norm(total-eye)),
          'scalar_A2':float(np.linalg.norm(a2-lam*eye)),
          'full_port_effect':float(np.linalg.norm(port-e*eye)),
          'nonblank_label_effect':float(np.linalg.norm(label-label_rate*eye))}
    require(max(errs.values())<1e-12,'original all128 identities at nu='+str(nu))
    for j in range(1,64):
        # Every nonblank label has complete ancillary port law (p^2,p).
        e0=k[2*j].conj().T@k[2*j]
        e1=k[2*j+1].conj().T@k[2*j+1]
        require(np.linalg.norm(m.P*e0-m.P**2*e1)<1e-13,
                'native nonblank ancillary port law nu='+str(nu)+' label='+str(j))
    # Real all128 charge recurrence, one small horizon only; analytically all n.
    cost=np.zeros_like(eye)
    for _ in range(4):
        cost=eye+port+sum((x.conj().T@cost@x for x in k),np.zeros_like(eye))
    require(np.linalg.norm(cost-4*(1+e)*eye)<1e-11,'full128 four-round cost recurrence nu='+str(nu))
    diag[str(nu)]={'A2_scalar':lam,'port_rate':e,'nonblank_label_rate':label_rate,'errors':errs}

# Actual entropy split uses h_phi(p^2,p)=2-p and the whole reduced tape.
u=sp.symbols('u',real=True)
lam=sp.Rational(5,128)*u*u
kappa=4*p**3*lam
label_rate=4*p**2*lam*(1-lam)
target=sp.diff(kappa,u)-(2-p)*sp.diff(label_rate,u)
formula=sp.Rational(5,16)*p**2*u*(p-(2-p)*(1-sp.Rational(5,64)*u*u))
require(sp.simplify(target-formula)==0,'exact remaining reduced-tape entropy-rate derivative target')

ell=math.log((1+math.sqrt(5))/2)
dk=float(delta)
result={'scope':'original DATA16 Fourier block; port cost minus complete coherent E entropy; arbitrary purified input',
        'source_pins':PINS,'checks':len(checks),'check_names':checks,
        'exact_gap_statement':'F_4096(3/5,C2)-F_4096(1/2,C1)>52/25 for all normalized inputs C1,C2',
        'numerical_sharper_lower_bound':4096*dk-math.log(256)/ell,
        'numerical_diagnostics':diag,
        'pointer_rate_equation':'h_red_prime=(5 p^2 nu/16)[p-(2-p)(1-5 nu^2/64)] when C1 rate limit is separately proved',
        'GR_closed':False}
print(json.dumps(result,indent=2,sort_keys=True))
