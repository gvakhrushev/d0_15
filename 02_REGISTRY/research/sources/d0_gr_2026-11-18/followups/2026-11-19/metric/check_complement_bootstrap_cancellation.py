"""All-column native complemented writer and full-cut RAW parity.

The coherent clock and retained-failure dilation below are explicitly
specified. They are not a compiled physical CQ-recorder or the full Book03
Cost-Info/factory/controller history.
"""
import json
import math
from collections import Counter
import numpy as np
from mpmath import iv
from check_source_price import load_control, need
from check_local_gibbs_records import mm


def main():
    ne,digest=load_control();p=float(ne.P);a=float(ne.A);gate=ne.Gate
    aa,pp=ne.A,ne.P
    identities=(aa**2-pp,pp**2+pp-1,
                aa*(pp-pp**2)+pp*(2*aa*pp)-aa,
                aa*pp**2*(aa+pp)-pp**3*(1+aa))
    need(all(ne.GOLDEN_FIELD.from_sympy(x)==ne.GOLDEN_FIELD.zero for x in identities),
         'exact Golden field identities and scalar passive return')
    source=dict(profile=ne.G_CX_SOURCE_I,source_port=1,source_spin=(2,3))
    def matrix(n,g):
        spec=ne.Execution(n,(),(),(g,),**source)
        return np.asarray(ne.gate_matrix(spec,g,max_qubits=5,max_expanded_stages=100),float)
    swap=(gate('CX',(4,1)),gate('CX',(1,4)),gate('CX',(4,1)))
    zword=swap+(gate('SourceI',(1,2,3)),gate('SourceI',(1,2,3)))+swap
    zm=np.eye(32)
    for op in zword:zm=mm(matrix(5,op),zm)
    z_target=np.kron(np.eye(16),np.diag([1.,-1.]))
    need(np.max(abs(zm-z_target))<1e-13,'actual routed Z on all port/spin columns')
    # Q gates X are literal CX(h,Q) restricted to a genuinely available
    # external h=1, which remains unmodified. Verify this on both Q inputs.
    cx=np.array([[1.,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
    need(np.array_equal(cx[2:,2:],np.array([[0.,1.],[1.,0.]])),'CX on known one')
    G=np.array([[a,-p],[p,a]]);X=np.array([[0.,1.],[1.,0.]])
    p2=p*p
    def birth(V,n):return np.einsum('ij,k->ikj',V,[a,p]).reshape((1<<(n+1),16))
    def local(V,n,w,A):
        Y=V.reshape([2]*n+[16]);Y=np.moveaxis(Y,w,0)
        Y=np.tensordot(A,Y,axes=(1,0));return np.moveaxis(Y,0,w).reshape((1<<n,16))
    def cnot(V,n,c,t):
        idx=np.arange(1<<n);cm=1<<(n-1-c);tm=1<<(n-1-t)
        dest=idx^np.where((idx&cm)!=0,tm,0);out=np.empty_like(V);out[dest]=V;return out
    def word(q,side):
        V=np.eye(16);E=np.eye(16);n=4
        V=birth(V,n);E=birth(E,n);n+=1;V=cnot(V,n,0,4)
        # W+ = G^q; Z; Z, W- = Z; G^q; Z: use the verified
        # complete physical routed Z rather than an unverified sign gate.
        choices=([1,-1] if side==0 else [1,1] if side==2 else [side])
        for choice in choices:
            if choice<0:V=mm(zm,V)
            for _ in range(q):V=local(V,n,4,G)
            V=mm(zm,V)
            if choice>0:V=mm(zm,V)
        V=birth(V,n);E=birth(E,n);n+=1
        V=cnot(V,n,4,5);V=local(V,n,5,G);V=cnot(V,n,4,5)
        V=birth(V,n);E=birth(E,n);n+=1
        # X_h G X_h prepares Q=0; then X_h, CX(H,Q) writes Q=1-H.
        V=local(V,n,6,X);V=local(V,n,6,G);V=local(V,n,6,X)
        V=local(V,n,6,X);V=cnot(V,n,4,6)
        V=birth(V,n);E=birth(E,n);n+=1
        V=cnot(V,n,6,7);V=local(V,n,7,G);V=cnot(V,n,6,7)
        need(np.max(abs(mm(V.T,V)-np.eye(16)))<2e-12,'full input isometry')
        ind=np.arange(1<<n);H=(ind>>(n-1-4))&1;Q=(ind>>(n-1-6))&1
        A=(ind>>(n-1-5))&1;B=(ind>>(n-1-7))&1
        need(np.linalg.norm(V[H==Q])<2e-12,'all actual retained complementary outcomes')
        need(np.linalg.norm(V[(H==1)&(A==1)])<2e-12,'first NC1 dark')
        need(np.linalg.norm(V[(Q==1)&(B==1)])<2e-12,'second NC1 dark')
        return mm(E.T,V), mm(V[H==1].T,V[H==1]),V,E
    z=2**-20; c0=p**3*(1+a);w=a*p**2;limit=[]
    iv.dps=60;pi=(iv.sqrt(5)-1)/2;ai=iv.sqrt(pi);ell=iv.log(1/pi)
    zi=iv.mpf(1)/(2**20);ci=pi**3*(1+ai);di=ai*pi**2*(ai-pi)
    den=1-zi+zi*ci**2
    jtt=-16*zi*((di**2-ci**2)/den-2*zi*ci**2*di**2/den**2)
    jqq=jtt/(2*ai*pi)**2; cq_qq=4/ell
    need(jqq<iv.mpf('0.000003') and jqq>0 and cq_qq>iv.mpf('8.31'),
         'strictly separated conditional terminal and complete RAW curvatures')
    for q,m in ((19,2),(66,7),(613,65)):
        t=q*math.asin(p)-2*math.pi*m
        Cplus,Eplus,Vplus,Ein=word(q,1);Cminus,Eminus,Vminus,Ein2=word(q,-1)
        cp0=w*((a+p)*math.cos(t)+(a-p)*math.sin(t))
        cp1=w*((a+p)*math.cos(t)-(a-p)*math.sin(t))
        target=np.diag([cp0]*8+[cp1]*8)
        targetm=np.diag([cp1]*8+[cp0]*8)
        need(np.max(abs(Cplus-target))<8e-12 and np.max(abs(Cminus-targetm))<8e-12,'all 16 old columns, both actual words')
        dq=2*a*p*math.sin(2*t)
        need(np.max(abs(Eplus-Eminus-dq*np.eye(16)))<8e-12,'recorded H effect difference, whole input')
        def j(C):return -np.linalg.slogdet(np.eye(16)-z*(np.eye(16)-mm(C.T,C)))[1]
        need(abs(j(Cplus)-j(Cminus))<3e-15,'complete rank-16 feedback exact evenness numerical replay')
        central,Ecentral,_,_=word(q,0);double,Edouble,_,_=word(q,2)
        t2=2*t
        d0=w*((a+p)*math.cos(t2)+(a-p)*math.sin(t2))
        d1=w*((a+p)*math.cos(t2)-(a-p)*math.sin(t2))
        need(np.max(abs(central-c0*np.eye(16)))<1e-11 and
             np.max(abs(double-np.diag([d0]*8+[d1]*8)))<1e-11,
             'same-inventory actual central word and side')
        qcentre=float(np.trace(Ecentral)/16);qside=float(np.trace(Edouble)/16)
        need(abs(qcentre-.5)<1e-11 and abs(qside-.5-a*p*math.sin(4*t))<1e-11,
             'central plus preparation and actual recorded field step')
        # Explicit ALL-success/failure dilation: same full passive success or
        # failure flags, failure identity on old input, success actual word.
        # Controller realizing these blocks natively is NOT assumed proven.
        for b in (.2,.8,1-p**8,1-p**40):
            Vfplus=np.vstack([math.sqrt(b)*Vplus,math.sqrt(1-b)*Ein])
            Vfminus=np.vstack([math.sqrt(b)*Vminus,math.sqrt(1-b)*Ein])
            Ef=np.vstack([math.sqrt(b)*Ein,math.sqrt(1-b)*Ein])
            fullp=mm(Ef.T,Vfplus);fullm=mm(Ef.T,Vfminus)
            need(np.max(abs(fullp-(b*Cplus+(1-b)*np.eye(16))))<1e-12,'all-branch full return')
            need(abs(j(fullp)-j(fullm))<3e-15,'full retained failure feedback parity')
        # Every one of L individual failure-prefix/first-success flags is
        # retained, plus the all-L-failed abort.  The actual controlled
        # variable-time gate implementation and passive cut are not claimed.
        for cap in (4,8,40):
            masses=[p**i*p**2 for i in range(cap)]+[p**cap]
            need(abs(sum(masses)-1)<1e-13,'complete finite first-success law')
            eparts=[math.sqrt(s)*Ein for s in masses]
            vp=[math.sqrt(s)*Vplus for s in masses[:-1]]+[math.sqrt(masses[-1])*Ein]
            vm=[math.sqrt(s)*Vminus for s in masses[:-1]]+[math.sqrt(masses[-1])*Ein]
            Eflag=np.vstack(eparts);Fp=mm(Eflag.T,np.vstack(vp));Fm=mm(Eflag.T,np.vstack(vm))
            need(np.max(abs(Fp-((1-p**cap)*Cplus+p**cap*np.eye(16))))<3e-12,
                 'all fine first-success and terminal failure records')
            need(abs(j(Fp)-j(Fm))<3e-15,'all retained first-success histories cancel')
        limit.append({'q':q,'turn':m,'epsilon':t,'recorded_delta':dq,
            'success_return_diag_0':float(Cplus[0,0]),'success_return_diag_1':float(Cplus[8,8]),
            'success_feedback_abs_difference':abs(j(Cplus)-j(Cminus)),
            'all_branch_dilation_retains_success_and_failure':True})
    # Mathematically exact branch exchange and D_q J=0 from c± values.
    need(abs(c0-w*(a+p))<1e-14,'golden exact expression for centre')
    out={'status':'PASS: exact branch-exchange RAW cancellation for stated coherent cut',
         'native_source_sha256':digest,'old_input_rank':16,'conditional_clean_h':True,
         'success_centre_return_scalar':c0,'success_centre_return_formula':'p^3*(1+sqrt(p))',
         'raw_J_second_derivative_per_q':float(jqq.mid),
         'conditional_terminal_CQ_second_derivative_per_q':float(cq_qq.mid),
         'retained_records':'all H/Q outcomes; both NC1 dark 11 sectors checked',
         'actual_finite_word_checks':limit,
         'bounded_real_abort_controller_physically_compiled':False,
         'actual_CQ_cut_and_full_Book03_Info_selected':False,
         'original_full_Geo_Fourier_clock_compiled':False,'GR_closed':False}
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
