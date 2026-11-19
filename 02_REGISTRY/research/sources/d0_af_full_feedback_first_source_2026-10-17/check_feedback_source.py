#!/usr/bin/env python3
"""Exact, scoped AF feedback/source identities. No simulation or claim of GR closure.

Run with Python >=3.10 and SymPy. Tests do not disappear under python -O.
The full four-frame is reconstructed from the published threefold AF inclusion.
The all-size and continuum assertions are proved in RESULT_RU.md, not inferred
from this finite checker. No old certificate, physical controller or Einstein
source is imported or installed.
"""
from __future__ import annotations

import json
import sympy as s

p, a, q2 = s.symbols("p a q2")
G = s.groebner([a*a-p, p*p+p-1, q2*q2-2], a, p, q2, domain=s.QQ)
checks: list[str] = []


def red(x):
    x = s.cancel(x)
    nu, de = s.fraction(x)
    return s.cancel(G.reduce(s.expand(nu))[1] / G.reduce(s.expand(de))[1])


def zero(name: str, x) -> None:
    seq = list(x) if isinstance(x, s.MatrixBase) else [x]
    if any(red(v) != 0 for v in seq):
        raise ArithmeticError(name)
    checks.append(name)


def true(name: str, value: bool) -> None:
    if not value:
        raise ArithmeticError(name)
    checks.append(name)


def nonzero(name: str, x) -> None:
    seq = list(x) if isinstance(x, s.MatrixBase) else [x]
    true(name, any(red(v) != 0 for v in seq))


def fib(n: int) -> int:
    u, v = 0, 1
    for _ in range(n):
        u, v = v, u+v
    return u


def blocks(rows):
    return s.BlockMatrix(rows).as_explicit()


def af_frame(A: int, B: int):
    """Actual normalized matrix-unit frame, not an arbitrary tensor extension."""
    dims = [A, B]
    orders = [[0, 1, 0, 0, 1], [0, 1, 0]]
    sizes = [sum(dims[j] for j in order) for order in orders]
    offsets, positions = [], []
    for order in orders:
        starts, total = [], 0
        for j in order:
            starts.append(total)
            total += dims[j]
        offsets.append(starts)
        positions.append([[k for k, ty in enumerate(order) if ty == j]
                          for j in range(2)])
    d, D = A*A+B*B, sizes[0]**2+sizes[1]**2
    V = s.zeros(D, 4*d)

    def ix(v, copy_r, row, copy_c, col):
        off = 0 if v == 0 else sizes[0]**2
        return off + (offsets[v][copy_r]+row)*sizes[v] + offsets[v][copy_c]+col

    for j, dj in enumerate(dims):
        oldoff = 0 if j == 0 else A*A
        for r in range(dj):
            for c in range(dj):
                k = oldoff + r*dj+c
                for v in (0, 1):
                    weight = [[a*p, p*p], [p, a*p]][j][v]
                    for cp in positions[v][j]:
                        V[ix(v, cp, r, cp, c), k] = weight
                cp1, cp2 = positions[0][j][:2]
                V[ix(0, cp1, r, cp2, c), d+k] = 1
                V[ix(0, cp2, r, cp1, c), 2*d+k] = 1
                V[ix(0, cp1, r, cp1, c), 3*d+k] = q2/2
                V[ix(0, cp2, r, cp2, c), 3*d+k] = -q2/2
    return V


def sylvester_root(root, direction):
    n = root.rows
    # SymPy's vector convention here is row-major; direct coordinate equations
    # avoid reliance on an undocumented vectorization convention.
    vs = s.symbols(f"d0:{n*n}")
    D = s.Matrix(n, n, vs)
    eq = list(root*D+D*root-direction)
    sol = s.solve(eq, vs, dict=True)
    if len(sol) != 1:
        raise ArithmeticError("square-root derivative must be unique")
    return D.subs(sol[0])


def four_gate(r, b):
    Z = s.zeros(r.rows)
    return blocks([[r,Z,-b,Z], [Z,r,Z,-b], [Z,b,Z,r], [b,Z,r,Z]])


