"""Direct 256x256 operator derivatives at a nonstationary rational-Gibbs control.
This checks the full local formulas independently of the symbolic trace reduction.
It is not the L=8 root certificate.
"""
from __future__ import annotations
from itertools import product
from pathlib import Path
import json
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
L=2;N=16;sites=list(product(range(2),repeat=4));I=np.eye(16)
def creator(r):
    C=np.zeros((16,16))
    for m in range(16):
        if not(m&(1<<r)):C[m|(1<<r),m]=(-1)**((m&((1<<r)-1)).bit_count())
    return C
C=[creator(r)for r in range(4)]
def Gamma(K):return sum((K[i,j]*C[i]@C[j].T for i in range(4)for j in range(4)),np.zeros((16,16)))
T=[]
for r in range(4):
    t=np.zeros((N,N))
    for x,s in enumerate(sites):
        target=list(s);target[r]=(target[r]+1)%L
        t[x,sites.index(tuple(target))]=1
    T.append(t)
d=L*sum((np.kron(t-np.eye(N),c)for t,c in zip(T,C)),np.zeros((256,256)))
D=d+d.T;Delta=D@D
Fourier=np.array([[(-1)**sum(k[r]*x[r]for r in range(4))/4 for x in sites]for k in sites])
z=np.array([[-4*k[r]for r in range(4)]for k in sites],float)
lambda_=np.sum(z*z,axis=1)
# beta=log(2)/16: these probabilities are exact rational products.
pbeta=np.array([2.**(-sum(k)) for k in sites]);Z=pbeta.sum();pbeta/=Z
pm=np.array([.25 if sum(k)==1 else 0 for k in sites]);dw=pm-pbeta
Rd=np.kron(Fourier.T@np.diag(dw)@Fourier,I/16)
res=[]
if not np.allclose(Delta,np.kron(Fourier.T@np.diag(lambda_)@Fourier,I),atol=1e-13,rtol=0):raise AssertionError('ACTUAL_D2_FULL_SYMBOL')
M=z.T@(dw[:,None]*z)
for i in range(4):
    for j in range(i,4):
        H=np.zeros((4,4));H[i,j]=H[j,i]=1
        K=np.zeros((256,256));K[:16,:16]=Gamma(H)
        deltaD=d.T@K-K@d.T
        actual=2*np.trace(Rd@D@deltaD)
        expected=np.sum(M*H)/N
        if abs(actual-expected)>1e-12:raise AssertionError(('LOCAL_METRIC',i,j,actual,expected))
        res.append({'kind':'metric','index':[i,j],'actual':float(actual),'expected':float(expected)})
phase=np.array([[(-1)**k[r]for r in range(4)]for k in sites])
Cm=z.T@(dw[:,None]*phase)
for r in range(4):
    y=[0]*4;y[r]=1;yi=sites.index(tuple(y))
    for a in range(4):
        for b in range(4):
            K=np.zeros((4,4));K[a,b]=1
            deltad=np.zeros((256,256));deltad[:16,16*yi:16*(yi+1)]=L*C[r]@Gamma(K)
            deltaD=deltad+deltad.T
            actual=2*np.trace(Rd@D@deltaD)
            expected=L/N*np.dot(Cm[:,r],np.eye(4)[:,r]*np.trace(K)-K[:,r])
            if abs(actual-expected)>1e-12:raise AssertionError(('LOCAL_LINK',r,a,b,actual,expected))
            res.append({'kind':'linear_link','index':[r,a,b],'actual':float(actual),'expected':float(expected)})
out={'status':'PASS','dimension':256,'metric_checks':10,'linear_link_checks':64,
     'numerical_tolerance':1e-12,'underlying_control':'integer CAR/shift matrices and rational Gibbs probabilities',
     'full_heat_partition_Z':float(16*Z),'thermal_mean_energy':float(pbeta@lambda_),
     'this_point_is_stationary':False,'checks':res}
(ROOT/'results/full_local_operator_check.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS_FULL_LOCAL_OPERATOR',10,'metric',64,'link derivatives; full 256x256 D and Delta')
