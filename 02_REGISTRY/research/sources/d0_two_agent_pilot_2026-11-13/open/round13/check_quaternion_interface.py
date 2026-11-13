#!/usr/bin/env python3
"""Exact one-SourceI algebra with four independent finite preparation slots."""
import importlib.util,itertools,json,math,sys
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('native_execution',Path(__file__).resolve().parent/'native_execution.py')
n=importlib.util.module_from_spec(spec);sys.modules[spec.name]=n;spec.loader.exec_module(n)
p,a,F=n.P,n.A,n.GOLDEN_FIELD;zero,one=F.zero,F.one
fa,fp=F.from_sympy(a),F.from_sympy(p);g=n.Gate
def eq(x,y=0):return F.from_sympy(s.expand(x-y))==F.zero
def meq(X,Y):return X.shape==Y.shape and all(eq(z) for z in X-Y)
checks=[]
def ck(x,name):
 if not x:raise AssertionError(name)
 checks.append(name)
L=s.Matrix(n.L_I);I=s.eye(4)
ck(L.T==-L and L*L==-I,'actual quaternion Spin generator is skew and squares to minus identity')
z,w=s.symbols('z w',real=True)
ck(s.expand((z*I+w*L).T*(z*I+w*L))==(z*z+w*w)*I,'arbitrary real quaternion-span output block has scalar effect')
# Left quaternion basis from OrderMemoryReadout.left (1,i,j,k). This is a
# matrix identity; it does not add SourceJ/SourceK to the native grammar.
Lj=s.Matrix([[0,0,-1,0],[0,0,0,1],[1,0,0,0],[0,-1,0,0]])
Lk=L*Lj
ck(Lj.T==-Lj and Lk.T==-Lk and Lj*Lj==-I and Lk*Lk==-I,'original left quaternion axes skew and square to minus identity')
ck(L*Lj==-Lj*L and Lj*Lk==-Lk*Lj and Lk*L==-L*Lk,'original left quaternion axes anticommute')
q0,q1,q2,q3=s.symbols('q0 q1 q2 q3',real=True)
Q=q0*I+q1*L+q2*Lj+q3*Lk
ck(s.expand(Q.T*Q)==(q0*q0+q1*q1+q2*q2+q3*q3)*I,'full real left quaternion block has scalar effect on all Spin')
# Complex coefficients are an explicitly out-of-profile diagnostic, not an
# admitted alternative physical program.
complexK=(I+s.I*L)/2
ck(s.simplify(s.conjugate(complexK.T)*complexK-complexK)==s.zeros(4) and complexK!=I/2,'complex-phase diagnostic can have nonscalar effects')

def vstate():
 result={}
 for bits in range(16):
  value=one
  for k in range(4):value*=fp if ((bits>>(3-k))&1) else fa
  result[bits]=(value,zero)
 return result
def accum(out,key,x,y):
 X,Y=out.get(key,(zero,zero));out[key]=(X+x,Y+y)
def apply(state,op,i,j=None):
 out={};mask=1<<(3-i)
 for bits,(x,y) in state.items():
  if op=='S':
   if bits&mask:accum(out,bits,-y,x)
   else:accum(out,bits,x,y)
  elif op=='C':accum(out,bits^((1<<(3-j)) if bits&mask else 0),x,y)
  elif bits&mask:
   accum(out,bits^mask,-fp*x,-fp*y);accum(out,bits,fa*x,fa*y)
  else:
   accum(out,bits,fa*x,fa*y);accum(out,bits|mask,fp*x,fp*y)
 return out
def mass(state,pred):return sum((x*x+y*y for bits,(x,y) in state.items() if pred(bits)),zero)
def b(bits,i):return (bits>>(3-i))&1

# Mapping work e,s,r,t to physical wire e0,sam3,r4,t5;
# physical Spin 1,2 and oldRIGHT6 are never individually addressed.
mapping={0:0,1:3,2:4,3:5}
def native(op):
 k,i,*rest=op
 if k=='S':return g('SourceI',(0,1,2))
 if k=='G':return g('G',(mapping[i],))
 return g('CX',(mapping[i],mapping[rest[0]]))
def run(state,word):
 for op in word:state=apply(state,*op)
 return state
def makewords(x,high):
 x0,x1,x2,x3=x
 # These are explicit finite local slot controls, not the full H1 writer.
 forward=([('G',0)] if x0 else [])+[('S',0),('C',1,0)]+([('G',1)] if x1 else [])
 backward=([('G',1)] if x3 else [])+[('C',1,0),('S',0)]+([('G',0)] if x2 else [])
 prefix=forward+[('C',0,2),('S',0),('S',0)]+backward
 suffix=([('G',2),('G',2)] if high else [])+[('C',2,3),('G',3),('C',2,3)]
 return forward,prefix+suffix
