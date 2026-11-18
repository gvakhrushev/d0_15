#!/usr/bin/env python3
"""Exact physical birth, routed inverse and tail SWAP; no full H.1 replay."""
from collections import Counter
from pathlib import Path
import importlib.util
import sys
import sympy as sp

source=Path(__file__).resolve().parents[1]/'inputs'/'native_execution.py'
spec=importlib.util.spec_from_file_location('tail_handoff_native',source)
nt=importlib.util.module_from_spec(spec); sys.modules[spec.name]=nt; spec.loader.exec_module(nt)
G=nt.Gate
cx=lambda a,b:G('CX',(a,b))
swap=lambda a,b:(cx(a,b),cx(b,a),cx(a,b))
port,r,t,z=0,1,2,3
spin=(4,5)
sign=swap(port,z)+(G('SourceI',(port,*spin)),)*2+swap(port,z)
inverse=sign+(G('G',(z,)),)+sign
word=inverse+swap(t,z)
counts=Counter(g.op for g in word)
assert counts=={'CX':15,'SourceI':4,'G':1} and len(word)==20
execution=nt.Execution(6,(),(),word,nt.G_CX_SOURCE_I,port,spin)
nt.validate_execution(execution,max_qubits=6,max_expanded_stages=20)
U=nt.word_matrix(execution,max_qubits=6,max_expanded_stages=20)
v=sp.Matrix([nt.A,nt.P])
J=sp.kronecker_product(sp.eye(8),v,sp.eye(4))

# Input order port,r,t,spin; output order port,r,t,z,spin.
V=sp.zeros(64,32)
for a in range(2):
  for b in range(2):
    for tail in range(2):
      for s in range(4):
        before=(((a*2+b)*2+tail)*4+s)
        after=((((a*2+b)*2+0)*2+tail)*4+s)
        V[after,before]=1
assert nt.exact_matrix_equal(U*J,V)
assert nt.exact_matrix_equal(V.T*V,sp.eye(32))

# For every matrix unit on the old tail, exact intertwining proves any old
# reader on that tail is moved to z (with arbitrary r, Spin, port and ref).
I2=sp.eye(2); I4=sp.eye(4)
for i in range(2):
  for j in range(2):
    e=sp.zeros(2); e[i,j]=1
    old=sp.kronecker_product(I2,I2,e,I4)
    moved=sp.kronecker_product(I2,I2,I2,e,I4)
    assert nt.exact_matrix_equal(V*old,moved*V)

# Coarse effect preservation on the ACTUAL valid support; explicit dirty-11
# counterexample shows that this is not an all-bank projector commutation.
P0in=sp.kronecker_product(I2,sp.diag(1,0),I2,I4)
P1in=sp.kronecker_product(I2,sp.diag(0,1),sp.diag(1,0),I4)
Pinv=sp.kronecker_product(I2,sp.diag(0,1),sp.diag(0,1),I4)
P0out=sp.kronecker_product(I2,sp.diag(1,0),I2,I2,I4)
P1out=sp.kronecker_product(I2,sp.diag(0,1),sp.diag(1,0),I2,I4)
P01out=sp.kronecker_product(I2,sp.diag(1,0),sp.diag(0,1),I2,I4)
assert nt.exact_matrix_equal(V.T*P0out*V,P0in)
assert nt.exact_matrix_equal(V.T*P1out*V,P1in+Pinv)
assert nt.exact_matrix_equal(V.T*P01out*V,sp.zeros(32))
assert not nt.exact_matrix_equal(V.T*P1out*V,P1in)
print('PASS: 1 birth + 20 calls: 15 CX, 4 SourceI, 1 G; 21 stages.')
print('PASS: all 32 true-cut columns, isometry, 4 old-tail matrix units and valid-support AD1.')
print('PASS: dirty-11 counterexample: full-bank original P1 is not preserved.')
print('Not checked: actual full H.1 execution, all required future reader transports, full clock or physical C.')
