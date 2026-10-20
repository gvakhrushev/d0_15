#!/usr/bin/env python3
"""New reconstruction check; exact identities plus an 85-digit diagnostic.
No repository writes; JSON goes to stdout or explicit --output path.
"""
import argparse
import hashlib
import json
import platform
import time
from pathlib import Path
import sympy as S
import mpmath as mp


def require(test, label):
    if not bool(test):
        raise RuntimeError(label)


def zero(expr):
    if isinstance(expr, S.MatrixBase):
        return all(S.simplify(v) == 0 for v in expr)
    return S.simplify(expr) == 0


def exact_checks():
    A = S.Matrix([[2, 3], [3, 0]])
    C = S.Matrix([[1, 4], [-2, 5]])  # rows x, columns y: deliberately nonsymmetric
    E = S.Matrix([[7, -1], [-1, 6]])
    D = S.diag(S.Rational(3, 2), S.Rational(-2, 3))
    I, O = S.eye(2), S.zeros(2)
    H = A.row_join(-I).col_join((-I).row_join(O))
    Hi = O.row_join(-I).col_join((-I).row_join(-A))
    require(H * Hi == S.eye(4), 'auxiliary inverse with nonzero A')
    for At in [O, S.diag(1, 0)]:
        Ht = At.row_join(-I).col_join((-I).row_join(O))
        Hit = O.row_join(-I).col_join((-I).row_join(-At))
        require(Ht * Hit == S.eye(4), 'inverse when Fxx is singular')
    J = I.row_join(O).col_join((A / 2).row_join(I))
    require(J.T * H * J == O.row_join(-I).col_join((-I).row_join(O)), 'exact inertia congruence')
    U = C.col_join(D)
    schur = E - U.T * Hi * U
    expected = E + D * C + C.T * D + D * A * D
    T = D.col_join(I)
    HF = A.row_join(C).col_join(C.T.row_join(E))
    require(schur == expected == T.T * HF * T, 'ordered coupled Hessian')
    require(expected != E + C * D + D * C.T + D * A * D, 'wrong cross-order hostile control')
    require(-Hi * U == D.col_join(C + A * D), 'section first derivative')

    x1, x2, y1, y2, zeta = S.symbols('x1 x2 y1 y2 zeta', real=True)
    xs, ys = S.Matrix([x1, x2]), S.Matrix([y1, y2])
    av = S.Matrix([2+zeta, 3-zeta])
    bv = S.Matrix([3+2*zeta, -2+zeta])
    F = (av.T*xs)[0]+(bv.T*ys)[0]+(xs.T*A*xs)[0]/2+(xs.T*C*ys)[0]+(ys.T*E*ys)[0]/2
    F += x1*y2*y2/7 + zeta*x1*x2
    s1, s2, pi1, pi2, X1, X2, Y1, Y2 = S.symbols('s1 s2 pi1 pi2 X1 X2 Y1 Y2', real=True)
    sv, piv = S.Matrix([s1, s2]), S.Matrix([pi1, pi2])
    B = zeta + zeta**2/2
    ext = B + F.subs({x1:s1, x2:s2}, simultaneous=True) + pi1*(x1-s1)+pi2*(x2-s2)
    transformed = ext.subs({x1:av[0]*X1/pi1, x2:av[1]*X2/pi2,
                            y1:pi1*Y1/av[0], y2:pi2*Y2/av[1]}, simultaneous=True)
    G = F.subs({x1:s1, x2:s2, y1:pi1*Y1/av[0], y2:pi2*Y2/av[1]}, simultaneous=True)-pi1*s1-pi2*s2
    target = B+av[0]*X1+av[1]*X2+G
    require(zero(transformed-target), 'exact extended-coordinate identity')
    base = {s1:0,s2:0,pi1:2,pi2:3,Y1:0,Y2:0,zeta:0}
    aux = [s1,s2,pi1,pi2]
    require(S.hessian(G,aux).subs(base) == H, 'actual auxiliary Hessian')
    actual_cross = S.Matrix([S.diff(G,u) for u in aux]).jacobian([Y1,Y2]).subs(base)
    require(actual_cross == U, 'actual ordered mixed block')
    require(S.hessian(G,[Y1,Y2]).subs(base) == E, 'actual direct YY block')

    # Same density formula has genuine independent-site homogeneity and moving zeta data.
    v1,v2,w1,w2,m1,m2 = S.symbols('v1 v2 w1 w2 m1 m2', nonzero=True)
    dens = {x1:v1**2*(w1+2*w2), x2:v2**2*(3*w1-w2),
            y1:(m1+zeta)/v1**2, y2:(m2-2*zeta)/v2**2}
    full = (B+F).subs(dens, simultaneous=True)
    linear = (B+(av.T*xs)[0]+(bv.T*ys)[0]).subs(dens, simultaneous=True)
    fields = [v1,v2,w1,w2,m1,m2,zeta]
    null = {v1:1,v2:1,w1:0,w2:0,m1:0,m2:0,zeta:0}
    gfull = S.Matrix([S.diff(full,v).subs(null) for v in fields])
    glin = S.Matrix([S.diff(linear,v).subs(null) for v in fields])
    require(gfull == glin, 'complete null-stratum source')
    require(gfull[-1] == 8, 'baseline plus moving material dictionary source')
    require(gfull[4] == 3 and gfull[5] == -2, 'nonzero null material source')
    require(S.diff(full-B,zeta).subs(null) == 7, 'dropping baseline changes source')
    no_y = (B+(av.T*xs)[0]).subs(dens, simultaneous=True)
    require(S.diff(no_y,zeta).subs(null) == 1, 'dropping null matter changes source')

    p = (S.sqrt(5)-1)/2
    zz = S.Rational(1,2**20)
    L = 4*p**3
    xx, yy = S.symbols('xx yy', real=True)
    scene = 4*(p+p*p*yy)**2*(1-(p+p*p*yy)**2)
    ell = 4*p*p*(1+xx)*(1-p*p*(1+xx))
    aa = ell+(1-ell)*scene
    r = 1-(1-zz*scene)*(1-zz*aa)
    at0 = {xx:0,yy:0}
    Q, R = 1-zz*L, 1-zz*L*(1+p**6)
    rx = S.simplify(S.diff(r,xx).subs(at0))
    ry = S.simplify(S.diff(r,yy).subs(at0))
    By, Byy = 8*p**6, 8*p**4*(1-6*p*p)
    Ax, Ay, Axx, Axy, Ayy = 4*p**11,8*p**12,-8*p**10,-32*p**11,p**6*Byy
    for lhs,rhs,label in [
        (S.diff(scene,yy).subs(at0),By,'By'),(S.diff(scene,yy,2).subs(at0),Byy,'Byy'),
        (S.diff(aa,xx).subs(at0),Ax,'Ax'),(S.diff(aa,yy).subs(at0),Ay,'Ay'),
        (S.diff(aa,xx,2).subs(at0),Axx,'Axx'),(S.diff(aa,xx,yy).subs(at0),Axy,'Axy'),
        (S.diff(aa,yy,2).subs(at0),Ayy,'Ayy'),
        (rx,zz*Q*Ax,'rx'),(ry,zz*(R*By+Q*Ay),'ry'),
        (S.diff(r,xx,2).subs(at0),zz*Q*Axx,'rxx'),
        (S.diff(r,xx,yy).subs(at0),zz*Q*Axy-zz**2*By*Ax,'rxy'),
        (S.diff(r,yy,2).subs(at0),zz*(R*Byy+Q*Ayy)-2*zz**2*By*Ay,'ryy')]:
        require(zero(lhs-rhs), 'literal detector '+label)
    ratio = S.simplify(ry/rx)
    finite = 10+6*S.sqrt(5)-8*zz*p**4/Q
    owner = 2*p**(-5)*(R/Q+p**6)
    require(zero(ratio-finite) and zero(owner-finite), 'exact finite ratio and current lambda owner')
    require(zero(1-p**6-L), 'Golden complement identity')
    require(not zero(finite-(10+6*S.sqrt(5))), 'finite ratio is not its limit')
    # Rational enclosures supply signs and the all-cap bound without decimal inference.
    lo, hi = S.Rational(618,1000), S.Rational(619,1000)
    require(lo**2+lo-1<0<hi**2+hi-1, 'Golden root rational bracket')
    require(4*lo**3>S.Rational(47,50) and 4*hi**3<1, '47/50<L<1')
    require(6*lo**2>1 and hi**2<S.Rational(1,2), 'Byy<0 and log_phi(2)<2')
    require(S.Rational(47,50)*(3-S.Rational(47,50))-2*zz>1, 'r0>2^-20')
    require(51-40/(1-S.Rational(1,2**19))>10, 'uniform finite-cap derivative lower bound')
    require(18+S.Rational(22,25)*40 == S.Rational(266,5)>53, 'owned unit-price lower bound')
    return {'coupled_KYY': [list(expected.row(i)) for i in range(2)],
            'full_null_source': list(gfull),
            'finite_ratio':str(S.N(finite,65)),
            'limit_minus_finite':str(S.N(8*zz*p**4/Q,65)),
            'all_cap_lower_factor':str(51-40/(1-S.Rational(1,2**19))),
            'exact_detector_derivatives':'PASS', 'wrong_cross_order':'REJECTED',
            'singular_Fxx':'PASS', 'source_deletion_controls':'REJECTED'}


