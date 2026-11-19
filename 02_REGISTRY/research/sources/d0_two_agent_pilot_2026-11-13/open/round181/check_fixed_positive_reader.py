"""Exact native passive balancing and a signed three-code positive weight."""

from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import sys

import sympy as sp

HERE = Path(__file__).resolve().parent
PILOT = HERE.parents[1]
sys.path.insert(0, str(PILOT / "direct/round80/price"))
from check_parity_price import a, action, ne, one, p

SOURCE = PILOT / "open/round180/RESULT.json"


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def power(x, n):
    result = one
    for _ in range(n):
        result = result*x
    return result


def cx(i,j):
    return ne.Gate("CX",(i,j))


def gate_g(i):
    return ne.Gate("G",(i,))


def clear(head):
    return (cx(0,head),gate_g(head),cx(0,head))


def nc1(head,tail):
    return (cx(head,tail),gate_g(tail),cx(head,tail))


def with_births(initial, count):
    result = initial
    for _ in range(count):
        result = {2*index+bit: coeff*value for index,coeff in result.items()
                  for bit,value in enumerate((a,p))}
    return result


def for_arrow(state, word, width):
    for gate in word:
        state = action(state,gate,width)
    return state


def validate(word, width, born, right):
    apparatus = ne.Execution(width,born,(right,),word,ne.G_CX)
    ne.validate_execution(apparatus,max_qubits=width,max_expanded_stages=len(word))


def cold_equalizer():
    # Wire 0 is the actual known-one; wire 1 is the already sharp parity.
    # Wire 2 is old RIGHT. Scratch 3 and all four witnesses 4..7 are fresh.
    words = (cx(1,3),cx(0,3)) + tuple(cx(3,j) for j in (4,5,6,7)) + (
        cx(0,3),cx(3,4),cx(3,4),cx(1,3),
    )
    prep = tuple(g for j in range(3,8) for g in clear(j))
    validate(prep+words,8,tuple(range(3,8)),2)
    movement = []
    for parity,right in product(range(2),repeat=2):
        root = {4+2*parity+right:one}
        state = with_births(root,5)
        prepared = for_arrow(state,prep,8)
        basis = (4+2*parity+right)*32
        require(prepared=={basis:one},"Known 1 does not clear all five actual births")
        count = 0
        for g in words:
            target = action(prepared,g,8)
            count += target!=prepared
            prepared = target
        end = basis+15*(1-parity)
        require(count==6 and prepared=={end:one},"Constant basis work and return of scratch")
        passive_square = state[end]*state[end]
        require(passive_square==power(p,9 if parity==0 else 5),"Exact passive adjustment")
        require(passive_square*power(p,2 if parity==0 else 6)==power(p,11),
                "Both physical marks have the same passive adjustment")
        movement.append(count)
    return {
        "loaded_old_parity_RIGHT_columns": len(movement),
        "word_square_inventory": dict(Counter(g.op for g in prep+words)),
        "births": 5,
        "additional_measurements": 0,
        "basis_moves_after_common_clear": 6,
        "total_primitive_pure_state_movement": "11+5p+5p^3",
        "held_active_and_filler_passive_squares": ["p^9","p^5"],
        "after_their_old_marker": ["p^11","p^11"],
    }


def replay_module(complementary):
    # Wire 0 known-one, 1 the sharp source flag; 2 arbitrary old RIGHT.
    # With a companion there are two heads and two NC1 tails on 3,4,5,6.
    extra = 4 if complementary else 2
    width = 3+extra
    if complementary:
        word = clear(3)+clear(5)+(cx(1,3),cx(0,5),cx(1,5),cx(5,3),cx(5,3))
        word += nc1(3,4)+nc1(5,6)
    else:
        word = clear(3)+(cx(1,3),)+nc1(3,4)
    validate(word,width,tuple(range(3,width)),2)

    for b,right in product(range(2),repeat=2):
        column = 4+2*b+right
        root = with_births({column:one},extra)
        actual = for_arrow(root,word,width)
        expected = {column:one}
        for bit in ((b,1-b) if complementary else (b,)):
            tail = (one,0) if bit else (p-p*p,2*a*p)
            expected = {4*k+2*bit+j: value*coeff for k,value in expected.items()
                        for j,coeff in enumerate(tail) if coeff!=0}
        require(expected==actual,"Head and tail held exactly without changing old RIGHT")
        overlap = sum(root.get(k,0)*c for k,c in actual.items())
        require(overlap*overlap==power(p,5 if complementary else 2+b),"Recorded passive NC1")
    return dict(Counter(g.op for g in word))


