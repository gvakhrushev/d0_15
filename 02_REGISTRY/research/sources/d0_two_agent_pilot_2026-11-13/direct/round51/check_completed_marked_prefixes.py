#!/usr/bin/env python3
"""Check exact paid-prefix placement and full unconditioned-effect algebra."""
from pathlib import Path
from hashlib import sha256
import json, sys
import sympy as S
import completed_marked_prefixes as p

sys.dont_write_bytecode = True
P = Path(__file__).resolve().parent
nb = p.paid.native


def placement():
    sam = (0, 1, 2)
    before = [nb.gate('G', 3), nb.gate('CX', 0, 3)]
    middle = [[nb.gate('G', 4)] if i % 2 else
              [nb.gate('CX', 3, 4), nb.gate('G', 3)]
              for i in range(len(p.processor_stages()))]
    returned = [nb.gate('CX', 1, 4), nb.gate('G', 4)]

    def core():
        yield from before
        yield {'op': 'B82_CUT', 'name': p.paid.CUTS[0]}
        for block in middle:
            yield from block
        yield {'op': 'B82_CUT', 'name': p.paid.CUTS[1]}
        yield from returned

    def control(axis, sign):
        if sign:
            yield nb.repeat(1 if sign > 0 else 2, nb.gate('G', sam[axis]))

    def processor(name):
        for block in middle[:p.descriptor(name)['processor_stage_count']]:
            yield from block

    cfg = {'sam': sam, 'controlL': 6,
           'coreL': len(before)+sum(map(len, middle))+len(returned)+4,
           'postL': 4, 'probeL': 4}

    def leaves(stream):
        return [gate for tree in stream for gate in p.paid.target.e.leaves(tree)]

    replays = []
    names = ['SOURCE_before_Qf']+[x['name'] for x in p.registry()]
    for sign in (-1, 0, 1):
        full = leaves(p.paid.family_blocks(cfg, core, lambda:iter(()), control,
                      lambda plane,sgn:iter(()), arm='matched' if sign else 'centre',
                      sign=sign, axis=0))
        for name in names:
            actual = leaves(p.assembled_prefix(lambda:iter(before), processor,
                            control, cfg, axis=0, sign=sign, name=name))
            size = cfg['controlL']+len(before)
            if name != 'SOURCE_before_Qf':
                size += cfg['controlL']+sum(map(len,middle[:p.descriptor(name)['processor_stage_count']]))
            assert len(actual) == size and actual == full[:size]
            replays.append({'sign': sign, 'mark': name, 'actual_native_prefix_calls': size})
    assert len(replays) == 39
    try:
        p.descriptor('inside_unfinished_REPORT')
        raise RuntimeError('unregistered internal mark accepted')
    except AssertionError:
        pass
    return replays


def algebra():
    # Joint CODE/WORK effects, including off-diagonal correlations, on
    # rectangular maps retaining two independent input columns.
    plus = S.Matrix(4,2,S.symbols('a0:8',real=True))
    minus = S.Matrix(4,2,S.symbols('b0:8',real=True))
    obs = S.Matrix(4,4,S.symbols('o0:16',real=True))
    d = S.symbols('d',nonzero=True,real=True)
    mid = (plus+minus)/2
    jet = (plus-minus)/(2*d)
    left = (plus.T*obs*plus-minus.T*obs*minus)/(2*d)
    right = mid.T*obs*jet+jet.T*obs*mid
    assert (left-right).applyfunc(S.expand) == S.zeros(2)
    # A fixed completed processor multiplies the FULL vector jet. Its
    # error is against the target derivative, not divided by d.
    idealD=S.Matrix([[0,1,0,0],[1,0,0,0],[0,0,0,1],[0,0,1,0]])
    errD=S.Matrix(4,4,S.symbols('e0:16',real=True))
    target=S.Matrix(4,2,S.symbols('j0:8',real=True))
    assert ((idealD+errD)*jet-idealD*target
            -(idealD+errD)*(jet-target)-errD*target).applyfunc(S.expand)==S.zeros(4,2)
    # Exact support and pre-/post-Q distinction; an unchanged bank is
    # enough to refute moving the geometric jet to the earlier prefix.
    R=S.Rational; t=R(1,10)
    rot=S.Matrix([[1-t*t,-2*t],[2*t,1-t*t]])/(1+t*t)
    code=S.kronecker_product(rot,S.eye(2))
    Dwork=S.kronecker_product(S.eye(2),S.diag(1,-1))
    assert code*Dwork == Dwork*code
    B=S.diag(S.eye(2),S.Matrix([[R(3,5),-R(4,5)],[R(4,5),R(3,5)]]))
    assert Dwork*code.T*B*code==code.T*Dwork*B*code
    born=S.Matrix([R(3,5),0,R(4,5),0])
    before_plus=code*born;before_minus=code.T*born
    after_plus=code.T*code*born;after_minus=code*code.T*born
    assert after_plus==after_minus and before_plus!=before_minus
    return {'joint_effect_polarization_all_input_columns':True,
            'fixed_processor_full_jet_transport_identity':True,
            'error_D_times_genuine_derivative_not_inverse_step':True,
            'pre_Qf_mark_cannot_inherit_post_Qf_geometric_jet':True}


def main():
    plan=p.build()
    assert plan==json.loads((P/'COMPLETED_MARKED_PREFIX_PLAN.json').read_text())
    for path,h in plan['source_sha256'].items():
        assert sha256(Path(path).read_bytes()).hexdigest()==h,path
    out={'status':'PASS_COMPLETED_PREFIX_PLACEMENT_AND_FULL_EFFECT_JET_IDENTITIES',
         'literal_A49_prefix_fixtures':placement(),'exact_algebra':algebra(),
         'production_prefixes_executed':False,'all_original_descriptor_marks_proved':False,
         'physical_C_closed':False,'GR_closed':False,
         'source_sha256':{str(f):sha256(f.read_bytes()).hexdigest() for f in
                          [Path(__file__),P/'completed_marked_prefixes.py',P/'COMPLETED_MARKED_PREFIX_PLAN.json']}}
    (P/'COMPLETED_MARKED_PREFIX_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
    print(out['status'])


if __name__=='__main__':
    main()
