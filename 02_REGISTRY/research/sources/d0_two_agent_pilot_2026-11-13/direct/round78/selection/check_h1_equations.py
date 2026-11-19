"""Certified H.1 probability chart and orientation of archive length minus entropy."""
from fractions import Fraction as F
from math import comb, log, lcm


def main():
    # The positive root of p²+p=1 lies strictly between these rationals.
    left, right = F(61803398874, 10**11), F(61803398876, 10**11)
    assert left**2 + left < 1 < right**2 + right
    weights = [F((-1)**(j-1)*comb(8, j), j*j) for j in range(1, 9)]
    denominator = lcm(*(w.denominator for w in weights))
    assert denominator == 705600
    count = sum(denominator*abs(w) for w in weights)
    assert count == 20316969
    for degree in range(8):
        assert sum(w*j**(2+degree) for j,w in enumerate(weights, 1)) == (degree == 0)

    # Every positive and reversed arm is between p² and p.
    # 4+Xi lies in [2,6], lambda_vis <= p^7 and 6p^7 < 1.
    assert 6*right**7 < 1
    low, high = count*left**38, count*right**37
    assert F(23,100) < low < high < F(38,100)
    # F'(Q)>0 iff Q > p³/(1+p³); the stronger F'(Q)>1/2
    # is equivalent to ((1-Q)/Q)² p^5 < 1.
    assert ((1-low)/low)**2 * right**5 < 1
    print("H.1 mark bounds", float(low), float(high))
    print("range of archive slope", *(3 - log(float((1-q)/q))/log(1/float(left))
                                      for q in (low, high)))
    print("positive source on every allowed direction at fixed calibration")


if __name__ == "__main__":
    main()
