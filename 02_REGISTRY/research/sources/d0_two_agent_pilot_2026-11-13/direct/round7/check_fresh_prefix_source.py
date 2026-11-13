#!/usr/bin/env python3
"""Exact source algebra and retained-CQ numerical diagnostics.

The isometries below test the abstract true-input interface, not a native H1
compiler. Native gates and paid AD2 are independently checked in B round12.
"""
import itertools
import json
import math

import numpy as np
import sympy as s

exact, numerical = [], []


def check(ok, label, target):
    if not bool(ok):
        raise AssertionError(label)
    target.append(label)


p = (s.sqrt(5)-1)/2
field = s.QQ.algebraic_field(s.sqrt(p))


def eq(x, y=0):
    return field.from_sympy(s.expand(x-y)) == field.zero


k = 1-2*p**6
offset = 4*p**3+4*p**6
check(eq(k, 8*s.sqrt(5)-17), 'actual high affine gain', exact)
check(s.simplify(k > s.Rational(1, 2)), 'two high blocks have a strict pure-cost margin', exact)
check(s.simplify(k < 1), 'one high block has the opposite zero-info sign', exact)
check(eq(offset-k*p, p), 'full high range lower endpoint', exact)
check(s.simplify(offset-k/2 > p), 'old collar lies inside the high-probability collar', exact)
check(eq(p/(1-p), 1/p), 'high logarithmic lower slope in Golden units', exact)
check(eq((1-p**2)/p**2, 1/p), 'old logarithmic upper slope in Golden units', exact)
check(s.simplify(p+p**3 < 1), 'actual noisy record support contracts', exact)

M, a, kap, hi, lo = s.symbols('M a kap hi lo', real=True)
ch, c0 = kap*(1+a*hi), 1-a*lo
den = M*ch-c0
check(s.expand(den-((M*kap-1)+a*(M*kap*hi+lo))) == 0,
      'signed gain retains the old terminal row', exact)
check(s.expand(den-(M*kap-1)*(1+a)-a*(M*kap*(hi-1)+lo+1)) == 0,
      'uniform gain margin identity', exact)
check(s.cancel((M*ch+c0)/den-(1+2*c0/den)) == 0,
      'positive terminal coefficient has bounded signed total variation', exact)
check(s.cancel((M*ch-c0)/den) == 1,
      'negative terminal coefficient gives total variation one', exact)
cancel = (1-kap)/(kap*hi+lo)
check(s.cancel(den.subs({M:1, a:cancel})) == 0,
      'one-prefix cancellation is exact', exact)
core, fixed = s.symbols('N_core N_fixed', integer=True, nonnegative=True)
nb = fixed+(M+1)*core+2*M+4*M
check(s.expand(nb-(fixed+(M+1)*core+6*M)) == 0,
      'both actual G and four-stage handoffs counted', exact)
check(s.expand(nb+2*nb-3*nb) == 0,
      'paid two-call padding uses actual new pre-padding count', exact)

# A genuine unequal off-diagonal common-lift fixture, no identification of
# the independent block maps. Coordinates x have dimension 5, geometry 2.
lift = s.Matrix([[1,0],[0,1],[0,0],[0,0],[0,0]])
maps = [s.Matrix([[1,0,1,2,-1],[0,1,0,1,3]]),
        s.Matrix([[1,0,-2,0,2],[0,1,1,-1,0]]),
        s.Matrix([[1,0,0,-3,1],[0,1,2,0,-2]])]
check(all(am*lift == s.eye(2) for am in maps), 'each distinct independent map has the real common lift', exact)
dh, do = s.symbols('c_high c_old', real=True)
am = (dh*(maps[1]+maps[2])-do*maps[0])/(2*dh-do)
check((am*lift-s.eye(2)).applyfunc(s.cancel) == s.zeros(2),
      'signed aggregate retains the exact right lift', exact)
