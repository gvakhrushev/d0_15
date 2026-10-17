"""Exact finite controls for relative-record cost / Schur survival.
Scope: conditional mathematics, not native-gate or GR refinement proof.
Run: python check_record_cost.py  ; python -O check_record_cost.py
"""
import json
import sympy as S

def require(condition, message):
    if not bool(condition):
        raise RuntimeError(message)

def equal(a, b):
    return S.simplify(a-b) == 0

def pivots(A):
    minors = [S.Integer(1)] + [A[:i, :i].det() for i in range(1, A.rows + 1)]
    return [S.cancel(minors[i] / minors[i - 1]) for i in range(1, len(minors))]

def run():
    count = 0
    def check(condition, message):
        nonlocal count
        require(condition, message)
        count += 1

    C = S.Matrix([[S.Rational(1,2), S.Rational(1,6), 0],
                  [0, S.Rational(1,3), S.Rational(1,7)],
                  [S.Rational(1,8), 0, S.Rational(1,4)]])
    A = C.T*C
    q = pivots(A)
    check(S.prod(q) == A.det(), "Schur product")
    check(q == [S.Rational(17,64), S.Rational(23,204), S.Rational(75,1127)], "Pivot fixture")
    outcomes = []
    remaining = S.Integer(1)
    for x in q:
        outcomes.append(remaining * (1-x))
        remaining *= x
    outcomes.append(remaining)
    check(sum(outcomes) == 1 and outcomes[-1] == A.det()
          and all(v>0 for v in outcomes), "Complete retained outcome cut")
    B = A.extract([2,0,1],[2,0,1])
    qp = pivots(B)
    check(qp != q and S.prod(qp) == S.prod(q), "Permutation scalar invariance")

    G0 = S.Matrix([[2,1],[1,3]])
    G1 = S.Matrix([[4,2],[2,4]])
    K = S.Matrix([[1,S.Rational(1,2)],[0,1]])
    check(G0*G1 != G1*G0 and
          equal(K.det()**2/(G0.det()*G1.det()), S.Rational(1,60)),
          "Noncommuting Gram ratio")
    U = S.Matrix([[1,1,0],[1,0,2],[0,2,3]])/20
    V = S.Matrix([[2,0,1],[0,1,1],[1,1,0]])/30
    t, s = S.symbols("t s")
    At = A+t*U+s*V
    Qt = pivots(At)
    D = At.det()
    check(equal(S.prod(Qt),D), "Moving determinant")
    check(A*U != U*A and A*V != V*A, "Noncommuting jet control")
    for var, perturbation in [(t,U),(s,V)]:
        lhs = S.diff(S.log(D),var).subs({t:0,s:0})
        check(equal(lhs,S.trace(A.inv()*perturbation)), "First matrix source")
        check(equal(lhs,sum(S.diff(S.log(v),var).subs({t:0,s:0})
                            for v in Qt)), "First conditional source")
    mixed = S.diff(S.log(D),t,s).subs({t:0,s:0})
    check(equal(mixed,-S.trace(A.inv()*U*A.inv()*V)), "Ordered second source")
    check(equal(mixed,S.Rational(16799,93750)), "Exact mixed fixture")

    x, y = S.Rational(1,2), S.Rational(1,3)
    check(1-x*y != (1-x)+(1-y), "Wrong nonlog serial cost")
    check(S.prod([A[i,i] for i in range(3)]) != A.det(), "Wrong diagonal event")
    H = lambda u:-u*S.log(u)-(1-u)*S.log(1-u)
    check(abs(float(S.N(H(x)+H(y)+S.log(x*y))))>0.1,
          "False pointer Shannon / success surprise equality")
    p = (S.sqrt(5)-1)/2
    z = S.Rational(1,2**20)
    alpha = p*(1-z)**3
    check(float(S.N(alpha))>0.6 and 0<float(S.N(p-alpha))<2e-6,
          "Golden perturbation bound")
    for v in pivots(S.diag(alpha,p)):
        check(float(S.N(alpha-v))<1e-13 and
              float(S.N(v-p))<1e-13, "Golden Schur corridor")
    return {"status":"PASS", "exact_controls":count, "det_A":str(A.det()),
            "pivots":[str(v) for v in q],
            "permuted_pivots":[str(v) for v in qp],
            "two_Gram_ratio":"1/60", "mixed_jet":str(mixed),
            "golden_p":str(S.N(p,16)),
            "min_conditional_q":str(S.N(alpha,16)),
            "native_action_selected":False,
            "raw_hm2_terminal_closed":False}

if __name__ == "__main__":
    print(json.dumps(run(),sort_keys=True,ensure_ascii=False))
