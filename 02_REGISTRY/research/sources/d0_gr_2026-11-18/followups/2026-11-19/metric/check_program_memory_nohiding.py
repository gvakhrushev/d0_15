"""Audit a retained schedule register against the 24-word state recurrence."""
import json
from itertools import product
from mpmath import iv
from check_paired_readers import ONE, ZERO, P, A, LAMBDA, const, birth, turn, cx, final_law
from check_complement_price import receiver_timeline
from check_memory_recurrence import source, convolution, evaluate, probability_row, entropy


def fprob(psi, bit):
    return sum((z*z for index, z in psi.items() if index & (1 << bit)), ZERO)


def check():
    iv.dps = 50
    co2 = P**3
    co4 = const(2)*co2**2-ONE
    co8 = const(2)*co4**2-ONE
    c = convolution(convolution([-ONE, ONE], [ONE, -const(2)*co4, ONE]), [ONE, -const(2)*co8, ONE])
    sources = {(t,m): source(t,m) for t,m in product((0,1),range(6))}
    assert all(sources[0,m] == sources[0,0] for m in range(6))
    assert all(sum((z*z for z in state.values()),ZERO)==ONE for state in sources.values())
    # Compare the literal post-birth native unitary on the whole h carrier.
    # Equality of T=0 blocks fixes any allowed common scalar to +1; on T=1
    # also check that no two h-only unitary blocks agree up to sign.
    def word(m,t,basis):
        state={basis:ONE}
        for _ in range(5-m): state=turn(state,0)
        if t: state={x^1:z for x,z in state.items()}
        for _ in range(m): state=turn(state,0)
        if t: state={x^1:z for x,z in state.items()}
        return state
    def col(m,t,basis):
        state=word(m,t,basis)
        return tuple(state.get(i,ZERO) for i in (0,1))
    blocks={(t,m): tuple(col(m,t,basis) for basis in (0,1))
            for t,m in product((0,1),range(6))}
    assert all(blocks[0,m] == blocks[0,0] for m in range(6))
    for m in range(6):
        for n in range(m):
            assert blocks[1,m] != blocks[1,n]
            assert blocks[1,m] != tuple(tuple(-x for x in column)
                                         for column in blocks[1,n])
    # In a block-diagonal six-dimensional physical program register, no signed
    # cancellation can occur even though the reduced source sum vanishes.
    assert sum(c,ZERO)==ZERO
    assert all(cm != ZERO for cm in c)
    label_trace_norm=sum(abs(evaluate(cm)) for cm in c)
    assert iv.mpf('4.1158') < label_trace_norm < iv.mpf('4.1159')
    # The first elementary step after h_0 birth differs between the real words:
    # m=0 turns G, m=5 applies CX(T,h_0); T=0 makes CX the identity.
    seed=birth({0:ONE},0)
    early_m0=turn(seed,0)
    early_m5=seed
    assert fprob(early_m0,0)==LAMBDA
    assert fprob(early_m5,0)==P**2
    early_difference=evaluate(LAMBDA-P**2)
    assert iv.mpf('.562') < early_difference < iv.mpf('.563')
    # Actual last LC1 rows, four schedules, selected program m=3.
    def both_one(t,i,j):
        state=receiver_timeline(sources[t,3],i,j)[-1][0]
        return final_law(state)[3]
    contrast=[]
    for t in (0,1):
        law={(i,j):both_one(t,i,j) for i,j in product((0,1),repeat=2)}
        assert law[0,0] == law[1,1] and law[0,1] == law[1,0]
        value=law[0,0]-law[0,1]
        contrast.append(value)
    slope=c[3]*(contrast[0]-contrast[1])
    assert contrast[0]!=ZERO and contrast[1]==ZERO
    slope_iv=evaluate(slope)
    assert iv.mpf('-.147933') < slope_iv < iv.mpf('-.147932')
    # An independently-born, actually registered Bernoulli(p) flag multiplies
    # the deterministic contingent-code contribution. Entropy of the independent
    # flag cancels in the four-word contrast, but implementation charges remain.
    ell=iv.ln((1+iv.sqrt(5))/2)
    bs=[fprob(sources[1,m],0) for m in range(6)]
    # Here fprob is Pr(h=1), whereas probability_row needs Pr(h=0).
    bs=[ONE-b for b in bs]
    gains=[(entropy(probability_row(b,False))-entropy(probability_row(b,True)))/ell
           if b not in (ZERO,ONE) else iv.mpf(0) for b in bs]
    gamma=-sum((evaluate(cm)*g for cm,g in zip(c,gains)),iv.mpf(0))
    assert iv.mpf('.07196831') < gamma < iv.mpf('.07196833')
    net_rare=gamma+evaluate(P**2)*slope_iv
    net_common=gamma+evaluate(P)*slope_iv
    assert net_rare > 0 and net_common < 0
    return dict(
      current_regime='24 words on original common T; no assumption that m is physically encoded in source work',
      T0_six_exact_terminal_source_states_identical=True,
      exact_distinct_T1_unitaries_up_to_global_sign=6,
      exact_pairwise_distinct_native_unitary_checks=15,
      programme_register_dimension=6,
      minimum_qubit_count=3,
      unobserved_program_label_gram_rank=6,
      full_labelled_signed_state_trace_norm=str(label_trace_norm),
      early_detector_probability_difference_T0=str(early_difference),
      selected_m3_joint_readout_source=str(slope_iv),
      gamma=str(gamma),
      golden_flag_p2_net_source=str(net_rare),
      golden_flag_p_net_source=str(net_common),
      limitations='orthogonal physical label is an explicit implementation; a fixed conditioned reader is an extra permitted operation, not a derived Book03 tariff; early diagnostic perturbs the run; physical work and full clock responses require own accounting',
      full_CD13=False)


if __name__=='__main__':
    print(json.dumps(check(),sort_keys=True,indent=2))