e = s.Matrix(s.symbols('E0 E1', real=True))
source = -dh*(maps[1].T+maps[2].T)*e+do*maps[0].T*e
check((source+(2*dh-do)*am.T*e).applyfunc(s.cancel) == s.zeros(5,1),
      'full five-component covector identity, not just diagonal derivative', exact)

pf, kf, af = float(p), float(k), float(offset)
ell = math.log(1/pf)


def entropy(mat):
    vals = np.linalg.eigvalsh((mat+mat.conj().T)/2)
    if np.min(vals) < -2e-12:
        raise AssertionError('nonpositive conditional state')
    positive = vals[vals > 2e-14]
    return float(-np.sum(positive*np.log(positive)))


def h(q):
    return -q*math.log(q)-(1-q)*math.log(1-q)


def mm(x, y):
    # Explicit contraction avoids this host's complex BLAS matmul emitting
    # floating-point flags on finite small matrices. Do not suppress warnings.
    return np.einsum('ij,jk->ik', x, y, optimize=False)


def slopes(q):
    x = af-kf*q
    return math.log(x/(1-x))/ell, math.log((1-q)/q)/ell


# Each actual local map creates a fresh quantum output. The output order is
# (live Spin, new WORK, previous reference/WORK); only live Spin is touched
# by the next map. All old WORK remains, even though its entanglement changes.
rng = np.random.default_rng(140613)
isos = []
for j in range(3):
    pair = []
    for b in (0,1):
        raw = rng.normal(size=(4,4))+1j*rng.normal(size=(4,4))
        unitary, _ = np.linalg.qr(raw)
        iso = unitary[:, [0,2]]
        check(np.linalg.norm(iso.conj().T@iso-np.eye(2)) < 1e-14,
              f'complete local branch isometry {j},{b}', numerical)
        pair.append(iso)
    isos.append(pair)
bell = np.array([1.,0,0,1.])/math.sqrt(2)
bell_state = np.outer(bell, bell)
states = [bell_state, .63*bell_state+.37*np.eye(4)/4, np.eye(4)/4]
rawqs = np.array([.407,.452,.473])
qs = np.array([af-kf*rawqs[0], af-kf*rawqs[1], rawqs[2]])


def outputs(probabilities, state, event_effects=None):
    blocks, probs, effects = [], [], []
    for bits in itertools.product((0,1), repeat=3):
        current = np.eye(4, dtype=complex)
        for j,b in enumerate(bits):
            olddim = current.shape[0]//2
            if event_effects is None:
                weight = probabilities[j] if b else 1-probabilities[j]
                local = math.sqrt(weight)*isos[j][b]
            else:
                effect = event_effects[j] if b else np.eye(2)-event_effects[j]
                vals, vecs = np.linalg.eigh(effect)
                if np.min(vals) <= 0:
                    raise AssertionError('effect left the declared interior collar')
                root = mm(vecs*np.sqrt(vals), vecs.conj().T)
                local = mm(isos[j][b],root)
            current = mm(np.kron(local, np.eye(olddim)), current)
        block = mm(mm(current, state), current.conj().T)
        blocks.append(block)
        probs.append(float(np.trace(block).real))
        effects.append(mm(current.conj().T, current))
    return blocks, np.array(probs), effects


max_effect_error, max_entropy_error = 0., 0.
for si,state in enumerate(states):
    blocks, probs, effects = outputs(qs, state)
    for idx,bits in enumerate(itertools.product((0,1), repeat=3)):
        weight = math.prod(qs[j] if b else 1-qs[j] for j,b in enumerate(bits))
        error = np.linalg.norm(effects[idx]-weight*np.eye(4))
        max_effect_error = max(max_effect_error,error)
        check(error < 2e-14, f'all-input full-history scalar effect {si},{bits}', numerical)
        check(abs(probs[idx]-weight) < 2e-14, f'full joint law with retained output {si},{bits}', numerical)
    hc = float(-np.sum(probs*np.log(probs)))
    iq = sum(entropy(block) for block in blocks)-entropy(state)
    target = sum(h(float(q)) for q in qs)
    max_entropy_error = max(max_entropy_error,abs(iq-target))
    check(max(abs(hc-target),abs(iq-target)) < 5e-12,
          f'complete CQ and classical entropy with all outputs {si}', numerical)
    check(abs(sum(probs[1::2])-qs[2]) < 2e-14,
          f'unchanged final old effect despite arbitrary retained backaction {si}', numerical)


