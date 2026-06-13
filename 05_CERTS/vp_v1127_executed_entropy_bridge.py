#!/usr/bin/env python3
"""
D0 v11.27 executed finite entropy bridge cert.
This cert does not compare to external data. It verifies the actual finite
bridge theorem used by bridge/passport claims:
  finite support -> response constraint -> unique entropy-maximizing kernel.
It then executes the construction for the D0 BAO two-window centers from
160 lambda^2 - 480 lambda + 359 = 0 on a fixed survey-response grid.
"""
import math, json

TOL=1e-11

def lambda_roots():
    # roots of 160*l^2 - 480*l + 359 = 0
    disc = 480*480 - 4*160*359
    assert disc == 640
    s = math.sqrt(disc)
    return ((480-s)/(320), (480+s)/(320))

def entropy(q):
    return -sum(x*math.log(x) for x in q if x > 0)

def softmax_dist(y, mean_target):
    """Max entropy distribution on finite y with E[y]=mean_target."""
    ymin, ymax = min(y), max(y)
    if not (ymin - 1e-14 <= mean_target <= ymax + 1e-14):
        raise ValueError("mean outside convex hull")
    # if boundary, unique delta on boundary support (possibly averaged over equal states)
    if abs(mean_target-ymin) < 1e-13:
        q=[1.0 if abs(v-ymin)<1e-13 else 0.0 for v in y]
        return q, float('-inf')
    if abs(mean_target-ymax) < 1e-13:
        q=[1.0 if abs(v-ymax)<1e-13 else 0.0 for v in y]
        return q, float('inf')
    def mean(lam):
        ex=[math.exp(lam*v) for v in y]
        z=sum(ex)
        return sum(v*e for v,e in zip(y,ex))/z
    lo, hi = -100.0, 100.0
    # bisection, mean increasing because variance > 0
    for _ in range(300):
        mid=(lo+hi)/2
        if mean(mid) < mean_target:
            lo=mid
        else:
            hi=mid
    lam=(lo+hi)/2
    ex=[math.exp(lam*v) for v in y]
    z=sum(ex)
    q=[e/z for e in ex]
    return q, lam

def check_unique(y, q, lam, mean_target):
    # KKT: log q_j = c + lam*y_j for all q_j>0
    vals=[math.log(qj)-lam*yj for qj,yj in zip(q,y) if qj>1e-14]
    kkt_span=max(vals)-min(vals)
    mean=sum(qj*yj for qj,yj in zip(q,y))
    return {
        "mean": mean,
        "target": mean_target,
        "mean_error": abs(mean-mean_target),
        "kkt_span": kkt_span,
        "entropy": entropy(q),
    }

def main():
    lam_c, lam_r = lambda_roots()
    # fixed finite response grid; not fitted to data and symmetric around 3/2.
    y=[1.0, 1.25, 1.5, 1.75, 2.0]
    windows={"lambda_c": lam_c, "lambda_r": lam_r}
    kernels={}
    for name,target in windows.items():
        q,theta=softmax_dist(y,target)
        chk=check_unique(y,q,theta,target)
        assert chk["mean_error"] < 1e-10
        assert chk["kkt_span"] < 1e-8
        kernels[name]={"target":target,"theta":theta,"grid":y,"kernel":q,"check":chk}
    # Verify polynomial roots exactly/numerically.
    poly_c=160*lam_c*lam_c-480*lam_c+359
    poly_r=160*lam_r*lam_r-480*lam_r+359
    assert abs(poly_c)<1e-12 and abs(poly_r)<1e-12
    # Verify convex-response order for simple convex tests t^2 and exp(t) between delta mean and entropy spread:
    # For Y with mean m, Jensen gives phi(m) <= E phi(Y).
    convex_checks=[]
    for name,k in kernels.items():
        m=k["target"]; q=k["kernel"]
        for test in ["square","exp","abs_center"]:
            if test=="square":
                lhs=m*m; rhs=sum(qj*yj*yj for qj,yj in zip(q,y))
            elif test=="exp":
                lhs=math.exp(m); rhs=sum(qj*math.exp(yj) for qj,yj in zip(q,y))
            else:
                lhs=abs(m-1.5); rhs=sum(qj*abs(yj-1.5) for qj,yj in zip(q,y))
            assert rhs + 1e-12 >= lhs
            convex_checks.append({"window":name,"test":test,"phi_mean":lhs,"mean_phi":rhs,"slack":rhs-lhs})
    result={
        "status":"PASS_V11_27_EXECUTED_ENTROPY_BRIDGE",
        "bao_window_roots":{"lambda_c":lam_c,"lambda_r":lam_r,"polynomial":"160*l^2 - 480*l + 359"},
        "finite_grid":y,
        "kernels":kernels,
        "convex_response_checks":convex_checks,
        "interpretation":"For each fixed D0 window center, the bridge kernel is not selected by fit: it is the unique finite maximum-entropy kernel on the declared response grid with the declared response mean.",
    }
    print(json.dumps(result,indent=2))

if __name__ == "__main__":
    main()
