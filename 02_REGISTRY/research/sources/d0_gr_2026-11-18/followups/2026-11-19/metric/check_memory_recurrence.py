"""Golden recurrence on a two-probe density, the literal clocks and the CQ entropies."""
from itertools import product
import json
from mpmath import iv

from check_paired_readers import (A, ONE, P, ZERO, LAMBDA, INV, birth, turn, cx, partial,
                                  final_law, add, clean, const)
from check_complement_price import receiver_timeline


def convolution(left, right):
    out=[ZERO]*(len(left)+len(right)-1)
    for i,x in enumerate(left):
        for j,y in enumerate(right):
            out[i+j]=out[i+j]+x*y
    return out


def source(t,m):
    psi={0:ONE}
    ntick=0
    for h in (0,1):
        psi=birth(psi,h)
        ntick+=1
        for _ in range(5-m):
            psi=turn(psi,h)
        if t: psi={x^(1<<h):z for x,z in psi.items()}
        for _ in range(m):
            psi=turn(psi,h)
        if t: psi={x^(1<<h):z for x,z in psi.items()}
        ntick+=7
    assert ntick==16
    # Optional retained coherent copies of both sources are INCLUDED in the full test.
    for h,shadow in ((0,2),(1,3)):
        psi=cx(turn(birth(psi,shadow),shadow,INV),h,shadow)
    return psi


def sesquilinear_sum(vectors,weights):
    out={}
    for state,w in zip(vectors,weights):
        for i,x in state.items():
            for j,y in state.items():
                add(out,(i,j),w*x*y)
    return clean(out)


def evaluate(z):
    p=(iv.sqrt(5)-1)/2
    a=iv.sqrt(p)
    return sum((c*a**i for i,c in enumerate(z.c)),iv.mpf(0))


def probability_row(b,same):
    y=b*LAMBDA
    joint=b*LAMBDA**2 if same else y**2
    return (ONE-y-y+joint,y-joint,y-joint,joint)


def entropy(row):
    return -sum((evaluate(x)*iv.ln(evaluate(x)) for x in row if x!=ZERO),iv.mpf(0))


def check():
    iv.dps=50
    co2=P**3
    co4=const(2)*co2**2-ONE
    co8=const(2)*co4**2-ONE
    c=convolution(convolution([-ONE,ONE],[ONE,-const(2)*co4,ONE]),[ONE,-const(2)*co8,ONE])
    assert sum(c,ZERO)==ZERO
    ell=iv.ln((1+iv.sqrt(5))/2)
    all_gains=[]
    all_b=[]
    for t in (0,1):
        sources=[source(t,m) for m in range(6)]
        assert not sesquilinear_sum(sources,c)
        bvals=[partial(s,[0]).get((0,0),ZERO) for s in sources]
        gains=[(entropy(probability_row(b,False))-entropy(probability_row(b,True)))/ell
               if b not in (ZERO,ONE) else iv.mpf(0) for b in bvals]
        all_gains.append(gains)
        all_b.append(bvals)
        for i,j in product(range(2),repeat=2):
            runs=[receiver_timeline(s,i,j) for s in sources]
            for m,b in enumerate(bvals):
                assert final_law(runs[m][-1][0])==probability_row(b,i==j)
            # Every raw matrix entry before/after actual births/CX/G, including the h/shadows.
            for age in range(17):
                assert not sesquilinear_sum([seq[age][0] for seq in runs],c)
    assert all(b==all_b[0][0] for b in all_b[0])
    gain=-sum((evaluate(k)*f for k,f in zip(c,all_gains[1])),iv.mpf(0))
    assert gain>iv.mpf('0.07196831') and gain<iv.mpf('0.07196833')
    total_abs=2*sum(abs(evaluate(k)) for k in c)
    assert total_abs>iv.mpf('8.2317') and total_abs<iv.mpf('8.2318')
    # A valuation reading the actual m=3 prefix and both final reports can distinguish fields.
    b0=all_b[0][3]; b1=all_b[1][3]
    assert b1==ONE
    accessible=c[3]*(b0*(ONE-b0)-b1*(ONE-b1))*LAMBDA**2
    witness=evaluate(accessible)
    assert witness<iv.mpf('-.01')
    return dict(exact_state_ring="Z[a], a^4+a^2=1",rank_source_wires=2,
                signed_recurrence_golden_coefficients=[list(v.c) for v in c],
                signs_in_experiment="minus c[m] times (00+11-01-10)/2",
                total_signed_l1=str(total_abs),schedules=24,
                each_seed_stage_count=8,source_count=2,full_work_wires_with_shadows=8,
                exact_full_state_at_stage_boundaries_per_ij_per_T=17,
                full_measured_rows_checked=48,field_gain_positive_interval=str(gain),
                rational_gain_certificate=["7196831/100000000","7196833/100000000"],
                parsed_gains_conditional_T1=[str(x) for x in all_gains[1]],
                signed_m3_sensitive_joint_charge_slope=str(witness),
                scope="affine common post-preparation instrument, even address-ij specific, with full retained new work and old right; prefix-setting m remains distinguishable unless economically excluded",
                full_CD13=False)


if __name__=='__main__':
    print(json.dumps(check(),indent=2,sort_keys=True))
