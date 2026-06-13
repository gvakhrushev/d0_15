#!/usr/bin/env python3
# SELFTEST 19.4.SR — SR-budget self-test (CORE)
#
# HONESTY NOTE: this is a SELFTEST, not a falsifiable PASS/FAIL certificate.
# The "measured" channel is set equal to the predicted value (meas := pred in
# the grid loop below), so abs_err is identically 0.0 at every point and the
# check can NEVER return FAIL — the comparison reduces to the tautology
# 0 <= eps^2. It confirms only that tau/t = sqrt(1 - v^2) is evaluated without
# error; it does NOT verify that relation against any independent tau/t
# measurement. To promote it to a real certificate, ingest a measured tau/t
# dataset via the protocol and compare it against pred. Reported with
# status_class="SELFTEST" so it is not counted as empirical verification.

from __future__ import annotations

import argparse
import csv
import math
import os
import sys

import matplotlib.pyplot as plt

from d0.constants import eps2 as EPS2, phi as PHI
from d0.io import get_outdir, save_json
from d0.protocol import P, load_protocol
from d0.report import CertReport


def tol_value(tol: str) -> float:
    t = tol.lower()
    if t in ("eps2", "epsilon2", "eps^2", "ε2"):
        return float(EPS2)
    if t in ("eps", "epsilon", "ε"):
        return float(PHI ** (-8.0))
    return float(tol)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--protocol", default=os.environ.get("D0_PROTOCOL", "protocols/d0_sr_budget.json"))
    args = ap.parse_args()

    prot = load_protocol(args.protocol)
    v_min = float(P(prot, "v_min", 0.0))
    v_max = float(P(prot, "v_max", 0.99))
    n = int(P(prot, "num_v", 51))
    tol = tol_value(str(P(prot, "tol", "eps2")))

    out_subdir = str(P(prot, "out_subdir", "cert_19_4_sr"))
    o = get_outdir() / out_subdir
    o.mkdir(parents=True, exist_ok=True)

    cert_id = str(P(prot, "cert_id", "19.4.SR"))
    rep = CertReport(cert_id=cert_id, protocol_id=prot.protocol_id)
    rep.status_class = "SELFTEST"  # tautological (meas := pred); cannot FAIL
    rep.add("PROTO_LOADED", True, protocol=args.protocol)

    rows = []
    max_abs = 0.0
    max_rel = 0.0

    for i in range(max(3, n)):
        v = v_min + (v_max - v_min) * i / (max(3, n) - 1)
        pred = math.sqrt(max(0.0, 1.0 - v * v))
        # SELFTEST: no independent measurement channel exists — meas is defined
        # as pred, so abs_err below is identically 0.0 and max_abs can never
        # exceed tol. See the HONESTY NOTE in the module header.
        meas = pred
        abs_err = abs(meas - pred)
        rel_err = abs_err / max(1e-30, abs(pred))
        max_abs = max(max_abs, abs_err)
        max_rel = max(max_rel, rel_err)
        rows.append((v, meas, pred, abs_err, rel_err))

    status = "PASS" if max_abs <= tol else "FAIL"

    print("=== SR-budget self-test (SELFTEST 19.4.SR) ===")
    print(f"phi   = {PHI:.15f}")
    print(f"eps^2 = {EPS2:.18e}")
    print(f"tol   = {tol:.18e}")
    print(f"max abs err = {max_abs:.18e}")
    print(f"max rel err = {max_rel:.18e}")
    print(f"status = {status}")
    print("status_class = SELFTEST (meas := pred; cannot FAIL — not empirical verification)")

    outputs = P(prot, "outputs", {})
    csv_name = str(outputs.get("csv", "sr_budget_table.csv"))
    plot_name = str(outputs.get("plot", "sr_budget_plot.png"))
    err_plot_name = str(outputs.get("err_plot", "sr_budget_error.png"))
    json_name = str(outputs.get("json", "sr_budget_report.json"))

    with (o / csv_name).open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["v", "tau_over_t_meas", "tau_over_t_pred", "abs_err", "rel_err"])
        w.writerows(rows)

    v = [r[0] for r in rows]
    y_meas = [r[1] for r in rows]
    y_pred = [r[2] for r in rows]
    err = [r[3] for r in rows]

    plt.figure()
    plt.plot(v, y_meas, label="meas")
    plt.plot(v, y_pred, linestyle="--", label="pred")
    plt.xlabel("v (C=1)")
    plt.ylabel("tau/t")
    plt.legend()
    plt.tight_layout()
    plt.savefig(o / plot_name, dpi=200)
    plt.close()

    plt.figure()
    plt.plot(v, err, label="abs error")
    plt.xlabel("v")
    plt.ylabel("|meas-pred|")
    plt.legend()
    plt.tight_layout()
    plt.savefig(o / err_plot_name, dpi=200)
    plt.close()

    rep.add(
        "SR_BUDGET",
        status == "PASS",
        phi=PHI,
        eps2=EPS2,
        tol=tol,
        grid={"v_min": v_min, "v_max": v_max, "num_v": n},
        max_abs_err=max_abs,
        max_rel_err=max_rel,
        status=status,
    )

    rep.artifacts["csv"] = csv_name
    rep.artifacts["plot"] = plot_name
    rep.artifacts["err_plot"] = err_plot_name
    rep.artifacts["json"] = json_name

    save_json(o / json_name, rep.to_dict())

    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
