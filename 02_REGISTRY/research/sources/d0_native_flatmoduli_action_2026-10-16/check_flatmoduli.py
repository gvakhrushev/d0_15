"""Flat-modulus test of the unchanged conditional D0 v8 H+J+R price.

All 4096 momenta and sixteen CAR grades are retained.  The positive
finite Hessian theorem uses the existing interval-owned Z<50 at the
homogeneous rank-128 shell root; numerical values are cross-checks, not
substitutes for that owner's exact enclosure.
"""
import hashlib
import json
import math
from itertools import product
from pathlib import Path

import numpy as np
import sympy as sp

HERE = Path(__file__).resolve().parent
L = 8
P = (math.sqrt(5) - 1)/2
N = 128*L*L
ALPHA = P*P/N
MPOWER = 2*N
BETA = MPOWER*ALPHA
ZETA = 2**-20
M = 128
D = 0.0636351915943445350
O = 0.0040167350432317253
GAMMA = 128-64*math.sqrt(2)

def require(condition, label):
    if not bool(condition):
        raise ArithmeticError(label)

# Exact rational orthogonal projectors; no numerical eigenvector ambiguity.
v0 = sp.Matrix([1,1,1,1]); v1=sp.Matrix([1,-1,0,0]); v2=sp.Matrix([1,1,-2,0]);
P0 = v0*v0.T/4
P1 = v1*v1.T/2
P2 = v2*v2.T/6
P3 = sp.eye(4)-P0-P1-P2
PS = [P0,P1,P2,P3]
V_exact = P1-P2
for i in range(4):
    for j in range(4):
        require(PS[i]*PS[j] == (PS[i] if i==j else sp.zeros(4)), "orthogonal_projectors")
require(sp.trace(V_exact)==0 and V_exact*sp.ones(4,1)==sp.zeros(4,1), "trace_free_shape")

projectors = [np.array(a,dtype=float) for a in PS]
V = projectors[1]-projectors[2]
a = D+3*O
b = D-O
G0 = (D-O)*np.eye(4)+O*np.ones((4,4))
require(a>b>0 and np.linalg.eigvalsh(G0)[0]>0, "positive_root")
require(abs(np.trace(np.linalg.solve(G0,V)))<1e-11, "first_det_jet_zero")

# IFT: (a+s)[(b-s/3)^2-t^2](b-s/3)=a b^3.
# dF/ds at 0 = b^2(b-a) != 0; s'(0)=0 and s''(0)=-2a/(b(a-b)).
s2 = -2*a/(b*(a-b))
G2 = s2*(projectors[0]-(projectors[1]+projectors[2]+projectors[3])/3)

def s_of(t):
    s = (s2/2)*t*t
    for _ in range(8):
        c = b-s/3
        f = (a+s)*c*(c*c-t*t)-a*b**3
        df = c*(c*c-t*t)-(a+s)*(c*c-t*t/3)
        s -= f/df
    return s

def path(t):
    s=s_of(t)
    return ((a+s)*projectors[0]+(b-s/3+t)*projectors[1]
            +(b-s/3-t)*projectors[2]+(b-s/3)*projectors[3])

# Actual finite L=8 Fourier symbol; original all16 CAR states multiply trace.
q=np.array(list(product(range(L),repeat=4)),dtype=int)
z=L*(np.exp(2j*np.pi*q/L)-1)

def lam_finite(matrix):
    return np.einsum('ki,ij,kj->k',z.conjugate(),matrix,z).real

def finite_components(matrix):
    lam=lam_finite(matrix)
    B=1-ALPHA*lam
    require(np.min(B)>0 and np.max(B)<=1+1e-12, "finite_gate_window")
    K=B**MPOWER
    Z=16*np.sum(K)
    A=1-ZETA+ZETA*K
    H=math.log(Z)/BETA
    J=-16*M*np.sum(np.log(A))
    R=GAMMA*np.trace(matrix)/4
    return H,J,R,Z

H0,J0,R0,Z0=finite_components(G0)
require(Z0<50 and 16/Z0>8/25, "owned_partition_box_check")
delta=M*BETA*ZETA*Z0/(1-ZETA)
require(delta<0.01 and MPOWER==16384, "coercivity_inputs")
l0=lam_finite(G0);dlam=lam_finite(V);B=1-ALPHA*l0
K=B**MPOWER;W=16*K/Z0;den=1-ZETA+ZETA*K;y=dlam/B
Ey=np.dot(W,y);Ey2=np.dot(W,y*y)
c=(MPOWER-1)*ALPHA
Hessian=(c*Ey2-BETA*Ey*Ey-M*BETA*ZETA*c*Z0*np.dot(W,y*y/den)
         +M*BETA**2*ZETA**2*Z0*np.dot(W,K*y*y/den**2))
Lower=0.3*BETA*Ey2
require(abs(Ey)<1e-9 and Ey2>0 and Hessian>Lower>0, "finite_positive_Hessian")

