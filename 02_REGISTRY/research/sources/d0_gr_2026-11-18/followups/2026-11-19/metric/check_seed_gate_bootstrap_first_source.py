"""Full-cut bootstrap gate jet at the literal native seed word.

The off-anchor rotation is a smooth matrix comparison, not a certified
native gate family or a physical Einstein field lift. Both Hodge degrees,
all input sectors and all real birth complements are included.
"""
from collections import Counter
import math
import numpy as np
import scipy.sparse as sparse
from mpmath import iv

from check_local_gibbs_records import mm
from check_seed_nc1_record_clock import make_clock
from check_source_price import load_control, need


def main():
    ne, digest = load_control()
    p,a=float(ne.P),float(ne.A)
    gate=ne.Gate
    source=dict(profile=ne.G_CX_SOURCE_I,source_port=1,source_spin=(2,3))
    spec=ne.Execution(7,(),(),(gate('G',(6,)),),**source)
    inv=ne.inverse_word(spec,max_qubits=7,max_expanded_stages=100)
    stages=[]; derivatives=[]; current=4
    def birth():
        nonlocal current
        b=np.kron(np.eye(1<<current),np.array([[a],[p]]))
        stages.append((b,b,'birth'));derivatives.append(np.zeros_like(b));current+=1
    def append(g, variable=False):
        spec=ne.Execution(current,(),(),(g,),**source)
        op=np.array(ne.gate_matrix(spec,g,max_qubits=7,max_expanded_stages=100),dtype=float)
        dop=np.zeros_like(op)
        if variable:
            need(g.op=='CX' and g.wires==(0,4) and current==5,'literal field gate')
            generator=np.kron(np.eye(16),np.array([[0.,-1.],[1.,0.]]))
            dop=mm(generator,op)
        stages.append((op,np.eye(1<<current),g.op));derivatives.append(dop)
    birth();append(gate('CX',(0,4)),True);birth()
    for g in (gate('CX',(4,5)),gate('G',(5,)),gate('CX',(4,5))):append(g)
    birth()
    for g in inv:append(g)
    append(gate('CX',(4,6)))
    need(Counter(kind for _,_,kind in stages)==Counter({'birth':3,'CX':10,'G':2,'SourceI':4}),
         'all actual stages retained')
    V=E=np.eye(16);dV=np.zeros((16,16))
    for (u,passive,_),du in zip(stages,derivatives):
        dV=mm(du,V)+mm(u,dV)
        V,E=mm(u,V),mm(passive,E)
    C,dC=mm(E.T,V),mm(E.T,dV)
    c0=p*p+a*p**3;c1=a*p*p+p**3
    d0=p**3-a*p*p;d1=a*p**3-p*p
    need(np.max(np.abs(C-np.diag([c0]*8+[c1]*8)))<5e-13,'native full-cut return')
    need(np.max(np.abs(dC-np.diag([d0]*8+[d1]*8)))<5e-13,'all full-input gate jet')
    need(np.max(np.abs(mm(V.T,dV)+mm(dV.T,V)))<5e-13,'linearized full isometry')
    h=(np.arange(128)>>2)&1
    one=V[h==1,:];done=dV[h==1,:]
    d_effect=mm(done.T,one)+mm(one.T,done)
    need(np.max(np.abs(d_effect-2*a*p*np.eye(16)))<5e-13,
         'actual recorded-H operator field jet on all input columns')
    T=make_clock(stages)
    need(T.shape==(1872,1872),'full unselected clock and every input sector')
    dims=[stages[0][0].shape[1]]+[s[0].shape[0] for s in stages[:-1]]
    offsets=np.cumsum([0]+dims)
    DT=sparse.coo_matrix((1872,1872)).tolil()
    DT[offsets[2]:offsets[3],offsets[1]:offsets[2]]=derivatives[1]
    DT=DT.tocsr();TT=sparse.csr_matrix(T)
    tangent=TT.T@DT+DT.T@TT
    need((max(abs(tangent.data)) if tangent.nnz else 0.0)<5e-13,
         'whole growing clock varies unitarily')
    need(abs(np.linalg.norm(derivatives[1],ord=2)-1)<5e-13,'true clock gate-jet norm')
    min_loop=min(len(stages)-(j+1) for j,(_,_,kind) in enumerate(stages[:-1]) if kind=='birth')
    need(min_loop==12,'true minimum closed loop after last birth')

    iv.dps=80;oneiv=iv.mpf(1);pp=(iv.sqrt(5)-oneiv)/2;aa=iv.sqrt(pp)
    zz=oneiv/(2**20);beta=2*pp**2
    cc0=pp**2+aa*pp**3;cc1=aa*pp**2+pp**3
    dc0=pp**3-aa*pp**2;dc1=aa*pp**3-pp**2
    dJ=-16*zz*(cc0*dc0/(oneiv-zz*(oneiv-cc0**2))+
               cc1*dc1/(oneiv-zz*(oneiv-cc1**2)))
    # G14 / LOCAL_GIBBS_RECORDS: the full two-degree heat derivative
    # has no terms before the genuine shortest clock loop L=12.
    x=beta/11;L=12
    tail=x**(L-1)/(math.factorial(L-1)*(oneiv-x/L))
    r=x*tail
    hbound=66*r/(359*beta)
    dq=2*aa*pp
    need(dJ-hbound>iv.mpf('0.0000021633') and dJ+hbound<iv.mpf('0.0000021634'),
         'strict nonzero entire bootstrap gate jet')
    need(dq>iv.mpf('0.9717') and dq<iv.mpf('0.9718'),'native recorded field jet')
    print('native source sha256:',digest)
    print('actual gate centre CX(k,H); entire rank-16 cut; both k sectors')
    print('19 stages, full clock D=1872, two Hodge degrees:',425*1872)
    print('full reported-bit effect derivative:',dq)
    print('full feedback derivative:',dJ)
    print('absolute full two-degree heat derivative bound:',hbound)
    print('full bootstrap derivative enclosure:',dJ-hbound,dJ+hbound)
    print('normalized by measured q derivative:',(dJ-hbound)/dq,(dJ+hbound)/dq)
    print('off-anchor matrix path not certified in native grammar; GR open')


if __name__=='__main__':main()