def complete_price(raw, state, bq, bc):
    current = np.array([af-kf*raw[0], af-kf*raw[1], raw[2]])
    blocks, probs, _ = outputs(current, state)
    cost = sum(pr*sum(1+b for b in bits)
               for pr,bits in zip(probs,itertools.product((0,1), repeat=3)))
    iq = sum(entropy(block) for block in blocks)-entropy(state)
    hc = float(-np.sum(probs*np.log(probs)))
    return cost-(bq*iq+bc*hc)/ell


derivative_max_error = 0.
step = 1e-5
for bq,bc in [(0.,0.),(.7,0.),(0.,.4),(.2,1.3)]:
    coeff = bq+bc
    for j in range(3):
        plus,minus = rawqs.copy(),rawqs.copy()
        plus[j] += step
        minus[j] -= step
        measured = (complete_price(plus,states[1],bq,bc)-complete_price(minus,states[1],bq,bc))/(2*step)
        lh,ll = slopes(rawqs[j])
        expected = -kf*(1+coeff*lh) if j<2 else 1-coeff*ll
        err = abs(measured-expected)
        derivative_max_error = max(derivative_max_error,err)
        check(err < 3e-8, f'independent slot full-CQ source {j},{bq},{bc}', numerical)

# Different backward actions have been deliberately retained; they do not
# form a common projector instrument. State/source equalities use scalar
# effects, not identical normalized branches or commuting backactions.
check(np.linalg.norm(isos[0][0]@isos[0][0].conj().T-isos[1][0]@isos[1][0].conj().T) > .2,
      'fresh-branch fixture does not reuse one common output projector', numerical)
check(abs(complete_price(rawqs,states[0],.3,.8)-complete_price(rawqs,states[2],.3,.8)) < 3e-12,
      'rank-changing initial-state comparison is exactly price neutral in the interface', numerical)

for count in (2,3,10,100):
    for q in (pf**2,.413,.49,.5):
        lh,ll = slopes(q)
        for coeff in (0.,.01,.5,2.,10000.):
            chf,c0f = kf*(1+coeff*lh),1-coeff*ll
            gain = count*chf-c0f
            variation = (count*chf+abs(c0f))/gain
            check(gain >= (count*kf-1)*(1+coeff)-1e-10,
                  f'positive margin M={count},q={q:.4f},a={coeff}', numerical)
            check(variation <= 1+2/(count*kf-1)+2e-12,
                  f'signed full-source norm M={count},q={q:.4f},a={coeff}', numerical)
qh = .43
lh,ll = slopes(qh)
one_cancel = (1-kf)/(kf*lh+ll)
check(one_cancel>0 and abs(kf*(1+one_cancel*lh)-(1-one_cancel*ll)) < 1e-14,
      'one-prefix numerical cancellation occurs at a positive coefficient', numerical)

# A registered extra alpha within b=0 is a real entropy contribution, even
# when its conditional law is constant. This is a negative control against
# treating separately registered labels as unobserved WORK.
def refined_h(q):
    vals = np.array([(1-q)*.5,(1-q)*.5,q])
    return float(-np.sum(vals*np.log(vals)))
qtest = .41
check(abs(refined_h(qtest)-(h(qtest)+(1-qtest)*math.log(2))) < 1e-14,
      'registered fine label contributes its actual conditional entropy', numerical)
fine_source = ((refined_h(qtest+step)-h(qtest+step))-(refined_h(qtest-step)-h(qtest-step)))/(2*step)
check(abs(fine_source+math.log(2)) < 1e-10,
      'constant unequal fine-branch entropies still have a nonzero source', numerical)

