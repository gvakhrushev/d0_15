#!/usr/bin/env python3
"""Two native high records plus old reader; exact finite Golden field."""
import importlib.util,itertools,json,sys
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('native_execution',Path(__file__).resolve().parent/'native_execution.py')
n=importlib.util.module_from_spec(spec);sys.modules[spec.name]=n;spec.loader.exec_module(n)
p,a,F,G=n.P,n.A,n.GOLDEN_FIELD,n.G_LOCAL;I=s.eye
def eq(x,y=0):return F.from_sympy(s.expand(x-y))==F.zero
def meq(X,Y):return X.shape==Y.shape and all(eq(z) for z in X-Y)
checks=[]
def ck(ok,name):
 if not ok:raise AssertionError(name)
 checks.append(name)
g=n.Gate;src=g('SourceI',(0,1,2));cx=lambda i,j:g('CX',(i,j))
def high(r,t):return (cx(0,r),src,src,g('G',(r,)),g('G',(r,)),cx(r,t),g('G',(t,)),cx(r,t))
def old(r,t):return (cx(0,r),src,src,cx(r,t),g('G',(t,)),cx(r,t))
word=high(3,4)+high(5,6)+old(7,8)
ex=n.Execution(10,(),(9,),word,n.G_CX_SOURCE_I,0,(1,2))
n.validate_execution(ex,max_qubits=10,max_expanded_stages=22)
iv=n.inventory(ex,max_qubits=10,max_expanded_stages=22)
ck((iv.g_count,iv.cx_count,iv.source_i_count,iv.gate_count)==(7,9,6,22),'literal three-reader inventory and native domain')
ck(all(9 not in gt.wires for gt in word),'protected oldRIGHT never addressed')
ck(all(not set(gt.wires)&{3,4} for gt in word[len(high(3,4)):]),'first stored record and its tail never touched later')
ck(all(not set(gt.wires)&{5,6} for gt in word[len(high(3,4))+len(high(5,6)):]),'second stored record and its tail never touched later')
source_ex=n.Execution(3,(),(),(src,src),n.G_CX_SOURCE_I,0,(1,2))
source_matrix=n.word_matrix(source_ex,max_qubits=3,max_expanded_stages=2)
ck(meq(source_matrix,s.kronecker_product(s.diag(1,-1),I(4))),'each paid SourceI pair is Z_e with identity on arbitrary Spin')
# A distinct live bank e can instead use the one fixed source port as a
# genuinely routed bus. The source port is restored on every input column.
swap=lambda i,j:(cx(i,j),cx(j,i),cx(i,j))
route=swap(0,3)+(src,src)+swap(0,3)
route_ex=n.Execution(4,(),(),route,n.G_CX_SOURCE_I,0,(1,2))
route_matrix=n.word_matrix(route_ex,max_qubits=4,max_expanded_stages=8)
ck(meq(route_matrix,s.kronecker_product(I(8),s.diag(1,-1))),'routed Z acts on separate event bank and restores source Spin on all columns')
def high_r(r,t):return (cx(3,r),)+route+(g('G',(r,)),g('G',(r,)),cx(r,t),g('G',(t,)),cx(r,t))
def old_r(r,t):return (cx(3,r),)+route+(cx(r,t),g('G',(t,)),cx(r,t))
routed=high_r(4,5)+high_r(6,7)+old_r(8,9)
rex=n.Execution(11,(),(10,),routed,n.G_CX_SOURCE_I,0,(1,2))
riv=n.inventory(rex,max_qubits=11,max_expanded_stages=40)
ck((riv.g_count,riv.cx_count,riv.source_i_count,riv.gate_count)==(7,27,6,40),'separate source-bus fully routed inventory')
ck(all(10 not in gt.wires for gt in routed),'routed word never touches oldRIGHT')
ck(all(not set(gt.wires)&{4,5} for gt in routed[len(high_r(4,5)):]) and all(not set(gt.wires)&{6,7} for gt in routed[len(high_r(4,5))+len(high_r(6,7)):]),'both routed high records remain untouched')

# Exact sparse seven-wire reduced simulation: source, then three born r/t
# pairs. Both SourceI calls are replaced only AFTER checking their joint
# all-column Z_e tensor I_Spin endpoint. Nothing is traced or measured.
f_a=F.from_sympy(a);f_p=F.from_sympy(p);one=F.one;zero=F.zero
def add(out,key,val):out[key]=out.get(key,zero)+val
state={}
for initial in (0,1):
 for bits in range(64):
  amp=one
  for k in range(6):amp*=f_p if ((bits>>(5-k))&1) else f_a
  state[((initial<<6)|bits,initial)]=amp
