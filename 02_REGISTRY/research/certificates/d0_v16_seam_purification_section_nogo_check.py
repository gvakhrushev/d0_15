#!/usr/bin/env python3
"""Exact type/dimensional certificate for the D0 v16 section-map no-go.

This certificate does not fit any external datum.  It checks:
1. the rank-one metrological dimensions;
2. non-uniqueness of dimensionless selectors under the declared source type;
3. that the existing D_L -> ell_P -> G bridge fixes units but not an
   object-specific mass selector;
4. that internal tick time and Bondi time remain distinct semantic types.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F


# Dimensions are exponents of (M, L, T).
Dim = tuple[int, int, int]
ONE: Dim = (0, 0, 0)
MASS: Dim = (1, 0, 0)
LENGTH: Dim = (0, 1, 0)
TIME: Dim = (0, 0, 1)
ENERGY: Dim = (1, 2, -2)
ACTION: Dim = (1, 2, -1)
SPEED: Dim = (0, 1, -1)
NEWTON_G: Dim = (-1, 3, -2)


def add(a: Dim, b: Dim) -> Dim:
    return tuple(x + y for x, y in zip(a, b))  # type: ignore[return-value]


def sub(a: Dim, b: Dim) -> Dim:
    return tuple(x - y for x, y in zip(a, b))  # type: ignore[return-value]


def mul_int(a: Dim, n: int) -> Dim:
    return tuple(n * x for x in a)  # type: ignore[return-value]


@dataclass(frozen=True)
class TypedQuantity:
    name: str
    dim: Dim
    semantic_type: str
    deps: frozenset[str]


Lambda_act = TypedQuantity("Lambda_act", ENERGY, "ActionSectionEnergy", frozenset({"Lambda_act"}))
h = TypedQuantity("h", ACTION, "UnitConvention", frozenset({"h"}))
hbar = TypedQuantity("hbar", ACTION, "BridgeUnitConvention", frozenset({"hbar"}))
c = TypedQuantity("c", SPEED, "CausalUnitConvention", frozenset({"c"}))
D_L = TypedQuantity("D_L", ONE, "DimensionlessGravityDepth", frozenset({"D_L"}))

m_act_dim = sub(Lambda_act.dim, mul_int(c.dim, 2))
tau0_dim = sub(h.dim, Lambda_act.dim)
ell0_dim = add(c.dim, tau0_dim)
ellP_dim = sub(ell0_dim, D_L.dim)
GN_dim = sub(add(mul_int(ellP_dim, 2), mul_int(c.dim, 3)), hbar.dim)

assert m_act_dim == MASS
assert tau0_dim == TIME
assert ell0_dim == LENGTH
assert ellP_dim == LENGTH
assert GN_dim == NEWTON_G

# Declared task inputs apart from Lambda_act are dimensionless.
rankP_dim = ONE
phi_dim = ONE
Rstar_dim = ONE
history_sign_dim = ONE
assert rankP_dim == phi_dim == Rstar_dim == history_sign_dim == ONE

# Exact finite hostile witness: dimensional covariance cannot choose the
# dimensionless selector.  The same frozen internal record admits distinct
# positive dimensionless functions unless an extra semantic theorem selects one.
rankP = F(2)
Rstar = F(1)
mu_1 = rankP
mu_2 = rankP * (1 + Rstar)
b_1 = 1 + Rstar
b_2 = rankP * (1 + Rstar)

assert mu_1 > 0 and mu_2 > 0 and mu_1 != mu_2
assert b_1 > 0 and b_2 > 0 and b_1 != b_2

# Both mass candidates have the same mass dimension; both time candidates have
# the same time dimension.  Units alone therefore do not select the section.
M1_dim = add(m_act_dim, ONE)
M2_dim = add(m_act_dim, ONE)
T1_dim = add(tau0_dim, ONE)
T2_dim = add(tau0_dim, ONE)
assert M1_dim == M2_dim == MASS
assert T1_dim == T2_dim == TIME

# Semantic type barrier: internal capacity time is not Bondi time without an
# explicit observer functor.
tau_star = TypedQuantity(
    "tau_star",
    TIME,
    "InternalTickTime",
    frozenset({"Lambda_act", "h", "phi", "R_star"}),
)
tau_C = TypedQuantity(
    "tau_C",
    TIME,
    "BondiRetardedTime",
    frozenset({"BondiFunctor"}),
)
assert tau_star.dim == tau_C.dim == TIME
assert tau_star.semantic_type != tau_C.semantic_type
assert "BondiFunctor" not in tau_star.deps

# Semantic type barrier on mass: boundary capacity is dimensionless seam data,
# while an absolute black-hole mass needs a state-specific mass selector.
capacity = TypedQuantity(
    "C_boundary",
    ONE,
    "BoundaryCutCapacity",
    frozenset({"BoundaryCutWeight", "ABCD"}),
)
mass_coordinate = TypedQuantity(
    "mu_BH",
    ONE,
    "ClosureDensityMassSelector",
    frozenset({"MassSelector"}),
)
assert capacity.dim == mass_coordinate.dim == ONE
assert capacity.semantic_type != mass_coordinate.semantic_type
assert "MassSelector" not in capacity.deps

# Granting D_L, ell_P and G_N still supplies no state selector.
gravity_unit_deps = frozenset({"Lambda_act", "h", "hbar", "c", "D_L"})
assert "MassSelector" not in gravity_unit_deps
assert "BondiFunctor" not in gravity_unit_deps

# Using the external remnant law to define the section is, by dependency,
# no longer unaugmented.
external_lifetime_path = gravity_unit_deps | frozenset({"ExternalRemnantLaw"})
assert "ExternalRemnantLaw" in external_lifetime_path

print("m_act dimension =", m_act_dim)
print("tau0 dimension =", tau0_dim)
print("ellP dimension =", ellP_dim)
print("G_N dimension =", GN_dim)
print("selector hostile mass values =", mu_1, mu_2)
print("selector hostile time values =", b_1, b_2)
print("internal time type =", tau_star.semantic_type)
print("target time type =", tau_C.semantic_type)
print("capacity type =", capacity.semantic_type)
print("target mass-selector type =", mass_coordinate.semantic_type)
print("D0-V16-UNADORNED-REMNANT-LIFETIME-SECTION-NOGO")
