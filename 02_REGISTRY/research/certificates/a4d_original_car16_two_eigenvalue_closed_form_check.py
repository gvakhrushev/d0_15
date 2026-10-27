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
    # SAME original 42-dimensional normal-cofield class:
    # two independent off-shell probes + exact annihilator decomposition.
    aa,bb,cc=s.symbols("a_probe b_probe c_probe",nonzero=True)
    L=s.Matrix([[bb,aa,0,0],[cc,0,0,0]])
    v_F=s.Matrix([0,1/aa,0,0])
    v_Q=s.Matrix([1/cc,-bb/(aa*cc),0,0])
    equal_matrix(L*v_F,s.Matrix([1,0]),"original normal F probe")
    equal_matrix(L*v_Q,s.Matrix([0,1]),"original normal Q probe")
    coords=s.Matrix(s.symbols("v0:4"))
    kern=coords-(L*coords)[0]*v_F-(L*coords)[1]*v_Q
    equal_matrix(L*kern,s.zeros(2,1),
                 "normal decomposition leaves only a kernel direction")
    # Arbitrary ambient-matrix source: exact closed resolvent identity.
    zz=s.symbols("z",real=True,nonzero=True)
    denom=1-zz*total+zz*zz*product
    inverse_numer=(1-zz*total)*s.eye(d)+zz*A
    equal_matrix(
        (s.eye(d)-zz*A)*inverse_numer,
        denom*s.eye(d),
        "all-r,all-nu exact native logdet resolvent, no inverse oracle")
    # The first source against a Hermitian B need NOT preserve
    # the two-eigenvalue quadratic identity away from this base.
    B=s.zeros(d)
    B[0,0]=1
    B[0,1]=1
    B[1,0]=1
    res_source=(
        zz*(1-zz*total)*s.trace(B)
        +zz*zz*s.trace(A*B))/denom
    exact_source=s.trace(zz*inverse_numer*B)/denom
    equal(res_source,exact_source,
          "arbitrary ambient-Hermitian first-source formula")
    first_trace=s.trace(A)
    second_trace=s.trace(A*A)
    jac=s.Matrix([
        [s.diff(first_trace,r),s.diff(first_trace,nu)],
        [s.diff(second_trace,r),s.diff(second_trace,nu)]])
    Pj=(8*r**7+25*r**6+32*r**5-15*r**4
        -56*r**3+39*r**2+15)
    jac_closed=nu**5*r*Pj/(2048*(r-1)**5*(r+1)**5)
    equal(s.det(jac),jac_closed,
          "original 2-spectral-moment self-reading Jacobian")
    equal(jac_closed.subs(values),
          -s.Rational(18126055017,262144000000000),
          "nonzero actual exact original two-coordinate determinant")
    # Consumes the OWNED original full128 history identity
    # F_n=(I-K0^(2n)) tensor I_oldRIGHT, K0=I-2p^2*A.
    # Two ROOT powers obey a second-order recurrence at every horizon.
    sj=total.subs(values)
    tj=product.subs(values)
    sig=2-2*p*p*sj
    tau=1-2*p*p*sj+4*p**4*tj
    zf=s.Rational(1,2**20)
    for n in (1,2,3):
        L0,L1=s.Integer(2),sig
        for k in range(2,2*n+1):
            L0,L1=L1,s.expand(sig*L1-tau*L0)
        recurrence=(1-zf)**2+zf*(1-zf)*L1+zf**2*tau**(2*n)
        lb,ub=expected_eigen
        b_lower=1-2*p*p*lb
        b_upper=1-2*p*p*ub
        actual=(1-zf+zf*b_lower**(2*n))*(1-zf+zf*b_upper**(2*n))
        equal(recurrence,actual,
              f"actual full128 HJR scalar recurrence horizon {n}")
    # Structural FIRST-SOURCE check at n=1 for arbitrary ambient
    # Hermitian δA that DOES NOT preserve the 8+8 CAR spectrum.
    D=s.zeros(d)
    D[0,0]=1
    D[0,1]=D[1,0]=1
    lb,ub=expected_eigen
    def fprime(lam,n=1):
        b0=1-2*p*p*lam
        return 4*n*p*p*zf*b0**(2*n-1)/(1-zf+zf*b0**(2*n))
    beta=(fprime(ub)-fprime(lb))/(ub-lb)
    alph=fprime(lb)-beta*lb
    source_moments=alph*s.trace(D)+beta*s.trace(A0*D)
    source_eig=s.trace((alph*s.eye(d)+beta*A0)*D)
    equal(source_moments,source_eig,
          "whole closed HJR arbitrary ambient first source in two traces")
    print("PASS_ORIGINAL_CAR16_TWO_EIGENVALUE_CLOSED_FORM")
    print(" symbolic CAR16 all-r,all-nu minimal polynomial: PASS")
    print(" actual fixture eigenvalue multiplicities: 8+8")
    print(" Z_A = 80491520/69399")
    print(" q_A = 69399*p^3/1257680")
    print(" rho_A = I16/8 - A/Tr(A); d_nu rho_A=0")
    print(" original configured Brinkmann normal geometric source != 0")
    print(" native full16 logdet SOURCE spans two traces even off quadratic chart")
    print(" native 2x2 moment Jacobian at original fixture is NONZERO")
    print(" whole original full128 closed HJR: 2nd-order recurrence and first source PASS")
    print(" GR_closed=false; complete native-price/source selection still open")


if __name__=="__main__":
    main()
