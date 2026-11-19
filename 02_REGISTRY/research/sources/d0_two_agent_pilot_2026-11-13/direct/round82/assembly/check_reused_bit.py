"""Enumerate all measured words on one reused Golden target and two fresh pointers per slot."""
from decimal import Decimal as D, getcontext
from itertools import product
import json

getcontext().prec = 75
ONE = D(1)
P = (D(5).sqrt() - 1) / 2
R = P * P
ELL = -P.ln()
TOL = D("1e-61")
LENGTH = {"00": 3, "01": 4, "10": 5}


def equal(left, right):
    if abs(left - right) > TOL:
        raise ValueError(f"Mismatch: {left} versus {right}")


def eta_for(k):
    # Each two-control addressing block gives 4 elementary rotations on the chosen sector.
    a, b = ONE, D(0)
    for _ in range(4 * k):
        a, b = a * P.sqrt() - b * P, a * P + b * P.sqrt()
    equal(a*a + b*b, ONE)
    return b*b


def entropy(values):
    return -sum(v*v.ln() for v in values if v) / ELL


def enumerate_words(n, y, eta):
    # Diagonal mass propagation for P=|11><11|. The input U is pure v.
    # On no informative read its coherence survives; the corresponding word is counted once.
    leaves = {}
    for word in product(LENGTH, repeat=n):
        u0, u1 = P, R
        for symbol in word:
            if symbol == "00":
                u0, u1 = (1-eta)*u0, (1-eta)*u1
            elif symbol == "01":
                u0, u1 = eta*u0, eta*u1*(1-y)
            else:
                u0, u1 = D(0), eta*u1*y
        if u0 + u1:
            leaves[word] = u0 + u1
    equal(sum(leaves.values()), ONE)
    return leaves


def summarize(leaves):
    price = {w: sum(LENGTH[b] for b in w) for w in leaves}
    average = sum(leaves[w]*price[w] for w in leaves)
    partition = sum(P**length for length in price.values())
    return average, entropy(leaves.values()), partition, min(price.values())


def check_last_read_and_writers(eta):
    """Selective, address-symmetric read disturbance and the W3 gates on basis controls."""
    def writer_distance(bit):
        head, t0, size = bit, 0, 0
        before = (head, t0, size)
        t0 ^= head
        middle = (head, t0, size)
        size ^= head
        after = (head, t0, size)
        return int(before != middle) + int(middle != after)

    def terminal_price(b, hit, rate):
        flags = (int(b and hit), int(not b and hit))
        cost = sum(1 + bit + rate*writer_distance(bit) for bit in (*flags, flags[0]))
        # One pointer has a nontrivial outcome. The blank pointer contributes zero.
        return cost + ((1-eta).sqrt() if hit else eta.sqrt())

    for rate in [D(0),D("0.125"),D(1),D(22).sqrt()]:
        delta = lambda hit: terminal_price(1,hit,rate) - terminal_price(0,hit,rate)
        equal(delta(True) - delta(False), 1 + 2*rate)



def main():
    h = entropy([P, R])
    equal(h, 1 + R)
    configurations = rectangles = 0
    examples = []
    for k in [1, 3]:
        eta = eta_for(k)
        check_last_read_and_writers(eta)
        for n in range(1, 8):
            low = enumerate_words(n, 0, eta)
            high = enumerate_words(n, 1, eta)
            l0, h0, z0, m0 = summarize(low)
            l1, h1, z1, m1 = summarize(high)
            equal(l0, n*(3+eta))
            equal(l1-l0, n*eta*R)
            equal(h0, n*entropy([eta,1-eta]))
            equal(h1-h0, (1-(1-eta)**n)*h)
            equal(z0, P**(2*n))
            equal(z1/z0-1, (P+P**3)**n - P**n)
            if m0 != 3*n or m1 != m0:
                raise ValueError("Minimum literal print length")
            if len(low) != 2**n or len(high) != 2**(n+1)-1:
                raise ValueError("Wrong physical supports")
            configurations += 2
            slopes = (l1-h1)-(l0-h0)
            if k == 3 and n in (1, 3, 4):
                examples.append([n, format(slopes, ".10f")])
            # Pair branches on every nonempty service mask; compare with a single hit.
            base = ("01",) + ("00",)*(n-1)
            base_hit = ("10",) + ("00",)*(n-1)
            for mask in product((0,1), repeat=n):
                m = sum(mask)
                if not m:
                    continue
                bit0 = tuple("01" if hit else "00" for hit in mask)
                bit1 = tuple("10" if hit else "00" for hit in mask)
                equal(high[bit1] / high[bit0], P)
                equal(high[bit1]*high[base]/(high[bit0]*high[base_hit]), ONE)
                ldiff = sum(LENGTH[a]-LENGTH[b] for a,b in zip(bit1,bit0))
                if ldiff - (LENGTH["10"]-LENGTH["01"]) != m-1:
                    raise ValueError("Unpaid rectangle")
                rectangles += 1
    aa = P+P**3
    # d(n+1)-d(n)=(1-P)P**n-(1-aa)*aa**n; the ratio decreases strictly.
    assert 0 < P < aa < 1
    assert (1-P)*P**2 > (1-aa)*aa**2 and (1-P)*P**3 < (1-aa)*aa**3
    assert examples[1][1].startswith("-") and not examples[2][1].startswith("-")
    print(json.dumps({"native_efficiencies": {str(k):format(eta_for(k), ".12f") for k in (1,3)},
                      "complete_trees":configurations,"nonempty_service_masks_checked":rectangles,
                      "price_minus_entropy_slope_k3":examples,
                      "best_literal_partition_contrast":{"n":3,"relative":format(aa**3-P**3, ".12f")},
                      "full_book_price_identified":False}, indent=2))


if __name__ == "__main__":
    main()
