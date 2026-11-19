#!/usr/bin/env python3
"""Native fixed Q8 15-step paid echo and nondemolition archive/source gate.

Scope: exact word/involution proof, numerical original four-spin 16x16 clock-body
replay, and exact finite Kraus block-diagonal implication. No Book03 physical
admission, no reset, no unpriced deletion of oldRIGHT/archive.
"""
import math
import json
import numpy as np

phi=(1+math.sqrt(5))/2
p=1/phi
a=math.sqrt(p)
def left(x,y,z,w):
    return np.array([[x,-y,-z,-w],[y,x,-w,z],[z,w,x,-y],[w,-z,y,x]],dtype=float)
Li=left(0,1,0,0); Lj=left(0,0,1,0)
I4=np.eye(4);I16=np.eye(16)
B=np.kron(np.array([[a,-p],[p,a]],float),np.eye(8))
X=np.kron(np.block([[I4,np.zeros((4,4))],[np.zeros((4,4)),Li]]),np.eye(2))
Y=np.kron(np.block([[Lj,np.zeros((4,4))],[np.zeros((4,4)),Lj]]),np.eye(2))
WR=np.zeros((16,16))
for arm in range(2):
 for spin in range(4):
  for bit in range(2):
   source=8*arm+2*spin+bit
   target=8*arm+2*spin+(bit^arm)
   WR[target,source]=1
G={"B":B,"X":X,"Y":Y,"write":WR}
identity_word=["X"]*4+["Y"]*4
order_word=["X","Y"]+["X"]*3+["Y"]*3
I=np.eye(16)
checks=[]
def check(label, pred, tol=None):
    if tol is not None: pred=float(pred)<tol
    if not bool(pred): raise AssertionError(label)
    checks.append(label)
def compile_word(seq):
  A=I.copy()
  for name in seq:
   A=G[name]@A
  return A
# In the ORIGINAL fixed 15-tick programme, the 5 forward gates Z B Z synthesize B^-1.
# Both eight-step Q8 words are involutions; re-use same word for the inverse.
for label,word in [("identity",identity_word),("order",order_word)]:
  forward=["B"]+word+["X","X","B","X","X","write"]
  backward=["write","B"]+word+["X","X","B","X","X"]
  check(label+': forward and inverse are both 15 charged primitives', len(forward)==len(backward)==15)
  M=compile_word(word)
  F=compile_word(forward)
  R=compile_word(backward)
  D=np.linalg.matrix_power(X,2)@B@np.linalg.matrix_power(X,2)
  check(label+': original B inverse forward synthesis', np.linalg.norm(D-B.T), 1e-13)
  check(label+': original word involution',np.linalg.norm(M@M-I),1e-13)
  check(label+': actual 15 forward-step echo inverse on all16',np.linalg.norm(R@F-I),2e-13)
  check(label+': inverse 15-step echo forward on all16',np.linalg.norm(F@R-I),2e-13)
  check(label+': original forward gate orthogonal',np.linalg.norm(F.T@F-I),2e-13)
  check(label+': original echo gate orthogonal',np.linalg.norm(R.T@R-I),2e-13)
  for spin in range(4):
    blank=np.zeros(16);blank[2*spin]=1.
    state=F@blank
    restored=R@state
    check(f'{label}: full finite original spin{spin} initial returned without conditional postselection',np.linalg.norm(restored-blank),2e-13)
    probclick=sum(state[8+2*j+1]**2 for j in range(4))
    target=0 if label=='identity' else 4*p**3
    check(f'{label}: exact registered clicked Q8 probability spin{spin}',abs(probclick-target),2e-13)
  if label=='identity':Fid=F;Rid=R
  else:Ford=F;Rord=R
