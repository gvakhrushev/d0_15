#!/usr/bin/env python3
"""Actual full-price null-source consumer and covariant matter mean limit.

Runs new exact CAR/block/query/price identities and bounded interval moments.
Reuses the pinned accepted root enclosure; no old root/heat/Lean suite is run.
Default is read-only; --output writes the single requested receipt.
"""
import argparse
import ast
import hashlib
import json
from collections import Counter
from itertools import combinations
from types import SimpleNamespace
from pathlib import Path
import numpy as np
import sympy as s
import mpmath as mp


def null_interval(root):
    root = Path(root)
    rel = ('02_REGISTRY/research/sources/d0_af_star_full_lattice_2026-10-17/'
           'NATIVE_SCALAR_PRICE_RESPONSE_RESULT.json')
    data = (root/rel).read_bytes()
    pin = 'd81ad34e47829ed0361c9d954d744f2a41d816ee7fb666407e8817431bca3aa6'
    if hashlib.sha256(data).hexdigest() != pin:
        raise RuntimeError('accepted root receipt changed')
    accepted = json.loads(data)['interval_source']
    mp.iv.dps = 80
    iv = mp.iv
    checks = []

    def require(test, label):
        if not bool(test):
            raise ArithmeticError(label)
        checks.append(label)

    a = iv.mpf(accepted['a_root_interval'])
    p = (iv.sqrt(5)-1)/2
    beta = 2*p*p
    z = iv.mpf(2)**-20
    C = a/beta
    require(a > iv.mpf('1.80') and a < iv.mpf('1.82'), 'reuse actual root enclosure')
    # The accepted theta tail is valid uniformly on this same interval.
    theta = 1+2*sum((iv.exp(-a*j*j) for j in range(1,13)), iv.mpf(0))
    theta += iv.mpf([0,'1e-128'])
    Z = 16*theta**4
    cache = {}

    def weight(K):
        if K not in cache:
            ee = iv.exp(-a*K)
            cache[K] = (-ee/Z+128*z*beta*ee/(1-z+z*ee)
                        +(iv.mpf(1)/128 if K == 1 else 0))
        return cache[K]

    radius = 7
    counts = Counter((i*i+j*j+k*k,i**4+j**4+k**4)
                     for i in range(-radius,radius+1)
                     for j in range(-radius,radius+1)
                     for k in range(-radius,radius+1))
    A = U = N0 = Nvv = Nrr = iv.mpf(0)
    for t in range(-radius-1,radius+1):
        x = iv.mpf(t)+iv.mpf(1)/2
        for (J,J4), multiplicity in counts.items():
            wk, wl = weight(t*t+J), weight((t+1)**2+J)
            ww = wk+wl
            dd = (wl-wk)/(2*t+1)
            count = C*multiplicity
            A += count*(ww*(2+8*x*x+iv.mpf(8)/3*J)
                        +dd*(2+4*x*x+16*x**4+iv.mpf(4)/3*J
                             -iv.mpf(32)/3*x*x*J+iv.mpf(16)/3*J4))
            U += count*(ww+dd)
            N0 += count*(48*ww+(48+16*J)*dd)
            Nvv += count*(8*ww+(4+16*x*x)*dd)
            Nrr += count*(24*ww+(24+iv.mpf(32)/3*J)*dd)

    # All three link operators have ||sqrt(C) W|| <= sqrt(48 C)<12.
    # For the null metric ||S||<=1 gives ||V||<=12(1+|k|).
    # Hence the same full4D shell majorant applies to every new entry.
    require(48*C < 144, 'rescaled full-CAR normal operator bound')
    Cw = iv.mpf(1)/16+128*z*beta/(1-z)
    j = radius+1
    ratio = (1+iv.mpf(1)/j)**7*iv.exp(-iv.mpf('1.80')*(2*j-1))
    first = ((64*j**3+16*j)*(1+2*j)**2
             *(2+iv.mpf('1.82')*(4*j+1)**2)
             *iv.exp(-iv.mpf('1.80')*(j-1)**2))
    tail = 16*Cw*144*first/(1-ratio)
    require(ratio < 1, 'Gaussian shell ratio')
    require(tail < iv.mpf('1e-25'), 'all omitted full-spectrum matrix entries bounded')
    error = iv.mpf(['-1e-25','1e-25'])
    A += error
    U += error
    N0 += error
    Nvv += error
    Nrr += error
    Nvr = -8*U
    determinant = Nvv*Nrr-Nvr*Nvr
    require(U > 0 and N0 < 0, 'full24 nonresonant spectral chamber')
    require(Nvv > 0 and determinant < 0, 'coupled vector block invertible')
    correction = U*U*(4*Nrr+16*Nvr+16*Nvv)/determinant
    reduced = A-36*U*U/N0-correction
    # Shift/telescoping identity also gives U=2b and the vector correction2b.
    b = U/2
    cc = 4*b-N0/24
    simplified = A-2*b-6*b*b/(4*b-cc)
    require(simplified.a <= reduced.b and reduced.a <= simplified.b,
            'simplified normal quotient overlaps direct interval result')
    bounds = {
        'bare_null': ('-0.4442906','-0.4442905'),
        'U': ('0.00136970','0.00136972'),
        'scalar_normal': ('-1.106243','-1.106242'),
        'vector00': ('0.0054788','0.0054789'),
        'vector01': ('-0.0109577','-0.0109576'),
        'vector11': ('-0.748453','-0.748452'),
        'vector_determinant': ('-0.00422073','-0.00422071'),
        'full_normal_reduced_null': ('-0.4455993','-0.4455991'),
    }
    values = [A,U,N0,Nvv,Nvr,Nrr,determinant,reduced]
    for (name,(lo,hi)), value in zip(bounds.items(),values):
        require(value > iv.mpf(lo) and value < iv.mpf(hi), name+' rational enclosure')
    return dict(status='PASS_INTERVAL',checks=checks,accepted_root_SHA256=pin,
        actual_price='full fixed-beta heat+feedback+fixedRIGHT Riesz H+J+R; '
                     'beta=2p^2,z=2^-20,M128,CAR16/reference128',
        normal_order=['L0','L2 (uncoupled)','Lv','Lr'],
        spectral_trace_convention='centered xi=t+1/2; Y2=sum yi^2; Y4=sum yi^4; '
                                  'C=a_root/beta and physical links rescaled by omega=2pi',
        coefficients_enclosed=bounds,tail_bound='1e-25',
        spatial_shell_pairs=len(counts),
        sum_rectangle=dict(time=[-8,7],space=[-7,7]),
        complete_proper_link_inertia=dict(positive=3,negative=21,zero=0),
        observer_link_kernel_dimension=3,
        physical_real_cosine_Hessian='half the complex base coefficient',
        comparison='EH null self-Hessian is zero, but this complete conditional '
                   'price has nonzero null self-response after every bounded normal correction.',
        limitations=['not a finite native Schur limit without the soft-channel rate',
                     'not a nonlinear generic joint-critical section',
                     'nonzero full-price response alone does not identify independent matter stress',
                     'not a full-D0 GR no-go or physical action selection theorem'])

def soft_interval(root):
    """Seven exact spectral moments; all finite soft-channel coefficients.

    This is the literal h-Taylor coefficient consumer, not a finite-h heat
    replacement. The exact CAR reduction is checked by soft_symbol below.
    """
    root = Path(root)
    rel = ('02_REGISTRY/research/sources/d0_af_star_full_lattice_2026-10-17/'
           'NATIVE_SCALAR_PRICE_RESPONSE_RESULT.json')
    raw = (root/rel).read_bytes()
    pin = 'd81ad34e47829ed0361c9d954d744f2a41d816ee7fb666407e8817431bca3aa6'
    if hashlib.sha256(raw).hexdigest() != pin:
        raise RuntimeError('accepted root receipt changed')
    mp.iv.dps = 80
    iv = mp.iv
    a = iv.mpf(json.loads(raw)['interval_source']['a_root_interval'])
    p = (iv.sqrt(5)-1)/2
    beta, z = 2*p*p, iv.mpf(2)**-20
    C, omega = a/beta, 2*iv.pi
    checks = []

    def require(test, label):
        if not bool(test):
            raise ArithmeticError(label)
        checks.append(label)

    require(a > iv.mpf('1.80') and a < iv.mpf('1.82'), 'accepted actual root')
    amin = iv.mpf('1.80')
    thmax = 1+2*sum((iv.exp(-amin*j*j) for j in range(1,13)), iv.mpf(0))
    thmax += iv.mpf([0,'1e-128'])
    m2max = 2*sum((j*j*iv.exp(-amin*j*j) for j in range(1,13)), iv.mpf(0))
    m4max = 2*sum((j**4*iv.exp(-amin*j*j) for j in range(1,13)), iv.mpf(0))
    m2max += iv.mpf([0,'1e-124'])
    m4max += iv.mpf([0,'1e-124'])
    require(thmax < iv.mpf('1.4') and m2max < iv.mpf('.35')
            and m4max < iv.mpf('.36'), 'uniform homogeneous moment bounds')
    # F'(a)=-Var(|k|^2)+2048 beta sum |k|^4 r_k(1-r_k).
    # The 0,+/-1 contributions alone give the following variance floor.
    radial_upper = (-8*iv.exp(-iv.mpf('1.82'))/iv.mpf('1.4')**2
                    +2048*iv.mpf('.77')*z/(1-z)
                    *(4*iv.mpf('.36')*iv.mpf('1.4')**3
                      +12*iv.mpf('.35')**2*iv.mpf('1.4')**2))
    transverse_floor = beta*(1/(16*iv.mpf('1.4')**4)-128*z*iv.mpf('.77')/(1-z))
    require(radial_upper < iv.mpf('-.64'), 'strict radial root derivative')
    require(transverse_floor > iv.mpf('.012'), 'strict transverse root Jacobian')
    theta = 1+2*sum((iv.exp(-a*j*j) for j in range(1,13)), iv.mpf(0))
    theta += iv.mpf([0,'1e-128'])
    Z = 16*theta**4
    cache = {}

    def weight(K):
        if K not in cache:
            ee = iv.exp(-a*K)
            cache[K] = (-ee/Z+128*z*beta*ee/(1-z+z*ee)
                        +(iv.mpf(1)/128 if K == 1 else 0))
        return cache[K]

    R = 8
    counts = Counter((i*i+j*j+k*k, i**4+j**4+k**4,
                      i*i*j*j+i*i*k*k+j*j*k*k)
                     for i in range(-R,R+1)
                     for j in range(-R,R+1)
                     for k in range(-R,R+1))
    m0 = m4 = m22 = iv.mpf(0)
    for t in range(-R,R+1):
        for (J,J4,J22), count in counts.items():
            w = count*weight(t*t+J)
            m0 += w
            m4 += w*t**4
            m22 += w*iv.mpf(J22)/3
    L0 = L2 = L4 = L22 = iv.mpf(0)
    for t in range(-R-1,R+1):
        for (J,J4,J22), count in counts.items():
            L = count*(weight((t+1)**2+J)-weight(t*t+J))/(2*t+1)
            L0 += L
            L2 += L*J
            L4 += L*J4
            L22 += L*J22

    # A sup shell j has <=(2j+1)^4<=81j^4 integer points;
    # every polynomial here has modulus <=3j^4, and |2t+1|>=1.
    # On omitted shifted shells both weights are <=Cw exp(-1.80(j-1)^2).
    # The Riesz part is supported on K=1, wholly inside the rectangle.
    Cw = iv.mpf(1)/16+128*z*beta/(1-z)
    j = R+1
    ratio = (iv.mpf(j+1)/j)**8*iv.exp(-iv.mpf('1.80')*(2*j-1))
    tail = 1000*Cw*j**8*iv.exp(-iv.mpf('1.80')*(j-1)**2)/(1-ratio)
    require(ratio < 1, 'degree8 Gaussian shell ratio')
    require(tail < iv.mpf('1e-35'), 'all seven omitted moment tails')
    error = iv.mpf(['-1e-35','1e-35'])
    m0,m4,m22,L0,L2,L4,L22 = [v+error for v in (m0,m4,m22,L0,L2,L4,L22)]
    A = L0+2*m0
    den = 3*A+L2
    require(den < 0, 'normal scalar denominator is separated from zero')
    ss = iv.mpf(16)/3*(L4+2*L22)+128*m22+32*m4-12*L2**2/den
    st = iv.mpf(16)/3*(L4-L22)+32*m22+32*m4
    tau = L2*(3*A+4*L2)/(3*den)
    null0 = A+iv.mpf(4)/3*L2+iv.mpf(16)/3*L4-9*A*A/(4*den)
    require(ss < 0 and st < 0, 'all three soft eigenvalues nonzero')
    correction = C*3*tau*tau/ss
    values = dict(physical_S2_singlet=C*omega**2*ss,
                  physical_S2_standard=C*omega**2*st,
                  physical_T1_imag=C*omega*tau,
                  bounded_normal_null=C*null0,
                  finite_soft_correction=correction,
                  actual_finite_full_null_limit=C*null0-correction,
                  h_times_observer_response_imag=-tau/(omega*ss))
    bounds = dict(physical_S2_singlet=('-10.670715','-10.670714'),
                  physical_S2_standard=('-35.813010','-35.813008'),
                  physical_T1_imag=('-0.641005','-0.641004'),
                  bounded_normal_null=('-0.4455993','-0.4455991'),
                  finite_soft_correction=('-0.1155182','-0.1155180'),
                  actual_finite_full_null_limit=('-0.3300812','-0.3300809'),
                  h_times_observer_response_imag=('-0.0600715','-0.0600713'))
    for name,(lo,hi) in bounds.items():
        require(values[name] > iv.mpf(lo) and values[name] < iv.mpf(hi), name)
    return dict(status='PASS_INTERVAL',checks=checks,accepted_root_SHA256=pin,
        coefficients_enclosed=bounds,tail_bound='1e-35',
        homogeneous_root_Jacobian=dict(radial_derivative_upper='-0.64',
            transverse_price_derivative_over_exp_lower='0.012',
            cross_terms='zero by parity',
            consumer='uniform finite-grid C1 convergence plus local implicit continuation'),
        moment_intervals={name:str(v) for name,v in
                         zip(('m0','m4','m22','L0','L2','L4','L22'),
                             (m0,m4,m22,L0,L2,L4,L22))},
        spatial_shells=len(counts),sum_rectangle=dict(time=[-9,8],space=[-8,8]),
        actual_price='unchanged finite-B H+J+R at beta=2p^2,z=2^-20; full CAR16/RIGHT128',
        conclusion='finite soft correction survives; full finite Schur and bounded '
                   'continuum normal quotient have different limits; physical observer '
                   'first response grows as 1/h',
        asymptotic_domain='finite Brillouin grids with Gaussian high-mode domination; '
                          'never an infinite fixed-h sine spectrum',
        limitations=['no uniform fixed-chart C1-bounded joint-normal section',
                     'does not exclude finite-h sections on shrinking charts',
                     'native edge h*Omega and physical Omega use different norms',
                     'not nonlinear joint-critical recovery or native action selection'])


