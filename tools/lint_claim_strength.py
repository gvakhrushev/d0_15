#!/usr/bin/env python3
"""Deterministic public claim-strength lint.

Scans README.md, 01_BOOKS/, and 02_REGISTRY/frontier/ for registered
overstatement phrases. Rules and the allowlist live in
02_REGISTRY/claim_strength_rules.json. forcing_routes.json supplies the
section ledger for unqualified independence claims.

This is a phrase and metadata check. It does not judge mathematics and it
does not change claim status.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RULES = ROOT / "02_REGISTRY" / "claim_strength_rules.json"
FIXTURES = ROOT / "tools" / "fixtures" / "claim_strength"

RULE_KEYS = {"id", "claim_ids", "pattern", "negation", "window", "message"}
LEDGER_KEYS = {
    "id",
    "claim_ids",
    "source",
    "pattern",
    "qualifier",
    "qualifier_lines",
    "message",
}
TOKEN_RE = re.compile(r"§\s*(\d+(?:\.\d+)+(?:[A-Za-z]+)?)")
HEADING_RE = re.compile(r"^(#{1,6})[ \t]+(.+?)\s*$", re.M)


class LintError(Exception):
    pass


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    rule_id: str
    message: str
    matched: str

    def format(self) -> str:
        snippet = self.matched.replace("\n", " ").strip()
        return f"{self.path}:{self.line}: {self.rule_id}: {self.message} | matched: {snippet}"


def load_rules(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise LintError(f"{path}: rules are not valid JSON: {exc}") from exc
    if data.get("schema") != "d0-claim-strength/1":
        raise LintError(f"{path}: schema must be d0-claim-strength/1")
    surfaces = data.get("surfaces")
    if not isinstance(surfaces, list) or not surfaces or not all(isinstance(s, str) and s for s in surfaces):
        raise LintError(f"{path}: surfaces must be a non-empty list of paths")
    rules = data.get("rules")
    if not isinstance(rules, list) or not rules:
        raise LintError(f"{path}: rules must be a non-empty list")
    seen: set[str] = set()
    for rule in rules:
        if not isinstance(rule, dict) or set(rule) != RULE_KEYS:
            raise LintError(f"{path}: rule keys must be {sorted(RULE_KEYS)}")
        rid = rule["id"]
        if not isinstance(rid, str) or not rid or rid in seen:
            raise LintError(f"{path}: duplicate or empty rule id {rid!r}")
        seen.add(rid)
        _compile(path, rid, rule["pattern"])
        _compile(path, rid, rule["negation"])
        if not isinstance(rule["window"], int) or rule["window"] < 0:
            raise LintError(f"{path}: {rid} window must be a non-negative integer")
        _claim_ids(path, rid, rule["claim_ids"])
        if not isinstance(rule["message"], str) or not rule["message"].strip():
            raise LintError(f"{path}: {rid} message is empty")
    ledger = data.get("ledger")
    if not isinstance(ledger, dict) or set(ledger) != LEDGER_KEYS:
        raise LintError(f"{path}: ledger keys must be {sorted(LEDGER_KEYS)}")
    if ledger["id"] in seen:
        raise LintError(f"{path}: ledger id collides with a phrase rule")
    _compile(path, ledger["id"], ledger["pattern"])
    _compile(path, ledger["id"], ledger["qualifier"])
    if not isinstance(ledger["qualifier_lines"], int) or ledger["qualifier_lines"] < 1:
        raise LintError(f"{path}: ledger qualifier_lines must be a positive integer")
    _claim_ids(path, ledger["id"], ledger["claim_ids"])
    if not isinstance(ledger["source"], str) or not ledger["source"]:
        raise LintError(f"{path}: ledger source is empty")
    allow = data.get("allowlist")
    if not isinstance(allow, list):
        raise LintError(f"{path}: allowlist must be a list")
    known = seen | {ledger["id"]}
    for entry in allow:
        if not isinstance(entry, dict):
            raise LintError(f"{path}: allowlist entry is not an object")
        if set(entry) != {"rule_id", "path", "contains", "reason"}:
            raise LintError(f"{path}: allowlist entry keys must be rule_id, path, contains, reason")
        if entry["rule_id"] not in known:
            raise LintError(f"{path}: allowlist rule_id {entry['rule_id']!r} is unknown")
        if not entry["path"] or not entry["contains"] or not entry["reason"]:
            raise LintError(f"{path}: allowlist path, contains, and reason must be non-empty")
    return data


def _compile(path: Path, rid: str, pattern: str) -> re.Pattern[str]:
    if not isinstance(pattern, str) or not pattern:
        raise LintError(f"{path}: {rid} has an empty pattern")
    try:
        return re.compile(pattern)
    except re.error as exc:
        raise LintError(f"{path}: {rid} pattern does not compile: {exc}") from exc


def _claim_ids(path: Path, rid: str, claim_ids: object) -> None:
    if not isinstance(claim_ids, list) or not claim_ids or not all(isinstance(c, str) and c for c in claim_ids):
        raise LintError(f"{path}: {rid} claim_ids must be a non-empty list of strings")


def check_claim_ids(repo: Path, rules: dict) -> None:
    claims = repo / "02_REGISTRY" / "claims.csv"
    if not claims.exists():
        return
    with claims.open(encoding="utf-8", newline="") as handle:
        known = {row.get("claim_id", "").strip() for row in csv.DictReader(handle)}
    cited: list[str] = []
    for rule in rules["rules"]:
        cited.extend(rule["claim_ids"])
    cited.extend(rules["ledger"]["claim_ids"])
    missing = sorted({cid for cid in cited if cid not in known})
    if missing:
        raise LintError("rules cite unknown claim ids: " + ", ".join(missing))


def surface_files(root: Path, rules: dict) -> list[tuple[str, Path]]:
    found: list[tuple[str, Path]] = []
    for rel in rules["surfaces"]:
        path = root / rel
        if path.is_file() and path.suffix == ".md":
            found.append((rel, path))
        elif path.is_dir():
            for child in sorted(path.rglob("*.md")):
                if any(part.startswith(".") for part in child.relative_to(root).parts):
                    continue
                found.append((child.relative_to(root).as_posix(), child))
    if not found:
        raise LintError(f"{root}: no markdown surfaces found")
    return found


def line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def line_text(text: str, index: int) -> str:
    start = text.rfind("\n", 0, index) + 1
    end = text.find("\n", index)
    if end < 0:
        end = len(text)
    return text[start:end]


def allowed(rules: dict, rule_id: str, rel: str, line: str) -> bool:
    for entry in rules["allowlist"]:
        if entry["rule_id"] == rule_id and entry["path"] == rel and entry["contains"] in line:
            return True
    return False


def scan(root: Path, rules: dict) -> list[Finding]:
    findings: list[Finding] = []
    texts: list[tuple[str, str]] = []
    for rel, path in surface_files(root, rules):
        texts.append((rel, path.read_text(encoding="utf-8", errors="replace")))
    for rule in rules["rules"]:
        pattern = re.compile(rule["pattern"])
        negation = re.compile(rule["negation"])
        radius = rule["window"]
        for rel, text in texts:
            for match in pattern.finditer(text):
                window = text[max(0, match.start() - radius) : min(len(text), match.end() + radius)]
                if negation.search(window):
                    continue
                current = line_text(text, match.start())
                if allowed(rules, rule["id"], rel, current):
                    continue
                findings.append(
                    Finding(
                        rel,
                        line_number(text, match.start()),
                        rule["id"],
                        rule["message"],
                        match.group(0)[:160],
                    )
                )
    findings.extend(scan_ledger(root, rules, texts))
    unique = {(item.path, item.line, item.rule_id): item for item in findings}
    return [unique[key] for key in sorted(unique)]


def ledger_hits(
    rules: dict,
    ledger: dict,
    pattern: re.Pattern[str],
    qualifier: re.Pattern[str],
    span: int,
    rel: str,
    text: str,
    start: int,
    end: int,
) -> list[Finding]:
    findings: list[Finding] = []
    for match in pattern.finditer(text[start:end]):
        absolute = start + match.start()
        line = line_number(text, absolute)
        if qualifier_near(text, line, span, qualifier):
            continue
        current = line_text(text, absolute)
        if allowed(rules, ledger["id"], rel, current):
            continue
        findings.append(
            Finding(rel, line, ledger["id"], ledger["message"], match.group(0)[:160])
        )
    return findings


def unbound_token_hits(
    rules: dict,
    ledger: dict,
    pattern: re.Pattern[str],
    qualifier: re.Pattern[str],
    span: int,
    rel: str,
    text: str,
    token: str,
) -> list[Finding]:
    """Anchor a section id that is named in prose rather than in a markdown heading."""
    findings: list[Finding] = []
    lines = text.splitlines(keepends=True)
    offset = 0
    for row in lines:
        next_offset = offset + len(row)
        if token_in(row, token) and not row.lstrip().startswith("#"):
            end = min(len(text), next_offset)
            # Keep the paragraph and the following qualifier window, and stop at a heading.
            tail = text[offset:]
            stop = len(tail)
            for later in HEADING_RE.finditer(tail):
                if later.start() > 0:
                    stop = later.start()
                    break
            window_end = offset + min(stop, 4000)
            findings.extend(
                ledger_hits(rules, ledger, pattern, qualifier, span, rel, text, offset, window_end)
            )
        offset = next_offset
    return findings


def scan_ledger(root: Path, rules: dict, texts: list[tuple[str, str]]) -> list[Finding]:
    ledger = rules["ledger"]
    source = root / ledger["source"]
    if not source.is_file():
        raise LintError(f"missing forcing ledger {ledger['source']}")
    try:
        data = json.loads(source.read_text(encoding="utf-8"))
    except Exception as exc:
        raise LintError(f"{ledger['source']}: ledger is not valid JSON: {exc}") from exc
    tokens = sorted({token for rec in iter_dicts(data) if overclaims(rec) for token in section_tokens(rec.get("section", ""))})
    if not tokens:
        raise LintError(f"{ledger['source']}: no audited non-independent sections")
    pattern = re.compile(ledger["pattern"])
    qualifier = re.compile(ledger["qualifier"])
    span = ledger["qualifier_lines"]
    findings: list[Finding] = []
    matched_token = False
    for rel, text in texts:
        sections = sections_for_tokens(text, tokens)
        if sections:
            matched_token = True
        for _token, start, end in sections:
            findings.extend(
                ledger_hits(rules, ledger, pattern, qualifier, span, rel, text, start, end)
            )
        bound = {token for token, _start, _end in sections}
        for token in tokens:
            if token in bound:
                continue
            findings.extend(unbound_token_hits(rules, ledger, pattern, qualifier, span, rel, text, token))
            if token_in(text, token):
                matched_token = True
    if not matched_token:
        raise LintError("forcing ledger sections did not match any scanned heading")
    return findings


def iter_dicts(obj: object) -> Iterator[dict]:
    if isinstance(obj, dict):
        yield obj
        for value in obj.values():
            yield from iter_dicts(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from iter_dicts(value)


def overclaims(record: dict) -> bool:
    if record.get("independent") is False or record.get("independent_now") is False:
        return True
    claimed = record.get("routes_claimed")
    real = record.get("routes_real")
    return isinstance(claimed, int) and isinstance(real, int) and claimed > real


def section_tokens(section: object) -> list[str]:
    if not isinstance(section, str):
        return []
    return TOKEN_RE.findall(section)


def token_in(text: str, token: str) -> bool:
    return re.search(rf"(?<![0-9A-Za-z.]){re.escape(token)}(?![0-9A-Za-z.])", text) is not None


def split_sections(text: str) -> list[tuple[str, int, int]]:
    """Return (heading, start, end) including nested subsections."""
    marks = list(HEADING_RE.finditer(text))
    sections: list[tuple[str, int, int]] = []
    for index, mark in enumerate(marks):
        level = len(mark.group(1))
        end = len(text)
        for later in marks[index + 1 :]:
            if len(later.group(1)) <= level:
                end = later.start()
                break
        sections.append((mark.group(2), mark.start(), end))
    return sections


def sections_for_tokens(text: str, tokens: list[str]) -> list[tuple[str, int, int]]:
    chosen: list[tuple[str, int, int]] = []
    for title, start, end in split_sections(text):
        for token in tokens:
            if token_in(title, token):
                chosen.append((token, start, end))
                break
    return chosen


def qualifier_near(text: str, line: int, span: int, qualifier: re.Pattern[str]) -> bool:
    rows = text.splitlines()
    begin = max(1, line - 2)
    finish = min(len(rows), line + span)
    return qualifier.search("\n".join(rows[begin - 1 : finish])) is not None


def report(findings: list[Finding]) -> int:
    for finding in findings:
        print(finding.format())
    if findings:
        print(f"{len(findings)} claim-strength finding(s)")
        return 1
    print("PASS claim-strength lint")
    return 0


def run_self_test(rules: dict) -> int:
    negative = FIXTURES / "negative"
    positive = FIXTURES / "positive"
    allow_root = FIXTURES / "allowlist"
    errors: list[str] = []
    try:
        negative_findings = scan(negative, rules)
    except LintError as exc:
        errors.append(f"negative fixture failed to scan: {exc}")
        negative_findings = []
    found = {item.rule_id for item in negative_findings}
    expected = {rule["id"] for rule in rules["rules"]} | {rules["ledger"]["id"]}
    missing = sorted(expected - found)
    extra = sorted(found - expected)
    if missing:
        errors.append("negative fixture missed rules: " + ", ".join(missing))
    if extra:
        errors.append("negative fixture reported unknown rules: " + ", ".join(extra))
    shell_matched = " ".join(
        item.matched for item in negative_findings if item.rule_id == "shell-compression-is-book-feedback"
    )
    if "spatialShellFluxCompression" not in shell_matched:
        errors.append("shell-compression rule did not match spatialShellFluxCompression")
    hom_matched = " ".join(
        item.matched for item in negative_findings if item.rule_id == "shell48-is-matter-selector"
    )
    if "Hom_{S3}" not in hom_matched:
        errors.append("shell48 rule did not match the stabilizer-equivariant Hom space")
    for rule in rules["rules"]:
        if rule["id"] != "shell48-is-matter-selector":
            continue
        if "L=2" in rule["message"] or "L = 2" in rule["message"]:
            errors.append("shell48 message still names L=2")
        if "Hom_{S3}" not in rule["message"]:
            errors.append("shell48 message does not name the equivariant Hom space")
    try:
        positive_findings = scan(positive, rules)
    except LintError as exc:
        errors.append(f"positive fixture failed to scan: {exc}")
        positive_findings = []
    if positive_findings:
        errors.append("positive fixture was not clean:\n" + "\n".join(item.format() for item in positive_findings))
    allow_rules = json.loads(json.dumps(rules))
    allow_rules["allowlist"] = [
        {
            "rule_id": "lcdm-unconditional-exclusion",
            "path": "README.md",
            "contains": "Every open graph with unitary archive dissipation excludes ΛCDM",
            "reason": "Fixture proves an explicit allowlist entry suppresses one reviewed line.",
        }
    ]
    try:
        allow_findings = scan(allow_root, allow_rules)
    except LintError as exc:
        errors.append(f"allowlist fixture failed to scan: {exc}")
        allow_findings = []
    if allow_findings:
        errors.append("allowlist fixture was not suppressed:\n" + "\n".join(item.format() for item in allow_findings))
    bare = json.loads(json.dumps(rules))
    bare["allowlist"] = []
    with tempfile.TemporaryDirectory() as tmp:
        probe = Path(tmp)
        (probe / "README.md").write_text(
            "Every open graph with unitary archive dissipation excludes ΛCDM.\n",
            encoding="utf-8",
        )
        (probe / "01_BOOKS").mkdir()
        (probe / "01_BOOKS" / "BOOK.md").write_text("## 99.1 Quiet\n\nNo independence phrase here.\n", encoding="utf-8")
        (probe / "02_REGISTRY").mkdir()
        (probe / "02_REGISTRY" / "frontier").mkdir()
        (probe / "02_REGISTRY" / "frontier" / "NOTE.md").write_text("# Note\n", encoding="utf-8")
        (probe / "02_REGISTRY" / "forcing_routes.json").write_text(
            (negative / "02_REGISTRY" / "forcing_routes.json").read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        try:
            probe_findings = scan(probe, bare)
        except LintError as exc:
            errors.append(f"unlisted exclusion probe failed to scan: {exc}")
            probe_findings = []
        if not any(item.rule_id == "lcdm-unconditional-exclusion" for item in probe_findings):
            errors.append("LCDM exclusion was silent when the allowlist entry was absent")
    try:
        with tempfile.TemporaryDirectory() as schema_dir:
            broken = json.loads(DEFAULT_RULES.read_text(encoding="utf-8"))
            broken["rules"][0]["pattern"] = "("
            blob = Path(schema_dir) / "broken.json"
            blob.write_text(json.dumps(broken), encoding="utf-8")
            try:
                load_rules(blob)
            except LintError:
                pass
            else:
                errors.append("a broken pattern was accepted")
    except Exception as exc:
        errors.append(f"schema rejection probe crashed: {exc}")
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("PASS claim-strength self-test")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Lint public prose against registered claim strength.")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--rules", type=Path, default=DEFAULT_RULES)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    try:
        rules = load_rules(args.rules)
        check_claim_ids(ROOT, rules)
        if args.self_test:
            return run_self_test(rules)
        return report(scan(args.root, rules))
    except LintError as exc:
        print(f"claim-strength lint error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