def total(matrix):
    H,J,R,_=finite_components(matrix)
    return H+J+R

det0=np.linalg.det(G0); trace0=np.trace(G0)
finite_controls=[]
for t in (1e-4,2e-4,4e-4):
    gp=path(t);gm=path(-t)
    for gg in (gp,gm):
        require(np.linalg.eigvalsh(gg).min()>0, "positive_full_coframe")
        require(abs(np.trace(gg)-trace0)<1e-12, "matter_shell_trace_constant")
        require(abs(np.linalg.det(gg)-det0)<1e-14, "lorentz_volume_constant")
    second=(total(gp)+total(gm)-2*total(G0))/(t*t)
    require(second>0 and abs(second-Hessian)<0.5, "finite_second_difference")
    finite_controls.append((t,second))

# Smooth continuum for alpha_L=p^2/(128 L^2), m_L=256 L^2, beta fixed.
# Subtract only FIELD-INDEPENDENT terms (log C_L)/beta and
# -16*M*L^4*log(1-zeta); the nonconstant remainder is:
# F_inf=log(16 sum K)/beta-16*M*sum log(1+(zeta/(1-zeta))*K).
# At the symmetric G0 and this V, sum K*lambda' = 0 by permutation symmetry.
def limit_Hessian(cutoff):
    ks=np.array(list(product(range(-cutoff,cutoff+1),repeat=4)),dtype=np.float64)
    k2=np.sum(ks*ks,axis=1);ksum=np.sum(ks,axis=1)
    ell=(2*np.pi)**2
    lamb=ell*(b*k2+O*ksum*ksum)
    qv=ell*((ks[:,0]-ks[:,1])**2/2-(ks[:,0]+ks[:,1]-2*ks[:,2])**2/6)
    rv=ell*(s2/3)*(ksum*ksum-k2)
    K=np.exp(-BETA*lamb)
    den=1-ZETA+ZETA*K
    T=np.sum(K)
    Bsum=np.dot(K,qv)
    require(abs(Bsum)<1e-9, "continuum_permutation_cancellation")
    Csum=np.dot(K,qv*qv)
    Dsum=np.dot(K,rv)
    Hess= BETA*(Csum/T-(Bsum/T)**2)-Dsum/T
    Hess+=16*M*BETA*ZETA*np.sum(K*rv/den)
    Hess-=16*M*BETA**2*ZETA*(1-ZETA)*np.sum(K*qv*qv/den**2)
    return Hess,16*T

Hinf5,Zinf5=limit_Hessian(5)
Hinf6,Zinf6=limit_Hessian(6)
require(abs(Hinf6-Hinf5)<1e-6 and 60<Hinf6<80, "continuum_nonzero")

# Analytic tail domination: b > .059 and beta(2*pi)^2*b > 1.7.
# For x=||k||^2, x exp(-1.7x), x^2 exp(-1.7x) <= exp(-0.85x).
# Omitted |k_i|>=6 has T<=8*3^3*exp(-.85*36)/(1-exp(-.85*13))
# < 432 exp(-30) < 4.1e-11. Then absolute tails of sums
# K, Kq, Kq^2, Kr are below T, 40T, 1600T, 6400T,
# with ||V||=1 and ||G2||<160; the expression's total tail error <0.001.
require(BETA*(2*np.pi)**2*b>1.7 and abs(s2)<160, "Gaussian_majorant")
tail=8*27*math.exp(-.85*36)/(1-math.exp(-.85*13))
require(tail<4.1e-11 and 6400*tail<3e-7, "Gaussian_tail_bound")

report={
 "scope":"unchanged conditional v8 action; not D0 physical admission or GR closure",
 "carriers":{"lattice_sites":L**4,"fock_grades":16,"reference":128,"record_power":MPOWER},
 "root":{"d":D,"o":O,"a":a,"b":b,"Z":Z0,"beta":BETA,"Hessian_affine_tracefree":Hessian,"strict_analytic_lower_bound":Lower,"Ey2":Ey2},
 "path":{"trace_fixed":True,"determinant_fixed":True,"shell_matter_fixed":True,"Lorentz_Ricci_zero":True,"Levi_Civita_and_torsion_zero":True,"IFT_s_second":s2,"central_differences":[{"t":t,"Hessian":h} for t,h in finite_controls]},
 "refinement":{"fixed_beta_and_M_z":True,"Hessian_cutoff5":Hinf5,"Hessian_cutoff6":Hinf6,"limit_shape_source_nonzero":True,"Gaussian_tail_majorant":tail,"conservative_total_Hessian_error_bound":0.001},
 "decision":"v8 H+J+R not equal to EH+cosmological+existing R on whole admitted flat-constant family; physical GR completion remains open",
 "checks":"PASS"
}
text=json.dumps(report,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n'
(HERE/'RESULT.json').write_text(text,encoding='utf-8')
print(text,end='')
