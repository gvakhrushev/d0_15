"""Complete local CX/SourceI and complemented-NC1 work-response map.

Native matrix prefixes, first recorded NC1 as a retained CQ direct sum, and
all independent old P/port/Spin input operators are retained. Pauli insertions
are a basis for conditional mean-local-work models, not selected D0 tariffs.
"""
import json
import math
import numpy as np
import scipy.linalg as la
from check_source_price import load_control


def need(c, m):
    if not c:
        raise AssertionError(m)


def mm(a,b):
    return np.einsum('ij,jk->ik',a,b,optimize=False)


I=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex)
Z=np.diag([1.,-1.]).astype(complex)
pauli={'I':I,'X':X,'Y':Y,'Z':Z}


def all_words(n):
    result=[('',np.array([[1.]],complex))]
    for _ in range(n):
        result=[(s+k,np.kron(v,m)) for s,v in result for k,m in pauli.items()]
    return result


def embedded1(g,wire,n):
    out=np.array([[1.]],complex)
    for j in range(n):out=np.kron(out,g if j==wire else I)
    return out


def born(n, v):
    return np.kron(np.eye(1<<n),v.reshape((2,1)))


def local_pull(v, dv, wires, n, basis):
    # Return V* K V and its derivative, summed over all CQ branches.
    labels=list(wires)+[i for i in range(n) if i not in wires]+[n]
    dim=1<<len(wires)
    env=1<<(n-len(wires))
    result=np.zeros((len(basis),16,16),complex)
    value=np.zeros((len(basis),16,16),complex)
    pm=np.stack([x[1] for x in basis])
    for x,dx in zip(v,dv):
        x=x.reshape([2]*n+[16]).transpose(labels).reshape((dim,env,16))
        dx=dx.reshape([2]*n+[16]).transpose(labels).reshape((dim,env,16))
        # K[a,b], sum conj(x[a]) K[a,b] dx[b] and its adjoint.
        tmp=np.einsum('aei,kab,bej->kij',x.conj(),pm,dx,optimize=True)
        result += tmp+tmp.transpose(0,2,1).conj()
        value += np.einsum('aei,kab,bej->kij',x.conj(),pm,x,optimize=True)
    return value,result


