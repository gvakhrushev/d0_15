#!/usr/bin/env python3
"""Original Q8 controlled programme: record-diagonal blindness and a conditional programme-mixing witness. Not physically selected."""
import math
import numpy as np
p=2/(1+math.sqrt(5)); a=math.sqrt(p); q=4*p**3
assert abs(p**6+q-1)<1e-14
checks=[]
def check(label,flag):
 if not flag:raise AssertionError(label)
 checks.append(label)
# spin index 4, output basis (arm,registered-bit,spin): 2*2*4=16
rid=np.zeros((16,4)); rord=np.zeros((16,4))
for i in range(4):
 rid[i,i]=1
 rord[i,i]=p**3
 rord[12+i,i]=-2*a*p # arm1 record1, index 12+i
check('identity four-spin isometry',np.linalg.norm(rid.T@rid-np.eye(4))<1e-13)
check('order four-spin isometry',np.linalg.norm(rord.T@rord-np.eye(4))<1e-13)
check('exact native p3 cross overlap',np.linalg.norm(rid.T@rord-p**3*np.eye(4))<1e-13)
# U outputs on arbitrary spin k and programme superposition
out_i=rid[:,0];out_o=rord[:,0]
for r in (1.8512395785208469e-6,.1,.37):
 alpha,beta=math.sqrt(1-r),math.sqrt(r)
 pure=alpha*np.kron([1,0],out_i)+beta*np.kron([0,1],out_o)
 rhopure=np.outer(pure,pure)
 rhomix=(1-r)*np.outer(np.kron([1,0],out_i),np.kron([1,0],out_i))+r*np.outer(np.kron([0,1],out_o),np.kron([0,1],out_o))
 check(f'norm pure {r}',abs(np.trace(rhopure)-1)<1e-13)
 check(f'norm mixed {r}',abs(np.trace(rhomix)-1)<1e-13)
 progz=np.kron(np.diag([1.,-1.]),np.eye(16))
 check(f'coherent is genuinely nondiagonal {r}',np.linalg.norm(rhopure-progz@rhopure@progz)>0)
 for E_16 in (np.eye(16),np.diag([1.]*4+[0.]*12),np.diag([0.]*12+[1.]*4)):
  for pp in (np.diag([1,0]),np.diag([0,1])):
   E=np.kron(pp,E_16)
   check(f'classical program/stage/readout effects are coherence blind {r}',abs(np.trace(E@(rhopure-rhomix)))<1e-14)
 X=np.kron(np.array([[0.,1.],[1.,0.]]),np.eye(16))
 expX=float(np.trace(X@rhopure).real)
 check(f'X-program interference exact p3 {r}',abs(expX-2*p**3*alpha*beta)<2e-14)
 check(f'X-program dephased zero {r}',abs(np.trace(X@rhomix))<2e-14)
 G=np.array([[a,-p],[p,a]])
 P0=np.kron(G.T@np.diag([1.,0.])@G,np.eye(16))
 pr=float(np.trace(P0@rhopure).real); mr=float(np.trace(P0@rhomix).real)
 check(f'Golden programme readout interference {r}',abs(pr-mr+2*a*p**4*alpha*beta)<2e-14)
 check(f'Golden no-negativity {r}',0<=pr<=1 and 0<=mr<=1)
 # Equal native Q8 classical (programme,record) pointer laws: id0, order0, order1.
 E=np.array([np.outer(np.kron([1,0],out_i),np.kron([1,0],out_i)),
             np.outer(np.kron([0,1],out_o),np.kron([0,1],out_o))])
 check(f'positive programme population check {r}',abs(np.trace(np.kron(np.diag([1.,0.]),np.eye(16))@rhopure)-(1-r))<2e-14)
print({'status':'PASS','controls':len(checks),'native_p3_overlap':p**3,'at_rare_r':{'r':1.8512395785208469e-6,'X_program_contrast':2*p**3*math.sqrt(1.8512395785208469e-6*(1-1.8512395785208469e-6)),'Golden_readout_contrast':-2*a*p**4*math.sqrt(1.8512395785208469e-6*(1-1.8512395785208469e-6))},'physical_status':'conditional programme mixing; Book03 active cut, M1 access, common initial writer open'})

# Genuine complete-retained-work fork: branch-conditional archive labels are orthogonal.
# The TRUE fully coherent joint state is still pure; its programme reduced state is dephased.
rrare=1.8512395785208469e-6
beta=math.sqrt(rrare);alpha=math.sqrt(1-rrare)
work0=np.array([1.,0.]); work1=np.array([0.,1.]);out_i=rid[:,0];out_o=rord[:,0]
workful_pure=alpha*np.kron(np.kron([1,0],work0),out_i)+beta*np.kron(np.kron([0,1],work1),out_o)
workful_rho=np.outer(workful_pure,workful_pure)
workful_mixed=(1-rrare)*np.outer(np.kron(np.kron([1,0],work0),out_i),np.kron(np.kron([1,0],work0),out_i))+rrare*np.outer(np.kron(np.kron([0,1],work1),out_o),np.kron(np.kron([0,1],work1),out_o))
X=np.array([[0.,1.],[1.,0.]])
Xprog=np.kron(np.kron(X,np.eye(2)),np.eye(16))
Xwork=np.kron(np.kron(np.eye(2),X),np.eye(16))
Xjoint=np.kron(np.kron(X,X),np.eye(16))
check('work-labelled coherent state pure', abs(float(np.trace(workful_rho@workful_rho))-1)<3e-14)
check('work-labelled program-only X exactly zero',abs(np.trace(Xprog@workful_rho))<1e-15)
check('work-labelled work-only X exactly zero',abs(np.trace(Xwork@workful_rho))<1e-15)
check('work-labelled joint X exact native p3 overlap',abs(np.trace(Xjoint@workful_rho)-2*p**3*alpha*beta)<3e-15)
check('work-labelled joint X dephased zero',abs(np.trace(Xjoint@workful_mixed))<1e-15)
G=np.array([[a,-p],[p,a]])
Eprog0=G.T@np.diag([1.,0.])@G
E_G=np.kron(np.kron(Eprog0,np.eye(2)),np.eye(16))
check('even relocated programme-Golden register alone blind for orthogonal work tags',abs(np.trace(E_G@(workful_rho-workful_mixed)))<1e-15)
for proj in (np.diag([1.,0.]),np.diag([0.,1.]),np.eye(2)):
 for prog_op in (Eprog0,X,np.eye(2)):
  E=np.kron(np.kron(prog_op,proj),np.eye(16))
  check('all work-diagonal effects blind to coherent joint source',abs(np.trace(E@(workful_rho-workful_mixed)))<2e-15)
print({'status':'PASS','controls_total':len(checks),'extra':'orthogonal full archive blocks programme-only interference, but joint test would recover p3 coherence','work_orthogonal':True,'program_Golden_contrast':float(np.trace(E_G@(workful_rho-workful_mixed))),'joint_X_contrast':float(np.trace(Xjoint@(workful_rho-workful_mixed)))})
