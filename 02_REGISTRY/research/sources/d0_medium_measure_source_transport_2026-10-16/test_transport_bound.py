"""Exact checks for the candidate C1 transport bound.

Negative controls must falsify the stated conclusion. An exception from the
arithmetic is a coding error, not one of those falsifications.
"""

from __future__ import annotations

import pathlib
import sys
import unittest
from fractions import Fraction

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import transport_bound as tb


def rational_family(q, jet):
    """Two cylinders, two cells, Z = 4+2q. jet is the price slope pair."""
    mu = {"c0": 3 + q, "c1": 1 + q}
    lam = {"c0": jet[0] * q, "c1": 4 + jet[1] * q}
    dmu = {"c0": Fraction(1), "c1": Fraction(1)}
    dlam = {"c0": Fraction(jet[0]), "c1": Fraction(jet[1])}
    return mu, lam, dmu, dlam


class RationalTransportTest(unittest.TestCase):
    def test_quotient_matches_independent_polynomial(self):
        q = Fraction(0)

        def moment(point):
            return (3 + point) * (5 * point) + (1 + point) * (4 + 7 * point)

        def normalizer(point):
            return 4 + 2 * point

        slope_m = (moment(1) - moment(-1)) / 2
        slope_z = (normalizer(1) - normalizer(-1)) / 2
        value = moment(q) / normalizer(q)
        independent = (slope_m - value * slope_z) / normalizer(q)

        mu, lam, dmu, dlam = rational_family(q, (5, 7))
        self.assertEqual(tb.normalized_average(mu, lam), Fraction(1))
        self.assertEqual(tb.full_derivative(mu, dmu, lam, dlam), independent)
        self.assertEqual(independent, Fraction(6))

    def test_same_values_different_jets_fail_the_conclusion(self):
        mu_a, lam_a, dmu, dlam_a = rational_family(Fraction(0), (0, 0))
        mu_b, lam_b, _, dlam_b = rational_family(Fraction(0), (5, 7))
        self.assertEqual(lam_a, lam_b)
        jet_a = tb.full_derivative(mu_a, dmu, lam_a, dlam_a)
        jet_b = tb.full_derivative(mu_b, dmu, lam_b, dlam_b)
        same_jet_determines_source = jet_a == jet_b
        self.assertFalse(same_jet_determines_source)
        self.assertEqual(jet_a, Fraction(1, 2))
        self.assertEqual(jet_b, Fraction(6))

    def test_deleting_dz_fails_normalized_equality(self):
        mu, lam, dmu, dlam = rational_family(Fraction(0), (5, 7))
        full = tb.full_derivative(mu, dmu, lam, dlam)
        bad = tb.deleted_z_derivative(mu, dmu, lam, dlam)
        gap = tb.deletion_gap(mu, dmu, lam, dlam)
        self.assertEqual(bad - full, gap)
        self.assertEqual(gap, Fraction(1, 2))
        equal_after_deleting_dz = full == bad
        self.assertFalse(equal_after_deleting_dz)

    def test_half_constant_is_sharp_for_values_and_weight_jet(self):
        mu = {"c0": Fraction(3), "c1": Fraction(1)}
        dmu = {"c0": Fraction(1), "c1": Fraction(1)}
        cells = ("i0", "i1")
        assignment = {"c0": "i0", "c1": "i1"}
        pushed = tb.pushforward(mu, assignment, cells)
        geometric = {"i0": Fraction(1), "i1": Fraction(1)}
        p = tb.normalized_probability(pushed)
        r = tb.normalized_probability(geometric)
        theta = tb.l1(p, r)
        cell_prices = {"i0": Fraction(0), "i1": Fraction(4)}
        osc = tb.oscillation(cell_prices)
        bound = tb.weight_value_bound(theta, osc)
        actual = tb.normalized_average(pushed, cell_prices) - tb.normalized_average(
            geometric, cell_prices
        )
        self.assertEqual(theta, Fraction(1, 2))
        self.assertEqual(osc, Fraction(4))
        self.assertEqual(bound, Fraction(1))
        self.assertEqual(abs(actual), bound)

        dp = tb.probability_derivative(pushed, tb.pushforward(dmu, assignment, cells))
        dr = tb.probability_derivative(geometric, {"i0": Fraction(0), "i1": Fraction(0)})
        theta1 = tb.l1(dp, dr)
        d_bound = tb.weight_derivative_bound(theta1, osc, theta, Fraction(0))
        d_prices = {"i0": Fraction(0), "i1": Fraction(0)}
        d_actual = tb.full_derivative(pushed, tb.pushforward(dmu, assignment, cells), cell_prices, d_prices)
        d_geometric = tb.full_derivative(geometric, {"i0": Fraction(0), "i1": Fraction(0)}, cell_prices, d_prices)
        self.assertEqual(d_geometric, Fraction(0))
        self.assertEqual(theta1, Fraction(1, 4))
        self.assertEqual(d_bound, Fraction(1, 2))
        self.assertEqual(abs(d_actual - d_geometric), d_bound)

        # Independent closed form of D(nu0/Z) at q=0, not the module's quotient.
        # nu0/Z = (3+q)/(4+2q); derivative at 0 is (4-6)/16.
        self.assertEqual(dp["i0"], Fraction(4 - 6, 16))

    def test_partition_motion_constant_is_sharp(self):
        mu = {"c0": Fraction(5)}
        cells = ("i0", "i1")
        here = {"c0": "i0"}
        there = {"c0": "i1"}
        prices = {"i0": Fraction(0), "i1": Fraction(4)}
        rho = tb.reassigned_fraction(mu, here, there)
        osc = tb.oscillation(prices)
        bound = tb.partition_motion_bound(rho, osc)
        left = tb.normalized_average(tb.pushforward(mu, here, cells), prices)
        right = tb.normalized_average(tb.pushforward(mu, there, cells), prices)
        self.assertEqual(rho, Fraction(1))
        self.assertEqual(bound, Fraction(4))
        self.assertEqual(abs(left - right), bound)

    def test_same_trace_without_spatial_map_fails_the_conclusion(self):
        mu = {"c0": Fraction(3), "c1": Fraction(1)}
        cells = ("i0", "i1")
        spatial = {"c0": "i0", "c1": "i1"}
        no_map_collapsed = {"c0": "i0", "c1": "i0"}
        pushed = tb.pushforward(mu, spatial, cells)
        collapsed = tb.pushforward(mu, no_map_collapsed, cells)
        same_total = tb.mass(pushed) == tb.mass(collapsed) == tb.mass(mu)
        self.assertTrue(same_total)
        trace_determines_cells = pushed == collapsed
        self.assertFalse(trace_determines_cells)

    def test_full_derivative_bound_uses_stated_coefficients(self):
        mu, lam, dmu, dlam = rational_family(Fraction(0), (5, 7))
        assignment = {"c0": "i0", "c1": "i1"}
        cells = ("i0", "i1")
        cell_prices = {"i0": Fraction(0), "i1": Fraction(4)}
        eta = {
            "c0": lam["c0"] - cell_prices["i0"],
            "c1": lam["c1"] - cell_prices["i1"],
        }
        deta = {"c0": dlam["c0"], "c1": dlam["c1"]}
        delta = tb.normalized_average(mu, eta)
        eps_prime = max(abs(value) for value in deta.values())
        eta_star = max(abs(eta[key] - delta) for key in eta)
        dmu_l1 = abs(dmu["c0"]) + abs(dmu["c1"])
        dz_abs = abs(tb.mass(dmu))
        fiber_bound = tb.fiber_derivative_bound(
            eps_prime, eta_star, dmu_l1, dz_abs, tb.mass(mu)
        )
        actual_fiber = tb.full_derivative(mu, dmu, lam, dlam) - tb.full_derivative(
            mu,
            dmu,
            {key: cell_prices[assignment[key]] for key in mu},
            {"c0": Fraction(0), "c1": Fraction(0)},
        )
        self.assertEqual(eps_prime, Fraction(7))
        self.assertEqual(eta_star, Fraction(0))
        self.assertEqual(fiber_bound, Fraction(7))
        self.assertLessEqual(abs(actual_fiber), fiber_bound)
        self.assertEqual(actual_fiber, Fraction(11, 2))
        coarse = tb.coarse_fiber_derivative_bound(
            eps_prime, Fraction(0), dmu_l1, tb.mass(mu)
        )
        self.assertEqual(coarse, fiber_bound)


