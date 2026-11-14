#!/usr/bin/env python3
"""Two independently placed finite inner SAM comparisons on the A30 word.

Only exact G/CX and canonical births are emitted. SourceI is used only in the
existing pre-compiler profile, which is transformed by the A29 compiler.
No expanded giant word, output measurement, new calibration, or free angle.
"""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json,sys
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;O=P.parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
sys.path.insert(0,str(D/'round32'))
import finite_book_comparison as a32
a=a32.core; nplus,nminus=a32.powers(); pplus,pminus=a32.align(nplus,nminus)
assert nplus+pplus==nminus+pminus
T=nplus+pplus
st=a.stages();cut=st.index({'kind':'RAW_RESOURCE_FRAME','intrinsic_inverse_depth':0})

def profile(which):
    """Old-profile split at two boundaries known to end with even SI parity."""
    if which=='forward_bank':
        for stage in st[:cut+1]:yield from a.stage_blocks(stage,0)
    elif which=='middle':
        for stage in st[cut+1:]:yield from a.stage_blocks(stage,0)
        lay=a.g.namespace()['layout']
        yield a.c.nb.z_word(lay['port'],lay['port'],tuple(lay['spin']))
        for stage in reversed(st[cut+1:]):yield from a.stage_blocks(stage,1)
    else:
        assert which=='reverse_bank'
        for stage in reversed(st[:cut+1]):yield from a.stage_blocks(stage,1)

def actual_section(which):
    """Finite compact G/CX stream; same compiler/namespace as actual A30."""
    yield from a.c.production_compiler().stream(profile(which))

def insertion(sign,j=2):
    """One actual SAM G power and paid exact all-column CX identity padding."""
    assert sign in ('plus','minus') and 0<=j<2688
    n,pad=(nplus,pplus) if sign=='plus' else (nminus,pminus)
    q=a.g.namespace()['layout']['SAM'][j]
    return a.c.nb.seq(a.c.nb.repeat(n,a.c.nb.gate('G',q)),a32.padding(pad))

def body_sections(slot,sign,j=2):
    """Logical-word compact sections; canonical births are separate stages."""
    assert slot in ('inner_forward','inner_backward')
    yield ('actual_A30_forward_bank',None)
    if slot=='inner_forward':yield ('paid_Q',insertion(sign,j))
    yield ('actual_A30_middle',None)
    if slot=='inner_backward':yield ('paid_Q',insertion(sign,j))
    yield ('actual_A30_reverse_bank',None)

def late_tail(n,K):
    """Physical addresses; last G of the last pair is actual closing gate."""
    assert K>0
    for i in range(K):
        yield {'kind':'canonical_RAW_birth','wire':n+i,'isometry':'psi -> psi tensor (sqrt(p),p)'}
        yield {'kind':'final_unitary_g' if i==K-1 else 'square_unitary_edge',
               'gate':{'op':'G','wires':[n+i]}}

def main():
    plan=json.loads((D/'round30/COMMON_SOURCE_MARKED_PLAN.json').read_text())
    n=plan['total_RAW_births']; L=int(plan['new_native_call_count']);K=66076
    assert n==10407050782
    base_gates=L+T;nbase=n+base_gates
    assert nbase<2**11647
    for sign in ('plus','minus'):
        q=insertion(sign)
        assert sum(a.c.nb.counts(q).values())==T
    tail=list(late_tail(n,K));assert len(tail)==2*K and tail[-1]['kind']=='final_unitary_g'
    assert tail[-1]['gate']=={'op':'G','wires':[n+K-1]}
    # Validate exact clock-dimension formula on small actual stage lists:
    # births n, base_gates, then K * (birth,G), last G is g.
    for n0 in range(1,5):
        for length in range(0,6):
            for k in range(1,6):
                dims=[2**j for j in range(n0)]+[2**n0]*length
                for j in range(k):dims += [2**(n0+j),2**(n0+j+1)]
                assert sum(dims)==2**n0*(length-2+3*2**k)-1
                assert len(dims)==n0+length+2*k
    # R11 heat estimate depends on D>=2^(n+K), common last g, and
    # B_prefix<=2*nbase*2^n. A32's more conservative c-derivative and
    # single-angle synthesis bounds apply (ours uses only one insertion).
    budget=a32.budget(nbase,K)
    assert budget['one_SAM_row_total']<F(1,2**73)
    repl=a.inventory()['replacement_error'];assert repl<F(1,2**3244)
    assert repl*2**3158<F(1,2**86)
    bound=budget['one_SAM_row_total']+repl*2**3158
    assert bound<F(1,2**74)
    # One pair for each independent inner coordinate: l2 <= sqrt(2) max,
    # replaced by a conservative rational 2 times max.
    assert 2*bound<F(1,2**71)
    # Independent local rotation axis on each of 2688 SAM wires and each
    # of two placements: sqrt(5376)<74. This is not the full algebra of
    # arbitrary multiwire SAM/old controls.
    assert 74**2>2*2688 and 74*bound<F(1,2**68)
    pins=[Path(__file__),P/'INNER_SUFFIX_CHECK.json',D/'round30/marked_source_schedule.py',D/'round30/COMMON_SOURCE_MARKED_PLAN.json',D/'round29/gcx_compiler.py',D/'round29/G_CX_ONLY_REALIZATION_RU.md',D/'round25/global_h1.py',D/'round32/finite_book_comparison.py',D/'round32/FINITE_BOOK_COMPARISON_PLAN.json',O/'round58/B58_A25_GCX_COVERAGE_AUDIT_RU.md',O/'round63/DETERMINANT_FD_BUDGET.json',O/'round63/SUFFICIENT_ENDPOINT_G_CERTIFICATE.json',O/'round64/B64_A32_FINITE_BOOK_AUDIT_RU.md']
    out={'status':'CONDITIONAL_PAID_INNER_GCX_PAIR_CONSTRUCTION','slots':['inner_forward_Qf_star','inner_backward_Qb'],'sam_index_example':2,'physical_sam_wire_example':4,'independent_slot_pairs':2,'T_power_plus_paid_padding_bit_length':T.bit_length(),'early_births':n,'late_birth_G_pairs':K,'final_g':'G on final fresh retention wire n+K-1','clock_dimension':'2^n * (L_base - 2 + 3*2^K) - 1','clock_layers':'n+L_base+2*K','L_base':'A30_core_L + T','L_base_below_2^11647_after_early_births':True,'same_clock_between_plus_and_minus_per_slot':True,'all_mode_A32_conservative_budget_lt':'2^-73 per row under R11','actual_replacement_derivative_error_over_gs_lt':'2^-86','exact_combined_rational_budget_lt':'2^-74 per slot','full_H_plus_J_inner_finite_source_row_under_Gamma_s_lt':'2^-72 per slot','two_inner_rows_l2_under_Gamma_s_lt':'2^-71','all_5376_local_SAM_axes_l2_under_Gamma_s_lt':'2^-68 from exact rational budget, not from 2^-72 row bound','arbitrary_multiwire_SAM_and_old_controls_covered':False,'same_task_membership_or_physical_selection_proved':False,'actual_A30_exact_reflection_claimed':False,'continuous_native_gate_claimed':False,'expanded_or_executed_giant_history':False,'physical_C_closed':False,'GR_closed':False,'source_sha256':{str(f):sha256(f.read_bytes()).hexdigest() for f in pins}}
    (P/'PAID_INNER_COMPARISON_PLAN.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'row_norm':out['full_H_plus_J_inner_finite_source_row_under_Gamma_s_lt'],'clock':out['clock_dimension']}))
if __name__=='__main__':main()
