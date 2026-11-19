"""Exact integer a posteriori Perron/source enclosure on the physical NT3 fugacity."""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import contextlib,io,runpy,json,sys,hashlib
import numpy as np
import sympy as sp
from scipy.linalg import eig, inv
from itertools import combinations

default=Path(__file__).resolve().parent.parent/"frozen"/"check_full128_cq_coframe_residual.py"
owner=Path(sys.argv[1]) if len(sys.argv)>1 else default
assert hashlib.sha256(owner.read_bytes()).hexdigest()=="2ac8b4202c0212cf19a66c0a8940680cf94a405bdd99f2466936076faa7e9d66"
with contextlib.redirect_stdout(io.StringIO()): b=runpy.run_path(str(owner))
ns,dns,a,da=[b[k] for k in ("ns","dns","a","da")]
G=[(m.H*a).applyfunc(sp.expand) for m in ns[1:]]
DG=[(dm.H*a+m.H*da).applyfunc(sp.expand) for m,dm in zip(ns[1:],dns[1:])]
n=16
N=n*n
pairs=list(combinations(range(n),2))
ip=[i+n*j for i,j in pairs]
im=[j+n*i for i,j in pairs]
diag=[i*(n+1) for i in range(n)]
metric=np.array([1]*16+[2]*(N-16),dtype=np.int64)
def addherm(re,iv):
    a=np.concatenate((re[:,diag],re[:,ip]+re[:,im],iv[:,im]-iv[:,ip]),axis=1)
    b=np.concatenate((iv[:,diag],iv[:,ip]+iv[:,im],re[:,ip]-re[:,im]),axis=1)
    assert not np.any(b[diag])
    return np.concatenate((a[diag],a[ip],b[ip]))
def gaussian(m,scale):
    m=(scale*m).applyfunc(sp.expand)
    assert all(sp.re(z).is_Integer and sp.im(z).is_Integer for z in m)
    return (np.array(m.applyfunc(sp.re).tolist(),dtype=np.int64),
            np.array(m.applyfunc(sp.im).tolist(),dtype=np.int64))
def kg(a,b,c,d):
    return (np.kron(a,c)+np.kron(b,d),np.kron(a,d)-np.kron(b,c))
A=np.zeros((7,N,N),dtype=np.int64);DA=A.copy(); AT=A.copy(); DAT=A.copy()
# Also compute the independent one-period trace and the irreducibility witness.
comm_rows=np.zeros((N,N),dtype=np.int64);piv={};ident=np.eye(n,dtype=np.int64)
period=[F(0) for _ in range(7)]; period0=period.copy()
for j,(g,dg) in enumerate(zip(G,DG),1):
    if not any(g):continue
    h=bin(j).count("1")
    a,ai=gaussian(g,3200);d,di=gaussian(dg,3200*432)
    A[h]+=addherm(*kg(a,ai,a,ai))
    r1,i1=kg(a,ai,d,di);r2,i2=kg(d,di,a,ai)
    DA[h]+=addherm(r1+r2,i1+i2)
    # Direct second construction using M_j^dagger on both sides, not a transpose guess.
    ah,aih,dh,dih=a.T,-ai.T,d.T,-di.T
    AT[h]+=addherm(*kg(ah,aih,ah,aih))
    rr1,ii1=kg(ah,aih,dh,dih);rr2,ii2=kg(dh,dih,ah,aih)
    DAT[h]+=addherm(rr1+rr2,ii1+ii2)
    period0[h]+=F(int(np.trace(a)**2+np.trace(ai)**2),3200**2)
    period[h]+=F(2*int(np.trace(a)*np.trace(d)+np.trace(ai)*np.trace(di)),3200**2*432)
    if len(piv)<255:
        m=(a+10*ai)%101
        for row in np.kron(ident,m)-np.kron(m.T,ident):
            row=row.copy()
            while (ids:=np.flatnonzero(row)).size:
                k=ids[0]
                if k not in piv:
                    comm_rows[k]=row*pow(int(row[k]%101),-1,101)%101
                    piv[k]=j
                    break
                row=(row-row[k]*comm_rows[k])%101
