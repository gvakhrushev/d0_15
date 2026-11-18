"""Exact H.1 centres, Golden interval codes, and complete stopped raw trees."""
from hashlib import sha256
from itertools import product
import json
import mpmath as mp


# Each pair represents x+y*p in Z[p], with p*p=1-p.
ZERO, ONE, P = (0, 0), (1, 0), (0, 1)


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def sub(a, b):
    return a[0] - b[0], a[1] - b[1]


def mul(a, b):
    x, y = a
    v, w = b
    return x * v + y * w, x * w + y * v - y * w


def power(a, n):
    result = ONE
    for _ in range(n):
        result = mul(result, a)
    return result


def sign(a):
    x, y = a
    k = 2*x-y
    if y * k >= 0:
        nonzero = k or y
        return (nonzero > 0) - (nonzero < 0)
    square_difference = k*k - 5*y*y
    return (1 if k > 0 else -1) * ((square_difference > 0) - (square_difference < 0))


def conjugate(a):
    return a[0]-a[1], -a[1]


def code_boundary(value):
    assert sign(value) >= 0 and sign(sub(ONE, value)) > 0
    invp = add(ONE, P)
    invp2 = mul(invp, invp)
    left, width, residual = ZERO, ONE, value
    digits = []
    while residual != ZERO:
        if sign(sub(residual, P)) < 0:
            digits.append(0)
            residual = mul(residual, invp)
            width = mul(width, P)
        else:
            digits.append(1)
            residual = mul(sub(residual, P), invp2)
            left = add(left, mul(width, P))
            width = mul(width, mul(P, P))
        assert add(left, mul(width, residual)) == value
        assert len(digits) < 5000
    assert left == value
    return digits


p2, p3, p4 = (power(P, i) for i in (2, 3, 4))
rho = add(p2, p4)
c = sub(add(P, P), ONE)
for _ in range(9):
    square = mul(c, c)
    c = sub(add(square, square), ONE)
Q = mul(add(power(P, 7), power(P, 7)), sub(ONE, c))
q = add(p2, mul(p3, Q))
assert sign(sub(ZERO, conjugate(q))) > 0
assert sign(sub(sub(ZERO, conjugate(q)), (10**473, 0))) > 0

targets = {}
mp.mp.dps = 1200
p = (mp.sqrt(5)-1)/2
for name, target in (("canonical_birth", p2), ("source_i_true_cold", rho),
                     ("SC6_sharp", Q), ("H1_noisy", q)):
    code = code_boundary(target)
    value = target[0]+target[1]*p
    envelope = {}
    for cutoff in (12, 24, 48, 96):
        mass = p**3+(1-p**3)*p**(2*cutoff)
        left_coin = p**4/mass
        width, left = mp.mpf(1), mp.mpf(0)
        for digit in code:
            if digit:
                left += width*left_coin
            width *= (1-left_coin) if digit else left_coin
        error = abs(left-value)
        assert error <= len(code)*abs(left_coin-p)+mp.mpf("1e-1000")
        envelope[cutoff] = mp.nstr(error, 7)
    digits = ''.join(str(d) for d in code)
    targets[name] = {"q": mp.nstr(value, 18), "fixed_count_of_logical_coins": len(code),
                     "threshold_sha256": sha256(digits.encode()).hexdigest(),
                     "threshold_bits": digits, "error_at_raw_cutoffs": envelope}

def two_clock_digits(value):
    inv_a = power(add(ONE, P),2)
    remainder = mul(value,inv_a)
    seen, digits = {}, []
    while len(digits) < 5000:
        k = len(digits)
        if k >= 2 and sign(sub((3,0),remainder)) > 0:
            if remainder in seen:
                start = seen[remainder]
                return digits[:start], digits[start:]
            seen[remainder] = k
        d = 0
        while d < k+1 and sign(sub(remainder,(d+1,0))) >= 0:
            d += 1
        digits.append(d)
        remainder = mul(sub(remainder,(d,0)), inv_a)
    raise ValueError("missing periodic code for tested algebraic input")