def apply(kind,i,j=None):
 global state
 out={};mask=1<<(6-i)
 for (bits,col),amp in state.items():
  if kind=='Z':add(out,(bits,col),-amp if bits&mask else amp)
  elif kind=='CX':add(out,(bits ^ ((1<<(6-j)) if bits&mask else 0),col),amp)
  else:
   if bits&mask:
    add(out,(bits^mask,col),-f_p*amp);add(out,(bits,col),f_a*amp)
   else:
    add(out,(bits,col),f_a*amp);add(out,(bits|mask,col),f_p*amp)
 state=out
def block(r,t,is_high):
 apply('CX',0,r);apply('Z',0)
 if is_high:apply('G',r);apply('G',r)
 apply('CX',r,t);apply('G',t);apply('CX',r,t)
block(1,2,True);block(3,4,True);block(5,6,False)
def bit(index,wire):return (index>>(6-wire))&1
def amplitude(index,col):return state.get((index,col),zero)
def event_effect(predicate):
 return [[sum((amplitude(b,i)*amplitude(b,j) for b in range(128) if predicate(b)),zero)
          for j in (0,1)] for i in (0,1)]
def iszero(mat):return all(x==zero for row in mat for x in row)
invalid=lambda b:any(bit(b,r)==1 and bit(b,t)==1 for r,t in ((1,2),(3,4),(5,6)))
ck(iszero(event_effect(invalid)),'no invalid 11 at any of three retained records on all source columns')
q0=p**2;q1=p;kap=1-2*p**6;A=4*p**3+4*p**6
q=[q0,q1];qh=[A-kap*q0,A-kap*q1]
last=event_effect(lambda b:bit(b,5)==1 and bit(b,6)==0)
ck(last[0][0]==F.from_sympy(q0) and last[1][1]==F.from_sympy(q1) and last[0][1]==last[1][0]==zero,'literal M2 full-output marginal restores old all-column effect')
for b1,b2,b3 in itertools.product((0,1),repeat=3):
 pred=lambda b:bit(b,1)==b1 and bit(b,3)==b2 and bit(b,5)==b3
 m=event_effect(pred)
 for j in (0,1):
  target=(qh[j] if b1 else 1-qh[j])*(qh[j] if b2 else 1-qh[j])*(q[j] if b3 else 1-q[j])
  ck(m[j][j]==F.from_sympy(s.expand(target)),f'joint recorded labels {b1}{b2}{b3}, source {j}')
 ck(m[0][1]==zero and m[1][0]==zero,f'joint record {b1}{b2}{b3} preserves input columns')

# Operator channel on the live source before the old final reader.
Z=s.diag(1,-1);P=s.diag(0,1);u=(a+p)/2;d=(a-p)/2
K0=u*Z+d*I(2);K1=u*Z-d*I(2)
L0=p**3*K0-2*a*p*K1;L1=2*a*p*K0+p**3*K1
adj=lambda X:L0.T*X*L0+L1.T*X*L1
E=q0*I(2)+p**3*P
ck(meq(adj(I(2)),I(2)),'high instrument is trace preserving, no postselection')
ck(meq(adj(P),P) and meq(adj(adj(E)),E),'two high records preserve old event and old report effect')
V=Z
L0v,L1v=V*L0,V*L1
adv=lambda X:L0v.T*X*L0v+L1v.T*X*L1v
ck(meq(adv(P),P) and not meq(V,I(2)),'actual nonidentity native backward Z also preserves event')
Vbad=G
badadj=lambda X:(Vbad*L0).T*X*(Vbad*L0)+(Vbad*L1).T*X*(Vbad*L1)
ck(not meq(badadj(P),P) and eq(badadj(P)[0,0],p**2),'actual independent backward G breaks old event guard')
gen=s.Matrix([[0,-1],[1,0]]);dP=gen*P-P*gen
gamma=-2*a*p
ck(meq(adj(dP),gamma*dP),'one high record multiplies independent final-projector tangent by -2ap')
ck(meq(adj(adj(dP)),4*p**3*dP),'two high records multiply that tangent by 4p cubed')
ck(bool(s.simplify(4*p**3<1)),'finite attenuation is strictly less than one')
# True born-cut warning: j* P j=Q I with 0<Q<1 is NOT a projector.
# This actual canonical source fixture has Q=p², and the off-cut event
# leakage is Q(1-Q)I=p³ I, even though its effect is scalar on input.
vv=s.Matrix([a,p]);Jcut=s.kronecker_product(vv,I(4));Pfull=s.kronecker_product(P,I(4))
Qcut=Jcut.T*Pfull*Jcut;Ccut=Jcut*Jcut.T
leak=Jcut.T*Pfull*(I(8)-Ccut)*Pfull*Jcut
ck(meq(Qcut,p**2*I(4)),'true canonical input compresses event to scalar p squared')
ck(meq(leak,p**3*I(4)),'event has strictly positive leakage out of true initial cut')
ck(not meq(Qcut*Qcut,Qcut),'compressed event is not a sharp projector')

