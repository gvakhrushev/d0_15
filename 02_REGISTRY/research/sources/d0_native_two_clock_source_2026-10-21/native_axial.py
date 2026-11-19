from __future__ import annotations
import numpy as np

P=(np.sqrt(5.)-1)/2
ELL=np.log(1/P)
ORDER=(0,2,3,1)
I=np.eye(16,dtype=complex)

def popcount(x): return bin(int(x)).count("1")

def adj(a): return a.conj().T

def creators():
    out=[]
    for role in range(4):
        c=np.zeros((16,16),complex)
        earlier=ORDER[:ORDER.index(role)]
        for s in range(16):
            if not (s>>role)&1:
                c[s|(1<<role),s]=(-1)**sum((s>>j)&1 for j in earlier)
        out.append(c)
    return out

def native_axial(L:int, a:float):
    h=1./L; nu=h*a
    if not (L>=4 and 0<nu<1): raise ValueError('strict original axial chart')
    c=creators(); b=np.sqrt(1-nu*nu)
    phases=(np.exp(2j*np.pi*h),1.,1.,1.)
    words=[]; jets=[]
    for r in range(4):
        fixed=nu*c[r]; dfixed=h*c[r]
        x=fixed*phases[r]; dx=dfixed*phases[r]
        # Genuine left and right Julia defects on this exact partial isometry.
        left=I-nu*nu/(1+b)*(c[r]@adj(c[r]))
        right=I-nu*nu/(1+b)*(adj(c[r])@c[r])
        dl=-nu*h/b*(c[r]@adj(c[r])); dr=-nu*h/b*(adj(c[r])@c[r])
        for w,dw in zip(((x,left),(adj(x),right),(-fixed,-left),(-adj(fixed),-right)),
                        ((dx,dl),(adj(dx),dr),(-dfixed,-dl),(-adj(dfixed),-dr))):
            words.extend((w,w)); jets.extend((dw,dw))
    ns=[]; dns=[]
    for label in range(32):
        signs=[(-1)**(popcount(label&j)%2) for j in range(32)]
        for coeff in range(2):
            ns.append(sum((sg*words[j][coeff] for j,sg in enumerate(signs)),np.zeros_like(I))/32)
            dns.append(sum((sg*jets[j][coeff] for j,sg in enumerate(signs)),np.zeros_like(I))/32)
    aa=ns[0]; daa=dns[0]
    k=[]; dk=[]
    for j,x in enumerate(ns):
        shared=adj(x)@aa
        ds=adj(dns[j])@aa+adj(x)@daa
        k.extend(((I if j==0 else np.zeros_like(I))-2*P**2*shared,-2*P*np.sqrt(P)*shared))
        dk.extend((-2*P**2*ds,-2*P*np.sqrt(P)*ds))
    w=4*np.sin(np.pi*h)**2
    d=16*aa/h; dd=16*daa/h
    lam=nu*nu*w/(h*h)
    uu=d/np.sqrt(lam)
    beta=c[0]+adj(c[0]); eta=1j*(c[0]-adj(c[0]))
    perp=np.cos(np.pi*h)*beta+np.sin(np.pi*h)*eta
    maj=[uu,perp]
    for r in range(1,4): maj.extend((c[r]+adj(c[r]),1j*(c[r]-adj(c[r]))))
    paulis=[]
    for s in range(256):
        prod=I.copy(); degree=popcount(s)
        for j in range(8):
            if s>>j&1: prod=prod@maj[j]
        paulis.append((1j)**(degree*(degree-1)//2)*prod)
    return dict(K=np.array(k),dK=np.array(dk),N=np.array(ns),dN=np.array(dns),D=d,dD=dd,
                Delta=lam*I,lambda_=lam,U=uu,majoranas=maj,paulis=paulis,
                h=h,nu=nu,b=b,q=P*P*nu*nu*w/64)

def superop(k):
    return sum((np.kron(x.conj(),x) for x in k),np.zeros((256,256),complex))

def choi(t):
    out=t.reshape(16,16,16,16,order='F').transpose(2,0,3,1).reshape(256,256)
    return (out+adj(out))/2

def entropy(a):
    vals=np.linalg.eigvalsh((a+adj(a))/2)
    if vals.min()<-1e-9: raise ArithmeticError('nonpositive state')
    pos=vals[vals>1e-14]
    return -float(pos@np.log(pos))/ELL

if __name__=='__main__':
    f=native_axial(4,2.4); t=superop(f['K']); q=f['q'];b=f['b'];nu=f['nu']
    print('complete',np.linalg.norm(sum(adj(k)@k for k in f['K'])-I))
    print('D2',np.linalg.norm(f['D']@f['D']-f['Delta']))
    err=[]
    for s,x in enumerate(f['paulis']):
        k=popcount(s); o=sum(popcount((s>>(2*r))&3)==1 for r in range(4));u=(-1)**(k-(s&1))
        ts=(1+b)**2/4+nu*nu/16*(-1)**k*(8-2*k)+(1-b)**2/16*(4-2*o)
        ms=1-q+q*u*ts
        img=(t@x.reshape(-1,order='F')).reshape(16,16,order='F')
        err.append(np.linalg.norm(img-ms*x))
    print('eigenmax',max(err),'q',q,'entropy2',entropy(choi(t@t)/16))
