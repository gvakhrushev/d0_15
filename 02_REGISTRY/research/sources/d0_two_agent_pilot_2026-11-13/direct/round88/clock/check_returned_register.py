"""Returned sharp fields, registered noisy 02 query, trace and actual square work."""
import itertools
import json
import math
from fractions import Fraction as Fr

import mpmath as mp
import numpy as np

p=(math.sqrt(5)-1)/2
a=math.sqrt(p)
v=np.array([a,p])
zero=np.array([1.,0]); one=zero[::-1]
G=np.array([[a,-p],[p,a]])
X=np.array([[0.,1],[1.,0]])
CX=np.eye(4)[[0,1,3,2]]
I2=np.eye(2)
Spin=np.array([[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0.]])
Src=np.zeros((8,8)); Src[:4,:4]=np.eye(4); Src[4:,4:]=Spin
w=2*p**3
n0=1-w
theta=math.asin(p)
z=2**-20
nu=.25


def rq(ok,msg):
    if not ok: raise ArithmeticError(msg)


def close(a,b,msg):
    rq(np.max(np.abs(np.asarray(a)-np.asarray(b)))<2e-11,msg)


def tens(*args):
    t=np.ones(1)
    for x in args: t=np.kron(t,x)
    return t.reshape((2,)*int(round(math.log2(t.size))))


def action(vec,gate):
    op=gate[0]
    mat={'G':G,'X':X,'B':I2,'C':CX,'I':Src}[op]
    axes=gate[1:]; front=np.moveaxis(vec,axes,range(len(axes)))
    out=np.einsum('ij,jr->ir',mat,front.reshape(len(mat),-1),optimize=False)
    return np.moveaxis(out.reshape(front.shape),range(len(axes)),axes)


def apply(vec,word):
    work=0.
    for gate in word:
        nxt=action(vec,gate)
        r=abs(np.vdot(vec,nxt))**2
        work+=0. if abs(1-r)<1e-12 else math.sqrt(max(0,1-r))
        vec=nxt
    return vec,work


def sw(q,r):
    return [('C',q,r),('C',r,q),('C',q,r)]


def inv(word):
    # Mechanically invert each physical G on the selected PAR=1 branch.
    out=[]
    for gate in reversed(word):
        out+=([('X',gate[1]),gate,('X',gate[1])] if gate[0]=='G' else [gate])
    return out


def sharp(q):
    return [('X',q),('G',q),('X',q)]


def nc1(head,tail):
    return [('C',head,tail),('G',tail),('C',head,tail)]


def rho(vec,ids):
    tmp=np.moveaxis(vec,ids,range(len(ids))).reshape(2**len(ids),-1)
    return tmp@tmp.T.conj()


def local_work(initial,word):
    dim=len(initial); bits=int(round(math.log2(dim))); state=initial.copy(); work=0.
    for gate in word:
        mat=np.stack([action(row.reshape((2,)*bits),gate).reshape(-1) for row in np.eye(dim)],axis=1)
        overlap=np.trace(state@mat)
        rr=abs(overlap)**2
        work+=0. if abs(1-rr)<1e-12 else math.sqrt(max(0,1-rr))
        state=mat@state@mat.T
    return state,work


def swaps(vec,ids):
    # Previous SWAPs act outside the next pair, hence leave its marginal intact.
    vv=np.outer(v,v); cost=0.
    for j in ids:
        old=rho(vec,[j])
        final,delta=local_work(np.kron(old,vv),sw(0,1))
        close(final,np.kron(vv,old),'complete SWAP to kept archive')
        cost+=delta
    return cost


def prefix(old):
    # x,y,PAR,PTAIL,PORT and two Spin bits. All other upfront births factor.
    rz=sw(2,4)+[('I',4,5,6)]*2+sw(2,4)
    raw,work=apply(tens(v,v,v,v,old),rz+[('G',2)]+rz+[('C',0,2),('C',1,2)]+nc1(2,3))
    odd=raw[:,:,1,0].reshape(4,8)
    bell=(tens(zero,one)+tens(one,zero)).reshape(-1)/math.sqrt(2)
    close(odd,math.sqrt(w)*np.outer(bell,old),'actual odd full old register')
    even=raw[:,:,0].reshape(4,2,8)
    evencoin=(p*tens(zero,zero)+p**2*tens(one,one))/math.sqrt(n0)
    close(even,np.einsum('i,j,k->ijk',math.sqrt(n0)*evencoin.reshape(-1),G@v,old),
          'actual common even full old register')
    # Restore PTAIL by the routed inverse on the even branch.
    ez=sw(0,1)+[('I',1,2,3)]*2+sw(0,1)
    rev,paid=apply(tens(G@v,old),ez+[('G',0)]+ez)
    close(rev,tens(v,old),'early tail and dirty real source')
    early=paid+swaps(tens(evencoin,v,v),[0,1,2,3])
    return work+n0*early


