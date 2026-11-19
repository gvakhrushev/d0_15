"""Full Julia tangent, protected native coordinate and a two-site uncentred report."""
import json
import math
import numpy as np


P = (math.sqrt(5) - 1) / 2
THETA = math.asin(P)
ORDER = (0, 2, 3, 1)
NU = 0.5
D = 32 * 8 * 4**4
H = 0.25
F = 1 * 32  # flatten (out,in): single e+ and vacuum
DONORS = [1 * 32, 2 * 32]
LAM = -(1099527356400 + 824647876594 * P) / 68720525311


def check(condition, message):
    if not condition:
        raise ValueError(message)


def creator(coords):
    c = np.zeros((16, 16))
    for pos, direction in enumerate(ORDER):
        for mask in range(16):
            if mask & (1 << direction):
                continue
            parity = sum((mask >> a) & 1 for a in ORDER[:pos])
            c[mask | (1 << direction), mask] = (-1)**parity * coords[direction]
    return c


def mul(a, b):
    return np.einsum("ij,j...->i...", a, b)


def sqrt_psd(m):
    vals, vecs = np.linalg.eigh(m)
    return mul(vecs * np.sqrt(vals), vecs.T)


def julia(u):
    c = creator(u)
    eye = np.eye(16)
    return np.block([[c, sqrt_psd(eye-mul(c,c.T))], [sqrt_psd(eye-mul(c.T,c)), -c.T]])


def julia_derivative(u, v):
    c, a = creator(u), creator(v)
    s = math.sqrt(1-u@u)
    t = 1/(1+s)
    dt = (u@v)/(s*(1+s)**2)
    out = -dt*(mul(c,c.T))-t*(mul(c,a.T)+mul(a,c.T))
    inp = -dt*(mul(c.T,c))-t*(mul(c.T,a)+mul(a.T,c))
    return np.block([[a, out], [inp, -a.T]])


def geometry_test():
    plus, minus = np.eye(4)[:2]
    base = NU * minus
    source = julia(base).ravel()
    w = np.column_stack([-julia_derivative(base, unit).ravel()
                         for unit in (plus, minus)])
    check(np.max(abs(mul(w.T, source))) < 1e-11, "full tangent orthogonality")
    check(np.array_equal(w[F], [-1, 0]), "dark channel")
    check(source[F] == 0, "nonzero initial signal")
    w[F] = 0
    u, singular, right = np.linalg.svd(w, full_matrices=False)
    # Set the exact invariant row; do not attribute LAPACK roundoff to a real drive.
    check(max(abs(u[F])) < 1e-14, "dark row of residual")
    u[F] = 0
    precision = []
    for b in (-0.40, 0.0, 0.23, 0.41):
        v = NU*(plus-b*minus)
        donor = julia(v).ravel()[DONORS]
        errors = []
        for t in (0.02, 0.01, 0.005):
            for sign in (-1, 1):
                delta = sign*t
                new = source.copy()
                live = donor.copy()
                # Actual coordinate rotation on (donor+, f); sin(gamma) = delta.
                new[F] = -delta * donor[0]
                live[0] *= math.sqrt(1-delta**2)
                src, dst = mul(right,live), mul(u.T,new)
                cs, sn = np.cos(delta*singular), np.sin(delta*singular)
                live += mul(right.T,(cs-1)*src-sn*dst)
                new += mul(u,sn*src+(cs-1)*dst)
                check(new[F] == -delta*NU, "protected finite coordinate")
                true = julia(base-delta*v).ravel()
                error = np.linalg.norm(np.r_[new-true, live-donor])
                if sign == 1:
                    errors.append(error)
                check(error <= 20*t*t, "whole-state quadratic bound")
        ratios = [errors[i]/errors[i+1] for i in (0, 1)]
        check(min(ratios) > 3.98 and max(ratios) < 4.02, "quadratic convergence")
        precision.append([round(x, 5) for x in ratios])
    return precision


def native_dark_rotation():
    # Literal phase word on a two-control witness; larger address cubes use the same identity.
    k = 2
    match = 1
    n = 580
    for x in range(1 << k):
        power = sum((-1)**(bin((x^match)&s).count("1"))*n for s in range(1 << k))
        check(power == (n*2**k if x == match else 0), "off-address leakage")
    return round(math.sin(n*2**k*THETA), 12)


def spectral_entry(k2, k3):
    n = np.zeros((4, 4))
    for a, coef in ((2, k2), (3, k3)):
        n[1, a] = n[a, 0] = coef
    u = np.eye(4)+n+mul(n,n)/2
    eta = np.array([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]])
    check(np.allclose(mul(mul(u.T,eta),u), eta), "null Lorentz lift")
    return u[2, 0], u[3, 0]


