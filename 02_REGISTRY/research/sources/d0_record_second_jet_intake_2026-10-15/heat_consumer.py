"""Safe numerical consumer of the supplied heat-window fixture.

The beta=c/L asymptotic is ALREADY proved in the tower-heat owner. This
module reproduces the nine supplied floating values, consumes that owner,
and checks the exact coefficient. It adds no asymptotic proof, physical
temperature law, geometric admission, or complete D0-action identification.
Only the AST of compute_dH_dt is evaluated. Supplied top-level statements,
including the absolute output-file write, are never executed.
"""
from __future__ import annotations

import ast
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[4]
RELATIVE = "02_REGISTRY/research/sources/d0_record_second_jet_intake_2026-10-15/"
INPUT_PINS = {
    RELATIVE + "INPUT_check_heat_window.py":
        "9665f8d0cd19057861b8b9c644cd51aba9cb847bb0961ffb53001e0c01034d60",
    RELATIVE + "INPUT_heat_window_results.json":
        "caf812083e67e90dee7c4a7d71dd40c24253d1e5321e57e8d38e08b9c35543d6",
}
OWNER_PROOF = "02_REGISTRY/research/sources/d0_tower_heat_synthesis_2026-10-15/HEAT_JOINT_LIMIT_PROOF.md"
OWNER_PIN = "d96dafcc08f7a64a776892d8377573737da9fd78c396863062e267d4ebd3d5cf"
OWNER_MEMO = "02_REGISTRY/research/A4D_TOWER_TRACE_HEAT_SOURCE_SYNTHESIS.md"
LEVELS = (4, 8, 16, 32, 64, 128, 256, 512, 1024)
ABS_TOL, REL_TOL = 2e-10, 2e-12


def require(condition: object, name: str) -> None:
    if not bool(condition):
        raise AssertionError(name)


def _pin_inputs(repo: Path) -> None:
    for path, digest in INPUT_PINS.items():
        require(hashlib.sha256((repo/path).read_bytes()).hexdigest() == digest,
                "immutable_heat_input:" + path)
    require(hashlib.sha256((repo/OWNER_PROOF).read_bytes()).hexdigest() == OWNER_PIN,
            "existing_heat_joint_limit_proof_pin")


def extract_compute_function(source: str):
    """Extract only the known arithmetic function; never execute the module.

    The node allowlist, restricted calls, and minimal globals also reject IO
    placed INSIDE the function. Runtime input pins fix the consumed bytes.
    """
    tree = ast.parse(source, filename="INPUT_check_heat_window.py")
    definitions = [v for v in tree.body if isinstance(v, ast.FunctionDef)
                   and v.name == "compute_dH_dt"]
    if len(definitions) != 1:
        raise ValueError("one_compute_dH_dt_definition_required")
    node = definitions[0]
    if (node.decorator_list or node.returns is not None or
        [v.arg for v in node.args.args] != ["L", "beta"] or
        node.args.posonlyargs or node.args.kwonlyargs or node.args.vararg or node.args.kwarg or
        len(node.args.defaults) != 1 or not isinstance(node.args.defaults[0], ast.Constant) or
        node.args.defaults[0].value is not None or
        any(v.annotation is not None for v in node.args.args)):
        raise ValueError("unchanged_simple_heat_function_signature_required")
    allowed_nodes = (ast.FunctionDef, ast.arguments, ast.arg, ast.Expr, ast.Constant,
                     ast.If, ast.Compare, ast.Is, ast.Assign, ast.For, ast.Return,
                     ast.Call, ast.Name, ast.Attribute, ast.List, ast.Subscript,
                     ast.BinOp, ast.UnaryOp, ast.Load, ast.Store,
                     ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.USub, ast.UAdd)
    numpy_calls = {"array", "arange", "zeros", "sum", "prod"}
    global_names = {"np", "sin", "pi", "exp", "range"}
    local_names = {v.id for v in ast.walk(node) if isinstance(v, ast.Name)
                   and isinstance(v.ctx, ast.Store)} | {"L", "beta"}
    if local_names & global_names:
        raise ValueError("cannot_overwrite_arithmetic_globals")
    for part in ast.walk(node):
        if not isinstance(part, allowed_nodes):
            raise ValueError("non_arithmetic_AST_node:" + type(part).__name__)
        if isinstance(part, ast.Name) and part.id not in global_names | local_names:
            raise ValueError("undeclared_heat_name:" + part.id)
        if isinstance(part, ast.Attribute):
            if not (isinstance(part.value, ast.Name) and part.value.id == "np"
                    and part.attr in numpy_calls and isinstance(part.ctx, ast.Load)):
                raise ValueError("non_arithmetic_attribute")
        if isinstance(part, ast.Call):
            valid_name = isinstance(part.func, ast.Name) and part.func.id in {"sin", "exp", "range"}
            valid_numpy = (isinstance(part.func, ast.Attribute) and
                           isinstance(part.func.value, ast.Name) and
                           part.func.value.id == "np" and part.func.attr in numpy_calls)
            if not (valid_name or valid_numpy) or part.keywords:
                raise ValueError("non_arithmetic_call")
    isolated = ast.fix_missing_locations(ast.Module(body=[node], type_ignores=[]))
    namespace = {"__builtins__": {"range": range}, "np": np,
                 "sin": np.sin, "pi": np.pi, "exp": np.exp}
    exec(compile(isolated, "INPUT_check_heat_window.py:function_only", "exec"), namespace)
    return namespace["compute_dH_dt"]