def null_symbol(root):
    root = Path(root)
    path = '02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py'
    node = next((n for n in ast.parse((root / path).read_text()).body if isinstance(n, ast.FunctionDef) and n.name == 'creator'))
    pin = hashlib.sha256(ast.dump(node, include_attributes=False).encode()).hexdigest()
    if not pin == '801b33d7ef3e41f6425be16153c82b1402215f6be757ea275ff06a69010f58e4':
        raise ArithmeticError("pin == '801b33d7ef3e41f6425be16153c82b1402215f6be757ea275ff06a69010f58e4'")
    ns = dict(s=s, SUBS=[tuple((i for i in range(4) if m & 1 << i)) for m in range(16)])
    exec(compile(ast.Module(body=[node], type_ignores=[]), path, 'exec'), ns)
    C = [ns['creator'](s.eye(4)[:, i]) for i in range(4)]
    I = [v.T for v in C]
    Cr = lambda v: sum((v[i] * C[i] for i in range(4)), s.zeros(16))
    Gamma = lambda O: sum((O[i, j] * C[i] * I[j] for i in range(4) for j in range(4)), s.zeros(16))
    Id = s.eye(16)
    eta = s.diag(1, -1, -1, -1)
    (x, w, c, t) = s.symbols('x omega c t', real=True)
    y = s.symbols('y1:4', real=True)
    (Y2, Y4, Y22) = s.symbols('Y2 Y4 Y22', real=True)
    mom = s.Matrix([x, *y])
    q = s.Matrix([w, 0, 0, 0])
    out = mom + q
    k = s.Matrix([1, 1, 0, 0])
    low = eta * k
    S = -k * low.T / 2
    checks = []

    def ck(name, test):
        if not test:
            raise ArithmeticError(name)
        checks.append(name)
    ex = lambda M: M.applyfunc(s.expand)
    ck('null', (k.T * eta * k)[0] == 0)
    ck('coframe_nilpotent', S * S == s.zeros(4) and s.trace(S) == 0)
    e = (s.eye(4) - t * S) / c
    U = c * (s.eye(4) + t * S) * eta
    ck('native_inverse_coframe_convention', ex(eta * e.inv().T - U) == s.zeros(4))
    ck('det_coframe_constant', s.factor(e.det() - c ** (-4)) == 0)
    ck('contravariant_metric_exact', ex(U.T * eta * U - c * c * (eta - t * k * k.T)) == s.zeros(4))
    ck('covariant_metric_exact', ex(e.T * eta * e - c ** (-2) * (eta + t * low * low.T)) == s.zeros(4))
    D = lambda m: s.I * c * sum((eta[r, r] * m[r] * (C[r] - I[r]) for r in range(4)), s.zeros(16))
    (Dk, Dl) = (D(mom), D(out))

    def metricjet(T):
        return ex(s.I * c * sum((mom[r] * Cr(T * eta[:, r]) - out[r] * Cr(T * eta[:, r]).T for r in range(4)), s.zeros(16)))
    V = metricjet(S)
    Q = ex(Dl * V + V * Dk)
    ck('null_jet_closed_form', ex(V + s.I * c * ((x + y[0]) * Cr(k) - (x + y[0] + w) * Cr(k).T) / 2) == s.zeros(16))
    gen = []
    names = []
    pairs = []
    for (a, b) in [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]:
        O = s.zeros(4)
        O[a, b] = 1
        O[b, a] = 1 if a == 0 else -1
        ck('Lorentz_generator_' + str(a) + str(b), O.T * eta + eta * O == s.zeros(4))
        gen.append(O)
        names.append(('B' if a == 0 else 'R') + str(a) + str(b))
        pairs.append((a, b))
    links = []
    labels = []
    characters = []
    for r in range(4):
        for (gi, O) in enumerate(gen):
            A = c * eta[r, r] * C[r] * Gamma(O)
            Z = A + A.T
            links.append(Z)
            labels.append(str(r) + ':' + names[gi])
            (a, b) = pairs[gi]
            chi = tuple((sum((j == z for z in (r, a, b))) % 2 for j in (1, 2, 3)))
            characters.append(chi)
    inner = lambda A, B: s.expand(sum((s.conjugate(a) * b for (a, b) in zip(A, B))))

    def even(v):
        P = s.Poly(s.expand(v), *y)
        return s.expand(sum((coeff * s.prod((z ** power for (z, power) in zip(y, powers))) for (powers, coeff) in P.terms() if all((power % 2 == 0 for power in powers))), s.S(0)))

    def avg(v):
        P = s.Poly(even(v), *y)
        res = 0
        for (powers, coeff) in P.terms():
            key = tuple(sorted(powers, reverse=True))
            factor = {(0, 0, 0): 1, (2, 0, 0): Y2 / 3, (4, 0, 0): Y4 / 3, (2, 2, 0): Y22 / 3}[key]
            res += coeff * factor
        return s.factor(res)
    parity = {''.join(map(str, ch)): [lab for (lab, ch2) in zip(labels, characters) if ch2 == ch] for ch in sorted(set(characters))}
    ck('eight_three_dimensional_parity_sectors', len(parity) == 8 and all((len(v) == 3 for v in parity.values())))
    raw_cross = {}
    averaged_cross = {}
    Qlinks = []
    for (lab, Z, ch) in zip(labels, links, characters):
        Qz = ex(Dl * Z + Z * Dk)
        Qlinks.append(Qz)
        v = inner(V, Z)
        qv = inner(Q, Qz)
        raw_cross[lab] = [str(s.factor(v / c ** 2)), str(s.factor(qv / c ** 4))]
        averaged_cross[lab] = [str(avg(v / c ** 2)), str(avg(qv / c ** 4))]
        if ch not in [(0, 0, 0), (1, 0, 0)]:
            ck('forbidden_parity_null_cross_' + lab, even(v) == 0 and even(qv) == 0)
    Zdict = dict(zip(labels, links))
    active = [Zdict['1:B01'] + Zdict['2:B02'] + Zdict['3:B03'], 2 * Zdict['1:B01'] - Zdict['2:B02'] - Zdict['3:B03'], Zdict['0:B01'], Zdict['2:R12'] + Zdict['3:R13']]
    anames = ['boost_trace', 'boost_traceless_11', 'boost_temporal_01', 'rotation_spatial_vector1']
    QA = [ex(Dl * Z + Z * Dk) for Z in active]
    vg = s.Matrix(4, 4, lambda i, j: avg(inner(active[i], active[j]) / c ** 2))
    qg = s.Matrix(4, 4, lambda i, j: avg(inner(QA[i], QA[j]) / c ** 4))
    for i in range(4):
        for j in range(4):
            if i < 2 and j >= 2 or (i >= 2 and j < 2) or {i, j} == {0, 1}:
                ck('active_irrep_block_' + str(i) + str(j), vg[i, j] == 0 and qg[i, j] == 0)
    for (label, Z) in [('even_difference23', Zdict['2:B02'] - Zdict['3:B03']), ('odd_difference23', Zdict['2:R12'] - Zdict['3:R13'])]:
        ck('null_decouples_' + label, avg(inner(V, Z)) == 0 and avg(inner(Q, ex(Dl * Z + Z * Dk))) == 0)
    for (lab, Z, ch) in zip(labels, links, characters):
        for axis in range(1, 4):
            reflection = s.diag(*[(-1) ** (m >> axis & 1) for m in range(16)])
            ck('link_character_' + lab + '_' + str(axis), reflection * Z * reflection == (-1) ** ch[axis - 1] * Z)
    R = s.zeros(4)
    R[0, 1] = 1
    R[1, 0] = -1
    B = s.zeros(4)
    B[0, 1] = B[1, 0] = 1
    GR = Gamma(R)
    T = 2 * y[0] * Id / w - GR
    Vboost = metricjet(B)
    Vz = ex(Vboost - s.I * w * Zdict['0:B01'])
    ck('individual_boost_kernel_dirac', ex(Vz - (T * Dk - Dl * T)) == s.zeros(16))
    Ek = c * c * (mom.T * mom)[0]
    El = c * c * (out.T * out)[0]
    ck('individual_boost_kernel_Delta', ex(Dl * Vz + Vz * Dk - (Ek - El) * T) == s.zeros(16))
    v = [S * eta[:, r] for r in range(4)]
    Vminus = V.subs(x, x - w)
    mixed = ex(T.conjugate().T * V - Vminus * T.conjugate().T)
    dv = [R * v[r] + (2 * v[0] if r == 1 else s.zeros(4, 1)) for r in range(4)]
    hom = s.I * c * sum((mom[r] * (Cr(dv[r]) - Cr(dv[r]).T) for r in range(4)), s.zeros(16))
    rest = ex((mixed - hom) / (s.I * w))
    ck('null_metric_mixed_kernel_closes_in_actual_rows', ex(rest - (Zdict['0:B01'] + Zdict['1:B01']) / 2) == s.zeros(16))
    xi = s.symbols('xi', real=True)
    center = lambda z: s.factor(z.subs(x, xi - w / 2).subs(w, 1))
    centered_self = {'V': str(center(avg(inner(V, V) / c ** 2))), 'Q': str(center(avg(inner(Q, Q) / c ** 4)))}
    centered_vg = vg.applyfunc(center)
    centered_qg = qg.applyfunc(center)
    centered_cv = [center(avg(inner(V, Z) / c ** 2)) for Z in active]
    centered_cq = [center(avg(inner(Q, Z) / c ** 4)) for Z in QA]
    ck('centered_null_cross_vectors_identical', centered_cv == centered_cq == [-6 * s.I, 0, 2 * s.I, -4 * s.I])
    g0 = eta / c ** 2
    ginv = c ** 2 * eta
    h = low * low.T / c ** 2
    q_up = ginv * q
    qs = (q.T * ginv * q)[0]
    trh = s.trace(ginv * h)
    qhq = (q_up.T * h * q_up)[0]
    Glin = s.Matrix(4, 4, lambda mu, nu: s.expand((qs * h[mu, nu] + q[mu] * q[nu] * trh - q[mu] * (q_up.T * h)[nu] - q[nu] * (q_up.T * h)[mu] + g0[mu, nu] * (qhq - qs * trh)) / 2))
    hraised = ginv * h * ginv
    ck('EH_null_self_contraction_zero', s.expand(s.trace(hraised * Glin)) == 0)
    ck('EH_full_rows_nonzero_transverse', Glin == s.diag(0, 0, -w * w / 2, -w * w / 2))
    qq = s.Matrix(s.symbols('q0:4', real=True))
    qu = ginv * qq
    qqs = (qq.T * ginv * qq)[0]
    qh = (qu.T * h * qu)[0]
    GG = s.Matrix(4, 4, lambda mu, nu: s.expand((qqs * h[mu, nu] + qq[mu] * qq[nu] * trh - qq[mu] * (qu.T * h)[nu] - qq[nu] * (qu.T * h)[mu] + g0[mu, nu] * (qh - qqs * trh)) / 2))
    ck('EH_null_self_zero_for_every_Fourier_covector', s.expand(s.trace(hraised * GG)) == 0)
    return dict(status='PASS', checks=checks, creator_AST_sha256=pin, physical=dict(U='eta e^-T', e='c^-1 (I+t k(eta k)^T/2)', k=[1, 1, 0, 0], S=S.tolist(), metric='g=c^-2[eta+t(eta k)(eta k)^T]', inverse_metric='q=c^2[eta-t k k^T]', det_e='c^-4', observer='n=e0 fixed'), momenta='incoming (x,y1,y2,y3), outgoing (x+omega,y1,y2,y3); physical Fourier q=(omega,0,0,0)', null_jet='V=-i c/2[(x+y1)C(k)-(x+y1+omega)I(k)]', raw_self={'Vnorm_div_c2': str(s.factor(inner(V, V) / c ** 2)), 'Qnorm_div_c4': str(s.factor(inner(Q, Q) / c ** 4))}, averaged_self={'Vnorm_div_c2': str(avg(inner(V, V) / c ** 2)), 'Qnorm_div_c4': str(avg(inner(Q, Q) / c ** 4))}, parity_sectors=parity, null_to_all24_before_average=raw_cross, null_to_all24_after_average=averaged_cross, centered=dict(convention='omega=1,x=xi-1/2; c=sqrt(C), physical link amplitudes rescaled by physical omega', self_traces=centered_self, V_Gram=centered_vg.tolist(), Q_Gram=centered_qg.tolist(), V_cross=centered_cv, Q_cross=centered_cq), kernel=dict(direction='physical observer/coframe boost B01 with link correction -i omega Z_0B01', T='2*y1/omega*I-Gamma(R01)', mixed_null='T^* V_S(k)-V_S(k-q) T^* = homogeneous_coframe_jet(dv) + i omega*(V_0B01+V_1B01)/2', dv='dv_r=R01*(S eta_r)+2 delta_r1*(S eta_0)', scope='Mixed Hessian compatibility follows only at the owned full homogeneous coframe/link stationary background and with the proper second jet/root-moment cancellation. This is not an off-shell gauge identity or a finite-h forward-stencil theorem.'), active_order=anames, active_V_gram_div_c2=vg.tolist(), active_Q_gram_div_c4=qg.tolist(), null_active_V_cross_div_c2=[str(avg(inner(V, Z) / c ** 2)) for Z in active], null_active_Q_cross_div_c4=[str(avg(inner(Q, Z) / c ** 4)) for Z in QA], averaging='Independent spatial signs followed by permutations; Y2=sum yi^2,Y4=sum yi^4,Y22=sum_{i<j}yi^2 yj^2. No replacement of actual spectral/Riesz weights by scalar constants; averaging requires those weights share these symmetries.', Einstein=dict(full_covariant_linearized_G=Glin.tolist(), self='zero for every q', sign='Fourier derivative=i q; standard G=Ricci-1/2 g R', action='EH metric Hessian self-contraction is zero at flat background, despite nonzero all-row Einstein response'), scope='Exact continuum fullCAR16 symbol only. No finite-forward-stencil Ward, spectral sum, Schur inverse, seagull cancellation or full native critical root asserted. Actual proper second jet and source weights still belong to the native price.')

