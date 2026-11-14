#!/usr/bin/env python3
"""Exact small all-column analogue: retained first success, site and fair leaves."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

def zero(n):return [[F(0) for _ in range(n)] for _ in range(n)]
def eye(n):
 a=zero(n)
 for i in range(n):a[i][i]=1
 return a
def scale(a,s):return [[s*x for x in row] for row in a]
def plus(a,b):return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def tensor(a,b):return [[a[i//len(b)][j//len(b)]*b[i%len(b)][j%len(b)] for j in range(len(a)*len(b))] for i in range(len(a)*len(b))]
def trans(a):return [list(x) for x in zip(*a)]
def mm(a,b):return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def pair(a,b):
 x=zero(3);x[a][b]=x[b][a]=1
 t=eye(3);t[a][a]=t[b][b]=0;t[a][b]=t[b][a]=1
 # delta=1 gives swap on pair and minus identity elsewhere
 v=scale(eye(3),-1);v[a][a]=v[b][b]=0;v[a][b]=v[b][a]=1
 assert mm(t,t)==eye(3) and mm(v,v)==eye(3) and trans(t)==t and trans(v)==v
 assert scale(plus(t,v),F(1,2))==x
 return x,(t,v)
x01,V01=pair(0,1);x12,V12=pair(1,2);x02,V02=pair(0,2);I=eye(3);I9=eye(9)
# All cap7 first-success histories, with outcomes abort/root/+/- each 1/4.
# Preserve all 7 raw outcomes even after success; all choices equiprobable.
counts=[0,0,0,0]
for hist in product(range(4),repeat=7):
 first=next((x for x in hist if x),0);counts[first]+=1
assert counts==[1,5461,5461,5461]
# Common READY, 2 attempts. Permute actual decoder labels as a function of SITE,
# including which raw symbol denotes abort; both palettes have tau=3/4.
decodes=[(0,1,2,3),(1,2,3,0)]
def label(site,t0,t1):
 d=decodes[site]
 return d[t0] or d[t1]
# Two alternative roots; selected leaf pair uses independent fair delta per copy.
# Site0 root: (X01 ⊗ X12 - X02 ⊗ I)/2.
# Site1 root: (X12 ⊗ X01 - X02 ⊗ I)/2.
roots=[scale(plus(tensor(x01,x12),scale(tensor(x02,I),-1)),F(1,2)),scale(plus(tensor(x12,x01),scale(tensor(x02,I),-1)),F(1,2))]
site_compressed=[];ready_counts=[];histories=[]
for site in range(2):
 result=zero(9);ready=0;labels={0:0,1:0,2:0,3:0}
 for a,b,branch,d0,d1 in product(range(4),range(4),range(2),range(2),range(2)):
  lab=label(site,a,b);labels[lab]+=1
  if not lab:continue
  ready+=1
  if lab==2:S=I9
  elif lab==3:S=scale(I9,-1)
  elif branch:
   S=scale(tensor(V02[d0],I),-1)  # negative constant, identity padding
  else:
   S=tensor((V01 if site==0 else V12)[d0],(V12 if site==0 else V01)[d1])
  assert mm(S,S)==I9 and trans(S)==S
  result=plus(result,scale(S,F(1,128)))
 assert ready==120 and labels=={0:8,1:40,2:40,3:40}
 expected=scale(roots[site],F(15,16*3))
 assert result==expected
 assert scale(result,F(16,15))==scale(roots[site],F(1,3))
 site_compressed.append(result);ready_counts.append(ready);histories.append(labels)
# All-column equality, including off-diagonal input correlations: source operator
# is block diagonal in the shared SITE, and extends by identity to any external R.
M=zero(18);target=zero(18)
for site in range(2):
 for i in range(9):
  for j in range(9):M[site*9+i][site*9+j]=site_compressed[site][i][j];target[site*9+i][site*9+j]=F(15,16*3)*roots[site][i][j]
assert M==target
# On |2,2>, shared delta for the *same* pair gives 1 vs target X⊗X=0.
shared=scale(plus(tensor(V01[0],V01[0]),tensor(V01[1],V01[1])),F(1,2))
independent=tensor(x01,x01)
assert shared[8][8]==1 and independent[8][8]==0
# An explicit arbitrary coherent SITE/data/external state: no inverse preparation.
# Weighted branch overlaps are the h=0/h=1 interference measured in X.
psi=[[(complex((i*3+e*5)%11-5,(i*7+e*2)%13-6)) for e in range(2)] for i in range(18)]
assert psi[0][0]*psi[9][1] != psi[0][1]*psi[9][0]  # entanglement across SITE/data and external
assert sum(psi[0][e]*psi[9][e].conjugate() for e in range(2)) != 0  # coherent SITE off-diagonal
norm=sum(abs(z)**2 for row in psi for z in row)
def expect(A):return sum(psi[i][e].conjugate()*A[i][j]*psi[j][e] for i in range(18) for j in range(18) for e in range(2)).real
raw_overlap=expect(M);expected_overlap=expect(target);assert abs(raw_overlap-expected_overlap)<1e-10
prob_plus=(F(15,16)*norm+raw_overlap)/2
prob_minus=(F(15,16)*norm-raw_overlap)/2
assert abs(prob_plus+prob_minus-F(15,16)*norm)<1e-10
out={'status':'PASS_EXACT_SMALL_RETAINED_HISTORY_OPERATOR_CHECK','full_site_data_dimension':18,'shared_external_spectator_test_dimension':2,'toy_coherent_site_and_external_input_test':True,'cap7_histories':4**7,'cap7_first_success_counts':counts,'toy_two_attempt_ready_probability':'15/16','all_site_data_operator_columns_checked':18,'toy_input_superposition_and_external_entanglement_test':True,'full_space_leaf_involution_identity':True,'identity_padding_and_negative_constant_checked':True,'top_plus_minus_identity_cancellation_checked':True,'unprepare_for_hadamard_effect_required':False,'shared_delta_counterexample_complement_value':str(shared[8][8]),'independent_delta_complement_value':str(independent[8][8]),'scope':'exact toy operator/count enumeration; not an execution of actual A16 or full native circuit','GR_closed':False}
Path(__file__).with_name('COHERENT_TOY_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
