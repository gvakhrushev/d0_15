import runpy, mpmath as mp, numpy as np
from pathlib import Path
mp.mp.dps=70
D=runpy.run_path(str(Path(__file__).with_name('check_native_n1_two_scalar_2d.py')))
M=D['M'];Nt=D['Nt'];Nx=D['Nx'];rho=D['rho'];h=D['h'];f=D['f'];tau=D['tau'];gt=D['gt'];gx=D['gx']; mat=D['mat_euler'];EPS=D['eps'] if 'eps' in D else .1

def price(x):
    A,B=D['unpack'](x)
    total=mp.mpf('0')
    for i in range(Nt-1):
        for j in range(Nx-1):
            qt=mp.mpf(str(gt[i]))*((mp.mpf(str(A[i+1,j]))-mp.mpf(str(A[i,j])))/h)**2
            qt+=mp.mpf(str(gt[i]))*((mp.mpf(str(B[i+1,j]))-mp.mpf(str(B[i,j])))/h)**2
            qt+=mp.mpf(str(gx[i]))*((mp.mpf(str(A[i,j+1]))-mp.mpf(str(A[i,j])))/h)**2
            qt+=mp.mpf(str(gx[i]))*((mp.mpf(str(B[i,j+1]))-mp.mpf(str(B[i,j])))/h)**2
            rr=M.raw(mp.mpf(str(-tau*f[i]/rho[i,j])),mp.mpf(str(tau/rho[i,j]))*qt)
            H=-(rr*mp.log(rr)+(1-rr)*mp.log(1-rr))/M.lnphi
            total-=mp.mpf(str(h*h*rho[i,j]))*H
    return total

dx=3e-5
for label,x in [('before',D['x0']),('solved',D['sol'].x)]:
    residual=mat(x)
    for j in [0,5,12,35,36,42,60,71]:
        x0=x.copy();x1=x.copy();x0[j]+=dx;x1[j]-=dx
        secant=float((price(x0)-price(x1))/(2*dx))
        analytic=2*tau*h*float(M.norm)*residual[j]
        assert abs(secant-analytic)<1e-15,(label,j,secant,analytic)
        print(label,j,'actual=',secant,'predicted=',analytic,'absolute_delta=',secant-analytic)

print("PASS_TRUE_N1_PRICE_TWO_SCALAR_SECANTS_BOTH_BEFORE_AND_AFTER")
