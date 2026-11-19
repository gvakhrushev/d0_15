"""A78 protected-RIGHT filtering loss and spectral reset-policy source gaps."""
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

PILOT = Path(__file__).resolve().parents[2]
PINS = {
    'direct/round75/history/check_two_site_source.py':
        '160576666914ac68d1fba4645d92d93ddd635e243915a7d78d2df2f177eef9ce',
    'direct/round75/curvature/check_local_coframe_source.py':
        '366be653f1d0389d883c9390beb93a360fb0b6cbd21b2a13fffec74bf921848e',
    'direct/round75/work/check_pointer_weyl.py':
        'd8cab0e1f53e3e1380885b362fa9e869dc0d4113299ace300ce1da264faad4fb',
    'direct/round78/selection/COUNTED_HJR_RU.md':
        '589d7e8a19f506baa079c142015784d70239b292db22487d989efcba5b592cac',
    'direct/round78/recovery/RECORD_RECOVERY_RU.md':
        'f23fa59fab314b6e1bdcf5c9442a18448e1d8e393e282a3486ed98acbdb0ce42',
}


def load():
    pilot = PILOT
    for relative, digest in PINS.items():
        path = pilot/relative
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise RuntimeError(f"pinned source changed: {relative}")
    for folder in ('direct/round75/history','direct/round75/work'):
        sys.path.insert(0,str(pilot/folder))
    import check_pointer_weyl
    import check_two_site_source
    return check_pointer_weyl, check_two_site_source


def filtering(pointer):
    interval = pointer.I
    checked = pointer.O
    p, state, weights, tangents, forward, backward, _, _, _ = pointer.site_vector()

    def dirac(x, w):
        return pointer.dirac(x,w,forward,backward)

    def blank(x, dx):
        # B=I−2p² A², A is the actual hD/16.
        ax = dirac(x,weights)
        dax = dirac(x,tangents)+dirac(dx,weights)
        aax = dirac(ax,weights)
        daax = dirac(ax,tangents)+dirac(dax,weights)
        return x-2*p.square()*aax, dx-2*p.square()*daax

    def diagonal_pair(x,y):
        products = pointer.flatten(x*y)
        while products.lo.shape[0] > 1:
            products = products[::2]+products[1::2]
        return products[0]

    first, first_jet = blank(state,interval(np.zeros_like(state.lo)))
    second, second_jet = blank(first,first_jet)
    g1 = diagonal_pair(first,first)
    g2 = diagonal_pair(second,second)
    dg1 = 2*diagonal_pair(first,first_jet)
    dg2 = 2*diagonal_pair(second,second_jet)
    ratio = g2/g1
    ratio_jet = (dg2-ratio*dg1)/g1
    # Rayleigh tests of M=G1^-1/2 G2 G1^-1/2, no eigenbasis needed.
    witness = ratio[57]-ratio[55]
    checked.require(witness.lo > .00448638864354, "strict accepted-mass loss")
    return {'RIGHT_labels': [55,57],
            'G2_diag_over_G1_diag': [checked.bounds(ratio[55]),checked.bounds(ratio[57])],
            'spread_witness': checked.bounds(witness),
            'witness_derivative_not_optimal_filter_derivative':
                checked.bounds(ratio_jet[57]-ratio_jet[55]),
            'original_blank_probability': checked.bounds(checked.reduce_sum(g1)),
            'conditional_exact_recovery_upper': float((interval(1.)-witness).hi)}


def reset_gaps(two_site):
    heat = two_site.heat
    interval = heat.I
    a,b,s,local = two_site.witness()
    scale = a*b
    z = interval.rational(heat.ZETA)
    b_spectrum = interval(1.)-heat.ALPHA*interval(s).square()
    b_floor = interval(1.)-25*heat.ALPHA
    # Same spectral and trace-pair tolerances as the pinned A75 source.
    dirac_error = interval.rational(Fraction(12,10**9))
    b_error = 10*heat.ALPHA*dirac_error
    polar_error = interval.rational(Fraction(64*5*3,10**9)+Fraction(2*5,10**7))

    def pair(f):
        return 2*heat.interval.reduce_sum(interval(s)*interval(local)*f)

    def widen(center,error):
        return center+interval(-error.hi,error.hi)

    inverse_trace = pair(interval(1.)/b_spectrum)
    inverse_error = (64*dirac_error/b_floor+64*5*b_error/b_floor.square()
                     +polar_error/b_floor)
    retained_heat = 2*widen(inverse_trace,inverse_error)/(4096*scale)
    depths = []
    for n in (1,64,512,8192):
        m = 2*n
        prefix = heat.power(b_spectrum,m-1)
        success = heat.power(b_spectrum,m)
        mean = 2*heat.interval.reduce_sum(success)/4096
        heat_trace = widen(pair(prefix),64*(dirac_error+5*(m-1)*b_error)+polar_error)
        fresh_heat = 2*heat_trace/(4096*scale*widen(mean,m*b_error))
        heat_gap = fresh_heat-retained_heat
        # F^-1−1/mean(F)=z(mean(Y)−Y)/(F mean(F)); keep the small z factor exact.
        f = interval(1.)-z+z*success
        f_mean = interval(1.)-z+z*mean
        feedback_pair = pair(prefix*(mean-success)/(f*f_mean))
        one_minus_z = interval(1.)-z
        cap = interval(1.)/one_minus_z.square()
        function_bound = (m-1)*b_error*cap+2*m*b_error*cap
        function_bound = function_bound+2*z*m*b_error/(one_minus_z*one_minus_z.square())
        pair_bound = 64*dirac_error*cap+64*5*function_bound+polar_error*cap
        feedback_gap = -256*z.square()*m*heat.ALPHA*widen(feedback_pair,pair_bound)/scale
        if heat_gap.lo <= 0 or (n < 8192 and feedback_gap.lo <= 0):
            raise RuntimeError(f"uncertified reset gap at depth {n}")
        depths.append({'depth':n,'D_H_fresh':heat.interval.bounds(fresh_heat),
                       'D_H_retain':heat.interval.bounds(retained_heat),
                       'D_H_fresh_minus_retain':heat.interval.bounds(heat_gap),
                       'D_J_retain_minus_reset':heat.interval.bounds(feedback_gap)})
    return depths


def main():
    pointer, two_site = load()
    output = {'A78_DATA_only_exact_recovery':filtering(pointer),
              'A75_actual_reset_noninterchange':reset_gaps(two_site),
              'pinned_inputs':PINS,'enlarged_Book_price_identified':False,'GR_closed':False}
    print(json.dumps(output,indent=2,sort_keys=True))


if __name__ == '__main__':
    main()
