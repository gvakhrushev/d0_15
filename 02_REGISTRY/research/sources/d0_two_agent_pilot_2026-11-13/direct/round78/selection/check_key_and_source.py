"""Test a physical fair-key calibration and the response of actual retained memory."""
from pathlib import Path
import sys

DIRECT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(DIRECT / "round78/memory"))
import check_blank_information as mem

I, O = mem.I, mem.O


def determinant(rows):
    (a, b, c), (d, e, f), (g, h, i) = rows
    return a*(e*i-f*h)-b*(d*i-f*g)+c*(d*h-e*g)


def bounds(x):
    return [float(x.lo), float(x.hi)]


def fair_key_test():
    # The original canonical coins have P(01)=P(10)=p^3. Conditional
    # on readiness the two stored physical keys occur with equal weights.
    import sympy as sp
    q = sp.symbols("q", positive=True)
    binary = (q, 1-q)
    for z in (0, 1):
        total = sum(binary[k ^ z]/2 for k in (0, 1))
        assert sp.simplify(total-sp.Rational(1, 2)) == 0
        for k in (0, 1):
            posterior = binary[k ^ z]/(2*total)
            assert sp.simplify(posterior/binary[k ^ z]-1) == 0
            # Evidence gained now, followed by learning the true key.
            assert sp.simplify((2*posterior)/posterior-2) == 0
    # The log scoring factors for accepted blank multiply a fixed literal
    # code weight. Pay both original ready pairs and the two cipher digits.
    p = (sp.sqrt(5)-1)/2
    assert sp.simplify(p**3 * (p+p**2) * 2*q - 2*p**3*q) == 0


def main():
    fair_key_test()
    import contextlib
    import io
    with contextlib.redirect_stdout(io.StringIO()):
        data = mem.run()
    probabilities = data["P"]
    phi_log = mem.LOG_PHI
    matrix3 = []
    for f, entries in data["fields"].items():
        a,b,c = probabilities
        da,db,dc = (x["mass"] for x in entries)
        s2, s3 = b/a, c/b
        u, v = (db-s2*da)/a, (dc-s3*db)/b
        target = (u/s2-v/s3)/phi_log
        dr = data["curvature"][f]["blank_gain"]
        # Explicitly paid realized single binary confirmation at each return.
        work = u-v
        remainder = target-(work-dr)
        alternative = data["curvature"][f]["binary_H"]
        scale = 10**6 if f == "A75" else 10**10
        matrix3.append((scale*u,scale*(v-2*u),scale*dr))
        print(f, "target",bounds(target),"work minus gain",bounds(work-dr),
              "residual",bounds(remainder),"negative entropy-gain of key",bounds(alternative),
              flush=True)
        if f == "A75":
            assert -2.69e-7 < remainder.lo <= remainder.hi < -2.67e-7
            fraction = (work-dr)/target
            print("fraction in this direction",bounds(fraction))
    det = determinant(matrix3)
    print("scaled determinant (ds2,ds3-2ds2,dRIGHT)",bounds(det))
    assert det.lo > 0 or det.hi < 0


if __name__ == "__main__":
    main()
