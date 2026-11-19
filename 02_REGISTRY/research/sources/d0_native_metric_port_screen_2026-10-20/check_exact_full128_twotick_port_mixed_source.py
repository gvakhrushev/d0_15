#!/usr/bin/env python3
"""Exact actual two-tick full128 Golden PORT-COST mixed-source test.

Original L4 k=(i,i,-1,-i), Jones+ fixed state, original Walsh/Julia roots
and all fresh GOOD/BAD/label channels. Direction: Q*=ell ell.T,
ell=(0,1,-1,1), and link Role-0 boost K_2=E02+E20.

Proves D_Q* D_K2 C_port^(2)=0 EXACTLY in Q(sqrt5,i),
even though d_K Eport != 0 and d_Q Phi(rho) != 0.
Independent companion: check_native_port_screen_local_star.py
proves old literal LOCAL G2/STAR mixed six-face symbol is -6.
NOT a proof of complete periodic Einstein Euler or full Book03 Cost-Info.
"""
import sympy as s

nu=s.Rational(3,5);b=s.Rational(4,5)
p=(s.sqrt(5)-1)/2;a=s.sqrt(p)
ph=[s.I,s.I,-1,-s.I]
eta=s.diag(1,-1,-1,-1)
ell=s.Matrix([0,1,-1,1])
H=eta*ell*ell.T
I=s.eye(16);Z=s.zeros(16);order=[0,2,3,1]
C=[]
for r in range(4):
    m=Z.copy();before=order[:order.index(r)]
    for bits in range(16):
        if not bits&(1<<r):
            m[bits+(1<<r),bits]=(-1)**sum(bool(bits&(1<<j)) for j in before)
    C.append(m)
left=[c*c.T for c in C];right=[c.T*c for c in C]
A=nu*sum((((z-1)*C[r]+(s.conjugate(z)-1)*C[r].T)/16
          for r,z in enumerate(ph)),Z.copy())
A_H=nu*sum(((((z-1)*sum((H[r,j]*C[j] for j in range(4)),Z.copy()))
   +(s.conjugate(z)-1)*sum((H[r,j]*C[j].T for j in range(4)),Z.copy()))/16
   for r,z in enumerate(ph)),Z.copy())
assert A_H==Z and H[0,:]==s.zeros(1,4)

def E(i,j):
    M=s.zeros(4);M[i,j]=1;return M
X=E(0,2)+E(2,0)
Gamma=sum((X[i,j]*C[i]*C[j].T for i in range(4)
           for j in range(4)),Z.copy())
A_X=nu*(ph[0]*C[0]*Gamma
   +s.conjugate(ph[0])*Gamma.T*C[0].T)/16
A_HX=nu*(ph[0]*sum((H[0,j]*C[j]*Gamma for j in range(4)),Z.copy())
       +s.conjugate(ph[0])*sum((H[0,j]*Gamma.T*C[j].T
                              for j in range(4)),Z.copy()))/16
assert A_HX==Z
E_X=4*p**3*(A*A_X+A_X*A)
assert any(s.simplify(x)!=0 for x in E_X)

psi=s.zeros(16,1)
psi[0]=psi[14]=-a
psi[1]=psi[15]=p
rho=psi*psi.T/2
B=A*rho*A

def rootder(proj,d):
    blocks=(I-proj,proj); eig=(1,b); out=Z.copy()
    for j in range(2):
        for k in range(2):
            out-=blocks[j]*d*blocks[k]/(eig[j]+eig[k])
    return out

# Exact Walsh parseval: the full 64 actual SELECT subcolumns (two
# coefficients × 32 labels) reduce to 32 primitive words for each port,
# with *two* occurrences of every word and 1/32 Hadamard normalization.
# Because d_H A=0 the full first-density derivative is
# d_H Phi(rho)=(4p²/32)Σ_(words,coeff,twice)
#   [ (dw)† (A rho A) w + w† (A rho A) dw ].
Phi_H=Z.copy()
for r in range(4):
    z=ph[r];v=nu*C[r]
    dv=nu*sum((H[r,j]*C[j] for j in range(4)),Z.copy())
    P=z*v;dP=z*dv;Pd=P.H;dPd=dP.H
    L=I+(b-1)*left[r]; R=I+(b-1)*right[r]
    dL=rootder(left[r],dP*Pd+P*dPd)
    dR=rootder(right[r],dPd*P+Pd*dP)
    items=((P,dP),(L,dL),(Pd,dPd),(R,dR),
           (-v,-dv),(-L,-dL),(-v.T,-dv.T),(-R,-dR))
    for w,dw in items:
        Phi_H+=2*(dw.H*B*w+w.H*B*dw)
Phi_H*=4*p**2/32
assert s.simplify(s.trace(Phi_H))==0
assert any(s.simplify(x)!=0 for x in Phi_H)

# C_port^(2)=2+Tr(Eport rho)+Tr(Eport Phi(rho)),
# Eport=4p³ A², Eport(0) is scalar. Since A_H=A_HX=0,
# E_H=E_HX=0, and Tr d_HX Phi=0, every term in
# D_H D_X C_port^(2) vanishes except Tr(E_X Phi_H).
cross=s.simplify(s.trace(E_X*Phi_H))
assert cross==0, cross
print('PASS exact original two-tick full128 Golden port cost coframe×link mixed source = 0')
print('PASS d_H Phi(rho) and d_X Eport separately NONZERO; exact full-source cancellation')
print('COMPARE literal local star G2/STAR 6-face symbol = -6 (companion checker)')
print('GR_closed=false: complete Book03 Cost−Info, physical prep and periodic Euler open')
