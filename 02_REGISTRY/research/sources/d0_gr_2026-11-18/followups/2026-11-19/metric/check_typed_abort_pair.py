"""One-attempt balanced-pair stopped instrument and native-clock obstruction."""
import json
import math
from pathlib import Path
import numpy as np
import sympy as sp

from check_source_price import load_control, need


def main():
    ne,digest=load_control()
    p=(math.sqrt(5)-1)/2; a=math.sqrt(p); r=p*p
    ps=ne.P;rs=ps**2;q=sp.symbols('q',real=True)
    # Exact true complete Born effect on the retained old T sector.  The
    # target stopped map is a direct sum of orthogonal output labels; this
    # calculation does NOT claim that its adaptive hardware is compiled.
    I=np.eye(2)
    K0=a*I
    K10=p*np.diag([a,p])
    K11=p*np.diag([p,a])
    total=sum(K.T@K for K in (K0,K10,K11))
    need(np.max(np.abs(total-I))<1e-14,'complete stopped instrument')
    for t in (0,1):
        probs=[float((K.T@K)[t,t]) for K in (K0,K10,K11)]
        expected=[p,r*(p if t==0 else r),r*(r if t==0 else p)]
        need(max(abs(x-y) for x,y in zip(probs,expected))<1e-14,
             'each native sector without selecting a branch')
    # Exact identities in the actual Golden algebraic field.
    field=ne.GOLDEN_FIELD
    zero=lambda x:field.from_sympy(sp.expand(x))==field.zero
    P0=ps;P10=rs*(ps-ps**3*q);P11=rs*(rs+ps**3*q)
    # Polynomial in q is reduced coefficient-wise in the actual field.
    need(all(zero(x) for x in sp.Poly(P0+P10+P11-1,q).all_coeffs()),'full mixture mass')
    need(zero(sp.diff(P11,q)-ps**5),'active joint event source')
    # Both active terminal words have length 5; abort word length 1.
    meanC=ps+5*rs
    # h(p²)/ln(phi) = p+2p²=1+p², directly from exact code lengths.
    meanInfo=(1+rs)*(1+rs)
    need(zero(meanC-meanInfo-ps),'exact full stopped code-CQ value')
    words=('0','10010','10100')
    need(all(not b.startswith(a) for a in words for b in words if a!=b),'complete labels prefix-free')

    # Compare two real already compiled common words, not a fabricated
    # stopped clock: append five literal CX;CX pairs on existing wires.
    receipt=json.loads(Path(__file__).with_name('native_balanced_pair_clock_result.json').read_text())
    D=receipt['clock_dimension'];width=receipt['final_work_dimension']
    need((D,width,receipt['stages'])==(415152,8192,99),'current full-carrier receipt')
    Dpad=D+10*width
    beta=2*r;x=beta/11
    old_return=receipt['minimum_return'];new_return=old_return+10
    halo=lambda L:2*x**L/(math.factorial(L)*(1-x/(L+1)))
    # β−1 log(Znew/Zold)=β−1 log(Dnew/Dold) plus a certified winding term.
    rel0=66*halo(old_return)/359;rel1=66*halo(new_return)/359
    trunc=(rel0/(1-rel0)+rel1/(1-rel1))/beta
    delta=math.log(Dpad/D)/beta
    universal=359*Dpad/(425*D)
    need(universal>1 and delta>0,'two native retained histories have different heat')
    # Five pairs multiply to identity on all full columns; rank-cut return F
    # and its J are exactly the same, independent of oldRIGHT.
    CX=np.array([[1.,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
    need(np.array_equal(np.linalg.matrix_power(CX,10),np.eye(4)),'paid padding all columns')

    # A HALT is not in the finite native gate grammar. This is an API/domain
    # fact, not a theorem excluding a separately implemented paid scheduler.
    bad=ne.Execution(1,(),(),(ne.Gate('HALT',(0,)),))
    try:
        ne.validate_execution(bad,max_qubits=1,max_expanded_stages=100)
        grammar_rejects=False
    except ne.DomainError:
        grammar_rejects=True
    need(grammar_rejects,'uncompiled HALT is not a native primitive')
    # Actual stage inventory is conditional on the externally admitted stop.
    stop_counts={'birth':3,'G':2,'CX':9,'SourceI':4}
    full_counts={'birth':9,'G':7,'CX':71,'SourceI':12}
    need(sum(stop_counts.values())==18 and sum(full_counts.values())==99,'physical branch schedules')
    expected_counts={k:stop_counts[k]+r*(full_counts[k]-stop_counts[k]) for k in stop_counts}
    print(json.dumps({
      'status':'PASS','native_source_sha256':digest,
      'terminal_words':list(words),'conditional_H1_word_length':5,
      'probabilities':'p; p^2*(p-p^3*q); p^2*(p^2+p^3*q)',
      'full_instrument_effects_sum_to_identity':True,
      'conditional_code_CQ_exact':'p','conditional_code_CQ_derivative_wrt_q':0,
      'probability_joint_H1_N1_derivative_wrt_q':round(p**5,12),
      'early_stop_H0_instruction_counts_if_dispatcher_admitted':stop_counts,
      'success_H1_instruction_counts_if_dispatcher_admitted':full_counts,
      'mean_instruction_counts_if_dispatcher_admitted':expected_counts,
      'physical_stop_dispatcher_compiled':False,'terminal_transmitter_compiled':False,
      'fixed_word_HALT_is_primitive':False,
      'existing_full_99stage_clock_dimension':D,'padded_native_clock_dimension':Dpad,
      'padded_pairs_in_native_word':5,'padded_word_full_clock_executed':False,
      'padded_feedback_unchanged':True,
      'heat_trace_universal_ratio_lower':universal,
      'heat_bootstrap_difference_center':delta,
      'heat_bootstrap_difference_truncation_bound':'{:.6e}'.format(trunc),
      'padded_witness_is_the_true_aborted_clock':False,
      'same_record_measures_do_not_determine_unpaid_clock':True,
      'Book_CostInfo_identified':False,'GR_closed':False,
    },sort_keys=True,indent=2))


if __name__=='__main__':main()
