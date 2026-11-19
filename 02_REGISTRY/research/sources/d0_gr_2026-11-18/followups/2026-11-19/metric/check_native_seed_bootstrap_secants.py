"""Actual equal-inventory native gate words approximate a bootstrap gate jet.

Every finite endpoint is a genuine G/CX/SourceI word. The common cut and
full Hodge heat bounds are retained. The physical Einstein-field lift and
Book Cost-Info are not assumed or proved.
"""
import math
import numpy as np
from mpmath import iv

from check_local_gibbs_records import mm
from check_source_price import load_control, need


def main():
    ne,digest=load_control(); p,a=float(ne.P),float(ne.A); gate=ne.Gate
    source=dict(profile=ne.G_CX_SOURCE_I,source_port=1,source_spin=(2,3))
    def matrix(n,g):
        spec=ne.Execution(n,(),(),(g,),**source)
        return np.array(ne.gate_matrix(spec,g,max_qubits=7,max_expanded_stages=100),dtype=float)
    def birth(V,n):return mm(np.kron(np.eye(1<<n),np.array([[a],[p]])),V)
    g=matrix(5,gate('G',(4,)))
    swap=(gate('CX',(4,1)),gate('CX',(1,4)),gate('CX',(4,1)))
    zword=swap+(gate('SourceI',(1,2,3)),gate('SourceI',(1,2,3)))+swap
    zmat=np.eye(32)
    for op in zword:zmat=mm(matrix(5,op),zmat)
    need(np.max(np.abs(zmat-np.kron(np.eye(16),np.diag([1.,-1.]))))<5e-14,
         'actual two-SourceI routed Z on every old column')
    spec=ne.Execution(7,(),(),(gate('G',(6,)),),**source)
    inverse=ne.inverse_word(spec,max_qubits=7,max_expanded_stages=100)
    need(len(inverse)==11,'real routed inverse for the environment')
    old=birth(np.eye(16),4)
    old=mm(matrix(5,gate('CX',(0,4))),old)
    E=birth(birth(birth(np.eye(16),4),5),6)
    def complete(macro):
        V=mm(macro,old)
        V=birth(V,5)
        for op in (gate('CX',(4,5)),gate('G',(5,)),gate('CX',(4,5))):
            V=mm(matrix(6,op),V)
        V=birth(V,6)
        for op in inverse:V=mm(matrix(7,op),V)
        V=mm(matrix(7,gate('CX',(4,6))),V)
        need(np.max(np.abs(mm(V.T,V)-np.eye(16)))<1e-11,'complete all-column isometry')
        h=(np.arange(128)>>2)&1;env=np.arange(128)&1
        need(np.linalg.norm(V[h!=env])<1e-11,'actual final NC1 environment')
        return mm(E.T,V), mm(V[h==1,:].T,V[h==1,:])

    iv.dps=90;one=iv.mpf(1);pp=(iv.sqrt(5)-one)/2;aa=iv.sqrt(pp)
    theta=iv.atan2(pp,aa);zz=one/(2**20);beta=2*pp**2
    c0=pp**2+aa*pp**3;c1=aa*pp**2+pp**3
    d0=pp**3-aa*pp**2;d1=aa*pp**3-pp**2
    def J(t):
        values=[c0*iv.cos(t)+d0*iv.sin(t),c1*iv.cos(t)+d1*iv.sin(t)]
        return -8*sum(iv.log(one-zz*(one-v*v)) for v in values)
    x=beta/11;L=12
    e=2*x**L/(math.factorial(L)*(one-x/(L+1)))
    heat_bound=132*e/(359*beta)
    base_j=-16*zz*(c0*d0/(one-zz*(one-c0*c0))+
                   c1*d1/(one-zz*(one-c1*c1)))
    limit=base_j/(2*aa*pp)
    for q,turn in ((19,2),(66,7),(613,65)):
        power=np.eye(32)
        for _ in range(q):power=mm(g,power)
        # Chronological words G^q;Z;Z and Z;G^q;Z, each q+16
        # actual calls, no uncharged inverse and the same full input cut.
        plus=mm(zmat,zmat,power)
        minus=mm(zmat,power,zmat)
        cp,ep=complete(plus);cm,em=complete(minus)
        t=q*theta-2*iv.pi*turn
        dq=2*aa*pp*iv.sin(2*t)
        dj=J(t)-J(-t)
        ratio=dj/dq
        err=heat_bound/abs(dq)
        need(ratio-err>iv.mpf('0.00000222') and ratio+err<iv.mpf('0.00000223'),
             'full bootstrap secant positive after both Hodge degrees')
        tmid=float(t.mid);dqn=float(dq.mid)
        # Endpoint identity independently verified against the literal
        # SourceI/CX/G products and every full input column.
        c0f=float(c0.mid);c1f=float(c1.mid);d0f=float(d0.mid);d1f=float(d1.mid)
        exp_p=np.diag([(c0f*math.cos(tmid)+d0f*math.sin(tmid))]*8+
                      [(c1f*math.cos(tmid)+d1f*math.sin(tmid))]*8)
        exp_m=np.diag([(c0f*math.cos(tmid)-d0f*math.sin(tmid))]*8+
                      [(c1f*math.cos(tmid)-d1f*math.sin(tmid))]*8)
        need(np.max(np.abs(cp-exp_p))<1e-11 and np.max(np.abs(cm-exp_m))<1e-11,
             'both literal physical return operators')
        need(np.max(np.abs(ep-em-dqn*np.eye(16)))<1e-11,
             'two actual recorded field effects on full input')
        print('q,turn:',q,turn,'epsilon:',t,'delta_q:',dq)
        print('native full-bootstrap secant/field enclosure:',ratio-err,ratio+err)
        print('actual full clock dimension, no padding:',1872+32*(q+16))
    print('exact limiting normalized bootstrap field source:',limit)
    print('native source sha256:',digest)
    print('different matched-layout native words; full Einstein lift and Book Info open')


if __name__=='__main__':main()
