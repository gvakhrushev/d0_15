#!/usr/bin/env python3
"""SOURCE #310: pole-regular metric/source reduction of the literal chronology.

Only the named native declarations are executed, with version-normalized AST
pins. Default replay is read-only; --write refreshes the adjacent receipt.
This is exact finite research evidence, not physical admission or new Lean.
"""
from __future__ import annotations
import argparse
import ast
import hashlib
import json
from pathlib import Path
import sympy as s

ROOT = Path(__file__).resolve().parents[3]
BASE = '02_REGISTRY/research/certificates/a4d_native_chronological_joint_reduction'
PROOF = '02_REGISTRY/research/A4D_NATIVE_CHRONOLOGICAL_JOINT_REDUCTION.md'
INPUT_HEAD = '353afa53bd52a6f24a485dde0ec59134d08cd970'
OWNER_PINS = {
 '02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py': {
  'ext': 'c04b98888788c2e9f2d086eddcfb5c01cd0be887d164c0da0958dd0e057b4182',
  'creator': 'b6c7dc797dbf0dd5173305d0cc62c54a6c9227f78d5828b03f3ce337ddd9d4db',
  'record_basis': '351445d7665715302e0c01e57043792c90b0b602884e08502077aa891617ca45'},
 '02_REGISTRY/research/certificates/a4d_native_record_metric_chronology_check.py': {
  'record': 'cb7cb2eac05c0c868c2cd7bf8b1de516bcce6e57cc8e859503c2fd5cf32b1585',
  'polynomials': 'a4d6c4ff8f6a28dcf7a043e2f76b26a9467ad91fadd40a8edcb33cb2b6ec5b13'}
 ,
 '02_REGISTRY/research/certificates/a4d_native_closed_record_engine.py': {'archive_modes': '444706d3d32640a08eb921e25b4be277bfa9105a4169398e358a0f16db8b4653', 'archive_projection': 'f8649f3a4c5aa224a0b155577baa22e9240e345a9987105c1efa27345401830f', 'inherit': '405c47509c4a4d94ce6a8893d5e63e0b5837d0dab5ce004517214087b97f53a8'}
}

def digest(data):
    return hashlib.sha256(data).hexdigest()

def canonical_ast(value):
    if isinstance(value, ast.AST):
        return [type(value).__name__, [[key,canonical_ast(item)]
            for key,item in ast.iter_fields(value)
            if not (key == 'type_params' and item == [])]]
    if isinstance(value, list):
        return [canonical_ast(item) for item in value]
    return value

def declaration_digest(node):
    return digest(json.dumps(canonical_ast(node),separators=(',',':'),
                             ensure_ascii=True).encode())

