"""Exact rational checks of the source witness and its scaling assumptions."""
from fractions import Fraction as F
import json


def req(test, message):
    if not test:
        raise ArithmeticError(message)


def ratios():
    # dI(z)=1, dI(w)=0, dV(z)=0, dV(w)=1.
    # F(I)=I^2/2 and S=F(I)+beta V, I=1 and s^2=4.
    # Raw gain at the scaled point changes by 4.
    beta, scale2 = F(3, 7), F(4)
    first = beta/F(1)
    second = scale2**2*beta/(scale2*scale2)
    req(first == second and beta != 0, "ratio equality requires a common cluster gain")

    # Arbitrary physical residual components on z,w, normalized by gain.
    cases = []
    for rz, rw, nz, nw in ((F(1, 8), F(1, 5), F(1), F(1)),
                            (F(-1, 4), F(-1, 3), F(2), F(3)),
                            (F(1, 10), F(-1, 9), F(4), F(2))):
        # residual norm E dominates residuals divided by probe norms
        E = max(abs(rz)/nz, abs(rw)/nw)
        R = rw/(1+rz)
        lower = abs(R)/(nw+abs(R)*nz)
        req(E >= lower, "measured ratio enforces normalized defect lower bound")
        cases.append({"ratio":str(R), "defect":str(E), "necessary_lower_bound":str(lower)})

    # A scalar report q=q0+gI+eta V gives an actual exact source.
    # General C1 postprocessing S=f(q) cancels from the two-row ratio.
    eta, g = F(2, 13), F(3, 5)
    q_ratio1, q_ratio2 = eta/g, scale2*eta/g
    slope1, slope2 = F(11, 17), F(5, 19)
    first_scaled = slope1*eta/(slope1*g)
    second_scaled = slope2*scale2**2*eta/(slope2*scale2*g)
    req((first_scaled, second_scaled) == (q_ratio1, q_ratio2),
        "scalar postprocessing and nonconstant gain cancel")
    req((q_ratio2-q_ratio1)/(scale2-1) == eta/g,
        "calibrated volume contamination")
    print(json.dumps({
        "scale_squared": str(scale2),
        "equal_ratio_with_nonzero_volume_term":str(first),
        "moving_gain_counterexample_beta":str(beta),
        "source_defect_witnesses": cases,
        "scalar_report_volume_ratios":[str(q_ratio1),str(q_ratio2)],
        "scalar_report_contamination":str(eta/g),
        "scope":"exact finite-dimensional dual algebra; physical ledger and source estimates require independent proof"
    },indent=2))


if __name__ == "__main__":
    ratios()
