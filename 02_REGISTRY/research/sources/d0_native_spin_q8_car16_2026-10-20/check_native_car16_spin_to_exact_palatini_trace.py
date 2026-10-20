#!/usr/bin/env python3
"""Exact D0 four-Jordan-Wigner CAR16 to nonlinear Spin/SO/Palatini traces.
Six faces are built from FOUR shared Spin links; all numbers rational.
Conditional algebraic intertwiner, not compulsory G0/Book action.
"""
from itertools import permutations, combinations, product
from sympy import Matrix, zeros, eye, Rational, trace, LeviCivita

n=16; I=eye(n); Z=zeros(n)
c=[]
for j in range(4):
    m=zeros(n)
    for state in range(n):
        if not state & (1<<j):
            m[state|(1<<j),state]=(-1)**((state&((1<<j)-1)).bit_count())
    c.append(m)
g=[c[0]+c[0].T]+[c[j]-c[j].T for j in (1,2,3)]
eta=Matrix.diag(1,-1,-1,-1)
for a,b in product(range(4),repeat=2):
    assert g[a]*g[b]+g[b]*g[a]==(2*eta[a,b]*I if a==b else Z)
    assert trace(g[a]*g[b])/16==eta[a,b]
omega=g[0]*g[1]*g[2]*g[3]
assert omega*omega==-I
def eps(a,b,c,d):
    return -trace(omega*g[a]*g[b]*g[c]*g[d])/16
for a,b,c0,d in product(range(4),repeat=4):
    assert eps(a,b,c0,d)==LeviCivita(a,b,c0,d)

def boost(a,b):
    B=g[a]*g[b];assert B*B==I
    return Rational(5,4)*I+Rational(3,4)*B,Rational(5,4)*I-Rational(3,4)*B
def rotation(a,b):
    B=g[a]*g[b];assert B*B==-I
    return Rational(3,5)*I+Rational(4,5)*B,Rational(3,5)*I-Rational(4,5)*B
def vector(s,si):
    assert s*si==I and si*s==I
    P=Matrix(4,4,lambda a,b:eta[b,b]*trace(g[b]*s*g[a]*si)/16)
    for a in range(4):
        assert s*g[a]*si==sum((P[a,b]*g[b] for b in range(4)),Z)
    assert P*eta*P.T==eta and P.det()==1
    return P
def star_up(F):
    return Matrix(4,4,lambda a,b:sum((
        eps(a,b,c,d)*eta[c,c]*eta[d,d]*F[c,d]
        for c,d in product(range(4),repeat=2)),0)/2)
Sb,Sbi=boost(0,1);Sr,Sri=rotation(1,2)
S=Sb*Sr;Si=Sri*Sbi
P=vector(S,Si);Pb=vector(Sb,Sbi);Pr=vector(Sr,Sri)
assert Sb*Sr!=Sr*Sb and (P==Pr*Pb or P==Pb*Pr)
assert vector(-S,-Si)==P
F=(P-P.inv())/2
assert F.T*eta+eta*F==zeros(4)
assert star_up(star_up(F*eta))==-F*eta
L=[];Lin=[]
for pair,op in [((0,1),boost),((1,2),rotation),
                ((0,2),boost),((2,3),rotation)]:
    a,b=op(*pair);L.append(a);Lin.append(b)
coframe=Matrix([[1,2,0,1],[0,1,1,0],[2,0,1,1],[1,0,0,2]])
assert coframe.det()!=0
faces=[]
for r,s in combinations(range(4),2):
    spin=L[r]*L[s]*Lin[r]*Lin[s]
    spin_inv=L[s]*L[r]*Lin[s]*Lin[r]
    p=vector(spin,spin_inv)
    f=(p-p.inv())/2
    assert f.T*eta+eta*f==zeros(4)
    assert star_up(star_up(f*eta))==-f*eta
    faces.append((r,s,f))
assert len(faces)==6
levi_total=0;trace_total=0
for r,s,f in faces:
    fu=f*eta
    for a,b,c,d in product(range(4),repeat=4):
        term=coframe[r,a]*coframe[s,b]*eta[a,a]*eta[b,b]*eta[c,c]*eta[d,d]*fu[c,d]
        levi_total+=term*LeviCivita(a,b,c,d)
        trace_total+=term*eps(a,b,c,d)
assert levi_total==trace_total==Rational(3325188579,200000000)
# Genuine finite Spin-vs-SO half-angle/central nonlinearity.
assert (Sb-Sbi)/2==Rational(3,4)*(g[0]*g[1])
assert abs(((Pb-Pb.inv())/2)[0,1])==Rational(15,8)
assert Rational(15,8)/Rational(3,4)==Rational(5,2)
assert (Sr-Sri)/2==Rational(4,5)*(g[1]*g[2])
assert abs(((Pr-Pr.inv())/2)[1,2])==Rational(24,25)
assert Rational(24,25)/Rational(4,5)==Rational(6,5)
q8=g[1]*g[2];p180=vector(q8,-q8)
assert p180!=eye(4) and p180*p180==eye(4)
assert (p180-p180.inv())/2==zeros(4)
assert (q8-(-q8))/2==q8
assert vector(-q8,q8)==p180
print("PASS original CAR16 recovers eta and ALL256 epsilon by exact trace")
print("PASS nonlinear rational noncommuting Spin boost/rotation SO lift")
print("PASS six faces from FOUR shared links, nonflat coframe Palatini 40 source kernel")
print("PASS exact shared-link epsilon-trace contraction",trace_total)
print("PASS intrinsic Lorentzian Hodge *^2=-1 on actual finite face curvature")
print("PASS exact half-angle boost 5/2, rotation 6/5")
print("PASS Q8 180-degree SO odd=0 but Spin odd!=0; Q8 center faithful")
print("FIREWALL: compulsory paid G0/Book H+J+R, matter stress, refinement OPEN")
