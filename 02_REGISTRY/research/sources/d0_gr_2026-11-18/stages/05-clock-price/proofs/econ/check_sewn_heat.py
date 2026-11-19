#!/usr/bin/env python3
"""An actual equal-inventory native counterexample to reconstructing full RAW heat from terminal sewing."""
import argparse
import importlib.util
import json
import math
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path
import sympy as sp


def require(condition, explanation):
    if not condition:
        raise ValueError(explanation)


def load_native(path):
    spec = importlib.util.spec_from_file_location("owned_native_gates", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def checked_words(native):
    addresses = dict(A=(0,1), B=(1,2), C=(2,0))
    words = ["AABBCC", "ABCBCA"]
    require(Counter(words[0]) == Counter(words[1]), "exact native gate/address inventory")
    swap = sp.zeros(8)
    for col in range(8):
        row = ((col & 4) >> 1) | ((col & 2) << 1) | (col & 1)
        swap[row, col] = 1
    v = sp.Matrix([native.A, native.P])
    vvv = sp.kronecker_product(v, v, v)
    for word, target in zip(words, [sp.eye(8),swap]):
        gates = tuple(native.Gate("CX",addresses[letter]) for letter in word)
        hardware = native.Execution(3, (), (), gates)
        U = native.word_matrix(hardware)
        require(U == target, "all columns of " + word)
        require(U*vvv == vvv, "identical full terminal vector " + word)
    return words


def clock_cycles(choice):
    # Internal CNOTs act between births. Their stage frames move their
    # product to the last gate in that block, as in ST1. Frames on every
    # birth boundary are unchanged. In the identical (v,w) basis on each
    # wire a SWAP is still the permutation of the two indicated wires.
    stages = []
    birth_after = []
    wires = 0
    for swap in choice:
        start = wires
        for _ in range(3):
            stages.append(("birth",wires,None))
            wires += 1
            birth_after.append(len(stages))
        for t in range(6):
            stages.append(("work",wires,start if swap and t == 5 else None))
    states = {(j, bits) for j, (_, width, _) in enumerate(stages)
              for bits in range(2**width)}
    permutation = {}
    for j,source_bits in states:
        bits = source_bits
        kind,width,swap = stages[j]
        if swap is not None:
            left,right = width-1-swap, width-2-swap
            if (bits >> left ^ bits >> right) & 1:
                bits ^= (1<<left) | (1<<right)
        if kind == "birth":
            permutation[j,source_bits] = (j+1, bits<<1)
            continue
        if j+1 < len(stages):
            dest = (j+1, bits)
        elif bits == 0:
            dest = (0,0)
        else:
            trailing = (bits & -bits).bit_length()-1
            latest = width-1-trailing
            dest = (birth_after[latest], bits>>trailing)
        permutation[j,source_bits] = dest
    require(set(permutation)==states and set(permutation.values())==states, "full G5 unitarity")
    remaining = states.copy()
    cycles = []
    while remaining:
        start = next(iter(remaining))
        at = start
        count = 0
        while at in remaining:
            remaining.remove(at)
            at = permutation[at]
            count += 1
        require(at == start, "clock closes")
        cycles.append(count)
    return Counter(cycles)


def difference(old,new):
    return Counter({k:old[k]-new[k] for k in old.keys()|new.keys() if old[k]!=new[k]})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--native",type=Path, default=Path(__file__).with_name("native_execution.py"))
    args = parser.parse_args()
    words = checked_words(load_native(args.native))
    baseline = clock_cycles([0])
    swapped = clock_cycles([1])
    require(baseline==Counter([9,8,7,7,6,6,6,6]),"one-block identity spectrum")
    require(swapped==Counter([9,15,7,12,6,6]),"one-block swap spectrum")
    clocks = {(a,b):clock_cycles([a,b]) for a in [0,1] for b in [0,1]}
    calc_A = Counter({16:1,17:1,15:2,33:-1,30:-1})
    calc_B = Counter({7:8,8:8,6:16,15:-8,12:-8})
    for bit in [0,1]:
        require(difference(clocks[0,bit],clocks[1,bit])==calc_A,"early cycles independent of later choice")
        require(difference(clocks[bit,0],clocks[bit,1])==calc_B,"late cycles independent of earlier choice")
    dimension = sum(k*v for k,v in clocks[0,0].items())
    require(dimension==495,"entire growing clock")
    # CT5/CT6; 3/4<beta=2p²<4/5 and exp(-beta)>1/3.
    def a_lower(n):
        return Fraction(13,3)*Fraction(3,88)**n/math.factorial(n)
    early_lower = 60*a_lower(15)
    late_lower = 8*24*a_lower(6)
    mixed_lower = early_lower*late_lower/(425*dimension)**2
    require(mixed_lower>0, "strict mixed source on two real finite settings")
    print(json.dumps({
      "status":"PASS", "words":words, "swap_wires":[0,1], "gates_per_word":6,
      "births_per_word":3, "same_address_inventory":True, "same_prepared_isometry":True,
      "one_block_cycle_lengths":[sorted(baseline.elements()),sorted(swapped.elements())],
      "one_block_hodge_modes":425*55,"two_block_hodge_modes":425*dimension,
      "two_block_clock_histograms":{str(a)+str(b):dict(sorted(c.items())) for (a,b),c in clocks.items()},
      "mixed_heat_finite_difference_sign":-1, "strict_abs_mixed_lower_at_beta_2p2":str(mixed_lower),
      "approx_lower_scientific":f"{float(mixed_lower):.4e}",
      "scope":"Entire selected RAW heat and feedback. Terminal input isometries only. No physical Book Cost-Info or Einstein-source identification."
    }, indent=2))


if __name__=="__main__":
    main()
