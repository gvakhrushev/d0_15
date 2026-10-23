#!/usr/bin/env python3
"""Exact full16 scalar-symbol consumers; no old suite or momentum census."""
import argparse,ast,hashlib,json
from pathlib import Path
import sympy as s
def lapse_traces(root):
    root = Path(root).resolve()
    path = '02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py'
    node = next((n for n in ast.parse((root / path).read_text()).body if isinstance(n, ast.FunctionDef) and n.name == 'creator'))
    pin = hashlib.sha256(ast.dump(node, include_attributes=False).encode()).hexdigest()
    if not pin == '801b33d7ef3e41f6425be16153c82b1402215f6be757ea275ff06a69010f58e4':
        raise ArithmeticError("Exact control failed: pin == '801b33d7ef3e41f6425be16153c82b1402215f6be757ea275ff06a69010f58e4'")
    ns = {'s': s, 'SUBS': [tuple((i for i in range(4) if m & 1 << i)) for m in range(16)]}
    exec(compile(ast.Module(body=[node], type_ignores=[]), path, 'exec'), ns)
    C = [ns['creator'](s.eye(4)[:, i]) for i in range(4)]
    I = [v.T for v in C]
    gamma = [C[i] - I[i] for i in range(4)]
    hat = [C[i] + I[i] for i in range(4)]
    N = [C[i] * I[i] for i in range(4)]
    Nsp = sum(N[1:], s.zeros(16))
    Gamma = lambda O: sum((O[i, j] * C[i] * I[j] for i in range(4) for j in range(4)), s.zeros(16))
    (x, omega) = s.symbols('x omega', real=True)
    y = s.symbols('y1:4', real=True)
    c = s.symbols('c', positive=True)
    d = c * c
    l = x + omega
    Y = sum((y[i - 1] * gamma[i] for i in range(1, 4)), s.zeros(16))
    Dk = s.I * c * (x * gamma[0] - Y)
    Dl = s.I * c * (l * gamma[0] - Y)
    Vp = s.I * c * (x * C[0] - l * I[0])
    Vn = c * Nsp * hat[0]
    Qp = s.expand(Dl * Vp + Vp * Dk)
    Qn = s.expand(Dl * Vn + Vn * Dk)
    if not s.expand(Qp - d * (2 * x * l * s.eye(16) + omega ** 2 * N[0])) == s.zeros(16):
        raise ArithmeticError('Exact control failed: s.expand(Qp - d * (2 * x * l * s.eye(16) + omega ** 2 * N[0])) == s.zeros(16)')
    Qn_expected = s.I * d * (omega * Nsp * (2 * N[0] - s.eye(16)) + sum((y[i - 1] * hat[i] * hat[0] for i in range(1, 4)), s.zeros(16)))
    if not s.expand(Qn - Qn_expected) == s.zeros(16):
        raise ArithmeticError('Exact control failed: s.expand(Qn - Qn_expected) == s.zeros(16)')
    inner = lambda A, B: s.expand(s.trace(A.conjugate().T * B))
    expected = {'Vp_norm2': 8 * d * (x * x + l * l), 'Qp_norm2': 8 * d * d * (8 * x * x * l * l + 4 * x * l * omega * omega + omega ** 4), 'Vp_Vn': 12 * s.I * d * omega, 'Qp_Qn': 12 * s.I * d * d * omega ** 3, 'Vn_norm2': 48 * d, 'Qn_norm2': d * d * (48 * omega * omega + 16 * sum((v * v for v in y)))}
    actual = {'Vp_norm2': inner(Vp, Vp), 'Qp_norm2': inner(Qp, Qp), 'Vp_Vn': inner(Vp, Vn), 'Qp_Qn': inner(Qp, Qn), 'Vn_norm2': inner(Vn, Vn), 'Qn_norm2': inner(Qn, Qn)}
    for key in expected:
        if not s.expand(actual[key] - expected[key]) == 0:
            raise ArithmeticError('Exact control failed: s.expand(actual[key] - expected[key]) == 0')
    B = s.zeros(4)
    for i in range(1, 4):
        B[0, i] = B[i, 0] = 1
    VB = s.I * c * (x * sum(gamma[1:], s.zeros(16)) - sum(y) * gamma[0] - omega * sum(I[1:], s.zeros(16)))
    families = []
    fam = [s.zeros(4) for _ in range(4)]
    fam[0] = B
    families.append(fam)
    fam = [s.zeros(4) for _ in range(4)]
    for i in range(1, 4):
        for j in range(1, 4):
            if j != i:
                fam[i][0, j] += 1
                fam[i][j, 0] += 1
    families.append(fam)
    fam = [s.zeros(4) for _ in range(4)]
    for i in range(1, 4):
        for j in range(1, 4):
            if j != i:
                fam[i][i, j] += 1
                fam[i][j, i] -= 1
    families.append(fam)
    other = [VB]
    eta = s.diag(1, -1, -1, -1)
    for fam in families:
        A = sum((c * eta[r, r] * C[r] * Gamma(fam[r]) for r in range(4)), s.zeros(16))
        other.append(A + A.T)

    def sign_even(poly):
        P = s.Poly(s.expand(poly), *y)
        return s.expand(sum((coeff * s.prod((v ** power for (v, power) in zip(y, powers))) for (powers, coeff) in P.terms() if all((power % 2 == 0 for power in powers))), s.S(0)))
    controls = {}
    for (name, V) in zip(['coframeboost', 'link1', 'link3', 'link4'], other):
        Q = s.expand(Dl * V + V * Dk)
        a = inner(Vp, V)
        b = inner(Qp, Q)
        if not (sign_even(a) == 0 and sign_even(b) == 0):
            raise ArithmeticError('Exact control failed: sign_even(a) == 0 and sign_even(b) == 0')
        controls[name] = {'Vp_V': str(s.factor(a)), 'Qp_Q': str(s.factor(b)), 'independent_spatial_sign_even_projection': [0, 0]}
    return {'status': 'PASS', 'creator_AST_sha256': pin, 'CAR_dimension': 16, 'price_scope': 'continuum limit of actual S8 heat+feedback+fixedRIGHT rank128 Riesz price, full spectral weights; no new action', 'parameters': 'U=c eta,d=c^2;l0=x+omega;q=(omega,0,0,0);x,y physicalFouriermomenta', 'Qp': 'd[2x(x+omega) I+omega^2 N0]', 'Qn': 'i d[omega Nsp(2N0-I)+sum_i yi hatgamma_i hatgamma_0]', 'traces': {key: str(s.factor(value)) for (key, value) in expected.items()}, 'other_normal_crosses': controls, 'decoupling_assumptions': 'full signed spatial momentum sum; spectral and Riesz weights even in every yi; properDab weightedtrace cancelled by owned jointrootmoments', 'one_normal_lapse_Schur': 'C_lapse=A-|B|^2/Cnormal ifCnormal!=0; no inverse of singular5normalmatrix', 'remaining_metric_warning': 'I_spatial isalsoinvariant scalar: lapse-to-I_spatial metriccoupling isnotforbidden bysignsymmetry', 'native_finite_h_warning': 'spatialreflection symmetry here usescontinuum ik symbols; no exactfiniteforward-stencil symmetry or finiteSchur limit proved', 'interval_certificate_claimed': False, 'native_finite_root_GR_claimed': False}