assert len(piv)==255 and period==[F(0),F(27,2000),F(-27,2000),F(27,2000),F(-27,2000),F(0),F(0)]
SCALE=2**44
DEN=141975 # 3200^2 lambda(1-lambda)
assert DEN==3200**2*F(9,640)*(1-F(9,640))
rtlo=F(isqrt(5*10**80),10**40); rthi=rtlo+F(1,10**40)
assert rtlo**2<=5<=rthi**2
tl,tu=2/rthi,2/rtlo
def norm(a):
    assert int(np.max(np.abs(a)))*a.shape[1] < 2**62
    return int(max(np.sum(np.abs(a),axis=1)))
def rounded(mat,den):
    big=2**86; accum=np.zeros((N,N),dtype=object); err=F(N,2*SCALE)
    for h in range(7):
        lo,hi=tl**h/den,tu**h/den
        w=round((lo+hi)*big/2)
        err+=norm(mat[h])*max(abs(lo-F(w,big)),abs(hi-F(w,big)))
        accum+=mat[h].astype(object)*w
    q=np.asarray((accum*SCALE+big//2)//big,dtype=np.int64)
    return q,err
def adj(m):
    out=m.transpose(0,2,1)*metric[None,None,:]
    assert not np.any(out%metric[None,:,None])
    return out//metric[None,:,None]
assert np.array_equal(adj(A),AT) and np.array_equal(adj(DA),DAT)
vecI=np.array([1]*n+[0]*(N-n),dtype=np.int64)
for op in (A,AT):
    assert np.array_equal(sum(op)@vecI,DEN*vecI)
for op in (DA,DAT):
    assert not np.any(sum(op)@vecI)
aq,ae=rounded(A,DEN); daq,dae=rounded(DA,DEN*432)
laq,lae=rounded(AT,DEN)
fast=aq.astype(float)/SCALE
vals,ls,rs=eig(fast,left=True)
idx=int(np.argmax(vals.real))
val=float(vals[idx].real)
r=rs[:,idx].real.copy();r/=r[0]
l=ls[:,idx].real.copy()/metric;l/=l[0]
def certify(q,e,v,w):
    # All accepted inequalities below use only integers or Fractions; eigenvectors
    # and inverse approximations supplied by SciPy are untrusted dyadic proposals.
    vq=np.rint(v*SCALE).astype(np.int64); wq=int(round(w*SCALE))
    assert vq[0]==SCALE
    vnorm=F(int(np.max(np.abs(vq))),SCALE)
    res=q.astype(object)@vq.astype(object)-wq*vq.astype(object)
    f0=F(int(max(abs(t) for t in res)),SCALE**2)+e*vnorm
    jp=2**26;yp=2**16
    jfull=np.zeros((N+1,N+1),dtype=np.int64)
    jfull[:N,:N]=q-np.eye(N,dtype=np.int64)*wq
    jfull[:N,N]=-vq
    jfull[N,0]=SCALE
    # Exact rounding, ties directed upward, irrelevant to the bound.
    ji=(jfull+SCALE//(2*jp))//(SCALE//jp)
    jerr=e+F(N+1,2*jp)
    Y=np.rint(inv(jfull.astype(float)/SCALE)*yp).astype(np.int64)
    assert (N+1)*int(np.max(abs(Y)))*int(np.max(abs(ji)))<2**62
    epsI=np.eye(N+1,dtype=np.int64)*yp*jp-Y@ji
    yn=F(norm(Y),yp)
    kap=F(norm(epsI),yp*jp)+yn*jerr
    rad=F(1,10**7)
    bound=yn*f0+(kap+2*rad*yn)*rad
    assert bound<rad and kap+2*rad*yn<1,(float(f0),float(yn),float(kap),float(bound/rad))
    # Sylvester certificate R(vq/SCALE) > 16*sqrt(2)*rad I. Use 32 rad.
    gr=np.zeros((n,n),dtype=object);gi=gr.copy()
    for x in range(n):gr[x,x]=int(vq[x])
    for t,(i,j) in enumerate(pairs):
        gr[i,j]=gr[j,i]=int(vq[n+t])
        gi[i,j]=int(vq[n+len(pairs)+t]);gi[j,i]=-gi[i,j]
    # Integer realification and fraction-free LDL elimination; no eigensolver input.
    real=np.block([[gr,-gi],[gi,gr]])
    # Exact 32*rad margin (larger than the conversion from entrywise radius).
    real=real*rad.denominator-np.eye(2*n,dtype=object)*(32*rad.numerator*SCALE)
    prev=1
    for j in range(2*n):
        pivot=real[j,j];assert pivot>0
        if j+1!=2*n:
            small=(real[j+1:,j+1:]*pivot-np.outer(real[j+1:,j],real[j,j+1:]))
            assert not np.any(small%prev)
            real[j+1:,j+1:]=small//prev
            prev=pivot
    assert kap < F(1,100) and bound < rad/10
    return vq,wq,rad,dict(inverse_defect_strict_upper="1/100",coordinate_radius=str(rad),self_map_ratio_strict_upper="1/10")
rq,wq,rr,rc=certify(aq,ae,r,val)
lq,lwq,lr,lc=certify(laq,lae,l,val)
assert wq==lwq
dN=sum((lq*metric).astype(object)*(daq.astype(object)@rq.astype(object)))
N0=F(int(dN),SCALE**3)
rho=F(wq,SCALE)
r0=F(int(np.max(abs(rq))),SCALE);l0=F(int(np.max(abs(lq))),SCALE)
dS=F(norm(daq),SCALE)+dae
E=int(sum(metric))*(lr*dS*(r0+rr)+l0*(dS*rr+dae*r0))
Z0=F(int(sum((lq*metric).astype(object)*rq.astype(object))),SCALE**2)
EZ=int(sum(metric))*(lr*(r0+rr)+l0*rr)
assert Z0>EZ and N0+E<0
drav=((N0-E)/(Z0-EZ),(N0+E)/(Z0+EZ))
assert drav[0]<drav[1]<0
def outward(a,b,scale=10**9):
    return [str(F((a*scale).__floor__(),scale)),str(F((b*scale).__ceil__(),scale))]
def prod(a,b):
    uv=[x*y for x in a for y in b];return (min(uv),max(uv))
def plus(a,b):
    return (a[0]+b[0],a[1]+b[1])
def power(a,k):
    assert 0<=a[0]<=a[1];return (a[0]**k,a[1]**k)
def scal(a,k):return prod(a,(k,k))
ps=((rtlo-1)/2,(rthi-1)/2);la=F(9,640);ss=la*(1-la)
cold=plus(scal(ps,0),plus((1,1),scal(power(ps,2),-2*la)))
base=plus(prod(ps,power(cold,2)),scal(power(ps,5),4*la**2))
bright=scal(power(ps,5),8*ss)
allrate=plus(base,prod(bright,(rho-rr,rho+rr)))
ratio=prod(prod(bright,drav),(1/allrate[1],1/allrate[0]))
assert F(-149,10**6)<ratio[0]<ratio[1]<F(-147,10**6)
t=(tl,tu)
period_numer=scal(prod(prod(t,(1-tu,1-tl)),plus((1,1),power(t,2))),F(27,2000))
period_den=(F(0),F(0))
for h in range(7): period_den=plus(period_den,scal(power(t,h),period0[h]))
extra=scal(power(ps,5),8)
period_den=plus(scal(base,256),prod(extra,period_den))
periodjet=prod(prod(extra,period_numer),(1/period_den[1],1/period_den[0]))
invariant=plus(periodjet,(-ratio[1],-ratio[0]))
assert invariant[0]>F(147,10**6)
print(json.dumps(dict(status="PASS_GOLDEN_NT3_COUNTER_PRESSURE_CERTIFIED",rank=len(piv),
    actual_commuting_labels=sorted(set(piv.values())),period_coefficient_by_popcount=list(map(str,period)),rho_bright=outward(rho-rr,rho+rr),
    D_rho_bright=outward(*drav),right=rc,left=lc,actual_adjoint_verified=True,
    period0_by_popcount=list(map(str,period0)),physical_log_pressure_derivative=outward(*ratio,scale=10**11),physical_log_pressure_sign=-1,closed_one_period_jet_sign=1,log_closed_jet=outward(*periodjet,scale=10**12),gauge_invariant_jet=outward(*invariant,scale=10**11)),indent=2))
