"""Enclose the positive-gain source cone for the actual A76 retained SITE."""
import hashlib
import json
import sys
from fractions import Fraction as Q
from pathlib import Path

import numpy as np

PILOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PILOT / "direct/round76/record"))
import check_noisy_site_price as source

I, O = source.I, source.O
PINS = {
    "direct/round76/record/check_noisy_site_price.py":
        "170f1b51e3f3cb1625c062b658e95782380a1a054328a921549df337b1838123",
    "direct/round75/history/TWO_SITE_SOURCE_RU.md":
        "b22c08ca55b1c6996fa58066b01b178f175c6db2ee1ddbceb0ae8ed945bdd29c",
    "open/round152/RESULT.json":
        "eaf0ff8edfa931b7a672b270c813870d26db91b96263506035d79342fc468fb2",
    "../../A4D_NATIVE_BOOK03_BORN_ENTROPY_BELLMAN_VERTEX_INFORMATION_WELD_2026_10_22.md":
        "6c4d8e175a2bc23ea2f6995fa111897b73ce07ed45e3ce19041bacaa5245a116",
}
GEOMETRY_LOWER = Q(2204, 100000)
WALK_CUT = 72


def positive_part(x):
    return I(np.maximum(0., x.lo), np.maximum(0., x.hi))


def elementwise_extremum(x, reduce):
    return I(reduce(x.lo), reduce(x.hi))


def stack(xs):
    return I(np.stack([x.lo for x in xs]), np.stack([x.hi for x in xs]))


def parity_sum(q, f):
    x = q*f
    while x.lo.shape[-1] > 1:
        x = x[..., ::2]+x[..., 1::2]
    return x[..., 0]


def physical_site():
    p, base, w, dw, fw, bw, u, du, _ = source.owner.site_vector()
    masses, slopes, multiples, fine_mass, fine_slope = [], [], [], [], []
    for cf in range(2):
        vals, ders = source.owner.actions(cf, w, dw, fw, bw, u, du)
        for label, (value, tangent) in enumerate(zip(vals, ders)):
            blank = label == cf == 0
            for port in ((0, 1) if blank else (1,)):
                factor = -2*(p.square() if port == 0 else p*p.sqrt())
                z = value*factor+base if blank and port == 0 else value*factor
                dz = tangent*factor
                q, dq = source.sum_at_site(z.square()), 2*source.sum_at_site(z*dz)
                O.require(np.all(q.lo > 0), "actual positive SITE masses")
                masses.append(q)
                slopes.append(dq)
                multiples.append(I(1.) if blank else 1+p)
                for scale in ((I(1.),) if blank else (I(1.), p)):
                    fine_mass.append(scale*O.reduce_sum(q))
                    fine_slope.append(scale*O.reduce_sum(dq))
    fine_mass, fine_slope = stack(fine_mass), stack(fine_slope)
    O.require(O.reduce_sum(fine_mass).contains(1)
              and O.reduce_sum(fine_slope).contains(0), "physical old normalization")
    O.require(fine_mass.lo.size == 64, "full positive old support")
    return p, stack(masses), stack(slopes), stack(multiples), fine_mass, fine_slope


def old_bound(q, dq, logphi):
    logq = -source.ln(q)/logphi
    h, dh = O.reduce_sum(q*logq), O.reduce_sum(dq*logq)
    score = dq/q
    lower = h*elementwise_extremum(score, np.min)-dh
    upper = h*elementwise_extremum(score, np.max)-dh
    return lower, upper, h, dh


def repeated_parity_cone(p, logphi, a, b, da, db):
    r0 = p.square()
    contrast = p*r0
    signed = a*db-b*da
    pos, neg = positive_part(signed), positive_part(-signed)
    negative, positive, k = I(np.zeros_like(a.lo)), I(np.zeros_like(a.lo)), I(1.)
    for j in range(WALK_CUT+1):
        rows = ((a+b, b),) if j == 0 else ((a*k+b, b), (a+b*k, b*k))
        for denom, mass1 in rows:
            r = r0+contrast*mass1/denom
            complement = I(1.)-r
            g0 = -source.ln(r)/(complement*logphi)
            g1 = -source.ln(complement)/(r*logphi)
            negative = negative+k*(pos*g0+neg*g1)/denom
            positive = positive+k*(pos*g1+neg*g0)/denom
        k = k*p
    tail = 2*k*source.absolute(signed)*(I(1.)/a+I(1.)/b)/(p*(I(1.)-p))
    return I(negative.lo,(negative+tail).hi), I(positive.lo,(positive+tail).hi)


