"""Guarded h=0/1 direct-sum route/source transport on the full old input.

The four Fredkin Toffolis are ideal logical gates. Physical factories, their
separate known-one resource, actual Book03 prices and all other gates remain
unbound. No new cost is selected by this check.
"""
import json
import math
from pathlib import Path
import numpy as np
from check_source_price import load_control, need
from check_native_complement_route_work import all_words, born, embedded1, local_pull, mm


def main():
    ne,digest=load_control();p=float(ne.P);a=float(ne.A);v=np.array([a,p]);G=np.array([[a,-p],[p,a]])
    def append_birth(V,n):
        return np.einsum('ij,k->ikj',V,v).reshape((1<<(n+1),2))
    def apply_local(V,n,w,A):
        y=V.reshape([2]*n+[2]);y=np.moveaxis(y,w,0)
        y=np.tensordot(A,y,axes=(1,0));return np.moveaxis(y,0,w).reshape((1<<n,2))
    def toggle(V,n,controls,target):
        ind=np.arange(1<<n);selected=np.ones(1<<n,dtype=bool)
        for w in controls:selected &= (ind&(1<<(n-1-w)))!=0
        dst=ind^np.where(selected,1<<(n-1-target),0);out=np.empty_like(V);out[dst]=V
        return out
    def fredkin(V,n,c,x,y):
        V=toggle(V,n,(y,),x);V=toggle(V,n,(c,x),y);return toggle(V,n,(y,),x)
    def nc1(V,n,c,target):
        V=toggle(V,n,(c,),target);V=apply_local(V,n,target,G);return toggle(V,n,(c,),target)
    # Physical wires P,h,first NC1 tail,D,W,H, in actual chronological order.
    V=np.eye(2);n=1
    for _ in range(2):V=append_birth(V,n);n+=1
    V=nc1(V,n,1,2)
    for _ in range(2):V=append_birth(V,n);n+=1
    V=fredkin(V,n,1,0,3)
    V=append_birth(V,n);n+=1
    V=toggle(V,n,(3,),5)
    V=fredkin(V,n,1,5,4)
    need(n==6,'actual completed guarded prefix has six wires')
    ind=np.arange(1<<n);h=(ind>>(n-1-1))&1
    eye=np.eye(2)
    def ket(*vects):
        out=np.array([1.])
        for w in vects:out=np.kron(out,w)
        return out
    expected0=np.zeros_like(V);expected1=np.zeros_like(V)
    tail0=np.einsum('ij,j->i',G,v,optimize=False)
    for j in (0,1):
        x=ket(eye[:,j],eye[:,0],tail0,v,v,v)*a
        # h=0 completed Fredkin is identity; D controls H, W stays fresh v.
        expected0[:,j]=toggle(x.reshape((-1,1)),n,(3,),5)[:,0]
        # h=1 swaps input P into D and actual H into W; old P and W's
        # original independent inputs now occupy two fresh spectator slots.
        expected1[:,j]=ket(v,eye[:,1],eye[:,0],eye[:,j],(v if j==0 else v[::-1]),v)*p
    err0=float(np.max(np.abs(V*(h==0)[:,None]-expected0)))
    err1=float(np.max(np.abs(V*(h==1)[:,None]-expected1)))
    need(err0<2e-14 and err1<2e-14,'actual literal guarded prefixes and physical dummy identification')
    need(np.max(np.abs(mm(V.T,V)-np.eye(2)))<1e-14,'all first NC1 h outcomes kept')

    # Full writer with both real h outcomes: four physical logical Fredkins,
    # the two complete native words S±, both terminal NC1 and all births.
    # Actual Z route acts as Z_W tensor identity on every old dirty-port/Spin
    # column (separately replayed for all 896 marked route positions below).
    def full_writer(q,side):
        w=e=np.eye(2);n0=1
        for _ in range(2):
            w=append_birth(w,n0);e=append_birth(e,n0);n0+=1
        w=nc1(w,n0,1,2)
        for _ in range(2):
            w=append_birth(w,n0);e=append_birth(e,n0);n0+=1
        w=fredkin(w,n0,1,0,3)
        w=append_birth(w,n0);e=append_birth(e,n0);n0+=1
        w=toggle(w,n0,(3,),5);w=fredkin(w,n0,1,5,4)
        zmat=np.diag([1.,-1.])
        for _ in range(2):
            if not side:w=apply_local(w,n0,4,zmat)
            for j in range(q):w=apply_local(w,n0,4,G)
            w=apply_local(w,n0,4,zmat)
            if side:w=apply_local(w,n0,4,zmat)
        w=fredkin(w,n0,1,5,4)
        w=append_birth(w,n0);e=append_birth(e,n0);n0+=1
        w=nc1(w,n0,5,6)
        w=append_birth(w,n0);e=append_birth(e,n0);n0+=1
        w=toggle(w,n0,(1,),7);w=apply_local(w,n0,7,G);w=toggle(w,n0,(1,),7)
        w=toggle(w,n0,(1,),7);w=toggle(w,n0,(5,),7)
        w=append_birth(w,n0);e=append_birth(e,n0);n0+=1
        w=nc1(w,n0,7,8);w=fredkin(w,n0,1,0,3)
        need(n0==9 and np.max(np.abs(mm(w.T,w)-np.eye(2)))<3e-12,
             'complete two-sided guarded writer isometry')
        return w,e
    z=2**-20;feedback=[]
    for qq,turn in ((19,2),(66,7),(613,65)):
        wp,epass=full_writer(qq,True);wm,epass2=full_writer(qq,False)
        need(np.max(np.abs(epass-epass2))<1e-14,'same passive birth input for both full graphs')
        cp=mm(epass.T,wp);cm=mm(epass.T,wm)
        need(np.max(np.abs(cp-np.diag(np.diag(cm)[::-1])))<5e-12 and
             np.max(np.abs(cm-np.diag(np.diag(cp)[::-1])))<5e-12,
             'both retained h branches complete full input return swaps P sectors')
        def feedback_value(c):
            defect=1-np.diag(c)**2
            return float(-8*np.sum(np.log1p(-z*defect)))
        jp,jm=feedback_value(cp),feedback_value(cm)
        need(abs(jp-jm)<1e-16,'actual full rank-16 RAW feedback parity')
        nbits=9;ind=np.arange(1<<nbits);hh=(ind>>(nbits-1-1))&1;H=(ind>>(nbits-1-5))&1;Q=(ind>>(nbits-1-7))&1
        selected=(hh==1)&(H==1)
        delta_q=2*a*p*math.sin(4*(qq*math.asin(p)-2*math.pi*turn))
        effect=mm(wp[selected].T,wp[selected])-mm(wm[selected].T,wm[selected])
        need(np.max(np.abs(effect-p*p*delta_q*np.eye(2)))<3e-12,
             'actual unconditioned success-field step on all old P columns')
        # Full actual h,H,Q CQ output: the input |chi(t)> is pure and
        # every fully retained outcome branch remains pure. Three actual
        # codes 0/10 have total length 3+h+H+Q. This is a declared partial
        # code-CQ functional, not the selected original D0 cost/Info.
        vec=np.array([1.,1.])/math.sqrt(2)
        dvec=np.array([-1.,1.])/math.sqrt(2)
        ell=math.log(1/p)
        def cq_derivative(w):
            y=np.einsum('ij,j->i',w,vec,optimize=False)
            dy=np.einsum('ij,j->i',w,dvec,optimize=False);total=0.
            for ih in (0,1):
                for iH in (0,1):
                    for iQ in (0,1):
                        mask=(hh==ih)&(H==iH)&(Q==iQ)
                        prob=float(np.dot(y[mask],y[mask]))
                        dprob=float(2*np.dot(y[mask],dy[mask]))
                        if prob>1e-28:
                            total+=dprob*(3+ih+iH+iQ+(1+math.log(prob))/ell)
                        else:
                            need(abs(dprob)<1e-12,'zero-probability CQ branch has no first weight')
            return total
        actual_cq=(cq_derivative(wp)-cq_derivative(wm))/(p*p*delta_q)
        eps=qq*math.asin(p)-2*math.pi*turn
        D=a*p*math.sin(4*eps)
        expected_cq=p**3*math.cos(4*eps)/(D*ell)*math.log((.5+D)/(.5-D))
        need(abs(actual_cq-expected_cq)<2e-10,
             'both h branches full CQ independent-input source with real success normalization')
        feedback.append({'q':qq,'turn':turn,'full_feedback_plus':jp,
                          'full_feedback_minus':jm,'full_feedback_delta':jp-jm,
                          'unconditional_success_field_delta':p*p*delta_q,
                          'full_h_H_Q_code_CQ_independent_P_source':actual_cq})

    root=Path(__file__).resolve().parent
    data=json.loads((root/'native_complement_route_work_result.json').read_text())
    need(data['modular_38_rank_lower_certificate']['distinct_nonzero_witnesses']==38,
         'prior certified complete route-space basis')
    labels=data['output_basis'];pos={x:i for i,x in enumerate(labels)}
    route=[row for row in data['operator_map_sparse_rows'] if row['stage'].startswith('z')]
    need(len(route)==896,'all 24 CX and 8 SourceI local mark basis elements')
    original=np.zeros((len(route),len(labels)))
    for i,row in enumerate(route):
        for key,value in row['coefficients'].items():original[i,pos[key]]=value
    # On h=0, W=v, the same route map as the h=1 writer's old P=0
    # sector, extended by I_P.  The actual branch weights are p,p^2.
    # Normalize by the unconditioned registered-success signal p^2 Delta q.
    guard=np.zeros_like(original)
    for i,label in enumerate(labels):
        if label[0]=='I':
            mate=pos['Z'+label[1:]]
            guard[:,i]=(original[:,i]+p*original[:,mate])/(p*p)
        else:
            guard[:,i]=original[:,i]
    tr=[i for i,x in enumerate(labels) if x!='IIII']
    pr=[i for i,x in enumerate(labels) if x[0]=='Z']
    rank=int(np.linalg.matrix_rank(guard,tol=1e-9));ranktr=int(np.linalg.matrix_rank(guard[:,tr],tol=1e-9))
    rankp=int(np.linalg.matrix_rank(guard[:,pr],tol=1e-9))
    need((rank,ranktr,rankp)==(38,37,19),'inverted exact branch transform preserves route/source ranks')
    # Exact algebra: each of the 19 pairs (I_P B,Z_P B) transforms by
    # [[1,p],[0,p^2]] divided by p^2; determinant 1/p^2 != 0.
    need(p>0 and p*p>0,'nonzero exact 2x2 transform determinant')

    # Independently replay all 896 individual route marks at each finite pair.
    gatecache={};spec_args=dict(profile=ne.G_CX_SOURCE_I,source_port=1,source_spin=(2,3))
    def gate(op,w):
        key=(op,tuple(w))
        if key not in gatecache:
            g=ne.Gate(op,tuple(w));spec=ne.Execution(5,(),(),(g,),**spec_args)
            gatecache[key]=np.asarray(ne.gate_matrix(spec,g,max_qubits=5,max_expanded_stages=10),complex)
        return gatecache[key]
    p2,p3=all_words(2),all_words(3)
    native_CX=gate('CX',(0,4))
    initial=born(4,np.array([a,p],complex))
    J=np.array([[0,-1],[1,0]],complex)
    def actual(side, eps, conditional):
        x=mm(native_CX,initial) if conditional else initial.copy()
        z=np.zeros_like(x);out={}
        def rot(x):
            r=np.array([[math.cos(eps),-math.sin(eps)],[math.sin(eps),math.cos(eps)]],complex)
            return mm(embedded1(r,4,5),x)
        def routeblock(x,k):
            for j,(op,w) in enumerate([('CX',(4,1)),('CX',(1,4)),('CX',(4,1)),
                         ('SourceI',(1,2,3)),('SourceI',(1,2,3)),('CX',(4,1)),('CX',(1,4)),('CX',(4,1))]):
                x=mm(gate(op,w),x)
                values,_=local_pull([x],[z],list(w),5,p2 if op=='CX' else p3)
                out['z%d_%d_%s'%(k,j,op)]=values
            return x
        for k in range(2):
            if not side:x=routeblock(x,2*k)
            x=rot(x)
            x=routeblock(x,2*k+1 if not side else 2*k)
            if side:x=routeblock(x,2*k+1)
        return out
    finite=[];theta=math.asin(p);max_err=0.
    for q,m in ((19,2),(66,7),(613,65)):
        eps=q*theta-2*math.pi*m;dq=2*a*p*math.sin(4*eps)
        v0p,v0m=actual(True,eps,False),actual(False,eps,False)
        v1p,v1m=actual(True,eps,True),actual(False,eps,True)
        normerr=0.;representative=0.
        for r in route:
            name=r['stage'];i=r['basis_index']
            d0=(v0p[name][i]-v0m[name][i])/dq
            d1=(v1p[name][i]-v1m[name][i])/dq
            p0=np.kron(np.eye(2),d1[:8,:8])
            normerr=max(normerr,float(np.max(np.abs(d0-p0))))
            # Full guarded pullback = p*failure + p²*success, normalized
            # by actual unconditional success signal p²*Delta q.
            guarded=(p*d0+p*p*d1)/(p*p)
            transformed=(p*p*d1+p*p0)/(p*p)
            normerr=max(normerr,float(np.max(np.abs(guarded-transformed))))
            if name=='z0_0_CX' and i==5: # XX in IXYZ x IXYZ
                alpha=(math.cos(2*eps)-1)/math.sin(4*eps)
                zcoef=a*p/(4*math.cos(2*eps))
                expected=(alpha+p*zcoef)/(p*p)*np.eye(16)+zcoef*np.kron(np.diag([1.,-1.]),np.eye(8))
                representative=float(np.max(np.abs(guarded-expected)))
        need(normerr<1e-10 and representative<1e-10,'all guarded finite route effects and XX witness')
        max_err=max(max_err,normerr)
        finite.append({'q':q,'turn':m,'epsilon':eps,'conditional_field_delta':dq,
            'unconditional_success_delta':p*p*dq,'max_all_896_dummy_branch_error':normerr,
            'first_CX_XX_witness_error':representative})
    ell=math.log(1/p);cq_slope=4*p**3/ell;route_slope=-a*p/2
    print(json.dumps({'status':'PASS','native_source_sha256':digest,
      'actual_ideal_fredkin_prefix_h0_max_error':err0,'actual_ideal_fredkin_prefix_h1_max_error':err1,
      'both_h_outcomes_retained':True,'h0_probability':p,'h1_probability':p*p,
      'h0_W_equals_independent_v_on_all_old_inputs':True,
      'h1_W_equals_original_writer_with_old_P_in_D':True,
      'full_logical_word_inventory':{'births':8,'G':'2q+4','CX':43,'SourceI':8,'ideal_Toffoli':4},
      'route_basis_count':len(route),'conditional_delta_to_unconditional_success_delta':p*p,
      'guarded_route_map_rank':rank,'guarded_traceless_source_rank':ranktr,
      'guarded_independent_programme_source_rank':rankp,
      'exact_rank_proof':'prior 38 modular minor and invertible block [[1,p],[0,p²]]/p²',
      'first_CX_positive_mark':'I+X_W X_port',
      'first_CX_limit_normalized_by_unconditional_signal':'(a/4) I + (a p/4) Z_P',
      'first_CX_independent_P_slope':route_slope,
      'declared_complementary_CQ_independent_P_slope':cq_slope,
      'full_guarded_writer_raw_parity_all_h_outcomes':feedback,
      'all_route_finite_branch_checks':finite,
      'ideal_Toffoli_factories_and_extra_failure_branches_compiled':False,
      'Book03_cost_info_chosen':False,'full_guard_euler_and_GR_closed':False},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
