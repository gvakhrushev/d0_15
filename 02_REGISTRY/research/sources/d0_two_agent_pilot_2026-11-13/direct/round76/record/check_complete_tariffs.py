"""Extrema on all finite complete one-word-per-outcome Golden F/R codes."""
import hashlib
import json
import sys
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path

DIRECT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(DIRECT/"round75/work"))
import check_pointer_weyl as pointer

O, I = pointer.O, pointer.I
SCALE = 10**21


def full_jets():
    for path, sha in O.PINS.items():
        O.require(hashlib.sha256((pointer.ROOT/path).read_bytes()).hexdigest() == sha, "primary input")
    p, state, w, dw, fw, bw, u, du, _ = pointer.site_vector()
    rows, probs = [I(0.) for _ in range(128)], [I(0.) for _ in range(128)]
    for coeff in range(2):
        vals, ders = pointer.actions(coeff,w,dw,fw,bw,u,du)
        for j,(v,dv) in enumerate(zip(vals,ders)):
            blank = j==coeff==0
            for port in ((0,1) if blank else (1,)):
                fac = -2*(p*p if port==0 else p*p.sqrt())
                z = v*fac + state if blank and port==0 else v*fac
                dz = dv*fac
                i = 8*j+2*coeff+port
                rows[i] = 2*O.reduce_sum(z*dz)
                probs[i] = O.reduce_sum(z.square())
                if not blank:
                    rows[i-1] = p*rows[i]
                    probs[i-1] = p*probs[i]
    O.require(sum(rows,I(0.)).contains(0) and sum(rows[1::2],I(0.)).contains(0),
              "total normalization and true port jet")
    O.require(sum(probs,I(0.)).contains(1), "complete probability")
    O.require(sum(float(v.lo)>0 for v in probs) == 64,"64 positive leaves, 64 literal dark outcomes")
    return rows, probs


def largest(weights):
    # Assign the smallest signed weight to the shortest remaining leaf.
    # A state orders slots by Golden *cost*, not by the number of letters.
    weights = sorted(weights)
    n = len(weights)
    tail = [0]*(n+1)
    for k in reversed(range(n)):
        tail[k] = weights[k]+tail[k+1]
    @lru_cache(maxsize=None)
    def value(k, current, following):
        # k symbols assigned. 'following' are the long children from
        # the previous cost layer; all other children are generated below.
        if k+current+following == n:
            return tail[k+current]
        best = None
        for expand in range(min(current,n-k-current-following)+1):
            if following == expand == 0:
                continue
            m = k+current-expand
            v = tail[m]+value(m,following+expand,expand)
            if best is None or best < v:
                best = v
        if best is None:
            raise ValueError("impossible finite prefix state")
        return best
    return value(0,1,0)


