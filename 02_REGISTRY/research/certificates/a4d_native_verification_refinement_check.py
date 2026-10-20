#!/usr/bin/env python3
"""Exact controls for verified processes and the literal one-dimensional phase tower.

All-size classifications are proved in the companion memo and Lean capsule.
Finite enumerations are independent controls, never the infinite-tower proof.
Default replay is immutable. No native action or admissibility law is added.
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction
from itertools import permutations, product
from math import factorial, prod
from pathlib import Path
import hashlib
import json
import sympy as sp

INPUT_HEAD = "606d8774bcaf4684d8caac60cb73912a8827091a"
INPUTS = [
    "03_FORMALIZATION/D0/Foundation/VerifiabilityNecessity.lean",
    "03_FORMALIZATION/D0/Foundation/EmpiricalTheoryFactorization.lean",
    "03_FORMALIZATION/D0/Foundation/M1ClassAdmissibility.lean",
    "03_FORMALIZATION/D0/Foundation/PhysicalComparisonRepresentation.lean",
    "03_FORMALIZATION/D0/Synthesis/ConcretePhysicalDetectorRepresentation.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveLaplacianRG.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveCanonicalDirichlet.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveRefinementTower.lean",
]


def truncation(L, K, i):
    assert 2 <= L < K and 0 <= i < K
    return i if i < L else 0


def composed_projection(L, K, i):
    for m in range(K-1, L-1, -1):
        i %= m
    return i


def compatible(L, K, sigma, tau):
    return all(truncation(L, K, tau[i]) == sigma[truncation(L, K, i)] for i in range(K))


def coherent_prefixes(lengths):
    families = [(s,) for s in permutations(range(lengths[0]))]
    for L, K in zip(lengths, lengths[1:]):
        families = [ss+(tau,) for tau in permutations(range(K)) for ss in families
                    if compatible(L, K, ss[-1], tau)]
    return families


def reverse_birth_blocks(lengths):
    initial = list(range(lengths[0]))
    initial[1:] = reversed(initial[1:])
    family = [tuple(initial)]
    for L, K in zip(lengths, lengths[1:]):
        family.append(family[-1]+tuple(reversed(range(L, K))))
    return family


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[3])
    ap.add_argument("--output", type=Path)
    ap.add_argument("--expect", type=Path)
    args = ap.parse_args(); repo = args.repo.resolve(); checks = []
    sha = lambda p: hashlib.sha256((repo/p).read_bytes()).hexdigest()
    def check(name, condition):
        assert bool(condition), name
        checks.append(name); print("PASS_"+name, flush=True)

    receipt_path = "02_REGISTRY/research/certificates/a4d_native_verification_refinement_results.json"
    receipt = json.loads((repo/receipt_path).read_text())
    assert receipt["status"] == "PASS" and receipt["compiler_exit_code"] == 0 and not receipt["sorryAx"]
    output = (repo/receipt["output"]).read_text()
    assert output.count("depends on axioms:") == 13
    assert output.count("does not depend on any axioms") == 3
    assert "sorryAx" not in output and "error:" not in output
    for path, digest in {**receipt["transitive_d0_source_sha256"], **receipt["toolchain_input_sha256"],
                         receipt["capsule"]: receipt["capsule_sha256"], receipt["output"]: receipt["output_sha256"]}.items():
        assert sha(path) == digest, "LEAN_INPUT_CHANGED: "+path
    check("COMPILED_INTERFACE_CLASSIFICATION_AND_ACTUAL_PHASE_BINDINGS", True)

    process_counts = {}
    for n in [2, 3, 4]:
        maps = list(product(range(n), repeat=n))
        lifts = [f for f in maps if all(sum(f[x] == y for x in range(n)) == 1 for y in range(n))]
        check("ALL_POINT_TEST_RUNS_ARE_EXACTLY_PERMUTATIONS_"+str(n),
              set(lifts) == set(permutations(range(n))) and len(lifts) == factorial(n))
        check("ACTUAL_INVERSE_PULL_TEST_LAW_"+str(n), all(
              (f[x] != y) == (x != f.index(y)) for f in lifts for x in range(n) for y in range(n)))
        # The empty point preimage of a constant map cannot be one reference test.
        f = (0,)*n
        check("CONSTANT_RUN_HAS_NO_POINT_TEST_LIFT_"+str(n),
              not any(all((f[x] != 1) == (x != ref) for x in range(n)) for ref in range(n)))
        tests = list(product([False, True], repeat=n))
        check("ALL_MAPS_HAVE_FULL_PREDICATE_PULL_TEST_LIFT_"+str(n), all(
              tuple(e[f[x]] for x in range(n))[s] == e[f[s]] for f in maps for e in tests for s in range(n)))
        # Exhaust every binary-valued observable: all-permutation invariance
        # permits precisely the two constant observables on the nonempty set.
        invariant = [a for a in tests if all(a[f[x]] == a[x] for f in lifts for x in range(n))]
        check("ALL_PROCESS_INVARIANT_OBSERVABLES_ARE_CONSTANT_"+str(n),
              invariant == [(False,)*n, (True,)*n])
        process_counts[str(n)] = {"all_runs": n**n, "point_test_lifts": len(lifts), "predicate_lifts": len(maps)}

    # The class-level concrete representation is already owned. Its primitive
    # result concerns profiles, not a two-element set of all comparison functions.
    observations = list(product([0, 1], repeat=3))
    def history_invariant(cmp):
        return all(cmp(x, y) == cmp((x[0], x[1], hx), (y[0], y[1], hy))
                   for x in observations for y in observations for hx in [0, 1] for hy in [0, 1])
    check("OWNED_CONCRETE_MEMBERSHIP_VALUE_CONTROLS", all(history_invariant(
          lambda x,y,k=k: x[k] != y[k]) for k in [0, 1]))
    check("HISTORY_COMPARISON_REJECTED", not history_invariant(lambda x,y: x[2] != y[2]))
    check("FULL_CURRENT_COMPARISONS_EXCEED_TWO_PRIMITIVE_PROFILES",
          history_invariant(lambda x,y: (x[0],x[1]) == (y[0],y[1])) and 2**(4*4) == 65536)

    def energy(f):
        L = len(f)
        return sum((f[i]-f[j])**2 for i in range(L) for j in range(L)
                   if min((i-j)%L, (j-i)%L) == 1)
    t, eps = sp.symbols("t eps", real=True)
    check("LITERAL_NATIVE_THREE_PHASE_DIRICHLET_ZERO_AND_PULSE", energy([0,0,0]) == 0 and energy([1,0,0]) == 4)
    check("LITERAL_NATIVE_RADIAL_ENERGY", sp.expand(energy([1+t,0,0])-4*(1+t)**2) == 0)
    check("NATIVE_CENTERED_CONTRAST_SIGN_AND_FACTOR", sp.expand(energy([1+eps,0,0])-energy([1-eps,0,0])-16*eps) == 0)
    check("VERIFIED_FLIP_DOES_NOT_ENFORCE_NATIVE_STATIONARITY", sp.diff(energy([1+t,0,0]),t).subs(t,0) == 8)

    for L, K in [(2,3),(3,4),(3,7),(4,8),(5,13),(8,16),(12,24)]:
        check("ACTUAL_COMPOSED_PHASE_PROJECTION_"+str(L)+"_"+str(K),
              all(composed_projection(L,K,i) == truncation(L,K,i) for i in range(K)))
    check("LONG_COMPOSITE_IS_NOT_ONE_MODULO", composed_projection(4,8,5) == 0 and 5%4 == 1)
    prefix_counts = {}
    for lengths in [[2,3], [2,3,4], [2,3,4,5], [2,3,4,5,6], [3,5], [2,4,6], [3,5,7]]:
        families = coherent_prefixes(lengths); H = len(lengths)-1
        increments = [b-a for a,b in zip(lengths,lengths[1:])]
        expected = factorial(lengths[0]-1)*prod(factorial(d) for d in increments[:-1])*factorial(increments[-1]+1)
        extendable = [ss for ss in families if ss[-1][0] == 0]
        expected_extendable = factorial(lengths[0]-1)*prod(factorial(d) for d in increments)
        key = "_".join(map(str,lengths))
        check("COMPLETE_FINITE_HORIZON_FIBER_CLASSIFICATION_"+key,
              len(families) == expected and len(extendable) == expected_extendable)
        check("ALL_LOWER_STAGES_FIX_ZERO_"+key, all(all(s[0] == 0 for s in ss[:-1]) for ss in families))
        if lengths[0] == 2 and set(increments) == {1}:
            check("ONLY_IDENTITY_PREFIX_CAN_EXTEND_"+key,
                  extendable == [tuple(tuple(range(L)) for L in lengths)] and len(families) == 2)
        prefix_counts[key] = {"finite_families": len(families), "extendable_families": len(extendable)}

    # The stated L in 4N can mean different subsequences. Keep that exception.
    dense = list(range(4, 132, 4)); sd = reverse_birth_blocks(dense)
    check("DENSE_FOUR_MULTIPLE_SUBSEQUENCE_HAS_NONTRIVIAL_EXACT_PROCESSES",
          all(compatible(L,K,s,u) for L,K,s,u in zip(dense,dense[1:],sd,sd[1:])) and sd[0] != tuple(range(4)))
    check("DENSE_BIRTH_BLOCK_DISPLACEMENT_IS_AT_MOST_THREE",
          all(max(abs(i-s[i]) for i in range(L)) <= 3 for L,s in zip(dense,sd)))
    sparse = [4*2**j for j in range(7)]; ss = reverse_birth_blocks(sparse)
    check("SPARSE_FOUR_MULTIPLE_SUBSEQUENCE_ALSO_COMMUTES_EXACTLY",
          all(compatible(L,K,s,u) for L,K,s,u in zip(sparse,sparse[1:],ss,ss[1:])))
    check("SPARSE_MACROSCOPIC_MOTION_IS_NOT_EXCLUDED",
          all(Fraction(abs(s[L//2]-L//2),L) == Fraction(1,2)-Fraction(1,L) for L,s in zip(sparse[1:],ss[1:])))
    for L in [2,3,4,5,8,9,12,16,32,64,128]:
        shift = lambda N,i: (i+N//2)%N
        distance = lambda x,y: Fraction(min((x-y)%L,(y-x)%L),L)
        defects = [distance(shift(L+1,i)%L,shift(L,i%L)) for i in range(L+1)]
        check("HALF_TURN_ADJACENT_ERROR_EXACTLY_INVERSE_SIZE_"+str(L), max(defects) == Fraction(1,L))
        if L%2 == 0:
            check("HALF_TURN_COMPOSED_ERROR_ONE_HALF_"+str(L),
                  distance(composed_projection(L,2*L,shift(2*L,0)),shift(L,composed_projection(L,2*L,0))) == Fraction(1,2))

    # Four roles and flattened ArchivePoints have different point-map fibers.
    for L in [2,3,4]:
        K = L+1; swap_roles = lambda x: (x[1],x[0],x[2],x[3])
        project = lambda x: tuple(i%L for i in x)
        check("FOUR_ROLE_PERMUTATION_IS_NONTRIVIAL_AND_COHERENT_"+str(L),
              all(project(swap_roles(x)) == swap_roles(project(x)) for x in product(range(K),repeat=4))
              and swap_roles((0,1,0,0)) != (0,1,0,0))
    flat = Counter(Counter(i%16 for i in range(81)).values())
    roles = Counter(Counter(tuple(i%2 for i in x) for x in product(range(3),repeat=4)).values())
    check("FLATTENED_AND_ROLE_PRODUCT_FIBER_TYPES_DIFFER", flat == {5:15,6:1} and roles == {1:1,2:4,4:6,8:4,16:1})

    payload = {"status":"PASS", "input_head":INPUT_HEAD,
        "scope":"Actual formal verification contract and point-test processes; exact one-dimensional phase permutations. No selection of physical dynamics and no whole-core no-go.",
        "inputs_sha256":{p:sha(p) for p in INPUTS}, "lean_receipt_sha256":sha(receipt_path),
        "checks":checks, "process_counts":process_counts, "finite_prefix_counts":prefix_counts,
        "verifiable_iff":"Nontrivial empirical quotient (classical formal representation only)",
        "point_test_runs":"all and only bijections", "full_phase_coherent_permutations":"identity only",
        "subsequence_group":"Sym({1,...,L0-1}) times product_j>=1 Sym({L_(j-1),...,L_j-1})",
        "finite_horizon_count":"(L0-1)! product_(1<=j<H) (Delta L_j)! (Delta L_H+1)!",
        "half_turn_adjacent_error":"1/L", "half_turn_composed_error":"1/2",
        "native_pulse_energy":"4", "native_radial_raw_contrast":"16 epsilon",
        "flat_fibers_2_to_3":dict(sorted(flat.items())), "role_product_fibers_2_to_3":dict(sorted(roles.items())),
        "protected_exceptions":["Physical realization/effective comparison of a classical equality oracle",
            "Different empirical test spaces and quotient processes", "Approximate refinement or different metrics",
            "Subsequences including sparse L in 4N", "Four-Role or flattened archive carriers",
            "Independently owned native variation constraints and physical readouts"]}
    out = json.dumps(payload, sort_keys=True, indent=2)+"\n"
    if args.output: args.output.write_text(out)
    else:
        ledger = args.expect or Path(__file__).with_name("a4d_native_verification_refinement_certificate.json")
        assert ledger.read_text() == out, "PINNED_LEDGER_MISMATCH"
        print("PASS_IMMUTABLE_PINNED_LEDGER")
    print("PASS_NATIVE_VERIFICATION_REFINEMENT",len(checks))


if __name__ == "__main__": main()
