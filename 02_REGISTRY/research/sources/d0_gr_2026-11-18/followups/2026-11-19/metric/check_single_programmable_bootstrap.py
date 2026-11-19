"""One fully native programmable seed/NC1 circuit and its common cut.

The two programmed branches are real; the global bootstrap is independent of
which input programme is prepared. Their sector bootstraps are different
functionals. Full physical programme preparation and Einstein lifting remain open.
"""
from collections import Counter
import math
import numpy as np
from mpmath import iv

from check_local_gibbs_records import mm
from check_source_price import load_control, need


def main():
    ne,digest=load_control();p,a=float(ne.P),float(ne.A);gate=ne.Gate
    source=dict(profile=ne.G_CX_SOURCE_I,source_port=2,source_spin=(3,4))
    cache={}
    def matrix(n,g):
        key=(n,g.op,g.wires)
        if key not in cache:
            spec=ne.Execution(n,(),(),(g,),**source)
            cache[key]=np.array(ne.gate_matrix(spec,g,max_qubits=8,max_expanded_stages=100),dtype=float)
            half=len(cache[key])//2
            need(np.max(np.abs(cache[key][:half,half:]))==0 and
                 np.max(np.abs(cache[key][half:,:half]))==0,
                 'each native gate preserves the programme sector')
        return cache[key]
    def birth(V,n):return mm(np.kron(np.eye(1<<n),np.array([[a],[p]])),V)
    invspec=ne.Execution(8,(),(),(gate('G',(7,)),),**source)
    inv=ne.inverse_word(invspec,max_qubits=8,max_expanded_stages=100)
    need(Counter(g.op for g in inv)==Counter({'CX':6,'SourceI':4,'G':1}),
         'full native routed inverse with old dirty port')
    E=birth(birth(birth(np.eye(32),5),6),7)
    Hout=(np.arange(256)>>2)&1;env=np.arange(256)&1
    selector=(np.arange(256)>>7)&1
    iv.dps=90;one=iv.mpf(1);pp=(iv.sqrt(5)-one)/2;aa=iv.sqrt(pp)
    th=iv.atan2(pp,aa);zz=one/(2**20);beta=2*pp**2
    cc0=pp**2+aa*pp**3;cc1=aa*pp**2+pp**3
    dc0=pp**3-aa*pp**2;dc1=aa*pp**3-pp**2
    def j(t):
        cs=[cc0*iv.cos(t)+dc0*iv.sin(t),cc1*iv.cos(t)+dc1*iv.sin(t)]
        return -8*sum(iv.log(one-zz*(one-c*c)) for c in cs)
    x=beta/11;L=12
    e=2*x**L/(math.factorial(L)*(one-x/(L+1)))
    heat_bound=132*e/(359*beta)
    def complete(q):
        V=birth(np.eye(32),5)
        V=mm(matrix(6,gate('CX',(1,5))),V) # original k field
        V=mm(matrix(6,gate('CX',(0,5))),V) # common selector, no branching
        g=matrix(6,gate('G',(5,)))
        for _ in range(q):V=mm(g,V)
        V=mm(matrix(6,gate('CX',(0,5))),V)
        V=birth(V,6)
        for op in (gate('CX',(5,6)),gate('G',(6,)),gate('CX',(5,6))):
            V=mm(matrix(7,op),V)
        V=birth(V,7)
        for op in inv:V=mm(matrix(8,op),V)
        V=mm(matrix(8,gate('CX',(5,7))),V)
        return V
    for q,turn in ((19,2),(66,7),(613,65)):
        V=complete(q)
        need(np.max(np.abs(mm(V.T,V)-np.eye(32)))<2e-11,'all 32 old-input columns')
        need(np.linalg.norm(V[Hout!=env])<2e-11,'all actual NC1 environment outcomes')
        need(np.linalg.norm(V[selector==1,:16])<2e-11 and
             np.linalg.norm(V[selector==0,16:])<2e-11,'selector preserved on entire output')
        C=mm(E.T,V)
        effects=mm(V[Hout==1,:].T,V[Hout==1,:])
        t=q*th-2*iv.pi*turn;dq=2*aa*pp*iv.sin(2*t)
        tf=float(t.mid); dqn=float(dq.mid)
        cf0,cf1=float(cc0.mid),float(cc1.mid)
        df0,df1=float(dc0.mid),float(dc1.mid)
        cs=[cf0*math.cos(tf)+df0*math.sin(tf),cf1*math.cos(tf)+df1*math.sin(tf),
            cf0*math.cos(tf)-df0*math.sin(tf),cf1*math.cos(tf)-df1*math.sin(tf)]
        need(np.max(np.abs(C-np.diag(sum(([c]*8 for c in cs),[]))))<2e-11,
             'four actual selector/k return blocks')
        ep,em=effects[:16,:16],effects[16:,16:]
        need(np.max(np.abs(ep-em-dqn*np.eye(16)))<2e-11,
             'different actual field effects, same other input and RIGHT')
        full_j=-sum(math.log1p(-(2**-20)*(1-c*c)) for c in cs for _ in range(8))
        sector_sum=float((j(t)+j(-t)).mid)
        need(abs(full_j-sector_sum)<1e-13,'full determinant is the sum of both sector J values')
        ratio=(j(t)-j(-t))/dq
        err=heat_bound/abs(dq)
        need(ratio-err>iv.mpf('0.00000222') and ratio+err<iv.mpf('0.00000223'),
             'sector bootstrap contrast nonzero, both Hodge degrees bounded')
        # Under either input selector the graph and its full-rank cut are
        # literally the same stage list, hence the full bootstrap difference
        # is identically zero; it is not the difference of sector actions.
        Dfull=3744+64*(q+2)
        print('q,turn:',q,turn,'common full clock D:',Dfull,'old cut rank: 32')
        print('true recorded-field difference:',dq,'common full bootstrap difference: 0')
        print('restricted-sector bootstrap secant/field:',ratio-err,ratio+err)
    print('fixed programme word per q: 3 births, 12 CX, q+2 G, 4 SourceI')
    print('native source sha256:',digest)
    print('no single full-cut positive bootstrap source; physical preparation and GR remain open')


if __name__=='__main__':main()
