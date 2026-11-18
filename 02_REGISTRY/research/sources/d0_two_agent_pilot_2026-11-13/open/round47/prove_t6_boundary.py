#!/usr/bin/env python3
"""Exact aux/port/Spin boundary lemmas, not H1 admission proof."""
from pathlib import Path
from hashlib import sha256
from itertools import zip_longest
import importlib.util,sys,json
import sympy as s
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');sys.path.insert(0,str(D/'round23'));import car_vacuum_prefix as n
nb=n.nb;lay=n.layout();port=lay['port'];spin=tuple(lay['spin']);x=n.inputs();J=s.Matrix([[0,-1],[1,0]]);I2=s.eye(2);W=s.diag(1,1,1,-1)
# Both source-domain Spin convention and the owned-checker convention; exact
# conjugacy carries any final identity on Spin between the two conventions.
L_domain=s.diag(J,J);L_owned=s.diag(J,-J);assert W*L_domain*W==L_owned and L_domain**2==L_owned**2==-s.eye(4)
def source_matrix(L,portslot,spin0,spin1,N):
 out=s.zeros(1<<N)
 for x0 in range(1<<N):
  p=x0>>portslot&1;u=x0>>spin0&1;v=x0>>spin1&1;j=2*u+v
  for y in range(4):
   z=(L if p else s.eye(4))[y,j]
   if z:out[(x0&~((1<<spin0)|(1<<spin1)))|((y//2)<<spin0)|((y%2)<<spin1),x0]=z
 return out
def swap_matrix(q,p,N):
 out=s.zeros(1<<N)
 for a in range(1<<N):
  b=a^(((a>>q&1)^(a>>p&1))*((1<<q)|(1<<p)));out[b,a]=1
 return out
def single(M,q,N):
 out=s.zeros(1<<N)
 for x0 in range(1<<N):
  k=x0>>q&1
  for j in (0,1):out[(x0&~(1<<q))|(j<<q),x0]=M[j,k]
 return out
C,S=s.symbols('C S',real=True);G=s.Matrix([[C,-S],[S,C]]);Z=s.diag(1,-1);assert Z*G*Z==G.T
for L in (L_domain,L_owned):
 A=source_matrix(L,0,1,2,3);assert A*A==single(Z,0,3) and A**4==s.eye(8) and A!=s.eye(8)
 # Input target q0, borrowed port q1, arbitrary two-bit Spin q2/q3.
 S4=source_matrix(L,1,2,3,4);SW=swap_matrix(0,1,4);Gp=single(G,1,4);out=SW*S4*S4*Gp*S4*S4*SW;assert out==single(G.T,0,4)
# Exact routed CZ from A13 really restores arbitrary port and Spin despite
# having 5 SourceI calls (pairwise counting alone would be incorrect).
cs=D/'round13/compile_native_cz.py';sp=importlib.util.spec_from_file_location('b47_cz',cs);cz=importlib.util.module_from_spec(sp);sys.modules[sp.name]=cz;sp.loader.exec_module(cz);word=cz.cz_word(0,1,2,(3,4));assert sum(g.op=='SourceI' for g in word)==5
for L in (L_domain,L_owned):
 src=source_matrix(L,2,3,4,5)
 for column in range(32):
  z=s.eye(32)[:,column]
  for gate in word:
   if gate.op=='CX':
    c,t=gate.wires;idx=next(i for i,v in enumerate(z) if v);value=z[idx];z=s.zeros(32,1);z[idx^(((idx>>c)&1)<<t)]=value
   else:z=src*z
  assert z==((-1)**((column&1)*((column>>1)&1)))*s.eye(32)[:,column]
# Exact symbolic scalar-corner theorem with arbitrary real W-operator blocks
# commuting with aux complex structure; no unitarity assumption is needed.
x00,x01,x10,x11,y00,y01,y10,y11,z00,z01,z11=s.symbols('x00 x01 x10 x11 y00 y01 y10 y11 z00 z01 z11',real=True)
X=s.Matrix([[x00,x01],[x10,x11]]);Y=s.Matrix([[y00,y01],[y10,y11]]);Zwork=s.Matrix([[z00,z01],[z01,z11]]);A=s.kronecker_product(X,I2)+s.kronecker_product(Y,J);JA=s.kronecker_product(s.eye(2),J);JW=s.kronecker_product(s.Matrix([1,0]),I2);M=s.expand(JW.T*A.T*s.kronecker_product(Zwork,I2)*A*JW)
assert A*JA==JA*A and M.T==M and s.simplify(M[0,1])==s.simplify(M[1,0])==0 and s.simplify(M[0,0]-M[1,1])==0
# J_aux symmetry alone does not erase an arbitrary D interaction. J⊗J is
# symmetric, commutes J_aux, yet is not a scalar on auxiliary×other D.
Q=s.kronecker_product(J,J);Jaux=s.kronecker_product(J,I2);assert Q.T==Q and Q*Jaux==Jaux*Q and Q!=s.eye(4)*Q[0,0]
# An arbitrarily near-identity unitary can produce a non-scalar compressed
# aux corner if a completed block is allowed to use aux as a control.
c=s.Rational(999999,1000001);ss=s.Rational(2000,1000001);assert c*c+ss*ss==1
N=s.eye(4);N[1,1]=N[3,3]=c;N[3,1]=ss;N[1,3]=-ss;ZW=s.diag(1,1,-1,-1);JJ=s.eye(4)[:,[0,1]];corner=JJ.T*N.T*ZW*N*JJ
assert corner==s.diag(1,c*c-ss*ss) and corner[0,0]!=corner[1,1]
# Reconstruct ALL actual A23 blocks from elementary macros independently.
def gate(op,*w):return {'op':op,'wires':list(w)}
def seq(*a):return {'op':'seq','children':list(a)}
def repeat(k,t):return {'op':'repeat','count':str(k),'child':t}
def swap(a,b):return seq(gate('CX',a,b),gate('CX',b,a),gate('CX',a,b))
src=gate('SourceI',port,*spin)
def zword(q):return seq(swap(q,port),seq(src,src),swap(q,port))
def rotation(q,k):
 if k>0:return repeat(k,gate('G',q))
 core=seq(src,src,repeat(-k,gate('G',port)),src,src);return seq(swap(q,port),core,swap(q,port))
def boolean(op,q):return seq(zword(q),rotation(q,(2 if op=='H' else 4)*x['boolean_k']))
def expected():
 for q in lay['internal_SITE']+lay['grade']+lay['RIGHT']:yield rotation(q,-1)
 for q in lay['internal_SITE']+lay['RIGHT'][1:]:yield boolean('H',q)
 q=lay['grade'];yield gate('G',q[0])
 for i in q[1:]:yield gate('CX',q[0],i)
 yield boolean('X',q[0])
 for cmd in n.commands(x['kappa'],lay,x['phase_k']):
  for mask in range(128):
   ids=[i for i in range(7) if mask>>i&1];par=[gate('CX',cmd['controls'][i],cmd['target']) for i in ids];sgn=(-1)**sum(cmd['pattern'][i] for i in ids)
   yield seq(*par,rotation(cmd['target'],sgn*cmd['k']),*reversed(par))
count=0
for a,b in zip_longest(expected(),n.prefix_blocks(lay)):
 assert a is not None and a==b;count+=1
assert count==40742 and not set(lay['internal_SITE']+lay['grade']+lay['RIGHT'])&{port,*spin,lay['oldRIGHT_witness']}
plan=json.loads((D/'round17/GLOBAL_REPORT_PLAN.json').read_bytes());assert plan['report_wire']!=plan['native_aux_arbitrary'] and plan['native_aux_arbitrary']>=plan['logical_wire_count']
out={'status':'PASS_T6_CONDITIONAL_AUX_AND_PORT_SPIN_MACRO_LEMMAS','A23_actual_compact_macro_syntax_rebuilt':count,'S_squared_exact_Zport_in_both_spin_conventions':True,'borrowed_arbitrary_port_and_spin_exactly_restored_at_A23_macro_boundaries':True,'A13_5_SourceI_CZ_exact_port_spin_identity_all32_columns':True,'arbitrary_aux_canonical_WORK_sufficient_under_full_factorization_and_embedding':True,'optional_aux_J_commutant_real_symmetric_scalar_lemma':True,'J_commutant_alone_without_other_D_identity_insufficient':True,'near_identity_aux_control_nonscalar_counterexample':True,'full_H1_macros_all_commutants_proved':False,'full_actual_T6_proved':False,'same_H1_births_marks_admission_proved':False,'GR_closed':False,'input_sha256':{str(p):sha256(p.read_bytes()).hexdigest() for p in [D/'round23/car_vacuum_prefix.py',D/'round14/native_boolean.py',cs,D/'round17/GLOBAL_REPORT_PLAN.json']}}
(P/'T6_AUX_PORT_SPIN_LEMMAS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'A23_macro_blocks':count,'full_T6_proved':False}))
