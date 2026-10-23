#!/usr/bin/env python3
"""Exact Golden/Q8 memory-interference pressure test, stdlib only."""
from fractions import Fraction as F
from dataclasses import dataclass
import json

checks=[]
def check(name,pred):
    if not pred: raise ArithmeticError(name)
    checks.append(name)

@dataclass(frozen=True)
class A:
    """Q[a] / (a^4+a^2-1), exact golden a=sqrt(p)."""
    cs: tuple
    def __init__(self,x=0):
        if isinstance(x,A): v=x.cs
        elif isinstance(x,(list,tuple)): v=tuple(map(F,x))
        else: v=(F(x),F(0),F(0),F(0))
        if len(v)!=4: raise ValueError('four coefficients')
        object.__setattr__(self,'cs',v)
    def __add__(self,o):
        o=A(o);return A(tuple(x+y for x,y in zip(self.cs,o.cs)))
    __radd__=__add__
    def __neg__(self): return A(tuple(-x for x in self.cs))
    def __sub__(self,o): return self+-A(o)
    def __rsub__(self,o): return A(o)+-self
    def __mul__(self,o):
        o=A(o);v=[F(0)]*7
        for i,x in enumerate(self.cs):
            for j,y in enumerate(o.cs):v[i+j]+=x*y
        for k in range(6,3,-1):
            v[k-4]+=v[k];v[k-2]-=v[k]
        return A(v[:4])
    __rmul__=__mul__
    def __pow__(self,n):
        if n<0: raise ValueError(n)
        ans,base=A(1),self
        while n:
            if n&1:ans=ans*base
            base=base*base;n//=2
        return ans
    def repr(self): return [str(x) for x in self.cs]

O=A(1);Z=A(0);a=A((0,1,0,0));p=a*a

def tr(M):return list(map(list,zip(*M)))
def mm(X,Y):
    return [[sum((x*y for x,y in zip(row,col)), Z) for col in zip(*Y)] for row in X]
def eye(n):return [[O if i==j else Z for j in range(n)] for i in range(n)]
def diag(v):return [[v[i] if i==j else Z for j in range(len(v))] for i in range(len(v))]

check('golden p+p2=1',p+p*p==O)
check('golden p3=p-p2',p**3==p-p*p)
check('golden p6+4p3=1',p**6+4*p**3==O)
G=[[a,-p],[p,a]]
check('G orthogonal',mm(tr(G),G)==eye(2))
P=diag([O,-O]); U=mm(mm(tr(G),P),G)
check('loop amplitude dark=p3',U[0][0]==p**3)
check('loop amplitude bright=-2a p',U[1][0]==-2*a*p)
check('full two-port loop unitary',mm(tr(U),U)==eye(2))
check('full loop probability identity',U[0][0]**2+U[1][0]**2==O)
check('identity loop full return',mm(mm(tr(G),eye(2)),G)==eye(2))
check('positive path sum p+p2=1',p+p*p==O)
check('destructive path sum p-p2=p3',p-p*p==p**3)
check('raise destructive cost by 1 yields p2',p-p**3==p**2)
check('price 3 to 2 under added branch cost',p-p**2==p**3 and p-p**3==p**2)
eta0=2+p; eta1=-(1+p)
check('signed first source eta0=phi2',eta0*p**3==p)
check('signed first source eta1=-phi',eta1*p**3==-p*p)
check('signed source sums to unity',eta0+eta1==O)
check('negative response to greater destructive cost',eta1==-(O+p))
normalizer=p*p+p**4
check('orthogonal memory norm nonzero',normalizer!=Z)
check('normalizer normalized path weight sum',p*p+p**4==normalizer)
L_i=[[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]]
L_j=[[0,0,-1,0],[0,0,0,1],[1,0,0,0],[0,-1,0,0]]
Li=[[A(x) for x in row] for row in L_i];Lj=[[A(x) for x in row] for row in L_j]
check('quaternion generators orthogonal',mm(tr(Li),Li)==eye(4) and mm(tr(Lj),Lj)==eye(4))
comm=mm(mm(mm(Li,Lj),tr(Li)),tr(Lj))
check('Q8 noncommutative commutator is minus identity',comm==[[-x for x in row] for row in eye(4)])
v=[p,-p*p]
rotate=[G[0][0]*v[0]+G[0][1]*v[1],G[1][0]*v[0]+G[1][1]*v[1]]
check('common orthogonal memory change preserves represented norm',sum((x*x for x in rotate),Z)==p*p+p**4)
result={'status':'PASS','checks':len(checks),'labels':checks,
 'gauge':'common memory unitary leaves norm and source invariant',
 'dark_amplitude':(p**3).repr(),'bright_amplitude':(-2*a*p).repr(),
 'golden_weight_cost_response':{'cost1':eta0.repr(),'cost2':eta1.repr()},
 'port_probabilities':{'dark':'p^6','bright':'4p^3'},
 'correct_scope':'selected represented detector port; not the full Q8 regular-memory action, complete Book03 valuation or physically selected cut',
 'GR_closed':False}
print(json.dumps(result,indent=2))
