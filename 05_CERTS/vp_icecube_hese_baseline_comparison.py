#!/usr/bin/env python3
"""IceCube HESE baseline comparison with empirical no-deco energy-shape null + secondary topology.

Implements low+mid to predict high bin under no-deco null vs frozen D0 damping.
No free params, no post-hoc cuts. Uses pinned data and curve only.
"""

from __future__ import annotations
import csv
import json
import math
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
PASSPORT_DIR = ROOT / "08_PASSPORTS" / "IceCube"
DATA_PATH = ROOT / "08_PASSPORTS" / "_EXTERNAL_DATA_CACHE" / "icecube" / "hese12" / "data.tab"
CURVE_PATH = PASSPORT_DIR / "icecube_phason_decoherence_curve.csv"
RESULTS_CSV = PASSPORT_DIR / "icecube_hese_baseline_results.csv"
SUMMARY_JSON = PASSPORT_DIR / "icecube_hese_baseline_summary.json"
SUMMARY_MD = PASSPORT_DIR / "icecube_hese_baseline_summary.md"

PASS_TOKEN = "PASS_ICECUBE_HESE_D0_BASELINE_COMPARISON"
FAIL_TOKEN = "FAIL_ICECUBE_HESE_D0_BASELINE_COMPARISON"
SKIP_ENERGY = "SKIP_ICECUBE_HESE_ENERGY_FIELD_REQUIRED"
SKIP_TABLE = "SKIP_ICECUBE_HESE_EVENT_TABLE_REQUIRED"

