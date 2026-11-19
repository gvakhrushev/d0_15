"""Check signed radix pricing with all attenuator outcomes retained."""
import hashlib
import json
import sys
from fractions import Fraction as Q
from pathlib import Path

PILOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PILOT / "open/round156"))
import check_fixed_parity_tariff as previous

I, O = previous.I, previous.O
add, scale, sign = previous.add, previous.scale, previous.sign
PINS = {
    "open/round156/check_fixed_parity_tariff.py":
        "00d07b8e76237bde04faf13c0771262d4b7a70415af4706f828510dfd420cfdf",
    "open/round156/RESULT.json":
        "ed3cb99c5d6e67003d4022016d2fd61edc236464a755d65c377f6e6548ffefdb",
    "direct/round78/clock/BLANK_CONFIRMATION_RU.md":
        "65e37fff5ff3433139e18ced7c6ceda8b58a0c31e9aab2563e14fb4bdc896a77",
}
RADIX = previous.DELTA_ONE
ANCHORS = {1: previous.DELTA_ONE, 6: previous.DELTA_SIX}


def multiply(left, right):
    a, b = left
    c, d = right
    return a*c+b*d, a*d+b*c-b*d


def digits(value, tolerance):
    O.require(tolerance > 0, "positive tolerance")
    k = 1 if value >= 0 else 6
    remaining = (abs(value), 0)
    magnitude = scale(ANCHORS[k],sign(ANCHORS[k]))
    level = 0
    while sign(add(remaining,(tolerance,0),-1)) > 0:
        count = previous.floor_ratio(remaining,magnitude)
        if level:
            O.require(count <= 4, "fractional radix digit")
        if count:
            yield k,level,count
        remaining = add(remaining,magnitude,-count)
        level += 1
        magnitude = multiply(magnitude,RADIX)


def compile_table(target, tolerance):
    size = len(target)
    O.require(size >= 2 and size & (size-1) == 0 and tolerance > 0, "binary table")
    for mask in range(1,size):
        c = -2*sum((Q(v)*(1-2*previous.parity(mask,word))
                    for word,v in enumerate(target)),Q(0))/size
        for k,noise,count in digits(c,tolerance/(size-1)):
            yield mask,k,noise,count


def scaled_anchor(k, noise):
    a = ANCHORS[k]
    for _ in range(noise):
        a = multiply(a,RADIX)
    return a


def sum_relative(plan, word):
    value = (0,0)
    for mask,k,noise,count in plan:
        if previous.parity(mask,word):
            value = add(value,scaled_anchor(k,noise),count)
    return value


def confirmation(probability, model):
    if model == "literal":
        return I(0.)
    if model == "registered":
        return I(2.)-probability
    O.require(model == "coherent" and probability.lo > .25, "coherent branch formula")
    return probability.sqrt()+(3*(I(1.)-probability)).sqrt()


def raw_gain(r, calibration, model, logphi):
    r0 = I(1.)-r
    h = -(r0*O.logarithm(r0)+r*O.logarithm(r))/logphi
    c0 = 1+calibration*confirmation(r0,model)
    c1 = 2+calibration*confirmation(r,model)
    diff = c1-c0
    return O.logarithm(r0)/logphi+2*h-r*diff, O.logarithm(r)/logphi+2*h+r0*diff


def check_gains(p, rates):
    logphi = -O.logarithm(p)
    contrast = p*p.square()
    result = {}
    for model, level, cal in (("literal","none",I(0.)),
                             ("registered","unit",I(1.)),
                             ("registered","sqrt22",I(22.).sqrt()),
                             ("coherent","unit",I(1.)),
                             ("coherent","sqrt22",I(22.).sqrt())):
        auxiliary = min(float((g-p*(1+contrast)).lo)
                        for g in raw_gain(p.square(),cal,model,logphi))
        terminal = [min(float(g.lo) for r in (rate,I(1.)-rate)
                        for g in raw_gain(r,cal,model,logphi)) for rate in rates]
        O.require(auxiliary > .19 and min(terminal) > .1458,
                  "all true fine outcomes and confirmation prices")
        result[model+"_"+level] = {"scratch_lower":auxiliary,"target_lower_by_anchor":terminal}
    return result