def full_normal_blocks(root):
    root = Path(root)
    p = root / '02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py'
    node = next((n for n in ast.parse(p.read_text()).body if isinstance(n, ast.FunctionDef) and n.name == 'creator'))
    pin = hashlib.sha256(ast.dump(node, include_attributes=False).encode()).hexdigest()
    if not pin == '801b33d7ef3e41f6425be16153c82b1402215f6be757ea275ff06a69010f58e4':
        raise ArithmeticError("pin == '801b33d7ef3e41f6425be16153c82b1402215f6be757ea275ff06a69010f58e4'")
    ns = {'s': s, 'SUBS': [tuple((i for i in range(4) if m & 1 << i)) for m in range(16)]}
    exec(compile(ast.Module(body=[node], type_ignores=[]), str(p), 'exec'), ns)
    C = [np.array(ns['creator'](s.eye(4)[:, i]).tolist(), dtype=np.int64) for i in range(4)]
    eta = [1, -1, -1, -1]
    gam = [x - x.T for x in C]

    def B(i):
        a = np.zeros((4, 4), dtype=np.int64)
        a[0, i] = a[i, 0] = 1
        return a

    def R(i, j):
        a = np.zeros((4, 4), dtype=np.int64)
        a[i, j] = 1
        a[j, i] = -1
        return a
    J = {1: R(2, 3), 2: R(3, 1), 3: R(1, 2)}

    def W(entries):
        out = np.zeros((16, 16), dtype=np.int64)
        for (r, om) in entries.items():
            G = sum((int(om[i, j]) * C[i] @ C[j].T for i in range(4) for j in range(4)), np.zeros((16, 16), dtype=np.int64))
            z = eta[r] * C[r] @ G
            out += z + z.T
        return out
    basis = {'scalar_boost_trace': {1: B(1), 2: B(2), 3: B(3)}, 'pseudo_rotation_trace': {1: J[1], 2: J[2], 3: J[3]}, 'polar_time_boost': {0: B(1)}, 'polar_rotation_anti': {2: J[3], 3: -J[2]}, 'axial_time_rotation': {0: J[1]}, 'axial_boost_anti': {2: B(3), 3: -B(2)}, 'tensor_boost_diag': {1: B(1), 2: -B(2)}, 'tensor_boost_offdiag': {1: B(2), 2: B(1)}, 'pseudo_tensor_rotation_diag': {1: J[1], 2: -J[2]}, 'pseudo_tensor_rotation_offdiag': {1: J[2], 2: J[1]}}
    names = list(basis)
    ops = [W(basis[n]) for n in names]

    def trace(a):
        return int(np.trace(a))

    def metric(fn):
        return [[fn(a, b) for b in ops] for a in ops]
    A = metric(lambda a, b: trace(a @ b))
    T = metric(lambda a, b: trace(a @ gam[0] @ b @ gam[0]))
    S = metric(lambda a, b: sum((trace(a @ g @ b @ g) for g in gam[1:])))
    (x, y1, y2, y3, q) = s.symbols('x y1 y2 y3 q', real=True)
    ii = s.I
    Cs = list(map(s.Matrix, C))
    gs = list(map(s.Matrix, gam))

    def dLambda(om):
        return sum((int(om[i, j]) * Cs[i] * Cs[j].T for i in range(4) for j in range(4)), s.zeros(16))
    Dk = ii * (x * gs[0] - y1 * gs[1] - y2 * gs[2] - y3 * gs[3])
    Dl = Dk + ii * q * gs[0]
    for (i, yi) in enumerate([y1, y2, y3], 1):
        u = [s.eye(4)[:, r] * eta[r] for r in range(4)]
        du = [s.Matrix(B(i)) * v for v in u]
        V = sum((ii * (x if r == 0 else [y1, y2, y3][r - 1]) * sum((du[r][j] * Cs[j] for j in range(4)), s.zeros(16)) - ii * (x + q if r == 0 else [y1, y2, y3][r - 1]) * sum((du[r][j] * Cs[j].T for j in range(4)), s.zeros(16)) for r in range(4)), s.zeros(16))
        V -= ii * q * s.Matrix(W({0: B(i)}))
        Tq = 2 * yi / q * s.eye(16) - dLambda(R(0, i))
        if not (V - (Tq * Dk - Dl * Tq)).applyfunc(s.simplify) == s.zeros(16):
            raise ArithmeticError('(V - (Tq * Dk - Dl * Tq)).applyfunc(s.simplify) == s.zeros(16)')
    out = {'status': 'PASS_EXACT_INTEGER_TRACES_AND_3_KERNEL_SYMBOLS', 'creator_pin': pin, 'names': names, 'A': A, 'T': T, 'S': S, 'spectral_sums_not_evaluated': True}

    def levi(i, j, k):
        return int(s.LeviCivita(i - 1, j - 1, k - 1))
    full_basis = []
    full_names = []

    def add(name, ent):
        full_names.append(name)
        full_basis.append(ent)
    add('scalar_boost', basis['scalar_boost_trace'])
    add('pseudo_scalar_rotation', basis['pseudo_rotation_trace'])
    for i in range(1, 4):
        add('polar_time_' + str(i), {0: B(i)})
        add('polar_anti_' + str(i), {r: sum((levi(i, r, j) * J[j] for j in range(1, 4)), np.zeros((4, 4), dtype=np.int64)) for r in range(1, 4)})
    for i in range(1, 4):
        add('axial_time_' + str(i), {0: J[i]})
        add('axial_anti_' + str(i), {r: sum((levi(i, r, j) * B(j) for j in range(1, 4)), np.zeros((4, 4), dtype=np.int64)) for r in range(1, 4)})
    traceless = [np.diag([1, -1, 0]), np.diag([1, 1, -2])]
    for (i, j) in [(0, 1), (0, 2), (1, 2)]:
        m = np.zeros((3, 3), dtype=np.int64)
        m[i, j] = m[j, i] = 1
        traceless.append(m)
    for (label, ctor) in [('tensor', B), ('pseudo_tensor', lambda j: J[j])]:
        for (j, m) in enumerate(traceless):
            add(label + '_' + str(j), {r: sum((int(m[r - 1, c - 1]) * ctor(c) for c in range(1, 4)), np.zeros((4, 4), dtype=np.int64)) for r in range(1, 4)})
    if not len(full_basis) == 24:
        raise ArithmeticError('len(full_basis) == 24')
    full_ops = [W(e) for e in full_basis]
    FA = np.array([[trace(u @ v) for v in full_ops] for u in full_ops])
    FT = np.array([[trace(u @ gam[0] @ v @ gam[0]) for v in full_ops] for u in full_ops])
    FS = np.array([[sum((trace(u @ g @ v @ g) for g in gam[1:])) for v in full_ops] for u in full_ops])
    MB = FA + FT
    MC = FS - 3 * FA
    EB = np.zeros((24, 24), dtype=np.int64)
    EC = EB.copy()
    EB[0, 0] = 96
    EC[0, 0] = -24
    EB[1, 1] = 96
    EC[1, 1] = -240
    for i in range(3):
        inds = slice(2 + 2 * i, 4 + 2 * i)
        EB[inds, inds] = np.array([[8, -16], [-16, 48]])
        EC[inds, inds] = np.array([[0, 0], [0, -16]])
        inds = slice(8 + 2 * i, 10 + 2 * i)
        EB[inds, inds] = np.array([[0, 0], [0, 16]])
        EC[inds, inds] = np.array([[-16, 0], [0, -16]])
    for off in [14, 19]:
        for (j, norm2) in enumerate([2, 6, 2, 2, 2]):
            EB[off + j, off + j] = 8 * norm2
            EC[off + j, off + j] = -8 * norm2
    if not np.array_equal(MB, EB):
        raise ArithmeticError('np.array_equal(MB, EB)')
    if not np.array_equal(MC, EC):
        raise ArithmeticError('np.array_equal(MC, EC)')
    (xx, qq, dd, ww) = s.symbols('xx qq dd ww', nonzero=True, real=True)
    if not s.expand(2 * (xx - qq) + qq - (2 * xx + qq)) == -2 * qq:
        raise ArithmeticError('s.expand(2 * (xx - qq) + qq - (2 * xx + qq)) == -2 * qq')
    if not s.expand(-s.Rational(1, 2) * ((2 * xx + qq) ** 2 - qq ** 2) + 2 * xx * (xx + qq)) == 0:
        raise ArithmeticError('s.expand(-s.Rational(1, 2) * ((2 * xx + qq) ** 2 - qq ** 2) + 2 * xx * (xx + qq)) == 0')
    out.update({'status': 'PASS_EXACT_FULL24_BLOCKS_AND_3_KERNEL_SYMBOLS', 'full_basis': full_names, 'full_b_coefficient': MB.tolist(), 'full_c_coefficient': MC.tolist(), 'full24_block_dimension': [1, 1, 2, 2, 2, 2, 2, 2, 5, 5], 'spectral_shift_identity': 'a+3c-b=0; B_lapse=24*omega*b; C_lapse=24*(4b-c)', 'certified_inertia_if_owned_B_positive_C_negative': {'positive': 3, 'negative': 21, 'zero': 0}, 'whole27_kernel_after_owned_mixed_Ward': 3, 'no_new_spectral_sum': True})
    out['matrix_sha256'] = hashlib.sha256(json.dumps([out['full_b_coefficient'], out['full_c_coefficient']], sort_keys=True).encode()).hexdigest()
    return {k: out[k] for k in ['status', 'creator_pin', 'full_basis', 'matrix_sha256', 'full24_block_dimension', 'spectral_shift_identity', 'certified_inertia_if_owned_B_positive_C_negative', 'whole27_kernel_after_owned_mixed_Ward', 'no_new_spectral_sum']}

