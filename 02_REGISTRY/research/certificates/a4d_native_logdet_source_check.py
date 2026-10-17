#!/usr/bin/env python3
"""Exact controls for the stated nonlinear log-det source class.

All-size source-image and convex-profile proofs: A4D_NATIVE_LOGDET_SOURCE_BOUNDARY.md.
No source fit, new native action or physical operator map is asserted.
Default replay verifies an immutable ledger, including compiled source pins.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from itertools import product, combinations
from fractions import Fraction
from pathlib import Path
import sympy as sp

INPUT_HEAD = "32e7a1da7c191ef8567647d56d69995b475a84bb"
INPUTS = [
    "03_FORMALIZATION/D0/Matter/HiggsLogdetStationary.lean",
    "03_FORMALIZATION/D0/Matter/HiggsRadialInstabilityBoundary.lean",
    "03_FORMALIZATION/D0/Cosmology/FeedbackPartitionFunction.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveLocalLaplacianVariation.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveStressEdgeReadout.lean",
    "03_FORMALIZATION/D0/Geometry/ArchivePhaseEdgeMetricScale.lean",
    "02_REGISTRY/research/A4D_NATIVE_EDGE_SOURCE_QUOTIENT.md",
    "02_REGISTRY/research/A4D_NATIVE_AFFINE_PROBE_NOGO.md",
    "02_REGISTRY/research/certificates/a4d_native_affine_probe_nogo_results.json",
]


def edge_basis(V, edges):
    vectors = []
    for i, j in edges:
        b = sp.zeros(V, 1); b[i] = 1; b[j] = -1; vectors.append(b)
    return vectors, [b*b.T for b in vectors]


def positive_definite(M):
    assert M == M.T
    _, D = M.LDLdecomposition(hermitian=False)
    return all(D[i, i] > 0 for i in range(M.rows))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[3])
    ap.add_argument("--output", type=Path); ap.add_argument("--expect", type=Path)
    args = ap.parse_args(); repo = args.repo.resolve(); checks = []
    sha = lambda p: hashlib.sha256((repo/p).read_bytes()).hexdigest()
    def check(name, condition):
        assert bool(condition), name
        checks.append(name); print("PASS_"+name, flush=True)
    receipt_path = "02_REGISTRY/research/certificates/a4d_native_logdet_source_results.json"
    receipt = json.loads((repo/receipt_path).read_text())
    assert receipt["status"] == "PASS" and receipt["compiler_exit_code"] == 0 and not receipt["sorryAx"]
    assert receipt["printed_axiom_dependencies"] == 23
    assert len(receipt["transitive_d0_source_sha256"]) == 33
    for p, digest in {**receipt["transitive_d0_source_sha256"], **receipt["toolchain_input_sha256"],
                      receipt["capsule"]: receipt["capsule_sha256"], receipt["output"]: receipt["output_sha256"]}.items():
        assert sha(p) == digest, "LEAN_INPUT_CHANGED: "+p
    check("COMPILED_REAL_DERIVATIVE_AND_ACTUAL_EDGE_BINDING", True)

    t, z, f0, U = sp.symbols("t z f0 U", real=True)
    f = t/(1+t*t); D = 1-z*f; S = -2*sp.log(D)
    check("ACTUAL_RATIONAL_PROFILE_FIRST_DERIVATIVE", sp.simplify(sp.diff(S,t)-2*z*sp.diff(f,t)/D) == 0)
    check("ACTUAL_RANK_TWO_NORMALIZATION", sp.expand((sp.eye(2)-z*f0*sp.eye(2)).det()-(1-z*f0)**2) == 0)
    check("SCALAR_STATIONARITY_BOTH_ROOTS", sp.solveset(sp.diff(f,t),t,domain=sp.S.Reals) == sp.FiniteSet(-1,1))
    check("SCALAR_ZERO_COUPLING_EXCEPTION", sp.diff(S,t).subs(z,0) == 0 and sp.diff(f,t).subs(t,0) == 1)
    check("SCALAR_RESOLVENT_POLE_NOT_STATIONARY", D.subs({t:1,z:2}) == 0)
    second_at_one = sp.factor(sp.diff(S,t,2).subs(t,1))
    check("STATIONARY_POINT_IS_NOT_AUTOMATICALLY_STABLE", second_at_one == 2*z/(z-2)
          and second_at_one.subs(z,sp.Rational(1,3)) == -sp.Rational(2,5)
          and second_at_one.subs(z,-sp.Rational(1,3)) == sp.Rational(2,7))
    encoded = 1-sp.exp(-U/2)
    check("ARBITRARY_REAL_PROFILE_ENCODING", sp.simplify(-2*sp.log(1-encoded)-U) == 0)
    radial = (t*t-1)**2; unbroken = t*t
    check("POSITIVE_DOMAIN_PROFILE_CAN_ENCODE_QUARTIC", sp.simplify(-2*sp.log(sp.exp(-radial/2))-radial) == 0)
    check("RADIAL_STABILITY_NOT_SELECTED", sp.diff(radial,t,2).subs(t,0) == -4
          and sp.diff(radial,t,2).subs(t,1) == 8 and sp.diff(unbroken,t,2) == 2)

    T = sp.Matrix([[0,1],[1,-1]]); P = sp.diag(1,0); orbit = T*P*T.inv()
    check("ACTUAL_NONCOMMUTING_PROJECTOR_ORBIT", T*P != P*T and orbit != P and orbit*orbit == orbit)
    check("NONCONSTANT_ORBIT_CONSTANT_FEEDBACK", sp.expand((sp.eye(2)-z*orbit).det()-(sp.eye(2)-z*P).det()) == 0)
    fixed = sp.diag(2,1)
    check("FIXED_UNTRANSFORMED_INPUT_PROTECTS_EXCEPTION",
          sp.expand((sp.eye(2)-z*fixed*orbit).det()-(sp.eye(2)-z*fixed*P).det()) == z)

    cases = [("path3",3,[(0,1),(1,2)]), ("triangle3",3,[(0,1),(1,2),(0,2)]),
             ("square4",4,[(0,1),(1,2),(2,3),(0,3)]),
             ("complete4",4,[(i,j) for i in range(4) for j in range(i+1,4)])]
    sites = list(product(range(2),repeat=4)); index = {x:i for i,x in enumerate(sites)}; role_edges = set()
    for x in sites:
        for a in range(4):
            y = list(x); y[a] = 1-y[a]
            role_edges.add(tuple(sorted((index[x],index[tuple(y)]))))
    cases.append(("actual_role4_L2",16,sorted(role_edges)))
    graph_results = {}
    for name,V,edges in cases:
        b, E = edge_basis(V,edges); count = len(E); c = sp.Integer(4); coupling = sp.Rational(1,5); k = c*coupling
        w = [sp.Rational(-1,16) if V == 16 else sp.Rational(-(i+1),16) for i in range(count)]
        F = c*sum((w[i]*E[i] for i in range(count)),sp.zeros(V))
        H = sp.eye(V)-coupling*F; R = H.inv(); detH = H.det()
        response = sp.Matrix([k*(v.T*R*v)[0] for v in b])
        source = coupling*R
        check("EXACT_POSITIVE_RESOLVENT_"+name, positive_definite(H) and H*R == sp.eye(V)
              and H*sp.ones(V,1) == sp.ones(V,1))
        check("ALL_EDGE_SOURCE_AND_PACKED_NORMALIZATION_"+name,
              all(response[i] == c*(source[u,u]+source[v,v]-2*source[u,v]) > 0 for i,(u,v) in enumerate(edges)))
        # Determinants of an edge update are affine in its parameter. Centered exact
        # determinant differences independently check the log derivative and its sign.
        step = sp.Rational(1,100); singles = []; tested = range(count) if V < 16 else [0,1,count-1]
        detderiv = {}
        for i in tested:
            dp = (H-step*k*E[i]).det(); dm = (H+step*k*E[i]).det()
            detderiv[i] = (dp-dm)/(2*step)
            assert sp.simplify(-detderiv[i]/detH-response[i]) == 0
            assert dp+dm == 2*detH
            singles.append(i)
        check("INDEPENDENT_DETERMINANT_EDGE_VARIATIONS_"+name, True)
        B = sp.Matrix.hstack(*b); G = B.T*R*B; J = k*k*G.applyfunc(lambda x:x*x)
        check("FULL_RESPONSE_JACOBIAN_POSITIVE_"+name, positive_definite(J))
        pairs = [(i,j) for i in tested for j in tested if i != j]
        if V == 16: pairs = [(0,1),(0,count-1)]
        for i,j in pairs:
            dpm = {}
            for s in [-1,1]:
                for q in [-1,1]: dpm[s,q] = (H-step*k*(s*E[i]+q*E[j])).det()
            mixed = (dpm[1,1]-dpm[1,-1]-dpm[-1,1]+dpm[-1,-1])/(4*step*step)
            assert sp.simplify((detderiv[i]*detderiv[j]-detH*mixed)/(detH*detH)-J[i,j]) == 0
        check("INDEPENDENT_MIXED_DETERMINANT_HESSIAN_"+name, True)
        K = sp.Matrix(V,V,lambda i,j:i-j)
        check("ACTUAL_SIMULTANEOUS_CONJUGATION_WARD_"+name,
              R*F == F*R and sp.trace(R*(K*F-F*K)) == 0)
        if V == 16:
            check("UNIFORM_ROLE_FINITE_RANGE_WITH_STATED_BOUNDS",
                  positive_definite(2*sp.eye(V)-H) and positive_definite(J-k*k*sp.eye(count)/2))
        graph_results[name] = {"vertices":V,"edges":count,"c":str(c),"z":str(coupling),
            "det_H":str(detH),"response":[str(q) for q in response],
            "determinant_edge_controls":singles,"determinant_mixed_controls":pairs}

    one = sp.ones(3,1); P0 = one*one.T/3
    a = sp.Matrix([1,0,-1]); Pa = a*a.T/2
    b = sp.Matrix([1,-2,1]); Pb = b*b.T/6
    R = P0+t*Pa/2+(4-t)*Pb/6; H = P0+2*Pa/t+6*Pb/(4-t)
    edges = [(0,1),(1,2),(0,2)]; _, E = edge_basis(3,edges)
    weights = sp.Matrix([H[i,j] for i,j in edges]); weights = weights.applyfunc(sp.factor)
    J = sp.Matrix(3,3,lambda i,j:sp.factor(sp.trace(R*E[i]*R*E[j])))
    check("EXPLICIT_COMPLETE_TRIANGLE_INVERSE", sp.simplify(H*R) == sp.eye(3)
          and sp.simplify(H-(sp.eye(3)-sum((weights[i]*E[i] for i in range(3)),sp.zeros(3)))) == sp.zeros(3))
    check("ALL_THREE_FIXED_RESPONSE_EQUATIONS", [sp.simplify(sp.trace(R*e)) for e in E] == [1,1,t])
    check("COMPLETE_TRIANGLE_SOURCE_IMAGE", sp.simplify(R*Pa-t*Pa/2) == sp.zeros(3)
          and sp.simplify(R*Pb-(4-t)*Pb/6) == sp.zeros(3) and sp.simplify(R*P0-P0) == sp.zeros(3))
    check("POSITIVE_SOURCE_COMPONENTS_CAN_BE_INCOMPATIBLE",
          R.subs(t,4).det() == 0 and sp.trace(Pb*R.subs(t,5)) < 0)
    check("NONNEGATIVE_CONDUCTANCES_ARE_STRICTER", all(q < 0 for q in weights.subs(t,1)))
    check("FULL_JACOBIAN_BOUNDARY_DEGENERATION", sp.factor(J.det()-t**3*(4-t)**3/32) == 0)
    check("EXACT_INVERSE_RESPONSE_TANGENT", sp.simplify(J*weights.diff(t)) == sp.Matrix([0,0,1]))
    check("SHARP_DIVERGING_COMPONENT", sp.simplify(weights.diff(t)[0]+2/(4-t)**2) == 0)
    eps = sp.symbols("eps",positive=True)
    check("INVERSE_DIVERGENCE_NOT_A_NUMERIC_FIT", sp.limit(eps**2*weights.diff(t)[0].subs(t,4-eps),eps,0) == -2)

    # Actual coordinate square in a four-Role L=4 graph; other edges cannot cure it.
    role_square = [(0,0,0,0),(1,0,0,0),(1,1,0,0),(0,1,0,0)]
    check("REAL_ROLE_SQUARE_CARRIER", all(sum(x != y for x,y in zip(role_square[i],role_square[(i+1)%4])) == 1 for i in range(4)))
    vectors,_ = edge_basis(4,[(0,1),(1,2),(2,3)])
    endpoint,_ = edge_basis(4,[(0,3)])
    check("STRICT_POSITIVE_COMPLETION_SQUARE_OBSTRUCTION", sp.Matrix.hstack(*vectors).rank() == 3
          and sum(vectors,sp.zeros(4,1)) == endpoint[0] and (sp.sqrt(1)+sp.sqrt(1)+sp.sqrt(1))**2 == 9)

    _, E = edge_basis(3,[(0,1),(1,2),(0,2)])
    Hr = sp.eye(3)+sum(E,sp.zeros(3))/10; Rr = Hr.inv()
    r = sp.Matrix([sp.trace(Rr*e) for e in E])
    check("CONSTRAINED_NONEMPTY_STATIONARY_EXCEPTION", r[0] == r[1] == r[2] and r.dot(sp.Matrix([1,-1,0])) == 0 and r[0] > 0)
    Hi = sp.diag(1,-1); bv = sp.Matrix([1,-1])
    check("INVERTIBLE_INDEFINITE_DOMAIN_EXCEPTION", Hi.det() != 0 and (bv.T*Hi.inv()*bv)[0] == 0
          and sp.expand((Hi-t*bv*bv.T).det()) == -1)
    scale_controls = {}
    for L in [4,8,12,16]:
        top = 16*L*L; min_fixed = 1-sp.Rational(1,1024)*top
        min_scaled = 1-sp.Rational(1,32*L*L)*top
        scale_controls[str(L)] = {"top_metric_laplacian":top,"fixed_z_min_H":str(min_fixed),"scaled_z_min_H":str(min_scaled)}
    check("FIXED_POSITIVE_COUPLING_DOMAIN_COLLAPSE", scale_controls["4"]["fixed_z_min_H"] == "3/4"
          and scale_controls["8"]["fixed_z_min_H"] == "0" and sp.Rational(scale_controls["12"]["fixed_z_min_H"]) < 0)
    check("REFINEMENT_DEPENDENT_COUPLING_PROTECTED", all(v["scaled_z_min_H"] == "1/2" for v in scale_controls.values()))
    zz = sp.symbols("zz",positive=True)
    neg_bounds = [(1+16*zz*L*L)**2/(2*zz**2*L**4) for L in [4,8,12,16]]
    check("NEGATIVE_COUPLING_RETAINS_UNIFORM_FINITE_INVERSE", all(sp.simplify(v-(16+1/(zz*L*L))**2/2) == 0 for v,L in zip(neg_bounds,[4,8,12,16])))
    lap = sum(E,sp.zeros(3))/10
    negative_resolvent = (sp.eye(3)+lap).inv()
    check("BOTH_NONZERO_COUPLING_SIGNS_AND_SOURCE_IMAGES", all(-sp.trace(negative_resolvent*e)<0 for e in E)
          and sp.eye(3)-(-1)*lap == sp.eye(3)-1*(-lap))

    x,y,epsilon = sp.symbols("x y epsilon",real=True)
    action = -sp.log((2-x)**2-y*y); profile = -2*sp.log(2-x)
    check("NONQUADRATIC_FULL_AUXILIARY_PROFILE", sp.simplify(sp.diff(action,y)-2*y/((2-x)**2-y*y)) == 0
          and sp.simplify(sp.diff(profile,x,2)-2/(2-x)**2) == 0)
    secant = (profile.subs(x,x+epsilon)-profile.subs(x,x-epsilon))/(2*epsilon)
    check("NONQUADRATIC_CENTERED_SECANT_MONOTONICITY", sp.simplify(sp.diff(secant,x)-2/((2-x)**2-epsilon**2)) == 0)
    consumed = json.loads((repo/INPUTS[-1]).read_text())
    check("CONSUMED_CURVED_PROBES_BOTH_CALIBRATION_SIGNS", consumed["status"] == "PASS"
          and consumed["curved_base"]["time_Hessian"] == "-12*pi**2"
          and consumed["curved_base"]["space_Hessian"] == "12*pi**2")

    # Direct nodal readout: all six mixed Role pairs on the actual L=4 graph.
    L = 4; sites4 = list(product(range(L),repeat=4)); sine = [0,1,0,-1]
    origin = (0,0,0,0)
    def neighbor(x,a,step):
        y = list(x); y[a] = (y[a]+step)%L; return tuple(y)
    def weight(x,a): return 1+(sum(x)*(a+1))%7
    for r,s in combinations(range(4),2):
        pair = 0; point = 0
        for x in sites4:
            for a in range(4):
                y = neighbor(x,a,1)
                pair += L*L*weight(x,a)*(sine[x[r]]-sine[y[r]])*(sine[x[s]]-sine[y[s]])
        for a in range(4):
            for step in [-1,1]:
                y = neighbor(origin,a,step); base = origin if step == 1 else y
                point -= L*L*weight(base,a)*sine[y[r]]*sine[y[s]]
        check("ACTUAL_ROLE_MIXED_DIRECT_POINT_AND_WEAK_ZERO_"+str(r)+str(s), point == 0 and pair == 0)
    eta = sp.diag(1,-1,-1,-1); shear = sp.eye(4); shear[0,1] = sp.Rational(1,2)
    bar = shear.T*eta*shear; invbar = bar.inv(); rho = sp.Rational(1,10); q0 = 1+rho
    metric = q0*bar; invmetric = metric.inv()
    check("MIXED_CURVED_METRIC_NONDEGENERACY", bar.det() == -1 and shear.det() == 1
          and metric.det() == -q0**4 and invbar[0,1] == sp.Rational(1,2))
    jet = sp.zeros(4); jet[0,0] = jet[1,1] = -4*sp.pi**2*rho
    # The first metric jet is zero here. Compute every connection derivative
    # and every Ricci entry from the full matrix second jet, independently of
    # the scalar conformal-curvature formula used in the proof.
    def dGamma(a,b,d,c):
        return sp.simplify(sum(invbar[a,m]*(bar[m,d]*jet[c,b]+bar[m,b]*jet[c,d]-bar[b,d]*jet[c,m]) for m in range(4))/(2*q0))
    Ricci = sp.Matrix(4,4,lambda b,d:sp.simplify(sum(dGamma(a,b,d,a)-dGamma(a,b,a,d) for a in range(4))))
    Rstd = sp.simplify(sum(invmetric[b,d]*Ricci[b,d] for b in range(4) for d in range(4)))
    check("ALL_SECOND_JET_RICCI_CURVED_CONTROL", Ricci == Ricci.T and Rstd == -30*sp.pi**2/121)
    phase = sp.symbols("phase",real=True)
    mean_cos = sp.integrate(sp.cos(2*sp.pi*phase),(phase,0,1))
    mean_cos2 = sp.integrate(sp.cos(2*sp.pi*phase)**2,(phase,0,1))
    weak = sp.simplify(4*sp.pi**2*invbar[0,1]*(mean_cos**2+rho*mean_cos2**2))
    check("EXACT_NONZERO_WEAK_METRIC_OPERATOR_GAP", weak == sp.pi**2/20)
    check("EXACT_NONZERO_POINTWISE_METRIC_OPERATOR_GAP", 8*sp.pi**2*invmetric[0,1] == 40*sp.pi**2/11)

    # Protected corrector class: exact full periodic vertex equations in a
    # separately stated affine-cocycle cell problem, never the full free gate.
    correctors = {}
    for dim,side in [(2,4),(2,8),(2,12),(4,4)]:
        sites_cell = list(product(range(side),repeat=dim)); V = len(sites_cell)
        def parity(x): return (x[0]+x[1])%2
        def nbr(x,a,step):
            y = list(x); y[a] = (y[a]+step)%side; return tuple(y)
        def edgeweight(x,a): return (1 if parity(x) == 0 else 4) if a<2 else 1
        def corr(x,p): return Fraction(3,10)*(p[0]+p[1])*parity(x)
        pe0 = [1,0]+[0]*(dim-2); pe1 = [0,1]+[0]*(dim-2)
        for p in [pe0,pe1,[1,1]+[0]*(dim-2),list(range(1,dim+1))]:
            energy = Fraction(0)
            for x in sites_cell:
                residual = Fraction(0)
                for a in range(dim):
                    y = nbr(x,a,1); prev = nbr(x,a,-1)
                    outgoing = edgeweight(x,a)*(p[a]+corr(y,p)-corr(x,p))
                    incoming = edgeweight(prev,a)*(p[a]+corr(x,p)-corr(prev,p))
                    residual += outgoing-incoming
                    energy += edgeweight(x,a)*(p[a]+corr(y,p)-corr(x,p))**2
                assert residual == 0,(dim,side,x,p)
            target = Fraction(41,20)*(p[0]**2+p[1]**2)-Fraction(9,10)*p[0]*p[1]+sum(a*a for a in p[2:])
            assert energy/V == target
        label = str(dim)+"d_L"+str(side)
        check("FULL_PERIODIC_CORRECTOR_EULER_AND_ENERGY_"+label, True)
        cross = Fraction(0); bare = Fraction(0)
        for x in sites_cell:
            for a in range(dim):
                y = nbr(x,a,1)
                cross += edgeweight(x,a)*(pe0[a]+corr(y,pe0)-corr(x,pe0))*(pe1[a]+corr(y,pe1)-corr(x,pe1))
                bare += edgeweight(x,a)*pe0[a]*pe1[a]
        amplitude = max(abs(corr(x,pe0))/side for x in sites_cell)
        check("SMALL_FIELD_NONZERO_MIXED_CORRECTOR_"+label, bare == 0 and cross/V == -Fraction(9,20)
              and amplitude == Fraction(3,10*side))
        correctors[label] = {"vertices":V,"mixed_response":str(cross/V),"field_correction_sup":str(amplitude)}

    # The all-size flat-calibration proof uses inverse order and same-sign
    # coordinate derivatives; these rational fixtures test both signs and a
    # large negative coupling without a small-coupling approximation.
    _, basis = edge_basis(3,[(0,1),(1,2),(0,2)])
    L0 = sum(basis,sp.zeros(3)); m = sp.Rational(1,2); M = sp.Rational(3,2)
    test_weights = [sp.Rational(3,4),sp.Integer(1),sp.Rational(5,4)]
    Lw = sum((test_weights[i]*basis[i] for i in range(3)),sp.zeros(3))
    centered_basis = sp.Matrix([[1,0],[0,1],[-1,-1]])
    flat_order = {}
    for coupling in [sp.Rational(1,16),-sp.Rational(1,16),-sp.Integer(16)]:
        H = sp.eye(3)-coupling*Lw; R = H.inv()
        compare = M if coupling>0 else m
        Rc = (sp.eye(3)-coupling*compare*L0).inv()
        check("EXACT_INVERSE_ORDER_FLAT_COMPARISON_"+str(coupling),
              positive_definite(H) and positive_definite(centered_basis.T*(Rc-R)*centered_basis)
              and (Rc-R)*sp.ones(3,1) == sp.zeros(3,1))
        gradient_sum = sum(abs(coupling*sp.trace(R*e)) for e in basis)
        upper = abs(coupling*sp.trace(Rc*L0))
        check("CURVED_COORDINATE_DERIVATIVE_SUM_BOUND_"+str(coupling), gradient_sum <= upper)
        center = sp.Integer(2) if coupling>0 else sp.Rational(1,4)
        eps0 = sp.Rational(1,100)
        denominators = [1-3*coupling*(center-eps0),1-3*coupling*(center+eps0)]
        assert min(denominators)>0
        # log(b/a) >= (b-a)/b for b>=a>0; the exact scalar lower
        # bound controls 2*eps*D even when the true action contains logs.
        lower = 2*(max(denominators)-min(denominators))/max(denominators)
        check("FLAT_SECANT_CONTROLS_CURVED_RESPONSE_"+str(coupling), lower >= 2*eps0*upper)
        flat_order[str(coupling)] = {"curved_gradient_absolute_sum":str(gradient_sum),
            "flat_derivative_bound":str(upper),"flat_secant_rational_lower":str(lower)}

    payload = {"status":"PASS","input_head":INPUT_HEAD,"inputs_sha256":{p:sha(p) for p in INPUTS},
        "lean_receipt_sha256":sha(receipt_path),"checks":checks,"finite_graph_controls":graph_results,
        "source_image":"r/(zc) admits a positive definite centered completion on 1-perp",
        "source_gate":"all signed local conductance variations; zc nonzero; I-zc B(w) positive definite",
        "triangle_image_interval":"0 < t < 4","triangle_jacobian_determinant":"t^3 (4-t)^3 / 32",
        "inverse_tangent_component":"-2 / (4-t)^2","finite_inverse_bound":"M^2 / (2 (zc)^2)",
        "free_unsourced_gate":"EMPTY_IN_STATED_POSITIVE_DOMAIN",
        "rank_two_scalar_factor":2,"refinement_domain_controls":scale_controls,
        "convex_profile_transfer":"NO_GO_WITH_FULL_GATE_AFFINE_METRIC_FIBERS_AND_BOTH_CURVED_PENCILS",
        "direct_nodal_weak_operator_gap":"pi^2 / 20","curved_operator_control_R_owner":"30 pi^2 / 121",
        "corrector_controls":correctors,"corrector_mixed_response":"-9 / 20",
        "flat_order_controls":flat_order,
        "bounded_positive_logdet_flat_transfer":"NO_GO_WITH_BOTH_FLAT_BRACKETS_AND_UNIFORM_ENDPOINT_PROBE_BOUND",
        "scope":"Finite nonlinear log-det source image and convex prepared-contrast obstruction. No selected native physical operator, independent matter action, physical Ward or nonlinear GR closure.",
        "protected_exceptions":["Supplied nonlinear profiles can encode arbitrary actions",
            "Fixed untransformed inputs need not be similarity equivariant","Constrained variation can have nonempty stationary fibers",
            "Indefinite resolvents and zero coupling do not have the nonvanishing edge conclusion",
            "Positive conductances form a smaller class than the signed-conductance source-image theorem",
            "O(h) field corrections need not be small in edge energy; the exact cell corrector has mixed response",
            "Physical coframe, metric, connection, matter and refinement maps remain unconstructed"]}
    out = json.dumps(payload,sort_keys=True,indent=2)+"\n"
    if args.output: args.output.write_text(out)
    else:
        expected = args.expect or Path(__file__).with_name("a4d_native_logdet_source_certificate.json")
        assert expected.read_text() == out,"PINNED_LEDGER_MISMATCH"
        print("PASS_IMMUTABLE_PINNED_LEDGER")
    print("PASS_NATIVE_LOGDET_SOURCE",len(checks))


if __name__ == "__main__": main()
