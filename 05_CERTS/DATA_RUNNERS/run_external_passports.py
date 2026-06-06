#!/usr/bin/env python3
"""Run the D0 external-data passport suite and write a summary table."""
from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
RESULT_DIR = ROOT / "08_PASSPORTS" / "_RESULTS"


@dataclass(frozen=True)
class PassportRun:
    passport: str
    dataset: str
    command: list[str]
    manifest: str
    frozen_d0_object: str
    baseline: str
    metric: str


RUNS = [
    PassportRun(
        "Nuclear shell-contact SRC",
        "nature2026_src",
        ["05_CERTS/vp_nuclear_shell_contact_src.py", "--mode", "nature2026_source_data"],
        "08_PASSPORTS/NuclearSRC/nature2026_src_manifest.json",
        "same-shell proton-neutron contact selector",
        "A-only / N-Z-only / density proxy",
        "source-data rank ordering",
    ),
    PassportRun(
        "LIGO merger mass defect - all catalog",
        "gwosc_ligo_merger_mass_defect",
        ["05_CERTS/vp_ligo_merger_mass_defect_current_catalog.py", "--mode", "all_catalog_run"],
        "08_PASSPORTS/GWOSC/gwosc_manifest.json",
        "finite merger mass-defect operator",
        "mean loss / spin-only negative control",
        "RMSE on all complete catalog rows",
    ),
    PassportRun(
        "LIGO merger mass defect - clean BBH",
        "gwosc_ligo_merger_mass_defect",
        ["05_CERTS/vp_ligo_merger_mass_defect_current_catalog.py", "--mode", "clean_BBH_run"],
        "08_PASSPORTS/GWOSC/gwosc_manifest.json",
        "finite merger mass-defect operator",
        "mean loss / spin-only negative control",
        "RMSE on clean BBH domain",
    ),
    PassportRun(
        "SPARC data ingest",
        "sparc_archive_phason_halo",
        ["05_CERTS/vp_archive_phason_halo_passport.py", "--mode", "sparc"],
        "08_PASSPORTS/SPARC/sparc_manifest.json",
        "SPARC mass-model data contract",
        "manifest/hash/table parser",
        "rows and galaxies parsed",
    ),
    PassportRun(
        "SPARC shape_only kernel",
        "sparc_archive_phason_halo",
        ["05_CERTS/vp_archive_phason_halo_passport.py", "--mode", "shape_only"],
        "08_PASSPORTS/SPARC/sparc_manifest.json",
        "naive inner-memory archive-phason kernel",
        "baryon-only residual shape",
        "per-galaxy normalized shape correlation",
    ),
    PassportRun(
        "SPARC one_global_scale kernel",
        "sparc_archive_phason_halo",
        ["05_CERTS/vp_archive_phason_halo_passport.py", "--mode", "one_global_scale"],
        "08_PASSPORTS/SPARC/sparc_manifest.json",
        "naive inner-memory archive-phason kernel with one global scale",
        "baryon-only residual",
        "global RMSE reduction",
    ),
    PassportRun(
        "IceCube HESE phason decoherence",
        "icecube_hese12",
        ["05_CERTS/vp_icecube_hese_baseline_comparison.py"],
        "08_PASSPORTS/IceCube/icecube_manifest.json",
        "Hurwitz phason decoherence kernel",
        "no-decoherence baseline protocol",
        "HESE event curve generated; baseline statistic required",
    ),
    PassportRun(
        "CMB phason flip entropy",
        "planck_cmb_phason_flip_entropy",
        ["05_CERTS/vp_cmb_phason_flip_entropy_passport.py", "--mode", "planck_pr3"],
        "08_PASSPORTS/PlanckCMB/planck_manifest.json",
        "phason-flip entropy operator",
        "LambdaCDM-only residual null",
        "multipole entropy residual",
    ),
    PassportRun(
        "BAO S_DE phason flip",
        "desi_bao_sde_phason_flip",
        ["05_CERTS/vp_bao_sde_phason_flip_passport.py", "--mode", "desi_dr2"],
        "08_PASSPORTS/DESI/desi_dr2_manifest.json",
        "S_DE phason-flip archive transfer",
        "constant-shape BAO baseline",
        "BAO residual/covariance response",
    ),
    PassportRun(
        "CKM holonomy external convention",
        "ckm_holonomy_external_convention",
        ["05_CERTS/vp_ckm_holonomy_external_convention_passport.py", "--mode", "pdg"],
        "08_PASSPORTS/CKM/ckm_manifest.json",
        "CKM phason holonomy matrix convention",
        "PDG convention table",
        "unitarity/convention residual",
    ),
    PassportRun(
        "Meson domain-wall PDG",
        "meson_domain_wall_pdg",
        ["05_CERTS/vp_meson_domain_wall_pdg_passport.py", "--mode", "pdg"],
        "08_PASSPORTS/PDG_Meson/pdg_meson_manifest.json",
        "meson phason domain-wall selector",
        "PDG mass-width table",
        "domain-wall class residual",
    ),
]


