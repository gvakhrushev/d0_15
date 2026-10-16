#!/usr/bin/env python3
"""New exact raw-row algebra only; no heat bounds or old checker entrypoints."""
import ast
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import sympy as s

ROOT = Path(__file__).resolve().parents[4]
CREATOR_PATH = '02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py'
SOURCE_PINS = {CREATOR_PATH:
    'bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da'}


def run(repo=None):
    repo = Path(repo) if repo is not None else ROOT
    checks = []

    def require(condition, name):
        if not bool(condition):
            raise ArithmeticError(name)
        checks.append(name)

    for path, digest in SOURCE_PINS.items():
        require(hashlib.sha256((repo/path).read_bytes()).hexdigest() == digest,
                'source_pin_' + Path(path).name)
    path = repo/CREATOR_PATH
    nodes = [node for node in ast.parse(path.read_text()).body if
             (isinstance(node, ast.FunctionDef) and node.name == 'creator') or
             (isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and
              t.id == 'EXTERIOR_ORDER' for t in node.targets))]
    require(len(nodes) == 2, 'only_actual_creator_and_order_definitions')
    scope = {'s': s, 'lru_cache': lru_cache}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), 'exec'), scope)
    c = [s.SparseMatrix(scope['creator'](j)) for j in range(4)]
    b = [x.T for x in c]
    eye16, zero16 = s.SparseMatrix(s.eye(16)), s.SparseMatrix(16,16,{})
    require(all(c[i]*b[j]+b[j]*c[i] == (eye16 if i == j else zero16)
                for i in range(4) for j in range(4)), 'actual_full16_CAR')

    def lift(a):
        return sum((a[i,j]*c[i]*b[j] for i in range(4) for j in range(4)
                    if a[i,j] != 0), zero16)

    def elem(i,j):
        a = s.zeros(4)
        a[i,j] = 1
        return a

    boosts = [elem(0,j)+elem(j,0) for j in (1,2,3)]
    rotations = [elem(i,j)-elem(j,i) for i,j in ((1,2),(1,3),(2,3))]
    generators = boosts+rotations
    lifts = [lift(a) for a in generators]
    eta = s.diag(1,-1,-1,-1)
    require(all(a.T*eta+eta*a == s.zeros(4) for a in generators),
            'six_actual_Lorentz_generators')
    require(all(h*h*h == h and h.T == h for h in lifts[:3]),
            'full_exterior_boost_minimal_polynomial')
    cosh, sinh = s.Rational(5,4), s.Rational(3,4)
    native_links = [s.eye(4)+sinh*a+(cosh-1)*a*a for a in boosts]
    links = [eye16+sinh*h+(cosh-1)*h*h for h in lifts[:3]]
    require(all(a.T*eta*a == eta and a.det() == 1 and a[0,0] > 0
                for a in native_links), 'three_rational_proper_orthochronous_links')
    require(all(links[x]*c[i] == sum((native_links[x][j,i]*c[j]
                for j in range(4)), zero16)*links[x]
                for x in range(3) for i in range(4)),
            'actual_full16_exterior_lift_intertwines_all_creators')

    size = 48
    eye = s.SparseMatrix(s.eye(size))
    shift = s.SparseMatrix(3,3,{(x,(x+1)%3):1 for x in range(3)})
    shift = s.kronecker_product(shift,eye16)
    mass = s.diag(*links)
    transport = mass*shift
    mesh = s.Rational(2,5)
    forward = (transport-eye)/mesh
    u = [s.Matrix([s.Rational(x+2,5),s.Rational(2*x-1,7),
                   s.Rational(x*x+1,11),s.Rational(3-x,13)]) for x in range(3)]
    cs = [sum((u[x][j]*c[j] for j in range(4)),zero16) for x in range(3)]
    coefficient = s.diag(*cs)
    d = coefficient*forward
    D = d+d.T
    delta = D*D
    # Test function only: F(Delta)=Tr(Delta+Delta^2/2), kappa=I+Delta.
    kappa = eye+delta
    Q = D*kappa+kappa*D
    require(D.T == D and Q.T == Q, 'true_adjoint_D_and_anticommutator_Q_Hermitian')

    def tp(a,bb):
        # Exact trace product, avoiding unnecessary full products in 39 directions.
        entries = a.todok() if isinstance(a,s.SparseMatrix) else a.todok()
        return sum((v*bb[j,i] for (i,j),v in entries.items()),s.S.Zero)

    def local(x,a):
        out = s.SparseMatrix(size,size,{})
        for (i,j),v in a.todok().items():
            out[16*x+i,16*x+j] = v
        return out

    def diagonal_pair(a,bb):
        return sum((tp(a[16*x:16*x+16,16*x:16*x+16],
                       bb[16*x:16*x+16,16*x:16*x+16])
                    for x in range(3)),s.S.Zero)

    coframe_row = forward*Q
    link_row = transport*Q*coefficient
    observer_row = d*Q-Q*d
    nonzero = {'coframe':0,'link':0,'observer':0}
    wrong = {'half_Q':False,'wrong_coframe_order':False,
             'wrong_link_order':False,'wrong_observer_order':False}

    def check_direction(v, expected, name, family):
        vD = v+v.T
        vdelta = D*vD+vD*D
        direct = tp(kappa,vdelta)
        paired = 2*tp(Q,v)
        require(direct == paired == expected, name)
        nonzero[family] += int(direct != 0)
        wrong['half_Q'] |= (direct != tp(Q,v))

    for x in range(3):
        for j in range(4):
            test = local(x,c[j])
            v = test*forward
            expected = 2*diagonal_pair(coframe_row,test)
            check_direction(v,expected,'coframe_site%d_component%d'%(x,j),'coframe')
            wrong['wrong_coframe_order'] |= expected != 2*diagonal_pair(Q*forward,test)
        for j,generator in enumerate(lifts):
            test = local(x,generator)
            # Literal physical left-link tangent: delta A=h*xi*A.
            v = coefficient*test*transport
            expected = 2*diagonal_pair(link_row,test)
            check_direction(v,expected,'physical_leftlink_site%d_generator%d'%(x,j),'link')
            wrong['wrong_link_order'] |= expected != 2*diagonal_pair(Q*coefficient*transport,test)
        for j,generator in enumerate(lifts[:3]):
            K = local(x,-generator)
            v = K*d-d*K
            expected = 2*diagonal_pair(observer_row,K)
            check_direction(v,expected,'observer_site%d_boost%d'%(x,j),'observer')
            wrong['wrong_observer_order'] |= expected != -expected
    require(all(n > 0 for n in nonzero.values()), 'each_source_family_has_nonzero_witness')
    for name,rejected in wrong.items():
        require(rejected,'hostile_'+name+'_rejected')
    require(mesh != 1 and nonzero['link'] > 0,
            'unscaled_raw_link_requires_extra_inverse_h_not_silently_identified')

    # Three independent formal spectral slots, no fitted physical heat numbers.
    lam = s.symbols('lambda0:3', real=True)
    energy = s.symbols('E0:3', positive=True)
    Z,beta,z,M,c0,tau = s.symbols('Z beta z M c0 tau', positive=True)
    a = 1-z
    kapp0 = [-energy[i]/Z+M*z*beta*energy[i]/(a+z*energy[i]) for i in range(3)]
    clock = c0*sum((kapp0[i]*lam[i]**2 for i in range(3)),s.S.Zero)/2
    moment = sum((lam[i]**2*energy[i] for i in range(3)),s.S.Zero)
    clock_sources = []
    for i in range(3):
        derivative = s.diff(clock,lam[i])-beta*energy[i]*(
            s.diff(clock,energy[i])+s.diff(clock,Z))
        fixedZ = -beta*energy[i]*s.diff(kapp0[i],energy[i])
        expected = c0*(lam[i]*kapp0[i]+lam[i]**2*fixedZ/2-
                       beta*moment*energy[i]/(2*Z**2))
        require(s.cancel(derivative-expected) == 0,
                'clock_total_derivative_global_normalizer_slot%d'%i)
        # Independent finite-clock P versus K coefficient, then d/dtau at zero.
        P = [energy[j]*(1-beta*c0*tau*lam[j]**2/2) for j in range(3)]
        K = P[i]/(1-c0*tau*lam[i])
        finite = -K/sum(P)+M*z*beta*K/(a+z*P[i])
        coefficient1 = s.diff(finite,tau).subs(tau,0)
        require(s.cancel(coefficient1-expected.subs(Z,sum(energy))) == 0,
                'clock_K_numerator_P_normalizer_and_feedback_slot%d'%i)
        clock_sources.append(expected)
    witness = dict(zip(lam,map(s.Rational,(1,2,3))))
    witness.update(dict(zip(energy,(s.Rational(1,2),s.Rational(1,3),s.Rational(1,5)))))
    witness.update({Z:sum(witness[e] for e in energy),beta:s.Rational(2,3),
                    z:s.Rational(1,7),M:s.Integer(2),c0:s.Rational(3,5)})
    dropped = c0*beta*moment*energy[0]/(2*Z**2)
    require(dropped.subs(witness) != 0,'hostile_drop_global_normalizer_clock_term_rejected')
    P = [energy[j]*(1-beta*c0*tau*lam[j]**2/2) for j in range(3)]
    K = [P[j]/(1-c0*tau*lam[j]) for j in range(3)]
    wrong_clock = -K[0]/sum(K)+M*z*beta*K[0]/(a+z*K[0])
    wrong_clock_coefficient = s.diff(wrong_clock,tau).subs(tau,0)
    discrepancy = s.factor((wrong_clock_coefficient-clock_sources[0]).subs(witness))
    require(discrepancy != 0,'hostile_K_instead_of_P_normalizer_and_feedback_rejected')
    require(s.Rational(3)-s.Rational(30,40) > 2 and s.Rational(96,40) > 2,
            'stated_h3_N30_plus_Nminus96_cutoff_is_little_o_h2')
    return {
        'status':'PASS','exact_check_groups':len(checks),'checks':checks,
        'source_pins':SOURCE_PINS,'full_Fock_components':16,'ring_sites':3,
        'ring_dimension':48,'fixture_mesh':'2/5',
        'fixture_kappa':'I+Delta; algebraic test function only, not thermal data',
        'coframe_directions_checked':12,'physical_link_directions_checked':18,
        'observer_directions_checked':9,'nonzero_witnesses':nonzero,
        'exact_rows':{'coframe':'B Q against delta C',
                      'physical_leftlink':'M S Q C against Gamma(xi), delta A=h xi A',
                      'observer':'d Q-Q d against K; no derivative of rough K'},
        'source_pairing':'delta S=2 Re Tr Q delta d, Q={D,kappa}',
        'clock_correction':'c0 [lambda_i kappa0_i + lambda_i^2 fixedZ(kappa0_i prime)/2 - beta (sum lambda_j^2 E_j) E_i/(2 Z^2)]',
        'wrong_K_in_P_slots_rational_discrepancy':str(discrepancy),
        'cutoff_budget_exponents':['9/4','12/5'],
        'scope':'NEW_EXACT_RAW_ROW_AND_SCALAR_CLOCK_IDENTITIES_ONLY',
        'not_proved':['analytic heat remainder or source sampling estimate',
                      'physical preparation/admission or Einstein source equality',
                      'o(h^2) in unscaled raw-link coordinates'],
        'old_entrypoints_executed':False,
    }


if __name__ == '__main__':
    print(json.dumps(run(),ensure_ascii=False,sort_keys=True,indent=2))
