"""Numerical replay of the full 33-scene; the inequalities are proved in the note."""
import json
from math import exp, factorial, log, log1p
import numpy as np
from scipy.linalg import block_diag, eigvalsh
from scipy.sparse import csr_matrix, diags, eye, kron

def mm(a, b):
    return np.einsum("ij,jk->ik", a, b, optimize=False)


p = (np.sqrt(5)-1)/2
a = np.sqrt(p)
G = np.array([[a,-p],[p,a]])
v = G[:,0:1]
spin = np.eye(4)
Li = np.array([[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]])
CX = np.eye(4)[[0,1,3,2]]
S = np.kron(spin, np.diag([1,0])) + np.kron(Li,np.diag([0,1]))
dims = [4,8,8,16,16]
cut = np.cumsum([0]+dims)
D = sum(dims)
gates = [np.kron(spin,v),np.kron(spin,G),np.kron(np.eye(8),v),
         np.kron(spin,CX),np.kron(S,np.eye(2))]
births = [True,False,True,False]
passive = [g if b else np.eye(g.shape[0]) for g,b in zip(gates,births)]
R = []
for j,d in enumerate(dims):
    E = np.eye(d)
    if j:
        E -= mm(passive[j-1],passive[j-1].T)
    tail = np.eye(d)
    for inc in passive[j:]:
        tail = mm(inc,tail)
    R.append(mm(E,tail.T))
T = np.zeros((D,D))
for j,g in enumerate(gates[:-1]):
    T[cut[j+1]:cut[j+2],cut[j]:cut[j+1]] = g
T[:,cut[-2]:] = mm(np.vstack(R),gates[-1])
frame = [spin,np.kron(spin,G),np.kron(spin,G),
         np.kron(np.kron(spin,G),G),np.kron(np.kron(spin,G),G)]
basis = block_diag(*frame)
T_native = mm(mm(basis.T,T),basis)

Tb = np.zeros_like(T)
for j,g in enumerate(gates[:-1]):
    inner = (np.kron(np.eye(dims[j]),np.array([[1],[0]])) if births[j]
             else mm(mm(frame[j].T,g),frame[j]))
    Tb[cut[j+1]:cut[j+2],cut[j]:cut[j+1]] = inner
# coordinate convention is |spin,port,aux>; latest w is the rightmost set bit.
for fin in range(dims[-1]):
    s, rem = divmod(fin,4)
    port, aux = divmod(rem,2)
    dest = cut[3]+fin if aux else (cut[1]+2*s+port if port else s)
    Tb[dest, cut[-2]:] = (mm(mm(frame[-1].T,gates[-1]),frame[-1]))[fin]
assert np.linalg.norm(Tb-T_native,np.inf) < 2e-14
assert np.linalg.norm(mm(Tb.T,Tb)-np.eye(D),np.inf) < 1e-14

scene = np.repeat(np.arange(3),[9,11,13])
A = (scene[:,None] != scene[None,:]).astype(float)
deg = A.sum(axis=0)+2
R = np.diag(1/np.sqrt(deg))
B, C = mm(mm(R,A),R), mm(R,R)
beta = 2*p*p
Sscene = kron(diags(np.sqrt(deg)),eye(D))
iSscene = kron(diags(1/np.sqrt(deg)),eye(D))
Mroute = kron(csr_matrix(A/deg),eye(D)) + kron(diags(1/deg),csr_matrix(Tb+Tb.T))
MsymBorn = kron(csr_matrix(B),eye(D)) + kron(diags(1/deg),csr_matrix(Tb+Tb.T))
error = Sscene@MsymBorn@iSscene-Mroute
assert np.max(np.abs(error.data)) < 3e-15

# Absolute probabilities selected per labelled move; overlaps can add no excess.
abs_basis = np.abs(Tb)+np.abs(Tb.T)
bound = np.max((deg[:,None]-2+abs_basis.sum(axis=0))/deg[:,None])
Cwalk = 12/11
assert bound <= Cwalk
temps = eigvalsh(T + T.T)
Mspec = np.concatenate([eigvalsh(B+t*C) for t in temps])
heat = np.mean(np.exp(-beta*(1-Mspec)))
mean = exp(-beta*Cwalk)*sum((beta**n/factorial(n))*np.mean(Mspec**n)
                              for n in range(18))
target = exp(-beta*(Cwalk-1))*heat
pois18 = exp(-beta*Cwalk) * (beta*Cwalk)**18/factorial(18)/(1-beta*Cwalk/19)
assert abs(mean-target) < 6e-15 + pois18
b = 66*exp(beta*(Cwalk-1))/359
lam = -log1p(-b)
replica = sum((-1)**(n+1)*(b*target)**n/n for n in range(1,31))
assert abs(log(359*D)+replica-log(359*D+66*D*heat)) < 1e-14
s = log(1/p)/beta
c = 2*b/(1+b)
r = (1-target)/2
weight = (1-c)**s
accept = weight
for n in range(1,100):
    weight *= (s+n-1)*c/n
    accept += weight*r**n
flag = accept * (359*D*(1-b))**(-s)
assert abs(flag-(359*D+66*D*heat)**(-s)) < 2e-17
print(json.dumps(dict(positive_flag=flag, stage_dimensions=dims, clock_dimension=D, primitive_word=[
    "birth port","G port","birth aux","CX port->aux","SourceI port Spin"],
    clock_orthogonality_error=float(np.linalg.norm(mm(Tb.T,Tb)-np.eye(D),np.inf)),
    max_clock_column_or_row_l1=float(max(np.max(np.sum(abs(Tb),axis=i)) for i in (0,1))),
    max_labelled_step_column_l1=float(bound), envelope=12/11,
    normalized_heat=heat, expected_signed_score=target, poisson_tail_18=pois18,
    expected_replicas=b/((1-b)*lam), log_partition=log(359*D+66*D*heat)),indent=2))
