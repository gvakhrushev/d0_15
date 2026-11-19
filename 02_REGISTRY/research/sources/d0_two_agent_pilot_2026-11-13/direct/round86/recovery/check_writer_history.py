"""Fine service histories of the two actual L=4 calibrated F5/F6 CAR writers."""
from itertools import product
import json
import mpmath as mp


iv = mp.iv
iv.dps = 90
mp.mp.dps = 90
ONE = iv.mpf(1)
p = (iv.sqrt(5) - 1) / 2
ell = -iv.ln(p)
a = iv.sqrt(p)
theta = iv.atan2(p, a)


def require(ok, msg):
    if not ok:
        raise ValueError(msg)


def inside(x, lo, hi):
    require(x.a > iv.mpf(lo) and x.b < iv.mpf(hi), f"outside ({lo}, {hi}): {x}")


def show(x):
    return mp.nstr(mp.mpf(x.mid), 18)


def ready(s, cap):
    return 1 - (1-s)**cap


def reg_weight(s, digits, cap):
    """Sum P p^length over fine successes, with NC1 words 0 and 10."""
    t = (1-s) * p**digits
    return s * p**(digits+1) * (1-t**cap) / (1-t)


def enumerate_short(s, digits, cap):
    """Each reached round is recorded. The two X signs are distinct."""
    outcomes = [((0,)*digits, 1-s)]
    if digits == 1:
        outcomes.append(((1,), s))
    else:
        outcomes.extend([((0, 1), s/2), ((1, 0), s/2)])
    reached = [((), ONE)]
    successful = []
    for _ in range(cap):
        new = []
        for prefix, prob in reached:
            for next_bits, chance in outcomes:
                row = prefix+next_bits, prob*chance
                (successful if any(next_bits) else new).append(row)
        reached = new
    def sum_weight(rows):
        return sum(q*p**(len(bits)+sum(bits)) for bits,q in rows)
    inside(abs(sum_weight(successful)-reg_weight(s, digits, cap)), "-1e-70", "1e-70")
    inside(abs(sum_weight(reached)-((1-s)*p**digits)**cap), "-1e-70", "1e-70")


def endpoints(amplitude):
    """Apply the source CX to the occupied columns, summing both CAR modes."""
    cosine = [1, 0, -1, 0]
    sine = [0, 1, 0, -1]
    clicks = []
    for axis in (0, 1):
        mass = 0
        for cell in product(range(4), repeat=4):
            n = cell[axis]
            other = (n+2*(axis == 1)) % 4
            mass += p**3 * amplitude**2 * (
                (cosine[n]-cosine[other])**2 + (sine[n]-sine[other])**2)
        clicks.append(mass / 256)
    require(clicks[0] == 0, "dark endpoint")
    inside(abs(clicks[1]-4*p**3*amplitude**2), "-1e-70", "1e-70")
    return clicks[1]


def old_address_test(amplitude):
    # The shift interchanges the two highest-address-bit columns.  A complex
    # reference pair represents both a coherent old input and its purification.
    from math import sqrt
    amp = float(amplitude.mid)
    af = float(a.mid)
    pf = float(p.mid)
    filler = sqrt(pf**2 - amp**2)
    for sign, tags in [(1, ((1,0),(1,0))), (-1, ((1,0),(-1,0))),
                       (0, ((1,0),(0,1))), (0, ((1,0),(1j,0)))]:
        rates = []
        for axis in (0,1):
            field = [[amp, af, filler], [amp if axis == 0 else -amp, af, filler]]
            click = 0.
            for x in range(2):
                for car in range(3):
                    for right in range(2):
                        delta = tags[1-x][right]*field[1-x][car]-tags[x][right]*field[x][car]
                        click += pf**3*abs(delta)**2/2
            rates.append(click)
        require(abs(rates[1]-rates[0]-4*pf**3*amp**2*sign) < 1e-15,
                "exact old-address coherence test including full address tag")
        if sign == 0:
            require(abs(rates[0]-2*pf**3) < 1e-15, "source vanishes on tagged old address")


def main():
    s0, s2, s3 = 2*p**3, 4*p**3, 16*p**9
    inside(abs(s2 - iv.sin(2*theta)**2), "-1e-80", "1e-80")
    inside(abs(s3 - iv.sin(4*theta)**2), "-1e-80", "1e-80")
    for s,m in ((s0,1), (s2,1), (s2,2), (s3,1)):
        for cap in (1,2,5):
            enumerate_short(s,m,cap)

    miss = 1-s0
    mode = miss**16
    runner_up = s0*mode
    require(s0**86 < runner_up < mode, "all full-ready fine leaves lose")
    # Reachable second-largest leaf: immediate plus, then 16 misses.
    inside(-iv.ln(s0)/ell, "1.55957", "1.55959")
    amplitude = p*iv.sin(712*theta)
    r = endpoints(amplitude)
    old_address_test(amplitude)
    gamma = ready(s0,16)**86 * ready(s2,32)**172 * ready(s3,32)**46
    weighted_first = reg_weight(s0,1,16)
    weighted_ready = (weighted_first**86 * reg_weight(s2,1,32)**86 *
                      reg_weight(s2,2,32)**86 * reg_weight(s3,1,32)**46)
    early_abort = (miss*p)**16*(1-weighted_first**86)/(1-weighted_first)
    tail = weighted_first**86
    dz = weighted_ready*(p-p**2)*r
    # Keep the small subtraction out of 1-epsilon using log1p.
    dlo = -iv.log1p(-dz/(early_abort+tail))/ell
    dhi = -iv.log1p(-dz/early_abort)/ell
    entropy = -(r*iv.ln(r)+(1-r)*iv.log1p(-r))/ell
    cq = gamma*(r-entropy)
    inside(gamma,".97334116981598",".97334116981599")
    inside(weighted_ready,"5.6257259705e-179","5.6257259707e-179")
    inside(tail/early_abort,"2.6332e-42","2.6333e-42")
    inside(dlo,"1.43671975663489e-175","1.43671975663491e-175")
    inside(dhi,"1.43671975663489e-175","1.43671975663491e-175")
    inside(cq,"-.002265953081914","-.002265953081912")
    require(r < p**2, "native tap below stationary entropy threshold")
    print(json.dumps({
        "first_abort_probability": show(mode), "runner_up_probability": show(runner_up),
        "max_successful_prefix_leaf_bound": show(s0**86),
        "raw_modal_cost": show(-iv.ln(mode)/ell), "raw_mode_gap": show(-iv.ln(s0)/ell),
        "fine_service_SUCCESS": show(gamma), "bright_tap_probability": show(r),
        "code_minus_full_record_entropy_F6_minus_F5": show(cq),
        "NC1_weighted_success_mass": show(weighted_ready),
        "unresolved_service_order_relative_bound": show(tail/early_abort),
        "minus_log_phi_weighted_sum_F6_minus_F5_strict_interval":
            ["1.43671975663489e-175","1.43671975663491e-175"],
        "common_raw_MDL_endpoint_difference": 0,
        "absolute_old_address_tag_all_three_secants": 0,
        "full_Book03_weight_identified": False, "GR_closed": False
    },indent=2))


if __name__ == "__main__":
    main()
