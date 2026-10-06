#!/usr/bin/env python3
"""Hostile metadata controls; no external dependencies or registry mutation."""
from pathlib import Path
import importlib.util
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "03_FORMALIZATION/tools/check_claim_map_coverage.py"
spec = importlib.util.spec_from_file_location("claim_coverage", PATH)
assert spec is not None and spec.loader is not None
coverage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(coverage)


def row(**changes):
    data = {
        "claim_id": "TEST-CLAIM", "lean_status": "LEAN_PROVED",
        "release_status": "CORE-FORMALIZED", "lean_module": "D0.Test",
        "lean_theorem": "test_theorem", "uses_bridge_assumptions": "false",
        "assumption_ids": "",
    }
    data.update(changes)
    return data


class CoverageTests(unittest.TestCase):
    def check_row(self, data, valid):
        errors = coverage.validate_rows([data], {"A", "B"}, required=set())
        self.assertEqual(not errors, valid, errors)

    def test_core_proof(self):
        self.check_row(row(), True)

    def test_missing_module(self):
        self.check_row(row(lean_module=""), False)

    def test_blank_theorem(self):
        self.check_row(row(lean_theorem="  "), False)

    def test_bad_proof_status(self):
        self.check_row(row(lean_status="PROVED_BY_CHAT"), False)

    def test_open_without_owner(self):
        self.check_row(row(lean_status="OPEN", release_status="PROOF-TARGET",
                           lean_module="", lean_theorem=""), True)

    def test_unproved_without_owner(self):
        self.check_row(row(lean_status="UNPROVED", release_status="FRONTIER",
                           lean_module="", lean_theorem=""), True)

    def test_open_cannot_be_core(self):
        self.check_row(row(lean_status="OPEN"), False)

    def test_unproved_cannot_be_core(self):
        self.check_row(row(lean_status="UNPROVED"), False)

    def test_python_cannot_be_core(self):
        self.check_row(row(lean_status="PYTHON_CERTIFIED"), False)

    def test_conditional_proof(self):
        self.check_row(row(lean_status="LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS",
                           release_status="BRIDGE-CLOSED", uses_bridge_assumptions="true",
                           assumption_ids="A"), True)

    def test_conditional_proof_requires_owner(self):
        self.check_row(row(lean_status="LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS",
                           release_status="BRIDGE-CLOSED", uses_bridge_assumptions="true",
                           assumption_ids="A", lean_theorem=""), False)

    def test_conditional_cannot_be_core(self):
        self.check_row(row(lean_status="LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS",
                           uses_bridge_assumptions="true", assumption_ids="A"), False)

    def test_hidden_bridge_cannot_be_unconditional_core(self):
        self.check_row(row(uses_bridge_assumptions="true", assumption_ids="A"), False)

    def test_open_bridge(self):
        self.check_row(row(lean_status="OPEN", release_status="PROOF-TARGET",
                           uses_bridge_assumptions="true", assumption_ids="A"), True)

    def test_unproved_bridge(self):
        self.check_row(row(lean_status="UNPROVED", release_status="FRONTIER",
                           uses_bridge_assumptions="true", assumption_ids="A"), True)

    def test_open_bridge_cannot_be_closed(self):
        self.check_row(row(lean_status="OPEN", release_status="BRIDGE-CLOSED",
                           uses_bridge_assumptions="true", assumption_ids="A"), False)

    def test_unproved_bridge_cannot_be_closed(self):
        self.check_row(row(lean_status="UNPROVED", release_status="BRIDGE-CLOSED",
                           uses_bridge_assumptions="true", assumption_ids="A"), False)

    def test_open_bridge_requires_assumptions(self):
        self.check_row(row(lean_status="OPEN", release_status="PROOF-TARGET",
                           uses_bridge_assumptions="true"), False)

    def test_open_bridge_requires_registered_assumption(self):
        self.check_row(row(lean_status="OPEN", release_status="PROOF-TARGET",
                           uses_bridge_assumptions="true", assumption_ids="MISSING"), False)

    def test_assumptions_require_bridge_flag(self):
        self.check_row(row(assumption_ids="A"), False)

    def test_certified_bridge(self):
        self.check_row(row(lean_status="PYTHON_CERTIFIED", release_status="FINITE-CERT-CLOSED",
                           uses_bridge_assumptions="true", assumption_ids=" A; B ",
                           lean_module="", lean_theorem=""), True)

    def test_proved_intermediate_open_release_is_not_promoted(self):
        original = row(release_status="PROOF-TARGET")
        snapshot = dict(original)
        self.check_row(original, True)
        self.assertEqual(original, snapshot)

    def test_missing_required_claim(self):
        errors = coverage.validate_rows([row()], set(), required={"MISSING"})
        self.assertTrue(any("missing required claim" in e for e in errors))

    def test_duplicate_claims(self):
        errors = coverage.validate_rows([row(), row()], set(), required=set())
        self.assertTrue(any("duplicate claim_id" in e for e in errors))

    def test_empty_claim_id(self):
        self.check_row(row(claim_id=" "), False)


if __name__ == "__main__":
    unittest.main()
