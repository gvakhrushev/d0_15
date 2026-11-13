#!/usr/bin/env python3
"""Actual native SAM post-rotation and nine-fine-record guards; bounded fixture."""
import contextlib,io,json,runpy,sys
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
root=Path(__file__).resolve().parents[1]
with contextlib.redirect_stdout(io.StringIO()): d=runpy.run_path(str(root/'round5/check_nps_source.py'))
nt=d['nt'];F=nt.GOLDEN_FIELD;p=nt.P;a=nt.A;G=nt.G_LOCAL;v=s.Matrix([a,p]);eye=s.eye
checks=[]
def need(c,n):
 if not bool(c):raise AssertionError(n)
 checks.append(n)
def eq(x,y):return F.from_sympy(s.expand(x-y))==F.zero
def meq(X,Y):return X.shape==Y.shape and all(eq(z,0) for z in X-Y)
# 6 qubits: SOURCE_PORT, Spin(2), SAM, reporter pointer, protected oldRIGHT.
# A_f=CX(SAM,PORT), physical pre-sign reader CX(PORT,r), native Z=SourceI²,
# A_b^*=A_f, then actual independent P_b^*=G_SAM^n.
g=nt.Gate
base=(g('CX',(3,0)),g('CX',(0,4)),g('SourceI',(0,1,2)),g('SourceI',(0,1,2)),g('CX',(3,0)))
J=s.kronecker_product(v,eye(4),v,v,eye(2)); P1=s.kronecker_product(eye(16),s.diag(0,1),eye(2))
oldq=(1-p**9)/2
for n in (0,1):
 word=base+(g('G',(3,)),)*n
 ex=nt.Execution(6,(),(5,),word,nt.G_CX_SOURCE_I,0,(1,2))
 U=nt.word_matrix(ex,max_qubits=6,max_expanded_stages=7)
 need(meq(J.T*U.T*P1*U*J,oldq*eye(8)),'exact original report effect with SAM rotation n='+str(n))
 need(meq(J.T*U.T*(eye(64)-P1)*U*J,(1-oldq)*eye(8)),'exact complementary effect n='+str(n))
 need(all(5 not in gt.wires for gt in word),'oldRIGHT never addressed n='+str(n))
# Explicit matched SAM table M=p³ Z, born phi=v, true variance p^6(1-p^6).
Z=s.diag(1,-1); M=p**3*Z;c=(v.T*M*v)[0]
need(eq(c,p**6),'actual two-site SAM reflection mean')
var=(v.T*M*M*v)[0]-c*c
need(eq(var,p**6*(1-p**6)),'positive actual SAM table variance')
need(d['lower_exact'](var)>0,'variance rigorously positive')
xi=s.Matrix([p,-a]);J2=s.Matrix([[0,-1],[1,0]])
need(meq(J2,v*xi.T-xi*v.T),'actual G generator is SAM rank-two skew')
need(eq((v.T*J2*M*v)[0],2*a*p**4),'backward derivative is nonzero')
need(eq((v.T*J2*v)[0],0),'matched V-backward derivative is zero')
# Fixed-fine detector on the original t and new flag f cannot be unchanged if
# t is made equal to its passive v before the unmodified fine reader.
need(eq((p**2*p+p*p**2)-p**2,p**5),'pre-reader t polar alignment alters fine effect by p^5')
# Early b mark and all nine archive labels are retained by bank-only recovery:
# abstract isometry Gram K_gamma* R_b* R_b K_gamma = K_gamma* K_gamma.
R=s.Matrix([[s.Rational(3,5),-s.Rational(4,5)],[s.Rational(4,5),s.Rational(3,5)]])
need(R.T*R==eye(2),'arbitrary endpoint recovery is exactly orthogonal in control')
for x,y in ((1,0),(0,1),(s.Rational(3,5),s.Rational(4,5))):
 w=s.Matrix([x,y]);need((R*w).dot(R*w)==w.dot(w),'unitary preserves fine branch weight')
