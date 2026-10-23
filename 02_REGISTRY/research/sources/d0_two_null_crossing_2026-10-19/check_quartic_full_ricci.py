#!/usr/bin/env python3
"""Exact full 4x4 Ricci through total amplitude degree four.

Same double-null original sixteen-coframe chart. Two explicitly computed
O(a²b²) corrections, one null-leg scale and one transverse conformal
scale, cancel ALL sixteen Ricci components after the exact cubic H/J
source corrections. No original finite full40 Cartan cubic/quartic
stationarity, physical native Cost-Info selection, or GR closure claimed.

Standard SymPy only. Independent rational source check.
"""
import sympy as s

x,y,a,b,h=s.symbols("x y a b h",real=True)
r2=x*x+y*y
u,v=s.symbols("u v",real=True)
coords=(u,v,x,y)
rat=s.Rational

def cut(F):
    terms=s.Poly(s.expand(F),a,b).terms()
    return s.expand(sum(coef*a**powers[0]*b**powers[1]
                        for powers,coef in terms if sum(powers)<=4))

def coeff(F,i,j):
    return s.Poly(s.expand(F),a,b).coeff_monomial(a**i*b**j)

def lap(F):
    return s.diff(F,x,2)+s.diff(F,y,2)

def lap_h(F):
    return s.cancel((F.subs(x,x+h)+F.subs(x,x-h)
          +F.subs(y,y+h)+F.subs(y,y-h)-4*F)/h**2)

def same_matrix(left,right):
    return left.shape==right.shape and all(
        s.simplify(s.expand(left[i,j]-right[i,j]))==0
        for i in range(left.rows) for j in range(left.cols))

def zero_matrix(matrix):
    return same_matrix(matrix,s.zeros(*matrix.shape))

def full_ricci(A,B,stage):
    """Stage 0: linear H/J; 1: cubic H/J; 2: +area sigma4; 3: +chi4."""
    AA=A[0]*x+A[1]*y
    BB=B[0]*x+B[1]*y
    aa=A[0]**2+A[1]**2
    bb=B[0]**2+B[1]**2
    H=a*AA
    J=b*BB
    if stage>=1:
        H-=a*a*b*aa*BB*r2/32
        J-=a*b*b*bb*AA*r2/32
    scale=aa*bb*a*a*b*b*r2*r2
    sigma=-scale/128 if stage>=2 else s.Integer(0)
    chi=3*scale/1024 if stage>=3 else s.Integer(0)
    rho=cut(1+sigma-H*J/4)
    C=cut(1+sigma+H*J/4)
    metric=s.zeros(4)
    metric[0,0]=cut((1+sigma)*H)
    metric[1,1]=J
    metric[0,1]=metric[1,0]=C
    metric[2,2]=metric[3,3]=-1-2*chi
    drho=cut(rho-1)
    invrho2=cut(1-2*drho+3*drho**2)
    inv=s.zeros(4)
    inv[0,0]=cut(-J*invrho2)
    inv[0,1]=inv[1,0]=cut(C*invrho2)
    inv[1,1]=cut(-(1+sigma)*H*invrho2)
    inv[2,2]=inv[3,3]=-1+2*chi
    dg=[s.zeros(4),s.zeros(4),metric.diff(x),metric.diff(y)]
    G=[[[cut(rat(1,2)*sum(
        inv[r,t]*(dg[i][t,j]+dg[j][t,i]-dg[t][i,j])
        for t in range(4)))
        for j in range(4)]for i in range(4)]for r in range(4)]
    Ric=s.zeros(4)
    for i in range(4):
        for j in range(4):
            ans=0
            for r in range(4):
                if r>=2:
                    ans+=s.diff(G[r][j][i],coords[r])
                if j>=2:
                    ans-=s.diff(G[r][r][i],coords[j])
                for k in range(4):
                    ans+=G[r][r][k]*G[k][j][i]-G[r][j][k]*G[k][r][i]
            Ric[i,j]=cut(ans)
    return Ric,rho

def check(A,B):
    assert A[0]*B[0]+A[1]*B[1]==0 and A!=(0,0) and B!=(0,0)
    aa=A[0]**2+A[1]**2
    bb=B[0]**2+B[1]**2
    q=aa*bb
    R1,_=full_ricci(A,B,1)
    R2,rho2=full_ricci(A,B,2)
    R3,rho3=full_ricci(A,B,3)
    # A cubic source-controlled H/J alone is NOT quartic vacuum.
    assert not zero_matrix(R1)
    # The orbit-area sigma4 removes ALL u,v orbit Ricci fourth-order.
    assert all(s.simplify(s.expand(R2[i,j]))==0
               for i in range(2) for j in range(2))
    expected=s.zeros(4)
    expected[2,2]=expected[3,3]=3*q*a*a*b*b*r2/64
    assert same_matrix(R2,expected),(A,B,R2)
    assert zero_matrix(R3),(A,B,R3)
    assert coeff(rho2,2,2)==0
    assert coeff(rho3,2,2)==0
    print("PASS quartic complete Einstein Ricci 16/16, A=",A,"B=",B)

if __name__=="__main__":
    for A,B in (((1,0),(0,1)),((0,1),(1,0)),
                ((1,1),(-1,1)),((1,2),(-2,1)),
                ((2,0),(0,3))):
        check(A,B)
    r,q,k=s.symbols("r q k",real=True)
    check((r,q),(-k*q,k*r))
    print("PASS symbolic arbitrary orthogonal family A=(r,q), B=k*(-q,r)")
    assert s.expand(lap_h(r2*r2)-16*r2-4*h*h)==0
    assert s.expand(lap_h(r2*r2-h*h*r2)-16*r2)==0
    assert s.expand(lap_h(lap_h(r2*r2))-64)==0
    print("PASS exact five-point stencil quartic source: Δ_h(r⁴−h²r²)=16r²")
    print("SCOPE: exact continuum Ricci degree<=4; finite all40 link/coframe")
    print("cubics/quartics, full retained native price and GR_closed remain OPEN.")
