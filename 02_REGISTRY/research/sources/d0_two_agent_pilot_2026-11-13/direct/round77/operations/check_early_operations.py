"""Two-site first jet of the original coefficient qubit on three early circuit cuts."""
import json
import sys
from fractions import Fraction as Q
from pathlib import Path

import numpy as np

sys.dont_write_bytecode = True
DIRECT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(DIRECT/"round75/work"))
import check_pointer_weyl as owner

O, I, spectral = owner.O, owner.I, owner.spectral


def trace(a):
    return O.reduce_sum(I(np.diag(a.lo), np.diag(a.hi)))


def gram(left, right):
    return spectral.matmul(spectral.transpose(owner.flatten(left)), owner.flatten(right))


def apply_mean(state, squares, backward):
    """(1/16) sum over the 16 original coefficient-00 word effects."""
    out = I(np.zeros_like(state.lo))
    for j, cr in enumerate(owner.car.ROLE_CREATION):
        ct = owner.car.transpose(cr)
        left = O.const_matrix_action(owner.car.mmul(cr, ct), state)
        right = O.const_matrix_action(owner.car.mmul(ct, cr), state)
        out = (out+O.broadcast_site(2*squares)*left
               +O.broadcast_site(squares+O.shifted(squares,backward[j]))*right)
    return out*Q(1,16)


def report(B, DB, p):
    prior = I(np.eye(128)/128.)
    q, dq = trace(B), trace(DB)
    logphi = -O.logarithm(p)
    dh = dq*O.logarithm((I(1)-q)/q)/logphi
    gain = I(0.)
    for g,dg in ((B,DB),(prior-B,-DB)):
        # The spectral checker only needs a bound for ||dg||_1 in its last
        # three arguments. Here 12 ||dg||_F >= sqrt(128) ||dg||_F.
        term,_,_ = spectral.posterior_certificate(g,dg,dg,I([[1.]]),I(6.))
        gain = gain+term/logphi
    distance = 2*(I(1)-2*q)*dq
    # For a pure complete incoming state and the complete two-tick comparator:
    # d(h) = 2 for q <= 1/4 and sqrt(q)+sqrt(3)*sqrt(1-q) otherwise.
    coherent = I(0.)
    for mass,jet in ((q,dq),(I(1.)-q,-dq)):
        if mass.hi < .25:
            coherent = coherent+2*jet
        else:
            O.require(mass.lo>.25 and mass.hi<1, "one coherent branch regime")
            root,comp = mass.sqrt(),(I(1.)-mass).sqrt()
            coherent = coherent+jet*(root+I(3.).sqrt()*comp
                                  +mass*(I(1.)/root-I(3.).sqrt()/comp)/2)
    return {k:O.bounds(v) for k,v in (
        ("probability",q),("rate",dq),("D_H_coeff",dh),("D_I_coeff_RIGHT",gain),
        ("D_S_coeff_RIGHT",dh-gain),("D_L_registered",distance),
        ("D_L_full_pure_two_tick",coherent))}


def main():
    p,state,w,dw,fw,bw,u,du,scales = owner.site_vector()
    s,ds = w.square(),2*w*dw
    prior = I(np.eye(128)/128.)
    # Extract the true early RIGHT blocks using both adjoint orderings,
    # including the backshift in P*P. The initial C does not move on this cut.
    b = gram(state,apply_mean(state,s,bw))
    db = gram(state,apply_mean(state,ds,bw))
    uniform = O.reduce_sum(s)*Q(9,4096)
    duniform = O.reduce_sum(ds)*Q(9,4096)
    O.require((trace(b)-uniform).contains(0) and (trace(db)-duniform).contains(0),
              "independent full Fourier and uniform-site scalar formulas")
    O.require((uniform-p*p*p*p*p*p*Q(9,16)).contains(0),"vacuum normalization")
    O.require(trace(db).hi<-.00007925531 and trace(db).lo>-.00007925534,
              "strict source despite DR=0")
    # After W and the entire Golden comparator, use ONLY the actual
    # coefficient-1 union. Equals 4 p^2 (AC)^* (I-M) (AC) by Walsh Parseval.
    z = u-apply_mean(u,s,bw)
    dz = du-apply_mean(du,s,bw)-apply_mean(u,ds,bw)
    end = 4*p*p*gram(u,z)
    dend = 4*p*p*(gram(du,z)+gram(u,dz))
    results = {
        "field_normalization_minus_DR":scales,
        "inside_Q_coeff0":report(b,db,p),
        "controlled_Q_idle_plus_active_coeff0":report(p*prior+p*p*b,p*p*db,p),
        "complete_comparator_coeff1":report(end,dend,p)}
    stages = (results["inside_Q_coeff0"], results["controlled_Q_idle_plus_active_coeff0"],
              results["complete_comparator_coeff1"])
    O.require(stages[0]["D_H_coeff"][1]<0<stages[1]["D_H_coeff"][0],
              "same final comparator permits opposite intermediate entropy derivatives")
    O.require(stages[0]["D_I_coeff_RIGHT"][0]>.00404661
              and stages[0]["D_S_coeff_RIGHT"][1]<-.00461165
              and stages[2]["D_S_coeff_RIGHT"][1]<-.00048223
              and stages[2]["D_L_registered"][1]<-.0000365,
              "separate early, terminal, and confirmed contributions")
    def entropy(x):
        return -(x*O.logarithm(x)+(I(1.)-x)*O.logarithm(I(1.)-x))/(-O.logarithm(p))
    # Each local positive CAR effect sums between these scalar bounds
    # before compression. 128 B is a positive compression on RIGHT.
    lower,upper = I(float(s.lo.min()))*Q(9,16), I(float(s.hi.max()))*Q(9,16)
    end_q = I(*stages[2]["probability"])
    end_ub = entropy(end_q)
    for name,stage,lo,hi in (
            ("shared_Q",stages[0],lower,upper),
            ("controlled_Q",stages[1],p+p*p*lower,p+p*p*upper)):
        initial_to_middle = min(entropy(lo).lo,entropy(hi).lo)
        O.require(initial_to_middle>end_ub.hi and initial_to_middle>0,
                  "strict increase and then decrease of conditional entropy")
        mid_source = I(*stage["D_S_coeff_RIGHT"])
        end_source = I(*stages[2]["D_S_coeff_RIGHT"])
        results[name+"_stage_variation"] = {
            "middle_conditional_entropy_lower":float(initial_to_middle),
            "final_conditional_entropy_upper":float(end_ub.hi),
            "D_inverse_Julia_layer":O.bounds(end_source-mid_source),
            "D_total_unsigned_change":O.bounds(2*mid_source-end_source)}
    print(json.dumps(results,indent=2,sort_keys=True))


if __name__ == "__main__":
    main()
