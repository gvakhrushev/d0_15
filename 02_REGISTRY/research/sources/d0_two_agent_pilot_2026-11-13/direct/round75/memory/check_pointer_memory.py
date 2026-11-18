"""One prepared DATA/RIGHT input, moving posterior, and a literal Golden control."""
import hashlib
import json
import math
from fractions import Fraction as F
from pathlib import Path

import sympy as sp


def check(condition, label):
    if not condition:
        raise AssertionError(label)


def gram_derivative(z, dz):
    return dz.T*z+z.T*dz


def rot(c, s):
    return sp.Matrix([[c,-s],[s,c]])


def test_moving_memory():
    q = sp.Rational
    two = sp.eye(2)
    skew = sp.Matrix([[0,-1],[1,0]])
    mix = rot(q(3,5),q(4,5))
    data_basis = sp.Matrix([[q(3,5),-q(4,5),0],[q(4,5),q(3,5),0],[0,0,1]])
    data_basis = sp.diag(1,mix)*data_basis
    data_axes = (data_basis[:,:2],data_basis[:,1:])
    singular = (sp.Matrix([1,2]),sp.Matrix([3,4]))
    ds = (sp.Matrix([2,0]),sp.Matrix([2,-2]))
    prior = sp.zeros(2)
    old_jet = sp.zeros(2)
    classical_entropy_jet = quantum_entropy_jet = weighted_entropy_jet = 0
    fixed_spectral_score = fixed_print_score = 0
    for y,(v,sv,dsv,u) in enumerate(zip((two,mix),singular,ds,data_axes)):
        z = u*sp.diag(*sv)*v.T/sp.sqrt(30)
        # Independent DATA rotation, RIGHT rotation and changing singular values.
        du = sp.Matrix([[0,-1,1],[1,0,0],[-1,0,0]])*u
        dz = (du*sp.diag(*sv)*v.T+u*sp.diag(*dsv)*v.T+
              (y+1)*u*sp.diag(*sv)*(v*skew).T)/sp.sqrt(30)
        old = z.T*z
        dold = gram_derivative(z,dz)
        prior += old
        old_jet += dold
        prob, dprob = old.trace(), dold.trace()
        check(dprob != 0, "leaf weight moves separately")
        eig = [s**2/30 for s in sv]
        posterior_score = sp.diag(*[-sp.log(l/prob) for l in eig])
        hp = sum(-s/prob*sp.log(s/prob) for s in eig)
        quantum_entropy_jet += (dold*v*posterior_score*v.T).trace()
        weighted_entropy_jet += dprob*hp
        data = z*z.T
        ddata = dz*z.T+z*dz.T
        fixed_spectral_score += (ddata*u*posterior_score*u.T).trace()
        values = list(data.diagonal())
        jets = list(ddata.diagonal())
        check(all(w>0 for w in values), "full computational rows have positive masses")
        fixed_print_score += sum(-j*sp.log(w/prob) for j,w in zip(jets,values))
        # Independent direct conditional-entropy derivative including Dq.
        posterior = [w/prob for w in values]
        posterior_jets = [j/prob-w*dprob/prob**2 for w,j in zip(values,jets)]
        classical_entropy_jet += -sum(dprob*w*sp.log(w)+prob*j*(sp.log(w)+1)
                                       for w,j in zip(posterior,posterior_jets))
    check(prior.trace()==1 and old_jet.trace()==0 and old_jet!=sp.zeros(2), "moving normalized prior")
    check(abs(float(weighted_entropy_jet)) > 1.e-4 and
          abs(float(quantum_entropy_jet-weighted_entropy_jet)) > 1.e-4,
          "both weight and conditional-state terms are nonzero")
    check(sp.simplify(fixed_spectral_score-quantum_entropy_jet)==0, "Schmidt source on accessible DATA")
    check(sp.simplify(fixed_print_score-classical_entropy_jet)==0, "actual conditional frozen rates")
    check(sp.simplify(fixed_print_score-(classical_entropy_jet-quantum_entropy_jet)
                      -quantum_entropy_jet)==0, "print minus the true new measurement entropy")
    return [float(x) for x in (weighted_entropy_jet,quantum_entropy_jet-weighted_entropy_jet)]