def kernel(root):
    root = Path(root).resolve()
    path = '02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py'
    node = next((n for n in ast.parse((root / path).read_text()).body if isinstance(n, ast.FunctionDef) and n.name == 'creator'))
    pin = hashlib.sha256(ast.dump(node, include_attributes=False).encode()).hexdigest()
    if not pin == '801b33d7ef3e41f6425be16153c82b1402215f6be757ea275ff06a69010f58e4':
        raise ArithmeticError("Exact control failed: pin == '801b33d7ef3e41f6425be16153c82b1402215f6be757ea275ff06a69010f58e4'")
    ns = {'s': s, 'SUBS': [tuple((i for i in range(4) if m & 1 << i)) for m in range(16)]}
    exec(compile(ast.Module(body=[node], type_ignores=[]), path, 'exec'), ns)
    C = [ns['creator'](s.eye(4)[:, i]) for i in range(4)]
    I = [c.T for c in C]
    cl = [C[i] - I[i] for i in range(4)]
    creator = lambda v: sum((v[i] * C[i] for i in range(4)), s.zeros(16))
    Gamma = lambda O: sum((O[i, j] * C[i] * I[j] for i in range(4) for j in range(4)), s.zeros(16))
    generators = []
    for i in range(1, 4):
        O = s.zeros(4)
        O[0, i] = O[i, 0] = 1
        generators.append(O)
    for (i, j) in [(1, 2), (1, 3), (2, 3)]:
        O = s.zeros(4)
        O[i, j] = 1
        O[j, i] = -1
        generators.append(O)
    eta = s.diag(1, -1, -1, -1)
    fam = [[s.zeros(4) for _ in range(4)] for _ in range(4)]
    fam[0][0] = sum(generators[:3], s.zeros(4))
    for i in range(1, 4):
        fam[1][i] = generators[i - 1]
        fam[2][i] = sum((generators[j - 1] for j in range(1, 4) if j != i), s.zeros(4))
        for j in range(1, 4):
            if j != i:
                fam[3][i][i, j] += 1
                fam[3][i][j, i] -= 1
    link = []
    for family in fam:
        A = sum((eta[r, r] * C[r] * Gamma(family[r]) for r in range(4)), s.zeros(16))
        link.append(A + A.T)
    flat = s.Matrix.hstack(*[V.reshape(256, 1) for V in link])
    if not flat.rank() == 4:
        raise ArithmeticError('Exact control failed: flat.rank() == 4')
    gram = s.Matrix(4, 4, lambda a, b: s.trace(link[a] * link[b]))
    if not gram == s.Matrix([[24, 0, 0, 24], [0, 48, 0, 0], [0, 0, 24, 0], [24, 0, 0, 72]]):
        raise ArithmeticError('Exact control failed: gram == s.Matrix([[24, 0, 0, 24], [0, 48, 0, 0], [0, 0, 24, 0], [24, 0, 0, 72]])')
    R = s.zeros(4)
    B = s.zeros(4)
    for i in range(1, 4):
        R[0, i] = 1
        R[i, 0] = -1
        B[0, i] = B[i, 0] = 1
    GR = Gamma(R)
    if not GR.T == -GR:
        raise ArithmeticError('Exact control failed: GR.T == -GR')
    if not cl[0] * GR + sum(I[1:], s.zeros(16)) + link[0] == s.zeros(16):
        raise ArithmeticError('Exact control failed: cl[0] * GR + sum(I[1:], s.zeros(16)) + link[0] == s.zeros(16)')
    k = s.Matrix(s.symbols('k0:4', real=True))
    Q = s.symbols('Q', nonzero=True, real=True)
    l = k + s.Matrix([Q, 0, 0, 0])
    D = lambda momentum: s.I * sum((eta[r, r] * momentum[r] * cl[r] for r in range(4)), s.zeros(16))
    (Dk, Dl) = (D(k), D(l))
    VB = s.I * (k[0] * sum(cl[1:], s.zeros(16)) - sum(k[1:]) * cl[0] - Q * sum(I[1:], s.zeros(16)))
    T = 2 * sum(k[1:]) * s.eye(16) / Q - GR
    Vz = VB - s.I * Q * link[0]
    if not s.expand(Vz - (T * Dk - Dl * T)) == s.zeros(16):
        raise ArithmeticError('Exact control failed: s.expand(Vz - (T * Dk - Dl * T)) == s.zeros(16)')
    Ek = sum((x * x for x in k))
    El = sum((x * x for x in l))
    if not s.expand(Dl * Vz + Vz * Dk - (Ek - El) * T) == s.zeros(16):
        raise ArithmeticError('Exact control failed: s.expand(Dl * Vz + Vz * Dk - (Ek - El) * T) == s.zeros(16)')
    Z = []
    for r in range(4):
        for O in generators:
            A = eta[r, r] * C[r] * Gamma(O)
            Z.append(A + A.T)
    Zflat = s.Matrix.hstack(*[z.reshape(256, 1) for z in Z])
    if not Zflat.rank() == 24:
        raise ArithmeticError('Exact control failed: Zflat.rank() == 24')
    zg = Zflat.T * Zflat

    def in_Z(A):
        v = A.reshape(256, 1)
        coeff = zg.inv() * Zflat.T * v
        if not Zflat * coeff == v:
            raise ArithmeticError('Exact control failed: Zflat * coeff == v')
        return coeff
    E = s.eye(4)
    basis = [E[:, 0] * E[:, 0].T, R, s.diag(0, 1, 1, 1), s.diag(0, 0, 0, 0), B]
    for i in range(1, 4):
        for j in range(1, 4):
            if i != j:
                basis[3][i, j] = 1
    mixed_controls = 0
    for S in basis:
        v = [S * eta[:, r] for r in range(4)]
        V = lambda momentum: s.I * sum((momentum[r] * creator(v[r]) - (momentum[r] + (Q if r == 0 else 0)) * creator(v[r]).T for r in range(4)), s.zeros(16))
        L = s.expand(T.T.conjugate() * V(k) - V(k - s.Matrix([Q, 0, 0, 0])) * T.T.conjugate())
        dv = [R * v[r] + (2 * v[0] if r > 0 else s.zeros(4, 1)) for r in range(4)]
        homogeneous = s.I * sum((k[r] * (creator(dv[r]) - creator(dv[r]).T) for r in range(4)), s.zeros(16))
        rest = s.expand((L - homogeneous) / (s.I * Q))
        expected = creator(v[0]) * GR - GR * creator(v[0]).T
        if not s.expand(rest - expected) == s.zeros(16):
            raise ArithmeticError('Exact control failed: s.expand(rest - expected) == s.zeros(16)')
        in_Z(rest)
        mixed_controls += 1
    for V in link:
        in_Z(GR * V - V * GR)
        mixed_controls += 1
    return {'status': 'PASS', 'creator_AST_sha256': pin, 'CAR_dimension': 16, 'scope': 'continuum isotropic U=sqrt(d)eta; full heat+feedback+fixedRIGHT Riesz objective; not finiteh exactkernel', 'link_operator_rank': 4, 'link_Gram_div_d': gram.tolist(), 'normal_order': ['coframeBsum', 'scalarlink1', 'scalarlink2', 'scalarlink3', 'scalarlink4'], 'normal_kernel': 'z=(1,-iQ,0,0,0),Q=physicalq0;Q=2pi forfirsttorusmode', 'commutator_identity': 'Vz=Tq Dk-Dl Tq;Tq=(2sum_spatial ki/Q)I-Gamma(R);R=sum_i(E0i-Ei0)', 'Delta_identity': 'Qz=(Ek-El)Tq (allenergiesincludecommonfactor d)', 'constant_CAR_identity': 'gamma0 Gamma(R)+sum_i I_i+Vlink1/sqrt(d)=0', 'native_zero_order_image_rank': 24, 'mixed_closure_controls': mixed_controls, 'mixed_metric_compatibility': 'H(z,x)=0 forall4metriccolumns atfull homogeneous coframe/linkroot,usingfullproperDabrootmomentcancellation', 'mixed_proof': 'term1+divideddifference=2sum_k wk tr Dk [Tq*Vx(k)-Vx(k-q)Tq*];bracketisownedhomogeneouscoframejet+native24zeroorderjet;theirfirstsourcesvanish', 'quotient': 'chooseboostcoefficient0 by subtractingmultipleofz;solve4linkblock B onlyifnonsingular;kernelcompatibility z*mix=0required', 'Schur': 'ifnormalN=[[a,c*],[c,B]],c=iQ B e1 anda=Q^2 B11;mixboost=-iQ mixlink1;reducedmetric=Kgg-KgL B^-1 KLg', 'not_original_Lorentz_gauge': 'coordinatevolume-preservingspatialshearplusEuclideanCARframerotation;all16andreference128retained', 'finite_h_claimed': False, 'normal_quotient_nonsingularity_claimed': False}

