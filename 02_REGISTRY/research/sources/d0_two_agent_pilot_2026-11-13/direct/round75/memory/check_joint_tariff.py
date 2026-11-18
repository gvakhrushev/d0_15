"""Complete exact Golden/truth-table accounting for the shared five-copy tariff."""
from functools import lru_cache
from fractions import Fraction as Q
from itertools import product
import json
import sympy as sp


p = sp.Symbol("p")
minimal = p*p+p-1
h = 2-p


def reduced(value):
    return sp.rem(sp.expand(value),minimal,p)


def check(test, label):
    if not test:
        raise AssertionError(label)


@lru_cache(None)
def physical_rows(flag, helper):
    # Each output type is prepared on its own wire, printed once and kept.
    b = flag and helper
    golden_or_zero = ["0" if flag else "v"]*3+["0" if b else "v"]
    one_or_zero = ["0" if flag else "1"]*8+["0" if b else "1"]
    return golden_or_zero+one_or_zero


def resources(flag, helper):
    stamp = physical_rows(flag, helper)
    # Each complete endpoint consists of a tuple of emitted bits on the 13 slots.
    free = [i for i,kind in enumerate(stamp) if kind=="v"]
    normalization = length = entropy = 0
    for digits in product((0,1), repeat=len(free)):
        assigned = dict(zip(free,digits))
        bits = [assigned[i] if kind=="v" else int(kind) for i,kind in enumerate(stamp)]
        charge = len(bits)+sum(bits)
        native_exponent = len(digits)+sum(digits)
        mass = p**native_exponent
        normalization += mass
        length += mass*charge
        entropy += mass*native_exponent
    check(reduced(normalization-1)==0,"all terminals kept")
    # The complete external Golden label reference has weight p^charge on each tuple.
    return sp.Matrix([reduced(length-entropy),reduced(entropy)])


def main():
    costs = []
    for flag in (False,True):
        # Golden helper is printed and retained in both cases, so its own
        # fixed vector can be removed from the difference.
        costs.append((1-p)*resources(flag,False)+p*resources(flag,True))
    delta = (costs[1]-costs[0]).applyfunc(reduced)
    check(delta==sp.Matrix([-5,-5]),"one physical flag removes five in both conventions")
    check(reduced(h*(3+p)-5)==0,"integer index in the Golden ring")
    check(reduced(h*h.subs(p,-1-p))==5,"norm of one complete Golden entropy in the integer ring")
    for k in range(1,41):
        coordinates = (Q(3*k,5),Q(k,5))
        check(all(x.denominator==1 for x in coordinates)==(k%5==0),"smallest possible integer transfer")
    # A moving, nonuniform finite classical archive; work is integer by label.
    t=sp.Symbol("t",real=True)
    probs=(sp.Rational(1,4)+t,sp.Rational(1,4)+t*t,sp.Rational(1,2)-t-t*t)
    tariffs=(0,2,5)
    work=sum(w*u for w,u in zip(tariffs,probs))
    for k in range(2):
        base=costs[0][k]
        suffix=sum(q*sum(base+(costs[1][k]-base)*int(w>=j) for j in range(1,6))
                   for q,w in zip(probs,tariffs))
        check(reduced(suffix+5*work-5*base)==0,"five-copy work cancels in mean at all fields")
    print(json.dumps({"admitted_classical_switch_required":True,"charged_output_slots_per_threshold":13,
                      "tariff_change_in_each_convention":-5,"smallest_integer_in_marked_golden_class":5,
                      "fixed_clock_controlled_inverse_assumed":False,"full_GR":False},sort_keys=True))


if __name__=="__main__":
    main()