def check_shared_routes():
    target_levels = (0,1,2,3)
    for f in (0,1):
        for helper in (0,1):
            for scratch in range(8):
                bits = [(scratch >> i) & 1 for i in range(3)]
                for initial in range(16):
                    target = [(initial >> i) & 1 for i in range(4)]
                    before = target[:]
                    u = helper
                    for i in range(len(target)):
                        target[i] ^= u
                    u ^= f
                    for i in range(len(target)):
                        target[i] ^= u
                    u ^= f
                    prefix = bits[:]
                    for i in range(1,3):
                        prefix[i] ^= prefix[i-1]
                    for i,level in enumerate(target_levels):
                        if level:
                            target[i] ^= prefix[level-1]
                    for i in (2,1):
                        prefix[i] ^= prefix[i-1]
                    O.require(u == helper and bits == prefix, "exact raw control return")
                    for i,level in enumerate(target_levels):
                        O.require(target[i] == before[i]^f^(sum(bits[:level]) % 2),
                                  "actual CNOT routes")
    return 512


def resource_example(target,tolerance):
    plan = list(compile_table(target,tolerance))
    for word,price in enumerate(target):
        error = add(sum_relative(plan,word),(price-target[0],0),-1)
        O.require(sign(add(error,(tolerance,0),-1)) < 0
                  and sign(add(error,(tolerance,0))) > 0,"exact full table approximation")
    terminals = sum(count for _,_,_,count in plan)
    maxima = {mask:max(level for other,_,level,_ in plan if mask == other)
              for mask,_,_,_ in plan}
    scratch = sum(maxima.values())
    # One shared actually registered work bit, returned after every A/B pair.
    golden_letters = 1+scratch+sum(k*count for _,k,_,count in plan)
    cx_letters = 2*sum(bin(mask).count("1") for mask in maxima)+2*terminals
    cx_letters += 2*sum(max(0,r-1) for r in maxima.values())
    cx_letters += sum(count for _,_,level,count in plan if level)
    raw = 1+terminals+scratch
    return {"terminal_pointers":terminals, "registered_scratch_bits":scratch,
            "borrowed_registered_bit":1,"G_including_births":golden_letters,"CX":cx_letters,
            "raw_coin_registrations":raw,"max_literal_0_10_slots":2*raw,
            "G_CX_plus_literal_slot_upper":golden_letters+cx_letters+2*raw}


def main():
    for path,digest in PINS.items():
        O.require(hashlib.sha256((PILOT/path).read_bytes()).hexdigest() == digest,"source pin")
    p, *_ = previous.strong.physical_site()
    gains = check_gains(p,list(previous.check_short_words(p)))
    tolerance = previous.PRECISION
    target = [Q(7,8)+3*((x&3)==3)-2*((x&6)==6)+Q(11,7)*(x==5) for x in range(8)]
    # Uniform depth for rounding a coefficient of either sign in the
    # rationalized 199-bit table; leading repeated cells are separate.
    unit = Q(1,1)
    widest = tolerance/(2*(2**199-1))
    max_level = max(level for value in (unit,-unit)
                    for _,level,_ in digits(value,widest))
    # A uniform analytic maximum also covers zero digits at deeper places.
    remaining = ANCHORS[1]
    analytic_level = 0
    while sign(add(remaining,(widest,0),-1)) > 0:
        remaining = multiply(remaining,RADIX)
        analytic_level += 1
    O.require(max_level <= analytic_level,"bound for all fractional expansions")
    b156 = json.loads((PILOT/"open/round156/RESULT.json").read_text())
    epsilon = I.rational(Q(1,100))
    logphi = -O.logarithm(p)
    old_factor = I.rational(Q(1,100))/logphi-2*epsilon
    O.require(old_factor.lo > .00078, "old and B155 gains under .01 uniform error")
    source_error = I(b156["raw_A76_moving_probability_l1_upper"])*epsilon
    tight_margin = I(b156["B155_crossing_margin_lower_for_compiled_literal_price"])-source_error
    O.require(tight_margin.lo > .00103027, "depth-one gain after wider quantization")
    proof_routes = check_shared_routes()
    print(json.dumps({
        "round":"B157",
        "pinned_source_hashes":PINS,
        "full_raw_confirmed_gain_bounds":gains,
        "fixed_three_bit_example_error_1e_10":resource_example(target,tolerance),
        "fixed_three_bit_example_error_0_01":resource_example(target,Q(1,100)),
        "B156_comparison_terminal_count_error_1e_10":b156["truth_table_example_bank_count"],
        "shared_CX_truth_table_inputs":proof_routes,
        "retained_old_gain_coefficient_at_error_0_01":float(old_factor.lo),
        "directional_error_for_uniform_pointwise_error_0_01_upper":float(source_error.hi),
        "max_fractional_place_for_each_199_bit_coefficient":analytic_level,
        "B155_crossing_margin_lower_under_literal_and_symmetric_bank_confirmation":
            float(tight_margin.lo),
        "full_physical_clock_prices_and_classes_selected":False,
        "GR_closed":False,
    },sort_keys=True,indent=2))


if __name__=="__main__":
    main()