def precision_checks():
    mp.mp.dps = 85
    p=(mp.sqrt(5)-1)/2
    z=mp.mpf(2)**-20
    alpha,beta,kappa=mp.mpf(3)/5,mp.mpf(5)/7,mp.mpf(54)
    logphi=mp.log(1/p)
    def r(x,y):
        b=4*(p+p*p*y)**2*(1-(p+p*p*y)**2)
        e=p*p*(1+x)
        ell=4*e*(1-e)
        aa=ell+(1-ell)*b
        return 1-(1-z*b)*(1-z*aa)
    def entropy(q):
        return -(q*mp.log(q)+(1-q)*mp.log(1-q))/logphi
    r0=r(0,0)
    rows=[]
    maxres=mp.mpf(0)
    maxrel=mp.mpf(0)
    for N in [1,2,7,31]:
        def V(q):
            return alpha*(kappa-beta*entropy(q))*mp.fsum([(beta*q)**j for j in range(N)])
        V0=V(r0)
        def F(x,y): return V(r(x,y))-V0
        def Fx(x,y): return mp.diff(lambda q: F(q,y),x)
        def Fy(x,y): return mp.diff(lambda q: F(x,q),y)
        a,b=Fx(0,0),Fy(0,0)
        d=b/a
        fxx=mp.diff(lambda q: F(q,0),0,2)
        fxy=mp.diff(lambda q: Fx(0,q),0)
        fyy=mp.diff(lambda q: F(0,q),0,2)
        k2=fyy+2*d*fxy+d*d*fxx
        require(a<0 if N==1 else a>0, 'cap slope sign')
        if N==1: require(k2>0,'one-cap induced material Hessian positive')
        def section(Y):
            eq1=lambda s,k: Fx(s,k*Y)/a-k
            eq2=lambda s,k: s-(Y/a)*Fy(s,k*Y)
            s,k=mp.findroot((eq1,eq2),(d*Y,1),tol=mp.mpf('1e-72'),maxsteps=40)
            res=max(abs(eq1(s,k)),abs(eq2(s,k)))
            require(k>0,'positive coframe scale')
            require(res<mp.mpf('1e-65'),'normalized auxiliary equations')
            return F(s,k*Y)-a*k*s,res,s,k
        samples=[]
        for Y in [mp.mpf('-1e-4'),mp.mpf('1e-4')]:
            kval,res,s,k=section(Y)
            maxres=max(maxres,res)
            samples.append({'Y':mp.nstr(Y,8),'s':mp.nstr(s,40),'pi_over_a':mp.nstr(k,40),
                            'residual':mp.nstr(res,12)})
        delta=mp.mpf('1e-14')
        kp,_,_,_=section(delta)
        km,_,_,_=section(-delta)
        fd=(kp+km)/(delta*delta)
        rel=abs((fd-k2)/k2)
        maxrel=max(maxrel,rel)
        require(rel<mp.mpf('1e-20'),'independently evaluated section second coefficient')
        rows.append({'N':N,'a':mp.nstr(a,45),'b_over_a':mp.nstr(d,45),
                     'K_second':mp.nstr(k2,45),'section_second_relative_error':mp.nstr(rel,12),
                     'samples':samples})
    return {'precision_digits':85, 'fixture':{'alpha':'3/5','beta':'5/7','kappa':'54'},
            'r0':mp.nstr(r0,45),'caps':rows,
            'max_normalized_auxiliary_residual':mp.nstr(maxres,20),
            'max_second_coefficient_relative_error':mp.nstr(maxrel,20)}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    start=time.perf_counter()
    result={'status':'PASS','kind':'new reconstruction, not historical replay',
            'runtime':{'python':platform.python_version(),'sympy':S.__version__,'mpmath':mp.__version__},
            'exact':exact_checks(),'high_precision':precision_checks()}
    result['elapsed_seconds']=time.perf_counter()-start
    result['checker_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    payload=json.dumps(result,indent=2,default=str)+'\n'
    if args.output:
        args.output.write_text(payload)
        print(json.dumps({'status':result['status'],'output':str(args.output),
                          'elapsed_seconds':result['elapsed_seconds'],
                          'residual':result['high_precision']['max_normalized_auxiliary_residual'],
                          'second_error':result['high_precision']['max_second_coefficient_relative_error']}))
    else: print(payload,end='')

if __name__=='__main__': main()
