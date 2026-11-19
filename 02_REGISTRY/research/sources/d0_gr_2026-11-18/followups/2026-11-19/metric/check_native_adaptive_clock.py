"""One native growing clock with recorded outcome and adaptive continuation."""
import json
import math
import numpy as np
import scipy.sparse as sparse

from check_source_price import load_control, need
from check_local_gibbs_records import scene, scene_heat


def main():
    ne, digest = load_control()
    Gate = ne.Gate
    p, a = float(ne.P), float(ne.A)
    source = dict(profile=ne.G_CX_SOURCE_I, source_port=2, source_spin=(3,4))
    # T,target,port,spin,spin are old; N, tail, flag, environment are born.
    one_flag = ne.Execution(8, (), (), (Gate('G',(7,)),), **source)
    one_env = ne.Execution(9, (), (), (Gate('G',(8,)),), **source)
    one_tail = ne.Execution(9, (), (), (Gate('G',(6,)),), **source)
    inv_flag = ne.inverse_word(one_flag,max_qubits=9,max_expanded_stages=200)
    inv_env = ne.inverse_word(one_env,max_qubits=9,max_expanded_stages=200)
    inv_tail = ne.inverse_word(one_tail,max_qubits=9,max_expanded_stages=200)

    # Square gates are verbatim native primitives; every inverse is expanded.
    stages = []
    current = 5
    descriptions = []
    gate_cache = {}
    G = np.array(ne.G_LOCAL,dtype=float)
    SI = np.array(ne.SOURCE_I_LOCAL,dtype=float)
    CX = np.array([[1.,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
    local = {'G':G, 'CX':CX, 'SourceI':SI}
    def matrix(n,g):
        key=(n,g.op,g.wires)
        if key in gate_cache:
            return gate_cache[key]
        A = local[g.op]
        shifts = tuple(n-1-w for w in g.wires)
        rr=[]; cc=[]; vals=[]
        for col in range(1<<n):
            incoming=0
            for shift in shifts:
                incoming=2*incoming+((col>>shift)&1)
            for outgoing in range(A.shape[0]):
                val=A[outgoing,incoming]
                if val:
                    row=col
                    for j,shift in enumerate(shifts):
                        bit=(outgoing>>(len(shifts)-1-j))&1
                        row=(row&~(1<<shift))|(bit<<shift)
                    rr.append(row);cc.append(col);vals.append(val)
        result=sparse.csr_matrix((vals,(rr,cc)),shape=(1<<n,1<<n))
        gate_cache[key]=result
        return result
    def birth():
        nonlocal current
        v=sparse.csr_matrix(np.array([[a],[p]]))
        birth_map=sparse.kron(sparse.eye(1<<current,format='csr'),v,format='csr')
        stages.append((birth_map,birth_map,'birth'))
        descriptions.append(('birth',current))
        current+=1
    def append(g):
        mat=matrix(current,g)
        stages.append((mat,sparse.eye(1<<current,format='csr'),g.op))
        descriptions.append((g.op,g.wires))
    birth()                                   # N
    append(Gate('CX',(0,5)))                  # field T -> N
    birth()                                   # TN
    for g in (Gate('CX',(5,6)),Gate('G',(6,)),Gate('CX',(5,6))):append(g)
    birth()                                   # flag, then genuinely prepare |0>
    for g in inv_flag:append(g)
    append(Gate('CX',(5,7)))                  # retained outcome flag
    birth()                                   # independent environment |0>
    for g in inv_env:append(g)
    append(Gate('CX',(7,8)))                  # complete orthogonal dilation
    append(Gate('CX',(7,1)))                  # adaptive data action
    for g in inv_tail:append(g)
    append(Gate('CX',(7,6)))
    for g in inv_tail:append(g)
    append(Gate('CX',(7,6)))                  # tail correction, last gate
    need(current==9, 'four actual births')
    need(sum(g[2]=='birth' for g in stages)==4, 'birth inventory')
    need(sum(g[2]=='SourceI' for g in stages)==16, 'real source-I inverse words')
    # Independent comparison with native exact-matrix implementation on full
    # 512 columns for representative local primitives and their wire order.
    verifier=ne.Execution(9,(),(),(),**source)
    for g in (Gate('G',(6,)),Gate('CX',(7,6)),Gate('SourceI',(2,3,4))):
        ref=np.array(ne.gate_matrix(verifier,g,max_qubits=9,max_expanded_stages=200),dtype=float)
        need(np.max(np.abs(matrix(9,g).toarray()-ref))<1e-14, 'native primitive agreement')

    # All 32 old input columns, with no restriction on target, port or Spin.
    V=np.eye(32)
    E=np.eye(32)
    for real,passive,_ in stages:
        V=real@V
        E=passive@E
    need(np.max(np.abs(np.einsum('ki,kj->ij',V,V)-np.eye(32)))<1e-12,
         'full initialized history is an isometry')
    C=np.einsum('ki,kj->ij',E,V)
    # The output isometry below gives these two exact target-space blocks.
    c0=a**5*np.eye(2)+a*p**4*np.array([[0.,1.],[1.,0.]])
    c1=p**3*np.eye(2)+p**4*np.array([[0.,1.],[1.,0.]])
    expected_C=sparse.block_diag((np.kron(c0,np.eye(8)),np.kron(c1,np.eye(8)))).toarray()
    need(np.max(np.abs(C-expected_C))<1e-12,'full prepared-input return blocks')
    pp, aa = ne.P, ne.A
    exact_checks=((aa**5+aa*pp**4)**2-5*pp**7,
                  (aa**5-aa*pp**4)**2-pp**7,
                  (pp**3+pp**4)**2-pp**4,
                  (pp**3-pp**4)**2-pp**10)
    need(all(ne.GOLDEN_FIELD.from_sympy(t)==ne.GOLDEN_FIELD.zero for t in exact_checks),
         'exact algebraic return eigenvalues')
    F=np.eye(32)-np.einsum('ki,kj->ij',C,C)
    F=(F+F.T)/2
    fvals=np.linalg.eigvalsh(F)
    need(fvals.min()>-1e-12 and fvals.max()<1+1e-12,'complete physical feedback effect')
    expected_f=np.sort(np.repeat([1-5*p**7,1-p**4,1-p**7,1-p**10],8))
    need(max(abs(fvals-expected_f))<1e-12,'four algebraic feedback eigenvalues')
    z=2**-20
    J=-sum(math.log1p(-z*x) for x in fvals)
    need(J>=0,'full adaptive-history determinant')
    # Last wires are N,TN,flag,environment, in that order.
    ix=np.arange(512)
    n=(ix>>3)&1; tail=(ix>>2)&1; flag=(ix>>1)&1; env=ix&1
    bad=((n!=flag)|(flag!=env)|(tail!=0))
    need(np.linalg.norm(V[bad,:])<1e-12,'all actual flag/env/tail branches retained')
    # Full two-branch output map, not merely outcome probabilities; target is
    # flipped iff the recorded flag is one, while port and Spin are unchanged.
    expected_V=np.zeros((512,32))
    for col in range(32):
        t=(col>>4)&1
        for nvalue in (0,1):
            amp=(a if nvalue==t else p)
            old_out=col^(nvalue<<3)
            row=(old_out<<4)|(nvalue<<3)|(nvalue<<1)|nvalue
            expected_V[row,col]=amp
    need(np.max(np.abs(V-expected_V))<1e-12,'complete recorded dilation on all old columns')

    # Measure the true NC1 instrument immediately after its three gates and
    # propagate each unnormalised sector. It agrees with reading the retained
    # environment at the end for the actual initialized subspace.
    partial=np.eye(32)
    for real,_,_ in stages[:6]:
        partial=real@partial
    need(partial.shape==(128,32),'actual NC1 measurement cut')
    bits=np.arange(128); nh=(bits>>1)&1; th=bits&1
    invalid=(nh==1)&(th==1)
    need(np.linalg.norm(partial[invalid,:])<1e-12,'NC1 invalid sector dark on all inputs')
    measurement_error=0.
    for outcome in (0,1):
        sector=partial.copy()
        sector[nh!=outcome,:]=0
        for real,_,_ in stages[6:]:
            sector=real@sector
        final=V.copy()
        final[env!=outcome,:]=0
        measurement_error=max(measurement_error,float(np.linalg.norm(sector-final)))
    need(measurement_error<1e-12,'true P0/P1 instrument versus orthogonal flag/environment')
    effect=[]
    for value in (0,1):
        block=V[flag==value,:]
        effect.append(np.einsum('ki,kj->ij',block,block))
    expected1=np.diag([p*p]*16+[p]*16)
    expected0=np.eye(32)-expected1
    need(np.max(np.abs(effect[0]-expected0))<1e-12,'full old-input no-click effect')
    need(np.max(np.abs(effect[1]-expected1))<1e-12,'full old-input click effect')

    # Construct ONE complete growing clock, including every birth complement.
    prefix=stages[:-1]
    last=stages[-1][0]
    dims=[32]+[s[0].shape[0] for s in prefix]
    offsets=np.cumsum([0]+dims)
    D=int(offsets[-1]); clock_len=len(dims)
    rows=[];cols=[];data=[]
    def put(block,row,col):
        coo=block.tocoo()
        rows.extend((coo.row+row).tolist());cols.extend((coo.col+col).tolist())
        data.extend(coo.data.tolist())
    for j,(real,_,_) in enumerate(prefix):
        put(real,offsets[j+1],offsets[j])
    emb=sparse.eye(512,format='csr')
    targets=[]
    for j in range(len(prefix),-1,-1):
        if j < len(prefix):
            emb=emb@prefix[j][1]
        if j==0:
            extra=sparse.eye(dims[j],format='csr')
        elif prefix[j-1][2]=='birth':
            B=prefix[j-1][1]
            extra=sparse.eye(dims[j],format='csr')-B@B.T
        else:
            continue
        block=extra@emb.T@last
        if block.nnz:
            targets.append(j)
            put(block,offsets[j],offsets[-2])
    clock=sparse.coo_matrix((data,(rows,cols)),shape=(D,D)).tocsr()
    error=clock.T@clock-sparse.eye(D,format='csr')
    max_unit=float(max(abs(error.data))) if error.nnz else 0.
    need(max_unit<2e-12,'all early birth complements and clock stages unitary')
    L=min(clock_len-j for j in targets)
    need(L>=32,'minimum real return after final birth')
    B,sc=scene(); beta=2*p*p; x=beta/11
    Q=128
    average=sum(scene_heat(B,sc,2*math.cos(2*math.pi*j/Q),beta) for j in range(Q))/Q
    per_dimension=359+2*float(np.trace(average))
    local_bound=2*x**L/(math.factorial(L)*(1-x/(L+1)))
    quadrature_bound=2*x**Q/(math.factorial(Q)*(1-x/(Q+1)))
    ZH=D*per_dimension
    heat_abs_bound=D*66*(local_bound+quadrature_bound)
    need(heat_abs_bound<1e-20,'full adaptive heat bound')
    # True relative weights of N are p² and p in the old T sectors.
    need(abs((p-p*p)-p**3)<1e-14,'actual registered source')
    print(json.dumps({
      'status':'PASS','native_source_sha256':digest,
      'old_input_dimension':32,'final_work_dimension':512,
      'births':4,'total_physical_stages':len(stages),
      'source_i_calls':sum(x[2]=='SourceI' for x in stages),
      'G_calls':sum(x[2]=='G' for x in stages),
      'CX_calls':sum(x[2]=='CX' for x in stages),
      'clock_dimension':D,'full_two_grade_modes':425*D,
      'clock_nonzeros':int(clock.nnz),'clock_unitarity_error':max_unit,
      'clock_minimum_return':L,
      'heat_trace_central':round(ZH,8),
      'heat_trace_analytic_truncation_upper':'{:.6e}'.format(heat_abs_bound),
      'feedback_rank_input':32,
      'feedback_eigenvalues':[round(float(q),12) for q in fvals],
      'feedback_eigenvalues_algebraic':['1-5*p^7','1-p^4','1-p^7','1-p^10'],
      'feedback_J':round(J,15),
      'click_given_T0':round(p*p,12),'click_given_T1':round(p,12),
      'record_code_CQ_gain':round(p**3,12),
      'all_actual_outcomes_and_orthogonal_environment_retained':True,
      'invalid_N1_TN1_probability_on_all_old_input_columns':0,
      'recorded_instrument_dilation_error':measurement_error,
      'invalid_ambient_columns_have_a_distinct_flag':False,
      'full_BALANCED_FACTORY_adaptive_clock':False,
      'physical_Book_CostInfo_identified':False,'GR_closed':False,
    },sort_keys=True,indent=2))


if __name__=='__main__':
    main()
