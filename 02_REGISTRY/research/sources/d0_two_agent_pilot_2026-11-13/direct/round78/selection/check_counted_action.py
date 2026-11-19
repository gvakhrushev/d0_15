"""Count-based log trace and trace log on the genuine 4096-dimensional regulator."""
from fractions import Fraction as Q
from pathlib import Path
import sys

import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"round75/curvature"))
import check_local_coframe_source as heat

I = heat.I


def main():
    s, _ = heat.numerical_basis()
    # The polar/SVD certificate bounds the two ordered singular value lists by Weyl.
    eig = I(np.maximum(0.,s-1.201e-8),s+1.201e-8)
    b = I(1.)-heat.ALPHA*eig.square()
    b = I(b.lo,np.minimum(1.,b.hi))
    average = lambda x: heat.interval.reduce_sum(x) * Q(1,2048)
    z = heat.ZETA
    feedback_source_error = 128*4096*z**4/(1-z)
    assert feedback_source_error < Q(44,10**20)
    ready = heat.power(I(1.)-heat.power(I(1.)-2*heat.P*heat.P*heat.P,12),12)
    assert ready.lo > 31/32
    # The scalar failure probability bound is sufficient, independent of the
    # eigenvectors and without applying a scalar recurrence to the feedback.
    rel = heat.power(I.rational(Q(231,232)),4096)
    assert rel.hi < 2.1e-8
    for n in (1,64,512,8192):
        y = heat.power(b,2*n)
        q = average(y)
        unready_adjusted = ready*q
        assert unready_adjusted.lo > 1/232
        u = (I(np.ones_like(s))-y)*z
        # Mark each failure i with an independent rank 1/i, keep all recorded
        # outcomes, including the case that the cap is reached.
        counted = average(u+u.square()/2+u.square()*u/3)*128*4096
        tail = (128*4096*z**4)/(4*(1-z))
        assert tail < Q(11,10**20)
        print("depth",n,"trace success probability",(float(q.lo),float(q.hi)),
              "three-check feedback sum",(float(counted.lo),float(counted.hi)))
    print("feedback derivative truncation <= ",float(feedback_source_error),"times ||dY||")


if __name__ == "__main__":
    main()
