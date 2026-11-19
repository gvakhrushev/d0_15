#!/usr/bin/env python3
"""Complete 4-label CQ record, retained qubit/oldRIGHT and rank-birth control.

A fixed 3-qubit coherent input and a fixed unitary perturbation. All outcomes
measured on two flag qubits; the third qubit remains as quantum work/reference.
Checks Fannes/Audenaert without any individual probability floor and verifies
that ambient entropy may lack C2, while price-value continuity still holds.
This is a diagnostic CPTP fixture, not the original D0 full128 execution.
"""
from __future__ import annotations
import json
import math
from pathlib import Path
import argparse
import numpy as np

PHI=(1+math.sqrt(5))/2
ELL=math.log(PHI)
checks=[]

def require(ok,label):
    if not bool(ok):
        raise AssertionError(label)
    checks.append(label)

def h_nat(q):
    return -sum(float(x)*math.log(float(x)) for x in q if x>0)

def state(eps):
    psi=np.zeros(8,dtype=complex)
    psi[0]=psi[7]=1/math.sqrt(2)
    x=np.kron(np.array([[0,1],[1,0]]),np.eye(4))
    # This is a true unitary, not a non-CP history tilt.
    return math.cos(eps)*psi+1j*math.sin(eps)*(x@psi)

def recorded(eps):
    psi=state(eps)
    blocks=[]
    for label in range(4):
        w=psi[2*label:2*label+2]
        blocks.append(np.outer(w,w.conj()))
    omega=np.zeros((8,8),dtype=complex)
    for i,block in enumerate(blocks):
        omega[2*i:2*i+2,2*i:2*i+2]=block
    q=np.array([np.trace(b).real for b in blocks])
    oldright=sum(blocks)
    return psi,omega,q,oldright

psi0,omega0,q0,right0=recorded(0.0)
require(np.allclose(q0,[.5,0,0,.5]),'literal two dark complete CQ records')
require(np.linalg.norm(right0-.5*np.eye(2))<1e-13,'oldRIGHT full marginal retained')
require(abs(q0.sum()-1)<1e-14,'complete trace one including dark outcomes')
require(abs(h_nat(q0)-math.log(2))<1e-13,'complete pure-conditional CQ entropy at zero')
charges=np.array([1.,2.,5.,8.])
cmax=float(max(charges))
rows=[]
prev=None
for eps in (.1,.05,.01,.005,.001,.0005):
    psi,omega,q,right=recorded(eps)
    require(np.linalg.norm(right-right0)<1e-12,f'eps{eps}: unchanged complete oldRIGHT average')
    require(q[1]>0 and q[2]>0,f'eps{eps}: both old dark outcomes acquire positive mass')
    require(abs(q.sum()-1)<1e-14,f'eps{eps}: all4 labels exactly normalized')
    # The actual quantum conditional blocks are rank one; no work is erased.
    for b in range(4):
        block=omega[2*b:2*b+2,2*b:2*b+2]
        require(abs(np.trace(block).real-q[b])<1e-14,f'eps{eps}: CQ block trace {b}')
        require(abs(np.linalg.det(block))<1e-15,f'eps{eps}: CQ block rank1 {b}')
    require(np.linalg.norm(omega-omega.conj().T)<1e-13,f'eps{eps}: Hermitian complete CQ')
    qent=h_nat(q)
    ev=np.linalg.eigvalsh(omega)
    require(np.min(ev)>-1e-14,f'eps{eps}: positive complete CQ operator')
    require(abs(h_nat(ev)-qent)<2e-13,f'eps{eps}: full von Neumann CQ entropy')
    tin=math.sqrt(max(0,1-abs(np.vdot(psi0,psi))**2))
    dout=omega-omega0
    tout=np.sum(abs(np.linalg.eigvalsh(dout)))/2
    require(tout<=tin+1e-12,f'eps{eps}: measured CQ trace distance contractive')
    rhs=tin*math.log(7)-tin*math.log(tin)-(1-tin)*math.log(1-tin)
    require(abs(qent-h_nat(q0))<=rhs+1e-12,f'eps{eps}: Fannes without q floor')
    charge=float(charges@q)
    charge0=float(charges@q0)
    price=charge-qent/ELL
    price0=charge0-h_nat(q0)/ELL
    modulus=2*cmax*tin+rhs/ELL
    require(abs(price-price0)<=modulus+1e-12,f'eps{eps}: complete charged-CQ modulus')
    second=(price+price-2*price0)/eps**2
    if prev is not None:
        require(second<prev,f'eps{eps}: rank-birth CQ second secant diverges negative')
    prev=second
    rows.append({'eps':eps,'dark_prob':float(q[1]),'trace_in':tin,'trace_out':float(tout),
                 'entropy_base_phi':qent/ELL,'paid_cost':charge,'full_price':price,
                 'ambient_second_secant':second,'Fannes_bound':rhs/ELL})
require(rows[-1]['ambient_second_secant']<rows[0]['ambient_second_secant']-15,
        'no artificial ambient-C2 assumption through dark-record birth')
result={'status':'PASS_COMPLETE_CQ_RANK_BIRTH_DIAGNOSTIC','checks_count':len(checks),
        'checks':checks,'four_classical_labels_two_quantum_oldright':rows,
        'scope':{'complete_record':True,'retained_quantum_work':True,
                 'no_outcome_probability_floor':True,'ambient_C2_is_false':True,
                 'original_full128_replay':False,'GR_closed':False}}
parser=argparse.ArgumentParser();parser.add_argument('--json',type=Path)
args=parser.parse_args()
s=json.dumps(result,sort_keys=True,indent=2)+'\n'
if args.json: args.json.write_text(s,encoding='utf-8')
print(s,end='')
