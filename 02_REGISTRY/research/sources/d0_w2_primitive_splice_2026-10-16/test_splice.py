"""Retained-record checks for the golden/cochain splice.

More than one test has to pass. A same-effect substitution and an erasure
of the return record are required to fail the label test.
"""

from __future__ import annotations

import unittest

import splice


class AlgebraAndOwners(unittest.TestCase):
    def test_gate_relations_and_nontrivial_sign_bridge(self):
        splice.algebra_relations()

    def test_declarations_resolve_to_source_lines(self):
        found = splice.resolve_declarations()
        self.assertGreaterEqual(len(found), 20)
        names = {item["name"] for item in found}
        self.assertIn("D0.Representation.GoldenOrderInterferometer.gate", names)
        self.assertIn("D0.Geometry.cochainForwardShift", names)
        self.assertIn("D0.Geometry.roleOrderIndex", names)
        self.assertIn("D0.Geometry.roleCode", names)
        for item in found:
            self.assertGreater(item["line"], 0)

    def test_scalar_specialization_matches_output_formula(self):
        splice.scalar_gate_matches_owner()


class RetainedRecord(unittest.TestCase):
    def test_full_cochain_basis_both_ports(self):
        count = splice.full_basis_term_diagram()
        self.assertEqual(count, 4 * (3 ** 4) * 16)

    def test_sign_bridge_commutes_and_complement_is_empty(self):
        count = splice.sign_and_complement()
        self.assertEqual(count, 4 * (3 ** 4) * 16)

    def test_same_effect_different_instrument_fails_labels(self):
        probe = splice.substitution_and_erasure()
        self.assertGreater(probe["labels_rejected"], 0)
        self.assertEqual(probe["labels_rejected"], probe["effects_agree"])
        self.assertEqual(probe["basis"], 3 ** 4 * 16)
        self.assertEqual(probe["relabel_rejected"], probe["basis"])

    def test_erasure_of_grade_sign_and_ports_fails(self):
        probe = splice.substitution_and_erasure()
        self.assertGreater(probe["grade_erasure_collisions"], 0)
        self.assertGreater(probe["sign_erasure_rejected"], 0)

    def test_l2_involution_is_not_the_negative_probe(self):
        splice.l2_involution_is_not_separating()


class TypedGaps(unittest.TestCase):
    def test_coefficient_orders_disagree_and_dilation_is_missing(self):
        splice.coefficient_orders_disagree()

    def test_four_interfaces_refuse_selection_and_price(self):
        splice.interface_refusals()
        gaps = splice.typed_gaps()
        self.assertEqual(len(gaps), 4)
        for gap in gaps:
            self.assertEqual(gap["kind"], "missing-engineering")
            self.assertTrue(gap["owners"])
            self.assertTrue(gap["input"])
            self.assertTrue(gap["missing_morphism"])
        with self.assertRaises(splice.MissingMorphism) as caught:
            splice.select_program(())
        self.assertEqual(caught.exception.kind, "unproved-selection-law")


if __name__ == "__main__":
    unittest.main()
