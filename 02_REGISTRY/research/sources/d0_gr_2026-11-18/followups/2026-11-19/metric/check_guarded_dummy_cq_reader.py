"""Actual NC1 on guarded W, complete input cut and separately declared CQ.

Four marked Toffolis are still ideal logical letters. The RAW cut uses the
coherent dilation, not an already compiled irreversible printer or full
factory-expanded Book03 clock.
"""
import json, math, subprocess, sys
from pathlib import Path
import numpy as np
import mpmath as mp
from check_source_price import need
from check_local_gibbs_records import mm


def main():
    root=Path(__file__).resolve().parent
    parent=json.loads(subprocess.check_output([sys.executable,'-B','-W','error',str(root/'check_guarded_complement_full_branch.py')],text=True))
    p=(math.sqrt(5)-1)/2;a=math.sqrt(p);ell=math.log(1/p)
    G=np.array([[a,-p],[p,a]]);Z=np.diag([1.,-1.])
    def birth(V,n):return np.einsum('ij,k->ikj',V,[a,p]).reshape((1<<(n+1),2))
    def local(V,n,w,A):
        T=V.reshape([2]*n+[2]);T=np.moveaxis(T,w,0);T=np.tensordot(A,T,axes=(1,0))
        return np.moveaxis(T,0,w).reshape((1<<n,2))
    def toggle(V,n,cs,t):
        idx=np.arange(1<<n);on=np.ones(1<<n,dtype=bool)
        for w in cs:on &= (idx&(1<<(n-1-w)))!=0
        dest=idx^np.where(on,1<<(n-1-t),0);out=np.empty_like(V);out[dest]=V;return out
    def cx(V,n,c,t):return toggle(V,n,(c,),t)
    def fredkin(V,n,c,x,y):return cx(toggle(cx(V,n,y,x),n,(c,x),y),n,y,x)
    def nc1(V,n,c,t):return cx(local(cx(V,n,c,t),n,t,G),n,c,t)
    def word(q,side):
        V=E=np.eye(2);n=1
        V=birth(V,n);E=birth(E,n);n+=1  # h
        V=birth(V,n);E=birth(E,n);n+=1  # tail h
        V=nc1(V,n,1,2)
        V=birth(V,n);E=birth(E,n);n+=1  # D
        V=birth(V,n);E=birth(E,n);n+=1  # W
        V=fredkin(V,n,1,0,3)
        V=birth(V,n);E=birth(E,n);n+=1  # H
        V=cx(V,n,3,5);V=fredkin(V,n,1,5,4)
        if side<0:V=local(V,n,4,Z)
        for _ in range(q):V=local(V,n,4,G)
        V=local(V,n,4,Z)
        if side>0:V=local(V,n,4,Z)
        V=fredkin(V,n,1,5,4)
        V=birth(V,n);E=birth(E,n);n+=1;V=nc1(V,n,5,6)  # tail H
        V=birth(V,n);E=birth(E,n);n+=1                 # Q
        V=cx(V,n,1,7);V=local(V,n,7,G);V=cx(V,n,1,7)
        V=cx(V,n,1,7);V=cx(V,n,5,7)
        V=birth(V,n);E=birth(E,n);n+=1;V=nc1(V,n,7,8)  # tail Q
        V=fredkin(V,n,1,0,3)
        oldC=mm(E.T,V)
        V=birth(V,n);E=birth(E,n);n+=1                 # actual fresh W tail
        V=nc1(V,n,4,9)
        need(n==10 and np.max(abs(mm(V.T,V)-np.eye(2)))<2e-12,'all full input columns')
        C=mm(E.T,V);need(np.max(abs(C-a*oldC))<2e-12,'additional NC1 passive overlap a I')
        ids=np.arange(1<<n);bit=lambda w:(ids>>(n-1-w))&1
        h,H,Q,W=bit(1),bit(5),bit(7),bit(4);T=bit(9)
        need(np.linalg.norm(V[(W==1)&(T==1)])<2e-12,'new W NC1 dark on every input')
        # Both possible unnormalized W outcomes, split by already retained h,
        # are exactly the actual projective effects on the full input.
        effects={}
        for hh in (0,1):
            for ww in (0,1):
                sub=V[(h==hh)&(W==ww)]
                effects[hh,ww]=mm(sub.T,sub)
        # Full declared classical receipt includes every h,H,Q,W report;
        # all other quantum environments and the old P remain in pure branches.
        x=np.array([1.,1.])/math.sqrt(2);psi=np.einsum('ij,j->i',V,x,optimize=False);probs={}
        for hh in (0,1):
          for Hh in (0,1):
           for Qq in (0,1):
            for ww in (0,1):
             mask=(h==hh)&(H==Hh)&(Q==Qq)&(W==ww)
             probs[hh,Hh,Qq,ww]=float(np.vdot(psi[mask],psi[mask]).real)
        need(abs(sum(probs.values())-1)<2e-12,'all four actual NC1 output flags retained')
        ent=-sum(w*math.log(w) for w in probs.values() if w>1e-28)/ell
        code=sum((4+hh+Hh+Qq+ww)*prob for (hh,Hh,Qq,ww),prob in probs.items())
        return C,effects,code-ent,probs
    z=2**-20
    def J(C):return -8*np.linalg.slogdet(np.eye(2)-z*(np.eye(2)-mm(C.T,C)))[1]
    mp.mp.dps=90;pp=(mp.sqrt(5)-1)/2;aa=mp.sqrt(pp);ll=mp.log(1/pp)
    fx=lambda x:1+x-(-x*mp.log(x)-(1-x)*mp.log(1-x))/ll
    rows=[]
    for x in parent['checks']:
        q=int(x['q']);m=int(x['turn']);t=q*math.asin(p)-2*math.pi*m
        Cp,Ep,pricep,_=word(q,1);Cm,Em,pricem,_=word(q,-1)
        need(abs(J(Cp)-J(Cm))<3e-15,'both h outcomes full rank16 RAW parity')
        u=a*p*math.sin(2*t);v=p*p*math.cos(t)**2+p*math.sin(t)**2
        for hh in (0,1):
            wp=v+u if hh==0 else p*p;wm=v-u if hh==0 else p*p
            mass=p if hh==0 else p*p
            need(np.max(abs(Ep[hh,1]-mass*wp*np.eye(2)))<2e-12 and
                 np.max(abs(Em[hh,1]-mass*wm*np.eye(2)))<2e-12,
                 'all actual W NC1 effects on arbitrary oldRIGHT')
        dt=q*mp.asin(pp)-2*mp.pi*m;uv=aa*pp*mp.sin(2*dt)
        vv=pp**2*mp.cos(dt)**2+pp*mp.sin(dt)**2
        declared=pp*(fx(vv+uv)-fx(vv-uv));delta_q=2*uv
        need(abs((pricep-pricem)-float(declared))<2e-12,
             'all h,H,Q,W 0/10 codes and CQ entropy; no omitted branch')
        ratio=declared/(pp**2*delta_q)
        rows.append({'q':q,'turn':m,'t':mp.nstr(dt,20),
          'all_record_code_minus_CQ_secant':mp.nstr(ratio,20),
          'secant_divided_by_t_squared':mp.nstr(ratio/dt**2,20),
          'RAW_J_plus_minus_abs_difference':abs(J(Cp)-J(Cm)),
          'full_CQ_direct_difference':pricep-pricem})
    result={'status':'PASS: actual added W NC1, full input cut and declared full classical receipt',
      'native_parent_guarded_word_replayed':True,'old_input_rank_including_dirty_port_spin':16,
      'both_h_branches_and_all_h_H_Q_W_CQ_receipts_counted':True,
      'W_NC1_added_births':1,'W_NC1_added_CX':2,'W_NC1_added_G':1,
      'coherent_passive_RAW_return_multiplicative_factor':a,
      'declared_code_CQ_secant_over_unconditional_success_signal_limit':0,
      'rate_limit_per_t_squared':str(1/(3*pp*ll)),
      'printed_CQ_cut_identified_with_coherent_RAW_cut':False,
      'four_Toffoli_factory_failures_expanded':False,'Book03_cost_and_Info_selected':False,
      'GR_closed':False,'checks':rows}
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
