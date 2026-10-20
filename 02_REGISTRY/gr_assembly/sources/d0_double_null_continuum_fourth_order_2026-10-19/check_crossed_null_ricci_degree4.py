#!/usr/bin/env python3
"""Exact continuum crossed-null Ricci jet through total amplitude degree 4.

For arbitrary real orthogonal transverse slopes A=(p,q), B=kappa*(-q,p),
this checks the cubic H/J Poisson corrections, the null-block area scale,
and a transverse conformal coframe mode. It computes every Ricci matrix entry
in Q[p,q,kappa,x,y][a,b]/(total degree > 4), and checks the two-Killing area
radius is harmonic to the same order. This is continuum geometry only; it is
not the original finite six-plaquette 40-row Palatini system or native D0 price.
"""
import sympy as s

R=s.Rational
a,b,x,y=s.symbols('a b x y', real=True)
p,q,kappa=s.symbols('p q kappa', real=True)
k=s.symbols('k', real=True)

def cut4(expr):
    poly=s.Poly(s.expand(expr),a,b)
    return s.expand(sum(c*a**i*b**j for (i,j),c in poly.terms() if i+j<=4))

def ricci_and_area(phi_coefficient):
    HA=p*x+q*y
    JB=-kappa*q*x+kappa*p*y
    normA=p*p+q*q
    normB=kappa*kappa*normA
    radius2=x*x+y*y
    H=a*HA-a*a*b*normA*JB*radius2/32
    J=b*JB-a*b*b*normB*HA*radius2/32
    C=1+cut4(H*J)/4
    area_defect=a*a*b*b*normA*normB*radius2**2/128
    area_scale=1-area_defect
    phi=phi_coefficient*a*a*b*b*normA*normB*radius2**2
    g=s.Matrix([[area_scale*H,area_scale*C,0,0],
                [area_scale*C,area_scale*J,0,0],
                [0,0,-(1+2*phi),0],
                [0,0,0,-(1+2*phi)]])
    q0=cut4(H*J/4)
    inv_lorentz_den=cut4(1+2*q0+3*q0*q0)
    inv_area=1+area_defect
    gi=s.Matrix([[cut4(-J*inv_lorentz_den*inv_area),
                  cut4(C*inv_lorentz_den*inv_area),0,0],
                 [cut4(C*inv_lorentz_den*inv_area),
                  cut4(-H*inv_lorentz_den*inv_area),0,0],
                 [0,0,cut4(-1+2*phi),0],
                 [0,0,0,cut4(-1+2*phi)]])
    coords=(s.Symbol('u'),s.Symbol('v'),x,y)
    dg=[s.zeros(4),s.zeros(4),g.diff(x),g.diff(y)]
    gamma=[[[cut4(R(1,2)*sum(
        gi[r,t]*(dg[i][t,j]+dg[j][t,i]-dg[t][i,j])
        for t in range(4))) for j in range(4)]
        for i in range(4)] for r in range(4)]
    ric=s.zeros(4)
    for i in range(4):
        for j in range(4):
            value=0
            for r in range(4):
                if r>=2:
                    value+=s.diff(gamma[r][j][i],coords[r])
                if j>=2:
                    value-=s.diff(gamma[r][r][i],coords[j])
                for t in range(4):
                    value+=gamma[r][r][t]*gamma[t][j][i]
                    value-=gamma[r][j][t]*gamma[t][r][i]
            ric[i,j]=cut4(value)
    rho=cut4(area_scale*(1-cut4(H*J)/4))
    lap_rho=cut4(s.diff(rho,x,2)+s.diff(rho,y,2))
    return ric,rho,lap_rho

def same_matrix(actual,expected):
    return actual.shape==expected.shape and all(
        s.simplify(actual[i,j]-expected[i,j])==0
        for i in range(actual.rows) for j in range(actual.cols))

if __name__=='__main__':
    ric, rho, lap_rho=ricci_and_area(k)
    norm_product=(p*p+q*q)**2*kappa*kappa
    r2=x*x+y*y
    residual=-(1024*k-3)*a*a*b*b*norm_product*r2/64
    for i in range(4):
        for j in range(4):
            wanted=residual if (i,j) in ((2,2),(3,3)) else 0
            assert s.simplify(ric[i,j]-wanted)==0, (i,j,s.factor(ric[i,j]-wanted))
    print('PASS before transverse conformal correction: only R_xx=R_yy remain')
    print('  residual:',s.factor(residual))
    assert same_matrix(ric.subs(k,R(3,1024)),s.zeros(4))
    print('PASS k=3/1024 cancels all 16 Ricci matrix entries through degree 4')
    assert s.simplify(lap_rho)==0
    print('PASS the two-Killing area radius is harmonic through degree 4')
    print('  rho:',s.factor(rho))
    print('SCOPE: exact continuum jet only; finite 24+16 Palatini and native Cost-Info remain open.')