def general_source(root):
    root = Path(root)
    checks = []

    def require(name, value):
        if value is not True:
            raise AssertionError(name)
        checks.append(name)
    (p, z, u, sign, f, q) = s.symbols('p z u sigma f q', real=True)
    e = p ** 2 * (1 + u * f)
    b = (p + sign * p ** 2 * u * q) ** 2
    B = 4 * b * (1 - b)
    lam = 4 * e * (1 - e)
    Q = 1 - z * B
    R = 1 - z * (lam + (1 - lam) * B)
    j = -528 * (s.log(Q) + s.log(R))
    Af = 528 * z * p ** 2 * u * (1 - B) * 4 * (1 - 2 * e) / R
    Bq = 8 * sign * p ** 2 * u * (p + sign * p ** 2 * u * q) * (1 - 2 * b)
    Cq = 528 * z * Bq * (1 / Q + (1 - lam) / R)
    require('literal full two-tick J2 general star derivative', s.cancel(s.diff(j, f) - Af) == 0)
    require('literal full two-tick J2 general scalar derivative', s.cancel(s.diff(j, q) - Cq) == 0)
    creators = []
    for a in range(4):
        C = s.zeros(16)
        for mask in range(16):
            if mask & 1 << a:
                continue
            preceding = bin(mask & (1 << a) - 1).count('1')
            C[mask | 1 << a, mask] = (-1) ** preceding
        creators.append(C)
    eta = (1, -1, -1, -1)
    G = [creators[a] + eta[a] * creators[a].T for a in range(4)]
    for a in range(4):
        for c in range(a, 4):
            require(f'full16 Lorentz CAR ({a},{c})', G[a] * G[c] + G[c] * G[a] == (2 * eta[a] * s.eye(16) if a == c else s.zeros(16)))
    (amp, scale) = s.symbols('amplitude spatial_scale', positive=True)
    E = s.diag(1, scale, 1, 1)
    metric = E.T * s.diag(*eta) * E
    k = s.Matrix([amp, 0, 0, 0])
    gamma = sum((k[a] * G[a] for a in range(4)), s.zeros(16))
    require('off-null full16 Clifford square', gamma * gamma == amp ** 2 * s.eye(16))
    qactual = (s.Matrix([amp, 0, 0, 0]).T * metric.inv() * s.Matrix([amp, 0, 0, 0]))[0]
    volume = E.det()
    require('spatial-scale CAR scalar has no hidden volume factor', s.simplify(qactual - amp ** 2) == 0)
    require('exact complete J2 has zero off-null spatial pressure row', s.diff(j.subs({f: 0, q: qactual}), scale) == 0)
    require('minimal covariant kinetic density has nonzero pressure row', s.simplify(s.diff(volume * qactual, scale) - amp ** 2) == 0)
    I = G[0] * G[1] * G[2] * G[3]
    require('full16 oriented pseudoscalar square', I * I == -s.eye(16))
    V = G[0] * (scale * G[1]) * G[2] * G[3]
    require('available CAR volume is a separate central contraction', -I * V == scale * s.eye(16))
    (ss, A0, V0) = s.symbols('s A0 V0', positive=True)
    mean = s.simplify(ss ** 2 * A0 / (ss ** 4 * V0))
    require('global coframe radial Ward forces zero mean at a full root', s.simplify(s.diff(mean, ss).subs(ss, 1) + 2 * A0 / V0) == 0)
    (Rsc, Qsc, Gamma, gam, coupling) = s.symbols('R q Gamma gamma_star lambda', real=True)
    trace = -gam * Rsc - coupling * Qsc + 2 * Gamma
    require('integrated mean metric trace is Gamma', s.expand(trace.subs(gam * Rsc + coupling * Qsc, Gamma) - Gamma) == 0)
    xs = s.symbols('x0:4', real=True)
    psi = xs[0] ** 2 + xs[0] * xs[1] + xs[1] ** 3 / 3 + xs[2] * xs[3]
    ds = [s.diff(psi, x) for x in xs]
    qpsi = sum((eta[a] * ds[a] ** 2 for a in range(4)))
    T = s.Matrix(4, 4, lambda a, c: ds[a] * ds[c] - (eta[a] * qpsi / 2 if a == c else 0))
    box = sum((eta[a] * s.diff(psi, xs[a], 2) for a in range(4)))
    for nu in range(4):
        div = sum((eta[a] * s.diff(T[a, nu], xs[a]) for a in range(4)))
        require(f'own scalar Ward component {nu}', s.expand(div - box * ds[nu]) == 0)
    pp = (s.sqrt(5) - 1) / 2
    for (N, k) in ((2, 1), (2, 2), (4, 1), (4, 4), (7, 3), (7, 7)):
        den = s.fibonacci(2 * N + 9)
        x = s.Rational(s.fibonacci(2 * N - k + 8), den)
        y = s.Rational(s.fibonacci(2 * N - k + 7), den)
        er = (pp ** (2 * N + 14) + pp ** (4 * N + 18)) / (1 - pp ** (4 * N + 18))
        for (name, w, pf) in (('x', x, pp ** (k + 1)), ('y', y, pp ** (k + 2))):
            gap = s.simplify(er - abs(s.simplify(w / pf - 1)))
            require(f'actual regular to PF relative bound N={N},k={k},{name}', gap.is_nonnegative is True)
    for m in range(1, 5):
        words = [('', 0)]
        cut = []
        while words:
            (word, cost) = words.pop()
            if cost >= m:
                cut.append((word, cost))
            else:
                words.extend(((word + 'F', cost + 1), (word + 'R', cost + 2)))
        require(f'complete PF macro cut m={m}', s.simplify(sum((pp ** cost for (_, cost) in cut)) - 1) == 0)
        require(f'exact Q-tail normalization m={m}', s.simplify(sum((2 * pp ** (cost + 3) for (_, cost) in cut)) - 2 * pp ** 3) == 0)
    paths = ['02_REGISTRY/research/A4D_LOCAL_LEFT_CODED_CAR_NULL_MATTER_EINSTEIN_2026_10_18.md', '02_REGISTRY/research/sources/d0_local_null_scalar_einstein_2026-10-18/check_local_null_scalar_source.py', '02_REGISTRY/research/A4D_GOLDEN_QUANTILE_CLOCK_SAME_CAR_VOLUME_BRIDGE_2026_10_18.md', '02_REGISTRY/research/A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md', '02_REGISTRY/research/A4D_AF_STAR_PALATINI_NONLINEAR_EINSTEIN_COMPOSITION_2026_10_17.md', '02_REGISTRY/research/sources/d0_af_star_full_lattice_2026-10-17/check_full_lattice.py']
    return {'status': 'PASS', 'checks': len(checks), 'checked_identities': checks, 'source_sha256': {path: hashlib.sha256((root / path).read_bytes()).hexdigest() for path in paths}, 'actual_general_source': 'DJ2/(nu*K)=sum_i pi_i [a_i Df_i+c_i Dq_i], a_i=528 z p^2 t^2(1-B_i) lambda_AF_prime(E_i)/R_i; c_i=528 z Bq_i[1/Q_i+(1-lambda_AF_i)/R_i]. Bq_i=8 sigma p^2 t^2(p+sigma p^2 t^2 q_i)(1-2b_i).', 'existing_limit': 'The current finite J2 has actual regular-left weights pi_i=D_j/K. Its untransported weak query is f_h+lambda*q, with f_h=h^(-4)*Pstar,h. Only after the owned regular-to-PF and physical quadrature estimates does it tend to a constant multiple of integral(Pstar_density+lambda*q_scalar) dx. Its null pp-wave theorem is valid, but this is not the full covariant minimal scalar source away from q=0.', 'exact_off_null_control': 'e=diag(1,s,1,1), links I, psi=amplitude*x0. All16 Clifford square = amplitude^2 I, f=0, q=amplitude^2, so complete J2 has Ds J2=0 for every admissible t. Covariant density J*q=s*amplitude^2 has Ds=amplitude^2.', 'positive_same_price_composite': 'Use the SAME finite J2 with its actual regular weights pi_i=D_j/K. Query r_h=f_h/J=h^(-4)*Pstar,h/J and q_h on physical moving quantile samples T_(J/V)(word_address). Consume the regular-to-PF estimate and the existing golden quadrature; do not replace pi by PF mu as an exact equality. The weak limit after its owned fixed normalization is Gamma=A/V, A=integral[Pstar_density+lambda*J*q], V=integral J. Sampling f_h itself with J would double the gravity volume factor and is incorrect.', 'complete_mean_source': 'D Gamma=(D A-Gamma*D V)/V. Actual cell motion and J-variation are both retained through the inverse quantile jet.', 'full_Euler_after_own_Cartan': 'gamma_star*G_munu+lambda*(dmu psi*dnu psi-0.5*g_munu*q)+0.5*Gamma*g_munu=0; dmu(J*g^munu*dnu psi)=0; D_omega(e wedge e)=0. Here Pstar_density=gamma_star*J*R after the connection equation.', 'free_scale_consumer': 'If global coframe scaling e->s e is genuinely admitted with links and psi fixed, A has degree 2 and V degree 4. Gamma has degree -2, so its own radial Euler forces Gamma=A=0. Then all full mean-price equations equal D A=0. If global scaling is fixed by a collar/calibration/volume constraint, this step cannot be used and a volume multiplier remains.', 'coupling': 'kappa=-lambda/gamma_star. Exact literal G2/Hodge contraction gives gamma_star=-sgn(det e)/2 for c_star=1. Hence kappa=2*sgn(det e)*lambda; the old det(e)<0 null-frame family has kappa=-2*lambda. No pp-wave fit, independent matter normalization or empirical Newton constant is selected.', 'gamma_owner': 'AF Palatini composition lines 153-168 explicitly defines f_h=gamma_star*P_P+O_C2(h), with gamma_star computed from c,G2,star,b. Full-lattice owner lines 94-100 fixes c=1 for its displayed density. Literal G2 and Hodge STAR are check_full_lattice.py lines 49-58, and their contraction lines 94-99. Orientation det T=-1 is explicitly retained; no gamma value is fitted here.', 'own_scalar_Ward': 'nabla^mu T_munu=(Box psi)*partial_nu psi. The scalar Euler supplies its stress conservation; no independent T is assigned.', 'existing_exact_null_root_transfer': 'The old exact pp-wave remains proved for the OLD inverse-PF word. It does not transfer automatically to the new regular/PF quantile programme: the old operands rho_AF^(-1)*f_hat and rho_AF^(-1)*q_hat produced bar_w*sum(Df_hat+lambda*Dq_hat), while changing to the scalar operands can leave sum_x w_x*(Df_hat+lambda*Dq_hat). Even at J=1,T=I,f=q=0, equality of profile values is insufficient. Exact finite transfer requires equality of the ENTIRE actual query jet together with its true weights, including inverse-PF normalization, or an independent source cancellation proof. The new general programme currently has the conditional C2 source limit and nonempty continuum Einstein-scalar solutions, not a claimed exact finite 40-row pp root.', 'finite_exact_price': 'J2=-nu*528*K*sum_i pi_i[log Q_i+log R_i], pi_i=D_type(i)/K. With full canonical PF macro cut C_m and genuine Q_w=FR+RF tails, tau(Q_w)=2*p^3*mu(w); c_AF=2*p^3 is an actual fixed cylinder mass, not a fitted probability. If a different supported old cut is used, its own exact normalization/quadrature constant must be retained.', 'regular_to_PF': 'For A_k subset A_N: x=F_(2N-k+8)/F_(2N+9), y=F_(2N-k+7)/F_(2N+9); PF minimal weights p^(k+1),p^(k+2). Relative discrepancy <=epsilon_reg(N)=[p^(2N+14)+p^(4N+18)]/[1-p^(4N+18)]. Hence every fixed diagonal H(theta) has C2 trace error <=epsilon_reg*||H||_C2, since actual trace coefficients and PF coefficients are field-independent and the total PF mass is 1.', 'normalized_weak_price': 'Let a0=528*z*4*p^11/R0, R0=1-z*(L+p^6*L), L=4*p^3. Set Phi_t(r,q)=[j_t(r,q)-j_0]/(a0*t^2). Its Taylor jet is r+lambda*q+O_C2(t^2), with actual input-derivative bounds. For the specified full macro cut c_AF, compare (J2-J20)/(nu*K*a0*c_AF*t^2) to Gamma=A/V. Only field-independent constants are used; the original price/cut is unchanged.', 'C2_source_bound': 'For the actual smooth chart, the normalized weak-price error is bounded by C_K,h*t^2 + E_geometry(h) + delta_m*max_(j<=2) Lip_u D_theta^j[(r_h+lambda*q_h) composed with T_(J/V)] + epsilon_reg(N)/c_AF*||Phi_t(r_h,q_h) composed with T||_C2 + C_compile*eta/t^2. Here r_h=h^(-4)*Pstar,h/J, delta_m<=2*p^floor(m/8), E_geometry(h)=O_C2(h) only under the owners smooth-chart assumptions, and all h,t-dependent derivative constants remain explicit. Add E_controller/sigma only if a SAME actual aggregation/source theorem proves that correction; no Shannon price is automatically added to J2. There is no leaf-count factor and no assertion pi=mu.', 'price_and_execution_scope': 'This is the specified full feedback trace-log J2. SAME-history Shannon w=q is a separate binding and is not substituted for J2. Physical admission of the moving query/whole tuple, fixed native prior, controller and additional full-price terms remains conditional; no fixed-grid diffeomorphism theorem, exact generic finite roots, or native forcing is claimed.'}


