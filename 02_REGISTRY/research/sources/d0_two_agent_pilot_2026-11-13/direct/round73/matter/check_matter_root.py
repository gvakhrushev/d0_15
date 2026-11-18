"""Exact finite-rank certificates for the original full-CAR prepared energy at L=4."""
from collections import defaultdict
from fractions import Fraction
from math import gcd, isqrt, prod, sqrt
from pathlib import Path
import sys

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[7]
PRIMARY = ROOT / "02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source"
sys.path.insert(0, str(PRIMARY))
import check_primary_car_preparation_source as core

MOD = 378349617288409583817001
COUNTS = list(core.actual_counts(ROOT))
assert min(COUNTS) == 29 and max(COUNTS) == 78 and sum(COUNTS) == 10946
SITES = core.SITES_LIST
FOURIER = core.fourier_numerators()
PRIMES = sorted({prime for n in COUNTS for prime in sp.factorint(n)} | {5})
SCALE = 10**18


def certify_modulus():
    divisors = sp.factorint(MOD-1)
    assert prod(int(q)**m for q,m in divisors.items()) == MOD-1
    for q in divisors:
        assert all(q % d for d in range(2, isqrt(q)+1))
        assert any(pow(b, MOD-1, MOD) == 1 and gcd(pow(b, (MOD-1)//q, MOD)-1, MOD)==1
                   for b in range(2,110))  # fully factored Lucas/Pocklington criterion


def blocks(mode):
    """Normalized by the common positive 256*sigma^2/(10946*128^2)."""
    if mode == "modular":
        roots = {q:int(sp.sqrt_mod(q, MOD)) for q in PRIMES}
        assert all(root*root % MOD == q for q,root in roots.items())
        p = (roots[5]-1)*pow(2,-1,MOD) % MOD
        a = int(sp.sqrt_mod(p, MOD))
        assert a*a % MOD == p and (p*p+p-1)%MOD == 0
        weight = [prod(roots[q]**k for q,k in sp.factorint(n).items()) % MOD for n in COUNTS]
        inv_a = pow(a,-1,MOD)
    elif mode == "rational":
        weight = [Fraction(isqrt(n*SCALE*SCALE), SCALE) for n in COUNTS]
        # Floor(SCALE*sqrt(phi)); verify the endpoints without float arithmetic.
        v = isqrt((SCALE*SCALE + isqrt(5*SCALE**4))//2)
        assert (2*v*v-SCALE**2)**2 <= 5*SCALE**4 < (2*(v+1)**2-SCALE**2)**2
        inv_a = Fraction(v, SCALE)
    else:
        weight = [sqrt(n) for n in COUNTS]
        a = sqrt((sqrt(5)-1)/2)
        inv_a = 1/a
    by_output = defaultdict(list)
    for i,site in enumerate(SITES):
        for mask in [0,1,14,15]:
            entries = defaultdict(int)
            literal = core.flat_column(site,mask)
            assert sum(abs(v) for v in literal.values()) <= 128
            for (out, grade, src), coefficient in literal.items():
                assert coefficient.denominator == 1
                entries[(out,grade)] += coefficient.numerator * weight[core.site_index(src)]
            for address,val in entries.items():
                by_output[address].append((i,mask,val))
    raw_kernel = {z:sum(a*b for a,b in zip(FOURIER[0],FOURIER[i])) for i,z in enumerate(SITES)}
    assert max(map(abs,raw_kernel.values())) <= 64
    # Fourier pairs give identical kernels at equal displacement, including the periodic seam.
    fourier_array = np.asarray(FOURIER, dtype=np.int64)
    complete_gram = fourier_array @ fourier_array.T
    pairs = {}
    for i,x in enumerate(SITES):
        for j,y in enumerate(SITES):
            pairs[i,j] = raw_kernel[tuple((a-b)%core.SIZE for a,b in zip(x,y))]
            assert pairs[i,j] == complete_gram[i,j]
    hs = {k:[[0]*len(SITES) for _ in SITES] for k in (0,15)}
    mass = [0]*len(SITES)
    for entries in by_output.values():
        for i,mask,v in entries:
            for j,grade,w in entries:
                if mask==14 and grade in (1,14):
                    mass[i] += v*w*pairs[i,j]*(inv_a if grade==1 else 1)
                elif mask in (0,15) and mask == grade:
                    hs[mask][i][j] += v*w*pairs[i,j]
                elif (mask,grade) in ((0,15),(15,0)):
                    raise AssertionError("D columns of degree 0 and 4 share an output grade")
    for mat in hs.values():
        for i,m in enumerate(mass):
            mat[i][i] -= m
        if mode == "modular":
            for row in mat:
                row[:] = [x%MOD for x in row]
    return hs


def det_mod(matrix, indices):
    mat = [[matrix[i][j] for j in indices] for i in indices]
    product = 1
    for k in range(len(mat)):
        pivotrow = next((i for i in range(k,len(mat)) if mat[i][k]), None)
        if pivotrow is None:
            return 0
        if pivotrow != k:
            mat[k],mat[pivotrow] = mat[pivotrow],mat[k]
            product = -product
        pivot = mat[k][k]
        product = product*pivot%MOD
        inverse = pow(pivot,-1,MOD)
        lead = mat[k]
        for i in range(k+1,len(mat)):
            mult = mat[i][k]*inverse%MOD
            if mult:
                mat[i][k+1:] = [(v-mult*u)%MOD for v,u in zip(mat[i][k+1:],lead[k+1:])]
    return product%MOD


def solve_mod(matrix, rhs):
    a = [list(row)+[b] for row,b in zip(matrix,rhs)]
    n = len(rhs)
    for k in range(n):
        i = next(i for i in range(k,n) if a[i][k] % MOD)
        a[k],a[i] = a[i],a[k]
        scale = pow(a[k][k], -1, MOD)
        a[k] = [v*scale%MOD for v in a[k]]
        for i in range(n):
            if i != k and a[i][k]:
                mul = a[i][k]
                a[i] = [(v-mul*u)%MOD for v,u in zip(a[i],a[k])]
    return [row[-1] for row in a]


def wave_equation(values, i):
    site = SITES[i]
    read = lambda z: values[core.site_index(z)]
    result = 0
    for mu,nu,sign in [(0,1,1),(1,0,1),(2,2,-1),(3,3,-1)]:
        prev = core.step(site,mu,-1)
        result += sign*(read(core.step(site,nu,1))-read(site)-read(core.step(prev,nu,1))+read(prev))
    return 16*result   # h^-2


def wave_row(indices, w):
    result = []
    for i in indices:
        unit = [0]*len(SITES)
        unit[i] = 1
        result.append(wave_equation(unit,w))
    return result


def certify_real_response(center, indices, external, boundary, estimate):
    n = len(indices)
    er = Fraction(10**11,SCALE)
    # Each D-column has total absolute integer coefficients <=128, each root <9,
    # and each Fourier kernel <=64. The estimated error of a single Gram entry
    # is <=e1; absolute entries <=g1.  The diagonal additionally sums 256 pairs
    # of blocks, one multiplied by 1/a (<2) with uncertainty 1/SCALE.
    e1 = Fraction(64*128**2*19,SCALE)
    g1 = 64*128**2*81
    assert e1 + 256*(3*e1+Fraction(g1,SCALE)) < er
    B = [[center[i][j] for j in indices] for i in indices]
    rhs = [-sum(center[i][j]*boundary[j] for j in external) for i in indices]
    inv = np.linalg.inv(np.array(B,dtype=float))
    def nearest(x): return Fraction(round(float(x)*10**14),10**14)
    T = [[nearest(d) for d in row] for row in inv]
    x0 = [nearest(estimate[i]) for i in indices]
    normT = max(sum(map(abs,row)) for row in T)
    defect = max(sum(abs(int(i==j)-sum(T[i][k]*B[k][j] for k in range(n)))
                     for j in range(n)) for i in range(n)) + normT*n*er
    assert defect < Fraction(1,100)
    res = max(abs(sum(c*x for c,x in zip(row,x0))-v) for row,v in zip(B,rhs))
    err = normT*(res+er*(n*max(map(abs,x0))+sum(abs(boundary[j]) for j in external)))/(1-defect)
    assert err < Fraction(1,10**8)
    raw = list(boundary)
    for i,x in zip(indices,x0):
        raw[i] = x
    w = core.site_index(core.W)
    wave = wave_equation(raw,w)
    assert Fraction(1037443,10**7) < raw[w]-err <= raw[w]+err < Fraction(1037445,10**7)
    assert Fraction(3280769,10**6) < wave-256*err <= wave+256*err < Fraction(3280771,10**6)

    # A Hessian is symmetric. Thus the same inverse bound also certifies
    # K_II^T z = L_I^T, where L is the actual target wave row at w.
    assert B == list(map(list,zip(*B)))
    L = wave_row(indices,w)
    z0 = [nearest(x) for x in np.linalg.solve(np.asarray(B,dtype=float).T, L)]
    zres = max(abs(sum(c*x for c,x in zip(row,z0))-d) for row,d in zip(B,L))
    zerr = normT*(zres+er*sum(map(abs,z0)))/(1-defect)
    z1max = sum(abs(x)+zerr for x in z0)
    z2max_sq = sum((abs(x)+zerr)**2 for x in z0)
    assert z1max < Fraction(602649,10**8)
    assert z2max_sq < Fraction(191829,10**8)**2
    unit = Fraction(2*256,10946*128**2)
    assert unit == Fraction(1,350272)
    needed = unit*(wave-256*err)
    assert needed > Fraction(1554,10**6)*z1max
    assert needed**2 > Fraction(4882,10**6)**2*z2max_sq


def main():
    certify_modulus()
    finite = blocks("modular")
    real = blocks("float")
    center = blocks("rational")
    w = core.site_index(core.W)
    full = list(range(len(SITES)))
    interior = [i for i,(u,v,x,y) in enumerate(SITES) if u in (1,2) and x in (1,2) and y in (1,2)]
    assert len(interior) == 32 and w in interior
    for name,indices in [("periodic",full),("collar",interior),("site",[w])]:
        for mask in (0,15):
            exact = det_mod(finite[mask],indices)
            assert exact != 0
            matrix = np.asarray(real[mask])[np.ix_(indices,indices)]
            spectrum = np.linalg.eigvalsh(matrix)
            print(name, mask, len(indices), exact, "diagnostic min_abs_eigenvalue",min(abs(spectrum)))
    norm = 2*256/(10946*128**2)*((sqrt(5)-1)/2)**6
    print("one-site raw Hessian", norm*real[15][w][w])
    b = [core.B(z) for z in SITES]
    assert all(wave_equation(b,i)==0 for i in interior)
    raw = finite[15]
    external = [i for i in full if i not in interior]
    bm = [(v.numerator*pow(v.denominator,-1,MOD))%MOD for v in b]
    exact = solve_mod([[raw[i][j] for j in interior] for i in interior],
                      [-sum(raw[i][j]*bm[j] for j in external)%MOD for i in interior])
    mat = np.asarray(real[15])
    observe = np.asarray(b,dtype=float)
    rhs = [-sum(mat[i,j]*observe[j] for j in external) for i in interior]
    observe[interior] = np.linalg.solve(mat[np.ix_(interior,interior)],rhs)
    # On the unchanged primary target B, the required extra physical gradient
    # per t is -K B /350272. Its pairing checks both sign and the old A72 row.
    primary_force = [-sum(raw[i][j]*bm[j] for j in full)%MOD for i in interior]
    L = wave_row(interior,w)
    adjoint = solve_mod([[raw[j][i] for j in interior] for i in interior],L)
    paired = sum(z*r for z,r in zip(adjoint,primary_force)) % MOD
    force_w = primary_force[interior.index(w)]*pow(350272,-1,MOD)%MOD
    assert (force_w*force_w*1684**2*13-21**2) % MOD == 0
    for i,x in zip(interior,exact):
        bm[i] = x
    assert all(sum(raw[i][j]*bm[j] for j in full)%MOD==0 for i in interior)
    assert bm[w] == 350864591474990130360766
    assert paired == wave_equation(bm,w)%MOD == 268255689805940822204261
    certify_real_response(center[15],interior,external,b,observe)
    print("root first jet b_w modulo prime",bm[w], "wave equation at w",wave_equation(bm,w)%MOD)
    print("necessary extra top gradient per t: linf > 0.001554; l2 > 0.004882")
    print("certified intervals: 0.1037443 < b < 0.1037445; 3.280769 < wave < 3.280771")

if __name__ == "__main__":
    main()
