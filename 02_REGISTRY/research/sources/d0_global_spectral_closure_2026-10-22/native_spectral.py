"""Literal Golden two-band scalar and exact first/second operand derivatives.

No field geometry or physical Book03 selection is inferred by this module.
ctx may be mpmath.mp or mpmath.iv.
"""
from __future__ import annotations


def jets(ctx, x, y, theta=0):
    p=(ctx.sqrt(5)-1)/2
    z=ctx.mpf(2)**-20
    beta=2*p*p
    E=p*p*(1+x); L=4*E*(1-E)
    Lx=4*p*p*(1-2*E); Lxx=-8*p**4
    b=p-p*p*y; B=4*b*b*(1-b*b)
    By=-8*p*p*b*(1-2*b*b); Byy=8*p**4*(1-6*b*b)
    A=L+(1-L)*B
    Ax=Lx*(1-B); Ay=(1-L)*By
    Axx=Lxx*(1-B); Axy=-Lx*By; Ayy=(1-L)*Byy
    ea=ctx.exp(-beta*A); eb=ctx.exp(-beta*B)
    j=-ctx.log(1-z*A)-ctx.log(1-z*B)
    t=ea+eb
    wA=z/(1-z*A)-theta*ea
    wB=z/(1-z*B)-theta*eb
    vA=z*z/(1-z*A)**2+theta*beta*ea
    vB=z*z/(1-z*B)**2+theta*beta*eb
    Fx=wA*Ax; Fy=wA*Ay+wB*By
    Fxx=vA*Ax**2+wA*Axx
    Fxy=vA*Ax*Ay+wA*Axy
    Fyy=vA*Ay**2+wA*Ayy+vB*By**2+wB*Byy
    F=j+theta*t/beta
    T=x*Fx-y*Fy
    Tx=Fx+x*Fxx-y*Fxy
    Ty=x*Fxy-Fy-y*Fyy
    H=F-x*Fx
    Hx=-x*Fxx; Hy=Fy-x*Fxy
    det=Tx*Hy-Ty*Hx
    return dict(A=A,B=B,Ax=Ax,Ay=Ay,By=By,Axx=Axx,Axy=Axy,Ayy=Ayy,Byy=Byy,
                j=j,t=t,F=F,Fx=Fx,Fy=Fy,Fxx=Fxx,Fxy=Fxy,Fyy=Fyy,
                T=T,Tx=Tx,Ty=Ty,H=H,Hx=Hx,Hy=Hy,ward_det=det,beta=beta,z=z)


def complete(ctx, x, y, W, Z0=0):
    a=jets(ctx,x,y)
    Z=Z0+2*W*a['t']
    theta=2/Z
    b=jets(ctx,x,y,theta)
    b.update(Z=Z,theta=theta,price=ctx.log(Z)/b['beta']+W*b['j'])
    # G=T(x,y; theta(x,y)), its true derivative includes thermal feedback.
    thx=theta**2*W*b['beta']*ctx.exp(-b['beta']*b['A'])*b['Ax']
    thy=theta**2*W*b['beta']*(ctx.exp(-b['beta']*b['A'])*b['Ay']+ctx.exp(-b['beta']*b['B'])*b['By'])
    Tth=-x*ctx.exp(-b['beta']*b['A'])*b['Ax']+y*(ctx.exp(-b['beta']*b['A'])*b['Ay']+ctx.exp(-b['beta']*b['B'])*b['By'])
    b.update(Gx=b['Tx']+Tth*thx,Gy=b['Ty']+Tth*thy,theta_x=thx,theta_y=thy)
    return b
