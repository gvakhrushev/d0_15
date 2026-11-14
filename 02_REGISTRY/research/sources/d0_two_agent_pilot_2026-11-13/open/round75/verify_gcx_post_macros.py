#!/usr/bin/env python3
"""All-column exact algebra and structural audit of the A38 macro DAGs."""
from pathlib import Path
from hashlib import sha256
from itertools import product
from collections import Counter
import importlib.util,json,sys
import sympy as s
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
A=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round38')
p=A/'gcx_post_macros.py'
spec=importlib.util.spec_from_file_location('a38_macros',p); a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
# Sentinel exponents identify all angle uses. pi8=1 permits counting directly.
ks={'pi8':1,'pi6':19,'half_theta':101,'minus_half_theta':107,'minus_theta':109,'beta':113,'minus_beta':127}
cert={'status':'PASS_SEVEN_CERTIFIED_POSITIVE_G_POWERS','error_bits':20000,
      'rotations':{n:{'exponent_hex':hex(v)} for n,v in ks.items()}}
m=a.Macros(cert)

def flatten(tree):
    op=tree['op']
    if op=='seq':
        for t in tree['children']: yield from flatten(t)
    elif op=='repeat':
        for _ in range(a.count_value(tree['count'])): yield from flatten(tree['child'])
    else: yield tree

def helper_phase(tree, inputs, helper):
    """Follow arbitrary helper as X^flip then a rotation on both columns.

    All tested CNOTs target helper; every G is a pi8 rotation of helper.
    Represent resulting all-column action as R(index*pi/8) X^flip.
    """
    angle=flip=0
    for g in flatten(tree):
        if g['op']=='G':
            assert g['wires']==[helper]
            angle += 1
        else:
            x,y=g['wires']; assert y==helper and x!=helper
            if inputs[x]: angle,flip=-angle,flip^1
    return angle%16,flip

# Arbitrary helper: exact conditional rotations are 0 or 8 units pi/8,
# and no residual flip occurs, independent of helper's input state.
for b in (0,1): assert helper_phase(m.z(0,1),{0:b},1)==(8*b,0)
for x in product((0,1),repeat=3):
    got=helper_phase(m.ccz(0,1,2,3),dict(enumerate(x)),3)
    assert got==(8*(x[0]*x[1]*x[2]),0)
assert a.counts(m.z(0,1))==Counter({'G':16,'CX':2})
assert a.counts(m.h(0,1))==Counter({'G':18,'CX':2})
assert a.counts(m.ccz(0,1,2,3))==Counter({'G':64,'CX':24})
assert a.counts(m.ccx(0,1,2,3))==Counter({'G':100,'CX':28})
assert m.h(0,1)==a.seq(m.z(0,1),m.pi8(0,2))
assert m.ccx(0,1,2,3)==a.seq(m.h(2,3),m.ccz(0,1,2,3),m.h(2,3))
sq=s.sqrt(2); Z=s.diag(1,-1); X=s.Matrix([[0,1],[1,0]])
rot45=s.Matrix([[1,-1],[1,1]])/sq; H=rot45*Z
assert H==s.Matrix([[1,1],[1,-1]])/sq and H*Z*H==X and H*H==s.eye(2)
# Exact chronology: for control=0, R(-h)R(h)=I; control=1,
# X R(-h) X R(h)=R(2h). The reverse exchanges the two signs.
c,t=s.symbols('c t',real=True)
plus=s.Matrix([[c,-t],[t,c]]);minus=s.Matrix([[c,t],[-t,c]])
assert X*minus*X==plus and X*plus*X==minus
assert minus*plus==(c*c+t*t)*s.eye(2)
assert X*minus*X*plus==plus*plus and X*plus*X*minus==minus*minus
for inverse in (False,True):
    first,second=('minus_half_theta','half_theta') if inverse else ('half_theta','minus_half_theta')
    assert m.controlled_g(0,1,inverse)==a.seq(m.angle(1,first),a.gate('CX',0,1),m.angle(1,second),a.gate('CX',0,1))
    p1,p2=(11,1) if inverse else (1,11)
    assert m.controlled_pi3(0,1,inverse)==a.seq(m.power(1,p1*ks['pi6']),a.gate('CX',0,1),m.power(1,p2*ks['pi6']),a.gate('CX',0,1))
    assert a.counts(m.controlled_g(0,1,inverse))==Counter({'G':208,'CX':2})
    assert a.counts(m.controlled_pi3(0,1,inverse))==Counter({'G':228,'CX':2})
