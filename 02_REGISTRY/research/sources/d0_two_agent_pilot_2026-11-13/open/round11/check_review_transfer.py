#!/usr/bin/env python3
"""Exact single-bit decoding bound and paid all-column inverse of two G."""
import importlib.util,json,sys
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('native_execution',Path(__file__).resolve().parent/'native_execution.py')
n=importlib.util.module_from_spec(spec);sys.modules[spec.name]=n;spec.loader.exec_module(n)
p,a,F,G=n.P,n.A,n.GOLDEN_FIELD,n.G_LOCAL
def eq(x,y=0):return F.from_sympy(s.expand(x-y))==F.zero
def meq(x,y):return x.shape==y.shape and all(eq(z) for z in x-y)
def pos(x):return bool(s.simplify(x>0))
checks=[]
def ck(ok,name):
 if not ok:raise AssertionError(name)
 checks.append(name)
k=1-2*p**6;A=1+3*p**6
q0=p**2;q1=s.Rational(1,2)
x0=A-k*q0;x1=A-k*q1
err=s.cancel((x1*(1-q0)-x0*(1-q1))/(x0+x1))
u=1;v=s.cancel(1-(2-q0-q1)/(x0+x1))
d=lambda x:(1-x)*u+x*v
ck(eq(A,4*p**3+4*p**6),'high-report offset agrees with actual two-G result')
ck(pos(k) and pos(1-k),'gain strictly between zero and one')
ck(pos(x0-x1) and pos(x1) and pos(1-x0),'high-report endpoint order and positive support')
ck(pos(err),'uniform decoding error is strictly positive')
ck(pos(v) and pos(1-v),'minimax endpoint decoder is stochastic')
ck(eq(d(x0)-q0,err) and eq(d(x1)-q1,-err),'candidate attains opposite endpoint errors')
# For arbitrary u,v in [0,1], e0=d(x0)-q0 and e1=d(x1)-q1:
# x1 e0-x0 e1 = u(x1-x0)+x0*q1-x1*q0.
# x1-x0<0 and u<=1 imply >= err*(x0+x1).  Its absolute
# value is <= (x0+x1)*max(|e0|,|e1|).  This proves optimality.
ck(eq(err*(x0+x1),x1*(1-q0)-x0*(1-q1)), 'exact dual lower-bound identity')
ck(eq(A/k-1,5*p**6/k) and pos(5*p**6/k),'unbiased bit inverse takes value above one')

gate=n.Gate
cx=lambda i,j:gate('CX',(i,j))
swap=lambda i,j:(cx(i,j),cx(j,i),cx(i,j))
src=gate('SourceI',(0,1,2));pulse=(gate('G',(3,)),gate('G',(3,)))
inv=swap(0,3)+(src,src,gate('G',(0,)),gate('G',(0,)),src,src)+swap(0,3)
def matrix(word):
 ex=n.Execution(4,(),(),word,n.G_CX_SOURCE_I,0,(1,2))
 return n.word_matrix(ex,max_qubits=4,max_expanded_stages=20)
back=matrix(inv);pulsed=matrix(pulse)
ck(len(inv)==12 and len(pulse)==2,'literal 12-stage routed inverse plus original two G')
ck(meq(back,s.kronecker_product(s.eye(8),G.T**2)),'routed inverse equals G^-2 on all source Spin pointer columns')
ck(meq(back*pulsed,s.eye(16)),'paid 14-stage endpoint restores exact original operator')
ck({op:sum(gt.op==op for gt in pulse+inv) for op in ('G','CX','SourceI')}=={'G':4,'CX':6,'SourceI':4},'all 14 calls accounted by primitive type')
print(json.dumps({'status':'PASS_EXACT','checks':len(checks),'names':checks,
 'matched_H1_interval':[float(s.N(q0,16)),float(q1)],
 'best_one_bit_uniform_error':float(s.N(err,16)),
 'best_one_bit_decoder_u':1.0,'best_one_bit_decoder_v':float(s.N(v,16)),
 'inverse_added_calls':{'G':4,'CX':6,'SourceI':4},
 'scope':'single-bit field-independent decoder; paid all-column inverse endpoint; no full H1 admission or full clock/price',
 'physical_C_discharged':False,'GR_closed':False},indent=2))
