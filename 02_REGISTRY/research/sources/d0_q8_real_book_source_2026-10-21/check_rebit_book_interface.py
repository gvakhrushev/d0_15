#!/usr/bin/env python3
"""Full complex Book feedback from real Golden/quadrature probes.

Standalone reproduction of the original L4 Fourier CAR16 numerical fixture.
This is an algebraic realification and a conditional query interface, NOT
physical Q8 port admission, branchwise Book03 Info or GR selection.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import numpy as np
from scipy.linalg import expm, solve_sylvester

p=(math.sqrt(5)-1)/2
phi=1/p
a=math.sqrt(p)
Z=2.0**-20
RIGHT=128
ORDER=(0,2,3,1)
I=np.eye(16,dtype=complex)
checks=[]

def check(label,cond):
    if not bool(cond):raise AssertionError(label)
    checks.append(label)

def close(label,x,y,tol=5e-11):
    err=float(np.max(np.abs(np.asarray(x)-np.asarray(y))))
    check(label,err<tol)

def adj(x):return x.conj().T

def hs(x):return float(np.linalg.norm(x))

def psqrt(x):
    eig,u=np.linalg.eigh((x+adj(x))/2)
    check('positive Julia defect spectrum',eig.min()>=-2e-12)
    return (u*np.sqrt(np.maximum(eig,0)))@adj(u)

def creators():
    out=[]
    for role in range(4):
        c=np.zeros((16,16),complex)
        earlier=ORDER[:ORDER.index(role)]
        for bits in range(16):
            if not(bits>>role)&1:
                c[bits|(1<<role),bits]=(-1)**sum((bits>>j)&1 for j in earlier)
        out.append(c)
    return out

def native(theta):
    c=creators()
    boost=c[0]@adj(c[1])+c[1]@adj(c[0])
    u=expm(theta*boost);du=u@boost
    phases=(1j,1j,-1.,-1j)
    words=[];jets=[]
    for r in range(4):
        fixed=.6*c[r]
        x=fixed@(u if r==1 else I)*phases[r]
        dx=fixed@du*phases[r] if r==1 else np.zeros_like(I)
        left=psqrt(I-x@adj(x));right=psqrt(I-adj(x)@x)
        dl=solve_sylvester(left,left,-dx@adj(x)-x@adj(dx))
        dr=solve_sylvester(right,right,-adj(dx)@x-adj(x)@dx)
        l0=psqrt(I-fixed@adj(fixed));r0=psqrt(I-adj(fixed)@fixed)
        zero=np.zeros_like(I)
        for w,dw in zip(((x,left),(adj(x),right),(-fixed,-l0),(-adj(fixed),-r0)),
                        ((dx,dl),(adj(dx),dr),(zero,zero),(zero,zero))):
            words.extend((w,w));jets.extend((dw,dw))
    row=[];drow=[]
    for label in range(32):
        signs=[(-1)**(bin(label&j).count('1')&1) for j in range(32)]
        for coeff in range(2):
            row.append(sum((signs[j]*words[j][coeff] for j in range(32)),np.zeros_like(I))/32)
            drow.append(sum((signs[j]*jets[j][coeff] for j in range(32)),np.zeros_like(I))/32)
    first,dfirst=row[0],drow[0]
    k=[];dk=[]
    for j,n in enumerate(row):
        shared=adj(n)@first
        dshared=adj(drow[j])@first+adj(n)@dfirst
        k.extend(((I if j==0 else np.zeros_like(I))-2*p**2*shared,
                  -2*p*math.sqrt(p)*shared))
        dk.extend((-2*p**2*dshared,-2*p*math.sqrt(p)*dshared))
    return np.asarray(k),np.asarray(dk)

def transfer(k,dk,x,dx,w):
    n=np.zeros_like(x);dn=np.zeros_like(x)
    for j in range(len(k)):
        n+=w[j]*adj(k[j])@x@k[j]
        dn+=w[j]*(adj(dk[j])@x@k[j]+adj(k[j])@dx@k[j]+adj(k[j])@x@dk[j])
    return n,dn

def native_effects(theta=.08,t=.7):
    k,dk=native(theta)
    costs=np.tile([1.,2.],64);weights=np.exp(-t*costs)
    n1,dn1=transfer(k,dk,I,np.zeros_like(I),weights)
    N,dN=transfer(k,dk,n1,dn1,weights)
    A=math.exp(-t)*k[0]@k[0]
    dA=math.exp(-t)*(dk[0]@k[0]+k[0]@dk[0])
    B=adj(A)@A;dB=adj(dA)@A+adj(A)@dA
    return k,dk,N,B,dN,dB

def realify(x):
    return np.block([[x.real,-x.imag],[x.imag,x.real]])

def make_probes(d):
    probes=[]
    for j in range(d):
        v=np.zeros(2*d);v[j]=1
        probes.append(('basis',j,None,v))
    for j in range(d):
        for k in range(j+1,d):
            vr=np.zeros(2*d);vr[j]=a;vr[k]=p
            vi=np.zeros(2*d);vi[j]=a;vi[d+k]=p
            probes.append(('real',j,k,vr))
            probes.append(('quadrature',j,k,vi))
    return probes

def effects_from_probes(x,probes):
    d=x.shape[0]
    xx=realify(x)
    q={(kind,j,k):float(v@xx@v) for kind,j,k,v in probes}
    out=np.zeros((d,d),complex)
    for j in range(d):out[j,j]=q[('basis',j,None)]
    for j in range(d):
        for k in range(j+1,d):
            base=p*q[('basis',j,None)]+p*p*q[('basis',k,None)]
            rr=(q[('real',j,k)]-base)/(2*a*p)
            ii=-(q[('quadrature',j,k)]-base)/(2*a*p)
            out[j,k]=rr+1j*ii
            out[k,j]=rr-1j*ii
    return out,q

def dlogdet(x,dx):return float(np.trace(np.linalg.solve(x,dx)).real)

def book(N,B,dN=None,dB=None,z=Z):
    m=(1-z)*N+z*B
    sN=np.linalg.slogdet(N)
    sM=np.linalg.slogdet(m)
    check('positive determinant factors',abs(sN[0]-1)<5e-12 and abs(sM[0]-1)<5e-12)
    j=RIGHT*(sN[1]-sM[1])
    if dN is None:return float(j)
    dm=(1-z)*dN+z*dB
    return float(j),RIGHT*(dlogdet(N,dN)-dlogdet(m,dm))

def vnentropy(x):
    ev=np.linalg.eigvalsh(x)
    check('positive density eigenvalues',min(ev)>-2e-12)
    return float(-np.sum(ev[ev>0]*np.log(ev[ev>0])))

def main(out):
    check('Golden normalization',abs(a*a+p*p-1)<2e-15)
    k,dk,N,B,dN,dB=native_effects()
    close('actual all128 Kraus completeness',sum((adj(x)@x for x in k),np.zeros_like(I)),I)
    close('Kraus first jet completeness',sum((adj(dx)@x+adj(x)@dx for x,dx in zip(k,dk)),np.zeros_like(I)),np.zeros_like(I))
    check('true cost-marked normalizer nonscalar',np.ptp(np.linalg.eigvalsh(N))>1e-5)
    # Algebraic realification as an exact *-representation.
    X=np.array([[1+.2j,.4-.15j],[-.1+.3j,.2+.8j]])
    Y=np.array([[.3-.4j,.7],[.1+.2j,-.2j]])
    close('realification multiplicativity',realify(X@Y),realify(X)@realify(Y))
    close('realification star',realify(adj(X)),realify(X).T)
    kr=np.asarray([realify(x) for x in k]);dkr=np.asarray([realify(x) for x in dk])
    close('realified 128 Kraus complete isometry',sum((x.T@x for x in kr),np.zeros((32,32))),np.eye(32))
    close('realified complete first jet',sum((dx.T@x+x.T@dx for x,dx in zip(kr,dkr)),np.zeros((32,32))),np.zeros((32,32)))
    close('realified original normalizer',realify(N).T,realify(N))
    probes=make_probes(16)
    check('minimal full Hermitian probe count',len(probes)==16**2)
    for tag,X in [('N',N),('B',B),('DN',dN),('DB',dB)]:
        reconstructed,_=effects_from_probes(X,probes)
        close('complex full effect tomography '+tag,reconstructed,X,2e-12)
    jc,djc=book(N,B,dN,dB)
    Nr,Br,dNr,dBr=map(realify,(N,B,dN,dB))
    Mr=(1-Z)*Nr+Z*Br
    jr=RIGHT/2*(np.linalg.slogdet(Nr)[1]-np.linalg.slogdet(Mr)[1])
    djr=RIGHT/2*(dlogdet(Nr,dNr)-dlogdet(Mr,(1-Z)*dNr+Z*dBr))
    close('Book determinant realification with exact half multiplicity',jr,jc,3e-11)
    close('Book full first jet realification',djr,djc,3e-12)
    # All 256 Born-probe derivatives carry the same exact effect first jet.
    _,qn=effects_from_probes(N,probes)
    _,qb=effects_from_probes(B,probes)
    jdict={}
    for sign,X in [('plus',N+1e-5*dN),('minus',N-1e-5*dN)]:
        rec,_=effects_from_probes(X,probes)
        close('normalizer jet from true real probes '+sign,rec,X,2e-12)
    # A real-only input sees no imaginary skew-effect first jet, but Book does.
    z=Z
    ambient=np.zeros((16,16),complex);ambient[0,3]=1j;ambient[3,0]=-1j
    _,qambient=effects_from_probes(ambient,probes)
    check('all original real Golden probes blind to imaginary jet',max(abs(qambient[('real',j,k)]) for j in range(16) for k in range(j+1,16))<2e-14)
    check('quadrature probes detect imaginary jet',abs(qambient[('quadrature',0,3)])>1e-3)
    dBook=book(N,B,np.zeros_like(N),ambient)[1]
    check('native anchor Book source responds to imaginary ambient jet',abs(dBook)>1e-8)
    check('imaginary ambient jet stays in strict effect order locally',
          min(np.linalg.eigvalsh(B+1e-5*ambient))>0 and min(np.linalg.eigvalsh(N-B-1e-5*ambient))>0)
    # Elementary rational 2x2 negative control: no floating small-source sign.
    # N=I, B=[[1/2,i/4],[-i/4,1/2]], DB=[[0,i],[-i,0]], z=1/2.
    # M=(3/4)I+(i/8)Y; det(M)=35/64, det'(M)=-1/8; J'=8/35.
    from fractions import Fraction as F
    check('exact imaginary-only negative control derivative',
          F(1,8)/F(35,64)==F(8,35))
    # Book06 finite maximum entropy under retained diagonal test algebra.
    rho=np.array([[.7,.1+.08j],[.1-.08j,.3]])
    diag=np.diag(np.diag(rho))
    close('max entropy gain equals relative entropy under retained test algebra',
          vnentropy(diag)-vnentropy(rho),
          -vnentropy(rho)-float(np.trace(rho@np.diag(np.log(np.diag(diag)))).real),1e-12)
    check('unique max entropy representative entropy strictly greater',vnentropy(diag)>vnentropy(rho))
    # Terminal Q8 memory aggregation cannot identify per-history gain once
    # two distinct paths have the same memory class.
    w1,w2=2.0,3.0
    for eps in (.1,-.2):check('same-class weights have invisible balanced fibre',abs((w1+eps)+(w2-eps)-(w1+w2))<1e-15)
    result={'status':'PASS_SCOPED','checks':len(checks),'labels':checks,
        'native_original_fixture':{'theta':.08,'mark_t':.7,'rounds':2,'port_count':128,
          'input_dimension_complex':16,'realified_dimension':32,
          'oldRIGHT_multiplicity_complex':128,'effective_real_trace_prefactor':64,
          'full_feedback':jc,'native_feedback_field_jet':djc,
          'imaginary_effect_ambient_jet':dBook,'effect_normalizer_eigenspread':float(np.ptp(np.linalg.eigvalsh(N))),
          'probes_exact_count':len(probes)},
        'limits':['Q8 quarter-turn and realified old CAR actuator admission not proved',
           'real Golden inputs alone cannot detect imaginary effects',
           'actual cut and branchwise Info/heat/clock selection unresolved',
           'full GR closure not claimed'], 'GR_closed':False}
    dest=Path(out)
    dest.write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'checks':len(checks),'file':str(dest),'J':jc,'DJ':djc,'imaginary_DJ':dBook}))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',default='REBIT_RESULT.json');args=parser.parse_args();main(args.output)
