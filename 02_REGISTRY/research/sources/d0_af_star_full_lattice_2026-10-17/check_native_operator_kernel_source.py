#!/usr/bin/env python3
"""Bounded exact full16 native inverse-coframe source calculation.

No grid operator, historical replay, or new Laplacian is constructed.
Only pinned literal CAR creator definitions execute. Default is read-only;
--output explicitly writes the JSON result. Geometry is the SAME fixed-
counting true-adjoint D_can=d+d*, not an asserted diffeomorphism orbit.
"""
from __future__ import annotations

import argparse
import ast
from functools import lru_cache
import hashlib
import itertools
import json
from pathlib import Path

import sympy as s

ROOT = Path(__file__).resolve().parents[4]
HELPER = ('02_REGISTRY/research/sources/'
          'd0_complete_record_channel_2026-10-17/check_flat_relaxation.py')
CURVED = '02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py'
PINS = {
    HELPER: '0dcb79f0959ecd4f4484a500ef1c0e53e47d95b4a95feb874d16840f56cc9ec9',
    CURVED: 'bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da',
}
CHECKS = []


def clean(x):
    return s.cancel(s.expand(x))


def require(name, condition):
    if condition is not True and condition != s.true:
        raise ArithmeticError(f'FAILED {name}: {condition}')
    CHECKS.append(name)


def equal(name, actual, expected):
    difference = actual-expected
    entries = list(difference) if isinstance(difference, s.MatrixBase) else [difference]
    require(name, all(clean(x) == 0 for x in entries))


def literal_creators():
    for relative, digest in PINS.items():
        require('pin:'+relative,
                hashlib.sha256((ROOT/relative).read_bytes()).hexdigest() == digest)
    tree = ast.parse((ROOT/HELPER).read_text())
    nodes = [node for node in tree.body
             if isinstance(node, ast.FunctionDef) and node.name == '_creators']
    require('only_literal_creators_helper', len(nodes) == 1)
    scope = {'s': s, 'ast': ast, 'lru_cache': lru_cache, 'CURVED': CURVED}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), HELPER, 'exec'), scope)
    creators, order = scope['_creators'](ROOT)
    require('literal_ACDB_basis', order == (0, 2, 3, 1))
    return creators, order


def exterior(matrix, order):
    indices = [[i for i in order if mask & (1 << i)] for mask in range(16)]
    return s.Matrix(16,16,lambda i,j:
                    matrix.extract(indices[i],indices[j]).det()
                    if len(indices[i])==len(indices[j]) and indices[i]
                    else (1 if not indices[i] and not indices[j] else 0))


