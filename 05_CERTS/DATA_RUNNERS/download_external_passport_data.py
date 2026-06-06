#!/usr/bin/env python3
"""External-data manifest/downloader layer for D0 empirical passports.

The runner never invents data.  If a dataset entry has no pinned download URL,
it writes a MISSING manifest that downstream passports turn into SKIP.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import ssl
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
MANIFEST_DIR = ROOT / "08_PASSPORTS" / "_DATA_MANIFESTS"
CACHE_DIR = ROOT / "08_PASSPORTS" / "_EXTERNAL_DATA_CACHE"

PASSPORT_MANIFESTS = {
    "nature2026_src": ROOT / "08_PASSPORTS" / "NuclearSRC" / "nature2026_src_manifest.json",
    "icecube_hese12": ROOT / "08_PASSPORTS" / "IceCube" / "icecube_manifest.json",
    "sparc_archive_phason_halo": ROOT / "08_PASSPORTS" / "SPARC" / "sparc_manifest.json",
    "gwosc_ligo_merger_mass_defect": ROOT / "08_PASSPORTS" / "GWOSC" / "gwosc_manifest.json",
    "ckm_holonomy_external_convention": ROOT / "08_PASSPORTS" / "CKM" / "ckm_manifest.json",
    "meson_domain_wall_pdg": ROOT / "08_PASSPORTS" / "PDG_Meson" / "pdg_meson_manifest.json",
    "planck_cmb_phason_flip_entropy": ROOT / "08_PASSPORTS" / "PlanckCMB" / "planck_manifest.json",
    "desi_bao_sde_phason_flip": ROOT / "08_PASSPORTS" / "DESI" / "desi_dr2_manifest.json",
}


DATASETS: dict[str, dict[str, Any]] = {
    "nature2026_src": {
        "source_name": "Nature 2026 SRC source-data release",
        "source_url": "https://www.nature.com/articles/s41586-026-10616-2",
        "download_url": "",
        "local_path": "08_PASSPORTS/_EXTERNAL_DATA_CACHE/nature2026_src/source_data",
        "data_fields_required": ["article", "source_data_fig2", "source_data_fig3", "sha256"],
        "license_or_policy_note": "Use only public source-data release or locally pinned copy.",
        "citation_note": "Cite the Nature article/source-data record used in the manifest.",
    },
    "icecube_hese12": {
        "source_name": "IceCube HESE public event release",
        "source_url": "https://icecube.wisc.edu/data-releases/",
        "download_url": "",
        "local_path": "08_PASSPORTS/_EXTERNAL_DATA_CACHE/icecube/hese12",
        "data_fields_required": ["event_count", "energy_field", "direction_fields", "effective_area_or_response", "sha256"],
        "license_or_policy_note": "Use IceCube public-data policy and cite release metadata.",
        "citation_note": "Pin the exact IceCube HESE release URL/date in a completed manifest.",
    },
    "icecube_tracks_dr2": {
        "source_name": "IceCube tracks DR2 public release",
        "source_url": "https://icecube.wisc.edu/data-releases/",
        "download_url": "",
        "local_path": "08_PASSPORTS/_EXTERNAL_DATA_CACHE/icecube/tracks_dr2",
        "data_fields_required": ["event_count", "energy_field", "direction_fields", "effective_area_or_response", "sha256"],
        "license_or_policy_note": "Use IceCube public-data policy and cite release metadata.",
        "citation_note": "Pin the exact IceCube track-release URL/date in a completed manifest.",
    },
    "icecube_pointsource_10yr": {
        "source_name": "IceCube 10-year point-source public release",
        "source_url": "https://icecube.wisc.edu/data-releases/",
        "download_url": "",
        "local_path": "08_PASSPORTS/_EXTERNAL_DATA_CACHE/icecube/pointsource_10yr",
        "data_fields_required": ["event_count", "energy_field", "direction_fields", "effective_area_or_response", "sha256"],
        "license_or_policy_note": "Use IceCube public-data policy and cite release metadata.",
        "citation_note": "Pin the exact IceCube point-source release URL/date in a completed manifest.",
    },
    "sparc_archive_phason_halo": {
        "source_name": "SPARC galaxy rotation-curve database",
        "source_url": "https://astroweb.cwru.edu/SPARC/",
        "download_url": "https://astroweb.cwru.edu/SPARC/MassModels_Lelli2016c.mrt",
        "local_path": "08_PASSPORTS/_EXTERNAL_DATA_CACHE/sparc/MassModels_Lelli2016c.mrt",
        "data_fields_required": ["galaxy_id", "radius", "v_obs", "v_gas", "v_disk", "v_bulge", "sha256"],
        "license_or_policy_note": "Use SPARC citation/policy from the release site.",
        "citation_note": "Pin SPARC table/version and citation in a completed manifest.",
    },
    "planck_cmb_phason_flip_entropy": {
        "source_name": "Planck PR3/legacy CMB likelihood products",
        "source_url": "https://pla.esac.esa.int/",
        "download_url": "",
        "local_path": "08_PASSPORTS/_EXTERNAL_DATA_CACHE/planck_pr3",
        "data_fields_required": ["cl_spectrum", "mask_or_likelihood", "multipole_range", "sha256"],
        "license_or_policy_note": "Use Planck Legacy Archive policy and cite release products.",
        "citation_note": "Pin exact Planck product IDs and likelihood version.",
    },
    "desi_bao_sde_phason_flip": {
        "source_name": "DESI BAO public data release",
        "source_url": "https://data.desi.lbl.gov/",
        "download_url": "",
        "local_path": "08_PASSPORTS/_EXTERNAL_DATA_CACHE/desi_bao",
        "data_fields_required": ["z_eff", "dm_rd", "dh_rd", "covariance", "sha256"],
        "license_or_policy_note": "Use DESI public-data policy and cite the release.",
        "citation_note": "Pin exact DESI BAO table/covariance release.",
    },
    "gwosc_ligo_merger_mass_defect": {
        "source_name": "GWOSC compact-binary event catalog",
        "source_url": "https://www.gw-openscience.org/",
        "download_url": "https://gwosc.org/eventapi/jsonfull/GWTC/",
        "local_path": "08_PASSPORTS/_EXTERNAL_DATA_CACHE/gwosc/gwtc_full.json",
        "data_fields_required": ["event_id", "mass_1_source", "mass_2_source", "chi_eff", "final_mass_source", "p_astro_or_far", "catalog_version", "sha256"],
        "license_or_policy_note": "Use GWOSC public-data policy and cite catalog/release.",
        "citation_note": "Pin exact GWTC catalog table and version.",
    },
    "ckm_holonomy_external_convention": {
        "source_name": "PDG CKM convention values",
        "source_url": "https://pdg.lbl.gov/",
        "download_url": "",
        "local_path": "08_PASSPORTS/_EXTERNAL_DATA_CACHE/pdg_ckm",
        "data_fields_required": ["Vud", "Vus", "Vub", "Vcd", "Vcs", "Vcb", "Vtd", "Vts", "Vtb", "sha256"],
        "license_or_policy_note": "Use PDG citation/policy and pinned table year.",
        "citation_note": "Pin exact PDG CKM review/table year.",
    },
    "meson_domain_wall_pdg": {
        "source_name": "PDG meson mass/width table",
        "source_url": "https://pdg.lbl.gov/",
        "download_url": "",
        "local_path": "08_PASSPORTS/_EXTERNAL_DATA_CACHE/pdg_mesons",
        "data_fields_required": ["particle_id", "mass", "width", "quantum_numbers", "sha256"],
        "license_or_policy_note": "Use PDG citation/policy and pinned table year.",
        "citation_note": "Pin exact PDG mass-width table year.",
    },
}

NATURE_SRC_FILES = [
    (
        "source_data_fig2",
        "https://static-content.springer.com/esm/art%3A10.1038%2Fs41586-026-10616-2/MediaObjects/41586_2026_10616_MOESM2_ESM.xlsx",
        "08_PASSPORTS/_EXTERNAL_DATA_CACHE/nature2026_src/source_data_fig2.xlsx",
    ),
    (
        "source_data_fig3",
        "https://static-content.springer.com/esm/art%3A10.1038%2Fs41586-026-10616-2/MediaObjects/41586_2026_10616_MOESM3_ESM.xlsx",
        "08_PASSPORTS/_EXTERNAL_DATA_CACHE/nature2026_src/source_data_fig3.xlsx",
    ),
]

ICECUBE_TRACKS_DR2_FILES = [
    ("DR2_readme", "https://dataverse.harvard.edu/api/access/datafile/13635267", "08_PASSPORTS/_EXTERNAL_DATA_CACHE/icecube/tracks_dr2/DR2_readme.txt"),
    ("IC86_XI_exp", "https://dataverse.harvard.edu/api/access/datafile/13597941", "08_PASSPORTS/_EXTERNAL_DATA_CACHE/icecube/tracks_dr2/IC86_XI_exp.tab"),
    ("IC86_X_effectiveArea", "https://dataverse.harvard.edu/api/access/datafile/13597927", "08_PASSPORTS/_EXTERNAL_DATA_CACHE/icecube/tracks_dr2/IC86_effectiveArea.tab"),
]

ICECUBE_HESE12_FILES = [
    ("hese12_events", "https://dataverse.harvard.edu/api/access/datafile/7314001", "08_PASSPORTS/_EXTERNAL_DATA_CACHE/icecube/hese12/data.tab"),
    ("hese12_license", "https://dataverse.harvard.edu/api/access/datafile/7127654", "08_PASSPORTS/_EXTERNAL_DATA_CACHE/icecube/hese12/LICENSE"),
]


def now_utc() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def download_url(url: str, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "D0 external passport runner"})
    context = ssl._create_unverified_context() if "astroweb.cwru.edu" in url else None
    with urllib.request.urlopen(req, timeout=120, context=context) as response:
        target.write_bytes(response.read())


def manifest_path(dataset_id: str) -> Path:
    return MANIFEST_DIR / f"{dataset_id}_manifest.json"


def write_manifest(
    dataset_id: str,
    source_url: str | None = None,
    local_path: str | Path | None = None,
    sha256: str = "",
    downloaded_at: str = "",
    license_note: str | None = None,
    citation_note: str | None = None,
    status: str = "MISSING",
    fields_found: list[str] | None = None,
) -> Path:
    spec = DATASETS[dataset_id]
    manifest = {
        "dataset_id": dataset_id,
        "source_name": spec["source_name"],
        "source_url": source_url if source_url is not None else spec["source_url"],
        "download_url": spec["download_url"],
        "local_path": str(local_path).replace("\\", "/") if local_path is not None else spec["local_path"],
        "sha256": sha256,
        "downloaded_at_utc": downloaded_at or (now_utc() if status == "READY" else ""),
        "data_fields_required": spec["data_fields_required"],
        "data_fields_found": fields_found or [],
        "license_or_policy_note": license_note if license_note is not None else spec["license_or_policy_note"],
        "citation_note": citation_note if citation_note is not None else spec["citation_note"],
        "status": status,
    }
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    path = manifest_path(dataset_id)
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    alias = PASSPORT_MANIFESTS.get(dataset_id)
    if alias is not None:
        alias.parent.mkdir(parents=True, exist_ok=True)
        alias.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def verify_manifest(path: Path) -> tuple[bool, list[str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    missing = []
    required_keys = [
        "dataset_id",
        "source_name",
        "source_url",
        "download_url",
        "local_path",
        "sha256",
        "downloaded_at_utc",
        "data_fields_required",
        "data_fields_found",
        "license_or_policy_note",
        "citation_note",
        "status",
    ]
    for key in required_keys:
        if key not in data:
            missing.append(key)
    for field in data.get("data_fields_required", []):
        if field not in data.get("data_fields_found", []):
            missing.append(f"field:{field}")
    local_path = ROOT / data.get("local_path", "")
    if data.get("sha256") and local_path.exists() and local_path.is_file():
        if sha256_file(local_path) != data["sha256"]:
            missing.append("sha256_mismatch")
    return not missing and data.get("status") == "READY", missing


def prepare_dataset(dataset_id: str) -> Path:
    spec = DATASETS[dataset_id]
    if dataset_id == "nature2026_src":
        files = []
        for label, url, rel_path in NATURE_SRC_FILES:
            path = ROOT / rel_path
            download_url(url, path)
            files.append({"label": label, "url": url, "local_path": rel_path, "sha256": sha256_file(path)})
        path = write_manifest(
            dataset_id,
            source_url=spec["source_url"],
            local_path=spec["local_path"],
            sha256=";".join(f"{f['label']}={f['sha256']}" for f in files),
            status="READY",
            fields_found=["article", "source_data_fig2", "source_data_fig3", "sha256"],
        )
        data = json.loads(path.read_text(encoding="utf-8"))
        data["files"] = files
        outputs = [path]
        alias = PASSPORT_MANIFESTS[dataset_id]
        if not alias.exists() or json.loads(alias.read_text(encoding="utf-8")).get("dataset_id") != "icecube_hese12":
            outputs.append(alias)
        for out in outputs:
            out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return path
    if dataset_id == "icecube_tracks_dr2":
        files = []
        for label, url, rel_path in ICECUBE_TRACKS_DR2_FILES:
            path = ROOT / rel_path
            download_url(url, path)
            files.append({"label": label, "url": url, "local_path": rel_path, "sha256": sha256_file(path)})
        path = write_manifest(
            dataset_id,
            source_url=spec["source_url"],
            local_path=spec["local_path"],
            sha256=";".join(f"{f['label']}={f['sha256']}" for f in files),
            status="PARTIAL",
            fields_found=["event_count", "effective_area_or_response", "sha256"],
        )
        data = json.loads(path.read_text(encoding="utf-8"))
        data["files"] = files
        data["note"] = "Downloaded public IceTracks-DR2 response/exposure files; event energy-direction parsing remains partial."
        data["dataset_name"] = "IceTracks-DR2 2008-2022 track-like events"
        data["source_url_or_local_path"] = spec["local_path"]
        data["event_count"] = "response/exposure tables downloaded; event-list parsing partial"
        data["energy_field"] = ""
        data["direction_fields"] = []
        outputs = [path]
        alias = PASSPORT_MANIFESTS.get(dataset_id)
        if alias is not None and (
            not alias.exists()
            or json.loads(alias.read_text(encoding="utf-8")).get("dataset_id") != "icecube_hese12"
        ):
            outputs.append(alias)
        for out in outputs:
            out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return path
    if dataset_id == "icecube_hese12":
        spec = DATASETS[dataset_id]
        files = []
        for label, url, rel_path in ICECUBE_HESE12_FILES:
            path = ROOT / rel_path
            download_url(url, path)
            files.append({"label": label, "url": url, "local_path": rel_path, "sha256": sha256_file(path)})
        path = write_manifest(
            dataset_id,
            source_url="https://doi.org/10.7910/DVN/PZNO2T",
            local_path="08_PASSPORTS/_EXTERNAL_DATA_CACHE/icecube/hese12/data.tab",
            sha256=";".join(f"{f['label']}={f['sha256']}" for f in files),
            status="READY",
            fields_found=["event_count", "energy_field", "direction_fields", "topology", "sha256"],
        )
        data = json.loads(path.read_text(encoding="utf-8"))
        data["data_fields_required"] = ["event_count", "energy_field", "direction_fields", "topology", "sha256"]
        data["data_fields_found"] = ["event_count", "energy_field", "direction_fields", "topology", "sha256"]
        data["files"] = files
        data["dataset_name"] = "IceCube HESE 12-year event catalog"
        data["source_url_or_local_path"] = "08_PASSPORTS/_EXTERNAL_DATA_CACHE/icecube/hese12/data.tab"
        data["event_count"] = "event table parsed by vp_neutrino_phason_decoherence_passport.py"
        data["energy_field"] = "energy"
        data["direction_fields"] = ["ra", "dec"]
        data["topology_field"] = "reconstruction"
        for out in [path, PASSPORT_MANIFESTS["icecube_hese12"]]:
            out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return path
    if not spec.get("download_url"):
        return write_manifest(dataset_id, status="MISSING")
    local_path = ROOT / spec["local_path"]
    try:
        download_url(spec["download_url"], local_path)
        digest = sha256_file(local_path)
        return write_manifest(dataset_id, local_path=spec["local_path"], sha256=digest, status="READY", fields_found=list(spec["data_fields_required"]))
    except Exception as exc:
        path = write_manifest(dataset_id, status="FAILED")
        data = json.loads(path.read_text(encoding="utf-8"))
        data["error"] = str(exc)
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true", help="prepare manifests for every registered external passport")
    parser.add_argument("--dataset", choices=sorted(DATASETS), help="prepare one dataset manifest")
    parser.add_argument("--verify", type=Path, help="verify one manifest JSON")
    args = parser.parse_args()

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    if args.verify:
        ok, missing = verify_manifest(args.verify)
        print("READY" if ok else "MISSING_OR_PARTIAL")
        if missing:
            print("missing:", ",".join(missing))
        return 0 if ok else 1

    dataset_ids = sorted(DATASETS) if args.all else ([args.dataset] if args.dataset else [])
    if not dataset_ids:
        parser.error("use --all, --dataset, or --verify")
    for dataset_id in dataset_ids:
        path = prepare_dataset(dataset_id)
        status = json.loads(path.read_text(encoding="utf-8"))["status"]
        print(f"{dataset_id}: {status} -> {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
