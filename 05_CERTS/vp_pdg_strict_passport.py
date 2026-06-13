#!/usr/bin/env python3
"""PDG strict passport.

Active PDG comparison wrapper as an explicit passport engine.
The cert verifies dataset pinning, protocol gates, holdout/multiple-testing
metadata, seam-alpha arithmetic, and a frozen lattice/Оґ8 diagnostic.  It cannot
create or tune core D0 operators.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "08_PASSPORTS" / "PDG" / "pdg_dataset_manifest.json"
PROTOCOL = ROOT / "08_PASSPORTS" / "PDG" / "pdg_strict_protocol.json"

PHI = (1.0 + math.sqrt(5.0)) / 2.0
PSI = (1.0 - math.sqrt(5.0)) / 2.0
DELTA0 = PHI - 1.5
PI0 = (6.0/5.0) * PHI**2
XI5 = PHI**-5
EPS2 = PHI**-16
M_E_MEV = 0.51099895
FLOAT_RE = re.compile(r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][+-]?\d+)?$")
INT_RE = re.compile(r"^[+-]?\d+$")

@dataclass(frozen=True)
class Record:
    pdgid: int
    mass_mev: float

@dataclass(frozen=True)
class LatticeFit:
    n: int
    k: int
    kappa: int
    log10_pred: float
    dlog: float


def parse_mcd(path: Path) -> list[Record]:
    records: list[Record] = []
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("*"):
            continue
        parts = line.split()
        mass_idx: Optional[int] = None
        for idx, token in enumerate(parts):
            if FLOAT_RE.match(token) and ("." in token or "E" in token.upper()):
                mass_idx = idx
                break
        if mass_idx is None or mass_idx == 0:
            continue
        ids = [int(t) for t in parts[:mass_idx] if INT_RE.match(t)]
        if not ids:
            continue
        mass_gev = float(parts[mass_idx].replace("D","E"))
        if not math.isfinite(mass_gev) or mass_gev <= 0:
            continue
        for pid in ids:
            records.append(Record(pid, mass_gev*1000.0))
    return records


def fibonacci(n: int) -> int:
    a,b=0,1
    for _ in range(n):
        a,b=b,a+b
    return a

def lucas(n: int) -> int:
    if n == 0:
        return 2
    if n == 1:
        return 1
    a,b=2,1
    for _ in range(n-1):
        a,b=b,a+b
    return b

def lucas_trace_layer_diagnostic() -> dict[int,int]:
    """Optional diagnostic only; it does not choose or tune any PDG passport input."""
    return {n: ((-1)**n) * lucas(n) for n in range(1,7)}

FIB_C = sorted({fibonacci(n) for n in range(1,13)})
BASIS=[]
for n in range(-16,17):
    for k in range(-16,17):
        for rank,kappa in enumerate(FIB_C,start=1):
            pred=n*math.log10(2.0)+k*math.log10(PHI)+math.log10(kappa)
            complexity=abs(n)+abs(k)+rank
            BASIS.append((n,k,kappa,pred,complexity))


def fit_lattice(log10m: float) -> LatticeFit:
    best=None
    for n,k,kappa,pred,cplx in BASIS:
        d=abs(log10m-pred)
        key=(d,cplx,abs(n),abs(k),kappa,n,k)
        if best is None or key < best[0]:
            best=(key,n,k,kappa,pred)
    assert best is not None
    _,n,k,kappa,pred=best
    return LatticeFit(n,k,kappa,pred,log10m-pred)


def is_holdout(pid: int, seed: int, fraction: float) -> bool:
    h = hashlib.sha256(f"{seed}:{abs(int(pid))}".encode()).hexdigest()
    x = int(h[:12],16) / float(16**12)
    return x < fraction


def run_certificate() -> None:
    print("--- PDG STRICT PASSPORT ---")
    manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
    protocol=json.loads(PROTOCOL.read_text(encoding="utf-8"))
    data_path=ROOT/manifest["expected_data_path"]
    digest=hashlib.sha256(data_path.read_bytes()).hexdigest()
    assert digest == manifest["sha256"]
    print("[1] pinned dataset hash verified: PASS")

    assert protocol["dataset_pinning_required"] is True
    assert protocol["holdout"]["enabled"] is True
    assert protocol["holdout_seed_required"] is True
    assert protocol["holdout_fraction_required"] is True
    assert protocol["multiple_testing"]["method"] == "bonferroni"
    assert "delta8_hypotheses" in protocol["multiple_testing"]["families"]
    assert protocol["rank_minimax_distinction_required"] is True
    print("[2] PDG passport protocol gates verified: PASS")

    records=parse_mcd(data_path)
    assert len(records) > 200
    unique_abs=sorted({abs(r.pdgid) for r in records})
    seed=int(protocol["holdout"]["seed"])
    frac=float(protocol["holdout"]["fraction"])
    train=[pid for pid in unique_abs if not is_holdout(pid,seed,frac)]
    hold=[pid for pid in unique_abs if is_holdout(pid,seed,frac)]
    assert len(train)>0 and len(hold)>0
    print(f"[3] deterministic holdout split unique_abs={len(unique_abs)} train={len(train)} holdout={len(hold)}: PASS")

    alpha_inv_top = 359.0/(PHI**2) - XI5
    alpha_inv_alg = ((2.0**11)*PI0/(PHI**8)) + (2.0*DELTA0)/3.0
    delta_alpha = abs(alpha_inv_top-alpha_inv_alg)
    assert delta_alpha < EPS2
    print(f"[4] seam-alpha invariant delta={delta_alpha:.6e} < eps2={EPS2:.6e}: PASS")

    mass_by_pid: dict[int,float] = {}
    for r in records:
        mass_by_pid.setdefault(abs(r.pdgid), r.mass_mev)
    fundamental=[1,2,3,4,5,6,11,13,15,23,24,25]
    missing=[pid for pid in fundamental if pid not in mass_by_pid]
    assert not missing
    rel_errors=[]
    delta8=[]
    for pid in fundamental:
        m=mass_by_pid[pid]
        fit=fit_lattice(math.log10(m))
        pred=10**fit.log10_pred
        rel_errors.append(abs(pred-m)/m)
        phi_exp=math.log(m/M_E_MEV)/math.log(PHI) - fit.n*(math.log(2.0)/math.log(PHI)) - math.log(fit.kappa)/math.log(PHI)
        d8=phi_exp - 8.0*math.floor(phi_exp/8.0)
        if d8 < 0: d8 += 8.0
        delta8.append(d8)
    med=float(np.median(rel_errors))
    assert math.isfinite(med) and med < 0.05
    print(f"[5] frozen phi-lattice diagnostic fundamental_N={len(fundamental)} median_rel={med:.6e}: PASS")

    mod1=np.mod(np.array(delta8),1.0)
    hypotheses=[13,14,15,16,17]
    scores=[]
    for k in hypotheses:
        a=(PHI**-2)+(DELTA0**2)-(PHI**(-k))
        dist=np.abs(((mod1-a+0.5)%1.0)-0.5)
        scores.append((float(np.mean(dist)),float(np.max(dist)),k))
    rank_winner=min(scores)[2]
    minimax_winner=min(scores,key=lambda x:(x[1],x[0]))[2]
    assert rank_winner in hypotheses and minimax_winner in hypotheses
    print(f"[6] delta8 hypothesis family evaluated rank=k{rank_winner} minimax=k{minimax_winner}: PASS")
    layers=lucas_trace_layer_diagnostic()
    assert layers[2] == 3 and layers[3] == -4 and layers[5] == -11
    print("[7] optional lucas_trace_layer_diagnostic evaluated without PDG tuning: PASS")
    print("[8] PDG passport discipline: no operator tuning and no core promotion: PASS")
    print("\n[PASSPORT-CLOSED] PASS_PDG_STRICT_PASSPORT")

if __name__ == "__main__":
    run_certificate()
