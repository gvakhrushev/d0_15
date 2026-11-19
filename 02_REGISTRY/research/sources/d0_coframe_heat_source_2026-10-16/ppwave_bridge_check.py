"""Bounded full16 pp-wave raising/Hodge/heat identity candidate.

No old checker is imported or run. The two actual CAR definition nodes are
AST-extracted from their frozen source. All output is returned or printed;
the module never writes a repository file.
"""
from pathlib import Path
from functools import lru_cache
import ast
import hashlib
import json
import sympy as s

ROOT = Path(__file__).resolve().parents[4]
PINS = {
    '02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py':
        'bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da',
    '02_REGISTRY/research/A4D_COFRAME_TORSION_INTRINSIC_GR_RECONSTRUCTION.md':
        '861eb7b753d333b8b51de55145a9a0078773854a74f0f619baa13056604d0eb9',
}


def _zero(value):
    if isinstance(value, s.MatrixBase):
        return all(s.expand(item) == 0 for item in value)
    return s.expand(value) == 0


def _creators(repo):
    path = repo / next(iter(PINS))
    tree = ast.parse(path.read_text())
    nodes = [node for node in tree.body
             if (isinstance(node, ast.FunctionDef) and node.name == 'creator')
             or (isinstance(node, ast.Assign) and any(
                 isinstance(target, ast.Name) and target.id == 'EXTERIOR_ORDER'
                 for target in node.targets))]
    if len(nodes) != 2:
        raise ArithmeticError('actual CAR definition extraction changed')
    scope = {'s': s, 'lru_cache': lru_cache}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), 'exec'), scope)
    return tuple(scope['creator'](i) for i in range(4))


