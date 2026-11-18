"""Four-mask native CAR program, complete analyzer and distinguishable signed source."""
from itertools import product

import sympy as sp


def require(test, label):
    if not test:
        raise ValueError(label)


def zero(matrix):
    return all(sp.expand(x) == 0 or sp.simplify(x) == 0 for x in matrix)


def main():
    p = (sp.sqrt(5) - 1)/2
    a = sp.sqrt(p)
    G = sp.Matrix([[a, -p], [p, a]])
    Z = sp.diag(1, -1)
    X = sp.Matrix([[0, 1], [1, 0]])
    J = X*Z
    L_i = sp.kronecker_product(sp.eye(2), J)
    L_j = sp.kronecker_product(J, Z)
    identity = sp.eye(4)
    require(L_i*L_j == -L_j*L_i and L_i**2 == L_j**2 == -identity, "true signed permutations")
    # The high wires of masks 0,1,14,15 are equal. Two CX turn them into
    # equal copies of the low and high labels, without reading the address.
    labels = []
    for h, low in product(range(2), repeat=2):
        mask = 14*h+low
        b3, b2, b1, b0 = ((mask >> k) & 1 for k in (3, 2, 1, 0))
        b3 ^= b1
        b3 ^= b0
        require((b3, b2, b1, b0) == (low, h, h, low), "physical CX recoding")
        labels.append((h, low))
    # Each doubled label is read after G† on both wires. Z on one of them
    # gives the common accepted amplitude -ap on 01 and 10.
    rows = {}
    for y in product(range(2), repeat=2):
        rows[y] = [(-1)**k * G[k, y[0]] * G[k, y[1]] for k in range(2)]
        if y[0] != y[1]:
            require(all(sp.simplify(x+a*p) == 0 for x in rows[y]), "common accepted row")
    require(zero(sum((sp.Matrix(x)*sp.Matrix(x).T for x in rows.values()), sp.zeros(2))-sp.eye(2)),
            "all outcomes of a single cap")
    c, b, d, clock = sp.symbols("c b d A", real=True)
    amps = [c, clock, d, b]
    role = [L_j**h * L_i**low for h, low in labels]
    unit = sum((x*g for x, g in zip(amps, role)), sp.zeros(4))
    require(zero(unit.T*unit - sum(x*x for x in amps)*identity), "quaternion normalization")
    total = [0]*4
    accepted = 0
    for left, right in product(rows, repeat=2):
        factors = [sp.simplify(rows[left][h]*rows[right][low]) for h, low in labels]
        cross = [sp.simplify(x*y) for x, y in product(factors, repeat=2)]
        require(all(sp.polys.numberfields.to_number_field(x, sp.sqrt(5)).as_expr().is_real for x in cross),
                "complete CP outcome belongs to Q(sqrt(5))")
        for i, value in enumerate(factors):
            total[i] += value**2
        if left[0] != left[1] and right[0] != right[1]:
            accepted += 1
            require(all(sp.simplify(x-p**3) == 0 for x in factors), "absolute coherent branch amplitude")
    require(accepted == 4 and all(sp.simplify(x-1) == 0 for x in total), "all sixteen leaves kept")
    prepared = unit*identity[:, 0]
    require(prepared == sp.Matrix([c, clock, d, -b]), "future address")
    # Read the rotations G vs G† in the low or high address. Division by
    # the actual slice mass is unnecessary on the unit incoming fiber.
    require(sp.simplify((a*c-p*clock)**2-(a*c+p*clock)**2+4*a*p*c*clock) == 0, "signed scalar")
    require(sp.simplify((a*clock+p*b)**2-(a*clock-p*b)**2-4*a*p*b*clock) == 0, "signed top")
    w, ell, action_plus, action_minus, scale, dc = sp.symbols("w ell Aplus Aminus scale dc", nonzero=True)
    price_difference = -ell*w*(action_plus-action_minus)
    necessary = sp.solve(price_difference-scale*dc, action_plus)[0]
    require(sp.simplify(ell*w*(necessary-action_minus)+scale*dc) == 0, "balanced signed class price")
    print("PASS 4 native labels, all 16 outcomes, fixed success 4*p^6, two signed field responses")


if __name__ == "__main__":
    main()
