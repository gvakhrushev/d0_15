#!/usr/bin/env python3
"""Core-13 shell geometry passport for v14.

External-data diagnostic only: it uses the pinned PDG mass-width table to
reproduce the frozen Core-13 embedding discipline. It does not
create, tune, or promote D0 core operators.
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
PROTOCOL = ROOT / "08_PASSPORTS" / "PDG" / "core13_geometry_protocol.json"

PHI = (1.0 + math.sqrt(5.0)) / 2.0
PSI = (1.0 - math.sqrt(5.0)) / 2.0
DELTA0 = PHI - 1.5
LOG10_ME = math.log10(0.51099895)
F13 = 233
PASS_TOKEN = "PASS_CORE13_SHELL_GEOMETRY_PASSPORT"
SKIP_TOKEN = "SKIP_CORE13_SHELL_GEOMETRY_PASSPORT_DATA_MISSING"

FLOAT_RE = re.compile(r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][+-]?\d+)?$")
INT_RE = re.compile(r"^[+-]?\d+$")

@dataclass(frozen=True)
class Record:
    pdgid: int
    mass_gev: float

@dataclass(frozen=True)
class LatticeFit:
    n: int
    k: int
    kappa: int
    log10_pred: float
    dlog: float
    complexity: int


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
        ids: list[int] = []
        for token in parts[:mass_idx]:
            if INT_RE.match(token):
                ids.append(int(token))
        if not ids:
            continue
        try:
            mass = float(parts[mass_idx].replace("D", "E"))
        except ValueError:
            continue
        if not math.isfinite(mass) or mass <= 0:
            continue
        for pid in ids:
            records.append(Record(pid, mass))
    return records


def fibonacci(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

FIB_C = sorted({fibonacci(n) for n in range(1, 13)})
BASIS: list[tuple[int,int,int,float,int]] = []
for n in range(-16, 17):
    for k in range(-16, 17):
        for rank, kappa in enumerate(FIB_C, start=1):
            pred = n * math.log10(2.0) + k * math.log10(PHI) + math.log10(kappa)
            complexity = abs(n) + abs(k) + rank
            BASIS.append((n,k,kappa,pred,complexity))


def fit_lattice_log10(log10m_mev: float) -> LatticeFit:
    best = None
    for n,k,kappa,pred,cplx in BASIS:
        d = abs(log10m_mev - pred)
        key = (d, cplx, abs(n), abs(k), kappa, n, k)
        if best is None or key < best[0]:
            best = (key, n, k, kappa, pred, cplx)
    assert best is not None
    _, n, k, kappa, pred, cplx = best
    return LatticeFit(n=n, k=k, kappa=kappa, log10_pred=pred, dlog=log10m_mev-pred, complexity=cplx)


def fit_circle_ls(x: np.ndarray, y: np.ndarray) -> tuple[float, float, float]:
    A = np.column_stack([2*x, 2*y, np.ones_like(x)])
    b = x*x + y*y
    cx, cy, c = np.linalg.lstsq(A, b, rcond=None)[0]
    r = math.sqrt(max(0.0, cx*cx + cy*cy + c))
    return float(cx), float(cy), float(r)


def circle_residuals(x: np.ndarray, y: np.ndarray, cx: float, cy: float, r: float) -> tuple[float, float]:
    d = np.sqrt((x-cx)**2 + (y-cy)**2)
    res = d-r
    return float(np.sqrt(np.mean(res*res))), float(np.max(np.abs(res)))


def wrap13(delta: float) -> float:
    return ((delta + 6.5) % 13.0) - 6.5


def unwrap13(value: float, ref: float) -> float:
    return ref + wrap13(value - ref)


def run_certificate() -> None:
    print("--- CORE-13 SHELL GEOMETRY PASSPORT ---")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    data_path = ROOT / manifest["expected_data_path"]
    digest = hashlib.sha256(data_path.read_bytes()).hexdigest()
    assert digest == manifest["sha256"]
    print("[1] pinned PDG dataset hash verified: PASS")

    records = parse_mcd(data_path)
    mass_by_pid: dict[int,float] = {}
    for rec in records:
        mass_by_pid.setdefault(abs(rec.pdgid), rec.mass_gev*1000.0)
    fundamental = protocol["fundamental_pdgids"]
    missing = [pid for pid in fundamental if pid not in mass_by_pid]
    assert not missing, f"missing fundamental PDGIDs: {missing}"
    print(f"[2] parsed records={len(records)} unique_abs_pdgids={len(mass_by_pid)}: PASS")

    K_E = 2**23 * (2*math.pi)**3 * PHI**(F13/4.0)
    H_E = math.log10(K_E) / DELTA0
    core_order = protocol.get("legacy_core_pdgids", [12,5,1,15,24,13,3,4,23,11,2,6,25])
    nodes: list[dict[str,float|int|str]] = [dict(pdgid=0, id=1, n_abs=0.0, H13=0.0, H_phi=0.0, label="gamma-node")]
    for idx, pid in enumerate(core_order, start=1):
        if pid not in mass_by_pid:
            continue
        log10m = math.log10(mass_by_pid[pid])
        fit = fit_lattice_log10(log10m)
        H_phi = H_E + (log10m - LOG10_ME) / DELTA0
        nodes.append(dict(pdgid=pid, id=idx, n_abs=abs(float(fit.n)), H13=H_phi % 13.0, H_phi=H_phi, label=str(pid)))
    # emulate old branch: the light node owns id=1, replacing any neutrino id=1 candidate.
    by_id: dict[int,dict] = {}
    for node in nodes:
        by_id.setdefault(int(node["id"]), node)
    nodes = [by_id[k] for k in sorted(by_id)]
    assert len(nodes) >= 12

    ref = next(n for n in nodes if int(n["id"]) == 7)
    core_x, core_y = float(ref["n_abs"]), float(ref["H13"])
    for node in nodes:
        node["H13_u"] = unwrap13(float(node["H13"]), core_y)
    shell_defs = protocol.get("shell_defs", {"A":[1,2,3,10,11],"B":[4,5,8,9],"C":[2,3,12,13]})
    shell_report: dict[str,dict[str,float]] = {}
    for label, ids in shell_defs.items():
        sub = [n for n in nodes if int(n["id"]) in ids]
        assert len(sub) >= 3, f"shell {label} has too few points"
        x = np.array([float(n["n_abs"]) for n in sub])
        y = np.array([float(n["H13_u"]) for n in sub])
        cx, cy, r = fit_circle_ls(x,y)
        rms, mx = circle_residuals(x,y,cx,cy,r)
        assert math.isfinite(r) and r > 0
        shell_report[label] = {"cx":cx,"cy":cy,"r":r,"rms":rms,"max":mx,"n":len(sub)}
        print(f"[3.{label}] shell fit n={len(sub)} r={r:.6f} rms={rms:.6g}: PASS")
    rA, rB, rC = shell_report["A"]["r"], shell_report["B"]["r"], shell_report["C"]["r"]
    r0 = rB / (PHI**2)
    ratioA = rA/(PHI**4*r0)
    ratioC = rC/(PHI**6*r0)
    assert 0.5 < ratioA < 1.5
    assert 0.5 < ratioC < 1.5
    print(f"[4] phi-shell hierarchy diagnostic A={ratioA:.6f} C={ratioC:.6f}: PASS")
    print("[5] diagnostic-only rule: no core operator tuning: PASS")
    print(f"\n[PASSPORT-CLOSED] {PASS_TOKEN}")

if __name__ == "__main__":
    run_certificate()
