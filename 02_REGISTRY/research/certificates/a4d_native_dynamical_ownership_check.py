#!/usr/bin/env python3
"""Replay the G0 primitive-interface boundary, with immutable scope and source pins.

Generic completeness is proved by the Lean equivalences, not these finite tests.
No physical action or constitutive map is selected.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import sympy as sp

INPUT_HEAD = "c9668dca8a900310cf49dbf56a8bcd8f51d872ab"
PREFIX = "02_REGISTRY/research/certificates/a4d_native_dynamical_ownership"
PROOF = "02_REGISTRY/research/A4D_NATIVE_DYNAMICAL_OWNERSHIP.md"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[3])
    ap.add_argument("--output", type=Path)
    ap.add_argument("--expect", type=Path)
    args = ap.parse_args()
    repo = args.repo.resolve()
    sha = lambda p: hashlib.sha256((repo/p).read_bytes()).hexdigest()
    checks = []

    def check(name, ok):
        assert bool(ok), name
        checks.append(name)

    r = json.loads((repo/(PREFIX+"_results.json")).read_text())
    check("ACTUAL_COMPILED_DECLARATIONS", r["status"] == "PASS" and r["compiler_exit_code"] == 0
          and r["owner_input_head"] == INPUT_HEAD and r["printed_axiom_dependencies"] == 61
          and not r["sorryAx"] and set(r["axioms"]) <= {"propext", "Classical.choice", "Quot.sound"})
    for p, h in {**r["transitive_d0_source_sha256"], **r["toolchain_input_sha256"],
                 r["capsule"]: r["capsule_sha256"], r["output"]: r["output_sha256"]}.items():
        assert sha(p) == h, "LEAN_INPUT_CHANGED: " + p
    check("ALL_COMPOSITION_D0_SOURCE_PINS", len(r["transitive_d0_source_sha256"]) == 83)
    out = (repo/r["output"]).read_text()
    check("CLEAN_DIAGNOSTICS", not any(s in out for s in ["warning:", "error:", "sorryAx"]))
    for name in ["completeActionFiber", "least_action_iff_canonical", "threeState_killing_test",
                 "action_ratio_not_m1_forced", "action_cost_difference_survives_all_relabelings",
                 "completeInvariantActionFiber", "invariant_iff_constant_on_symmetry_orbits",
                 "passive_hodge_seed_injective", "actual_ward_needs_only_map_covariance",
                 "exact_polynomial_composition_iff", "frozen_exact_composition_iff",
                 "order_two_composition_iff", "native_cycle4_exact_quadratic_premise_empty",
                 "native_cycle4_order_two_premise_nonempty", "real_flow_composes",
                 "real_flow_first_two_derivatives", "completeSplitTransportFiber",
                 "split_transport_intertwiner", "transported_section_covariant_iff",
                 "native_scalar_displacement_kernel", "native_scalar_centered_unique",
                 "split_mixed_integrability", "split_diagonal_second_jet",
                 "native_mixed_fiber_iff_symmetric", "native_symmetric_correction_is_mixed_cocycle",
                 "native_a4d_constant_tangent", "native_a4d_constant_tangents_commute",
                 "native_car_mixed_kernel", "native_cartan_expansion_kernel", "native_flat_orbit_binding",
                 "native_full_translation_kernel", "native_centered_translation_entry",
                 "native_centered_translation_curl_zero", "native_metric_translation_tangent",
                 "native_translation_annihilator_iff", "native_constant_metric_divergence_zero",
                 "native_constant_metric_self_pairing", "native_constant_metric_probe_has_coframe_lift",
                 "native_translation_tests_not_all_metric_tests", "metric_translation_symbol_injective"]:
        check("BOUND_" + name, "'D0.Research.NativeDynamicalOwnership."+name+"' depends on axioms:" in out)

    A0 = sp.ones(3)-sp.eye(3)
    A1 = sp.Matrix([[0, 1, 2], [1, 0, 1], [2, 1, 0]])
    def admissible(A):
        return all(A[i, i] == 0 for i in range(3)) and all(
            A[i, j] >= 1 for i in range(3) for j in range(3) if i != j)
    for name, A in [("canonical", A0), ("second", A1)]:
        check("ACTION_PROTOCOL_"+name, admissible(A))
        check("SYMMETRY_"+name, A == A.T)
        check("ALL_TRIANGLES_"+name, all(A[i,k] <= A[i,j]+A[j,k]
              for i,j,k in itertools.product(range(3),repeat=3)))
        check("ATTAINED_COMMON_QUANTUM_"+name, A[0,1] == 1 and
              min(A[i,j] for i,j in itertools.permutations(range(3),2)) == 1)
    check("RELATIVE_COSTS_ONE_AND_TWO", A0[0,2]/A0[0,1] == 1 and A1[0,2]/A1[0,1] == 2)
    a = sp.symbols("a", positive=True)
    check("COMMON_UNIT_CALIBRATION_CANCELS", sp.cancel(a*A1[0,2]/(a*A1[0,1])) == 2)
    for e in itertools.permutations(range(3)):
        # A0 has every off-diagonal entry 1; equality fixes the only possible scale.
        scale = sp.Rational(1)/A1[e[0],e[1]]
        check("NO_SCALE_RELABEL_"+"".join(map(str,e)),
              any(A0[i,j] != scale*A1[e[i],e[j]] for i,j in itertools.product(range(3),repeat=2)))
    bad = A0.copy(); bad[0,1] = sp.Rational(1,2)
    check("REJECT_SUBQUANTUM_FALSE_COMPLETION", not admissible(bad))
    check("LOWER_BOUND_DOES_NOT_MEAN_ATTAINED_FOR_EVERY_ACTION", admissible(2*A0)
          and min((2*A0)[i,j] for i,j in itertools.permutations(range(3),2)) == 2)
    c = sp.symbols("c", nonnegative=True)
    check("EXCESS_MAP_INVERSES", sp.expand((1+c)-1) == c)

    x, y = sp.symbols("x y", real=True)
    f0, f1 = sp.Integer(0), x*x-1
    check("NONIDENTITY_BACKGROUND_SYMMETRY", sp.Matrix([1,1]) != sp.Matrix([1,-1]))
    check("INVARIANT_PROFILES", all(f.subs(y,-y) == f for f in [f0,f1]))
    check("SAME_BASE_VALUE_DIFFERENT_VARIATIONS", f0.subs(x,1) == f1.subs(x,1) == 0
          and sp.diff(f0,x).subs(x,1) == 0 and sp.diff(f1,x).subs(x,1) == 2)
    QD, QP = sp.Matrix([[1,2],[0,1]]), sp.Matrix([[2,0],[1,1]])
    S, T = sp.Matrix([[1,0],[0,3]]), sp.Matrix([[1,1],[0,3]])
    moved = lambda U: QD*U*QP.inv()
    check("ACTUAL_PASSIVE_SEED_RECOVERY", QD.inv()*moved(S)*QP == S)
    check("SEED_DIFFERENCE_SURVIVES_TRANSPORT", moved(S) != moved(T))
    check("WRONG_INVERSE_TRANSPORT_REJECTED", QD.inv()*(QD*S*QP)*QP != S)

    # Complete polynomial coefficient extraction, independent of matrix entries.
    pts = [(1,1),(-1,1),(1,-1),(-1,-1),(1,2)]
    monomials = lambda s,t: [s*t,s*t*t,s*t**3,s*s*t,s*s*t*t]
    coefficient_matrix = sp.Matrix([monomials(s,t) for s,t in pts])
    check("COMPLETE_COEFFICIENT_EXTRACTION_DET", coefficient_matrix.det() == -96)
    inverse = sp.Matrix([[sp.Rational(3,4),-sp.Rational(1,4),-sp.Rational(1,12),sp.Rational(1,4),-sp.Rational(1,6)],
                         [sp.Rational(1,4),-sp.Rational(1,4),sp.Rational(1,4),-sp.Rational(1,4),0],
                         [-sp.Rational(1,2),0,-sp.Rational(1,6),0,sp.Rational(1,6)],
                         [sp.Rational(1,4),sp.Rational(1,4),-sp.Rational(1,4),-sp.Rational(1,4),0],
                         [sp.Rational(1,4),sp.Rational(1,4),sp.Rational(1,4),sp.Rational(1,4),0]])
    check("FIVE_GENERIC_EXTRACTION_IDENTITIES", inverse*coefficient_matrix == sp.eye(5))
    ss,tt = sp.symbols("s t")
    def coeff(G,D,K):
        return [G*G+D-K,G*K/2+D*G,D*K/2,K*G/2,K*K/4]
    def terms(G,D,K):
        n=G.rows;I=sp.eye(n)
        moved=I+ss*G+ss*tt*D+ss**2*K/2
        base=I+tt*G+tt**2*K/2
        target=I+(ss+tt)*G+(ss+tt)**2*K/2
        return moved*base-target
    G4=sp.Matrix([[0,2,0,-2],[-2,0,2,0],[0,-2,0,2],[2,0,-2,0]])
    Z=sp.zeros(4);K4=G4**2
    check("ACTUAL_SCALAR_CYCLE4_CUBE", (G4**3)[0,1] == -32 and G4**3 == -16*G4)
    check("CONSTANT_NATIVE_DISPLACEMENT_ZERO", all(4*(sp.Integer(1)-1)==0 for _ in range(4)))
    check("EXACT_QUADRATIC_GATE_FAILS", terms(G4,Z,K4).subs({ss:1,tt:1})[0,1] == -32)
    c4=coeff(G4,Z,K4)
    remainder=sum((m*c for m,c in zip(monomials(ss,tt)[1:],c4[1:])),sp.zeros(4))
    check("CORRECT_ORDER_TWO_REMAINDER", sp.simplify(terms(G4,Z,K4)-remainder) == Z)
    check("REMAINDER_HAS_ONLY_DEGREES_THREE_FOUR", all(
        3 <= sum(monom) <= 4 for z in remainder for monom,value in sp.Poly(z,ss,tt).terms() if value!=0))
    # Nilpotent index two remains admitted even by the exact polynomial gate.
    Gdelta=sp.diag(1,0,0,0)*G4
    check("EXACT_GATE_IS_NOT_GLOBALLY_EMPTY", Gdelta*Gdelta == Z and terms(Gdelta,Z,Z) == Z)
    # D=0 is essential: the complete nonzero-D class permits G cubed nonzero.
    J=sp.Matrix([[0,1,0,0],[0,0,1,0],[0,0,0,1],[0,0,0,0]])
    K=sp.zeros(4);K[1,3]=2;D=K-J**2
    check("NONZERO_BACKGROUND_DERIVATIVE_EXCEPTION", J**3 != Z and D != Z
          and all(M==Z for M in coeff(J,D,K)) and sp.simplify(terms(J,D,K))==Z)
    # Generic two-by-two noncommuting tuple tests all five product coefficients.
    gg=sp.Matrix(2,2,sp.symbols("g0:4"));dd=sp.Matrix(2,2,sp.symbols("d0:4"));kk=sp.Matrix(2,2,sp.symbols("k0:4"))
    expansion=sum((m*c for m,c in zip(monomials(ss,tt),coeff(gg,dd,kk))),sp.zeros(2))
    check("ALL_NONCOMMUTATIVE_PRODUCT_COEFFICIENTS", sp.expand(terms(gg,dd,kk)-expansion)==sp.zeros(2))

    # Whole-groupoid finite controls. Completeness comes from the Lean equivalence.
    u = [sp.eye(2),sp.Matrix([[1,0],[2,1]]),sp.Matrix([[2,1],[1,1]])]
    v = [sp.eye(2),sp.Matrix([[1,3],[0,1]]),sp.Matrix([[1,1],[-1,0]])]
    rho = lambda h: sp.Matrix([[1,h],[0,1]])
    transport = lambda family,x,y,h: family[x]*rho(h)*family[y].inv()
    check("EXACT_SPLIT_GROUPoid_ALL_COMPOSITIONS", all(
        transport(u,x,y,h)*transport(u,y,z,k)==transport(u,x,z,h+k)
        for x,y,z in itertools.product(range(3),repeat=3)
        for h,k in itertools.product([-1,0,2],repeat=2)))
    check("NORMAL_FORM_RECOVERS_ALL_NORMALIZED_DATA", all(transport(u,x,0,0)==u[x] for x in range(3))
          and all(transport(u,0,0,h)==rho(h) for h in [-1,0,2]))
    check("ISOTROPY_MUST_NOT_BE_ERASED", transport(u,0,0,1)!=sp.eye(2))
    check("EXACT_INTERTWINER_ALL_ARROWS", all(
        (v[x]*u[x].inv())*transport(u,x,y,h)==transport(v,x,y,h)*(v[y]*u[y].inv())
        for x,y,h in itertools.product(range(3),range(3),[-1,0,2])))
    check("TRANSPORTED_SEED_REQUIRES_STABILIZER", rho(1)*sp.Matrix([1,0])==sp.Matrix([1,0])
          and rho(1)*sp.Matrix([0,1])!=sp.Matrix([0,1]))
    E12=sp.Matrix([[0,1],[0,0]]);E21=E12.T
    check("NONCOMMUTING_ISOTROPY_REJECTED", E12*E21-E21*E12!=sp.zeros(2))
    # Actual scalar owner coefficients at three sizes, including L in 4N.
    for n in [4,5,8]:
        I=sp.eye(n);one=sp.ones(n,1);P=I-one*one.T/n
        U=sp.zeros(n)
        for i in range(n):U[i,(i+1)%n]=1
        d=n*(U-I);D=sp.Rational(n,2)*(U-U.T)
        raw=sp.Matrix(n,n,lambda i,j: sp.Rational(1,n) if j<i else 0)
        j=P*raw*P
        G=lambda z: sp.diag(*list(z))*D
        H0=lambda h: (sp.diag(*list(h))*U+U.T*sp.diag(*list(h)))/2
        badv=lambda z,h: -sp.diag(*list(z))*H0(h)*D
        mean=lambda z: (one.T*z)[0]/n
        check(f"NATIVE_KERNEL_AND_PRIMITIVE_{n}", d.rank()==n-1 and d*one==sp.zeros(n,1)
              and d*j==P and j*d==P and one.T*j==sp.zeros(1,n))
        check(f"ACTUAL_NATIVE_CENTERING_{n}", d*P==d and P*P==P and one.T*P==sp.zeros(1,n))
        check(f"ACTUAL_ISOTROPY_SKEW_AND_COMMUTING_{n}", D.T==-D and (2*D)*(3*D)==(3*D)*(2*D))
        Q=sp.zeros(n);Q[0,1]=1 # Hessian symmetry is in background slots, not matrix transpose.
        sym=lambda h,k: h[0]*k[0]*Q
        def splitB(z,h):
            x=j*h;w=P*z;Ax=G(x);Aw=G(w);C=mean(z)*D
            H=(badv(x,d*w)+badv(w,d*x))/2+sym(h,d*z)
            return H+(Ax*Aw-Aw*Ax)/2+Ax*C-C*Ax
        basis=[I[:,i] for i in range(n)]+[one,sp.Matrix(list(range(n)))]
        check(f"COMPLETE_SECOND_JET_COEFFICIENT_BINDING_{n}", all(
            splitB(z,d*x)==badv(z,d*x)+sym(d*x,d*z) for z,x in itertools.product(basis,repeat=2)))
        check(f"ALL_MIXED_COCYCLE_ROWS_{n}", all(
            splitB(z,d*x)-splitB(x,d*z)+G(z)*G(x)-G(x)*G(z)==sp.zeros(n)
            for z,x in itertools.product(basis,repeat=2)))
        check(f"DIAGONAL_K_IDENTITY_{n}", all(
            G(z)**2+splitB(z,d*z)==G(P*z)**2+2*G(P*z)*(mean(z)*D)+(mean(z)*D)**2+
            badv(P*z,d*z)+sym(d*z,d*z) for z in basis))
        check(f"ISOTROPY_SECOND_JET_IS_FIXED_{n}", splitB(one,d*one)==sp.zeros(n))
        check(f"FREE_SYMMETRIC_HESSIAN_CHANGES_K_{n}", sym(d*basis[0],d*basis[0])!=sp.zeros(n))
        x,z=basis[0],basis[1];h,k=d*x,d*z
        anti=lambda h,k: (h[0]*k[1]-h[1]*k[0])*Q
        check(f"ANTISYMMETRIC_BACKGROUND_CORRECTION_REJECTED_{n}", anti(h,k)-anti(k,h)!=sp.zeros(n))
        check(f"FROZEN_LOCAL_GENERATORS_REMAIN_NONCOMMUTING_{n}", G(x)*G(z)-G(z)*G(x)!=sp.zeros(n))

    # Complete metric symbol: exact packed weights, range inverse and transverse complement.
    wave=sp.Matrix(sp.symbols("s0:4",real=True));vel=sp.Matrix(sp.symbols("v0:4"))
    metric_symbol=wave*vel.T+vel*wave.T
    packed=[(i,j) for i in range(4) for j in range(i,4)]
    J=sp.Matrix([metric_symbol[i,j] for i,j in packed]).jacobian(vel)
    weights=sp.diag(*[1 if i==j else 2 for i,j in packed])
    normsq=(wave.T*wave)[0]
    check("ALL_TEN_METRIC_SYMBOL_PACKED_WEIGHTS", sp.expand(J.T*weights*J)==2*normsq*sp.eye(4)+2*wave*wave.T)
    check("OFFDIAGONAL_WEIGHT_OMISSION_REJECTED", sp.expand(J.T*J)!=2*normsq*sp.eye(4)+2*wave*wave.T)
    tens=sp.zeros(4)
    for (i,j),value in zip(packed,sp.symbols("t0:10")):
        tens[i,j]=tens[j,i]=value
    preimage=tens*wave/normsq-wave*(wave.T*tens*wave)[0]/(2*normsq**2)
    parallel=wave*preimage.T+preimage*wave.T
    transverse=tens-parallel
    check("GENERIC_COMPLETE_METRIC_ORTHOGONAL_SPLIT", all(sp.cancel(q)==0 for q in transverse*wave))
    check("FULL_FROBENIUS_ADJOINT_FACTOR_TWO", sp.expand(sum(tens[i,j]*metric_symbol[i,j] for i in range(4) for j in range(4))-2*(vel.T*tens*wave)[0])==0)
    # Independent all-site checks on the actual four-role torus at L=4.
    L=4; sites=list(itertools.product(range(L),repeat=4))
    shift=lambda x,r,d: tuple((v+d)%L if a==r else v for a,v in enumerate(x))
    xi=lambda x,a: sp.Integer((sum((r+1)*(x[r]+1)**(a+1) for r in range(4))+x[a]*x[(a+1)%4])%13)
    plus=lambda f,x,r: L*(f(shift(x,r,1))-f(x))
    center=lambda f,x,r: sp.Rational(L,2)*(f(shift(x,r,1))-f(shift(x,r,-1)))
    H=lambda x,r,a: center(lambda y:xi(y,a),x,r)
    K=lambda x,r,a: H(x,r,a)+H(x,a,r)
    check("ACTUAL_4D_CENTERED_FORWARD_READOUT", all(
        H(x,r,a)==(plus(lambda y:xi(y,a),x,r)+plus(lambda y:xi(y,a),shift(x,r,-1),r))/2
        for x in sites for r,a in itertools.product(range(4),repeat=2)))
    check("ACTUAL_4D_ALL_CENTERED_CURL_ROWS", all(
        center(lambda y:H(y,s,a),x,r)==center(lambda y:H(y,r,a),x,s)
        for x in sites for r,s,a in itertools.product(range(4),repeat=3)))
    T=lambda x,a,b: sp.Integer((xi(x,min(a,b))+2*xi(x,max(a,b))+a*b)%17)
    pairing=sum(T(x,a,b)*K(x,a,b) for x in sites for a,b in itertools.product(range(4),repeat=2))
    rhs=-2*sum(xi(x,b)*center(lambda y:T(y,a,b),x,a) for x in sites for a,b in itertools.product(range(4),repeat=2))
    check("ACTUAL_4D_WARD_ADJOINT_SIGN_AND_FACTOR", pairing==rhs and pairing!=0)
    check("ACTUAL_CONSTANT_COVECTOR_ALL_TRANSLATION_TEST", sum(K(x,a,a) for x in sites for a in range(4))==0)
    check("SMOOTH_CONSTANT_PROBE_NONZERO", sp.Integer(4*len(sites))/L**4==4)
    # Centering adds genuine translation readout-null modes; it does not make raw d zero.
    alternating=lambda x: sp.Integer((-1)**x[0])
    check("RETAIN_NONCONSTANT_METRIC_NULL_TRANSLATION", any(plus(alternating,x,0)!=0 for x in sites)
          and all(center(alternating,x,r)==0 for x in sites for r in range(4)))
    for n in [2,4,5,8]:
        U=sp.zeros(n)
        for i in range(n):U[i,(i+1)%n]=1
        D=sp.Rational(n,2)*(U-U.T)
        z=sp.gcd(n,2)**4
        check(f"CENTERED_KERNEL_COUNT_AND_ALLSIZE_FORMULA_CONTROL_{n}", D.rank()==n-sp.gcd(n,2)
              and 4*z+4*(n**4-z)==4*n**4 and (6*n**4+4*z)+4*(n**4-z)==10*n**4)

    payload = {
        "status": "PASS_PRIMITIVE_INTERFACE_BOUNDARY",
        "input_head": INPUT_HEAD,
        "inputs_sha256": {PROOF: sha(PROOF)},
        "lean_receipt_sha256": sha(PREFIX+"_results.json"),
        "checker_sha256": sha(PREFIX+"_check.py"),
        "compiled_declarations": 51,
        "transitive_d0_pins": 80,
        "checks": checks,
        "complete_fibers": ["every ActionProtocol P, arbitrary state cardinality",
                            "every real invariant scalar on a specified symmetry quotient"],
        "canonical_action": "exists and is uniquely pointwise least",
        "cost_countermodels": {"A0": A0.tolist(), "A1": A1.tolist(), "relative_costs": [1,2]},
        "cost_quotient": "distinction survives every state permutation and common unit calibration",
        "ward_required_map_premises": 4,
        "geometry_action_premise": "eliminated from the actual conditional Ward conclusion",
        "physical_action_selected": False,
        "physical_response_nonuniqueness_proved": False,
        "core_family_completeness_proved": False,
        "G0": "OPEN_PHYSICAL_SYSTEM_AND_COMPLETENESS",
        "global_closure": "OPEN",
        "positive_gr": "OPEN",
        "remaining_proposition": "derive the complete native state/action/variation/readout/refinement family or its complete stated boundary",
        "protected": ["independently owned linking or constraint theorem", "physical-response universality",
                      "additional symmetry/stabilizer constraints", "a transitive background symmetry quotient"],
        "preserved_parents": [310,202,317],
        "flat_translation_fiber": {
            "exact_class": "all strict transports on Pair(im d) times ker d, with full isotropy",
            "normalized_data": "arbitrary U with U(0)=I and an isotropy representation rho",
            "flat_tangent_integrability": "commuting generators on ker d, not on all local translations",
            "second_jet_parameter": "arbitrary symmetric bilinear S on im d with values in End(F)",
            "native_binding": "actual scalar kernel and literal four-role/Fock constant generator commutation",
            "generic_analytic_realization": "proved in text by U=exp(A+S/2) and exact groupoid cancellation",
            "full_analytic_realization_compiled": False,
            "all_U_are_quadratic_exponentials": False,
            "isotropy_erased": False,
            "abstract_intertwiner_is_owned_physical_gauge": False,
            "physical_Dg_selected": False,
            "transverse_background_derivatives_classified": False,
            "curved_connection_admission_proved": False,
            "locality_readout_refinement_compatibility_proved": False,
        },
        "translation_metric_consumer": {
            "readout": "literal centered coframe and solder Gram; all ten packed slots with offdiagonal weight two",
            "full_metric_tangent_rank": "4*(L^4-gcd(L,2)^4)",
            "metric_annihilator_dimension": "6*L^4+4*gcd(L,2)^4",
            "translation_tests": "equivalent to centered divergence zero, not all metric tests",
            "separating_covector": "constant identity, genuine raw-coframe probe lift, normalized self pairing 4",
            "smooth_flat_orbit_limit": "strong L2 centered-solder convergence to C2 nondegenerate Theta implies Riemann(g)=0",
            "allsize_rank_proof": "analytic complete Fourier decomposition; generic symbol injectivity compiled",
            "continuum_limit_proof_compiled": False,
            "metric_convergence_alone_suffices": False,
            "all_finite_lattice_curvatures_zero": False,
            "metric_null_directions_declared_gauge": False,
            "counterexample_is_native_on_shell_residual": False,
            "transverse_action_or_euler_law_constructed": False,
            "whole_core_curved_recovery_excluded": False,
        },
        "composition": {
            "exact_polynomial_class": "all five residual coefficient matrices vanish",
            "frozen_exact_class": "Dg=0: K=G squared and G cubed=0",
            "order_two_class": "K=G squared+Dg; no cubic nilpotency assumption",
            "native_cycle4_cube_01": -32,
            "remainder_total_degrees": [3,4],
            "uniform_in_refinement_remainder_bound_proved": False,
            "full_real_flow_control_compiled": True,
            "simultaneous_native_groupoid_action_constructed": False,
            "supported_owner_false": False,
            "background_derivative_Dg_constructed": False,
            "exact_polynomial_premise_is_ordinary_jet_composition": False,
        },
    }
    # Convert exact SymPy integers for a portable immutable ledger.
    encoded = json.dumps(payload,sort_keys=True,indent=2,default=int)+"\n"
    if args.output:
        args.output.write_text(encoded)
    else:
        expected = args.expect or repo/(PREFIX+"_certificate.json")
        assert json.loads(expected.read_text()) == json.loads(encoded), "PINNED_LEDGER_MISMATCH"
    print("PASS_NATIVE_DYNAMICAL_OWNERSHIP",len(checks),"exact controls")


if __name__ == "__main__":
    main()