def certify_rank_38_mod_prime(ne, witnesses):
    """Exact specialization of Q(a,i), a^4+a^2-1=0, to F_1009.

    The 38 one-hot witness images occur at the first real CX and the first
    real SourceI of the first Z route. Their nonzero diagonal 38-minor mod a
    good prime certifies rank >=38 in characteristic zero. The structural
    old-port/Spin split proves the matching upper bound independently.
    """
    modulus=1009
    aa=226
    ii=469
    pp=aa*aa%modulus
    need((aa**4+aa**2-1)%modulus==0 and (ii*ii+1)%modulus==0,
         'valid Q(a,i) finite-field specialization')
    ident=np.eye(2,dtype=np.int64)
    xp=np.array([[0,1],[1,0]],dtype=np.int64)
    yp=np.array([[0,-ii],[ii,0]],dtype=np.int64)%modulus
    zp=np.diag([1,-1]).astype(np.int64)%modulus
    mp={'I':ident,'X':xp,'Y':yp,'Z':zp}
    def product(a,b):return (a@b)%modulus
    def tensor(lst):
        r=np.array([[1]],dtype=np.int64)
        for a in lst:r=np.kron(r,a)%modulus
        return r
    def local(mark,wires,n):
        parts=[ident]*n
        for ch,wire in zip(mark,wires):parts[wire]=mp[ch]
        return tensor(parts)
    spec_args=dict(profile=ne.G_CX_SOURCE_I,source_port=1,source_spin=(2,3))
    def native(op,w):
        g=ne.Gate(op,tuple(w))
        spec=ne.Execution(5,(),(),(g,),**spec_args)
        return np.asarray(ne.gate_matrix(spec,g,max_qubits=5,max_expanded_stages=10),
                          dtype=np.int64)%modulus
    birth=np.kron(np.eye(16,dtype=np.int64),np.array([[aa],[pp]],dtype=np.int64))
    v0=product(native('CX',(0,4)),birth)
    generator=np.array([[0,-1],[1,0]],dtype=np.int64)%modulus
    gen=tensor([ident,ident,ident,ident,generator])
    dv0=product(gen,v0)
    cx1=native('CX',(4,1));cx2=native('CX',(1,4));source=native('SourceI',(1,2,3))
    u0=cx1
    u3=product(source,product(cx1,product(cx2,cx1)))
    states={'z0_0_CX':(product(u0,v0),product(u0,dv0),(4,1)),
            'z0_3_SourceI':(product(u3,v0),product(u3,dv0),(1,2,3))}
    inverse=pow((8*aa*pp)%modulus,-1,modulus)
    checked=[]
    for w in witnesses:
        need(w['stage'] in states,'exact witness uses first route only')
        v,dv,wires=states[w['stage']]
        k=local(w['mark'],wires,5)
        effect=(product(v.T,product(k,dv))+product(dv.T,product(k,v)))%modulus
        effect=effect*inverse%modulus
        target=tensor([mp[ch] for ch in w['output']])
        val=w['coefficient']
        magnitude=(pow(2,-1,modulus) if abs(abs(val)-.5)<1e-12
                   else aa*pp*pow(4,-1,modulus)%modulus)
        scalar=(magnitude if val>0 else -magnitude)%modulus
        need(scalar!=0 and np.array_equal(effect,scalar*target%modulus),
             'exact modular one-hot witness '+w['output'])
        checked.append(w['output'])
    need(len(set(checked))==38,'exact nonzero 38-minor')
    return {'prime':modulus,'a_root':aa,'imaginary_root':ii,
            'p_mod_prime':pp,'distinct_nonzero_witnesses':len(checked)}