def soft_symbol(root):
    root = Path(root)
    path = root / '02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py'
    node = next((n for n in ast.parse(path.read_text()).body if isinstance(n, ast.FunctionDef) and n.name == 'creator'))
    pin = hashlib.sha256(ast.dump(node, include_attributes=False).encode()).hexdigest()
    if not pin == '801b33d7ef3e41f6425be16153c82b1402215f6be757ea275ff06a69010f58e4':
        raise ArithmeticError('exact soft symbol identity')
    ns = dict(s=s, SUBS=[tuple((i for i in range(4) if m & 1 << i)) for m in range(16)])
    exec(compile(ast.Module(body=[node], type_ignores=[]), str(path), 'exec'), ns)
    C = [s.SparseMatrix(ns['creator'](s.eye(4)[:, i])) for i in range(4)]
    I = [v.T for v in C]
    zero = lambda : s.zeros(16)
    ex = lambda A: s.SparseMatrix(A.applyfunc(s.expand))
    cr = lambda v: sum((v[i] * C[i] for i in range(4)), zero())
    ga = lambda O: sum((O[i, j] * C[i] * I[j] for i in range(4) for j in range(4)), zero())
    eta = s.diag(1, -1, -1, -1)
    x = s.symbols('x', real=True)
    yy = s.symbols('y1:4', real=True)
    (d2, o2) = s.symbols('d2 o2', real=True)
    p = s.Matrix([x, *yy])
    l = p + s.Matrix([1, 0, 0, 0])
    (xi, Y2, Y4, Y22) = s.symbols('xi Y2 Y4 Y22', real=True)
    dot = lambda A, B: s.expand(sum((s.conjugate(v) * B[i, j] for ((i, j), v) in A.todok().items())))

    def avg(z):
        z = s.expand(z.subs(x, xi - s.Rational(1, 2)))
        P = s.Poly(z, xi, *yy)
        out = 0
        for (powers, co) in P.terms():
            if any((v % 2 for v in powers)):
                continue
            spatial = tuple(sorted(powers[1:], reverse=True))
            f = {(0, 0, 0): 1, (2, 0, 0): Y2 / 3, (4, 0, 0): Y4 / 3, (2, 2, 0): Y22 / 3}.get(spatial)
            if f is None:
                raise ValueError(spatial)
            out += co * xi ** powers[0] * f
        return s.factor(out)

    def vv_cf(S, U=eta):
        du = [cr((S * U)[:, r]) for r in range(4)]
        return [ex(s.I * sum((p[r] * du[r] - l[r] * du[r].T for r in range(4)), zero())), ex(-sum((p[r] ** 2 * du[r] + l[r] ** 2 * du[r].T for r in range(4)), zero()) / 2), ex(-s.I * sum((p[r] ** 3 * du[r] - l[r] ** 3 * du[r].T for r in range(4)), zero()) / 6)]

    def D(v):
        return [ex(s.I * sum((v[r] * eta[r, r] * (C[r] - I[r]) for r in range(4)), zero())), ex(-sum((v[r] ** 2 * eta[r, r] * (C[r] + I[r]) for r in range(4)), zero()) / 2), ex(-s.I * sum((v[r] ** 3 * eta[r, r] * (C[r] - I[r]) for r in range(4)), zero()) / 6)]
    (Dk, Dl) = (D(p), D(l))
    O = []
    labels = []
    pairs = []
    for (a, b) in [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]:
        om = s.zeros(4)
        om[a, b] = 1
        om[b, a] = 1 if a == 0 else -1
        O.append(om)
        pairs.append((a, b))
    VV = []
    null = s.Matrix([1, 1, 0, 0])
    SS = [-null * (eta * null).T / 2] + O[:3]
    for S in SS:
        VV.append(vv_cf(S))
    for r in range(4):
        for (gi, om) in enumerate(O):
            A = eta[r, r] * C[r] * ga(om)
            VV.append([ex(A + A.T), ex(s.I * (p[r] * A - l[r] * A.T)), ex(-(p[r] ** 2 * A + l[r] ** 2 * A.T) / 2)])
            labels.append(str(r) + ':' + ('B' if gi < 3 else 'R') + ''.join(map(str, pairs[gi])))
    VZ = [[ex(VV[1 + i][j] - s.I * VV[4 + i][j]) for j in range(3)] for i in range(3)]

    def qjet(v):
        return [ex(sum((Dl[t] * v[j - t] + v[j - t] * Dk[t] for t in range(j + 1)), zero())) for j in range(3)]
    QZ = [qjet(v) for v in VZ]
    QQ = [qjet(v)[:2] for v in VV]
    k1 = []
    for (lab, v, q) in zip(['null', 'obs1', 'obs2', 'obs3'] + labels, VV, QQ):
        row = []
        for (vz, qz) in zip(VZ, QZ):
            row.append([str(avg(dot(v[0], vz[1]) + dot(v[1], vz[0]))), str(avg(dot(q[0], qz[1]) + dot(q[1], qz[0])))])
        k1.append(dict(label=lab, coeffs=row))
    k2 = []
    A0 = []
    B0 = []
    weight_poly = []
    for i in range(3):
        rr = []
        aa = []
        bb = []
        pp = []
        for j in range(3):
            (vz, wz) = (VZ[i], VZ[j])
            (qz, rz) = (QZ[i], QZ[j])
            a = dot(vz[0], wz[0])
            b = dot(qz[0], rz[0])
            aa.append(a)
            bb.append(b)
            rr.append([str(avg(sum((dot(vz[t], wz[2 - t]) for t in range(3)), s.S(0)))), str(avg(sum((dot(qz[t], rz[2 - t]) for t in range(3)), s.S(0))))])
            bp = s.cancel(b / (2 * x + 1))
            if not s.denom(bp) == 1:
                raise ArithmeticError('exact soft symbol identity')
            poly = s.expand(a + a.subs(x, x - 1) + bp.subs(x, x - 1) - bp)
            pp.append(poly)
        k2.append(rr)
        A0.append(aa)
        B0.append(bb)
        weight_poly.append(pp)
    U2 = eta * ((d2 - o2) * s.eye(4) + o2 * s.ones(4)) / 2

    def dU(v):
        return ex(s.I * sum((v[r] * (cr(U2[:, r]) - cr(U2[:, r]).T) for r in range(4)), zero()))
    (dk2, dl2) = (dU(p), dU(l))
    vU = []
    for i in range(3):
        uc = vv_cf(O[i], U2)[0]
        A = cr(U2[:, 0]) * ga(O[i])
        vU.append(ex(uc - s.I * (A + A.T)))
    qU = [ex(dl2 * VZ[i][0] + VZ[i][0] * dk2 + Dl[0] * vU[i] + vU[i] * Dk[0]) for i in range(3)]
    E2bg = lambda pp: (d2 - o2) * (pp.T * pp)[0] + o2 * sum(pp) ** 2
    de2 = E2bg(l) - E2bg(p)
    bg = []
    for i in range(3):
        row = []
        for j in range(3):
            va = dot(VZ[i][0], vU[j]) + dot(vU[i], VZ[j][0])
            qa = dot(QZ[i][0], qU[j]) + dot(qU[i], QZ[j][0]) - s.cancel(de2 * B0[i][j] / (2 * x + 1))
            row.append([str(avg(va)), str(avg(qa))])
        bg.append(row)
    delatt = -(sum((v ** 4 for v in l)) - sum((v ** 4 for v in p))) / 12
    lattice_dd = [[str(avg(-s.cancel(delatt * B0[i][j] / (2 * x + 1)))) for j in range(3)] for i in range(3)]
    (m0, m4, m22, L0, L2, L4, L22) = s.symbols('m0 m4 m22 L0 L2 L4 L22', real=True)
    loc = {str(v): v for v in [xi, Y2, Y4, Y22, d2, o2]}
    checks = []

    def ck(name, value):
        if not value:
            raise ArithmeticError(name)
        checks.append(name)

    def folded(a, b):
        a = s.sympify(a, locals=loc)
        b = s.sympify(b, locals=loc)
        rem = s.expand(b).subs(xi, 0)
        bp = s.cancel((b - rem) / (2 * xi))
        ap = a.subs(xi, x + s.Rational(1, 2))
        bp = bp.subs(xi, x + s.Rational(1, 2))
        pp = s.expand(ap + ap.subs(x, x - 1) + bp.subs(x, x - 1) - bp)
        return (pp, rem)

    def reduced(a, b):
        (pp, rem) = folded(a, b)
        pp = pp.subs({Y2: sum((v * v for v in yy)), Y4: sum((v ** 4 for v in yy)), Y22: sum((yy[i] ** 2 * yy[j] ** 2 for i in range(3) for j in range(i + 1, 3)))})
        res = 0
        for (powers, co) in s.Poly(s.expand(pp), x, *yy).terms():
            if any((v % 2 for v in powers)):
                continue
            key = tuple(sorted(powers, reverse=True))
            res += co * {(0, 0, 0, 0): m0, (2, 0, 0, 0): 0, (4, 0, 0, 0): m4, (2, 2, 0, 0): m22}[key]
        rp = s.Poly(rem, Y2, Y4, Y22)
        if not rp.total_degree() <= 1:
            raise ArithmeticError('exact soft symbol identity')
        res += rp.coeff_monomial(1) * L0 + s.diff(rem, Y2) * L2 + s.diff(rem, Y4) * L4 + s.diff(rem, Y22) * L22
        return s.factor(res)
    Ak = sum((p[r] * C[r] * I[r] for r in range(4)), zero())
    comm = lambda a, b: ex(a * b - b * a)
    for r in range(4):
        ck('halfedge_creator_' + str(r), comm(Ak, C[r]) == p[r] * C[r])
    ck('halfedge_D1', ex(Dk[1] - s.I * comm(Ak, Dk[0]) / 2) == s.zeros(16))
    Dh2 = ex(-s.I * sum((p[r] ** 3 * eta[r, r] * (C[r] - I[r]) for r in range(4)), zero()) / 24)
    ck('halfedge_D2', ex(Dk[2] - Dh2 + comm(Ak, comm(Ak, Dk[0])) / 8) == s.zeros(16))
    ck('no_linear_Delta_term', ex(Dk[0] * Dk[1] + Dk[1] * Dk[0]) == s.zeros(16))
    ck('quartic_Delta_term', ex(Dk[0] * Dk[2] + Dk[1] * Dk[1] + Dk[2] * Dk[0] + sum((v ** 4 for v in p)) * s.eye(16) / 12) == s.zeros(16))
    A = L0 + 2 * m0
    Y = s.Matrix(24, 3, lambda i, j: reduced(*k1[4 + i]['coeffs'][j]))
    expected = s.zeros(24, 3)
    for i in range(3):
        expected[i, i] = -2 * A
    for i in range(3):
        for j in range(3):
            expected[6 * (i + 1) + i, j] = 8 * L2 / 3
    for (gi, (a, b)) in enumerate(pairs):
        if a > 0:
            expected[6 * a + gi, b - 1] = -2 * A
            expected[6 * b + gi, a - 1] = 2 * A
    ck('all24_link_K1_Z_entries', ex(Y - expected) == s.zeros(24, 3))
    g = s.Matrix([reduced(*v) for v in k1[0]['coeffs']])
    ck('null_K1_Z_raw', ex(g - s.Matrix([-s.I * (A + 4 * L2 / 3), -4 * s.I * L2 / 3, -4 * s.I * L2 / 3])) == s.zeros(3, 1))
    for i in range(3):
        for j in range(3):
            (pp, rem) = folded(*bg[i][j])
            ck('U2_DD_moment_' + str(i) + str(j), s.expand(pp - (32 * d2 * (x * x - Y2) if i == j else -32 * o2 * Y2)) == 0 and rem == 0)
            ck('U2_DD_vanish_' + str(i) + str(j), reduced(*bg[i][j]) == 0)
            ck('weight2_exact_fold_' + str(i) + str(j), s.expand(weight_poly[i][j] - (32 * (x * x - 3 * yy[i] ** 2) if i == j else -96 * yy[i] * yy[j])) == 0)
    K2 = s.Matrix(3, 3, lambda i, j: reduced(k2[i][j][0], s.sympify(k2[i][j][1], locals=loc) + s.sympify(lattice_dd[i][j], locals=loc)) + (-s.Rational(16, 3) * m4 if i == j else 24 * m22))
    kd = A + s.Rational(16, 3) * L4 + 64 * m22 + 32 * m4
    ko = s.Rational(16, 3) * L22 + 32 * m22
    ck('all_nine_K2_ZZ_entries', ex(K2 - s.Matrix(3, 3, lambda i, j: kd if i == j else ko)) == s.zeros(3))
    As = reduced(48, 48 + 16 * Y2)
    At = reduced(4, 4 + s.Rational(16, 3) * Y2)
    Av = s.Matrix([[reduced(8, 4 + 16 * xi ** 2), reduced(-8, -8)], [reduced(-8, -8), reduced(24, 24 + s.Rational(32, 3) * Y2)]])
    cs = reduced(-6, -6)
    cv = s.Matrix([reduced(2, 2), reduced(-4, -4)])
    vs = 8 * L2
    vv = s.Matrix([-2 * A, 4 * A])
    den = 3 * A + L2
    ck('scalar_gap_block', s.expand(As - 16 * den) == 0)
    ck('standard_gap_block', s.expand(At - s.Rational(4, 3) * (3 * A + 4 * L2)) == 0)
    ck('vector_gap_block', ex(Av - s.Matrix([[4 * A, -8 * A], [-8 * A, 24 * A + s.Rational(32, 3) * L2]])) == s.zeros(2))
    ck('vector_elimination_identity', s.factor((vv.T * Av.inv() * vv)[0] - A) == 0)
    tau = L2 * (3 * A + 4 * L2) / (3 * den)
    ss = s.Rational(16, 3) * (L4 + 2 * L22) + 128 * m22 + 32 * m4 - 12 * L2 ** 2 / den
    st = s.Rational(16, 3) * (L4 - L22) + 32 * m22 + 32 * m4
    ck('soft_singlet_schur', s.factor(kd + 2 * ko - 3 * vs ** 2 / As - (vv.T * Av.inv() * vv)[0] - ss) == 0)
    ck('soft_standard_schur', s.factor(kd - ko - (vv.T * Av.inv() * vv)[0] - st) == 0)
    ck('metric_soft_common_source', s.factor(-g[1] / s.I + vs * cs / As - tau) == 0)
    ck('metric_soft_anisotropy_cancel', s.factor((g[0] - g[1]) / s.I - (vv.T * Av.inv() * cv)[0]) == 0)
    nself = reduced(2 + 8 * xi ** 2 + s.Rational(8, 3) * Y2, 2 + 4 * xi ** 2 + 16 * xi ** 4 + s.Rational(4, 3) * Y2 - s.Rational(32, 3) * xi ** 2 * Y2 + s.Rational(16, 3) * Y4)
    nbar = A + s.Rational(4, 3) * L2 + s.Rational(16, 3) * L4 - 9 * A * A / (4 * den)
    ck('continuum_null_schur', s.factor(nself - cs ** 2 / As - (cv.T * Av.inv() * cv)[0] - nbar) == 0)
    reduced_output = dict(moments='m0=sum w; m4=sum w*x^4; m22=sum w*y1^2*y2^2; Lj=sum L*{1,Y2,Y4,Y22}. Y2=sum yi^2,Y4=sum yi^4,Y22=sum_i<j yi^2*yj^2. L=(w_l-w_k)/(2*x+1).', A=str(A), K1_links_Z=Y.tolist(), K1_null_Z=g.tolist(), K2_ZZ=K2.tolist(), gap_scalar=str(As), gap_standard=str(At), gap_vector=Av.tolist(), soft_singlet=str(ss), soft_standard=str(st), T1_imag=str(tau), null24=str(nbar), full_null_limit_div_C=str(nbar - 3 * tau * tau / ss), scale='For physical Fourier omega, C=c^2*omega^2, epsilon=h*omega. Metric and link variables both use dimensionless normal basis: physical link Omega=omega times this coordinate. K0=C*Kbar0; metric-soft t_h=C*epsilon*i*tau*ones+o(epsilon); soft S_h=C*epsilon^2*(ss*Psinglet+st*Pstandard)+o(epsilon^2). Full null Schur tends C*(null24-3*tau^2/ss). h times original observer response=-i*tau/(omega*ss)*ones.', scope='Assumes the owned exact proper-root moments, U_h=c eta+O(h^2), fixed-beta finite-B weight and stable Riesz shell convergence with enough weighted moments to pass this Taylor limit. No root existence or dominated convergence is proved by the algebra checker; no physical GR closure. No d2/o2, fit, heat-time truncation, dropped grades, or independent matter source is used.')
    out = dict(status='PASS_EXACT_FINITE_SOFT_SYMBOL', checks=checks, reduced=reduced_output, creator_pin=pin, halfedge='D_h(p)=exp(i h sum p_r N_r/2) [(2i/h)sum eta_r sin(h p_r/2)(C_r-I_r)] exp(-i h sum p_r N_r/2). The transformed symbol has no O(h) term; Delta_h=sum 4sin^2(hp_r/2)/h^2 is scalar.', convention='c=omega=1; x incoming time, outgoing x+1; each pair multiplies W=w_k+w_l, L=(w_l-w_k)/(2x+1). Outside c^2; replace L by c^2 Lphysical. avg independent signs of xi=x+1/2,y plus spatial permutations.', K1_field_Z=k1, K2_ZZ_raw=k2, weight2_folded=[[str(s.factor(a)) for a in row] for row in weight_poly], U2_E2background=bg, lattice_E2_DD=lattice_dd)
    return out


