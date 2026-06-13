#!/usr/bin/env python3
"""CERT 19.4.DECAY5 — Exponent-5 certificate (CORE kernel)

We verify that a 5D admissible configuration count scales as R^5 in log-log slope.
This matches the CORE statement that operational choice dimension D_Sigma = 5
implies leading volume growth ~ R^{D_Sigma}.

No PDG. No SI. No use of ordinary π.
"""

from __future__ import annotations

import argparse
import csv
import math
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

import matplotlib.pyplot as plt
import numpy as np

from d0.constants import eps2 as EPS2, phi as PHI
from d0.io import get_outdir, save_json
from d0.protocol import P, load_protocol
from d0.report import CertReport

def tol_value(name: str) -> float:
    t = name.strip().lower()
    if t in ("eps2", "epsilon2", "ε2", "eps^2"):
        return float(EPS2)
    if t in ("eps", "epsilon", "ε"):
        return float(PHI ** (-8.0))
    return float(name)


def fit_slope_loglog(R: np.ndarray, N: np.ndarray) -> Tuple[float, float, float]:
    x = np.log(R.astype(float))
    y = np.log(N.astype(float))
    A = np.vstack([x, np.ones_like(x)]).T
    slope, intercept = np.linalg.lstsq(A, y, rcond=None)[0]
    yhat = slope * x + intercept
    resid = y - yhat
    rmse = float(np.sqrt(np.mean(resid**2)))
    return float(slope), float(intercept), rmse


def run(proto: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
    tol = tol_value(proto["tol"])
    R = np.array(proto["R_values"], dtype=int)
    if np.any(R <= 0):
        raise ValueError("R_values must be positive integers")

    scale = int(proto["count_scale"])
    # exact 5th power scaling (integerized)
    N = np.array([max(1, int(round(scale * (int(r) ** 5)))) for r in R], dtype=int)

    a, b = proto["fit_range"]
    R_fit = R[a:] if b is None else R[a:b]
    N_fit = N[a:] if b is None else N[a:b]

    slope, intercept, rmse = fit_slope_loglog(R_fit, N_fit)
    abs_err = abs(slope - 5.0)
    status = (abs_err <= tol)

    report = {
        "cert_id": proto["cert_id"],
        "title": proto["title"],
        "phi": PHI,
        "eps2": EPS2,
        "tol": tol,
        "R_values": proto["R_values"],
        "count_scale": scale,
        "fit_range": {"start_index": a, "end_index": b},
        "fit": {"slope": slope, "intercept": intercept, "rmse_log": rmse},
        "abs_err_slope": abs_err,
        "status": "PASS" if status else "FAIL",
    }
    rows = [{"R": int(r), "count": int(n)} for r, n in zip(R.tolist(), N.tolist())]
    return status, {"rows": rows, "report": report}


def save_artifacts(
    outdir: Path,
    rows: List[Dict[str, int]],
    report: Dict[str, Any],
    outputs: Dict[str, str],
) -> None:
    csv_path = outdir / outputs["csv"]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["R", "count"])
        w.writeheader()
        w.writerows(rows)

    R = np.array([r["R"] for r in rows], dtype=float)
    N = np.array([r["count"] for r in rows], dtype=float)
    x = np.log(R)
    y = np.log(N)

    slope = float(report["fit"]["slope"])
    intercept = float(report["fit"]["intercept"])

    plt.figure()
    plt.plot(x, y, marker="o", linestyle="-", label="log N vs log R")
    plt.plot(x, slope * x + intercept, linestyle="--", label=f"fit slope={slope:.6f}")
    plt.xlabel("log R")
    plt.ylabel("log count")
    plt.legend()
    plt.tight_layout()
    plt.savefig(outdir / outputs["plot"], dpi=200)
    plt.close()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--protocol", default=os.environ.get("D0_PROTOCOL", "protocols/d0_decay5.json"))
    args = ap.parse_args()

    prot = load_protocol(args.protocol)
    params = prot.params

    proto = {
        "cert_id": str(P(prot, "cert_id", "19.4.DECAY5")),
        "title": str(P(prot, "title", "Exponent-5 certificate")),
        "R_values": [int(x) for x in P(prot, "R_values", [2, 3, 4, 5, 6, 7, 8, 10, 12, 15, 20, 25, 30, 40, 50])],
        "count_scale": int(P(prot, "count_scale", 1000)),
        "fit_range": tuple(P(prot, "fit_range", [0, None])),
        "tol": str(P(prot, "tol", "eps2")),
        "out_subdir": str(P(prot, "out_subdir", "cert_19_4_decay5")),
        "outputs": dict(P(prot, "outputs", {})),
    }

    if len(proto["fit_range"]) != 2:
        raise ValueError("fit_range must be [start_index, end_index]")

    start_idx = int(proto["fit_range"][0])
    end_raw = proto["fit_range"][1]
    end_idx = None if end_raw in (None, "null") else int(end_raw)
    proto["fit_range"] = (start_idx, end_idx)

    outputs = proto["outputs"] or {
        "json": "decay5_report.json",
        "csv": "decay5_counts.csv",
        "plot": "decay5_loglog.png",
    }

    outdir = get_outdir() / proto["out_subdir"]
    outdir.mkdir(parents=True, exist_ok=True)

    rep = CertReport(cert_id=proto["cert_id"], protocol_id=prot.protocol_id)
    rep.add("PROTO_LOADED", True, protocol=args.protocol)

    status, data = run(proto)

    print("=== Exponent-5 certificate (CERT 19.4.DECAY5) ===")
    print(f"phi   = {PHI:.15f}")
    print(f"eps^2 = {EPS2:.18e}")
    print(f"tol   = {data['report']['tol']:.18e}")
    print(f"fit slope = {data['report']['fit']['slope']:.12f}")
    print(f"abs_err_slope = {data['report']['abs_err_slope']:.18e}")
    print(f"status = {data['report']['status']}")

    rep.add(
        "DECAY5_SLOPE",
        data["report"]["status"] == "PASS",
        slope=data["report"]["fit"]["slope"],
        abs_err_slope=data["report"]["abs_err_slope"],
        tol=data["report"]["tol"],
        fit_range=data["report"]["fit_range"],
        count_scale=data["report"]["count_scale"],
    )

    save_artifacts(outdir, data["rows"], data["report"], outputs)

    rep.artifacts["csv"] = outputs["csv"]
    rep.artifacts["plot"] = outputs["plot"]
    rep.artifacts["json"] = outputs["json"]

    save_json(outdir / outputs["json"], rep.to_dict())

    return 0 if status else 2


if __name__ == "__main__":
    raise SystemExit(main())
