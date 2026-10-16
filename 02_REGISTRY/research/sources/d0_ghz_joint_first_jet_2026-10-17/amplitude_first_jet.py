#!/usr/bin/env python3
"""Experimental exact GHZ shell amplitude first jet, not joint field EL.

Only the pinned pure matrix constructor is used. No old run(), root,
eigenspectrum, receipt writer, or source suite is called. All16 outputs
and all8 reference-supported shell columns are retained.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import sympy as s

ROOT = Path(__file__).resolve().parents[4]
BUILDER = '02_REGISTRY/research/sources/d0_cone_source_balanced_preparation_2026-10-16/check_cone_source_balanced_preparation.py'
PINS = {
    BUILDER:'1a84b5dbfa86c03d55dfe3db41330272e4937d2a47f30c3e0929d584996859c3',
    '02_REGISTRY/research/sources/d0_cone_matter_corrector_2026-10-16/check_cone_matter_corrector.py':
        '7bbf1589f3a32af381036df64f76d720ce14a9f2e502b3a1a6f43f5b5e776d58',
    '02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py':
        'bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da',
}


def _zero(matrix):
    return all(s.expand(v) == 0 for v in matrix)


def _real_system(columns, target):
    complex_matrix = s.Matrix.hstack(*columns)
    real = complex_matrix.applyfunc(lambda v:s.expand(s.re(v)))
    imag = complex_matrix.applyfunc(lambda v:s.expand(s.im(v)))
    rhs = target.applyfunc(lambda v:s.expand(s.re(v))).col_join(
          target.applyfunc(lambda v:s.expand(s.im(v))))
    matrix = real.col_join(imag)
    keep = [i for i in range(matrix.rows)
            if any(matrix[i,j] != 0 for j in range(matrix.cols)) or rhs[i] != 0]
    return matrix.extract(keep,range(matrix.cols)),rhs.extract(keep,[0]),keep


def _particular(matrix,rhs):
    reduced,pivots = matrix.row_join(rhs).rref()
    if matrix.cols in pivots:
        return None,len(pivots)-1
    solution = s.zeros(matrix.cols,1)
    for row,pivot in enumerate(pivots):
        solution[pivot] = reduced[row,-1]
    if not _zero(matrix*solution-rhs):
        raise ArithmeticError('particular solution residual')
    return solution,len(pivots)


def _left_witness(matrix,rhs):
    equations = matrix.T.col_join(rhs.T)
    target = s.zeros(equations.rows,1)
    target[-1] = 1
    witness,_ = _particular(equations,target)
    if witness is None or not _zero(witness.T*matrix) or (witness.T*rhs)[0] != 1:
        raise ArithmeticError('left witness residual')
    return witness


def run(repo=None):
    repo = Path(repo) if repo is not None else ROOT
    checks = []

    def require(condition,label):
        if not bool(condition):
            raise ArithmeticError(label)
        checks.append(label)

    def eq(actual,expected,label):
        difference = actual-expected
        values = difference if isinstance(difference,s.MatrixBase) else (difference,)
        require(all(s.cancel(value) == 0 for value in values),label)

    for path,digest in PINS.items():
        require(hashlib.sha256((repo/path).read_bytes()).hexdigest() == digest,
                'input_pin_'+Path(path).name)
    spec = importlib.util.spec_from_file_location('ghz_matrix_definition_input',repo/BUILDER)
    owner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(owner)
    A,shell,c,b = owner._matrix_definitions_only(repo)
    I = s.eye(16)
    chi = I[:,0]+I[:,15]  # Common sqrt2 removed from every equation.
    gamma = [c[j]-b[j] for j in range(4)]
    beta = [c[j]+b[j] for j in range(4)]

    def lift(h):
        return sum((h[i,j]*c[i]*b[j] for i in range(4) for j in range(4)),s.zeros(16))

    def dirac(p):
        return s.I*sum((p[j]*gamma[j] for j in range(4)),s.zeros(16))

    def minus_adj(p):
        return s.I*sum((p[j]*beta[j] for j in range(4)),s.zeros(16))

    fields = []
    for i in range(4):
        for j in range(i,4):
            H = s.zeros(4)
            H[i,j] = H[j,i] = 1
            fields.append(('H%d%d'%(i,j),-lift(H)/2,s.zeros(16)))
    for aa in range(4):
        for bb in range(4):
            for cc in range(bb+1,4):
                q = c[bb]*c[cc]*b[aa]
                fields.append(('T%d_%d%d'%(aa,bb,cc),s.zeros(16),q+q.T))
    fields.append(('log_measure',I/2,s.zeros(16)))

    def response(l,k,field):
        _,K,Z = field
        # K_-q=K_q*, and Z_-q=conjugate(Z_q), for real geometric fields.
        dD = K*minus_adj(k)-minus_adj(l)*K-Z
        return dirac(l)*dD+dD*dirac(k)

    # Actual metric normalization check: H=delta G/s^2 at G=s^2 I.
    for p in shell:
        for field in fields[:10]:
            name,K,_ = field
            H = s.zeros(4)
            i,j = int(name[1]),int(name[2])
            H[i,j] = H[j,i] = 1
            require(_zero(response(p,p,field)+(s.Matrix(p).T*H*s.Matrix(p))[0]*I),
                    'constant_metric_normalization_'+str(p)+'_'+name)

    def block(i,j):
        return A[16*i:16*i+16,16*j:16*j+16]

    def stack(vectors):
        return s.Matrix.vstack(*vectors)

    forced = {(0,0,0,0),(0,0,2,0),(0,0,-2,0)}
    for i,l in enumerate(shell):
        for j,k in enumerate(shell):
            q = tuple(l[r]-k[r] for r in range(4))
            require(q in forced or _zero(block(i,j)*I[:,[0,15]]),
                    'whole_plane_shell_forcing_supported_0_plusminus2e2_'+str(i)+'_'+str(j))

    columns0 = [stack([response(p,p,field)*chi for p in shell]) for field in fields]
    columns0.append(stack([-chi for _ in shell]))
    rhs0 = stack([-block(j,j)*chi for j in range(8)])
    M0,r0,rows0 = _real_system(columns0,rhs0)
    solution0,rank0 = _particular(M0,r0)

    # Both opposite-y shell columns are imposed with ONE real field Fourier law.
    incoming,outgoing = 4,5
    k,l = shell[incoming],shell[outgoing]
    columns2 = []
    for field in fields:
        plus = response(l,k,field)*chi
        minus = response(k,l,field)*chi
        columns2.append(stack([plus,minus]))
    for field in fields:
        plus = response(l,k,field)*chi
        minus = response(k,l,field)*chi
        columns2.append(stack([s.I*plus,-s.I*minus]))
    rhs2 = stack([-block(outgoing,incoming)*chi,-block(incoming,outgoing)*chi])
    M2,r2,rows2 = _real_system(columns2,rhs2)
    solution2,rank2 = _particular(M2,r2)

    # Parameter theorem, not a scan of preparations or spectral eigenspaces.
    # The actual24 real torsion coordinates map to4 negative axes x6 twoforms.
    vac,top = I[:,0],I[:,15]
    twoforms = [3,5,6,9,10,12]
    torsion_fields = fields[10:34]

    def plane_vector(state,field=None):
        values = []
        for axis in range(4):
            p = shell[2*axis]
            vector = (response(p,p,field)*state if field is not None
                      else -block(2*axis,2*axis)*state)/s.I
            require(all(vector[j] == 0 for j in range(16) if j not in twoforms),
                    'plane_q0_only_twoform_outputs_'+str(len(checks)))
            require(_zero(s.conjugate(vector)-vector),
                    'plane_q0_divided_by_i_real_'+str(len(checks)))
            values.extend(vector[j] for j in twoforms)
        return s.Matrix(values)

    Mvac = s.Matrix.hstack(*[plane_vector(vac,field) for field in torsion_fields])
    Mtop = s.Matrix.hstack(*[plane_vector(top,field) for field in torsion_fields])
    K = Mvac.T*Mtop
    u,v = Mvac.T*plane_vector(vac),Mvac.T*plane_vector(top)
    eq(Mvac.T*Mvac,s.eye(24),'vacuum_torsion_image_exact_isometry')
    eq(Mtop,Mvac*K,'top_torsion_image_factorization')
    eq(K.T,K,'real_symmetric_plane_intertwiner_K')
    eq(K*K,s.eye(24),'plane_intertwiner_K_squared_identity')
    eq(K*u,-v,'forcing_Ku_minus_v')
    eq(K*v,-u,'forcing_Kv_minus_u')
    eq((u.T*u)[0],s.Rational(1,2),'forcing_u_squared_norm_half')
    eq((v.T*v)[0],s.Rational(1,2),'forcing_v_squared_norm_half')
    eq((u.T*v)[0],0,'forcing_u_v_orthogonal')
    torsion_names = [field[0] for field in torsion_fields]
    expected_u,expected_v = s.zeros(24,1),s.zeros(24,1)
    for name,value in {'T0_02':s.Rational(1,2),'T1_12':s.Rational(1,2)}.items():
        expected_u[torsion_names.index(name)] = value
    for name,value in {'T0_13':-s.Rational(1,2),'T1_03':s.Rational(1,2)}.items():
        expected_v[torsion_names.index(name)] = value
    eq(u,expected_u,'explicit_u_torsion_coefficients')
    eq(v,expected_v,'explicit_v_torsion_coefficients')
    for axis in range(4):
        for state in (vac,top):
            eq(block(2*axis+1,2*axis+1)*state,-block(2*axis,2*axis)*state,
               'opposite_momentum_forcing_sign_'+str(axis)+'_'+str(state==top))
        for field in torsion_fields:
            eq(response(shell[2*axis+1],shell[2*axis+1],field)*I[:,[0,15]],
               -response(shell[2*axis],shell[2*axis],field)*I[:,[0,15]],
               'both_momentum_signs_torsion_image_'+str(axis)+'_'+field[0])

    aa,bb = s.symbols('a b',real=True)
    corrector0 = ((aa*aa+bb*bb)*u+2*aa*bb*v)/(aa*aa-bb*bb)
    eq((aa*s.eye(24)+bb*K)*corrector0,aa*u+bb*v,
       'general_real_unbalanced_line_exact_q0_corrector')
    realpart = s.symbols('x',real=True)
    eq(K*(-u),v,'complex_relative_phase_imag_equation_forces_t_minus_u')
    eq((aa*s.eye(24)+realpart*K)*(-u)-(aa*u+realpart*v),-2*aa*u,
       'complex_relative_phase_real_equation_has_nonzero_residual')

    # Better than the GHZ-only RREF solution: this cancels the WHOLE plane.
    universal = {'T2_02':-s.Rational(1,4),'T2_12':s.Rational(1,4)}
    for out_index,in_index in ((5,4),(4,5)):
        correction = sum((coefficient*response(shell[out_index],shell[in_index],
                          next(field for field in torsion_fields if field[0] == name))
                          for name,coefficient in universal.items()),s.zeros(16))
        eq((block(out_index,in_index)+correction)*I[:,[0,15]],s.zeros(16,2),
           'universal_q2_correction_entire_plane_and_all16_outputs_'+str(out_index))

    # Exact trace-weighted q0 twoform residual for EVERY common plane density.
    # Both signs, each with normalized shell weight1/8, give2/8=1/4.
    r,x,y = s.symbols('r x y',real=True)
    density = s.Matrix([[r,x+s.I*y],[x-s.I*y,1-r]])
    t = s.Matrix(s.symbols('t0:24',real=True))
    E0,E1 = t-u,K*t-v
    residual_columns = E0.row_join(E1)
    direct = s.trace(density*residual_columns.T*residual_columns)/4
    delta = 2*r-1
    quadratic = ((t.T*t)[0]+2*x*(t.T*K*t)[0]-2*delta*(t.T*u)[0]+s.Rational(1,2))/4
    eq(s.expand(direct-quadratic),0,'general_density_q0_twoform_residual_identity')
    eq(s.expand(quadratic.subs(r,s.Rational(1,2))-
       ((t.T*(s.eye(24)+2*x*K)*t)[0]+s.Rational(1,2))/4),0,
       'balanced_density_positive_quadratic_plus_one_eighth')
    inverse = (s.eye(24)-2*x*K)/(1-4*x*x)
    eq((s.eye(24)+2*x*K)*inverse,s.eye(24),'nonendpoint_density_quadratic_inverse')
    minimizer = delta*inverse*u
    minimum = (density.det()+y*y)/(2*(1-4*x*x))
    eq(quadratic.subs(dict(zip(t,minimizer)))-minimum,0,
       'general_nonendpoint_density_minimum_formula')
    for sign in (-1,1):
        state = vac+sign*top
        w = I[:,5]+sign*I[:,10]
        eq((w.T*block(0,0)*state)[0],-s.I,'GHZ_plusminus_actual_A_witness_'+str(sign))
        require(all((w.T*response(shell[0],shell[0],field)*state)[0] == 0
                    for field in fields),'GHZ_plusminus_annihilates_all_real_fields_'+str(sign))
    eq(s.Rational(2,8),s.Rational(1,4),'full8_momentum_density_normalization_factor')
    eq(s.Rational(1,4)*s.Rational(1,2),s.Rational(1,8),'balanced_residual_one_eighth')

    cases = []
    for label,matrix,rhs,rows,solution,rank in (
        ('q0',M0,r0,rows0,solution0,rank0),
        ('q_plus_and_minus_2e2_real_conjugate',M2,r2,rows2,solution2,rank2)):
        result = {'frequency':label,'real_system_shape':list(matrix.shape),
                  'rank':rank,'augmented_rank':rank+int(solution is None),
                  'original_real_rows_retained':rows,'consistent':solution is not None}
        if solution is None:
            witness = _left_witness(matrix,rhs)
            result['left_annihilator_nonzero_coefficients'] = {
                str(rows[i]):str(v) for i,v in enumerate(witness) if v != 0}
            result['annihilator_rhs'] = '1'
        elif label == 'q0':
            names = [field[0] for field in fields]+['epsilon1']
            result['particular_field_coefficients'] = {name:str(v) for name,v in zip(names,solution)
                                                       if v != 0}
        else:
            count = len(fields)
            result['particular_plus_frequency_coefficients'] = {
                field[0]:str(s.expand(solution[j]+s.I*solution[count+j]))
                for j,field in enumerate(fields) if solution[j] != 0 or solution[count+j] != 0}
            result['negative_frequency'] = 'complex conjugate of plus frequency'
        cases.append(result)
    return {
        'status':'AMP_FIRST_JET_SOLVABLE' if solution0 is not None and solution2 is not None
                 else 'AMP_FIRST_JET_OBSTRUCTION',
        'exact_checks':len(checks),'checks':checks,
        'source_pins':PINS,'shell_momenta':[list(p) for p in shell],
        'preparation':'rho=(P_Sigma/8) tensor |(mask0+mask15)/sqrt2><same|',
        'full_Fock_output_components':16,'occupied_amplitude_columns':8,
        'reference_dimension_retained':128,'actual_reference_rank':8,
        'real_field_slots':{'metric':10,'torsion':24,'log_measure':1},
        'conventions':{
            'scale':'solve dimensionless s=1; A1 and deltaDelta have common s^-2; physical G1=s^2 H',
            'torsion':'deltaD_t=-(Q_t+Q_t^T)/s with orthonormal-frame t conventions',
            'metric_and_measure':'K_q=-Gamma(H_q)/2+(delta log mu)_q I/2',
            'actual_offdiagonal_firstjet':'deltaD_lk=K_q i beta(k)-i beta(l)K_q-Z_t(q); X_lk=D_l deltaD+deltaD D_k',
            'Fourier':'q=l-k, realfields v_-q=conjugate(v_q)',
            'equation_row_order':'q0:8momenta then16masks; qpair:+2edge then-2edge; real rows then imaginary rows',
        },
        'cases':cases,'unrelated_Fourier_jets':'set zero',
        'general_common_plane_density_theorem':{
            'density':'sigma=[[r,z],[conjugate(z),1-r]], z=x+i*y, sigma>=0; rho=P_Sigma/8 tensor sigma',
            'intertwiner':'Mvac orthogonal, Mtop=Mvac K, K=K^T, K^2=I24',
            'forcing':'||u||^2=||v||^2=1/2, u.v=0, Ku=-v, Kv=-u',
            'u':{torsion_names[i]:str(value) for i,value in enumerate(u) if value != 0},
            'v':{torsion_names[i]:str(value) for i,value in enumerate(v) if value != 0},
            'exact_q0_twoform_residual_squared':'[t^T(I+2*x*K)t-2*(2*r-1)*t.u+1/2]/(4*s^4)',
            'scalar_metric_epsilon_outputs':'orthogonal grades0/4 add a nonnegative term; can set H=epsilon1=0',
            'balanced_uniform_bound':'sigma00=sigma1515=1/2 => residual_squared>=1/(8*s^4), any rank or complex coherence',
            'balanced_bound_reason':'PSD sigma gives |2 Re(z)|<=1; K symmetric involution implies I+2 Re(z)K>=0',
            'balanced_full_normalized_amplitude_Euler_bound':'first_residual_squared>=1/(2*s^4)',
            'nonendpoint_minimum':'(det(sigma)+(Im z)^2)/(2*s^4*(1-4*(Re z)^2)) when |2 Re z|<1',
            'q0_compatibility_iff':'rank(sigma)=1, Im(sigma0,15)=0, sigma00!=sigma1515',
            'rank_two_plane':'impossible; its support contains a forbidden GHZ line',
            'real_pure_unbalanced_corrector':'chi=a|0>+b|15>: t0=[(a^2+b^2)u+2abv]/(a^2-b^2), H=measure=epsilon1=0',
            'universal_plus_and_minus_2e2_coefficients':{name:str(coefficient) for name,coefficient in universal.items()},
            'universal_spatial_correction':'t^2_02(y)=-(1/2)cos(2y), t^2_12(y)=(1/2)cos(2y)',
            'all_resonant_amplitude_rows':'solved for every real pure unbalanced line by combining t0 with universal q2 correction',
            'all_other_Fourier_force':'verified zero on the WHOLE vacuum/top plane, not only GHZ+',
            'reference_normalization':'rho=P_Sigma/8 tensor sigma, Tr sigma=1; C0 can be blockdiag(sqrt(sigma)/sqrt8), zero padded to128 columns',
            'reference_ranks':'8 for pure common sigma,16 for rank2 common sigma; total retained dimension128',
            'native_preparation_balance_admission':'separate owner premise; not inferred by this matrix calculation',
        },
        'joint_field_Euler_rows_solved':False,'joint_branch_proved':False,
        'old_run_or_eigenspectrum_called':False,
    }


if __name__ == '__main__':
    print(json.dumps(run(),ensure_ascii=False,sort_keys=True,indent=2))
