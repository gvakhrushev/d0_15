"""Conditional fine-label/RIGHT entropy on the primary two-site variation."""
import hashlib
import json
import os
import sys
from pathlib import Path

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
sys.dont_write_bytecode = True
import numpy as np

DIRECT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(DIRECT / "round75/work"))
import check_pointer_weyl as W

O, I, spectral = W.O, W.I, W.spectral


class Branch:
    def __init__(self):
        self.mass = I(0.)
        self.dmass = I(0.)
        self.raw = I(0.)
        self.direction = I(0.)

    def add(self, q, dq, slog, dlog):
        # slog=Tr(B log rho), dlog=Tr(dB log rho), rho=B/q.
        self.mass += q
        self.dmass += dq
        self.raw += q * O.logarithm(q) + slog
        self.direction += dq * O.logarithm(q) + dlog

    def entropy(self, logphi):
        return (O.logarithm(self.mass) - self.raw / self.mass) / logphi

    def derivative(self, logphi, stationary=False):
        transport = I(0.) if stationary else self.dmass * self.raw / self.mass.square()
        return (transport - self.direction / self.mass) / logphi


def main():
    for rel, digest in O.PINS.items():
        O.require(hashlib.sha256((W.ROOT / rel).read_bytes()).hexdigest() == digest, rel)
    p, state, w, dw, fw, bw, u, du, _ = W.site_vector()
    ports = [Branch(), Branch()]
    mark19 = [Branch(), Branch()]
    count = 0
    old = I(np.zeros((128, 128)))
    dold = I(np.zeros((128, 128)))
    for coeff in range(2):
        values, directions = W.actions(coeff, w, dw, fw, bw, u, du)
        for j, (v, dv) in enumerate(zip(values, directions)):
            blank = j == coeff == 0
            for e in ((0, 1) if blank else (1,)):
                fac = -2 * (p*p if e == 0 else p*p.sqrt())
                Z = W.flatten(v*fac + state if blank and e == 0 else v*fac)
                DZ = W.flatten(dv*fac)
                active = np.any((DZ.lo != 0) | (DZ.hi != 0), axis=1)
                za, da = Z[active], DZ[active]
                cross = spectral.matmul(spectral.transpose(za), da)
                DB = cross + spectral.transpose(cross)
                B = spectral.matmul(spectral.transpose(Z), Z)
                dlog, q, _ = spectral.posterior_certificate(B, DB, za, da, I(1.))
                # The same verified matrix-log routine with test matrix B gives the
                # unnormalised static entropy. ||B||_1=||Z||_F^2 <= 2||Z||_F^2.
                slog, _, _ = spectral.posterior_certificate(B, B, Z, Z, I(1.))
                dq = O.reduce_sum(I(np.diag(DB.lo), np.diag(DB.hi)))
                copies = [(e, I(1.))] if blank else [(0, p), (1, I(1.))]
                for port, m in copies:
                    index = 8*j + 2*coeff + port
                    args = (m*q, m*dq, m*slog, m*dlog)
                    ports[port].add(*args)
                    mark19[int(index == 19)].add(*args)
                    old += m * B
                    dold += m * DB
                    count += 1
    O.require(count == 64 and old.contains(np.eye(128)/128)
              and dold.contains(np.zeros((128, 128))), "all active labels, original fixed RIGHT")
    logphi = -O.logarithm(p)
    report = {}
    for name, group, fixed in (("port", ports, True), ("mark19", mark19, False)):
        y0, y1 = group
        O.require((y0.mass + y1.mass).contains(1) and (y0.dmass + y1.dmass).contains(0),
                  name + " total mass and its tangent")
        if fixed:
            O.require(y0.dmass.contains(0) and y1.dmass.contains(0), "original port identity on DR=0")
        e0, e1 = (y.entropy(logphi) for y in group)
        d0, d1 = (y.derivative(logphi, stationary=fixed) for y in group)
        a = y1.mass.sqrt()
        pref = (1 + a) / 2
        dpref = I(0.) if fixed else y1.dmass / (4*a)
        penalty = -pref * (d1 - d0) - dpref * (e1 - e0)
        if fixed:
            fee_derivative = I(0.)
        else:
            # The original emitted port costs 1+P; mark 19 always has P=1.
            delta_fee = (I(1.) - ports[1].mass) / y0.mass
            ddelta_fee = delta_fee * y1.dmass / y0.mass
            fee_derivative = dpref * delta_fee + pref * ddelta_fee
        if fixed:
            O.require(-0.000031434710 < d0.lo <= d0.hi < -0.000031434659, "zero-port branch")
            O.require(-0.018741946 < d1.lo <= d1.hi < -0.018741927, "one-port branch")
            O.require(0.009727190 < penalty.lo <= penalty.hi < 0.009727201, "stopped port CQ sign")
        else:
            O.require(0.053721221 < penalty.lo <= penalty.hi < 0.053721231, "moving mass of mark 19")
            O.require(0.05362 < (penalty + fee_derivative).lo
                      <= (penalty + fee_derivative).hi < 0.05365, "known original fee on mark 19")
        report[name] = {key: O.bounds(value) for key, value in [
            ("x", y1.mass), ("dx", y1.dmass), ("e0", e0), ("e1", e1),
            ("de0", d0), ("de1", d1), ("de1-de0", d1-d0),
            ("D[-(1+sqrt(x))(e1-e0)/2]", penalty),
            ("D[conditional original port fee minus branch entropy]", penalty + fee_derivative)]}
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