def load_data():
    if not DATA_PATH.exists():
        return None, None
    events = []
    with DATA_PATH.open("r", encoding="utf-8", errors="ignore", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            try:
                e = float(row.get("energy", 0))
                reco = row.get("reconstruction", "").strip()
                events.append({"energy": e, "reco": reco})
            except:
                pass
    return events, len(events)

def load_curve():
    if not CURVE_PATH.exists():
        return []
    rows = []
    with CURVE_PATH.open("r", encoding="utf-8", errors="ignore", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                rows.append({
                    "energy": float(row["energy"]),
                    "damping": float(row["damping_d0"]),
                    "reco": row.get("reconstruction", "")
                })
            except:
                pass
    return rows

def bin_events(events, bins):
    # bins = list of (low, high) or use quantiles but fixed log for reproducibility
    counts = [0] * (len(bins)+1)
    for ev in events:
        e = ev["energy"]
        placed = False
        for i, (lo, hi) in enumerate(bins):
            if lo <= e < hi:
                counts[i] += 1
                placed = True
                break
        if not placed:
            counts[-1] += 1
    return counts

def make_log_bins(events, n=3):
    es = sorted(e["energy"] for e in events)
    if not es: return []
    lo = math.log10(min(es))
    hi = math.log10(max(es))
    edges = [10** (lo + i*(hi-lo)/n) for i in range(n+1)]
    bins = [(edges[i], edges[i+1]) for i in range(n)]
    return bins, edges

def compute_poisson_loglik(k, mu):
    if mu <= 0:
        return -1e9 if k > 0 else 0.0
    return k * math.log(mu) - mu - math.lgamma(k+1)

def main():
    events, n_events = load_data()
    curve = load_curve()
    if events is None or n_events == 0:
        print(SKIP_TABLE)
        return 1
    if not any("energy" in e for e in events) or all(e["energy"]<=0 for e in events):
        print(SKIP_ENERGY)
        return 1

    # make 3 log bins from data
    bins, edges = make_log_bins(events, 3)
    # low+mid = first 2 bins for shape estimation; high = last
    low_mid_events = [e for e in events if bins[0][0] <= e["energy"] < bins[1][1]]
    high_events = [e for e in events if e["energy"] >= bins[1][1]]

    # null: use low+mid count density to predict high bin width scaled
    # simple: total low_mid / effective 'width' , but for counts, use ratio of bin 'measures'
    # for conservative empirical: assume power law alpha fitted from low/mid counts
    # or simplest: expected_high_null = n_high_observed * (but no, use shape from lowmid to scale)
    # Better: total events in lowmid, assume uniform in log or fit alpha
    n_lm = len(low_mid_events)
    n_high_obs = len(high_events)
    # fit rough alpha from bin counts (use mid/low ratio)
    # bins[0] low, bins[1] mid
    c0 = sum(1 for e in events if bins[0][0] <= e["energy"] < bins[0][1])
    c1 = sum(1 for e in events if bins[1][0] <= e["energy"] < bins[1][1])
    # expected ratio mid/low ~ (width ratio) * 10**(alpha * dlog)
    # for null prediction of high: extrapolate
    if c0 > 0 and c1 > 0:
        alpha = math.log10( (c1 / max(c0,1e-9)) ) / (math.log10(bins[1][0]) - math.log10(bins[0][0]) + 1e-9)
    else:
        alpha = -2.0  # typical astro
    # predict high count under null (scale from mid bin)
    logw_mid = math.log10(bins[1][1]) - math.log10(bins[1][0])
    logw_high = math.log10(edges[-1]) - math.log10(bins[1][1])
    scale = (10**(alpha * logw_high)) * (logw_high / max(logw_mid,1e-9))
    mu_null = max(c1 * scale, 0.1)  # expected high under null

    # D0: average damping in high bin
    high_curve = [c for c in curve if c["energy"] >= bins[1][1]]
    if high_curve:
        avg_damp = sum(c["damping"] for c in high_curve) / len(high_curve)
    else:
        avg_damp = 0.9999
    mu_d0 = mu_null * avg_damp

    k = n_high_obs
    loglik_null = compute_poisson_loglik(k, mu_null)
    loglik_d0 = compute_poisson_loglik(k, mu_d0)
    delta_loglik = loglik_d0 - loglik_null

    # chi2 approx (k-mu)^2 / mu for high bin
    chi2_null = (k - mu_null)**2 / max(mu_null, 1)
    chi2_d0 = (k - mu_d0)**2 / max(mu_d0, 1)
    delta_chi2 = chi2_d0 - chi2_null   # smaller better, so if negative D0 better

    # topology ratio if available
    topo_metric = None
    if any(e["reco"] for e in events):
        def ratio_in_bin(evlist, lo, hi):
            sub = [e for e in evlist if lo <= e["energy"] < hi]
            n_track = sum(1 for e in sub if "Track" in e.get("reco",""))
            n_shower = len(sub) - n_track
            return n_track / max(n_shower,1) if sub else None
        r_low = ratio_in_bin(events, bins[0][0], bins[0][1])
        r_mid = ratio_in_bin(events, bins[1][0], bins[1][1])
        r_high = ratio_in_bin(events, bins[1][1], 1e10)
        if r_low and r_mid and r_high:
            # null: ratio flat ~ avg lowmid
            null_ratio = ( (r_low or 0) + (r_mid or 0) ) / 2
            d0_ratio_pred = null_ratio  # D0 damping same for track/shower here
            # metric |r_high - null| vs |r_high - d0| but since same, use variance or just report
            topo_metric = abs(r_high - null_ratio)
            # for D0 same, no improvement assumed unless curve had reco diff (it doesn't strongly)

    # decide
    # if D0 better on delta_loglik >0 (higher lik) or delta_chi2 <0 (lower chi2), and not tiny
    improved = (delta_loglik > 0.1) or (delta_chi2 < -0.1)
    if improved:
        token = PASS_TOKEN
    else:
        token = FAIL_TOKEN

    # write results csv
    with RESULTS_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["bin", "lo", "hi", "obs", "mu_null", "mu_d0", "avg_damp_high", "loglik_null", "loglik_d0"])
        for i, (lo,hi) in enumerate(bins):
            obs_i = sum(1 for e in events if lo <= e["energy"] < hi)
            # rough per bin mu (for display; main is high)
            w.writerow([f"bin{i}", lo, hi, obs_i, "", "", "", "", ""])
        w.writerow(["high_extrap", bins[1][1], edges[-1], k, mu_null, mu_d0, avg_damp, loglik_null, loglik_d0])

    # summary json
    summary = {
        "status": token,
        "events_used": n_events,
        "bins_log10_energy_edges": edges,
        "high_bin_obs": k,
        "mu_null_high": mu_null,
        "mu_d0_high": mu_d0,
        "avg_damping_high": avg_damp,
        "poisson_loglik_null": loglik_null,
        "poisson_loglik_d0": loglik_d0,
        "delta_loglik": delta_loglik,
        "chi2_null_high": chi2_null,
        "chi2_d0_high": chi2_d0,
        "delta_chi2": delta_chi2,
        "topology_ratio_metric": topo_metric,
        "baseline_used": "empirical_no_deco_energy_shape_from_low_mid_extrap",
        "d0_curve": "frozen from vp_neutrino_phason_decoherence_passport --mode hese12",
        "forbidden": ["free damping", "posthoc cuts", "event deletion after result"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    # md
    md = f"""# IceCube HESE Baseline Comparison

**Token:** {token}

**events_used:** {n_events}

**Baseline:** empirical no-deco energy-shape null (low+mid log bins extrapolated to high via power-law alpha)

**D0:** frozen damping curve (avg_damp_high = {avg_damp:.6g})

**Metrics (high bin):**
- obs = {k}
- mu_null = {mu_null:.2f}
- mu_d0 = {mu_d0:.2f}
- delta_loglik = {delta_loglik:.3f}
- delta_chi2 = {delta_chi2:.3f}

**Topology secondary:** {topo_metric}

**Meaning:** { 'D0 damping improves high-energy description over no-deco null extrapolation.' if improved else 'No-deco null (or equivalent) describes high-energy bin as well or better than tiny D0 damping.' }
"""
    SUMMARY_MD.write_text(md, encoding="utf-8")

    print(token)
    print(f"events_used: {n_events}")
    print(f"delta_loglik: {delta_loglik:.4f}")
    print(f"delta_chi2: {delta_chi2:.4f}")
    print(f"avg_damping_high: {avg_damp:.6g}")
    if topo_metric is not None:
        print(f"topology_ratio_metric: {topo_metric:.4f}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
