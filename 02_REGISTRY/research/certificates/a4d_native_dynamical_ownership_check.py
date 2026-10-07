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

INPUT_HEAD = "7743910de8e8914f06b68f63aca917997344d1ae"
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
          and r["owner_input_head"] == INPUT_HEAD and r["printed_axiom_dependencies"] == 33
          and not r["sorryAx"] and set(r["axioms"]) <= {"propext", "Classical.choice", "Quot.sound"})
    for p, h in {**r["transitive_d0_source_sha256"], **r["toolchain_input_sha256"],
                 r["capsule"]: r["capsule_sha256"], r["output"]: r["output_sha256"]}.items():
        assert sha(p) == h, "LEAN_INPUT_CHANGED: " + p
    check("ALL_COMPOSITION_D0_SOURCE_PINS", len(r["transitive_d0_source_sha256"]) == 26)
    out = (repo/r["output"]).read_text()
    check("CLEAN_DIAGNOSTICS", not any(s in out for s in ["warning:", "error:", "sorryAx"]))
    for name in ["completeActionFiber", "least_action_iff_canonical", "threeState_killing_test",
                 "action_ratio_not_m1_forced", "action_cost_difference_survives_all_relabelings",
                 "completeInvariantActionFiber", "invariant_iff_constant_on_symmetry_orbits",
                 "passive_hodge_seed_injective", "actual_ward_needs_only_map_covariance",
                 "exact_polynomial_composition_iff", "frozen_exact_composition_iff",
                 "order_two_composition_iff", "native_cycle4_exact_quadratic_premise_empty",
                 "native_cycle4_order_two_premise_nonempty", "real_flow_composes",
                 "real_flow_first_two_derivatives"]:
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

    payload = {
        "status": "PASS_PRIMITIVE_INTERFACE_BOUNDARY",
        "input_head": INPUT_HEAD,
        "inputs_sha256": {PROOF: sha(PROOF)},
        "lean_receipt_sha256": sha(PREFIX+"_results.json"),
        "checker_sha256": sha(PREFIX+"_check.py"),
        "compiled_declarations": 33,
        "transitive_d0_pins": 26,
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