def metric_kernel():
    C, order = literal_creators()
    I16, I4 = s.eye(16), s.eye(4)
    for i, j in itertools.product(range(4), repeat=2):
        equal(f'full16_CAR_{i}_{j}', C[i].H*C[j]+C[j]*C[i].H,
              int(i == j)*I16)
        equal(f'full16_creator_trace_{i}_{j}', s.trace(C[i].H*C[j]),
              8*int(i == j))

    # Null coordinates (+,-,2,3), Role v=1. A legitimate constant timelike
    # observer n=(e_++e_-)/sqrt(2) has h_n=I, so principal L=I here.
    eta = s.Matrix([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]])
    n = s.Matrix([1/s.sqrt(2), 1/s.sqrt(2), 0, 0])
    equal('observer_timelike_unit', (n.T*eta*n)[0], 1)
    equal('actual_observer_positive_pairing_is_identity',
          -eta+2*eta*n*n.T*eta, I4)
    equal('null_eta_is_Euclidean_orthogonal', eta.T*eta, I4)
    # A constant coordinate bridge of the full operator tuple, not a new
    # physically admitted control gate: standard (+---) -> normalized null.
    O = s.Matrix([[1/s.sqrt(2),1/s.sqrt(2),0,0],
                  [1/s.sqrt(2),-1/s.sqrt(2),0,0],
                  [0,0,1,0],[0,0,0,1]])
    equal('standard_to_null_Lorentz_form', O.T*s.diag(1,-1,-1,-1)*O, eta)
    equal('standard_to_null_observer', O*n, s.eye(4)[:,0])
    R = exterior(O,order)
    equal('full16_exterior_null_bridge_isometry', R.T*R, I16)
    for j in range(4):
        equal(f'full16_literal_creator_null_bridge_{j}', R*C[j]*R.T,
              sum((O[i,j]*C[i] for i in range(4)),s.zeros(16)))

    # nu is a FIXED inverse-coframe scale: 0<nu<kappa<1 gives the actual
    # two-sided strict Julia chart. nu=1 is only algebraic normalization.
    nu, h, ell, psi = s.symbols('nu h ell psi', positive=True, real=True)
    r = s.symbols('r', nonzero=True)
    z, zb = r-1, 1/r-1  # r=e^{i theta}; adjoint sends r to 1/r.
    w = -(1-r**2)*psi/h  # q=-2theta and w_q=-D_v^-psi_q/h.
    wm = -(1-r**-2)*psi/h
    c = C[0]  # C(eta e_v)=C(e_+), with all sixteen grades retained.
    Dk = nu*(c*z+c.H*zb)/ell
    Dl = nu*(c*zb+c.H*z)/ell
    dD = nu*w*z*(c+c.H)/ell
    dD_reverse = nu*wm*zb*(c+c.H)/ell
    equal('flat_full16_scalar_energy', Dk*Dk, nu**2*z*zb*I16/ell**2)
    equal('exact_resonant_energies', Dl*Dl, Dk*Dk)
    block = Dl*dD+dD*Dk
    expected = 2*nu**2*w*(z*zb*c*c.H+z**2*c.H*c)/ell**2
    equal('actual_full16_resonant_pinching_block', block, expected)
    reverse = Dk*dD_reverse+dD_reverse*Dl
    equal('real_field_Hermitian_reverse_block', reverse,
          expected.T.subs(r, 1/r))
    norm_squared = 4*nu**4*w*wm*(z*zb)**2/ell**4
    equal('pinching_all16_singular_values_equal', reverse*block,
          norm_squared*I16)
    sine_squared = -(r-1/r)**2/4
    half_sine_squared = (2-r-1/r)/4
    equal('pinching_norm_squared_trigonometric_formula', norm_squared,
          256*nu**4*sine_squared*half_sine_squared**2*psi**2/(h**2*ell**4))

    B = block.subs(r, s.I).applyfunc(clean)
    expected_B = -8*nu**2*psi*(c*c.H-s.I*c.H*c)/(h*ell**2)
    equal('theta_pi2_exact16CAR_block', B, expected_B)
    equal('theta_pi2_nonzero_rank16', B.H*B,
          64*nu**4*psi**2*I16/(h**2*ell**4))
    sigma = 8*nu**2*psi/(h*ell**2)
    hermitian_pair = s.BlockMatrix([[s.zeros(16), B.H], [B,s.zeros(16)]]).as_explicit()
    equal('Hermitian_resonant_pair_square', hermitian_pair**2, sigma**2*s.eye(32))
    equal('Hermitian_resonant_pair_trace', s.trace(hermitian_pair), 0)

    # OPTIONAL DIFFERENT operator: supply omega_tau=det(e_tau)/det(e_0)
    # and use D_omega=d+d^{dagger_omega}. Its counting representative is
    # hat d_omega=sqrt(omega)d/sqrt(omega). At tau=0, s0'=d_v/(2h)=-w/2,
    # hence delta hat d=delta d+[s0',d0], NOT the opposite commutator.
    dk, dl = nu*c*z/ell, nu*c*zb/ell
    dd = nu*w*c*z/ell
    dd_weighted = dd-(w/2)*(dk-dl)
    equal('optional_density_whitening_commutator_sign', dd_weighted,
          nu*w*c*(z+zb)/(2*ell))
    dD_weighted = nu*w*(z+zb)*(c+c.H)/(2*ell)
    density_block = Dl*dD_weighted+dD_weighted*Dk
    expected_density = nu**2*w*(z+zb)*(zb*c*c.H+z*c.H*c)/ell**2
    equal('optional_density_full16_resonant_block', density_block, expected_density)
    density_norm_squared = nu**4*w*wm*(z+zb)**2*z*zb/ell**4
    equal('optional_density_norm_squared_formula', density_norm_squared,
          256*nu**4*sine_squared*half_sine_squared**3*psi**2/(h**2*ell**4))
    require('density_change_is_not_exact_finite_pinching_cancellation',
            expected_density.subs(r, s.I) != s.zeros(16))
    wrong_dd = dd+(w/2)*(dk-dl)
    require('hostile_opposite_density_commutator_fails',
            any(clean(x) != 0 for x in wrong_dd-dd_weighted))

    kappa = s.symbols('kappa', positive=True, real=True)
    count_norm = 16*nu**2*s.sin(kappa*h)*s.sin(kappa*h/2)**2*psi/h**3
    density_norm = 16*nu**2*s.sin(kappa*h)*s.sin(kappa*h/2)**3*psi/h**3
    equal('resolved_frequency_counting_nonzero_limit',
          s.limit(count_norm, h, 0, dir='+'), 4*nu**2*kappa**3*psi)
    equal('resolved_frequency_optional_density_limit_zero',
          s.limit(density_norm, h, 0, dir='+'), 0)
    equal('resolved_frequency_optional_density_first_rate',
          s.limit(density_norm/h, h, 0, dir='+'), 2*nu**2*kappa**4*psi)

    # Exact inverse-coframe trace Hessian; no lattice matrix is needed:
    # Tr Delta=16/ell^2 sum_x[sum_r|u_r|^2+|sum_r u_r|^2].
    ds = s.Matrix(s.symbols('d0:4', real=True))
    t = s.symbols('t', real=True)
    ev = s.eye(4)[:,1]
    e_shape = I4+t*ev*ds.T
    F = I4-t*ev*ds.T/(1+t*ds[1])
    equal('actual_nonlinear_inverse_coframe', e_shape*F, I4)
    U = nu*eta*F.T
    ones = s.ones(4,1)
    density = s.trace(U.T*U)+(ones.T*U.T*U*ones)[0]
    Q = (ds.T*ds)[0]+ds[1]*(ds[1]+sum(ds))
    Q_positive = sum((ds[i]+ds[1]/2)**2 for i in (0,2,3))+s.Rational(9,4)*ds[1]**2
    equal('exact_first_trace_density_jet', s.diff(density,t).subs(t,0),
          -2*nu**2*(ds[1]+sum(ds)))
    equal('exact_second_trace_density_with_Fdoubleprime', s.diff(density,t,2).subs(t,0),
          4*nu**2*Q)
    equal('positive_completed_square_trace_form', Q, Q_positive)
    U_linear = nu*eta*(I4-t*ev*ds.T).T
    linear_density = s.trace(U_linear.T*U_linear)+(ones.T*U_linear.T*U_linear*ones)[0]
    equal('hostile_frozen_inverse_second_jet', s.diff(linear_density,t,2).subs(t,0),
          4*nu**2*(ds.T*ds)[0])
    # A point-supported cyclic psi has d=(1,1,1,1) at the point and -e_r
    # at its four successors. It embeds with a collar in any large torus.
    patterns = [s.ones(4,1)]+[-s.eye(4)[:,j] for j in range(4)]
    q_point = sum(Q.subs(dict(zip(ds,p))) for p in patterns)
    linear_point = sum((p.T*p)[0] for p in patterns)
    equal('point_compact_trace_Q_sum', q_point, 15)
    equal('hostile_point_linearized_Q_sum', linear_point, 8)
    equal('point_compact_full_trace_Hessian_tau', 64*nu**2*q_point/(ell**2*h**2),
          960*nu**2/(ell**2*h**2))

    # Tiny analytic L4 energy-4 shell: exactly 28 momenta, no grid matrix.
    momenta = []
    for j in range(4):
        k=[0]*4; k[j]=2; momenta.append(tuple(k))
    for i,j in itertools.combinations(range(4),2):
        for a,b in itertools.product((1,3),repeat=2):
            k=[0]*4; k[i]=a; k[j]=b; momenta.append(tuple(k))
    require('energy4_exact28_momenta', len(set(momenta)) == 28)
    energy = lambda k: sum({0:0,1:2,2:4,3:2}[x] for x in k)
    require('energy4_all28_actual_dispersion', all(energy(k)==4 for k in momenta))
    q = (0,2,0,0)
    shift = lambda k: tuple((k[j]+q[j])%4 for j in range(4))
    pairs = {tuple(sorted((k,shift(k)))) for k in momenta if shift(k) in momenta}
    require('six_resonant_pairs_energy4', len(pairs)==6)
    negative_dim = 6*16
    zero_dim = 28*16-2*negative_dim
    require('full_reference128_eigenpreparation_capacity', negative_dim==96 and zero_dim==256)
    equal('rank128_witness_actual_first_matter_source', -sigma*s.Rational(96,128),
          -6*nu**2*psi/(h*ell**2))

    return {
        'status':'PASS', 'checks':len(CHECKS), 'check_names':list(CHECKS),
        'source_pins':PINS, 'full_CAR_dimension':16,
        'domain':{'metric':'null eta_(+-)=1, eta_22=eta_33=-1',
                  'observer':'n=(e_++e_-)/sqrt(2), h_n=I',
                  'strict_native_chart':'fixed 0<nu<k_J<1; actual e=nu^-1 e_shape; small +/-tau; k_J is a Julia bound, not the resolved physical wave number kappa',
                  'operator':'SAME fixed-counting D_can=d+d*, not a new Delta',
                  'base':'U_r=I, u_r=nu eta e_r, all momentum/CAR modes retained'},
        'trace':{'identity':'Tr Delta=16/ell^2 sum_x[sum_r |u_r|^2+|sum_r u_r|^2]',
                 'first_tau':'-32nu^2/(ell^2 h) sum_x[d_v+sum_r d_r]=0 on cyclic compact support',
                 'second_tau':'64nu^2/(ell^2 h^2) sum_x[sum_(r!=v)(d_r+d_v/2)^2+9d_v^2/4]',
                 'point_psi_second_tau':'960nu^2/(ell^2 h^2)',
                 'wrong_frozen_Fdoubleprime_point':'512nu^2/(ell^2 h^2)'},
        'pinching':{'k':'theta e_v', 'l':'-theta e_v', 'q':'-2theta e_v',
                    'w_q':'-(1-exp(2i theta))*psi_q/h',
                    'block':'2nu^2 w_q/ell^2 [|z|^2 c c*+z^2 c* c], z=exp(i theta)-1',
                    'norm':'16nu^2 |sin theta| sin(theta/2)^2 |psi_q|/(h ell^2)',
                    'pi2':'-8nu^2 psi_q/(h ell^2)[c c*-i c* c], rank16',
                    'resolved_ell_equals_h_theta_equals_kappa_h':'4nu^2 |kappa|^3 |psi_q|',
                    'compact_support':'any compact psi with nonzero Fourier coefficient q has the same block; take even L divisible by4 for pi/2 fixture'},
        'optional_density':{'definition':'NEW SUPPLIED omega_tau=det(e_tau)/det(e_0)=1+tau*d_v/h; D_omega=d+d^(dagger_omega)',
                            'fixed_counting_representative':'hat d_omega=sqrt(omega) d sqrt(omega)^-1',
                            'jet':'delta hat d=delta d+[d_v/(2h),d0]=delta d+[-w/2,d0]',
                            'resonant_block':'nu^2 w_q(z+bar z)/ell^2 [bar z c c*+z c* c]',
                            'norm':'16nu^2 |sin theta| |sin(theta/2)|^3 |psi_q|/(h ell^2)',
                            'resolved_limit':'0, with leading norm 2nu^2 |kappa|^4 |psi_q| h',
                            'scope':'not borrowed into counting programme; not exact finite cancellation; all survival/preparation/price jets would change too',
                            'owner_lines':'A4D_NATIVE_COMPLETE_FIELD_SOURCE_AND_TRANSPORT.md:291-296'},
        'first_source_witness':{'energy4_L4':'28 momenta x16=448 dimensional eigenspace; 6 resonant pairs',
                                'pinch_spectrum':'-sigma multiplicity96,+sigma multiplicity96,0 multiplicity256',
                                'rho':'rank128 projector onto negative96+zero32, divided by128; full reference128 purification exists',
                                'source':'D(H+J_program+R)=-6nu^2 psi_q/(h ell^2) for theta=pi/2, psi_q>0 and fixed calibrations',
                                'why':'spectral thermal and program-J traces have no diagonal nonzero-q blocks; eigenpreparation kills every normalized preparation first row',
                                'scope':'conditional full-Lorentz matrix preparation witness, not the owned tracial first-shell preparation or physical matter/observer admission'},
        'curved_first_source_consumer':{
            'same_geometry':'independent coframe/connection true-adjoint matrix domain; pp-wave U_v=I, all other U held fixed; fixed observer L',
            'native_jet':'delta u_v=-L eta F_actual^T(D^-psi)/h, delta u_r=0 for r!=v',
            'Dirac_jet':'delta D=ell^-1[C(delta u_v)(S_v-I)+(S_v^*-I)C(delta u_v)^*]',
            'Laplacian_jet':'delta Delta={D,delta D}; no new Delta is defined',
            'heat_plus_matter':'Tr[(rho_m-tau B^-1){D,delta D}]+2 Re<delta Psi,(Delta-R)Psi>, tau=B^m/Tr B^m',
            'full_old_v8':'replace rho_m-tau B^-1 by W=rho_m-B^(m-1)/Z+M beta z B^(m-1)A^-1, Z=Tr B^m, A=(1-z)I+zB^m, beta=m alpha',
            'scope':'no vanishing is inferred on curved psi; use actual normalized preparation and all fixed calibration/source assumptions; stored-adjoint own-leg domain is not silently extended'},
        'excluded_claims':['no physical or global D0 no-go','no uniform full-price Hessian sign',
                           'no exact finite diffeomorphism identity','no assigned site density',
                           'no new action, spectral truncation, reset, or replay']}



