#!/usr/bin/env python3
"""Exact Golden 0/10 native N1 nonlinear constitutive/Legendre source theorem.

No replacement geometric action, fitted Info, Newton coefficient or physical
Book03 selection. Default: outward Hessian certificate on WHOLE x,y square.
--original42: rigorous inputs from old h0 exact 42-root ball.
--full42: additionally compare ALL 42 source rows directly on the SAME scalar.
The original h0 1764-Hessian Banach existence proof is consumed, NOT rerun.
"""
from __future__ import annotations
from pathlib import Path
import argparse
import sys
from mpmath import mp, iv

def require(b, name):
    if not bool(b):
        raise RuntimeError("FAILED "+name)

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
    det=hxx*hyy-hxy*hxy
    h=-(r*ctx.log(r)+(1-r)*ctx.log(1-r))/lp
    # Exactly the same original two-tick N1 flat click, NOT a fit.
    r0=z*4*p**3*(2+p**6)-z*z*(4*p**3)**2*(1+p**6)
    h0=-(r0*ctx.log(r0)+(1-r0)*ctx.log(1-r0))/lp
    c=(r-h)-(r0-h0) # Literal original 0/10 E Cost =1+r, minus Shannon.
    return {"r":r,"rx":rx,"ry":ry,"rxx":rxx,"rxy":rxy,"ryy":ryy,
            "c":c,"a":cp*rx,"b":cp*ry,"hxx":hxx,"hxy":hxy,"hyy":hyy,
            "det":det,"lambda":ry/rx}

def core_cert():
    iv.dps=100
    result=native(iv,iv.mpf(['-0.01','0.01']),iv.mpf(['-0.01','0.01']))
    require(result["r"].a>iv.mpf('1.8e-6'),"native report stays positive")
    require(result["r"].b<iv.mpf('1.9e-6'),"native report stays below one")
    require(result["rx"].a>iv.mpf(0),"no source-ratio singularity")
    require(result["hxx"].a>iv.mpf('1.07e-6'),"strict positive first minor")
    require(result["hyy"].a>iv.mpf('3.8e-5'),"strict positive second diag")
    require(result["det"].a>iv.mpf('2.24e-11'),"full native two-operand det")
    require((result["hxx"]+result["hyy"]).b<iv.mpf('5e-5'),
            "uniform strong-convexity eigen bound")
    print("PASS full box |x|,|y|<=0.01: original F/R 0/10 N1 cost strictly convex")
    print("CERT Hxx lower >1.07e-6, Hyy lower >3.8e-5, det >2.24e-11")
    print("CERT all Hessian eigenvalues >4.48e-7; unique analytic 2-response inverse")

def flat_running_source():
    mp.dps=75
    v=native(mp,mp.mpf(0),mp.mpf(0))
    lam=v["lambda"]
    dx=(v["rxy"]*v["rx"]-v["ry"]*v["rxx"])/v["rx"]**2
    dy=(v["ryy"]*v["rx"]-v["ry"]*v["rxy"])/v["rx"]**2
    require(abs(lam+mp.mpf("23.4164067518840749729"))<mp.mpf("1e-18"),
            "original exact Golden J2 Einstein/CAR ratio")
    print("PASS original lambda_-= ",mp.nstr(lam,24))
    print("PASS nonlinear lambda_x, lambda_y=",mp.nstr(dx,20),mp.nstr(dy,20))

