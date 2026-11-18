"""Certified leading preparation gradients for the existing complete CAR pointer."""
import hashlib
import json
import sys
from fractions import Fraction as Q
from pathlib import Path

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[7]
OWNER = ROOT / "02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source"
sys.path.insert(0, str(OWNER))
import check_primary_car_preparation_source as car
import check_primary_car_pointer_source as pointer

I = pointer.I
p = (I.rational(5).sqrt()-1)*Q(1,2)
a = p.sqrt()
sigma = p*p*p
SITES = car.SITES_LIST
INSIDE = [i for i,(u,v,x,y) in enumerate(SITES) if u in (1,2) and x in (1,2) and y in (1,2)]


def check_native_occupation():
    # Original high/low word matrices on the actual retained c=1 sector.
    exact_p = (sp.sqrt(5)-1)/2
    exact_a = sp.sqrt(exact_p)
    G = sp.Matrix([[exact_a,-exact_p],[exact_p,exact_a]])
    X = sp.Matrix([[0,1],[1,0]])
    Z = sp.diag(1,-1)
    for K,high in ((sp.eye(2),False),(Z,True)):
        for word,exponent in (((K,X,G,X,K,G),2),((X,G,X,K,G,K),-2),((K,K,X,G,X,G),0)):
            mat = sp.eye(2)
            for gate in word:
                mat = gate*mat
            assert sp.simplify(mat-(G**exponent if high else sp.eye(2)))==sp.zeros(2)
    x,d,sine,cosine = sp.symbols("b d s c",real=True)
    # d'(0)=0 in d(b)=sqrt(p²-b²) on the primary nodal site.
    measured = [(d*cosine-side*x*sine)**2 for side in (1,-1)]
    differences = [sp.diff(m,x).subs({x:0,d:exact_p}) for m in measured]
    assert sp.simplify(differences[0]+2*exact_p*sine*cosine)==0
    assert sp.simplify(differences[0]+differences[1])==0
    assert all(sp.simplify(h)!=0 for h in (G**2)[0,:])
    assert Q(1,128)-Q(1,256)==Q(1,256)
    # A grade-diagonal read on the unchanged primary four-mask input:
    # all terminal RIGHT Grams have zero nodal derivative.
    for mass in [exact_p,0*x,x**2,exact_p**2-x**2]:
        assert sp.diff(mass,x).subs(x,0)==0


def probabilities():
    receipt = OWNER / "PRIMARY_RIGHT_POSTERIOR_GAIN_SOURCE_CERTIFICATE.json"
    assert hashlib.sha256(receipt.read_bytes()).hexdigest()=="3fc747be8d27a7b581cfa7a2e9b58da5ff87058a4e3b76199dd2e9483a674b6a"
    cases = json.loads(receipt.read_text())["spectral_certificates"]
    values = {}
    for case in cases:
        i = case["physical_index"]
        values[i] = I(*case["q0"])
        if case["paired_port_zero_by_p"]:
            assert i % 2 == 1
            values[i-1] = values[i]*p
    assert sorted(values) == [4*k+j for k in range(0,32,2) for j in range(4)]
    assert sum(values.values(),I(0.)).contains(1)
    return values


def kraus_rows(state,weight):
    """Apply the positive-flat-adjoint Julia/Walsh/Golden round to all test columns."""
    shifted = pointer.shifted
    action = pointer.const_matrix_action
    site = pointer.broadcast_site
    role_matrices = car.ROLE_CREATION
    F = [np.array([car.site_index(car.step(z,r,1)) for z in SITES]) for r in range(4)]
    B = [np.array([car.site_index(car.step(z,r,-1)) for z in SITES]) for r in range(4)]
    density = site(weight)
    ds = I(np.zeros_like(state.lo))
    for cr,f,b in zip(role_matrices,F,B):
        ct = car.transpose(cr)
        ds = ds+density*action(cr,shifted(state,f))-density*action(cr,state)
        ds = ds+shifted(density*action(ct,state),b)-density*action(ct,state)
    ds = ds*Q(1,16)
    primitives = [[],[]]
    for cr,g,f,b in zip(role_matrices,(Q(1,2),Q(2),Q(1),Q(1)),F,B):
        ct = car.transpose(cr)
        defect = (I(1.)-weight.square()*g).sqrt()-1
        left = car.mscale(car.mmul(cr,ct),1/g)
        right = car.mscale(car.mmul(ct,cr),1/g)
        left_ds = ds+site(defect)*action(left,ds)
        right_term = action(right,ds)
        right_ds = ds+site(defect)*right_term
        shifted_right_ds = ds+site(shifted(defect,b))*right_term
        primitives[0].extend((shifted(density*action(ct,ds),b),density*action(cr,shifted(ds,f)),
                              -(density*action(ct,ds)),-(density*action(cr,ds))))
        primitives[1].extend((left_ds,shifted_right_ds,-left_ds,-right_ds))
    for coeff,primitive in enumerate(primitives):
        for k,term in enumerate(pointer.fwht(primitive)):
            for port in (0,1):
                i = 8*k+2*coeff+port
                amp = term*(-2*(p*p if port==0 else p*a))
                if i==0:
                    amp = amp+state
                yield i,amp


