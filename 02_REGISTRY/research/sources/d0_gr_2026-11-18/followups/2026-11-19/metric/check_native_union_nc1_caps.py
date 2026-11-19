"""NC1 union-flag interface and a conditional O(delta^2) factory bound.

The physical all-path growing clock and actual Book03 tariffs are not computed.
The bound assumes every successful marked-factory transcript implements the
specified unitary on the protected input and has a scalar effect there.
"""
import json
import math
import numpy as np
import mpmath as mp


def need(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    p=(math.sqrt(5)-1)/2
    a=math.sqrt(p)
    G=np.array([[a,-p],[p,a]])
    X=np.array([[0.,1.],[1.,0.]])
    CX=np.array([[1.,0.,0.,0.],[0.,1.,0.,0.],[0.,0.,0.,1.],[0.,0.,1.,0.]])
    V=CX@np.kron(np.eye(2),G)@CX@np.kron(np.eye(2),np.array([[a],[p]]))
    P0=np.diag([1.,1.,0.,0.]);P10=np.diag([0.,0.,1.,0.]);P11=np.diag([0.,0.,0.,1.])
    effects=[V.T@P@V for P in (P0,P10,P11)]
    targets=[np.diag([1.,0.]),np.diag([0.,1.]),np.zeros((2,2))]
    effect_error=max(np.max(np.abs(x-y)) for x,y in zip(effects,targets))
    need(effect_error<2e-15,'native NC1 effects')
    need(np.max(np.abs(V[:,0]-np.kron([1.,0.],G@np.array([a,p]))))<2e-15,'tail at zero')
    need(np.max(np.abs(V[:,1]-np.array([0.,0.,1.,0.])))<2e-15,'tail at one')
    # Arbitrary entangled flag/RIGHT vector: each measured branch is the
    # corresponding input projector with its native conditional tail.
    rng=np.random.default_rng(19061)
    max_error=0.
    for _ in range(50):
        psi=rng.normal(size=6)+1j*rng.normal(size=6);psi/=np.linalg.norm(psi)
        W=np.kron(V,np.eye(3))@psi
        for branch,P in enumerate((P0,P10)):
            got=np.kron(P,np.eye(3))@W
            inp=psi.reshape(2,3)[branch]
            tail=G@np.array([a,p]) if branch==0 else np.array([1.,0.])
            want=np.kron(np.kron(np.eye(2)[branch],tail),inp)
            max_error=max(max_error,float(np.linalg.norm(got-want)))
    need(max_error<2e-15,'NC1 exact on entangled RIGHT')

    mp.mp.dps=100
    pp=(mp.sqrt(5)-1)/2
    sigma3=16*pp**9
    records={}
    for n in (2,8,20,40,80):
        m=16;d=pp**(n+1);M=m*(2*n+2)+2*(m-1)
        # Each of the three summands has budget delta^2/3.
        budget=d*d/3
        def first_below(fn):
            j=0
            while fn(j)>budget:j+=1
            return j
        l1=first_below(lambda j:pp**j)
        l2=first_below(lambda j:6*M*pp**(6*j))
        l3=first_below(lambda j:M*(1-sigma3)**j)
        b1=1-pp**l1;b2=1-pp**(6*l2);b3=1-(1-sigma3)**l3
        beta=b2**6*b3
        fail=1-b1*beta**M
        upper=pp**l1+M*(6*pp**(6*l2)+(1-sigma3)**l3)
        need(fail<=upper and upper<=d*d,'all factory flags, union bound')
        q=1-(1-d)**m
        m_pre=m*n+(m-1);m_post=m*(n+2)+(m-1)
        need(m_pre+m_post==M,'all physical Toffoli positions')
        reach=b1*beta**m_pre
        not_reach=1-reach
        post_failure=reach*(1-beta**m_post)
        ready=reach*beta**m_post
        need(abs(not_reach+post_failure+ready-1)<mp.mpf('1e-90'),'pre/post stop masses')
        need(abs(not_reach+post_failure-fail)<mp.mpf('1e-90'),'all failure classes retained')
        # Worst possible pair of normalized failure states contributes <=2 fail.
        bound=2*(1-fail)*q+2*fail
        need(bound<=2*m*d+2*d*d,'full trace norm bound including failure')
        records[str(n)]={'m':m,'logical_toffoli_M':M,'delta':float(d),
            'toffoli_before_NC1':m_pre,'toffoli_after_NC1':m_post,
            'report_reach_probability':float(reach),'post_report_failure_probability':float(post_failure),
            'cap_one_l1':l1,'cap_x_l2':l2,'cap_ccz_l3':l3,
            'max_x_cycles':4*M*l2,'max_cz_attempts':2*M*l2,'max_ccz_attempts':M*l3,
            'factory_success':float(1-fail),'failure_probability':float(fail),
            'union_bound_failure':float(upper),'delta_squared':float(d*d),
            'full_trace_difference_bound_over_delta':float(bound/d)}
    out={'status':'PASS; conditional successful-transcript and factory assumptions',
         'nc1_effect_error':effect_error,'entangled_RIGHT_branch_error':max_error,
         'nc1_forbidden_11_dark':True,'union_PVM_logical_flags':'0,10',
         'failure_classes_preserved_not_simulated':True,'caps':records,
         'successful_environment_independent_requires_full_unitary_channel':True,
         'all_factory_success_maps_verified_here':False,
         'full_growing_clock_and_Book03_price_computed':False,'GR_closed':False}
    print(json.dumps(out,indent=2,ensure_ascii=False))


if __name__=='__main__':main()