def exact_star_eh_normalization(root):
    root = Path(root)
    source = root / '02_REGISTRY/research/sources/d0_af_star_full_lattice_2026-10-17/check_full_lattice.py'
    nodes = []
    names = {'ETA', 'T', 'TI', 'G', 'STAR', 'SM'}
    for n in ast.parse(source.read_text()).body:
        if isinstance(n, ast.Assign) and any((isinstance(t, ast.Name) and t.id in names for t in n.targets)):
            nodes.append(n)
        elif isinstance(n, ast.For) and isinstance(n.iter, ast.Call) and isinstance(n.iter.func, ast.Attribute) and isinstance(n.iter.func.value, ast.Name) and (n.iter.func.value.id == 'SM'):
            nodes.append(n)
    pairs = list(combinations(range(4), 2))
    ns = dict(s=s, E=SimpleNamespace(PAIRS=pairs))
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(source), 'exec'), ns)
    (eta, T, G, star) = [ns[n] for n in ['ETA', 'T', 'G', 'STAR']]
    sourcepin = hashlib.sha256(ast.dump(ast.Module(body=nodes, type_ignores=[]), include_attributes=False).encode()).hexdigest()
    checks = []

    def ck(name, test):
        if not test:
            raise ArithmeticError(name)
        checks.append(name)
    ck('literal_star_pin', sourcepin == 'eab41dd2fbc14213356d461dfe587f7f0443e95d0102c09c401d3a2a601ed467')
    eps = s.LeviCivita
    zero = lambda : s.zeros(4)
    Em = s.Matrix(6, 6, lambda i, j: eps(*pairs[i], *pairs[j]))
    ck('literal_G2STAR_minus_epsilon', G * star == -Em)
    ck('literal_null_orientation_T', T.det() == -1 and T.T * eta * T == s.Matrix([[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, -1, 0], [0, 0, 0, -1]]))
    e = s.Matrix(4, 4, lambda i, j: s.Symbol('e' + str(i) + str(j), real=True))
    det = e.det()
    adj = e.adjugate()
    wedge = lambda u, v: s.Matrix([u[a] * v[b] - u[b] * v[a] for (a, b) in pairs])
    for (r, t) in pairs:
        (u, v) = [j for j in range(4) if j not in (r, t)]
        for (ai, (a, b)) in enumerate(pairs):
            C = s.zeros(6, 1)
            C[ai] = 1
            P = eps(r, t, u, v) * (wedge(e[:, u], e[:, v]).T * G * star * C)[0]
            ric_numerator = 2 * (adj[r, a] * adj[t, b] - adj[r, b] * adj[t, a])
            ck('arbitrary_coframe_curvature_' + str(r) + str(t) + '_' + str(a) + str(b), s.expand(det * P + ric_numerator / 2) == 0)
    B = s.zeros(4)
    B[0, 1] = B[1, 0] = 1
    Fb = {(0, 1): B}

    def density(ee, faces):
        out = 0
        for ((r, t), F) in faces.items():
            (u, v) = [j for j in range(4) if j not in (r, t)]
            FC = F * eta
            cv = s.Matrix([FC[a, b] for (a, b) in pairs])
            out += eps(r, t, u, v) * (wedge(ee[:, u], ee[:, v]).T * G * star * cv)[0]
        return s.factor(out)

    def scalar_curv(ee, faces):
        ei = ee.inv()
        out = 0
        for ((r, t), F) in faces.items():
            FC = F * eta
            out += 2 * sum((ei[r, a] * ei[t, b] * FC[a, b] for a in range(4) for b in range(4)), s.S(0))
        return s.factor(out)
    ck('positive_orientation_unit_curvature', density(s.eye(4), Fb) == 1 and scalar_curv(s.eye(4), Fb) == -2)
    neg = s.diag(-1, 1, 1, 1)
    ck('negative_orientation_unit_curvature', density(neg, Fb) == 1 and scalar_curv(neg, Fb) == 2)
    PP = 0
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    PP += s.Rational(1, 2) * eps(a, b, c, d) * eps(a, b, 0, 1) * (B * eta)[c, d]
    ck('literal_standard_Palatini_unit', PP == -2)
    cp = root / '02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py'
    cn = next((n for n in ast.parse(cp.read_text()).body if isinstance(n, ast.FunctionDef) and n.name == 'creator'))
    cpin = hashlib.sha256(ast.dump(cn, include_attributes=False).encode()).hexdigest()
    ck('creator_pin', cpin == '801b33d7ef3e41f6425be16153c82b1402215f6be757ea275ff06a69010f58e4')
    cns = dict(s=s, SUBS=[tuple((i for i in range(4) if mask & 1 << i)) for mask in range(16)])
    exec(compile(ast.Module(body=[cn], type_ignores=[]), str(cp), 'exec'), cns)
    Cr = [cns['creator'](s.eye(4)[:, a]) for a in range(4)]
    Gam = [Cr[a] + eta[a, a] * Cr[a].T for a in range(4)]
    for a in range(4):
        for b in range(4):
            ck('full16_Clifford_trace_' + str(a) + str(b), s.trace(Gam[a] * Gam[b]) / 16 == eta[a, b])
    (hh, amp) = s.symbols('H amp', real=True)
    en = s.eye(4)
    en[1, 0] = hh / 2
    eo = T * en
    etaN = T.T * eta * T
    ko = s.Matrix([amp, 0, 0, 0])
    gg = eo.T * eta * eo
    correct = (ko.T * eo.inv() * eta * eo.inv().T * ko)[0]
    incorrect = (ko.T * eo.inv().T * eta * eo.inv() * ko)[0]
    ck('coframe_inverse_transpose_null', s.simplify(correct) == 0 and s.simplify((ko.T * gg.inv() * ko)[0]) == 0)
    ck('old_displayed_inverse_is_not_valid_column_convention', s.simplify(incorrect) != 0)
    rr = s.symbols('rr', positive=True)
    ck('density_dressing_same_gamma', density(rr * s.eye(4), Fb) == rr ** 2 and scalar_curv(rr * s.eye(4), Fb) == -2 / rr ** 2)
    return dict(status='PASS', checks=checks, literal_star_AST_sha256=sourcepin, creator_AST_sha256=cpin, unit=dict(face='01', F='B01=E01+E10', e='I', Pstar=1, R=-2, Palatini=-2), identity='Pstar=-(c_star/2) det(e) R(e,omega); normalized checker has c_star=1. Equivalently Pstar=-(c_star/2)*(1/2 epsilon_abcd e^a wedge e^b wedge F^cd).', density_gamma='For J=abs(det e), gamma_star=-(c_star/2)*sgn(det e) on each nondegenerate orientation component. Positive density dressing preserves this sign.', old_local='The literal old null-frame e has owned-diagonal representative T*e_null, det T=-1 and det e_null=+1. Thus its gamma_star=+1/2 relative to J R, and kappa=-2 lambda_mat, matching old Ric_uu=-2 Lambda_sigma s^2 without a pp-wave fit.', full16='Tr16 Gamma(v)^2 /16=v^T eta v; no extra16 or128 enters gamma. With column coframe, v=e^-T Dpsi.', source='The 36 exact arbitrary-coframe curvature coefficient identities imply the full16 coframe first-source identity and all independent curvature/connection sources by differentiation. This is a local algebraic normalization, not finite-root existence or native whole-price admission.')


