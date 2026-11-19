"""Exact terminal-channel secant and two-copy source-equivalence bound.

The native marked clock, gate order and intermediate Book03 cost are not
represented by this terminal-only channel and require separate accounting.
"""
import json
import math
import numpy as np
from check_clock_coherence import mm
p=(math.sqrt(5)-1)/2;a=math.sqrt(p);ap=a*p;theta=math.asin(p)
G=np.array([[a,-p],[p,a]]);Z=np.diag([1.,-1.]);J=np.array([[0.,-1.],[1.,0.]])
v=np.array([a,p]);I=np.eye(2)
def cnot(control,target,n):
    M=np.zeros((1<<n,1<<n))
    for j in range(1<<n):
        bits=[(j>>(n-1-i))&1 for i in range(n)]
        if bits[control]:bits[target]^=1
        out=sum(b<<(n-1-i) for i,b in enumerate(bits));M[out,j]=1
    return M
# Input old P -> P,H with independent v and actual CX(P,H).
V=mm(cnot(0,1,2),np.kron(I,v.reshape(2,1)))
# Common actual NC1 acting P,H -> P,H,A, with flag and physical tail retained.
A=mm(cnot(1,2,3),np.kron(np.kron(I,I),G),cnot(1,2,3),np.kron(np.eye(4),v.reshape(2,1)))
P0=np.diag([int(((j>>1)&1)==0) for j in range(8)])
P1=np.diag([int(((j>>1)&1)==1 and (j&1)==0) for j in range(8)])
Pd=np.diag([int(((j>>1)&1)==1 and (j&1)==1) for j in range(8)])
Kbase=[mm(P0,A),mm(P1,A)];assert np.linalg.norm(mm(Pd,A))<1e-13
rotJ=np.kron(I,J)
K0=[mm(K,V) for K in Kbase];Kd=[mm(K,rotJ,V) for K in Kbase]

def apply(Ks,X):
    out=np.zeros((16,16),complex)
    for i,K in enumerate(Ks):out[8*i:8*i+8,8*i:8*i+8]=mm(K,X,K.conj().T)
    return out

def deriv(X):
    out=np.zeros((16,16),complex)
    for i,(K,D) in enumerate(zip(K0,Kd)):
        out[8*i:8*i+8,8*i:8*i+8]=mm(D,X,K.conj().T)+mm(K,X,D.conj().T)
    return out

def trace_norm(X):return float(np.abs(np.linalg.eigvalsh((X+X.conj().T)/2)).sum())
rng=np.random.default_rng(19407)
res=[]
for q,mturn in ((19,2),(66,7),(613,65)):
    eps=q*theta-2*math.pi*mturn
    # Two matched native words W+W+, W-W- on H, numerical matrix products.
    Gq=np.linalg.matrix_power(G,q);wp=Z@Z@Gq;wm=Z@Gq@Z
    def make(U):return [mm(K,np.kron(I,U),V) for K in Kbase]
    Kp=make(wp@wp);Km=make(wm@wm)
    delta=2*ap*math.sin(4*eps)
    maxerr=0.
    # Matrix units prove equality on arbitrary complex input by linearity.
    for i in range(2):
        for j in range(2):
            X=np.zeros((2,2),complex);X[i,j]=1
            got=(apply(Kp,X)-apply(Km,X))/delta
            want=deriv(X)/(2*ap)
            maxerr=max(maxerr,float(np.max(np.abs(got-want))))
    assert maxerr<1e-9
    # Two programmes, arbitrary potentially entangled joint input. The four
    # actual record blocks are retained, not combined into marginal flags.
    v4=rng.normal(size=4)+1j*rng.normal(size=4);v4/=np.linalg.norm(v4)
    rho=np.outer(v4,v4.conj());outp=np.zeros((256,256),complex);outm=outp.copy();limit=outp.copy()
    for h1 in range(2):
        for h2 in range(2):
            pos=64*(2*h1+h2);sl=slice(pos,pos+64)
            Cp=np.kron(Kp[h1],Kp[h2]);Cm=np.kron(Km[h1],Km[h2]);C=np.kron(K0[h1],K0[h2])
            D=np.kron(Kd[h1],K0[h2])+np.kron(K0[h1],Kd[h2])
            outp[sl,sl]=mm(Cp,rho,Cp.conj().T);outm[sl,sl]=mm(Cm,rho,Cm.conj().T)
            limit[sl,sl]=(mm(D,rho,C.conj().T)+mm(C,rho,D.conj().T))/(2*ap)
    err=trace_norm((outp-outm)/delta-limit)
    bound=4*math.sin(2*eps)**2/ap  # general m=2, odd k>=3 term empty
    assert err<=bound+1e-10
    u=math.sin(2*eps)**2;ss=abs(math.sin(4*eps));m16=(2*16*15*u+sum(math.comb(16,k)*ss**(k-1) for k in range(3,17,2)))/ap
    res.append({'q':q,'epsilon':eps,'delta_q':delta,'m16_diamond_bound':m16,'matrix_unit_max_error':maxerr,
                'two_copy_actual_error_trace':err,'two_copy_diamond_bound':bound})
