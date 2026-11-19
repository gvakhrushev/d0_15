"""One real branching clock for H, N and N xor H, with both NC1 outputs."""
import json
import math
import numpy as np
import scipy.sparse as sparse

from check_source_price import load_control, need
from check_local_gibbs_records import scene,scene_heat


def main():
    ne,digest=load_control(); Gate=ne.Gate
    p,a=float(ne.P),float(ne.A)
    source=dict(profile=ne.G_CX_SOURCE_I,source_port=1,source_spin=(2,3))
    invH=ne.inverse_word(ne.Execution(7,(),(),(Gate('G',(6,)),),**source),
                         max_qubits=13,max_expanded_stages=300)
    invN=ne.inverse_word(ne.Execution(10,(),(),(Gate('G',(9,)),),**source),
                         max_qubits=13,max_expanded_stages=300)
    invB=ne.inverse_word(ne.Execution(11,(),(),(Gate('G',(10,)),),**source),
                         max_qubits=13,max_expanded_stages=300)
    local={'G':np.array(ne.G_LOCAL,dtype=float),
           'SourceI':np.array(ne.SOURCE_I_LOCAL,dtype=float),
           'CX':np.array([[1.,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])}
    cache={}; stages=[]; current=4
    def matrix(n,g):
        key=(n,g.op,g.wires)
        if key in cache:return cache[key]
        A=local[g.op];shifts=tuple(n-1-w for w in g.wires);rows=[];cols=[];data=[]
        for col in range(1<<n):
            k=0
            for shift in shifts:k=2*k+((col>>shift)&1)
            for out in range(A.shape[0]):
                value=A[out,k]
                if value:
                    row=col
                    for j,shift in enumerate(shifts):
                        bit=(out>>(len(shifts)-1-j))&1
                        row=(row&~(1<<shift))|(bit<<shift)
                    rows.append(row);cols.append(col);data.append(value)
        M=sparse.csr_matrix((data,(rows,cols)),shape=(1<<n,1<<n))
        cache[key]=M;return M
    def birth():
        nonlocal current
        B=sparse.kron(sparse.eye(1<<current,format='csr'),
                      sparse.csr_matrix(np.array([[a],[p]])),format='csr')
        stages.append((B,B,'birth'));current+=1
    def append(g):
        A=matrix(current,g)
        stages.append((A,sparse.eye(1<<current,format='csr'),g.op))
    def nc1(control,tail):
        append(Gate('CX',(control,tail)));append(Gate('G',(tail,)));append(Gate('CX',(control,tail)))
    # Old input: T, port, and two arbitrary Spin wires. H is tried once.
    birth();birth();nc1(4,5)             # H, H-tail, then H's actual NC1
    birth()
    for g in invH:append(g)
    append(Gate('CX',(4,6)))             # retained H environment
    birth();append(Gate('CX',(0,7)))     # N controlled by old T
    birth();nc1(7,8)                     # genuine N readout
    measurement_cut=len(stages)
    birth()
    for g in invN:append(g)
    append(Gate('CX',(7,9)))             # retained N environment
    birth()
    for g in invB:append(g)
    append(Gate('CX',(7,10)))            # NB=N xor H, all H outcomes
    append(Gate('CX',(4,10)))
    birth();nc1(7,11)                    # actual terminal N NC1
    birth();nc1(10,12)                   # actual terminal NB NC1
    # Paid neutral pairs maintain a long closed-time winding after last birth.
    for _ in range(20):
        append(Gate('CX',(0,7)));append(Gate('CX',(0,7)))
    need(current==13 and sum(s[2]=='birth' for s in stages)==9,'all nine actual births')
    need(sum(s[2]=='SourceI' for s in stages)==12,'all real inverse words')
    # Representative full official 9-qubit matrices verify the bit embedding.
    verifier=ne.Execution(9,(),(),(),**source)
    for g in (Gate('G',(8,)),Gate('CX',(0,7)),Gate('SourceI',(1,2,3))):
        official=np.array(ne.gate_matrix(verifier,g,max_qubits=9,max_expanded_stages=300),dtype=float)
        need(np.max(np.abs(matrix(9,g).toarray()-official))<1e-14,'native alphabet/wire order')

    # Complete actual input and passive initial cut on all old columns.
    V=np.eye(16);E=np.eye(16)
    for physical,passive,_ in stages:
        V=physical@V;E=passive@E
    need(V.shape==(8192,16),'all final work and old input columns')
    need(np.max(np.abs(np.einsum('ki,kj->ij',V,V)-np.eye(16)))<1e-12,
         'complete initialized isometry')
    C=np.einsum('ki,kj->ij',E,V)
    F=np.eye(16)-np.einsum('ki,kj->ij',C,C);F=(F+F.T)/2
    eig=np.linalg.eigvalsh(F)
    need(eig.min()>-1e-12 and eig.max()<1+1e-12,'actual complete feedback effect')
    z=2**-20;J=-sum(math.log1p(-z*x) for x in eig)
    ix=np.arange(8192)
    T=(ix>>12)&1;H=(ix>>8)&1;ht=(ix>>7)&1;he=(ix>>6)&1
    N=(ix>>5)&1;nt=(ix>>4)&1;nenv=(ix>>3)&1;NB=(ix>>2)&1;no=(ix>>1)&1;bo=ix&1
    bad=((H!=he)|(N!=nenv)|(NB!=(N^H))|((H==1)&(ht==1))|
         ((N==1)&(nt==1))|((N==1)&(no==1))|((NB==1)&(bo==1)))
    need(np.linalg.norm(V[bad,:])<1e-12,'both record environments and all actual NC1 branches')
    for h in (0,1):
      for n in (0,1):
        block=V[(H==h)&(N==n),:]
        eff=np.einsum('ki,kj->ij',block,block)
        ph=(p*p if h else p)
        q0=(p*p if n else p);q1=(p if n else p*p)
        expected=np.diag([ph*q0]*8+[ph*q1]*8)
        need(np.max(np.abs(eff-expected))<1e-12,'full H,N outcome effect on oldRIGHT carrier')
    # Independently project the actual NC1 H and N outcomes at their cut,
    # propagate all later physical letters, and compare with the orthogonal
    # retained H/N environment sectors of the unmeasured full dilation.
    partial=np.eye(16)
    for physical,_,_ in stages[:measurement_cut]:
        partial=physical@partial
    need(partial.shape==(512,16),'actual first two NC1 measurement cut')
    mid=np.arange(512);mh=(mid>>4)&1;mht=(mid>>3)&1
    mn=(mid>>1)&1;mnt=mid&1
    need(np.linalg.norm(partial[((mh==1)&(mht==1))|((mn==1)&(mnt==1)),:])<1e-12,
         'all actually forbidden H/N outcomes are dark')
    measurement_error=0.
    for h in (0,1):
      for n in (0,1):
        branch=partial.copy();branch[(mh!=h)|(mn!=n),:]=0
        for physical,_,_ in stages[measurement_cut:]:
            branch=physical@branch
        retained=V.copy();retained[(he!=h)|(nenv!=n),:]=0
        measurement_error=max(measurement_error,float(np.linalg.norm(branch-retained)))
    need(measurement_error<1e-12,'exact PVM branches versus retained environments')

    # Build the exact temporal block graph, all born-complement targets, and
    # its full dimension. Local stage-isometry + nested orthogonal complement
    # identity proves unitary without allocating a D-by-D dense matrix.
    pre=stages[:-1];dims=[16]+[s[0].shape[0] for s in pre]
    D=sum(dims); count=len(dims)
    targets=[0]+[j+1 for j,s in enumerate(pre) if s[2]=='birth']
    L=min(count-j for j in targets)
    need(L>=40 and count==len(stages),'all real clock stages and last birth age')
    # Stage algebra: the Golden birth has unit norm, G and CX and SourceI are
    # full unitaries; their embeddings and cut closure preserve orthogonality.
    need(abs(a*a+p*p-1)<1e-14,'all birth maps isometric')
    for name in ('G','CX','SourceI'):
        A=local[name]
        need(np.max(np.abs(np.einsum('ki,kj->ij',A,A)-np.eye(A.shape[0])))<1e-14,
             'native primitive full-column unitarity')
    B,diag=scene();beta=2*p*p;x=beta/11;quadrature=128
    avg=sum(scene_heat(B,diag,2*math.cos(2*math.pi*j/quadrature),beta)
            for j in range(quadrature))/quadrature
    per=359+2*float(np.trace(avg));ZH=D*per
    halo=lambda n:2*x**n/(math.factorial(n)*(1-x/(n+1)))
    trunc=D*66*(halo(L)+halo(quadrature))
    need(trunc<1e-20,'full two-grade heat trace truncation')

    # All outcomes recorded: H is independent of N given old T; NB=N xor H.
    # Hence H,N contribute exactly two binary entropies, not three.
    ell=math.log(1/p);hh=lambda x:-x*math.log(x)-(1-x)*math.log1p(-x)
    need(abs(hh(p*p)/ell-(1+p*p))<1e-13,'golden entropy exact')
    q=.37;Nmean=p*p+p**3*q;NBmean=p*p+p**3*Nmean
    cost=3+p*p+Nmean+NBmean
    net=cost-2*hh(p*p)/ell
    expected_net=1+2*p*Nmean
    need(abs(net-expected_net)<1e-12,'all-record full conditional code-CQ')
    slope=2*p**4
    need(abs(slope-(p**3+p**6))<1e-13,'all-record source includes H0 continuation')
    print(json.dumps({
      'status':'PASS','native_source_sha256':digest,
      'old_input_dimension':16,'final_work_dimension':8192,
      'born_wires':9,'stages':len(stages),
      'G_calls':sum(t=='G' for _,_,t in stages),
      'CX_calls':sum(t=='CX' for _,_,t in stages),
      'SourceI_calls':sum(t=='SourceI' for _,_,t in stages),
      'clock_dimension':D,'full_two_degree_modes':425*D,'minimum_return':L,
      'clock_isometry':'full-stage and nested-complement theorem; not numerically materialized',
      'heat_trace_central':round(ZH,6),'heat_analytic_truncation_upper':'{:.6e}'.format(trunc),
      'feedback_eigenvalues':[round(float(x),12) for x in eig],
      'feedback_J':round(J,15),'native_both_record_instrument_all_columns':True,
      'PVM_H_N_versus_retained_environment_error':measurement_error,
      'P_H1':round(p*p,12),'H1_pair_complementary':True,'H0_pair_identical':True,
      'H0_continues_instead_of_early_abort':True,
      'three_terminal_codes_are_declared_not_physically_printed':True,
      'declared_all_record_source_wrt_q':round(slope,12),
      'H1_only_pair_length_source_wrt_q':0,
      'conditional_HN_marker_source_requires_joint_readout_or_new_Toffoli':True,
      'Book_CostInfo_identified':False,'full_BALANCED_FACTORY_clock':False,
      'GR_closed':False,
    },sort_keys=True,indent=2))


if __name__=='__main__':main()
