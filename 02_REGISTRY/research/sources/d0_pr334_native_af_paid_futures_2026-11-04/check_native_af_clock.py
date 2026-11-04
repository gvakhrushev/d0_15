"""Full growing clock of the literal AF cut; eigenvalues are diagnostics.

Exact dimensions, return and conjugacy are proved in the companion text.
No homogeneous-clock substitution, physical Info choice or GR closure.
"""
import json
import numpy as np

checks = []
def need(ok, label):
    if not bool(ok):
        raise RuntimeError(label)
    checks.append(label)

p = (np.sqrt(5.)-1)/2
a = np.sqrt(p)
beta = 2*p*p
zeta = 2.**-20
v = np.array([a,p])
G = np.array([[a,-p],[p,a]])
G4 = np.linalg.matrix_power(G,4)
U = np.zeros((8,8))
for q in range(4):
    for i in range(2):
        for j in range(2):
            U[4*i+q,4*j+q] = (np.eye(2) if q == 0 else G4)[i,j]
J0 = np.kron(np.eye(2),v[:,None])
J1 = np.kron(np.eye(4),v[:,None])
dims = [2,4]+[8]*32
off = np.cumsum([0]+dims)
Dsmall = int(off[-1])
R = np.zeros((Dsmall,8))
R[:2] = (J1@J0).T
R[2:6] = (np.eye(4)-J0@J0.T)@J1.T
R[6:14] = np.eye(8)-J1@J1.T
T = np.zeros((Dsmall,Dsmall))
for j in range(len(dims)-1):
    leg = J0 if j == 0 else J1 if j == 1 else np.eye(8)
    T[off[j+1]:off[j+2],off[j]:off[j+1]] = leg
T[:,-8:] += R@U
need(Dsmall == 262 and len(dims) == 34, 'true reduced stage dimensions')
need(np.linalg.norm(R.T@R-np.eye(8)) < 2e-14, 'complete birth closing isometry')
need(np.linalg.norm(T.T@T-np.eye(Dsmall)) < 2e-13, 'whole reduced clock numerical unitarity')
E0=(J1@J0)@(J1@J0).T
E1=J1@(np.eye(4)-J0@J0.T)@J1.T
E2=np.eye(8)-J1@J1.T
need(np.linalg.norm(E0+E1+E2-np.eye(8)) < 2e-14, 'all birth details retained')
need(np.linalg.norm(U@E0-E0@U)>0.1, 'endpoint really mixes birth layers')
# Elimination of the unequal-delay legs, checked away from the spectrum.
def logdet_pivoted(A):
    A=np.array(A,dtype=complex,copy=True)
    value=0j
    for k in range(len(A)):
        row=k+int(np.argmax(np.abs(A[k:,k])))
        if abs(A[row,k])<1e-10:
            raise RuntimeError('unexpected small secular-check pivot')
        if row!=k:
            A[[k,row]]=A[[row,k]]
            value+=1j*np.pi
        value+=np.log(A[k,k])
        A[k+1:,k+1:]-=np.outer(A[k+1:,k]/A[k,k],A[k,k+1:])
    return value
for lam in (1.2, 1.1+0.3j):
    lg=logdet_pivoted(lam*np.eye(Dsmall)-T)
    ld=logdet_pivoted(np.eye(8)-U@(lam**-34*E0+lam**-33*E1+lam**-32*E2))
    ratio=np.exp(lg-ld-Dsmall*np.log(complex(lam)))
    need(abs(ratio-1)<2e-11,'full unequal-age secular identity '+str(lam))

ev=np.linalg.eigvals(T)
need(np.max(np.abs(np.abs(ev)-1))<3e-14,'all262 clock eigenvalues on unit circle diagnostically')
need(np.count_nonzero(np.abs(ev-1)<1e-11)==2,'two reduced constant clock modes')
x=ev.real
parts=np.array([9.,11.,13.]); co=1/(35-parts)
small=np.zeros((len(x),3,3))
for i in range(3):
    small[:,i,i]=1-2*x*co[i]
    for j in range(i):
        small[:,i,j]=small[:,j,i]=-np.sqrt(parts[i]*parts[j]*co[i]*co[j])
active=np.exp(-beta*np.linalg.eigvalsh(small)).sum(axis=1)
active+=np.sum((parts-1)*np.exp(-beta*(1-2*x[:,None]*co)),axis=1)
D=8*Dsmall
full=425*D
offset=359*D
nullity=offset+32
Z=offset+16*float(active.sum())
H=np.log(Z)/beta
c4=2*p**6-1
h=p**4+p**2+2*p**3*c4
J=-16*np.log1p(-zeta*(1-h))
need(D==2096 and full==890800 and offset==752464 and nullity==752496,
     'all spectator and harmonic multiplicities retained')
Zlower=nullity+(full-nullity)*np.exp(-2*beta)
need(Zlower<=Z<=full,'full heat lies inside exact analytic enclosure')
need(abs(H-(np.log(Z/8)/beta+np.log(8)/beta))<1e-13,
     'absolute spectator heat anchor retained')
ell=-np.log(p)
af=p*p*((1+c4)*np.log1p(c4)+(1-c4)*np.log1p(-c4))/ell
Ac=p*p*np.log((1+c4)/(1-c4))/ell
Auu=p*p*(1-c4*c4)/abs(c4)*np.log((1+abs(c4))/(1-abs(c4)))/ell
print(json.dumps({
    'status':'PASS','checks':checks,
    'exact_counts':{'calls':32,'births':2,'N':34,'D':D,'input_rank':16,
                    'full_Hodge_modes':full,'harmonic_offset':offset,'total_Hodge_nullity':nullity},
    'diagnostics_not_interval_certificate':{k:format(val,'.14g') for k,val in {
        'c4':c4,'cold_squared_gain_h':h,'H_lower':np.log(Zlower)/beta,
        'H':H,'H_upper':np.log(full)/beta,'J':J,'H_plus_J':H+J,
        'AF_code_Cost':2+p**3,'AF_operator_Cost_minus_Info_at_u0':af,
        'AF_source_dc':Ac,'AF_preparation_Hessian_uu':Auu}.items()},
    'scope':{'physical_Info_selected':False,'code_cost_is_primitive_cost':False,
             'native_smooth_angle_lift_proved':False,'GR_closed':False}},indent=2,sort_keys=True))