def run(repo=None):
    repo = Path(repo) if repo is not None else ROOT
    checks = []

    def require(condition, name):
        if not bool(condition):
            raise ArithmeticError(name)
        checks.append(name)

    for path, digest in PINS.items():
        require(hashlib.sha256((repo / path).read_bytes()).hexdigest() == digest,
                'source_pin_' + Path(path).name)
    c = _creators(repo)
    b = tuple(ci.T for ci in c)
    I = s.eye(16)
    Z = s.zeros(16)
    require(all(_zero(c[i]*b[j]+b[j]*c[i]-(I if i == j else Z))
                for i in range(4) for j in range(4)), 'all16_owned_CAR')

    def create(v):
        return sum((v[i]*c[i] for i in range(4)), s.zeros(16))

    def Gamma(A):
        return sum((A[i,j]*c[i]*b[j] for i in range(4) for j in range(4)),
                   s.zeros(16))

    H, hx, hy, hxx, hxy, hyy = s.symbols('H hx hy hxx hxy hyy', real=True)
    eta = s.diag(1,-1,-1,-1)
    N = s.zeros(4)
    N[0,0] = N[0,3] = s.Rational(1,2)
    N[3,0] = N[3,3] = -s.Rational(1,2)
    e, F = s.eye(4)+H*N, s.eye(4)-H*N
    W = s.Matrix([[0,hx,hy,0], [hx,0,0,hx], [hy,0,0,hy],
                  [0,-hx,-hy,0]])/2
    omega = (W, s.zeros(4), s.zeros(4), W)
    U = I
    for i in (1,2,3):
        U = U*(I-2*c[i]*b[i])
    require(_zero(U*U-I) and _zero(W.T*eta+eta*W),
            'eta_intertwiner_and_vector_Lorentz_connection')

    # Direct torsion dtheta (no substitution of a desired differential).
    dH = (0,hx,hy,0)
    torsion = {}
    Q = s.zeros(16)
    for a in range(4):
        for j in range(4):
            for k in range(j+1,4):
                value = s.expand(sum(F[mu,j]*F[nu,k]*
                    (dH[mu]*N[a,nu]-dH[nu]*N[a,mu])
                    for mu in range(4) for nu in range(4)))
                torsion[a,j,k] = value
                Q += value*c[j]*c[k]*b[a]
    raising = sum((create(eta*F.row(r).T)*Gamma(omega[r]) for r in range(4)), Z)
    wrong = sum((create(eta*F.row(r).T)*Gamma(-omega[r].T) for r in range(4)), Z)
    require(_zero(U*raising*U-Q), 'native_plus_vector_LC_is_exterior_raising_full16')
    require(not _zero((U*wrong*U-Q).subs({H:0,hx:1,hy:0})),
            'wrong_original_covector_sign_rejected_full16')

    # Constant positive orthogonal null-coordinate basis (not a gauge claim).
    ca, cb = (c[0]+c[3])/s.sqrt(2), (c[0]-c[3])/s.sqrt(2)
    ba, bb = ca.T, cb.T
    cx, cy, bx, by = c[1], c[2], b[1], b[2]
    cs = (ca, cb, cx, cy)
    gs = tuple(ci-ci.T for ci in cs)
    ga, gb, gx, gy = gs
    Bx, By = cx*ca*bb+cb*ba*bx, cy*ca*bb+cb*ba*by
    Qnull = hx*cx*ca*bb+hy*cy*ca*bb
    Vhodge = hx*Bx+hy*By
    T = hx*gx*ga+hy*gy*ga
    norm2 = hx*hx+hy*hy
    require(_zero(T*T+norm2*I), 'native_first_order_T_square_full16')
    require(not _zero((hx*cx*ca+hy*cy*ca).subs({hx:1,hy:0})),
            'native_d_squared_nonzero_derivative_witness')
    require(all(_zero(cs[j]*Qnull+Qnull*cs[j] -
                    (hx*cx*ca+hy*cy*ca if j == 1 else Z)) for j in range(4))
            and _zero(Qnull*Qnull)
            and _zero(cx*(hxx*cx*ca*bb+hxy*cy*ca*bb)
                      +cy*(hxy*cx*ca*bb+hyy*cy*ca*bb)),
            'added_coframe_Q_cancels_full_operator_d_squared')

    G = s.Matrix([[1+H*H,H,0,0],[H,1,0,0],[0,0,1,0],[0,0,0,1]])
    Gi = s.Matrix([[1,-H,0,0],[-H,1+H*H,0,0],[0,0,1,0],[0,0,0,1]])
    require(_zero(G*Gi-s.eye(4)) and G.det() == 1, 'positive_metric_inverse_det1')

    # Actual squared Dirac: principal -Ginv; native first-order -T partial_b.
    principal = (ga,gb-H*ga,gx,gy)
    native_first = (Z,-T,Z,Z)
    native_conn = (H*T/2,T/2,Z,Z)
    require(all(_zero(-2*sum((Gi[mu,nu]*native_conn[mu]
                             for mu in range(4)), Z)-native_first[nu])
                for nu in range(4)), 'native_D_squared_first_order_completion')
    native_E = -sum((Gi[mu,nu]*native_conn[mu]*native_conn[nu]
                    for mu in range(4) for nu in range(4)), Z)
    require(_zero(native_E-norm2*I/4), 'native_actual_Bochner_endomorphism')

    # Compute Hodge completion from D_hodge=D_native+Q+Q*, not from its name.
    hodge_first = tuple(native_first[nu]+principal[nu]*Vhodge
                        +Vhodge*principal[nu] for nu in range(4))
    hodge_conn = tuple(-sum((G[mu,nu]*hodge_first[nu] for nu in range(4)), Z)/2
                       for mu in range(4))
    hodge_zero = (gx*(hxx*Bx+hxy*By)+gy*(hxy*Bx+hyy*By)
                  +Vhodge*Vhodge)
    dx_conn = hodge_conn[2].diff(H)*hx+hodge_conn[2].diff(hx)*hxx+hodge_conn[2].diff(hy)*hxy
    dy_conn = hodge_conn[3].diff(H)*hy+hodge_conn[3].diff(hx)*hxy+hodge_conn[3].diff(hy)*hyy
    hodge_E_trace = s.expand(-s.trace(hodge_zero+dx_conn+dy_conn)
        -sum(Gi[mu,nu]*s.trace(hodge_conn[mu]*hodge_conn[nu])
             for mu in range(4) for nu in range(4)))
    require(s.simplify(hodge_E_trace-2*norm2) == 0,
            'LC_actual_full16_Hodge_endomorphism_trace')

    # Independent Christoffel computation; H is a generic smooth function.
    x,y=s.symbols('x y', real=True)
    Hfun=s.Function('H')(x,y)
    coords=(s.Symbol('a'),s.Symbol('b'),x,y)
    metric=G.subs(H,Hfun)
    inverse=Gi.subs(H,Hfun)
    christ=[[[s.simplify(sum(inverse[i,l]*(s.diff(metric[l,k],coords[j])
        +s.diff(metric[l,j],coords[k])-s.diff(metric[j,k],coords[l]))
        for l in range(4))/2) for k in range(4)] for j in range(4)] for i in range(4)]
    ric=s.Matrix(4,4,lambda j,k:s.simplify(sum(
        s.diff(christ[i][j][k],coords[i])-s.diff(christ[i][j][i],coords[k])
        +sum(christ[i][i][l]*christ[l][j][k]-christ[i][k][l]*christ[l][j][i]
             for l in range(4)) for i in range(4))))
    scalar=s.simplify(sum(inverse[j,k]*ric[j,k] for j in range(4) for k in range(4)))
    require(s.simplify(scalar+(s.diff(Hfun,x)**2+s.diff(Hfun,y)**2)/2)==0
            and all(s.simplify(sum(inverse[j,k]*christ[i][j][k]
                    for j in range(4) for k in range(4)))==0 for i in range(4)),
            'independent_Christoffel_R_G_and_contracted_Gamma_zero')
    R=-norm2/2
    a2_native=s.simplify(s.trace(native_E)+16*R/6)
    a2_lc=s.simplify(hodge_E_trace+16*R/6)
    require(s.simplify(a2_native-s.Rational(8,3)*norm2)==0
            and s.simplify(a2_lc-s.Rational(2,3)*norm2)==0,
            'actual_heat_a2_native_and_LC_factor_four_full16')

    # det e=1 and n constant make the scalar endpoint density jet exactly zero.
    Wpoint=W.subs({hx:1,hy:0})
    require(s.simplify(e.det()-1)==0 and Wpoint != s.zeros(4)
            and s.trace(Wpoint)==0 and not _zero(Gamma(Wpoint)),
            'constant_density_endpoint_jet_zero_but_LC_connection_nonzero')
    require(s.simplify(s.trace(Wpoint.T*Wpoint)-1)==0,
            'LC_nonzero_connection_has_exact_positive_matrix_norm')

    # Independent Lorentz transgression in the ORIGINAL coordinate basis.
    # These are actual exterior products; no scalar curvature substitution.
    theta = tuple(create(e.row(a).T) for a in range(4))
    torsion_coordinate = tuple(sum(((dH[r]*N[a,t]-dH[t]*N[a,r])*c[r]*c[t]
        for r in range(4) for t in range(r+1,4)), Z) for a in range(4))
    Cup = tuple(tuple((W*eta)[a,b]*(c[0]+c[3]) for b in range(4))
                for a in range(4))
    require(all(_zero(sum((omega[0][a,j]*(W*eta)[j,b]
                    *(c[0]+c[3])*(c[0]+c[3]) for j in range(4)), Z))
                for a in range(4) for b in range(4)),
            'Lorentz_C_wedge_C_identically_zero')
    boundary = s.zeros(16)
    L_T = s.zeros(16)
    for a in range(4):
        for b0 in range(4):
            for d in range(4):
                for f in range(4):
                    eps = s.LeviCivita(a,b0,d,f)
                    if eps:
                        boundary += eps*theta[a]*theta[b0]*Cup[d][f]/2
                        L_T -= eps*torsion_coordinate[a]*theta[b0]*Cup[d][f]
    require(_zero(boundary), 'Lorentz_transgression_boundary_B_identically_zero')
    require(_zero(L_T), 'Lorentz_quadratic_L_T_identically_zero')
    require(s.simplify(a2_native-a2_lc-2*norm2)==0
            and (a2_native-a2_lc).subs({hx:1,hy:0})==2,
            'positive_heat_difference_nonzero_despite_Lorentz_L_T_zero')

    return {'status':'PASS','exact_checks':len(checks),'checks':checks,
            'carrier':16,'source_pins':PINS,
            'native_connection_sign':'+omega_LC on vector native slot',
            'coefficient_connection_after_eta':'-omega_LC.T',
            'det_positive_metric':'1','R_G':'-(Hx**2+Hy**2)/2',
            'trace_E_native':'4*(Hx**2+Hy**2)',
            'trace_E_LC':'2*(Hx**2+Hy**2)',
            'trace_a2_native':'8*(Hx**2+Hy**2)/3',
            'trace_a2_LC':'2*(Hx**2+Hy**2)/3',
            'positive_heat_a2_difference':'2*(Hx**2+Hy**2)',
            'Lorentz_transgression_boundary_B':'0 identically',
            'Lorentz_C_wedge_C':'0 identically',
            'Lorentz_L_T':'0 identically',
            'scope':'local continuum operator identity, not finite-v8 price/source equivalence or physical admission'}


if __name__ == '__main__':
    print(json.dumps(run(),sort_keys=True,indent=2))