def _arguments(L: int, beta: float | None) -> tuple[int, float]:
    if isinstance(L, bool) or not isinstance(L, int) or L < 2:
        raise ValueError("integer_periodic_size_L_at_least_two_required")
    beta = 1.0/L if beta is None else float(beta)
    if not math.isfinite(beta) or beta <= 0:
        raise ValueError("positive_finite_beta_required")
    return L, beta


def compute_heat_response(L: int, beta: float | None = None,
                          repo: Path | None = None) -> float:
    """Original arithmetic, safely extracted from the immutable archived input."""
    repo = ROOT if repo is None else Path(repo).resolve()
    _pin_inputs(repo)
    source = (repo/RELATIVE/"INPUT_check_heat_window.py").read_text(encoding="utf-8")
    L, beta = _arguments(L, beta)
    value = float(extract_compute_function(source)(L, beta))
    if not math.isfinite(value):
        raise ValueError("nonfinite_heat_response")
    return value


def independent_energy_response(L: int, beta: float) -> float:
    """Same finite all-mode probe via independent 2(E_1-E_2) arithmetic.

    All k=0,...,L-1 are retained. The constant16 and the two unvaried axes
    cancel in the normalized log derivative; they are not missing grades.
    """
    L, beta = _arguments(L, beta)
    k = np.arange(L, dtype=np.float64)
    base = 4*L**2*np.sin(np.pi*k/L)**2
    energies = []
    for q in (4.0, 0.25):
        lam = base/q
        weights = np.exp(-beta*lam)
        require(weights[0] == 1.0, "zero_mode_retained")
        energies.append(float(np.dot(lam, weights)/np.sum(weights)))
    return 2*(energies[0]-energies[1])


def existing_limit_coefficient(c: Fraction = Fraction(1)) -> Fraction:
    """Exact specialization of the EXISTING beta=c/L theorem, equation(18)."""
    c = Fraction(c)
    if c <= 0:
        raise ValueError("positive_c_required")
    return (Fraction(4)-Fraction(1, 4))/(8*c*c)