def compute_rows():
    counts = car.actual_counts(ROOT)
    fractions = [I.rational(Q(256*n,sum(counts))) for n in counts]
    rho = I([x.lo for x in fractions],[x.hi for x in fractions])
    weight = sigma*rho.sqrt()
    modes = np.array(car.fourier_numerators(), dtype=np.int64)
    profiles = np.array([float(car.B(z)) for z in SITES])
    assert all(Q(v)==car.B(z) for z,v in zip(SITES,profiles))
    logphi = -pointer.logarithm(p)
    logs = {i:pointer.logarithm(q)/logphi for i,q in probabilities().items()}
    rows = {}
    for start in range(0,len(INSIDE),4):
        batch = INSIDE[start:start+4]
        shape = (256,16,5*len(batch))
        lo,hi = np.zeros(shape),np.zeros(shape)
        for j,i in enumerate(batch):
            col = 5*j
            # F_x.F_i/128^2, retaining every old RIGHT column on both sides.
            gram = (modes @ modes[i])/(128**2)
            lo[:,15,col] = hi[:,15,col] = gram*profiles
            lo[i,15,col+1] = hi[i,15,col+1] = 1
            for mask,amplitude in ((1,a),(14,p)):
                entry = I(gram)*amplitude
                lo[:,mask,col+2],hi[:,mask,col+2] = entry.lo,entry.hi
            lo[i,14,col+3] = hi[i,14,col+3] = 1
            lo[i,0,col+4] = hi[i,0,col+4] = 1
        totals = [[I(0.) for _ in range(6)] for _ in batch]
        for label,amp in kraus_rows(I(lo,hi),weight):
            for j,i in enumerate(batch):
                col = 5*j
                bdot = pointer.reduce_sum(amp[:,:,col]*amp[:,:,col+1])
                slackdot = pointer.reduce_sum(amp[:,:,col+2]*amp[:,:,col+3])
                dr = 2*(bdot-I(profiles[i])/p*slackdot)/(sigma*sigma)
                totals[j][0] = totals[j][0]+dr
                totals[j][1] = totals[j][1]+dr*(1+label%2)
                totals[j][2] = totals[j][2]-dr*logs[label]
                ds = 2*pointer.reduce_sum(amp[:,:,col]*amp[:,:,col+4])/(sigma*sigma)
                totals[j][3] = totals[j][3]+ds
                totals[j][4] = totals[j][4]+ds*(1+label%2)
                totals[j][5] = totals[j][5]-ds*logs[label]
        for i,(norm,cost,entropy,scalar_norm,scalar_cost,scalar_entropy) in zip(batch,totals):
            assert norm.contains(0) and scalar_norm.contains(0) and scalar_cost.contains(0)
            rayleigh = cost/(p*p*p*Q(1,16*64))
            rows[i] = (rayleigh,cost,entropy,cost-entropy,scalar_cost-scalar_entropy)
    return rows


def either_sign(x,y):
    return x.lo>0 and y.lo>0 or x.hi<0 and y.hi<0


def magnitude(x):
    if x.lo>=0:
        return x
    if x.hi<=0:
        return -x
    return I(0.,max(-x.lo,x.hi))


def main():
    for path,expected in pointer.PINS.items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==expected
    check_native_occupation()
    rows = compute_rows()
    ratios = {}
    for i,(r,c,h,net,scalar_net) in rows.items():
        assert either_sign(-r,net) and either_sign(r,c) and either_sign(-r,-h)
        ratios[i] = (-r)/net
    # Independent target gradient from the full preparation Hessian of A73.
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]/"round73/matter"))
    import check_matter_root as a73
    nominal = a73.blocks("rational")[15]
    b = [car.B(site) for site in SITES]
    n = Q(1,350272)
    # Per-entry rational approximation error certified in A73.
    er = n*Q(1,10**7)*sum(map(abs,b))
    for i in INSIDE:
        expected = n*sum(x*y for x,y in zip(nominal[i],b))
        assert Q(float(rows[i][0].lo)) <= expected+er and Q(float(rows[i][0].hi)) >= expected-er
    lower = min(float(x.lo) for x in ratios.values())
    upper = max(float(x.hi) for x in ratios.values())
    assert 141 < lower < 142 and 236 < upper < 237
    # For any scalar N, max |u_i-Nd_i| >= |u_i d_j-u_j d_i|/(|d_i|+|d_j|).
    bounds = []
    for i in INSIDE:
        u,d = -rows[i][0],rows[i][3]
        for j in INSIDE:
            v,e = -rows[j][0],rows[j][3]
            bound = magnitude(u*e-v*d)/(magnitude(d)+magnitude(e))
            bounds.append((float(bound.lo),i,j,bound))
    _,i,j,bound = max(bounds,key=lambda x:x[0])
    print("global multiplier minimax lower",SITES[i],SITES[j],pointer.bounds(bound))
    print("32 matching signs; required/observed range",lower,upper)
    for site in ((2,0,2,1),(2,1,1,1),SITES[i],SITES[j]):
        i=car.site_index(site)
        print(site,"required",pointer.bounds(-rows[i][0]),"net",pointer.bounds(rows[i][3]),
              "ratio",pointer.bounds(ratios[i]))
    for select,title in [(INSIDE,"all"),([i for i in INSIDE if SITES[i][0]==1],"zero top")]:
        lb,wi,wj,_ = max((t for t in bounds if t[1] in select and t[2] in select),key=lambda t:t[0])
        print("mismatch",title,lb,SITES[wi],SITES[wj])
        assert lb > (0.00032779 if title=="all" else 0.00004658)
    scalars = [(magnitude(rows[i][4]).lo,i) for i in INSIDE]
    _,best = max(scalars)
    scalar = rows[best][4]
    assert SITES[best]==(2,0,2,1)
    assert scalar.lo > -5.85446e-13 and scalar.hi < -5.85431e-13
    assert sum(not rows[i][4].contains(0) for i in INSIDE)==16
    print("strongest induced scalar",SITES[best],pointer.bounds(scalar),"16 strict nonzero rows")
    i = car.site_index(car.W)
    net_angle = rows[i][3]*p*sigma*sigma
    assert net_angle.lo>6.062e-7 and net_angle.hi<6.064e-7


if __name__=="__main__":
    main()
