#!/usr/bin/env python3
"""Exact finite controls for the Book 03 Cost-Info junction certificate."""

from fractions import Fraction as F
import json


def require(condition, message):
    if not condition:
        raise SystemExit("FAIL: " + message)


def zone(v):
    if v < 9:
        return 0
    if v < 20:
        return 1
    return 2


vertices = range(33)
edges = [(u, v) for u in vertices for v in vertices if zone(u) != zone(v)]
require(len(edges) == 718, "literal K(9,11,13) directed edge count")
neighbors = {v: [u for u in vertices if zone(v) != zone(u)] for v in vertices}
require(all(neighbors.values()), "every actual scene vertex has a predecessor and successor")


def cost(edge):
    u, v = edge
    return F((17 * u + 7 * v) % 83 + 9, 7)


def info(v):
    return F(v * v + 3 * v + 1, 11)


def edge_cost(u, v):
    return cost((u, v))


def allocated(u, v, theta):
    return edge_cost(u, v) - theta * info(u) - (1 - theta) * info(v)


def allocated_path(path, theta):
    return sum((allocated(u, v, theta) for u, v in zip(path, path[1:])), F(0))


def literal(path):
    return sum((edge_cost(u, v) for u, v in zip(path, path[1:])), F(0)) - sum(
        (info(v) for v in path), F(0)
    )


thetas = [F(0), F(1, 3), F(1, 2), F(1)]
edge_boundary_checks = 0
for theta in thetas:
    for eta in thetas:
        for u, v in edges:
            lhs = allocated(u, v, theta) - allocated(u, v, eta)
            rhs = (theta - eta) * (info(v) - info(u))
            require(lhs == rhs, "allocation difference is the endpoint coboundary")
            edge_boundary_checks += 1

two_step_paths = [
    (u, v, w)
    for v in vertices
    for u in neighbors[v]
    for w in neighbors[v]
]
require(len(two_step_paths) == 15708, "complete two-step scene path carrier")

literal_defect_checks = 0
additivity_checks = 0
endpoint_checks = 0
for u, v, w in two_step_paths:
    require(literal((u, v, w)) == literal((u, v)) + literal((v, w)) + info(v),
            "literal all-vertices Info has exactly one shared-junction defect")
    literal_defect_checks += 1
    for theta in thetas:
        require(allocated_path((u, v, w), theta) ==
                allocated_path((u, v), theta) + allocated_path((v, w), theta),
                "edge-attached allocation composes additively")
        additivity_checks += 1
    for theta in thetas:
        for eta in thetas:
            delta = (allocated(u, v, theta) + allocated(v, w, theta)) - (
                allocated(u, v, eta) + allocated(v, w, eta)
            )
            require(delta == (theta - eta) * (info(w) - info(u)),
                    "two-step action difference is endpoint-only")
            endpoint_checks += 1

closed_checks = 0
for u, v in edges:
    for theta in thetas:
        for eta in thetas:
            require(allocated(u, v, theta) + allocated(v, u, theta) ==
                    allocated(u, v, eta) + allocated(v, u, eta),
                    "closed two-step histories erase the allocation parameter")
            closed_checks += 1

open_control = allocated(0, 9, F(1)) - allocated(0, 9, F(0))
require(open_control == info(9) - info(0) and open_control != 0,
        "open-history boundary term is not universally invisible")
wrong_sign_control = ((allocated(0, 9, F(1)) - allocated(0, 9, F(0))) !=
                      (info(0) - info(9)))
require(wrong_sign_control, "wrong-sign boundary mutation is detected")

result = {
    "status": "PASS_SCOPED_COST_INFO_BOUNDARY",
    "vertices": 33,
    "directed_edges": len(edges),
    "two_step_paths": len(two_step_paths),
    "allocation_parameters": [str(theta) for theta in thetas],
    "checks": {
        "edge_boundary_identity": edge_boundary_checks,
        "literal_junction_defect": literal_defect_checks,
        "edge_additivity": additivity_checks,
        "open_endpoint_difference": endpoint_checks,
        "closed_two_step_invariance": closed_checks,
        "hostile_controls": 2,
    },
    "open_control_difference": str(open_control),
    "lean_theorem_scope": "universal identities are proved in the companion Lean certificate",
    "physical_cost_info_map_selected": False,
    "physical_source_or_gr_closure": False,
}
print(json.dumps(result, sort_keys=True, separators=(",", ":")))
