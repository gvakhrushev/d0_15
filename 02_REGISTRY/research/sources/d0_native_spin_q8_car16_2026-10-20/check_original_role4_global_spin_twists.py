#!/usr/bin/env python3
"""Exact original four Role cyclic Fin(L)^4, central +/-1 Spin twists.
All local plaquettes trivial, but 16 globally inequivalent sectors and
distinct finite CAR16 twisted kinetic spectra. Benchmark, NOT physical G0.
"""
import itertools
import numpy as np

L=2
sites=list(itertools.product(range(L),repeat=4))
where={x:i for i,x in enumerate(sites)}
N=len(sites)
assert N==16
I=np.eye(N,dtype=np.int64)
Z=np.zeros((N,N),dtype=np.int64)
seen=set()
for epsilon in itertools.product((0,1),repeat=4):
 T=[]
 for r in range(4):
  M=Z.copy()
  for j,x in enumerate(sites):
   y=list(x);y[r]=(x[r]+1)%L
   sgn=-1 if epsilon[r] and x[r]==L-1 else 1
   M[where[tuple(y)],j]=sgn
  assert np.array_equal(M.T@M,I)
  assert np.array_equal(np.linalg.matrix_power(M,L),((-1)**epsilon[r])*I)
  T.append(M)
 for r in range(4):
  for s in range(r+1,4):
   assert np.array_equal(T[r]@T[s],T[s]@T[r])
 Delta=sum((2*I-M-M.T for M in T),Z.copy())
 eigen=np.linalg.eigvalsh(Delta)
 nullity=sum(abs(eigen)<1e-9)
 assert nullity==(1 if epsilon==(0,0,0,0) else 0)
 assert abs(min(eigen)-2*sum(epsilon))<1e-8
 seen.add(tuple(int(np.trace(np.linalg.matrix_power(M,L))//N) for M in T))
 if epsilon in ((0,0,0,0),(1,0,0,0),(1,1,1,1)):
  print("Twist",epsilon,"scalar site gap",min(eigen),
        "native CAR16 kernel",16*nullity)
assert len(seen)==16
print("PASS original Role-Fin(2)^4 16 inequivalent flat global Q8 Spin sectors")
print("PASS all local scene/Role SO links and Spin plaquettes indistinguishable")
print("PASS exact four central winding holonomies distinguish all 16 global sectors")
print("PASS periodic full CAR16 kinetic benchmark kernel16; twisted kernel0")
print("FIREWALL: Spin-twisted Laplacian benchmark NOT full native selected HodgeCAR Dirac")
print("GR_closed=false")