def run_checks(repo: Path | None = None) -> dict:
    repo = ROOT if repo is None else Path(repo).resolve()
    _pin_inputs(repo)
    source = (repo/RELATIVE/"INPUT_check_heat_window.py").read_text(encoding="utf-8")
    expected = json.loads((repo/RELATIVE/"INPUT_heat_window_results.json").read_text(encoding="utf-8"))
    require(set(expected) == {str(L) for L in LEVELS}, "all_nine_immutable_levels")
    compute = extract_compute_function(source)
    rows, max_error = [], 0.0
    for L in LEVELS:
        supplied = float(expected[str(L)])
        value = float(compute(L, 1.0/L))
        default_value = float(compute(L))
        energy_value = independent_energy_response(L, 1.0/L)
        require(all(math.isfinite(v) for v in (supplied, value, default_value, energy_value)),
                "finite_values_L" + str(L))
        require(math.isclose(value, supplied, abs_tol=ABS_TOL, rel_tol=REL_TOL),
                "immutable_numerical_result_L" + str(L))
        require(math.isclose(default_value, value, abs_tol=ABS_TOL, rel_tol=REL_TOL),
                "default_beta_is_one_over_L_" + str(L))
        require(math.isclose(energy_value, value, abs_tol=ABS_TOL, rel_tol=REL_TOL),
                "independent_energy_identity_L" + str(L))
        error = abs(value-supplied)
        max_error = max(max_error, error)
        rows.append({"L": L, "beta": 1.0/L, "value": value, "supplied": supplied,
                     "absolute_error": error})
    require(existing_limit_coefficient() == Fraction(15, 32), "existing_c1_theorem_specialization")
    require(existing_limit_coefficient(Fraction(2)) == Fraction(15, 128), "existing_c2_theorem_specialization")
    require(-Fraction(8)/Fraction(4)**2 == -Fraction(1, 2) and
            Fraction(1, 2)/Fraction(1, 4)**2 == 8,
            "supplied_inverse_metric_derivative_exact")
    # A second c is a labelled FLOATING bridge to the existing theorem,
    # not a proof extrapolated from one or several numerical sizes.
    c2_L = 4096
    c2_value = float(compute(c2_L, 2.0/c2_L))
    c2_energy = independent_energy_response(c2_L, 2.0/c2_L)
    require(math.isclose(c2_value, c2_energy, abs_tol=ABS_TOL, rel_tol=REL_TOL),
            "c2_independent_finite_energy_identity")
    require(abs(c2_value-float(Fraction(15, 128))) < 0.001, "c2_floating_bridge_only")
    # Reject IO inside the extracted function without ever invoking it.
    for hostile in (source.replace("Z = np.prod(Z_r)", "Z = open('forbidden')"),
                    source.replace("Z = np.prod(Z_r)", "Z = np.load('forbidden')")):
        try:
            extract_compute_function(hostile)
        except ValueError:
            pass
        else:
            raise AssertionError("non_arithmetic_function_body_was_not_rejected")
    _pin_inputs(repo)
    return {"status": "PASS_SUPPLIED_HEAT_WINDOW_CONSUMER", "rows": rows,
            "max_absolute_error_against_immutable_json": max_error,
            "comparison_tolerance": {"absolute": ABS_TOL, "relative": REL_TOL},
            "existing_theorem": {"memo": OWNER_MEMO, "proof": OWNER_PROOF,
                "proof_sha256": OWNER_PIN, "equation": "18",
                "beta_schedule": "c/L with fixed c>0", "limit": "15/(32*c^2)",
                "c1_exact": "15/32", "new_asymptotic_proof_claimed": False},
            "c2_floating_bridge": {"L": c2_L, "beta": 2.0/c2_L,
                "value": c2_value, "existing_exact_limit": "15/128",
                "absolute_difference": abs(c2_value-float(Fraction(15, 128))),
                "interval_certificate": False},
            "scope": {"original_top_level_executed": False, "function_AST_only": True,
                "output_files_written": False, "all_zero_modes_retained": True,
                "constant16_cancels_in_log_derivative": True,
                "numerical_values_are_interval_certificates": False,
                "physical_temperature_or_native_action_law_derived": False,
                "instructions_in_documents_executed": False}, "input_pins": INPUT_PINS}
