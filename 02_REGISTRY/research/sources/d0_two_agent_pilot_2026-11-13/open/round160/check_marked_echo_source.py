"""Outward gain bounds for a truly marked RC3 echo and two 0/10 copies."""
import hashlib
import json
import sys
from fractions import Fraction as Q
from pathlib import Path

import numpy as np

PILOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PILOT/"direct/round76/record"))
import check_noisy_site_price as owner

I,O = owner.I,owner.O
PINS = {
    "direct/round78/selection/H1_EQUATIONS_RU.md":
        "8d95e35baa5c0e48c761dc952007fc81b44b5e5dc59f28b8e1efb95cd27c8a98",
    "direct/round78/clock/BLANK_CONFIRMATION_RU.md":
        "65e37fff5ff3433139e18ced7c6ceda8b58a0c31e9aab2563e14fb4bdc896a77",
    "direct/round70/coding/REPEATED_WRITER_RU.md":
        "d1d096c08db4dceba68eb944a4cc34f2ecba93f80980296b3153fb24bc90ef1e",
}
QMIN,QMAX = Q(1,16),Q(19,50)
Z = Q(1,2**20)


def bounds(v):
    return [float(np.min(v.lo)),float(np.max(v.hi))]


def power(v,n):
    result = I(1.)
    for _ in range(n):
        result = result*v
    return result


def cell_grid():
    grid = [I.rational(QMIN+(QMAX-QMIN)*Q(k,1024)) for k in range(1025)]
    return I(np.array([t.lo for t in grid[:-1]]),np.array([t.hi for t in grid[1:]]))


def marked_return(p,q):
    s = p.sqrt()+p
    h, dh, ddh, recorded_return = I(0.),I(0.),I(0.),I(0.)
    for mark, (a,b) in enumerate(((p.sqrt(),p),(p,p.sqrt()))):
        mass = a.square()+(b.square()-a.square())*q
        amplitude = a-s*q
        w = power(p,7+5*mark)
        O.require(np.all(mass.lo > 0) and np.all(amplitude.lo > 0),
                  "both full-root branches occupied and nonzero")
        recorded_return = recorded_return+amplitude.square()
        h = h+w*amplitude.square()/mass
        dh = dh-w*s*amplitude*(mass+a*b)/mass.square()
        ddh = ddh+2*w*(s*a*b).square()/(mass*mass.square())
    eta = 2*p*p.sqrt()
    coherent = (I(1.)-2*q).square()
    expected = coherent+2*(I(1.)-eta)*q*(I(1.)-q)
    O.require(np.all((recorded_return-expected).lo <= 0)
              and np.all((recorded_return-expected).hi >= 0), "CP return identity")
    z = I.rational(Z)
    cold_gain = -dh/(I(1.)-z+z*h)
    O.require(np.min(cold_gain.lo) > .04595 and np.min(ddh.lo) > 0,
              "marked occupied-range cold derivatives")
    return {
        "H_Range_overlap":bounds(h),
        "H_Range_first_derivative":bounds(dh),
        "H_Range_second_derivative":bounds(ddh),
        "Cold_DJ_over_root_rank_z_Dq":bounds(cold_gain),
        "Born_CP_return_minus_coherent":bounds(2*(I(1.)-eta)*q*(I(1.)-q)),
    }


def entropy_branch_work(probability, model):
    if model == "literal":
        return I(0.)
    if model == "registered":
        return I(2.)-probability
    O.require(model=="coherent" and np.min(probability.lo) > .25,"branch formula")
    return probability.sqrt()+(3*(I(1.)-probability)).sqrt()


