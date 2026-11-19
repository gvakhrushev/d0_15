"""Exact basis recovery and interval/finite checks of the registered laws."""

from contextlib import redirect_stdout
from io import StringIO
from itertools import product
import json
from math import comb
from pathlib import Path
import subprocess
import sys

import mpmath as mp
import numpy as np

PILOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PILOT / "open/round183"))
from check_registered_anchor import word_weights, require


def native_permutation(m, n):
    """Verify the Fredkin word and a matched rare event without new rotations."""
    width = n + 1

    def fredkin(k, x, y):
        x ^= y
        y ^= k & x
        x ^= y
        return x, y

    for k, x, y in product(range(2), repeat=3):
        require(fredkin(k,x,y) == ((y,x) if k else (x,y)), "Controlled swap")

    def align(bits):
        row = list(bits)
        for j in range(width):
            row[j], row[width+j] = fredkin(1,row[j],row[width+j])
        row[0], row[1] = fredkin(1,row[0],row[1])
        return tuple(row)

    def rare(bits, site):
        return not any(bits[site*width:(site+1)*width])

    def descriptor(bits, k):
        return tuple(bits[i*width] | (k and rare(bits,i)) for i in range(m))

    def selected(bits):
        return rare(bits,0) and bits[width:width+2] == (1,0) and all(
            not rare(bits,i) for i in range(2,m))

    a, b = set(), set()
    for bits in product(range(2), repeat=m*width):
        target = align(bits)
        require(sum(target) == sum(bits), "The alignment must preserve Golden amplitudes")
        if selected(bits):
            require(descriptor(bits,0) == descriptor(target,1), "Retained T changed")
            require(rare(target,1) and not rare(target,0), "Incorrect unique rare address")
            a.add(bits)
            b.add(target)
    require(len(a) == len(b) and a.isdisjoint(b), "The two selected inputs must be paired")
    return {"seeds":m, "N":n, "checked_columns":2**(m*width),
            "paired_columns_per_program":len(a)}


def coeffs(m, p, mpf, sqrt):
    r = p*p
    tv = mpf(0)
    hard = mpf(0)
    amp = mpf(0)
    for s in range(m+1):
        binom = comb(m,s)
        P = r**s*p**(m-s)
        x, y = (m-s)/p, s/r
        tv += binom*P*abs(x-y)/2
        hard += binom*P*(sqrt(x)-sqrt(y))**2/2
        amp += binom*sqrt(P)*(sqrt(y)-sqrt(x))
    return tv, hard, amp, m/(8*r*p)


def overlap_defects(m, n, ctx):
    p = (ctx.sqrt(5)-1)/2
    d = p**(n+1)
    q = 1-(1-d)**m
    arrays = [word_weights(m,d,k,p,pow) for k in (0,1)]
    hard, direct, tv = [ctx.mpf(0) for _ in range(3)]
    amp0, amp1, early = [ctx.mpf(0) for _ in range(3)]
    for s, ((a,U0),(b,U1)) in enumerate(zip(*arrays)):
        P0 = U0-a if s != m else ctx.mpf(0)
        P1 = U1-b if s != 0 else ctx.mpf(0)
        count = comb(m,s)
        hard += count*(ctx.sqrt(P0)-ctx.sqrt(P1))**2/2
        direct += count*(ctx.sqrt(U0)-ctx.sqrt(U1))**2/2
        tv += count*abs(U1-U0)/2
        weight = count*ctx.sqrt(a)
        early += weight
        amp0 += weight+count*ctx.sqrt(P0)
        amp1 += weight+count*ctx.sqrt(P1)
    thin = d*hard+(1-d)*direct
    return d,q,tv,hard,direct,thin,early/amp0,early/amp1,ctx.log(amp0/amp1)/ctx.log(1/p)


