#!/usr/bin/env python3
"""Exact two-G NPS report; does not assert original task admission."""
import importlib.util,json,sys
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('native_execution',Path(__file__).resolve().parent/'native_execution.py')
n=importlib.util.module_from_spec(spec);sys.modules[spec.name]=n;spec.loader.exec_module(n)
p,a,F,G=n.P,n.A,n.GOLDEN_FIELD,n.G_LOCAL
I=s.eye;v=s.Matrix([a,p]);P0=s.diag(1,0);P1=s.diag(0,1);g=n.Gate
def eq(x,y):return F.from_sympy(s.expand(x-y))==F.zero
def meq(x,y):return x.shape==y.shape and all(eq(z,0) for z in x-y)
checks=[]
def ck(ok,name):
 if not ok:raise AssertionError(name)
 checks.append(name)
src=g('SourceI',(0,1,2));C=g('CX',(0,3));flip=(g('G',(3,)),g('G',(3,)))
E0=(g('CX',(3,4)),g('G',(4,)),g('CX',(3,4)))
old=(C,src,src)+E0;new=(C,src,src)+flip+E0
def matrix(word):
 ex=n.Execution(5,(),(),word,n.G_CX_SOURCE_I,0,(1,2))
 return n.word_matrix(ex,max_qubits=5,max_expanded_stages=10)
U0,U=matrix(old),matrix(new)
ck(len(old)==6 and len(new)==8 and all(x.op=='G' and x.wires==(3,) for x in flip),'two extra real G calls, no birth or old wire')
ck(meq(G**2,s.Matrix([[p**3,-2*a*p],[2*a*p,p**3]])),'exact original golden G squared')
J=s.kronecker_product(I(8),v,v)
event1=s.kronecker_product(I(8),P1,P0)
bad=s.kronecker_product(I(8),P1,P1)
event0=s.kronecker_product(I(8),P0,I(2))
effect=lambda V,Q:J.T*V.T*Q*V*J
Q=s.kronecker_product(P1,I(4));Eold=p**2*I(8)+p**3*Q
lam=1-2*p**6;const=4*p**3+4*p**6
Ehi=const*I(8)-lam*Eold
ck(meq(effect(U0,event1),Eold),'original NPS effect on all source and spin columns')
ck(meq(effect(U,event1),Ehi),'two-G high report exact effect')
ck(meq(effect(U,bad),s.zeros(8)),'invalid 11 exactly zero on all source spin inputs')
ck(meq(effect(U,event0)+effect(U,event1),I(8)),'both valid output branches complete')
ck(meq(effect(U,event1)-effect(U0,event1),8*p**6*(I(8)-Q)),'original fixed-effect AD1 changes by nonzero operator')
ck(meq(effect(U,event0),I(8)-Ehi),'reversed rare event has complete complementary effect')
ck(eq((v.T*P0*v)[0],p) and eq((v.T*P1*v)[0]*(v.T*P0*v)[0],p**3),'same earliest born code masses p and p cubed')
ck(eq(p+p**3,1-p**4),'passive valid-support mass preserves unread invalid complement')
# Report bounds for the whole E_f in [0,I]; tight endpoint values.
lo=const-lam*p;hi=const-lam*p**2
ck(eq(lo,p),'whole input E_f=1 high report is p')
ck(eq(hi,1-p*(4*p-3)**2),'whole input E_f=0 high report upper endpoint')
ck(bool(s.simplify(lam>0)) and bool(s.simplify(lo>s.Rational(1,2))) and bool(s.simplify(hi<1)), 'strict signs proved in positive golden embedding')
ck(meq(U.T*U,I(32)),'full five-wire native execution is unitary')
# Sharp serializer control: pre-readout branch maps K0,K1 have K0* K1=0,
# so the cross term vanishes, unlike the noisy NPS input.
cs=2*a*p;cc=p**3
ck(eq(cs**2,4*p**3) and eq(cc**2,p**6),'sharp conditional mixing coefficients')
ck(eq(cs**2-cc**2,lam),'sharp and noisy monotonicity slopes coincide')
qmu=p**2/(1+p**2)
ck(bool(s.simplify(4*p**3-lam*qmu>s.Rational(1,2))), 'sharp original event collar also yields high report')
print(json.dumps({'status':'PASS_EXACT','check_count':len(checks),'checks':checks,
 'lambda':float(s.N(lam,16)),'all_input_high_q_range':[float(s.N(lo,16)),float(s.N(hi,16))],
 'h1_matched_high_q_at_Q_half':float(s.N(const-lam/2,16)),
 'source_info_binding_proved':False,'original_H1_AD1_preserved':False,'GR_closed':False},indent=2))