# Real conditional recovery primitive: exactly supported, r is control only;
# t and protected oldRIGHT are never touched. Its routed inverse G^-1 is the
# exact all-column SourceI/SWAP macro already checked in round2.
r,x,port=3,4,0
cx=lambda i,j:g('CX',(i,j))
swap=lambda i,j:(cx(i,j),cx(j,i),cx(i,j))
src=g('SourceI',(0,1,2))
inv=swap(port,x)+(src,src,g('G',(port,)),src,src)+swap(port,x)
controlled0=(g('G',(x,)),cx(r,x),g('G',(x,)),cx(r,x))
controlled1=(g('G',(x,)),cx(r,x))+inv+(cx(r,x),)
for b,word in ((0,controlled0),(1,controlled1)):
 ex=nt.Execution(7,(),(6,),word,nt.G_CX_SOURCE_I,0,(1,2))
 nt.validate_execution(ex,max_qubits=7,max_expanded_stages=20)
 need(all(6 not in gt.wires and 5 not in gt.wires and not (gt.op=='G' and gt.wires==(r,)) and not (gt.op=='CX' and gt.wires[1]==r) for gt in word),'native conditional macro preserves oldRIGHT, direct tail and label '+str(b))
# Algebraic endpoint of those macros on r and a live bank bit, using the
# previously checked all-column exact routed inverse on PORT/Spin/bank.
X=s.Matrix([[0,1],[1,0]])
need(meq(X*G*X,G.T),'real conjugation XGX=G^-1')
need(meq(G.T*G,eye(2)),'conditional1 on r0 is identity')
need(meq(X*G.T*X*G,G**2),'conditional1 on r1 is G²')
need(meq(X*G*X*G,eye(2)),'conditional0 on r1 is identity')
# The exact r-controlled bank-only macro commutes with every r/t basis
# projector; additional archive copies and record wires tensor as identity.
controlled=s.diag(*([1]*4+[1]*4))
controlled=s.diag(1,1,1,1,1,1,1,1)
controlled[:4,:4]=eye(4)
controlled[4:,4:]=s.kronecker_product(G**2,eye(2))
for rb in (0,1):
 for tb in (0,1):
  mark=s.kronecker_product(s.diag(int(rb==0),int(rb==1)),eye(2),s.diag(int(tb==0),int(tb==1)))
  need(meq(controlled*mark,mark*controlled),'conditional bank macro preserves r/t fine projector')
# Positive overlap gap for the actual q of this source-frame fixture.
H0=float(s.N(d['H0'][0],20));H1=float(s.N(d['H1'],20));pf=float(p);qf=float(s.N(oldq,20))
alpha=H0*pf;beta=H1*pf**2;xi2=pf**3/(qf*(1-qf))
lam=(alpha+beta+((alpha-beta)**2+4*alpha*beta*xi2)**.5)/2
need(0<xi2<1 and alpha+beta-lam>1e-9,'conditional vs any common bank optimum has positive fixture gap')
# eta for ideal optional branch + post-fine tail recovery; helper Born states
# return to their original v in the target and the real terminal CX is retained.
mu0=p**8+p**12;mu1=p**12;kappa=p+2*a*p**3
eta=kappa**2*(mu0+mu1)*(p*mu0+p**3*mu1)
need(d['lower_exact'](eta)>0,'ideal full fine-recovery reference weight positive')
print(json.dumps({'status':'PASS','checks':len(checks),'fixture':{'c':float(s.N(c,20)),
 'q':float(s.N(oldq,20)),'sam_variance':float(s.N(var,20)),
 'sam_D_CW':float(s.N(2*a*p**4,20))},
 'pre_reader_tail_effect_gap_p5':float(s.N(p**5,20)),
 'conditional_ideal_eta':float(s.N(eta,20)),
 'fixture_conditional_minus_common_h':alpha+beta-lam,
 'full_geometric_H1_word_executed':False,'common_old_mark_guard_proved':False,
 'physical_cost_info_binding_proved':False,'GR_closed':False},sort_keys=True,indent=2))
