#!/usr/bin/env python3
"""Four-label complete CQ entropy rank-birth control, with retained oldRIGHT.

Author diagnostic CPTP fixture (not a native full128 replay). The initial
GHZ-like three-qubit state is perturbed by a true fixed unitary, two flag
qubits are measured and the third is retained as quantum work/reference.
No individual record-probability floor or ambient C2 hypothesis is imposed.
"""
from __future__ import annotations
import json,math,argparse
from pathlib import Path
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
require(np.allclose(q0,[.5,0,0,.5]),'two initially dark complete CQ records')
require(np.linalg.norm(right0-.5*np.eye(2))<1e-13,'oldRIGHT complete marginal')
require(abs(q0.sum()-1)<1e-14,'complete normalized output')
require(abs(h_nat(q0)-math.log(2))<1e-13,'complete baseline entropy')
charges=np.array([1.,2.,5.,8.])
cmax=float(max(charges))
rows=[]
prev=None
for eps in (.1,.05,.01,.005,.001,.0005):
    psi,omega,q,right=recorded(eps)
    require(np.linalg.norm(right-right0)<1e-12,f'eps{eps}: oldRIGHT retained in average')
    require(q[1]>0 and q[2]>0,f'eps{eps}: dark outcomes born')
    require(abs(q.sum()-1)<1e-14,f'eps{eps}: normalized four labels')
    for b in range(4):
        block=omega[2*b:2*b+2,2*b:2*b+2]
        require(abs(np.trace(block).real-q[b])<1e-14,f'eps{eps}: trace block {b}')
        require(abs(np.linalg.det(block))<1e-15,f'eps{eps}: pure conditional block {b}')
    require(np.linalg.norm(omega-omega.conj().T)<1e-13,f'eps{eps}: CQ Hermitian')
    qent=h_nat(q)
    ev=np.linalg.eigvalsh(omega)
    require(np.min(ev)>-1e-14,f'eps{eps}: CQ positive')
    require(abs(h_nat(ev)-qent)<2e-13,f'eps{eps}: full quantum CQ entropy')
    tin=math.sqrt(max(0,1-abs(np.vdot(psi0,psi))**2))
    tout=np.sum(abs(np.linalg.eigvalsh(omega-omega0)))/2
    require(tout<=tin+1e-12,f'eps{eps}: complete CQ contractivity')
    rhs=tin*math.log(7)-tin*math.log(tin)-(1-tin)*math.log(1-tin)
    require(abs(qent-h_nat(q0))<=rhs+1e-12,f'eps{eps}: entropy floor-free bound')
    charge=float(charges@q)
    charge0=float(charges@q0)
    price=charge-qent/ELL
    price0=charge0-h_nat(q0)/ELL
    modulus=2*cmax*tin+rhs/ELL
    require(abs(price-price0)<=modulus+1e-12,f'eps{eps}: complete paid CQ modulus')
    second=2*(price-price0)/eps**2
    if prev is not None:
        require(second<prev,f'eps{eps}: divergent negative ambient CQ second secant')
    prev=second
    rows.append({'eps':eps,'dark_prob':float(q[1]),
                 'trace_in':tin,'trace_out':float(tout),
                 'entropy_base_phi':qent/ELL,
                 'paid_cost':charge,'full_price':price,
                 'ambient_second_secant':second,
                 'Fannes_bound':rhs/ELL})
require(rows[-1]['ambient_second_secant']<rows[0]['ambient_second_secant']-15,
        'ambient C2 at rank birth is false')
result={'status':'PASS_COMPLETE_CQ_RANK_BIRTH_DIAGNOSTIC',
        'checks_count':len(checks),'checks':checks,'examples':rows,
        'scope':{'full_CQ_record':True,'retained_quantum_work':True,
                 'zero_record_probs_at_base':True,'ambient_C2_false':True,
                 'original_full128_replay':False,'GR_closed':False}}
parser=argparse.ArgumentParser()
parser.add_argument('--json',type=Path)
args=parser.parse_args()
payload=json.dumps(result,sort_keys=True,indent=2)+'\n'
if args.json:
    args.json.write_text(payload,encoding='utf-8')
print(payload,end='')
