"""Exact cell-flow and native SITE functional checks. Python standard library."""
from fractions import Fraction as Q
import json


def need(ok, label):
    if not ok:
        raise ArithmeticError(label)


def weighted(m, f):
    return sum(p*x for p,x in zip(m,f))


def site_tests():
    # Arbitrary rational finite bank values in T3's seven-probability
    # polynomial. No admission as a particular geometric H.1 metric is inferred.
    weights = [Q(x,20) for x in (2,3,5,4,6)]
    bank = [[Q(1+(u*(i+2)+i*i+2*u*u) % 15, 17) for u in range(7)] for i in range(5)]
    features = []
    for py1,py0,pf,p0,px1,px0,pq in bank:
        features.append((py1-py0)*(pf-p0)+(px1-px0)*(pq-p0))
    mean = weighted(weights,features)
    var = weighted(weights,[(f-mean)**2 for f in features])
    need(var>0 and sum(weights)==1, "nonconstant site features")
    # Optimal mass tangent. Norm squared of the Born amplitude tangent is
    # sum(dm_i^2 / (4 mu_i)); the code need never round a square root.
    dm = [m*(f-mean) for m,f in zip(weights,features)]
    born_sq = sum(d*d/(4*m) for m,d in zip(weights,dm))
    slope = weighted(dm,features)
    need(sum(dm)==0 and slope**2/born_sq == 4*var, "sharp native SITE norm")
    # Flux across a connected chain realizes any zero-total tangent.
    flux = [Q(0)]
    for d in dm:
        flux.append(flux[-1]-d)
    need(flux[-1]==0 and [flux[i]-flux[i+1] for i in range(5)] == dm, "boundary support and flux")
    k = next(i for i in range(4) if features[i] != features[i+1])
    flow = Q(3,17)
    local_dm = [Q(0)]*5
    local_dm[k], local_dm[k+1] = -flow,flow
    need(weighted(local_dm,features) == flow*(features[k+1]-features[k]), "single real-address face")
    need(sum(d*d/(4*m) for m,d in zip(weights,local_dm)) ==
         flow**2*(1/weights[k]+1/weights[k+1])/4, "two-cell amplitude norm")
    # A constant comparator baseline and any common error drop out against dm.
    need(weighted(dm,[4+x for x in features]) == slope, "constant T3 baseline cancels")
    return {"fixed_probabilities": [str(x) for x in weights], "Xi": [str(x) for x in features],
            "four_times_variance_exact": str(4*var), "single_face_source_before_calibration":str(weighted(local_dm,features)),
            "scope":"seven rational bank entries per cell test the true T3 polynomial; no claim that this particular table is realized by a D0 geometry"}


def interval(n):
    # dx on [0,1], F=x, xi=x(1-x). Flux vanishes at both ends.
    def xi(x):
        return x*(1-x)
    h=Q(1,n)
    born_sq=load=bank=midpoint_only=Q(0)
    for k in range(n):
        left,right = k*h,(k+1)*h
        mid = (left+right)/2
        dm = xi(left)-xi(right)
        # Integral of the transported density times its passively transported
        # scalar has derivative equal to minus the boundary flux of x*xi(x).
        cell_product_deriv = left*xi(left)-right*xi(right)
        df = (cell_product_deriv-mid*dm)/h
        need(dm == -h*(1-2*mid), "cell continuity equation")
        need(df == -(xi(left)+xi(right))/2, "conditional cell mean, not just midpoint")
        born_sq += dm**2/(4*h)
        load += mid*dm
        bank += h*df
        midpoint_only -= h*xi(mid)
    need(born_sq==(1-h*h)/12, "finite Hellinger tangent")
    need(load==(1-h*h)/6 and bank==-load, "exact signed passive cancellation")
    need(load+midpoint_only==-h*h/4, "midpoint bias")
    return {"cells":n,"loader_amplitude_norm_squared":str(born_sq),
            "loader_source":str(load),"transported_cell_mean_source":str(bank),
            "exact_sum":"0","sum_with_point_sampled_bank":str(load+midpoint_only)}


if __name__ == "__main__":
    print(json.dumps({"status":"PASS","native_response_polynomial":site_tests(),
                      "cell_calibration":[interval(n) for n in (2,4,8,16,64)],
                      "limits":{"amplitude_norm_squared":"1/12","loader_source":"1/6","bank_source":"-1/6"},
                      "metric_only_Ward_established":False,"physical_price_selected":False},indent=2))
