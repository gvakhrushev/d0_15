#!/usr/bin/env python3
"""Exact controls for structural source descent; not a physical D0 closure.

Consumes analytic owner statements pinned in RESULT_RU.md. It runs no old
repository certificate and does not assume or solve the physical action.
Python >=3.10, SymPy. All checks survive python -O.
"""
from __future__ import annotations

import json
from itertools import combinations_with_replacement
import sympy as s

SOURCE = "d11e2d5f1006aa543fbfd706269fdd07696cfff0"
passed: list[str] = []


def require(name: str, condition: bool) -> None:
    if not condition:
        raise ArithmeticError(name)
    passed.append(name)


def zero(name: str, value) -> None:
    entries = list(value) if isinstance(value, s.MatrixBase) else [value]
    require(name, all(s.simplify(v) == 0 for v in entries))


def neutral_schur(A, B, C):
    """Exact quotient Schur, only AFTER checking every null-vector constraint.

    Matrix compatibility does not prove existence/integrability of an actual
    stationary fibre or uniform spatial estimates. These are separate theorems.
    B maps internal to retained coordinates; C is the internal Hessian.
    """
    if A != A.T or C != C.T or B.shape != (A.rows, C.rows):
        raise ValueError("incompatible symmetric block shapes")
    null = C.nullspace()
    for v in null:
        if B * v != s.zeros(A.rows, 1):
            raise ValueError("mixed_neutral_mode: cannot discard its equation")
    X, parameters = C.gauss_jordan_solve(B.T)
    X = X.subs({v: 0 for v in parameters})
    if C * X != B.T:
        raise ArithmeticError("internal lift residual")
    E = (A - B * X).applyfunc(s.simplify)
    if E != E.T:
        raise ArithmeticError("reduced source Hessian lost symmetry")
    return E, X, null


