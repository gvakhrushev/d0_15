#!/usr/bin/env python3
"""Independent high-precision price-gradient and Jacobian controls for the
full 4D native-Golden N1 two-scalar numerical root.

The solver's assembled Euler vector is checked against direct differentiation
of its Bernoulli-entropy price using mpmath and the original nodal field
values. Representative coordinates also use centered secants of that price.
This remains a finite fixed-geometry matter-subsystem check.
"""
from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path
import runpy

import mpmath as mp
import numpy as np

mp.mp.dps = 80
HERE = Path(__file__).resolve().parent
SOLVER = HERE / "check_native_n1_two_scalar_full4d.py"
with redirect_stdout(StringIO()):
    D = runpy.run_path(str(SOLVER))

M = D["M"]
L = D["L"]
h = mp.mpf(str(D["h"]))
h4 = h**4
Nin = D["Nin"]
cells = D["cells"]
unknown_sites = D["unknown_sites"]
idxmap = D["idxmap"]


def high_precision_price_gradient(x):
    """Differentiate the written entropy price from nodal differences."""
    fields = D["state"](x)
    gradient = [mp.mpf("0") for _ in range(2 * Nin)]
    for ci, cell in enumerate(cells):
        rho = mp.mpf(str(D["RHO"][ci]))
        y_multiplier = mp.mpf(str(D["Ymul"][ci]))
        probability_x = mp.mpf(str(D["X"][ci]))
        q = mp.mpf("0")
        cell_gradients = []
        for species in range(2):
            for direction in range(4):
                neighbor = list(cell)
                neighbor[direction] += 1
                neighbor = tuple(neighbor)
                low = mp.mpf(str(fields[(species,) + cell]))
                high = mp.mpf(str(fields[(species,) + neighbor]))
                derivative = (high - low) / h
                metric = mp.mpf(str(D["Gcoeff"][ci, species * 4 + direction]))
                cell_gradients.append((species, direction, neighbor, derivative, metric))
                q += metric * derivative**2
        # M.native_y is the exact derivative of the same -binary-entropy
        # price used by M.raw, evaluated at 80 decimal digits.
        price_y = M.native_y(probability_x, y_multiplier * q)
        common = h4 * rho * y_multiplier * price_y
        for species, direction, neighbor, derivative, metric in cell_gradients:
            contribution = 2 * common * metric * derivative / h
            if cell in idxmap:
                gradient[species * Nin + idxmap[cell]] -= contribution
            if neighbor in idxmap:
                gradient[species * Nin + idxmap[neighbor]] += contribution
    return gradient


def local_price(x, flat_index, perturbation):
    """Re-evaluate only price cells incident to one perturbed nodal value."""
    species = flat_index // Nin
    site = unknown_sites[flat_index % Nin]
    fields = D["state"](x)
    affected = []
    for ci, cell in enumerate(cells):
        if cell == site:
            affected.append(ci)
            continue
        if any(tuple(cell[d] + (1 if d == direction else 0) for d in range(4)) == site
               for direction in range(4)):
            affected.append(ci)
    total = mp.mpf("0")
    for ci in affected:
        cell = cells[ci]
        rho = mp.mpf(str(D["RHO"][ci]))
        q = mp.mpf("0")
        for field_species in range(2):
            for direction in range(4):
                neighbor = list(cell)
                neighbor[direction] += 1
                neighbor = tuple(neighbor)
                low = mp.mpf(str(fields[(field_species,) + cell]))
                high = mp.mpf(str(fields[(field_species,) + neighbor]))
                if field_species == species and cell == site:
                    low += perturbation
                if field_species == species and neighbor == site:
                    high += perturbation
                derivative = (high - low) / h
                metric = mp.mpf(str(D["Gcoeff"][ci, field_species * 4 + direction]))
                q += metric * derivative**2
        probability = M.raw(
            mp.mpf(str(D["X"][ci])),
            mp.mpf(str(D["Ymul"][ci])) * q,
        )
        # -H_phi = [p log p + (1-p) log(1-p)] / log(1/phi).
        minus_entropy = (
            probability * mp.log(probability)
            + (1 - probability) * mp.log(1 - probability)
        ) / M.lnphi
        total += h4 * rho * minus_entropy
    return total


def price_secant(x, flat_index, step):
    delta = mp.mpf(step)
    return (
        local_price(x, flat_index, delta)
        - local_price(x, flat_index, -delta)
    ) / (2 * delta)