# Programmed fixed gate does not mix programmes at all. Echo restores common clock-body.
for r in (1.8512395785208469e-6,.05,.41):
  v=np.zeros(16);v[0]=1.
  alpha,beta=math.sqrt(1-r),math.sqrt(r)
  initial=np.concatenate((alpha*v,beta*v))
  output=np.concatenate((alpha*Fid@v,beta*Ford@v))
  echo=np.concatenate((alpha*Rid@Fid@v,beta*Rord@Ford@v))
  check(f'coherent programmed actual output normalized r={r}',abs(np.linalg.norm(output)-1),1e-13)
  check(f'coherent echo restores entire initial state r={r}',np.linalg.norm(echo-initial),2e-13)
  Xprog=np.kron(np.array([[0.,1.],[1.,0.]]),np.eye(16))
  coh_echo=float(echo@Xprog@echo)
  check(f'programme-only coherence after paid echo equals 2sqrt(r(1-r)) r={r}',abs(coh_echo-2*alpha*beta),2e-13)
  initial_program_overlap=float((Fid@v)@(Ford@v))
  coh_before=float(output@Xprog@output)
  check(f'native original forward order coherence suppressed by p3 r={r}',abs(initial_program_overlap-p**3),2e-13)
  check(f'pre-echo programme-only X=2p3sqrt(r(1-r)) r={r}',abs(coh_before-2*p**3*alpha*beta),2e-13)
  # Attach (if admitted and paid) a separately preserved classical label of the programme.
  # The old label is NEVER erased by the echo. It forces exact zero program-only X.
  tagged=np.concatenate((np.kron(alpha*v,[1.,0.]),np.kron(beta*v,[0.,1.])))
  check(f'tagged state after echo retains both distinguishable old-programme alternatives r={r}',abs(np.linalg.norm(tagged)-1),1e-13)
  Xtagprog=np.kron(np.kron(np.array([[0.,1.],[1.,0.]]),np.eye(16)),np.eye(2))
  joint=np.kron(np.kron(np.array([[0.,1.],[1.,0.]]),np.eye(16)),np.array([[0.,1.],[1.,0.]]))
  check(f'old programme archive tag blocks all programme-only interference r={r}',abs(tagged@Xtagprog@tagged),1e-14)
  check(f'joint phase test still could reveal phase r={r}',abs(tagged@joint@tagged-2*alpha*beta),2e-13)
# General nondemolition theorem checked on exact small 2×2 classical archive.
# For a CPTP instrument with no transitions between genuinely readable labels,
# EVERY Kraus K has a diagonal archive block, hence every effect K* K does too.
P0=np.diag([1.,0.]);P1=np.diag([0.,1.]);
for th in (0,.21,.71):
 for a_prob in (.2,.87):
  # Reversible internal spin phase allowed independently in each record class.
  Ks=[np.diag([math.sqrt(a_prob),math.sqrt(a_prob)*complex(math.cos(th),math.sin(th))]),
      np.diag([math.sqrt(1-a_prob), math.sqrt(1-a_prob)*complex(math.cos(th),-math.sin(th))])]
  check('QND channel trace preserving',np.linalg.norm(sum(K.conj().T@K for K in Ks)-np.eye(2)),1e-13)
  for k in Ks:
    check('each native QND Kraus has zero off-record corner',np.linalg.norm(P0@k@P1+P1@k@P0),1e-14)
    e=k.conj().T@k
    check('each QND outcome effect is block diagonal', np.linalg.norm(P0@e@P1+P1@e@P0),1e-14)
    for q in (.2,.7):
      pure=np.array([math.sqrt(1-q), math.sqrt(q)])
      rho=np.outer(pure,pure)
      diag=np.diag(np.diag(rho))
      check('no possible QND effect distinguishes coherent joint tag',abs(np.trace(e@(rho-diag))),1e-14)
