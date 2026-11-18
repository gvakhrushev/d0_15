#!/usr/bin/env python3
"""Exact small all-column algebra, literal field evaluator and selector checks."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import hashlib,json,sys
import sympy as S
import sam_only_compiler as p
e=p.e;P=Path(__file__).resolve().parent


def symbolic(targets):
    a=S.sqrt((S.sqrt(5)-1)/2);memo={};todo=[(x,False) for x in targets]
    while todo:
        x,ready=todo.pop()
        if x in memo:continue
        if x.op=='field':
            memo[x]=sum(S.Rational(c.numerator,c.denominator)*a**j for j,c in enumerate(x.args[0].v));continue
        if not ready:
            todo.append((x,True));todo.extend((y,False) for y in x.args);continue
        t=[memo[y] for y in x.args]
        if x.op=='add':v=t[0]+t[1]
        elif x.op=='neg':v=-t[0]
        elif x.op=='mul':v=t[0]*t[1]
        elif x.op=='div':v=t[0]/t[1]
        else:assert x.op=='sqrt';v=S.sqrt(t[0])
        memo[x]=S.simplify(v)
    return [memo[x] for x in targets]


def rpow(c,s,n):
    u,v=F(1),F(0)
    for _ in range(n):u,v=u*c-v*s,v*c+u*s
    return u,v


def native_column(blocks,m,col,c,s,offset=0):
    v=[F(i==col) for i in range(1<<m)];counts=Counter()
    for tree in blocks:
        for op in e.leaves(tree):
            counts[op['op']]+=1;w=[q-offset for q in op['wires']]
            assert all(0<=q<m for q in w)
            t=1<<w[-1]
            for x in range(len(v)):
                if x&t:continue
                y=x|t
                if op['op']=='G':v[x],v[y]=c*v[x]-s*v[y],s*v[x]+c*v[y]
                elif (x>>w[0])&1:v[x],v[y]=v[y],v[x]
    return v,counts


def check_field():
    X=S.Symbol('a');mod=X**4+X**2-1
    def poly(v):return sum(S.Rational(c.numerator,c.denominator)*X**j for j,c in enumerate(v.v))
    def red(v):return S.rem(S.expand(v),mod,X)
    assert e.A**4+e.A**2==1 and e.A*e.A+e.SIN*e.SIN==1
    for i in range(7):
        a=e.Q4(tuple(F(j-i,1+j) for j in range(4)))
        b=e.Q4(tuple(F(i+2*j,2+j) for j in range(4)))
        assert red(poly(a)*poly(b))==poly(a*b)
    # Independent full 16x16 polynomial native word, two SAM/two WORK bits.
    blocks=[p.gate('G',0),p.gate('CX',2,0),p.gate('G',1),p.gate('CX',0,1),
            p.repeat(2,p.gate('G',0)),p.gate('CX',3,1)]
    W=S.eye(16)
    for op in (g for tree in blocks for g in e.leaves(tree)):
        G=S.zeros(16);w=op['wires'];t=1<<w[-1]
        for b in range(16):
            if op['op']=='CX':G[b^t if (b>>w[0])&1 else b,b]=1
            else:
                G[b,b]=X;G[b^t,b]=X**2 if not b&t else -X**2
        W=(G*W).applyfunc(red)
    vv=[poly(v) for v in e.born(2)]
    for b in range(4):
        expected=red(sum(vv[i]*W[(b<<2)|i,(b<<2)|j]*vv[j] for i in range(4) for j in range(4)))
        actual=e.compressed_entry(4,(2,3),b,lambda:iter(blocks))
        assert poly(actual)==expected
    for i in range(16):
        for j in range(16):
            if (i>>2)!=(j>>2):assert W[i,j]==0
    return 4


def check_householder():
    fixtures=[([F(3,5),F(4,5)],[F(5,13),F(12,13)]),
              ([F(1,5),F(2,5),F(2,5),F(4,5)],[F(2,5),F(1,5),F(4,5),F(2,5)]),
              ([F(1,5),F(2,5),F(2,5),F(4,5)],[F(1,5),F(2,5),F(2,5),F(4,5)])]
    for aa,bb in fixtures:
        chi=list(map(e.expr,aa));xi=list(map(e.expr,bb));z=[a+b for a,b in zip(chi,xi)]
        hn=e.norm(z);h=[x/hn for x in z];d=len(chi);actual=S.eye(d)
        stars=list(p.target_stars(chi,h));assert len(stars)==4*(d-1)
        for j,c,s in stars:
            c,s=symbolic([c,s]);R=S.eye(d);R[0,0]=R[j,j]=c;R[j,0]=s;R[0,j]=-s
            actual=(R*actual).applyfunc(S.simplify)
        x=S.Matrix(symbolic(chi));y=S.Matrix(symbolic(xi));hh=S.Matrix(symbolic(h))
        target=(S.eye(d)-2*x*x.T)*(S.eye(d)-2*hh*hh.T)
        K=x*y.T-y*x.T;rank2=S.eye(d)+K+K*K/(1+(x.T*y)[0])
        assert (actual-target).applyfunc(S.simplify)==S.zeros(d)
        assert (actual-rank2).applyfunc(S.simplify)==S.zeros(d)
        assert (actual*y-x).applyfunc(S.simplify)==S.zeros(d,1)
    return len(fixtures)


def check_walsh():
    cases=columns=0
    for m in (2,3,4):
        for j in range(1,1<<m):
            for k in (1,2):
                blocks=list(p.star_blocks(range(2,m+2),j,k));L=1<<(m-1)
                c,s=rpow(F(3,5),F(4,5),L*k)
                for col in range(1<<m):
                    v,counts=native_column(blocks,m,col,F(3,5),F(4,5),offset=2)
                    target=[F(x==col) for x in range(1<<m)]
                    if col==0:target[0],target[j]=c,s
                    if col==j:target[0],target[j]=-s,c
                    assert v==target
                    assert counts=={'G':L*k,'CX':(m-1)*L+2*(bin(j).count('1')-1)}
                    columns+=1
                cases+=1
    return cases,columns


def check_intervals():
    ctx=e.Dyadic(256);S0=ctx.S
    a=ctx.field(e.A)
    # a is the unique positive root of x^4+x^2=1.
    lo,hi=(F(x,S0) for x in a)
    assert lo**4+lo**2<=1<=hi**4+hi**2
    for v in (F(1,5),F(3,5),F(4,5)):
        x=e.root(e.expr(v*v));iv=ctx.evaluate([x])[0]
        assert F(iv[0],S0)<=v<=F(iv[1],S0)
    # atan enclosure contains independent rational alternating-series bounds.
    for x in (F(1,2),F(3,4)):
        n=int(x*S0);iv=p.atan_positive(ctx,n);N=700
        total=sum(((-1)**i*x**(2*i+1)/F(2*i+1) for i in range(N)),F())
        rem=x**(2*N+1)/F(2*N+1)
        assert F(iv[0],S0)<=total-rem<total+rem<=F(iv[1],S0)
        assert p.atan_signed(ctx,-n)==(-iv[1],-iv[0])
    # One actual 20,080-bit grid selection, not an assumed arbitrary angle.
    c,s=p.divided_angle(e.expr(F(3,5)),e.expr(F(-4,5)),2)
    k=p.select_positive_power(c,s)
    pn,q,cert=p.uniform_grid();assert 1<=k<=q
    # The selected cell is checked independently against a higher precision
    # enclosure of atan(-1/2)/(2pi). Uniform orbit error itself is B80.
    high=e.Dyadic(22000);alpha=p.atan_signed(high,-high.S//2)
    pi0=[int(v,16) for v in cert['pi_interval_hex']];shift=cert['precision_bits']-high.bits
    pi=(pi0[0]>>shift,-((-pi0[1])>>shift));tau=high.div(alpha,(2*pi[0],2*pi[1]))
    cell=F((k*pn)%q,q)
    for endpoint in tau:
        diff=(cell-F(endpoint,high.S))%1;dist=min(diff,1-diff)
        assert dist<=F(3,4*q)
    return {'exponent_hex':hex(k),'exponent_bits':k.bit_length(),'independent_target':'atan(-1/2)/(2pi)',
            'selected_rational_cell_error_le':'3/(4q)','uniform_actual_G_error_from_B80_strict_lt':'2^-20075'}


def main():
    field=check_field();hh=check_householder();cases,columns=check_walsh();selection=check_intervals()
    plan=p.build();assert plan==json.loads((P/'SAM_ONLY_COMPILER_PLAN.json').read_text())
    for f,h in plan['source_sha256'].items():assert hashlib.sha256(Path(f).read_bytes()).hexdigest()==h
    for disabled in (p.production_word,e.production_target):
        try:disabled();raise AssertionError('unimplemented production path accepted')
        except NotImplementedError:pass
    pins=[Path(__file__),P/'exact_target.py',P/'sam_only_compiler.py',P/'SAM_ONLY_COMPILER_PLAN.json']
    out={'status':'PASS_EXACT_SMALL_ALL_COLUMNS_AND_ACTUAL_MODULAR_SELECTION',
      'independent_polynomial_M_entries':field,'exact_full_Householder_rank2_fixtures':hh,
      'exact_native_Walsh_star_words':cases,'all_basis_columns_checked':columns,
      'actual_uniform_grid_selection':selection,
      'all_column_production_norm_bound_checked':True,'production_Python_provider_implemented':False,
      'production_target_table_or_word_materialized':False,'physical_C_closed':False,'GR_closed':False,
      'source_sha256':{str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in pins}}
    (P/'SAM_ONLY_COMPILER_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('status','exact_full_Householder_rank2_fixtures','all_basis_columns_checked')}))


if __name__=='__main__':main()