# First-source test: arbitrary entangled old RIGHT, real trace-norm tangent
# and bounded terminal observable. Equality is differentiated exactly.
z=rng.normal(size=6)+1j*rng.normal(size=6);z/=np.linalg.norm(z);rho=np.outer(z,z.conj())
x=rng.normal(size=(6,6))+1j*rng.normal(size=(6,6));X=(x+x.conj().T)/2;X-=np.trace(X)*np.eye(6)/6
O=rng.normal(size=(48,48))+1j*rng.normal(size=(48,48));O=(O+O.conj().T)/2
q=66;eps=q*theta-2*math.pi*7;U=np.linalg.matrix_power(G,q);wp=Z@Z@U;wm=Z@U@Z
Kp=[np.kron(mm(K,np.kron(I,wp@wp),V),np.eye(3)) for K in Kbase]
Km=[np.kron(mm(K,np.kron(I,wm@wm),V),np.eye(3)) for K in Kbase]
Kc=[np.kron(K,np.eye(3)) for K in K0];Dc=[np.kron(K,np.eye(3)) for K in Kd]
def apply48(Ks,X):
    out=np.zeros((48,48),complex)
    for i,K in enumerate(Ks):out[24*i:24*i+24,24*i:24*i+24]=mm(K,X,K.conj().T)
    return out
def der48(X):
    out=np.zeros((48,48),complex)
    for i,(K,D) in enumerate(zip(Kc,Dc)):
        out[24*i:24*i+24,24*i:24*i+24]=mm(D,X,K.conj().T)+mm(K,X,D.conj().T)
    return out
step=2*ap*math.sin(4*eps)
left=np.trace(mm(O,(apply48(Kp,X)-apply48(Km,X))/step))
right=np.trace(mm(O,der48(X)/(2*ap)))
assert abs(left-right)<1e-9
# Analytic constants for 16-copy bound.
print(json.dumps({'status':'PASS','one_copy_exact_normalized_channel':'B/(2ap)',
 'B':'M([J,V (.) V*])','B_diamond_upper':2,'A_diamond_upper':2,
 'm_copy_diamond_remainder':'[2m(m-1)sin^2(2eps)+sum_{odd k>=3} C(m,k)|sin(4eps)|^(k-1)]/(ap)',
 'one_copy_source_old_RIGHT_identity_error':abs(left-right),
 'actual_mixed_2copy_error_is_below_analytic_diamond_bound':True,
 'matched_physical_cut':'same seed old input and complete terminal NC1 CQ output',
 'full_marked_clock_preparation_gate_prices_included':False,
 'actual_total_Gamma_and_GR_source_derived':False,'GR_closed':False,'examples':res},indent=2))
