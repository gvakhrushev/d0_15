#!/usr/bin/env python3
"""Independent exact Q-insertion and full-clock slot-swap fixtures."""
from pathlib import Path
import json,sympy as s
P=Path(__file__).resolve().parent;R=s.Rational;I=s.eye
# Endpoints alone cannot determine inserted source kernel. B,C controlled,
# S reflected and CODE-disjoint; change B,C in compensating fashion.
rot=lambda a,b:s.Matrix([[a,-b],[b,a]])
X=s.Matrix([[0,1],[1,0]]);Z=s.diag(1,-1);J=s.Matrix([[0,-1],[1,0]]);I2=I(2)
controlled=lambda a,b:s.diag(a,b)
B=controlled(I2,rot(R(3,5),R(4,5)));S=s.kronecker_product(I2,Z);Y=s.kronecker_product(J,I2)
C=B.T;T=controlled(rot(R(5,13),R(12,13)),I2)
Bh=T*B;Ch=C*S*T.T*S
assert C*S*B==Ch*S*Bh
assert C*Y*S*B!=Ch*Y*S*Bh
assert Y*S==S*Y
# Compute a genuinely nonsymmetric cross-kernel for a real actual C != B^T.
Bh=controlled(I2,rot(R(3,5),R(4,5)));Ch=controlled(rot(R(5,13),R(12,13)),I2)
w=s.Matrix([1,0]);L=s.Matrix(2,2,lambda c,b:(w.T*Ch[2*c:2*c+2,2*c:2*c+2]*Z*Bh[2*b:2*b+2,2*b:2*b+2]*w)[0])
assert L[0,1]!=L[1,0]
# Different +/- actual words: not adjoint to one another. Each slot uses
# exactly two stages and identity filler X;X. Move the same word across S.
qplus=[s.kronecker_product(rot(R(3,5),R(4,5)),I2),s.kronecker_product(X,I2)]
qminus=[s.kronecker_product(rot(R(5,13),R(12,13)),I2),s.kronecker_product(X,I2)]
pad=s.kronecker_product(X,I2);S1=s.kronecker_product(I2,rot(R(5,13),R(12,13)));S2=s.kronecker_product(I2,X)
post=s.kronecker_product(rot(R(8,17),R(15,17)),I2)
def mul(seq):
 z=I(4)
 for a in seq:z=a*z
 return z
assert mul(qminus)!=mul(qplus).T

def clock(gates):
 born=s.Matrix([1,0,0,0]);birth=I(4).col_join(s.zeros(4,4));end=s.kronecker_product(rot(R(3,5),R(4,5)),I(4))
 acts=[born]+gates+[birth,end];pas=[born]+[I(4)]*len(gates)+[birth,I(8)];dims=[1]+[4]*(len(gates)+1)+[8];starts=[];total=0
 for d in dims:starts.append(total);total+=d
 def comp(j):
  z=I(dims[j])
  for k in range(j,len(dims)-1):z=pas[k]*z
  return z
 ret=comp(0).T
 for j in range(1,len(dims)):ret=ret.col_join((I(dims[j])-pas[j-1]*pas[j-1].T)*comp(j).T)
 assert ret.T*ret==I(8)
 shift=s.zeros(total)
 for j in range(len(dims)-1):shift[starts[j+1]:starts[j+1]+dims[j+1],starts[j]:starts[j]+dims[j]]=acts[j]
 ef=s.zeros(8,total);ef[:,starts[-1]:]=I(8);clockT=shift+ret*acts[-1]*ef;pro=s.zeros(total);a=I(1);prefix=[]
 for j in range(len(dims)):
  prefix.append(a);pro[starts[j]:starts[j]+dims[j],starts[j]:starts[j]+dims[j]]=a*a.T
  if j<len(dims)-1:a=acts[j]*a
 return clockT,pro,prefix,dims
for word in (qplus,qminus):
 early=[B,*word,S1,S2,pad,pad,Ch,post];late=[B,pad,pad,S1,S2,*word,Ch,post]
 assert mul(early)==mul(late)
 T1,P1,a,d=clock(early);T2,P2,b,dd=clock(late);assert d==dd
 U=I(4);V=I(4);blocks=[I(1),I(4)]
 for x,y in zip(early,late):U=x*U;V=y*V;blocks.append(V*U.T)
 assert blocks[-1]==I(4);blocks.append(I(8));G=s.diag(*blocks)
 assert T2==G*T1*G.T and P2==G*P1*G.T
 F1=P1*T1.T*(I(T1.rows)-P1)*T1*P1;F2=P2*T2.T*(I(T2.rows)-P2)*T2*P2;assert F2==G*F1*G.T
 sceneB=s.Matrix([[R(1,3),R(1,7)],[R(1,7),R(2,5)]]);sceneC=s.Matrix([[R(1,8),R(1,11)],[R(1,11),R(1,6)]])
 delta=I(2*T1.rows)-s.kronecker_product(sceneB,I(T1.rows))-s.kronecker_product(sceneC,T1+T1.T);deltap=I(2*T1.rows)-s.kronecker_product(sceneB,I(T2.rows))-s.kronecker_product(sceneC,T2+T2.T);gg=s.kronecker_product(I2,G);assert deltap==gg*delta*gg.T
 mark=s.kronecker_product(Z,I2);assert a[3].T*mark*a[3]!=b[3].T*mark*b[3]
out={'status':'PASS_NONSYMMETRIC_KERNEL_AND_EXACT_GROWING_CLOCK_SWAP','endpoint_equality_does_not_fix_insertion_kernel':True,'actual_nonsymmetric_kernel_example':True,'two_noninverse_control_words':True,'same_Q_word_commutes_with_work_middle':True,'both_full_growing_clocks_and_feedback_heat_conjugate':True,'birth_complements_retained':True,'fixed_intermediate_mark_not_equal':True,'fixture_not_production_execution':True,'original_mark_admission_proved':False,'GR_closed':False}
(P/'NONSYMMETRIC_CLOCK_FIXTURE_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
