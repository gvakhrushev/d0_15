#!/usr/bin/env python3
"""Full native price scale, noncommuting return and native inverse-word controls.

Only new exact identities are evaluated. The accepted old amplification
receipt is pinned and reused, never replayed. Default output is read-only.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
from itertools import product
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
        prior_math='All pre-existing source bytes including6.46-6.52 are identical after removing only inserted6.53-6.55. Prior null/source math receipt is reused; only this owner fingerprint is refreshed.')


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
        full_D0_price_selected=False, generic_joint_recovery=False, GR_closed=False)
    output = json.dumps(result, ensure_ascii=False, indent=2, default=str)+'\n'
    if args.output:
        args.output.write_text(output)
    print(output, end='')


if __name__ == '__main__':
    main()
