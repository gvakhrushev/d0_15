"""Parse a primary-owned finite kernel candidate block; no scientific registry.

All statements, dispositions, hypotheses and declaration selectors live in the
primary architecture artifact. This parser validates its immutable block pin
and shape. It never infers semantic correspondence, acceptance or coverage.
"""

import hashlib
import json
import re


HEADING = "C0 Book02 mathematical-unit candidates"
FIELDS = {"atom", "disposition", "source_range", "hypotheses", "statement",
          "declaration", "declaration_kind", "type_sha256"}
DISPOSITIONS = {"definition", "construction", "conditional_theorem",
                "negative_control_component", "negative_control"}


def parse_unit_candidates(primary_text: str, expected_sha256: str, *, heading=HEADING) -> list:
    """Return exact pinned primary fields, rejecting ambiguity and malformed data."""
    # Bound the exact H3 section at the next H1/H2/H3. Later unrelated reports
    # may legitimately contain JSON; they are not part of this candidate block.
    headings = list(re.finditer(r"(?m)^#{1,3} [^\r\n]*$", primary_text))
    sections = [primary_text[h.end():headings[i + 1].start() if i + 1 < len(headings)
                             else len(primary_text)]
                for i, h in enumerate(headings) if h.group().strip() == "### " + heading]
    if len(sections) != 1:
        raise ValueError("expected exactly one primary kernel candidate section")
    blocks = re.findall(r"(?m)^```json\r?\n(.*?)\r?\n```[ \t]*$", sections[0], re.S)
    if len(blocks) != 1:
        raise ValueError("expected exactly one primary kernel JSON block")
    raw = blocks[0]
    if hashlib.sha256(raw.encode("utf-8")).hexdigest() != expected_sha256:
        raise ValueError("primary kernel candidate block digest mismatch")

    def unique_object(pairs):
        obj = {}
        for key, value in pairs:
            if key in obj:
                raise ValueError("duplicate primary kernel JSON key: " + key)
            obj[key] = value
        return obj

    obj = json.loads(raw, object_pairs_hook=unique_object)
    if (not isinstance(obj, dict) or set(obj) != {"schema", "units"}
            or obj["schema"] not in ("d0-c0-kernel-unit-candidates/1",
                                     "d0-c0-kernel-unit-candidates/2")):
        raise ValueError("unexpected primary kernel candidate schema")
    # Version 2 binds each atom to its actual owning module, which may differ
    # from its declaration namespace. Version 1 retains the single-owner view.
    fields = FIELDS | {"module"} if obj["schema"].endswith("/2") else FIELDS
    units = obj["units"]
    if not isinstance(units, list) or not units:
        raise ValueError("primary kernel candidates must be a nonempty list")
    for unit in units:
        if not isinstance(unit, dict) or set(unit) != fields:
            raise ValueError("unexpected primary kernel candidate fields")
        if any(not isinstance(unit[k], str) or not unit[k] for k in fields - {"source_range"}):
            raise ValueError("kernel candidate text fields must be nonempty strings")
        span = unit["source_range"]
        if (not isinstance(span, list) or len(span) != 2
                or any(type(x) is not int for x in span) or not 0 <= span[0] < span[1]):
            raise ValueError("invalid kernel candidate source range")
        if unit["disposition"] not in DISPOSITIONS:
            raise ValueError("unexpected kernel candidate disposition")
        if unit["declaration_kind"] not in ("definition", "inductive", "theorem"):
            raise ValueError("unexpected kernel candidate declaration kind")
        if not re.fullmatch(r"[0-9a-f]{64}", unit["type_sha256"]):
            raise ValueError("malformed kernel candidate type digest")
        if "module" in fields and not re.fullmatch(r"D0(?:\.[A-Za-z0-9_]+)+", unit["module"]):
            raise ValueError("malformed kernel candidate owner module")
    if len({u["atom"] for u in units}) != len(units):
        raise ValueError("duplicate kernel candidate atom")
    if len({u["declaration"] for u in units}) != len(units):
        raise ValueError("duplicate kernel candidate declaration")
    return units