def load(bit):
    # Physical CX(PAR,K) or CX(PTAIL,K). Both are real CX; PTAIL=0 on odd.
    word=sharp(0)+[('X' if bit else 'B',0)]
    key,fw=apply(v,word)
    close(key,one if bit else zero,'paid K at query')
    final,bw=apply(key,inv(word))
    close(final,v,'physical K returned to canonical v')
    return fw+bw,len(word)+len(inv(word))


def recipe(k1,k2,tag,m,n):
    # Data x,y,Q,R,N,T. Actual sharp K control is X or identity on its sector.
    b1='X' if k1 else 'B'; b2='X' if k2 else 'B'
    A=[(b1,2)]+[('G',2)]*m+[(b1,2)]
    B=[(b2,3)]+[('G',3)]*n+[(b2,3)]
    V=sharp(2)+A+[('C',0,2)]+sw(2,3)+B+sw(2,3)
    emit=[('C',2,4)]+(sharp(5)+[('C',2,5)] if tag else [])
    return V,emit


def scan(s,t,tag,m=1,n=2):
    k1=int(s<0);k2=int(t<0)
    V,emit=recipe(k1,k2,tag,m,n)
    odd=(tens(zero,one)+tens(one,zero))/math.sqrt(2)
    state=tens(odd,v,v,v,v)
    state,body=apply(state,V+emit+inv(V))
    keys=[load(k) for k in (k1,k2)]
    body+=sum(cost for cost,_ in keys)
    q=(1+math.sin(2*s*m*theta)*math.sin(2*t*n*theta))/2
    n1=p*p+p**3*q
    # d: paid 0, then N->d, then PAR=1 ->d. All subsequent gates preserve N.
    _,prepare=apply(v,sharp(0))
    body+=prepare
    nred=rho(state,[4])
    dstate,copies=local_work(np.kron(nred,np.outer(zero,zero)),[('C',0,1),('X',1)])
    body+=copies
    # NC1 on N and a new v; after the complement copy N has been decohered.
    _,readwork=local_work(np.kron(np.diag([1-n1,n1]),np.outer(v,v)),nc1(0,1))
    body+=readwork
    colds=[]
    born_square=0.
    for bit,nb in enumerate((1-n1,n1)):
        cut=np.take(state,bit,axis=4)/math.sqrt(nb)
        close(np.vdot(cut,cut),1,'observed noisy outcome probability')
        # Cut uses five true wires x,y,Q,R,T. N head/tail and copied complement
        # have net passive square p^4 independent of this measured outcome.
        old_overlap=np.vdot(tens(v,v,v,v,v),cut)
        cb=w**.5*((1-q)*v[bit]*(a if tag else 1)+q*v[1-bit]*(p if tag else 1))/math.sqrt(nb)
        close(old_overlap,cb,'normalized actual occupied leaf')
        close(v[bit]**2*p*v[1-bit]**2,p**4,'equal passive raw/read/complement')
        colds.append(p**3*p**4*abs(old_overlap)**2)
        body+=nb*swaps(cut,[0,1,2,3])
        born_square+=nb*abs(old_overlap)**2/w
    S=2*(p-p**3*q)-p**6*q*(1-q)/n1 if tag else (
        2-(a-p)**2*q*(1-q)/(p**3+p**6*q*(1-q)))
    h=p*n0+sum(colds)
    close(h,p*n0+2*p**10*S,'whole singular-value trace on every old column')
    if not tag: close(1-born_square,2*(a-p)**2*q*(1-q),'actual work leakage before swaps')
    count=sum(length for _,length in keys)+len(V+emit+inv(V))+5+3
    return q,n1,h,body,count


def entropy(x):
    return -x*math.log(x)/math.log(1/p)-(1-x)*math.log(1-x)/math.log(1/p)


