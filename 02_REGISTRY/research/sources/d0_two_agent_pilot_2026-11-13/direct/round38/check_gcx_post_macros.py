#!/usr/bin/env python3
"""Exact finite algebra, negative controls, source pins and actual W census.

The production astronomical word is not expanded. Provider lowering is
checked structurally on seq/repeat/primitive cases and replay fixtures.
"""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from collections import Counter
from itertools import islice
import json
import sympy as S
import gcx_post_macros as m
import gcx_anchor_phase as anchor
P=Path(__file__).resolve().parent


def expanded(t,limit=10000):
    assert sum(m.counts(t).values())<=limit
    if t['op']=='seq':
        return sum((expanded(c,limit) for c in t['children']),[])
    if t['op']=='repeat': return expanded(t['child'],limit)*m.count_value(t['count'])
    return [t]


def main():
    macro=m.Macros(); k=macro.ks['pi8']
    for name,tree,cnt in [
        ('Z',macro.z(0,3),{'G':16*k,'CX':2}),
        ('H',macro.h(0,3),{'G':18*k,'CX':2}),
        ('X',macro.x(0,3),{'G':20*k,'CX':2}),
        ('CCZ',macro.ccz(0,1,2,3),{'G':64*k,'CX':24}),
        ('CCX',macro.ccx(0,1,2,3),{'G':100*k,'CX':28})]:
        assert m.counts(tree)==cnt,name
    for inv in (False,True):
        assert m.counts(macro.controlled_g(0,1,inv))=={
            'G':macro.ks['half_theta']+macro.ks['minus_half_theta'],'CX':2}
        assert m.counts(macro.controlled_pi3(0,1,inv))=={'G':12*macro.ks['pi6'],'CX':2}
    # Inspect the actual CCZ DAG: every parity is restored, and all 16
    # control/helper basis columns see (-1)^(abc), not only helper=0.
    ccz=macro.ccz(0,1,2,3)
    angles=[]
    for b in range(8):
        total=0
        for term in ccz['children']:
            children=term['children'];rot=[(i,x) for i,x in enumerate(children) if x['op']=='repeat']
            assert len(rot)==1
            i,r=rot[0];left=children[:i];right=children[i+1:]
            assert right==left[::-1] and r['child']==m.gate('G',3)
            assert all(x['op']=='CX' and x['wires'][1]==3 for x in left)
            parity=sum((b>>x['wires'][0])&1 for x in left)%2
            total+=(-1)**parity*(m.count_value(r['count'])//k)
        assert total%16==(8 if b==7 else 0)
        angles.append(total%16)
    H=S.Matrix([[1,1],[1,-1]])/S.sqrt(2); Z=S.diag(1,-1)
    Rquarter=S.Matrix([[1,-1],[1,1]])/S.sqrt(2)
    assert Rquarter*Z==H and H*Z*H==S.Matrix([[0,1],[1,0]])
    # Controlled rotation chronological order: R+ ; CX ; R- ; CX.
    angle=S.symbols('a',real=True)
    R=lambda a:S.Matrix([[S.cos(a),-S.sin(a)],[S.sin(a),S.cos(a)]])
    X=S.Matrix([[0,1],[1,0]])
    assert (R(-angle)*R(angle)).applyfunc(S.trigsimp)==S.eye(2)
    assert (X*R(-angle)*X*R(angle)-R(2*angle)).applyfunc(S.trigsimp)==S.zeros(2)
    # Reverse exact original DAG; repeated targets are lowered once and
    # repeated with their integer errors. No count-level order assumption.
    t=m.seq(m.gate('G',1),m.repeat(3,m.seq(m.gate('CX',1,2),m.gate('G',2))))
    before=expanded(t)
    out,e=macro.lower(t,inverse=True)
    assert e==4 and m.counts(out)=={'G':4*macro.ks['minus_theta'],'CX':3}
    assert out['children'][0]['op']=='repeat'
    assert out['children'][0]['child']['children'][0]==macro.angle(2,'minus_theta')
    ctl,ce=macro.lower(t,inverse=True,control=0,helper=3)
    assert ce==4*2+3*100
    assert m.counts(ctl)=={'G':4*(macro.ks['half_theta']+macro.ks['minus_half_theta'])+300*k,'CX':8+84}
    assert list(m.reverse_replay(lambda:iter(before)))==before[::-1]
    for bad in (m.gate('G',0),m.gate('CX',0,1)):
        try:macro.lower(bad,control=0,helper=3)
        except AssertionError:pass
        else:raise AssertionError('control aliases target')
    try:macro.ccx(0,1,2,2)
    except AssertionError:pass
    else:raise AssertionError('helper alias accepted')
    n=10407050782; cb=n
    assert [m.copied_wire(q,cb) for q in (0,1,2,2689,2690,n-1)]==[
        cb,cb+1,2,2689,cb+2,cb+n-2688-1]
    b=m.controlled_W_budget(macro); L=b['original_G']+b['original_CX']
    # Targeted integration on actual provider prefix. All other blocks use
    # the same proved DAG lowering; this is not a full production traversal.
    sample=list(islice(m.controlled_W_blocks(cb+n-2688,cb+n-2688+1,cb,macros=macro),3))
    assert len(sample)==3 and all(sum(m.counts(t).values())>0 for t in sample)
    assert L.bit_length()==11647
    assert b['error_units']<=100*L
    assert b['error_units']<1<<11654
    assert 39366*b['error_units']<1<<11670
    for N in range(3,8):
        for reflection in (False,True):
            for inverse in (False,True):
                actual=Counter()
                for tree in anchor.zero_phase_blocks(range(N),N,range(N+1,2*N-1),
                         2*N-1,2*N,reflection=reflection,inverse=inverse,macro=macro):
                    actual.update(m.counts(tree))
                expected=anchor.budget(N,macro,reflection)
                assert actual=={'G':expected['G'],'CX':expected['CX']}
                assert expected['error_units']==400*N-(504 if reflection else 508)
    # The large descriptor is O(number of ranges), not O(number of wires).
    huge=anchor.Ranges(range(2,2690),range(n,n+n-2688))
    assert len(huge)==n and huge[0]==2 and huge[-1]==n+n-2688-1
    assert anchor.budget(n,macro)['error_units']<1<<42
    # All-column approximation to actual A30 W, including dirty helper,
    # hence valid under arbitrary spectator entanglement.
    assert F(b['error_units'],1<<20000)<F(1,1<<8346)
    assert F(39366*b['error_units'],1<<20000)<F(1,1<<8330)
    # Seven direct certificates must pin the exact generator bytes.
    cert=json.loads((P/'POST_ANGLE_CERTIFICATE.json').read_text())
    assert cert['generator_sha256']==sha256((P/'certify_post_angles.py').read_bytes()).hexdigest()
    for v in cert['rotations'].values():
        assert int(v['operator_error_L1_numerator_hex'],16)*(1<<20000)<1<<v['denominator_pow2']
    s=m.a30_owner()
    pins=[P/'gcx_post_macros.py',P/'gcx_anchor_phase.py',anchor.B,
          P/'certify_post_angles.py',P/'POST_ANGLE_CERTIFICATE.json',
          Path(__file__),Path(s.__file__),Path(s.b.__file__),Path(s.c.__file__),
          s.c.old.B/'round57/GADGET_G_POWER_CERTIFICATE.json',
          P.parent/'round30/COMMON_SOURCE_MARKED_PLAN.json']
    result={'status':'PASS_GCX_POST_MACROS_AND_CONTROLLED_ACTUAL_W_CENSUS',
            'macro_all_column_proof_checks':True,'CCZ_all_eight_control_angles_mod16':angles,
            'helper_is_arbitrary_not_promised_zero':True,'exact_reversal_fixture':True,
            'source_primitive_repeat_error_not_new_word_length':True,
            'controlled_W_and_separately_compiled_adjoint_same_census':True,
            'controlled_W_error_strict_lt':'2^-8346',
            '39366_controlled_W_calls_error_strict_lt':'2^-8330',
            'controlled_W_census_hex':{k:hex(v) for k,v in b.items()},
            'controlled_W_call_length_bit_length':(b['G']+b['CX']).bit_length(),
            'controlled_W_finite_provider_defined':True,
            'actual_forward_provider_blocks_checked':3,
            'linear_anchor_counts_checked_N_3_through_7':True,
            'linear_anchor_requires_clean_scratch_and_flag':True,
            'production_stream_flattened_or_executed':False,
            'reverse_provider':'finite O(B^2) immutable replay; not benchmarked at production size',
            'complete_post_SAM_circuit_emitted':False,'full_new_clock_and_heat_computed':False,
            'physical_task_admission_proved':False,'physical_C_closed':False,'GR_closed':False,
            'source_sha256':{str(p):sha256(p.read_bytes()).hexdigest() for p in pins}}
    (P/'GCX_POST_MACROS_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','controlled_W_call_length_bit_length',
          'controlled_W_error_strict_lt','39366_controlled_W_calls_error_strict_lt')}))


if __name__=='__main__':main()
