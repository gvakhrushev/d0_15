#!/usr/bin/env python3
from __future__ import annotations

import csv
import html
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLAIM_MAP = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"
ASSUMPTION_LEDGER = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "LEAN_ASSUMPTION_LEDGER.csv"
THEORY_DIR = ROOT / "03_THEORY_MAP"
LEAN_INDEX = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "LEAN_CORE_THEOREM_INDEX.md"
SEMANTIC_INDEX = THEORY_DIR / "theory_semantic_index.md"
FRONTIER_RELEASE_STATUSES = {
    "FRONTIER",
    "PROOF-TARGET",
    "CERT-CANDIDATE",
    "OPERATOR-SCAFFOLD-COMPLETE",
    "OPERATOR-SCAFFOLD-CERTIFIED",
    "SPIN-FLAVOUR-TRANSFER-CERTIFIED",
    "EMPIRICAL-PASSPORT-CANDIDATE",
    "LOWER-BOUND-TARGET",
    "THEOREM-TARGET-SHARPENED",
    "PROOF-OBLIGATION-EXPOSED",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def split_values(value: str) -> list[str]:
    return [part.strip() for part in value.replace(",", ";").split(";") if part.strip()]


def claim_text(row: dict[str, str]) -> str:
    fields = [
        "claim_id",
        "book",
        "section",
        "lean_module",
        "lean_theorem",
        "lean_status",
        "release_status",
        "notes",
        "assumption_ids",
        "python_cert",
    ]
    parts = [str(row.get(field) or "") for field in fields]
    return " ".join(parts).lower()


def text_tokens(text: str) -> set[str]:
    normalized = "".join(ch.lower() if ch.isalnum() else " " for ch in text)
    return {part for part in normalized.split() if part}


def claim_domain(row: dict[str, str]) -> str:
    text = claim_text(row)
    tokens = text_tokens(text)
    release = row["release_status"]

    if release in FRONTIER_RELEASE_STATUSES:
        return "frontier"
    if row["release_status"] == "EXTERNAL-BACKGROUND" or "external background" in text:
        return "external_background"
    if "interpretation spine" in text or "interpretation package" in text:
        return "interpretation_spine"
    if "si" in tokens and "calibration" in tokens:
        return "si_calibration"
    if "rg" in tokens or "renormal" in text or "renormalization" in text:
        return "rg"
    if "smooth" in tokens or "continuum" in tokens:
        return "smooth_geometry"
    if (
        "cosmo" in text
        or "cosmology" in tokens
        or "friedmann" in tokens
        or "underdensity" in tokens
        or "underdense" in tokens
    ):
        return "cosmology"
    if "spectral action" in text or ("spectral" in tokens and "action" in tokens) or "heat trace" in text:
        return "spectral_action"
    if any(term in tokens for term in {"empirical", "observational", "qnm", "bao", "pdg", "desi", "pantheon"}):
        return "empirical_passport"
    if "likelihood" in tokens and ("passport" in tokens or "external" in tokens):
        return "empirical_passport"
    if "yang" in tokens or "killing" in tokens or "gauge" in tokens:
        return "gauge_bridge"
    return "formal_core"


def claim_type(row: dict[str, str]) -> str:
    release = row["release_status"]
    lean = row["lean_status"]
    if release in FRONTIER_RELEASE_STATUSES:
        return "frontier"
    if release == "DEPRECATED" or lean == "DEPRECATED":
        return "deprecated"
    if release.startswith("NO-GO") or release == "NO_GO_PROVED":
        return "no-go"
    if release == "BRIDGE-CALIBRATION":
        return "bridge"
    if release == "CORE_BRIDGE_SPLIT":
        return "bridge"
    if release == "CERT-CLOSED" or lean == "PYTHON_CERTIFIED":
        return "certificate"
    if row["uses_bridge_assumptions"].lower() == "true" or release.startswith("BRIDGE"):
        return "bridge"
    if release == "EXTERNAL-BACKGROUND":
        return "external"
    return "core"


def scope_guard(row: dict[str, str]) -> str:
    ctype = claim_type(row)
    domain = claim_domain(row)
    if row["release_status"] == "BRIDGE-CALIBRATION":
        return "Bridge-calibration row; SI or dimensional interpretation requires an explicit external calibration object."
    if row["release_status"] == "CORE_BRIDGE_SPLIT":
        return "Core/bridge split row; the formal spine is proved while physical coherence remains an explicit package."
    if ctype == "deprecated":
        return "Deprecated or historical row; not a live promotion path."
    if ctype == "external":
        return "External background only; not an active D0-core dependency."
    if ctype == "no-go":
        return "Boundary/no-go row; prevents promotion of this route."
    if ctype == "certificate":
        return "Certificate-bounded row; valid only for declared finite inputs and negative controls."
    if ctype == "bridge":
        return "Conditional bridge row; not a D0-core closure without listed assumptions."
    if ctype == "frontier":
        return "Frontier/proof-target row; not a core closure, certificate pass or empirical passport."
    if domain == "rg":
        return "Formal/finite RG proxy only; smooth or physical RG meaning requires explicit bridge assumptions."
    if domain == "si_calibration":
        return "D0 core is dimensionless; SI constants require an explicit ExternalSICalibration bridge."
    if domain == "cosmology":
        return "Formal finite cosmology shape statement; not an observational cosmology fit without certificate/passport data."
    if domain == "spectral_action":
        return "Finite spectral-action or heat-trace statement; no continuum Einstein-Hilbert promotion by default."
    if domain == "smooth_geometry":
        return "Finite/symbolic smooth-geometry proxy; continuum covariance requires declared bridge assumptions."
    if domain == "empirical_passport":
        return "Passport or empirical interface row; not a D0-core theorem without external data discipline."
    if domain == "gauge_bridge":
        return "Gauge-sector statement; physical Yang-Mills interpretation remains bridge-scoped when assumptions appear."
    return "Lean-owned finite/formal D0 core statement."


def module_path(module: str) -> Path:
    return ROOT / "09_LEAN_FORMALIZATION" / (module.replace(".", "/") + ".lean")


def modules_exist(lean_module: str) -> bool:
    # A row may list several semicolon/comma-separated modules; all must resolve.
    mods = split_values(lean_module)
    return bool(mods) and all(module_path(m).exists() for m in mods)


_CERT_INDEX: dict[str, Path] | None = None


def _cert_index() -> dict[str, Path]:
    # basename -> path for every cert under 05_CERTS (incl. ported_legacy_primary/).
    global _CERT_INDEX
    if _CERT_INDEX is None:
        _CERT_INDEX = {}
        for p in (ROOT / "05_CERTS").rglob("*.py"):
            _CERT_INDEX.setdefault(p.name, p)
    return _CERT_INDEX


def cert_path(cert: str) -> Path:
    # Some rows already prefix the cert with "05_CERTS/"; strip it to avoid 05_CERTS/05_CERTS/.
    cert = cert.strip().replace("\\", "/")
    if cert.startswith("05_CERTS/"):
        cert = cert[len("05_CERTS/"):]
    direct = ROOT / "05_CERTS" / cert
    if direct.exists():
        return direct
    # Fallback: locate by basename anywhere under 05_CERTS (e.g. ported_legacy_primary/<ID>/).
    return _cert_index().get(Path(cert).name, direct)


def dot_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def write_json(claims: list[dict[str, str]], assumptions: list[dict[str, str]]) -> None:
    assumption_by_id = {row["assumption_id"]: row for row in assumptions}
    nodes: list[dict[str, object]] = []
    edges: list[dict[str, str]] = []

    for row in claims:
        claim_id = row["claim_id"]
        assumption_ids = split_values(row["assumption_ids"])
        certs = split_values(row["python_cert"])
        mods = split_values(row["lean_module"])
        mpath = module_path(mods[0]) if mods else module_path(row["lean_module"])
        mexists = modules_exist(row["lean_module"])
        ctype = claim_type(row)
        domain = claim_domain(row)

        nodes.append(
            {
                "id": claim_id,
                "kind": "claim",
                "claim_id": claim_id,
                "type": ctype,
                "domain": domain,
                "scope_guard": scope_guard(row),
                "book": row["book"],
                "section": row["section"],
                "lean_module": row["lean_module"],
                "lean_theorem": row["lean_theorem"],
                "lean_status": row["lean_status"],
                "uses_bridge_assumptions": row["uses_bridge_assumptions"].lower() == "true",
                "assumption_ids": assumption_ids,
                "cert": row["python_cert"],
                "python_cert": certs,
                "status": row["release_status"],
                "notes": row["notes"],
                "module_path": str(mpath.relative_to(ROOT)).replace("\\", "/"),
                "module_exists": mexists,
                "certs_exist": all(cert_path(cert).exists() for cert in certs),
            }
        )

        domain_id = f"domain:{domain}"
        nodes.append(
            {
                "id": domain_id,
                "kind": "semantic_domain",
                "label": domain,
            }
        )
        edges.append({"source": claim_id, "target": domain_id, "kind": "semantic_domain"})

        module_id = f"module:{row['lean_module']}"
        nodes.append(
            {
                "id": module_id,
                "kind": "lean_module",
                "label": row["lean_module"],
                "path": str(mpath.relative_to(ROOT)).replace("\\", "/"),
                "exists": mexists,
            }
        )
        edges.append({"source": claim_id, "target": module_id, "kind": "implemented_in"})

        for cert in certs:
            cid = f"cert:{cert}"
            cpath = cert_path(cert)
            nodes.append(
                {
                    "id": cid,
                    "kind": "python_cert",
                    "label": cert,
                    "path": str(cpath.relative_to(ROOT)).replace("\\", "/"),
                    "exists": cpath.exists(),
                }
            )
            edges.append({"source": claim_id, "target": cid, "kind": "certified_by"})

        for aid in assumption_ids:
            assumption = assumption_by_id.get(aid, {})
            nodes.append(
                {
                    "id": f"assumption:{aid}",
                    "kind": "bridge_assumption",
                    "label": aid,
                    "lean_name": assumption.get("lean_name", ""),
                    "status": assumption.get("status", ""),
                    "assumption_type": assumption.get("assumption_type", ""),
                    "external_source_or_cert": assumption.get("external_source_or_cert", ""),
                }
            )
            edges.append({"source": claim_id, "target": f"assumption:{aid}", "kind": "uses_assumption"})

    deduped_nodes = {str(node["id"]): node for node in nodes}
    summary = {
        "claims": len(claims),
        "release_status": dict(Counter(row["release_status"] for row in claims)),
        "lean_status": dict(Counter(row["lean_status"] for row in claims)),
        "claim_type": dict(Counter(claim_type(row) for row in claims)),
        "domain": dict(Counter(claim_domain(row) for row in claims)),
    }
    payload = {
        "generated_from": [
            "09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv",
            "09_LEAN_FORMALIZATION/docs/LEAN_ASSUMPTION_LEDGER.csv",
        ],
        "summary": summary,
        "nodes": list(deduped_nodes.values()),
        "edges": edges,
    }
    (THEORY_DIR / "theory_graph.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def write_status_csv(claims: list[dict[str, str]]) -> None:
    out = THEORY_DIR / "theory_status_map.csv"
    fieldnames = [
        "claim_id",
        "book",
        "section",
        "type",
        "domain",
        "scope_guard",
        "lean_module",
        "lean_theorem",
        "lean_status",
        "release_status",
        "uses_bridge_assumptions",
        "assumption_ids",
        "python_cert",
        "module_exists",
        "certs_exist",
        "notes",
    ]
    with out.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in claims:
            certs = split_values(row["python_cert"])
            writer.writerow(
                {
                    "claim_id": row["claim_id"],
                    "book": row["book"],
                    "section": row["section"],
                    "type": claim_type(row),
                    "domain": claim_domain(row),
                    "scope_guard": scope_guard(row),
                    "lean_module": row["lean_module"],
                    "lean_theorem": row["lean_theorem"],
                    "lean_status": row["lean_status"],
                    "release_status": row["release_status"],
                    "uses_bridge_assumptions": row["uses_bridge_assumptions"],
                    "assumption_ids": row["assumption_ids"],
                    "python_cert": row["python_cert"],
                    "module_exists": modules_exist(row["lean_module"]),
                    "certs_exist": all(cert_path(cert).exists() for cert in certs),
                    "notes": row["notes"],
                }
            )


def write_dot(claims: list[dict[str, str]]) -> None:
    colors = {
        "core": "#2f7d4f",
        "bridge": "#6f5fb5",
        "certificate": "#1f6f9f",
        "no-go": "#9f3f3f",
        "external": "#6f6f6f",
        "deprecated": "#9f7a2f",
        "frontier": "#8a6d1f",
    }
    lines = ["digraph D0Theory {", "  rankdir=LR;", "  node [shape=box, style=filled, fontname=Arial];"]
    for row in claims:
        ctype = claim_type(row)
        label = f"{row['claim_id']}\\n{row['release_status']}\\n{claim_domain(row)}"
        lines.append(
            f"  {dot_quote(row['claim_id'])} [label={dot_quote(label)}, fillcolor={dot_quote(colors[ctype])}, fontcolor=\"white\"];"
        )
    for row in claims:
        module_id = f"module:{row['lean_module']}"
        lines.append(
            f"  {dot_quote(module_id)} [label={dot_quote(row['lean_module'])}, shape=ellipse, fillcolor=\"#eeeeee\", fontcolor=\"#111111\"];"
        )
        lines.append(f"  {dot_quote(row['claim_id'])} -> {dot_quote(module_id)} [label=\"module\"];")
        for cert in split_values(row["python_cert"]):
            cid = f"cert:{cert}"
            lines.append(
                f"  {dot_quote(cid)} [label={dot_quote(cert)}, shape=note, fillcolor=\"#fff0cc\", fontcolor=\"#111111\"];"
            )
            lines.append(f"  {dot_quote(row['claim_id'])} -> {dot_quote(cid)} [label=\"cert\"];")
        for aid in split_values(row["assumption_ids"]):
            aid_node = f"assumption:{aid}"
            lines.append(
                f"  {dot_quote(aid_node)} [label={dot_quote(aid)}, shape=diamond, fillcolor=\"#f0e8ff\", fontcolor=\"#111111\"];"
            )
            lines.append(f"  {dot_quote(row['claim_id'])} -> {dot_quote(aid_node)} [label=\"assumption\"];")
        domain_id = f"domain:{claim_domain(row)}"
        lines.append(
            f"  {dot_quote(domain_id)} [label={dot_quote(claim_domain(row))}, shape=folder, fillcolor=\"#e8f4ff\", fontcolor=\"#111111\"];"
        )
        lines.append(f"  {dot_quote(row['claim_id'])} -> {dot_quote(domain_id)} [label=\"domain\"];")
    lines.append("}")
    (THEORY_DIR / "theory_graph.dot").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_html(claims: list[dict[str, str]]) -> None:
    status_counts = Counter(row["release_status"] for row in claims)
    type_counts = Counter(claim_type(row) for row in claims)
    domain_counts = Counter(claim_domain(row) for row in claims)
    summary_html = "".join(
        f"<li><code>{html.escape(key)}</code>: {count}</li>"
        for key, count in sorted(status_counts.items())
    )
    type_html = "".join(
        f"<li><code>{html.escape(key)}</code>: {count}</li>"
        for key, count in sorted(type_counts.items())
    )
    domain_html = "".join(
        f"<li><code>{html.escape(key)}</code>: {count}</li>"
        for key, count in sorted(domain_counts.items())
    )
    rows = []
    for row in claims:
        certs = ", ".join(split_values(row["python_cert"]))
        rows.append(
            "<tr>"
            f"<td>{html.escape(row['claim_id'])}</td>"
            f"<td>{html.escape(row['book'])}</td>"
            f"<td>{html.escape(claim_type(row))}</td>"
            f"<td>{html.escape(claim_domain(row))}</td>"
            f"<td>{html.escape(row['release_status'])}</td>"
            f"<td>{html.escape(row['lean_status'])}</td>"
            f"<td><code>{html.escape(row['lean_module'])}</code></td>"
            f"<td>{html.escape(row['lean_theorem'])}</td>"
            f"<td>{html.escape(certs)}</td>"
            f"<td>{html.escape(scope_guard(row))}</td>"
            f"<td>{html.escape(row['notes'])}</td>"
            "</tr>"
        )
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>D0 Theory Status Map</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 24px; color: #181818; }}
h1 {{ margin-bottom: 4px; }}
.meta {{ color: #555; margin-bottom: 24px; }}
.summary {{ display: flex; gap: 48px; align-items: flex-start; }}
table {{ border-collapse: collapse; width: 100%; font-size: 13px; }}
th, td {{ border: 1px solid #ddd; padding: 6px 8px; vertical-align: top; }}
th {{ background: #f3f3f3; position: sticky; top: 0; }}
code {{ white-space: nowrap; }}
</style>
</head>
<body>
<h1>D0 Theory Status Map</h1>
<div class="meta">Generated from CLAIM_TO_LEAN_MAP.csv and LEAN_ASSUMPTION_LEDGER.csv.</div>
<div class="summary">
<section><h2>Release Status</h2><ul>{summary_html}</ul></section>
<section><h2>Claim Type</h2><ul>{type_html}</ul></section>
<section><h2>Semantic Domain</h2><ul>{domain_html}</ul></section>
</div>
<table>
<thead><tr><th>Claim</th><th>Book</th><th>Type</th><th>Domain</th><th>Release</th><th>Lean</th><th>Module</th><th>Theorem(s)</th><th>Cert</th><th>Scope guard</th><th>Notes</th></tr></thead>
<tbody>
{''.join(rows)}
</tbody>
</table>
</body>
</html>
"""
    (THEORY_DIR / "theory_graph.html").write_text(page, encoding="utf-8")


def write_markdown_index(claims: list[dict[str, str]]) -> None:
    lines = [
        "# Lean claim/status index",
        "",
        "Generated from `09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv`.",
        "This is the current status index for D0 theory branches, Lean anchors, certificates, and no-go boundaries.",
        "",
        "| Claim | Type | Domain | Release status | Lean status | Module | Theorem(s) | Cert | Scope guard |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for row in claims:
        cert = row["python_cert"] or ""
        theorem = row["lean_theorem"].replace("|", "\\|")
        guard = scope_guard(row).replace("|", "\\|")
        lines.append(
            f"| {row['claim_id']} | {claim_type(row)} | {claim_domain(row)} | {row['release_status']} | {row['lean_status']} | "
            f"`{row['lean_module']}` | `{theorem}` | `{cert}` | {guard} |"
        )
    LEAN_INDEX.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_semantic_index(claims: list[dict[str, str]]) -> None:
    status_counts = Counter(row["release_status"] for row in claims)
    domain_counts = Counter(claim_domain(row) for row in claims)
    type_counts = Counter(claim_type(row) for row in claims)
    lines = [
        "# D0 theory semantic index",
        "",
        "Generated from `09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv` and `09_LEAN_FORMALIZATION/docs/LEAN_ASSUMPTION_LEDGER.csv`.",
        "Purpose: make bridge boundaries, risky physical domains, Lean anchors, certificates, and legacy rows visible to both humans and Graphify.",
        "",
        "## Status counts",
        "",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"- `{status}`: {count}")
    lines.extend(["", "## Type counts", ""])
    for ctype, count in sorted(type_counts.items()):
        lines.append(f"- `{ctype}`: {count}")
    lines.extend(["", "## Domain counts", ""])
    for domain, count in sorted(domain_counts.items()):
        lines.append(f"- `{domain}`: {count}")

    for domain in sorted(domain_counts):
        lines.extend(["", f"## Domain: {domain}", ""])
        domain_rows = [row for row in claims if claim_domain(row) == domain]
        domain_rows.sort(key=lambda row: (claim_type(row), row["release_status"], row["claim_id"]))
        for row in domain_rows:
            cert = row["python_cert"] or "none"
            assumptions = row["assumption_ids"] or "none"
            theorem = row["lean_theorem"] or "none"
            lines.extend(
                [
                    f"### {row['claim_id']}",
                    "",
                    f"- type: `{claim_type(row)}`",
                    f"- release_status: `{row['release_status']}`",
                    f"- domain: `{domain}`",
                    f"- book: `{row['book']}`",
                    f"- module: `{row['lean_module']}`",
                    f"- theorem: `{theorem}`",
                    f"- cert: `{cert}`",
                    f"- assumptions: `{assumptions}`",
                    f"- scope: {scope_guard(row)}",
                    f"- notes: {row['notes']}",
                    "",
                ]
            )

    SEMANTIC_INDEX.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    THEORY_DIR.mkdir(parents=True, exist_ok=True)
    claims = read_csv(CLAIM_MAP)
    assumptions = read_csv(ASSUMPTION_LEDGER)
    write_json(claims, assumptions)
    write_status_csv(claims)
    write_dot(claims)
    write_html(claims)
    write_markdown_index(claims)
    write_semantic_index(claims)
    print(f"Synced {len(claims)} claims into {THEORY_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
