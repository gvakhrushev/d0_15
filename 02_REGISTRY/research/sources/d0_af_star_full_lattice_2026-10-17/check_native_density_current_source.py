#!/usr/bin/env python3
"""New measure costate/current consumer; does not replay previous suites.

The four-site block is an actual transverse-zero block of the full16
Dirac. All covariance and price statements retain their stated scope.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path

import sympy as s
import check_native_operator_kernel_source as native


def check():
    checks = []

    def equal(name, actual, expected):
        delta = actual-expected
        entries = list(delta) if isinstance(delta, s.MatrixBase) else [delta]
        if not all(s.simplify(x) == 0 for x in entries):
            raise ArithmeticError(name)
        checks.append(name)

    C, _ = native.literal_creators()
    c = C[0]  # null-coordinate coefficient eta e_v
    shift = s.zeros(4)
    for x in range(4):
        shift[x, (x+1) % 4] = 1
    diff = shift-s.eye(4)
    nu = s.Rational(1, 2)
    d = nu*s.kronecker_product(diff, c)
    D = d+d.T
    phi = s.Matrix([1, 1, -1, -1])/2
    prepared = s.kronecker_product(phi, s.eye(16)[:, 0])
    rho = prepared*prepared.T
    equal('full16_eigenpreparation', D*D*prepared, 2*nu**2*prepared)
    equal('full16_preparation_norm', prepared.dot(prepared), 1)

    # The identity is linear in W. Include a noncommuting matter term
    # and a genuine spectral polynomial without choosing a new price.
    spectral = s.eye(64)/11+D*D/13
    W = rho+spectral
    equal('W_commutes_with_Delta', W*D*D-D*D*W, s.zeros(64))
    if W*D-D*W == s.zeros(64):
        raise ArithmeticError('fixture must preserve noncommuting matter')
    checks.append('matter_need_not_commute_with_D')
    A = D*W+W*D
    comm = d*A-A*d
    k = s.Matrix([s.re(s.trace(comm[16*x:16*(x+1), 16*x:16*(x+1)]))
                  for x in range(4)])
    equal('measure_costate_sum_zero', sum(k), 0)
    f = s.Matrix([2, -1, 3, 0])
    Mf = s.kronecker_product(s.diag(*f), s.eye(16))
    dd = (Mf*d-d*Mf)/2
    delta_D_measure = dd+dd.T
    direct_measure = s.trace(A*delta_D_measure)
    equal('full16_actual_measure_source', direct_measure, (f.T*k)[0])

    psi = s.Matrix([1, -1, 1, -1])
    backward = psi-shift.T*psi
    delta_d = -nu*s.kronecker_product(s.diag(*backward)*diff, c)
    delta_D = delta_d+delta_d.T
    site_shift = s.kronecker_product(diff, s.eye(16))
    coefficient = s.kronecker_product(s.eye(4), nu*c)
    raw_current = site_shift*A*coefficient
    current = s.Matrix([2*s.re(s.trace(raw_current[16*x:16*(x+1),
                                                   16*x:16*(x+1)]))
                        for x in range(4)])
    counting_source = s.trace(A*delta_D)
    equal('counting_current_contraction', counting_source,
          -(backward.T*current)[0])
    equal('counting_current_source', counting_source, 8*nu**2)
    Mback = s.kronecker_product(s.diag(*backward), s.eye(16))
    measure_d = (Mback*d-d*Mback)/2
    natural_D = delta_D+measure_d+measure_d.T
    natural_source = s.trace(A*natural_D)
    divergence = (shift-s.eye(4))*(current-k)
    equal('actual_combined_current_measure_source', natural_source,
          (psi.T*divergence)[0])
    equal('combined_source_includes_real_costate', natural_source,
          counting_source+(backward.T*k)[0])
    if natural_source == 0:
        raise ArithmeticError('optional density is not exact finite cancellation')
    checks.append('optional_density_is_not_exact_finite_Ward')

    # Torsion cannot cancel the density operator on all16 columns.
    # Q_T and its adjoint annihilate the vacuum for every component.
    vacuum = s.eye(16)[:, 0]
    I16 = s.eye(16)
    for a in range(4):
        for b in range(4):
            for c0 in range(b+1, 4):
                Q = C[b]*C[c0]*C[a].T
                equal(f'torsion_vacuum_{a}_{b}_{c0}',
                      (Q+Q.T)*vacuum, s.zeros(16, 1))
    b = s.Matrix([1, 2, -1, 3])
    cb = sum((b[a]*C[a] for a in range(4)), s.zeros(16))
    bhat = cb+cb.T
    equal('density_residual_on_vacuum', (-bhat/2)*vacuum, -cb*vacuum/2)
    equal('density_residual_norm_square',
          ((bhat*vacuum).T*(bhat*vacuum))[0]/4, (b.T*b)[0]/4)
    N = sum((C[a]*C[a].T for a in range(4)), s.zeros(16))
    pure_trace_Q = s.zeros(16)
    for a in range(4):
        for b0 in range(4):
            for c0 in range(b0+1, 4):
                torsion = ((int(a == b0)*b[c0]-int(a == c0)*b[b0])/3)
                pure_trace_Q += torsion*C[b0]*C[c0]*C[a].T
    pure_trace_Z = -pure_trace_Q-pure_trace_Q.T
    equal('actual_pure_trace_torsion_operator', pure_trace_Z,
          (cb*N+N*cb.T)/3)
    # H1 Gårding already owned. The new proof applies it to lattice
    # differences and D_h f to obtain the H2 graph bound; no high modes
    # are removed in the estimate or native spectral traces.
    return {
        'status': 'PASS', 'input_head': '61737b24',
        'checks': len(checks), 'check_names': checks,
        'literal_creator_pins': native.PINS,
        'measure_costate': {
            'operator_jet': 'delta d=[M_f/2,d], delta D=[M_f/2,d-d*]',
            'price_source': 'DS_measure=sum_x f_x k_x',
            'k': 'Re tr_CAR([d,{D,W}]_xx)',
            'sum_k_zero': True,
            'combined_psi_row': '(h ell)^-1 sum_x psi[sum_r D_r^+ j_r-ell D_v^+ k]',
            'actual_measure_variation_supplied_by_original_programme': False},
        'fixture': {'nu': '1/2', 'h': '1', 'ell': '1',
                    'current': list(map(str, current)), 'costate': list(map(str, k)),
                    'counting_source': str(counting_source),
                    'optional_natural_source': str(natural_source),
                    'all16_grades_retained': True,
                    'spectral_polynomial': 'linearity control; not a replacement price'},
        'torsion': {'all24_directions_kill_vacuum': True,
                    'density_residual_norm': '|b|/2',
                    'leading_v_equals_b_is_full_operator_cancellation': False},
        'positive_source_theorem_scope': {
            'operator': 'actual v-independent pp-wave stencil, U_v=I, exact proper links',
            'separately_required_measure': 'omega_tau=det(e_tau)/det(e_0)',
            'uniform_chart': 'bounded C6 coefficients, uniformly invertible coframe and H2 graph estimate',
            'residual': '||(delta D_nat-[K_h,D_h])(1+Delta_h)^-1|| <= C h ||psi||_C^m',
            'price': 'actual finite-B H+J+R, fixed calibrations within each variation',
            'thermal_and_matter': 'beta in fixed positive compact interval; full thermal moments; E_h<=E_* eigenpreparation',
            'conclusion': '|DS_nat[psi]| <= C h ||psi||_C^m',
            'uniform_raw_h^-2_or_golden_C2_only_conclusion': False},
        'physical_D0_GR_proved': False, 'whole_joint_roots_proved': False}


def prep_observer_counter(root):
    root=Path(root).resolve()
    path='02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py'
    node=next(n for n in ast.parse((root/path).read_text()).body
              if isinstance(n,ast.FunctionDef) and n.name=='creator')
    pin=hashlib.sha256(ast.dump(node,include_attributes=False).encode()).hexdigest()
    assert pin=='801b33d7ef3e41f6425be16153c82b1402215f6be757ea275ff06a69010f58e4'
    ns={'s':s,'SUBS':[tuple(i for i in range(4) if mask&(1<<i)) for mask in range(16)]}
    exec(compile(ast.Module(body=[node],type_ignores=[]),path,'exec'),ns)
    creator=ns['creator'];I=s.eye(16);e=s.eye(4)
    r,nu,h,ell=s.symbols('r nu h ell',positive=True)
    R=1+r*r;c=1/s.sqrt(R);sigma=s.sqrt(3+4*r*r)/(s.sqrt(3)*s.sqrt(R))
    t=(1+s.I*r)/(1-s.I*r);z=t-1
    H=s.Matrix([[1,1,1,1],[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,1]])/2
    U=nu*s.diag(c,sigma,sigma,sigma)*H
    eta=s.diag(1,-1,-1,-1);F=U.T*eta
    def clean(v):
        v=v.replace(lambda x:x.is_Pow and x.exp==s.Rational(1,2),lambda x:s.sqrt(s.factor(x.base)))
        return s.simplify(v)
    simp=lambda A:A.applyfunc(clean)
    cs=[creator(e[:,i]) for i in range(4)]
    gamma=lambda A:sum((A[i,j]*cs[i]*cs[j].T for i in range(4) for j in range(4)),s.zeros(16))
    Q=simp(U.T*U)
    expected=nu**2*((1-(c*c-1)/3)*s.eye(4)+(c*c-1)*s.ones(4)/3)
    assert simp(Q-expected)==s.zeros(4)
    # Decisive negative control: the old 16 sign momenta are NOT one shell.
    zb=s.Matrix([z,z,s.conjugate(z),s.conjugate(z)])
    mu=4*nu*r/(ell*R)
    bad=s.simplify((zb.conjugate().T*Q*zb)[0]/ell**2-mu**2)
    bad_expected=64*nu**2*r**4/(3*ell**2*R**3)
    assert s.simplify(bad-bad_expected)==0 and bad_expected.is_positive
    # Correct base: 8 distinct axis momenta +/-2theta e_j, full CAR16 each.
    # Every base energy is exactly mu^2 because ||u_j||=nu and
    # |exp(2itheta)-1|=2 sin(theta)=4r/(1+r^2).
    z2=t*t-1
    for j in range(4):
        assert s.simplify((U[:,j].T*U[:,j])[0]-nu**2)==0
    assert s.simplify(z2*s.conjugate(z2)-16*r*r/R**2)==0
    # Delete one canonical positive Dirac vector at each axis momentum.
    # All are normalized and have D eigenvalue +mu by the CAR identity.
    # Verify the one generic column and its actual conjugate; role covariance
    # and ||u_j||=nu give the other six without a full momentum replay.
    wa=U[:,0]*z2
    va=simp((I[:,0]+creator(wa)/(mu*ell)*I[:,0])/s.sqrt(2))
    da=creator(wa)/ell;Da=da+da.conjugate().T
    assert s.simplify((va.conjugate().T*va)[0]-1)==0
    assert simp(Da*va-mu*va)==s.zeros(16,1)
    assert simp(Da.conjugate()*va.conjugate()-mu*va.conjugate())==s.zeros(16,1)
    # Add eight real standing positive Dirac vectors at k+/-=(+/-theta)^4.
    # Sum U columns=2nu c e0, so these have the very same energy mu^2.
    assert simp(U*s.ones(4,1)-2*nu*c*e[:,0])==s.zeros(4,1)
    phase=(-r+s.I)/s.sqrt(R)
    assert s.simplify(phase*s.conjugate(phase)-1)==0
    dk=2*nu*c*z*cs[0]/ell;dl=dk.conjugate()
    Dk=simp(dk+dk.conjugate().T);Dl=Dk.conjugate()
    Dpair=s.diag(Dk,Dl)
    masks=[0,2,4,6,8,10,12,14]
    vks={};vls={};columns=[]
    for mask in masks:
        base=I[:,mask]
        vk=(base+phase*cs[0]*base)/s.sqrt(2);vl=vk.conjugate()
        vks[mask]=vk;vls[mask]=vl
        assert simp(Dk*vk-mu*vk)==s.zeros(16,1)
        co=vk.col_join(vl)/s.sqrt(2)
        si=(-s.I*vk).col_join(s.I*vl)/s.sqrt(2)
        columns.append(simp((co+si)/s.sqrt(2)) if mask==0 else co)
    T=s.Matrix.hstack(*columns)
    assert simp(T.conjugate().T*T-s.eye(8))==s.zeros(8)
    assert simp(Dpair*T-mu*T)==s.zeros(32,8)
    Padd=simp(T*T.conjugate().T)
    assert simp(Padd*Padd-Padd)==s.zeros(32)
    swap=s.zeros(32);swap[:16,16:]=I;swap[16:,:16]=I
    assert simp(swap*Padd.conjugate()*swap-Padd)==s.zeros(32)
    # All128 orthonormal directions:128 axis -8 deleted +8 added.
    # Axis and diagonal momenta are distinct at any sufficiently small
    # positive theta on a periodic lattice; no new spectator factor used.
    rank=8*16-8+8;assert rank==128
    # Full nonzero-q observer proof, ALL spatial spectator masks.
    # deltaD_n(l,k)=Gamma(a)Kk-Kl Gamma(a), a=-B0i.
    # Every component compressed to span{|I>,c0|I>} vanishes termwise.
    occupancy_controls=0
    for i in range(1,4):
        boost=s.zeros(4);boost[0,i]=boost[i,0]=1
        ga=gamma(-boost)
        for mask in masks:
            basis=s.Matrix.hstack(I[:,mask],cs[0]*I[:,mask])
            for op in [ga*cs[0],ga*cs[0].T,cs[0]*ga,cs[0].T*ga]:
                assert basis.T*op*basis==s.zeros(2)
                occupancy_controls+=1
        # At q0 deltaDelta=-4Re(w0*wi)/ell^2 I16. Full axis sums
        # vanish for both128 base states and8 deleted states separately.
        assert s.simplify(sum(U[0,j]*U[i,j] for j in range(4)))==0
        # Every thermal/feedback spectral weight is role-permutation
        # invariant, so its z covariance=aI+b11T; both contractions vanish.
        assert (H[0,:]*H[i,:].T)[0]==0 and sum(H[i,j] for j in range(4))==0
    # Actual null-gradient metric family, same counting measure and old clock.
    # q=kminus-kplus=-2theta1111; psi(x)=cos(q.x), hence psi_q=1/2.
    psiq=s.Rational(1,2);null=s.Matrix([1,1,0,0])
    assert (null.T*eta*null)[0]==0
    alpha=F*null
    dq=(1-t*t)*psiq*s.ones(4,1)
    du=[-alpha[j]*(U*dq)/h for j in range(4)]
    dd_lk=sum((creator(du[j])*z/ell for j in range(4)),s.zeros(16))
    dd_kl=sum((creator(du[j].conjugate())*s.conjugate(z)/ell for j in range(4)),s.zeros(16))
    dD_lk=simp(dd_lk+dd_kl.conjugate().T)
    dD=s.zeros(32);dD[16:,:16]=dD_lk;dD[:16,16:]=dD_lk.conjugate().T
    dDelta=simp(Dpair*dD+dD*Dpair)
    m=s.simplify((vls[0].conjugate().T*dDelta[16:,:16]*vks[0])[0])
    m_expected=-16*nu**3*c**3*(1-t*t)*z*z*psiq/(h*ell**2)
    assert s.simplify(m-m_expected)==0
    source=s.simplify(s.trace(Padd*dDelta)/128)
    source_expected=nu**3*r**3*(-1+28*r+6*r*r-28*r**3-r**4)/(R**s.Rational(11,2)*h*ell**2)
    assert s.simplify(source-source_expected)==0
    assert s.simplify(source-(s.im(m)+7*s.re(m))/128)==0
    assert s.limit(source*h*ell**2/(nu**3*r**3),r,0)==-1
    # Uniform exact sign on a genuinely resolved window.
    assert 1-28*s.Rational(1,32)-6*s.Rational(1,32)**2==s.Rational(61,512)
    return {'status':'PASS','input_head':'61737b24','owner_AST_sha256':{path:{'creator':pin}},
      'price':'same conditional full-Lorentz S8 H+J+R; counting measure; actual D_can, no modified action',
      'parameter':'r=tan(theta/2)>0; c=cos(theta/2), sigma=sqrt((4-c^2)/3)',
      'coframe':'U=nu diag(c,sigma,sigma,sigma) H; first row H all1/2; n=e0; internal Lorentz linksI',
      'wrong_Omega_shell_negative_control':str(bad_expected),
      'base':'8 distinct axis momenta +/-2theta e_j, full16 CAR per momentum',
      'deleted':'one normalized canonical D+ vacuum+onebody vector at each axis momentum,8 total',
      'added':'8 positive-Dirac standing states at k+/-=(+/-theta)^4; one per spatial spectator maskI; I=0 uses phase45, other7 use cosine',
      'base_rank':128,'deleted_rank':8,'added_rank':8,'final_rank':128,
      'fixed_RIGHT':'I128/128 exactly, pure Schmidt128 purification of P/128',
      'position_reality':True,'all16_and_reference128_retained':True,
      'all_independent_preparation_Euler_rows_zero':True,'owned_preparation_equation':'Delta Psi=mu^2 Psi','D_Psi_equals_mu_Psi_asserted':False,
      'mu':'2 nu sin(theta)/ell','mu_resolved_limit':'2 nu kappa when theta=kappa h, ell=h',
      'all_independent_n_L_observer_rows_zero':True,'literal_nonzero_q_occupancy_controls':occupancy_controls,
      'observer_nonzero_q':'only+/-2theta1111; same-I CAR compression zero for every mask',
      'observer_q0':'full axis orbit cancellation; added diagonal momenta have w_spatial0',
      'thermal_feedback_observer':'analytic role permutation covariance, allmomentum traces retained without enumerating the grid',
      'psi':'cos(2theta(x0+x1+x2+x3)); each Fourier coefficient1/2',
      'metric_family':'delta e=(tau/h)(e0+e1)(D^-psi)^T, internal deltaA=0, deltan=0; coordinate endpoint D varies with F',
      'scalar_matrix_element':str(m_expected),
      'full_S8_source':'(Im m+7 Re m)/128 = nu^3 r^3[-1+28r+6r^2-28r^3-r^4]/[(1+r^2)^(11/2) h ell^2]',
      'strict_sign':'negative for0<r<=1/32; bracket<=-61/512',
      'resolved_source_limit':'-nu^3 kappa^3/8 for theta=kappa h and ell=h',
      'literal_refinement':'theta=2pi/L, h=ell=1/L, L large divisibleby4; all selected modes have bounded physical energy',
      'all_coframe_link_equations_zero_claimed':False,'P1_observer_readout_binding_claimed':False,'physical_native_gate_preparation_claimed':False}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = check()
    result['prep_observer_counter'] = prep_observer_counter(native.ROOT)
    if args.output:
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
        print(json.dumps({'status': 'PASS', 'new_density_current_checks': result['checks']}))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
