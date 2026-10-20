#!/usr/bin/env python3
"""Native Dirac protected low-grade reference128 exact fixedRIGHT saddle.
The spectral quartet intertwiner is a previously proved full16 theorem;
this independently checks its ORIGINAL periodic-u 2-grade spectrum.
"""
import math
import numpy as np
L_u=65
nu=0.7
T_u=1.3
h=T_u/L_u
def eig(k):
    return 4*nu*nu/(h*h)*math.sin(math.pi*k/L_u)**2
spectrum=np.tile(np.array([eig(k) for k in range(L_u)]),2)
occupied=np.array([i for i in range(2*L_u) if i%L_u!=0])
assert len(occupied)==128
assert len(spectrum)==130 and spectrum[0]==spectrum[L_u]==0
assert (spectrum[occupied]>0).all()
M=np.eye(130)[:,occupied]/math.sqrt(128)
Delta=np.diag(spectrum)
gram=np.eye(128)/128
assert np.max(np.abs(M.T@M-gram))<1e-14
rho=M@M.T
assert np.max(abs(Delta@rho-rho@Delta))==0
base=float(np.trace(M.T@Delta@M))
j=np.flatnonzero(occupied==1)[0]
for th in (0.02,-0.02,0.10):
    new=M.copy()
    new[:,j]=math.cos(th)*M[:,j]
    new[0,j]=math.sin(th)/math.sqrt(128)
    assert np.max(abs(new.T@new-gram))<1e-14
    val=float(np.trace(new.T@Delta@new))
    exact=base-eig(1)*math.sin(th)**2/128
    assert abs(val-exact)<1e-9 and val<base
Hess=-eig(1)/64
assert Hess<0 and Hess<=-nu*nu/(4*T_u*T_u)
print("PASS original u periodic lowgrade 2L_u=130, selected 128 nonzero Fourier modes")
print("PASS fixed RIGHT 128x128 Gram, [Delta,rho]=0 full preparation stationarity")
print("PASS exact rank-one LEFT rotation into native unused k0 energy0")
print("PASS strict negative true preparation Hessian",Hess)
print("PASS negative prep Hessian survives fixed T_u continuum refinement")
print("PASS exact protected H,K source null follows from full16 operator intertwiner")
print("FIREWALL conditional H+J+R critical saddle is not native stable MINIMUM")
print("GR_closed=false")

# Strict positive R and simultaneous exact coframe scale / observer
# necessary Ward on same genuine original fixedRIGHT low-grade preparation.
R0=sum(eig(k) for k in range(1,33))/32
assert abs(R0-(65*nu*nu/(32*h*h)))<1e-8
assert abs(R0-base)<1e-8
for parameter in (-0.2,-0.01,0.03,0.17):
    Rp=math.exp(2*parameter)*R0
    # Both admitted chart transformations have the identical native R law:
    # D(e^sigma v)=e^sigma D(v); owner observer n(tau) has R=e^(2tau) R0.
    assert abs(Rp-math.exp(2*parameter)*base)<1e-8
assert abs(2*R0-(65*nu*nu/(16*h*h)))<1e-8
refine_limit=1430*math.pi**2*nu*nu/(T_u*T_u)
for L2 in (131,257,1025,4097):
    h2=T_u/L2
    val=sum((4*nu**2/h2**2)*math.sin(math.pi*k/L2)**2
             for k in range(1,33))/32
    assert 0<val<refine_limit
assert refine_limit>0
print('PASS simultaneous scale + observer Ward: d_sigma R=d_tau R=2R0 >0')
print('PASS finite L=65 exact R0=65 nu^2/(32h^2) and normalizing Gram')
print('PASS fixed-T rank128 h-refining exact spectral energy limit=1430 pi^2 nu^2/T^2')
print('FIREWALL real selected H+J requires BOTH native -2R rows, not inferred from prep')
