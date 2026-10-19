#!/usr/bin/env python3
"""Exact cubic continuum Ricci completion, with finite Poisson stencil.

For H=a A.x, J=b B.x and A.B=0, the full Lorentzian Ricci tensor
has only two cubic components. A source-forced, transverse-rotationally
covariant pair of cubic profile corrections eliminates every Ricci
component through total (a,b)-degree 3. The original five-point
finite Laplacian reproduces the same cubic source EXACTLY at every h.

This is NOT an original finite six-plaquette all40 Cartan root;
the finite cubic link equations and native complete price remain open.
"""
import sympy as s
a,b,x,y,h=s.symbols("a b x y h",real=True,nonzero=False)
R=s.Rational

def cut(expr):
    poly=s.Poly(s.expand(expr),a,b)
    return s.expand(sum(c*a**i*b**j for (i,j),c in poly.terms()
                        if i+j<=3))

def ricci_cubic(A,B,repair=False):
    HA=A[0]*x+A[1]*y
    JB=B[0]*x+B[1]*y
    modA=A[0]**2+A[1]**2
    modB=B[0]**2+B[1]**2
    H=a*HA
    J=b*JB
    if repair:
        # The coefficients below follow from the uncorrected Einstein
        # null-source and Δ[(B.x)(x²+y²)]=8(B.x), not from a fitted action.
        H-=a*a*b*R(1,32)*modA*JB*(x*x+y*y)
        J-=a*b*b*R(1,32)*modB*HA*(x*x+y*y)
    mixed=cut(H*J)
    C=1+mixed/4
    invOm2=1+mixed/2  # (1−HJ/4)^(-2) through total degree 3
    g=s.Matrix([[H,C,0,0],[C,J,0,0],
                [0,0,-1,0],[0,0,0,-1]])
    gi=s.Matrix([[-cut(J*invOm2),cut(C*invOm2),0,0],
                 [cut(C*invOm2),-cut(H*invOm2),0,0],
                 [0,0,-1,0],[0,0,0,-1]])
    coords=(s.Symbol("u"),s.Symbol("v"),x,y)
    dg=[s.zeros(4),s.zeros(4),g.diff(x),g.diff(y)]
    gamma=[[[cut(R(1,2)*sum(
       gi[r,t]*(dg[i][t,j]+dg[j][t,i]-dg[t][i,j])
       for t in range(4))) for j in range(4)]
       for i in range(4)] for r in range(4)]
    Ric=s.zeros(4)
    for i in range(4):
        for j in range(4):
            val=0
            for r in range(4):
                if r>=2:
                    val+=s.diff(gamma[r][j][i],coords[r])
                if j>=2:
                    val-=s.diff(gamma[r][r][i],coords[j])
                for k in range(4):
                    val+=gamma[r][r][k]*gamma[k][j][i]
                    val-=gamma[r][j][k]*gamma[k][r][i]
            Ric[i,j]=cut(val)
    return Ric

def discrete_lap(F):
    return s.expand((F.subs(x,x+h)+F.subs(x,x-h)+
                     F.subs(y,y+h)+F.subs(y,y-h)-4*F)/h**2)

def require(condition,label):
    if not condition:
        raise ArithmeticError(label)

if __name__=="__main__":
    tests=(((1,0),(0,1)),((0,1),(1,0)),
           ((1,1),(1,-1)),((1,2),(-2,1)))
    for A,B in tests:
        require(A[0]*B[0]+A[1]*B[1]==0,"orthogonal test only")
        normA=A[0]**2+A[1]**2
        normB=B[0]**2+B[1]**2
        HA=A[0]*x+A[1]*y
        JB=B[0]*x+B[1]*y
        target=s.zeros(4)
        target[0,0]=a*a*b*normA*JB/8
        target[1,1]=a*b*b*normB*HA/8
        require(ricci_cubic(A,B)==target,
                "complete uncorrected cubic Ricci tensor")
        require(ricci_cubic(A,B,repair=True)==s.zeros(4),
                "entire Lorentz Ricci through degree 3")
        radius=x*x+y*y
        require(discrete_lap(JB*radius)==8*JB,
                "finite Laplacian must exactly recover first source")
        require(discrete_lap(HA*radius)==8*HA,
                "finite Laplacian must exactly recover second source")
        print("PASS full Ricci cubic cancellation / native five-point Poisson",A,B)
    print("SCOPE: continuum Einstein degree<=3 + finite scalar Poisson only;")
    print("finite third-order 24 Cartan/16 solder and full native Cost-Info are OPEN.")
