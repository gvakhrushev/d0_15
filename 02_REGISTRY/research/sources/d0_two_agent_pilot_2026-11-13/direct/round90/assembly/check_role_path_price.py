"""A90. Matched word placements, genuine order memory, and the field of Golden odds."""
from itertools import product
import json

import mpmath as mp
import sympy as sp

mp.mp.dps = 70
p = (mp.sqrt(5) - 1) / 2
a = mp.sqrt(p)
theta = mp.asin(p)
n = 2320
pulse = n * theta - 2 * mp.pi * mp.nint(n * theta / (2 * mp.pi))
phi = 1 / p
eye = mp.eye(2)
z = mp.diag([1, -1])
gold = mp.matrix([[a, -p], [p, a]])
absolute = mp.matrix([[a, p], [p, a]])


def close(x, y):
    if abs(x-y) > mp.mpf("1e-58"):
        raise AssertionError((x,y))


def matrix_close(x, y):
    for i in range(x.rows):
        for j in range(x.cols):
            close(x[i,j], y[i,j])


def words(g, sign):
    half = g ** (n//2)
    full = half * half
    return [full*sign*sign, sign*half*sign*half, sign*full*sign]


def check_matched_words():
    actual = words(gold,z)
    matrix_close(actual[0], gold**n)
    matrix_close(actual[1], eye)
    matrix_close(actual[2], (gold**n).T)
    # Common scalar normalization PER G prevents overflow and changes no ratio.
    for g in (absolute/(a+p), mp.matrix([[p,p*p],[p*p,p]])):
        raw = words(g,eye)
        matrix_close(raw[0],raw[1])
        matrix_close(raw[1],raw[2])


def marker_blocks():
    # Coordinates flag, parked 0 on port, spin. Test the whole accepted subspace.
    li = sp.Matrix([[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]])
    ident = sp.eye(4)
    source = sp.diag(ident,li,ident,li)
    swap = sp.zeros(16,16)
    for flag,port,spin in product(range(2),range(2),range(4)):
        swap[8*port+4*flag+spin,8*flag+4*port+spin] = 1
    columns = list(range(4)) + list(range(8,12))
    for k in range(3):
        # k legal SourceI's while the flag is on the port; other calls see 0.
        circuit = swap * source**k * swap * source**(2-k)
        target = sp.diag(ident,ident,li**k,li**k)
        assert circuit[:,columns] == target[:,columns]
        assert (li**k + (li**k).T)/2 == (1-k)*ident


def archive_response(visibility):
    amplitude = p * mp.sin(448 * theta)
    material = [2*p**3*amplitude**2*f for f in (1,mp.mpf(21)/16)]
    def total(xs):
        # The split is an illustrative common fine upstream tape exactly as in A89.
        leaves = [mp.mpf(2)/3]
        for j,s,m,phase,b in product(range(2),repeat=5):
            pm = material[j] if m else 1-material[j]
            x = (-1)**(s^m)*xs[j^s]
            c,t = mp.cos(x),mp.sin(x)
            q = p*p*c*c + p*t*t + 2*a*p*visibility*c*t
            if phase:
                q = 1-q
            leaves.append(pm*(q if b else 1-q)/24)
        close(sum(leaves),1)
        return sum(mp.sqrt(prob) for prob in leaves)
    rows = []
    for k in range(2):
        plus,minus = [0,0],[0,0]
        plus[k],minus[k] = pulse,-pulse
        rows.append(mp.log(total(minus)/total(plus))/mp.log(phi))
    close(rows[0],-rows[1])
    return rows


def check_number_field():
    # Exact F = Q[p] / (p^2+p-1); a is an extra generator with a^2=p.
    # tan(n theta) = a * Y_n / X_n. Recurrence from (1+i*a)^n.
    # Store F-integers as c+d*p, never round the actual 2321-step word.
    def mul_p(x):
        c,d = x
        return d,c-d
    X,Y = (1,0),(0,0)
    wanted = {1,n-1,n+1}
    for step in range(1,n+2):
        pY = mul_p(Y)
        X,Y = (X[0]-pY[0], X[1]-pY[1]), (X[0]+Y[0], X[1]+Y[1])
        if step in wanted:
            assert X != (0,0) and Y != (0,0)
    # Norm p=-1; the new positive metric reproduces center Born weights.
    t = (sp.sqrt(5)-1)/2
    assert sp.simplify(t*(-1-t)) == -1
    assert sp.simplify(t**2/t + t**4/t**2 - 1) == 0


def test_rational_metric_and_entangled_output():
    t = (sp.sqrt(5)-1)/2
    metric = sp.diag(1,1/t)
    reduced = sp.Matrix([[1,-1],[t,1]])
    assert (reduced.T*metric*reduced - (1+t)*metric).applyfunc(sp.simplify).is_zero_matrix
    # Native word on two prepared zeros. Cross-check by multiplying all four columns.
    cx = mp.matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
    both = mp.matrix(4)
    for i,j in product(range(4),repeat=2):
        both[i,j] = gold[i//2,j//2]*gold[i%2,j%2]
    output = both*cx*mp.matrix([a,0,p,0])
    close(sum(x*x for x in output),1)
    close(output[1],a*p*(a-p))
    close(output[3],a*p*(a+p))
    odds = (output[3]/output[1])**2
    close(odds,((1+a)/(1-a))**2)
    assert odds > 1
    return mp.nstr(odds,17)


def main():
    check_matched_words()
    marker_blocks()
    check_number_field()
    entangled_odds = test_rational_metric_and_entangled_output()
    rows = {r:archive_response(r) for r in (-1,0,1)}
    close(rows[0][0],0)
    close(rows[1][0],-rows[-1][0])
    assert rows[1][0] < 0
    output = {"golden_gates_per_field_word":n, "logical_Z_per_field_word":2,
              "primitive_source_I_per_marker":2, "swaps_per_marker_after_parking":2,
              "microscopic_absolute_kernel_depends_on_signed_setting":False,
              "golden_odds_negative_conjugate_at_exponents":[1,1-n,1+n],
              "marked_log_price_difference_illustrative_common_tape":{
                  str(r):[mp.nstr(x,16) if abs(x)>mp.mpf("1e-58") else "0" for x in row]
                  for r,row in rows.items()},
              "native_entangled_odds_outside_Q_sqrt5":entangled_odds,
              "physical_C_closed":False, "GR_closed":False}
    print(json.dumps(output,indent=2))


if __name__ == "__main__":
    main()