def integer_rows(rows):
    low = [Q.from_float(float(v.lo))*SCALE for v in rows]
    high = [Q.from_float(float(v.hi))*SCALE for v in rows]
    return [a.numerator//a.denominator for a in low],[-((-a.numerator)//a.denominator) for a in high]


def extrema(rows):
    low,high = integer_rows(rows)
    return (I.rational(Q(-largest([-v for v in low]),SCALE)),
            I.rational(Q(-largest([-v for v in high]),SCALE)),
            I.rational(Q(largest(low),SCALE)),
            I.rational(Q(largest(high),SCALE)))


def extent(rows):
    lo,lu,hl,hi = extrema(rows)
    return [[float(lo.lo),float(lu.hi)], [float(hl.lo),float(hi.hi)]]


def minimum_cost(weights):
    low,high = integer_rows(weights)
    left = I.rational(Q(-largest([-v for v in low]),SCALE))
    right = I.rational(Q(-largest([-v for v in high]),SCALE))
    return I(left.lo,right.hi)


def shortest_source(probs,rows):
    # Finite code envelopes are concave. Two chords on each linearized
    # probability ray enclose both one-sided derivatives at the center.
    # Reconstruct the dominant blank from the much smaller nonblank rows.
    p = probs.copy()
    p[0] = 1+(-sum(p[1:],I(0.)))
    price = minimum_cost(p)
    bottom,top = -1.,1.
    for t in (Q(1,64),Q(1,256),Q(1,1024),Q(1,4096),Q(1,16384)):
        left = [q-t*d for q,d in zip(p,rows)]
        right = [q+t*d for q,d in zip(p,rows)]
        if any(min(x.lo,y.lo)<0 for x,y in zip(left,right)):
            continue
        high = (price-minimum_cost(left))/t
        low = (minimum_cost(right)-price)/t
        bottom,top = max(bottom,float(low.lo)),min(top,float(high.hi))
    O.require(bottom<=top and top-bottom<1e-5,"one-sided near-optimal expected code response")
    return O.bounds(price), [bottom,top]


@lru_cache(maxsize=None)
def all_trees(n):
    if n==1:
        return {(0,)}
    return {tuple(sorted([x+1 for x in a]+[x+2 for x in b]))
            for k in range(1,n) for a in all_trees(k) for b in all_trees(n-k)}


def exhaustive_control():
    for n in range(1,9):
        for sign in (1,-1):
            weights = sorted(sign*((k*17)%11-5) for k in range(n))
            expected = max(sum(x*y for x,y in zip(weights,ls)) for ls in all_trees(n))
            O.require(largest(weights)==expected,"ordered Golden tree DP")


def main():
    exhaustive_control()
    rows,probs = full_jets()
    active = [i for i,q in enumerate(probs) if q.lo>0]
    fixed = sum(((7+bin(i).count("1"))*dq for i,dq in enumerate(rows)),I(0.))
    p = (I.rational(5).sqrt()-1)*Q(1,2)
    six_bits = [sum((dq for i,dq in enumerate(rows) if (i>>(j+1))&1),I(0.)) for j in range(6)]
    six_reader = p*p*p*sum(six_bits,I(0.))
    abs_row = lambda v: v if v.lo >= 0 else -v if v.hi <= 0 else I(0.,max(-v.lo,v.hi))
    l1 = sum((abs_row(v) for v in rows),I(0.))
    fisher = sum((rows[i].square()/probs[i] for i in active),I(0.))
    # Full uncompressed 128-letter type code, including zero-probability labels.
    # For m=2^k, T<= (m+1)^127, ln2<.7, ln(phi)<.5 and ln(phi)>.48.
    cutoff = None
    for k in range(2,61,2):
        c_over = (I.rational(Q(7,10))*(k+1)*127+I.rational(Q(17,10))).square()+2
        err = fisher.sqrt()*c_over.sqrt()/(I.rational(Q(48,100))*2**(k//2))
        if err.hi < 0.001:
            cutoff = [k,float(err.hi)]
            break
    O.require(cutoff is not None,"finite iid code derivative budget")
    any128 = extent(rows)
    active64 = extent([rows[i] for i in active])
    separate = [extrema(rows[parity::2]) for parity in (0,1)]
    common = extrema([rows[i]+rows[i+1] for i in range(0,128,2)])
    port_first = [[float((separate[0][i]+separate[1][i]).lo),
                   float((separate[0][i+1]+separate[1][i+1]).hi)] for i in (0,2)]
    first_label = [[float(common[i].lo),float(common[i+1].hi)] for i in (0,2)]
    O.require(sum(rows[1::2],I(0.)).contains(0),"known port charge")
    O.require(six_reader.lo > 2.78e-7 and six_reader.hi < 2.81e-7,"physical six-reader price")
    required_span = (I.rational(Q(2204,100000))-I.rational(Q(306235,10**9)))/(l1*Q(1,2))
    O.require(required_span.lo>1116,"necessary length spread even after subtracting RIGHT gain")
    candidates = shortest_source(probs,rows)
    O.require(any128[0][0] > -.004345 and any128[1][1]<.004356,"all full code extrema")
    O.require(0.00018582<candidates[1][0]<candidates[1][1]<0.00018583,
              "minimum expected full code has the opposite sign to the required charge")
    print(json.dumps({"TV":O.bounds(l1*Q(1,2)), "seven_native_bits":O.bounds(fixed),
                      "actual_six_reader":O.bounds(six_reader),
                      "six_bit_primes":[O.bounds(x) for x in six_bits],
                      "fisher":O.bounds(fisher),"one_iid_budget_log2_m_and_error":cutoff,
                      "expected_shortest_128":candidates,
                      "complete_128":any128, "active_64":active64, "port_then_independent_labels":port_first,
                      "common_labels_then_port":first_label,
                      "required_spread_with_RIGHT_gain_lower":float(required_span.lo)}, sort_keys=True))


if __name__ == "__main__":
    main()