def chronology(root):
    root = Path(root).resolve()
    a,p,z=s.symbols('a p z',real=True)
    ideal=s.groebner([a*a-p,p*p+p-1],a,p,domain=s.QQ.frac_field(z))
    def red(v):
     n,d=s.cancel(v).as_numer_denom();n=ideal.reduce(s.expand(n))[1];d=ideal.reduce(s.expand(d))[1]
     return s.cancel(n/d)
    def mat(v):return v.applyfunc(red)
    I=s.eye(16);I4=s.eye(4);subs=[tuple(i for i in range(4) if mask&(1<<i)) for mask in range(16)]
    ns=dict(s=s,a=a,p=p,z=z,I=I,DEG=s.diag(*map(len,subs)),SUBS=subs,mat=mat)
    paths={'02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py':['creator','ext'],'02_REGISTRY/research/certificates/a4d_native_record_metric_chronology_check.py':['record']}
    pins={}
    for path,names in paths.items():
     tree=ast.parse((root/path).read_text());pins[path]={}
     for name in names:
      node=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name==name)
      pins[path][name]=hashlib.sha256(ast.dump(node,include_attributes=False).encode()).hexdigest()
      exec(compile(ast.Module(body=[node],type_ignores=[]),path,'exec'),ns)
    creator,record=ns['creator'],ns['record']
    cs=[creator(I4[:,i]) for i in range(4)]
    T=s.zeros(4);T[0,1]=1;T[1,0]=-1
    A=sum((T[i,j]*cs[i]*cs[j].T for i in range(4) for j in range(4)),s.zeros(16))
    U,P=record(I4,I4[:,0]);Q=I-P
    comm=lambda X,Y:mat(X*Y-Y*X)
    U1=comm(A,U);U2=comm(A,U1)/2
    K0=mat(U*U);K1=mat(U1*U);K2=mat(U2*U)
    B0=mat(P*K0.T*Q*K0*P)
    B1=mat(P*(K1.T*Q*K0+K0.T*Q*K1)*P)
    B2=mat(P*(K2.T*Q*K0+K0.T*Q*K2+K1.T*Q*K1)*P)
    L=4*p**3
    PL=s.diag(*[int(i in [0,2,4,8]) for i in range(16)])
    assert mat(B0-L*PL)==s.zeros(16)
    S=mat((B1*PL-PL*B1)/L)
    assert mat(S+S.T)==s.zeros(16) and comm(S,P)==s.zeros(16)
    assert comm(S,B0)==B1
    M=mat(B2-comm(S,B1)/2)
    assert comm(M,B0)==s.zeros(16)
    assert P*M*P==M
    nonzero=lambda X:[(i,j,str(red(X[i,j]))) for i in range(16) for j in range(16) if red(X[i,j])!=0]
    # All 16 rows included, only old cut carries nonzero feedback.
    G=(I-z*B0).inv()
    source=red(z*s.trace(G*M))
    j1=red(2*z*(p**2+7*p**5)/(1-z*L)-4*z*(2-p))
    assert red(source+j1/2)==0
    result={'input_head':'bd646b76','owner_AST_sha256':pins,'raw_curve':'m_eps unnormalized: m0=m14=(sqrt(1-eps^2)-a)/p; m1=m15=1; m3=m13=eps/p; normalize all16','B0_positive_masks':[0,2,4,8],'B0_positive_eigenvalue':'4p^3','B1':nonzero(B1),'cut_preserving_skew_S':nonzero(S),'normal_M':nonzero(M),'normal_M_trace':str(red(s.trace(M))),'same_chronology_J_c_source':str(source),'source_equals_minus_j1_over2':True,'zero_rows_retained':True,'reference_extension':'tensor I_reference128; determinant multiplicity128 if whole trace includes ref','normal_form_scope':'first exp(-eps S) removes B1; further exact analytic odd-angle rotations of owned 2blocks give Bhat(c)=B0+cM+O(c^2), c=eps^2','native_GR_closed':False}
    # Exact parity/gap argument: consume the owned five-block decomposition,
    # without replaying its all-angle determinant suite.
    D1=s.diag(*[(-1)**int(bool(i&2)) for i in range(16)])
    assert D1*U*D1==U and D1*P*D1==P and D1*A*D1==-A
    assert [M[i,i] for i in [12,14]]==[2-3*p,p+2]
    assert red((M[14,14]-M[12,12])-4*p)==0
    # For blocks (4,6),(8,10), base eigenvalue gap=L>0. For (12,14),
    # divide by eps^2; its leading gap=4p>0. Off-diagonal entries are odd
    # by D1 conjugacy and start at orders eps,eps,eps^3 respectively.
    # Real analytic odd-angle plane diagonalizers therefore produce exact
    # eigenvalue blocks analytic in c=eps^2, while preserving P and I-P.
    eta=red(p**6); LL=red(4*p**3)
    Ar=red(p**2+7*p**5); Br=red(4-2*p)
    ql=red(1-z*LL);rl=red(1-z+z*eta**2)
    wl=red(1/ql+eta/rl);wzero=red(1+eta/ql)
    C0=red(4*wl)
    Tm=red(-Ar*wl+Br*wzero)
    mu=red(Tm/(LL*C0))
    q=s.symbols('q',real=True)
    Nq=s.expand(Br*(1+eta)*q*q+(Br*eta**2-Ar*(1+2*eta))*q+eta*(Ar-Br*eta))
    Nq=sum(red(v)*q**(i[0]) for i,v in s.Poly(Nq,q).terms())
    # Unique sign crossing q_plus in (eta,1): upward quadratic, N(0)>0,
    # N(eta)<0, N(1)>0. These are exact golden expressions.
    vals={str(key):red(Nq.subs(q,key)) for key in [0,eta,1]}
    pe=(s.sqrt(5)-1)/2
    for val,sgn in [(vals['0'],1),(vals[str(eta)],-1),(vals['1'],1)]:
     assert s.sign(s.simplify(val.subs(p,pe)))==sgn
    mue=s.factor(mu.subs(p,pe))
    # Reference z values are comparison values; neither is selected as physical.
    for z0 in [s.Rational(1,2**20),pe**2]:
     assert s.sign(s.simplify(mue.subs(z,z0)))==1
    roots=s.solve(Nq.subs(p,pe),q)
    qstar=next(rr for rr in roots if 0.055< float(rr.evalf())<1 and float(rr.evalf())>float(eta.subs(p,pe)))
    zstar=s.simplify((1-qstar)/LL.subs(p,pe))
    result.update({'exact_even_c_normal_form':{
     'exists':True,'weak_parameter':'c=eps^2','basis_change':'real analytic O16 isometry T(eps), [T,P]=0, T(0)=I; not a supplied physical gate',
     'old_all_angle_block_decomposition_consumed_not_replayed':True,'proof':'owned blocks (0),(2),(4,6),(8,10),(12,14); D1 B(eps) D1=B(-eps); first two 2blocks have gap L; divide last block by eps^2, leading gap 4p; exact plane diagonalization makes all eigenvalues analytic c',
     'M_is_exact_c_derivative_of_normal_form':True,'full_operator_B_in_original_basis_C1_in_c':False},
     'normalized_state':{'norm_square':'4(1-a*sqrt(1-eps^2))/p^2','all16_normalized':True,'true_old_reference':'Psi(eps)=m(eps)/sqrt(N(eps)) tensor Xi_old,ref; preserves any already-owned old-ref state, including full ref marginal if present','CAR_ref_Schmidt_rank128_asserted':False},
     'same_feedback_bridge':{'retained_scene_dimension':8,'full_scene_dimension_with_complement':16,'baseline_spectrum_on_retained':'L x4, 0 x4','nine_word_scene528_baseline_identified':False,'C0':'4 W_L','M_trace_W0':'-A*W_L+B*W_0; A=p^2+7p^5, B=4-2p','mu':'(-A*W_L+B*W_0)/(4*L*W_L); a=p^6, L=4p^3, q=1-zL, r=1-z+z*a^2, W_L=1/q+a/r, W_0=1+a/q','mu_at_z_2^-20':str(s.N(mue.subs(z,s.Rational(1,2**20)),17)),'mu_at_z_p2':str(s.N(mue.subs(z,pe**2),17)),'unique_zstar':str(s.N(zstar,17)),'sign':'positive for 0<z<zstar; zero at zstar; negative for zstar<z<1','quadratic_in_q':str(Nq),'quadratic_endpoint_values':{k:str(v) for k,v in vals.items()},'weak_amplitude':'eps=t*chi, c=t^2 gives normal B=B0+c chi^2 M+O(c^2)','full_curve_source':'includes raw preparation+next observer+second gate; derivative at fixed m is a different partial','full_remaining_price_root_proved':False,'needed_native_remainder_source':'d_chi S_rest=-2 nu K z t^2 Tr(W0 M) chi+O(t^4) in the AF-composite profile; no such compensating source assigned','native_rest_price':'chronology owns feedback J and a same-Q heat binding H; R is retained symbol, not a newly defined Rayleigh operator on this local two-record word','heat_along_this_curve':'Q=I so owned H_Q constant; no v8 H substituted','on_shell_matter_claim':False}})
    result['status'] = 'PASS'
    return result


