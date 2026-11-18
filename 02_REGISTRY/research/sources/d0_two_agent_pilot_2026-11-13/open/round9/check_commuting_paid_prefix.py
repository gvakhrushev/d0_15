#!/usr/bin/env python3
"""Exact native commuting gates: equal endpoint and distinct born prefixes."""
import importlib.util,json,sys
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('native_execution',Path(__file__).resolve().parent/'native_execution.py')
n=importlib.util.module_from_spec(spec);sys.modules[spec.name]=n;spec.loader.exec_module(n)
p,a,F,G=n.P,n.A,n.GOLDEN_FIELD,n.G_LOCAL
v=s.Matrix([a,p]);I=s.eye;Z1=s.diag(0,1)
def eq(x,y):return F.from_sympy(s.expand(x-y))==F.zero
def meq(x,y):return x.shape==y.shape and all(eq(t,0) for t in x-y)
passed=[]
def ck(ok,label):
 if not ok:raise AssertionError(label)
 passed.append(label)
cx=n.Gate('CX',(0,3));src=n.Gate('SourceI',(0,1,2))
def matrix(word):
 e=n.Execution(4,(),(),word,n.G_CX_SOURCE_I,0,(1,2))
 return n.word_matrix(e,max_qubits=4,max_expanded_stages=8)
C,S=matrix((cx,)),matrix((src,))
ck(meq(C*S,S*C),'native SourceI and CX commute on all 16 columns')
w1,w2=(cx,src,src),(src,cx,src)
U1,U2=matrix(w1),matrix(w2)
ck(meq(U1,U2),'two chronological three-call words have same full endpoint')
ck({op:sum(g.op==op for g in w1) for op in ('CX','SourceI')}=={'CX':1,'SourceI':2},'literal paid gate inventory one CX and two SourceI')
ck(sorted(g.op for g in w1)==sorted(g.op for g in w2),'equal primitive inventory and stage count')
J=s.kronecker_product(I(8),v)
Pr=s.kronecker_product(I(8),Z1)
EC=J.T*C.T*Pr*C*J;ES=J.T*S.T*Pr*S*J
ck(meq(ES,p**2*I(8)),'source-first prefix report effect is p squared on all inputs')
ck(meq(EC,p**2*I(8)+p**3*s.kronecker_product(Z1,I(4))),'CX-first prefix report effect exposes source-port population')
ck(meq(EC-ES,p**3*s.kronecker_product(Z1,I(4))),'prefix effect gap exact positive source projector')
ck(eq((v.T*Z1*v)[0],p**2),'toy canonical source-port population')
ck(eq(p**3*(v.T*Z1*v)[0],p**5),'born-source prefix gap is p to fifth')
ck(eq((p**2+p**5)-p**2,p**5),'prefix contrast sign')
# Existing E0 suffix is exactly three paid native gates; no new readout is
# asserted admissible inside a particular fixed-clock H1 task.
X=s.Matrix([[0,1],[1,0]])
CC=s.diag(I(2),X)
E0=CC*s.kronecker_product(I(2),G)*CC
Jt=s.kronecker_product(I(2),v)
label10=s.diag(0,0,1,0)
invalid11=s.diag(0,0,0,1)
ck(meq(Jt.T*E0.T*label10*E0*Jt,Z1),'owned E0 maps valid 10 mark to the same prior r effect')
ck(meq(Jt.T*E0.T*invalid11*E0*Jt,s.zeros(2)),'owned E0 invalid mark is zero on born tail')
# Endpoint feedback on the same unchanged proper cut P is identical, for
# every supplied P, because the two full operators are literally equal.
P=s.kronecker_product(I(8),s.diag(1,0))
F1=P*U1.T*(I(16)-P)*U1*P
F2=P*U2.T*(I(16)-P)*U2*P
ck(meq(F1,F2),'same-cut feedback operators identical on explicit nontrivial cut')
ck(meq(F1,s.kronecker_product(Z1,I(4),s.diag(1,0))),'the compared feedback is nonzero and retains all spin columns')
print(json.dumps({'status':'PASS_EXACT','check_count':len(passed),'checks':passed,
 'born_port_prefix_gap':float(s.N(p**5,16)),
 'scope':'finite native source-I code; earlier optional test needs actual H1 timing and payment',
 'physical_price_preserving_map_proved':False,'physical_C_discharged':False,'GR_closed':False},indent=2))
