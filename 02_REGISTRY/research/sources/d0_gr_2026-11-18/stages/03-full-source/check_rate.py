"""All paid terminal histories of a chain of exact two-read trials."""
from fractions import Fraction as F
import json
import sympy as sp


def enumerate_trials(rounds, x, nu, alpha, penalty):
    failures = ((1 - x) ** 2, x * (1 - x), x * (1 - x))
    through = F(1)
    leaves = []
    for _ in range(rounds):
        for probability in failures:
            weight = (through * probability) ** nu * alpha ** (penalty * rounds)
            leaves.append((through * probability, weight))
        through *= x * x
    leaves.append((through, through ** nu))
    assert sum(p for p, _ in leaves) == 1
    return leaves


verified = 0
for rounds in range(1, 9):
    for x in (F(5, 8), F(2, 3), F(3, 4)):
        for nu in (1, 2):
            alpha = F(5, 9)
            leaves = enumerate_trials(rounds, x, nu, alpha, 4)
            a = x ** (2 * nu)
            b = (1 - x) ** (2 * nu) + 2 * (x * (1 - x)) ** nu
            target = a ** rounds + alpha ** (4 * rounds) * b * (1 - a ** rounds) / (1 - a)
            assert sum(w for _, w in leaves) == target
            assert len(leaves) == 3 * rounds + 1
            verified += len(leaves)

# Exact derivatives for moving preparation, raw field signal, and moving failure tariff.
y = sp.Symbol('y')
x = (2 + y) / 3
alpha = (1 + y) / 2
preparation = sp.exp(-3 * y)
nu = 2
a = x ** (2 * nu)
b = (1 - x) ** (2 * nu) + 2 * (x * (1 - x)) ** nu
rows = []
for rounds in (1, 2, 4, 8, 16, 32):
    relative = (alpha ** 6 / a) ** rounds * b * (1 - a ** rounds) / (1 - a)
    raw = preparation * a ** rounds * (1 + relative)
    slope = (raw.diff(y) / raw / rounds).subs(y, 0)
    target = (a.diff(y) / a + preparation.diff(y) / preparation / rounds).subs(y, 0)
    error = abs(slope - target)
    assert error <= 20 * F(81, 1024) ** rounds
    rows.append({"rounds": rounds, "normalised_slope": float(slope),
                 "error_after_exact_prefix": float(error)})
assert rows[-1]["error_after_exact_prefix"] < 1e-32

# An independently moving price per successful block survives division by length.
k = sp.exp(-7 * y)
assert sp.simplify((k * a).diff(y) / (k * a) - a.diff(y) / a) == -7
print(json.dumps({"status": "PASS", "exact_positive_ledger_leaves": verified,
                  "moving_price_examples": rows, "uncancelled_price_per_block": -7,
                  "physical_absorption_from_Book03_established": False}, indent=2))
