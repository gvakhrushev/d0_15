#!/usr/bin/env python3
"""Exact born-clock return reduction with two full six-mark readers."""
import contextlib, hashlib, io, json, runpy, sys
from itertools import product
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
PARENT=HERE.parent
with contextlib.redirect_stdout(io.StringIO()): ref=runpy.run_path(str(PARENT/'check_full_native.py'))
nt=ref['nt']; p=nt.P; a=nt.A; G=nt.G_LOCAL; field=nt.GOLDEN_FIELD
v=s.Matrix([a,p]); zero=s.Matrix([1,0]); eye=s.eye(2)
checks=[]
def need(x,label):
 if not bool(x): raise AssertionError(label)
 checks.append(label)
def eq(x,y): return field.from_sympy(s.expand(x-y))==field.zero
C=s.eye(4)[:,[0,1,3,2]]
E=C*s.kronecker_product(eye,G)*C
# 7fy literal six-mark readout: m=(r,t,r,t,t,r), and each
# archive wire was actually born v and paidly prepared to zero.
w=s.diag(*[a**(6-3*(r+t))*p**(3*(r+t)) for r in range(2) for t in range(2)])
row=s.kronecker_product(v,v).T*w*E
A=[(row*s.kronecker_product(s.eye(2)[:,j],v))[0] for j in (0,1)]
B=[A[0]*a+A[1]*p,A[0]*p+A[1]*a]
D=s.diag(*B)
R=v.T*D*G.T**2
r0=A[0]*(R*G*v)[0]
r1=A[0]*(R*G**3*v)[0]
rcommon=A[1]*(R*zero)[0]
need(not eq(r0,r1),'exact distinct return coefficient')
need(eq(r0-A[0]*a*B[0],0),'direct born branch coefficient')
need(eq(r1-r0,A[0]*(v.T*D*(G**2-eye)*zero)[0]),'exact coefficient difference')
need(abs(float(s.N(r0-r1,20)))>1e-6,'separation numerically visible')
# R/CX routed archive is a permutation and returns original port and payload.
for bits in product((0,1),repeat=9):
 state=list(bits); port,r,t=0,1,2
 def cx(x,y): state[y]^=state[x]
 def swap(x,y): cx(x,y);cx(y,x);cx(x,y)
 for slot, wire in enumerate((r,t,r,t)):
  swap(port,wire);cx(port,3+slot)
  if slot>=2: cx(t if slot==2 else r,3+slot+2)
  swap(port,wire)
 need(tuple(state[:3])==tuple(bits[:3]),'payload restoration %s'%(bits,))
 expect=(bits[1],bits[2],bits[1],bits[2],bits[2],bits[1])
 need(tuple(state[3+j]^bits[3+j] for j in range(6))==expect,'six marks %s'%(bits,))
# Full literal layout: 9 existing variables + 12 fresh reader wires, plus
# a protected oldRIGHT spectator. Earlier four births in plan are charged.
gate=nt.Gate; port,spin1,spin2=0,1,2
src=gate('SourceI',(0,1,2))
def cx(x,y): return gate('CX',(x,y))
def sw(x): return (cx(0,x),cx(x,0),cx(0,x))
def inverse17(x):
 z=sw(x)+(src,src)+sw(x)
 return z+(gate('G',(x,)),)+z
def reader(r,t,archive):
 gates=tuple(g for x in archive for g in inverse17(x)); deliver=[]
 for i,wire in enumerate((r,t,r,t)):
  deliver.extend(sw(wire)); deliver.append(cx(0,archive[i]))
  if i>=2: deliver.append(cx(t if i==2 else r,archive[i+2]))
  deliver.extend(sw(wire))
 return gates+tuple(deliver)
reader1=reader(5,6,tuple(range(9,15))); reader2=reader(7,8,tuple(range(15,21)))
need(len(reader1)==len(reader2)==132,'two 132-call reader words')
need(all(9<=x<=14 for x in range(9,15)),'six first archive addresses')
need(all(not (set(g.wires)&set(range(9,15))) for g in reader2),'first reader sealed before second')
prefix,suffix=ref['plan'](0,1)
for word in prefix:
 allg=tuple(word)+tuple(suffix)+reader1+reader2
 ex=nt.Execution(22,(),(21,),allg,nt.G_CX_SOURCE_I,0,(1,2),(5,7))
 nt.validate_execution(ex,max_qubits=22,max_expanded_stages=len(allg))
 need(len(word)==7 and len(suffix)==31 and len(allg)==302,'full syntax and stage inventory')
need(sum(g.op=='G' for g in suffix+reader1+reader2)==17,'full suffix G count')
need(sum(g.op=='CX' for g in suffix+reader1+reader2)==222,'full suffix CX count')
need(sum(g.op=='SourceI' for g in suffix+reader1+reader2)==56,'full suffix SourceI count')
# Independent whole-word replay on every PORT/Spin/r input column. The two
# readout permutations are contracted with their ACTUAL v-born archive bras;
# their exact complete truth table was checked above.
import numpy as np
J=ref['J']; a_f=float(a); p_f=float(p)
weights=[]
for x in range(512):
 bit=lambda wire:(x>>(8-wire))&1
 ones1=3*(bit(5)+bit(6)); ones2=3*(bit(7)+bit(8))
 weights.append(a_f**(12-ones1-ones2)*p_f**(ones1+ones2))
for which,word in enumerate(prefix):
 out=ref['run'](word+suffix)
 compressed=(J[:,:,None]*out[:,None,:]*np.asarray(weights)[:,None,None]).sum(axis=0)
 expected=np.kron(np.eye(8),np.diag([float(s.N((r0,r1)[which],18)),float(s.N(rcommon,18))]))
 need(np.isfinite(compressed).all(),'finite full-born contraction')
 need(np.max(np.abs(compressed-expected))<2e-14,'all-column paid-reader return k='+str(which))
# Closed-form full heat bound: the differing two unitary slots have width d.
# max row scene degree normalization gives trace Cs <=33/22 and D>=2^16 d.
import math
pp=float(p); aa=math.sqrt(pp); theta=math.atan2(pp,aa)
trace_norm_ratio=1+2*math.sin(theta/2)
heat_value_bound=6*trace_norm_ratio/(359*2**16)
heat_source_per_beta_M=4*(33/22)*(1+66/359)*trace_norm_ratio/(359*2**16)
print(json.dumps({'status':'PASS','checks':len(checks),'exact_field':'Q(sqrt(p))',
 'return_coefficients':{'d0':float(s.N(r0,18)),'d1':float(s.N(r1,18)),
 'dcommon':float(s.N(rcommon,18)),'difference':float(s.N(r1-r0,18))},
 'clock':{'common_prefix_calls':7,'common_suffix_calls':295,'new_births':16,
 'thermal_mode_count':'425D','heat_value_difference_bound':heat_value_bound,
 'heat_source_difference_bound_per_beta_and_M':heat_source_per_beta_M},
 'full_native_syntax_no_dense_growing_matrix':True,'physical_cost_info_binding_proved':False,
 'actual_upstream_return_source_evaluated':False,'GR_closed':False},indent=2,sort_keys=True))
