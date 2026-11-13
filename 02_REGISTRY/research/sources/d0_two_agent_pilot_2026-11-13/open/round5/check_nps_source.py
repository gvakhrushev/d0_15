#!/usr/bin/env python3
"""Exact NPS branch cut, prior-prefix hostile control, uniform q-source sign."""
import contextlib,io,json,runpy,sys
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
root=Path(__file__).resolve().parents[1]
with contextlib.redirect_stdout(io.StringIO()): d=runpy.run_path(str(root/'round3/check_rc3.py'))
nt=d['nt']; F=nt.GOLDEN_FIELD;p=nt.P;a=nt.A;G=nt.G_LOCAL;v=s.Matrix([a,p]); I=s.eye(4)
u=(a+p)/2; w=(a-p)/2; S=p**3
checks=[]
def need(c,n):
 if not bool(c):raise AssertionError(n)
 checks.append(n)
def eq(x,y):return F.from_sympy(s.expand(x-y))==F.zero
def meq(X,Y):return X.shape==Y.shape and all(eq(z,0) for z in X-Y)
# Rigorous rational enclosure of the positive real a: a^4+a^2-1=0.
N=10**30; low=0; high=N
while high-low>1:
 mid=(low+high)//2
 if mid**4+mid**2*N**2-N**4<=0:low=mid
 else:high=mid
lo=s.Rational(low,N);hi=s.Rational(high,N)
def lower_exact(x):
 v=F.from_sympy(x) if not hasattr(x,'to_list') else x
 cs=v.to_list(); out=s.Rational(0)
 for i,c in enumerate(cs):
  c=s.Rational(int(c.numerator),int(c.denominator));k=len(cs)-1-i
  out+=c*(lo**k if c>=0 else hi**k)
 return out
def positive(x,name):need(lower_exact(x)>0,name)
positive(a,'positive golden radical'); positive(w,'u minus d direction nondegenerate')
positive(1-S,'golden s lies below one'); positive(2*u-S*w,'positive first-derivative numerator')
need(eq(1-2*p**2,p**3),'original q and reflection c identity')
H0=[d['H00'],d['H10']];H1=d['H1']
wrong_H1=d['mu1']*d['coeff'](v.T,d['tau1'])
need(meq(s.diag(1,0)*v,a*s.Matrix([1,0])),'early b1 reference is a|0>')
need(not eq(wrong_H1,H1),'unprojected b1 reference changes marked h')
for i,H in enumerate(H0):
 A=F.from_sympy(H)*F.from_sympy(p);B=F.from_sympy(H1)*F.from_sympy(p**2)
 uf=F.from_sympy(u);df=F.from_sympy(w);sf=F.from_sympy(S);one=F.one
 margin=A*(2*uf-sf*df)/(one+sf)**2-B*(2*uf)/(one-sf)**2
 positive(margin,'uniform derivative margin word '+str(i))
 lower=(4*df/sf)*margin
 positive(lower-F.from_sympy(s.Rational(3,10000)),'uniform -dh/dq exceeds 3/10000 word '+str(i))
# Native cut witness: arbitrary Spin4, canonical port and pointer born v;
# G^3 is a real earlier prefix; SourceI^2=Z on its live source port.
g=nt.Gate; exe=nt.Execution(4,(),(),(g('G',(0,)),)*3+(g('CX',(0,3)),)+(g('SourceI',(0,1,2)),)*2,nt.G_CX_SOURCE_I,0,(1,2))
U=nt.word_matrix(exe,max_qubits=4,max_expanded_stages=6)
J=s.kronecker_product(v,I,v);P0=s.kronecker_product(s.eye(8),s.diag(1,0));P1=s.kronecker_product(s.eye(8),s.diag(0,1))
X0=J.T*P0*U*J;X1=J.T*P1*U*J
Z=s.diag(1,-1);phys=G**3*v
CW=(v.T*Z*phys)[0];CV=(v.T*phys)[0];Q=phys[1]**2
need(meq(X0,a*(u*CW+w*CV)*I),'X0 exact cross compression on all Spin columns')
need(meq(X1,p*(u*CW-w*CV)*I),'X1 exact cross compression on all Spin columns')
need(not eq(CV,1),'old physical input is not the passive born input')
need(not eq(CW,1-2*Q),'event expectation is not cross compression')
positive(Q,'toy original event Q positive');positive(s.Rational(1,2)-Q,'toy original event Q below half')
q=p**2+p**3*Q
need(meq(J.T*U.T*P1*U*J,q*I),'actual noisy report effect q on all Spin columns')
positive(q-p**2,'toy noisy q above p^2');positive(s.Rational(1,2)-q,'toy noisy q below half')
print(json.dumps({'status':'PASS','checks':len(checks),'golden_a_rational_interval':[str(lo),str(hi)],
 'uniform_minus_dh_dq_lower_bound':'3/10000 (both words, matched scalar branch)',
 'early_b1_reference_H1':float(s.N(H1,20)),'incorrect_unprojected_H1':float(s.N(wrong_H1,20)),
 'toy':{'Q':float(s.N(Q,20)),'q':float(s.N(q,20)),
 'C_W_cross':float(s.N(CW,20)),'C_V_cross':float(s.N(CV,20)),
 '1_minus_2Q':float(s.N(1-2*Q,20))},
 'toy_scope':'native four-wire source frame; not full geometric H1 admission',
 'whole_history_physical_scalar_binding_proved':False,'GR_closed':False},indent=2,sort_keys=True))
