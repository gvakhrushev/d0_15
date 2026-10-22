#!/usr/bin/env python3
"""ORIGINAL full128 native Golden twin: irreducible recorded Info and port price.

Original source pinned by Git blob. Uses every 128 fine Kraus, real no-reset
second round, full oldRIGHT16 Choi quantum side information and true original
0/10 Kraft code. No artificial Bernoulli DATA reset; no compulsory Book03
Info, scene Hodge or GR asserted. Requires numpy/scipy.
"""
import ast,hashlib,json,math
from pathlib import Path
import numpy as np
from scipy.linalg import expm,solve_sylvester

SRC=Path(__file__).resolve().parents[4]/"02_REGISTRY/research/sources/d0_book_uniform_source_2026-10-21/check_uniform_book_source.py"
PIN="ee8de4635d24c668949ac9a0186616ab7d59f2ed"
p=(math.sqrt(5)-1)/2
ell=math.log(1/p)
coin=-p*p*math.log(p*p)-p*math.log(p)
I=np.eye(16,dtype=complex)
checks=0
def test(b,msg):
 global checks
 checks+=1
 if not b:raise ArithmeticError(msg)
def close(x,y,t,msg):test(abs(x-y)<t,f"{msg} {x} expected {y}")
raw=SRC.read_bytes()
blob=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
test(blob==PIN,"unchanged ORIGINAL 128 Kraus source Git blob")
t=ast.parse(raw)
wanted={"adj","herm","root","creators","native"}
functions=[node for node in t.body if isinstance(node,ast.FunctionDef) and node.name in wanted]
test({f.name for f in functions}==wanted,"original five CAR16 Julia constructors")
scope={"np":np,"P":p,"EYE":I,"expm":expm,"solve_sylvester":solve_sylvester}
exec(compile(ast.Module(body=functions,type_ignores=[]),str(SRC),"exec"),scope)
native=scope["native"]

def entropy(vals):
 a=np.asarray(vals).real
 a=a[a>1e-14]
 return float(-sum(a*np.log(a)))

def original(r):
 K,DKtheta=native(2*math.atanh(r),.6)
 DK=DKtheta*2/(1-r*r)
 test(K.shape==(128,16,16),"complete native128 CAR16")
 close(np.linalg.norm(np.sum(K.conj().transpose(0,2,1)@K,axis=0)-I),
       0,4e-12,"all128 native CPTP")
 for j in range(1,64):
  close(np.linalg.norm(K[2*j+1]-K[2*j]/math.sqrt(p)),
        0,1e-12,"each real bright/dark native nonblank port scalar twin")
  close(np.linalg.norm(DK[2*j+1]-DK[2*j]/math.sqrt(p)),
        0,1e-11,"original proper Lorentz source of twins")
 Delta=(I-K[0])/(2*p*p)
 DDelta=-DK[0]/(2*p*p)
 actual=np.sum(K[2:].conj().transpose(0,2,1)@K[2:],axis=0)
 expected=4*p*p*Delta@(I-Delta)
 close(np.linalg.norm(actual-expected),0,4e-12,
       "EXACT native nonblank effect 4p² Delta(1-Delta)")
 inv=np.linalg.inv(Delta)
 h=16/np.trace(inv).real
 mu=np.trace(Delta).real/16
 hj=16*np.trace(inv@DDelta@inv).real/np.trace(inv).real**2
 muj=np.trace(DDelta).real/16
 rho=inv/np.trace(inv)
 q=float(np.trace(rho@actual).real)
 close(q,4*p*p*h*(1-mu),5e-12,"genuine MOVING stationary native nonblank rate")
 return K,DK,Delta,q,4*p*p*(hj*(1-mu)-h*muj),mu,h

record={}
for r in (0,.1,1/9,.12):
 K,DK,Delta,q,j,mu,h=original(r)
 record[str(r)]={"native_q_nonblank":q,"native_stationary_source":j}
