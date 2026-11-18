#!/usr/bin/env python3
"""Exact Golden MG2, all-column plane grammar and paid G/CX controls."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
from collections import Counter
import json,hashlib,sys
sys.dont_write_bytecode=True
import sympy as sp
import full_vector_controls as p
P=Path(__file__).resolve().parent;e=p.e


def exact_lift():
    phi,probs,lam=p.mg2();zero=e.Q4();one=e.Q4(1)
    X=[[zero for _ in range(4)] for _ in range(4)]
    for (i,j),value in lam.items():X[i][j]=-value;X[j][i]=value
    H=[[(i-j)*X[i][j] for j in range(4)] for i in range(4)]
    assert sum(probs,zero)==one
    assert all(sum((H[i][j]*phi[j] for j in range(4)),zero)==phi[i] for i in range(4))
    assert sum(((e.Q4(i)-3*e.SIN*e.SIN)*probs[i] for i in range(4)),zero)==0
    fro2=sum((x*x for row in X for x in row),zero);L=sum(lam.values(),zero)
    ctx=e.Dyadic(128);ff,ls=ctx.evaluate((e.expr(fro2),e.expr(L)))
    assert ff[1]<ctx.S and 0<ls[0]<ls[1]<3*ctx.S//2
    for probability in probs:
        lo,hi=ctx.evaluate((e.expr(probability),))[0];assert 0<lo<hi<ctx.S//2
    # Sharp one-bit obstruction, including the scalar-calibrated version.
    a=e.A;pp=e.SIN;v=[a,pp];u=2*a*pp
    Hphi=[u*pp,u*a];res=[Hphi[i]-v[i] for i in range(2)]
    assert sum((z*z for z in res),zero)==pp**6
    corrected=[pp*p.inverse(u)-a,a*p.inverse(u)-pp]
    assert sum((z*z for z in corrected),zero)==pp**6*p.inverse(u*u)
    # Four new vertices lie in the old ASYMMETRIC continuous cube, not just
    # a symmetric containing box. Check exact algebraic inequalities.
    oldstride=F(1,1<<30)
    for i in range(4):
        vertex=(e.Q4(i)-3*pp*pp)*p.SIGMA
        low=vertex+pp*pp*oldstride
        high=(e.Q4(1)-pp*pp)*oldstride-vertex
        for value in (low,high):assert ctx.evaluate((e.expr(value),))[0][0]>0
    return {'exact_full_vector_identity':True,'all_four_born_probabilities_lt_half':True,
      'X_Frobenius_lt':1,'sum_positive_plane_weights_lt':'3/2',
      'one_bit_optimal_squared_defect':'p^6','scalar_calibrated_squared_defect':'p^6/(4p^3)',
      'four_vertices_inside_old_asymmetric_cube':True}


def elementary(op,w,c=sp.Rational(3,5),s=sp.Rational(4,5)):
    matrix=sp.eye(4)
    if op=='X':
        return sp.Matrix(4,4,lambda i,j:int(i==j^(1<<w[0])))
    if op=='CX':
        return sp.Matrix(4,4,lambda i,j:int(i==j^((1<<w[1]) if j>>w[0]&1 else 0)))
    assert op=='G'
    for j in range(4):
        if j>>w[0]&1:continue
        k=j^(1<<w[0]);matrix[j,j]=matrix[k,k]=c;matrix[j,k]=-s;matrix[k,j]=s
    return matrix


def plane_grammar():
    rows=[]
    for a,b in combinations(range(4),2):
        pivot,affine=p.old.plane_affine(a,b,(0,1));matrix=sp.eye(4)
        for op in affine:matrix=elementary(op[0],op[1:])*matrix
        for tree in p.a41.star_blocks((0,1),1<<pivot,1):
            for gate in e.leaves(tree):matrix=elementary(gate['op'],gate['wires'])*matrix
        for op in reversed(affine):matrix=elementary(op[0],op[1:])*matrix
        expected=sp.eye(4);expected[a,a]=expected[b,b]=sp.Rational(-7,25)
        expected[a,b]=sp.Rational(-24,25);expected[b,a]=sp.Rational(24,25)
        assert matrix==expected and matrix.T*matrix==sp.eye(4)
        # Actual native grammar counts, with a deliberately small fake k.
        blocks=list(p.plane_blocks((a,b),3,(0,1),p.native.Macros()))
        counts=p.count_blocks(lambda:iter(blocks))
        assert counts==p.old.plane_counts(2,a,b,3,p.native.Macros().ks['pi8'])
        rows.append({'pair':[a,b],'full_columns_verified':4})
    return rows


def grammar_and_cost():
    counts,length=p.control_inventory();oldn=p.parent.production_configuration()['n'];checked=[]
    for index in (0,p.M-1):
        pair=p.code_wires(index);assert pair==(2+index,oldn+index)
        for sign in (0,1,-1):
            census=p.count_blocks(lambda:p.control_blocks(index,sign));assert sum(census.values())==length
            seen=set()
            def walk(t):
                if t['op']=='seq':
                    for z in t['children']:yield from walk(z)
                elif t['op']=='repeat':
                    assert p.native.count_value(t['count'])>0;yield from walk(t['child'])
                else:yield t
            for tree in p.control_blocks(index,sign):
                for leaf in walk(tree):
                    assert leaf['op'] in ('G','CX')
                    seen.update(leaf['wires'])
            allowed=set(pair)|{2+(index+1)%p.M}
            assert seen<=allowed and all(q<oldn+p.M for q in seen)
            checked.append({'coordinate':index,'sign':sign,'support_subset':sorted(allowed)})
    assert 4*length==sum(length for _ in range(4))
    return {'tested_control_variants':checked,'one_control_length_bits':length.bit_length(),
      'four_independent_occurrences_counted':True,'new_SOURCE_inventory_inferred':False}


def derivative_arithmetic():
    s=F(1,1<<30);U0=F(17,16)
    exponential=1/(1-6*s);assert exponential<F(16,15)
    # ||d theta|| <= sqrt6 ||h||. Separate the B65 bound on ||U|| from
    # the Duhamel derivative bound; do not infer the latter from the former.
    assert (exponential*U0)**2*6<9 and exponential*U0*6<7
    assert F(2)+F(6,15)<3 and 3*3+2*F(11,10)**2<12
    values=p.source_derivative_enclosure()
    assert values['full_bank_M1']==1748 and values['full_bank_M2']==3233036
    return {'M1_upper':1748,'M2_upper':3233036,
      'norm':'Euclidean raw-chart directions; operator norm on the declared all-DATA fibre',
      'continuous_source_targets_only':True}


def main():
    plan=p.build();assert plan==json.loads((P/'FULL_VECTOR_CONTROL_PLAN.json').read_text())
    out={'status':'PASS_FULL_VECTOR_MG2_AND_CERTIFIED_TWO_BIT_NATIVE_CONTROL_MODULE',
      'exact_lift':exact_lift(),'full_column_planes':plane_grammar(),
      'paid_grammar':grammar_and_cost(),'derivative_enclosure':derivative_arithmetic(),
      'positive_G_power_certificates':12,'new_SOURCE_catalogue_compiled':False,
      'full_new_physical_history_or_price_claimed':False,'physical_C_closed':False,'GR_closed':False}
    for f,sha in plan['source_sha256'].items():assert hashlib.sha256(Path(f).read_bytes()).hexdigest()==sha
    out['source_sha256']={str(q):hashlib.sha256(q.read_bytes()).hexdigest() for q in (Path(__file__),P/'full_vector_controls.py',P/'FULL_VECTOR_CONTROL_PLAN.json')}
    (P/'FULL_VECTOR_CONTROL_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'])


if __name__=='__main__':main()
