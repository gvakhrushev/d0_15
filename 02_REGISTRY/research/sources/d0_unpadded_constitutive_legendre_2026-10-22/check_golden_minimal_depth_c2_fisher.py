#!/usr/bin/env python3
"""Original unpadded Golden N1: min depth, exact C2 source, 4D complete KL.

Mathematical field-query scale tau=p^m, with m=min{m:p^m<=1/L^2};
physical G0 actuation and full Book03 HJR NOT proved or assumed.
"""
from mpmath import mp, iv


def check(ok, msg):
    if not bool(ok):
        raise RuntimeError(msg)


def native(ctx, x, y):
    p=(ctx.sqrt(5)-1)/2
    z=ctx.mpf(2)**(-20)
    lp=ctx.log(1/p)
    E=p*p*(1+x)
    ell=4*E*(1-E)
    ellx=4*p*p*(1-2*E)
    ellxx=-8*p**4
    b=p-p*p*y
    B=4*b*b*(1-b*b)
    By=-8*p*p*b*(1-2*b*b)
    Byy=8*p**4*(1-6*b*b)
    A=ell+(1-ell)*B
    Ax=ellx*(1-B);Ay=(1-ell)*By
    Axx=ellxx*(1-B);Axy=-ellx*By;Ayy=(1-ell)*Byy
    r=z*(A+B)-z*z*A*B
    rx=z*Ax*(1-z*B)
    ry=z*(Ay*(1-z*B)+By*(1-z*A))
    rxx=z*Axx*(1-z*B)
    rxy=z*(Axy*(1-z*B)-z*Ax*By)
    ryy=z*(Ayy*(1-z*B)+Byy*(1-z*A)-2*z*Ay*By)
    hp=ctx.log((1-r)/r)/lp
    cp=1-hp
    cpp=1/(lp*r*(1-r))
    hxx=cpp*rx*rx+cp*rxx
    hxy=cpp*rx*ry+cp*rxy
    hyy=cpp*ry*ry+cp*ryy
    ent=-(r*ctx.log(r)+(1-r)*ctx.log(1-r))/lp
    L0=4*p**3
    A0=L0*(1+p**6)
    r0=z*(A0+L0)-z*z*A0*L0
    ent0=-(r0*ctx.log(r0)+(1-r0)*ctx.log(1-r0))/lp
    return dict(r=r,rx=rx,ry=ry, c=(r-ent)-(r0-ent0),
                a=cp*rx,b=cp*ry,hxx=hxx,hxy=hxy,hyy=hyy,
                det=hxx*hyy-hxy*hxy)


def norm(w):
    return mp.sqrt(sum(x*x for x in w))