def output_gains(p,q):
    ell = -O.logarithm(p)
    r = p.square()+p*p.square()*q
    r0 = I(1.)-r
    ln1, ln0 = owner.ln(r),owner.ln(r0)
    entropy = -(r0*ln0+r*ln1)/ell
    literal_slope = 2*p*p.square()*(I(1.)-(ln0-ln1)/ell)
    O.require(np.min(literal_slope.lo) > .06089, "two genuine copies, positive BORN+GAIN slope")
    results = {}
    for model, suffix, scale in (("literal","",I(0.)),
                                 ("registered","",I(1.)),
                                 ("registered","_sqrt22", I(22.).sqrt()),
                                 ("coherent","",I(1.)),
                                 ("coherent","_sqrt22",I(22.).sqrt())):
        difference = 2+scale*(entropy_branch_work(r,model)-entropy_branch_work(r0,model))
        gain0 = ln0/ell+2*entropy-r*difference
        gain1 = ln1/ell+2*entropy+r0*difference
        floor = min(float(np.min(gain0.lo)),float(np.min(gain1.lo)))
        O.require(floor > .4787, "strict old-to-new raw report gain")
        results[model+suffix] = floor
    return {
        "new_report_probability":bounds(r),
        "BORN_GAIN_literal_two_copies_derivative_over_Dq":bounds(literal_slope),
        "raw_realized_Info_lower_by_work":results,
    }


def check_exact_occupied_ranges():
    import sympy as sm

    identity = sm.eye(2)
    isometry = identity.col_join(sm.zeros(2))
    mix = sm.Matrix([[sm.Rational(7,25),-sm.Rational(24,25)],
                     [sm.Rational(24,25),sm.Rational(7,25)]])
    rot = sm.diag(mix,mix)
    c = sm.diag(sm.Rational(4,5),sm.Rational(12,13))
    s = sm.diag(sm.Rational(3,5),sm.Rational(5,13))
    forward = rot.T*c.row_join(-s).col_join(s.row_join(c))*rot
    projector = sm.diag(0,0,1,1)
    effect = isometry.T*forward.T*projector*forward*isometry
    O.require(effect[0,1] != 0 and forward.T*forward == sm.eye(4),
              "check in a non-diagonal protected basis")
    returned = sm.zeros(2)
    for a,b in ((sm.Rational(4,5),sm.Rational(3,5)),
                (sm.Rational(3,5),sm.Rational(4,5))):
        k = forward.T*(a*(sm.eye(4)-projector)-b*projector)*forward*isometry
        g = a*a*(identity-effect)+b*b*effect
        a_root = a*identity-(a+b)*effect
        normalized = k*g.inv()*k.T
        O.require(k.T*k == g and normalized*normalized == normalized,
                  "actual full occupied range")
        O.require(isometry.T*normalized*isometry == a_root*g.inv()*a_root,
                  "actual passive compression")
        returned += a_root*a_root
    eta = 2*sm.Rational(12,25)
    O.require(returned == (identity-2*effect)**2+2*(1-eta)*effect*(identity-effect),
              "separate unnormalized CP sum")
    q,a,b = sm.symbols("q a b", real=True)
    amplitude = a-(a+b)*q
    gram = a*a+(b*b-a*a)*q
    f = amplitude**2/gram
    O.require(sm.cancel(sm.diff(f,q)+(a+b)*amplitude*(gram+a*b)/gram**2)==0,
              "exact first derivative")
    O.require(sm.cancel(sm.diff(f,q,2)-2*((a+b)*a*b)**2/gram**3)==0,
              "exact second derivative")
    return True


def main():
    for path,digest in PINS.items():
        O.require(hashlib.sha256((PILOT/path).read_bytes()).hexdigest()==digest,
                  f"source pin {path}")
    p = (I(5.).sqrt()-1)/2
    q = cell_grid()
    print(json.dumps({
        "round":"B160",
        "exact_full_column_range_and_derivative_checks":check_exact_occupied_ranges(),
        "fixed_q_range":[str(QMIN),str(QMAX)],
        "record_containers":2,
        "cold_retained_RC3":marked_return(p,q),
        "paid_two_copy_record":output_gains(p,q),
        "physical_requirements":["single computed flag accessible before echo inverse",
                                 "one true retained marker after inverse",
                                 "fixed passive root and scalar compressed effect",
                                 "two paid 0/10 containers with retained copies",
                                 "constant z and applicable RC3 graph"],
        "primary_PR334_snapshot":"b75efdf2e4e1cdd3a2cc78106886919bbda72a57",
        "full_native_clock_cost_selected":False,
        "full_macro_catalogue_physically_closed":False,
        "GR_closed":False,
        "pinned_inputs":PINS,
    },sort_keys=True,indent=2))


if __name__=="__main__":
    main()
