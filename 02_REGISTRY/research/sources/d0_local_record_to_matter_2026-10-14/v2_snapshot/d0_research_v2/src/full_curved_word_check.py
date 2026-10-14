"""Exact integer checks: the FULL adjacent-grade D^2 from golden pair comparisons.
Includes noncommuting returns and the complete 16-grade exterior fibre.
Integer coefficients are twice the real word coefficients. No sampling of signs.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[1]
checks=[];negative=[]
def ck(n,b):
    if not bool(b):raise AssertionError(n)
    checks.append(n)
def eq(n,A,B):ck(n,np.array_equal(A,B))
def reject(n,A,B):ck('REJECT_'+n,not np.array_equal(A,B));negative.append(n)
def c(r):
    a=np.zeros((16,16),dtype=np.int64)
    for mask in range(16):
        if not mask&(1<<r):a[mask|(1<<r),mask]=(-1)**((mask&((1<<r)-1)).bit_count())
    return a
C=[c(r) for r in range(4)];If=np.eye(16,dtype=np.int64)
X=np.array([[0,1],[1,0]],dtype=np.int64);Z=np.diag([1,-1]).astype(np.int64)
# Two genuine noncommuting coefficient returns. Other two returns retained as identity.
Ls=[X,Z,np.eye(2,dtype=np.int64),np.eye(2,dtype=np.int64)]
T=[np.kron(t,If) for t in Ls];Cs=[np.kron(np.eye(2,dtype=np.int64),ci)for ci in C]
I=np.eye(32,dtype=np.int64)
for i in range(4):
 for j in range(4):eq(f'CAR_{i}_{j}',Cs[i]@Cs[j].T+Cs[j].T@Cs[i],int(i==j)*I)
d=sum((ci@(t-I) for ci,t in zip(Cs,T)),np.zeros((32,32),dtype=np.int64))
D=d+d.T;Delta=D@D
words=[];coef=[]
for r,(ci,t) in enumerate(zip(Cs,T)):
 beta=ci+ci.T;gam=ci-ci.T
 eq(f'beta_unitary_{r}',beta.T@beta,I);eq(f'gamma_unitary_{r}',gam.T@gam,I)
 wr=[beta@t,gam@t,t.T@beta,t.T@gam,beta]
 words.extend(wr);coef.extend([1,1,1,-1,-2])
 for j,w in enumerate(wr):eq(f'unitary_word_{r}_{j}',w.T@w,I)
eq('twenty_words_equal_actual_D',sum((n*w for n,w in zip(coef,words)),np.zeros_like(I)),2*D)
ck('zero_coefficient_sum',sum(coef)==0)
rec=np.zeros_like(I)
for j in range(20):
 for k in range(j+1,20):
  diff=words[j]-words[k];K=diff.T@diff
  rec-=coef[j]*coef[k]*K
  ck(f'pair_difference_symmetric_{j}_{k}',np.array_equal(K,K.T))
eq('all190_pairs_equal_full_D_square',rec,4*Delta)
ck('integer_arithmetic_safe',np.max(np.abs(rec))<10**6)
scalar=sum(((t-I).T@(t-I) for t in T),np.zeros_like(I))
reject('drop_noncommuting_curvature_terms',Delta,scalar)
ck('actual_nonzero_d_square',np.any(d@d))
# General CAR expansion: here coefficient returns commute with the Fock factors,
# but NOT with one another. All curvature terms are kept.
W=[t-I for t in T]
curv=np.zeros_like(I)
for r in range(4):
 for q in range(4):curv+=Cs[r]@Cs[q].T@(W[r]@W[q].T-W[q].T@W[r])
for r in range(4):
 for q in range(r+1,4):
  curv+=Cs[r]@Cs[q]@(W[r]@W[q]-W[q]@W[r])
  curv+=Cs[r].T@Cs[q].T@(W[r].T@W[q].T-W[q].T@W[r].T)
eq('complete_curvature_identity',Delta,scalar+curv)
# Independent first derivative on a real orthogonal return, full D, all words.
A=np.array([[0,-1],[1,0]],dtype=np.int64)
dT=[np.kron(A@Ls[0],If)]+[np.zeros_like(I)for _ in range(3)]
dd=sum((ci@dt for ci,dt in zip(Cs,dT)),np.zeros_like(I));dD=dd+dd.T
dwords=[]
for ci,t,dt in zip(Cs,T,dT):
 beta=ci+ci.T;gam=ci-ci.T
 dwords.extend([beta@dt,gam@dt,dt.T@beta,dt.T@gam,np.zeros_like(I)])
drec=np.zeros_like(I)
for j in range(20):
 for k in range(j+1,20):
  f=words[j]-words[k];df=dwords[j]-dwords[k]
  drec-=coef[j]*coef[k]*(df.T@f+f.T@df)
eq('actual_link_first_variation_kept',drec,4*(dD@D+D@dD))
reject('freeze_return_variations',np.zeros_like(I),drec)
# Ten Gram components on the abelian reference, operator identities not moment fits.
U=[np.kron(X,np.eye(2,dtype=np.int64)),np.kron(np.eye(2,dtype=np.int64),X)]
J=np.eye(4,dtype=np.int64)
for r in range(2):
 for q in range(r+1,2):
  wr,wq=U[r]-J,U[q]-J
  K_r=wr.T@wr;K_q=wq.T@wq;K_rq=(U[r]-U[q]).T@(U[r]-U[q])
  eq('cross_Gram_from_pairwise_errors',wr.T@wq+wq.T@wr,K_r+K_q-K_rq)
# Second control: genuine degree-preserving exterior lifts of proper spatial
# rotations. These returns no longer commute with the matching CAR creators.
def exterior_signed_permutation(F):
    result=np.zeros((16,16),dtype=np.int64)
    for mask in range(16):
        r=[];sgn=1
        for i in range(4):
            if mask&(1<<i):
                nz=np.flatnonzero(F[:,i]);ck('signed_permutation_column',len(nz)==1)
                j=int(nz[0]);r.append(j);sgn*=int(F[j,i])
        sgn*=(-1)**sum(r[i]>r[j]for i in range(len(r))for j in range(i+1,len(r)))
        result[sum(1<<j for j in r),mask]=sgn
    return result
R12=np.eye(4,dtype=np.int64);R12[1,1]=R12[2,2]=0;R12[1,2]=-1;R12[2,1]=1
R23=np.eye(4,dtype=np.int64);R23[2,2]=R23[3,3]=0;R23[2,3]=-1;R23[3,2]=1
E12=exterior_signed_permutation(R12);E23=exterior_signed_permutation(R23)
Tf=[E12,E12,E23,If]
df=sum((ci@(tr-If)for ci,tr in zip(C,Tf)),np.zeros_like(If))
Df=df+df.T;Deltaf=Df@Df
wf=[];cf=[]
for ci,tr in zip(C,Tf):
    beta=ci+ci.T;gam=ci-ci.T
    wr=[beta@tr,gam@tr,tr.T@beta,tr.T@gam,beta]
    wf.extend(wr);cf.extend([1,1,1,-1,-2])
    for w in wr:eq('exterior_word_unitary',w.T@w,If)
rf=np.zeros_like(If)
for j in range(20):
    for k in range(j+1,20):
        diff=wf[j]-wf[k];rf-=cf[j]*cf[k]*(diff.T@diff)
eq('actual_SO3_exterior_returns_full_D_square',rf,4*Deltaf)
reject('exterior_return_commutes_with_creator',C[1]@Tf[1],Tf[1]@C[1])
badwords=[]
for ci,tr in zip(C,Tf):
    beta=ci+ci.T;gam=ci-ci.T
    badwords.extend([beta@tr,gam@tr,beta@tr.T,gam@tr.T,beta])
reject('reverse_adjoint_word_order_is_harmless',sum((v*w for v,w in zip(cf,badwords)),np.zeros_like(If)),2*Df)
out={'status':'PASS','exact_controls':len(checks),'checks':checks,
     'executed_negative_claims':negative,'word_count':20,'pair_count':190,
     'full_dimension':32,'Fock_dimension':16,
     'coefficient_returns_commute':False,'full_curvature_retained':True,
     'native_physical_admission':False,'physical_Ward_GR':False,'additional_actual_exterior_rotation_control':True}
(R/'results/full_curved_words.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS_FULL_CURVED_WORDS',len(checks),'controls;',len(negative),'negative claims')