def adaptive_bounds(p, logphi, q, dq, repeat):
    # Hellinger mass drops by exactly 1-beta at a separating query.
    # The bound is independent of the order of queries and stopping leaves.
    root = q.sqrt()
    joint_root = root[:, :, None]*root[:, None, :]
    v = dq/q
    score_gap = source.absolute(v[:, :, None]-v[:, None, :])
    # Each pair occurs twice; the posterior denominator supplies a second /2.
    pairs = O.reduce_sum(joint_root*score_gap)/4
    beta = 2*(p*p.square()).sqrt()
    pair_bound = 2*p.square()*pairs/(I(1.)-beta)
    prior = q/repeat[:, None]
    # Sum the per-y entropy–oscillation product rather than multiply
    # by the largest score range occurring on any fine leaf.
    score_max = I(np.max(v.lo, axis=1), np.max(v.hi, axis=1))
    score_min = I(np.min(v.lo, axis=1), np.min(v.hi, axis=1))
    extent = score_max-score_min
    h_by_tag = parity_sum(-q*source.ln(prior), I(1.))
    entropy_bound = O.reduce_sum(h_by_tag*extent)/(p*p*p.square())
    return {"pair_hellinger": O.bounds(pair_bound), "entropy_oscillation": O.bounds(entropy_bound),
            "H_native_hidden_given_old": O.bounds(O.reduce_sum(h_by_tag)/logphi)}


def main():
    for name, digest in PINS.items():
        O.require(hashlib.sha256((PILOT/name).read_bytes()).hexdigest() == digest,
                  f"pinned source {name}")
    p, q, dq, multiplicity, qy, dqy = physical_site()
    logphi = -O.logarithm(p)
    rlo, rhi, hy, dhy = old_bound(qy, dqy, logphi)
    masks = I(np.array([[bin(mask & x).count("1") % 2 for x in range(256)]
                       for mask in range(1,256)]))
    not_masks = I(1.)-masks
    a, b = parity_sum(q[:, None, :], not_masks), parity_sum(q[:, None, :], masks)
    da, db = parity_sum(dq[:, None, :], not_masks), parity_sum(dq[:, None, :], masks)
    neg, pos = repeated_parity_cone(p, logphi, a, b, da, db)
    neg, pos = neg*multiplicity[:, None], pos*multiplicity[:, None]
    worst_neg_by_tag = I(np.max(neg.lo, axis=1),np.max(neg.hi,axis=1))
    worst_pos_by_tag = I(np.max(pos.lo, axis=1),np.max(pos.hi,axis=1))
    neg_tag, pos_tag = O.reduce_sum(worst_neg_by_tag), O.reduce_sum(worst_pos_by_tag)
    neg_by_mask = sum((neg[tag] for tag in range(q.lo.shape[0])), I(0.))
    pos_by_mask = sum((pos[tag] for tag in range(q.lo.shape[0])), I(0.))
    resid = I.rational(GEOMETRY_LOWER)+rlo-neg_tag
    O.require(rlo.lo > -.000573797, "all old redistributions included")
    O.require(neg_tag.hi < .012352516 and resid.lo > .00911368, "routed suffix gap")
    candidates = np.delete(neg_by_mask.hi,127)
    O.require(neg_by_mask[127].lo > np.max(candidates), "mask 128 is the most negative shared choice")
    O.require(neg_by_mask[207].hi < .009971592, "literal B152 parity")
    qmass = parity_sum(q,I(1.))*multiplicity
    adaptive = adaptive_bounds(p, logphi, q*multiplicity[:, None], dq*multiplicity[:, None],qmass)
    result = {
        "round": "B153",
        "pinned_source_hashes": PINS,
        "positive_old_leaves": qy.lo.size,
        "old_H": O.bounds(hy),
        "old_DH": O.bounds(dhy),
        "old_lower": O.bounds(rlo),
        "old_upper": O.bounds(rhi),
        "sum_possible_negative_suffix_with_old_tag_routing": O.bounds(neg_tag),
        "sum_possible_positive_suffix_with_old_tag_routing": O.bounds(pos_tag),
        "worst_negative_suffix_one_shared_mask": [int(np.argmax(neg_by_mask.hi))+1,
                                                  O.bounds(elementwise_extremum(neg_by_mask,np.max))],
        "worst_positive_suffix_one_shared_mask": [int(np.argmax(pos_by_mask.hi))+1,
                                                  O.bounds(elementwise_extremum(pos_by_mask,np.max))],
        "mask208_negative_suffix": O.bounds(neg_by_mask[207]),
        "mask208_positive_suffix": O.bounds(pos_by_mask[207]),
        "geometry_lower_minus_old_and_routed_single_parity": O.bounds(resid),
        "adaptive_tail_upper_bounds": adaptive,
        "absolute_Book03_cost_info_proven": False,
        "GR_closed": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