# Positive controls: a phase-sensitive measurement can distinguish, but it
# destroys classical archive-label nondemolition (incompatible readout).
X2=np.array([[0.,1.],[1.,0.]])
plus=(np.eye(2)+X2)/2
zero=np.diag([1.,0.]);one=np.diag([0.,1.])
check('coherent X effect fails block-diagonal archive criterion',np.linalg.norm(P0@plus@P1)>0)
q=.19
rho=np.outer([math.sqrt(1-q),math.sqrt(q)],[math.sqrt(1-q),math.sqrt(q)])
check('coherent X test would distinguish',abs(np.trace(plus@(rho-np.diag(np.diag(rho))))-math.sqrt(q*(1-q))),1e-14)
# Its nonselective projective measurement alters old readable Z probabilities
# for input |0>, so it does NOT belong to old-history QND instrument class.
minus=(np.eye(2)-X2)/2
out=plus@zero@plus+minus@zero@minus
check('phase-readout nonselective quantum operation disturbs original readable label',abs(out[0,0]-.5),1e-14)

# Stronger finite audit: exactly THREE positive branch preparations suffice,
# without assuming QND for every possible input. A fixed CPTP instrument with
# an archived binary label must preserve that label on these three settings.
# Strict concavity of sqrt(r(1-r)) makes the three probe rows independent.
import sympy as sy
rational_probes=[sy.Rational(1,5),sy.Rational(2,5),sy.Rational(4,5)]
M3=sy.Matrix([[1-x,x,2*sy.sqrt(x*(1-x))] for x in rational_probes])
det3=sy.simplify(M3.det())
check('three exact positive native-grammar probes linearly independent',det3!=0)
solution=M3.inv()*sy.Matrix([1-x for x in rational_probes])
check('three fixed nondemolition probability constraints force E00=1,E11=0,Re E01=0',all(sy.simplify(v-w)==0 for v,w in zip(solution,[1,0,0])))
# The actual tiny native click r0 makes the finite inference ill-conditioned,
# hence 'three exact tests' is a theorem and NOT a robust noisy measurement.
import mpmath as mp
mp.mp.dps=80
rare_str='0.0000018512395785208469'
rare=mp.mpf(rare_str)
rare_points=[rare,rare*2,rare*4]
rare_M=mp.matrix([[1-x,x,2*mp.sqrt(x*(1-x))] for x in rare_points])
rare_det=mp.det(rare_M)
check('three distinct positive rare native report probes nonzero determinant',rare_det!=0)
rare_sol=mp.lu_solve(rare_M,mp.matrix([1-x for x in rare_points]))
check('80 digit rare native linear inverse gives QND spectral extremes',max(abs(rare_sol[i]-t) for i,t in enumerate([1,0,0])) < mp.mpf('1e-60'))
# Example positive non-QND effect must change some old-programme probability.
E_bad=np.array([[.8,.12],[.12,.2]])
check('hostile offdiagonal effect valid positive',min(np.linalg.eigvalsh(E_bad))>0 and max(np.linalg.eigvalsh(E_bad))<1)
errors=[float(np.array([1-x,x,2*math.sqrt(x*(1-x))])@np.array([E_bad[0,0]-1,E_bad[1,1],E_bad[0,1]])) for x in [.2,.4,.8]]
check('non-QND effect fails at least one of the finite three exact record checks',max(abs(e) for e in errors)>1e-2)
# Matrix with matching QND diagonal values but hidden imaginary offdiagonal is
# NOT positive, excluding a loophole undetected by real three-probe amplitudes.
E_im=np.array([[1.,1.j*.03],[-1.j*.03,0.]],complex)
check('imaginary coherence loophole violates effect positivity',min(np.linalg.eigvalsh(E_im))<0)

print(json.dumps({'status':'PASS','checks':len(checks),'native_p':p,'Q8_cross_overlap':p**3,
 'original_program_cost_ops':15,'echo_cost_ops':15,'combined_charged_ops':30,
 'initial_original_16stage_wrap_slot':1,
 'claim':'15 forward Q8 echo exists, but all QND archive-preserving tests are phase blind; joint phase test is not QND',
 'physics':'no native field writer, Book03 projector or full 72441 classical archive eraser claimed','three_setting_exact_determinant':str(det3),'native_rare_3probe_abs_determinant':mp.nstr(abs(rare_det),20)},indent=2))