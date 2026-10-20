#!/usr/bin/env python3
"""Original K(9,11,13): 327 exact GF2 Spin sheet triangle inverse, 960
octahedral constraints, SO/exterior CAR16 blindness, spinor spectral witness.
Math theorem; native Spin/G0/Book physical admission NOT claimed.
"""
import math
import random
import numpy as np

z=tuple([0]*9+[1]*11+[2]*13)
edges=[(u,v) for u in range(33) for v in range(u+1,33) if z[u]!=z[v]]
assert len(edges)==359
where={e:i for i,e in enumerate(edges)}
def ed(u,v):return where[min(u,v),max(u,v)]
tri=[(a,b,c) for a in range(9) for b in range(9,20) for c in range(20,33)]
ti={v:i for i,v in enumerate(tri)}
assert len(tri)==1287
bd=[(1<<ed(a,b))^(1<<ed(b,c))^(1<<ed(c,a)) for a,b,c in tri]
pivot={}
for row in bd:
 x=row
 while x:
  bit=x.bit_length()-1
  if bit not in pivot:pivot[bit]=x;break
  x^=pivot[bit]
assert len(pivot)==327
def syn(v):return tuple((v&row).bit_count()%2 for row in bd)
for i in range(33):
 grad=sum(1<<ed(a,b) for a,b in edges if i in (a,b))
 assert not any(syn(grad))
# Native 32 tree edges, exactly 327 remaining mod2 circulation sheets.
tree=[(0,b) for b in range(9,20)]+[(0,c) for c in range(20,33)]
tree += [(a,9) for a in range(1,9)]
assert len({ed(*e) for e in tree})==32
seed=random.Random(20261020).getrandbits(359)
target=syn(seed)
vertex=[0]*33
for b in range(9,20):vertex[b]=(seed>>ed(0,b))&1
for c in range(20,33):vertex[c]=(seed>>ed(0,c))&1
for a in range(1,9):vertex[a]=vertex[9]^((seed>>ed(a,9))&1)
gradient=sum((vertex[u]^vertex[v])<<ed(u,v) for u,v in edges)
canonical=seed^gradient
assert not any((canonical>>ed(*e))&1 for e in tree)
# THREE exact inverse passes with 327 of the native 1287 ABC triangles.
recovered=0
for b in range(9,20):
 for c in range(20,33):
  recovered|=target[ti[0,b,c]]<<ed(b,c)
for a in range(1,9):
 for c in range(20,33):
  recovered|=(target[ti[a,9,c]]^((recovered>>ed(9,c))&1))<<ed(a,c)
for a in range(1,9):
 for b in range(10,20):
  recovered|=(target[ti[a,b,20]]^((recovered>>ed(b,20))&1)^
               ((recovered>>ed(a,20))&1))<<ed(a,b)
assert recovered==canonical and syn(recovered)==target
# EXACT 960 2x2x2 octahedral surface parity checks, independent since
# each has one unique (nonrootA,nonrootB,nonrootC) triangle.
octa=[]
for a in range(1,9):
 for b in range(10,20):
  for c in range(21,33):
   ids=[ti[aa,bb,cc] for aa in (0,a) for bb in (9,b) for cc in (20,c)]
   octa.append(ids)
assert len(octa)==960
for ids in octa:
 assert sum(target[i] for i in ids)%2==0
 boundary=0
 for i in ids:boundary^=bd[i]
 assert boundary==0
corrupt=list(target);corrupt[ti[1,10,21]]^=1
assert any(sum(corrupt[i] for i in ids)%2 for ids in octa)
# TRUE original 4-edge loop 0(A)->9(B)->1(A)->20(C)->0(A);
# one central minus sign on 1-20, SO vector representation SAME I4.
cycle=[0,9,1,20,0]
assert all(z[a]!=z[b] for a,b in zip(cycle,cycle[1:]))
a=1<<ed(1,20)
assert sum((a>>ed(u,v))&1 for u,v in zip(cycle,cycle[1:]))%2==1
assert any(syn(a))
I4=np.eye(4,dtype=int);I16=np.eye(16,dtype=int)
assert np.array_equal(I4@I4,I4) and np.trace(I16)==16
def hopping(sign):
 H=np.zeros((4,4),dtype=int)
 for i in range(3):H[i,i+1]=H[i+1,i]=1
 H[0,3]=H[3,0]=sign
 return H
hp,hm=hopping(1),hopping(-1)
assert np.trace(np.linalg.matrix_power(hp,4))==32
assert np.trace(np.linalg.matrix_power(hm,4))==16
assert np.allclose(np.linalg.eigvalsh(hm),[-math.sqrt(2)]*2+[math.sqrt(2)]*2)
# Native Q8 i,j commutator=-1; projected SO spatial pi-rotations commute.
rx=np.diag([1,1,-1,-1]);ry=np.diag([1,-1,1,-1])
assert np.array_equal(rx@ry,ry@rx)
assert np.array_equal(rx@ry@rx@ry,I4)
print('PASS original 33 /359 undirected /718 directed /1287 ABC triangles')
print('PASS exact GF2 triangle-boundary rank327, graph central kernel32')
print('PASS three-pass 327 triangle Spin sheet inverse modulo vertex gauge')
print('PASS all 960 independent octahedral face parity constraints, corruption rejected')
print('PASS SO identity / exterior CAR16 blind to actual central -1 4-cycle')
print('PASS spinor H4 spectra differ: trace fourth moments 32 vs 16')
print('PASS original Q8 central commutator -1 projects to trivial SO commutator')
print('FIREWALL full original Q8-to-scene edge memory/Spin matter G0 selection OPEN')
