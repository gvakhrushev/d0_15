#!/usr/bin/env python3
"""Narrow exact retained-code and actual-ledger gap controls.

Loads only named primitive/entropy definitions and one literal tape
expression from the pinned earlier writer checker. It never runs that
checker or any old geometry, root, rank or compiler suite.
"""

import argparse
import ast
from collections import defaultdict
from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path
import subprocess


SOURCE_REF = "f64d4c3389b507c7e7fb66ace9480ed6191c463d"
OLD_CHECKER = ("02_REGISTRY/research/sources/"
               "d0_paid_moment_field_writer_2026-10-21/code/"
               "check_paid_code_and_moment_writer.py")
CHECKS = []


def require(name, condition):
    if not condition:
        raise RuntimeError("FAILED: " + name)
    CHECKS.append(name)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def owned_definitions(data):
    tree = ast.parse(data.decode())
    wanted = {"cx", "ccx", "code_cell", "fredkin",
              "prime_logs_integer", "log_form", "entropy", "lincomb"}
    selected = [node for node in tree.body
                if isinstance(node, ast.FunctionDef) and node.name in wanted]
    require("all_requested_owned_definitions_present",
            {node.name for node in selected} == wanted)
    env = {"F": Q, "defaultdict": defaultdict}
    exec(compile(ast.Module(body=selected, type_ignores=[]),
                 "<pinned writer definitions only>", "exec"), env)
    ledger = next(node for node in tree.body
                  if isinstance(node, ast.FunctionDef)
                  and node.name == "ledger_controls")
    tape_node = next(node.value for node in ledger.body
                     if isinstance(node, ast.Assign)
                     and any(isinstance(t, ast.Name) and t.id == "tape"
                             for t in node.targets))
    tape = eval(compile(ast.Expression(body=tape_node),
                        "<pinned literal structural tape>", "eval"),
                {"F": Q})
    return env, tape


def complete_selected_state(code, n, plus_counts, env):
    c, u, b = env["code_cell"]((1, 0, 0), code)
    require("actual_blank_cell_" + str(code), (c, u, b) == (1, 1, code))
    state = {}
    for l0, l1, x0, x1 in itertools.product(range(n), range(n), (0, 1), (0, 1)):
        signs = (1 if l0 < plus_counts[0] else -1,
                 1 if l1 < plus_counts[1] else -1)
        rows, output = [x0, x1], 0
        for j in range(2):
            _, rows[j], output = env["fredkin"](
                (int(b == j), rows[j], output))
        key = (c, u, b, l0, l1, rows[0], rows[1], output)
        state[key] = signs[0]**x0 * signs[1]**x1
    norm = sum(a*a for a in state.values())
    require("complete_selector_injective_" + str((code, n)),
            len(state) == 4*n*n)
    require("complete_pure_norm_" + str((code, n)), norm == 4*n*n)
    require("retained_actual_code_and_u_" + str((code, n)),
            all(key[:3] == (1, 1, code) for key in state))
    require("old_output_blank_retained_" + str((code, n)),
            all(key[5+code] == 0 for key in state))
    # Partial trace is used only to display the actual selected moment.
    # Every key, including both raw labels and the unselected row, remains
    # in the complete state used for the trace-distance argument.
    rho = [[Q(0), Q(0)], [Q(0), Q(0)]]
    for key, a in state.items():
        for target in (0, 1):
            other = key[:-1] + (target,)
            rho[key[-1]][target] += Q(a*state.get(other, 0), norm)
    mean = Q(2*plus_counts[code], n)-1
    require("actual_selected_pair_density_" + str((code, n)),
            rho == [[Q(1, 2), mean/2], [mean/2, Q(1, 2)]])
    return state, rho, mean


