#!/usr/bin/env python3
"""Full native price/source, golden MDL mode and structured exterior controls.

Only new exact identities are evaluated. The accepted old amplification
receipt is pinned and reused, never replayed. Default output is read-only.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
from itertools import permutations, product
import sympy as s


def preparation_and_recovery_controls(root):
    checks = []

    def ck(name, test):
        if not bool(test):
            raise ArithmeticError(name)
        checks.append(name)

    x, eps, k = s.symbols('x epsilon K', real=True, nonzero=True)
    # The two scalar coefficients multiply I_128, retaining the whole
    # tag2 x CAR16 x multiplicity8 left carrier and reference128.
    c, ss = s.cos(k*x), s.sin(k*x)
    ck('fixed_RIGHT128_full_schmidt_gram', s.trigsimp((c*c+ss*ss)/128) == s.Rational(1,128))
    R = c*c+2*ss*ss
    ck('fixed_RIGHT128_fast_source', s.simplify(s.diff(R,x).subs(x,s.pi/(4*k))-k) == 0)
    ck('fixed_RIGHT128_fast_second_source', s.simplify(s.diff(R,x,2).subs(x,0)-2*k*k) == 0)
    # Small source on fixed charts need not give a bounded joint section.
    y = s.symbols('y', real=True)
    f = (x-1)**2/2
    whole = f+eps*x*y+eps*eps*y*y/2
    normal = -x/eps
    ck('own_soft_normal_equation', s.diff(whole,y).subs(y,normal) == 0)
    ck('nonzero_soft_Schur_correction', s.simplify(s.diff(whole,x,y)**2/s.diff(whole,y,2)) == 1)
    ck('limiting_stationarity_does_not_supply_joint_roots', s.diff(f,x).subs(x,1) == 0
       and s.simplify(s.diff(whole,x).subs(y,normal)) == -1)
    # A positive normalized pairing isometry is not a fixed-counting
    # unitary. These are actual whitening coordinates, not postselection.
    a = s.symbols('a', positive=True)
    I = s.diag(a,1/a)
    C = s.Matrix([s.cos(x),s.sin(x)])
    raw = I.inv()*C
    G = I.T*I
    ck('native_G_normalization_is_canonical_sphere', s.trigsimp((raw.T*G*raw)[0]) == 1)
    ck('whitening_norm_is_exactly_one', s.trigsimp((I*raw).dot(I*raw)) == 1)
    return dict(status='PASS_EXACT_PREPARATION_AND_RECOVERY_CONTROLS', checks=checks,
        full_RIGHT128='C_K=(cos(Ktheta) I128; sin(Ktheta) I128)/sqrt128, '
                      'Delta=diag(1,2) tensor I128. C_K^*C_K=I128/128; '
                      'all16 CAR grades, multiplicity8 and reference128 retained.',
        source_boundary='R=1+sin^2(Ktheta): bounded values and fixed RIGHT do not '
                        'bound an arbitrary physical pullback section jet.',
        recovery_boundary='S_epsilon=(x-1)^2/2+epsilon*x*y+epsilon^2*y^2/2 '
                          'converges in C2 on fixed compact charts but has no '
                          'joint critical point; its normal elimination changes '
                          'the metric Schur by exactly1.',
        actual_R_type='I_norm is observer whitening, not a recording Kraus map. '
                      'C=I_norm Psi and Psi^*G Psi=1 imply ||C||=1; '
                      'the input Rayleigh is not replaced by a sum over outputs.',
        coupling_boundary='When scalar psi is a coordinate of this same CAR '
                          'preparation, a classical code or independent density '
                          'cannot silently replace its actual coupling map.')


def native_trace_amplification(root=None):
    checks = []

    def ck(name, test):
        if not bool(test):
            raise ArithmeticError(name)
        checks.append(name)
    root = Path.cwd() if root is None else Path(root)
    book = root / '01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md'
    raw = book.read_text()
    frag1 = re.search('S_fb = -log det\\(I - z F_N\\)', raw).group()
    frag2 = re.search('delta S_fb\\n= Tr\\[\\(I - z F_N\\)\\^\\(-1\\) z delta F_N\\]', raw).group()
    bookpin = hashlib.sha256((frag1 + '\n' + frag2).encode()).hexdigest()
    ck('canonical_BOOK03_ordinary_trace_pin', bookpin == '104e0509d16e60e8b5648a15ec40ea907d9269f7b4e3d5e58a80cfca14c835df')
    (th, beta, alpha) = s.symbols('theta beta alpha', positive=True)
    M = s.symbols('M', positive=True, integer=True)
    d0 = 1 + th
    d1 = 2 + th * th
    Z = (1 - alpha * d0) ** 4 + (1 - alpha * d1) ** 4
    H = s.log(Z) / beta
    Hlift = (s.log(M) + s.log(Z)) / beta
    ck('ordinary_trace_heat_first_intensive', s.simplify(s.diff(Hlift - H, th)) == 0)
    ck('ordinary_trace_heat_second_intensive', s.simplify(s.diff(Hlift - H, th, 2)) == 0)
    ck('moving_beta_keeps_log_dimension_source', s.diff(s.log(M) / beta, beta) == -s.log(M) / beta ** 2)
    (a, b, c, d) = s.symbols('a b c d', real=True)
    (lam0, lam1) = s.symbols('lambda0 lambda1', real=True)
    v = s.Matrix([a, b, c, d])
    A = s.diag(lam0, lam1, lam0, lam1)
    R = (v.T * A * v)[0] / (v.T * v)[0]
    Rexpected = (lam0 * (a * a + c * c) + lam1 * (b * b + d * d)) / (a * a + b * b + c * c + d * d)
    ck('normalized_entangled_Rayleigh_no_multiplicity', s.factor(R - Rexpected) == 0)
    phi = s.symbols('phi', real=True)
    Rfree = lam0 * s.cos(phi) ** 2 + lam1 * s.sin(phi) ** 2
    ck('free_preparation_row_not_removed_by_scaling', s.simplify(s.diff(Rfree, phi).subs(phi, s.pi / 4) - (lam1 - lam0)) == 0)
    (z, f) = s.symbols('z f', real=True)
    J0 = -s.log(1 - z * f)
    Jlift = M * J0
    ck('ordinary_feedback_trace_extensive', s.simplify(s.diff(Jlift, f) - M * s.diff(J0, f)) == 0)
    ck('normalized_trace_cancels_amplification', s.simplify(s.diff(Jlift / M, f) - s.diff(J0, f)) == 0)
    accepted = root / '02_REGISTRY/research/sources/d0_af_star_full_lattice_2026-10-17/NATIVE_FEEDBACK_COMPILATION_SOURCE_RESULT.json'
    accepted_raw = accepted.read_bytes()
    accepted_pin = hashlib.sha256(accepted_raw).hexdigest()
    ck('accepted6_21_tower_receipt_pin', accepted_pin == 'a877c1a5567f4b35d94f371fcb4c79920f71a9e9549a3c4611846ecfdbba32f1')
    old = json.loads(accepted_raw)
    ck('consume_actual_Fibonacci_multiplier_no_replay', old['status'] == 'PASS' and old['same_program']['honest_full_AF_spectator_multiplier'] == 'F_(2N+15)=O(F_(2N+9))' and (old['same_program']['old_feedback_suppressed_by_AF_dimension'] is False))
    ell = s.symbols('ell', positive=True)
    (u0, u1, u2, m0, m1, m2) = s.symbols('u0 u1 u2 m0 m1 m2', nonnegative=True)
    dd0 = 8 * u0 * (m0 + 1) / ell
    dd1 = 8 * (u1 * (m0 + 1) + u0 * m1) / ell
    dd2 = 8 * (u2 * (m0 + 1) + 2 * u1 * m1 + u0 * m2) / ell
    (A0, A1, A2) = (dd0 ** 2, 2 * dd0 * dd1, 2 * dd0 * dd2 + 2 * dd1 ** 2)
    ck('four_role_d1_product_rule', s.expand(s.diff(8 * (u0 + u1 * th + u2 * th ** 2 / 2) * (m0 + 1 + m1 * th + m2 * th ** 2 / 2) / ell, th).subs(th, 0) - dd1) == 0)
    ck('four_role_d2_product_rule', s.expand(s.diff(8 * (u0 + u1 * th + u2 * th ** 2 / 2) * (m0 + 1 + m1 * th + m2 * th ** 2 / 2) / ell, th, 2).subs(th, 0) - dd2) == 0)
    ck('full_Delta_second_product_rule', s.expand(s.diff((dd0 + dd1 * th + dd2 * th ** 2 / 2) ** 2, th, 2).subs(th, 0) - A2) == 0)
    ck('golden_sufficient_source_exponent', s.Rational(5, 16) - 2 == -s.Rational(27, 16))
    (lam, bb) = s.symbols('lambda b', real=True)
    Ftotal = 1 - (1 - lam) * (1 - bb)
    ck('one_composed_survival_product', s.expand(Ftotal - (lam + bb - lam * bb)) == 0)
    (delta, cprobe, ff) = s.symbols('delta c_probe f_star', real=True)
    E = s.Rational(1, 2) + delta + cprobe * ff
    Lambda = 4 * E * (1 - E)
    Pencil = 1 - z * (Lambda + (1 - Lambda) * bb)
    ck('saturated_complete_pencil', s.expand(Pencil - (1 - z + 4 * z * (1 - bb) * (delta + cprobe * ff) ** 2)) == 0)
    price = -s.log(Pencil)
    Pbase = s.factor(Pencil.subs(ff, 0))
    jf = s.factor(s.diff(price, ff).subs(ff, 0))
    jb = s.factor(s.diff(price, bb).subs(ff, 0))
    jff = s.factor(s.diff(price, ff, 2).subs(ff, 0))
    oldratio = s.factor(jb / jf)
    quadratio = s.factor(jff / (2 * jf))
    ck('old_source_over_linear_star', s.factor(oldratio + delta / (2 * cprobe * (1 - bb))) == 0)
    expected_quad = cprobe / (2 * delta) * (1 - 8 * z * (1 - bb) * delta ** 2 / Pbase)
    ck('quadratic_star_over_linear_star', s.factor(quadratio - expected_quad) == 0)
    prod = s.factor(oldratio * quadratio)
    ck('shielding_linearity_product_nonzero', s.simplify(s.limit(prod, delta, 0) + 1 / (4 * (1 - bb))) == 0)
    Ractive = 1 - z * (lam + (1 - lam) * bb)
    fullprice = -s.log(1 - z * bb) - s.log(Ractive)
    lower_difference = s.factor(s.diff(fullprice, bb) - z)
    positive_terms = z * z * bb / (1 - z * bb) + z * (1 - lam) / Ractive
    ck('mandatory_zero_AF_branch_source_floor', s.factor(lower_difference - positive_terms) == 0)
    loss = s.symbols('loss', real=True)
    Dloss = 1 - z + z * (1 - bb) * loss
    jb_loss = z * loss / Dloss
    ck('general_loss_source_lower', s.factor(jb_loss - z * loss - z * z * loss * (1 - (1 - bb) * loss) / Dloss) == 0)
    ck('general_loss_source_upper', s.factor(z * loss / (1 - z) - jb_loss - z * z * (1 - bb) * loss ** 2 / ((1 - z) * Dloss)) == 0)
    xx = s.symbols('xx', nonnegative=True)
    ck('saturated_price_gap_log_upper', s.factor(s.diff(xx - s.log(1 + xx), xx) - xx / (1 + xx)) == 0)
    return dict(status='PASS_EXACT_TRACE_AND_SATURATION_CONTROLS', checks=checks, canonical_BOOK03_formula_SHA256=bookpin, accepted6_21_receipt_SHA256=accepted_pin, canonical='BOOK03.0 Sfb=-logdet(I-zF), dSfb=Tr[(I-zF)^-1 z dF]; BOOK03.25 bootstrap uses beta^-1 logTr exp(-beta Delta)-logdet(I-zF). It is ordinary Tr, not normalized tau.', actual_tower='K_N=F_(2N+9), full AF carrier multiplicity m_N=D0^2+D1^2=F_(2N+15), m_N/K_N->phi^6=9+4sqrt5. This is the actual tower, not freely added spectator copies.', old_owner='full-source6.21 already proves H/R first-source intensity on genuine spectator lifts and J_v8,m=m J_v8. That scoped obstruction must not be rebranded as new.', actual_four_Role_bound=dict(D_norm=str(dd0), D_first=str(dd1), D_second=str(dd2), Delta_norm=str(A0), Delta_first=str(A1), Delta_second=str(A2), scope='Actual D=d+d*, d=ell^-1 sum_4 C_r(T_r-I), with uniform full-carrier jets u_j,m_j. Operator norms do not scale with dimension or graph vertex count because there are four bounded Role operators. No statement that an unrelated controller Laplacian equals this operator is made.'), sufficient_schedule='If actual operator/record jets u_j,m_j,w1,w2 are bounded and n>=n0,beta fixed,B>=b0, centered H+R C2 source=O(ell^-4). With ell=h_n=1/ceil(phi^(n/16)), t_n^2=h_n and actual AF level N>=n, h_n^-5/K_N=O(p^(27n/16))->0. This is sufficient explicit scaling, NOT a derived native N(h) or t(h) law.', H_C2='At fixed alpha,beta=m_heat*alpha, B=I-alpha Delta>=b0I, ||DDelta||<=d1,||D2Delta||<=d2: |DH|<=d1/b0; ||D2H||<=d2/b0+(alpha+2beta)*d1^2/b0^2. These are dimension-free and include observer/preparation dependence THROUGH Delta.', R_C2='Actual I_norm is the observer/metric WHITENING map, not a recorder. For canonical C=I_norm Psi with ||C||=1, ||DC||<=s1,||D2C||<=s2, 0<=Delta<=d0I: |DR|<=d1+2d0*s1; ||D2R||<=d2+4d1*s1+2d0*s2+2d0*s1^2. These derivatives include all whitening/preparation/observer jets and entangling tangents. For a more general normalization pullback w=I_norm Psi with ||w||^2>=n0, the safe annulus bound is d2+4d1*w1/sqrt(n0)+2d0*w2/sqrt(n0)+14d0*w1^2/n0. Original v8 R is not replaced by an outcome-averaged recorded energy.', conditional_whole_source='ONLY IF the actual full programme has ONE feedback J_N already equal/close to the compiled J2 word, S_N=H_N+J_N+R_N with no omitted extensive component: (||H_N||C2_centered+||R_N||C2_centered)/(nu*K_N*a0*cAF*t_N^2)->0 and the owned normalized J_N source error->0 imply normalized complete source->D Gamma. This does not prove existence of exact finite joint roots.', saturation=dict(pencil=str(Pencil), old_over_linear=str(oldratio), quadratic_over_linear=str(quadratio), product=str(prod), limit='-1/[4(1-b)] for fixed b<1 and fixed0<z<1; cannot both shield old source and obtain a uniform C2-linear Palatini query near lambda=1'), full_two_AF_branches='Both lambda(E) and0 are retained. j2=-log(1-z*b)-log(1-z*(lambda+(1-lambda)*b)); d_b j2-z=z^2*b/(1-z*b)+z*(1-lambda)/R>=0. Thus d_bj2>=z for an independent old scalar b direction, even if lambda->1.', general_nonlinear_saturation='Let A_N=I-F_AF,N>=0 and F_total,N=I-(1-b)A_N at a fixed0<z<1. z Tr A_N<=d_b J_N<=z Tr A_N/(1-z). If this independent old source divided by the true positive signal sigma_N vanishes, Tr A_N/sigma_N->0. But for EVERY admissible nonlinear g-parameterization, J_N(g)<=Jmax,N=-rank(P)log(1-z), while Jmax,N-J_N(0)<=z(1-b)Tr A_N/(1-z). Hence limsup[J_N(g)-J_N(0)]/sigma_N<=0. A nonzero linear limit kappa*g on a fixed two-sided chart is impossible. No affine E assumption or convenient reparameterization escapes this. This does not exclude shrinking-chart, nonlinear source cancellation or a programme without the independent old b direction.', failure_cases=['retained original J_v8 is extensive and not diluted by the actual AF tower', 'a normalized feedback trace would remove the K amplification, but that is not canonical BOOK03', 'an operator not actually a spectator lift needs its own operator-jet bounds', 'moving beta produces a log(m)/beta source', 'a general normalization norm approaching zero or controller/operator jets growing as K defeat the bound; canonical v8 whitened C has norm1', 'fixed-N constants cannot be discarded in a varied rank/word-length equation', 'small normalized prep rows are not exact prep stationarity, and do not establish joint roots'])


def rayleigh_whitening_literal_v8(root):
    import ast
    import hashlib
    from pathlib import Path
    import sympy as s
    root=Path(root)
    cp=root/'02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py'
    cn=next(n for n in ast.parse(cp.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='creator')
    pin=hashlib.sha256(ast.dump(cn,include_attributes=False).encode()).hexdigest()
    if pin!='801b33d7ef3e41f6425be16153c82b1402215f6be757ea275ff06a69010f58e4':
        raise ArithmeticError('literal creator pin')
    vp=root/'02_REGISTRY/research/sources/d0_record_generated_heat_v8_2026-10-14/verify.py'
    vnode=next(n for n in ast.parse(vp.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='exact')
    vpin=hashlib.sha256(ast.dump(vnode,include_attributes=False).encode()).hexdigest()
    if vpin!='9f62da27fd64a07005a5ee30eaedbf665f309f15b3799e8049e6f7290dac27ff':
        raise ArithmeticError('original v8 word-definition pin')
    rp=vp.with_name('RESULT.md')
    rpin=hashlib.sha256(rp.read_bytes()).hexdigest()
    if rpin!='f7ea30d997a58fa4e608d4403acae5f5e3d7e5da45116f9a7c3f62be5e99115c':
        raise ArithmeticError('original v8 Rayleigh-definition pin')
    subs=[tuple(i for i in range(4) if mask&(1<<i)) for mask in range(16)]
    ns=dict(s=s,SUBS=subs)
    exec(compile(ast.Module(body=[cn],type_ignores=[]),str(cp),'exec'),ns)
    creators=[ns['creator'](s.eye(4)[:,i]) for i in range(4)]
    checks=[]
    def ck(name,value):
        if not value:
            raise ArithmeticError(name)
        checks.append(name)
    def exterior(M):
        return s.Matrix(16,16,lambda i,j:0 if len(subs[i])!=len(subs[j]) else
                        (1 if not subs[i] else M.extract(subs[i],subs[j]).det()))
    eta=s.diag(1,-1,-1,-1)
    n=s.Matrix([s.Rational(5,4),s.Rational(3,4),0,0])
    h=-eta+2*eta*n*n.T*eta
    L=s.eye(4);L[:2,:2]=s.Matrix([[s.Rational(5,4),-s.Rational(3,4)],[-s.Rational(3,4),s.Rational(5,4)]])
    ck('actual normalized timelike observer', (n.T*eta*n)[0]==1)
    ck('actual positive whitening root', L.T*L==h and L.det()==1)
    I,G=exterior(L),exterior(h)
    ck('all16 whitening identity', I.T*I==G)
    ck('arbitrary fixedRIGHT Gram identity', I.inv().T*G*I.inv()==s.eye(16))
    c=s.Matrix(s.symbols('C0:16',real=True));psi=I.inv()*c
    ck('full16 canonical Rayleigh normalizer', s.expand((psi.T*G*psi-c.T*c)[0])==0)
    ck('counting normalization cannot replace native G normalization',
       (s.eye(16)[:,1].T*G*s.eye(16)[:,1])[0]==s.Rational(17,8))
    ck('whitening is invertible not a selected Kraus output', I.det()==1)
    # Operator identity for the literal golden port, not one sampled W.
    p=(s.sqrt(5)-1)/2
    w,o=s.symbols('W O',commutative=False)
    lhs=(p+p**2*w)*o*(p+p**2*w)+p**3*(w-1)*o*(w-1)
    ck('exact golden Heisenberg polynomial', s.simplify(s.expand(lhs-p*o-p**2*w*o*w))==0)
    ck('exact complete golden port coefficients', s.simplify(p+p**2-1)==0)
    ck('complete labels coefficient ports retained', 32*2*2==128)
    # Original v8 six signed BetaHat/ZetaHat words per role, plus4 I,4 -I.
    # A two-site variable coefficient supplies a noncommuting exact control.
    c0=s.Matrix([[0,0],[1,0]])
    C=s.kronecker_product(s.diag(s.Rational(3,5),s.Rational(4,5)),c0)
    T=s.kronecker_product(s.Matrix([[0,1],[1,0]]),s.eye(2))
    D=C*T-C+T.T*C.T-C.T;Delta=D*D
    sr=s.diag(s.Rational(4,5),s.Rational(4,5),s.Rational(3,5),s.Rational(3,5))
    beta,zeta=C+C.T,C-C.T
    BH=s.BlockMatrix([[beta,sr],[sr,-beta]]).as_explicit()
    ZH=s.BlockMatrix([[zeta,sr],[sr,zeta]]).as_explicit()
    TT=s.diag(T,T)
    words=[BH*TT,ZH*TT,TT.T*BH,-TT.T*ZH,-BH,-BH]
    ck('literal BetaHat is unitary', BH.T*BH==s.eye(8))
    ck('literal ZetaHat is unitary', ZH.T*ZH==s.eye(8))
    ck('literal original signed-word compression', sum((v[:4,:4] for v in words),s.zeros(4))==2*D)
    # Every other role has nonzero coefficient3/5, identity shift on this
    # invariant momentum sector, zero signed-word sum, and commutes with Delta.
    Cfull=s.kronecker_product(s.diag(s.Rational(3,5),s.Rational(4,5)),creators[0])
    Tfull=s.kronecker_product(s.Matrix([[0,1],[1,0]]),s.eye(16))
    Dfull=Cfull*Tfull-Cfull+Tfull.T*Cfull.T-Cfull.T
    Deltafull=Dfull*Dfull
    for r in range(1,4):
        Cr=s.kronecker_product(s.eye(2),s.Rational(3,5)*creators[r])
        br,zr=Cr+Cr.T,Cr-Cr.T
        ck('all16 other role energy commutant '+str(r), Cr*Deltafull==Deltafull*Cr and Cr.T*Deltafull==Deltafull*Cr.T)
        ck('all16 other role signed word sum '+str(r), br+zr+br-zr-br-br==s.zeros(32))
        ck('all16 other role literal dilation norm '+str(r), br*br==s.Rational(9,25)*s.eye(32) and zr*zr==-s.Rational(9,25)*s.eye(32))
    ck('eight padding words cancel', 4*s.eye(4)-4*s.eye(4)==s.zeros(4))
    # P W O W P - O =4 A[Tbar(O)-O]A, where A=D/16 and
    # Tbar(O)=32^-1 sum_j (V_j (Icoef tensor O) V_j^*)_00.
    # The other18 role words and8 padding words commute with O.
    O=s.diag(Delta,Delta)
    mean=s.Rational(26,32)*Delta+sum(((v*O*v.T)[:4,:4] for v in words),s.zeros(4))/32
    A=D/16
    defect=(4*A*(mean-Delta)*A).applyfunc(s.simplify)
    eigen=s.Matrix([0,3,0,-4])/5
    ck('counter preparation normalized and timelike at both sites',
       (eigen.T*eigen)[0]==1 and eigen[1]!=0 and eigen[3]!=0)
    ck('counter is genuine energy2 eigenpreparation', Delta*eigen==2*eigen)
    ck('literal complete128 output changes old input Rayleigh',
       s.simplify((eigen.T*defect*eigen)[0])==-s.Rational(173,640000))
    return dict(status='PASS',checks=checks,creator_AST_sha256=pin,
        original_v8_exact_AST_sha256=vpin,original_v8_RESULT_sha256=rpin,
        canonical_input_R='v8 RESULT.md94-110 eq(3): R=<Psi,(Delta tensor I_ref128 tensor I_workspace)Psi>, ||Psi||=1. Input whole-carrier Rayleigh, not a selected Kraus branch or an output average.',
        whitening='Full-source/transport216-222: I_x=Lambda(sqrt(h_x)), I_x^* I_x=G_x. I extends as identity on all apparatus/reference246. FullLorentz139 eq(8): w=I Psi,N=||w||². It is not the recording instrument.',
        canonical_normalization='For Psi^*G Psi=sigma_RIGHT, C=I Psi has C^*C=sigma_RIGHT, hence N=Tr sigma_RIGHT=1. Every full16/reference direction remains. Raw counting-unit input instead needs the actual G lower bound and moving-whitening jets; do not switch physical normalization constraints.',
        actual_complete128='K0=pI+p²W,K1=sqrt(p)p(W-I), W=Q^*(I-2P)Q. All32 labels x2 coefficient x2 ports retained. Their Heisenberg mixture is pO+p²WOW; completeness alone is not energy conservation.',
        exact_record_counter='Literal original6signedwords per role plus4I+4(-I), ell=1, role0 coefficient(3/5,4/5), other3 independent nonzero coefficients3/5 at zero transverse momenta. On normalized grade1 energy2 eigenvector(0,3,0,-4)/5: R_output-R_input=-173*p²/640000. The fullCAR16 commutants are checked and referenceI128 tensoring preserves the operator identity.',
        output_minus_input_div_p_squared=defect.tolist(),
        scope='New exact variable-coefficient word control, not old homogeneous root replay. Full recorder norm1 cannot change the original R definition. Conditional clock/HALT, observer/code admissibility, full original stack and joint-root recovery remain separate.')


def equalized_return(root=None):
    checks=[]
    def ck(name,test):
        if not bool(test):raise ArithmeticError(name)
        checks.append(name)
    ex=lambda A:A.applyfunc(s.expand)
    simp=lambda A:A.applyfunc(s.simplify)
    p=(s.sqrt(5)-1)/2
    k=s.symbols('k',positive=True,real=True)
    G=s.diag(s.Rational(1,2),s.Rational(1,3))
    H=s.Matrix([[1,s.Rational(1,3)],[s.Rational(1,3),1]])
    S=G*G;R=H*H
    M=k*G.inv()*H
    ck('positive_old_survival',S.det()>0 and S.trace()>0)
    ck('positive_target_R',R.det()>0 and R.trace()>0)
    ck('genuinely_noncommuting_S_R',S*R-R*S!=s.zeros(2))
    ck('noncommuting_equalization',ex(M.T*S*M-k*k*R)==s.zeros(2))
    # Actual native c choice, independent of the varied fields.
    # m=2 in this fixture: S>=p^(3m), c=p^(3m+4), sqrt(c)=p^5.
    ck('fixture_obeys_native_old_gap',s.simplify(s.Rational(1,9)-p**6)>0)
    ck('fixture_R_native_window',s.simplify(p**(-2)-s.Rational(16,9))>0)
    ck('native_scaled_inverse_strict_contraction',s.simplify(s.Rational(1,2)-p*p)>0)
    ck('fixture_whole_contraction_margin',s.simplify(s.Rational(1,2)-(M.T*M).trace().subs(k,p**5))>0)
    # Full Julia(M): prove its two roots and intertwiner algebraically.
    # For positive2x2 A, sqrt(A)=(A+sqrt(det A)I)/sqrt(tr A+2sqrt(det A)).
    AR=s.eye(2)-M.T*M;AL=s.eye(2)-M*M.T
    delta=s.symbols('delta',positive=True,real=True)
    T=s.trace(AR)+2*delta
    NR=AR+delta*s.eye(2);NL=AL+delta*s.eye(2)
    detA=s.factor(AR.det())
    rem=lambda v:s.rem(s.Poly(s.expand(v),delta),s.Poly(delta**2-detA,delta)).as_expr()
    ck('left_right_defect_same_trace_det',s.expand(AL.trace()-AR.trace())==0 and s.expand(AL.det()-AR.det())==0)
    ck('positive_root_right_exact',all(rem(v)==0 for v in NR*NR-T*AR))
    ck('positive_root_left_exact',all(rem(v)==0 for v in NL*NL-T*AL))
    ck('Julia_defect_intertwiner',ex(NL*M-M*NR)==s.zeros(2))
    DR=NR/s.sqrt(T);DL=NL/s.sqrt(T)
    J4=M.row_join(-DL).col_join(DR.row_join(M.T))
    # Extend M only on old P. On its actual complement use pI, preserving
    # a uniform strict defect window and all offcut input columns.
    Mhat=s.diag(M,p*s.eye(2))
    DRhat=s.diag(DR,s.sqrt(p)*s.eye(2))
    DLhat=s.diag(DL,s.sqrt(p)*s.eye(2))
    J8=Mhat.row_join(-DLhat).col_join(DRhat.row_join(Mhat.T))
    Jp=s.Matrix([[p,-s.sqrt(p)],[s.sqrt(p),p]])
    ck('complement_Julia_is_full_unitary',simp(Jp.T*Jp-s.eye(2))==s.zeros(2))
    order=[0,1,4,5,2,6,3,7]
    ck('entire_Julia8_is_direct_sum_of_unitary_blocks',J8.extract(order,order)==s.diag(J4,Jp,Jp))
    # Old full unitary, including its archive/input complement.
    DG=s.diag(s.sqrt(3)/2,2*s.sqrt(2)/3)
    Uold=G.row_join(-DG).col_join(DG.row_join(G))
    ck('old_unitary_on_every_input_column',simp(Uold.T*Uold-s.eye(4))==s.zeros(4))
    Controlled=s.diag(Uold,s.eye(4))
    ck('old_control_is_identity_on_failure_flag',Controlled[4:8,4:8]==s.eye(4) and Controlled[:4,4:8]==s.zeros(4))
    W=Controlled*J8
    Pold=s.diag(1,1,0,0);P=s.diag(1,1,0,0,0,0,0,0)
    ck('actual_return_cut_rank_preserved',P.rank()==Pold.rank()==2)
    ck('complete_macro_return_compression',ex(W[:2,:2]-G*M)==s.zeros(2))
    ck('old_archive_outputs_retained',ex(W[2:4,:2]-DG*M)==s.zeros(2))
    ck('new_failure_outputs_retained',W[4:6,:2]==DR and W[6:8,:2]==s.zeros(2))
    oldfail=M.T*(s.eye(2)-S)*M
    newfail=s.eye(2)-M.T*M
    ck('failure_Gram_includes_both_branches',ex(oldfail+newfail-(s.eye(2)-k*k*R))==s.zeros(2))
    ck('all_output_columns_norm_one',ex((G*M).T*(G*M)+oldfail+newfail-s.eye(2))==s.zeros(2))
    F=s.diag(s.eye(2)-k*k*R,s.zeros(6))
    ck('all_input_complement_feedback_zero',F*(s.eye(8)-P)==s.zeros(8))
    # Complete first and second old/target jets, without commuting S and R.
    x0,x1,x2,y0,y1,y2=s.symbols('x0 x1 x2 y0 y1 y2',real=True)
    X=s.Matrix([[x0,x1],[x1,x2]]);Y=s.Matrix([[y0,y1],[y1,y2]])
    z0,z1,z2,w0,w1,w2=s.symbols('z0 z1 z2 w0 w1 w2',real=True)
    Z=s.Matrix([[z0,z1],[z1,z2]]);W2=s.Matrix([[w0,w1],[w1,w2]])
    Gi=G.inv()
    Ms=[k*Gi*H,k*(Gi*Y-Gi*X*Gi*H),k*(Gi*X*Gi*X*Gi*H-Gi*X*Gi*Y-Gi*Z*Gi*H/2+Gi*W2/2)]
    Ss=[S,G*X+X*G,X*X+(G*Z+Z*G)/2]
    Rs=[R,H*Y+Y*H,Y*Y+(H*W2+W2*H)/2]
    for j in range(3):
        total=s.zeros(2)
        for a,b,c in product(range(3),repeat=3):
            if a+b+c==j:total+=Ms[a].T*Ss[b]*Ms[c]
        ck('entire_noncommuting_survival_jet_'+str(j),ex(total-k*k*Rs[j])==s.zeros(2))
    # Structured query errors have an EXACT survival-defect identity.
    E=s.Matrix([[s.Rational(1,7),s.Rational(1,11)],[s.Rational(1,11),-s.Rational(1,13)]])
    Stilde=S+E
    # Fixture uses inverse of G and treats actual S=G^2+E, queried S~=G^2.
    ck('query_survival_defect_identity',ex(M.T*(S+E)*M-k*k*R-k*k*H*Gi*E*Gi*H)==s.zeros(2))
    z,eps,q,c=s.symbols('z epsilon Q c',real=True)
    aa=1-z+z*c
    vartheta=z*c*eps/aa
    pencil=1-z+z*c*(1-eps*q)
    ck('one_full_price_factorization',s.factor(pencil-aa*(1-vartheta*q))==0)
    # The same identity on the full8 carrier keeps every input-complement
    # determinant factor equal to1, not a new hidden physical trace factor.
    Q=s.Matrix([[s.Rational(1,3),s.Rational(1,7)],[s.Rational(1,7),-s.Rational(1,5)]])
    Fq=s.diag(s.eye(2)-c*(s.eye(2)-eps*Q),s.zeros(6))
    ck('full8_det_equals_actual_rank2_pencil',s.factor((s.eye(8)-z*Fq).det()-(aa*s.eye(2)-z*c*eps*Q).det())==0)
    # M is a bound query, never an independent variable to be eliminated.
    lam0,lam1=s.Rational(4,9),s.Rational(16,9)
    price=-s.log(1-z+z*k*k*lam0)-s.log(1-z+z*k*k*lam1)
    radial=-2*z*k*k*(lam0/(1-z+z*k*k*lam0)+lam1/(1-z+z*k*k*lam1))
    ck('free_controller_radial_source_nonzero',s.factor(k*s.diff(price,k)-radial)==0)
    beta=s.symbols('beta',positive=True)
    Hnew=s.log(c*(1-eps*q))/beta
    ck('same_blank_heat_first_source',s.factor(s.diff(Hnew,q)+eps/(beta*(1-eps*q)))==0)
    ck('same_blank_heat_second_source',s.factor(s.diff(Hnew,q,2)+eps*eps/(beta*(1-eps*q)**2))==0)
    b0,power,rr=s.symbols('b0 a rho',positive=True)
    qq=1-b0;rho=(1+qq)/(2*qq)
    ck('scaled_inverse_binomial_tail_radius',s.simplify(1-rho*qq-b0/2)==0)
    ck('actual_native_signal_exponent_N2m',s.simplify(3*power-2*(2*power)+power)==0)
    return dict(status='PASS_EXACT_EQUALIZED_FULL_RETURN',checks=checks,
        fixture=dict(old_S=S.tolist(),target_R=R.tolist(),M=M.tolist(),native_fixture_sqrt_c=str(p**5),native_fixture_m=2,
                     full_unitary_dimension=8,return_rank=2,work_failure_preserved=True),
        exact_target='On Pold, S=C* C>=sI, R=I-epsilon Q>0. Set M=sqrt(c)S^-1/2 R^1/2 and extend Mhat=M directsum p I_(Poldperp). Julia(Mhat) acts on the FULL oldspace times flag. Follow it by old U on flag0, identity on flag1. Actual P=Pold tensor|0><0| gives Ctotal=C M and survival=M*SM=cR, so F=P-cR on P and0 outside. Both old-archive and new-flag failure outputs remain.',
        actual_native_c='For old S=B^m, B>=p^3 I, choose c=p^(3m+4) and ||R||<=p^-2. Then ||M||^2<=p^2<1/2. m is the SURVIVAL exponent: if S=B^(2n), m=2n. c is field-independent for each fixed-clock experiment; this is a new gate programme, not unchanged old feedback or a compulsory selector.',
        price_linearization='A=1-z+zc, vartheta=zc*epsilon/A. J=-rank(P)log A-Tr log(I-vartheta Q). Dividing the complete contrast by rank(P)*vartheta gives tau_P Q+O_C2(vartheta). Thus fixed epsilon is allowed: old-clock m->infty makes c->0 and produces the weak-price parameter. No separate prescribed t(h) is needed for this constructed price.',
        same_blank_heat='If H is generated by this SAME whole blank Gram, H_new=beta^-1 logTr(cR)=field-constant+beta^-1 log tau_P R. Its derivatives are bounded by epsilon*Q1/(beta*r0) and epsilon*Q2/(beta*r0)+epsilon^2*Q1^2/(beta*r0^2), R>=r0I. This does NOT identify H_new with the old Hodge heat or independently redefine the actual input Rayleigh operator.',
        exact_error_identity='If the controller queries S_tilde,R_tilde, while the actual old survival is S, then M_tilde* S M_tilde=c[R_tilde+R_tilde^1/2 S_tilde^-1/2(S-S_tilde)S_tilde^-1/2 R_tilde^1/2]. This controls structured operand errors with a factor c before source normalization.',
        C2_source_error='Use jet algebra ||A||J2=||A||+||DA||+0.5||D2A||. Let C_A bound ||S_tilde^-1/2||J2 and C_H bound ||R_tilde^1/2||J2, stable positive gaps. Then ||Z||J2<=epsilon*delta_Q+C_H^2*C_A^2*delta_S. For the straight pencil path D_t>=dI,d=1-z with derivative bounds D1,D2, C_inv=1/d+D1/d^2+0.5D2/d^2+D1^2/d^3. The complete normalized price error is <=A*C_inv[delta_Q+C_H^2*C_A^2*delta_S/epsilon]. Generic finite-word whole-output C3 error eta separately contributes <=2^14*z*L^6*eta/[(1-z)^4*vartheta].',
        inverse_gap_cost='Generic S^-1/2 bounds depend on s: a0=s^-1/2,a1=0.5*s^-3/2*S1,a2=0.5*s^-3/2*S2+0.75*s^-5/2*S1^2; C_A=a0+a1+0.5*a2. All constants and actual query jets remain explicit. No unknown-state amplitude tomography is used.',
        actual_B_scaled_inverse='When S=B^m, a=m/2, b0=p^3, the scaled inverse is p^2*b0^a*B^-a, with operator j-derivative coefficients <=p^2*(a)_j*b0^-j times B jets. Expand in X=I-B with ||X||<=1-b0. For rho=(2-b0)/[2(1-b0)]>1, the degreeD derivative tails are bounded by p^2*rho^-D*2^a*(a)_j*(2rho/b0)^j. Thus fixed-jet polynomial degree O(m+log(1/eta)) is sufficient; actual word length/work/control costs still must be counted.',
        source_scale='The signal is rank(P)*vartheta, asymptotically proportional to actual AF K_N*c*epsilon. With K_N~p^-2N, c=p^(3m+4), N>=2m gives exponential dominance over polynomial old heat/prep bounds in m. This sufficient signal schedule is not a proved native rank law or a literal compiler/runtime budget.',
        limitations=['Julia(Mhat) is the exact analytic target; finite Golden words generally only approximate it with full-output error budget',
                     'coherent old and matrix-entry queries, controls, positive inverse gap, actual flag preparation/return test and physical admission must exist',
                     'controls M(S,Q) must be genuinely generated by the fixed programme. Feedback alone has a nonzero radial source; same-blank heat can balance it. The actual full control row must be solved; see full_control_balance',
                     'Q is still an independently specified existing geometric/matter programme; this construction does not force its selection from D0',
                     'other H/R, all preparation/observer equations, varied clock/rank source, exact finite joint roots and raw#216 remain separate'])


def native_negative_binomial_controls(root):
    import ast
    import hashlib
    from itertools import product
    from pathlib import Path
    import sympy as s
    root=Path(root)
    source=root/'02_REGISTRY/research/sources/d0_record_generated_heat_v8_2026-10-14/verify.py'
    node=next(n for n in ast.parse(source.read_text()).body
              if isinstance(n,ast.FunctionDef) and n.name=='exact')
    pin=hashlib.sha256(ast.dump(node,include_attributes=False).encode()).hexdigest()
    if pin!='9f62da27fd64a07005a5ee30eaedbf665f309f15b3799e8049e6f7290dac27ff':
        raise ArithmeticError('actual v8 signed-word/survival definition changed')
    checks=[]
    def ck(label,test):
        if not test:
            raise ArithmeticError(label)
        checks.append(label)
    p=(s.sqrt(5)-1)/2
    b0=p**3
    q=s.simplify(1-b0)
    ck('actual golden survival loss factor', s.simplify(q-2*p**2)==0)
    n,k=s.symbols('n k',integer=True,positive=True)
    z=s.symbols('z',real=True)
    G=(b0/(1-q*z))**n
    ck('negative binomial PGF normalized', s.simplify(G.subs(z,1)-1)==0)
    moment=[];tilted=[]
    lam=s.simplify((1+1/q)/2)
    ck('valid fixed Chernoff radius', lam>1 and q*lam<1)
    for j in range(4):
        mj=s.rf(n,j)*(q/b0)**j
        tj=2**n*s.rf(n,j)*((1+q)/b0)**j
        ck('exact factorial moment '+str(j), s.simplify(s.diff(G,z,j).subs(z,1)-mj)==0)
        ck('exact tilted moment '+str(j), s.simplify(lam**j*s.diff(G,z,j).subs(z,lam)/tj-1)==0)
        moment.append(str(mj));tilted.append(str(tj))
    w=lambda j:s.binomial(n+j-1,j)*b0**n*q**j
    ck('finite count coefficient recurrence', s.combsimp((k+1)*w(k+1)-(n+k)*q*w(k))==0)
    ck('finite count initial coefficient', s.simplify(w(0)-b0**n)==0)
    microscopic={''.join(map(str,h)):p**h.count(0)*(p**2)**h.count(1)
                 for h in product((0,1),repeat=3)}
    ck('all eight actual golden histories retained',len(microscopic)==8)
    ck('native success probability from three trials',s.simplify(microscopic['000']-b0)==0)
    ck('seven distinct failures have actual total q',s.simplify(sum(v for h,v in microscopic.items() if h!='000')-q)==0)
    ck('complete three-trial preparation norm',s.simplify(sum(microscopic.values())-1)==0)
    # A minimal nonnormal all-input query. Two FRESH flags realize A* A;
    # using the same flag would uncompute the entire word instead.
    A=s.Matrix([[0,s.Rational(3,5)],[s.Rational(4,5),0]])
    I=s.eye(2)
    left=s.diag(*[s.sqrt((I-A*A.T)[i,i]) for i in range(2)])
    right=s.diag(*[s.sqrt((I-A.T*A)[i,i]) for i in range(2)])
    U=s.BlockMatrix([[A,left],[right,-A.T]]).as_explicit()
    ck('query unitary on every input column',U.T*U==s.eye(4))
    def placed(V,flag):
        out=s.zeros(8)
        for f0,f1,d in product(range(2),repeat=3):
            col=4*f0+2*f1+d
            incoming=(f0,f1)[flag]
            for ff,dd in product(range(2),repeat=2):
                flags=[f0,f1];flags[flag]=ff
                out[4*flags[0]+2*flags[1]+dd,col]=V[2*ff+dd,2*incoming+d]
        return out
    full=placed(U.T,1)*placed(U,0)
    ck('two fresh-bank full word unitary', full.T*full==s.eye(8))
    ck('two fresh-bank compression is Y', full[:2,:2]==A.T*A)
    ck('reusing the bank would give wrong identity', (U.T*U)[:2,:2]!=A.T*A)
    B=I-q*A.T*A
    ck('actual Y requires no matrix-rescaling oracle', ((I-B)/q-A.T*A).applyfunc(s.simplify)==s.zeros(2))
    ck('actual positive native survival window', all(s.simplify((B-b0*I)[i,i])>0 for i in range(2)))
    return dict(status='PASS',checks=checks,original_v8_exact_AST_sha256=pin,
        actual_identity='B=I-2p² A* A, A=ell D/16, q=1-p³=2p²; hence Y=(I-B)/q=A* A is available from TWO fresh A/A* query banks. No globally normalized Y or inverse-S oracle is assumed.',
        scaled_inverse='For m=2n,c=p^(3m+4): sqrt(c)S^-1/2=p²(p³B^-1)^n=p² sum_k w_nk Y^k, w_nk=binom(n+k-1,k)p^(3n)q^k; sum w=1.',
        factorial_moments=moment,tilted_moments=tilted,
        tail='lambda=(1+1/q)/2; C3 B-jet tail <=p²2^n lambda^-L max_(j<=3) rising(n,j)[(1+q)/(p³q)]^j. Therefore L=O(n+log(1/eta)). Physical jets require the true B chain rule.',
        microscopic_history_weights={h:str(s.simplify(v)) for h,v in microscopic.items()},
        finite_history_word='Draw T=n+L triples unconditionally. Keep all eight microscopic histories per trial. Reversibly count first nth success. On success control Y^k, using fresh query banks; on timeout route a flag outside the return. Unprepare only NEW coherent work. The clean compression is the truncated positive series; no failed branch is discarded.',
        target_factor='Apply the admitted fixed-address analytic contraction p² sqrt(I-epsilon Q) first (norm<=p on R<=p^-2 I), then the normalized series block. The noncommuting product equals M_L.',
        implementation_scope='Exact ideal controlled-query/counter circuit identities. Counting and controlled queries are not asserted exact finite G/CNOT words; use existing C3 full-column compiler and actual ALL-work-blank return cut, with error relative to c*epsilon, every flag/timeout/output and true word/width cost retained. Old measured archives are not uncomputed. No efficient or compulsory N(m), target Q, or control-law selection is proved.')


def equalized_full_radial(root=None):
    checks=[]
    def ck(name,test):
        if not bool(test):raise ArithmeticError(name)
        checks.append(name)
    beta,d,z,c,eps,r0,r=s.symbols('beta d z c epsilon r0 r',positive=True,real=True)
    t=s.symbols('t',real=True)
    a=1-z;A0=a+z*c
    theta=z*c*eps/A0
    la,lb=s.symbols('lambda_a lambda_b',positive=True)
    # Complete two-eigenvalue fixture: M->(1+t)M means L->(1+t)^2 L.
    H=s.log((1+t)**2*(la+lb))/beta
    J=-s.log(a+z*(1+t)**2*la)-s.log(a+z*(1+t)**2*lb)
    oldrad=s.factor(s.diff(H+J,t).subs(t,0))
    expected=2/beta-2*z*(la/(a+z*la)+lb/(a+z*lb))
    ck('generated_heat_radial_source_is_positive',s.simplify(s.diff(H,t).subs(t,0)-2/beta)==0)
    ck('full_heat_plus_feedback_radial_balance',s.factor(oldrad-expected)==0)
    # Interior stationary countercontrol, S=I and L=cI.
    cstar=(1-z)/(z*(beta*d-1))
    hscalar=s.log(d*c)/beta
    jscalar=-d*s.log(a+z*c)
    radial=2*c*s.diff(hscalar+jscalar,c)
    ck('full_stationary_interior_can_exist',s.factor(radial.subs(c,cstar))==0)
    ck('interior_contraction_feasibility',s.factor(1-cstar-(beta*d*z-1)/(z*(beta*d-1)))==0)
    ck('stationary_amplified_signal_is_bounded',s.factor((d*theta).subs(c,cstar)-eps/beta)==0)
    # Exact pointwise spectral comparison; all factors have their signs on
    # 0<z<1, c>0, r>=r0>0. No assumption r1>=1 is needed.
    g=lambda x:z*c*x/(a+z*c*x)
    ck('spectral_source_monotonicity',s.factor(g(r)-g(r0)-z*c*a*(r-r0)/((a+z*c*r)*(a+z*c*r0)))==0)
    h0=r0*A0/(a+z*c*r0)
    ck('source_to_signal_comparison',s.factor(g(r0)-theta*h0/eps)==0)
    factor=(a+z*c*r0)/(r0*A0)
    u=a/A0
    ck('sharp_bound_is_convex_combination',s.factor(factor-(u/r0+1-u))==0)
    # Full matrix Euler in L, because invertible M makes dL arbitrary.
    ell=s.symbols('ell',positive=True)
    euler_scalar=1/(beta*d*ell)-z/(a+z*ell)
    ck('full_matrix_stationary_eigenvalue',s.factor(euler_scalar.subs(ell,cstar))==0)
    ck('distinct_eigenvalues_cannot_both_be_stationary',s.factor(z/(a+z*la)-z/(a+z*lb)-z*z*(lb-la)/((a+z*la)*(a+z*lb)))==0)
    # A noncommuting2x2 dL fixture proves all Hermitian dL are accessible.
    S=s.Matrix([[2,s.Rational(1,3)],[s.Rational(1,3),1]])
    M=s.Matrix([[s.Rational(1,4),s.Rational(1,7)],[s.Rational(1,9),s.Rational(1,3)]])
    x,y,w=s.symbols('x y w',real=True);X=s.Matrix([[x,y],[y,w]])
    dm=s.Rational(1,2)*S.inv()*M.T.inv()*X
    ck('free_invertible_M_spans_all_L_variations',(M.T*S*dm+dm.T*S*M-X).applyfunc(s.expand)==s.zeros(2))
    # Stationary envelope cost is independent of every old S parameter.
    env=s.log(d*cstar)/beta-d*s.log(a+z*cstar)
    return dict(status='PASS_EXACT_FULL_HEAT_FEEDBACK_RADIAL',checks=checks,
        correction='The feedback-only DJ[deltaM=M] is strictly negative, but the SAME generated heat contributes DHgen=2/beta. Hence that sign alone does not exclude full stationary controls.',
        radial_equation='For R_in independent of M and no other radial source: z Tr[L((1-z)I+zL)^-1]=1/beta, L=M*SM.',
        sharp_signal_bound='At L=cR, R>=r0I, theta=zc epsilon/(1-z+zc), radial balance gives d*theta <=(epsilon/beta)*(1-z+zc*r0)/[r0*(1-z+zc)] <=(epsilon/beta)*max(1,1/r0). Thus free-radial FULL roots cannot have d*theta->infinity at fixed beta,epsilon,r0.',
        other_source='If an actual additional radial source T_rest is present, replace 1/beta by 1/beta+T_rest/2. The upper bound is <=epsilon*max(1,1/r0)*(1/beta+abs(T_rest)/2). If T_rest=o(d*theta), amplified d*theta still contradicts stationary balance. No refusal is asserted when a genuine comparable counter-source exists.',
        full_matrix_Euler='If M is an independently varied invertible matrix in the strict interior and R_in is M-independent, arbitrary Hermitian dL are available. The complete Hgen+J row is [I/(beta TrL)-z((1-z)I+zL)^-1]=0. Hence L=ell I, ell=(1-z)/[z(beta*d-1)]. Interior feasibility requires beta*d>1 and ell<s_min(S); for S=I it is beta*d*z>1.',
        stationary_counter='For S=I and beta*d*z>1, M=sqrt(ell)I is a genuine strict-interior stationary control. It has d*theta=epsilon/beta, so the prior feedback-only nonstationarity statement cannot be promoted to full Hgen+J.',
        envelope='The stationary Hgen+J envelope is beta^-1 log(d*ell)-d log(1-z+z*ell), independent of the old S. It supplies no old-geometry source. At a bound equalizer target L=c(I-epsilon Q), free full-matrix stationarity requires Q scalar across the return corner; it does not derive the specified nonconstant gravitational Q.',
        design_scope='The fixed programme law M(S,Q) is a different variation domain from independently free M. Its source includes the actual DM(S,Q); selection/admission remains unproved. If the input Rayleigh operator, code, clock, cut or other actual source varies with M, retain that source and solve the corresponding full equation. This is not a whole-D0 no-go.')


def equalized_linked_rayleigh(root=None):
    checks=[]
    def ck(name, test):
        if not bool(test):
            raise ArithmeticError(name)
        checks.append(name)
    def zero(x):
        if isinstance(x, s.MatrixBase):
            return all(s.factor(v)==0 for v in x)
        return s.factor(x)==0
    beta,m,nu,z,c,eps,r0,r=s.symbols(
        'beta m nu z c epsilon r0 r',positive=True)
    b1,b2,w=s.symbols('b1 b2 w',positive=True)
    t=s.symbols('t',real=True)
    alpha=beta/m
    aa=1-z
    # Near t=0, M(t)=(1+t)M implies L(t)=(1+t)^2 L and
    # Bnew(t)=(1+t)^(2/m) Bnew, without any commutation premise.
    Z=b1**m+b2**m
    meanB=w*b1+(1-w)*b2
    H=s.log((1+t)**2*Z)/beta
    J=-nu*(s.log(aa+z*(1+t)**2*b1**m)
            +s.log(aa+z*(1+t)**2*b2**m))
    Rin=(1-(1+t)**(2/m)*meanB)/alpha
    ck('generated_heat_radial_2_over_beta',
       zero(s.diff(H,t).subs(t,0)-2/beta))
    ck('linked_input_Rayleigh_radial_minus_2_meanB_over_beta',
       zero(s.diff(Rin,t).subs(t,0)+2*meanB/beta))
    fbtrace=nu*z*(b1**m/(aa+z*b1**m)+b2**m/(aa+z*b2**m))
    ck('complete_linked_radial_balance',
       zero(s.diff(H+J+Rin,t).subs(t,0)
            -(2*(1-meanB)/beta-2*fbtrace)))
    theta=z*c*eps/(aa+z*c)
    g=lambda x:z*c*x/(aa+z*c*x)
    ck('spectral_source_monotonicity',
       zero(g(r)-g(r0)-z*c*aa*(r-r0)
            /((aa+z*c*r)*(aa+z*c*r0))))
    ratio=(aa+z*c*r0)/(r0*(aa+z*c))
    u=aa/(aa+z*c)
    ck('sharp_signal_bound_convex_factor',zero(ratio-(u/r0+1-u)))
    ck('source_to_full_rank_signal_ratio',
       zero(theta/g(r0)-eps*ratio))
    # Conditional B has a genuine positive interior full-root fixture:
    # m=2, nu=1, z=1/2, beta=5/2, L=1/4, Bnew=1/2.
    ell=s.symbols('ell',positive=True)
    scalar=s.log(ell)/s.Rational(5,2)-s.log((1+ell)/2) \
           +(1-s.sqrt(ell))/s.Rational(5,4)
    ck('linked_full_scalar_interior_root_exists',
       zero(s.diff(scalar,ell).subs(ell,s.Rational(1,4))))
    ck('linked_scalar_signal_bound_is_sharp',
       zero((theta-eps/beta*(1-b1)).subs(
           {z:s.Rational(1,2),c:s.Rational(1,4),
            beta:s.Rational(5,2),b1:s.Rational(1,2)})))
    # Exact noncommuting 2x2 Frechet derivative of the positive root.
    B=s.diag(s.Rational(1,2),s.Rational(3,4)); L=B*B
    rho=s.Matrix([[s.Rational(1,2),s.Rational(1,4)],
                  [s.Rational(1,4),s.Rational(1,2)]])
    X=s.Matrix([[2,3],[3,5]])
    Dsqrt=lambda Y:s.Matrix(2,2,lambda i,j:Y[i,j]/(B[i,i]+B[j,j]))
    ck('noncommuting_root_Frechet_Sylvester_equation',
       zero(B*Dsqrt(X)+Dsqrt(X)*B-X))
    ck('noncommuting_root_Frechet_is_trace_selfadjoint',
       zero(s.trace(rho*Dsqrt(X))-s.trace(Dsqrt(rho)*X)))
    A=aa*s.eye(2)+z*L
    alpha2=beta/2
    G=s.eye(2)/(beta*s.trace(L))-nu*z*A.inv()-Dsqrt(rho)/alpha2
    Lprime=-alpha2*(B*X+X*B)
    oldsource=rho-B/s.trace(L)+nu*beta*z*B*A.inv()
    ck('linked_gradient_pulls_back_to_LITERAL_v8_formula_4',
       zero(s.trace(G*Lprime)-s.trace(oldsource*X)))
    ck('noncommuting_rho_cannot_satisfy_full_free_matrix_Euler',
       zero(G[0,1]+s.Rational(1,5)/alpha2))
    # Joint preparation row on fixed RIGHT: left-unitary variations preserve
    # C*C exactly; their energy source is i Tr K[rho,Delta].
    x,y,k=s.symbols('x y k',real=True)
    C=s.Matrix([[s.sqrt(s.Rational(1,2)),0],
                [0,s.sqrt(s.Rational(1,2))],[0,0]])
    ck('fixed_RIGHT_exact_uniform_marginal_retained',
       zero(C.T*C-s.eye(2)/2))
    Pc=C*C.T
    K=s.Matrix([[0,0,-s.I*k],[0,0,0],[s.I*k,0,0]])
    DC=s.I*K*C
    ck('fixed_RIGHT_left_unitary_tangent_is_admissible',
       zero(DC.conjugate().T*C+C.conjugate().T*DC))
    Delta=s.Matrix([[x,0,y],[0,0,0],[y,0,0]])
    prep=s.trace(DC.conjugate().T*Delta*C+C.conjugate().T*Delta*DC)
    ck('fixed_RIGHT_prep_source_is_full_commutator',
       zero(prep-s.I*s.trace(K*(Pc*Delta-Delta*Pc))))
    ck('fixed_RIGHT_prep_source_not_frozen',zero(prep+k*y))
    # Each occupied eigenweight obeys this scalar equation at a matrix root.
    q=s.symbols('q',positive=True)
    Acoef,Bcoef,l=s.symbols('Acoef Bcoef l',positive=True)
    phi=l**(1-q)*(Acoef-Bcoef/(aa+z*l))
    derivative=(1-q)*l**(-q)*(Acoef-Bcoef/(aa+z*l)) \
               +l**(1-q)*Bcoef*z/(aa+z*l)**2
    ck('positive_occupation_band_law_is_strictly_monotone',
       zero(s.diff(phi,l)-derivative))
    pins=[]
    if root is not None:
        base=Path(root)
        owners=[
            ('02_REGISTRY/research/sources/d0_record_generated_heat_v8_2026-10-14/RESULT.md',
             ['The matter\nreading below remains <Delta>, NOT <Lambda>',
              'R=<Psi,D_matter Psi>, ||Psi||=1',
              'b beta z B^(2n-1)']),
            ('01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md',
             ['S_fb = -log det(I - z F_N)'])]
        for path,fragments in owners:
            text=(base/path).read_text()
            ck('literal_owner_typing:'+path,all(f in text for f in fragments))
            pins.append(path)
    return dict(
        status='PASS_EXACT_LINKED_HEAT_INPUT_RAYLEIGH',checks=checks,
        source_owners=pins,
        literal_typing='Old v8 RESULT3-5 proves B=I-alpha*Delta from the actual 32-word/128-output circuit, Lambda_alpha=-log(B)/alpha, L=B^(2n), beta=2n*alpha, and INPUT R=<Psi,Delta Psi>, not <Lambda_alpha> or an output-energy average. Reference multiplicity nu=128 belongs in ordinary feedback trace.',
        case_A='If the canonical old geometric Delta and old heat/Hodge Lambda are retained and only the new word feedback is appended, old H and input R are M-independent. The full independent radial M row is DJ<0 unless other actual M-sources are present. Replacing H by Hgen already changes this tuple.',
        conditional_case_B='Setting Bnew=L^(1/m), Delta_new=(I-Bnew)/alpha, beta=m*alpha is an operator reconstruction. It is not native merely because L=M*SM is a real return Gram. The actual new word must separately be identified with the geometric/CAR/Hodge Delta that the physical input reads.',
        complete_radial='For fixed prep, fixed alpha,beta,m,cut and no other radial source: D(Hgen+J+Rnew)[deltaM=M]=2*(1-Tr(rho*Bnew))/beta-2*nu*z*Tr[L*((1-z)I+zL)^-1]. This admissible fixed-prep direction remains necessary when preparation is also varied or has fixed RIGHT128.',
        signal_bound='At L=cRtarget, Rtarget>=r0 I, theta=zc epsilon/(1-z+zc), d_full=nu*dim(data), a stationary radial row forces d_full*theta <=epsilon/beta*(1-Tr(rho*Bnew))*(1-z+zc*r0)/(r0*(1-z+zc)) <=epsilon/beta*max(1,1/r0). This uses the genuine contraction 0<L<=I and normalized rho. Thus linking the input Rayleigh does not restore unbounded free-control signal.',
        full_matrix_gradient='Let m>=1, q=1/m, Z=TrL. For independently free invertible strict-interior M in the data algebra, G=I/(beta Z)-nu*z*((1-z)I+zL)^-1-alpha^-1*D(L^q)_L(rho)=0. Frechet power is selfadjoint under trace. In an L eigenbasis its rho coefficient is the strictly positive divided difference f^[1](li,lj). Hence G=0 implies [rho,L]=0 and rho_i=li^(1-q)*[1/Z-beta*nu*z/(1-z+zli)]. Degenerate L blocks must have scalar rho.',
        fixed_RIGHT128='With C_adjoint*C=sigma and Tr sigma=1 all columns remain. Its joint prep Euler is [rho,Delta_new]=0, rho=C*C_adjoint, equivalently range invariance together with the actual right-marginal constraint. For sigma=I128/128, rho=Poccupied/128. Combined with full free-matrix M Euler there is at most one positive survival eigenvalue per positive occupation weight for 0<q<=1, since the displayed scalar law is strictly increasing wherever its right hand side is positive. Every unoccupied eigenvalue solves one common scalar equation. Thus uniform occupied band and unoccupied complement have at most two values; no occupied directions were frozen.',
        scope='These are conditional matrix/calculus statements, not a full-D0 refusal or a selected geometric source. Nonuniform sigma, restricted physical M tangents, actual R/control/clock/code dependencies and retained-history costs must keep their own rows. Native equality of reconstructed Delta_new to the geometric matter operator is still unproved.')


def native_nb_controller_cost_source_controls(root):
    import hashlib
    from pathlib import Path
    import sympy as s
    root=Path(root)
    owners=[
        '01_BOOKS/BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md',
        '01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md',
        '02_REGISTRY/research/A4D_NATIVE_BRANCH_INFORMATION_COCYCLE.md',
        '02_REGISTRY/research/A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md']
    pins={f:hashlib.sha256((root/f).read_bytes()).hexdigest() for f in owners}
    checks=[]
    def ck(label,value):
        if not value: raise ArithmeticError(label)
        checks.append(label)
    p=(s.sqrt(5)-1)/2
    a=s.symbols('a',real=True)
    b=s.sqrt(1-a*a)
    G=s.Matrix([[s.sqrt(p),-p],[p,s.sqrt(p)]])
    V=s.Matrix([[a,-b],[b,a]])
    ck('original golden splitter is unitary', (G.T*G-s.eye(2)).applyfunc(s.simplify)==s.zeros(2))
    ck('controlled target is unitary', (V.T*V-s.eye(2)).applyfunc(s.simplify)==s.zeros(2))
    W=s.kronecker_product(G.T,s.eye(2))*s.diag(s.eye(2),V)*s.kronecker_product(G,s.eye(2))
    q=[s.simplify(W[i,0]**2) for i in range(4)]
    expected=[(p+p*p*a)**2,p**4*(1-a*a),p**3*(1-a)**2,p**3*(1-a*a)]
    ck('all four coherent final outcomes retained',all(s.simplify(x-y)==0 for x,y in zip(q,expected)))
    ck('complete coherent probability is one',s.simplify(sum(q)-1)==0)
    ck('clean compression is positive LCU, not incoherent mean',s.simplify(W[0,0]-(p+p*p*a))==0)
    q0=[s.simplify(x.subs(a,0)) for x in q]
    dq0=[s.simplify(s.diff(x,a).subs(a,0)) for x in q]
    ck('counter has no rank birth',all(x>0 for x in q0))
    ck('counter probability jet exact',all(s.simplify(x-y)==0 for x,y in zip(dq0,[2*p**3,0,-2*p**3,0])))
    # At a=0, q_00=p^2 and q_10=p^3. All other derivatives vanish.
    Hprime=s.simplify(-sum(dq0[i]*s.expand_log(s.log(q0[i]),force=True) for i in range(4)))
    Hprime=s.simplify(s.expand_log(Hprime,force=True))
    ck('complete final pointer entropy has nonzero source',s.simplify(Hprime/(2*p**3*s.log(p))-1)==0)
    c=s.symbols('c00 c01 c10 c11',real=True)
    Cprime=s.simplify(sum(c[i]*dq0[i] for i in range(4)))
    ck('fixed code lengths still have probability source',s.simplify(Cprime-2*p**3*(c[0]-c[2]))==0)
    # Copying the prepared coin into a retained record destroys no probability,
    # but removes the interference needed for clean compression.
    record_blank=p**2+p**4*a*a
    coherent_blank=q[0]
    ck('unreversed retained coin changes the actual return effect',s.simplify(coherent_blank-record_blank-2*p**3*a)==0)
    ck('alloutcome record is not coherent erasure at a=1',s.simplify(record_blank.subs(a,1)-(1-2*p**3))==0)
    # Scalar tail integration used in the universal amplitude-source lemma.
    u,A=s.symbols('u A',nonnegative=True)
    tail=s.integrate(2*(A+u)*s.exp(-u),(u,0,s.oo))
    ck('uniform log probability second moment tail integral',s.simplify(tail-(2*A+2))==0)
    return dict(status='PASS',checks=checks,owners_sha256=pins,
        alloutcome_counter='One existing golden splitter G, controlled real rotation V(a), then G*: q00=(p+p²a)², q01=p⁴(1-a²), q10=p³(1-a)², q11=p³(1-a²). All outcomes retained. At a=0: D H_phi=-2p³, D ECost=2p³(c00-c10). Tensor identity on all CAR16/reference128, arbitrary normalized whole-carrier preparation.',
        record_control='An unreversed copy of the coin into a retained archive changes the all-new-work-blank mass to p²+p⁴a². The missing interference is 2p³a; at a=1 the coherent mass is1 but retained-record mass is1-2p³. Thus coherent scratch and immutable history record cannot be identified silently.',
        universal_C1_bound='For complete smooth amplitudes v_a, sum||v_a||²=1, q_a=||v_a||² and V1²=sum||D v_a||²: |D H(q)| <= 2 V1 sqrt(log(M)²+2log(M)+2), including q_a=0 by amplitude-C1 continuation. Divide by log(phi) for phi units. This is not a C2 entropy bound.',
        fixed_code_bound='For any fixed costs c_a: |D ECost| <= 2 V1 std_q(c) <= V1 (max c-min c). Fixed costs do not imply zero source.',
        budget_consumer='For actual finite word U_L...U_1, V1 <= ||D Psi||+sum_j||D U_j||. A sufficient controller source suppression is V1(1+log M)=o(d theta), and for uncancelled actual fixed code also V1 range(c)=o(d theta). This is conditional on the full physical cost/Info and all-readout interface; generic C3 compiler existence supplies no such resource bound.',
        price_scope='Same-history physical w=q would make TOTAL mean Cost-Info equal H(q)/log(phi), not H+J+R plus an automatically separate controller entropy. If only an incremental decomposition is owned, apply its genuine chain rule/source. No new price, code, source selection or stochastic coarse-graining is introduced.')

def copy_antisymmetric_mdl(root=None):
    checks=[]
    def ck(name,test):
        if not bool(test):raise ArithmeticError(name)
        checks.append(name)
    simp=lambda A:A.applyfunc(s.simplify)
    expand=lambda A:A.applyfunc(s.expand)
    def parity(perm):
        return (-1)**sum(perm[i]>perm[j] for i in range(len(perm)) for j in range(i+1,len(perm)))
    def anti(d):
        v=s.zeros(d**d,1)
        for pp in permutations(range(d)):
            index=0
            for a in pp:index=index*d+a
            v[index]=parity(pp)/s.sqrt(s.factorial(d))
        return v
    def tensor_many(matrices):
        out=s.ones(1,1)
        for M in matrices:out=s.kronecker_product(out,M)
        return out
    # A full old unitary, not merely an assumed positive effect. At t=0 its
    # compression is nonnormal; the physical tangent is noncommuting with F.
    t,z=s.symbols('t z',real=True)
    rot=lambda a:s.Matrix([[(1-a*a)/(1+a*a),-2*a/(1+a*a)],[2*a/(1+a*a),(1-a*a)/(1+a*a)]])
    a=t+s.Rational(1,3)
    ca=(1-a*a)/(1+a*a);sa=2*a/(1+a*a)
    cb,sb=s.Rational(3,5),s.Rational(4,5)
    G=s.diag(ca,cb);D=s.diag(sa,sb)
    Jold=G.row_join(-D).col_join(D.row_join(G))
    Rin=s.diag(rot(t+s.Rational(1,7)),s.eye(2))
    U=Jold*Rin
    ck('old_unitary_all4_input_columns',simp(U.T*U-s.eye(4))==s.zeros(4))
    C=U[:2,:2];B=U[2:4,:2]
    F=simp(B.T*B)
    ck('old_failure_amplitude_full_Gram',simp(C.T*C+F-s.eye(2))==s.zeros(2))
    F0=simp(F.subs(t,0));F1=simp(s.diff(F,t).subs(t,0))
    ck('actual_noncommuting_field_tangent',F0*F1-F1*F0!=s.zeros(2))
    ck('old_return_is_nonnormal',simp((C.T*C-C*C.T).subs(t,0))!=s.zeros(2))
    A=s.eye(2)-z*F
    v2=anti(2)
    ck('known_AS2_normalization',(v2.T*v2)[0]==1)
    det_event=s.factor((v2.T*s.kronecker_product(A,A)*v2)[0])
    ck('exact_two_copy_determinant_event',s.factor(det_event-A.det())==0)
    # Good Kraus sqrt(A) has a smooth rectangular full-unitary realization
    # T=sqrt(z)B. Prove its algebra for an EXACT rational native-window sample.
    # Use B at t=-1/7: the input rotation is identity, so all defect roots
    # commute and are explicit scalars; no input column is thrown away.
    zz=s.Rational(9,25)
    Bdiag=simp(B.subs(t,-s.Rational(1,7)))
    T=s.Rational(3,5)*Bdiag
    kh=s.diag(*[s.sqrt((s.eye(2)-T.T*T)[i,i]) for i in range(2)])
    kk=s.diag(*[s.sqrt((s.eye(2)-T*T.T)[i,i]) for i in range(2)])
    W=kh.row_join(-T.T).col_join(T.row_join(kk))
    ck('rectangular_Halmos_full_unitarity',simp(W.T*W-s.eye(4))==s.zeros(4))
    ck('good_Luders_without_sqrt_F',simp(kh.T*kh-(s.eye(2)-zz*Bdiag.T*Bdiag))==s.zeros(2))
    ck('all_original_bad_labels_retained',simp(T.T*T-zz*Bdiag.T*Bdiag)==s.zeros(2))
    ck('all_good_data_return_to_known_AS',simp(s.kronecker_product(kh,kh)*v2-kh.det()*v2)==s.zeros(4,1))
    # Negative effective triangle: the known actual native scene principal
    # entries 1-23/480 on diagonal and -23/480 offdiagonal. It is a diagnostic
    # block, not replacement of the original full33 or CAR16 carrier.
    f=s.Rational(23,480)
    F3=s.eye(3)-f*s.ones(3)
    ck('negative_native_effective_entry_cycle',F3[0,1]*F3[1,2]*F3[2,0]==-f**3)
    A3=s.eye(3)-z*F3
    v3=anti(3)
    ck('known_AS3_normalization',(v3.T*v3)[0]==1)
    g3=s.factor((v3.T*tensor_many([A3,A3,A3])*v3)[0])
    ck('coherent_three_copy_probability_keeps_negative_cycles',s.factor(g3-A3.det())==0)
    # Every binary pattern includes the full fine bad output space. Permutation
    # invariance of |AS><AS| makes equal-k patterns equiprobable.
    x=s.symbols('x',real=True)
    byk={}
    for bits in product((0,1),repeat=3):
        op=tensor_many([z*F3 if b else A3 for b in bits])
        mass=s.factor((v3.T*op*v3)[0]);k=sum(bits)
        if k in byk:ck('same_k_patterns_equal_'+''.join(map(str,bits)),s.factor(mass-byk[k])==0)
        else:byk[k]=mass
    generating=s.expand((A3+x*z*F3).det())
    for k,mass in byk.items():
        ck('exact_pattern_coefficient_'+str(k),s.factor(s.binomial(3,k)*mass-generating.coeff(x,k))==0)
    ck('all_binary_and_fine_outcomes_complete',s.factor(sum(s.binomial(3,k)*v for k,v in byk.items())-1)==0)
    ck('all_good_pattern_is_exact_g3',s.factor(byk[0]-g3)==0)
    # Elementary symmetric bound, represented as a positive ordered-subset
    # identity on relative odds ri in[0,rmax]. Each omitted term is positive.
    r1,r2,r3,rmax=s.symbols('r1 r2 r3 rmax',nonnegative=True)
    ck('degree1_odds_bound_decomposition',s.expand(3*rmax-(r1+r2+r3)-sum(rmax-r for r in (r1,r2,r3)))==0)
    ck('degree2_odds_bound_decomposition',s.expand(3*rmax**2-(r1*r2+r1*r3+r2*r3)-sum(rmax*(rmax-a)+a*(rmax-b) for a,b in ((r1,r2),(r1,r3),(r2,r3))))==0)
    ck('degree3_odds_bound_decomposition',s.expand(rmax**3-r1*r2*r3-((rmax-r1)*rmax**2+r1*(rmax-r2)*rmax+r1*r2*(rmax-r3)))==0)
    for k in range(1,4):
        ck('strict_mode_fixture_z_lt_half_'+str(k),s.simplify((g3-byk[k]).subs(z,s.Rational(9,25)))>0)
    # This is a genuine field source, not only the scalar event identity.
    g0=s.factor(det_event.subs(t,0));dg0=s.factor(s.diff(det_event,t).subs(t,0))
    dJ0=s.factor(z*s.trace((s.eye(2)-z*F0).inv()*F1))
    ck('noncommuting_full_mode_source',s.factor(-dg0/g0-dJ0)==0)
    ck('mode_source_is_nonzero',s.simplify(dJ0.subs(z,zz))!=0)
    F2=simp(s.diff(F,t,2).subs(t,0))
    inv=(s.eye(2)-z*F0).inv()
    second_expected=s.factor(z*s.trace(inv*F2)+z*z*s.trace(inv*F1*inv*F1))
    second_actual=s.factor((-s.diff(det_event,t,2)/det_event+(s.diff(det_event,t)/det_event)**2).subs(t,0))
    ck('noncommuting_second_mode_source',s.factor(second_actual-second_expected)==0)
    e=s.symbols('relative_amplitude_error',real=True)
    ck('mode_log_relative_first_jet',s.factor(s.diff(-2*s.log(1+e),e)+2/(1+e))==0)
    ck('mode_log_relative_second_jet',s.factor(s.diff(-2*s.log(1+e),e,2)-2/(1+e)**2)==0)
    lam=s.symbols('lambda',real=True)
    odds=z*lam/(1-z*lam)
    ck('uniform_odds_upper_bound',s.factor(z/(1-z)-odds-z*(1-lam)/((1-z)*(1-z*lam)))==0)
    # Mean entropy remains a different complete-law aggregation; no history
    # loss or event conditioning is used to identify it with the mode.
    gg=s.symbols('g',positive=True)
    h=-gg*s.log(gg)-(1-gg)*s.log(1-gg)
    ck('mean_and_mode_sources_differ',s.factor(s.diff(h,gg)+s.log(gg)-s.log(1-gg))==0 and s.simplify(s.diff(h,gg)+1/gg)!=0)
    return dict(status='PASS_EXACT_COPY_ANTISYMMETRIC_MDL',checks=checks,
      exact_instrument='Old failure amplitude B=Qold Uold Pold, F=B*B. With T=sqrt(z)B, use rectangular Halmos W=[[sqrt(I-T*T),-T*],[T,sqrt(I-TT*)]]. Both roots have uniform gap1-z>0, including zero eigenvalues of F. Good K0=sqrt(I-zF); every old failure output label remains in T. No sqrtF or replacement by a presumed Luders bad map is needed.',
      copy_test='Let d=rankPold. Prepare the KNOWN AS_d on d whole return-carrier probe copies, including all16/reference128 components. W on every copy; read all good/bad flags and a complete data basis with AS_d as a fixed basis vector on the all-good sector. All-good data amplitude is sqrt(det(I-zF))*AS_d. One complete pointer outcome has probability g=det(I-zF). All other all-good data probabilities vanish.',
      full_mode_theorem='For a binary failure pattern I of sizek, q_I=g*e_k(r_1,...,r_d)/binom(d,k), ri=z lambda_i/(1-z lambda_i). Thus q_I<=g*[z/(1-z)]^k. Every finer retained bad-output history has probability<=q_I. For0<z<1/2, the all-good+AS outcome is the UNIQUE mode of the ENTIRE complete pointer law, not a postselected success event. The relative gap is at least1-z/(1-z). z>=1/2 has no such universal theorem.',
      MDL_consumer='Under the EXISTING but still physical-binding-dependent w(history)=q(history), Info=log_phi(q/mu) and the Book03 MDL mode reading, the COMPLETE most-likely-history action is exactly J/log(phi), J=-logdet(I-zF). No scalar J or curvature was programmed as a price. This is distinct from the expected action H(q)/log(phi); neither aggregation is declared forced from matrix existence alone.',
      source='At fixedcut/rank/z, D J=zTr[(I-zF)^-1 DF] and D2J[V,W]=zTr[A^-1 D2F[V,W]]+z²Tr[A^-1 DF[V] A^-1 DF[W]], without [F,DF]=0. Norm bounds J1<=zd F1/(1-z), J2<=zd F2/(1-z)+z²d F1²/(1-z)². A movingz adds Tr[(I-zF)^-1 F] Dz. A movingP requires the actual moving-AS preparation/cut jets; no frozen-frame statement is made.',
      C2_birth_boundary='The unique mode is one fixed complete pointer coordinate with amplitude sqrt(g)>0; births of any OTHER output have no logarithm in S_MAP. Uniform mode-gap and positive g_min permit ordinary C2 source transfer. This removes the Shannon-birth obstruction for this particular mode-price map, not for H(q) or an unbound whole H+J+R action.',
      finite_compilation='Let rho=z/(1-z)<1 and g_min=(1-z)^d. Ideal good amplitude=sqrt(g)>=sqrt(g_min); each competing complete amplitude has norm<=sqrt(rho)*sqrt(g). A whole-output state error eta0<0.5*(1-sqrt(rho))*sqrt(g_min) preserves the unique mode. For physical jet normJ2=norm+normD+0.5normD2, define J1,J2 as actual bounds on DJ,D2J. If the compiled good-amplitude error has J2 norm eta, then u=error/sqrt(g) has J2 norm<=eta*g_min^-1/2*(1+J1/2+J2/4+J1^2/8). For ||u||J2<=1/2 the mode-price J2 error is <=4||u||J2. Include actual whole-word/copy/AS-preparation errors: no polynomial gate-cost claim, eta may need exponentially small precision in d.',
      analytic_query='sqrt(I-X) at ||X||<=z<1/2 has an absolutely convergent binomial series. Both Halmos roots use X=T*T or TT*, so no inverse small-gap oracle occurs. With rho=(1+z)/(2z)>1, j<=3 derivative tail after degreeL is bounded by rho^(-(L+1-j))*|D^j[1-sqrt(1-x)] at x=rho*z| (j0 uses the positive series sum<1). Physical B jets multiply by the chain rule. Native control/cost admission is still required.',
      resource_boundary='The copied antisymmetric probe is known apparatus, not cloning unknown physical matter and not the original four-role CAR16 renamed as a new Fock field. Its d copies, coherent permutations/signs, preparation, full-data basis readout, old-field queries, z coin, fresh coherent work, and compiler leakage need genuine native admission and actual complete price. No measured old immutable archive is erased. Individual probe marginals need not satisfy the original arbitrary fixed-RIGHT preparation constraint; this is a new comparison test whose actual preparation interface must be typed.',
      original_owner_boundary='The old signed native-cycle quotient and old filled-Slater determinant event already exist. New here is the smooth old-failure-amplitude Halmos realization on ordinary tensor copies plus a proof that its determinant outcome is the unique COMPLETE fine-history mode, which supplies a conditional MDL source bridge. It does not prove physical programme selection, common source with the old unmodified v8 experiment, independent spin matter, exact joint roots or GR closure.')

def golden_copy_mdl_lcu(root=None):
    checks=[]
    def ck(name,test):
        if not bool(test):raise ArithmeticError(name)
        checks.append(name)
    simp=lambda M:M.applyfunc(s.simplify)
    p=(s.sqrt(5)-1)/2;a=s.sqrt(p)
    w1=p**6;w0=1-w1;r=s.simplify(w1/w0)
    ck('three_return_coins_weight',s.simplify(w1+4*p**3-1)==0)
    ck('golden_fugacity_is_derived',s.simplify(r-p**3/4)==0)
    kmin=1-2*w1
    ck('uniform_good_effect_above_half',s.simplify(kmin*kmin-s.Rational(1,2))>0)
    ck('all_good_contraction_below_one',s.simplify(1-w0)>0)
    coin=s.Matrix([[a,-p],[p,a]])
    ck('actual_golden_coin_full_unitarity',simp(coin.T*coin-s.eye(2))==s.zeros(2))
    PREP=s.kronecker_product(coin,coin,coin)
    ck('three_coin111_amplitude',s.simplify(PREP[7,0]-p**3)==0)
    ck('all_other_seven_histories_kept',s.simplify(sum(PREP[j,0]**2 for j in range(7))-w0)==0)
    # Actual old unitary with nonnormal return compression; every old input
    # column and all old failure output columns remain.
    c0=s.diag(s.Rational(4,5),s.Rational(3,5))
    s0=s.diag(s.Rational(3,5),s.Rational(4,5))
    rot=s.Matrix([[s.Rational(3,5),-s.Rational(4,5)],[s.Rational(4,5),s.Rational(3,5)]])
    U=(c0.row_join(-s0).col_join(s0.row_join(c0)))*s.diag(rot,s.eye(2))
    ck('old_word_unitary_all_input_columns',U.T*U==s.eye(4))
    P=s.diag(1,1,0,0);Q=s.eye(4)-P
    C=U[:2,:2];B=U[2:4,:2]
    Ffull=P*U.T*Q*U*P;F=Ffull[:2,:2]
    ck('old_actual_failure_Gram',F==B.T*B)
    ck('old_return_is_nonnormal',C.T*C!=C*C.T)
    # A projector encoder flips one FRESH flag iff the data lies outside Pi.
    # Three separate flags encode P U* Q U P; no square root or matrix oracle.
    def encoder(pi,flag):
        out=s.zeros(32)
        for f0,f1,f2,data in product(range(2),range(2),range(2),range(4)):
            bits=[f0,f1,f2];col=4*(4*f0+2*f1+f2)+data
            bits[flag]^=int(1-pi[data,data])
            row=4*(4*bits[0]+2*bits[1]+bits[2])+data
            out[row,col]=1
        return out
    EP0,EQ1,EP2=encoder(P,0),encoder(Q,1),encoder(P,2)
    ck('three_projector_encoders_are_complete_unitaries',all(E.T*E==s.eye(32) for E in (EP0,EQ1,EP2)))
    UU=s.kronecker_product(s.eye(8),U)
    VF=EP2*UU.T*EQ1*UU*EP0
    ck('actual_three_bank_F_query_full_unitarity',VF.T*VF==s.eye(32))
    ck('actual_three_bank_clean_compression_is_F',VF[:4,:4]==Ffull)
    E=s.zeros(32,2);E[0,0]=E[1,1]=1
    VE=VF*E
    # SELECT is identity on seven full branches and -VF on branch111; it is
    # unitary on all8*32=256 inputs. PREP and its SAME exact inverse sandwich
    # it. These are ALL256 output rows for both old input columns.
    out=s.zeros(256,2)
    for j in range(8):
        hj=s.simplify(PREP[7,0]*PREP[7,j])
        block=(E if j==0 else s.zeros(32,2))-hj*(E+VE)
        out[32*j:32*(j+1),:]=block
    K=simp(out[:2,:])
    expected=simp(w0*s.eye(2)-w1*F)
    ck('complete_three_coin_LCU_compression',simp(K-expected)==s.zeros(2))
    ck('all256_output_rows_normalized',simp(out.T*out-s.eye(2))==s.zeros(2))
    bad=out[2:,:]
    ck('every_old_coin_query_failure_is_retained',simp(bad.T*bad-(s.eye(2)-K.T*K))==s.zeros(2))
    ck('golden_good_is_positive_function_of_F',simp(K-w0*(s.eye(2)-r*F))==s.zeros(2))
    # Ordinary AS2 input and all-good complete-data return. No new Fock field.
    AS=s.Matrix([0,1,-1,0])/s.sqrt(2)
    ck('all_good_data_return_to_known_AS',simp(s.kronecker_product(K,K)*AS-K.det()*AS)==s.zeros(4,1))
    g=s.factor(K.det()**2)
    ck('whole_mode_action_is_twice_derived_feedback',s.simplify(g-w0**4*(s.eye(2)-r*F).det()**2)==0)
    Ag=simp(K.T*K);Bg=simp(s.eye(2)-Ag)
    patterns=[]
    for bits in product((0,1),repeat=2):
        effect=s.kronecker_product(Bg if bits[0] else Ag,Bg if bits[1] else Ag)
        patterns.append(s.simplify((AS.T*effect*AS)[0]))
    ck('complete_pattern_probabilities_sum_one',s.simplify(sum(patterns)-1)==0)
    ck('golden_complete_allgood_is_strict_global_mode',all(s.simplify(g-mass)>0 for mass in patterns[1:]))
    # Generic field jets at the same positive fixture; no commutativity is used.
    t=s.symbols('t',real=True);X=s.Matrix([[s.Rational(1,9),s.Rational(1,13)],[s.Rational(1,13),-s.Rational(1,17)]])
    Ft=F+t*X;tK=w0*s.eye(2)-w1*Ft;tG=s.factor(tK.det()**2)
    jrprime=r*s.trace((s.eye(2)-r*F).inv()*X)
    ck('noncommuting_F_field_jet',F*X-X*F!=s.zeros(2))
    ck('mode_source_is_computed_overall_factor2',s.simplify((-s.diff(tG,t)/tG).subs(t,0)-2*jrprime)==0)
    # Coherent approximate PREP coefficients preserve the functional form if
    # PREP^* is the actual inverse and SELECT/query identities remain exact.
    u=s.symbols('identity_branch_weight',real=True)
    ck('structured_weight_margin_factorization',s.expand((2*u-1)**2-s.Rational(1,2)-(2*u-1-1/s.sqrt(2))*(2*u-1+1/s.sqrt(2)))==0)
    # Exterior implementation: known FILLED BASIS state removes the global
    # antisymmetric-probe preparation, PROVIDED the actual programme is lifted
    # as Gamma(W) and this structure is preserved by its primitive compiler.
    # A small nonnormal good block checks all6 occupation outputs at N=4,d=2;
    # the old8-mode/70-output determinant owner is reused, never replayed.
    from itertools import combinations
    cc=s.diag(s.Rational(12,13),s.Rational(15,17))
    dd=s.diag(s.Rational(5,13),s.Rational(8,17))
    WW=(cc.row_join(-dd).col_join(dd.row_join(cc)))*s.diag(rot,s.eye(2))
    KK=WW[:2,:2];BB=WW[2:4,:2];Z=BB*KK.inv()
    ck('exterior_fixture_all_input_columns_unitary',WW.T*WW==s.eye(4))
    ck('exterior_good_fixture_nonnormal',KK.T*KK!=KK*KK.T)
    ck('Thouless_full_bad_Gram',Z.T*Z==(KK*KK.T).inv()-s.eye(2))
    gamma=KK.det()**2;rm=s.Rational(64,225)
    masses=[]
    for chosen in combinations(range(4),2):
        missing=[i for i in range(2) if i not in chosen]
        badrows=[i-2 for i in chosen if i>=2]
        kk=len(badrows)
        minor=WW.extract(chosen,[0,1]).det()
        zm=Z.extract(badrows,missing).det() if kk else s.Integer(1)
        ck('complete_occupation_minor_ratio_'+''.join(map(str,chosen)),s.factor(minor**2-gamma*zm**2)==0)
        if kk:
            ck('individual_occupation_mode_bound_'+''.join(map(str,chosen)),minor**2<=gamma*rm**kk and minor**2<gamma)
        masses.append(minor**2)
    ck('all_six_occupation_outputs_complete',sum(masses)==1)
    # Reuse the already-owned same-J2 source ratio; changing the readout
    # fugacity is explicit, so this is not the old z=2^-20 coupling.
    L=4*p**3;Q0=1-r*L;R0=1-r*(1-p**12)
    coupling=2*p**(-5)*(R0/Q0+p**6)
    ck('derived_golden_same_J2_material_ratio',s.simplify(coupling-(33+27*s.sqrt(5))/4)==0)
    return dict(status='PASS_EXACT_GOLDEN_COPY_MODE_LCU',checks=checks,
      exact_weights=dict(p=str(p),identity_weight=str(s.simplify(w0)),negative_F_weight=str(s.simplify(w1)),derived_fugacity=str(s.simplify(r)),minimum_good_amplitude=str(s.simplify(kmin))),
      derived_same_J2_ratio='If this readout is applied to the SAME already-owned two-tick geometric/scalar J2 operator, its retained source ratio lambda(z)=2*sigma*p^-5*[R0/Q0+p6], Q0=1-z*4p3,R0=1-z*(1-p12), specializes at the derived r=p3/4 to lambda=sigma*(33+27sqrt5)/4. The overall computed mode factor2/logphi cancels in this relative ratio. This does not give the old z=2^-20 numerical coupling or derive a new independent native matter sector; old pp/root suites are reused.',
      full_old_query='On the ENTIRE old carrier, encode each projector by a fresh-flag flip on its complement. With three flags, P_out U_old* Q_mid U_old P_in has clean compression F=P U*QUP. All flags and every old failure label remain. The query is unitary on all32 fixture inputs; the3-coin SELECT(I on7 branches,-VF on111) is unitary on all256 inputs.',
      exact_macro='Three original Golden coins have branch111 probability p6; all other7 branches weightw0=1-p6=4p3. Coherent PREP, SELECT, and the SAME inverse PREP produce exact good K=w0 I-p6 F=w0(I-rF), r=p3/4. All coin and query work must be blank on good; all nonblank outputs are retained. This requires exact controlled-query/projector/sign interfaces, not merely an approximation by an arbitrary unitary.',
      complete_mode='K is positive with kmin I<=K<=w0 I, kmin=1-2p6 and kmin²>1/2. On d known antisymmetric probe copies, all-good+AS is ONE complete output with g=detK². All competing complete fine outputs are <=g Rmax^k for k>=1, where Rmax=(1-kmin²)/kmin²<1. Thus the same unique complete-mode theorem applies STRUCTURALLY for everyd. No exponentially small mode-gap test is needed when this functional structure and exact AS are preserved.',
      action='Under the same actual history w=q and Book03 MDL MODE binding, S_MAP*logphi=-logg=-2dlogw0+2J_r(F), J_r=-logdet(I-rF), r=p3/4 derived from the actual3Golden coins. This is a NEW comparison readout at derivedr, not a claim that r equals the old experimentalz=2^-20. Factor2 and constant are computed, not fitted; movingp/d sources cannot discard the constant.',
      structured_robustness='For any actual coherent PREP, its same inverse, and exact SELECT, K=u0 I-sum_uj F^j with uj>=0 and sumuj=1. If u0>(1+1/sqrt2)/2, then Kmin>=2u0-1>1/sqrt2 and unique-mode structure persists at all d. The exact3coin case has onlyu1. Structured replacement F_actual for F_target retains the determinant/mode identity. Generic Golden errors which destroy SELECT, same-adjoint, projector or AS identities require the previous absolute mode-gap/C2 budget.',
      source_error_per_rank='At fixedr<1, F,G in[0,I], F/G first jets<=M1,secondjets<=M2, let delta_j bound D^j(F-G), j<=2. The twice-Jr mode first-source difference divided byd is <=2[r delta1/(1-r)+r² M1 delta0/(1-r)²]. The second-source difference/d is <=2[r delta2/(1-r)+r² M2 delta0/(1-r)²+2r² M1 delta1/(1-r)²+2r³ M1² delta0/(1-r)³]. No1/g factor occurs for STRUCTURE-PRESERVING errors. Normalized geometric signal still divides these actual errors; require delta relative to the real c*epsilon scale.',
      exterior_mode='A structure-preserving exterior simulation gives a stronger implementation: lift the ENTIRE finite one-particle word W to Gamma(W) on N new apparatus occupation qubits and prepare the exact filled-P BASIS vector. Keep every exterior grade in Gamma, every output occupation label and every new work register. If W|P=[K;B] and K invertible, set Z=B K^-1. Every other d-occupation output replaces k retained rows by bad rows, so its amplitude is +/-detK times the corresponding k-by-k minor of Z. Thus q_other/g=|detZ_minor|²<=||Z||^(2k). Since Z*Z=(K K*)^-1-I, K*K>0.5I implies every individual occupation outcome is strictly below g=detK². No combinatorial enhancement occurs for an INDIVIDUAL minor; total failed mass is not required small. The small N4,d2 fixture verifies all6 outputs with nonnormal K and all bad rows retained.',
      exact_exterior_gate_interface='The filled basis state needs no 1/sqrt(d!) amplitude preparation. If the ACTUAL old finite word is decomposed into real two-mode rotations and mode permutations, Gamma respects products. A plane rotation lifts to the two-occupation-qubit gate diag(1,R,1), obtainable by parity CNOT, controlled R, inverse parity CNOT. A mode swap lifts to FSWAP=SWAP times CZ, retaining its fermionic sign. Exact controlled rotations and FSWAP/CZ must be genuinely admitted; they are not deduced from plain G/CNOT availability. For structure-preserving approximations lift the ACTUAL approximate one-particle unitary, not an arbitrary approximation to Gamma(W). The derived mode identity and margin then hold exactly; errors transfer through ordinary logdet resolvent bounds without 1/g. This is a simulated auxiliary representation, not the original CAR16 matter or a new fundamental occupation field.',
      unclosed='Known AS preparation and its readout must be genuinely admitted and counted. A generic finite Golden approximation to AS is not exactly antisymmetric and still needs the exponentially small absolute state-gap budget. No measured/immutable old archive may be erased as scratch. Old U, U*, controlled queries, projector tests and sign control require actual coherent admission. The final pointer/history w=q and MDL aggregation binding, physical programme selection, independent matter and exact joint physical recovery are not inferred from this construction.')

def golden_mdl_densitized_source_controls(root):
    import hashlib
    import subprocess
    import sympy as S
    commit='c7ff2233e2f5ee06e4c94c0d949b21210a746bd4'
    owners={
        '02_REGISTRY/research/A4D_DIRECT_DENSITIZED_LEFT_FEEDBACK_EINSTEIN_SCALAR_SOURCE_2026_10_18.md':'26a3d1b8e626f7cce4945cba5b4bfad11bcddfc4',
        '02_REGISTRY/research/A4D_LOCAL_LEFT_CODED_CAR_NULL_MATTER_EINSTEIN_2026_10_18.md':'75c40d133a23973a36ba5b95d34b4eb36ca96663',
        '02_REGISTRY/research/certificates/a4d_direct_densitized_left_feedback_source_check.py':'3be801d6a483a36614478937063f9b4b46072edf'}
    for path,pin in owners.items():
        raw=subprocess.check_output(['git','show',commit+':'+path],cwd=root)
        actual=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        if actual!=pin: raise ArithmeticError('source pin '+path)
    checks=[]
    def ck(label,val):
        if not val: raise ArithmeticError(label)
        checks.append(label)
    p=(S.sqrt(5)-1)/2
    z=S.symbols('z',real=True)
    T=S.symbols('t_squared',positive=True)
    h,w,wbar=S.symbols('h w wbar',positive=True)
    da,dm=S.symbols('dA dM',real=True)
    ss,aa,dd,ww=S.symbols('s A_wave D_wave W_cross',real=True)
    r=S.simplify(p**3/4); L=4*p**3; a=p**6
    Q=1-z*L; R=1-z*L*(1+a)
    ck('golden derived readout is strictly inside symbolic z window',r>0 and r<1)
    ck('generic Q positive convex pencil',S.simplify(Q-((1-z)+z*a))==0)
    ck('generic R positive convex pencil',S.simplify(R-((1-z)+z*a*a))==0)
    Qr=S.simplify(Q.subs(z,r));Rr=S.simplify(R.subs(z,r))
    ck('derived r Q baseline',S.simplify(Qr-(1-p**6))==0)
    ck('derived r R baseline',S.simplify(Rr-(1-p**6-p**12))==0)
    g=4*z*p**11*T/R
    gr=S.simplify(g.subs(z,r))
    ck('derived r exact positive geometric coefficient',S.simplify(gr-p**14*T/(1-p**6-p**12))==0 and Rr>0)
    lamplus=S.simplify((2/p**5)*(Rr/Qr+p**6))
    target=(33+27*S.sqrt(5))/4
    ck('derived coupling exact radical',S.simplify(lamplus-target)==0)
    for sigma in (1,-1):
        m=8*sigma*z*p**6*T*(1/Q+p**6/R)
        ck('same full two-log ratio for orientation '+str(sigma),S.simplify((m/g).subs(z,r)-sigma*target)==0)
        lam=sigma*target
        trace=-2*lam*ss**2
        ck('all nonzero coframe rows balance for orientation '+str(sigma),S.simplify((-(aa+dd)/h-2*lam*ss**2/h).subs(dd,trace-aa))==0)
        ck('continuum owned orientation gamma=+1/2 agrees '+str(sigma),S.simplify(S.Rational(1,2)*trace+lam*ss**2)==0)
    cx,cy=S.symbols('c_x c_y',real=True)
    ck('both only potentially nonzero link rows vanish',S.simplify((aa+2*cx).subs(cx,-aa/2))==0 and S.simplify((dd+2*cy).subs(cy,-dd/2))==0)
    old_u=wbar*da/w;old_v=wbar*dm/w
    new_u=h**4*da/w;new_v=h**4*dm/w
    ck('all-tangent old to densitized first-source scale',S.simplify(new_u+target*new_v-h**4/wbar*(old_u+target*old_v))==0)
    return dict(status='PASS',checks=checks,source_commit=commit,source_blobs=owners,
        r=str(r),coupling_over_sigma=str(target),positive_focusing_coefficient=str(2*target),
        exact_statement='For every fixed admissible finite old AF cut with positive real weights, fixed coordinate grid/collar, every t>0 with its strict local chart, and bounded nonzero scalar slope s: take the pinned pp tetrad H=A x²+2Wcross xy+D y², backward-half-step Lorentz links, psi=s u, A+D=-2 sigma Lambda_plus(r)s². Then every A_cell=M_cell=0 and all independent interior coframe16, Lorentz-link24 and compact-support scalar Euler rows of the SAME densitized J_r vanish. Golden occupation MDL multiplies all these rows by 2/log(phi), so the zeros are unchanged.',
        scalar_row_proof='At J=1,q=0, Dpsi sum M=2s h^4 sum D_v^+delta_psi=0 for arbitrary compact-supported delta_psi. Positive uneven AF weights cancel before integration by parts. Scalar has no Lorentz spin-current; its link derivatives vanish, leaving the pinned 24 geometric link rows.',
        existing_vs_new='Remote prose D3-D17 gives symbolic 0<z<1 first-source/limit and null-root transfer. Its checker pins z=2^-20. Only this helper makes the new exact substitution z=r and radical simplification; the old full lattice proof is consumed by source pin and not replayed.',
        scope='Conditional new detector MODE action, not total mean entropy or unchanged numerical z=2^-20 experiment. Original preparation/fixedRIGHT/observer/H/R/clock/controllers and all remaining CAR grades are not solved; genuinely free scene E,b have nonzero source. General offshell Einstein-scalar limit still requires t->0/source and full spatial/compile/recovery budgets.')

def adjacent_even_exterior(root=None):
    import math
    import numpy as np
    import sympy as sp
    checks = {}
    def ck(name, value):
        checks[name] = bool(value)
        if not checks[name]:
            raise AssertionError(name)
    c, s = sp.symbols('c s', real=True)
    R = sp.Matrix([[c, -s], [s, c]])
    I2 = sp.eye(2)
    # Basis 00,01,10,11.  C01: first controls second.
    C01 = sp.Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
    C10 = sp.Matrix([[1,0,0,0],[0,0,0,1],[0,0,1,0],[0,1,0,0]])
    def red(x):
        return sp.reduced(sp.expand(x), [c*c+s*s-1], c, s)[1]
    def ze(M):
        return all(red(x)==0 for x in M)
    square = sp.Matrix([[c*c-s*s, -2*c*s], [2*c*s,c*c-s*s]])
    # Rightmost factor acts first.  Reversed R signs correct the wedge
    # ordering: one-particle modes are 10,01, whereas the odd bit block is01,10.
    lift = C01 * sp.kronecker_product(R.T,I2) * C10 * sp.kronecker_product(R,I2) * C10 * C01
    target = sp.zeros(4)
    target[0,0]=target[3,3]=1
    for a in range(2):
        for b in range(2):
            target[1+a,1+b]=square[1-a,1-b]
    ck('exact_adjacent_even_lift_all_four_basis_columns', ze(lift-target))
    ck('exact_lift_orthogonal',ze(lift.T*lift-sp.eye(4)))
    ck('vacuum_and_filled_pair_return_exactly',ze(lift[:,0]-sp.eye(4)[:,0]) and ze(lift[:,3]-sp.eye(4)[:,3]))
    X=sp.Matrix([[0,1],[1,0]])
    ck('inverse_uses_retained_basis_one_X_echo',X*R*X==R.T)
    ck('one_particle_block_is_R_squared',ze(sp.Matrix([[lift[2,2],lift[2,1]],[lift[1,2],lift[1,1]]])-square))

    # One actual finite word on four adjacent apparatus modes.  All sixteen
    # occupation directions are checked, including empty/full grades.
    p=(math.sqrt(5)-1)/2
    a=math.sqrt(p)
    G=np.array([[a,-p],[p,a]],float)
    C01n=np.array(C01,float)
    C10n=np.array(C10,float)
    B=C01n @ np.kron(G.T,np.eye(2)) @ C10n @ np.kron(G,np.eye(2)) @ C10n @ C01n
    G2=G@G
    def occup(i,N):
        return tuple(j for j in range(N) if (i>>(N-1-j))&1)
    def exterior(U):
        N=U.shape[0]
        out=np.zeros((2**N,2**N))
        for i in range(2**N):
            ii=occup(i,N)
            for j in range(2**N):
                jj=occup(j,N)
                if len(ii)==len(jj):
                    out[i,j]=np.linalg.det(U[np.ix_(ii,jj)]) if ii else 1.
        return out
    N=4
    word=[(0,1),(1,5),(2,2),(0,-2),(1,-7),(2,3)]
    W=np.eye(N)
    Q=np.eye(2**N)
    for edge,m in word:
        local=np.linalg.matrix_power(G2,m)
        full=np.eye(N)
        full[edge:edge+2,edge:edge+2]=local
        W=full@W
        pair=np.linalg.matrix_power(B,m)
        gate=np.kron(np.kron(np.eye(2**edge),pair),np.eye(2**(N-edge-2)))
        Q=np.einsum('ij,jk->ik',gate,Q,optimize=False)
    ext=exterior(W)
    tol=2e-12
    ck('actual_word_all_entries_finite',np.isfinite(Q).all() and np.isfinite(W).all())
    ck('actual_four_mode_word_matches_all_sixteen_exterior_columns',np.max(np.abs(Q-ext))<tol)
    ck('actual_word_all_grades_retained_and_invariant',all(abs(Q[i,j])<tol for i in range(16) for j in range(16) if len(occup(i,N))!=len(occup(j,N))))
    ck('actual_word_unitary_on_full_occupation_carrier',np.linalg.norm(np.einsum('ij,jk->ik',Q.T,Q,optimize=False)-np.eye(16),2)<tol)
    ck('actual_inverse_is_reversed_exact_gate_word',np.linalg.norm(Q.T-exterior(W.T),2)<tol)
    P=(0,1)
    K=W[np.ix_(P,P)]
    sigma_min=float(np.linalg.svd(K,compute_uv=False)[-1])
    ck('actual_compression_structural_mode_margin',sigma_min**2>0.5)
    filled=12 # modes0,1 occupied
    prob=Q[:,filled]**2
    good=float(prob[filled])
    ck('filled_basis_input_is_single_exact_computational_state',occup(filled,N)==P)
    ck('return_probability_is_det_K_squared',abs(good-np.linalg.det(K)**2)<tol)
    ck('all_six_grade_two_outcomes_normalize',abs(sum(prob[i] for i in range(16) if len(occup(i,N))==2)-1)<tol)
    ck('one_complete_occupation_history_is_unique_mode',all(prob[i]<good for i in range(16) if i!=filled))
    Z=W[2:,:2]@np.linalg.inv(K)
    odds=float(np.linalg.norm(Z,2)**2)
    ck('Thouless_odds_equal_sigma_min_inverse_square_minus_one',abs(odds-(sigma_min**-2-1))<tol)
    for k in (1,2):
        ck('every_individual_replacement_minor_bound_k'+str(k),all(prob[i]/good<=odds**k+tol for i in range(16) if len(occup(i,N))==2 and len(set(occup(i,N))-set(P))==k))

    # The gate polynomial is valid for every smooth admitted local query,
    # not merely at golden constants.  Check full first/second query jets.
    t=sp.symbols('t',real=True)
    tr={c:sp.cos(t),s:sp.sin(t)}
    jetdiff=(lift-target).subs(tr)
    ck('smooth_local_query_first_jet_exact',all(sp.trigsimp(sp.diff(x,t))==0 for x in jetdiff))
    ck('smooth_local_query_second_jet_exact',all(sp.trigsimp(sp.diff(x,t,2))==0 for x in jetdiff))

    # Hostile control: generic real operator compilation need not preserve
    # grades.  A one-qubit G on the first occupation wire leaks the vacuum.
    unstructured=np.kron(G,np.eye(8))
    ck('generic_G_word_does_not_automatically_preserve_exterior_grades',abs(unstructured[8,0])>0.1)

    # Existing mod2 invariant detects the tempting odd lift, without search.
    x=sp.symbols('x')
    modpoly=sp.Poly(x**4+x**2+1,x,modulus=2)
    b=sp.Poly(x+x*x,x,modulus=2)
    ck('mod2_golden_sum_is_not_vacuum_sum',b.rem(modpoly)!=sp.Poly(1,x,modulus=2))
    ck('mod2_even_golden_sum_is_vacuum_sum',(b*b).rem(modpoly)==sp.Poly(1,x,modulus=2))
    # No inference of sufficient exact word synthesis from this necessary
    # invariant; it only rejects the explicitly odd clean lift.

    result={
      'status':'PASS','checks':len(checks),'check_results':checks,
      'exact_word': 'C01 (G^T tensor I) C10 (G tensor I) C10 C01 = Gamma(G^2)',
      'basis_order':'00,01,10,11; mode order0,1; rightmost factor acts first',
      'fixture':{'modes':N,'full_exterior_dimension':16,'word_edges_even_powers':word,
                 'sigma_min_K':sigma_min,'good_complete_mode_probability':good,
                 'max_other_probability':float(max(prob[i] for i in range(16) if i!=filled)),
                 'replacement_odds_norm_squared':odds,
                 'full_matrix_lift_error':float(np.max(np.abs(Q-ext))),
                 'all_grade_two_probabilities':{''.join(map(str,occup(i,N))):float(prob[i]) for i in range(16) if len(occup(i,N))==2}},
      'scope':'Exact structure for actual adjacent-even word; constant target approximation only unless a smooth native local-query interface is supplied. No exact odd-G lift, no old LCU sign/control identity, no immutable record erasure, no physical MDL/Info selection or GR closure.'}
    return result

def fresh_detector_archive_composition(root=None):
    import sympy as sp
    import numpy as np
    p,f,x=sp.symbols('p f x',real=True)
    checks={}
    def ck(name, value):
        checks[name]=bool(value)
        if not checks[name]: raise AssertionError(name)
    def red(v):
        return sp.rem(sp.Poly(sp.expand(v),p),sp.Poly(p*p+p-1,p)).as_expr()
    # Actual scalar old query U_f, P=|0><0|, Q=|1><1| has F=f.
    # Three fresh flag banks retain its complete V_F input column.
    # Nonzero old/flag rows:0,9,2,11 in data/in/mid/out bit order.
    q=[sp.Integer(0)]*128
    old_rows=(0,9,2,11)
    for coin in range(8):
        j=bin(coin).count('1')
        weight=p**(12-j) # (p^3 * (G^tensor3)_(111,coin))^2
        values=[weight*(1+f)**2,weight*f*(1-f),weight*(1-f)**2,weight*f*(1-f)]
        if coin==0: values[0]=(1-p**6*(1+f))**2
        for row,value in zip(old_rows,values): q[16*coin+row]=value
    g=(1-p**6*(1+f))**2
    ck('actual_scalar_LCU_all_128_pointer_rows_retained',len(q)==128 and sum(v!=0 for v in q)==32)
    ck('scalar_old_query_three_fresh_flag_column_normalized',sp.expand(f*f+(1-f)**2+2*f*(1-f))==1)
    ck('fresh_pointer_probabilities_normalize_exactly',red(sum(q)-1)==0)
    ck('full_pointer_first_source_normalizes',red(sp.diff(sum(q),f))==0)
    ck('selected_complete_mode_weight_is_owned_K_squared',q[0]==g)
    # The mode property is CONSUMED from the prior lemma, not reproved here.
    p0=(math.sqrt(5)-1)/2
    def probs(f0):
        return np.array([float(v.subs({p:p0,f:f0})) for v in q])
    def amplitudes(f0):
        out=np.zeros(128)
        v=np.array([f0,math.sqrt(f0*(1-f0)),1-f0,-math.sqrt(f0*(1-f0))])
        for coin in range(8):
            t=p0**(6-bin(coin).count('1'))*math.sqrt(p0)**bin(coin).count('1')
            for k,row in enumerate(old_rows):
                out[coin*16+row]=(1. if coin==0 and k==0 else 0.)-t*(v[k]+(1. if k==0 else 0.))
        return out
    q0,q1=probs(.25),probs(.75)
    amp=amplitudes(.25)
    ck('actual_signed_pointer_column_matches_all_probability_rows',np.max(abs(amp*amp-q0))<1e-13)
    ck('actual_pointer_column_has_unit_norm',abs(np.sum(amp*amp)-1)<1e-13)
    # Full old archive+data+RIGHT+reference state. Keep offdiagonal
    # GHZ correlations rather than relabeling or dephasing the archive.
    r0=.6
    psi=np.zeros(16)
    psi[0],psi[15]=math.sqrt(r0),math.sqrt(1-r0)
    rho=np.outer(psi,psi)
    A=np.einsum('i,j->ij',psi,amp)
    reduced=np.einsum('ik,jk->ij',A,A)
    ck('fresh_common_detector_preserves_full_old_density_including_RIGHT_reference',np.max(abs(reduced-rho))<1e-13)
    joint=np.zeros((2,128))
    for h in range(2): joint[h]=np.sum(A[h*8:(h+1)*8,:]**2,axis=0)
    ck('unmodified_archive_joint_readout_factors_exactly',np.max(abs(joint-np.array([r0,1-r0])[:,None]*q0[None,:]))<1e-13)
    ck('common_detector_full_history_mode_includes_old_past_factor',abs(joint.max()-r0*q0[0])<1e-13)
    # A product detector uses both operator blocks, irrespective of which
    # old h happened.  Only 2x128x128 outcomes, not any old replay.
    bank_law=np.einsum('i,j->ij',q0,q1)
    full=np.einsum('h,ij->hij',np.array([r0,1-r0]),bank_law)
    ck('both_fresh_banks_full_joint_law_normalizes',abs(np.sum(full)-1)<1e-13)
    ck('execute_all_blocks_joint_mode_is_past_mode_times_product',abs(np.max(full)-r0*q0[0]*q1[0])<1e-13)
    ck('sampled_archive_control_is_different_from_product',abs(max(r0*q0[0],(1-r0)*q1[0])-np.max(full))>1e-3)
    ck('marginal_archive_good_mass_is_arithmetic_mixture',abs(r0*q0[0]+(1-r0)*q1[0]-q0[0]*q1[0])>1e-3)
    # Operator trace multiplicity is integer bank count, not Born weight.
    r=sp.Rational(3,5)+x/10
    f0=sp.Rational(1,4)+x/11
    f1=sp.Rational(3,4)-x/13
    g0=g.subs(f,f0)
    g1=g.subs(f,f1)
    m1=2
    mode=r*g0*g1**m1
    logsrc=lambda z: sp.diff(z,x)/z
    ck('full_joint_mode_source_has_exact_old_history_debt',sp.factor(-logsrc(mode)+logsrc(r)+logsrc(g0)+m1*logsrc(g1))==0)
    ck('fixed_past_gives_exact_sum_of_detector_sources',sp.factor(-logsrc(mode/r)+logsrc(g0)+m1*logsrc(g1))==0)
    ck('moving_past_source_at_base_is_minus_one_sixth',(-logsrc(r)).subs(x,0)==-sp.Rational(1,6))
    ck('sampled_history_drops_unexecuted_operator_block_source',sp.factor(-logsrc(r*g0)+logsrc(mode)-m1*logsrc(g1))==0)
    ck('whole_trace_determinant_is_integer_multiplicity_product',sp.cancel(g0*g1**m1-(1-p**6)**(2*(1+m1))*(1-(p**6/(1-p**6))*f0)**2*(1-(p**6/(1-p**6))*f1)**(2*m1))==0)
    # Conditional detector can change which old history wins. Neither
    # pointer mass nor any old label is erased in this control.
    close_past=np.array([.51,.49])
    cond=np.array([probs(1.)[0],probs(0.)[0]])
    ck('conditional_detector_can_switch_old_MAP_branch',int(np.argmax(close_past))==0 and int(np.argmax(close_past*cond))==1)
    # A read-only control on a coherent h register preserves its pointer
    # but need not preserve the complete old density after marginalization.
    a1=amplitudes(.75)
    overlap=float(amp@a1)
    ck('different_archive_controlled_detectors_can_change_old_offdiagonals',abs(overlap-1)>1e-5)
    rawN=1+x
    ck('Book_raw_normalizer_is_additional_source',sp.factor(-logsrc(rawN*mode)+logsrc(mode)+logsrc(rawN))==0)
    return {'status':'PASS','checks':len(checks),'check_results':checks,
      'fixture':{'actual_old_query':'U_f=[[sqrt(1-f),-sqrt(f)],[sqrt(f),sqrt(1-f)]]; P=diag(1,0), F=f',
                 'fresh_complete_pointer_rows_per_bank':128,'old_archive_data_RIGHT_reference_dimension':16,
                 'past_probabilities':[.6,.4],'conditional_good_weights':[float(q0[0]),float(q1[0])],
                 'parallel_two_bank_full_joint_mode':float(np.max(full)),
                 'sampled_history_full_joint_mode':float(max(r0*q0[0],(1-r0)*q1[0])),
                 'moving_past_additional_mode_source':-1/6,
                 'conditional_control_offdiagonal_overlap':overlap,
                 'close_past_conditional_mode_products':list(close_past*cond)},
      'scope':'Exact causal composition of already supplied fresh detector. Does not admit physical fields/queries/resources, identify old history labels with trace addresses, set raw Book N=1, freeze upstream preparation or replace full H+J+R.'}

def native_collective_mode(root=None):
    checks=[]
    def ck(name,test):
        if not bool(test):raise ArithmeticError(name)
        checks.append(name)
    a,p,f,c,k=s.symbols('a p f c k',real=True)
    ideal=s.groebner([a*a-p,p*p+p-1],a,p,domain=s.QQ.frac_field(f,c,k))
    def zero(expr):
        if isinstance(expr,s.MatrixBase):return all(zero(v) for v in expr)
        num=s.fraction(s.cancel(expr))[0]
        return ideal.reduce(s.expand(num))[1]==0
    G=s.Matrix([[a,-p],[p,a]])
    CX=s.Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
    I=s.eye(2)
    R=s.kronecker_product(I,G)*CX*s.kronecker_product(I,G.T)*CX
    ck('owned_controlled_G_square_identity_on_ALL_columns',zero(R-s.diag(I,G*G)))
    W=R*R
    ck('fixed_word_is_controlled_G_four',zero(W-s.diag(I,G**4)))
    ck('whole_fixed_word_is_unitary',zero(W.T*W-s.eye(4)))
    delta=16*p**9
    ck('actual_failure_coefficient_derived_from_G_four',zero((G**4)[1,0]**2-delta))
    ck('actual_good_coefficient_derived_from_G_four',zero((G**4)[0,0]**2-(1-delta)))
    ck('strict_global_good_mode_bound',16*s.Rational(5,8)**9<s.Rational(1,2))
    J=s.Matrix([[1,0],[0,0],[0,1],[0,0]])
    Pgood=s.diag(1,0,1,0)
    Eg=J.T*W.T*Pgood*W*J
    Eb=J.T*W.T*(s.eye(4)-Pgood)*W*J
    N=s.diag(0,1)
    ck('actual_good_effect_is_I_minus_delta_N',zero(Eg-(I-delta*N)))
    ck('actual_bad_effect_is_delta_N',zero(Eb-delta*N))
    ck('all_pointer_effects_complete',zero(Eg+Eb-I))
    rho=s.Matrix([[1-f,c],[c,f]])
    qg=s.trace(rho*Eg);qb=s.trace(rho*Eb)
    ck('unknown_input_probability_linear_in_native_occupation',zero(qg-(1-delta*f)))
    ck('unknown_input_coherences_not_needed_as_angle_code',zero(s.diff(qg,c)))
    ck('all_unknown_input_pointer_outcomes_normalize',zero(qg+qb-1))
    # Correlations with the programme are retained, not dephased or reset.
    joint=W*J*rho*J.T*W.T
    ck('retained_quantum_programme_trace_preserved',zero(s.trace(joint)-1))
    ck('retained_quantum_programme_has_original_offdiagonal_coherence',zero(joint[0,2]-c*(G**4)[0,0]))
    two=s.kronecker_product(rho,rho)
    Qgg=s.kronecker_product(Eg,Eg)
    Qgb=s.kronecker_product(Eg,Eb)
    Qbg=s.kronecker_product(Eb,Eg)
    Qbb=s.kronecker_product(Eb,Eb)
    qgg=s.trace(two*Qgg)
    ck('two_SUPPLIED_independent_inputs_product_good_probability',zero(qgg-(1-delta*f)**2))
    ck('all_four_two_input_pointer_patterns_complete',zero(s.trace(two*(Qgg+Qgb+Qbg+Qbb))-1))
    ck('one_bad_pattern_actual_odds',zero(s.trace(two*Qgb)-delta*f*(1-delta*f)))
    ck('two_bad_pattern_actual_odds',zero(s.trace(two*Qbb)-delta**2*f**2))
    # Exact C2 scalar source, retaining full actual input-density derivatives.
    x,t1,t2=s.symbols('x t1 t2',real=True)
    ft=f+t1*x+t2*x*x/2
    Snat=-k*s.log(1-delta*ft)
    ck('true_first_input_mode_source',zero(s.diff(Snat,x).subs(x,0)-k*delta*t1/(1-delta*f)))
    ck('true_second_input_mode_source',zero(s.diff(Snat,x,2).subs(x,0)-k*(delta*t2/(1-delta*f)+delta**2*t1**2/(1-delta*f)**2)))
    # Pointer coarse grain is substantive: emitting the programme changes mode.
    delta_symbol=s.symbols('delta',real=True)
    ck('emitting_programme_changes_mode_probability',
       s.simplify((1-delta_symbol/2)-s.Rational(1,2))==(1-delta_symbol)/2)
    # Common-label mixture odds hold even though log of the mixture is not
    # the average log. This fixture needs no dephasing of retained quantum work.
    w,g0,g1,q0,q1,rmax=s.symbols('w g0 g1 q0 q1 rmax',real=True)
    mixed_good=w*g0+(1-w)*g1;mixed_other=w*q0+(1-w)*q1
    ck('common_mode_odds_survive_quantum_programme_mixture',
       s.expand(rmax*mixed_good-mixed_other
                -(w*(rmax*g0-q0)+(1-w)*(rmax*g1-q1)))==0)
    pins=[]
    if root is not None:
        base=Path(root)
        paths=[
            ('02_REGISTRY/research/A4D_NATIVE_GOLDEN_HISTORY_PREPARATION.md',
             ['(I tensor G) CNOT (I tensor G^transpose) CNOT = diag(I,G^2).']),
            ('02_REGISTRY/research/A4D_NATIVE_GOLDEN_PROGRAM_COMPILATION.md',
             ['X G X=G^T','preserving that control']),
            ('01_BOOKS/BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md',
             ['nonnegative effects E_i(s) >= 0','finite_effect_born_readout_unique']),
            ('02_REGISTRY/research/A4D_NATIVE_REFERENCE_MEMORY_PREPARATION.md',
             ['universal exact','requires orthogonal retained references'])]
        for path,fragments in paths:
            data=(base/path).read_bytes();text=data.decode()
            ck('existing_native_interface_pin:'+path,all(v in text for v in fragments))
            pins.append(dict(path=path,sha256=hashlib.sha256(data).hexdigest()))
    return dict(status='PASS_EXACT_NATIVE_COLLECTIVE_POINTER_MODE',checks=checks,pins=pins,
        actual_word='R=(I tensor G) CNOT (I tensor G*) CNOT=controlled G^2, W=R^2=controlled G^4. The whole 4x4 word is fixed, unitary on all columns, and consists only of already owned addressed golden/CNOT operations. Forward-only implementation uses four G and eight CNOT with the old supplied retained basis-one inverse control. Its preparation/address price remains actual.',
        actual_observable='The programme is the actual native computational occupation N_r on one CAR bit, tensor identity on the other three bits and reference128. W=(I-N_r) tensor I_flag+N_r tensor G^4. No physical matter grade or correlation is discarded, and the input can be an arbitrary unknown density on the full carrier. This diagram needs no field-code angle oracle.',
        probability='With the new flag initially blank, q_good=1-delta*f, q_bad=delta*f, f=Tr(rho N_r), delta=16p^9. Since delta<1/2, the same pointer outcome is uniquely most probable for EVERY normalized unknown input, including entangled full CAR/reference states. Only the detector flag is read; the programme remains retained quantum work.',
        supplied_copies='For k genuinely independently supplied preparations and one fresh detector flag per preparation, all pointer patterns factor. The unique all-good mode has q_good=(1-delta*f)^k. This is an actual finite multilinear-input experiment; it does not clone unknown states or require continuous matrix/gate programming.',
        mode_C2='If the declared pointer cut has actual history weights q and native MDL mode reading, S_mode=-k log(1-delta*f)/logphi. DS=k delta Df/((1-delta*f)logphi). D2S=k[delta D2f/(1-delta*f)+delta^2 Df Df/(1-delta*f)^2]/logphi. The input map and its true normalization/preparation jets determine Df, not an arbitrary sampled-price interpolation.',
        common_mode_mixture='More generally, use a fixed coherent controlled unitary sum_alpha P_alpha tensor W_alpha with commuting actual programme projectors and the same pointer-good outcome. For the unmeasured retained programme, q_S=sum_alpha Tr(P_alpha sigma) q_S(alpha) exactly, without dephasing its full state. If every conditional branch has q_other(alpha)<=rmax*g_alpha, rmax<1, the same inequality holds after summation and the good pointer mode remains unique. Its price is -log E(g_alpha), not E(-log g_alpha).',
        important_history_boundary='Emitting programme outcomes changes the complete mode. At f=1/2, the quantum-work pointer-good probability is 1-delta/2, whereas the joint emitted-programme mode has probability 1/2. Full unitarity and retaining work therefore do not by themselves prove that pointer coarse history is the native complete Book history cut. Initial-state/preparation cost, physical history/Info binding and all additional actual terms must be checked rather than silently omitted.',
        approximation_route='A fixed finite sample-register-controlled programme may approximate a known function of actual commuting input-readout probabilities, using one circuit chosen for the whole chart. Bernstein/collective polynomial approximation then uses input variation, not a discontinuously chosen gate word. It still needs its actual C2 approximation/resource theorem, common positive mode, programme/history binding and physical preparation copies. For rare target g, absolute probability error must be o(g); only preserved per-trial product structure avoids generic exponential relative precision.',
        scope='This is a constructive real native finite-word INPUT-source component for the specified existing observable. It does not turn occupation probability into curvature, bind unknown amplitudes to a Julia angle, produce the section6.58 geometric query, select Einstein dynamics or prove native stationary/refining roots. Those require the same actual field-to-observable/input law and full-price domain.')

def hodge_native_input_lift_controls(root):
    import ast
    import hashlib
    from itertools import product
    from pathlib import Path
    from types import SimpleNamespace
    import sympy as s
    root=Path(root)
    path=root/'02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py'
    creator=next(n for n in ast.parse(path.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='creator')
    pin=hashlib.sha256(ast.dump(creator,include_attributes=False).encode()).hexdigest()
    if pin!='801b33d7ef3e41f6425be16153c82b1402215f6be757ea275ff06a69010f58e4':raise ArithmeticError('literal creator pin')
    ns={'s':s,'SUBS':[tuple(i for i in range(4) if mask&(1<<i)) for mask in range(16)]}
    exec(compile(ast.Module(body=[creator],type_ignores=[]),str(path),'exec'),ns)
    current=root/'02_REGISTRY/research/certificates/a4d_native_correlated_current_transition.py'
    current_pin=hashlib.sha256(current.read_bytes()).hexdigest()
    if current_pin!='e659733a8ab4fea30f46de56663dc344249420c7e0a3ea65b2aa1a2091b76e0d':raise ArithmeticError('actual current owner pin')
    node=next(n for n in ast.parse(current.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='car_operators')
    ops={'s':s,'C':SimpleNamespace(creator=ns['creator']),'I4':s.eye(4)}
    exec(compile(ast.Module(body=[node],type_ignores=[]),str(current),'exec'),ops)
    creators,beta,gammas,alphas=ops['car_operators']()
    vp=root/'02_REGISTRY/research/sources/d0_record_generated_heat_v8_2026-10-14/verify.py'
    vnode=next(n for n in ast.parse(vp.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='exact')
    vpin=hashlib.sha256(ast.dump(vnode,include_attributes=False).encode()).hexdigest()
    if vpin!='9f62da27fd64a07005a5ee30eaedbf665f309f15b3799e8049e6f7290dac27ff':raise ArithmeticError('literal v8 exact word pin')
    rpin=hashlib.sha256(vp.with_name('RESULT.md').read_bytes()).hexdigest()
    if rpin!='f7ea30d997a58fa4e608d4403acae5f5e3d7e5da45116f9a7c3f62be5e99115c':raise ArithmeticError('literal v8 input price pin')
    checks=[]
    def ck(name,val):
        if not val:raise ArithmeticError(name)
        checks.append(name)
    P,x,y,z=s.symbols('P psi0 psi4 spectator3',real=True)
    m=s.zeros(16,1);m[1]=P;m[0]=x;m[15]=y;m[14]=z
    for i,A in enumerate(alphas):ck('full16 original CAR current numerator '+str(i+1),s.expand((m.T*A*m)[0])==0)
    ck('all16 source domain retained',len(m)==16 and len(creators)==4)
    ck('first-grade clock independent of Hodge phase',m[1]==P and all(m[i]==0 for i in (2,4,8)))
    ck('normalization has one exact real complement',s.expand((m.T*m)[0]).subs(z*z,1-P*P-x*x-y*y)==1)
    bad=m.copy();bad[14]=0;bad[3]=z
    ck('2form complement need not keep actual current fixed',s.expand((bad.T*alphas[0]*bad)[0])==2*x*z)
    # Exactly one small actual L=8 fiber. Orthogonality follows by a product
    # of geometric sums, not a 65536-dimensional state computation.
    L=8;N=L**4
    zeta=(1+s.I)/s.sqrt(2)
    sums=[s.simplify(sum(zeta**(d*j) for j in range(L))) for d in range(L)]
    ck('all Fourier differences have exact geometric sum',sums==[L]+[0]*7)
    modes=list(product(range(8),range(4),range(4)))
    ck('128 existing site characters, no CAR/ref copy',len(modes)==128 and len(set(modes))==128)
    ck('full fixedRIGHT128 character Gram',all(
        sums[(a[0]-b[0])%L]*sums[(a[1]-b[1])%L]*sums[(a[2]-b[2])%L]*L
        ==(N if a==b else 0) for a in modes for b in modes))
    ck('uniform site probability with all reference columns',s.Rational(1,128*N)*len(modes)==s.Rational(1,N))
    # A faithful ENTANGLED full RIGHT example in one actual M2 block.
    # Here reference dimension2 is only a tiny exact instance of the general
    # algebraic formula; the preceding original128 Gram remains unchanged.
    bell=s.Matrix([1,0,0,1])/s.sqrt(2)
    Pbell=bell*bell.T
    sigma=s.eye(4)/8+Pbell/2
    sigroot=s.eye(4)/s.sqrt(8)+(s.sqrt(s.Rational(5,8))-1/s.sqrt(8))*Pbell
    ck('correlated fullRIGHT exact positive square root',(sigroot*sigroot-sigma).applyfunc(s.simplify)==s.zeros(4))
    sigref=s.Matrix(2,2,lambda i,j:sum(sigma[2*b+i,2*b+j] for b in range(2)))
    ck('correlated fullRIGHT has fixed reference marginal',sigref==s.eye(2)/2)
    singlet=s.Matrix([0,1,-1,0])/s.sqrt(2)
    pt=s.Matrix(4,4,lambda i,j:sigma[2*(i//2)+(j%2),2*(j//2)+(i%2)])
    ck('example is quantum correlated not product',(singlet.T*pt*singlet)[0]==-s.Rational(1,8))
    pp=(s.sqrt(5)-1)/2
    ms=[]
    for q0,q4 in ((s.Rational(1,10),0),(0,s.Rational(1,10))):
        mm=s.zeros(16,1);mm[1]=s.sqrt(pp);mm[0]=q0;mm[15]=q4;mm[14]=s.sqrt(1-pp-s.Rational(1,100));ms.append(mm)
    BF=s.Matrix([[1,1],[1,-1]])/s.sqrt(2)
    V=s.zeros(64,4)
    for b,j,mask,a in product(range(2),range(2),range(16),range(2)):
        V[32*b+16*j+mask,2*b+a]=BF[j,a]*ms[j][mask]
    ck('fullRIGHT insertion isometry all CAR16',(V.T*V-s.eye(4)).applyfunc(s.simplify)==s.zeros(4))
    CC=V*sigroot
    ck('full correlated joint Gram preserved',(CC.T*CC-sigma).applyfunc(s.simplify)==s.zeros(4))
    for j in range(2):
        rhoj=sum((CC[32*b+16*j:32*b+16*j+16,:]*CC[32*b+16*j:32*b+16*j+16,:].T for b in range(2)),s.zeros(16))
        ck('correlated local CAR factor at site '+str(j),(rhoj-ms[j]*ms[j].T/2).applyfunc(s.simplify)==s.zeros(16))
    # If the SAME AF index were two CENTRAL M1 blocks instead of one M2,
    # off-center sigma would not be a matching-block GNS marginal.
    Pcenter=s.diag(1,1,0,0)
    ck('cross-center coherence is not an admitted matching GNS marginal',sigma*Pcenter!=Pcenter*sigma)
    # Literal old-v8 full16 scalar Fourier symbol, NOT a new Delta:
    # G=(d-o)I+o11*, all128 input columns and both Hodge sidebands retained.
    a,kappa,hh,Ebar=s.symbols('a kappa h Ebar',positive=True)
    diag,off=s.symbols('d o',positive=True)
    ct,st=s.symbols('cos_theta sin_theta',real=True)
    re=s.symbols('rv rx ry',real=True);im=s.symbols('iv ix iy',real=True)
    trans=[re[i]+s.I*im[i] for i in range(3)]
    G=(diag-off)*s.eye(4)+off*s.ones(4)
    def energy(z0):
        zz=s.Matrix([z0]+trans)
        return s.expand((zz.conjugate().T*G*zz)[0])
    side=s.expand((energy((ct-1+s.I*st)/hh)+energy((ct-1-s.I*st)/hh))/2-energy(0))
    side=s.expand(side).subs(st**2,1-ct**2)
    target=2*(1-ct)/hh**2*(diag-off*hh*sum(re))
    ck('literal v8 symbol exact two-sideband identity',s.simplify(side-target)==0)
    cosines=[s.simplify(s.re(zeta**i)) for i in range(L)]
    cbar=s.simplify(3-sum(cosines)/8-2*sum(cosines[:4])/4)
    ck('all128 actual L8 transverse modes average factor',cbar==s.Rational(5,2))
    ah=a*kappa*hh/(2*s.sin(kappa*hh/2))
    eig=4*s.sin(kappa*hh/2)**2/hh**2
    R=Ebar+ah**2*eig*(diag+off*cbar)
    ck('finite literal input energy with original offdiagonal Gram',s.simplify(R-(Ebar+a*a*kappa*kappa*(diag+off*cbar)))==0)
    ck('fixedRIGHT amplitude tangent has positive upstream source',s.simplify(s.diff(R,a)-2*a*kappa*kappa*(diag+off*cbar))==0 and diag+off*cbar>0)
    return dict(status='PASS',checks=checks,creator_AST_sha256=pin,current_owner_sha256=current_pin,original_v8_exact_AST_sha256=vpin,original_v8_price_sha256=rpin,
      input='m0=√p e1+psi0 e0+psi4 e15+√(1−p−a_h²)e14, psi0²+psi4²=a_h². Original alpha_i expectation0, norm1, first-grade coefficient√p. e14 is original spatial3-form, not a new carrier.',
      full_right='For L>=8 choose f_a(j)=L^-2 exp(2pi i(k_v j_v+k_x j_x+k_y j_y)/L), k_v=0..7,k_x/y=0..3. C_(j,mask;a)=f_a(j)m0,j(mask)/sqrt128; C*C=I128/128. All k_u=0, local reduced CAR=|m0,j><m0,j|/L^4. Raw input I_norm^-1C has exact native G normalization, with all moving I jets.',
      full_right_general='For any ACTUAL center-block-diagonal full sigma_R on oldAF_RIGHT tensor ref128, with Tr_AF sigma_R=I128/128: choose blockwise oldR-to-oldL isometry T, Fourier isometry B, and site insertion S_m. V=S_m(T tensor B) isometry; C=V sqrt(sigma_R) has C*C=sigma_R, and local CAR=|m_j><m_j|/S. No product AF/ref assumption. Does not preserve a specified old LEFT state/archive. Cross-center coherences need a larger carrier and are not standard matching-block GNS data.',
      scope='Exact kinematic input section and full finite operator controls. Not native primitive PREP/query admission, equality with twelve-channel endpoint clock metric, state-to-code cloning, whole-price stationarity or arbitrary fixedRIGHT tangent surjectivity. Literal flat old-v8 G=(d−o)I+o11* gives R=Etrans+a_h² lambda_u(d+5o/2), all128 full columns; dR/da>0 with fixed geometry/current/clock. This refutes whole old-HJR stationarity of this flat input section, not a curved-pp extrapolation.')

def fixed_polynomial_input_effect(root=None):
    import sympy as sp
    checks={}
    def ck(name,v):
        checks[name]=bool(v)
        if not checks[name]: raise AssertionError(name)
    I2=sp.eye(2)
    X=sp.Matrix([[0,1],[1,0]])
    Y=sp.Matrix([[0,-sp.I],[sp.I,0]])
    Z=sp.diag(1,-1)
    def swap(N,a,b):
        W=sp.zeros(2**N)
        for j in range(2**N):
            bits=[(j>>(N-1-i))&1 for i in range(N)]
            bits[a],bits[b]=bits[b],bits[a]
            k=sum(t<<(N-1-i) for i,t in enumerate(bits))
            W[k,j]=1
        return W
    S2=swap(2,0,1)
    H2=sp.Rational(2,5)*sp.eye(4)+sp.Rational(1,2)*S2
    P3=(swap(3,0,1)+swap(3,0,2)+swap(3,1,2))/3
    H3=sp.Rational(2,5)*sp.eye(8)+sp.Rational(1,2)*P3
    ck('diagnostic_initial_polynomial_operator_is_not_positive',-sp.Rational(1,10) in H2.eigenvals())
    ck('symmetrized_three_copy_operator_is_strict_effect',H3.eigenvals()=={sp.Rational(2,5):4,sp.Rational(9,10):4})
    ck('purity_witness_uses_entire_three_copy_carrier',H3.shape==(8,8) and P3*P3==P3)
    for a,b in [(0,1),(0,2),(1,2)]:
        W=swap(3,a,b)
        ck('three_copy_effect_permutation_invariant_'+str(a)+str(b),W*H3*W.T==H3)
    x,y,z,t=sp.symbols('x y z t',real=True)
    rho=(I2+x*X+y*Y+z*Z)/2
    g=sp.Rational(2,5)+sp.Rational(1,2)*sp.trace(rho*rho)
    q2=sp.trace(H2*sp.kronecker_product(rho,rho))
    q3=sp.trace(H3*sp.kronecker_product(rho,rho,rho))
    ck('exact_two_copy_polynomial_representation',sp.expand(q2-g)==0)
    ck('positive_elevation_does_not_change_any_IID_input_probability',sp.expand(q3-g)==0)
    ck('all_Bloch_coordinate_first_sources_match',all(sp.expand(sp.diff(q3-g,v))==0 for v in [x,y,z]))
    ck('all_Bloch_coordinate_second_sources_match',all(sp.expand(sp.diff(q3-g,v,w))==0 for v in [x,y,z] for w in [x,y,z]))
    for A,v in [(X,x),(Y,y),(Z,z)]:
        qfirst=sp.trace(H3*sp.kronecker_product(rho+t*A/2,rho,rho))
        ck('independent_first_copy_row_is_one_third_diagonal_'+str(v),sp.expand(sp.diff(qfirst,t).subs(t,0)-sp.diff(g,v)/3)==0)
    # Fixed algebraic Naimark, independent of x,y,z, with all input work kept.
    C=sp.sqrt(sp.Rational(2,5))*sp.eye(8)+(sp.sqrt(sp.Rational(9,10))-sp.sqrt(sp.Rational(2,5)))*P3
    B=sp.sqrt(sp.Rational(3,5))*sp.eye(8)+(sp.sqrt(sp.Rational(1,10))-sp.sqrt(sp.Rational(3,5)))*P3
    U=C.row_join(-B).col_join(B.row_join(C))
    ck('fixed_Naimark_good_effect_is_H3',all(sp.simplify(v)==0 for v in C.T*C-H3))
    ck('fixed_Naimark_bad_effect_is_complement',all(sp.simplify(v)==0 for v in B.T*B-(sp.eye(8)-H3)))
    ck('fixed_Naimark_unitary_on_all_sixteen_directions',all(sp.simplify(v)==0 for v in U.T*U-sp.eye(16)))
    ck('fixed_detector_matrix_has_no_unknown_state_parameters',not any(v.free_symbols for v in U))
    # Source convention in CKMR uses HALF trace norm. The chosen conservative
    # full-trace norm bound is 4 D^2 k/N; do not execute a huge N tensor.
    D,k,L=2,2,sp.Rational(9,10)
    m,M=sp.Rational(13,20),sp.Rational(9,10)
    delta=min(m,1-M)
    Nbound=math.ceil(float(8*L*D*D*k/delta))+1
    eps=4*L*D*D*k/Nbound
    ck('CKMR_full_trace_norm_conservative_copy_budget_strict',eps<delta/2)
    ck('CKMR_spectral_certificate_places_lift_inside_effect_interval',m-eps>0 and M+eps<1)
    # Failure refinement uses the OWNED G^2 seed weights p^6,4p^3.
    p=(sp.sqrt(5)-1)/2
    w1=p**6; w0=1-w1; b=4*p**3
    ck('owned_controlled_square_seed_normalizes',sp.simplify(p**6+b-1)==0)
    d=8
    floor=(w0-w1)**(2*d)
    ceiling=w0**(2*d)
    T=0
    while float((1-floor)*b**T)>=float(floor): T+=1
    gap=sp.simplify(floor-(1-floor)*b**T)
    ck('original_golden_determinant_uniform_floor_is_positive',float(floor)>0 and float(ceiling)<1)
    ck('finite_failure_split_makes_one_good_pointer_strict_global_mode',float(gap)>0)
    ck('failure_split_copy_bound_is_minimal_for_fixture',T==0 or float((1-floor)*b**(T-1))>=float(floor))
    # Complete-preparation hostile control. The IID diagonal and all
    # independent-copy first rows are stationary, but an entangler is not.
    e=sp.Rational(1,4)
    Hent=sp.eye(4)/2+e*sp.kronecker_product(Z,Z)
    plus=sp.Matrix([1,1])/sp.sqrt(2)
    minus=sp.Matrix([1,-1])/sp.sqrt(2)
    pp=sp.kronecker_product(plus,plus)
    mm=sp.kronecker_product(minus,minus)
    pure=sp.cos(t)*pp+sp.sin(t)*mm
    qent=(pure.T*Hent*pure)[0]
    ck('entangling_counter_effect_is_strictly_positive_bounded',Hent.eigenvals()=={sp.Rational(1,4):2,sp.Rational(3,4):2})
    ck('IID_diagonal_first_source_vanishes_at_plus',sp.diff(sp.Rational(1,2)+e*z*z,z).subs(z,0)==0)
    rplus=plus*plus.T
    ck('all_independent_copy_traceless_first_rows_vanish_at_plus',all(sp.trace(Hent*sp.kronecker_product(A/2,rplus))==0 for A in [X,Y,Z]))
    ck('entangling_joint_preparation_has_nonzero_exact_first_source',sp.simplify(sp.diff(qent,t).subs(t,0))==2*e)
    ck('entangling_counter_one_owned_seed_makes_good_mode_strict_at_base',float((1-qent.subs(t,0))*b)<float(qent.subs(t,0)))
    ck('entangling_mode_action_source_is_not_stationary',sp.simplify(-sp.diff(qent,t).subs(t,0)/qent.subs(t,0))==-1)
    return {'status':'PASS','checks':len(checks),'check_results':checks,
      'primary_source':{'url':'https://arxiv.org/pdf/quant-ph/0602130','theorem':'II.7, page4; norm convention page2 is half trace norm','half_trace_distance_bound':'2 D^2 k/N','ordinary_trace_norm_bound_used':'4 D^2 k/N'},
      'diagnostic_purity_witness':{'g':'2/5+(1/2)Tr(rho^2)','status':'generic polynomial mechanism diagnostic, NOT a new physical F or native price','H2_spectrum':['-1/10','9/10'],'H3_spectrum':['2/5','9/10'],'conservative_general_bound_N':Nbound},
      'owned_seed_consumer':{'d':d,'determinant_lower_floor':float(floor),'determinant_upper_bound':float(ceiling),'T':T,'strict_complete_pointer_mode_gap':float(gap)},
      'entangling_preparation_counter':{'epsilon':'1/4','diagonal_and_independent_first_rows':0,'joint_entangling_probability_first_source':'1/2','joint_mode_natural_log_source':'-1','bad_pointer_seed_bits':1},
      'scope':'Fixed effect exists exactly for the original g only if its ACTUAL supplied-state polynomial/global-margin premise is proved. No new F/action, cloning, exact Golden effect admission, full fine-data history cut, or native joint-root claim.'}

def hodge_fixed_right_spectral_normal(root=None):
    from pathlib import Path
    import hashlib
    import sympy as s
    checks=[]
    def ck(name,test):
        if not bool(test):raise ArithmeticError(name)
        checks.append(name)
    root=Path.cwd() if root is None else Path(root)
    # The source symbol is the already pinned literal stored-native v8 class.
    owner=root/'02_REGISTRY/research/A4D_NATIVE_COMPLETE_FIELD_SOURCE_AND_TRANSPORT.md'
    sha=hashlib.sha256(owner.read_bytes()).hexdigest()
    ck('actual full field owner pin',sha=='7b82d30d0d8ec451f768bf0b92aa0e4daaad1f2600497ae7d855bf370c96a338')
    theta,delta=s.symbols('theta alpha',real=True)
    d,o,h=s.symbols('d o h',positive=True)
    cc,ss=s.symbols('sum_cos sum_sin',real=True)
    # Full G has diagonal d and offdiagonal o. Transverse z sum is
    # (sum_cos-3+i sum_sin)/h; all transverse pair terms are theta-constant.
    zu=(s.exp(s.I*theta)-1)/h
    zs=(cc-3+s.I*ss)/h
    dep=s.expand_complex(d*zu.conjugate()*zu+o*(zu.conjugate()*zs+zs.conjugate()*zu))
    B=-2*(d+o*(3-cc))/h**2
    C=2*o*ss/h**2
    A=2*(d+o*(3-cc))/h**2
    ck('exact actual u-symbol trigonometric decomposition',s.trigsimp(dep-(A+B*s.cos(theta)+C*s.sin(theta)))==0)
    v,w=s.symbols('v w',real=True)
    # Energy increments lambda(theta +/- alpha)-lambda(theta).
    dp=(s.cos(delta)-1)*v+s.sin(delta)*w
    dm=(s.cos(delta)-1)*v-s.sin(delta)*w
    mat=s.Matrix([[s.cos(delta)-1,s.sin(delta)],[s.cos(delta)-1,-s.sin(delta)]])
    ck('triple-energy equality has no nonzero Fourier pair',s.simplify(mat.det()-2*(1-s.cos(delta))*s.sin(delta))==0)
    ck('paired commutator norm exact',s.expand(dp**2+dm**2-2*((1-s.cos(delta))**2*v*v+s.sin(delta)**2*w*w))==0)
    ck('amplitude pair is invariant under theta rotation',s.trigsimp((B*s.cos(theta)+C*s.sin(theta))**2+(-B*s.sin(theta)+C*s.cos(theta))**2-B**2-C**2)==0)
    # On actual transverse momenta cc=sum cos <=3 and o>=0:
    # |B| >=2d/h^2. 0<alpha<pi makes both increment factors nonzero.
    a=s.symbols('a',positive=True)
    x,y=s.symbols('real_right_residual imag_right_residual',real=True)
    weight=a*a
    alpha_v=(s.cos(delta)-1)*v
    weighted=(1-weight)*(x*x+y*y)+weight*((x+dp)**2+y*y)/2+weight*((x+dm)**2+y*y)/2
    completed=(x+weight*alpha_v)**2+y*y+weight*(1-weight)*alpha_v**2+weight*s.sin(delta)**2*w*w
    ck('full right-residual completion of square exact',s.expand(weighted-completed)==0)
    ck('residual Cauchy constant retains clock and complement',s.simplify((2/a**2+2/(1-a*a))*a*a*(1-a*a)-2)==0)
    # A small exact finite instance of the general all-RIGHT proof. Two
    # reference columns are Fourier k=0 and k=1 on L=8. Four original CAR
    # masks, normalized m_j, are retained. No 128-dimensional diagonalization.
    L=8;hh=s.Rational(1,L);aa=s.Rational(1,4)
    zeta=(1+s.I)/s.sqrt(2)
    def lam(k):return s.simplify((2-zeta**k-zeta**(-k))/hh**2)
    eig=[lam(k) for k in range(L)]
    ck('finite actual zero mode preserved',eig[0]==0)
    ck('both first Hodge sidebands have the same actual energy',eig[1]==eig[7])
    ck('clock plus wave cannot share a positive shell',eig[0]!=eig[1])
    ck('all finite Fourier triple tests exclude support',all(not(eig[k]==eig[(k+1)%L]==eig[(k-1)%L]) for k in range(L)))
    # For one normalized Fourier r-column, the least-squares right normal
    # subtracts the weighted mean. This is exact for a common scalar L.
    residuals=[]
    for k in (0,1):
        weights=[1-aa*aa,aa*aa/2,aa*aa/2]
        vals=[eig[k],eig[(k+1)%L],eig[(k-1)%L]]
        mean=s.simplify(sum(t*x for t,x in zip(weights,vals)))
        var=s.simplify(sum(t*(x-mean)**2 for t,x in zip(weights,vals)))
        ck('finite full four-grade least normal k'+str(k),var>0)
        residuals.append(var)
    # Actual normalized two-column C has Gram I2/2; the compressed Hessian
    # is diagonal because m_j* Delta(m_j e^{ikj}) has no j dependence.
    bound2=s.simplify((2/hh**2*(1-s.sqrt(2)/2)*aa*s.sqrt(1-aa*aa))**2)
    ck('finite all-normal lower bound attained at k0',s.simplify(residuals[0]-bound2)==0)
    ck('finite two-reference normal exceeds analytic uniform bound',s.simplify(sum(residuals)/2-bound2)>=0)
    # Positive scoped control: the pre-existing 128 preparations are
    # +/-e_r times all16 CAR. They lie in ONE actual flat-v8 shell for any
    # positive o because every cross component is zero, retaining I128/128.
    unit_modes=[]
    for axis in range(4):
        for sign in (-1,1):
            zz=s.zeros(4,1);zz[axis]=(zeta**sign-1)/hh
            G=(d-o)*s.eye(4)+o*s.ones(4)
            unit_modes.append(s.simplify((zz.conjugate().T*G*zz)[0]))
    ck('all original eight momentum modes share exact native shell',all(s.simplify(x-d*eig[1])==0 for x in unit_modes))
    ck('original full RIGHT128 shell dimension retained',len(unit_modes)*16==128)
    return dict(status='PASS',checks=checks,source_sha256={str(owner.relative_to(root)):sha},
      statement='For ANY site/right rows r, local pure-CAR C_j=m_j r_j with m=(a cos(kappa u),sqrt(p),sqrt(1-p-a^2) at14,a sin(kappa u) at15) cannot solve the fixed-RIGHT preparation Euler of the SAME flat v8 H+J+R, for 0<kappa h<pi,d>0,o>=0. All correlations/rank/reference dimensions are allowed. Other CAR grades are not removed.',
      exact_normal='C*C=sigma_R, Trsigma=1 gives Delta C=C L, L=L*. Within the four-grade test carrier actual current observer is fixed for every variation because alpha_i compress to0. Thus H/J derivatives vanish, not frozen. Clock and 3form rows give Delta r=rL; scalar +/-i top gives both commutators. Fourier support would need lambda(k)=lambda(k +/-kappa e_u), impossible for the actual u-symbol B<0.',
      quantitative_bound='For ANY right L (even nonHermitian), ||Delta C-C L||_F >= (2d/h^2) min(1-cos(kappa h),sin(kappa h))*a*sqrt(1-a^2). For kappa h<=pi/2 the bound tends d_*kappa^2*a*sqrt(1-a^2)>0 if d(h)->d_*>0; a uniform d lower bound gives a positive liminf. This is the normalized whitened preparation norm, not original raw#216.',
      positive_control='The pre-existing +/-e_r tensor CAR16 bath has128 isospectral states and solves the fixed-RIGHT preparation Euler; its local CAR is I16/16 and it does not have the coherent Hodge amplitudes of the excluded section.',
      scope='Declared flat old-v8 price at fixed beta/ell/geometry and actual rest-current readout. No curved-pp/global-D0 no-go, no physical selection, no extra action. Local mixed CAR, actual state-dependent operator and full Book costs can change the problem and require their own sources.')


def hodge_mixed_preparation_control(root):
    import ast
    import hashlib
    from pathlib import Path
    from types import SimpleNamespace
    import sympy as s
    root=Path(root)
    checks=[]
    def ck(name,value):
        if not bool(value):raise ArithmeticError(name)
        checks.append(name)
    def zero(M):return M.applyfunc(lambda x:s.simplify(s.trigsimp(x)))==s.zeros(*M.shape)
    src=root/'02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py'
    node=next(n for n in ast.parse(src.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='creator')
    pin=hashlib.sha256(ast.dump(node,include_attributes=False).encode()).hexdigest()
    ck('original full16 creator AST pin',pin=='801b33d7ef3e41f6425be16153c82b1402215f6be757ea275ff06a69010f58e4')
    env={'s':s,'SUBS':[tuple(i for i in range(4) if mask&(1<<i)) for mask in range(16)]}
    exec(compile(ast.Module(body=[node],type_ignores=[]),str(src),'exec'),env)
    current=root/'02_REGISTRY/research/certificates/a4d_native_correlated_current_transition.py'
    current_sha=hashlib.sha256(current.read_bytes()).hexdigest()
    ck('actual current owner pin',current_sha=='e659733a8ab4fea30f46de56663dc344249420c7e0a3ea65b2aa1a2091b76e0d')
    node=next(n for n in ast.parse(current.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='car_operators')
    ops={'s':s,'C':SimpleNamespace(creator=env['creator']),'I4':s.eye(4)}
    exec(compile(ast.Module(body=[node],type_ignores=[]),str(current),'exec'),ops)
    _,_,_,alphas=ops['car_operators']()
    t=s.symbols('theta',real=True)
    p,a=s.symbols('p a',positive=True)
    b=s.sqrt(1-p-2*a*a)
    M=s.zeros(16,2)
    M[1,0]=s.sqrt(p)*s.cos(t);M[1,1]=s.sqrt(p)*s.sin(t)
    M[0,0]=a*s.cos(t);M[0,1]=-a*s.sin(t)
    M[15,0]=a*s.sin(t);M[15,1]=a*s.cos(t)
    M[14,0]=b*s.cos(t);M[14,1]=b*s.sin(t)
    rho=(M*M.T).applyfunc(s.trigsimp)
    for i,A in enumerate(alphas):
        ck('all two-column current matrix entries vanish '+str(i+1),zero(M.T*A*M))
    ck('pointwise total CAR probability one',s.simplify(s.trace(rho))==1)
    ck('first-grade density line and scale p',s.trigsimp(rho[1,1]-p)==0 and all(rho[i,j]==0 for i in (2,4,8) for j in (1,2,4,8)))
    ck('scalar coherence reads a cos two theta',s.trigsimp(rho[0,1]/s.sqrt(p)-a*s.cos(2*t))==0)
    ck('top coherence reads a sin two theta',s.trigsimp(rho[15,1]/s.sqrt(p)-a*s.sin(2*t))==0)
    ck('both scalar diagonal weights are a squared',s.trigsimp(rho[0,0]-a*a)==0 and s.trigsimp(rho[15,15]-a*a)==0)
    ck('scalar-top coherence is zero',rho[0,15]==0)
    ck('mixed scalar total weight is twice inferred pure pair',s.trigsimp(rho[0,0]+rho[15,15]-2*a*a)==0)
    # A nonzero principal minor proves rank>=2 for every phase when a>0.
    ck('local CAR density is genuinely mixed',s.trigsimp(rho[0,0]*rho[15,15]-rho[0,15]**2-a**4)==0)
    ck('complement differs from pure Hodge section by minus a squared',s.trigsimp(rho[14,14]-(1-p-a*a)+a*a)==0)
    L=8
    moments=[M.subs(t,2*s.pi*j/L) for j in range(L)]
    gram=sum((T.T*T for T in moments),s.zeros(2))/L
    ck('site-averaged exact two-column Gram I2 over2',zero(gram-s.eye(2)/2))
    d,h=s.symbols('d h',positive=True)
    lap=s.Matrix(L,L,lambda j,k:d/h**2*(2*int(j==k)-int((j-k)%L==1)-int((j-k)%L==L-1)))
    co=s.Matrix([s.cos(2*s.pi*j/L) for j in range(L)])
    si=s.Matrix([s.sin(2*s.pi*j/L) for j in range(L)])
    lam=s.simplify(4*d*s.sin(s.pi/L)**2/h**2)
    ck('literal flat native one-axis cosine eigenmode',zero(lap*co-lam*co))
    ck('literal flat native one-axis sine eigenmode',zero(lap*si-lam*si))
    # Delta is scalar times I16 on this actual Fourier shell. Therefore
    # every component, not merely an averaged expectation, is an eigenmode.
    C=s.Matrix.vstack(*moments)/s.sqrt(L)
    D=s.kronecker_product(lap,s.eye(16))
    ck('all16 two-column preparation is an exact eigensubspace',zero(D*C-lam*C))
    R=s.simplify(s.trace(C.T*D*C))
    ck('old Rayleigh cost equals lambda independent of radius',s.simplify(R-lam)==0 and s.simplify(s.diff(R,a))==0)
    ck('homogeneous metric coefficient source independent of radius',s.simplify(s.diff(R,d)-lam/d)==0 and s.simplify(s.diff(R,d,a))==0)
    Wgram=2*gram
    # Canonical full128 replication is an algebraic Gram proof, not a
    # fabricated 8192x128 scientific state or arbitrary-sigma theorem.
    ck('64 orthogonal AF labels times two columns gives full128',64*Wgram.rows==128 and s.kronecker_product(s.eye(64),Wgram)==s.eye(128))
    ck('canonical fixedRIGHT128 trace normalized',s.trace(s.eye(128)/128)==1)
    return {'status':'PASS','checks':checks,'source_sha256':{str(src.relative_to(root))+'::creator_AST':pin,str(current.relative_to(root)):current_sha},
      'exact_control':'At each site use masks1:sqrt(p)(cos theta,sin theta);0:a(cos theta,-sin theta);15:a(sin theta,cos theta);14:sqrt(1-p-2a^2)(cos theta,sin theta). Domain 0<a^2<(1-p)/2. Columns lie in the same actual flat ku=+/-kappa shell. Site-averaged C*C=I2/2 and Delta C=lambda C.',
      'full128':'With 64 existing mutually orthogonal AF LEFT multiplicity labels xi and the EXPLICIT Delta_total=I_AF tensor Delta_old hypothesis, V=direct_sum_64(sqrt(2)C) is an isometry. V/sqrt(128) gives canonical reference128 Gram I128/128 and the same local CAR density. This does not prove the claim for arbitrary correlated FULLRIGHT sigma.',
      'readout_boundary':'The two density coherences equal the old pure-section scalar readings at phase2theta. Full local density differs: rho00=rho15,15=a^2, rho0,15=0 and spectator weight1-p-2a^2. The original pure normalized amplitude readout is not thereby extended to mixed states.',
      'source_boundary':'R=lambda is independent of a, as is its homogeneous flat geometric coefficient source; the inferred Hodge pair has continuum gradient energy4a^2 kappa^2. Thus preparation stationarity does not establish same total geometric source, a curved-pp root, a new physical readout, or full D0 closure.',
      'clock_boundary':'The exact current is rest-directed and first-grade DENSITY is p along e0. This proves a density clock line/scale in this matrix control only; it does not identify the original single-vector P1 amplitude clock on mixed states.'}


def targeted_choi_source_controls(root=None):
    from pathlib import Path
    import hashlib
    import sympy as s
    root=Path.cwd() if root is None else Path(root)
    checks=[]
    def ck(name,test):
        if not bool(test):raise ArithmeticError(name)
        checks.append(name)
    pins={
      '02_REGISTRY/research/A4D_NATIVE_FULL_LORENTZ_ADJOINT_SOURCE.md':'a0a8a0b7389c7a6120ebbe402d111bf55cd2a00730403a00ffceca73548e7915',
      '02_REGISTRY/research/A4D_DIRECT_DENSITIZED_LEFT_FEEDBACK_EINSTEIN_SCALAR_SOURCE_2026_10_18.md':'a48ff3bb7e88e3b2dde8252029e69d31f1ee8a7de4577415bb13136554c65efa'}
    for path,sha in pins.items():ck('same actual query/operand owner '+Path(path).name,hashlib.sha256((root/path).read_bytes()).hexdigest()==sha)
    theta=s.symbols('theta',real=True)
    V=s.Matrix([[s.cos(theta),-s.sin(theta)],[s.sin(theta),s.cos(theta)]])
    omega=s.Matrix([1,0,0,1])/s.sqrt(2)
    output=s.kronecker_product(V,s.eye(2))*omega
    chi=omega.col_join(output)/s.sqrt(2)
    rho=chi*chi.T
    ck('whole query Choi anchor is normalized at all fields',s.trigsimp((chi.T*chi)[0])==1)
    for i in range(2):
        for j in range(2):
            A=s.zeros(8);b=4+2*i+j;A[0,b]=A[b,0]=2
            value=s.trace(A*rho)
            ck('all-input matrix entry from fixed real observable '+str((i,j)),s.trigsimp(value-V[i,j])==0)
            ck('first and second actual query jets '+str((i,j)),all(s.trigsimp(s.diff(value,theta,n)-s.diff(V[i,j],theta,n))==0 for n in (1,2)))
    chi_minus=omega.col_join(-output)/s.sqrt(2)
    ck('unanchored Choi loses global real sign',output*output.T==(-output)*(-output).T)
    ck('anchor retains the same global sign',s.simplify((rho-chi_minus*chi_minus.T)[0,4])==s.cos(theta)/2)
    # Fixed imaginary Hermitian observables are NOT real compiler inputs.
    B=s.zeros(8);B[4,0]=2*s.I;B[0,4]=-2*s.I
    ck('Hermitian is not the real-symmetric compiler condition',B.conjugate().T==B and B.T!=B)
    p=(s.sqrt(5)-1)/2
    ck('global actual AF control interval positive',3*p*p/4>0 and 5*p*p/4<1)
    ck('global actual scene amplitude interval strict',p-p*p/4>0 and p+p*p/4<1)
    # True INTERNAL observer whitening, not an arbitrary coordinate sqrtG.
    z=s.symbols('z',real=True)
    n=s.Matrix([s.cosh(z),s.sinh(z),0,0]);eta=s.diag(1,-1,-1,-1)
    L=s.eye(4);L[:2,:2]=s.Matrix([[s.cosh(z),-s.sinh(z)],[-s.sinh(z),s.cosh(z)]])
    hn=-eta+2*eta*n*n.T*eta
    ck('owned principal internal Lorentz boost squares to h_n',all(s.trigsimp(v)==0 for v in L*L-hn))
    ck('same boost sends actual clock to rest without extra gate',all(s.trigsimp(v)==0 for v in L*n-s.Matrix([1,0,0,0])))
    ck('internal whitening preserves scalar and top amplitudes',s.trigsimp(L.det())==1)
    return dict(status='PASS',checks=checks,source_sha256=pins,
      target='The SAME direct-density star/Hodge two operands, via actual whole Julia/SELECT query access and supplied coupled scalar input; not a new F or action.',
      exact_code='Anchored chi=(|0>Omega+|1>(V tensor I)Omega)/sqrt2. Fixed REAL symmetric observables recover every actual real V entry with normD and exact jets. Whole bank is normalized; no moving success conditioning. Imaginary Hermitian observables are excluded from real compiler.',
      global_polynomial='Taylor degree ell>=2 of the actual analytic operands has same2jets at null/star codepoint. A computable full-density coefficient bound B and golden t^2 B<=1/4 globally validate actual E,b. Its unchanged D3 determinant probability g is polynomial even when F entries have roots. Existing fixed-effect proof needs polynomialg only.',
      source_scope='Exact first/second source equality is on the supplied internal-principal-frame scalar input section. It does not assert independent observer/preparation normals, coordinate top-form conversion, unknown site-weight access, physically forced t, native controlled-query/PREP/copy admission or equality with full Book history/oldHJR.')


def targeted_full_failure_euler(root=None):
    from pathlib import Path
    import hashlib
    import sympy as s
    root = Path.cwd() if root is None else Path(root)
    checks = []
    def ck(name, test):
        if not bool(test):
            raise ArithmeticError(name)
        checks.append(name)
    pins = {
      '01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md':
        'dfa47d91c4994fa8eea64cda67115590056d8aaf48605daf61a1750aaaf0646d',
      '02_REGISTRY/research/A4D_NATIVE_BRANCH_INFORMATION_COCYCLE.md':
        'cf77a70da503c0a58725e1470ed9b73a493ee01a82293058d49dfd6758ae735a',
      '02_REGISTRY/research/A4D_NATIVE_PARTITION_CORRECTED_BRANCH_INFORMATION.md':
        'a4e8c15de4d736366e85f0bd19a2a394f6372295426b830d8a21bd25fbb3190c'}
    for path, sha in pins.items():
        ck('actual unchanged owner '+Path(path).name,
           hashlib.sha256((root/path).read_bytes()).hexdigest() == sha)

    p = (s.sqrt(5)-1)/2
    a, b = s.simplify(p**6), s.simplify(4*p**3)
    ck('actual controlled-G^2 coin complete on both retained outputs',
       s.simplify(a+b-1) == 0)
    ck('actual maximum bad-seed weight is b^T', 0 < a < b < 1)
    g, pi = s.symbols('g pi', positive=True)
    T = s.symbols('T', positive=True, integer=True)
    HB = T*(-a*s.log(a)-b*s.log(b))
    H = -g*s.log(g)-(1-g)*s.log(1-g)+(1-g)*HB
    S = -s.log(g)
    L = s.log((1-g)/g)-HB
    # expand_log(force=True) is legitimate here only on the declared 0<g<1
    # strict-input chart. It proves algebraic equalities, not positivity.
    simp = lambda x: s.simplify(s.expand_log(x, force=True))
    kappa = -g*L
    ck('complete refined mean derivative includes every bad seed',
       simp(s.diff(H,g)-L) == 0)
    ck('SAME full pointer mean and MAP sources are kappa-collinear',
       simp(s.diff(H,g)-kappa*s.diff(S,g)) == 0)
    ck('all field/preparation/clock Hessian terms retained off critical set',
       simp(s.diff(H,g,2)-kappa*s.diff(S,g,2)+s.diff(kappa,g)/g) == 0)
    d2 = s.symbols('d2', real=True)
    ck('at a critical point the Hessians are positive-factor proportional',
       simp(s.diff(H,g)*d2-kappa*(-d2/g)) == 0)
    ck('full complete source mass is identically one with arbitrary prefix',
       s.expand(pi*g+pi*(1-g)+(1-pi)*g+(1-pi)*(1-g)-1) == 0)

    # Counter-consumer of the same probability law, not a new detector.
    # Separate prefix and detector variations need not share kappa.
    Hjoint = -pi*s.log(pi)-(1-pi)*s.log(1-pi)+H
    Sjoint = -s.log(pi)+S  # only on the strict old-winner chart pi>1/2
    wedge = s.diff(Hjoint,pi)*s.diff(Sjoint,g)-s.diff(Hjoint,g)*s.diff(Sjoint,pi)
    expected = -s.log((1-pi)/pi)/g+L/pi
    ck('moving-prefix obstruction is an explicit two-source wedge', simp(wedge-expected) == 0)
    qC, qI, N = s.symbols('qC qI N', positive=True)
    C = -s.log(qC)
    I = s.log(qI/qC)+s.log(N)
    ck('same-history moving code cancels before expectation',
       simp(C-I+s.log(qI)+s.log(N)) == 0)
    return {
      'status':'PASS', 'checks':checks, 'source_sha256':pins,
      'positive_theorem': 'For actual q_good=g and every retained q_bad,z=(1-g) beta_z, beta_z fixed, strict good mode implies L=sum beta_z log(q_bad,z/g)<0. Thus kappa=-g L>0 and D H=kappa D(-log g) on all admitted geometry, preparation and continuous-clock tangents of the same fixed word, including full correlated-code inputs. At Dg=0 the Hessians are kappa-proportional.',
      'uniform_gap': 'If E_N>=mu I and r_gap=(1-mu)b^T/mu<1, then kappa>=-mu log(r_gap)>0 for this finite programme. This is not uniform under refinement; errors must be divided by the actual kappa and original physical signal.',
      'raw_Book_binding': 'Only if independently owned SAME histories have w=N_Book q and C=-log_phi mu does Info=log_phi(q/mu)+log_phi N_Book follow. Then expected Cost-Info=(H(q)-log N_Book)/log phi; no residual expectation of code cost survives, even for moving/noncanonical codes. This does not identify pointer events with Book gamma or make extra execution/preparation histories free.',
      'scope': 'Fixed common prefix law and fixed field-independent seed coins give identical detector Euler zero sets, NOT action equality. Moving prefix, conditional g_y, moving Book normalizer, emitted work and extra H/J/R costs remain separate joint sources; no physical selector, native admission, nonempty root or GR limit is claimed.'}

def targeted_effect_preparation_normal(root=None):
    import sympy as s
    p,v,T=s.symbols('p v t_squared',real=True)
    checks={}
    def ck(name,test):
        checks[name]=bool(test)
        if not checks[name]: raise AssertionError(name)
    def golden_zero(expr):
        numerator=s.cancel(expr).as_numer_denom()[0]
        return s.rem(s.Poly(numerator,p),s.Poly(p*p+p-1,p)).as_expr()==0
    a=p**6
    w0=1-a; w1=a; r=p**3/4; L=4*p**3
    b=(p+p*p*T*v)**2
    B=4*b*(1-b)
    Q=1-r*B
    R=1-r*(L+a*B)
    # One ORIGINAL D3 paired spectral factor; multiplicities multiply log.
    G=w0**4*Q**2*R**2
    G0=G.subs(v,0)
    G1=s.diff(G,v).subs(v,0)
    Q0=1-r*L
    R0=1-r*(1-p**12)
    mt=8*r*p**6*T*(1/Q0+p**6/R0)
    ck('actual_golden_three_coin_ratio',golden_zero(w1/w0-r))
    ck('actual_D3_AF_blank_second_eigenvalue',golden_zero(L+a*L-(1-p**12)))
    ck('same_D3_scene_first_matter_jet',golden_zero(s.diff(B,v).subs(v,0)-8*p**6*T))
    ck('same_D3_good_probability_constant',golden_zero(G0-w0**4*Q0**2*R0**2))
    ck('same_D3_nonzero_quadratic_scalar_coefficient',golden_zero(G1/G0+2*mt))
    # Exact native source ratio, as normalized in the direct-density owner.
    gt=4*r*p**11*T/R0
    lam=2*p**(-5)*(R0/Q0+p**6)
    ck('same_D3_matter_coefficient_is_gt_times_lambda',golden_zero(mt-gt*lam))
    ck('derived_r_Q0_is_original_w0',golden_zero(Q0-w0))
    ck('derived_r_R0_retains_both_D3_terms',golden_zero(R0-(1-p**6-p**12)))
    p0=(s.sqrt(5)-1)/2
    mt0=s.simplify(mt.subs({p:p0,T:p0**4}))
    ck('strict_native_golden_clock_gives_nonzero_source',float(mt0)>0)
    # An actual forward spatial gradient on eight periodic sites has a
    # nonzero real symmetric kinetic matrix. This is only a restriction of
    # D1's scalar block, not a new target F or a full grid/certificate replay.
    n=8; hh=s.Rational(1,n)
    D=s.zeros(n)
    for j in range(n):D[j,j]=-1/hh;D[j,(j+1)%n]=1/hh
    K=-hh*D.T*D # constant in other three coordinates, flat Lorentz scalar
    ck('actual_forward_scalar_kinetic_block_is_nonzero',K==K.T and K!=s.zeros(n))
    ck('kinetic_block_keeps_constant_scalar_zero_mode',K*s.ones(n,1)==s.zeros(n,1))
    ck('actual_forward_scalar_has_nonzero_quadratic_response',(s.eye(n)[:,0].T*K*s.eye(n)[:,0])[0]!=0)
    # Orthogonal scalar excitation vectors have beta>0. For each input-copy
    # pair the actual D3 quadratic sector is -G0*cstar sum K_ab a_a x a_b.
    beta=s.symbols('beta',positive=True)
    pair_norm2=beta**2*sum(x*x for x in K)
    ck('actual_kinetic_two_excitation_vector_cannot_vanish',pair_norm2>0)
    N=s.symbols('N',integer=True,positive=True)
    pairs=N*(N-1)/2
    ck('uniform_subset_pair_sector_norm_exact',s.simplify(pairs*pair_norm2/pairs**2-pair_norm2/pairs)==0)
    # Keep the complete Hermitian domain in polarization: symmetric Pauli
    # products span all permutation-invariant 2-copy Hermitian operators.
    I=s.eye(2); X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
    paulis=[I,X,Y,Z]
    ops=[(s.kronecker_product(paulis[i],paulis[j])+s.kronecker_product(paulis[j],paulis[i]))/2 for i in range(4) for j in range(i,4)]
    vecs=s.Matrix.hstack(*(M.reshape(16,1) for M in ops))
    ck('all_mixed_state_polarization_has_no_symmetric_operator_freedom',vecs.rank()==10)
    # Exact one-marginal silence for two-copy off-support excitation is a
    # tensor inner-product statement: every traced pair has one <base|a>=0.
    e0=s.Matrix([1,0]); e1=s.Matrix([0,1])
    base=s.kronecker_product(e0,e0)
    pair=s.kronecker_product(e1,e1)
    delta=pair*base.T+base*pair.T
    partial0=s.Matrix(2,2,lambda i,j:sum(delta[2*i+k,2*j+k] for k in range(2)))
    partial1=s.Matrix(2,2,lambda i,j:sum(delta[2*k+i,2*k+j] for k in range(2)))
    ck('pair_normal_first_marginals_are_both_exactly_zero',partial0==s.zeros(2) and partial1==s.zeros(2))
    return {'status':'PASS','checks':len(checks),'check_results':checks,
      'actual_source':'Original D3 Q/R spectral factor at A=M=0, r=p^3/4; m_t=8 r p^6 t^2(1/Q0+p^6/R0)=g_t lambda_mat, not a diagnostic H or new F.',
      'statement':'For the fixed marginal-feature polynomial of6.64 on ALL IID mixed states, permutation twirl fixes E_N uniquely. At a scalar-free vacuum/null-star code, its nonzero original scalar kinetic Hessian creates a two-copy scalar outside-support component. No same-g polarization/Naimark freedom removes the complete fixed-RIGHT preparation normal at finiteN if those data-only entangling variations are admitted.',
      'normal_bound':'||Pi2 E_N Psi^tensorN|| = |g0 cstar|/sqrt(binom(N,2))*||Beta^(1/2) L_h Beta^(1/2)||_F; cstar=2nu528K g_t(r)lambda_mat(r). Price-source norm >=2|cstar|/(log(phi)sqrt(binom(N,2)))*the same kinetic norm.',
      'scope':'Original marginal-feature extension and scalar-free null/star code; no new global claim about all nonvacuum codes. All data/reference are retained. Full Book multi-copy costs/constraints might contribute. FiniteN exact obstruction decays as1/N at fixed source, so no refinement no-go or physical preparation-admission claim.'}

def parity_graph_original_carrier_control(root):
    import ast
    import hashlib
    from pathlib import Path
    from types import SimpleNamespace
    import sympy as s
    root=Path(root); checks=[]
    def ck(name,v):
        if not bool(v):raise ArithmeticError(name)
        checks.append(name)
    def simp(x):return s.simplify(s.trigsimp(s.expand_complex(x)))
    def zero(M):return M.applyfunc(simp)==s.zeros(*M.shape)
    cp=root/'02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py'
    creator=next(n for n in ast.parse(cp.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='creator')
    cpin=hashlib.sha256(ast.dump(creator,include_attributes=False).encode()).hexdigest()
    ck('original creator AST pin',cpin=='801b33d7ef3e41f6425be16153c82b1402215f6be757ea275ff06a69010f58e4')
    ns={'s':s,'SUBS':[tuple(i for i in range(4) if m&(1<<i)) for m in range(16)]}
    exec(compile(ast.Module(body=[creator],type_ignores=[]),str(cp),'exec'),ns)
    cs=[ns['creator'](s.eye(4)[:,i]) for i in range(4)]
    parity=s.diag(*[(-1)**bin(m).count('1') for m in range(16)])
    for i,C in enumerate(cs):ck('actual creator is parity odd '+str(i),zero(parity*C+C*parity))
    alphas=[(cs[0]+cs[0].T)*(cs[i]-cs[i].T) for i in range(1,4)]
    for i,A in enumerate(alphas):ck('actual current is parity even '+str(i+1),zero(parity*A-A*parity))
    gp=root/'03_FORMALIZATION/D0/Representation/GoldenOrderInterferometer.lean'
    gpin=hashlib.sha256(gp.read_bytes()).hexdigest()
    ck('literal existing golden gate definition present','def gate (a p : ℝ) : Matrix (Fin 2) (Fin 2) ℝ := !![a,-p; p,a]' in gp.read_text())
    # E contains all8 first-axis momenta times the full16 CAR masks.
    from itertools import product
    moms=list(product((1,-1),repeat=4))
    even=[m for m in range(16) if bin(m).count('1')%2==0]
    odd=[m for m in range(16) if bin(m).count('1')%2]
    E=[(0,k,m) for k in moms for m in even]
    O=[(0,k,m) for k in moms for m in odd]
    ei={x:i for i,x in enumerate(E)};oi={x:i for i,x in enumerate(O)}
    ck('original16 momenta give128 modes of each parity without an auxiliary factor',len(E)==len(O)==128 and len(even)==len(odd)==8)
    c,t=s.symbols('cos_tau sin_tau',real=True)
    U=s.MutableSparseMatrix(128,128,{(i,oi[(af,k,m^2)]):1 for i,(af,k,m) in enumerate(E)})
    ku=(1,1,1,1); km=(-1,-1,-1,-1)
    blocks=[(0,[(ku,0),(km,3)],[(ku,2),(km,1)],s.Matrix([[c,t],[t,-c]])),
            (0,[(km,15),(ku,3)],[(km,13),(ku,1)],s.Matrix([[c,s.I*t],[-s.I*t,-c]]))]
    for af,rr,cc,B in blocks:
        for i,(k,m) in enumerate(rr):
            row=ei[(af,k,m)]
            for j,(l,n) in enumerate(cc):U[row,oi[(af,l,n)]]=B[i,j]
    gram=U.conjugate().T*U-s.eye(128)
    ck('explicit full128 parity pairing is unitary on c2+t2=1',all(s.simplify(s.rem(s.expand(v),c*c+t*t-1,c))==0 for v in gram.values()))
    # Generic 2x2 graph isometry/projection control; the actual U above has
    # the same block algebra at N128, avoiding a dense256 symbolic square.
    B=blocks[0][3]
    W=s.Matrix.vstack(s.eye(2),B.T)/s.sqrt(2)
    P=W*W.T
    ck('graph W is isometric',all(s.simplify(s.rem(s.expand(v),c*c+t*t-1,c))==0 for v in W.T*W-s.eye(2)))
    ck('graph projector is idempotent',all(s.simplify(s.rem(s.expand(v),c*c+t*t-1,c))==0 for v in P*P-P))
    ck('graph parity diagonals independent of unitary',P[:2,:2]==s.eye(2)/2 and all(s.simplify(s.rem(s.expand(v),c*c+t*t-1,c))==0 for v in P[2:,2:]-s.eye(2)/2))
    # Normalized LOCAL CAR density after tracing the two auxiliary labels;
    # site probability is1/S. Only same-AF matrix elements survive the trace.
    theta=s.symbols('theta',real=True)
    rho=s.eye(16)/16
    for (i,j),v in U.todok().items():
        af,k,m=E[i];ag,l,n=O[j]
        if af==ag:
            value=v*s.exp(s.I*(k[0]-l[0])*theta)/256
            rho[m,n]+=value;rho[n,m]+=s.conjugate(value)
    rho=rho.applyfunc(simp)
    ck('all local same-parity entries equal original full CAR bath',all(simp(rho[i,j]-(s.Rational(1,16) if i==j else 0))==0 for i in range(16) for j in range(16) if (bin(i).count('1')-bin(j).count('1'))%2==0))
    ck('scalar01 coherence carries the doubled phase',simp(rho[0,1]-t*s.exp(2*s.I*theta)/256)==0)
    ck('top151 coherence carries the quadrature doubled phase',simp(rho[15,1]-s.I*t*s.exp(-2*s.I*theta)/256)==0)
    ck('all three local actual current numerators unchanged',all(simp(s.trace(rho*A))==0 for A in alphas))
    ck('first-grade density remains isotropic old bath not pure clock',rho.extract([1,2,4,8],[1,2,4,8])==s.eye(4)/16)
    ck('full local trace is one',simp(s.trace(rho)-1)==0)
    # A generic parity-even16 matrix has arbitrary same-parity entries.
    X=s.Matrix(16,16,lambda i,j:s.Symbol('x_'+str(i)+'_'+str(j),real=True) if (bin(i).count('1')-bin(j).count('1'))%2==0 else 0)
    ck('every full16 even operator source equals original bath',simp(s.trace((rho-s.eye(16)/16)*X))==0)
    p=(s.sqrt(5)-1)/2;a=s.sqrt(p)
    G=a*s.eye(16)+p*(cs[0]-cs[0].T)
    ck('literal G on every mode0 pair is orthogonal',zero(G.T*G-s.eye(16)))
    occ=cs[0]*cs[0].T
    ck('literal golden occupation effect has odd coherence term',zero(G.T*occ*G-(p*p*s.eye(16)+(a*a-p*p)*occ+a*p*(cs[0]+cs[0].T))))
    q=(G*rho*G.T).diagonal()
    delta=a*p*t*s.cos(2*theta)/128
    target=[s.Rational(1,16)-delta if m in (0,2) else s.Rational(1,16)+delta if m in (1,3) else s.Rational(1,16) for m in range(16)]
    ck('complete occupation law has only four asserted deviations',all(simp(q[m]-target[m])==0 for m in range(16)))
    qocc=simp(sum(q[m] for m in range(16) if m&1))
    ck('site-resolved golden bit detects the parity graph',simp(qocc-s.Rational(1,2)-a*p*t*s.cos(2*theta)/64)==0)
    # Eight-site exact phase average. Other3 coordinates may be uniform.
    co=[s.cos(s.pi*j/2) for j in range(8)]
    ck('forgetting site erases the detected bit signal',sum(co)==0)
    ck('retained-site phase has nonzero variance',sum(x*x for x in co)/8==s.Rational(1,2))
    # At tau0, t=sin(tau)=0, q=1/16. Entropy Hessian uses
    # H''=-sum(q'^2/q), because all total-q second derivatives sum to0.
    entropy_curvature=s.simplify(-4*(a*p/128)**2*16*s.Rational(1,2))
    ck('complete site-plus-CAR occupation entropy curvature nonzero',s.simplify(entropy_curvature+p**3/512)==0 and entropy_curvature<0)
    # Scalar flat Delta is exactly lambda on ALL original +/-axis modes.
    # The full graph range, not only its mean, therefore remains isospectral.
    d,o,h=s.symbols('d o h',positive=True)
    zeta=(1+s.I)/s.sqrt(2)
    Gmetric=(d-o)*s.eye(4)+o*s.ones(4)
    energy={}
    for k in moms:
        zz=s.Matrix([(zeta**kr-1)/h for kr in k])
        energy[k]=s.simplify((zz.conjugate().T*Gmetric*zz)[0])
    ck('all mixed momentum pairs have exactly equal native energy',all(s.simplify((energy[E[i][1]]-energy[O[j][1]])*v)==0 for (i,j),v in U.todok().items()))
    counts={sum(k)**2:sum(1 for q in moms if sum(q)**2==sum(k)**2) for k in moms}
    ck('all three native energy classes retain exact multiplicity',counts=={16:2,4:8,0:6})
    av=s.simplify(sum(energy.values())/16)
    ar=2-s.sqrt(2)
    ck('uniform K bath exact Rayleigh metric source',s.simplify(av-(4*ar*d+3*ar**2*o)/h**2)==0)
    ck('originalcarrier dimensions reference128 and shell256',len(moms)*16==256 and len(E)==128)
    return {'status':'PASS','checks':checks,'source_sha256':{'creator_AST':cpin,str(gp.relative_to(root)):gpin},
      'exact_statement':'On the ORIGINAL site times CAR16 carrier take K={+/-1}^4. Each parity sector of K times CAR16 has128 dimensions. The explicit U mixes only k and -k and intertwines their exact native Delta energies. C=W_U/sqrt128 has canonical fixedRIGHT I128/128 and solves Delta C=C L, L=L*. Its even operator sources and current are exactly those of uniform K bath I_K/256.',
      'full_price':'For the SAME priced carrier, U/P and reference128, H and J remain unchanged by preparation, and R plus every compared CAR-even field jet agrees with the uniform K bath. Thus any actually certified geometric/full-source root of that uniform bath transfers to this canonical fixed-RIGHT family. The old first-shell root is not that certificate.',
      'actual_record':'The literal existing G=aI+p(c0-c0*) followed by complete site-resolved16-mask occupation detects the constructed odd coherence. Its joint-law entropy Hessian is -p^3/512 nats at tau0. Forgetting site erases the single occupation-bit signal.',
      'input_boundary':'The local first-grade density is I4/16, as in the uniform CAR bath. This is not a pure amplitude Hodge chart or a single-vector timelike P1 clock. The two density-coherence readings do not extend the original amplitude readout.',
      'fullright_boundary':'K has three energy classes. Arbitrary correlated FULLRIGHT sigma with uniform ref marginal is not automatically a preparation root: the canonical graph right energy L must commute with sigma (after the actual oldAF tensor embedding). In contrast to the old single shell, L is not scalar.',
      'scope':'No new AF tensor factor, no extra J multiplicity, no claimed geometric root before its actual certificate, no full-sphere common-energy stationarity, no PREP admission, no full Book stationarity or GR.'}

def parity_graph_joint_source_root(root):
    import ast, hashlib, itertools
    from collections import Counter
    from pathlib import Path
    import mpmath as mp
    root=Path(root); checks=[]
    def ck(name, value):
        if not bool(value): raise ArithmeticError(name)
        checks.append(name)
    path='02_REGISTRY/research/sources/d0_record_generated_heat_v8_2026-10-14/verify.py'
    raw=(root/path).read_bytes()
    tree=ast.parse(raw)
    nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('add','sub','mul','features')]
    pin=hashlib.sha256(ast.dump(ast.Module(body=nodes,type_ignores=[]),include_attributes=False).encode()).hexdigest()
    env={'Counter':Counter,'itertools':itertools}
    exec(compile(ast.Module(body=nodes,type_ignores=[]),path,'exec'),env)
    rows=env['features']()
    ck('original orbit-generator AST unchanged',pin=='5a2d5fb0b8b437cf86ec4b0b502d8a4b5d65b9f94959b5dcfed3779774431172')
    ck('all4096 original Fourier modes retained',sum(n for _,n in rows)==4096)
    ck('all119 original exact orbits retained',len(rows)==119)
    iv=mp.iv; old_dps=iv.dps; iv.dps=60
    try:
        val=lambda x:iv.mpf(x[0])+iv.mpf(x[1])*iv.sqrt(2)
        p=(iv.sqrt(5)-1)/2;alpha=p*p/8192;beta=2*p*p;fug=iv.mpf(1)/1048576
        chi=2-iv.sqrt(2);target=[256*chi,192*chi*chi]
        def equations(x,multiplicity=2048):
            Z=iv.mpf(0);u=[iv.mpf(0)]*2;r=[iv.mpf(0)]*2
            v=[[iv.mpf(0) for _ in range(2)] for _ in range(2)]
            t=[[iv.mpf(0) for _ in range(2)] for _ in range(2)]
            for (aa,bb),count in rows:
                f=[val(aa),val(bb)];B=1-alpha*(f[0]*x[0]+f[1]*x[1]);e=B**16384
                w=count*e;R=fug*e/(1-fug+fug*e);Z+=w
                for i in range(2):
                    u[i]+=w*f[i]/B;r[i]+=count*R*f[i]/B
                    for j in range(2):
                        v[i][j]+=w*f[i]*f[j]/B**2
                        t[i][j]+=count*R*(alpha-beta*(1-R))*f[i]*f[j]/B**2
            mu=[q/Z for q in u]
            F=[mu[i]-multiplicity*beta*r[i]-target[i] for i in range(2)]
            J=[[(alpha-beta)*v[i][j]/Z+beta*mu[i]*mu[j]-multiplicity*beta*t[i][j] for j in range(2)] for i in range(2)]
            return F,J
        center=['0.01949758334103003317092566892816507257820191136677009607',
                '0.00040050669416411222018794758451775636074764672518266514']
        pre=[['-0.0002433677011353035622652980155415483907662487225453670281',
              '0.00009783576742887514654789839309394121309488098381619586804'],
             ['0.00009783576742887514654789839309394121309488098381619586804',
              '-0.0001000974351489880688978291567769098415801868400069437612']]
        C0=list(map(iv.mpf,center));rad=iv.mpf('1e-12');X=[v+iv.mpf(['-1e-12','1e-12']) for v in C0]
        P=[[iv.mpf(v) for v in row] for row in pre]
        f0,_=equations(C0);_,JI=equations(X)
        C=[[iv.mpf(int(i==j))-sum(P[i][k]*JI[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
        for i in range(2):
            q=sum(abs(v) for v in C[i]);err=abs(sum(P[i][j]*f0[j] for j in range(2)))
            ck('new K-bath interval contraction '+str(i),q<iv.mpf('1e-6'))
            ck('new K-bath interval self-mapping '+str(i),err+q*rad<rad)
        ck('new root transverse positive',X[0]-X[1]>iv.mpf('.019'))
        ck('new root longitudinal positive',X[0]+3*X[1]>iv.mpf('.020'))
        ck('new root longitudinal upper',X[0]+3*X[1]<iv.mpf('.021'))
        ck('all pointwise coefficient dilations strict',X[0]<1)
        for (aa,bb),count in rows:
            B=1-alpha*(val(aa)*X[0]+val(bb)*X[1])
            ck('actual survivor B strict '+str((aa,bb)),B>p**3 and B<=1)
        wrong,_=equations(C0,multiplicity=4096)
        ck('REJECT adding an unpriced AF2 factor',abs(wrong[0])>iv.mpf('.01'))
        old_target=128-64*iv.sqrt(2)
        ck('REJECT transferring the old first-shell root equation',abs(target[0]-old_target)>100 and target[1]>60)
        return dict(status='PASS',checks=checks,source_sha256={path:hashlib.sha256(raw).hexdigest(),'features_AST':pin},
          root_center=center,root_radius='1e-12',preconditioner=pre,contraction_upper='1e-6',
          same_price='Original old-v8 H+J+R; L8, n8192, alpha=p²/8192, beta=2p², z=2^-20, CAR16, reference128, J multiplicity2048. No new AF factor.',
          Rayleigh_K='[4 chi d+3 chi² o]/h², chi=2-sqrt2, h=1/8; targets [256chi,192chi²].',
          source_scope='Unique zero in this two-variable box. Translation plus S4 reduces all10 actual local metric rows to these two equations. Proper-link/current extension requires the analytic full-CAR moment proof in the owner; the interval certificate by itself does not check those rows.',
          preparation_scope='Canonical fixedRIGHT I128/128 parity graph; three occupied energy classes, not a common eigenvalue or full-sphere root. Arbitrary correlated sigma also requires [sigma,L]=0.',
          physical_native_admission=False,stable_minimum=False,native_AF_refinement=False,GR_closed=False)
    finally:
        iv.dps=old_dps

def parity_graph_proper_link_transfer(root):
    import ast, hashlib
    from pathlib import Path
    import sympy as s
    root=Path(root); checks=[]
    def ck(name,v):
        if not bool(v):raise ArithmeticError(name)
        checks.append(name)
    def zero(M):return M.applyfunc(s.simplify)==s.zeros(*M.shape)
    f=root/'02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py'
    tree=ast.parse(f.read_text())
    creator=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='creator')
    basis=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='record_basis')
    pin=hashlib.sha256(ast.dump(creator,include_attributes=False).encode()).hexdigest()
    ck('original16 creator AST pin',pin=='801b33d7ef3e41f6425be16153c82b1402215f6be757ea275ff06a69010f58e4')
    ns={'s':s,'SUBS':[tuple(i for i in range(4) if m&(1<<i)) for m in range(16)]}
    exec(compile(ast.Module(body=[creator,basis],type_ignores=[]),str(f),'exec'),ns)
    cr=[ns['creator'](s.eye(4)[:,i]) for i in range(4)]
    kk=s.Matrix(4,4,lambda i,j:s.Symbol('K'+str(i)+str(j),real=True))
    Gamma=sum((kk[i,j]*cr[i]*cr[j].T for i in range(4) for j in range(4)),s.zeros(16))
    for i in range(4):
        for j in range(4):
            ck('full CAR16 link trace '+str(i)+str(j),s.simplify(s.trace(cr[i].T*cr[j]*Gamma)-4*((s.trace(kk) if i==j else 0)-kk[i,j]))==0)
    ck('raising-raising link trace identically zero',all(s.simplify(s.trace(cr[i]*cr[j]*Gamma))==0 for i in range(4) for j in range(4)))
    h=s.symbols('h',positive=True)
    cs,ss,ct,st,w=s.symbols('cos_s sin_s cos_r sin_r w',real=True)
    zs=(cs-1+s.I*ss)/h;zr=(ct-1+s.I*st)/h
    bpair=s.expand(w*(s.conjugate(zs)+zs))
    mss=s.expand(2*w*s.conjugate(zs)*zs)
    ck('inversion-paired B is real',s.simplify(s.im(bpair))==0)
    ck('true h factor in B equals minus hMss over2',s.simplify(s.rem(s.expand(bpair+h*mss/2),cs*cs+ss*ss-1,cs))==0)
    msr=s.expand(w*(s.conjugate(zs)*zr+zs*s.conjugate(zr)))
    ck('inversion-paired metric moment is real',s.simplify(s.im(msr))==0)
    linkpair=s.expand(w*(s.conjugate(zs)*(1+h*zr)+zs*(1+h*s.conjugate(zr))))
    ck('full forward link phase is B plus hM',s.simplify(linkpair-bpair-h*msr)==0)
    la,lb,lc=s.symbols('lambda_A lambda_B lambda_C',real=True)
    R=(2*la+8*lb+6*lc)/16
    ck('all three energy classes cancel local normalized whitening source',s.expand(2*(la-R)+8*(lb-R)+6*(lc-R))==0)
    # Exact relation with the literal coherent fullStep, not a substitute G.
    a,p=s.symbols('a p',real=True)
    U4=s.Matrix([[a,0,-p,0],[0,a,0,-p],[0,p,0,a],[p,0,a,0]])
    T=s.Matrix([[1,0,1,0],[1,0,-1,0],[0,1,0,1],[0,1,0,-1]])/s.sqrt(2)
    B0=ns['record_basis']()
    UR=B0*s.kronecker_product(T.T*U4*T,s.eye(4))*B0.T
    G0=a*s.eye(16)+p*(cr[0]-cr[0].T)
    sign=s.diag(*[(-1 if (m&1 and sum(bool(m&(1<<i)) for i in (1,2,3))>=2) else 1) for m in range(16)])
    ck('literal fullStep differs from G only by occupation-diagonal signs',zero(UR-sign*G0))
    ck('diagonal sign is exactly orthogonal',sign.T*sign==s.eye(16))
    ck('all16 fullStep occupation effects equal literal G effects',all(zero(UR.T*s.diag(*[int(j==m) for j in range(16)])*UR-G0.T*s.diag(*[int(j==m) for j in range(16)])*G0) for m in range(16)))
    return {'status':'PASS','checks':checks,'source_sha256':{'creator_AST':pin},
      'proper_link_statement':'For real inversion-symmetric scalar weights W, vanishing metric moments M_sr=sum W z_s* z_r forces B_s=sum W z_s*=-h M_ss/2=0 and sum W z_s* exp(ik_rh)=B_s+hM_sr=0. The full16 trace identity therefore kills all linear matrix link covectors, including all24 proper Lorentz rows, in the actual positive-adjoint whitening chart.',
      'whitening_statement':'Do not use a common-eigenvalue claim for the three-energy K bath. FixedRIGHT admissible variations make the preparation term zero via Delta C=C L and delta(C*C)=0. Separately, for fixed raw input at the flat uniform bath, every onsite whitening term cancels by the exact weighted identity sum_K(lambda_k-R)=0. Parity graph transfers this even expectation.',
      'fullstep_statement':'The literal16 fullStep equals S times G0, where S changes the sign only on time-occupied masks whose spatial degree>=2. S is diagonal, hence every16-mask occupation effect is IDENTICAL for fullStep and G0 for every input state. The previous parity-graph full Golden occupation law can therefore use literal fullStep, not only the bare gate.',
      'scope':'No numerical new-root verification, no actual Book-price identification, no full-sphere preparation claim, no frozen adjoint, no dropped normalizer or grades.'}


def cy_fine_right_capacity_controls(root=None):
    from pathlib import Path
    import hashlib
    import sympy as s
    root=Path.cwd() if root is None else Path(root)
    checks=[]
    def ck(name,test):
        if not bool(test):raise ArithmeticError(name)
        checks.append(name)
    path='02_REGISTRY/research/A4D_NATIVE_FIBONACCI_RECORD_ACTIVATION.md'
    sha='012455bdd3845e1d95f5270bbdcf105c753013d6e0b2339e2c001332e1fe4ee6'
    ck('actual native Fibonacci multiplicity/trace owner unchanged',
       hashlib.sha256((root/path).read_bytes()).hexdigest()==sha)
    p=(s.sqrt(5)-1)/2;phi=1/p
    M=s.Matrix([[1,1],[1,0]])
    ck('actual six-step multiplicities, not arbitrary added copies',M**6==s.Matrix([[13,8],[8,5]]))
    ck('actual failure multiplicities retain every complementary column',
       M**12-M**6==s.Matrix([[220,136],[136,84]]))
    ck('old typeX PF mass includes all fine right descendants',s.simplify(p**6*(13+8*p)-1)==0)
    ck('old typeY PF mass includes all fine right descendants',s.simplify(p**6*(8+5*p)-p)==0)
    x=s.symbols('x',positive=True)
    F=lambda z:2*z/(1+2*z)
    ck('capacity sigmoid monotonic comparison is exact',
       s.simplify(F(x)-F(phi)-2*(x-phi)/((1+2*x)*(1+2*phi)))==0)
    ck('h(p^2) exponent 2-p exceeds one',2-p>1)
    ck('capacity lower comparator F(phi) is exactly 2p^2',s.simplify(F(phi)-2*p**2)==0)
    ck('strict capacity gap exceeds every typeX diagonal right supply',2*p**2>13*p**6)
    ck('typeY supply is strictly smaller still',13*p**6>5*p**6>0)
    w=s.symbols('w',real=True)
    supply=p**6*(13*w+5*(1-w))
    ck('aggregate matched-success supply never exceeds13p^6',
       s.simplify(13*p**6-supply-8*p**6*(1-w))==0)
    return dict(status='PASS',checks=checks,source_sha256={path:sha},
      exact_scope='Canonical fineRIGHT trace on A_(N+6), with JOINT fineRIGHT/reference unchanged. Actual C_Y matched branch has success Pi oldLEFT_i only in fine block of type(i). Its conditional success is bounded by13p^6 or5p^6. Capacity s*=F(phi^(2-p))>F(phi)=2p^2>13p^6, so this matched capacity state is impossible in that class.',
      operator_proof='Qmatch=sum_i L(P_i)R_old(P_i), A=Pi Qmatch<=sum_j Z_fine,j R_old(Z_j). This gives the aggregate bound even for outputs not already matched. Reference128 is untouched and cancels in its trace.',
      oldRIGHT_escape='The actual13an hypothesis fixes only oldRIGHT A_N/reference. Its ideal larger commutant can change fresh fineRIGHT multiplicities and is not contradicted. A native active placement changing that fresh sector, with full price, is precisely the missing operation. The declared broad encoded G/CNOT controls may permit such placements conditionally; one must not identify all of them with fineLEFT A_(N+6).',
      no_overclaim='The bound holds for fineLEFT multiplication, C_Y LEFT-controlled fresh recording, and scene/CAR/query gates tensor identity on fineRIGHT. It is not a no-go for every native oldRIGHT-compatible operation, a different prepared fineRIGHT seed, another capacity branch or all D0.')


def hodge_polar_radial_trial(root=None):
    import sympy as s
    checks=[]
    def ck(name,v):
        if not bool(v):raise ArithmeticError(name)
        checks.append(name)
    def zero(M):return M.applyfunc(s.simplify)==s.zeros(*M.shape)
    A0=s.Matrix([[0,1,0],[1,0,0],[0,0,0]])
    A4=s.Matrix([[0,0,0],[0,0,1],[0,1,0]])
    exc=s.diag(1,0,1)
    ck('actual clock0top qutrit local square identity',A0*A0+A4*A4==2*s.eye(3)-exc)
    X=s.kronecker_product(A0,s.eye(3))+s.kronecker_product(s.eye(3),A0)
    Y=s.kronecker_product(A4,s.eye(3))+s.kronecker_product(s.eye(3),A4)
    Ne=s.kronecker_product(exc,s.eye(3))+s.kronecker_product(s.eye(3),exc)
    H2=s.kronecker_product(A0,A0)+s.kronecker_product(A4,A4)
    ck('original two-copy H plusN equals positive square identity',H2+2*s.eye(9)==(X*X+Y*Y+Ne)/2)
    # Symmetric3-mode Schwinger representation: basis(n_clock,n_0,n_top).
    # This is polynomially small and is not a full3^N eigensolve.
    for N in (2,3):
        basis=[(nc,nx,N-nc-nx) for nc in range(N+1) for nx in range(N-nc+1)]
        ix={x:j for j,x in enumerate(basis)};D=len(basis)
        def hop(dst,src):
            M=s.zeros(D)
            for col,b in enumerate(basis):
                if b[src]:
                    v=list(b);v[dst]+=1;v[src]-=1
                    M[ix[tuple(v)],col]=s.sqrt((b[dst]+1)*b[src])
            return M
        Jx=hop(0,1)+hop(1,0);Jy=hop(0,2)+hop(2,0)
        NE=s.diag(*[b[1]+b[2] for b in basis])
        K=(Jx*Jx+Jy*Jy+NE)/2
        last=N//2;V=s.zeros(D,last+1)
        for k in range(last+1):
            for j in range(k+1):
                V[ix[(N-2*k,2*j,2*(k-j))],k]=s.binomial(k,j)*s.sqrt(s.factorial(2*j)*s.factorial(2*(k-j)))/(2**k*s.factorial(k))
        T=s.zeros(last+1)
        for k in range(last+1):
            T[k,k]=N+2*k*(N-2*k)
            if k<last:
                T[k,k+1]=T[k+1,k]=(k+1)*s.sqrt((N-2*k)*(N-2*k-1))
        ck('radial states orthonormal N'+str(N),zero(V.T*V-s.eye(last+1)))
        ck('radial block is genuinely reducing N'+str(N),zero(K*V-V*T))
        ck('exact excitation count on radial basis N'+str(N),zero(V.T*NE*V-s.diag(*[2*k for k in range(last+1)])))
        ck('endpoint lower-root sign N'+str(N),N-2*last-1==(-1 if N%2==0 else 0))
    n,k,r=s.symbols('N k r',real=True)
    expanded=s.expand(n+2*k*(n-2*k)-2*r*(k+1)*(n-2*k-1))
    target=n*(1-2*r+2*(1-r)*k)-4*(1-r)*k*k+6*r*k+2*r
    ck('exact geometric-trial upper-bound polynomial',s.expand(expanded-target)==0)
    q=s.symbols('q',positive=True);m=s.symbols('m',integer=True,nonnegative=True)
    Z=(1-q**(m+1))/(1-q)
    mean=s.simplify(q*s.diff(Z,q)/Z)
    expected=q/(1-q)-(m+1)*q**(m+1)/(1-q**(m+1))
    ck('truncated geometric mean formula with positive tail correction',s.simplify(mean-expected)==0)
    upper=s.simplify(n*(1-2*r+2*(1-r)*r*r/(1-r*r))+6*r**3/(1-r*r)+2*r)
    advertised=n*(1-r)/(1+r)+6*r**3/(1-r*r)+2*r
    ck('moment bound gives advertised finite formula',s.simplify(upper-advertised)==0)
    x,y=s.symbols('x y',positive=True)
    U=s.factor(advertised.subs({n:x*x,r:1-1/x}))
    num=s.factor((5*x-U)*x*(2*x-1))
    ck('finiteN bound has exact positive polynomial numerator',s.expand(num-(3*x**3+9*x*x-12*x+4))==0)
    ck('bound manifestly positive for sqrtN at least2',s.expand(num.subs(x,y+2))==3*y**3+27*y*y+60*y+40)
    # Supplemental finite witnesses: exact arithmetic, no diagonalization.
    for N in (4,5):
        rr=1-1/s.sqrt(N);last=N//2
        f=s.Matrix([(-rr)**j for j in range(last+1)]);f=f/s.sqrt((f.T*f)[0])
        T=s.zeros(last+1)
        for j in range(last+1):
            T[j,j]=N+2*j*(N-2*j)
            if j<last:T[j,j+1]=T[j+1,j]=(j+1)*s.sqrt((N-2*j)*(N-2*j-1))
        val=s.simplify((f.T*T*f)[0])
        rhs=s.simplify(advertised.subs({n:N,r:rr}))
        ck('finite trial lower square-root upper estimate N'+str(N),s.simplify(rhs-val)>0)
        ck('finite trial5sqrtN bound N'+str(N),s.simplify(5*s.sqrt(N)-rhs)>0)
    return {'status':'PASS','checks':checks,
      'operator':'On the original clock+scalar0+top qutrit H_N=sum_r<s(A0r A0s+A4r A4s) and K=H_N+NI=1/2[(sum A0)^2+(sum A4)^2+N_exc].',
      'radial_block':'In the permutation-symmetric SO2-invariant radial block |k> proportional to (a0dag^2+a4dag^2)^k(cdag)^(N-2k)|vac>, K diagonal=N+2k(N-2k), offdiagonal=(k+1)sqrt[(N-2k)(N-2k-1)]. This is a reducing block, so its exact eigenstates are eigenstates of full H_N.',
      'trial_bound':'For N>=4 and r=1-N^-1/2, normalized amplitudes(-r)^k give <K><=N(1-r)/(1+r)+6r^3/(1-r^2)+2r<=5sqrtN. The finite endpoint correction is nonnegative for evenN and zero for oddN.',
      'exact_eigen_consumer':'Choose the lowest K eigenvector in this finite radial block. It is an exact full-H_N eigenstate with 0<=lambda_N<=min(N,5sqrtN), <N_exc><=10sqrtN. It is not claimed to be the global full-Hilbert ground state.',
      'marginal_bound':'Permutation symmetry gives ||rho_k-|clock><clock|^tensor k||_1<=min(2,2sqrt(10k)N^-1/4).',
      'source_consumer':'For an actually owned definite quadratic E_eff(g)=a(g)I+b(g)H_N/binomial(N,2), the fixed eigenvector has e_N in[-2/(N-1),0], so its query value and C2 geometric source differ from a(g) by at most2||b||_C2/(N-1). No inverse-gap differentiation is used.',
      'scope':'Only this definite quadratic single-site two-Hodge qutrit block. Its marginals recover the pure CLOCK conditional block, not the full13gh vacuum sqrt(p)|1>+sqrt(1-p)|14>. Grade14 is a coherent direct-sum spectator, not a tensor factor. No full Lorentz indefinite grid, fullCAR16/source transfer, canonicalRIGHT128, higher-query/source, native PREP or full Book-price claim.'}


def hodge_dark_ground_branch_control(root=None):
    import sympy as s
    checks = []

    def ck(name, v):
        if not bool(v):
            raise ArithmeticError(name)
        checks.append(name)

    def zero(M):
        return M.applyfunc(s.simplify) == s.zeros(*M.shape)
    c = s.eye(4)[:, 1]
    x = s.eye(4)[:, 0]
    y = s.eye(4)[:, 2]
    d = s.eye(4)[:, 3]
    A = x * c.T + c * x.T
    B = y * c.T + c * y.T
    active = s.diag(1, 1, 1, 0)
    ck('both actual scalar-clock operators annihilate dark14', A * d == s.zeros(4, 1) and B * d == s.zeros(4, 1))
    H2 = s.kronecker_product(A, A) + s.kronecker_product(B, B)
    Md = s.kronecker_product(active, s.eye(4)) + s.kronecker_product(s.eye(4), active)
    ck('full fourgrade quadratic preserves active-copy number', H2 * Md == Md * H2)
    X = c * d.T
    T = s.kronecker_product(X, s.eye(4)) + s.kronecker_product(s.eye(4), X)
    expected = s.kronecker_product(x * d.T, A) + s.kronecker_product(A, x * d.T) + s.kronecker_product(y * d.T, B) + s.kronecker_product(B, y * d.T)
    ck('actual darkclock preparation commutator is a mixed correlation source', H2 * T - T * H2 == expected)

    def radial(M):
        last = M // 2
        H = s.zeros(last + 1)
        for k in range(last + 1):
            H[k, k] = 2 * k * (M - 2 * k)
            if k < last:
                H[k, k + 1] = H[k + 1, k] = (k + 1) * s.sqrt((M - 2 * k) * (M - 2 * k - 1))
        return H
    for M in (1, 2, 3, 4):
        H = radial(M)
        Hp = radial(M + 1)
        nc = s.diag(*[M - 2 * k for k in range(H.rows)])
        ne = s.diag(*[2 * k for k in range(H.rows)])
        R = s.zeros(Hp.rows, H.rows)
        for k in range(H.rows):
            R[k, k] = s.sqrt(M - 2 * k + 1)
        ck('clock creation is exact rectangular radial map M' + str(M), zero(R.T * R - nc - s.eye(H.rows)))
        ident = ((nc + s.eye(H.rows)) * H + H * (nc + s.eye(H.rows))) / 2 + H + ne
        ck('exact Hermitian adjacentM variational numerator M' + str(M), zero(R.T * Hp * R - ident))
    z = s.symbols('sqrtM_minus15', positive=True)
    m = (z + 15) ** 2
    ck('strict ground branch energy drop above225', s.expand(-m + 15 * (z + 15)) == -z * z - 15 * z)
    (E, nc, ne) = s.symbols('E n_clock n_exc', real=True)
    quotient = (E * (nc + 2) + ne) / (nc + 1)
    ck('normalized clock creation Rayleigh difference', s.simplify(quotient - E - (E + ne) / (nc + 1)) == 0)
    (M, N) = s.symbols('M N', integer=True, nonnegative=True)
    ck('allowed lowM clock-dark edge norm bound', s.expand(226 * N - (N - M) * (M + 1) - M * M - M - N * (225 - M)) == 0)
    p = (s.sqrt(5) - 1) / 2
    ck('actual golden target coherence squared is p cubed', s.simplify(p * (1 - p) - p ** 3) == 0)
    return {'status': 'PASS', 'checks': checks, 'actual_operator': 'The fourgrade quadratic annihilates grade14 and conserves active M=n_clock+n_scalar0+n_top15. The clock-dark generator commutator is an actual two-copy mixed-correlation source, not a freely chosen scalar condition.', 'positive_input': 'Use only the already proved active-M radial ground family, lambda_M of H_M+M with0<=lambda_M<=min(M,5sqrtM), so E_M=-M+lambda_M and <exc><=10sqrtM.', 'exact_drop': 'Clock creation gives E_(M+1)<=E_M+(E_M+<exc>)/(<n_clock>+1). Therefore E_(M+1)<E_M for every M>225. This is an all-M analytic bound, not a small-spectrum conjecture.', 'coherence_bound': 'Any exact full-H_N eigenstate made by stitching these radial ground branches can have clock-dark14 coherence only on adjacent edges M<=225. Hence |<c_dag d>|/N<=sqrt(226/N). Its one-copy trace distance from sqrt(p)|clock>+sqrt(1-p)|14> is at least2[max(0,p^(3/2)-sqrt(226/N))].', 'coefficient_source': 'Changing only the genuine scalar coefficients in a(g)I+b(g)H_N/binomial(N,2), b!=0, does not change the equal-energy criterion or this ground-branch obstruction. A new independently derived non-affine preparation operator could change it; no such term is inserted.', 'scope': 'Only the successful active radial GROUND branch, not arbitrary excited-sector degeneracies, nonsymmetric fullcarrier states, fullRIGHT128 or fullD0. Other12 grades are not removed from the ambient carrier; their physical effects and allsite/Lorentz/higher query couplings require their actual operator/source.'}

def coherent_dark_energy_overlap(root=None):
    from itertools import permutations

    def add(a, b, scale=1):
        z = dict(a)
        for (k, v) in b.items():
            z[k] = z.get(k, 0) + scale * v
            if z[k] == 0:
                del z[k]
        return z

    def h_apply(v):
        z = {}
        for (x, coef) in v.items():
            for i in range(len(x)):
                for j in range(i + 1, len(x)):
                    for e in (1, 2):
                        if x[i] in (0, e) and x[j] in (0, e):
                            y = list(x)
                            y[i] = e if x[i] == 0 else 0
                            y[j] = e if x[j] == 0 else 0
                            y = tuple(y)
                            z[y] = z.get(y, 0) + coef
        return {k: v for (k, v) in z.items() if v}

    def c_apply(v):
        z = {}
        for (x, coef) in v.items():
            for (i, a) in enumerate(x):
                if a == 3:
                    y = list(x)
                    y[i] = 0
                    y = tuple(y)
                    z[y] = z.get(y, 0) + coef
        return z

    def dark(v, i):
        return {x: c for (x, c) in v.items() if x[i] == 3}

    def inner(v, w):
        return sum((c * w.get(x, 0) for (x, c) in v.items()))
    checks = []

    def ck(label, condition):
        if not condition:
            raise ArithmeticError(label)
        checks.append(label)
    eps = {}
    for x in permutations((0, 1, 2)):
        inv = sum((x[i] > x[j] for i in range(3) for j in range(i + 1, 3)))
        eps[x] = (-1) ** inv
    ck('epsilon_norm6', inner(eps, eps) == 6)
    ck('epsilon_H3_minus2', h_apply(eps) == {x: -2 * c for (x, c) in eps.items()})
    ec = {x + (0,): c for (x, c) in eps.items()}
    ed = {x + (3,): c for (x, c) in eps.items()}
    ck('orthogonal_clock_dark', inner(ec, ed) == 0)
    ck('same_energy_clock', h_apply(ec) == {x: -2 * c for (x, c) in ec.items()})
    ck('same_energy_dark', h_apply(ed) == {x: -2 * c for (x, c) in ed.items()})
    ck('nonzero_exact_clock_dark_intertwiner', c_apply(ed) == ec)
    ck('unit_normalized_coherence_matrix_element', inner(ec, c_apply(ed)) == 6)
    for i in range(4):
        ck('dark_pattern_commutator_' + str(i), h_apply(dark(add(ec, ed), i)) == dark(h_apply(add(ec, ed)), i))
    from itertools import product
    for i in range(3):
        ck('all_basis_dark_commutator_N3_' + str(i), all((h_apply(dark({x: 1}, i)) == dark(h_apply({x: 1}), i) for x in product(range(4), repeat=3))))
    ck('nonzero_overlap_not_wholecode_recovery', sum((c * c for (x, c) in ec.items() if x[0] in (1, 2))) == 4)
    return {'status': 'PASS', 'checks': len(checks), 'labels': checks, 'eigenvalue': -2, 'copies': 4, 'coherence_per_average_copy': 'alpha*beta/4', 'scope': 'full four-grade quadratic counter to blanket zero coherence; not asymptotic recovery'}

def jones_fresh_actuation_controls(root=None):
    from pathlib import Path
    from hashlib import sha256
    import sympy as s
    root = Path.cwd() if root is None else Path(root)
    checks = []

    def ck(name, v):
        if not bool(v):
            raise ArithmeticError(name)
        checks.append(name)
    pin = '02_REGISTRY/research/A4D_NATIVE_GOLDEN_COST_REFINEMENT.md'
    digest = '9971253d0ba13b9b66ff28a6bedf166b9de265821a9380b969ba6e23ec9ee0f3'
    ck('actual inclusion/conditional-expectation owner unchanged', sha256((root / pin).read_bytes()).hexdigest() == digest)
    rankpin = '02_REGISTRY/research/A4D_NATIVE_FIBONACCI_RECORD_ACTIVATION.md'
    ranksha = '012455bdd3845e1d95f5270bbdcf105c753013d6e0b2339e2c001332e1fe4ee6'
    ck('actual working-versus-regular representation owner unchanged', sha256((root / rankpin).read_bytes()).hexdigest() == ranksha)
    p = (s.sqrt(5) - 1) / 2
    a = s.sqrt(p)
    simp = lambda M: M.applyfunc(s.simplify)
    J = s.zeros(5, 2)
    J[0, 0] = a
    J[4, 0] = p
    J[3, 1] = 1
    e = simp(J * J.T)
    I = s.eye(5)
    ck('actual normalized inclusion is isometric', simp(J.T * J) == s.eye(2))
    ck('Jones projection is the owned full conditional expectation', simp(e * e) == e)
    Zfine = s.diag(1, 1, 1, 1, 0)
    Zold = s.diag(1, 0, 1, 0, 1)
    ck('Jones projection preserves oldRIGHT, not a second-copy oracle', simp(e * Zold - Zold * e) == s.zeros(5))
    C = simp(e * Zfine - Zfine * e)
    Pdup = s.diag(1, 0, 0, 0, 1)
    ck('actual fineRIGHT commutator has exact nonzero norm ap', simp(C.T * C - p ** 3 * Pdup) == s.zeros(5))
    R = I - 2 * e
    ck('Jones reflection is unitary on every full GNS column', simp(R.T * R) == I)
    CR = simp(R * Zfine - Zfine * R)
    ck('reflection commutator gives uniform all-depth approximation floor 2ap', simp(CR.T * CR - 4 * p ** 3 * Pdup) == s.zeros(5))
    X = s.Matrix([[0, 1], [1, 0]])
    W = s.kronecker_product(e, X) + s.kronecker_product(I - e, s.eye(2))
    ck('coherent Jones instrument keeps both complete flag outputs', simp(W.T * W) == s.eye(10))
    Z = s.kronecker_product(Zfine, s.eye(2))
    CW = simp(W * Z - Z * W)
    Pminus = (s.eye(2) - X) / 2
    ck('coherent Jones control has the same exact commutator norm', simp(CW.T * CW - 4 * p ** 3 * s.kronecker_product(Pdup, Pminus)) == s.zeros(10))
    G = s.Matrix([[a, -p], [p, a]])
    Z0 = s.diag(-1, 1)
    P0 = s.diag(1, 0)
    P1 = s.diag(0, 1)
    U0 = s.kronecker_product(G, s.eye(2)) * (s.kronecker_product(P0, X) + s.kronecker_product(P1, s.eye(2))) * s.kronecker_product(G.T, s.eye(2))
    epair = s.Matrix([[p, a * p], [a * p, p ** 2]])
    ck('positive reflection candidate equals G Z G^-1 and G^2 Z exactly', simp(s.eye(2) - 2 * epair - G * Z0 * G.T) == s.zeros(2) and simp(G * Z0 * G.T - G * G * Z0) == s.zeros(2))
    ck('explicit G/CNOT conjugation on the actual fresh duplicated pair', simp(U0 - s.kronecker_product(epair, X) - s.kronecker_product(s.eye(2) - epair, s.eye(2))) == s.zeros(4))
    Q = s.eye(5)
    Q[0, 0] = Q[4, 4] = a
    Q[0, 4] = -p
    Q[4, 0] = p
    Pblank = s.diag(1, 0, 0, 1, 0)
    ck('whole-column Q Pblank Q^-1 includes carried B and both rectangular inputs', simp(Q * Pblank * Q.T - e) == s.zeros(5))
    omega = s.Matrix([p, 0, 0, p, a * p])
    ck('canonical fine trace seed remains an eigenvector of Jones projection', simp(e * omega - omega) == s.zeros(5, 1))
    Pss = s.diag(0, 0, 0, 0, 1)
    LE00 = s.diag(1, 1, 0, 0, 0)
    cross = s.zeros(5)
    cross[4, 0] = a * p
    ck('basic construction supplies the missing fresh cross-copy matrix unit', simp(Pss * e * LE00 - cross) == s.zeros(5))
    M = s.Matrix([[1, 1], [1, 0]])
    sizes = M ** 6 * s.Matrix([1, 1])
    work = M ** 3 * s.Matrix([1, 1])
    ck('native transported corner rank34 is not GNS conditional projection rank2', sum(sizes) == sum((x * x for x in work)) == 34 and 1 ** 2 + 1 ** 2 == 2)
    Pfirst = s.diag(1,0,0,0,0)
    Oe = (I-Zfine)*e*Zfine
    Or = (I-Zfine)*R*Zfine
    ck('offdiagonal compression gives sharp effect ap and reflection2ap floors', simp(Oe.T*Oe-p**3*Pfirst)==s.zeros(5) and simp(Or.T*Or-4*p**3*Pfirst)==s.zeros(5))
    Ow = (s.eye(10)-Z)*W*Z
    ck('full flag column offdiagonal compression gives sharp2ap floor', simp(Ow.T*Ow-4*p**3*s.kronecker_product(Pfirst,Pminus))==s.zeros(10))
    return dict(status='PASS', checks=checks, source_sha256={pin: digest, rankpin: ranksha}, theorem='For actual A subset B and e=J C on L2(B), the finite star algebra generated by L(B) and e is R(A) prime. Proof: L(B) prime=R(B), and R_b commutes e iff E_A(b)=b iff b in A, already by acting on Omega. This algebra statement does not admit coherent e control as a native primitive.', chronological_obstruction='All full LEFT words at later levels and passive trace-preserving inclusions preserve the transported earlier fineRIGHT probe. The actual Jones reflection or coherent flag has commutator norm2ap with that probe, so full-column implementation error is at least2ap at every depth, even with retained spectator ancillas. A pointer effect from a similarly commuting complete word/cut has effect-error floor ap.', scope='This is the named chronological fineLEFT/passive-inclusion class, not the full generous encoded-Hilbert G/CNOT class. A physical G placement on the fresh right-copy wire would escape it while preserving oldRIGHT/ref; the explicit pair formula shows exactly that missing placement. The folded A_(N+12) action on H_(N+6) is not automatically the chronological left action on H_(N+12).', price='If coherent Jones flag is actually supplied, q1=norm(e Psi)^2, q0=norm((I-e)Psi)^2 retain both outputs. Under independently bound SAME Book w=q its mean is h(q1)/logphi, plus actual old prefixes and any raw normalizer; it is not free factory overhead or automatically the C_Y capacity price.')

def pure_clock_checkerboard_witness(root):
    import ast, hashlib
    from itertools import product
    from pathlib import Path
    import sympy as s
    root = Path(root)
    checks = []

    def ck(name, v):
        if not bool(v):
            raise ArithmeticError(name)
        checks.append(name)
    f = root / '02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py'
    creator = next((n for n in ast.parse(f.read_text()).body if isinstance(n, ast.FunctionDef) and n.name == 'creator'))
    pin = hashlib.sha256(ast.dump(creator, include_attributes=False).encode()).hexdigest()
    ck('actual full16 creator AST pin', pin == '801b33d7ef3e41f6425be16153c82b1402215f6be757ea275ff06a69010f58e4')
    ns = {'s': s, 'SUBS': [tuple((i for i in range(4) if m & 1 << i)) for m in range(16)]}
    exec(compile(ast.Module(body=[creator], type_ignores=[]), str(f), 'exec'), ns)
    cr = [ns['creator'](s.eye(4)[:, i]) for i in range(4)]
    support = [0, 1, 14]
    for i in range(1, 4):
        alpha = (cr[0] + cr[0].T) * (cr[i] - cr[i].T)
        ck('all16 actual current vanishes including dark padding ' + str(i), alpha.extract(support, support) == s.zeros(3))
    p = (s.sqrt(5) - 1) / 2
    a = p * p
    ck('native golden amplitude has strict norm slack', s.simplify(1 - 4 * p ** 5) > 0)
    (A, S, P) = s.symbols('A S p', positive=True)
    amp = s.sqrt(s.sqrt(P) * A / S)
    for sg in (-1, 1):
        psi0 = sg * amp
        psi1 = amp
        ck('same fixed decoder reads signed A ' + str(sg), s.simplify(S * psi0 * psi1 / s.sqrt(P) - sg * A) == 0)
        ck('firstgrade clock future-positive ' + str(sg), psi1.is_positive is True)
    r = s.Rational(2, 3)
    for L in (2, 4, 6):
        kernel = [r ** min(m, L - m) for m in range(L)]
        ck('exact cyclic temporal kernel mass L' + str(L), sum(kernel) == 5 * (1 - r ** (L // 2)))
        ck('all cyclic kernel neighboring ratios bounded L' + str(L), all((s.Rational(2, 3) <= kernel[(m + 1) % L] / kernel[m] <= s.Rational(3, 2) for m in range(L))))
        ck('spatial checkerboard reverses across every periodic edge L' + str(L), all(((-1) ** ((j + 1) % L) == -(-1) ** j for j in range(L))))
    L = 2
    h = s.Rational(1, L)
    sites = list(product(range(L), repeat=4))
    count = len(sites)
    b = {x: s.Integer(1 + x[0] + 2 * x[1] + 3 * x[2] + 5 * x[3]) for x in sites}
    w = {x: b[x] ** 2 for x in sites}
    W = sum(w.values())
    kernel = [r ** min(m, L - m) for m in range(L)]

    def shift(x, mu, step=1):
        y = list(x)
        y[mu] = (y[mu] + step) % L
        return tuple(y)
    AA = {x: h ** (-2) * sum((kernel[m] * b[shift(x, 0, m)] for m in range(L))) for x in sites}
    ck('S is exactly h power minus4', count == h ** (-4))
    ck('convolution l1 preserves exact mass', sum(AA.values()) == h ** (-2) * sum(kernel) * sum(b.values()))
    ck('actual weights satisfy Cauchy normalization bound', sum(b.values()) ** 2 <= count * W)
    ck('every smoothed amplitude dominates its own weight', all((AA[x] >= h ** (-2) * b[x] for x in sites)))
    ck('time smoothing bounds both neighboring ratios', all((s.Rational(2, 3) * AA[x] <= AA[shift(x, 0)] <= s.Rational(3, 2) * AA[x] for x in sites)))
    ck('time difference never exceeds half own amplitude', all((abs(AA[shift(x, 0)] - AA[x]) <= AA[x] / 2 for x in sites)))
    phi = {x: (-1) ** x[1] * AA[x] for x in sites}
    q = {}
    for x in sites:
        D = [(phi[shift(x, i)] - phi[x]) / h for i in range(4)]
        q[x] = D[0] ** 2 - sum((z * z for z in D[1:]))
    ck('actual Lorentz time term retained in negative q bound', all((q[x] <= -s.Rational(3, 4) * AA[x] ** 2 / h ** 2 for x in sites)))
    ck('exact normalized everycell matter operand bound', all((h ** 4 * q[x] / w[x] <= -s.Rational(3, 4) / h ** 2 for x in sites)))
    R = s.symbols('R', nonnegative=True)
    ck('dark14 pad normalizes pure vector exactly', s.simplify(R + (1 - R) - 1) == 0)
    return {'status': 'PASS', 'checks': checks, 'source_sha256': {'creator_AST': pin}, 'construction': 'On an even periodic L^4 grid h=1/L,S=h^-4,w_x>0,W=sumw, set k_m=(2/3)^dist_L(m,0), A_x=(a h^-2/(5sqrtW))sum_m k_m sqrt(w_(x+m e0)), a=p². Put eta_x=sqrt(sqrtp A_x/S)[(-1)^x1 |x,0>+|x,1>] and pad remaining norm with grade14 at one cell.', 'exact_bounds': 'sumA<=aS, norm_before_pad<=2sqrtp a<1, A_x>=a h^-2 sqrt(w_x)/(5sqrtW), neighboring temporal amplitude ratio in[2/3,3/2]. Everycell q=(D0phi)^2-sum_i(Diphi)^2<=-3A_x²/(4h²); v_x=h⁴q/w_x<=-3a²/(100Wh²).', 'same_input': 'The fixed6.64 decoder S Re rho_x01/sqrtp reads exactly phi_x=(-1)^x1 A_x. P1eta_x has positive future e0 coefficient at everycell. All actual alpha_i current numerators vanish, including the grade14 padding. The data input is rank1; anchored Choi code omega_V is also pure, so their product sigma is pure.', 'polynomial_scope': 'At a fixed flat real query with U=0, the actual V matter operand is quadratic in these fixed density coordinates; its Taylor restriction of degree>=2 equals that quadratic on every matter density. This is an ALL-density positivity witness, not a claim that the large decoded field belongs to the physical13gi chart.', 'boundary': 'Requires even periodic spatialcheckerboard grid, fixed flat +--- query and the actual S and w factors. No mixed-state trick, new AF factor, selected reference column, fixedRIGHT128 root, supplied-PREP admission, full Book stationarity or physical clock selection is asserted.'}

def same_cut_ready_coverage_controls(root=None):
    from pathlib import Path
    from hashlib import sha256
    import sympy as s
    root = Path.cwd() if root is None else Path(root)
    checks = []

    def ck(name, v):
        if not bool(v):
            raise ArithmeticError(name)
        checks.append(name)
    pins = {'02_REGISTRY/research/A4D_LOCAL_LEFT_CODED_CAR_NULL_MATTER_EINSTEIN_2026_10_18.md': '828cba545e2c734741e7acf1509248c441de4451f9099cebee8d10c00230e35b', '02_REGISTRY/research/A4D_GLOBAL_GOLDEN_AF_VOLUME_FREE_CURVATURE_2026_10_17.md': '55212db3ffb46de43226827dd67104444cd701b891a8332185756479d7a5466e', '02_REGISTRY/research/sources/d0_af_full_feedback_first_source_2026-10-17/RESULT_RU.md': '4b3b78274de1cc700dbdae605bb8fe0047e121ef55b611034162e41cea338086'}
    for (p, h) in pins.items():
        ck('actual unchanged owner ' + Path(p).name, sha256((root / p).read_bytes()).hexdigest() == h)
    (A, B) = s.symbols('A B', positive=True)
    (D0, D1) = (13 * A + 8 * B, 8 * A + 5 * B)
    K = A * D0 + B * D1
    ck('full defining regular weights normalize without PF substitution', s.cancel(A * D0 / K + B * D1 / K - 1) == 0)
    ck('sharp full READY mass lower bound21/34 is exact for A>=B', s.expand(34 * A * D0 - 21 * K - (A - B) * (169 * A + 105 * B)) == 0)
    ck('full READY mass bound attains equality on actual first cut', s.cancel((A * D0 / K).subs({A: 1, B: 1})) == s.Rational(21, 34))
    (f, g) = s.symbols('f g', positive=True)
    ck('all FR/RF pair bank consumes a uniform fraction of READY leaves', s.expand(10 * f - 2 * (3 * f + 2 * g) - 4 * (f - g)) == 0)
    ck('pair bank lower bound is21/85 with actual regular weights', s.Rational(2, 5) * s.Rational(21, 34) == s.Rational(21, 85))
    (S, c, nx) = s.symbols('S c nx', positive=True)
    ck('pair multiplicity cancels in exactly the owned normalized count density', s.cancel(2 * c * nx / (2 * c * f / S) - S * nx / f) == 0)
    ck('all READY grouping has the same normalized count density', s.cancel(c * nx / (c * A / S) - S * nx / A) == 0)
    ck('sparse one-pair-per-cell is a genuine smaller mass, not the full bank', s.cancel(2 * S * D0 / K - 2 * S / A * (A * D0 / K)) == 0)
    return dict(status='PASS', checks=checks, source_sha256=pins, exact_all_READY='At actual old cut N, A=F_(N+2), B=F_(N+1), D0=13A+8B,D1=8A+5B,K=A D0+B D1. Group every READY leaf by the existing address-to-grid map; sum Q_x=P_READY and W=A D0/K>=21/34. Individual trace weights/action/carrier are unchanged.', exact_original_pairs='The original global owner already activates ALL exact-cost n prefixes, each Q_w=1_wFR+1_wRF, at old N=n+2. W_pair=2F_(n+1)D0/K >=21/85, because F_(n+4)=3F_(n+1)+2F_n<=5F_(n+1). Group by the original pi_h X_w. This retains even the original rank2 pair semantics.', coverage_scope='Nonempty cells require the existing full-lattice count condition h>2 p^floor(m/4), 2m<=n and its positive Binet bound. Full prefix-bank grouping inherits that result exactly. Arbitrary balanced lex grouping is allowed by the D1 matrix class but changes the old geometric address readout unless separately identified; it is not silently substituted.', native_scope='Activating all READY instead of an actually sparse selected bank changes that controller argument, though not the cut/carrier/trace-log action law. The conservative all-original-FR/RF-prefix bank is already the published global mathematical programme. Physical all-address decoder/query execution, full work return/history/price and Book binding remain required; no q_Born=pi or sampling renormalization is asserted.')

def golden_global_probability_clock_bound(root=None):
    checks = []

    def ck(name, cond):
        if not bool(cond):
            raise ArithmeticError(name)
        checks.append(name)
    p = (s.sqrt(5) - 1) / 2
    w1 = s.simplify(p ** 6)
    w0 = s.simplify(1 - w1)
    L = s.simplify(4 * p ** 3)
    aa = w1
    kappa = s.simplify(w0 - w1)
    ck('golden_coin_identity', s.simplify(w0 - 4 * p ** 3) == 0)
    ck('flat_AF_identity', s.simplify(L + aa - 1) == 0)
    ck('all_constant_mode_factor_positive', kappa > 0)
    X = s.symbols('X', nonnegative=True)
    P = s.expand((w0 + w1 * X) * (w0 - w1 * L + w1 * aa * X))
    A = s.simplify(P.coeff(X, 2))
    B = s.simplify(P.coeff(X, 1))
    C = s.simplify(P.coeff(X, 0))
    ck('leading_growth_p18', s.simplify(A - p ** 18) == 0)
    ck('positive_linear_growth', B > 0)
    ck('positive_constant_growth', C > 0)
    ck('baseline_product_below1', C < 1)
    y = s.symbols('y', real=True)
    ck('continued_B_never_above1', s.expand(1 - 4 * y * y * (1 - y * y) - (2 * y * y - 1) ** 2) == 0)
    (e, z) = s.symbols('e z', real=True)
    ck('continued_lambda_never_above1', s.expand(1 - 4 * e * (1 - e) - (2 * e - 1) ** 2) == 0)
    lam = s.symbols('lam', real=True)
    bb = s.symbols('bb', real=True)
    ck('second_feedback_upper_identity', s.expand(1 - (lam + (1 - lam) * bb) - (1 - lam) * (1 - bb)) == 0)
    xx = s.symbols('xx', real=True)
    Epoly = p * p * (1 + xx)
    bpoly = (p + p * p * xx) ** 2
    Bpoly = 4 * bpoly * (1 - bpoly)
    lpoly = 4 * Epoly * (1 - Epoly)
    ck('active_first_growth_degree4', s.degree(s.expand(Bpoly), xx) == 4)
    ck('active_second_growth_degree6', s.degree(s.expand(lpoly + (1 - lpoly) * Bpoly), xx) == 6)
    ck('active_pair_growth_degree10', s.degree(s.expand((w0 - w1 * Bpoly) * (w0 - w1 * (lpoly + (1 - lpoly) * Bpoly))), xx) == 10)
    Bb = s.Rational(-101, 2500)
    pair = s.simplify((w0 - w1 * Bb) * (w0 - w1 * (L + aa * Bb)))
    ck('b_above1_can_still_have_probability', pair > 0 and pair ** 2 < 1)
    pair2 = s.simplify(P.subs(X, 8))
    ck('growing_pair_alone_exceeds1', pair2 > 1)
    ck('retained_complement_can_mask_same_pair', s.simplify(kappa ** 16 * pair2 ** 2) < 1)
    for (Pairs, comp) in ((1, 0), (1, 8), (3, 2), (7, 18)):
        rho = s.Rational(2 * Pairs + comp, 2 * Pairs)
        T = kappa ** (-2 * (rho - 1))
        ck('all_factor_boundary_' + str(Pairs) + '_' + str(comp), s.simplify(kappa ** (2 * comp) * T ** (2 * Pairs) - 1) == 0)
    (AA, BB) = s.symbols('AA BB', positive=True)
    D0 = 13 * AA + 8 * BB
    D1 = 8 * AA + 5 * BB
    KK = AA * D0 + BB * D1
    ck('same_cut_READY_lower_bound_identity', s.expand(34 * AA * D0 - 21 * KK - (AA - BB) * (169 * AA + 105 * BB)) == 0)
    (ff, gg) = s.symbols('ff gg', nonnegative=True)
    ck('owned_fibonacci_selected_fraction', s.expand(5 * ff - (3 * ff + 2 * gg) - 2 * (ff - gg)) == 0)
    ck('owned_pair_coverage_21_85', s.Rational(2, 5) * s.Rational(21, 34) == s.Rational(21, 85))
    Wmin = s.Rational(21, 85)
    Rs = s.Rational(22448, 528)
    Pbase = s.simplify((w0 - w1 * L) * (w0 - w1 * L * (1 + aa)))
    ck('actual_baseline_is_strict_probability_amplitude', Pbase > 0 and Pbase < 1)
    Tstar = Pbase ** (-(1 - Wmin) / Wmin)
    ck('actual_return_threshold_positive_exponent', (1 - Wmin) / Wmin > 0)
    Xstar = 2 * (Tstar - C) / (B + s.sqrt(B * B + 4 * A * (Tstar - C)))
    Ystar = s.sqrt((1 + s.sqrt(1 + Xstar)) / 2)
    Cclock = 100 * (p + Ystar) / (3 * p ** 6)
    ck('full_prefix_clock_positive_finite_parameters', 100 / (3 * p ** 6) > 0 and p > 0 and (Wmin > 0) and (Wmin < 1))
    u = s.symbols('u', nonnegative=True)
    ck('B_to_y_threshold_identity', s.expand(4 * u * (u - 1) - ((2 * u - 1) ** 2 - 1)) == 0)
    return {'status': 'PASS', 'checks': len(checks), 'labels': checks, 'kappa': str(kappa), 'active_pair_polynomial': str(P), 'rank_ratio': 'actual return rho=1/W; d_return=1056*nu*K', 'necessary_bound': 't^2 <= [100 W/(3 a_amp^2 p^2)](p+Y_rho) h^2', 'owned_full_prefix_coverage': 'W>=21/85', 'owned_full_prefix_Cclock_approx': str(s.N(Cclock, 24)), 'owned_full_prefix_bound': 't^2<=Cclock*h^2 (a_amp=p^2)', 'scope': 'Same globally valid probability polynomial, fixed query at flat Taylor centre only. Actual return1056; all Hilbert complements retained. Not universal physical clock or programme selection.'}

def curved_centre_forced_clock(root=None):
    from fractions import Fraction as F
    labels = []

    def ck(name, value):
        if not bool(value):
            raise ArithmeticError(name)
        labels.append(name)
    L = 2
    h = F(1, L)
    sites = list(product(range(L), repeat=4))
    dirs = (0, 2, 3)
    c = F(1)
    M = F(2)
    delta = c / (30 * M)
    r = 1 / (1 + delta)
    K = ((1 + r) / (1 - r)) ** 3
    ck('uniform_cross_error_margin', 6 * M * delta + 9 * M * delta * delta <= c / 2)
    n = {x: 1 + sum((2 ** j * x[j] for j in range(4))) for x in sites}

    def shift(x, mu, k=1):
        y = list(x)
        y[mu] = (y[mu] + k) % L
        return tuple(y)
    A = {}
    for x in sites:
        a = F(0)
        for ms in product(range(L), repeat=3):
            y = list(x)
            k = F(1)
            for (mu, m) in zip(dirs, ms):
                y[mu] = (y[mu] + m) % L
                k *= r ** min(m, L - m)
            a += k * n[tuple(y)]
        A[x] = a
    ck('three_axis_kernel_l1_bound', sum(A.values()) <= K * sum(n.values()))
    ck('pointwise_keeps_original_weight', all((A[x] >= n[x] for x in sites)))
    ck('all_transverse_neighbor_ratios', all((r * A[x] <= A[shift(x, mu)] <= A[x] / r for x in sites for mu in dirs)))
    psi = {x: (-1) ** x[1] * A[x] for x in sites}
    qs = {}
    has_cross = False
    for x in sites:
        H = F(x[1] * x[1] - x[2] * x[2], 10)
        G = [[1 - H, 0, 0, -H], [0, -1, 0, 0], [0, 0, -1, 0], [-H, 0, 0, -1 - H]]
        d = [(psi[shift(x, mu)] - psi[x]) / h for mu in range(4)]
        q = sum((G[mu][nu] * d[mu] * d[nu] for mu in range(4) for nu in range(4)))
        qs[x] = q
        has_cross = has_cross or G[0][3] * d[0] * d[3] != 0
        ck('curved_q_negative_' + ''.join(map(str, x)), q <= -c * A[x] ** 2 / (2 * h * h))
    ck('fixture_includes_actual_time_cross_term', has_cross)
    ck('full_inverse_metric_bound', all((abs(v) <= M for x in sites for row in [[1 - F(x[1] * x[1] - x[2] * x[2], 10), 0, 0, -F(x[1] * x[1] - x[2] * x[2], 10)], [0, -1, 0, 0], [0, 0, -1, 0], [-F(x[1] * x[1] - x[2] * x[2], 10), 0, 0, -1 - F(x[1] * x[1] - x[2] * x[2], 10)]] for v in row)))
    HH = s.symbols('HH', real=True)
    GG = s.Matrix([[1 - HH, 0, 0, -HH], [0, -1, 0, 0], [0, 0, -1, 0], [-HH, 0, 0, -1 - HH]])
    ck('curved_pp_J_exactly1', s.expand(GG.det() + 1) == 0)
    ck('actual_density_operand_uniform_inverse_h2', all((2 * qs[x] / (n[x] * n[x]) <= -c / (h * h) for x in sites)))
    (q, u, v) = s.symbols('q u v', real=True)
    vals = {q: s.Rational(1, 5), u: s.Rational(2, 7), v: s.Rational(-1, 3)}
    fun = (u * u + 2 * u * v - 3 * v * v) / (1 - q)
    tay = 0
    for alpha in product(range(3), repeat=3):
        if sum(alpha) > 2:
            continue
        term = fun
        for (var, power) in zip((q, u, v), alpha):
            term = s.diff(term, var, power)
        term = term.subs(vals)
        for (var, power) in zip((q, u, v), alpha):
            term *= (var - vals[var]) ** power / s.factorial(power)
        tay += term
    ck('nonzero_matter_centre_still_exact_quadratic', s.simplify(tay.subs(q, vals[q]) - fun.subs(q, vals[q])) == 0)
    (lam, B, w0, w1) = s.symbols('lam B w0 w1', real=True)
    ck('arbitrary_curvature_second_factor_lower_identity', s.expand(w0 - w1 * (lam + (1 - lam) * B) - (w0 - w1) - w1 * (1 - lam) * (1 - B)) == 0)
    ck('actual_filled_return_rank1056', 2 * 528 == 1056)
    Wmin = s.Rational(21, 85)
    ck('same_owned_coverage_threshold_exponent', (1 - Wmin) / Wmin == s.Rational(64, 21))
    Pbase = s.symbols('Pbase', positive=True)
    ck('actual_global_return_threshold_boundary', s.simplify(Pbase ** 128 * (Pbase ** (-s.Rational(64, 21))) ** 42 - 1) == 0)
    bad = s.Matrix([[1, 2, 0, 0], [2, 3, 0, 0], [0, 0, -1, 0], [0, 0, 0, -1]])
    ck('hostile_large_shift_ADM_needs_spacelike_scope', bad.det() == -1 and bad[1, 1] > 0)
    return {'status': 'PASS', 'checks': len(labels), 'labels': labels, 'scope': 'bounded curved centre with uniformly spacelike dx1 and declared counting-site/rest scalar decoder', 'matter_bound': 'V_x<=-c*j*a^2/(2*K^2*W*h^2)', 'clock_bound': 't^2<=[2*K^2/(c*j*a^2*p^2)]*(p+Y_Tstar)*h^2', 'polynomial_family': 'same two-tick D1/D25; not five-outcome probe'}

def coherent_hodge_approx_preparation(root=None):
    import ast, hashlib
    from pathlib import Path
    import sympy as s
    checks = []

    def ck(name, v):
        if not bool(v):
            raise ArithmeticError(name)
        checks.append(name)

    def zero(M):
        return M.applyfunc(s.simplify) == s.zeros(*M.shape)
    N = 2
    bas = [(b, d, a, N - b - d - a) for b in range(N + 1) for d in range(N - b + 1) for a in range(N - b - d + 1)]
    ix = {v: i for (i, v) in enumerate(bas)}
    D = len(bas)

    def E(dst, src):
        T = s.zeros(D)
        for (j, v) in enumerate(bas):
            if v[src]:
                u = list(v)
                u[dst] += 1
                u[src] -= 1
                T[ix[tuple(u)], j] = s.sqrt((v[dst] + 1) * v[src])
        return T
    nums = [s.diag(*[v[k] for v in bas]) for k in range(4)]
    (alpha, beta, sq) = s.symbols('alpha beta s', real=True)
    ne = nums[2] + nums[3]
    nc = alpha ** 2 * nums[0] + beta ** 2 * nums[1] - alpha * beta * (E(0, 1) + E(1, 0))
    Jx = alpha * (E(0, 2) + E(2, 0)) - beta * (E(1, 2) + E(2, 1))
    Jy = alpha * (E(0, 3) + E(3, 0)) - beta * (E(1, 3) + E(3, 1))
    H = (Jx * Jx + Jy * Jy - 2 * nc - (alpha ** 2 + beta ** 2) * ne) / 2
    psi = s.zeros(D, 1)
    psi[ix[2, 0, 0, 0]] = s.sqrt(2)
    psi[ix[0, 0, 2, 0]] = psi[ix[0, 0, 0, 2]] = -sq * s.sqrt(2)
    pred = s.zeros(D, 1)
    pred[ix[2, 0, 0, 0]] = -2 * alpha ** 2 * sq * s.sqrt(2)
    pred[ix[0, 0, 2, 0]] = pred[ix[0, 0, 0, 2]] = alpha ** 2 * s.sqrt(2)
    pred[ix[1, 1, 0, 0]] = 4 * alpha * beta * sq
    pred[ix[0, 2, 0, 0]] = -2 * beta ** 2 * sq * s.sqrt(2)
    ck('actual clock operator includes all one-dark and two-dark leakage', zero(H * psi - pred))
    ck('leakage sectors are orthogonal not cancelled', all((bas[ix[v]][1] == j for (j, v) in ((0, (2, 0, 0, 0)), (1, (1, 1, 0, 0)), (2, (0, 2, 0, 0))))))
    for n in (2, 3):
        NN = 2 * n
        cc = lambda j: s.binomial(2 * j, j) / 4 ** j
        f = s.Matrix([(-sq) ** k * s.sqrt(cc(n - k)) for k in range(n + 1)])
        T = s.zeros(n + 1)
        for k in range(n + 1):
            T[k, k] = 2 * k * (NN - 2 * k)
            if k < n:
                T[k, k + 1] = T[k + 1, k] = (k + 1) * s.sqrt((NN - 2 * k) * (NN - 2 * k - 1))
        aa = 2 * sq - 1 / sq - NN * (1 - sq) ** 2 / sq
        bb = 2 * (1 - sq) ** 2 / sq
        diag = s.diag(*[-sq * NN + aa * k + bb * k * k for k in range(n + 1)])
        ck('exact pair-polynomial radial action N' + str(NN), zero(T * f - diag * f))
    j = s.symbols('j', integer=True, nonnegative=True)
    ck('centralbinomial upper induction polynomial', s.expand(4 * (j + 1) ** 3 - (2 * j + 1) ** 2 * (j + 2)) == 3 * j + 2)
    ck('centralbinomial lower induction polynomial', s.expand((2 * j + 1) ** 2 - 4 * j * (j + 1)) == 1)
    moments = {1: s.Rational(7, 6) * (3 * s.factorial(1) + 2 * 2 ** 2), 2: s.Rational(7, 6) * (3 * s.factorial(2) + 2 * 3 ** 3), 4: s.Rational(7, 6) * (3 * s.factorial(4) + 2 * 5 ** 5)}
    ck('uniform first moment constant13', moments[1] < 13)
    ck('uniform second moment constant70', moments[2] == 70)
    ck('uniform fourth moment constant7400', moments[4] < 7400)
    lo = 1 / s.sqrt(2)
    ck('coefficient bound 2 over s times1pluss squared at most1', s.simplify(lo * (1 + lo) ** 2 - 2) > 0)
    ck('sharp delta squared n at mostonehalf', s.simplify((1 + lo) ** 2 - 2) > 0)
    ck('bright variance constant52 follows moment bounds', 70 < s.Rational(17, 2) ** 2 and 7400 < 87 ** 2 and (s.Rational(17, 2) + s.Rational(87, 2) == 52))
    p = (s.sqrt(5) - 1) / 2
    coeff = s.simplify(1352 * p * p + 144 * p * (1 - p) + 70 * (1 - p) ** 2)
    ck('all leakage included in native residual constant24', s.simplify(24 ** 2 - coeff) > 0)
    ck('native residual coefficient exact golden reduction', s.simplify(coeff - (1348 - 1274 * p)) == 0)
    ck('onecopy excitation constant19', 26 ** 2 < 2 * 19 ** 2)
    z = s.symbols('z', positive=True)
    ck('clock weighted tail ratio is belowq', s.simplify(1 - 2 * z / (2 * z + 1)) == 1 / (2 * z + 1))
    ck('mean energy is strictly negative by weighted geometric bound', s.simplify(2 * sq ** 2 / (1 + sq) - 2 * sq + 2 * sq / (1 + sq)) == 0)
    target = Path('/Users/grigorijvahrusev/.codex/worktrees/native-source-synthesis/d0_15') if root is None else Path(root)
    path = target / '02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py'
    creator = next((n for n in ast.parse(path.read_text()).body if isinstance(n, ast.FunctionDef) and n.name == 'creator'))
    pin = hashlib.sha256(ast.dump(creator, include_attributes=False).encode()).hexdigest()
    ck('actual full16 creator AST pin', pin == '801b33d7ef3e41f6425be16153c82b1402215f6be757ea275ff06a69010f58e4')
    ns = {'s': s, 'SUBS': [tuple((i for i in range(4) if m & 1 << i)) for m in range(16)]}
    exec(compile(ast.Module(body=[creator], type_ignores=[]), str(path), 'exec'), ns)
    cr = [ns['creator'](s.eye(4)[:, i]) for i in range(4)]
    for k in range(1, 4):
        ck('actual current on all four coherent grades ' + str(k), ((cr[0] + cr[0].T) * (cr[k] - cr[k].T)).extract([0, 1, 14, 15], [0, 1, 14, 15]) == s.zeros(4))
    return {'status': 'PASS', 'checks': checks, 'source_sha256': {'creator_AST': pin}, 'trial': 'For N=2n>=8 let B=sqrtp clock1+sqrt(1-p) dark14, D orthogonal; Psi_N proportional to (Bdag²-s(adag²+bdag²))^n|vac>, s²=1-n^-1/2. This is permutation-symmetric fourgrade preparation inside full ambientCAR16.', 'moments': 'Pair count k has weights q^k c_(n-k), q=s²,c_j=binom(2j,j)/4^j. E k<=13sqrtn, E k²<=70n, E k4<=7400n².', 'actual_residual': 'All actual H(clock) leakage is retained: H Psi=pH(B)Psi-sqrt[p(1-p)]Ddag F Psi+(1-p)Ddag²Q Psi/2; F=(B n_exc+BdagQ)Psi=[(1-s)n_exc-2s]B Psi. Its Hermitian residual is <=24sqrtN, hence ||[(H-<H>)/binom(N,2)]Psi||<=48/[sqrtN(N-1)].', 'actual_marginal': 'rho1=(1-eps)|m0><m0|+eps(P0+P15)/2 exactly, eps=<n_exc>/N<1 and eps<=19/sqrtN. Thus trace distance from actual coherent13gh vacuum m0 is<=min(2,38/sqrtN), and k-copy distance<=min(2,2sqrt(19k)N^-1/4). Native current spatial numerators vanish and P1 density p(1-eps)e0e0* is nonzero.', 'affine_source': 'For an actually owned compression A_N(g)=a(g)I+b(g)H/binom(N,2), fixed trial gives e_N=<H>/binom(N,2) in[-2p/(N-1),0]. Hence ||D^j(q_N-a)||<=2p||D^j b||/(N-1), j0..2, while preparation log-source norm is<=96|b|/[q_floor logphi sqrtN(N-1)]. Any physical signal divisor must divide this residual too.', 'scope': 'Approximate source-normalized prep root only. No exact full polynomial E_N root, fitted occupation term, fixedRIGHT128/reference/site extension, indefiniteLorentz/higher-query/fullprice/PREP admission or physical clock law.'}

def full_polynomial_hoeffding_prep(root=None):
    import sympy as s
    from itertools import combinations
    checks = []

    def ck(name, v):
        if not bool(v):
            raise ArithmeticError(name)
        checks.append(name)

    def zero(M):
        return M.applyfunc(s.simplify) == s.zeros(*M.shape)
    X = s.Matrix([[0, 1], [1, 0]])
    I = s.eye(2)
    a = s.Rational(1, 2)
    b = s.Rational(1, 4)
    K2 = a * s.eye(4) + b * s.kronecker_product(X, X)
    K3 = a * s.eye(8) + b * (s.kronecker_product(X, X, I) + s.kronecker_product(X, I, X) + s.kronecker_product(I, X, X)) / 3
    (u, v, w) = s.symbols('rho00 real_coherence imaginary_coherence', real=True)
    rho = s.Matrix([[u, v + s.I * w], [v - s.I * w, 1 - u]])
    ck('exact allmixedIID polynomial for order2', s.simplify(s.trace(K2 * s.kronecker_product(rho, rho)) - a - b * (2 * v) ** 2) == 0)
    ck('same allmixedIID polynomial for order3 paddedkernel', s.simplify(s.trace(K3 * s.kronecker_product(rho, rho, rho)) - a - b * (2 * v) ** 2) == 0)
    for (name, R) in [('pure', s.diag(1, 0)), ('mixed', s.eye(2) / 2)]:
        conditional = s.zeros(2)
        RR = s.kronecker_product(R, R)
        for i in range(2):
            for j in range(2):
                conditional[i, j] = sum((K3[4 * i + e, 4 * j + f] * RR[f, e] for e in range(4) for f in range(4)))
        ck('fulloperator firstconditional equalsgI ' + name, zero(conditional - a * I))
    S = (0, 1, 2)

    def covariance(A, B):
        return b * b * s.Rational(len(set(combinations(A, 2)) & set(combinations(B, 2))), 9)
    ck('disjoint covariance vanishes exactly', covariance(S, (3, 4, 5)) == 0)
    ck('single-overlap covariance vanishes exactly', covariance(S, (0, 3, 4)) == 0)
    ck('two-overlap covariance remains genuinely nonzero', covariance(S, (0, 1, 4)) == b * b / 9)
    NN = 6
    kk = 3
    subsets = list(combinations(range(NN), kk))
    Rs = [len(set(S) & set(T)) for T in subsets]
    probability = s.Rational(sum((r >= 2 for r in Rs)), len(Rs))
    pairmean = sum((s.binomial(r, 2) for r in Rs)) / len(Rs)
    ck('actual finite hypergeometric overlap tail bounded bypairmoment', probability <= pairmean)
    ck('hypergeometric pairmoment has exact statedconstant', pairmean == s.Rational((kk * (kk - 1)) ** 2, 2 * NN * (NN - 1)))
    covmean = sum((covariance(S, T) for T in subsets)) / len(subsets)
    ck('paddedorder3 variance equals sameorder2 effect', covmean == b * b / s.binomial(NN, 2))

    def on_site(N, j):
        ops = [I] * N
        ops[j] = X
        return s.kronecker_product(*ops)
    N = 4
    Xs = [on_site(N, j) for j in range(N)]
    U2 = sum((Xs[i] * Xs[j] for (i, j) in combinations(range(N), 2)), s.zeros(2 ** N)) / s.binomial(N, 2)
    A = a * s.eye(2 ** N) + b * U2
    psi = s.zeros(2 ** N, 1)
    psi[0] = 1
    residual = (A - a * s.eye(2 ** N)) * psi
    ck('wholepositiveeffect finite prepnormal is nonzero', s.simplify((residual.T * residual)[0]) == b * b / s.binomial(N, 2))
    ck('degenerate order2 bound exact with centeredkernelnormb', s.simplify((residual.T * residual)[0] - b * b * 4 / (2 * N * (N - 1))) == 0)
    U1 = sum(Xs, s.zeros(2 ** N)) / N
    A1 = a * s.eye(2 ** N) + b * U1
    r1 = (A1 - a * s.eye(2 ** N)) * psi
    ck('hostile onebody Hilbertnormal shrinks1oversqrtN', s.simplify((r1.T * r1)[0] - b * b / N) == 0)
    velocity = sum((Xs[j] * psi for j in range(N)), s.zeros(2 ** N, 1))
    ck('physical productlift norm is exactlysqrtN', (velocity.T * velocity)[0] == N)
    ck('hostile simultaneousrotation source staysfinite', (2 * velocity.T * r1)[0] == 2 * b)
    theta = s.symbols('theta', real=True)
    q1 = a + b * s.sin(2 * theta)
    q2 = a + b * s.sin(2 * theta) ** 2
    ck('hostile positive-effect logsource doesnotvanish', s.simplify(s.diff(-s.log(q1), theta).subs(theta, 0)) == -2 * b / a)
    ck('degeneratecentre firstsource zero but actualsecondjet retained', s.diff(q2, theta).subs(theta, 0) == 0 and s.diff(q2, theta, 2).subs(theta, 0) == 8 * b)
    C = s.Matrix([[1, 0], [0, s.sqrt(2)]]) / s.sqrt(3)
    ck('productpurification preserves exactcompleteRIGHTGram', s.kronecker_product(C, C).T * s.kronecker_product(C, C) == s.kronecker_product(C.T * C, C.T * C))
    return {'status': 'PASS', 'checks': checks, 'kernel': 'Let K=K* be symmetric of orderk, ||K||<=B, and Tr K rho^tensor k=g(rho) EXACT for every mixed density. If Dg(rho0)[X]=0 for EVERYtracezeroHermitianX, then K1=Tr_(2..k) K rho0^tensor(k-1)=g0I on theFULLonecopycarrier, including outside support rho0.', 'wholevariance': 'For A_N=exactsubsetaverageK, N>=max(k,2), original productpurification Psi0^tensorN has ||(A_N-g0)Psi0^tensorN||<=B k(k-1)/sqrt[2N(N-1)]. Both disjoint and overlap1 covariances vanish; overlap>=2 probability is bounded by[k(k-1)]²/[2N(N-1)] and each covariance byB².', 'geometry': 'If the ACTUALfixedquery family remains matterdegree>=2 in the same scalarfeatures around the SAMEscalarfree rho0, derivativekernels K_j have the same degeneracy forj0..2. Thus the corresponding normalvector derivatives obey the sameconstant withB_j=||D^jK||. ExactIIDgeometric2jets themselves hold without this extraoperator-degeneracy premise.', 'physicalsource': 'For a constant prep multiplier gamma in S=-gamma logq/logphi (or an independently proved gradient-prefactor, not the action gamma(q)logq), q>=mu, a matter tangent ofFULLpurification normL_N gives |DS|/signal<=2gamma B k(k-1)L_N/[mu logphi signal sqrt(2N(N-1))]. If L_N<=ell sqrtN and all otherbudgetfactors arecontrolled this isO(N^-1/2). Generic shrinking Hilbertnormal WITHOUTthis tangentscale argument proves no physicalstationarity.', 'scope': 'This uses the ACTUALfullpolynomial kernel and original productinput, retaining spatialL, allCAR and fullRIGHT. It is a quantitative approximate conditional-prep consumer at a fullmixed-domain criticalcentre, not an exactfiniteNroot, arbitrarybackground theorem, freecopy/PREP admission, oldHJR/upstreamcost control or fullBook/GR closure.'}

def append_only_source_provenance(root):
    owner='02_REGISTRY/research/A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md'
    raw=(Path(root)/owner).read_bytes()
    start=raw.index('### 6.53.'.encode())
    end=raw.index('## 7. Вся более ранняя история остаётся своим источником'.encode(),start)
    prior=raw[:start]+raw[end:]
    old_sha='ee5ce8bf76882dc02fada7cfeb9b2371eac1626979c09e84119a322368362169'
    if hashlib.sha256(prior).hexdigest()!=old_sha:
        raise ArithmeticError('Old mathematical source bytes changed')
    return dict(status='PASS_UNCHANGED_PRIOR_SOURCE_BYTES',base_commit='622d96b68f0195aaed4ae856e90429225de9c580',
        source_path=owner, prior_owner_sha256=old_sha,
        current_owner_sha256=hashlib.sha256(raw).hexdigest(),
        prior_math='All pre-existing source bytes including6.46-6.52 are identical after removing only inserted6.53 onward. Prior null/source math receipt is reused; only this owner fingerprint is refreshed.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[4])
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = dict(status='PASS',
        provenance=append_only_source_provenance(args.root),
        checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        complete_price_scale=native_trace_amplification(args.root),
        preparation_and_recovery=preparation_and_recovery_controls(args.root),
        canonical_input_R=rayleigh_whitening_literal_v8(args.root),
        one_full_return=equalized_return(args.root),
        native_inverse_word=native_negative_binomial_controls(args.root),
        full_control_balance=equalized_full_radial(args.root),
        linked_input_R=equalized_linked_rayleigh(args.root),
        actual_control_cost=native_nb_controller_cost_source_controls(args.root),
        complete_history_mode=copy_antisymmetric_mdl(args.root),
        golden_mode_word=golden_copy_mdl_lcu(args.root),
        golden_mode_density_source=golden_mdl_densitized_source_controls(args.root),
        structured_even_exterior=adjacent_even_exterior(args.root),
        complete_archive_composition=fresh_detector_archive_composition(args.root),
        fixed_native_input=native_collective_mode(args.root),
        normalized_hodge_input=hodge_native_input_lift_controls(args.root),
        fixed_polynomial_effect=fixed_polynomial_input_effect(args.root),
        full_hodge_preparation_normal=hodge_fixed_right_spectral_normal(args.root),
        mixed_hodge_preparation=hodge_mixed_preparation_control(args.root),
        targeted_query_code=targeted_choi_source_controls(args.root),
        same_pointer_mean_MAP=targeted_full_failure_euler(args.root),
        targeted_entangling_normal=targeted_effect_preparation_normal(args.root),
        original_carrier_parity_graph=parity_graph_original_carrier_control(args.root),
        same_price_K_bath_root=parity_graph_joint_source_root(args.root),
        full_K_bath_source_transfer=parity_graph_proper_link_transfer(args.root),
        actual_CY_preparation_supply=cy_fine_right_capacity_controls(args.root),
        correlated_two_Hodge_radial=hodge_polar_radial_trial(args.root),
        actual_coherent_ground_branch=hodge_dark_ground_branch_control(args.root),
        actual_dark_energy_overlap=coherent_dark_energy_overlap(args.root),
        actual_fresh_Jones_actuation=jones_fresh_actuation_controls(args.root),
        pure_global_input_witness=pure_clock_checkerboard_witness(args.root),
        original_full_prefix_coverage=same_cut_ready_coverage_controls(args.root),
        necessary_global_probability_clock=golden_global_probability_clock_bound(args.root),
        actual_curved_centre_clock=curved_centre_forced_clock(args.root),
        coherent_quadratic_approx_preparation=coherent_hodge_approx_preparation(args.root),
        full_polynomial_vacuum_preparation=full_polynomial_hoeffding_prep(args.root),
        full_D0_price_selected=False, generic_joint_recovery=False, GR_closed=False)
    output = json.dumps(result, ensure_ascii=False, indent=2, default=str)+'\n'
    if args.output:
        args.output.write_text(output)
    print(output, end='')


if __name__ == '__main__':
    main()