def rigorous_transverse(s,t,tag):
    # Only terms changing between equal q corners are needed: the common
    # prefix, even branch, complement copy and final noisy NC1 cancel exactly.
    iv=mp.iv;iv.dps=45
    pp=(iv.sqrt(5)-1)/2
    aa=iv.sqrt(pp)
    ww=2*pp**3
    vv=[aa,pp]
    def apply_born(x,word):
        norm=sum(u*u for u in x)
        dim=(len(x)-1).bit_length()
        result=iv.mpf(0)
        for gate in word:
            what=gate[0];mask=1<<(dim-1-gate[-1])
            if what=='B':
                continue
            if what=='G':
                y=[(aa*i+pp*x[j^mask]) if j&mask else (aa*i-pp*x[j^mask])
                   for j,i in enumerate(x)]
            else:
                ctrl=0 if what=='X' else (1<<(dim-1-gate[1]))
                y=[x[j^mask] if not ctrl or j&ctrl else x[j] for j in range(len(x))]
            hit=sum(a0*b0 for a0,b0 in zip(x,y))
            rad=(norm-hit)*(norm+hit)
            if rad>0:
                result+=iv.sqrt(rad)
            else:
                rq(rad<iv.mpf('1e-35'),'vanishing interval of a movement')
                result+=iv.mpf([0,'1e-17'])
            x=y
        return x,result
    def append(x):
        return [a0*b0 for a0 in x for b0 in vv]
    state=[iv.mpf(0),aa*pp,aa*pp,iv.mpf(0)]
    for _ in range(4):state=append(state)
    keys=[int(s<0),int(t<0)]
    V,emit=recipe(*keys,tag,1,2)
    final,total=apply_born(state,V+emit+inv(V))
    for bit in keys:
        word=sharp(0)+[('X' if bit else 'B',0)]
        _,expense=apply_born(vv,word+inv(word))
        total+=ww*expense
    for b in (0,1):
        # Halve amplitudes by the actual measured N; no postselected division:
        # each cost is sqrt(mass^2 - amplitude_overlap^2).
        post=[u for j,u in enumerate(final) if ((j>>1)&1)==b]
        for target in range(4):
            _,expense=apply_born(append(post),sw(target,5))
            total+=expense
    return total


def main():
    old=np.zeros(8);old[0]=1.
    common=prefix(old)
    for index in range(1,8):prefix(np.eye(8)[index])
    prefix(np.exp(.27j*np.arange(8))*(np.arange(8)+1)/np.linalg.norm(np.arange(8)+1))
    output={}
    for label,tag in [('only_complement',False),('also_true_T',True)]:
        out=[]
        for s,t in itertools.product((-1,1),repeat=2):
            q,prob,h,body,period=scan(s,t,tag)
            total=common+w*body
            out.append(dict(signs=[s,t],q=round(q,12),N=round(prob,12),h=round(h,12),
                            complete_square_work=round(total,9),odd_square_interval=period))
        delta=-8*math.log1p(z*(out[0]['h']-out[1]['h'])/(1-z+z*out[1]['h']))
        if tag: rq(delta>2**-30,'strict direct eight-column direction')
        else: close(delta,0.,'equal complementary q cold determinant')
        bound=Fr(528,359)*Fr(1,11)**32/math.factorial(32)/(1-Fr(1,11*33))
        rq(bound<Fr(1,2**200) and min(r['odd_square_interval'] for r in out)>32,
           'complete heat on the actual comparison')
        transverse=rigorous_transverse(1,1,tag)-rigorous_transverse(-1,-1,tag)
        fl=math.floor(100*(out[3]['complete_square_work']-out[0]['complete_square_work']))
        rq(transverse>mp.iv.mpf(fl)/100 and transverse<mp.iv.mpf(fl+1)/100,
           'rigorous full equal-q work contrast')
        pp=out[0]['N'];pm=out[1]['N']
        linfo=w*(pp-entropy(pp)-pm+entropy(pm))
        close(linfo,w*(pp-pm),'whole printed code minus full CQ secant')
        output[label]=dict(fields=out,complete_registered_code_CQ_contrast=round(linfo,12),
                           full_RC3_same_sign_minus_opposite=round(delta,17),
                           rigorous_equal_signal_work_hundredths=[fl,fl+1],
                           equal_signal_work_plusplus_minus_minusminus=round(out[3]['complete_square_work']-out[0]['complete_square_work'],9))
    # Derivatives at q=1/2 and one stored true quantum bit.
    son=2*(p-p**3/2)-p**6/2
    hs=p*n0+2*p**10*son
    sq=-2*p**3+p**9
    jp=-z*(2*p**10)*sq/(1-z+z*hs)
    output.update(growing_clock_slope_per_face_no_T=0,
                  growing_clock_slope_per_face_with_T=8*jp/(2*nu**2),
                  genuinely_registered_code_CQ_slope_per_face=w*p**3/(2*nu**2),
                  trace_calibration='one moving q, common fieldname interface',old_rank=8,
                  independently_recorded_full_initializer_work=False,GR_closed=False)
    print(json.dumps(output,indent=2))


if __name__=='__main__':
    main()