def retained_code_controls(env, tape):
    require("literal_owned_structural_tape",
            tape == (Q(1, 2), Q(1, 4), Q(1, 16), Q(3, 16)))
    a_pre, gamma = sum(tape[2:]), tape[-1]
    require("all_probability_retained", sum(tape) == 1)
    require("late_abort_contributes_to_code_distance", a_pre > gamma)
    rows = []
    for n, plus_counts in ((4, (1, 2)), (8, (4, 5)), (32, (16, 17))):
        s0, rho0, t0 = complete_selected_state(0, n, plus_counts, env)
        s1, rho1, t1 = complete_selected_state(1, n, plus_counts, env)
        inner_numerator = sum(a*s1.get(key, 0) for key, a in s0.items())
        require("full_postcode_states_orthogonal_" + str(n), inner_numerator == 0)
        require("retained_code_supports_disjoint_" + str(n),
                set(s0).isdisjoint(s1))
        # Every late block is a difference of normalized positive
        # rank-one operators with orthogonal supports. Thus |A-B|=A+B.
        trace_norm = sum(2*p for p in tape[2:])
        trace_distance = trace_norm/2
        require("complete_trace_distance_including_late_abort_" + str(n),
                trace_distance == a_pre)
        # The actual u/b test gives the same lower bound without any
        # assumptions about an extra retained initial instruction tape.
        code_law0 = (*tape[:2], a_pre, Q(0))
        code_law1 = (*tape[:2], Q(0), a_pre)
        tv = sum(abs(x-y) for x, y in zip(code_law0, code_law1))/2
        require("actual_register_test_saturates_bound_" + str(n), tv == a_pre)
        pair_distance = abs(t1-t0)/2
        rows.append({"labels_per_row": n,
                     "moments": [str(t0), str(t1)],
                     "conditional_active_pair_trace_distance": str(pair_distance),
                     "complete_CQ_trace_distance": str(trace_distance),
                     "complete_vector_terms_each": len(s0)})
    require("arbitrarily_close_moment_pattern",
            rows[-1]["conditional_active_pair_trace_distance"] == "1/32"
            and rows[-1]["complete_CQ_trace_distance"] == "1/4")
    # If an extra initial controller already stores orthogonal intended
    # words, even the early sectors differ. Equality a_pre is no longer
    # claimed for that larger state, whereas its lower bound survives.
    enlarged_distance = sum(tape)
    require("extra_instruction_tape_needs_lower_bound_not_equality",
            enlarged_distance == 1 and enlarged_distance > a_pre)
    return {"a_pre": str(a_pre), "gamma": str(gamma),
            "retained_late_abort": str(tape[2]), "fixtures": rows,
            "scope": "owned rational structural tape; actual-law statement is analytic",
            "full_controller_bound": "D_trace >= a_pre; equality needs common early sector"}


def gap_controls(env, tape):
    gamma = tape[-1]
    # These are the original two-row fixture's actual post-H reports.
    r0, r1 = Q(3, 4), Q(1, 2)
    ent0 = env["entropy"]((1-r0, r0))
    ent1 = env["entropy"]((1-r1, r1))
    gap_form = env["lincomb"]((gamma, ent1), (-gamma, ent0))
    expected = {2: -Q(3, 16), 3: Q(9, 64)}
    require("actual_complete_CQ_price_gap", gap_form == expected)
    # D=(3/64)*log_phi(27/16)>0, with exact integer sign control.
    require("strict_gap_sign_without_floating_logs", 3**3 > 2**4)
    cases = []
    for slack, correction, expected_margin in (
            (Q(0), Q(0), Q(-1)),
            (Q(1, 2), Q(1, 4), Q(-1, 4)),
            (Q(1, 2), Q(1, 2), Q(0)),
            (Q(3, 2), Q(0), Q(1, 2))):
        margin = slack-1+correction
        require("finite_envelope_identity_" + str((slack, correction)),
                margin == expected_margin)
        require("exact_correction_threshold_" + str((slack, correction)),
                (margin >= 0) == (correction >= 1-slack))
        cases.append({"implementation_slack_over_D": str(slack),
                      "full_price_correction_over_D": str(correction),
                      "candidate_minus_root_infimum_over_D": str(margin)})
    require("hostile_omitted_slack_changes_conclusion",
            cases[-1]["candidate_minus_root_infimum_over_D"] == "1/2")
    return {"reports": [str(r0), str(r1)],
            "D_exact": "(3/64)*log_phi(27/16)",
            "finite_comparison": "U(w1)-U(w0) >= D-Delta0 is necessary",
            "controls": cases,
            "physical_geometry_claim_from_fixture": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    packet = Path(__file__).resolve().parent
    pin_bytes = (packet/"STATIONARITY_SOURCE_PINS.json").read_bytes()
    pins = json.loads(pin_bytes)
    require("historical_source_ref", pins["source_ref"] == SOURCE_REF)
    historical = {}
    for entry in pins["sources"]:
        data = subprocess.check_output(
            ["git", "show", SOURCE_REF+":"+entry["path"]], cwd=args.repo)
        require("historical_pin_"+entry["path"],
                sha(data) == entry["sha256"] and len(data) == entry["bytes"])
        historical[entry["path"]] = data
    env, tape = owned_definitions(historical[OLD_CHECKER])
    trace_result = retained_code_controls(env, tape)
    gap_result = gap_controls(env, tape)
    proof = packet/"RETAINED_CODE_LIFT_AND_APPARATUS_ELIMINATION.md"
    result = {"status": "PASS", "scientific_input": SOURCE_REF,
              "historical_sources_verified": len(historical),
              "retained_code": trace_result, "finite_price_gap": gap_result,
              "proof_sha256": sha(proof.read_bytes()),
              "checker_sha256": sha(Path(__file__).read_bytes()),
              "source_pins_sha256": sha(pin_bytes),
              "checks_count": len(CHECKS),
              "actual_factory_law_recomputed": False,
              "smooth_complete_state_writer_proved": False,
              "original_physical_price_identified": False,
              "GR_closed": False}
    output = json.dumps(result, indent=2, sort_keys=True)+"\n"
    if args.output:
        args.output.write_text(output)
    print(output, end="")


if __name__ == "__main__":
    main()
