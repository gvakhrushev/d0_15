#!/usr/bin/env python3
"""Exact symbolic original four-CAR/Julia/Walsh N0 spectrum and source gate.

ALL computations are 16x16 over Q[i,r,nu,(1-r^2)^-1]. Uses literal native
creator ordering (0,2,3,1), original phases (i,i,-1,-i), frozen boost
U_{1/9}=I+G^2/40+9G/40 and nu=3/5 only at the final diagnostic.
No synthetic Kraus/channel, continuum metric, source fit, physical GR
closure or numerical eigenvalue/rank thresholds.
"""
import sympy as s


def check(expr, name):
    if expr is not True and expr != s.true:
        raise AssertionError(name)


def equal(a, b, name):
    check(s.cancel(a-b)==0,name)


def equal_matrix(a, b, name):
    if a.shape!=b.shape or any(s.cancel(z)!=0 for z in a-b):
        raise AssertionError(name)


def main():
    d=16
    I=s.I
    r, nu=s.symbols("r nu",real=True,nonzero=True)
    creators=[]
    order=(0,2,3,1)
    for mode in range(4):
        C=s.zeros(d)
        predecessors=order[:order.index(mode)]
        for bits in range(d):
            if not (bits>>mode)&1:
                sign=(-1)**sum((bits>>j)&1 for j in predecessors)
                C[bits | (1<<mode),bits]=sign
        creators.append(C)
    for i in range(4):
        for j in range(4):
            equal_matrix(
                creators[i]*creators[j]+creators[j]*creators[i],
                s.zeros(d),f"CAR cc {i},{j}")
            equal_matrix(
                creators[i]*creators[j].T+creators[j].T*creators[i],
                s.eye(d) if i==j else s.zeros(d),
                f"CAR cd {i},{j}")
    G=creators[0]*creators[1].T+creators[1]*creators[0].T
    equal_matrix(G**3,G,"native boost G^3=G")
    U=s.eye(d)+2*r/(1-r*r)*G+2*r*r/(1-r*r)*G*G
    a=s.zeros(d)
    for j,c in enumerate(creators):
        b=nu*c
        x=[I*b,I*b*U,-b,-I*b][j]
        # Literal original 32 first Julia Walsh endpoints:
        # x,x^dagger,-b,-b^dagger, each repeated TWICE.
        a+=x+x.H-b-b.H
    a=a/16
    equal_matrix(a.H,a,"actual original N0 is Hermitian")
    A=a.H*a
    P=5*r**4+r**3-8*r**2-r+5
    Q=23*r**4+6*r**3-32*r**2-10*r+25
    total=nu**2*P/(64*(1-r*r)**2)
    product=nu**4*Q/(16384*(1-r*r)**2)
    equal_matrix(A*A-total*A+product*s.eye(d),s.zeros(d),
                 "ALL symbolic 16x16 original A quadratic identity")
    equal(s.trace(A),8*total,"multiplicity-eight trace")
    Z=8*total/product
    equal(Z,2048*P/(nu**2*Q),"trace-inverse simple rational")
    rho=s.eye(d)/8-A/s.trace(A)
    # Since A*rho=I/Z and Tr rho=1, this IS A^-1/Tr A^-1.
    equal_matrix(A*rho,s.eye(d)/Z,"direct normalized inverse")
    equal(s.trace(rho),1,"canonical rho trace")
    equal_matrix(rho* A,A*rho,"canonical state commutes with A")

    values={r:s.Rational(1,9),nu:s.Rational(3,5)}
    A0=A.subs(values)
    check(bool(A0==A0.H),"physical finite A Hermitian")
    expected_eigen = [
        (s.Rational(141489,10240000)-9*s.sqrt(397841)/10240000),
        (s.Rational(141489,10240000)+9*s.sqrt(397841)/10240000)]
    actual=A0.eigenvals()
    check(len(actual)==2 and all(actual.get(v,0)==8 for v in expected_eigen),
          "original exact 8+8 eigenvalues")
    equal(s.trace(A0),s.Rational(141489,640000),
          "original fixture trace")
    equal(Z.subs(values),s.Rational(80491520,69399),
          "original fixture trace inverse")
    p=(s.sqrt(5)-1)/2
    equal(p*p+p,1,"single Golden identity")
    qa=p**3*nu**2*Q/(32*P)
    equal(qa.subs(values),s.Rational(69399,1257680)*p**3,
          "original 128-Kraus mean port1 probability")
    ratio_der=s.diff(Q/P,r)/(Q/P)
    equal(ratio_der.subs(r,s.Rational(1,9)),
          -s.Rational(17814168,121224631),
          "original native relative first source")
    # The density has ZERO nu-derivative for the actual native chart.
    equal_matrix(rho.diff(nu),s.zeros(d),
                 "original endogenous preparation scale invariance")

    h,x,y,eps=s.symbols("h x y eps",real=True,nonzero=True)
    H=eps*(x*x+y*y)
    lap=(H.subs(x,x+h)+H.subs(x,x-h)
         +H.subs(y,y+h)+H.subs(y,y-h)-4*H)/(h*h)
    equal(lap,4*eps,"exact original 5-point Brinkmann transverse stencil")
    equal(-lap/(2*h),-2*eps/h,"configured normal coframe source")
    print("PASS_ORIGINAL_CAR16_TWO_EIGENVALUE_CLOSED_FORM")
    print(" symbolic CAR16 all-r,all-nu minimal polynomial: PASS")
    print(" actual fixture eigenvalue multiplicities: 8+8")
    print(" Z_A = 80491520/69399")
    print(" q_A = 69399*p^3/1257680")
    print(" rho_A = I16/8 - A/Tr(A); d_nu rho_A=0")
    print(" original configured Brinkmann normal geometric source != 0")
    print(" GR_closed=false; complete native-price/source selection still open")


if __name__=="__main__":
    main()