def graded_density_intertwiner(root):
    root = Path(root)
    source = root / '02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py'
    creator = next((n for n in ast.parse(source.read_text()).body if isinstance(n, ast.FunctionDef) and n.name == 'creator'))
    pin = hashlib.sha256(ast.dump(creator, include_attributes=False).encode()).hexdigest()
    if pin != '801b33d7ef3e41f6425be16153c82b1402215f6be757ea275ff06a69010f58e4':
        raise ArithmeticError('literal creator pin')
    subs = [tuple((i for i in range(4) if mask & 1 << i)) for mask in range(16)]
    ns = dict(s=s, SUBS=subs)
    exec(compile(ast.Module(body=[creator], type_ignores=[]), str(source), 'exec'), ns)
    C = [ns['creator'](s.eye(4)[:, i]) for i in range(4)]
    N = s.diag(*map(len, subs))
    I = s.eye(16)
    (a, ax, ay) = s.symbols('a ax ay', positive=True)
    A = lambda b: s.diag(*[b ** (2 - len(q)) for q in subs])
    zero = s.zeros(16)
    checks = []

    def ck(name, value):
        if not value:
            raise ArithmeticError(name)
        checks.append(name)
    ck('full16 grade multiplicities', [sum((len(q) == k for q in subs)) for k in range(5)] == [1, 4, 6, 4, 1])
    ck('amplitude square equals OWNED pairing weight', A(a).T * A(a) == s.diag(*[a ** (4 - 2 * len(q)) for q in subs]))
    ck('amplitude is volume/degree exterior lift', A(a) == a ** 2 * s.diag(*[a ** (-len(q)) for q in subs]))
    ck('full16 determinant one', s.simplify(A(a).det()) == 1)
    for (i, c) in enumerate(C):
        ck(f'creator[{i}] conjugates to density-dressed operator', s.simplify(A(a) * c * A(a).inv() - c / a) == zero)
        ck(f'annihilator[{i}] has inverse scale', s.simplify(A(a) * c.T * A(a).inv() - a * c.T) == zero)
        ck(f'number commutator creator[{i}]', N * c - c * N == c)
    ck('identity grading connection', s.simplify(A(ax) * A(ay).inv() - A(ax / ay)) == zero)
    for (i, c) in enumerate(C):
        ck(f'actual edge[{i}] includes relative grading connection', s.simplify(A(ax) * c * A(ay).inv() - c / ax * A(ax / ay)) == zero)
    ck('edge grading term cannot be proper Lorentz', A(ax / ay)[0, 0] == (ax / ay) ** 2 and A(ax / ay)[15, 15] == (ay / ax) ** 2)
    ck('fixed counting CAR not an isometry', A(s.Integer(2)).T * A(s.Integer(2)) != I)
    ck('graded pairing differs from uniform density multiplier', A(s.Integer(2)) != 2 * I)
    for k in range(5):
        idx = [j for (j, q) in enumerate(subs) if len(q) == k]
        for i in idx:
            for j in idx:
                ck(f'generic grade{k} pairing coefficient {i},{j}', s.simplify(A(a)[i, i] * A(a)[j, j] - a ** (4 - 2 * k)) == 0)
    Q = I - N / 2
    ck('connection grading generator', s.diff(A(a), a).subs(a, 1) / 2 == Q)
    ck('connection is flat by scalar potential', s.simplify(A(ax) * A(ay).inv() * A(ay) * A(a).inv() - A(ax) * A(a).inv()) == zero)
    Draw = s.I * (C[0] - C[0].T)
    Dconj = s.simplify(A(a) * Draw * A(a).inv())
    Dcount = s.I * (C[0] / a - C[0].T / a)
    ck('raw complete CAR16 one-leg square', s.simplify(Draw ** 2 - I) == zero)
    ck('true conjugated square unchanged', s.simplify(Dconj ** 2 - I) == zero)
    ck('counting-adjoint rebuilding square changes', s.simplify(Dcount ** 2 - I / a ** 2) == zero)
    ck('dressed counting Dirac differs from weighted conjugation', Dcount.subs(a, 2) != Dconj.subs(a, 2))
    return dict(status='PASS', checks=checks, creator_AST_sha256=pin, chi_convention='a=sqrt(chi), chi=mu/mubar, ghat=chi*g_raw, qraw=chi*qhat', amplitude='A_chi=chi^(1-N/2), NOT the weight W_chi=chi^(2-N)', exact_pairing='A_chi^T W(qhat,mhat) A_chi=W(qraw,mraw); mhat=A_chi*mraw and observer radial rescaling leaves its line unchanged', local_operator='A_chi X A_chi^-1=chi^-1/2 X for X=C(u)rho(M), with M grade-preserving', actual_edge='A_x X_xy A_y^-1=chi_x^-1/2 X_xy (chi_x/chi_y)^(1-N/2)', connection='Q=I-N/2; edge factor=exp[Q*(log chi_x-log chi_y)], a flat exact grading/density connection', continuum='A_chi partial_mu A_chi^-1=partial_mu-Q*partial_mu log(chi) for the degree-preserving fiber derivative. Thus A_chi d A_chi^-1=chi^-1/2 sum_mu C(dx_mu)[partial_mu-Q*partial_mu log(chi)], with Q acting on the incoming grade. Creator scaling must not be omitted.', proper_Lorentz_obstruction='rho(M) fixes grade0/4; new relative factor scales them by chi_x/chi_y and inverse. Cannot delete it while claiming the old proper-Lorentz word.', complete_CAR16_adjoint_counter='D=i(C0-C0^T) has D^2=I. A D A^-1 still squares to I. Rebuilding Dcount=i chi^-1/2(C0-C0^T) with the OLD counting adjoint squares to I/chi. Hence its full16 heat trace is 16 exp(-beta/chi), not 16 exp(-beta). Weighted isometry alone does not preserve the old price.', scope='Exact kinematic weighted-Hilbert intertwiner. It does not establish fixed-counting CAR unitarity, old cut/preparation/adjoint transport, equality of whole native price, independently derived spin stress, or Einstein recovery. Existing full H+J+R soft-source obstruction is not changed.')