def extract_result(stdout: str, returncode: int) -> str:
    for token in stdout.split():
        if token.startswith(("PASS_", "FAIL_", "SKIP_")):
            return token
    if returncode != 0:
        return "FAIL_EXTERNAL_PASSPORT_RUNNER_COMMAND"
    return "UNKNOWN_EXTERNAL_PASSPORT_RESULT"


def manifest_hash(path: Path) -> str:
    if not path.exists():
        return "missing"
    import hashlib

    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def run_one(spec: PassportRun) -> dict[str, Any]:
    proc = subprocess.run(
        [sys.executable, *spec.command],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=120,
    )
    stdout = proc.stdout.strip()
    stderr = proc.stderr.strip()
    manifest_path = ROOT / spec.manifest
    result = extract_result(stdout, proc.returncode)
    notes = stdout.splitlines()[-1] if stdout else stderr.splitlines()[-1] if stderr else ""
    return {
        "Passport": spec.passport,
        "Dataset": spec.dataset,
        "Manifest": spec.manifest,
        "Hash": manifest_hash(manifest_path),
        "Frozen D0 object": spec.frozen_d0_object,
        "Baseline": spec.baseline,
        "Metric": spec.metric,
        "Result": result,
        "Notes": notes,
        "returncode": proc.returncode,
        "stdout": stdout,
        "stderr": stderr,
    }


def markdown_table(rows: list[dict[str, Any]]) -> str:
    columns = ["Passport", "Dataset", "Manifest", "Hash", "Frozen D0 object", "Baseline", "Metric", "Result", "Notes"]
    out = ["# D0 External Passport Summary", ""]
    pass_rows = [r for r in rows if str(r["Result"]).startswith("PASS_")]
    fail_rows = [r for r in rows if str(r["Result"]).startswith("FAIL_")]
    skip_rows = [r for r in rows if str(r["Result"]).startswith("SKIP_")]
    pass_names = [f"{r['Passport']}: {r['Result']}" for r in pass_rows]
    fail_names = [f"{r['Passport']}: {r['Result']}" for r in fail_rows]
    skip_names = [f"{r['Passport']}: {r['Result']}" for r in skip_rows]
    out.extend([
        "## Counters",
        "",
        f"- PASS: {len(pass_rows)}",
        f"- FAIL: {len(fail_rows)}",
        f"- SKIP: {len(skip_rows)}",
        "",
        "PASS rows:",
        *[f"- {name}" for name in pass_names],
        "",
        "FAIL rows:",
        *[f"- {name}" for name in fail_names],
        "",
        "SKIP rows:",
        *[f"- {name}" for name in skip_names],
        "",
        "SPARC data ingest PASS is a data-ingest PASS only, not a physics PASS.",
        "",
    ])
    out.append("| " + " | ".join(columns) + " |")
    out.append("| " + " | ".join(["---"] * len(columns)) + " |")
    for row in rows:
        values = []
        for col in columns:
            value = str(row[col]).replace("|", "\\|").replace("\n", " ")
            if col == "Hash" and len(value) > 16:
                value = value[:16]
            values.append(value)
        out.append("| " + " | ".join(values) + " |")
    out.append("")
    out.append("PASS means a pinned external-data manifest was complete and the declared comparison executed. SKIP means either source data are incomplete or the observable baseline/kernel comparison is not implemented yet; see Notes.")
    return "\n".join(out) + "\n"


def main() -> int:
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    rows = [run_one(spec) for spec in RUNS]
    summary = {
        "status": "EXTERNAL_PASSPORT_SUMMARY",
        "counters": {
            "PASS": [r["Passport"] for r in rows if str(r["Result"]).startswith("PASS_")],
            "FAIL": [r["Passport"] for r in rows if str(r["Result"]).startswith("FAIL_")],
            "SKIP": [r["Passport"] for r in rows if str(r["Result"]).startswith("SKIP_")],
            "sparc_data_ingest_is_physics_pass": False,
        },
        "rows": rows,
    }
    (RESULT_DIR / "external_passport_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (RESULT_DIR / "external_passport_summary.md").write_text(markdown_table(rows), encoding="utf-8")
    for row in rows:
        print(f"{row['Passport']}: {row['Result']}")
    return 1 if any(row["returncode"] != 0 for row in rows) else 0


if __name__ == "__main__":
    raise SystemExit(main())