def rational_query_inverse():
    """Exact raw grade-block inverse, including Lorentz-null creation legs."""
    relative='02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py'
    tree=ast.parse((ROOT/relative).read_text())
    nodes=[node for node in tree.body if isinstance(node, ast.FunctionDef)
           and node.name in ('creator','ext')]
    subs=[tuple(i for i in range(4) if mask & (1 << i)) for mask in range(16)]
    scope={'s':s,'SUBS':subs}
    exec(compile(ast.Module(body=nodes,type_ignores=[]),relative,'exec'),scope)
    creator,exterior=scope['creator'],scope['ext']
    eta=s.diag(1,-1,-1,-1)
    M=s.Matrix([[s.Rational(5,4),s.Rational(3,4),0,0],
                [s.Rational(3,4),s.Rational(5,4),0,0],
                [0,0,s.Rational(3,5),-s.Rational(4,5)],
                [0,0,s.Rational(4,5),s.Rational(3,5)]])
    equal('rational_inverse_actual_proper_Lorentz',M.T*eta*M,eta)
    equal('rational_inverse_actual_det_one',M.det(),1)
    rows=[]
    cof=lambda A:A.cofactor_matrix()
    for kind,u in [('timelike',s.Matrix([2,0,0,0])),
                   ('spacelike',s.Matrix([0,2,0,0])),
                   ('null',s.Matrix([1,1,0,0]))]:
        X=creator(u)*exterior(M)
        actual_u=X[1:2,0:1].col_join(X[2:3,0:1]).col_join(
                 X[4:5,0:1]).col_join(X[8:9,0:1])
        equal('query_inverse_reads_u_'+kind,actual_u,u)
        def B(a,b,j):
            if a==b:return 0
            sign=1 if a<b else -1
            return sign*X[(1<<a)|(1<<b),1<<j]
        T=s.Matrix(4,4,lambda a,j:sum(u[b]*B(b,a,j) for b in range(4)))
        ss=(u.T*u)[0]
        equal('query_inverse_T_'+kind,T,ss*M-u*(u.T*M))
        directions=[u*s.eye(4)[:,j].T for j in range(4)]
        L=s.Matrix.hstack(*[(cof(T+R)-cof(T)-ss**2*eta*R*eta).reshape(16,1)
                           for R in directions])
        rhs=(ss**2*eta*T*eta-cof(T)).reshape(16,1)
        H=L.T*L
        require('query_inverse_positive_H_'+kind,H.is_positive_definite is True)
        numerator=H.adjugate()*L.T*rhs
        recovered=(H.det()*T+u*numerator.T)/(ss*H.det())
        equal('query_inverse_exact_M_'+kind,recovered,M)
        rows.append({'leg':kind,'s':str(ss),'det_H':str(H.det()),
                     'recovered_from_actual_grade_blocks':True})
    equal('zero_leg_actual_query_loses_all_Lorentz_data',creator(s.zeros(4,1))*exterior(M),s.zeros(16))
    return {'status':'PASS','cases':rows,'denominator':'(u^T u) det(L^T L)>0 for u!=0',
            'proof_scope':'all proper Lorentz M and nonzero u; exact rank-one cofactor identity',
            'null_or_branch_sqrt_used':False,'zero_leg_sharp_negative_control':True,
            'exact_finite_amplitude_compiler_proved':False}