def series(digits, weight):
    total = ZERO
    for d in digits:
        total = add(total,mul((d,0),weight))
        weight = mul(weight,p2)
    return total,weight


two_clocks = {}
for name, target in (("canonical_birth",p2),("source_i_true_cold",rho),
                     ("SC6_sharp",Q),("H1_noisy",q)):
    prefix, cycle = two_clock_digits(target)
    before, next_weight = series(prefix,p2)
    tail,_ = series(cycle,next_weight)
    divisor = sub(ONE,power(p2,len(cycle)))
    assert mul(sub(target,before),divisor) == tail

    def digit(k):
        return prefix[k] if k < len(prefix) else cycle[(k-len(prefix)) % len(cycle)]

    rows = {}
    q_value = target[0]+target[1]*p
    for cutoff in (4,12,24,48,96):
        yes = mp.mpf(0)
        weight = p**8
        # For k=i+j, admissible i is in [max(0,k-L+1),min(L-1,k,d_k-1)].
        for k in range(2*cutoff-1):
            lo = max(0,k-cutoff+1)
            hi = min(cutoff-1,k,digit(k)-1)
            yes += max(0,hi-lo+1)*weight
            weight *= p**2
        mass = p**3+(1-p**3)*p**(2*cutoff)
        report = yes/mass**2
        error = q_value-report
        assert -mp.mpf("1e-1000") <= error <= 2*p**(2*cutoff-3)
        z = (p**2+p**4)*mass**2 + (1-p**2-p**4)*yes
        assert z >= p**6*(p**2+p**4)
        rows[str(cutoff)]={"q_error":mp.nstr(error,9),"true_absolute_mass":mp.nstr(z,13)}
    two_clocks[name]={"preperiod_length":len(prefix),"period_length":len(cycle),
                      "preperiod_digits":prefix,"repeated_digits":cycle,"caps":rows}

# Separate independent enumeration of ALL microscopic paths, preserving times and timeouts.
audited = 0
for cutoff in (1, 2, 3, 4):
    micro = [("0"*(j-1)+"1", int(j>1), power(P, 2*j+2)) for j in range(1, cutoff+1)]
    micro.append(("0"*cutoff, 1, power(P, 2*cutoff)))
    total = ZERO
    for _, _, weight in micro:
        total = add(total, weight)
    assert total == add(p3, mul(sub(ONE,p3), power(P,2*cutoff)))
    for depth in (1, 2, 3):
        boundary = (1 << depth)//2+1
        raw_mass = ZERO
        yes_mass = ZERO
        paid = ZERO
        for history in product(micro, repeat=depth):
            word = 0
            value = ONE
            for _, bit, weight in history:
                word = 2*word+bit
                value = mul(value, weight)
            raw_mass = add(raw_mass, value)
            if word < boundary:
                yes_mass = add(yes_mass,value)
                paid = add(paid,value)
                audited += 1
            else:
                paid = add(paid,add(mul(value,p2), mul(value,p4)))
                audited += 2
        assert raw_mass == power(total, depth)
        assert paid == add(mul(raw_mass, rho),mul(sub(ONE,rho),yes_mass))

# A genuinely complete equal-depth raw register has a different outcome law.
raw_escort = p**4/(p**2+p**4)
assert abs(raw_escort-p**2) > mp.mpf("0.1")
print(json.dumps({"status": "PASS", "full_micro_leaves_counted": audited,
                  "raw_tree_convention": "one quadratic read on all orthogonal terminal histories",
                  "first_hit_total_in_limit": "p^3", "normalised_early_late": ["p","p^2"],
                  "retained_extra_split_factor": "p^2+p^4", "H1_targets": targets,
                  "two_clock_codes":two_clocks,
                  "uniform_two_clock_full_mass_floor":"p^6*(p^2+p^4)",
                  "complete_Book03_source_binding": False}, indent=2))