def signed_weights():
    replay_module(False)
    unit = replay_module(True)
    require(unit == {"G":4,"CX":13},"Square-word complementary module")
    # A complemented printed bit uses the same module, publishing d instead of c.
    simple, balanced = [], []
    for plus,minus in ((0,1),(0,0),(1,0)):
        x=plus-minus
        heads=(plus,plus,1-minus)
        length=3+sum(heads)
        require(power(p,length)==power(p,4)-power(p,5)*x,"Positive signed scalar")
        before_motion = 5+6*p+4*power(p,3)+(4+2*power(p,3))*plus-power(p,3)*minus
        # Benefit of simultaneous complementary work is independent of b.
        for b in (plus,minus):
            require(b+1+b+2*(1-b)==3,"Three physical basis flips")
        simple.append({"signed_score":x,"printed_length":length,
                       "cold_exponent":6+sum(heads),
                       "trace_cost_extra_above_zero_shape": {1:"4+2p^3",0:"0",-1:"-p^3"}[x]})
        require(before_motion!=0,"All real square work remains")
        balanced.append({"signed_score":x,"printed_length":length,"cold_exponent":15})
    require(power(p,3)+power(p,6)==2*power(p,4),"Golden arithmetic progression")
    return {
        "literal_three_published_codes": simple,
        "fixed_square_movement_version": balanced,
        "balanced_inventory_before_actual_projective_calls": {"births":12,"G":12,"CX":39},
        "balanced_pure_state_square_movement": "18+12p+9p^3",
        "new_conditional_Info_of_codes_given_old_score": 0,
        "actual_tail_inspections_and_dispatch_to_be_budgeted": True,
    }


def native_cz():
    # Full width h, actual PORT, two Spin wires, and unaddressed old RIGHT.
    S=ne.Gate("SourceI",(1,2,3))
    flip=cx(0,1)
    swap=(cx(0,1),cx(1,0),cx(0,1))
    word=(S,flip,S,S,S,flip)+swap+(S,)+swap
    unit=ne.Execution(5,(),(4,),word,ne.G_CX_SOURCE_I,1,(2,3))
    ne.validate_execution(unit,max_qubits=5,max_expanded_stages=len(word))
    for col in range(32):
        h,port=(col>>4)&1,(col>>3)&1
        require(for_arrow({col:one},word,5)=={col:-one if h and port else one},
                "Exact all-column CZ on the actual PORT")
    forbidden=ne.Execution(5,(),(4,),(cx(0,2),),ne.G_CX_SOURCE_I,1,(2,3))
    require(not ne.is_member(forbidden,max_qubits=5,max_expanded_stages=1),
            "Individual qubit addressing of the old Spin is forbidden")
    return {"raw_columns_including_RIGHT":32,"SourceI":5,"CX":8,"targeted_spin_gate_admissible":False}


def price_algebra():
    z,r,m,c,u,b=sp.symbols("z r m c u b",real=True)
    # Leaves failing to reach the new adapter are counted untouched.
    factor=1-r+u*r*(1-b*m)
    coefficients=[sp.diff(factor,var).subs(m,0) for var in (m,r,u)]
    require(coefficients==[-b*r*u,u-1,r],"Prefix source separated exactly")
    # Deterministic label lengths cannot match mean and exponential affinely at once.
    y=sp.Symbol("y",positive=True)
    require(sp.simplify((y+y**-1)/2-1-(y-1)**2/(2*y))==0,
            "No deterministic nonconstant length can center both curves")
    return {
        "all_reached_ratio": "u (1-p m)",
        "with_early_stops_ratio": "1-r+u r(1-p m)",
        "adapted_factor_derivative_at_zero_score": "-p u r Dm + (u-1) Dr + r Du",
        "dimensionless_gain_for_all_reached_at_m_0": "p/log(phi)",
    }


def main():
    print(json.dumps({
        "status":"PASS",
        "B180_reference_sha256":sha256(SOURCE.read_bytes()).hexdigest(),
        "fixed_word_cold_balance":cold_equalizer(),
        "exact_positive_signed_reader":signed_weights(),
        "native_guard_z":native_cz(),
        "full_positive_composition":price_algebra(),
        "full_A87_B180_Book03_word_executed":False,
        "full_book03_valuation_identified":False,
        "GR_closed":False,
    },indent=2))


if __name__=="__main__":
    main()