def interval_check():
    ctx = mp.iv
    ctx.dps = 80
    p = (ctx.sqrt(5)-1)/2
    result = coeffs(16,p,ctx.mpf,ctx.sqrt)
    a,b,c,d = result
    require(a > ctx.mpf("3.27177") and a < ctx.mpf("3.27178"), "TV coefficient")
    require(b > ctx.mpf("0.56490") and b < ctx.mpf("0.56491"), "Hard loss coefficient")
    require(c > 0, "Strict amplitude contrast coefficient")
    require(b+d > 9 and b+d < 10, "Thinned quadratic coefficient")
    delta,q,tv,hard,direct,thin,A,B,price = overlap_defects(16,8,ctx)
    require(A > B and price > ctx.mpf("-0.08270") and price < ctx.mpf("-0.08269"),
            "Equal Born anchor must not imply equal amplitude-weighted anchor")
    require(thin/delta < hard/delta, "The paid selection changes deterministic recovery error")


def clock_audit():
    revision = "a4becb8500ab97a6ad9821e23870a90a1e879b40"
    source = ("02_REGISTRY/research/sources/d0_gr_2026-11-18/followups/"
              "2026-11-19/metric/check_union_clock_inventory.py")
    program = subprocess.check_output(
        ["git", "show", f"{revision}:{source}"], cwd=PILOT, text=True)
    owner = {"__name__":"primary_owner"}
    exec(compile(program, f"{revision}:{source}", "exec"), owner)
    original_clock = owner["clock"]
    measures = {}

    def observed_clock(stages):
        T, dims = original_clock(stages)
        reached = np.eye(dims[0])
        for stage in stages:
            reached = stage @ reached
        closed = T[:, -dims[-1]:] @ reached
        root = np.eye(dims[0])
        require(np.max(np.abs(closed[:dims[0]]-root)) < 1e-12
                and np.max(np.abs(closed[dims[0]:])) < 1e-12,
                "The implemented clock must close the actual forward root onto itself")
        measures["clock_dimension"] = T.shape[0]
        measures["actual_generated_clock_return"] = "identity"
        return T,dims

    owner["clock"] = observed_clock
    out = StringIO()
    with redirect_stdout(out):
        owner["main"]()
    standalone = json.loads(out.getvalue())
    eig = standalone["toy_feedback_eigenvalues"]
    require(eig[0] > 0.96 and standalone["toy_RAW_J"] > 0,
            "The separate passive feedback uses different return data")
    measures["standalone_passive_F_eigenvalues"] = [f"{v:.10f}" for v in eig]
    measures["standalone_passive_J"] = f"{standalone['toy_RAW_J']:.10e}"
    return measures


def main():
    with mp.workdps(130):
        p = (mp.sqrt(5)-1)/2
        tv_limit, hard_limit, amp_limit, direct_limit = coeffs(16,p,mp.mpf,mp.sqrt)
        fmt = lambda x: mp.nstr(x,18)
        rows = []
        for n in (8,16,40,80):
            d,q,tv,hard,direct,thin,A,B,price = overlap_defects(16,n,mp)
            row = {"m":16, "N":n, "delta":fmt(d),
                   "anchor_Born_hard":fmt(1-q), "anchor_Born_thinned":fmt(d*(1-q)),
                   "optimal_exact_failure_per_delta_both_modes":fmt(tv/d),
                   "optimal_coherence_defect_hard_per_delta":fmt(hard/d),
                   "optimal_coherence_defect_thinned_per_delta_squared":fmt(thin/d**2),
                   "normalized_amplitude_anchor_masses":list(map(fmt,(A,B))),
                   "conditional_amplitude_absolute_price_difference":fmt(price)}
            rows.append(row)
        result = {
            "paired_native_logical_columns": [native_permutation(m,n) for m,n in ((2,2),(2,3),(3,2),(3,3))],
            "limiting_TV_per_delta":fmt(tv_limit),
            "limiting_hard_loss_per_delta":fmt(hard_limit),
            "limiting_thinned_loss_per_delta_squared":fmt(hard_limit+direct_limit),
            "amplitude_sum_difference_limit_per_sqrt_delta":fmt(amp_limit),
            "numerical_cases":rows,
            "macro_clock_audit":clock_audit(),
            "finite_native_program_for_abstract_optimum_proved":False,
            "economic_Book_binding_proved":False, "GR_closed":False}
    interval_check()
    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    main()