def native_moving_query(root=None):
    checks = []

    def ck(name, test):
        if not bool(test):
            raise ArithmeticError(name)
        checks.append(name)
    (u, x, theta) = s.symbols('u x theta', real=True)
    F = x + theta * (x * x - x)
    M = s.Rational(3, 2)
    Phi = s.expand(x + (u - F) / M)
    ck('CDF_unit_endpoints', F.subs(x, 0) == 0 and F.subs(x, 1) == 1)
    ck('CDF_density', s.diff(F, x) == 1 + theta * (2 * x - 1))
    ck('CDF_uniform_positive_window', s.simplify(s.diff(F, x).subs({theta: s.Rational(1, 2), x: 0})) == s.Rational(1, 2))
    ck('CDF_upper_window', s.simplify(s.diff(F, x).subs({theta: s.Rational(1, 2), x: 1})) == s.Rational(3, 2))
    ck('inverse_iteration_lower_endpoint', s.expand(Phi.subs(x, 0) - u / M) == 0)
    ck('inverse_iteration_upper_endpoint', s.expand(Phi.subs(x, 1) - (1 - (1 - u) / M)) == 0)
    ck('inverse_iteration_derivative', s.expand(s.diff(Phi, x) - (1 - s.diff(F, x) / M)) == 0)
    a = u - u * u
    b = 2 * (1 - 2 * u) * a
    Tjet = u + theta * a + theta ** 2 * b / 2
    residual = s.Poly(s.expand(F.subs(x, Tjet) - u), theta)
    for j in range(3):
        ck('inverse_CDF_jet_' + str(j), residual.coeff_monomial(theta ** j) == 0)
    an = bn = s.S(0)
    r = s.Rational(1, 3)
    for n in range(1, 17):
        (an, bn) = (s.expand(r * an + (1 - r) * a), s.expand(r * bn + 2 * (1 - r) * (1 - 2 * u) * an))
        ck('static_inverse_first_jet_' + str(n), s.expand(an - a * (1 - r ** n)) == 0)
        ck('static_inverse_second_jet_' + str(n), s.expand(bn - b * (1 - r ** n - (1 - r) * n * r ** (n - 1))) == 0)
    ck('frozen_sample_has_nonzero_cell_mass_source', s.diff(F, theta).subs(x, s.Rational(1, 2)) == -s.Rational(1, 4))
    ck('moving_query_source_is_present', s.expand(s.diff(Tjet ** 2, theta).subs(theta, 0) - 2 * u * (u - u * u)) == 0)
    (aa, bb) = s.symbols('angle0 angle1', real=True)
    rot = lambda t: s.Matrix([[s.cos(t), -s.sin(t)], [s.sin(t), s.cos(t)]])
    P0 = s.diag(1, 0)
    P1 = s.eye(2) - P0
    Word = s.kronecker_product(P0, rot(aa)) + s.kronecker_product(P1, rot(bb))
    for (i, Pleaf) in enumerate((P0, P1)):
        Q = s.kronecker_product(Pleaf, s.eye(2))
        ck('actual_leaf_guard_commutator_' + str(i), Word * Q - Q * Word == s.zeros(4))
    V = s.kronecker_product(rot(aa), P0) + s.kronecker_product(rot(bb), P1)
    P = s.kronecker_product(P0, P0)
    Pwrong = s.kronecker_product(P0, s.eye(2))
    simp = lambda A: A.applyfunc(s.trigsimp)
    feed = lambda W, Q: simp(Q * W.T * (s.eye(4) - Q) * W * Q)
    FF = feed(V, P)
    Fwrong = feed(V, Pwrong)
    ck('whole_unitary_completion', simp(V.T * V) == s.eye(4))
    ck('feedback_on_actual_retained_cut', simp(FF - s.sin(aa) ** 2 * P) == s.zeros(4))
    ck('all_input_complement_feedback_zero', FF * (s.eye(4) - P) == s.zeros(4))
    ck('wrong_Iwork_cut_adds_feedback', simp(Fwrong - s.sin(aa) ** 2 * P - s.sin(bb) ** 2 * s.kronecker_product(P0, P1)) == s.zeros(4))
    z = s.symbols('z', real=True)
    ck('same_full_feedback_determinant', s.factor((s.eye(4) - z * FF).det()) == 1 - z * s.sin(aa) ** 2)
    ck('wrong_cut_changes_determinant', s.simplify((s.eye(4) - z * Fwrong).det() - (1 - z * s.sin(aa) ** 2) * (1 - z * s.sin(bb) ** 2)) == 0)
    leak = s.symbols('leak', real=True)
    Veps = s.kronecker_product(s.eye(2), rot(leak)) * V
    Feps = feed(Veps, P)
    ck('all_workspace_leakage_outputs_count', simp(Feps - (s.sin(aa) ** 2 + s.cos(aa) ** 2 * s.sin(leak) ** 2) * P) == s.zeros(4))
    (pi0, pi1, theta0, theta1) = s.symbols('pi0 pi1 theta0 theta1', real=True)
    Trace = s.diag(pi0, pi1)
    H = s.diag(theta0, theta1)
    ck('fixed_trace_weight_factorization', s.trace(Trace * H) == pi0 * theta0 + pi1 * theta1)
    return dict(status='PASS_EXACT_MOVING_QUERY_AND_FEEDBACK_CUT', checks=checks, inverse_CDF=dict(map=str(Phi), window='|theta|<=1/2, x,u in[0,1]', density_bounds=['1/2', '3/2'], fixed_M='3/2', contraction='2/3', generic='For 0<m<=Fprime<=M, F(0)=0,F(1)=1, x_next=x+(u-F(x))/M maps[0,1] to itself and contracts by q=1-m/M. M is fixed on one field chart, not varied with the field. q=0 is the constant-density one-step case.', first_inverse_jet=str(a), second_inverse_jet=str(b), C2_rate='C(1+N)^2 q^(N-2) on a fixed C3-bounded positive chart; all four triangular stages retain this rate with larger constants. C3 version uses a C4-bounded chart and C(1+N)^3 q^(N-3).'), implementation='At fixed h and macro cut, compile angle_i(z)=theta(r_h(T_(J/V)(c_i);z),q_h(T_(J/V)(c_i);z)) directly as a smooth analytic function of a finite collection of ACTUAL continuous Julia/scalar query operands. Use a fixed analytic interpolation/evaluation model and fixed inverse-CDF iterations; a merely smooth model instead uses the owned C3 approximation with actual higher-derivative bounds, without an asserted analytic rate. This is an address-controlled operand word, not a change to golden p/p^2 branching.', branch_law='A structured block word sum_i P_i LEFT tensor W_i commutes with every old leaf projector. Hence Tr(rho P_i) is preserved for every input rho, including unknown correlations. It need not equal pi_i or PF mu_i. The J2 weights pi_i=D_type(i)/K are regular trace multiplicities; Binet supplies their PF limit without any Born preparation law.', exact_cut='With actual P=P_old tensor |0work><0work|, a complete ideal macro satisfying U_ideal(v tensor0)=(U_old v)tensor0 for ALL old input columns gives F_ideal=F_old tensor |0><0| and det(I-z F_ideal)=det(I-z F_old). F=0 on every INPUT complement due to the actual P compression. Arbitrary offblank U action is retained and need not be identity. Clean return on ONE state is insufficient.', finite_compiler='For whole-output operator C3 error eta on the actual retained input cut, existing6.19 gives ||J_U-J_V||C3<=2^14*z*r*L^6*eta/(1-z)^4. All leaked OUTPUT sectors belong to I-P and contribute to F. No reset, postselection, additive controller Shannon price or discarded complement is used.', source_budget='After normalization by nu*K*a0*c_AF*t^2, compiler error<=2^14*z*r*L^6*eta/[(1-z)^4*nu*K*a0*c_AF*t^2]. Operand-evaluation error delta in (r_h,q_h) propagates as Cdelta because Dj_t/Dr,Dj_t/Dq=O(t^2). delta must include h^-4*star interpolation and every field/address jet; a bare nearest-cell map has no C2 guarantee.', remaining=['actual native admission of coherent Julia/scalar operands and scalar work/return test', 'unknown raw matter amplitudes are not supplied as readable scalar queries', 'physical interpolation/evaluation and actual finite word runtime/cut binding', 'other H/R, preparation, controller and immutable history terms need their OWN complete price/source theorem', 'this is a constructive J2 query-source consumer, not compulsory selection, nonlinear finite roots or D0=>GR'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[4])
    parser.add_argument('--output', type=Path, help='write exactly this receipt; default read-only')
    args = parser.parse_args()
    result = dict(status='PASS',
        null_symbol=null_symbol(args.root),
        full_normal_blocks=full_normal_blocks(args.root),
        continuum_null_interval=null_interval(args.root),
        finite_soft_symbol=soft_symbol(args.root),
        finite_soft_interval=soft_interval(args.root),
        general_matter_source=general_source(args.root),
        exact_star_normalization=exact_star_eh_normalization(args.root),
        graded_density_bridge=graded_density_intertwiner(args.root),
        moving_query_and_actual_cut=native_moving_query(args.root),
        GR_closed=False, native_execution_forced=False,
        generic_joint_critical_recovery=False)
    output = json.dumps(result, ensure_ascii=False, indent=2, default=str)+'\n'
    if args.output:
        args.output.write_text(output)
    print(output, end='')


if __name__ == '__main__':
    main()