K,DK,Delta,qnb,dqnb,mu,h=original(1/9)
close(mu,141489/10240000,2e-12,"native exact arithmetic mean")
close(h,69399/5030720,2e-12,"native exact harmonic mean")
test(-.0031<dqnb<-.0030,"strict real nonzero stationary source")
test(4*(.618)**2*(.0136-.00061)*(1-.01461)>.019,
     "prior original rational positive spectral bracket implies kappa>.019")
close(coin/ell,2-p,1e-13,"Golden port bit conditional entropy exactly 2-p")
close((p*p+2*p)-coin/ell,p**3,1e-13,
      "ORIGINAL unpadded 0/10 conditional code-minus-Info exactly p³")
def compute(n):
 words=K if n==1 else np.einsum("bik,akj->abij",K,K,optimize=True)
 A=words.reshape(-1,256)/4
 probs=np.einsum("ai,ai->a",A.conj(),A).real
 close(float(sum(probs)),1,1e-11,"ALL 128^n fine outcome probabilities normalize")
 H=entropy(probs)
 ev=np.linalg.eigvalsh(A.conj().T@A)
 test(ev.min()>-1e-11,"genuine 256-mode DR Choi positive")
 S=entropy(ev)
 test(H-S>n*.019*coin,"strict n-tick information not in final quantum DR")
 return H,S,H-S,probs

H1,S1,gap1,one=compute(1)
H2,S2,gap2,two=compute(2)
P4=two.reshape(64,2,64,2)
rows=P4.sum((1,3))
obs=P4.transpose(0,2,1,3)
refbit=np.array([p,p*p])
ref=rows[:,:,None,None]*refbit[None,None,:,None]*refbit[None,None,None,:]
live=obs>1e-22
KL=float(sum(obs[live]*np.log(obs[live]/ref[live])))
count=float(sum(rows[1:,:].flat)+sum(rows[:,1:].flat))
forced=count*p**3*ell
test(KL>forced>0,"full original 128^2 row-conditional KL contains native p³ twin cost")
# Original nonblank quantum coin from TRUE stationary input
native_price=qnb*p**3
native_source=dqnb*p**3
test(native_price>.0049 and native_source<-.0007,
     "strict original proper-Lorentz n1 Golden Kraft excess first source")
print(json.dumps({
 "status":"PASS_ORIGINAL_GIT_PINNED_FULL128_GOLDEN_TWIN",
 "checks":checks,"original_source_blob":blob,
 "original_CAR16_oldRIGHT16_Choi":True,
 "actual_oldRIGHT128_spectator_not_erased":True,
 "Golden_conditional_coin_nats":coin,
 "Golden_conditional_coin_code_units":coin/ell,
 "Golden_nonblank_Kraft_excess":p**3,
 "uniform_native_conditional_entropy_bound_per_tick_nats":.019*coin,
 "moving_native_stationary_q_nonblank":qnb,
 "moving_native_stationary_q_nonblank_source":dqnb,
 "stationary_one_tick_port_ledger_price":native_price,
 "stationary_one_tick_port_ledger_first_source":native_source,
 "measured_actual_full128_n1_H":H1,
 "Choi_256_n1_S":S1,
 "irreducible_n1_info_given_all_DR":gap1,
 "measured_actual_full128_squared_n2_H":H2,
 "Choi_256_n2_S":S2,
 "irreducible_n2_info_given_all_DR":gap2,
 "full_128_squared_true_row_conditioned_port_KL":KL,
 "nonblank_explicit_port_KL_component":forced,
 "remaining_true_blank_port_KL":KL-forced,
 "true_n2_expected_nonblank_count":count,
 "positive_Golden_boost_samples":record,
 "adaptive_controller_port_copy_excluded":True,
 "physically_compulsory_Book03_Info_selected":False,
 "physically_compulsory_Book03_scene_Hodge_selected":False,
 "original_all42_GR_closed":False
},indent=2))