# Inverse lowering reverses ORIGINAL children and recursively compiles their
# signed targets. It does not invert the much longer compiled approximation.
tree=a.seq(a.gate('G',0),a.repeat(2,a.seq(a.gate('CX',0,1),a.gate('G',1))))
fwd,ef=m.lower(tree,control=5,helper=6)
rev,er=m.lower(tree,inverse=True,control=5,helper=6)
assert ef==er==3*2+2*100
assert fwd==a.seq(m.controlled_g(5,0),a.repeat(2,a.seq(m.ccx(5,0,1,6),m.controlled_g(5,1))))
assert rev==a.seq(a.repeat(2,a.seq(m.controlled_g(5,1,True),m.ccx(5,0,1,6))),m.controlled_g(5,0,True))
assert list(a.reverse_replay(lambda: iter([1,2,3])))==[3,2,1]
n=10407050782;base=n
assert [a.copied_wire(q,base) for q in (0,1,2,2689,2690,n-1)]==[base,base+1,2,2689,base+2,base+n-2689]
# Inventory/budget: high-level counts only; no claim this stream was executed.
sched=a.a30_owner(); inventory=sched.inventory()['W_new']; g,cx=inventory['G'],inventory['CX']
budget=m.controlled_W_budget() if False else a.controlled_W_budget(m)
assert budget['G']==g*(ks['half_theta']+ks['minus_half_theta'])+cx*100*ks['pi8']
assert budget['CX']==2*g+28*cx and budget['error_units']==2*g+100*cx
assert budget['error_units'].bit_length()==11648 and 39366 < 2**16
# Inspect the first three ACTUAL mapped A30 blocks (not the whole stream).
anchor_path=A/'gcx_anchor_phase.py'
sys.path.insert(0,str(A))
spec2=importlib.util.spec_from_file_location('a38_anchor',anchor_path); anchor=importlib.util.module_from_spec(spec2);spec2.loader.exec_module(anchor)
for N in range(3,8):
    controls=range(N); flag=N; work=range(N+1,2*N-1); rebit=2*N-1; helper=2*N
    for reflection in (False,True):
        for inverse in (False,True):
            blocks=list(anchor.zero_phase_blocks(controls,flag,work,rebit,helper,inverse=inverse,reflection=reflection,macro=m))
            cnt=Counter()
            for block in blocks: cnt.update(a.counts(block))
            expected=anchor.budget(N,macro=m,reflection=reflection)
            assert cnt==Counter({'G':expected['G'],'CX':expected['CX']})
            manual=2*(2*20+(2*N-3)*100)+(16 if reflection else 12)
            assert expected['error_units']==manual
stop=base+n-2688
stream=a.controlled_W_blocks(stop,stop+1,base,macros=m)
for _ in range(3):
    assert set(a.counts(next(stream))).issubset({'G','CX'})
# Link the same lowering to the real A38 exponent certificate, without
# expanding its gigantic powers. Angle precision is independently checked by
# verify_post_angles_independent.py, not by this structure/census check.
real_cert_path=A/'POST_ANGLE_CERTIFICATE.json'
real=a.Macros(); real_budget=a.controlled_W_budget(real)
assert (real_budget['G']+real_budget['CX']).bit_length()==31725
real_stream=a.controlled_W_blocks(stop,stop+1,base,macros=real)
for _ in range(3):
    assert set(a.counts(next(real_stream))).issubset({'G','CX'})
out={'status':'PASS_EXACT_ALGEBRA_AND_DAG_FIXTURES','macro_sha256':sha256(p.read_bytes()).hexdigest(),
     'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
     'helper_scope':'all columns, including arbitrary helper superposition',
     'counts_CCX_pi8_units':100,'counts_CCX_CX':28,
     'controlled_G_error_units':2,'controlled_pi3_error_units':12,
     'controlled_W_budget_formula_checked':True,
     'controlled_W_error_units_bit_length':budget['error_units'].bit_length(),
     'single_controlled_W_error_conditional_lt':'2^-8352',
     '39366_controlled_W_total_error_conditional_lt':'2^-8336',
     'toy_reverse_order_checked':True,
     'anchor_sha256':sha256(anchor_path.read_bytes()).hexdigest(),
     'anchor_counts_and_error_units_checked_for_N_3_through_7':True,
     'first_three_actual_physical_W_blocks_lowered_and_counted':True,
     'real_certificate_sha256':sha256(real_cert_path.read_bytes()).hexdigest(),
     'first_three_actual_blocks_also_checked_with_real_exponents':True,
     'real_controlled_W_gate_count_bit_length':31725,
     'actual_giant_controlled_W_executed':False,'production_angle_precision_checked_by_this_script':False,
     'physical_C_closed':False,'GR_closed':False}
(HERE/'B75_MACRO_ALGEBRA_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'])
