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
a,b,x,y,h=s.symbols("a b x y h",real=True)
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

def same_matrix(actual,expected):
    return actual.shape==expected.shape and all(
        s.simplify(actual[i,j]-expected[i,j])==0
        for i in range(actual.rows) for j in range(actual.cols))

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
        require(same_matrix(ricci_cubic(A,B),target),
                "complete uncorrected cubic Ricci tensor")
        require(same_matrix(ricci_cubic(A,B,repair=True),s.zeros(4)),
                "entire Lorentz Ricci through degree 3")
        radius=x*x+y*y
        require(discrete_lap(JB*radius)==8*JB,
                "finite Laplacian must exactly recover first source")
        require(discrete_lap(HA*radius)==8*HA,
                "finite Laplacian must exactly recover second source")
        print("PASS full Ricci cubic cancellation / native five-point Poisson",A,B)
    r,q,scale=s.symbols("r q scale",real=True)
    A=(r,q)
    B=(-scale*q,scale*r)
    HA=A[0]*x+A[1]*y
    JB=B[0]*x+B[1]*y
    normA=A[0]**2+A[1]**2
    normB=B[0]**2+B[1]**2
    target=s.zeros(4)
    target[0,0]=a*a*b*normA*JB/8
    target[1,1]=a*b*b*normB*HA/8
    require(s.simplify(A[0]*B[0]+A[1]*B[1])==0,
            "symbolic gradients must be orthogonal")
    require(same_matrix(ricci_cubic(A,B),target),
            "arbitrary orthogonal cubic source")
    require(same_matrix(ricci_cubic(A,B,repair=True),s.zeros(4)),
            "arbitrary orthogonal Ricci cancellation through degree 3")
    radius=x*x+y*y
    require(s.expand(discrete_lap(JB*radius)-8*JB)==0,
            "symbolic finite Laplacian must exactly recover first source")
    require(s.expand(discrete_lap(HA*radius)-8*HA)==0,
            "symbolic finite Laplacian must exactly recover second source")
    print("PASS symbolic arbitrary orthogonal gradients A=(r,q), B=scale*(-q,r)")
    print("SCOPE: this checker proves continuum Einstein degree<=3 and scalar Poisson;")
    print("the local finite all40 cubic jet is checked separately by check_cubic_finite_cartan_range.py.")
    print("Neither checker proves periodic all-order dynamics or native Cost-Info selection.")


    # 2-Killing vacuum's EXACT orbit-current trace requires Δ rho = 0,
    # with rho=sqrt(-det lambda)=det(e_orb)>0. After the uniquely sourced
    # cubic H/J particular solutions in the *minimal* double-null ansatz,
    # rho4 is inevitably bi-Laplacian-nonharmonic. Arbitrary cubic
    # harmonic additions do not change its nonzero bi-Laplacian.
    for AV,BV in tests:
        normA=AV[0]**2+AV[1]**2
        normB=BV[0]**2+BV[1]**2
        HA=AV[0]*x+AV[1]*y
        JB=BV[0]*x+BV[1]*y
        rad=x*x+y*y
        rho4=(normA*JB*JB+normB*HA*HA)*rad/128
        expected=normA*normB*rad**2/128
        require(s.expand(rho4-expected)==0,
                "orthogonal covariant quartic area coefficient")
        require(s.expand(discrete_lap(discrete_lap(expected))
                         -normA*normB/2)==0,
                "nonzero quartic area biharmonic obstruction")
        sigma4=-expected
        require(s.expand(discrete_lap(expected+sigma4))==0,
                "one algebraic area scalar restores harmonicity")
        print("PASS fourth-order area trace obstruction and sigma source",AV,BV)

    ra,qa,sa=s.symbols("ra qa sa",real=True)
    AV=(ra,qa)
    BV=(-sa*qa,sa*ra)
    normA=AV[0]**2+AV[1]**2
    normB=BV[0]**2+BV[1]**2
    HA=AV[0]*x+AV[1]*y
    JB=BV[0]*x+BV[1]*y
    rad=x*x+y*y
    Hprofile=a*HA-a*a*b*normA*JB*rad/32
    Jprofile=b*JB-a*b*b*normB*HA*rad/32
    orbit=s.Matrix([[Hprofile,1+Hprofile*Jprofile/4],
                    [1+Hprofile*Jprofile/4,Jprofile]])
    require(s.expand(orbit.det()+(1-Hprofile*Jprofile/4)**2)==0,
            "exact positive-branch Killing-area determinant")
    rho=s.expand(1-Hprofile*Jprofile/4)
    rho_poly=s.Poly(rho,a,b)
    rho2=rho_poly.coeff_monomial(a*b)
    rho4_from_metric=rho_poly.coeff_monomial(a*a*b*b)
    rho4=(normA*JB*JB+normB*HA*HA)*rad/128
    expected=normA*normB*rad**2/128
    require(s.simplify(AV[0]*BV[0]+AV[1]*BV[1])==0,
            "symbolic crossed gradients must be orthogonal")
    require(s.expand(rho4-expected)==0,
            "arbitrary orthogonal quartic area coefficient")
    lap=lambda t:s.diff(t,x,2)+s.diff(t,y,2)
    require(s.expand(rho4_from_metric-expected)==0,
            "fourth-order orbit area from the exact metric determinant")
    require(s.expand(lap(rho2))==0,
            "quadratic orbit area is harmonic for perpendicular gradients")
    require(s.expand(lap(lap(expected))-normA*normB/2)==0,
            "arbitrary orthogonal continuum area biharmonic")
    require(s.expand(discrete_lap(discrete_lap(expected))
                     -normA*normB/2)==0,
            "arbitrary orthogonal quartic area biharmonic")
    amp4=a*a*b*b
    scaled=1-amp4*expected/2
    area=1+a*b*rho2+amp4*expected
    scale_residual=s.Poly(s.expand(scaled**2*area-(1+a*b*rho2)),a,b)
    require(all(i+j>4 for (i,j),_ in scale_residual.terms()),
            "orbit-coframe scale cancels the area coefficient through degree 4")
    print("PASS symbolic arbitrary orthogonal fourth-order area and coframe-scale cancellation")

    F=s.Function("F")(x,y)
    C=s.Function("C")(x,y)
    ux,uy=s.symbols("ux uy",real=True)
    for L in (F,C):
        linear=ux*x+uy*y
        ident=lap(lap(linear*L))-linear*lap(lap(L))-4*(
            ux*s.diff(lap(L),x)+uy*s.diff(lap(L),y))
        require(s.simplify(ident)==0,
                "arbitrary smooth harmonic cubic freedom cannot repair biharmonic volume")
    print("PASS general harmonic freedoms cannot remove the quartic area bi-Laplacian")
    print("SCOPE: forced fourth-order AREA trace only, not the full fourth-order Einstein system.")