def run():
    ne,digest=load_control()
    p=float(ne.P);a=float(ne.A);v0=np.array([a,p],complex)
    J=np.array([[0.,-1.],[1.,0.]],complex)
    spec_args=dict(profile=ne.G_CX_SOURCE_I,source_port=1,source_spin=(2,3))
    cache={}
    def gate(n,op,w):
        key=(n,op,tuple(w))
        if key not in cache:
            g=ne.Gate(op,tuple(w))
            spec=ne.Execution(n,(),(),(g,),**spec_args)
            cache[key]=np.array(ne.gate_matrix(spec,g,max_qubits=8,max_expanded_stages=100),complex)
        return cache[key]
    p1=all_words(1);p2=all_words(2);p3=all_words(3)
    old_basis=all_words(3)
    output_basis=[(lead+lab,np.kron(pauli[lead],m)) for lead in ('I','Z') for lab,m in old_basis]
    output_mats=np.stack([m for _,m in output_basis])
    idx_trace=[j for j,(label,_) in enumerate(output_basis) if label!='IIII']

    def trajectory(plus,epsilon=0.):
        n=4
        states=[np.eye(16,dtype=complex)];derivs=[np.zeros((16,16),complex)]
        results={}
        def apply(u,du=None):
            nonlocal states,derivs
            if du is None:du=np.zeros_like(u)
            prev=states
            states=[mm(u,w) for w in prev]
            derivs=[mm(du,w)+mm(u,dw) for w,dw in zip(prev,derivs)]
        def birth(label):
            nonlocal n
            u=born(n,v0);apply(u);n+=1
            results[label]=local_pull(states,derivs,[n-1],n,p1)
        def stage(label,op,w):
            u=gate(n,op,w);apply(u)
            results[label]=local_pull(states,derivs,list(w),n,p1 if len(w)==1 else p2 if len(w)==2 else p3)
        def x_from_h(label,w):
            # Exact restriction of the actual CX(h,w) to independently
            # prepared, untouched h=|1>, including any one-wire Q mark.
            apply(embedded1(X,w,n))
            results[label]=local_pull(states,derivs,[w],n,p1)
        def rotation():
            # At epsilon=0 the q repeated native Gs have product I, and
            # d/d epsilon G^q = J on H; all G-stage marks are owned separately.
            rot=np.array([[math.cos(epsilon),-math.sin(epsilon)],
                          [math.sin(epsilon),math.cos(epsilon)]],complex)
            apply(embedded1(rot,4,n),embedded1(mm(J,rot),4,n))
        def zroute(k):
            for i,(op,w) in enumerate([('CX',(4,1)),('CX',(1,4)),('CX',(4,1)),
                                       ('SourceI',(1,2,3)),('SourceI',(1,2,3)),
                                       ('CX',(4,1)),('CX',(1,4)),('CX',(4,1))]):
                stage('z%d_%d_%s'%(k,i,op),op,w)
        birth('birth_H')
        stage('initial_CX','CX',(0,4))
        for k in range(2):
            if not plus:zroute(2*k)
            rotation()
            zroute(2*k+1 if not plus else 2*k)
            if plus:zroute(2*k+1)
        birth('birth_A')
        stage('H_NC1_1','CX',(4,5));stage('H_NC1_2','G',(5,));stage('H_NC1_3','CX',(4,5))
        # Actual readout makes an orthogonal retained CQ direct sum. On the
        # supported state, the 0/10 projectors coincide with H=0/1.
        proj0=embedded1((I+Z)/2,4,n);proj1=embedded1((I-Z)/2,4,n)
        need(max(np.max(np.abs(mm(proj0,w)+mm(proj1,w)-w)) for w in states)<1e-12,'PVM completeness')
        states=[mm(proj0,states[0]),mm(proj1,states[0])]
        derivs=[mm(proj0,derivs[0]),mm(proj1,derivs[0])]
        birth('birth_Q')
        x_from_h('Q_prep_X1',6);stage('Q_prep_G','G',(6,));x_from_h('Q_prep_X2',6)
        x_from_h('Q_make_one',6);stage('Q_xor_H','CX',(4,6))
        birth('birth_B')
        stage('Q_NC1_1','CX',(6,7));stage('Q_NC1_2','G',(7,));stage('Q_NC1_3','CX',(6,7))
        # The second recorded Q is a direct sum; its projectors sum to I.
        # No physical mark follows it in this bounded writer.
        return results,states,derivs,n

    plus,sp,dsp,n=trajectory(True);minus,sm,dsm,n2=trajectory(False)
    need(n==n2==8 and plus.keys()==minus.keys(),'same full writer and paired stage labels')
    scale=1/(8*a*p)  # Delta q=2ap sin(4 epsilon), derivative 8ap.
    rows=[];metadata=[];stage_stats={}
    comm=np.kron(Z,np.eye(8))
    maxherm=maxcomm=0.
    for name in plus:
        dif=(plus[name][1]-minus[name][1])*scale
        for j,A in enumerate(dif):
            maxherm=max(maxherm,float(np.max(np.abs(A-A.conj().T))))
            maxcomm=max(maxcomm,float(np.max(np.abs(mm(comm,A)-mm(A,comm)))))
            coeff=np.real(np.einsum('iab,ba->i',output_mats,A,optimize=True))/16
            rows.append(coeff);metadata.append((name,j))
        traceless=np.delete(np.real(np.einsum('iab,kba->ki',output_mats,dif,optimize=True))/16,0,axis=1)
        stage_stats[name]={'basis_count':int(len(dif)),
             'traceless_coefficient_frobenius':float(np.linalg.norm(traceless)),
             'max_traceless_coefficient':float(np.max(np.abs(traceless)))}
    need(maxherm<1e-10 and maxcomm<1e-10,'all effects Hermitian and P-program block diagonal')
    rows=np.asarray(rows)
    rank_all=int(np.linalg.matrix_rank(rows,tol=1e-9))
    rank_traceless=int(np.linalg.matrix_rank(rows[:,idx_trace],tol=1e-9))
    route=[i for i,(label,_) in enumerate(metadata) if label.startswith('z')]
    suffix=[i for i,(label,_) in enumerate(metadata) if not label.startswith('z') and label not in ('birth_H','initial_CX')]
    rank_route=int(np.linalg.matrix_rank(rows[route][:,idx_trace],tol=1e-9))
    rank_suffix=int(np.linalg.matrix_rank(rows[suffix][:,idx_trace],tol=1e-9))
    need(max(stage_stats['birth_H']['max_traceless_coefficient'],stage_stats['initial_CX']['max_traceless_coefficient'])<1e-14,'common prefix cancels')
    # h->Q restriction must preserve the known-one factor exactly; no claim on
    # the actual (separate) heralded preparation or failure branches is made.
    # Explicit normalized remaining preparation row for each mark is its
    # coefficient of Z_P tensor any old-port/Spin Pauli, retained in JSON.
    p_rows=[i for i,(lab,_) in enumerate(output_basis) if lab[0]=='Z']
    p_rank=int(np.linalg.matrix_rank(rows[:,p_rows],tol=1e-9))
    singular_values=la.svdvals(rows)
    need(singular_values[37]>0.9 and singular_values[38]<1e-10,
         'numerical rank has separated nonzero and zero singular values')
    # SourceI's active port is precisely the current H; the dirty old port
    # sits on wire H throughout the SourceI pair. Other marks act on H/port
    # only before or after both SourceI letters, so spin has been restored.
    # Thus only P⊗(port-local + Spin-local) Pauli labels are possible.
    allowed=set()
    for lead in ('I','Z'):
        for lab,_ in old_basis:
            if lab[0]=='I' or lab[1:]=='II':allowed.add(lead+lab)
    need(len(allowed)==38,'38-dimensional structural upper space')
    forbidden=[i for i,(lab,_) in enumerate(output_basis) if lab not in allowed]
    need(np.max(np.abs(rows[:,forbidden]))<1e-10,'every actual mark lies in structural upper space')
    # Scalar and all 37 traceless columns are each generated by an individual
    # local Pauli mark, with coefficient ±1/2 or ±ap/4. Their orthogonal
    # one-hot witnesses give a structural rank-38 proof in characteristic 0;
    # the finite-field check below independently verifies the exact algebra.
    exact_witnesses=[]
    local_letters='IXYZ'
    for lab in sorted(allowed):
        target=next(i for i,(s,_) in enumerate(output_basis) if s==lab)
        matches=[]
        for j,row in enumerate(rows):
            nz=np.flatnonzero(np.abs(row)>1e-10)
            if len(nz)==1 and nz[0]==target:
                matches.append(j)
        need(matches,'one-hot witness for '+lab)
        j=matches[0]; stage,idx=metadata[j]
        count=3 if 'SourceI' in stage else 2 if 'CX' in stage else 1
        basis_words=list(all_words(count))
        val=rows[j,target]
        need(min(abs(abs(val)-.5),abs(abs(val)-a*p/4))<1e-12,
             'witness exact algebraic coefficient')
        exact_witnesses.append({'output':lab,'stage':stage,'mark':basis_words[idx][0],
                                'coefficient':float(val)})
    modular_certificate=certify_rank_38_mod_prime(ne,exact_witnesses)
    # A concrete physical local pair: the first actual CX is H->port and
    # I+X_H X_port is positive semidefinite. Its scalar I component cancels.
    xx_index=next(i for i,(name,_) in enumerate(p2) if name=='XX')
    example_row=rows[metadata.index(('z0_0_CX',xx_index))]
    expected=np.zeros(len(output_basis))
    expected[next(i for i,(label,_) in enumerate(output_basis) if label=='ZIII')]=a*p/4
    need(np.max(np.abs(example_row-expected))<1e-12,
         'first actual CX positive mark has exact P source ap/4 Z_P')
    # Re-evaluate every local basis insertion at three actual finite natively
    # reachable angles; the G^q product equals R(epsilon), and prior owners
    # independently replay all individual G calls and port routes literally.
    finite=[]
    theta=math.asin(p)
    for q,turn in ((19,2),(66,7),(613,65)):
        epsilon=q*theta-2*math.pi*turn
        fp,_,_,_=trajectory(True,epsilon)
        fm,_,_,_=trajectory(False,epsilon)
        delta=2*a*p*math.sin(4*epsilon)
        largest=0.
        for name in plus:
            exact_limit=(plus[name][1]-minus[name][1])*scale
            current=(fp[name][0]-fm[name][0])/delta
            largest=max(largest,float(np.max(np.abs(current-exact_limit))))
        # After the first CX(H,port), its XX mark pulls back to X_H.
        # Exact finite secant includes a scalar term plus the physical Z_P
        # preparation row; the I part of the positive mark I+XX cancels.
        cx_current=(fp['z0_0_CX'][0][xx_index]-fm['z0_0_CX'][0][xx_index])/delta
        scalar=(math.cos(2*epsilon)-1)/math.sin(4*epsilon)
        zcoeff=a*p/(4*math.cos(2*epsilon))
        expected_cx=scalar*np.eye(16)+zcoeff*comm
        need(np.max(np.abs(cx_current-expected_cx))<1e-10,
             'finite positive first-CX mark on entire old input')
        finite.append({'q':q,'turns':turn,'epsilon':epsilon,'delta_q':delta,
                       'max_operator_entry_error':largest,
                       'first_CX_scalar_coefficient':scalar,
                       'first_CX_ZP_coefficient':zcoeff})
    need(finite[2]['max_operator_entry_error']<finite[1]['max_operator_entry_error']<finite[0]['max_operator_entry_error'],
         'all-mark finite source map converges along checked native pairs')
    print(json.dumps({'status':'PASS','scope':'conditional complete additive local work maps, no selected Book03 tariff',
      'native_source_sha256':digest,'old_input_dimension':16,'h_fixed_to_independently_heralded_one':True,
      'first_NC1_retained_CQ_branches':2,'Z_routes_CX':24,'Z_routes_SourceI':8,
      'local_mark_basis_count':int(len(rows)),'route_basis_count':len(route),'suffix_basis_count':len(suffix),
      'max_hermiticity_error':maxherm,'max_P_commutator_error':maxcomm,
      'complete_local_work_linear_map_rank':rank_all,'traceless_source_map_rank':rank_traceless,
      'route_traceless_source_rank':rank_route,'suffix_traceless_source_rank':rank_suffix,
      'independent_P_source_map_rank':p_rank,'smallest_nonzero_singular_value':float(singular_values[37]),
      'largest_zero_singular_value':float(singular_values[38]),
      'exact_structural_basis':sorted(allowed),'one_hot_rank_witnesses':exact_witnesses,
      'modular_38_rank_lower_certificate':modular_certificate,
      'positive_first_CX_mark':'I + X_H X_port',
      'positive_first_CX_normalized_operator':'(a p / 4) Z_P',
      'positive_first_CX_d_dt_with_t_Pr_P1':-a*p/2,
      'full_local_map_checked_at_native_finite_pairs':finite,
      'output_basis':[x[0] for x in output_basis],
      'stage_statistics':stage_stats,
      'operator_map_sparse_rows':[{'stage':stage,'basis_index':idx,
          'coefficients':{output_basis[j][0]:float(value)
                          for j,value in enumerate(row) if abs(value)>1e-12}}
          for (stage,idx),row in zip(metadata,rows)],
      'field_dependent_local_marks_included':False,'known_one_prep_failure_and_printer_cost_included':False,
      'complete_Book03_source_computed':False,'GR_closed':False},ensure_ascii=False,indent=2))


if __name__=='__main__':run()
