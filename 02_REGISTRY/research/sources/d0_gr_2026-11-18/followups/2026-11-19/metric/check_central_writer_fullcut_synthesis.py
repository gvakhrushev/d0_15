"""One native central writer, retained selector, and conditional Fourier effect.

Every writer gate is native and every old column is checked. Fourier success
is consumed from its separately conditional hardware interface; FQ weights
are tested candidates, not selected physical Book03 costs.
"""
from collections import Counter
import contextlib
import io
import json
import math
import numpy as np
from mpmath import iv
from scipy.linalg import eigvalsh

from check_local_gibbs_records import mm
from check_source_price import load_control, need
from check_direct_writer_fourier_effect import main as writer_fourier_check


def main():
    captured=io.StringIO()
    with contextlib.redirect_stdout(captured):writer_fourier_check()
    owner=json.loads(captured.getvalue())
    need(owner['protected_SITE_P_RIGHT_dimension_tested']==8 and
         owner['full_geometric_bank_or_joint_clock_compiled'] is False,
         'consume exact conditional Fourier interface, preserve limitations')
    ne,digest=load_control();p,a=float(ne.P),float(ne.A);gate=ne.Gate
    source=dict(profile=ne.G_CX_SOURCE_I,source_port=2,source_spin=(3,4))
    cache={}
    def matrix(n,g):
        key=n,g.op,g.wires
        if key not in cache:
            spec=ne.Execution(n,(),(),(g,),**source)
            cache[key]=np.array(ne.gate_matrix(spec,g,max_qubits=8,max_expanded_stages=100),dtype=float)
            half=len(cache[key])//2
            need(not np.any(cache[key][:half,half:]) and not np.any(cache[key][half:,:half]),
                 'every physical gate preserves selector s')
        return cache[key]
    def birth(V,n):return mm(np.kron(np.eye(1<<n),np.array([[a],[p]])),V)
    invspec=ne.Execution(8,(),(),(gate('G',(7,)),),**source)
    inv=ne.inverse_word(invspec,max_qubits=8,max_expanded_stages=100)
    need(Counter(g.op for g in inv)==Counter({'CX':6,'SourceI':4,'G':1}),
         'all routed SourceI inverse calls')
    E=birth(birth(birth(np.eye(32),5),6),7)
    bits=np.arange(256);sout=(bits>>7)&1;hout=(bits>>2)&1;tail=(bits>>1)&1;env=bits&1
    def complete(q):
        V=birth(np.eye(32),5)
        V=mm(matrix(6,gate('CX',(1,5))),V) # actual P-to-H writer
        V=mm(matrix(6,gate('CX',(0,5))),V) # actual selector s
        G=matrix(6,gate('G',(5,)))
        for _ in range(2*q):V=mm(G,V)
        V=mm(matrix(6,gate('CX',(0,5))),V)
        V=birth(V,6)
        for op in (gate('CX',(5,6)),gate('G',(6,)),gate('CX',(5,6))):V=mm(matrix(7,op),V)
        V=birth(V,7)
        for op in inv:V=mm(matrix(8,op),V)
        return mm(matrix(8,gate('CX',(5,7))),V)
    iv.dps=80;I=iv.mpf(1);pp=(iv.sqrt(5)-I)/2;aa=iv.sqrt(pp)
    ell=iv.log(I/pp);theta=iv.atan2(pp,aa);base=(I+pp)/2
    locator=(255+pp)/256
    expected_limit=pp**2/(ell*base)
    eig_limit=pp**5/2
    need(expected_limit>iv.mpf('.98113955') and expected_limit<iv.mpf('.98113956'),
         'candidate central success response')
    need(eig_limit>iv.mpf('.04508497') and eig_limit<iv.mpf('.04508498'),
         'nonzero full-input scalarity obstruction')
    for q,turn in ((19,2),(66,7),(613,65)):
        V=complete(q)
        need(np.max(np.abs(mm(V.T,V)-np.eye(32)))<4e-11,'all actual input columns')
        need(np.linalg.norm(V[hout!=env])<4e-11 and np.linalg.norm(V[(hout==1)&(tail==1)])<4e-11,
             'actual two NC1 outcomes and dark 11')
        need(np.linalg.norm(V[sout==0,16:])<4e-11 and np.linalg.norm(V[sout==1,:16])<4e-11,
             'one preserved selector on complete output')
        E1=mm(V[hout==1,:].T,V[hout==1,:]);E0=np.eye(32)-E1
        eps=q*theta-2*iv.pi*turn
        D=aa*pp*iv.sin(4*eps); dq=2*D; zeta=pp**3*iv.cos(4*eps)/2
        nums=[float((I/2+D-zeta).mid),float((I/2+D+zeta).mid),
              float((I/2-D-zeta).mid),float((I/2-D+zeta).mid)]
        need(np.max(np.abs(E1-np.diag(sum(([x]*8 for x in nums),[]))))<4e-11,
             'complete central-side writer effects including program P')
        need(np.max(np.abs(E1[:16,:16]-E1[16:,16:]-float(dq.mid)*np.eye(16)))<4e-11,
             'two actual recorded effects differ by scalar Delta q')
        # Keep the program selector and both NC1 records; the two input
        # programs are orthogonal even though the reduced descriptor
        # outcomes approach each other.
        inpplus=np.zeros(32);inpminus=np.zeros(32)
        inpplus[0]=inpplus[8]=1/math.sqrt(2)
        inpminus[16]=inpminus[24]=1/math.sqrt(2)
        outp,outm=mm(V,inpplus),mm(V,inpminus)
        def cq(out):
            parts=[]
            for h in (0,1):
                v=out.copy();v[hout!=h]=0;parts.append(np.outer(v,v))
            return sum(parts)
        rplus,rminus=cq(outp),cq(outm)
        distance=float(np.abs(eigvalsh(rplus-rminus,check_finite=False)).sum())
        need(abs(distance-2)<4e-11,'full recorded s=0/1 outputs have orthogonal support')
        # Writer and locator are both tilted only for the separate candidate;
        # normalization removes the conditional hardware success eta.
        Z=float(locator.mid)*(E0+p*E1)
        ev=np.linalg.eigvalsh(Z)
        dist=(ev[-1]-ev[0])/2
        predicted=float((locator*pp**2*(abs(D)+abs(zeta))).mid)
        need(abs(dist-predicted)<4e-11,'exact full-cut distance to scalar')
        slope=-iv.log((base-pp**2*D)/(base+pp**2*D))/(ell*dq)
        need(slope>iv.mpf('.98') and slope<iv.mpf('.99'),
             'central candidate response to actual finite selector secant')
        # The full bootstrap graph/cut is literally one fixed list: changing
        # selector input does not change either full clock or full F.
        print('q,turn:',q,turn,'actual Delta q:',dq)
        print('common rank-32 bootstrap source: 0')
        print('candidate success slope:',slope,'full-cut scalarity distance/eta:',dist)
        print('full retained programme trace distance:',distance,'divided by |Delta q|:',distance/abs(float(dq.mid)))
    print('success candidate slope limit:',expected_limit)
    print('writer-effect scalarity-distance limit before locator/eta:',eig_limit)
    print('all actual writer columns retained; complete Fourier factory/Book03 source open')
    print('native source sha256:',digest)


if __name__=='__main__':main()
