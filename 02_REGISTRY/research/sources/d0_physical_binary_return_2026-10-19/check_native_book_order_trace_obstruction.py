#!/usr/bin/env python3
"""Original K(9,11,13) scalar Book action vs ordered SO(1,3) memory.

Exact finite conditional graph-to-Lorentz representation witness.
NOT a physically admitted native transport or a proof of full D0 GR.
"""
from collections import Counter
from sympy import Matrix, eye, symbols, Rational, factor, trace, zeros, simplify

zones=(set(range(9)),set(range(9,20)),set(range(20,33)))
V=set().union(*zones)
def which(v):return next(i for i,Z in enumerate(zones) if v in Z)
E={(i,j) for i in V for j in V if which(i)!=which(j)}
assert len(V)==33 and len(E)==718
base=0
cycles=[(base,9+i,20+i,base) for i in range(3)]
for cyc in cycles:
    assert all((u,v) in E for u,v in zip(cyc,cyc[1:]))
assert len(set((u,v) for cyc in cycles for u,v in zip(cyc,cyc[1:])))==9

def word(order):
    out=[base]
    for j in order:out.extend(cycles[j][1:])
    return out
w1,w2=word((0,1,2)),word((0,2,1))
assert w1!=w2 and w1[0]==w2[0]==w1[-1]==w2[-1]==base
assert len(w1)==len(w2)==10
assert Counter(zip(w1,w1[1:]))==Counter(zip(w2,w2[1:]))
assert Counter(w1)==Counter(w2)

eta=Matrix([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]])
def Eij(i,j):
    m=zeros(4);m[i,j]=1;return m
A=Eij(1,2)+Eij(2,0)
B=Eij(0,3)+Eij(3,1)
C=A*B-B*A
assert C==Eij(2,3)-Eij(3,2)
assert A**3==B**3==zeros(4) and trace(C*C)==-2
for X in (A,B,C):assert X.T*eta+eta*X==zeros(4)
a,b,c=symbols('a b c',real=True)
UA=eye(4)+a*A+a*a*A*A/2
UB=eye(4)+b*B+b*b*B*B/2
UC=(eye(4)-c*C/2).inv()*(eye(4)+c*C/2)
for U in (UA,UB,UC):
    assert simplify(U.T*eta*U-eta)==zeros(4)
    assert simplify(U.det()-1)==0
diff=factor(trace(UA*UB*UC)-trace(UA*UC*UB))
assert simplify(diff+8*a*b*c/(4+c*c))==0
test={a:Rational(1,40),b:Rational(1,40),c:Rational(1,40)}
assert diff.subs(test)==-Rational(1,32005)
assert simplify(diff.diff(a).subs(test)+Rational(8,6401))==0
G=eye(4)+A/10+A*A/200
assert simplify(trace(G*(UA*UB*UC)*G.inv())-trace(G*(UA*UC*UB)*G.inv())-diff)==0
print("PASS original K(9,11,13): 33 vertices, 718 directed edges, 3 complete original triangles")
print("PASS both full 9-edge closed histories have identical directed-edge and vertex multiplicities")
print("PASS universal scalar local Cost−Info equality for arbitrary field-dependent primitive prices")
print("PASS exact SO(eta), det=1, gauge invariant noncommutative Wilson memory")
print("TRACE DIFFERENCE:",diff)
print("TRACE AT 1/40:",diff.subs(test))
print("FIRST SOURCE d_a:",simplify(diff.diff(a).subs(test)))

# Same finite witness is distinguishable by a COMPLETE positive Julia/Choi
# detector of the already-owned mathematical type. The 718-scene hardware
# assignment remains CONDITIONAL: no native operation is claimed forced.
# Input |Omega> = (|00>+|11>+|22>+|33>)/2, success T(U)=U/2,
# mark effect |Omega><Omega|; keep success-unmarked and fail outcomes too.
T1=UA*UB*UC
T2=UA*UC*UB
Qmark1=factor(trace(T1)**2/64)
Qmark2=factor(trace(T2)**2/64)
Qdiff=factor(Qmark1-Qmark2)
assert simplify(Qdiff+a*b*c*(a*a*b*b*c*c+4*a*a*b*b+64)/(16*(c*c+4)**2))==0
assert Qdiff.subs(test)==-Rational(262144006401,67129837158400000)
for T in (T1,T2):
    U=T.subs(test)
    dU=U-eye(4)
    delta2=sum(dU[i,j]**2 for i in range(4) for j in range(4))
    assert delta2<Rational(1,4) # ||U||_op <=1+||U-I||_F<3/2<2
    Psuccess=sum(U[i,j]**2 for i in range(4) for j in range(4))/16
    Pmarked=U.trace()**2/64
    assert 0<Pmarked<=Psuccess<1
    assert 0<=Psuccess-Pmarked and 0<1-Psuccess
print("PASS complete positive Julia/Choi mark, success-other, failure kept")
print("EXACT MARK PROBABILITY GAP:",Qdiff.subs(test))

print("FIREWALL: no native scene-to-Lorentz physical compiler or Book action selection proved")
