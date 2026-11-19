"""Exact successful fixed-clock realization of the typed balanced output.

Six original suffix wires and three reusable dummy wires are really born on
both H branches. Toffoli factories, their failure branches and full physical
cost are not simulated; the check is on their successful logical action.
"""
import json
from collections import Counter
import numpy as np
import mpmath as mp
from check_source_price import load_control, need
from check_local_gibbs_records import scene,scene_heat


def main():
    ne, digest = load_control()
    Gate = ne.Gate
    p, a = float(ne.P), float(ne.A)
    source = dict(profile=ne.G_CX_SOURCE_I, source_port=1, source_spin=(2,3))
    def inv(n,wire):
        return ne.inverse_word(ne.Execution(n,(),(),(Gate('G',(wire,)),),**source),max_qubits=13,max_expanded_stages=300)
    prefix = [None,None,Gate('CX',(4,5)),Gate('G',(5,)),Gate('CX',(4,5)),None,*inv(7,6),Gate('CX',(4,6))]
    suffix = [Gate('CX',(0,7)),Gate('CX',(7,8)),Gate('G',(8,)),Gate('CX',(7,8)),
              *inv(10,9),Gate('CX',(7,9)),*inv(11,10),Gate('CX',(7,10)),Gate('CX',(4,10)),
              Gate('CX',(7,11)),Gate('G',(11,)),Gate('CX',(7,11)),
              Gate('CX',(10,12)),Gate('G',(12,)),Gate('CX',(10,12))]
    need(len(prefix)==18 and sum(g is None for g in prefix)==3,'real H prefix')
    counts=Counter(g.op for g in suffix)
    need(counts==Counter({'CX':22,'G':5,'SourceI':8}),'un-padded native suffix')
    special=[g for g in suffix if 4 in g.wires]
    need(len(special)==1 and special[0].op=='CX' and tuple(special[0].wires)==(4,10),'H special gate')
    occurrence=sum(len(g.wires) for g in suffix if 4 not in g.wires)
    need(occurrence==71,'all data wire routes counted')

    G=np.array(ne.G_LOCAL,dtype=float)
    SI=np.array(ne.SOURCE_I_LOCAL,dtype=float)
    CX=np.array([[1.,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
    mats={'G':G,'CX':CX,'SourceI':SI}

    def birth(V):
        return np.einsum('ij,k->ikj',V,np.array([a,p])).reshape(V.shape[0]*2,V.shape[1])
    def gate(V,n,wires,U):
        # Full-column operation, including arbitrary old port and Spin.
        q=len(wires); rest=[i for i in range(n) if i not in wires]
        axes=list(wires)+rest+[n]
        v=V.reshape([2]*n+[V.shape[1]]).transpose(axes)
        w=np.einsum('ij,jk->ik',U,v.reshape(1<<q,-1),optimize=False)
        shape=[2]*n+[V.shape[1]]
        return w.reshape(shape).transpose(np.argsort(axes)).reshape(V.shape)
    def swap0(V,n,h,u,v):
        ix=np.arange(1<<n,dtype=np.uint32)
        hm=np.uint32(1<<(n-1-h));um=np.uint32(1<<(n-1-u));vm=np.uint32(1<<(n-1-v))
        cond=((ix&hm)==0)&(((ix&um)!=0)^((ix&vm)!=0))
        src=ix^np.where(cond,um|vm,np.uint32(0))
        return V[src]
    # Independent Fredkin-zero gate template, for each of eight inputs.
    for h in (0,1):
      for u in (0,1):
       for v in (0,1):
        x,y=u,v
        x^=y;y^=x;x^=y            # unconditional physical SWAP, 3 CX
        x^=y;y^=(h&x);x^=y        # positive Fredkin, 2 CX + Toffoli
        need((x,y)==((v,u) if h==0 else (u,v)),'negative Fredkin exact')

    V=np.eye(16); E=np.eye(16); n=4
    for g in prefix:
        if g is None:
            V=birth(V);E=birth(E);n+=1
        else:
            V=gate(V,n,g.wires,mats[g.op])
    need(n==7,'H registered before remaining births')
    ix7=np.arange(1<<7);hh=(ix7>>2)&1;ht=(ix7>>1)&1;he=ix7&1
    need(np.max(np.abs(V[(hh!=he)|((hh==1)&(ht==1))]))<1e-12,
         'true H NC1 sectors retained in H environment; forbidden outcome dark')
    for _ in range(9):
        V=birth(V);E=birth(E);n+=1
    need(n==16 and V.shape==(65536,16),'all six suffix and three shared dummies are born')
    initial=V.copy()
    # Actual route: two Fredkin-zero gates around each declared native U.
    def routed(V,ops):
        for g in ops:
            wires=tuple(g.wires)
            if 4 in wires:
                V=gate(V,n,wires,mats[g.op]);continue
            for w,d in zip(wires,(13,14,15)):
                V=swap0(V,n,4,w,d)
            V=gate(V,n,wires,mats[g.op])
            for w,d in reversed(list(zip(wires,(13,14,15)))):
                V=swap0(V,n,4,w,d)
        return V
    # At the H1 branch after the true initial N-NC1, insert its actual PVM.
    # H0 has no N measurement and its six wires stay in their pure input.
    Ncut=routed(V,suffix[:4])
    V=routed(Ncut,suffix[4:])
    # Independently execute each primitive on the data in H=1 and on three
    # shared dummy wires in H=0. Dummies are NOT reset between gates.
    test=initial.copy(); rows=np.arange(1<<n,dtype=np.uint32)
    hmask=((rows>>(n-1-4))&1).astype(bool)
    for g in suffix:
        wires=tuple(g.wires)
        real=gate(test,n,wires,mats[g.op])
        if 4 in wires:
            test=real
        else:
            shadow=gate(test,n,tuple((13,14,15)[:len(wires)]),mats[g.op])
            test=np.where(hmask[:,None],real,shadow)
    err=float(np.max(np.abs(V-test)))
    need(err<1e-12,'all 16 protected-input columns, no dummy reset')
    need(np.max(np.abs(np.einsum('ki,kj->ij',V,V,optimize=False)-np.eye(16)))<1e-12,'complete logical success isometry')
    # Complete effects, treating private H=0 idle wires and dummy as quantum
    # output, not discarding them. N=1 is read only on H=1.
    N=((rows>>(n-1-7))&1).astype(bool)
    effects=[]
    for mask in (~hmask,hmask&~N,hmask&N):
        block=V[mask];effects.append(np.einsum('ki,kj->ij',block,block,optimize=False))
    rr=p*p
    expected=[p*np.eye(16),rr*np.diag([p]*8+[rr]*8),rr*np.diag([rr]*8+[p]*8)]
    effect_err=max(float(np.max(np.abs(x-y))) for x,y in zip(effects,expected))
    need(effect_err<1e-12,'all three typed effects on full old carrier')
    E_N=((rows>>(n-1-9))&1).astype(bool)
    pvm_err=0.
    for value in (False,True):
        isolated=Ncut.copy()
        isolated[~(hmask & (N==value))]=0
        actual=routed(isolated,suffix[4:])
        retained=V.copy();retained[~(hmask & (E_N==value))]=0
        pvm_err=max(pvm_err,float(np.max(np.abs(actual-retained))))
    need(pvm_err<1e-12,'true N measurement sectors equal actual retained environment')
    # H=0 conditional environment is exactly the same for all old columns:
    # matrix support is confined to unchanged T,port,Spin and common vector.
    old=(rows>>(n-4))&15
    common=None
    for col in range(16):
        need(np.max(np.abs(V[(~hmask)&(old!=col),col]))<1e-12,'H0 keeps old carrier')
        segment=V[(~hmask)&(old==col),col]
        if common is None:common=segment
        else:need(np.max(np.abs(segment-common))<1e-12,'H0 dummy and idle wires independent of old input')

    C=np.einsum('ki,kj->ij',E,V,optimize=False)
    F=np.eye(16)-np.einsum('ki,kj->ij',C,C,optimize=False);F=(F+F.T)/2
    eig=np.linalg.eigvalsh(F);z=2**-20
    need(eig.min()>-1e-12 and eig.max()<1+1e-12,'full-cut feedback logical word')
    J=-sum(np.log1p(-z*eig))
    mp.mp.dps=70;pm=(mp.sqrt(5)-1)/2
    b2=1-pm**384;b3=1-(1-16*pm**9)**64;beta=b2**6*b3
    prob=beta**(2*occurrence)
    num_stages=len(prefix)+9+len(suffix)+12*occurrence
    need(num_stages==914,'logical ideal stage count')
    # Full direct-sum dimension of this IDEAL logical word. Each explicitly
    # born wire contributes its actual complement. The last nine births are
    # followed by the full unpadded routed suffix; factory gates are not here.
    prefix_dim=0; nb=4
    for g in prefix:
        prefix_dim+=1<<nb
        if g is None:nb+=1
    for _ in range(9):
        prefix_dim+=1<<nb;nb+=1
    suffix_stages=len(suffix)+12*occurrence
    D=prefix_dim+suffix_stages*(1<<16)
    need(D==58197680 and suffix_stages==887,'entire ideal growing-clock dimension')
    B,sc=scene();beta_float=2*p*p
    avg=sum(scene_heat(B,sc,2*np.cos(2*np.pi*j/128),beta_float) for j in range(128))/128
    heat_central=D*(359+2*float(np.trace(avg)))
    x=2*pm**2/11
    bound=lambda k:66*D*2*x**k/(mp.factorial(k)*(1-x/(k+1)))
    tail_bound=bound(887)+bound(128)
    need(tail_bound<mp.mpf('1.1e-353'),'analytic winding and quadrature bound')
    print(json.dumps(dict(status='PASS',source_sha256=digest,old_input_columns=16,
      final_work_dimension=65536,prefix_real_stages=18,
      fresh_wires_after_prefix=9,shared_dummy_wires=3,old_suffix_wires_born_on_both_H_branches=6,
      suffix_native_ops=dict(counts),suffix_wire_occurrences=occurrence,
      routed_word_logical_Toffoli=2*occurrence,routed_word_logical_CX=9+22+10*occurrence,
      routed_word_logical_G=7,routed_word_logical_SourceI=12,
      ideal_word_births=12,ideal_word_stages=num_stages,
      success_branch_two_plane_error=err,typed_effect_operator_error=effect_err,
      N_pvm_versus_retained_environment_error=pvm_err,
      H0_dummy_history_depends_on_q=False,H0_actual_physical_clock_stops=False,
      site_or_oldRIGHT_measured=False,feedback_F_eigenvalues=[round(float(x),12) for x in eig],
      feedback_J=round(float(J),15),
      ideal_clock_dimension=D,ideal_full_two_degree_modes=425*D,
      ideal_minimum_return_lower_bound=887,ideal_clock_matrix_materialized=False,
      ideal_heat_trace_central=round(heat_central,5),
      ideal_heat_truncation_and_quadrature_upper=str(tail_bound),
      probability_all_142_Toffoli_if_independent=str(prob),
      all_failure_records_and_full_physical_clock_compiled=False,
      terminal_printer_compiled=False,Book_CostInfo_identified=False,GR_closed=False),indent=2))

if __name__=='__main__':
    main()
