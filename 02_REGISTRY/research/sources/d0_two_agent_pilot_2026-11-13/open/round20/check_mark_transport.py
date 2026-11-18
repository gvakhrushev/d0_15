#!/usr/bin/env python3
"""Native all-column mark transport and seal boundary; bounded fixture only."""
from pathlib import Path
import importlib.util,sys
import sympy as sp

source=Path(__file__).resolve().parents[1]/'inputs'/'native_execution.py'
spec=importlib.util.spec_from_file_location('marks_native',source)
nt=importlib.util.module_from_spec(spec);sys.modules[spec.name]=nt;spec.loader.exec_module(nt)
G=nt.Gate;cx=lambda c,t:G('CX',(c,t));I=sp.eye(2)
spin=(0,1);e,b,r,t=2,3,4,5
profile=nt.G_CX_SOURCE_I

def ex(word,old=()):return nt.Execution(6,(),tuple(old),tuple(word),profile,e,spin)
def mat(word):return nt.word_matrix(ex(word),max_qubits=6,max_expanded_stages=128)
def same(a,b):return nt.exact_matrix_equal(a,b)

# Actual NPS14 owner fixture, not the ten-sign H.1 bank itself.
nps=(cx(b,e),cx(e,r),G('SourceI',(e,*spin)),G('SourceI',(e,*spin)),
     cx(b,e),cx(r,t),G('G',(t,)),cx(r,t))
nt.validate_execution(ex(nps),max_qubits=6,max_expanded_stages=128)
assert len(nps)==8

# NPS's new pointer copy preserves the actual port event P_e1, but need
# not preserve a noncommuting earlier coherent observable on that port.
copy=mat((cx(e,r),))
Pe=sp.kronecker_product(I,I,sp.diag(0,1),I,I,I)
Xe=sp.kronecker_product(I,I,sp.Matrix([[0,1],[1,0]]),I,I,I)
assert same(copy.T*Pe*copy,Pe)
assert not same(copy.T*Xe*copy,Xe)

# An actual supported suffix and its *physically expanded* native inverse.
word=(G('G',(t,)),cx(r,t),G('G',(t,)),cx(r,t))
word_ex=ex(word);nt.validate_execution(word_ex,max_qubits=6,max_expanded_stages=128)
reverse=nt.inverse_word(word_ex,max_qubits=6,max_expanded_stages=128)
assert len(word)==4 and len(reverse)==24
R=mat(word);Rinv=mat(reverse)
assert same(Rinv,R.T) and same(Rinv*R,sp.eye(64))
P0=sp.kronecker_product(I,I,I,I,sp.diag(1,0),I)
P1=sp.kronecker_product(I,I,I,I,sp.diag(0,1),sp.diag(1,0))
Pbad=sp.kronecker_product(I,I,I,I,sp.diag(0,1),sp.diag(0,1))
assert all(same(R.T*P*R,P) for P in (P0,P1,Pbad))
O=sp.kronecker_product(I,I,I,I,I,sp.diag(1,0))
transported=R*O*R.T
assert same(R.T*transported*R,O) and not same(transported,O)
assert not nt.is_member(ex(reverse,old=(t,)),max_qubits=6,max_expanded_stages=128)
assert not nt.is_member(ex(word,old=(r,)),max_qubits=6,max_expanded_stages=128)

# NPS14 plus an exact inverse echo, on its original 4-column Spin cut.
# The two normalized NR readiness identities are tested through their
# unnormalized version; the equality control is a separate live pointer.
inv17=(cx(e,t),cx(t,e),cx(e,t),G('SourceI',(e,*spin)),G('SourceI',(e,*spin)),
       cx(e,t),cx(t,e),cx(e,t),G('G',(t,)),
       cx(e,t),cx(t,e),cx(e,t),G('SourceI',(e,*spin)),G('SourceI',(e,*spin)),
       cx(e,t),cx(t,e),cx(e,t))
echo=(cx(r,t),)+inv17+(cx(r,t),)+inv17
assert len(echo)==36
A=mat(nps+echo)
v=sp.Matrix([nt.A,nt.P]);J0=sp.kronecker_product(sp.eye(4),v,v,v,v)
V=A*J0;qb=nt.P**2+2*nt.P**6
for proj,prob in ((P0,1-qb),(P1,qb)):
    branch=proj*V
    assert same(branch.T*branch,prob*sp.eye(4))
    assert same(J0.T*A.T*branch,prob*sp.eye(4))
assert same(Pbad*V,sp.zeros(64,4))
assert not same((1-qb)*sp.eye(4),qb*sp.eye(4))

# Private r',t' are genuine born v factors; prepare both zero using the
# owner's exact routed inverse compiler, then copy the live external r.
pe,outer,pr,pt=0,1,2,3;pspin=(4,5)
private=nt.Execution(6,(),(),(G('G',(pr,)),G('G',(pt,))),profile,pe,pspin)
prep=nt.inverse_word(private,max_qubits=6,max_expanded_stages=128)
assert len(prep)==22
copy_private=nt.Execution(6,(),(),prep+(cx(outer,pr),),profile,pe,pspin)
Ucopy=nt.word_matrix(copy_private,max_qubits=6,max_expanded_stages=128)
Jcopy=sp.kronecker_product(I,I,v,v,sp.eye(4))
expected=sp.zeros(64,16)
for portbit in range(2):
  for value in range(2):
    for s in range(4):
      col=(portbit*2+value)*4+s
      row=((((portbit*2+value)*2+value)*2+0)*4+s)
      expected[row,col]=1
assert same(Ucopy*Jcopy,expected)

# AD2 handoff on an arbitrary dirty input of source e and fresh h=v.
swapword=(cx(0,1),cx(1,0),cx(0,1))
se=nt.Execution(2,(),(),swapword)
S=nt.word_matrix(se,max_qubits=2,max_expanded_stages=3)
v=sp.Matrix([nt.A,nt.P]); J=sp.kronecker_product(I,v); Vhandoff=sp.kronecker_product(v,I)
assert same(S*J,Vhandoff)
assert not nt.is_member(nt.Execution(2,(),(1,),(cx(0,1),)),max_qubits=2,max_expanded_stages=3)

print('PASS: actual 8-call NPS14 fixture; event-copy commutator and hostile coherent mark.')
print('PASS: 4-call exact support, native 24-call inverse, transported projector and two sealed-address rejections.')
print('PASS: paid birth+3-CX AD2 handoff on every old-source column; sealed old address rejected.')
print('PASS: NPS14+36 echo: both scalar NR branch identities on all four Spin columns, unequal q0/q1 and zero invalid.')
print('PASS: 2 private births + 22 paid inverse calls + 1 CX copy on all 16 live input columns.')
print('Scope: local literal fixture; no full ten-sign H.1 word or complete mark/address ledger emitted.')