def original_root(full42=False):
    roots=[d for d in Path(__file__).resolve().parents
           if (d/"02_REGISTRY/research/sources").is_dir()]
    require(len(roots)>0,"run --original42 from the original GitHub checkout")
    root=roots[0]
    folder=root/"02_REGISTRY/research/sources/d0_original_unpadded42_2026-10-22"
    require(folder.is_dir(),"original independently certified nonflat full42 owner")
    sys.path.insert(0,str(folder))
    from certified_unpadded import NativeUnpaddedCQ as CQ, rational_center, CENTER
    from decimal import Decimal
    iv.dps=110
    m=CQ(iv)
    eps=Decimal("1e-24")
    z=[iv.mpf([str(Decimal(u)-eps),str(Decimal(u)+eps)])
       for u in CENTER["z42"]]
    e,U,ps=m.nodes(z)
    for j in range(2):
        co=m.E[0] if j==0 else e
        us=m.U[0] if j==0 else U
        vs=U if j==0 else m.U[2]
        f=m.curvature(co,us,vs)
        g=(co.T*m.eta*co)**-1
        q=iv.mpc(0)
        for k in (0,1):
            v=iv.matrix([(ps[j+1][k]-ps[j][k])/m.h,
                         m.amp if k==1 else iv.mpf(0),0,0])
            q+=(v.T*g*v)[0]
        x=(-m.tau*f/m.rho[j]).real
        y=(m.tau*q/m.rho[j]).real
        require(x.a>iv.mpf("-0.01") and x.b<iv.mpf("0.01"),"actual f in convex chart")
        require(y.a>iv.mpf("-0.01") and y.b<iv.mpf("0.01"),"actual CAR in convex chart")
        v=native(iv,x,y)
        V=v["a"]*x+v["b"]*y-v["c"] # derived Legendre potential, NOT a counterterm
        if j==0:
            require(v["lambda"].b<iv.mpf("-23.51"),"cell0 offnull source")
        else:
            require(v["lambda"].a>iv.mpf("-23.41"),"cell1 offnull source")
        print("PASS ORIGINAL exact h0 42-root ball cell",j,
              "x",float(x.a),"y",float(y.a),
              "lambda source",float(v["lambda"].a),float(v["lambda"].b),
              "derived PF-potential",float(V.a),float(V.b))
    print("PASS genuine two-cell running response is DISTINCT on exact 42-root ball")
    if full42:
        mp.dps=72
        point=CQ(mp)
        center=rational_center(mp)
        def cells(Z):
            e,U,ps=point.nodes(Z)
            out=[]
            for j in (0,1):
                co=point.E[0] if j==0 else e
                us=point.U[0] if j==0 else U
                vs=U if j==0 else point.U[2]
                f=point.curvature(co,us,vs)
                g=(co.T*point.eta*co)**-1
                q=mp.mpc(0)
                for k in (0,1):
                    v=mp.matrix([(ps[j+1][k]-ps[j][k])/point.h,
                         point.amp if k==1 else mp.mpf(0),0,0])
                    q+=(v.T*g*v)[0]
                out.append((-point.tau*f/point.rho[j],
                            point.tau*q/point.rho[j]))
            return out
        xx=cells(center)
        response=[tuple(native(mp,*v)[s] for s in ("a","b")) for v in xx]
        V=[aa*xi+bb*yi-native(mp,xi,yi)["c"]
           for (aa,bb),(xi,yi) in zip(response,xx)]
        kappa=-point.norm
        def dual_price(Z):
            return kappa*sum(point.rho[j]*
                  (response[j][0]*xi+response[j][1]*yi-V[j])
                  for j,(xi,yi) in enumerate(cells(Z)))
        require(abs(dual_price(center)-point.price(center))<mp.mpf("1e-56"),
                "exact native scalar price equals algebraic dual at root")
        step=mp.mpf("1e-27")
        err=mp.mpf(0)
        for k in range(42):
            v=list(center);v[k]+=1j*step
            err=max(err,abs(mp.im(dual_price(v)-point.price(v))/step))
        require(err<mp.mpf("1e-30"),
                "all42 SAME original free-field Euler/source rows preserved")
        print("PASS FULL original 42 variations of SAME scalar price versus fixed-response dual, max first-source error",mp.nstr(err,14))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--original42",action="store_true")
    ap.add_argument("--full42",action="store_true")
    opt=ap.parse_args()
    core_cert()
    flat_running_source()
    if opt.original42 or opt.full42:
        original_root(opt.full42)
    print("SCOPE native unpadded configured N1; physical compulsory Book03/G0 selection still OPEN; GR_closed=false")

if __name__=="__main__":
    main()
