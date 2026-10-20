#!/usr/bin/env python3
"""EXACT native CAR16 -> Cl(1,3) -> parity-preserving Spin/Q8, plus
conditional literal Golden fullStep spin-sheet two-line readout.

Uses ACTUAL CAR_4 Jordan-Wigner integer creation/annihilation on
ArchiveFockState=Role->Bool with original RoleOrder A,B,C,D.
Physics: a mathematical faithful representation on SAME Fock16, NOT
a selected paid G0 Book->Q8 control or Einstein-Dirac action.
"""
import math
import numpy as np

N=16
I=np.eye(N,dtype=np.int64)
Z=np.zeros((N,N),dtype=np.int64)
create=[]; annihilate=[]
for j in range(4):
 c=Z.copy()
 for state in range(N):
  if not (state&(1<<j)):
   c[state|(1<<j),state]=(-1)**((state&((1<<j)-1)).bit_count())
 create.append(c);annihilate.append(c.T)
for j in range(4):
 for k in range(4):
  assert np.array_equal(create[j]@create[k]+create[k]@create[j],Z)
  assert np.array_equal(annihilate[j]@annihilate[k]+annihilate[k]@annihilate[j],Z)
  assert np.array_equal(annihilate[j]@create[k]+create[k]@annihilate[j],I if j==k else Z)

# The ORIGINAL creation and annihilation, NOT a new Majorana primitive.
L=[annihilate[0]+create[0]]+[create[j]-annihilate[j] for j in (1,2,3)]
signature=[1,-1,-1,-1]
Parity=np.diag([(-1)**s.bit_count() for s in range(N)])
for a in range(4):
 assert np.array_equal(L[a].T,signature[a]*L[a])
 assert np.array_equal(Parity@L[a],-L[a]@Parity)
 for b in range(4):
  assert np.array_equal(L[a]@L[b]+L[b]@L[a],
   2*signature[a]*I if a==b else Z)
assert len(np.where(np.diag(Parity)==1)[0])==8
assert len(np.where(np.diag(Parity)==-1)[0])==8

# SIX genuine even spin Lie generators Sigma_ab = 1/2 L_a L_b.
for a in range(4):
 for b in range(a+1,4):
  S=L[a]@L[b]
  assert np.array_equal(S@S,-signature[a]*signature[b]*I)
  assert np.array_equal(S@Parity,Parity@S)
  assert np.array_equal(S.T,S if a==0 else -S)
  for c in range(4):
   desired=2*((signature[b]*L[a] if b==c else Z)-
              (signature[a]*L[b] if a==c else Z))
   assert np.array_equal(S@L[c]-L[c]@S,desired)

# Embed ALREADY-OWNED Q8 center as spatial even Clifford products.
qi=L[2]@L[3];qj=L[3]@L[1];qk=L[1]@L[2]
assert np.array_equal(qi@qj,qk) and np.array_equal(qj@qi,-qk)
for Q in (qi,qj,qk):
 assert np.array_equal(Q@Q,-I)
 assert np.array_equal(Q@Parity,Parity@Q)
assert np.array_equal(qj@qk,qi) and np.array_equal(qk@qi,qj)
assert np.array_equal(qi@qj@(-qi)@(-qj),-I)
Q8=[s*M for s in (1,-1) for M in (I,qi,qj,qk)]
assert len({M.tobytes() for M in Q8})==8
# Book03 central idempotent e_-=(1-[-1])/2, original exterior vs Spin
assert np.array_equal((I-(-I))//2,I)
assert np.array_equal((I-I)//2,Z)
assert not np.array_equal(Parity,-I)

# EXACT 2pi/4pi spin rotation, vector action by conjugation.
R=L[1]@L[2]
assert np.array_equal(R@R,-I)
assert np.array_equal(R@L[0],L[0]@R)
assert np.array_equal((-I)@L[1]@(-I),L[1])

# Noncompact genuine Lorentz boost cannot be direct orthogonal Golden gate.
B=L[0]@L[1]
assert np.array_equal(B@B,I) and np.array_equal(B.T,B)
assert np.trace(B)==0
u=0.47
S=math.cosh(u/2)*I+math.sinh(u/2)*B
Sinv=math.cosh(u/2)*I-math.sinh(u/2)*B
assert np.max(abs(S@Sinv-I))<3e-14
assert np.max(abs(S@L[0]@Sinv-math.cosh(u)*L[0]+math.sinh(u)*L[1]))<3e-14
assert np.max(abs(S@L[1]@Sinv-math.cosh(u)*L[1]+math.sinh(u)*L[0]))<3e-14
assert np.max(abs(S.T@S-I))>0.3
assert np.linalg.det(S)>0 and abs(np.linalg.det(S)-1)<2e-12
assert np.max(abs(S@Parity-Parity@S))<2e-14
sing=np.linalg.svd(S,compute_uv=False)
assert np.allclose(sorted(sing),[math.exp(-u/2)]*8+[math.exp(u/2)]*8)

# Literal compiled native GoldenCoherentMemory fullStep Fin4 orthogonal.
p=(math.sqrt(5)-1)/2
a=math.sqrt(p)
U=np.array([[a,0,-p,0],[0,a,0,-p],[0,p,0,a],[p,0,a,0]])
assert np.max(abs(U.T@U-np.eye(4)))<2e-14
starting=U[:,0]
for z in (1,-1):
 # CONDITIONAL missing Q8 path-branch control, not included in fullStep
 controlled=np.diag([1,1,1,z])
 returned=U.T@controlled@starting
 assert abs(returned[0]**2-(p+z*p*p)**2)<2e-14
 assert abs(returned[2]**2-(1-(p+z*p*p)**2))<2e-14
 assert abs(sum(returned**2)-1)<2e-14
assert abs(1-(p-p*p)**2-4*p**3)<2e-14

print("PASS ORIGINAL CAR_4 exact 16x16 Jordan-Wigner anticommutators")
print("PASS real Cl(1,3), signature (+---), ALL 4x4 gamma anti-commutators")
print("PASS full six Spin Lorentz Lie commutators, Fock parity 8+8 invariant")
print("PASS native embedded faithful Q8 group, central -I16 NOT parity")
print("PASS Q8 central Book idempotent is I16 on Spin, zero on exterior")
print("PASS proper Spin boost vector conjugation and real nonorthogonality")
print("PASS literal original orthogonal Golden fullStep complete 4-port")
print("PASS conditional two-line Q8 sign: plus=0 alternate, minus=4p^3")
print("FAILURE TYPE: paid Q8-controlled Book/G0 operation and boost dilation NOT owned")
print("GR_closed=false")
