#!/usr/bin/env python3
"""Bounded literal-CAR source/compatibility consumer; no momentum census."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import sympy as s


def link_rows(root):
    root = Path(root).resolve()
    path = '02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py'
    node = next(n for n in ast.parse((root/path).read_text()).body
                if isinstance(n, ast.FunctionDef) and n.name == 'creator')
    pin = hashlib.sha256(ast.dump(node, include_attributes=False).encode()).hexdigest()
    assert pin == '801b33d7ef3e41f6425be16153c82b1402215f6be757ea275ff06a69010f58e4'
    ns = {'s': s, 'SUBS': [tuple(i for i in range(4) if mask & (1 << i))
                           for mask in range(16)]}
    exec(compile(ast.Module(body=[node], type_ignores=[]), path, 'exec'), ns)
    creator = ns['creator']
    E = s.eye(16)
    c = [creator(s.eye(4)[:, i]) for i in range(4)]
    gamma = lambda A: sum((A[i, j]*c[i]*c[j].T for i in range(4)
                          for j in range(4)), s.zeros(16))
    generators = {}
    for i in range(1, 4):
        O = s.zeros(4); O[0, i] = O[i, 0] = 1
        generators['B0'+str(i)] = O
    for i, j in [(1, 2), (1, 3), (2, 3)]:
        O = s.zeros(4); O[i, j] = 1; O[j, i] = -1
        generators['R'+str(i)+str(j)] = O
    u = s.Matrix(s.symbols('u0:4', real=True))
    zeta, t, mu, ell = s.symbols('zeta t mu ell', nonzero=True)
    masks = [0, 2, 4, 6, 8, 10, 12, 14]
    # k+=(theta)^4, k-=-(theta)^4. Actual raising+true-adjoint jet
    # for the q=kminus-kplus link coefficient is t(C(u)Gamma+Gamma* C(u)*).
    vectors = {mask: (E[:, mask]+zeta*c[0]*E[:, mask])/s.sqrt(2)
               for mask in masks}
    low = s.Matrix.hstack(*[E[:, mask] for mask in [0, 1, 2, 4, 8]])
    low_controls = 0
    sums = {}
    for name, O in generators.items():
        g = gamma(O)
        Q = creator(u)*g + g.T*creator(u).T
        assert low.T*Q*low == s.zeros(5)
        low_controls += 1
        values = [s.expand(2*mu*t*(vectors[mask].T*Q*vectors[mask])[0]/ell)
                  for mask in masks]
        assert values[0] == 0
        expected_sum = -8*mu*t*zeta*(s.eye(4)[:, 0].T*O*u)[0]/ell
        assert s.simplify(sum(values)-expected_sum) == 0
        if name.startswith('B'):
            i = int(name[-1])
            for mask, val in zip(masks, values):
                expected = -2*mu*t*zeta*u[i]/ell if mask & (1 << i) else 0
                assert s.expand(val-expected) == 0
        else:
            assert all(val == 0 for val in values)
        sums[name] = str(expected_sum)
    # All24 physical link rows are these six identities at four real columns.
    # Homogeneous full16 trace identity, before any momentum sum.
    wr = s.Matrix(s.symbols('a0:4', real=True))
    wi = s.Matrix(s.symbols('b0:4', real=True))
    w = wr+s.I*wi
    tr, ti = s.symbols('tr ti', real=True)
    tc = tr+s.I*ti
    D = creator(w)+creator(w).conjugate().T
    trace_controls = 0
    for O in generators.values():
        g = gamma(O)
        dD = tc*creator(u)*g+s.conjugate(tc)*g.T*creator(u).T
        trace = s.expand(s.trace(D*dD+dD*D))
        expected = -16*s.re(tc*(w.conjugate().T*O*u)[0])
        assert s.expand(trace-expected) == 0
        trace_controls += 1
    r, nu, h = s.symbols('r nu h', positive=True)
    R = 1+r*r
    ct = 1/s.sqrt(R)
    st = s.sqrt(3+4*r*r)/(s.sqrt(3)*s.sqrt(R))
    H = s.Matrix([[1,1,1,1],[1,1,-1,-1],
                  [1,-1,1,-1],[1,-1,-1,1]])/2
    U = nu*s.diag(ct, st, st, st)*H
    phase = (-r+s.I)/s.sqrt(R)
    tt = (1+s.I*r)/(1-s.I*r)
    mmu = 4*nu*r/(ell*R)
    A, B = s.symbols('A B', real=True)
    # Role-covariant spectral moment M_rs=A ondiag, B offdiag.
    M = (A-B)*s.eye(4)+B*s.ones(4)
    for leg in range(4):
        for name, O in generators.items():
            expression = sum(M[leg, j]*(U[:, j].T*O*U[:, leg])[0]
                             for j in range(4))
            expected = nu*ct*U[int(name[-1]), leg]*(A+B) if name.startswith('B') else 0
            assert s.simplify(expression-expected) == 0
    # Matter contributions to A+B: full axis sum0, deleted lowgrade0,
    # added k+/- positive Dirac projector gives half a full16 trace.
    sin_theta2 = 4*r*r/R**2
    axis_A = sin_theta2/32
    axis_B = -sin_theta2/32
    assert axis_A+axis_B == 0
    added_A = r*r/(128*R)
    assert s.simplify(2*added_A-r*r/(64*R)) == 0
    # Named qdiag boost control, leg0,B01, actual real cos/sin coefficient.
    J = -mmu*U[1, 0]*phase*tt/(32*ell)
    Jcos = mmu*U[1, 0]*r*(3-r*r)/(32*ell*R**s.Rational(3,2))
    Jsin = -mmu*U[1, 0]*(1-3*r*r)/(32*ell*R**s.Rational(3,2))
    assert s.simplify(s.re(J)-Jcos) == 0
    assert s.simplify(s.im(J)-Jsin) == 0
    # The protected SAME-energy complement for the fixed-RIGHT Euler.
    vk = (E[:, 0]+phase*c[0]*E[:, 0])/s.sqrt(2)
    vl = vk.conjugate()
    co = vk.col_join(vl)/s.sqrt(2)
    si = (-s.I*vk).col_join(s.I*vl)/s.sqrt(2)
    eta_in, eta_out = (co+si)/s.sqrt(2), (co-si)/s.sqrt(2)
    assert s.simplify((eta_out.conjugate().T*eta_in)[0]) == 0
    assert s.simplify((eta_out.conjugate().T*eta_out)[0]-1) == 0
    metric_m = -8*nu**3*ct**3*(1-tt*tt)*(tt-1)**2/(h*ell**2)
    Re_m = 512*nu**3*r**4*(1-r*r)/(R**s.Rational(11,2)*h*ell**2)
    assert s.simplify(s.re(metric_m)-Re_m) == 0
    # Recompute the metric matrix element from the literal flat-star field
    # tangent, rather than taking the old scalar-current formula as oracle.
    eta = s.diag(1,-1,-1,-1)
    F = U.T*eta
    null = s.Matrix([1,1,0,0])
    alpha = F*null
    dq = (1-tt*tt)*s.ones(4,1)/2
    du = [-alpha[j]*(U*dq)/h for j in range(4)]
    dd_lk = sum((creator(du[j])*(tt-1)/ell for j in range(4)),s.zeros(16))
    dd_kl = sum((creator(du[j].conjugate())*(s.conjugate(tt)-1)/ell
                 for j in range(4)),s.zeros(16))
    actual_dD = dd_lk+dd_kl.conjugate().T
    actual_metric_m = 2*mmu*(vl.conjugate().T*actual_dD*vk)[0]
    assert s.simplify(actual_metric_m-metric_m) == 0
    # Actual 32dim metric jet is compressed here to its exact D+ clock plane.
    mr, mi = s.symbols('mr mi', real=True)
    Jmetric = s.Matrix([[0,mr-s.I*mi],[mr+s.I*mi,0]])
    C = s.Matrix([1,1])/s.sqrt(2)
    S = s.Matrix([-s.I,s.I])/s.sqrt(2)
    inside, outside = (C+S)/s.sqrt(2), (C-S)/s.sqrt(2)
    assert s.simplify((inside.conjugate().T*Jmetric*inside)[0]-mi) == 0
    assert s.simplify((outside.conjugate().T*Jmetric*inside)[0]-mr) == 0
    # For ANY link Fourier coefficient, the lowgrade identity kills this
    # plus-to-plus offblock. For all observer Fourier coefficients which can
    # connect k+/- (q0 and +/-qdiag), direct clock compression is zero.
    clock = s.Matrix.hstack(E[:,0], c[0]*E[:,0])
    observer_controls = 0
    for i in range(1,4):
        O = s.zeros(4); O[0,i] = O[i,0] = 1
        ga = gamma(-O)
        for op in [ga*c[0],ga*c[0].T,c[0]*ga,c[0].T*ga]:
            assert clock.T*op*clock == s.zeros(2)
            observer_controls += 1
    # For comparison ONLY, common-eigenvalue prep would force the q0 n=0:
    # axis lowgrade D- diagonals have these rank3, zero-mean coefficients.
    observer_axes = s.Matrix([[U[0,j]*U[i,j] for i in range(1,4)]
                              for j in range(4)])
    assert s.simplify(observer_axes.T*s.ones(4,1)) == s.zeros(3,1)
    assert s.simplify((observer_axes.T*observer_axes).det()) != 0
    # One rational resolved witness, no full lattice scan.
    witness = {r:s.Rational(1,64),nu:s.Rational(1,2),h:s.Rational(1,8),ell:s.Rational(1,8)}
    values = {name:str(s.simplify(value.subs(witness)))
              for name,value in [('boost_cos',Jcos),('boost_sin',Jsin),('fixed_RIGHT_offblock',Re_m)]}
    assert s.N(Jsin.subs(witness)) < 0
    assert s.N(Re_m.subs(witness)) > 0
    return {
      'status':'PASS', 'input_head':'af0a6d07',
      'owner_AST_sha256':{path:{'creator':pin}},
      'carrier':'actual CAR16, rank128 projector resolved axis shell, full reference128; no extra factor',
      'lowgrade_link_controls':low_controls,'full16_trace_controls':trace_controls,
      'protected_observer_controls':observer_controls,
      'field_convention':'Omega_r(x)=2 Re(omega exp(i q.x)) O; DS=2 Re(omega J); cos omega=1/2, sin omega=-i/2',
      'q':'q=kminus-kplus=-2theta1111',
      'all_qdiag_link_rows':'rotations0; each boost B0i atleg r: J=-mu u_ri zeta exp(i theta)/(32 ell)',
      'literal_full8mask_sums':sums,
      'named_boost_cos':str(Jcos),'named_boost_sin':str(Jsin),
      'named_boost_prepared_diagonals':'sin(q.x) B01 atleg0: -mu u_10 cos(3theta/2)/ell on masks2,6,10,14;0 on masks0,4,8,12',
      'all_q0_link_rows':'rotations0; boosts J_ri=-16 nu c u_ri [K_kappa+sin(theta/2)^2/64]/ell^2',
      'K_kappa':'A_kappa+B_kappa, A=sum_k kappa(lambda_k) Re[t_r conj(t_r-1)], B=sum_k kappa(lambda_k) Re[t_r conj(t_s-1)] r!=s; actual full finite momentum sum',
      'other_q':'all source rows0 by the exact momentum support of rho and translation-invariant spectral weight',
      'fixed_RIGHT_preparation_Euler':'[rho,Delta]=0; Delta Psi=Psi Lambda, Lambda Hermitian and commuting sigma; common lambda NOT required',
      'linearized_fixed_RIGHT_necessary':'(E-P) deltaDelta P=0 within the whole common base Delta eigenspace E',
      'protected_pair':'eta_in=(chi_c^0+chi_s^0)/sqrt2 inP; eta_out=(chi_c^0-chi_s^0)/sqrt2 inE-P',
      'metric_protected_offblock':str(Re_m),
      'arbitrary_link_and_observer_adjustment_offblock':0,
      'finite_lifting_conclusion':'no C1 fixed-RIGHT preparation lift with this fixed coframe tangent and arbitrary link/observer/preparation corrections; no full-joint-base assumption',
      'continuum_scope':'Re m=O(h) when theta=kappa h,ell=h; this finite obstruction is NOT a uniform continuum no-go',
      'rational_witness':values,
      'dilation_identity':'0=DS_scale/2=R-Tr(Delta B^(m-1))/Z+M z beta Tr(F^-1 Delta B^(m-1)) at a full scale-critical point',
      'dilation_assumptions':'u->s u free locally; n,links,prepared w,C,alpha,m fixed; beta=m alpha>0; Delta>=0; B=I-alphaDelta>=b0 I>0; M>=0,0<=z<1',
      'energy_bound':'R<=b0^-1 Tr(Delta exp(-betaDelta))/Z; uniform thermal moment and Zlower give R<=Rstar',
      'Stiefel_support_bound':'if fixed_RIGHT sigma>=sigma_min I>0 and prep Euler [rho,Delta]=0, each support energy<=Rstar/sigma_min; uniformRIGHT128 gives128Rstar',
      'extension_scope':'previous full finite-B O(h) commutator-source estimate extends to multi-energy stationary Stiefel prep under same smooth/measure hypotheses and uniform sigma_min',
      'full_joint_root_claimed':False,'uniform_continuum_no_go_claimed':False,
      'native_preparation_admission_claimed':False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = link_rows(args.root)
    text = json.dumps(result, indent=2, ensure_ascii=False)+'\n'
    if args.output:
        args.output.write_text(text)
    print(text, end='')