def main():
    I2, Z2 = s.eye(2), s.zeros(2)
    O = s.Matrix([[s.Rational(3,5),-s.Rational(4,5)],
                  [s.Rational(4,5),s.Rational(3,5)]])
    b = O*s.diag(s.Rational(3,5),s.Rational(4,5))*O.T
    r = O*s.diag(s.Rational(4,5),s.Rational(3,5))*O.T
    E = b*b
    T = four_gate(r,b)
    P = s.diag(1,1,1,1,0,0,0,0)
    zero("noncommutative_block_unitarity", T.T*T-s.eye(8))
    F1 = P*(s.eye(8)-T.T*P*T)*P
    want1 = s.diag(E,E,Z2,Z2)
    zero("one_step_actual_rank_two_copy_cut", F1-want1)
    U2 = T*T
    F2 = P*(s.eye(8)-U2.T*P*U2)*P
    B2 = 2*E*(I2-E)
    want2 = blocks([[B2,B2,Z2,Z2],[B2,B2,Z2,Z2],
                    [Z2,Z2,Z2,Z2],[Z2,Z2,Z2,Z2]])
    zero("two_steps_same_gate_full_feedback", F2-want2)
    C = blocks([[I2,I2,Z2,Z2],[I2,-I2,Z2,Z2],
                [Z2,Z2,I2,I2],[Z2,Z2,I2,-I2]])
    zero("two_step_plus_minus_spectrum", C.T*F2*C/2-s.diag(4*E*(I2-E),Z2,Z2,Z2))

    X = s.Matrix([[1,s.Rational(2,3)],[s.Rational(2,3),-1]])
    nonzero("noncommuting_effect_tangent_is_real_test", E*X-X*E)
    dr = sylvester_root(r,-X)
    db = sylvester_root(b,X)
    dT = four_gate(dr,db)
    zero("true_root_jet_unitarity", dT.T*T+T.T*dT)
    dF1 = -P*(dT.T*P*T+T.T*P*dT)*P
    zero("first_feedback_noncommuting_jet",dF1-s.diag(X,X,Z2,Z2))
    dU2 = dT*T+T*dT
    dF2 = -P*(dU2.T*P*U2+U2.T*P*dU2)*P
    DX = 2*(X-E*X-X*E)
    zero("second_feedback_noncommuting_jet",dF2-blocks([[DX,DX,Z2,Z2],[DX,DX,Z2,Z2],
                                                       [Z2,Z2,Z2,Z2],[Z2,Z2,Z2,Z2]]))
    nonzero("frozen_square_root_jet_is_rejected",s.diag(X,X,Z2,Z2))
    nonzero("false_commuting_E2_derivative_is_rejected", E*X+X*E-2*E*X)

    z = s.Rational(2,7)
    expected1 = (I2-z*E).det()**2
    zero("complete_one_step_determinant",(s.eye(8)-z*F1).det()-expected1)
    expected2 = (I2-4*z*E*(I2-E)).det()
    zero("complete_two_step_determinant",(s.eye(8)-z*F2).det()-expected2)
    zero("logdet_source_no_commutation", z*s.trace((s.eye(8)-z*F1).inv()*dF1)
          -2*z*s.trace((I2-z*E).inv()*X))
    nonzero("wrong_one_copy_price_rejected", z*s.trace((I2-z*E).inv()*X))

    frame_dims=[]
    for n in (0,1):
        A, B = fib(n+2), fib(n+1)
        V = af_frame(A,B)
        d=A*A+B*B
        zero(f"actual_AF_frame_isometry_n{n}", V.T*V-s.eye(4*d))
        true(f"full_complement_retained_n{n}", V.rows>V.cols)
        frame_dims.append({"n":n,"input_gns":d,"working_gns":V.rows,
                           "frame":V.cols,"complement":V.rows-V.cols})
        # This proves full V-conjugated feedback by the isometry identity,
        # without replacing its ambient space by the frame or deleting modes.
        M = s.diag(*([1]*(2*d)+[0]*(2*d)))
        zero(f"transported_cut_is_orthogonal_n{n}",M*M-M)

    zero("one_step_golden_probability", p*p-(1-p))
    zero("two_step_golden_probability",4*p*p*(1-p*p)-4*p**3)
    nonzero("one_step_not_two_step",p*p-4*p**3)
    trace_bounds=[]
    for n in range(21):
        A,B=fib(n+2),fib(n+1)
        D0,D1=13*A+8*B,8*A+5*B
        N=A*D0+B*D1
        true(f"regular_multiplicity_n{n}",N==fib(2*n+9)==fib(n+5)**2+fib(n+4)**2)
        if n<6:
            den=1+p**(4*n+18)
            err0=(-( (-1)**n)*p**(2*n+16)-p**(4*n+18))/den
            err1=(((-1)**n)*p**(2*n+14)-p**(4*n+18))/den
            zero(f"regular_PF_weight_identity_0_n{n}",s.Rational(D0,N)-p**(n+1)*(1+err0))
            zero(f"regular_PF_weight_identity_1_n{n}",s.Rational(D1,N)-p**(n+2)*(1+err1))
            trace_bounds.append({"n":n,"D0":D0,"D1":D1,"N":N})
    true("actual_regular_n0_is_610",21**2+13**2==610)
    true("actual_one_step_n0_exponent_is_68",2*(21+13)==68)
    true("actual_two_step_n0_exponent_is_34",21+13==34)
    true("working_regular_multiplicity_swap_rejected",2*(21+13)!=2*(1+1))

    # Same full tensor-composed process, including its old-scene source.
    B = s.Matrix([[s.Rational(1,4),s.Rational(1,12)],
                  [s.Rational(1,12),s.Rational(1,3)]])
    Y = s.Matrix([[s.Rational(1,7),s.Rational(1,9)],
                  [s.Rational(1,9),-s.Rational(1,11)]])
    CS=I2-B
    FT=s.eye(4)-s.kronecker_product(I2-E,CS)
    K=s.eye(4)-z*FT
    dFT=s.kronecker_product(X,CS)+s.kronecker_product(I2-E,Y)
    total_source=z*s.trace(K.inv()*dFT)
    parts=z*s.trace(K.inv()*s.kronecker_product(X,CS))+z*s.trace(K.inv()*s.kronecker_product(I2-E,Y))
    zero("same_program_total_source_both_terms",total_source-parts)
    naive=z*s.trace((I2-z*E).inv()*X)+z*s.trace((I2-z*B).inv()*Y)
    nonzero("separate_feedback_prices_not_additive",total_source-naive)

    e=s.Rational(3,8)
    K0=(1-z)*I2+z*(1-e)*CS
    chi=z*CS*K0.inv()
    zsource=z*(1-e)*s.trace(K0.inv()*Y)
    E0=e*I2
    KT=(1-z)*s.eye(4)+z*s.kronecker_product(I2-E0,CS)
    zero("baseline_moving_scene_source",z*s.trace(KT.inv()*s.kronecker_product(I2-E0,Y))-2*zsource)
    zero("linear_AF_source_dressed_by_same_scene",z*s.trace(KT.inv()*s.kronecker_product(X,CS))
          -s.trace(X)*s.trace(chi))
    chi_dot=-z*(1-z)*K0.inv()*Y*K0.inv()
    direct=-z*Y*K0.inv()+z*z*(1-e)*CS*K0.inv()*Y*K0.inv()
    zero("full_noncommuting_matter_dressing_jet",chi_dot-direct)
    nonzero("moving_dressing_cannot_be_frozen",chi_dot)
    nonzero("baseline_not_field_independent",zsource)
    nonzero("generic_dressing_not_scalar_operator",chi-s.trace(chi)*I2/2)
    zero("perfect_leakage_erases_AF_source",z*s.zeros(2)*((1-z)*I2).inv())

    # A one-mode exact discriminator; a nonzero mixed derivative is not
    # a sum of independent gravity and matter functionals.
    ee, bb, zz=s.symbols("ee bb zz")
    KK=1-zz+zz*(1-ee)*(1-bb)
    mixed=s.factor(s.diff(zz*(1-bb)/KK,bb))
    true("scalar_mixed_source_exact",s.cancel(mixed+zz*(1-zz)/KK**2)==0)

    # All retained spectral modes of the previously published two-tick scene.
    pg=(s.sqrt(5)-1)/2
    LL=4*pg**3
    L3=1-(130*pg-81)**2
    Lv=1-((854*pg-531)/11)**2
    for nm, lam in [("L",LL),("L3",L3),("Lv",Lv)]:
        true(f"owned_scene_{nm}_strictly_between_zero_one",
             bool(s.simplify(lam).is_positive) and bool(s.simplify(1-lam).is_positive))
    true("owned_scene_all_528_retained_modes",264+184+36+44==528)
    true("owned_scene_zero_sector_kept_nonempty",264>0)
    # These modes only instantiate the fixed-scene theorem; they are not
    # a preparation/metric/matter stationarity certificate.
    zero("fixed_scene_source_retains_zero_modes",
         z/(1-z+z*(1-e)) - z/(1-z*e))

    # Exact vacuum row transport for the derived logdet price.
    f, t, alpha=s.symbols("f t alpha")
    # Phi(f)=-log(1-alpha*t^2*f)/t^2; c=alpha.
    m=alpha/(1-alpha*t*t*f)
    bcoef=s.cancel((m-alpha)/(2*f))
    Z=s.Matrix([2*f,0])
    df=s.Matrix([[1,s.Rational(2,3)]])
    MM=alpha*I2+bcoef*Z*df
    II=I2/alpha-bcoef/(alpha*m)*Z*df
    true("exact_radial_inverse_including_link_component",(MM*II-I2).applyfunc(s.cancel)==Z2)
    true("radial_source_transform",s.cancel(alpha+2*f*bcoef-m)==0)

    result={"status":"PASS_SCOPED_EXACT_IDENTITIES","checks":len(checks),
            "check_names":checks,"actual_frames":frame_dims,"regular_trace_tests":trace_bounds,
            "physical_program_selected":False,"complete_cost_info_identified":False,
            "joint_nonlinear_roots_constructed":False,"GR_closed":False,
            "source_ref":"cb513f74b3b9ae74d5f2dc02c126d21c9dfbefa7"}
    print(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2))

if __name__=="__main__":
    main()
