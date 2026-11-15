#!/usr/bin/env python3
"""Paid lengths, exact growing-clock feedback, fixed-post derivative identity."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import hashlib,json,sys
import sympy as S
import fixed_post_paid_family as p
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent


def count(factory):
    out=Counter()
    for t in factory():out.update(p.native.counts(t))
    return out


def classical(op,x):
    name,*w=op
    if name=='X':return x^(1<<w[0])
    assert name=='CX';return x^((1<<w[1]) if (x>>w[0])&1 else 0)


def small_families():
    ks={'pi8':1,'pi6':2,'half_theta':3,'minus_half_theta':4,'minus_theta':5,'beta':6,'minus_beta':7}
    macro=p.native.Macros({'status':'PASS_SEVEN_CERTIFIED_POSITIVE_G_POWERS','error_bits':20000,
      'rotations':{k:{'exponent_hex':hex(v)} for k,v in ks.items()}})
    sam=(1,2,3);n=4
    core=[p.gate('G',0),p.gate('CX',sam[0],0),p.gate('G',0)]
    post=[p.gate('G',sam[0]),p.gate('CX',sam[1],sam[2])]
    coref=lambda:iter(core);postf=lambda:iter(post)
    cfg=p.align(n,sam,count(coref),count(postf),(2,3),3,1);cfg['K']=2
    cases=[];columns=0
    for a in range(8):
        for b in range(a+1,8):
            pivot,ops=p.plane_affine(a,b,tuple(range(3)))
            for x in range(8):
                y=x
                for op in ops:y=classical(op,y)
                if x==a:assert y==0
                if x==b:assert y==1<<pivot
                for op in reversed(ops):y=classical(op,y)
                assert y==x;columns+=1
            for k in (2,3):
                actual=count(lambda:p.plane_blocks(a,b,k,sam,macro))
                assert actual==p.plane_counts(3,a,b,k,1)
                assert all(actual[x]<=cfg['probe_upper'][x] for x in ('G','CX'))
                cases.append({'outgoing_plane':(a,b),'outgoing_power':k})
    for sign in ('centre','plus','minus'):
        for j in range(3):cases.append({'incoming_sign':sign,'incoming_index':j})
    summary=[]
    for args in cases:
        dim=1;D=0;steps=0;calls=Counter();width=0;last=None
        for stage in p.execution_stages(cfg,coref,postf,macro,**args):
            D+=dim;steps+=1;last=stage
            if stage['kind']=='canonical_RAW_birth':
                assert stage['wire']==width;width+=1;dim*=2
            else:
                assert max(stage['gate']['wires'])<width
                calls[stage['gate']['op']]+=1
        assert last=={'kind':'final_unitary_g','gate':p.gate('G',n+cfg['K']-1)}
        assert width==n+cfg['K'] and steps==cfg['Nbase']+2*cfg['K']
        assert sum(calls.values())==cfg['Lbase']+cfg['K']
        assert D==(1<<n)*(cfg['Lbase']-2+3*(1<<cfg['K']))-1
        summary.append((steps,D,dim))
    assert len(set(summary))==1
    # Every small identity padding is I on every SAM basis input.
    for length in range(4,23):
        trees=list(p.padding(length,tuple(range(3))));ops=[g for t in trees for g in p.a41.e.leaves(t)]
        assert len(ops)==length
        for x in range(8):
            y=x
            for g in ops:y=classical((g['op'],*g['wires']),y)
            assert y==x
    return len(cases),columns


def exact_clock(K):
    """Full G1-G10 rational fixture, same birth/rotation shape, not Golden numerics."""
    c,s=S.Rational(3,5),S.Rational(4,5)
    def birth(d):return (c*S.eye(d)).col_join(s*S.eye(d))
    def Gnew(d):return (c*S.eye(d)).row_join(-s*S.eye(d)).col_join((s*S.eye(d)).row_join(c*S.eye(d)))
    # One early birth; one native-shape rotation; K birth/G pairs, last G final.
    actions=[birth(1),Gnew(1)];passive=[birth(1),S.eye(2)];dims=[1,2];d=2
    for j in range(K):
        dims += [d,2*d];actions += [birth(d),Gnew(d)];passive += [birth(d),S.eye(2*d)];d*=2
    N=len(actions);D=sum(dims);df=dims[-1];starts=[];pos=0
    for width in dims:starts.append(pos);pos+=width
    def B(start):
        out=S.eye(dims[start])
        for j in range(start,N-1):out=passive[j]*out
        return out
    R=B(0).T
    for j in range(1,N):
        detail=S.eye(dims[j])-passive[j-1]*passive[j-1].T
        R=R.col_join(detail*B(j).T)
    assert R.T*R==S.eye(df)
    shift=S.zeros(D)
    for j in range(N-1):
        shift[starts[j+1]:starts[j+1]+dims[j+1],starts[j]:starts[j]+dims[j]]=actions[j]
    Ef=S.zeros(df,D);Ef[:,starts[-1]:]=S.eye(df)
    T=shift+R*actions[-1]*Ef
    assert T.T*T==S.eye(D) and T*T.T==S.eye(D)
    cut=S.zeros(D);A=S.eye(1)
    for j in range(N):
        cut[starts[j]:starts[j]+dims[j],starts[j]:starts[j]+dims[j]]=A*A.T
        if j<N-1:A=actions[j]*A
    C=(B(0).T*actions[-1]*A)[0]
    assert C==c**(K+1)
    feedback=cut*T.T*(S.eye(D)-cut)*T*cut
    last_projector=S.zeros(D);last_projector[starts[-1]:,starts[-1]:]=A*A.T
    assert feedback==(1-C*C)*last_projector
    assert S.trace(last_projector)==1
    z=S.Rational(1,16)
    assert (S.eye(D)-z*feedback).det()==1-z+z*C*C
    assert D==2*(1-2+3*(1<<K))-1
    return {'K':K,'clock_dimension':D,'stages':N,'return':str(C)}


def fixed_post_identity():
    chi=S.Matrix([1,2,2,4])/5
    M=S.diag(S.Rational(9,10),S.Rational(4,5),S.Rational(3,4),S.Rational(7,8))
    q=(chi.T*M*M*chi)[0];r=S.sqrt(q);xi=M*chi/r
    K=chi*xi.T-xi*chi.T;U=S.eye(4)+K+K*K/(1+(chi.T*xi)[0])
    assert (U.T*chi-xi).applyfunc(S.simplify)==S.zeros(4,1)
    c=(chi.T*U*M*chi)[0];assert S.simplify(c-r)==0
    checked=0
    for a in range(4):
        for b in range(a+1,4):
            X=S.zeros(4);X[b,a]=1;X[a,b]=-1
            cp=(chi.T*U*M*X*chi)[0]
            qprime=(chi.T*(X.T*M*M+M*M*X)*chi)[0]
            assert S.simplify(2*c*cp-qprime)==0
            # Holding post fixed, differentiating only the incoming factor.
            assert S.simplify((chi.T*U*X*M*chi)[0])!=cp or qprime==0
            checked+=1
    return checked


def main():
    histories,columns=small_families();clocks=[exact_clock(k) for k in (1,2)]
    derivative_cases=fixed_post_identity()
    plan=p.build();assert plan==json.loads((P/'FIXED_POST_PAID_FAMILY_PLAN.json').read_text())
    for f,h in plan['source_sha256'].items():assert hashlib.sha256(Path(f).read_bytes()).hexdigest()==h
    cfg=p.production_configuration()
    try:
        next(p.execution_stages(cfg,lambda:iter(()),lambda:iter(()),p.native.Macros()))
        raise AssertionError('production upper counts accepted as an actual word')
    except NotImplementedError:pass
    pins=[Path(__file__),P/'fixed_post_paid_family.py',P/'FIXED_POST_PAID_FAMILY_PLAN.json']
    out={'status':'PASS_FIXED_POST_PAID_LENGTHS_FULL_CLOCK_FEEDBACK_AND_SOURCE_IDENTITY',
      'full_small_histories_replayed':histories,'exact_affine_basis_columns_checked':columns,
      'full_small_rational_clock_fixtures':clocks,'independent_fixed_post_derivative_planes':derivative_cases,
      'full_clock_unitarity_and_rank_one_feedback_checked':True,
      'same_fixed_post_in_all_small_incoming_comparisons':True,
      'production_upper_count_not_confused_with_materialized_word':True,
      'new_clock_coefficient':3,'late_retention_pairs':137444,
      'production_word_or_absolute_heat_trace_evaluated':False,
      'full_original_H1_four_slot_admission_proved':False,'physical_C_closed':False,'GR_closed':False,
      'source_sha256':{str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in pins}}
    (P/'FIXED_POST_PAID_FAMILY_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('status','full_small_histories_replayed','independent_fixed_post_derivative_planes')}))


if __name__=='__main__':main()
