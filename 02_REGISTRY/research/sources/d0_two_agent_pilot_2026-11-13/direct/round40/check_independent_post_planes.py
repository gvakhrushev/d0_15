#!/usr/bin/env python3
"""All small planes, actual comparator IR, full toy histories and norm debt."""
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
from itertools import islice
import hashlib,json
import sympy as S
import independent_post_planes as p
P=Path(__file__).resolve().parent


def classical(op,reg):
    name,*w=op
    if name=='X':reg[w[0]]^=1
    elif name=='CX':reg[w[1]]^=reg[w[0]]
    else:
        assert name=='CCX';reg[w[2]]^=reg[w[0]]*reg[w[1]]


def main():
    ks={'pi8':1,'pi6':2,'half_theta':3,'minus_half_theta':4,'minus_theta':5,'beta':6,'minus_beta':7}
    macro=p.m.Macros({'status':'PASS_SEVEN_CERTIFIED_POSITIVE_G_POWERS','error_bits':20000,
                     'rotations':{k:{'exponent_hex':hex(v)} for k,v in ks.items()}})
    l=p.old.Layout(old=8,sam_count=4)
    w=[p.m.seq(p.m.gate('G',0),p.m.gate('CX',2,1))];wc=Counter(G=1,CX=1)
    def assembly(n):return p.old.Assembly(n,sam_index=0,level=0,layout=l,macros=macro,
                                W_factory=lambda:iter(w),W_counts=wc)
    base=assembly(0);plane_count=0;columns=0
    for a in range(16):
        for b in range(a+1,16):
            q=p.Plane(a,b,2,base);plane_count+=1
            affine=list(q.affine());reverse=list(q.affine(True))
            assert reverse==affine[::-1]
            selector=list(p.anchor.b.zero_predicate_ir(q.controls,l.flag,q.work))
            for x in range(16):
                reg={j:0 for j in range(l.total)}
                for j,wire in enumerate(l.sam):reg[wire]=(x>>j)&1
                for op in affine:classical(op,reg)
                mapped=sum(reg[wire]<<j for j,wire in enumerate(l.sam))
                if x==a:assert mapped==0
                if x==b:assert mapped==1<<q.pivot
                for op in selector:classical(op,reg)
                assert reg[l.flag]==(x in (a,b))
                assert all(reg[j]==0 for j in q.work)
                for op in reversed(selector):classical(op,reg)
                assert reg[l.flag]==0
                for op in reverse:classical(op,reg)
                assert sum(reg[wire]<<j for j,wire in enumerate(l.sam))==x
                columns+=1
            for inverse in (False,True):
                actual=Counter()
                for tree in q.blocks(inverse):actual.update(p.m.counts(tree))
                c=q.budget();assert actual=={'G':c['G'],'CX':c['CX']}
            # Both signs compile the same original power with identical cost,
            # independently, not B63's different positive inverse exponent.
            assert q.power==2
    assert plane_count==120 and columns==1920
    # The affine-conjugated real rotation is precisely one a,b plane.
    c,s=S.Rational(3,5),S.Rational(4,5)
    for a,b in ((0,1),(1,14),(7,8),(14,15)):
        q=p.Plane(a,b,1,base)
        perm=[]
        for x in range(16):
            reg={j:0 for j in range(l.total)}
            for j,w0 in enumerate(l.sam):reg[w0]=(x>>j)&1
            for op in q.affine():classical(op,reg)
            perm.append(sum(reg[w0]<<j for j,w0 in enumerate(l.sam)))
        U=S.zeros(16)
        for x,y in enumerate(perm):U[y,x]=1
        rot=S.eye(16);other=1<<q.pivot
        rot[0,0]=rot[other,other]=c;rot[other,0]=s;rot[0,other]=-s
        actual=U.T*rot*U;target=S.eye(16)
        target[a,a]=target[b,b]=c;target[b,a]=s;target[a,b]=-s
        assert actual==target and actual.T*actual==S.eye(16)
    # All positive/negative probes leave the deferred last scratch gate's
    # support disjoint. Full native toy histories use production generators.
    aa={n:assembly(v) for n,v in [('centre',0),('plus',2),('minus',3)]}
    basecfg=p.old.align_family(aa);cfg=p.configuration(basecfg,power=2);cfg['K']=3
    totals=[]
    for a,b in ((0,1),(7,8)):
        for sign in ('centre','plus','minus'):
            dim=1;dimension_sum=0;stages=0;calls=Counter();width=0;last=None
            for stage in p.execution_stages(a,b,sign,cfg):
                dimension_sum+=dim;stages+=1;last=stage
                if stage['kind']=='canonical_RAW_birth':
                    assert stage['wire']==width;width+=1;dim*=2
                else:
                    assert max(stage['gate']['wires'])<width;calls[stage['gate']['op']]+=1
            assert last=={'kind':'final_unitary_g','gate':p.m.gate('G',l.final_wire)}
            assert sum(calls.values())==cfg['Lbase']+cfg['K']
            assert stages==cfg['Nbase']+2*cfg['K']
            assert dimension_sum==(1<<l.total)*(cfg['Lbase']-3+4*(1<<cfg['K']))-1
            totals.append((stages,dim,dimension_sum))
    assert len(set(totals))==1
    # Weight identity for arbitrary normalized real states, no uniform-SAM
    # assumption and no independence of the enormous finite row errors.
    weights=[S.Rational(1,10),S.Rational(2,10),S.Rational(3,10),S.Rational(4,10)]
    assert sum(weights)==1
    assert sum(weights[i]+weights[j] for i in range(4) for j in range(i+1,4))==3
    x,y,z=S.symbols('x y z',real=True)
    v=S.Matrix([1,0]);yy=S.Matrix([S.Rational(3,5),S.Rational(4,5)])
    xx=S.Matrix([S.Rational(5,13),S.Rational(12,13)])
    diff=xx-yy
    assert (yy.T*diff)[0]==-diff.dot(diff)/2
    assert (v.T*diff)[0]==((v-yy).T*diff)[0]-diff.dot(diff)/2
    # Row-functional representation: A=(1/2)sum r_ab X_ab, so ||A||F^2
    # is sum(r_ab^2)/2, and Cauchy/nuclear norm supplies the dimension factor.
    rows={(0,1):x,(0,2):y,(1,2):z};A=S.zeros(3)
    for (a,b),r in rows.items():A[b,a]=r/2;A[a,b]=-r/2
    assert S.trace(A.T*A)==(x*x+y*y+z*z)/2
    for (a,b),r in rows.items():
        X=S.zeros(3);X[b,a]=1;X[a,b]=-1
        assert S.trace(A.T*X)==r
    # Actual production centre starts emitting; no hidden repeat zero.
    assert p.m.counts(next(p.before_final_blocks(0,1,'centre')))['CX']>0
    plan=p.build();assert plan==json.loads((P/'INDEPENDENT_POST_PLANES_PLAN.json').read_text())
    for f,h in plan['source_sha256'].items():assert hashlib.sha256(Path(f).read_bytes()).hexdigest()==h
    assert plan['late_retention_pairs']==162576 and plan['dimension_debt_bits']==4032
    assert 162576==146448+4*4032
    b={k:p.decode(v) for k,v in plan['bounds'].items()}
    assert b['feedback_full_covector_dual']+b['heat_full_covector_dual']==b['full_H_plus_J_finite_covector_dual']<F(1,1<<75)
    pins=[Path(__file__),P/'independent_post_planes.py',P/'INDEPENDENT_POST_PLANES_PLAN.json']
    out={'status':'PASS_ALL_SMALL_PLANES_FULL_TOY_CLOCK_AND_DIMENSION_AWARE_BOUNDS',
         'exhaustive_small_planes':plane_count,'all_basis_columns_checked':columns,
         'exact_symbolic_Givens_matrices_checked':4,'full_small_histories_replayed':6,
         'same_original_exponent_for_plus_and_inverse_targets':True,
         'weight_sum_and_finite_covector_normalization_checked':True,
         'all_row_dimension_debt_in_heat_paid':True,'giant_word_or_plane_family_materialized':False,
         'physical_C_closed':False,'GR_closed':False,
         'source_sha256':{str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in pins}}
    (P/'INDEPENDENT_POST_PLANES_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('status','exhaustive_small_planes','full_small_histories_replayed')}))


if __name__=='__main__':main()