class GoldenInclusionTest(unittest.TestCase):
    def setUp(self):
        self.ready = ("R1", "R2")
        self.pending = ("P",)
        self.mu = {
            "R1": tb.P * tb.P,
            "R2": tb.P * tb.P,
            "P": tb.P * tb.P * tb.P,
        }
        self.cells = ("i1", "i2", "i3")
        self.assignment = {"R1": "i1", "R2": "i2", "P": "i3"}
        self.cell_prices = {
            "i1": tb.Quad(0),
            "i2": tb.Quad(1),
            "i3": tb.Quad(3),
        }

    def test_real_parent_does_not_split_pending(self):
        parent = tb.real_cost_children(self.ready, self.pending)
        false_parent = tb.false_uniform_split(self.ready, self.pending)
        pending_children = [child for child, owner in parent.items() if owner == "P"]
        false_children = [child for child, owner in false_parent.items() if owner == "P"]
        self.assertEqual(len(pending_children), 1)
        self.assertEqual(len(false_children), 2)
        self.assertNotEqual(set(parent), set(false_parent))

    def test_commuting_pushforward_preserves_cells_and_mass(self):
        parent = tb.real_cost_children(self.ready, self.pending)
        refined = tb.refine_golden_weights(self.mu, self.ready, self.pending)
        fine_assignment = tb.commuting_assignment(self.assignment, parent)
        coarse = tb.pushforward(self.mu, self.assignment, self.cells)
        fine = tb.pushforward(refined, fine_assignment, self.cells)
        self.assertEqual(tb.mass(self.mu), tb.Quad(1))
        self.assertEqual(tb.mass(refined), tb.Quad(1))
        self.assertEqual(fine, coarse)
        self.assertEqual(coarse["i1"], tb.P * tb.P)
        self.assertEqual(coarse["i3"], tb.P * tb.P * tb.P)

    def test_same_trace_and_noncommuting_map_fail_the_conclusion(self):
        parent = tb.real_cost_children(self.ready, self.pending)
        refined = tb.refine_golden_weights(self.mu, self.ready, self.pending)
        commuting = tb.commuting_assignment(self.assignment, parent)
        broken = dict(commuting)
        broken[("start", "R1")] = "i3"
        coarse = tb.pushforward(self.mu, self.assignment, self.cells)
        fine_ok = tb.pushforward(refined, commuting, self.cells)
        fine_bad = tb.pushforward(refined, broken, self.cells)
        self.assertEqual(tb.mass(fine_ok), tb.mass(fine_bad))
        trace_determines_cells = fine_bad == coarse
        self.assertFalse(trace_determines_cells)
        self.assertEqual(fine_ok, coarse)

    def test_three_cell_value_and_motion_constants(self):
        pushed = tb.pushforward(self.mu, self.assignment, self.cells)
        geometric = {cell: tb.Quad(1) for cell in self.cells}
        actual = tb.normalized_average(pushed, self.cell_prices) - tb.normalized_average(
            geometric, self.cell_prices
        )
        # A_pi - A_w = -10/3 + 5p < 0, so the absolute value is 10/3 - 5p.
        absolute = tb.Quad(Fraction(10, 3), -5)
        self.assertEqual(actual, -absolute)
        # (1/2) * ||p-r||_1 * osc = 4 - 6p, with osc = 3.
        bound = tb.Quad(4, -6)
        self.assertTrue((bound - absolute).is_positive())

        parent = tb.real_cost_children(self.ready, self.pending)
        refined = tb.refine_golden_weights(self.mu, self.ready, self.pending)
        commuting = tb.commuting_assignment(self.assignment, parent)
        moved = dict(commuting)
        moved[("start", "R1")] = "i3"
        rho = tb.reassigned_fraction(refined, commuting, moved)
        osc = tb.oscillation(self.cell_prices)
        motion_bound = tb.partition_motion_bound(rho, osc)
        left = tb.normalized_average(
            tb.pushforward(refined, commuting, self.cells), self.cell_prices
        )
        right = tb.normalized_average(
            tb.pushforward(refined, moved, self.cells), self.cell_prices
        )
        self.assertEqual(rho, tb.P * tb.P * tb.P * tb.P)
        self.assertEqual(osc, tb.Quad(3))
        self.assertEqual(abs_quad_difference(left, right), motion_bound)


