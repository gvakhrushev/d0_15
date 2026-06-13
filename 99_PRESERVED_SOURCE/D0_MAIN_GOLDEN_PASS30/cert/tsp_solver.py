# -*- coding: utf-8 -*-
"""
φ-TSP Solver — CERT 24.5.3 (D0 §24): TSP as CORE navigation/certificate

Key strictness fix:
- "φ-cutoff" of the best/φ type is NOT a valid mechanism for exact optimum
  (it can drop the optimal branch). Therefore CERT needs a scheme with:
  (A) poly(n) solution construction, (B) poly(n) verification/certificate.

In this demonstrator:
- φ-CORE class: all points lie on the convex hull (convex position).
  Then the optimal TSP tour = traversal of hull vertices in cyclic order.
  Certificate: |Hull| == n (checkable in O(n log n)).
- The generator uses the "golden angle" (φ) to place points on a circle,
  to emphasize φ-structure, but the certificate core is the convex hull.

For calibration:
- For small n we also compute the exact Held–Karp optimum (O(n^2 2^n))
  and check the match (COP≡DP on φ-CORE input).
"""

import random
import math
import time
import argparse
import os
from typing import List, Tuple, Optional

from d0.constants import phi as PHI, eps2 as EPS2
from d0.protocol import load_protocol, P
from d0.io import get_outdir, save_json
from d0.report import CertReport

# BRIDGE: the Euclidean circle uses ordinary π (not a CORE invariant).
GOLDEN_ANGLE = 2 * math.pi * (1 - 1 / PHI)  # = 2π/φ^2


def generate_phi_cities_on_circle(n: int, seed: int = 42, radius: float = 100.0) -> List[Tuple[float, float]]:
    """
    φ-CORE generator:
    - points on a circle ⇒ all points on the hull
    - angles follow the golden-angle sequence plus a random offset (seed)
    """
    rng = random.Random(seed)
    offset = rng.random() * 2 * math.pi
    angles = [(offset + k * GOLDEN_ANGLE) % (2 * math.pi) for k in range(n)]
    angles.sort()
    return [(radius * math.cos(a), radius * math.sin(a)) for a in angles]


def cross(o, a, b) -> float:
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def convex_hull_indices(points: List[Tuple[float, float]]) -> List[int]:
    """Andrew monotonic chain, hull indices in CCW order (no duplicates)."""
    pts = [(p[0], p[1], i) for i, p in enumerate(points)]
    pts.sort()

    if len(pts) <= 1:
        return [pts[0][2]] if pts else []

    lower: List[Tuple[float, float, int]] = []
    for p in pts:
        while len(lower) >= 2 and cross((lower[-2][0], lower[-2][1]),
                                        (lower[-1][0], lower[-1][1]),
                                        (p[0], p[1])) <= 0:
            lower.pop()
        lower.append(p)

    upper: List[Tuple[float, float, int]] = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross((upper[-2][0], upper[-2][1]),
                                        (upper[-1][0], upper[-1][1]),
                                        (p[0], p[1])) <= 0:
            upper.pop()
        upper.append(p)

    hull = lower[:-1] + upper[:-1]
    return [p[2] for p in hull]