# The general error theorem also allows nonscalar, incompatible effects.
# This is an abstract robustness fixture, not a claim that a Spin-changing
# native primitive has been added to D0. All quantum output is still retained.
X = np.array([[0.,1.],[1.,0.]])
Z = np.diag([1.,-1.])
directions = [X,Z,(X+Z)/math.sqrt(2)]
deltas = np.array([kf*.006,kf*.005,.004])
near_effects = [q*np.eye(2)+delta*direction
                for q,delta,direction in zip(qs,deltas,directions)]
check(np.linalg.norm(mm(near_effects[0],near_effects[1])-mm(near_effects[1],near_effects[0])) > 1e-5,
      'robustness fixture effects genuinely do not commute', numerical)
log_bounds = np.array([max(abs(math.log((1-t)/t)) for t in (q-d,q+d))
                       for q,d in zip(qs,deltas)])
entropy_bound = float(log_bounds@deltas)
ideal_entropy = sum(h(float(q)) for q in qs)
ideal_cost = float(np.sum(1+qs))
largest_joint_defect = 0.
max_near_entropy_error = 0.
for si,state in enumerate(states):
    blocks, probs, effects = outputs(qs,state,near_effects)
    check(np.linalg.norm(sum(effects)-np.eye(4)) < 2e-13,
          f'full incompatible-effect history remains complete {si}', numerical)
    iq = sum(entropy(block) for block in blocks)-entropy(state)
    hc = float(-np.sum(probs*np.log(probs)))
    cost = sum(pr*sum(1+b for b in bits)
               for pr,bits in zip(probs,itertools.product((0,1), repeat=3)))
    max_near_entropy_error = max(max_near_entropy_error,abs(iq-ideal_entropy),abs(hc-ideal_entropy))
    check(max(abs(iq-ideal_entropy),abs(hc-ideal_entropy)) <= entropy_bound+1e-12,
          f'nodewise complete CQ and classical error bound {si}', numerical)
    check(abs(cost-ideal_cost) <= float(np.sum(deltas))+1e-13,
          f'nodewise full parser-cost error bound {si}', numerical)
    ideal_probs = np.array([math.prod(qs[j] if b else 1-qs[j] for j,b in enumerate(bits))
                           for bits in itertools.product((0,1),repeat=3)])
    largest_joint_defect = max(largest_joint_defect,float(np.max(abs(probs-ideal_probs))))
    for bq,bc in [(0.,0.),(.3,0.),(0.,.7),(.4,1.2)]:
        actual_price = cost-(bq*iq+bc*hc)/ell
        ideal_price = ideal_cost-(bq+bc)*ideal_entropy/ell
        bound = float(np.sum(deltas))+(bq+bc)*entropy_bound/ell
        check(abs(actual_price-ideal_price) <= bound+2e-12,
              f'noncommuting full price bound {si},{bq},{bc}', numerical)
check(largest_joint_defect > 1e-5,
      'near-scalar law is actually correlated and was not replaced by a product', numerical)

print(json.dumps({
    'status':'PASS_SCOPED_FRESH_PREFIX_SOURCE',
    'exact_count':len(exact),'exact_checks':exact,
    'numeric_count':len(numerical),'numeric_checks':numerical,
    'diagnostics':{
        'M2_zero_info_margin':2*kf-1,
        'one_high_cancelling_a_at_q_043':one_cancel,
        'max_full_effect_error':max_effect_error,
        'max_full_CQ_entropy_error':max_entropy_error,
        'max_independent_source_error':derivative_max_error,
        'retained_quantum_output_dimension':32,
        'joint_record_count':8,
        'extra_registered_label_source':fine_source,
        'noncommuting_near_scalar_joint_defect':largest_joint_defect,
        'noncommuting_near_scalar_entropy_error':max_near_entropy_error,
        'noncommuting_near_scalar_entropy_bound':entropy_bound},
    'scope':'Exact signed source algebra and numerical full retained-CQ checks for the stated scalar interface; no native H1 compiler or physical price binding.',
    'full_H1_admission_proved':False,
    'physical_C_closed':False,'GR_closed':False
},indent=2))
