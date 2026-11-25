"""Native-logical guarded first h attempt, both h outcomes, full passive cut.

All four Fredkin Toffolis are ideal logical letters; their actual factories,
independent known-one and all Toffoli failures are deliberately not modeled.
This script does not claim a complete native physical clock or Book03 price.
"""
import json, math
import numpy as np
from check_source_price import load_control, need
from check_local_gibbs_records import mm


def main():
    ne,digest=load_control();p=float(ne.P);a=float(ne.A);G=np.array([[a,-p],[p,a]])
    pp,aa=ne.P,ne.A;f1=aa*(2*pp**2+pp**4)
    alpha_exact=pp*aa*(pp*aa*pp**2*(1+f1)+pp**4*(pp+f1))
    alpha0=float(alpha_exact)
    gate=ne.Gate;source=dict(profile=ne.G_CX_SOURCE_I,source_port=1,source_spin=(2,3))
    def mat(n,g):
        spec=ne.Execution(n,(),(),(g,),**source)
        return np.asarray(ne.gate_matrix(spec,g,max_qubits=5,max_expanded_stages=100),float)
    sw=(gate('CX',(4,1)),gate('CX',(1,4)),gate('CX',(4,1)))
    route=sw+(gate('SourceI',(1,2,3)),gate('SourceI',(1,2,3)))+sw
    Z=np.eye(32)
    for op in route:Z=mm(mat(5,op),Z)
    need(np.max(abs(Z-np.kron(np.eye(16),np.diag([1.,-1.]))))<2e-14,
         'literal two-SourceI route Z preserves all old port and spin inputs')
    def birth(V,n):return np.einsum('ij,k->ikj',V,[a,p]).reshape((1<<(n+1),2))
    def local(V,n,w,A):
        Y=V.reshape([2]*n+[2]);Y=np.moveaxis(Y,w,0)
        Y=np.tensordot(A,Y,axes=(1,0));return np.moveaxis(Y,0,w).reshape((1<<n,2))
    def toggle(V,n,cs,t):
        ind=np.arange(1<<n);on=np.ones(1<<n,dtype=bool)
        for w in cs:on &= (ind & (1<<(n-1-w))) != 0
        dst=ind ^ np.where(on,1<<(n-1-t),0);out=np.empty_like(V);out[dst]=V;return out
    def cx(V,n,c,t):return toggle(V,n,(c,),t)
    def tof(V,n,c,d,t):return toggle(V,n,(c,d),t)
    def fredkin(V,n,c,x,y):
        V=cx(V,n,y,x);V=tof(V,n,c,x,y);return cx(V,n,y,x)
    def nc1(V,n,c,t):return cx(local(cx(V,n,c,t),n,t,G),n,c,t)
    def word(q,side):
        # old input P; born h, tail, program-dummy D, route-dummy W,
        # writer H, tail A, complement Q, tail B, in the listed real order.
        V=E=np.eye(2);n=1
        V=birth(V,n);E=birth(E,n);n+=1 # h
        V=birth(V,n);E=birth(E,n);n+=1 # h tail
        V=nc1(V,n,1,2)
        V=birth(V,n);E=birth(E,n);n+=1 # D
        V=birth(V,n);E=birth(E,n);n+=1 # W
        V=fredkin(V,n,1,0,3)          # route P into D on success
        V=birth(V,n);E=birth(E,n);n+=1 # H
        V=cx(V,n,3,5)
        V=fredkin(V,n,1,5,4)          # route H onto W iff h=1
        # W± are expanded G and routed Z (whose full old-port action was
        # verified above), no uncharged inverse G is used.
        z=np.diag([1.,-1.])
        if side<0:V=local(V,n,4,z)
        for _ in range(q):V=local(V,n,4,G)
        V=local(V,n,4,z)
        if side>0:V=local(V,n,4,z)
        V=fredkin(V,n,1,5,4)
        V=birth(V,n);E=birth(E,n);n+=1 # A
        V=nc1(V,n,5,6)
        V=birth(V,n);E=birth(E,n);n+=1 # Q
        V=cx(V,n,1,7);V=local(V,n,7,G);V=cx(V,n,1,7)
        V=cx(V,n,1,7);V=cx(V,n,5,7)
        V=birth(V,n);E=birth(E,n);n+=1 # B
        V=nc1(V,n,7,8)
        V=fredkin(V,n,1,0,3)          # return true P or leave it untouched
        need(n==9 and np.max(abs(mm(V.T,V)-np.eye(2)))<2e-12,'full input isometry')
        ind=np.arange(1<<n);h=(ind>>(n-1-1))&1
        htail=(ind>>(n-1-2))&1;H=(ind>>(n-1-5))&1;Q=(ind>>(n-1-7))&1
        A=(ind>>(n-1-6))&1;B=(ind>>(n-1-8))&1
        need(np.linalg.norm(V[(h==1)&(htail==1)])<1e-12,'preparation NC1 dark')
        need(np.linalg.norm(V[(H==1)&(A==1)])<1e-12 and
             np.linalg.norm(V[(Q==1)&(B==1)])<1e-12,'both writer NC1 dark')
        need(np.linalg.norm(V[(h==1)&(H==Q)])<1e-12,'complement on real success')
        # Failure h=0 leaves the actual old input unchanged as a complete
        # isometry, not merely as a scalar averaged effect.
        lower=(ind&(1<<(n-1)))==0;upper=~lower
        need(np.linalg.norm(V[(h==0)&lower,1])<1e-12 and
             np.linalg.norm(V[(h==0)&upper,0])<1e-12 and
             np.linalg.norm(V[(h==0)&lower,0]-V[(h==0)&upper,1])<1e-12,
             'full failure isometry is identity on old P and arbitrary RIGHT')
        C=mm(E.T,V);C0=mm(E[h==0].T,V[h==0]);C1=mm(E[h==1].T,V[h==1])
        need(np.max(abs(C-C0-C1))<1e-13,'both actual h branches retained')
        eff1=mm(V[h==1].T,V[h==1]);eff0=mm(V[h==0].T,V[h==0])
        need(np.max(abs(eff1-p*p*np.eye(2)))<1e-12 and np.max(abs(eff0-p*np.eye(2)))<1e-12,
             'full h success/failure scalar effects on arbitrary input')
        return C,C0,C1,V,E
    z=2**-20;w=a*p*p;c=p**3*(1+a)
    out=[];first=None
    for q,m in ((19,2),(66,7),(613,65)):
        ep=q*math.asin(p)-2*math.pi*m
        Cp,Fp,Sp,Vp,E=word(q,1);Cm,Fm,Sm,Vm,E2=word(q,-1)
        states=np.arange(Vp.shape[0]);h=(states>>(9-1-1))&1;W=(states>>(9-1-4))&1
        H=(states>>(9-1-5))&1
        fail=(h==0);report=(h==0)&(W==0)
        delta_q=2*a*p*math.sin(2*ep)
        signal=(h==1)&(H==1)
        diff=mm(Vp[signal].T,Vp[signal])-mm(Vm[signal].T,Vm[signal])
        need(np.max(abs(diff-p*p*delta_q*np.eye(2)))<1e-12,
             'unconditional actual success field effect on every old input')
        p_report=float(np.linalg.norm(Vp[report,0])**2-np.linalg.norm(Vm[report,0])**2)
        need(abs(p_report+p*delta_q)<1e-12,
             'actual failure-dummy projector has nonzero normalized first source')
        overlap=float(np.dot(Vp[fail,0],Vm[fail,0]))
        trace_fail=2*math.sqrt(max(0.,p*p-overlap*overlap))
        need(abs(trace_fail-2*p*abs(math.sin(2*ep)))<2e-10,
             'full retained h=0 pure failure-state trace distance')
        success=np.diag([w*((a+p)*math.cos(ep)+(a-p)*math.sin(ep)),
                         w*((a+p)*math.cos(ep)-(a-p)*math.sin(ep))])
        need(np.max(abs(Sp-a*p*p*success))<4e-12,'true h=1 success block')
        need(np.max(abs(Fp-np.eye(2)*Fp[0,0]))<1e-12,'true failure protects arbitrary old input')
        need(np.max(abs(Fp-Fm))<4e-12,'fresh passive routing dummy has even cosine overlap')
        need(np.max(abs(Sp-np.diag(np.diag(Sm)[::-1])))<4e-12,'success blocks exchange')
        need(np.max(abs(Cp-np.diag(np.diag(Cm)[::-1])))<4e-12,'full cut includes actual h=0 and h=1')
        if first is None:first=float(Fp[0,0]/math.cos(ep))
        need(abs(first-alpha0)<3e-12,'exact Golden expression for full failure branch')
        need(abs(Fp[0,0]-first*math.cos(ep))<4e-12,'same failure overlap at all q')
        # I8 is old dirty-port/Spin with verified actual Z route.
        def J(C):return -8*np.linalg.slogdet(np.eye(2)-z*(np.eye(2)-mm(C.T,C)))[1]
        need(abs(J(Cp)-J(Cm))<3e-15,'all h branches full rank-16 J even')
        out.append({'q':q,'turn':m,'t':ep,'h0_failure_return':float(Fp[0,0]),
                    'h0_dummy_report_delta':p_report,
                    'h0_dummy_report_delta_over_unconditional_success_signal':p_report/(p*p*delta_q),
                    'h0_full_failure_trace_distance':trace_fail,
                    'h1_success_return_diag':np.diag(Sp).tolist(),
                    'full_rank16_feedback_abs_difference':abs(J(Cp)-J(Cm))})
    return {'status':'PASS: all h branches on explicitly guarded logical word; ideal Toffoli conditional',
        'native_source_sha256':digest,'old_input_rank_with_dirty_port_spin':16,
        'h_success_probability':p*p,'h_failure_probability':p,
        'h_failure_overlap_coefficient_alpha0':first,'h_failure_overlap_formula':'alpha0*cos(t)',
        'h_failure_alpha0_exact':'p*a*(p*a*p^2*(1+f1)+p^4*(p+f1)); f1=a*(2*p^2+p^4)',
        'h_success_multiplier':a*p*p,
        'literal_gate_inventory_excluding_four_Toffoli_factories':{'births':8,'G':'q+4','CX':31,'SourceI':4,'ideal_Toffoli':4},
        'first_success_more_than_one_attempt_compiled':False,
        'four_Toffoli_factories_and_failures_compiled':False,
        'separate_known_one_for_Toffoli_factories_available':False,
        'full_CQ_printing_and_clock_compiled':False,
        'Book03_Info_or_cost_derived':False,'GR_closed':False,'checks':out}

if __name__=='__main__':print(json.dumps(main(),indent=2))