def abs_quad_difference(left, right):
    gap = left - right
    if gap.is_zero():
        return gap
    if gap.is_positive():
        return gap
    return -gap


class DepthParameterFirewallTest(unittest.TestCase):
    def test_cost_step_is_not_a_smooth_partial(self):
        ready = ("R",)
        pending = ("P",)
        mu = {"R": tb.P, "P": tb.P * tb.P}
        parent = tb.real_cost_children(ready, pending)
        refined = tb.refine_golden_weights(mu, ready, pending)
        assignment = {"R": "i1", "P": "i2"}
        cells = ("i1", "i2")
        commuting = tb.commuting_assignment(assignment, parent)
        broken = dict(commuting)
        broken[("start", "R")] = "i2"
        coarse = tb.pushforward(mu, assignment, cells)
        bad = tb.pushforward(refined, broken, cells)
        inclusion_gap = bad["i1"] - coarse["i1"]
        # Smooth stand-in t |-> t at the numerical point t=2, and a mesh factor h^2.
        t_partial = Fraction(1)
        h_partial = 2 * Fraction(2)
        self.assertEqual(inclusion_gap, -(tb.P * tb.P * tb.P))
        self.assertNotEqual(inclusion_gap, tb.Quad(t_partial))
        self.assertNotEqual(inclusion_gap, tb.Quad(h_partial))


if __name__ == "__main__":
    unittest.main()
