"""Native two-reader balance with an independently varied registered controller.

The 13-qubit check retains all controls and NC1 tails; it computes the full
positive registered law and checks the scalar Shannon-ledger formula.  It is
not an identification with the full microscopic Book03 action.
"""
import json
import math
from pathlib import Path
import numpy as np

p = (math.sqrt(5)-1)/2
r = p*p
s = p**3
ell = math.log(1/p)
a = math.sqrt(p)
SIZE = 1 << 13
ids = np.arange(SIZE, dtype=np.int64)
N,D1,D2,E1,E2,R1,R2,TN,TD1,TD2,TR1,TR2,NB = range(13)
tails = {N:TN,D1:TD1,D2:TD2,R1:TR1,R2:TR2}


def oneq(state, k, mat):
    i = ids[(ids & (1 << k)) == 0]
    j = i | (1 << k)
    result = state.copy()
    result[i] = mat[0,0]*state[i] + mat[0,1]*state[j]
    result[j] = mat[1,0]*state[i] + mat[1,1]*state[j]
    return result


def cx(state, control, target):
    i = ids[((ids & (1 << control)) != 0) & ((ids & (1 << target)) == 0)]
    j = i | (1 << target)
    result = state.copy()
    result[i],result[j] = state[j],state[i]
    return result


def birth(state,k,x):
    t,z = math.sqrt(1-x),math.sqrt(x)
    return oneq(state,k,np.array([[t,-z],[z,t]]))


def nc1(state,k):
    t = tails[k]
    state = cx(state,k,t)
    state = oneq(state,t,np.array([[a,-p],[p,a]]))
    state = cx(state,k,t)
    bit = (ids & (1 << k)) != 0
    tail = (ids & (1 << t)) != 0
    return tuple(state * mask for mask in (~bit, bit & ~tail, bit & tail))


def prob(state):
    return float(np.vdot(state,state).real)


def build(u,Q,shared=False):
    state=np.zeros(SIZE); state[0]=1
    for k,x in ((N,u),(D1,r),(D2,r),(E1,Q),(E2,0 if shared else Q),
                (R1,r),(R2,r),(TN,r),(TD1,r),(TD2,r),(TR1,r),(TR2,r)):
        state=birth(state,k,x)
    # NB=1-N, using a prepared, registered known-one H on the accepted branch.
    state=cx(state,N,NB)
    state=oneq(state,NB,np.array([[0.,1.],[1.,0.]]))
    initial_norm=prob(state)
    table={}; invalid=0.
    for n,ns in enumerate(nc1(state,N)[:2]):
      invalid+=prob(nc1(state,N)[2]) if n==0 else 0.
      for d1,ds1 in enumerate(nc1(ns,D1)[:2]):
       invalid+=prob(nc1(ns,D1)[2]) if d1==0 else 0.
       for d2,ds2 in enumerate(nc1(ds1,D2)[:2]):
        invalid+=prob(nc1(ds1,D2)[2]) if d2==0 else 0.
        x1=cx(ds2,E1 if d1==0 else N,R1)
        out1=nc1(x1,R1)
        invalid+=prob(out1[2])
        for b1,b1s in enumerate(out1[:2]):
         x2=cx(b1s,(E1 if shared else E2) if d2==0 else NB,R2)
         out2=nc1(x2,R2)
         invalid+=prob(out2[2])
         for b2,b2s in enumerate(out2[:2]):
          table[n,d1,d2,b1,b2]=prob(b2s)
    assert abs(initial_norm-1)<1e-12 and invalid<1e-25
    assert abs(sum(table.values())-1)<2e-12
    return table,invalid


def h(x):
    return -x*math.log(x)-(1-x)*math.log(1-x)


def f(x):
    return 1+x-h(x)/ell


def fp(x):
    return 1-math.log((1-x)/x)/ell


def ledger(u,Q):
    q=r+s*Q
    return f(u)+2*f(r)+2*p*f(q)+r*(f(r)+f(p))


def analytic_table(u,Q):
    table={}
    for n in (0,1):
     for d1 in (0,1):
      for d2 in (0,1):
       q1=r+s*(Q if d1==0 else n)
       q2=r+s*(Q if d2==0 else 1-n)
       for b1 in (0,1):
        for b2 in (0,1):
         table[n,d1,d2,b1,b2]=(
           (u if n else 1-u)*(r if d1 else p)*(r if d2 else p)
           *(q1 if b1 else 1-q1)*(q2 if b2 else 1-q2))
    return table


