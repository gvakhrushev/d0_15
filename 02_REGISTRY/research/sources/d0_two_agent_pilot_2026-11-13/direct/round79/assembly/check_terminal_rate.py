"""Three native preparations rule out a universal price for the last active phase edge."""
from fractions import Fraction as F
from pathlib import Path
import sys

import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parent.parent/"heat"))
from check_phase_work import a,p,one,enclosure,interval,plus,minus,times,trace_distance,inside
from check_phase_price import word


def trig(n):
    c,s=one,0*p
    for _ in range(n):
        c,s=a*c-p*s,p*c+a*s
    return c,s


def fourth(x):
    return x*x*x*x


def gap(k):
    c,s=trig(k+1)
    xi=2*c*s
    distances=[trace_distance(p+side*p*p*xi) for side in (1,-1)]
    w=[fourth(trig(k)[0]),fourth(trig(k+2)[0])]
    records=[]
    for j,target in enumerate((4,3)):
        cold,cq,count,overlaps=word(k,target,5,True)
        assert count==26 and np.allclose(cold.T@cold,float(enclosure(w[j])[0])*np.eye(4))
        assert abs(overlaps[-1] - float(enclosure(p+(1-2*j)*p*p*xi)[0]))<2e-12
        records.append((cq,overlaps))
    assert np.allclose(records[0][0],records[1][0])
    x,y=records[0][1],records[1][1]
    assert np.allclose(x[:18],y[:18]) and np.allclose(x[18:],list(reversed(y[18:])))
    # log(1-z+zw) differs from z(w-1) by at most z²/(2(1-z)).
    z=F(1,2**20)
    gap_error=4*z*z/(1-z)
    approx=times(4*z, enclosure(w[1]-w[0]))
    return plus(approx,(-gap_error,gap_error)), minus(*distances)


def main():
    old,dist=gap(0)
    # Each of the ten preparation letters can differ by trace norm <=2D_f.
    # Both phase secants include the heat on the same complete paid 18-block tail.
    heat=F(240,359*4**18)
    for k,expected_cost,expected_dist in ((1,('0.00000245','0.00000247'),('.53','.54')),
                                          (5,('0.00000025','0.00000026'),('-.062','-.060'))):
        new,d=gap(k)
        delta=plus(minus(new,old),(-heat,heat))
        change=minus(d,dist)
        inside(delta,*expected_cost)
        inside(change,*expected_dist)
        print("preparation",k,"spectral gap change",tuple(map(float,delta)),
              "last-edge gap change",tuple(map(float,change)))


if __name__=='__main__':
    main()