def hphi(q):
    return -(q*math.log(q)+(1-q)*math.log1p(-q))/math.log(1/P)


def archive_test():
    # The two hidden coherent sign arms remain in WORK; only O is dephased.
    # Explicitly construct WORK x O to test the actual conditional quantum ranks.
    ops = [np.array([[0.,s],[s,0.]]) for s in (1.,-1.)]
    head = np.array([[math.sqrt(P),-P],[P,math.sqrt(P)]])
    entropies = []
    probs = []
    for t in (-0.13, 0.13):
        old = np.array([t, math.sqrt(1-t*t)])
        psi = np.zeros((2,2,2))
        for arm, op in enumerate(ops):
            arms = np.column_stack((math.sqrt(P)*old, P*mul(op,old)))
            psi[arm] = mul(arms,head)/math.sqrt(2)
            if arm == 0:
                psi[arm] = psi[arm,:,::-1]
        work_o = psi.reshape(4,2)
        cq = np.zeros((8,8))
        for o in range(2):
            cq[4*o:4*o+4,4*o:4*o+4] = np.outer(work_o[:,o],work_o[:,o])
        ev = np.linalg.eigvalsh(cq)
        nz = ev[ev>1e-14]
        q = float(work_o[:,1]@work_o[:,1])
        check(len(nz)==2 and abs(q-(0.5+4*P**3*old.prod())) < 1e-12,
              "purified record probabilities or conditional ranks")
        s = -sum(v*math.log(v) for v in nz)/math.log(1/P)
        check(abs(s-hphi(q))<1e-12, "full WORK and binary entropy")
        entropies.append(s)
        probs.append(q)
    check(abs(sum(probs)-1)<1e-12 and abs(entropies[0]-entropies[1])<1e-12,
          "full conditional archive symmetry")
    return round(entropies[0],10)


def report_test():
    b, eta = 2*P**3*(1-5/16), P**3*5/16*H**2
    e0 = 2*(P*math.sin(448*THETA)/H)**2
    energies = (e0, 2*e0)
    # Two small unequal independent link stencils; weights h^4*w sum to 1 per strip.
    links = (((0.08,-0.09), (0.06,0.01), (-0.05,-0.11)),
             ((0.09,0.02), (0.10,-0.03), (0.04,0.04)))
    curv = []
    for center, east, north in links:
        cx, cy = spectral_entry(*center)
        ex, _ = spectral_entry(*east)
        _, ny = spectral_entry(*north)
        curv.append((cx-ex+cy-ny)/H**2)
    check(abs(sum(curv)) > 0.1, "common curvature accidentally cancelled")
    # For one native balanced transposition use physical ± arms and both raw probabilities.
    for sign in (-1, 1):
        x, y = -NU*sign/64/math.sqrt(D), 0.08/(2*math.sqrt(D))
        click0 = 2*P**3*(x-y)**2
        click1 = 2*P**3*(x+y)**2
        check(abs((1-click0+click1)/2 - (0.5+4*P**3*x*y)) < 3e-15,
              "coherent balanced arms")
    # Example gain for numerical archive check. Circuit gain is set by actual slot compiler.
    gain, alpha, d = 1e-4, 3/17, 1/32
    rows = [r-2*LAM*e for r,e in zip(curv, energies)]
    for pulse in ((1,0), (0,1), (1,1)):
        recorded = []
        for sign in (-1, 1):
            value = 0.0
            for j, ej in enumerate(energies):
                pm = b+eta*ej
                for m, prob in ((0,1-pm),(1,pm)):
                    q = 0.5+sign*gain*d*pulse[j]*(curv[j]-2*LAM*(m-b)/eta)
                    check(0<q<1, "invalid probability")
                    value += alpha/2*prob*(1+q-hphi(q))
            recorded.append(value)
        target = sum(v*r for v,r in zip(pulse,rows))
        recovered = (recorded[1]-recorded[0])/(2*d*alpha*gain/2)
        check(abs(recovered-target) < 1e-8, "retained-history finite secant")
    check(abs(sum(rows))>0.1, "common mode accidentally blind")
    return [round(x,10) for x in curv], [round(x,10) for x in rows]


def main():
    ratios = geometry_test()
    curv, rows = report_test()
    result = {"julia_full_error_ratios_at_halved_steps": ratios,
              "protected_native_example_sin_2320theta": native_dark_rotation(),
              "off_cartan_curvature": curv, "explicit_full_work_entropy": archive_test(), "two_uncentred_volume_rows": rows,
              "common_volume_row": round(sum(rows), 10),
              "physical_full_book_selection_proved": False,
              "GR_closed": False}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
