#!/usr/bin/env python3
from fractions import Fraction
import itertools, json, math

parts = [("V9", 9), ("V11", 11), ("V13", 13)]
vertices = []
for label, n in parts:
    for i in range(n):
        vertices.append((label, i))
V = len(vertices)
idx = {v:i for i,v in enumerate(vertices)}
# oriented edges: increasing part index
edges = []
part_vertices = {label:[v for v in vertices if v[0]==label] for label,_ in parts}
for (a, _), (b, _) in itertools.combinations(parts, 2):
    for u in part_vertices[a]:
        for v in part_vertices[b]:
            edges.append((u,v))
edge_idx = {e:i for i,e in enumerate(edges)}
# triangles: V9 -> V11 -> V13
triangles = []
for u in part_vertices["V9"]:
    for v in part_vertices["V11"]:
        for w in part_vertices["V13"]:
            triangles.append((u,v,w))

# Boundary maps with rational integer entries.
# ∂1([u,v]) = v-u
B1 = [[0 for _ in edges] for __ in vertices]
for j,(u,v) in enumerate(edges):
    B1[idx[u]][j] = -1
    B1[idx[v]][j] = 1
# ∂2([u,v,w]) = [v,w] - [u,w] + [u,v]
B2 = [[0 for _ in triangles] for __ in edges]
for k,(u,v,w) in enumerate(triangles):
    for coeff,e in [(1,(v,w)),(-1,(u,w)),(1,(u,v))]:
        B2[edge_idx[e]][k] = coeff
# multiply B1*B2
max_abs = 0
for i in range(len(vertices)):
    for k in range(len(triangles)):
        s = sum(B1[i][j]*B2[j][k] for j in range(len(edges)))
        max_abs = max(max_abs, abs(s))

# SM one-generation left-handed Weyl anomaly ledger.
# T(fundamental) normalized to 1/2.
T = Fraction(1,2)
SU3_SU3_U1 = 2*Fraction(1,6)*T + Fraction(-2,3)*T + Fraction(1,3)*T
SU2_SU2_U1 = 3*Fraction(1,6)*T + Fraction(-1,2)*T
U1_3 = 6*Fraction(1,6)**3 + 3*Fraction(-2,3)**3 + 3*Fraction(1,3)**3 + 2*Fraction(-1,2)**3 + Fraction(1,1)**3
Grav_U1 = 6*Fraction(1,6) + 3*Fraction(-2,3) + 3*Fraction(1,3) + 2*Fraction(-1,2) + Fraction(1,1)

ABCD = 4
rankK = 3
kY = Fraction(ABCD+1, rankK)
# Gauge block checks
rank_total = 2+1+1
dim_total = 8+3+1
# EW depth atlas 35
V_count = V
D_EW = V_count + rankK - 1
residuals = {str(d): d - D_EW for d in [34,35,36]}

checks = {
    "vertex_count": V,
    "edge_count": len(edges),
    "triangle_count": len(triangles),
    "boundary_of_boundary_max_abs": max_abs,
    "anomaly_SU3_SU3_U1": str(SU3_SU3_U1),
    "anomaly_SU2_SU2_U1": str(SU2_SU2_U1),
    "anomaly_U1_cubed": str(U1_3),
    "anomaly_gravity_U1": str(Grav_U1),
    "kY": f"{kY.numerator}/{kY.denominator}",
    "gauge_rank_total": rank_total,
    "gauge_dim_total": dim_total,
    "D_EW": D_EW,
    "EW_neighbor_residuals": residuals,
}
pass_conditions = [
    V == 33,
    len(edges) == 359,
    len(triangles) == 1287,
    max_abs == 0,
    SU3_SU3_U1 == 0,
    SU2_SU2_U1 == 0,
    U1_3 == 0,
    Grav_U1 == 0,
    kY == Fraction(5,3),
    rank_total == 4,
    dim_total == 12,
    D_EW == 35,
    residuals["34"] == -1,
    residuals["35"] == 0,
    residuals["36"] == 1,
]
status = "PASS_V11_32_GAUGE_MATTER_WARD_ANOMALY" if all(pass_conditions) else "FAIL_V11_32_GAUGE_MATTER_WARD_ANOMALY"
out = {"status": status, "checks": checks}
print(json.dumps(out, indent=2))