A=4*p**3+4*p**6;kappa=1-2*p**6
ffA=F.from_sympy(A);ffk=F.from_sympy(kappa)
fine_witness=None
fine_entropy={}
for x in itertools.product((0,1),repeat=4):
 forward,old=makewords(x,False);_,high=makewords(x,True)
 for word in (old,high):
  ex=n.Execution(7,(),(6,),tuple(map(native,word)),n.G_CX_SOURCE_I,0,(1,2))
  n.validate_execution(ex,max_qubits=7,max_expanded_stages=20)
 forw=run(vstate(),forward)
 Q=mass(forw,lambda bits:b(bits,0)==1)
 expect=F.from_sympy(p**2)+F.from_sympy(p**3)*Q
 oldstate=run(vstate(),old);highstate=run(vstate(),high)
 qold=mass(oldstate,lambda bits:b(bits,2)==1 and b(bits,3)==0)
 qhigh=mass(highstate,lambda bits:b(bits,2)==1 and b(bits,3)==0)
 ck(qold==expect,'four-slot old NPS exact effect '+str(x))
 ck(qhigh==ffA-ffk*qold,'four-slot high effect has exact negative gain '+str(x))
 ck(mass(oldstate,lambda bits:b(bits,2)==1 and b(bits,3)==1)==zero and mass(highstate,lambda bits:b(bits,2)==1 and b(bits,3)==1)==zero,'four-slot both invalid effects vanish '+str(x))
 ck(mass(oldstate,lambda _:True)==one and mass(highstate,lambda _:True)==one,'four-slot complete outputs retained '+str(x))
 if x==(0,0,0,0):
  values=[mass(highstate,lambda bits,ee=ee,ss=ss:b(bits,0)==ee and b(bits,1)==ss and b(bits,2)==1 and b(bits,3)==0) for ee,ss in itertools.product((0,1),repeat=2)]
  positive=[float(s.N(F.to_sympy(value),16)) for value in values if value!=zero]
  ck(len(positive)>=2,'optional real fine WORK label has nontrivial conditional distribution')
  fine_witness=positive
 if x==(0,0,1,0):
  pre=run(vstate(),old[:-3]);cross_total=zero;cross_vector=zero;different_cross=False
  cs=F.from_sympy(2*a*p);cc=F.from_sympy(p**3)
  for ee,ss in itertools.product((0,1),repeat=2):
   C=zero;D=zero
   for tt in (0,1):
    i0=(ee<<3)|(ss<<2)|tt;i1=i0|(1<<1)
    x0,y0=pre[i0];x1,y1=pre[i1]
    C+=x0*x1+y0*y1;D+=x0*y1-y0*x1
   m0=mass(pre,lambda bits,ee=ee,ss=ss:b(bits,0)==ee and b(bits,1)==ss and b(bits,2)==0)
   m1=mass(pre,lambda bits,ee=ee,ss=ss:b(bits,0)==ee and b(bits,1)==ss and b(bits,2)==1)
   actual=mass(highstate,lambda bits,ee=ee,ss=ss:b(bits,0)==ee and b(bits,1)==ss and b(bits,2)==1 and b(bits,3)==0)
   ck(actual==cs*cs*m0+cc*cc*m1+2*cs*cc*C,'fine alpha high effect includes its actual quaternion cross')
   cross_total+=C;cross_vector+=D
   different_cross |= C!=F.from_sympy(a*p)*(m0+m1)
  ck(cross_total==F.from_sympy(a*p) and cross_vector==zero,'sum of complete quaternion fine cross terms is the known coarse NPS cross')
  ck(different_cross,'individual fine cross is not fixed by coarse overlap times alpha mass')
 if x in ((0,0,0,0),(1,0,0,0)):
  H=0.
  for bb in (0,1):
   probs=[float(s.N(F.to_sympy(mass(highstate,lambda bits,ee=ee,ss=ss,bb=bb:
       b(bits,0)==ee and b(bits,1)==ss and b(bits,2)==bb)),16))
       for ee,ss in itertools.product((0,1),repeat=2)]
   total=sum(probs)
   H-=sum(vv*math.log(vv/total) for vv in probs if vv>0)
  fine_entropy[str(x)]=H
ck(abs(fine_entropy[str((0,0,0,0))]-fine_entropy[str((1,0,0,0))])>1e-7,
   'optional fine conditional entropy changes between two finite native slots, numerical diagnostic')

# AD2/source-ref isometry on all four source/reference columns.
cx=lambda i,j:g('CX',(i,j));swap=(cx(0,1),cx(1,0),cx(0,1))
e=n.Execution(3,(),(2,),swap,n.G_CX)
U=n.word_matrix(e,max_qubits=3,max_expanded_stages=3);vv=s.Matrix([a,p]);id2=s.eye(2)
ck(meq(U*s.kronecker_product(id2,vv,id2),s.kronecker_product(vv,id2,id2)),'paid AD2 source handoff preserves arbitrary entangled source/reference input')
print(json.dumps({'status':'PASS_EXACT_AND_NUMERIC','check_count':len(checks),'exact_check_count':len(checks)-1,'numeric_diagnostic_count':1,'four_independent_finite_preparation_patterns':16,
 'checks':checks,'optional_real_fine_subprobabilities':fine_witness,
 'optional_fine_conditional_entropy_nats_numerical':fine_entropy,
 'scope':'real one-SourceI finite profile, all protected Spin/reference inputs; explicit four-slot fixture not full H1 word or required fine-label inventory',
 'full_H1_extended_task_admission':False,'full_fine_entropy_source_proved':False,'physical_C_closed':False,'GR_closed':False},indent=2))
