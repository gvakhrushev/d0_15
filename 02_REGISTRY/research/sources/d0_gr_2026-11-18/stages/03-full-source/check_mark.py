"""Literal Golden two-tick dilation, all binary histories, and one harmonic report."""
from fractions import Fraction
from itertools import product
from functools import reduce
from math import gcd
from pathlib import Path
import json
import mpmath as mp
import sympy as sp
from sympy.polys.matrices import DomainMatrix

p=(sp.sqrt(5)-1)/2
a=sp.sqrt(p)
field=sp.QQ.algebraic_field(a)
G=sp.Matrix([[a,-p],[p,a]])
cx=sp.Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
cut=sp.eye(8)[:,[0,2]]
def matrix(mat):
    return DomainMatrix.from_Matrix(mat).convert_to(field).to_sparse()
def scalar(num):
    return field.from_sympy(sp.sympify(num))
j=matrix(cut)
P=j*j.transpose()
I=matrix(sp.eye(8))
Q=I-P
i2=matrix(sp.eye(2))
z=Fraction(1,2**20)
N=6
D=4*(2**(20*(N-1)))*reduce(lambda x,y:x*y//gcd(x,y),range(1,N+1),1)
width=(D-1).bit_length()
ready=Fraction(D,2**width)
omega={n:z**(n-1)/(4*n) for n in range(1,N+1)}
tickets={n:int(D*v) for n,v in omega.items()}
assert all(Fraction(k,D)==omega[n] for n,k in tickets.items())
assert sum(tickets.values())<=D and Fraction(1,2)<ready<=1
cases=[]
for G_e,G_b in [(G,G),(G**3,G),(G,G**3)]:
    U=matrix(sp.kronecker_product((cx*sp.kronecker_product(G_e,sp.eye(2)))**2,G_b**2))
    T=U.transpose()
    assert U*T==I
    F=j.transpose()*T*Q*U*j
    assert not F[0,1].element==field.zero
    # Entire projective instruments on the literal 8D forward/reverse cut.
    paths={():j}
    expected=matrix(sp.zeros(2))
    for n in range(1,N+1):
        op=U if n%2 else T
        yes=Q if n%2 else P
        paths={hist+(mark,):proj*op*k for hist,k in paths.items()
               for mark,proj in [(0,I-yes),(1,yes)]}
        full=sum((k.transpose()*k for k in paths.values()),matrix(sp.zeros(2)))
        assert full==i2
        branch=paths[(1,)*n]
        assert branch.transpose()*branch==F**n
        expected+=(F**n)*scalar(omega[n]*ready)
    detected=matrix(sp.zeros(2))
    for hist,k in paths.items():
        eligible=sum(tickets[n] for n in range(1,N+1) if all(hist[:n]))
        detected+=(k.transpose()*k)*scalar(Fraction(eligible,2**width))
    assert expected==detected
    final=detected.to_Matrix()
    cases.append({"histories":len(paths),"P_on_uniform_input":float(final.trace()/2)})

mp.mp.dps=75
zz=mp.mpf(2)**(-20)
angle=mp.asin((mp.sqrt(5)-1)/2)
def price(e,b,depth=None):
    u=mp.sin(2*b)**2
    v=1-(1-u)*(1-mp.sin(2*e)**2)
    if depth is not None:
        return sum(zz**n*(u**n+v**n)/n for n in range(1,depth+1))
    return -mp.log(1-zz*u)-mp.log(1-zz*v)
derivative_errors=[]
for axis in [0,1]:
    def slope(n):
        return mp.diff(lambda t:price(t,angle,n) if axis==0 else price(angle,t,n),angle)
    error=abs(slope(N)-slope(None))
    assert error<8*zz**(N+1)/(1-zz)
    derivative_errors.append(mp.nstr(error,10))

# Exact ordered-root determinant formula on a nondiagonal three-channel corner.
A=sp.Matrix([[1,2,0],[-1,1,1],[0,1,-2]])/4
F=A.T*A
Z=sp.Rational(1,2**20)
M=sp.eye(3)-Z*F
pivots=[]
for i in range(3):
    tail=M[i+1:,i+1:]
    if i==2:
        pivot=M[i,i]
    else:
        c=F[i+1:,i]
        pivot=1-Z*F[i,i]-Z**2*(c.T*tail.inv()*c)[0]
    assert pivot==1/(M[i:,i:].inv()[0,0])
    pivots.append(pivot)
assert sp.prod(pivots)==M.det()
print(json.dumps({"status":"PASS","query":"full 8D U, rank-2 true cut",
    "binary_history_depth":N,"settings":cases,"fair_ticket_width":width,
    "sampling_factor":str(ready),"two_true_derivative_errors":derivative_errors,
    "ordered_root_pivots":"exact, 3 non-diagonal modes",
    "scope":"Observable realization on the admitted query/flags. Physical valuation and GR remain open."},indent=2))
