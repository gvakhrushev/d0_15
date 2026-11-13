"""Exact finite controls for SOURCE_COVERAGE_RU.md; no physical valuation inferred."""
from pathlib import Path
import hashlib
import json
import platform
import sympy as S


def run():
    checks = []

    def need(condition, label):
        if not bool(condition):
            raise AssertionError(label)
        checks.append(label)

    def eq(a, b, label):
        delta = a - b
        good = (all(S.simplify(v) == 0 for v in delta)
                if isinstance(delta, S.MatrixBase) else S.simplify(delta) == 0)
        need(good, label)

    def coverage(L, R):
        need(L.rows == R.rows, "common tangent carrier")
        if L.rank() == L.row_join(R).rank():
            C = L.pinv() * R
            eq(L*C, R, "exact lift factorization")
            return {"covered": True, "C": C}
        for n in L.T.nullspace():
            if n.T*R != S.zeros(1, R.cols):
                eq(n.T*L, S.zeros(1, L.cols), "annihilator kills all tests")
                need(n.T*R != S.zeros(1, R.cols), "annihilator sees physical lift")
                return {"covered": False, "witness": n.T}
        raise AssertionError("missing separating covector")

    A = S.Matrix([[1, 0, 0, 0]])
    R = S.ones(4, 1)
    L = S.eye(4)[:, 1:]
    eq(A*R, S.ones(1, 1), "LC9 structural right lift")
    bad = coverage(L, R)
    need(not bad["covered"], "three backward/internal slots miss forward slot")
    eq(bad["witness"], A, "explicit unseen forward source")
    repeated = L.row_join(L).row_join(L)
    need(not coverage(repeated, R)["covered"], "repeating tests cannot repair coverage")
    repaired = coverage(S.eye(4), R)
    eq(repaired["C"], R, "adding a real forward map would cover the block")
    P = S.eye(4)-R*A
    eq(P*P, P, "nuisance projector is idempotent")
    eq(A*P, S.zeros(1,4), "nuisance image lies in kernel of decoder")
    eq(P*R, S.zeros(4,1), "nuisance projector kills right lift")
    r = S.Matrix([[2,3,5,7]])
    eq((r*R)*A+r*P, r, "full covector decomposition retains all rows")
    internal = S.Matrix([[1,-1,0,0]])
    eq(internal*R, S.zeros(1,1), "physical projection can vanish")
    need(internal != S.zeros(1,4), "zero physical projection is not zero full residual")

    conditioning = []
    for d in (S.Rational(1,2), S.Rational(1,10), S.Rational(1,1000)):
        Q = S.Matrix([[1,1],[0,d]])
        target = S.Matrix([0,1])
        C = coverage(Q, target)["C"]
        eq(C, S.Matrix([-1/d,1/d]), f"conditioned coefficients at d={d}")
        eq((C.T*C)[0], 2/d**2, f"exact norm squared at d={d}")
        residual = S.Matrix([[0,1]])
        eq(residual*Q, S.Matrix([[0,d]]), f"small measured rows at d={d}")
        eq(residual*target, S.ones(1,1), f"unit physical error survives at d={d}")
        conditioning.append({"d":str(d),"coefficient_norm_squared":str(2/d**2),
                             "measured_norm_squared":str(d**2),"physical_error":"1"})

    # Approximate containment without a bound on the unknown covector is insufficient.
    d = S.Rational(1,1000)
    small_lift = S.Matrix([1,d])
    visible = S.Matrix([1,0])
    invisible_r = S.Matrix([[0,1/d]])
    eq(invisible_r*visible, S.zeros(1,1), "approximate coverage measured source is zero")
    eq(invisible_r*small_lift, S.ones(1,1), "small geometric leakage can hide unit source")

    # A consistent overcomplete system: pseudoinverse discards only its kernel.
    over = S.Matrix([[1,0,1],[0,1,0]])
    target = S.eye(2)
    C0 = coverage(over, target)["C"]
    null = S.Matrix([[-1,0],[0,0],[1,0]])
    eq(over*null, S.zeros(2), "free factorization term is in kernel")
    eq(C0.T*null, S.zeros(2), "minimum solution orthogonal to free kernel")
    eq((C0+null).T*(C0+null), C0.T*C0+null.T*null,
       "minimum norm proof keeps positive kernel term")

    t, eps = S.symbols("t eps", real=True, positive=True)
    spike = eps*S.sin(t/eps)
    eq(S.diff(spike,t).subs(t,0), S.Integer(1), "C0-small smooth function can have unit first jet")
    h, M = S.symbols("h M", positive=True)
    eq(S.integrate(M*t,(t,0,h))/h, M*h/2, "central-secant Lipschitz derivative bound")
    bound = eps/h+M*h/2
    optimum = S.sqrt(2*eps/M)
    eq(bound.subs(h,optimum), S.sqrt(2*M*eps), "balanced step derivative error")
    eq(S.diff(bound,h).subs(h,optimum), S.Integer(0), "balanced step is stationary")
    need(S.diff(bound,h,2).is_positive, "balanced step is minimum on positive steps")

    x, y, z, a, b = S.symbols("x y z a b", real=True)
    coords = S.Matrix([x,y,z])
    X, Y = S.Matrix([1,0,0]), S.Matrix([0,1,x])
    bracket = Y.jacobian(coords)*X-X.jacobian(coords)*Y
    eq(bracket, S.Matrix([0,0,1]), "control bracket generates missing z direction")
    need(X.row_join(Y).rank() == 2, "instantaneous controls have rank two")
    need(X.row_join(Y).row_join(bracket).rank() == 3, "bracket closure has rank three")

    def flow_x(point, time):
        u,v,w = point
        return S.Matrix([u+time,v,w])

    def flow_y(point, time):
        u,v,w = point
        return S.Matrix([u,v+time,w+u*time])

    loop = flow_y(flow_x(flow_y(flow_x(coords,a),b),-a),-b)
    eq(loop, S.Matrix([x,y,z+a*b]), "four real flows give exact area displacement")
    contact = S.Matrix([[0,-x,1]])
    eq(contact*X, S.zeros(1,1), "nonclosed form kills first control")
    eq(contact*Y, S.zeros(1,1), "nonclosed form kills second control")
    eq(contact*bracket, S.ones(1,1), "nonclosed form does not kill control bracket")
    eq(S.diff(contact[1],x)-S.diff(contact[0],y), S.Integer(-1),
       "contact form has nonzero exterior derivative")
    comm_bound = 4*eps/h+M*h**2/2
    comm_step = (4*eps/M)**S.Rational(1,3)
    eq(S.diff(comm_bound,h).subs(h,comm_step), S.Integer(0),
       "commutator finite error has balanced cubic step")
    eq(comm_bound.subs(h,comm_step),
       S.Rational(3,2)*4**S.Rational(2,3)*M**S.Rational(1,3)*eps**S.Rational(2,3),
       "commutator derivative error retains two-thirds exponent")
    need(S.diff(comm_bound,h,2).is_positive, "commutator step is minimum")
    f = S.Function("f")(x)
    nuisance_1, nuisance_2 = S.Matrix([0,1,z]), S.Matrix([0,y,1])
    nuisance_bracket = nuisance_2.jacobian(coords)*nuisance_1-nuisance_1.jacobian(coords)*nuisance_2
    eq((S.Matrix([f]).jacobian(coords)*nuisance_bracket)[0], S.Integer(0),
       "brackets of forward-preserving controls still preserve forward coordinate")

    here = Path(__file__).resolve().parent
    owner = here.parents[2]/"A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md"
    # Path resolution is anchored to the source folder, not the current working directory.
    return {"status":"PASS", "check_count":len(checks), "checks":checks,
            "conditioning_controls":conditioning,
            "baseline_commit":"dc411daf01f697ec85dd22f28bfe124171796645",
            "owner_sha256":hashlib.sha256(owner.read_bytes()).hexdigest(),
            "proof_sha256":hashlib.sha256((here/"SOURCE_COVERAGE_RU.md").read_bytes()).hexdigest(),
            "environment":{"python":platform.python_version(),"sympy":S.__version__},
            "scope":{"exact_rational_controls":True,"full_H1_executed":False,
                     "physical_weight_binding_proved":False,"physical_C_closed":False,
                     "GR_closed":False}}


if __name__ == "__main__":
    result = run()
    target = Path(__file__).with_name("CHECK_RESULT.json")
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"status":result["status"],"checks":result["check_count"],
                      "output":str(target)},ensure_ascii=False))