def run():
    iv.dps=100
    V=native(iv,iv.mpf(['-0.01','0.01']),iv.mpf(['-0.01','0.01']))
    Hrow=max(V['hxx'].b+abs(V['hxy']).b,V['hyy'].b+abs(V['hxy']).b)
    check(Hrow < iv.mpf('5e-5'),'global Hessian row upper')
    check(V['det'].a>iv.mpf('2.24e-11'),'strict positive convex determinant')
    print('PASS WHOLE |x|,|y|<=.01 native N1 Hessian operator norm <5e-5')
    mp.dps=75
    p=(mp.sqrt(5)-1)/2;phi=1/p
    o=native(mp,mp.mpf(0),mp.mpf(0))
    lp=mp.log(phi);r0=o['r'];hp=mp.log((1-r0)/r0)/lp
    K0=1/(hp*o['rx'])
    a,b=o['a'],o['b']
    gam=K0*a;lam=b/a
    check(abs(lam+mp.mpf('23.416406751884075'))<mp.mpf('1e-12'),
          'unaltered source ratio')
    quad=[K0*o['hxx']/2,K0*o['hxy'],K0*o['hyy']/2]
    print('PASS original gamma, lambda:',mp.nstr(gam,16),mp.nstr(lam,16))
    print('PASS fixed f², fq, q² correction:',*[mp.nstr(v,18) for v in quad])

    # Actual nonnull moving-PF field profile; test every untruncated source
    # derivative through SECOND order vs the analytical global error budget.
    def rho(t):return mp.mpf('1.1')+mp.mpf('.05')*t+mp.mpf('.04')*t*t
    def f(t):return mp.mpf('.7')+mp.mpf('.2')*t+mp.mpf('.1')*t*t
    def q(t):return -mp.mpf('.3')+mp.mpf('.1')*t+mp.mpf('.15')*t*t
    w=mp.matrix([f(0),q(0)])
    dw=mp.matrix([mp.diff(f,0),mp.diff(q,0)])
    ddw=mp.matrix([mp.diff(f,0,2),mp.diff(q,0,2)])
    r=rho(0);dr=mp.diff(rho,0);ddr=mp.diff(rho,0,2)
    M=mp.mpf('5e-5')
    for L in (16,32,64,128,256):
        h=mp.mpf(1)/L
        m=0
        while phi**m<L*L:m+=1
        s=0
        while phi**s<L:s+=1
        tau=p**m
        check(p*h*h<tau<=h*h,'minimum native cylinder depth')
        check(m<=2*s<=m+1,'at most one Golden code cost improvement')
        check(tau*norm(w)/r<mp.mpf('.01'),'genuine nonnull query in chart')
        def S(t):
            density=rho(t)
            return K0/tau*density*native(mp,tau*f(t)/density,
                                              tau*q(t)/density)['c']
        def A(t):return K0*(a*f(t)+b*q(t))
        errs=[abs(mp.diff(S,0,k)-mp.diff(A,0,k)) for k in range(3)]
        bounds=[K0*M*tau*norm(w)**2/(2*r),
                K0*M*tau*(norm(w)*norm(dw)/r+norm(w)**2*abs(dr)/(2*r*r)),
                K0*M*tau*(norm(w)*norm(ddw)/r+norm(w)**2*abs(ddr)/(2*r*r)
                           +norm(dw-w*dr/r)**2/r)]
        for k in range(3):
            check(errs[k]<bounds[k],f'full native moving-PF C{k} bound')
        correction=K0*tau/(2*r)*(w.T*mp.matrix([
                     [o['hxx'],o['hxy']],[o['hxy'],o['hyy']]])*w)[0]
        check(abs(S(0)-A(0)-correction)<2*tau**2,
              'original quadratic correction exact to O(tau²)')
        print('PASS offnull C0,C1,C2 L=',L,'m=',m,'tau=',mp.nstr(tau,8),
              'errors=',*[mp.nstr(err,7) for err in errs])

    # 4D critical full-RECORD information under the explicitly stated
    # independent per-site execution hypothesis. No clicked-only conditioning.
    def KL(v,z):return v*mp.log(v/z)+(1-v)*mp.log((1-v)/(1-z))
    wa=(mp.mpf('.7'),-mp.mpf('.3'))
    wb=(mp.mpf('.2'),mp.mpf('.1'))
    d=o['rx']*(wa[0]-wb[0])+o['ry']*(wa[1]-wb[1])
    check(abs(d)>mp.mpf('1e-8'),'true nonvanishing original comparison')
    coef=d*d/(2*r0*(1-r0))
    for L in (16,32,64,128,256,512,1024):
        m=0
        while phi**m<L*L:m+=1
        tau=p**m
        signalA=native(mp,tau*wa[0],tau*wa[1])['r']
        signalB=native(mp,tau*wb[0],tau*wb[1])['r']
        info=L**4*KL(signalA,signalB)
        scaled=L**4*tau**2
        check(p**2<scaled<=1,'exact 4D Golden information window')
        check(abs(info/(scaled*coef)-1)<mp.mpf('.01'),
              'complete Bernoulli KL agrees with exact native quadratic signal')
        print('PASS 4D full-record Bernoulli L=',L,'L^4 tau²=',
              mp.nstr(scaled,10),'KLtotal=',mp.nstr(info,10))
    print('PASS: minimal native depth, complete offnull C² source, 4D Fisher criticality')
    print('PHYSICAL status: query-strength gate/writer and whole Book03 HJR NOT SELECTED; GR_closed=false')

if __name__=='__main__':run()