# AD2: exact source handoff with arbitrary source/reference correlations.
se=n.Execution(3,(),(2,),swap(0,1),n.G_CX)
swapU=n.word_matrix(se,max_qubits=3,max_expanded_stages=3)
input_embed=s.kronecker_product(I(2),vv,I(2))
output_embed=s.kronecker_product(vv,I(2),I(2))
ck(meq(swapU*input_embed,output_embed),'AD2 handoff returns fresh source on every source/reference column')

# High; handoff; High; handoff; Old, same fixed source port. Handoff
# memories and all six r/t wires remain in the output. The exact state
# below starts unused future-born wires in v only for matrix evaluation;
# physical births still occur at their true chronological stages.
handoff_word=high(3,4)+swap(0,5)+high(6,7)+swap(0,8)+old(9,10)
hexec=n.Execution(12,(),(11,),handoff_word,n.G_CX_SOURCE_I,0,(1,2))
hiv=n.inventory(hexec,max_qubits=12,max_expanded_stages=28)
ck((hiv.g_count,hiv.cx_count,hiv.source_i_count,hiv.gate_count)==(7,15,6,28),'two AD2 handoffs and three real readers exact native inventory')
ck(all(11 not in gt.wires for gt in handoff_word),'handoff word never touches protected oldRIGHT')
ck(all(not set(gt.wires)&{3,4,5} for gt in handoff_word[len(high(3,4))+3:]) and all(not set(gt.wires)&{6,7,8} for gt in handoff_word[len(high(3,4))+3+len(high(6,7))+3:]),'handoff archives and prior report pairs stay sealed')
state9={}
for bits in range(512):
 amp=one
 for k9 in range(9):amp*=f_p if ((bits>>(8-k9))&1) else f_a
 state9[bits]=amp
def apply9(kind,i,j=None):
 global state9
 out={};mask=1<<(8-i)
 for bits,amp in state9.items():
  if kind=='Z':add(out,bits,-amp if bits&mask else amp)
  elif kind=='CX':add(out,bits ^ ((1<<(8-j)) if bits&mask else 0),amp)
  elif bits&mask:
   add(out,bits^mask,-f_p*amp);add(out,bits,f_a*amp)
  else:
   add(out,bits,f_a*amp);add(out,bits|mask,f_p*amp)
 state9=out
def block9(r,t,is_high):
 apply9('CX',0,r);apply9('Z',0)
 if is_high:apply9('G',r);apply9('G',r)
 apply9('CX',r,t);apply9('G',t);apply9('CX',r,t)
def swap9(i,j):apply9('CX',i,j);apply9('CX',j,i);apply9('CX',i,j)
block9(1,2,True);swap9(0,3);block9(4,5,True);swap9(0,6);block9(7,8,False)
def bit9(bits,wire):return (bits>>(8-wire))&1
def prob9(predicate):return sum((amp*amp for bits,amp in state9.items() if predicate(bits)),zero)
bad9=lambda b:any(bit9(b,r)==1 and bit9(b,t)==1 for r,t in ((1,2),(4,5),(7,8)))
ck(prob9(bad9)==zero,'handoff fixture retains no invalid code in every reader')
qfresh=p**2+p**5;hfresh=A-kap*qfresh
for x,y,z in itertools.product((0,1),repeat=3):
 pred=lambda b:bit9(b,1)==x and bit9(b,4)==y and bit9(b,7)==z
 target=(hfresh if x else 1-hfresh)*(hfresh if y else 1-hfresh)*(qfresh if z else 1-qfresh)
 ck(prob9(pred)==F.from_sympy(s.expand(target)),f'handoff full retained joint law {x}{y}{z}')
ck(prob9(lambda b:bit9(b,7)==1)==F.from_sympy(qfresh),'final original report has its scalar original law after handoffs')
print(json.dumps({'status':'PASS_EXACT','checks':len(checks),'names':checks,
 'literal_word':{'high_readers':2,'old_readers':1,'G':7,'CX':9,'SourceI':6,'calls':22,'canonical_births':6,'total_stages':28},
 'separate_live_bank_routed_word':{'G':7,'CX':27,'SourceI':6,'calls':40,'record_births':6,'total_stages_excluding_bank_and_bus_births':46},
 'fresh_source_handoff_word':{'G':7,'CX':15,'SourceI':6,'calls':28,'record_and_handoff_births':8,'total_stages_excluding_initial_source_birth':36},
 'fresh_old_report_probability':float(s.N(qfresh,16)),
 'fresh_high_report_probability':float(s.N(hfresh,16)),
 'single_step_coherence_factor':float(s.N(gamma,16)),
 'two_step_independent_final_tangent_factor':float(s.N(4*p**3,16)),
 'scope':'actual finite source-frame toy; conditional commutant and common P, not full H1 scheduling or full paid Cost-Info',
 'full_H1_admission_proved':False,'physical_C_discharged':False,'GR_closed':False},indent=2))