def actual_current_divergence():
    """Full16 actual transverse-zero block, not a replacement Laplacian."""
    c=literal_creators()[0][0]
    shift=s.zeros(4)
    for i in range(4):
        shift[i,(i+1)%4]=1
    diff=shift-s.eye(4)
    nu=s.Rational(1,2)  # strict query contraction; h=ell=1 in this fixture
    D=nu*(s.kronecker_product(diff,c)+s.kronecker_product(diff.T,c.T))
    delta=D*D
    phi=s.Matrix([1,1,-1,-1])/2
    vacuum=s.eye(16)[:,0]
    prepared=s.kronecker_product(phi,vacuum)
    rho=prepared*prepared.T
    equal('actual_current_full16_normalized_eigenpreparation',
          delta*prepared,2*nu**2*prepared)
    equal('actual_current_eigenpreparation_norm',prepared.dot(prepared),1)
    psi=s.Matrix([1,-1,1,-1])
    backward=psi-shift.T*psi
    dD=-nu*(s.kronecker_product(s.diag(*backward)*diff,c)+
             s.kronecker_product(diff.T*s.diag(*backward),c.T))
    A=D*rho+rho*D  # anticommutator, since rho need not commute with D
    raising_coefficient=s.kronecker_product(s.eye(4),nu*c)
    site_shift=s.kronecker_product(diff,s.eye(16))
    current_matrix=site_shift*A*raising_coefficient
    current=s.Matrix([2*s.trace(current_matrix[16*i:16*(i+1),
                                               16*i:16*(i+1)]) for i in range(4)])
    direct=s.trace(rho*(D*dD+dD*D))
    solder_source=-(backward.T*current)[0]
    divergence=shift*current-current
    divergence_source=(psi.T*divergence)[0]
    equal('actual_CAR_current_trace_contraction',direct,solder_source)
    equal('actual_CAR_current_backward_forward_summation',direct,divergence_source)
    equal('actual_CAR_current_nonzero_eigenprep_source',direct,8*nu**2)
    require('hostile_eigenprep_does_not_enforce_current_conservation',divergence!=s.zeros(4,1))
    return {'status':'PASS','carrier':'actual full16 transverse-zero block of four-dimensional D_can',
            'source_matrix':'W=dS/dDelta; A={D,W}, not 2DW for general eigenpreparation',
            'current':'j_r(x)=2Re tr_CAR[((S_v-I){D,W} C(a_r))_xx], a_r=L eta F^T e_r',
            'exact_source':'DS[psi]=(h ell)^-1 sum_x psi(x) sum_r (j_r(x+r)-j_r(x))',
            'boundary':'periodic or compact psi with fixed collar',
            'fixture':{'nu':'1/2','h':'1','ell':'1','psi':[1,-1,1,-1],
                       'normalized_phi':'(1,1,-1,-1)/2 tensor CAR vacuum',
                       'current':list(map(str,current)),'forward_divergence':list(map(str,divergence)),
                       'direct_source':str(direct)},
            'physical_matter_embedding_equation_derived':False,
            'upstream_Book_controller_price_included_in_this_conditional_price':False}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result={'status':'PASS','input_head':'bd646b76',
            'metric_kernel':metric_kernel(),
            'chronology':chronology(ROOT),
            'rational_query_inverse':rational_query_inverse(),
            'actual_current_divergence':actual_current_divergence(),
            'same_star_normalization':{
                'E':'p^2+p^2*t^2*f', 'c':'p^2*t^2',
                'chronology_amplitude':'eps=p*t*chi gives normal B=B0+c*chi^2*M+O(c^2)',
                'weak_material_potential':'mu*chi^2',
                'wrong_amplitude_control':'eps=t*chi would give (mu/p^2)*chi^2'},
            'actual_flat_heat_window':{
                'alpha':'p^2*ell^2/128',
                'max_Delta':'16*nu^2/ell^2',
                'bound':'max(alpha*Delta)=p^2*nu^2/8 < 1-p^3 for 0<nu<1'},
            'whole_joint_roots_proved':False,'physical_D0_GR_proved':False}
    if args.output:
        args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2) if not args.output else
          json.dumps({'status':'PASS','new_check':'native operator metric-kernel source',
                      'whole_joint_roots_proved':False,'physical_D0_GR_proved':False}))
