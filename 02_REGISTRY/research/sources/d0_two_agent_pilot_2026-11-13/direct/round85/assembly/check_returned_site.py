"""Return of one native half-period probe on every occupied SITE column."""
import itertools
import json

import mpmath as mp
import numpy as np

mp.mp.dps = 55
p = (mp.sqrt(5)-1)/2
a = mp.sqrt(p)
z = mp.mpf(2)**-20
A = p * mp.sin(712*mp.asin(p))
u = 2*p**3
sites = np.array(list(itertools.product(range(4), repeat=4)))
swap = np.arange(len(sites)).reshape([4]*4).take([2,3,0,1], axis=1).ravel()
pairs = np.arange(len(sites)) < swap
cos = np.array([1,0,-1,0])
sin = np.array([0,1,0,-1])


def require(value, msg):
    if not value:
        raise ValueError(msg)


def close(x, y, msg):
    require(np.allclose(x, y, atol=3e-13, rtol=3e-13), msg)


def physical(t):
    data = np.zeros((len(sites),16))
    for mode, weight in ((0,1-t), (1,t)):
        b = float(A)*np.sqrt(weight)
        data[:,0] += b*cos[sites[:,mode]]
        data[:,15] += b*sin[sites[:,mode]]
    data[:,1] = float(a)
    data[:,14] = np.sqrt(float(p**2)-data[:,0]**2-data[:,15]**2)
    close(np.sum(data**2, axis=1), 1, "isometry on every old SITE")
    return data


def direct_effect(t):
    data = physical(t)
    overlaps = np.sum(data*data[swap], axis=1)
    phi = sites[:,0] - sites[:,1]
    closed = (float(p)+float(A**2)*(1-2*t)
              +np.sqrt(float((p**2-A**2)**2)-4*float(A**4)*t*(1-t)*cos[phi%4]**2))
    close(overlaps, closed, "CAR overlap including the true positive filler")
    # The four old reference coordinates stay entangled while the native head
    # and its inverse rotation act on the supplied full SITE x CAR16.
    rng = np.random.default_rng(342)
    right = rng.normal(size=(len(sites),4)) + 1j*rng.normal(size=(len(sites),4))
    old = data[:,:,None]*right[:,None,:]
    no = float(p)*old + float(p**2)*old[swap]
    yes = float(a*p)*(old[swap]-old)
    close(np.vdot(yes,yes)+np.vdot(no,no), np.vdot(old,old), "both raw Kraus outcomes")
    effect_right = float(u)*(right-overlaps[:,None]*right[swap])
    close(np.vdot(yes,yes), np.vdot(right,effect_right), "occupied old SITE with reference")
    matrix = float(u)*np.eye(len(sites))
    matrix[np.arange(len(sites)),swap] -= float(u)*overlaps
    values = np.r_[float(u)*(1-overlaps[pairs]),float(u)*(1+overlaps[pairs])]
    close(np.sort(values), np.linalg.eigvalsh(matrix), "all 256 old-column eigenvalues")
    close(np.trace(matrix),len(sites)*float(u),"constant first trace")


def j(e):
    return -mp.log1p(z*(p*(p-p**3*e)**2-1))


def prime(e):
    return 2*z*p**4*(p-p**3*e)/(1-z+z*p*(p-p**3*e)**2)


def analytic(t):
    total = derivative = mp.mpf(0)
    # Of 128 disjoint half-period SITE pairs, 64 have each of cos^2=0 and 1.
    for b in [0,1]:
        root = mp.sqrt((p**2-A**2)**2-4*A**4*t*(1-t)*b)
        c = p+A**2*(1-2*t)+root
        dc = -2*A**2-2*A**4*(1-2*t)*b/root
        left, right = u*(1-c),u*(1+c)
        total += 64*(j(left)+j(right))
        derivative += 64*u*dc*(prime(right)-prime(left))
    return total, derivative


def main():
    require(all(np.bincount(cos[(sites[pairs,0]-sites[pairs,1])%4]**2) == [64,64]), "pair counts")
    for t in (0, .25, .5, .75, 1):
        direct_effect(t)
    half = mp.mpf(1)/2
    for t in (0, half/5, half, 1-half/5, 1):
        value, slope = analytic(t)
        require(slope > 0 and abs(mp.diff(lambda x: analytic(x)[0],t)-slope) < mp.mpf("1e-48"),
                "passive return has positive derivative")
    limit = A**2/(p*mp.sqrt(p**2-2*A**2))
    require(limit < 1 and 1-2*A**2>0 and 1-z>z*p**3, "uniform monotonicity bounds")
    wave0, wave1 = physical(0),physical(1)
    taps = [float(a*p)**2*np.sum((w[swap]-w)**2)/len(sites) for w in (wave0,wave1)]
    close(taps, [0, float(4*p**3*A**2)], "native calibrated endpoint reports on uniform SITE")
    print(json.dumps({"full_old_site": len(sites), "pair_multiplicity": [64,64],
                      "recalibrated_writer_G_block_count": 712, "amplitude": mp.nstr(A,14),
                      "endpoint_tap_probabilities": [0,mp.nstr(4*p**3*A**2,14)],
                      "trace_effect_per_old_site": mp.nstr(u,14),
                      "endpoint_return_log_difference": mp.nstr(analytic(1)[0]-analytic(0)[0],14),
                      "center_return_log_derivative": mp.nstr(analytic(half)[1],14),
                      "relative_bound_on_overlap_derivative_correction": mp.nstr(limit,12),
                      "old_right_spectator": True, "whole_writer_tape_priced": False,
                      "GR_closed": False}, indent=2))


if __name__ == "__main__":
    main()