def time_pullback_ward(root):
    root = Path(root).resolve()
    path = '02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py'
    node = next((n for n in ast.parse((root / path).read_text()).body if isinstance(n, ast.FunctionDef) and n.name == 'creator'))
    pin = hashlib.sha256(ast.dump(node, include_attributes=False).encode()).hexdigest()
    if not pin == '801b33d7ef3e41f6425be16153c82b1402215f6be757ea275ff06a69010f58e4':
        raise ArithmeticError("Time pullback exact identity failed: pin == '801b33d7ef3e41f6425be16153c82b1402215f6be757ea275ff06a69010f58e4'")
    ns = {'s': s, 'SUBS': [tuple((i for i in range(4) if m & 1 << i)) for m in range(16)]}
    exec(compile(ast.Module(body=[node], type_ignores=[]), path, 'exec'), ns)
    C = ns['creator'](s.Matrix([1, 0, 0, 0]))
    I = C.T
    gamma = C - I
    hat = C + I
    if not (gamma * gamma == -s.eye(16) and hat * hat == s.eye(16)):
        raise ArithmeticError('Time pullback exact identity failed: gamma * gamma == -s.eye(16) and hat * hat == s.eye(16)')
    (c, Q, x, a) = s.symbols('c Q x a', real=True, nonzero=True)
    Vp = s.I * c * (x * C - (x + Q) * I)
    f = s.symbols('f', real=True)
    Vf = -s.I * c * Q * f * hat / 2
    combined = s.expand(a * Vp + Vf.subs(f, -a))
    target = s.I * c * a * (x + Q / 2) * gamma
    if not combined == s.expand(target):
        raise ArithmeticError('Time pullback exact identity failed: combined == s.expand(target)')
    Kq = -a * (x + Q / 2) / Q
    Dk = s.I * c * x * gamma
    Dl = s.I * c * (x + Q) * gamma
    if not s.expand(Kq * Dk - Dl * Kq - target) == s.zeros(16):
        raise ArithmeticError('Time pullback exact identity failed: s.expand(Kq * Dk - Dl * Kq - target) == s.zeros(16)')
    t = s.symbols('t', real=True)
    eps = s.symbols('eps', real=True)
    xi = s.Function('xi')(t)
    phi = s.Function('phi')(t)
    J = 1 + eps * s.diff(xi, t)
    time = s.simplify(c / s.sqrt(J) * s.diff(phi / s.sqrt(J), t))
    expanded = c * (s.diff(phi, t) / J - s.diff(J, t) * phi / (2 * J ** 2))
    if not s.simplify(time - expanded) == 0:
        raise ArithmeticError('Time pullback exact identity failed: s.simplify(time - expanded) == 0')
    derivative = s.simplify(s.diff(time, eps).subs(eps, 0))
    expected = -c * s.diff(xi, t) * s.diff(phi, t) - c * s.diff(xi, t, 2) * phi / 2
    if not s.simplify(derivative - expected) == 0:
        raise ArithmeticError('Time pullback exact identity failed: s.simplify(derivative - expected) == 0')
    measure = J
    u0 = c / J
    if not s.simplify(measure * u0 - c) == 0:
        raise ArithmeticError('Time pullback exact identity failed: s.simplify(measure * u0 - c) == 0')
    return {'status': 'PASS', 'creator_AST_sha256': pin, 'CAR_dimension': 16, 'family': 'orientation-preserving time diffeo F_eps(t)=t+eps xi(t),J=F_eps_prime>0,onperiodictorus', 'coframe': 'e_eps=c^-1 diag(J,1,1,1);U_eps=c diag(J^-1,-1,-1,-1)', 'measure': 'omega_eps=det(e_eps)/det(e0)=J, genuine physical operator measure; notjustrepresentationchange', 'connection': 'Omega=0 exactly: all coframe1formsclosed,Cartan torsion0; noOmega correction needed', 'observer': 'internaln=e0;physicalclockoneforma=J dt/c ispulledback,notfrozen', 'raw_D': 'c J^-1 gamma0 partial0-c sum_i gamma_i partial_i,adjointinL2(Jdx)', 'whitened_D': 'c gamma0 J^-1/2 partial0 J^-1/2-c sum_i gamma_i partial_i', 'unitary': '(U_F psi)(t,x)=sqrt(J(t)) psi(F(t),x) onALL16components;U_F^*U_F=I', 'full_operator_identity': 'Dhat_eps=U_F D0 U_F^-1;Delta_eps=U_F Delta0 U_F^-1', 'prep': 'rho_eps=U_F rho0 U_F^-1;Pcluster_eps=U_F Pcluster0 U_F^-1;Psi_eps=(U_F tensorI128)Psi0;RIGHTandallSchmidtweightsunchanged', 'whole_conditional_price': 'Rconstant,Zconstant,andfeedbackspectraltracesconstantunderunitary;S_eps=S0 withsamefixedglobalcalibrations', 'feedback_trace_scope': 'finitepositiveB spectralpricewhenrealizedonacovariantfinitecarrier;continuumusesheatK=exp(-betaDelta)andrelative logdet withfieldindependentinfiniteconstantremoved', 'generator': 'Kxi=xi partial0+xi_prime/2,skew;Dhat_prime=[Kxi,D0]', 'Fourier_lapse': 'a=-xi_prime,genuinef=delta logomega=xi_prime=-a;xi_q=i a/Q', 'all16_firstjet_identity': 'aVp+Vmeasure(f=-a)=i c a(x+Q/2)gamma0=Kq Dk-Dl Kq', 'measure_source': 'owned k_x=Re trCAR([d,{D,W}]xx),DSmeasure=sum_x f_x k_x;independentphysicaldensityvariationisneeded', 'passive_vs_active': 'simultaneouschangeofHilbertframemovesDandrhoandcancelswithoutaddinganynewphysicalrow;varyingactualomegaatfixedrawframechangesadjoint/instrumentandhasownedkrow', 'minimal_native_input': 'sameexecutedprogramme mustsupplylocaldensity/timeembeddinglaw withDlogomega=-trS onthisfamily,anditsownsource/preparationtransport;notanassignednewaction', 'finite_stencil_warning': 'fixedgridforwardstencilisnotassertedexactlydiffeocovariant;ownedfinitewholeexperimentidentityalsomovesembeddingX;finitehSchurlimitstillrequiresproof', 'Einstein_warning': 'restoringwholeexperimentWarddoesnotselectEinsteinsourceorprovefullphysicalCostInfoforcing', 'native_measure_admission_claimed': False, 'finite_h_Schur_limit_claimed': False}

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('root',type=Path);parser.add_argument('--output',type=Path);args=parser.parse_args()
 result={'status':'PASS_EXACT','kernel':kernel(args.root),'lapse_traces':lapse_traces(args.root),'time_pullback_ward':time_pullback_ward(args.root)}
 text=json.dumps(result,indent=2,default=str)+'\n'
 if args.output:args.output.write_text(text)
 print(text,end='')