def observed_ledger(table):
    return sum(v*(5+sum(k)) for k,v in table.items()) + sum(v*math.log(v) for v in table.values() if v)/ell


def main():
    receipt=json.loads(Path(__file__).with_name('paid_predictor_result.json').read_text())
    qlo,qhi=map(float,receipt['q_star']); qstar=(qlo+qhi)/2
    Q=(qstar-r)/s
    # The physically registered one-attempt H preparation uses the same
    # actual NC1; its 0 and 10 branches are both kept.
    flag=np.zeros(SIZE); flag[0]=1
    flag=birth(birth(flag,N,r),TN,r)
    f0,f1,fx=nc1(flag,N)
    assert abs(prob(f0)-p)<1e-14 and abs(prob(f1)-r)<1e-14
    assert prob(fx)<1e-25
    max_err=0.; max_price_err=0.; max_invalid=0.
    for u in (0.2,r,0.67):
     for bank in (0.07,Q,0.39):
      table,invalid=build(u,bank); expected=analytic_table(u,bank)
      max_err=max(max_err,max(abs(table[k]-expected[k]) for k in table))
      max_price_err=max(max_price_err,abs(observed_ledger(table)-ledger(u,bank)))
      max_invalid=max(max_invalid,invalid)
    assert max_err<1e-12 and max_price_err<1e-12 and max_invalid<1e-25
    assert abs(fp(r))<1e-14
    curv=1/(ell*r*(1-r))
    slope=2*p*s*fp(qstar)
    assert 0.25 < fp(qstar) < 1/3 and slope>0
    eps=1e-6
    numeric_dQ=(ledger(r,Q+eps)-ledger(r,Q-eps))/(2*eps)
    numeric_du=(ledger(r+eps,Q)-ledger(r-eps,Q))/(2*eps)
    assert abs(numeric_dQ-slope)<1e-8 and abs(numeric_du)<1e-8
    # One independent canonical NC1 H=1 succeeds with probability r;
    # its encoded cost minus entropy is exactly f(r)=0.
    assert abs(f(r))<1e-14
    # The actual retained-EIGHT use: E1 is the very same previously
    # registered T in both readings, not two independent SITE preparations.
    for u in (0.2,r,0.67):
     for t in (0,1):
      table,invalid=build(u,t,shared=True)
      expected=analytic_table(u,t)
      assert max(abs(table[k]-expected[k]) for k in table)<1e-12
      assert invalid<1e-25
      assert abs(observed_ledger(table) - (f(u)+r*s+2*p*s*t))<1e-12
    # Independent controls on the two retained T sectors are distinct Euler
    # coordinates; conditioning prevents any mixture entropy from being lost.
    for pi in (0.1,0.42,0.9):
     for u0,u1 in ((0.2,0.67),(r,r)):
      a0=observed_ledger(build(u0,0,shared=True)[0])
      a1=observed_ledger(build(u1,1,shared=True)[0])
      full=r*((1-pi)*a0+pi*a1) # H's own net code cost is f(r)=0
      formula=r*((1-pi)*f(u0)+pi*f(u1)+r*s+2*p*s*pi)
      assert abs(full-formula)<2e-12
    unconditional_pi_slope=r*2*p*s
    assert abs(unconditional_pi_slope-2*p**6)<1e-14
    answer={
      'schema':'d0.balanced-registered-controller-source/1',
      'status':'PASS','positive_registered_leaves':32,
      'max_quantum_law_error':max_err,'max_ledger_error':max_price_err,
      'max_invalid_nc1_probability':max_invalid,
      'q_native_centre':qstar,'Q_native_centre':Q,
      'stationary_controller_u':r,'controller_second_derivative':curv,
      'native_f_prime':fp(qstar),'gain_wrt_Q_on_H_success':slope,
      'gain_wrt_Q_with_paid_one_attempt':r*slope,
      'gain_ratio_to_one_native_reader_with_paid_one_attempt':2*p*r,
      'eight_retained_same_T_pi_slope_on_H_success':2*p*s,
      'eight_retained_same_T_pi_slope_with_paid_one_attempt':unconditional_pi_slope,
      'eight_retained_constant_after_controller_stationarity':p**7,
      'eight_retained_same_T_ratio_to_one_repeat':2*p*r,
      'independent_T_conditioned_controllers_tested':2,
      'old_eight_catalogue_or_writer_price_accounted':False,
      'complete_book_cost_info_identified':False,
      'all_independent_controller_rows_closed':False,
      'GR_closed':False}
    print(json.dumps(answer,indent=2,ensure_ascii=False))


if __name__=='__main__':
    main()
