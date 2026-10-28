#!/usr/bin/env python3
"""Actual Golden/SourceI echo family and finite-source secants.
A native finite eight-coordinate example, NOT the whole CAR/READY programme.
Large run-length words are verified by product identities, not expanded gates.
"""
import json, math
import numpy as np
import sympy as sp
import mpmath as mp
mp.mp.dps=90
mp.iv.dps=70
p=(mp.sqrt(5)-1)/2
alpha=mp.atan(mp.sqrt(p))
z=mp.mpf(2)**-20
rank=4*128
checks=0

def ck(ok,label):
 global checks
 checks+=1
 if not bool(ok):raise AssertionError(label)

ps=(sp.sqrt(5)-1)/2
G=sp.Matrix([[sp.sqrt(ps),-ps],[ps,sp.sqrt(ps)]])
Li=sp.Matrix([[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]])
X=sp.diag(sp.eye(4),Li)
G8=sp.kronecker_product(G,sp.eye(4))
Z=X*X
ck(all(sp.simplify(q)==0 for q in Z*G8*Z-G8.T),'full8-column forward inverse XXGXX')
ck(Z==sp.diag(sp.eye(4),-sp.eye(4)),'actual SourceI squared is the marking reflection')
# Irrational angle certificate: 2 cos(2 alpha)=2sqrt5-4 has a conjugate < -2.
y=sp.symbols('y')
ck(sp.expand((y+4)**2-20)==y*y+8*y-4,'angle minimal polynomial')
ck(-4-2*sp.sqrt(5)<-2,'conjugate excludes rational angle/pi')
# Exact product scope: for ANY k, inverse uses XXGXX k times;
# monodromy=(G8^T)^k Z G8^k and hence has four +/- eigenvalues.
# Verify literal expanded native words for small k, all full8 columns.
g=np.array(G8.evalf(17),float);x=np.array(X,float);zz=np.array(Z,float)
for k in [0,1,2,5,9]:
 U=np.eye(8)
 for _ in range(k):U=g@U
 for _ in range(2):U=x@U
 for _ in range(k):
  for gate in [x,x,g,x,x]:U=gate@U
 target=np.linalg.matrix_power(g.T,k)@zz@np.linalg.matrix_power(g,k)
 ck(np.max(abs(U-target))<2e-13,'literal finite native inverse/mark sequence')
 ck(np.max(abs(U@U-np.eye(8)))<3e-13,'native full-column echo involution')

# Deterministic search of Golden powers. High-precision verification follows.
def compile_rotation(target,delta,max_k=30000000):
 aa=float(alpha);tt=float(target);best=(float('inf'),None)
 for start in range(0,max_k+1,250000):
  end=min(start+250000,max_k+1)
  ks=np.arange(start,end,dtype=np.float64)
  err=np.abs(np.remainder(ks*aa-tt+math.pi,2*math.pi)-math.pi)
  idx=int(np.argmin(err));v=float(err[idx]);k=start+idx
  if v<best[0]:best=(v,k)
  if v < .8*float(delta):
   dd=mp.fmod(mp.mpf(k)*alpha-target+mp.pi,2*mp.pi)-mp.pi
   if dd>mp.pi:dd-=2*mp.pi
   if dd<-mp.pi:dd+=2*mp.pi
   op=2*abs(mp.sin(dd/2))
   if op<delta:return k,op
 raise ArithmeticError(('no search claim beyond explicit budget',best,mp.nstr(delta)))

def J(t):return -rank*mp.log1p(-z*mp.sin(2*t)**2)
t0=mp.mpf('0.2');true=mp.diff(J,t0)
rows=[]
for m in [3,4,5]:
 tau=mp.mpf(2)**(-m);delta=tau**3/128
 kp,ep=compile_rotation(t0+tau,delta)
 km,em=compile_rotation(t0-tau,delta)
 iv=mp.iv; pi=(iv.sqrt(5)-1)/2; ai=iv.atan2(pi,iv.sqrt(pi))
 ti=iv.mpf(1)/(2**m); di=ti**3/128
 epi=2*abs(iv.sin((kp*ai-(iv.mpf('0.2')+ti))/2))
 emi=2*abs(iv.sin((km*ai-(iv.mpf('0.2')-ti))/2))
 ck(epi<di and emi<di,'outward interval full operator approximation')
 # SAME inventory across this paid comparison: count all idle stages.
 # Forward V padded to kmax; actual inverse has 5 slots per original G,
 # and 5 idle slots for a padded identity, plus two marking SourceI calls.
 kmax=max(kp,km);clock=6*kmax+2
 native=(J(kp*alpha)-J(km*alpha))/(2*tau)
 ideal=(J(t0+tau)-J(t0-tau))/(2*tau)
 # Pure-state trace distance <= 2 delta, projector probability error <=2delta.
 # Full return price Lipschitz in q <=4 rank z/(1-z).
 bound=8*rank*z*max(ep,em)/((1-z)*tau)
 ck(abs(native-ideal)<bound,'explicit compiled secant error bound')
 rows.append({'tau':str(tau),'target_rotation_tolerance':mp.nstr(delta,25),
  'k_plus':kp,'k_minus':km,'common_paid_clock':clock,
  'full8_operator_error_plus':mp.nstr(ep,25),'full8_operator_error_minus':mp.nstr(em,25),
  'operator_error_plus_interval':str(epi),'operator_error_minus_interval':str(emi),
  'compiled_source':mp.nstr(native,35),'ideal_derivative':mp.nstr(true,35),
  'compiled_source_error':mp.nstr(abs(native-true),30),
  'compiler_only_source_bound':mp.nstr(bound,30),
  'ideal_central_difference_error':mp.nstr(abs(ideal-true),30)})
ck(all(mp.mpf(rows[i+1]['compiled_source_error'])<mp.mpf(rows[i]['compiled_source_error']) for i in range(2)),
 'native finite secant convergence in executed three depths')
print(json.dumps({'status':'PASS_NATIVE_GOLDEN_ECHO_SECANTS','checks':checks,
 'palette':['G_phi on port','SourceI=diag(I4,L_i)'],
 'inverse_word':'SourceI SourceI G SourceI SourceI',
 'full_fibre_dimension':8,'RIGHT_spectator':128,
 'small_expanded_native_words_checked':True,
 'large_run_length_words_checked_by_power_identities':True,
 'large_expanded_gate_stream_executed':False,
 'original_gravity_programme_compiled':False,
 'rows':rows,'unconditional_GR_closed':False},indent=2))