class TSPSolver:
    def __init__(self, cities: List[Tuple[float, float]]):
        self.cities = cities
        self.n = len(cities)
        self.dist = self._compute_dist()

    def _compute_dist(self) -> List[List[float]]:
        n = self.n
        d = [[0.0] * n for _ in range(n)]
        for i in range(n):
            xi, yi = self.cities[i]
            for j in range(n):
                if i == j:
                    continue
                xj, yj = self.cities[j]
                d[i][j] = math.hypot(xi - xj, yi - yj)
        return d

    def tour_cost(self, path: List[int]) -> float:
        return sum(self.dist[path[i]][path[i+1]] for i in range(len(path)-1))

    # ----- D0 φ-CORE solver -----
    def solve_phi_core(self) -> Tuple[Optional[float], Optional[List[int]], dict]:
        hull = convex_hull_indices(self.cities)
        cert = {
            "cert_id": "24.5.3.tsp",
            "phi": PHI,
            "eps2": EPS2,
            "phi_core": False,
            "hull_size": len(hull),
            "n": self.n,
            "hull_indices": hull,
        }

        if len(hull) != self.n:
            return None, None, cert

        cert["phi_core"] = True

        # rotate hull order so city 0 is first
        if 0 in hull:
            k0 = hull.index(0)
            order = hull[k0:] + hull[:k0]
        else:
            order = hull

        path = order + [order[0]]
        cost = self.tour_cost(path)

        cert["tour_path"] = path
        cert["tour_cost"] = cost
        return cost, path, cert

    # ----- Strict exact for small n -----
    def solve_exact_held_karp(self) -> Tuple[float, List[int]]:
        n = self.n
        INF = float("inf")
        dp = [[INF] * n for _ in range(1 << n)]
        parent = [[(-1, -1)] * n for _ in range(1 << n)]

        dp[1][0] = 0.0

        for mask in range(1, 1 << n):
            for last in range(n):
                if not (mask & (1 << last)):
                    continue
                cur = dp[mask][last]
                if cur == INF:
                    continue
                for nxt in range(n):
                    if mask & (1 << nxt):
                        continue
                    nm = mask | (1 << nxt)
                    v = cur + self.dist[last][nxt]
                    if v < dp[nm][nxt]:
                        dp[nm][nxt] = v
                        parent[nm][nxt] = (mask, last)

        full = (1 << n) - 1
        best_cost = INF
        best_last = -1
        for last in range(n):
            v = dp[full][last] + self.dist[last][0]
            if v < best_cost:
                best_cost = v
                best_last = last

        # reconstruct
        path = []
        mask = full
        cur = best_last
        while cur != -1:
            path.append(cur)
            pm, pl = parent[mask][cur]
            if pm == -1:
                break
            mask, cur = pm, pl
        path.reverse()
        path.append(0)
        return best_cost, path


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--protocol", default=os.environ.get("D0_PROTOCOL", "protocols/book5_tsp_solver.json"))
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    PROT = load_protocol(args.protocol)

    outdir = get_outdir() / "cert_24_5_3_phi_tsp"
    outdir.mkdir(parents=True, exist_ok=True)

    rep = CertReport(cert_id="CERT_24_5_3_PHI_TSP", protocol_id=PROT.protocol_id)
    rep.add("PROTO_LOADED", True, protocol=args.protocol)

    seed = int(P(PROT, "seed", 42))
    n_list = list(map(int, P(PROT, "n_list", [10, 12, 15, 50, 200])))
    radius = float(P(PROT, "radius", 100.0))
    exact_max_n = int(P(PROT, "exact_max_n", 15))

    print("=== φ-TSP Solver — Demonstration (CERT 24.5.3) ===\n")
    print("φ-CORE condition: |Hull| == n (all points on hull) ⇒ optimal tour = hull traversal.\n")

    for n in n_list:
        cities = generate_phi_cities_on_circle(n, seed=seed, radius=radius)
        solver = TSPSolver(cities)

        core_cost, core_path, cert = solver.solve_phi_core()
        core_ok = (core_cost is not None)
        rep.add(f"HULL_CERT_N{n}", bool(core_ok), hull_size=int(cert["hull_size"]), n=int(n))

        if core_cost is None:
            continue

        if n <= exact_max_n:
            t0 = time.time()
            exact_cost, exact_path = solver.solve_exact_held_karp()
            dt = time.time() - t0
            same = abs(exact_cost - core_cost) < 1e-9
            rep.add(f"HK_MATCH_N{n}", bool(same), time_sec=float(dt), core_cost=float(core_cost), exact_cost=float(exact_cost))
        else:
            rep.skip(f"HK_MATCH_N{n}", f"n>{exact_max_n}")

    out_json = outdir / P(PROT, "outputs")["json"]
    save_json(out_json, rep.to_dict())
    return 0 if rep.ok() else 2


if __name__ == "__main__":
    raise SystemExit(main())