def test_one_copy_limit():
    old = sp.diag(sp.Rational(1,3),sp.Rational(1,6))
    log_prior = sp.Matrix([[0,1],[1,0]])
    direction = log_prior*old-old*log_prior
    # Right-unitary rotation never changes the available left density.
    z = sp.diag(sp.sqrt(old[0,0]),sp.sqrt(old[1,1]))
    dz = z*direction
    check(dz*z.T+z*dz.T==sp.zeros(2), "left terminal unchanged")
    check((log_prior*gram_derivative(z,dz)).trace()!=0, "right modular observable moves")
    a = sp.symbols("a",positive=True)
    p = a*a
    g = rot(a,p)
    ctrl = sp.eye(4)
    ctrl.row_swap(2,3)
    op_g = sp.diag(g,g)
    v = sp.Matrix([a,p])
    initial = sp.kronecker_product(v,v)
    states = (op_g*ctrl*ctrl*initial,ctrl*op_g*ctrl*initial)
    zero = lambda h: sp.rem(sp.expand(h),a**4+a**2-1,a)==0
    for which,flat in enumerate(states):
        branches = [flat[:2,0],flat[2:,0]]
        probs = [(item.T*item)[0] for item in branches]
        check(all(zero(t-u) for t,u in zip(probs,(p,p**2))), "same actual measured label law")
        prior = sum((item*item.T for item in branches),sp.zeros(2))
        det = (0,4*p**6)[which]
        check(zero(prior.det()-det), "two prepared prior spectra after sealing unknown RIGHT")
    check(zero(1-4*p**3-p**6), "literal discriminant of the mixed prior")


def primary_receipt():
    repo = Path(__file__).resolve().parents[7]
    rel = Path("02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source")
    blob = (repo/rel/"PRIMARY_RIGHT_POSTERIOR_GAIN_SOURCE_CERTIFICATE.json").read_bytes()
    check(hashlib.sha256(blob).hexdigest()=="3fc747be8d27a7b581cfa7a2e9b58da5ff87058a4e3b76199dd2e9483a674b6a",
          "original RIGHT128 numerical receipt")
    receipt = json.loads(blob)
    cases = receipt["spectral_certificates"]
    norm = receipt["complete_normalization"]
    check(len(cases)==33 and norm["active_fine_labels"]==64 and norm["exact_Walsh_dark_labels"]==64,
          "all 128 labels with positive active prior")
    coeff = list(map(lambda x:F(str(x)),receipt["linear_coefficients"]["RIGHT_posterior_gain_phi"]))
    check(F(21910472,10**16)<coeff[0]<=coeff[1]<F(21910478,10**16), "signed source for complete prior")
    return [-float(coeff[1]),-float(coeff[0])]


def check_paid_writer():
    # Actual complete Golden records. Sort a single common prefix catalogue,
    # then use a different initial segment for each already observed label.
    p = (math.sqrt(5)-1)/2
    ell = -math.log(p)
    n = 6
    prefix = [p**(n+bin(x).count("1")) for x in range(2**n)]
    check(abs(sum(prefix)-1)<3e-15 and max(prefix)<=p**n, "complete prefix law")
    for target in (0.12,0.37,0.57,0.95):
        k = 0
        while k < len(prefix) and sum(prefix[:k+1]) <= target:
            k += 1
        f = sum(prefix[:k])
        check(0<=target-f<=p**n+1e-15, "native prefix rate error")
        avg = entropy = 0.0
        for word,mass in enumerate(prefix):
            for b,ordinary in enumerate((p,p**2)):
                v = (p**2,p)[b] if word<k else ordinary
                joint = mass*v
                avg += joint*(n+bin(word).count("1")+1+b)
                entropy -= joint*math.log(joint)/ell
        check(abs(avg-entropy-p**3*f)<5e-14,
              "all printed selector and outcome lengths minus their own joint entropy")
    eta = 0.05
    for t in (eta,eta/math.e**2,eta/10**8):
        check(t*math.log(eta/t)**2<=4*eta/math.e**2+1e-14, "clipped log source estimate")


def check_variational_price():
    p = (math.sqrt(5)-1)/2
    ell = -math.log(p)
    length = (1.0,2.0)
    law = ((0.8,0.2),(0.375,0.625))
    q = (0.3,0.7)
    # Two feasible original purifications. These RIGHT entropies specify
    # pure conditional bipartite amplitudes with given DATA diagonals.
    T = 0.6
    conditional = -sum(qy*w*math.log(w)/ell for qy,row in zip(q,law) for w in row)
    n = 7
    prefix = [p**(n+bin(i).count("1")) for i in range(2**n)]
    for proposal in (law, ((0.5,0.5),(0.75,0.25))):
        printed = divergence = 0.0
        for qy,row,ready in zip(q,law,proposal):
            for px,ref,raw in zip(row,ready,length):
                target = (2-math.log(ref)/ell-raw)/p**3
                whole = math.floor(target)
                hit = 0.0
                for atom in prefix:
                    if hit >= target-whole:
                        break
                    hit += atom
                printed += qy*px*(raw+p**3*(whole+hit))
                divergence += qy*px*math.log(px/ref)/ell
        excess = printed-(conditional-T)-(2+T+divergence)
        check(-1e-14 <= excess <= p**(n+3)+1e-14, "upper cylinders give exact KL price envelope")


if __name__=="__main__":
    parts = test_moving_memory()
    test_one_copy_limit()
    check_paid_writer()
    check_variational_price()
    print(json.dumps({"moving_weight_and_state_terms_nats":parts,
                      "primary_added_angle_coefficient_phi":primary_receipt(),
                      "one_copy":True,"RIGHT_read":False,"GR_closed":False},sort_keys=True))
