#!/usr/bin/env python3
"""Original D0 finite L4 momentum: metric strong-screen vs native Golden port
and literal finite G2/STAR Palatini local mixed CELL symbol.
The companion script reconstructs actual original full128 Walsh likelihoods.
NOT the full periodic S_star Euler or compulsory physical Book03 action.
"""
import sympy as s
from itertools import combinations
eta=s.diag(1,-1,-1,-1)
p=(s.sqrt(5)-1)/2
nu=s.Rational(3,5)
ph=(s.I,s.I,-1,-s.I)
k=s.Matrix([z-1 for z in ph])
q=s.symbols('q0:10',real=True)
Q=s.zeros(4)
j=0
for r in range(4):
    for c in range(r,4):
        Q[r,c]=Q[c,r]=q[j]
        j+=1
A=s.Matrix([[s.diff(s.re((Q*k)[r]),v) for v in q] for r in range(4)] +
           [[s.diff(s.im((Q*k)[r]),v) for v in q] for r in range(4)])
assert A.rank()==7
N=s.Matrix([[1,-2,1],[-1,1,0],[0,1,-1],[0,-1,1],
            [1,0,0],[0,-1,0],[0,1,0],[0,0,1],[0,0,-1],[0,0,1]])
assert A*N==s.zeros(8,3)
def fromcol(col):
    result=s.zeros(4)
    slot=0
    for i in range(4):
        for j in range(i,4):
            result[i,j]=result[j,i]=col[slot]
            slot+=1
    return result
Qs=[fromcol(N[:,j]) for j in range(3)]
assert all(Qm*k==s.zeros(4,1) for Qm in Qs)
ell=s.Matrix([0,1,-1,1])
Qstar=sum(Qs,s.zeros(4))
assert Qstar==ell*ell.T
assert Qstar*eta*k==s.zeros(4,1)
t=s.symbols('t',real=True)
F=s.eye(4)+t*eta*Qstar
assert s.simplify(F.T*k-k)==s.zeros(4,1)
assert s.simplify(F.T*eta*F-(eta+(2*t-3*t*t)*Qstar))==s.zeros(4)
assert s.factor(F.det())==1-3*t
Cport=lambda Ft:2+(p**3*nu**2/s.Integer(32))*s.expand_complex(
    ((Ft.T*k).conjugate().T*(Ft.T*k))[0])
assert s.simplify(Cport(F)-Cport(s.eye(4)))==0
for Qi in Qs:
    Ft=s.eye(4)+t*eta*Qi
    assert s.simplify(s.diff(Cport(Ft),t).subs(t,0))==0
# Strong moment screen is 3D; the TOTAL scalar port-price first kernel
# is larger, so do not falsely call Q*k=0 the entire cost nullspace.
first_source=s.Matrix([s.diff(s.diff(Cport(s.eye(4)+t*eta*Q),t).subs(t,0),v) for v in q])
assert first_source.rank()==1
assert s.simplify((first_source.T*N))==s.zeros(1,3)

V=[Qi*eta*k for Qi in Qs]
G=s.Matrix(3,3,lambda i,j:s.simplify(s.re((V[i].conjugate().T*V[j])[0])))
assert G==s.Matrix([[16,-24,8],[-24,56,-32],[8,-32,24]])
assert G.rank()==2 and G*s.ones(3,1)==s.zeros(3,1)
assert s.simplify(s.trace(eta*Qstar)+3)==0

pairs=list(combinations(range(4),2))
idx={pair:i for i,pair in enumerate(pairs)}
G2=s.diag(*(eta[r,r]*eta[u,u] for r,u in pairs))
star=s.zeros(6)
star_map={(0,1):((2,3),-1),(0,2):((1,3),1),(0,3):((0,2),-1),
          (1,2):((0,3),1),(1,3):((0,2),-1),(2,3):((0,1),1)}
# Independent literal original STAR_MAP used in the accepted certificate.
star_map[(0,3)]=((1,2),-1)
star_map[(1,3)]=((0,2),-1)
for pair,(target,sign) in star_map.items():
    star[idx[target],idx[pair]]=sign
assert star*star==-s.eye(6)
def E(i,j):
    return s.eye(4)[:,i]*s.eye(4)[:,j].T
def bivector(u,v):
    return s.Matrix([u[i]*v[j]-u[j]*v[i] for i,j in pairs])
def curvature_vector(X):
    return s.Matrix([(X*eta)[i,j] for i,j in pairs])
def sign_of_face(face):
    order=list(face)+[r for r in range(4) if r not in face]
    return (-1)**sum(order[i]>order[j] for i in range(4) for j in range(i+1,4))
lor=[E(0,j)+E(j,0) for j in (1,2,3)] + [
    E(1,2)-E(2,1),E(1,3)-E(3,1),E(2,3)-E(3,2)]
M=[]
for Qi in Qs:
    h=eta*Qi
    row=[]
    for link in range(4):
        for X in lor:
            total=0
            for face in pairs:
                u,v=[r for r in range(4) if r not in face]
                dB=bivector(h[:,u],s.eye(4)[:,v])+bivector(s.eye(4)[:,u],h[:,v])
                dP=s.zeros(4)
                if link==face[0]:
                    dP+=(1-ph[face[1]])*X
                if link==face[1]:
                    dP+=(ph[face[0]]-1)*X
                total+=sign_of_face(face)*(dB.T*G2*star*curvature_vector(dP))[0]
            row.append(s.simplify(total))
    M.append(row)
M=s.Matrix(M)
assert M.rank()==3
assert (s.ones(1,3)*M)[1]==-6
# Trace-free two-dimensional chosen screen cross-source remains rank2.
TF=s.Matrix([[1,0],[0,1],[0,-2]])
assert (TF.T*M).rank()==2
print("PASS native finite L4 screen Q*k=0 rank7; strong metric directions 3")
print("PASS native Golden TWO-PORT cost flat through exact full finite Qstar(t)")
print("PASS original local finite G2/STAR Palatini mixed CELL 3x24 rank3")
print("PASS exact Qstar link0/boost2 mixed slot -6; trace-free plane rank2")
print("IMPORTANT: strong screen dim3 is NOT full 9D first-jet port-price kernel")
print("GR_closed=false: local cell symbol and native port only; full Book action OPEN")
