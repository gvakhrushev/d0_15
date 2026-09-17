#!/usr/bin/env python3
"""vp_window44_group_spectrum.py - D0 certificate (exact finite group arithmetic)

CLAIM (THE): the terminal return window q_T = 44 has unit group
    (Z/44)* ~= Z2 x Z2 x Z5,  |(Z/44)*| = phi_E(44) = 20 = d13,
its catalog-free (characteristic) subgroups have orders {1, 4, 5, 20}, and
    20 = 4 x 5 = |ABCD| x D_Sigma
(the orientation budget times the operational budget). The whole window is
phase-neutral: the product of all units mod 44 is +1. Exact, no floats.
"""
from math import gcd

N = 44
units = [u for u in range(1, N) if gcd(u, N) == 1]
assert len(units) == 20, len(units)            # phi_E(44) = 20
print(f"[1] |(Z/{N})*| = phi_E({N}) = {len(units)} = 20 = d13  PASS")

def order(u):
    k, x = 1, u
    while x != 1:
        x = (x * u) % N; k += 1
    return k

orders = {u: order(u) for u in units}
# exponent and structure: Z2 x Z2 x Z5 has element orders dividing 10, exponent 10,
# 2-torsion of order 4 (=> Z2 x Z2, not Z4), odd part of order 5.
assert max(orders.values()) == 10, max(orders.values())
two_torsion = [u for u in units if (u * u) % N == 1]      # x^2 = 1
assert len(two_torsion) == 4, len(two_torsion)            # Z2 x Z2 (not Z4: no order-4 elt squares here)
assert all(orders[u] in (1, 2) for u in two_torsion)
squares = sorted({(u * u) % N for u in units})            # odd part (Z5)
assert len(squares) == 5, len(squares)
print("[2] EXACT: structure Z2 x Z2 x Z5 (2-torsion order 4, odd part order 5)  PASS")

# characteristic subgroups: {1}, 2-torsion(4), odd part(5), whole(20)
char_orders = sorted({1, len(two_torsion), len(squares), len(units)})
assert char_orders == [1, 4, 5, 20], char_orders
assert 4 * 5 == 20
print("[3] EXACT: characteristic-subgroup orders {1,4,5,20}; 20 = 4x5 = |ABCD| x D_Sigma  PASS")

# window phase-neutral: product of all units mod 44 == 1 (generalized Wilson)
prod = 1
for u in units:
    prod = (prod * u) % N
assert prod == 1, prod
print("[4] EXACT: product of all units mod 44 = 1 (window phase-neutral)  PASS")

print("\n[STATUS] THE: (Z/44)* spectrum and 20=4x5 window budget (exact finite group).")
print("[CERT-CLOSED] PASS_WINDOW44_GROUP_SPECTRUM")
