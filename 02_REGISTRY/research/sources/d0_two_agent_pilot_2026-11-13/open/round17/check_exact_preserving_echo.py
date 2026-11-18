#!/usr/bin/env python3
"""Exact source-profile inverse echo after original E0, on every column."""
from collections import Counter
from pathlib import Path
import importlib.util,sys
import math
import numpy as np
import sympy as sp

source=Path(__file__).resolve().parents[1]/'inputs'/'native_execution.py'
spec=importlib.util.spec_from_file_location('echo_native',source)
nt=importlib.util.module_from_spec(spec);sys.modules[spec.name]=nt;spec.loader.exec_module(nt)
G=nt.Gate;cx=lambda x,y:G('CX',(x,y)); swap=lambda x,y:(cx(x,y),cx(y,x),cx(x,y))
port,r,t=0,1,2; spin=(3,4)
sign=swap(port,t)+(G('SourceI',(port,*spin)),)*2+swap(port,t)
inv=sign+(G('G',(t,)),)+sign
echo=(cx(r,t),)+inv+(cx(r,t),)+inv
E0=(cx(r,t),G('G',(t,)),cx(r,t))
assert len(inv)==17 and len(echo)==36
assert Counter(g.op for g in echo)=={'CX':26,'SourceI':8,'G':2}

def matrix(word):
    e=nt.Execution(5,(),(),word,nt.G_CX_SOURCE_I,port,spin)
    nt.validate_execution(e,max_qubits=5,max_expanded_stages=40)
    return nt.word_matrix(e,max_qubits=5,max_expanded_stages=40)

U=matrix(echo); W=matrix(E0+echo); I2=sp.eye(2); I4=sp.eye(4)
g=nt.G_LOCAL; gi=g.T
block=sp.diag(1,1,1,1);block[:2,:2]=gi**2
assert nt.exact_matrix_equal(U,sp.kronecker_product(I2,block,I4))
assert nt.exact_matrix_equal(W,sp.kronecker_product(I2,I2,gi,I4))
P0=sp.kronecker_product(I2,sp.diag(1,0),I2,I4)
P1=sp.kronecker_product(I2,sp.diag(0,1),sp.diag(1,0),I4)
Pinv=sp.kronecker_product(I2,sp.diag(0,1),sp.diag(0,1),I4)
for P in (P0,P1,Pinv): assert nt.exact_matrix_equal(U.T*P*U,P)
v=sp.Matrix([nt.A,nt.P]); zero=sp.Matrix([1,0])
J=sp.kronecker_product(I2,I2,v,I4); Z=sp.kronecker_product(I2,I2,zero,I4)
assert nt.exact_matrix_equal(W*J,Z)
assert nt.exact_matrix_equal((sp.eye(32)-P0-P1)*W*J,sp.zeros(32,16))

# Diagnostic of the general ideal u target on arbitrary entangled pointer
# and bank/reference amplitudes; this is not an exact finite native word.
pf=float(nt.P); af=math.sqrt(pf); angle=math.asin(pf)
gf=np.array([[af,-pf],[pf,af]])
vf=np.array([af,pf]); rng=np.random.default_rng(1717)
psi=rng.normal(size=(2,7))+1j*rng.normal(size=(2,7));psi/=np.linalg.norm(psi)
for theta in np.linspace(0,math.pi/2,9):
    delta=theta-2*angle
    rot=np.array([[math.cos(delta),-math.sin(delta)],[math.sin(delta),math.cos(delta)]])
    zero_tail=np.array([1.,0.]); desired=np.array([math.cos(theta),math.sin(theta)])
    actual0=np.outer(rot@gf@vf,psi[0]); expected0=np.outer(desired,psi[0])
    actual1=np.outer(gf.T@vf,psi[1]); expected1=np.outer(zero_tail,psi[1])
    assert np.linalg.norm(actual0-expected0)<1e-12 and np.linalg.norm(actual1-expected1)<1e-12
print('PASS: inverse echo has 36 calls: 26 CX, 8 SourceI, 2 G; no births.')
print('PASS: all 32 columns: inverse echo diag(G^-2,I), preserves P0/P1/Pinvalid exactly.')
print('PASS: original E0 + inverse echo equals I_r tensor G^-1 on every column.')
print('PASS: all 16 true input columns map t=v to t=0 without LC4 or information loss.')
print('PASS: 9 ideal general-u targets on a complex entangled pointer/bank diagnostic.')
print('Not checked: complete H.1 writer, all marked readers, full clock or physical C.')