checks = {}
price_gradients = {}
for label, x in (("initial", D["x0"]), ("root", D["x"])):
    exact_gradient = high_precision_price_gradient(x)
    source, _ = D["source"](x)
    scale = 2 * h4 * mp.mpf("0.05") * M.norm
    normalized = np.array([float(v / scale) for v in exact_gradient])
    price_gradients[label] = {
        "max_abs_price_derivative": float(max(abs(v) for v in exact_gradient)),
        "max_normalized_euler": float(np.max(np.abs(normalized))),
        "max_delta_vs_solver_source": float(np.max(np.abs(normalized - source))),
        "solver_source_inf": float(np.max(np.abs(source))),
    }

# Validate the normalized source on the initial and solved configurations.
assert price_gradients["initial"]["max_delta_vs_solver_source"] < 2e-11
assert price_gradients["root"]["max_delta_vs_solver_source"] < 2e-11
assert price_gradients["root"]["max_abs_price_derivative"] < 1e-20
assert price_gradients["root"]["max_normalized_euler"] < 2e-11

# Direct Bernoulli-entropy secants on representative variables from both fields.
selected = (0, 648, 1295, 1728, 2591)
secant_rows = []
for label, x in (("initial", D["x0"]), ("root", D["x"])):
    exact_gradient = high_precision_price_gradient(x)
    for flat_index in selected:
        secant = price_secant(x, flat_index, "1e-7")
        delta = abs(secant - exact_gradient[flat_index])
        secant_rows.append({
            "state": label,
            "variable": flat_index,
            "site": list(unknown_sites[flat_index % Nin]),
            "species": flat_index // Nin,
            "abs_secant_delta": float(delta),
        })
assert max(row["abs_secant_delta"] for row in secant_rows) < 1e-20

# Check the analytic sparse Jacobian by a deterministic directional secant.
rng = np.random.default_rng(20261021)
direction = rng.normal(size=len(D["x"]))
direction /= np.linalg.norm(direction, np.inf)
jacobian_rows = []
for label, x in (("initial", D["x0"]), ("root", D["x"])):
    _, _, jacobian = D["source"](x, True)
    analytic = jacobian @ direction
    step = 1e-5
    finite = (
        D["source"](x + step * direction)[0]
        - D["source"](x - step * direction)[0]
    ) / (2 * step)
    error = np.linalg.norm(finite - analytic, np.inf)
    relative = error / max(np.linalg.norm(finite, np.inf), 1e-300)
    jacobian_rows.append({
        "state": label,
        "step": step,
        "directional_relative_error": float(relative),
    })
assert max(row["directional_relative_error"] for row in jacobian_rows) < 2e-8

source_before, _ = D["source"](D["x0"])
source_after, (q_after, _) = D["source"](D["x"])
solver_root = {
    "iterations": int(D["it"]),
    "source_inf_before": float(np.max(np.abs(source_before))),
    "source_inf_after": float(np.max(np.abs(source_after))),
    "species_source_inf_after": [
        float(np.max(np.abs(source_after[a * Nin:(a + 1) * Nin])))
        for a in range(2)
    ],
    "max_field_value_correction": float(np.max(np.abs(D["x"] - D["x0"]))),
    "max_resulting_nonlinear_q": float(np.max(np.abs(q_after))),
    "native_pf_minmax": [float(np.min(D["rho"])), float(np.max(D["rho"]))],
}

result = {
    "status": "PASS_FULL4D_TRUE_ENTROPY_PRICE_GRADIENT_AND_JACOBIAN_CONTROLS",
    "native_histories": 75025,
    "native_sites": 4096,
    "forward_cells": len(cells),
    "interior_scalar_unknowns": 2 * Nin,
    "all_four_dimensional_dirichlet_collars_fixed": True,
    "mp_dps": mp.mp.dps,
    "solver_root": solver_root,
    "price_gradient": price_gradients,
    "representative_price_secants": secant_rows,
    "sparse_jacobian_directional_secants": jacobian_rows,
    "scope": {
        "fixed_geometry_matter_subsystem_only": True,
        "coframe16_root": False,
        "proper_link24_root": False,
        "compulsory_Book03_price_selected": False,
        "uniform_refinement_proved": False,
        "physical_GR_closed": False,
    },
}
print(json.dumps(result, indent=2))
