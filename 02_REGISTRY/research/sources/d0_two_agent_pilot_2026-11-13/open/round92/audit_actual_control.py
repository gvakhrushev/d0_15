#!/usr/bin/env python3
"""B92: independent integer interval and compressed-word audit of frozen A47."""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt,gcd
from itertools import combinations
from collections import Counter
from hashlib import sha256
import json,sys
sys.dont_write_bytecode=True
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
sys.path.insert(0,str(D/'round47'))
import full_vector_controls as a
P=Path(__file__).resolve().parent
files={'full_vector_controls.py':'31ff35852f723b4b0cb8d04e3d46be5a0e03785fb9aa0b00f7ce140b54d46ad9','FULL_VECTOR_CONTROL_PLAN.json':'0e813ed5d9ab8d82bd45027b211f3d975145bdeadcc314363365b391fcf878b6','FULL_VECTOR_CONTROL_CHECK.json':'2f8c9414a5da53cf73dedae891d7cc8d7028e86db2ea8cd4ed8955141691c56e','FULL_VECTOR_REPAIR_RU.md':'b89a13313689bb2f39bbc76714e6ca5445bcf86bf3e4cce7732d5c4123f07d44'}
for name,h in files.items():assert sha256((D/'round47'/name).read_bytes()).hexdigest()==h,name
plan=json.loads((D/'round47/FULL_VECTOR_CONTROL_PLAN.json').read_text())
cert=json.loads(a.a41.CERT.read_text());pn=int(cert['numerator_hex'],16);q=int(cert['denominator_hex'],16);pb=cert['precision_bits'];E=int(cert['abs_qgamma_minus_numerator_bound_numerator_hex'],16)
assert gcd(pn,q)==1 and q*E<1<<pb
# Independent fixed-point interval arithmetic. No A41 angle selector/atan/evaluator.
BITS=20736;S=1<<BITS
def divup(x,y):return -((-x)//y)
def add(x,y):return x[0]+y[0],x[1]+y[1]
def neg(x):return -x[1],-x[0]
def mul(x,y):
    vals=[i*j for i in x for j in y];return min(vals)//S,divup(max(vals),S)
def ratio(x,n,d):
    assert d>0
    return (x[0]*n//d,divup(x[1]*n,d)) if n>=0 else neg(ratio(x,-n,d))
def divide(x,y):
    assert y[0]>0
    vals=[F(i*S,j) for i in x for j in y];return min(v.numerator//v.denominator for v in vals),max(divup(v.numerator,v.denominator) for v in vals)
def sqrt(x):
    assert x[0]>=0
    lo=isqrt(x[0]*S);hi=isqrt(x[1]*S);return lo,hi+(hi*hi<x[1]*S)
root5=sqrt((5*S,5*S));p=ratio(add(root5,(-S,-S)),1,2);alpha=sqrt(p)
powers=[(S,S),alpha,mul(alpha,alpha),mul(mul(alpha,alpha),alpha)]
def expression(coeff):
    z=(0,0)
    for (n,d),power in zip(coeff,powers):z=add(z,ratio(power,int(n),int(d)))
    return z
def atan_interval(z):
    # atan(z)=sum to degree 27 + remainder <= |z|^29/29.
    z2=mul(z,z);term=z;out=(0,0)
    for k in range(14):
        v=ratio(term,1,2*k+1);out=add(out,v if k%2==0 else neg(v));term=mul(term,z2)
    rem=divup(max(abs(term[0]),abs(term[1])),29)
    return out[0]-rem,out[1]+rem
pi0=[int(x,16) for x in cert['pi_interval_hex']];sh=pb-BITS;pi=(pi0[0]>>sh,divup(pi0[1],1<<sh));assert 3*S<pi[0]<pi[1]<4*S
records=[]
for pair in combinations(range(4),2):
    key='%d_%d'%pair;lam=expression(plan['lambda_Qa'][key]);assert 0<lam[0]<lam[1]
    for sign in (1,-1):
        entry=plan['positive_G_power_library'][key][str(sign)];k=int(entry['k_hex'],16);j=int(entry['signed_grid_index_hex'],16)
        assert 1<=k<=q and (k*pn-j)%q==0
        z=ratio(lam,sign,1<<1702);turn=divide(atan_interval(z),ratio(pi,2,1))
        cell=max(abs(j*S-q*turn[0]),abs(j*S-q*turn[1]))
        bound=7*(F(cell,q*S)+F(k*E,q*(1<<pb)))
        assert bound<F(1,1<<20075),(key,sign)
        records.append({'pair':list(pair),'sign':sign,'positive_exponent':True,'certified_half_angle_lt':'2^-20075'})
# Independent recursive compressed census; no expansion of huge repeats.
def count(tree):
    op=tree['op']
    if op=='seq':
        c=Counter()
        for child in tree['children']:c.update(count(child))
        return c
    if op=='repeat':
        n=int(tree['count'],16);assert n>0
        return Counter({k:n*v for k,v in count(tree['child']).items()})
    assert op in ('G','CX') and len(set(tree['wires']))==len(tree['wires'])
    return Counter({op:1})
def census(trees):
    c=Counter()
    for t in trees:c.update(count(t))
    return c
k8=int(json.loads((D/'round38/POST_ANGLE_CERTIFICATE.json').read_text())['rotations']['pi8']['exponent_hex'],16)
raw={}
for sign in (-1,1):
    expected=Counter()
    for i,j in combinations(range(4),2):
        k=int(plan['positive_G_power_library'][f'{i}_{j}'][str(sign)]['k_hex'],16)
        ones=bin(i).count('1');diff=bin(i^j).count('1')
        expected.update({'G':2*(2*k+40*ones*k8),'CX':2*(2+2*(diff-1)+4*ones)})
    got=census(a.raw_control_blocks(0,sign));assert got==expected
    assert {k:hex(v) for k,v in got.items()}==plan['raw_control_counts'][str(sign)]
    raw[sign]=got
length=max(map(lambda c:sum(c.values()),raw.values()))+4
assert hex(length)==plan['each_padded_control_calls_hex'] and hex(4*length)==plan['all_four_controls_calls_hex']
for index in (0,a.M-1):
    for sign in (-1,0,1):
        got=census(a.control_blocks(index,sign));assert sum(got.values())==length
# Prove the two padding building blocks as exact permutations on all 8 columns.
def cx(v,c,t):return v^(((v>>c)&1)<<t)
for v in range(8):
    w=cx(cx(v,0,1),0,1);assert w==v
    w=v
    for c,t in [(0,1),(1,2),(0,1),(1,2),(0,2)]:w=cx(w,c,t)
    assert w==v
# Independently establish each affine map sends a to zero and b to positive pivot.
for i,j in combinations(range(4),2):
    pivot,ops=a.old.plane_affine(i,j,(0,1))
    def apply(v):
        for op in ops:
            if op[0]=='X':v^=1<<op[1]
            else:v=cx(v,op[1],op[2])
        return v
    assert apply(i)==0 and apply(j)==1<<pivot
# Test nominal X lowering and all six actual star/affine orientations on full 4x4 matrices.
import sympy as sp
def rotation(w,c,s):
    m=sp.eye(4)
    for v in range(4):
        if v>>w&1:continue
        j=v^(1<<w);m[v,v]=m[j,j]=c;m[v,j]=-s;m[j,v]=s
    return m
def cmat(c,t):return sp.Matrix(4,4,lambda i,j:int(i==cx(j,c,t)))
def xmat(q):return sp.Matrix(4,4,lambda i,j:int(i==(j^(1<<q))))
for q0,h in ((0,1),(1,0)):
    nominal=rotation(q0,0,1)*rotation(h,0,-1)*cmat(q0,h)*rotation(h,0,1)*cmat(q0,h)
    assert nominal==xmat(q0)
class NominalX:
    def x(self,q,helper):return {'op':'X','wires':[q]}
for i,j in combinations(range(4),2):
    m=sp.eye(4)
    for tree in a.plane_blocks((i,j),1,(0,1),NominalX()):
        if tree['op']=='repeat':
            assert int(tree['count'],16)==1 and tree['child']['op']=='G'
            gate=rotation(tree['child']['wires'][0],sp.Rational(3,5),sp.Rational(4,5))
        elif tree['op']=='CX':gate=cmat(*tree['wires'])
        else:assert tree['op']=='X';gate=xmat(tree['wires'][0])
        m=gate*m
    target=sp.eye(4);target[i,i]=target[j,j]=sp.Rational(-7,25)
    target[i,j]=sp.Rational(-24,25);target[j,i]=sp.Rational(24,25)
    assert m==target
# Exact rational budgets; no claims about future source compilation.
t=F(1,1<<1700);sigma=F(1,1<<80);L=F(3,2);delta=F(1,1<<20000)
eps=F(17,48)*L**3*t**3+504*delta
assert eps<F(1,1<<5099)
eB=F(1,1<<3300);eM=F(1,1<<3298);gain=F(1,1<<3208)
extra=(eB+2*eps)/(sigma*t)+F(4,3)*104*1748*t*t
ideal=sigma*104**2*3233036
assert extra<F(1,1<<1519) and ideal+extra<F(1,1<<44) and eM/gain<F(1,1<<89)
result={'status':'PASS_INDEPENDENT_FROZEN_A47_GRID_GRAMMAR_CENSUS_CONDITIONAL_BUDGET','frozen_sha256':files,'independent_interval_precision_bits':BITS,'independent_positive_angles':records,'grid_certificate_sha256':sha256(a.a41.CERT.read_bytes()).hexdigest(),'six_affine_plane_maps_checked':True,'nominal_macro_and_six_oriented_full_4x4_planes_checked':True,'compressed_word_counts_match':True,'all_three_controls_equal_length':True,'four_control_occurrences':4,'padding_identity_checked_all_eight_columns':True,'control_error_lt':'2^-5099','conditional_full_finite_jet_lt':'2^-44','new_source_recompiled':False,'new_full_clock_or_heat_computed':False,'marked_history_admission_proved':False,'GR_closed':False}
(P/'B92_ACTUAL_CONTROL_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
print(result['status'])