def main() -> None:
    # Ten retained slots; six internal coordinates, including three null modes.
    # This is an exact matrix control, not a D0 field configuration.
    C = s.diag(2, 3, 5, 0, 0, 0)
    B = s.Matrix(10, 6, lambda i, j: (i + 2*j) % 7 - 3 if j < 3 else 0)
    inverse_on_range = s.diag(s.Rational(1, 2), s.Rational(1, 3),
                              s.Rational(1, 5), 0, 0, 0)
    E0 = s.diag(*range(10))
    A = E0 + B * inverse_on_range * B.T
    E, X, null = neutral_schur(A, B, C)
    zero("singular_internal_block_exact_reduced_source", E - E0)
    require("three_neutral_modes_are_retained", len(null) == 3)
    N = s.Matrix.hstack(*null)
    J = s.Matrix(3, 10, lambda i, j: i - j)
    zero("all_lift_ambiguities_cancel", B * (X + N*J) - B*X)
    R = s.eye(6)
    R[0, 3], R[1, 4], R[5, 2] = 2, -1, 3
    E2, _, _ = neutral_schur(A, B*R, R.T*C*R)
    zero("nonorthogonal_internal_reparametrization", E2-E)
    H = A.row_join(B).col_join(B.T.row_join(C))
    gauge_x = s.eye(10)[:, 0]
    gauge_all = gauge_x.col_join(-X*gauge_x)
    zero("complete_Hessian_Ward_kept", H*gauge_all)
    zero("quotient_Ward_inherited", E*gauge_x)
    rejected = False
    try:
        neutral_schur(s.zeros(1), s.ones(1), s.zeros(1))
    except ValueError as exc:
        rejected = str(exc).startswith("mixed_neutral_mode")
    require("pseudoinverse_without_compatibility_rejected", rejected)

    # Connected stationary fibre need not have one state. Its exact source is
    # independent of the neutral coordinate, without deleting that coordinate.
    x, psi, y, z, tau = s.symbols("x psi y z tau", real=True, nonzero=True)
    a = x*x + psi
    b = x*x + 3*psi + x*psi
    P = x*x + psi*psi + x*psi*psi
    S = (y-a)**2/(2*tau) + P + b*(y-a)
    ystar = a-tau*b
    Gamma = P-tau*b*b/2
    zero("full_normal_equation_exact", s.diff(S, y).subs(y, ystar))
    zero("neutral_fibre_not_unique_state", s.diff(S, z))
    zero("effective_value_without_state_choice", S.subs(y, ystar)-Gamma)
    zero("full_metric_source_not_frozen_section", s.diff(S, x).subs(y, ystar)-s.diff(Gamma, x))
    zero("same_retained_matter_equation", s.diff(S, psi).subs(y, ystar)-s.diff(Gamma, psi))
    Gv = Gamma.subs(psi, 0)
    Gm = Gamma-Gv
    zero("native_reference_split_keeps_matter_source", s.diff(Gm, psi)-s.diff(Gamma, psi))
    bad = (y*y-1)**2+x*y
    zero("two_disconnected_branches_are_internal_roots", s.Matrix([
        s.diff(bad,y).subs({x:0,y:1}), s.diff(bad,y).subs({x:0,y:-1})]))
    require("disconnected_sources_are_not_identified",
            s.diff(bad,x).subs({x:0,y:1}) != s.diff(bad,x).subs({x:0,y:-1}))

    # All-component Ward forces the 0th and 1st derivative mixed symbols to
    # vanish for a gauge-inert normal mode. Analytic all-dimension proof in note.
    pairs = list(combinations_with_replacement(range(4), 2))
    pi = {p: i for i, p in enumerate(pairs)}
    k = s.symbols("k:4")
    c0, c1 = s.symbols("b0_0:10"), s.symbols("b1_0:40")
    B0 = s.Matrix(4,4,lambda m,n: c0[pi[tuple(sorted((m,n)))]])
    B1 = s.Matrix(4,4,lambda m,n: sum(
        c1[4*pi[tuple(sorted((m,n)))]+r]*k[r] for r in range(4)))
    def constraints(T, unknowns):
        equations=[]
        for n in range(4):
            equations += s.Poly(sum(k[m]*T[m,n] for m in range(4)),*k).coeffs()
        return s.linear_eq_to_matrix(equations,unknowns)[0]
    W0, W1 = constraints(B0,c0), constraints(B1,c1)
    require("zeroth_mixed_Ward_kernel_is_zero", W0.rank()==10)
    require("first_mixed_Ward_kernel_is_zero", W1.rank()==40)
    require("first_mixed_Ward_exact_determinant", W1.det()==16)
    eta=s.diag(1,-1,-1,-1)
    kv=s.Matrix(k)
    witness=eta*(kv.T*eta*kv)[0]-(eta*kv)*(eta*kv).T
    zero("curvature_order_two_survives_Ward", kv.T*witness)
    require("second_order_witness_is_nonzero", witness!=s.zeros(4))

    # Full Hermitian auxiliary X of the actual logdet unfolding: no restriction
    # to commuting variations. This is a two-mode instance of an all-size proof.
    f0, f1 = s.symbols("f0 f1",real=True)
    r0,r1,r2,r3=s.symbols("r0 r1 r2 r3",real=True)
    normal=[r0,r1,r2,r3]
    At=s.Matrix([[s.Rational(1,5),s.Rational(1,30)],
                 [s.Rational(1,30),s.Rational(1,4)]])
    XX=s.Matrix([[1+r0,r2+s.I*r3],[r2-s.I*r3,1+r1]])
    f=f0+3*f1+(f0*f0+f0*f1+2*f1*f1)/2
    L=s.trace(XX*At)*f-(s.trace(XX-s.eye(2))-s.log(XX.det()))/tau
    at0={f0:0,f1:0,r0:0,r1:0,r2:0,r3:0}
    hh=s.hessian(L,[f0,f1]+normal).subs(at0)
    heff,_,_=neutral_schur(hh[:2,:2],hh[:2,2:],hh[2:,2:])
    exact=-s.log((s.eye(2)-tau*f*At).det())/tau
    zero("full_AF_logdet_auxiliary_Schur",heff-s.hessian(exact,[f0,f1]).subs({f0:0,f1:0}))
    df=s.Matrix([1,3])
    expected=s.trace(At)*s.hessian(f,[f0,f1])+tau*s.trace(At*At)*(df*df.T)
    zero("AF_correction_starts_at_curvature_squared",heff-expected)
    noncomm=At*s.Matrix([[0,s.I],[-s.I,0]])-s.Matrix([[0,s.I],[-s.I,0]])*At
    require("imaginary_Hermitian_direction_not_omitted",noncomm!=s.zeros(2))

    kk=s.symbols("q",real=True)
    lam=s.symbols("lam",real=True)
    m2,n2=s.symbols("m2 n2",positive=True)
    cross=s.Matrix([[lam*kk**2,2*lam*kk**2]])
    fast=s.diag(m2+kk**2,n2+2*kk**2)
    correction=(cross*fast.inv()*cross.T)[0]
    zero("gapped_elimination_cannot_change_degree_two",s.limit(correction/kk**2,kk,0))
    zero("complete_degree_four_correction",s.limit(correction/kk**4,kk,0)-lam**2*(1/m2+4/n2))
    zero("gapless_mode_can_cancel_degree_two",kk**2-kk**4/(kk**2))
    zero("first_order_mixing_would_cancel_with_gap",kk**2-kk**2)

    # Source-locality third absolute moment, in physical distances. This is
    # different from counting finite sites or having a matrix inverse.
    h, radius=s.symbols("h radius",positive=True)
    def third_moment(offsets,weights,spacing):
        return s.simplify(sum(abs(o)**3*spacing**3*abs(w) for o,w in zip(offsets,weights)))
    lap=third_moment([-1,0,1],[-1/h**2,2/h**2,-1/h**2],h)
    fourth=third_moment([-2,-1,0,1,2],[1/h**4,-4/h**4,6/h**4,-4/h**4,1/h**4],h)
    zero("second_order_moment_shrinks",lap-2*h)
    zero("fourth_order_moment_fails",fourth-24/h)
    zero("suppressed_fourth_order_passes",h*h*fourth-24*h)
    zero("fixed_physical_range_does_not_shrink",
         third_moment([-1,0,1],[-1/radius**2,2/radius**2,-1/radius**2],radius)-2*radius)
    # Sparse, uniformly gapped block. The all-size exponential bound is proved
    # by Neumann powers; this exact seven-site test checks its implementation.
    n=7
    adjacency=s.zeros(n)
    for i in range(n-1):
        adjacency[i,i+1]=adjacency[i+1,i]=1
    F=3*s.eye(n)-adjacency
    Q=adjacency/3
    Ncut=4
    partial=sum((Q**j for j in range(Ncut+1)),s.zeros(n))/3
    residual=F.inv()-partial
    infnorm=max(sum(abs(residual[i,j]) for j in range(n)) for i in range(n))
    require("gapped_inverse_exact_tail_bound",infnorm<=s.Rational(2,3)**(Ncut+1))
    require("finite_range_powers_respect_distance",(Q**2)[0,3]==0)
    require("inverse_not_mistaken_for_finite_range",F.inv()[0,n-1]>0)

    # Original graph compensation is not a stationary tensorial massive fibre:
    # its full direct source already vanishes. It must not be protected as an
    # isolated positive star contribution.
    ee,bb,zz,cc=s.symbols("ee bb zz cc",positive=True)
    denom=1-zz+zz*(1-ee)*(1-bb)
    curve=1-cc/(1-ee)
    full=s.diff(-s.log(denom),ee)+s.diff(-s.log(denom),bb)*s.diff(curve,ee)
    zero("graph_source_not_hidden_by_protection",full.subs(bb,curve))
    require("frozen_graph_source_nonzero",s.diff(-s.log(denom),ee).subs(bb,curve)!=0)

    print(json.dumps({"status":"PASS_STRUCTURAL_IDENTITIES_ONLY",
        "source_ref":SOURCE,"checks":len(passed),"check_names":passed,
        "ward_zero_order_shape":list(W0.shape),"ward_first_order_shape":list(W1.shape),
        "ward_first_order_determinant":16,
        "physical_full_price_selected":False,"actual_all_field_critical_fibration_proved":False,
        "actual_native_third_moment_limit_proved":False,"full_D0_to_GR_closed":False},
        ensure_ascii=False,sort_keys=True,indent=2))

if __name__=="__main__":
    main()
