#!/usr/bin/env python3
"""Exact Fraction control on one legal path of the original 33-state scene."""
from fractions import Fraction as Q
import json

parts = (9, 11, 13)
offsets = (0, 9, 20)
N = 101
path = [offsets[t % 3] + (t // 3) % parts[t % 3] for t in range(N + 1)]
zone = lambda i: 0 if i < 9 else (1 if i < 20 else 2)
assert all(zone(u) != zone(v) for u, v in zip(path, path[1:]))
counts = [[0] * 33 for _ in range(33)]
for u, v in zip(path, path[1:]):
    counts[u][v] += 1
outgoing = [sum(row) for row in counts]
incoming = [sum(counts[u][i] for u in range(33)) for i in range(33)]
assert min(outgoing) > 0
P = [[Q(counts[u][v], outgoing[u]) for v in range(33)] for u in range(33)]
cov = [[Q(0)] * 33 for _ in range(33)]
for u, v in zip(path, path[1:]):
    eps = [Q(int(i == v)) - P[u][i] for i in range(33)]
    for i in range(33):
        for j in range(33):
            cov[i][j] += eps[i] * eps[j] / N

naive = [[Q(int(i == j) * outgoing[i], N) -
          sum(Q(outgoing[u], N) * P[u][i] * P[u][j] for u in range(33))
          for j in range(33)] for i in range(33)]
endpoint = [Q(int(path[-1] == i) - int(path[0] == i), N) for i in range(33)]
assert all(incoming[i] - outgoing[i] ==
           int(path[-1] == i) - int(path[0] == i) for i in range(33))
assert all(cov[i][j] == naive[i][j] + (endpoint[i] if i == j else 0)
           for i in range(33) for j in range(33))
assert all(sum(row) == 0 for row in cov)
assert any(sum(row) != 0 for row in naive)
assert path[0] != path[-1]
print(json.dumps({
    "status": "PASS",
    "originalVertices": 33,
    "pathTransitions": N,
    "allOutgoingVerticesVisited": True,
    "initialVertex": path[0],
    "terminalVertex": path[-1],
    "all1089ExactEndpointMatrixEqualities": True,
    "all33ExactCovarianceConstantModeEqualities": True,
    "omittedEndpointDestroysConstantMode": True,
    "nonzeroNaiveRowSums": {
        str(i): str(sum(row)) for i, row in enumerate(naive) if sum(row)
    },
}, indent=2))