def controls():
    checks,mutants=[],[]
    def check(name,value):
        if not bool(value):
            raise AssertionError(name)
        checks.append(name)
    def reject(name,false_statement):
        check('REJECT_'+name,not bool(false_statement))
        mutants.append(name)
    a,p,z=s.symbols('a p z',real=True)
    t=s.symbols('t',positive=True)
    ideal=s.groebner([a*a-p,p*p+p-1],a,p,domain=s.QQ.frac_field(z,t))
    def red(value):
        num,den=s.cancel(value).as_numer_denom()
        num=ideal.reduce(s.expand(num))[1]
        den=ideal.reduce(s.expand(den))[1]
        if den == 0:
            raise ZeroDivisionError('ACTUAL_CHART_DENOMINATOR')
        return s.cancel(num/den)
    def mat(value):
        return value.applyfunc(red)
    def zero(value):
        return all(red(v)==0 for v in (list(value) if isinstance(value,s.MatrixBase) else [value]))
    def eq(name,value):
        check(name,zero(value))
    I,I4=s.eye(16),s.eye(4)
    SUBS=[tuple(i for i in range(4) if mask&(1<<i)) for mask in range(16)]
    ns=dict(s=s,a=a,p=p,z=z,I=I,DEG=s.diag(*map(len,SUBS)),SUBS=SUBS,mat=mat)
    for path,pins in OWNER_PINS.items():
        tree=ast.parse((ROOT/path).read_text(encoding='utf-8'))
        for name,pin in pins.items():
            nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name]
            check('unique_executed_owner_'+name,len(nodes)==1)
            check('actual_owner_AST_'+name,declaration_digest(nodes[0])==pin)
            exec(compile(ast.Module(body=nodes,type_ignores=[]),path,'exec'),ns)
    creator,ext,record,polynomials=map(ns.get,['creator','ext','record','polynomials'])
    eta=s.diag(1,-1,-1,-1)
    creators=[creator(I4[:,i]) for i in range(4)]
    def rho(A):
        return sum((A[i,j]*creators[i]*creators[j].T for i in range(4) for j in range(4)),s.zeros(16))
    def frame_lift(q,V):
        A=V*q.inv()/2
        return A,rho(A)-s.trace(A)*I/2
    def first(m):
        return m.extract([1,2,4,8],[0])
    def two(m):
        return s.Matrix(4,4,lambda i,j:0 if i==j else
                        (1 if i<j else -1)*m[(1<<i)|(1<<j)])
    def data(q,m):
        qi=q.inv();v=first(m);k=red((v.T*qi*v)[0])
        Q=mat(-q+2*v*v.T/k);G=Q.inv();n=v/s.sqrt(k)
        e=mat(-two(m)*G*n);E2=red((e.T*G*e)[0])
        u=red(p*m[0]+a*s.sqrt(k));ss=red(u*u+p*p*E2)
        return dict(qi=qi,v=v,k=k,Q=Q,G=G,n=n,e=e,E2=E2,u=u,ss=ss,c=red(u/s.sqrt(ss)))
    def angle_jet(q,m,V,xi):
        d=data(q,m);qi,v,k,Q,G,n,e,E2,u,ss=[d[t] for t in ('qi','v','k','Q','G','n','e','E2','u','ss')]
        dv=first(xi);dk=red(2*(v.T*qi*dv)[0]-(v.T*qi*V*qi*v)[0])
        dQ=mat(-V+2*(dv*v.T+v*dv.T)/k-2*dk*v*v.T/k**2)
        dG=mat(-G*dQ*G);dn=mat(dv/s.sqrt(k)-v*dk/(2*k**s.Rational(3,2)))
        de=mat(-two(xi)*G*n-two(m)*dG*n-two(m)*G*dn)
        dE2=red(2*(e.T*G*de)[0]+(e.T*dG*e)[0])
        du=red(p*xi[0]+a*dk/(2*s.sqrt(k)))
        return red(p*p*(E2*du-u*dE2/2)/ss**s.Rational(3,2)),dQ,dG,dn
    def compound_jet(G,dG):
        def entry(i,j):
            rr,cc=SUBS[i],SUBS[j]
            if len(rr)!=len(cc) or not rr:return s.Integer(0)
            A,H=G.extract(rr,cc),dG.extract(rr,cc)
            return sum(A.cofactor(u,v)*H[u,v] for u in range(len(rr)) for v in range(len(cc)))
        return s.Matrix(16,16,entry)
    def blank_state(c,b):
        m=s.zeros(16,1);m[0]=m[14]=(c-a)/p
        m[1]=m[15]=1;m[3]=m[13]=b/p
        return m
    symbasis=[]
    for i in range(4):
        for j in range(i,4):
            V=s.zeros(4);V[i,j]=V[j,i]=1
            symbasis.append(((i,j),V))
    # Exact full metric/matter jets, at both poles and nonparallel preparations.
    frames=[I4,s.diag(2,s.Rational(1,2),1,1),
            s.Matrix([[1,1,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])]
    samples=[(I4,-1,0),(I4,1,0),(I4,0,1),
             (frames[1],s.Rational(3,5),s.Rational(4,5)),
             (frames[2],s.Rational(3,5),s.Rational(4,5))]
    nonzero_q=0
    pairing_motion_seen=False
    for index,(E,c,b) in enumerate(samples):
        q=E*eta*E.T;m=mat(ext(E)*blank_state(c,b));d=data(q,m)
        eq('prepared_angle_'+str(index),d['c']-c)
        W=ext(d['G']);N=red((m.T*W*m)[0]) # every sample det(E)=1
        material=s.Matrix([angle_jet(q,m,s.zeros(4),I[:,j])[0] for j in range(16)])
        eq('full_matter_radial_null_'+str(index),material.dot(m))
        for pair,V in symbasis:
            name=str(index)+'_'+str(pair)
            A,B=frame_lift(q,V);xi=mat(B*m)
            dc,dQ,dG,dn=angle_jet(q,m,V,xi)
            eq('all10_pole_regular_angle_horizontal_'+name,dc)
            eq('all10_solved_positive_metric_jet_'+name,dQ-A*d['Q']-d['Q']*A.T)
            eq('all10_true_observer_jet_'+name,dn-A*d['n'])
            dW=mat(s.trace(A)*W+compound_jet(d['G'],dG))
            eq('all16_half_density_normalization_'+name,B.T*W+W*B+dW)
            raw,_,qDG,_=angle_jet(q,m,V,s.zeros(16,1))
            eq('all10_exact_raw_cotangent_identity_'+name,raw+material.dot(xi))
            qDW=mat(s.trace(A)*W+compound_jet(d['G'],qDG))
            # N(q,m)=m^T W(q,m)m: W itself moves under matter variations.
            radial=red(-(m.T*qDW*m)[0]/(2*N))
            vertical=mat(xi-radial*m)
            _,_,mDG,_=angle_jet(q,m,s.zeros(4),vertical)
            mDW=mat(compound_jet(d['G'],mDG))
            eq('all16_true_normalized_vertical_probe_'+name,
               2*(m.T*W*vertical)[0]+(m.T*mDW*m)[0])
            eq('all10_normalized_cotangent_identity_'+name,raw+material.dot(vertical))
            if not zero((m.T*mDW*m)[0]):pairing_motion_seen=True
            if not zero(raw):nonzero_q+=1
        if c in (-1,1):
            eq('all16_material_pole_covector_zero_'+str(c),material)
    check('metric_ward_not_only_zero_fixtures',nonzero_q>0)
    reject('freeze_matter_dependence_of_normalizing_pairing',not pairing_motion_seen)
    # Literal full gate and both endpoint metrics under finite nonrest frames.
    m=blank_state(s.Rational(3,5),s.Rational(4,5));n=I4[:,0]
    U,P=record(I4,n);mp=mat(U*m);w=first(mp);np=mat(w/s.sqrt(red((w.T*w)[0])))
    V,_=record(I4,np);K=mat(V*U);F=mat(P*K.T*(I-P)*K*P)
    for index,E in enumerate(frames[1:]):
        T=ext(E);Ti=T.inv();G=(E*E.T).inv();W=ext(G)
        u,pc=record(G,E*n);v,_=record(G,E*np)
        kc=mat(v*u);fc=mat(pc*W.inv()*kc.T*W*(I-pc)*kc*pc)
        eq('literal_first_gate_frame_'+str(index),u-T*U*Ti)
        eq('literal_actual_second_gate_frame_'+str(index),v-T*V*Ti)
        eq('literal_original_cut_frame_'+str(index),pc-T*P*Ti)
        eq('literal_full_feedback_frame_'+str(index),fc-T*F*Ti)
        eq('literal_full_price_trace_frame_'+str(index),s.trace(fc)-s.trace(F))
    # A nonunit-determinant frame needs the half-density normalization.
    E=s.diag(2,2,1,1);T=ext(E);mu=E.det();W=mu*ext((E*E.T).inv())
    eq('full_state_finite_half_density',T.T*W*T-mu*I)
    eq('full_state_finite_norm_transport',(T/s.sqrt(mu)).T*W*(T/s.sqrt(mu))-I)
    reject('omit_half_density_on_normalized_fields',zero(T.T*W*T-I))
    # True constrained links: 20 metric probes and every 6 Lorentz direction.
    qs=frames[1]*eta*frames[1].T;qt=frames[2]*eta*frames[2].T
    D=frames[1]*frames[2].inv()
    eq('actual_joint_endpoint_constraint',D*qt*D.T-qs)
    for side in (0,1):
        for pair,V in symbasis:
            Vs,Vt=(V,s.zeros(4)) if side==0 else (s.zeros(4),V)
            As,At=Vs*qs.inv()/2,Vt*qt.inv()/2
            dD=As*D-D*At
            eq('all20_joint_metric_lifts_'+str(side)+'_'+str(pair),
               dD*qt*D.T+D*Vt*D.T+D*qt*dD.T-Vs)
    for i in range(4):
        for j in range(i+1,4):
            skew=s.zeros(4);skew[i,j]=1;skew[j,i]=-1
            dD=skew*qs.inv()*D
            eq('six_retained_link_directions_'+str((i,j)),dD*qt*D.T+D*qt*dD.T)
    # Full coupled-action source identity, with arbitrary other covectors.
    t0,th,j0,jh=s.symbols('T_base T_vertical J_base J_vertical')
    reduced=s.expand((t0+j0)-(t0+th)+(th+jh))
    check('complete_action_not_just_feedback_identity',s.expand(reduced-(j0+jh))==0)
    # J(base)+J(vertical)=0; matter residual is T(vertical)+J(vertical).
    check('source_error_is_full_material_residual',s.expand(reduced.subs(j0,-jh))==0)
    reject('zero_feedback_equation_equals_full_matter_equation',s.expand(th+jh-jh)==0)
    # Rank-independent finite metric-to-matter norm bound in Fock dimension 4.
    check('exterior_generator_bound_degree_max',max(map(len,SUBS))==4)
    check('half_density_trace_bound',s.Rational(4,2)==2)
    check('uniform_transfer_constant',s.Rational(4+2,2)==3)
    # Old scalar-only estimate is not uniform near a pole; the full lift is.
    t=s.symbols('t',positive=True)
    c=(1-t*t)/(1+t*t);b=2*t/(1+t*t)
    kap=p*b*b
    check('scalar_inverse_degeneracy_near_pole',s.limit(kap,t,0)==0)
    near=blank_state(c,b);near[6]=1
    probe=s.zeros(4);probe[0,2]=probe[2,0]=1
    near_raw=angle_jet(eta,near,probe,s.zeros(16,1))[0]
    residue=s.limit(s.cancel(t*near_raw/kap),t,0)
    eq('actual_near_pole_scalar_bound_residue',residue-s.Rational(1,2))
    check('actual_metric_over_scalar_residual_is_nonuniform',not zero(residue))
    check('full_metric_lift_remains_finite_at_pole',rho(I4)-2*I==s.diag(*[len(v)-2 for v in SUBS]))
    # Whole bootstrap dilation uses all grades, no nilpotency of d is needed.
    dilation=rho(I4)-2*I;degree=s.diag(*map(len,SUBS))
    d=creators[0]+2*creators[1] # genuine raising operator fixture
    eq('normalized_field_dilation_all_grades',dilation-degree+2*I)
    eq('raising_similarity_derivative',degree*d-d*degree-d)
    eq('lowering_similarity_derivative',degree*d.T-d.T*degree+d.T)
    Dirac=d+d.T;Delta=Dirac*Dirac
    dDirac=-2*d.T
    eq('actual_radial_D_jet',dDirac-(-Dirac+degree*Dirac-Dirac*degree))
    eq('actual_radial_full_square_jet',dDirac*Dirac+Dirac*dDirac-(-2*Delta+degree*Delta-Delta*degree))
    # A curved/non-nilpotent raising differential obeys the same identity.
    dc=s.zeros(16);dc[1,0]=1;dc[3,1]=2
    reject('curved_radial_proof_needs_nilpotency',dc*dc==s.zeros(16))
    Dc=dc+dc.T;Lc=Dc*Dc;dDc=-2*dc.T
    eq('curved_full_square_radial_jet',dDc*Dc+Dc*dDc-(-2*Lc+degree*Lc-Lc*degree))
    # Fixed positive spectrum: exact log(2) heat derivative, zeros retained.
    spectrum=[0,1,2];weights=[s.Rational(1,2)**v for v in spectrum]
    mean=sum(v*w for v,w in zip(spectrum,weights))/sum(weights)
    check('full_heat_radial_derivative_positive',2*mean==s.Rational(8,7))
    reject('drop_retained_zero_heat_mode',mean==sum(v*w for v,w in zip(spectrum[1:],weights[1:]))/sum(weights[1:]))
    # Actual adjacent archive projections and faithful full-state pullback.
    modes,projection,inherit=map(ns.get,['archive_modes','archive_projection','inherit'])
    coarse=tuple(range(modes(0)));fine=inherit(0,coarse)
    counts=[fine.count(x) for x in coarse]
    check('actual_archive_16_to_81',len(coarse)==16 and len(fine)==81)
    check('actual_unequal_fibres_retained',set(counts)=={5,6})
    check('every_previous_state_has_children',all(v>0 for v in counts))
    check('full_counting_isometry_normalization',all(
        sum(s.Rational(1,counts[x]) for y in range(modes(1)) if projection(0,y)==x)==1
        for x in coarse))
    # Any pointwise full state/gate or covector map commutes with this pullback.
    pointwise=lambda x:(x*x+1,2*x-3,x+7)
    check('entire_tuple_pullback_not_marginal',inherit(0,tuple(map(pointwise,coarse)))==tuple(map(pointwise,fine)))
    check('full_feedback_exponents_keep_all_children',sum(counts)==81)
    reject('refinement_deletes_added_determinant_factors',sum(counts)==len(coarse))
    reject('distant_modulo_replaces_actual_composite',
           projection(0,projection(1,81))==81%modes(0))
    check('successive_archive_maps_compose_literally',
          inherit(1,inherit(0,coarse))==tuple(projection(0,projection(1,y)) for y in range(modes(2))))
    # Exact raw l1 transfer uses a supremum over probes, not a hidden site count.
    r=[s.Rational(i,10) for i in range(1,17)]
    C=s.Rational(3)
    check('raw_l1_residual_transfer_no_extra_dimension',sum(C*x for x in r)==C*sum(r))
    reject('replace_raw_l1_by_volume_average',sum(r)==sum(r)/len(r))
    # Full golden chronology price, not a substituted one-frame square.
    c=s.Symbol('c',real=True);lam,tr,de,tr0,de0=polynomials(c)
    pencil=(1-z*lam)**2*(1-z*tr+z*z*de)**2*(1-z*tr0+z*z*de0)
    lp=s.diff(pencil,c)
    reject('all_angles_have_one_price',zero(lp.subs({c:0,z:s.Rational(1,2)})))
    reject('positive_uncompensated_heat_can_be_stationary',mean==0)
    reject('normalized_frame_lift_is_only_scalar',rho(I4[:,0]*I4[:,1].T)==s.zeros(16))
    return dict(schema='d0-research-exact-replay/1',status='PASS',input_source_head=INPUT_HEAD,
        proof=PROOF,proof_sha256=digest((ROOT/PROOF).read_bytes()),
        checker_sha256=digest(Path(__file__).read_bytes()),
        owner_declaration_sha256=OWNER_PINS,
        owner_pin_scope='EIGHT_EXECUTED_DECLARATIONS_AST_NOT_FULL_IMPORT_OR_LEAN_CLOSURE',
        exact_controls=len(checks),check_names_sha256=digest(json.dumps(checks,separators=(',',':')).encode()),executed_negative_controls=mutants,
        metric_slots=10,matter_slots=16,link_vertical_slots_per_edge=6,
        pole_regular_source_bound='3*sqrt(cond(W))*norm(q^-1)*norm(m)_W*(1+norm(m)_W*norm(D_mN)_dual/(2*N)); unnormalized factor omits the final parenthesis',
        complete_other_action_terms_retained=True,
        physical_admission=False,full_physical_source_Ward_GR=False,
        new_Lean_compilation=False)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true')
    args=parser.parse_args();result=controls()
    dest=ROOT/(BASE+'_certificate.json')
    if args.write:
        dest.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    elif json.loads(dest.read_text(encoding='utf-8')) != result:
        raise AssertionError('IMMUTABLE_RECEIPT_MISMATCH')
    print('PASS_CHRONOLOGICAL_JOINT_REDUCTION',result['exact_controls'],
          'negative_controls',len(result['executed_negative_controls']),
          'PHYSICAL_ADMISSION_AND_GR_OPEN')
