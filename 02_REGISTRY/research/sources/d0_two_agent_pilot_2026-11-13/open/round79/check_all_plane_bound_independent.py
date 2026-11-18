#!/usr/bin/env python3
"""Independent exact small plane simulation, full clock and A40 bounds."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from hashlib import sha256
from itertools import combinations
import importlib.util,json,sys
import sympy as s
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
owner=D/'round40/independent_post_planes.py';pfile=D/'round40/INDEPENDENT_POST_PLANES_PLAN.json'
spec=importlib.util.spec_from_file_location('b79_owner',owner);a=importlib.util.module_from_spec(spec);sys.modules[spec.name]=a;spec.loader.exec_module(a)
plan=json.loads(pfile.read_text());assert all(sha256(Path(p).read_bytes()).hexdigest()==h for p,h in plan['source_sha256'].items())
m=a.m;old=a.old
ks={'pi8':1,'pi6':2,'half_theta':3,'minus_half_theta':4,'minus_theta':5,'beta':6,'minus_beta':7}
cert={'status':'PASS_SEVEN_CERTIFIED_POSITIVE_G_POWERS','error_bits':20000,
      'rotations':{name:{'exponent_hex':hex(v)} for name,v in ks.items()}}
mac=m.Macros(cert);layout=old.Layout(old=10,sam_count=4)
wtree=[m.seq(m.gate('G',2),m.gate('CX',0,6))];wc=Counter()
for tr in wtree:wc.update(m.counts(tr))
assembly=old.Assembly(0,sam_index=0,level=0,layout=layout,macros=mac,
                      W_factory=lambda:iter(wtree),W_counts=wc)

def apply(reg,ops):
    for op,*w in ops:
        if op=='X':reg^=1<<w[0]
        elif op=='CX':
            if reg>>w[0]&1:reg^=1<<w[1]
        else:
            assert op=='CCX'
            if reg>>w[0]&1 and reg>>w[1]&1:reg^=1<<w[2]
    return reg

def logical_plane_column(plane,index,sign):
    # Logical sequence before/after the controlled rotation, including the
    # exact emitted zero-test and literal reversal. Scratch starts at zero.
    data=sum(((index>>j)&1)<<plane.l.sam[j] for j in range(plane.size))
    aff=list(plane.affine());rev=list(plane.affine(True))
    test=list(a.anchor.b.zero_predicate_ir(plane.controls,plane.l.flag,plane.work))
    test_inv=list(a.anchor.b.zero_predicate_ir(plane.controls,plane.l.flag,plane.work,True))
    mid=apply(apply(data,aff),test)
    active=(mid>>plane.l.flag)&1;bit=(mid>>plane.target)&1
    branches=[(mid,F(1))] if not active else [(mid,F(3,5)),(mid^(1<<plane.target),F(4,5)*sign*(1 if bit==0 else -1))]
    out={}
    for state,coeff in branches:
        state=apply(apply(state,test_inv),rev)
        idx=sum(((state>>plane.l.sam[j])&1)<<j for j in range(plane.size))
        assert state==sum(((idx>>j)&1)<<plane.l.sam[j] for j in range(plane.size))
        out[idx]=out.get(idx,F())+coeff
    return {k:v for k,v in out.items() if v}

for left,right in combinations(range(16),2):
    plane=a.Plane(left,right,2,assembly)
    # The actual affine mapping sends left to zero and right to pivot.
    aff=list(plane.affine())
    def samreg(i):return sum(((i>>j)&1)<<layout.sam[j] for j in range(4))
    assert apply(samreg(left),aff)==0
    assert apply(samreg(right),aff)==1<<plane.target
    for x in range(16):
        for sign in (-1,1):
            got=logical_plane_column(plane,x,sign)
            if x==left: want={left:F(3,5),right:sign*F(4,5)}
            elif x==right:want={right:F(3,5),left:-sign*F(4,5)}
            else:want={x:F(1)}
            assert got==want,(left,right,x,sign,got,want)
    for inverse in (False,True):
        counts=Counter()
        for block in plane.blocks(inverse):
            counts.update(m.counts(block))
            for leaf in old.primitive_leaves(block):
                assert all(q in layout.sam or q==layout.flag or q==layout.helper or q in plane.work for q in leaf['wires'])
                assert layout.scratch[-1] not in leaf['wires']
        budget=plane.budget()
        assert counts==Counter({key:budget[key] for key in ('G','CX')})
        # Independently tally error units from the actual logical IR.
        affcounts=Counter(op[0] for op in plane.affine())
        predcounts=Counter(op[0] for op in a.anchor.b.zero_predicate_ir(plane.controls,layout.flag,plane.work))
        expected=2*plane.power+len(plane.borrowed)+2*(20*affcounts['X']+20*predcounts['X']+100*predcounts['CCX'])
        assert expected==budget['E']

# Identical positive exponent n: exact ideal n*theta and -n*theta are
# inverses even if the negative native macro itself is only approximated.
n=s.symbols('n',integer=True,positive=True);x=s.symbols('x',real=True)
R=s.Matrix([[s.cos(n*x),-s.sin(n*x)],[s.sin(n*x),s.cos(n*x)]])
assert s.simplify(R.T*R)==s.eye(2)
# Exact plane displacement ||Rv-v||²=2(1-cos angle)*(v_a²+v_b²).
c,h,A,B=s.symbols('c h A B',real=True)
rot=s.Matrix([[c,-h],[h,c]]);v=s.Matrix([A,B])
displ=s.expand(((rot-s.eye(2))*v).dot((rot-s.eye(2))*v))
assert s.factor(displ-2*(1-c)*(A*A+B*B))==(A*A+B*B)*(c*c+h*h-1)

# Weight identity and nuclear bridge, with nonuniform product chi and all
# off-diagonal matrix entries explicitly represented, not only local axes.
base=[F(3,5),F(4,5)];chi=[]
for x in range(16):
    value=F(1)
    for k in range(4):value*=base[(x>>k)&1]
    chi.append(value)
assert sum(v*v for v in chi)==1
assert sum(chi[i]**2+chi[j]**2 for i,j in combinations(range(16),2))==15
rows=s.symbols('r0:6');mat=s.zeros(4)
for row,(i,j) in zip(rows,combinations(range(4),2)):
    X=s.zeros(4);X[j,i]=1;X[i,j]=-1;mat+=row*X/2
assert s.expand(s.trace(mat.T*mat)-sum(r*r for r in rows)/2)==0

# Full clock on a toy family, using SAME implementation for centre and ±.
toy={name:old.Assembly(power,sam_index=0,level=0,layout=layout,macros=mac,
      W_factory=lambda:iter(wtree),W_counts=wc)
      for name,power in (('centre',0),('plus',2),('minus',3))}
baseconf=tuple(old.align_family(toy)); cfg=a.configuration(baseconf,power=2); cfg['K']=3
for i,j in ((0,1),(1,14),(6,9)):
    for sign in ('centre','plus','minus'):
        dim=1;clock_D=0;N=0;last=None;counts=Counter()
        for stage in a.execution_stages(i,j,sign,cfg):
            N+=1;clock_D+=dim;last=stage
            if stage['kind']=='canonical_RAW_birth':dim*=2
            else:counts[stage['gate']['op']]+=1
        assert N==cfg['Nbase']+2*cfg['K']
        assert clock_D==(1<<layout.total)*(cfg['Lbase']-3+4*(1<<cfg['K']))-1
        assert dim==1<<(layout.total+cfg['K'])
        assert sum(counts.values())==cfg['Lbase']+cfg['K']
        assert last=={'kind':'final_unitary_g','gate':m.gate('G',layout.scratch[-1])}

# Full A39 centre prefix is used literally, not A39 ±. Compare tokens for
# representative exact address pairs on first streaming blocks.
cfg=a.configuration(); assert cfg['Nbase'].bit_length()==31740 and cfg['K']==162576
assert cfg['dimension_debt']==4032 and cfg['base_config'][0]['centre'].power==0
assert len(assembly.l.scratch)>len(a.Plane(0,1,2,assembly).work)
centre=cfg['base_config'][0]['centre']; assert centre.l.total==31221149661
assert plan['last_actual_g']=={'op':'G','wire':centre.l.final_wire}
assert plan['all_planes_and_signs_common_clock_and_eta'] is True
assert plan['original_A30_RAW_checkpoint_layer_hex']==json.loads((D/'round39/POST_SAM_ASSEMBLY_PLAN.json').read_text())['original_RAW_checkpoint_layer_hex']
assert cfg['probeL']==cfg['upper']['G']+cfg['upper']['CX']+4
assert cfg['Lbase']==cfg['base_config'][4]+cfg['probeL']
assert cfg['Nbase']==centre.l.total+cfg['Lbase']
assert cfg['K']==4*(cfg['Nbase'].bit_length()+3158+1638+75+1+4032)
assert int(plan['new_Lbase_hex'],16)==cfg['Lbase']
assert int(plan['new_Nbase_hex'],16)==cfg['Nbase']
assert int(plan['actual_clock_layers_N_hex'],16)==cfg['Nbase']+2*cfg['K']
# Traverse the actual compact production DAG stream for two opposite bit
# patterns, without expanding any G power or the underlying A39/W stream.
for left,right in ((0,1),((1<<2688)-2,(1<<2688)-1)):
    actual_plane=a.Plane(left,right,cfg['power'],centre)
    for inverse in (False,True):
        counts=Counter()
        for node in actual_plane.blocks(inverse):counts.update(m.counts(node))
        expected=actual_plane.budget()
        assert counts==Counter({k:expected[k] for k in ('G','CX')})
        assert sum(counts.values())<=cfg['probeL']-4

# Exact recomputation of all numerical error and all-plane dual bounds.
def dec(v):return F(int(v['numerator_hex'],16),int(v['denominator_hex'],16))
bounds={k:dec(v) for k,v in plan['bounds'].items()}
baseplan=json.loads((D/'round39/POST_SAM_ASSEMBLY_PLAN.json').read_text())
e0=dec(baseplan['bounds']['full_post_vector_error']);mu=F(cfg['upper']['E'],2**20000);delta=e0+mu
assert bounds['probe_native_error']==mu and bounds['combined_vector_error']==delta
assert mu<F(1,2**15120) and delta<F(1,2**6023)
t=F(1,2**1618);gs=F(1,2**3158);z=F(1,2**20);half=(centre.l.sam_count+1)//2
J_l2=(1<<(half+1))*delta/gs+(1<<centre.l.sam_count)*delta**2/(2*t*gs)
J_dual=(1<<half)*J_l2
heatrow=F(6*cfg['Nbase'],359)/(t*(F(8,3)*z*gs))*F(1,2**(cfg['K']//4))
heatdual=(1<<cfg['dimension_debt'])*heatrow
assert bounds['feedback_all_row_l2']==J_l2 and bounds['feedback_full_covector_dual']==J_dual
assert bounds['heat_each_row']==heatrow and bounds['heat_full_covector_dual']==heatdual
assert bounds['full_H_plus_J_finite_covector_dual']==J_dual+heatdual<F(1,2**75)
assert J_dual<F(1,2**175) and heatdual<F(1,2**76)

out={'status':'PASS_INDEPENDENT_ALL_PLANE_FINITE_AUDIT',
     'owner_sha256':sha256(owner.read_bytes()).hexdigest(),'plan_sha256':sha256(pfile.read_bytes()).hexdigest(),
     'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
     'size4_all_120_planes_all_columns_both_directions_checked':True,
     'logical_zero_test_and_dirty_private_contract':'clean borrowed input, full-vector error retained',
     'same_exponent_plus_minus_exact_target_inverse':True,
     'actual_probe_dag_counts_error_units_verified':True,
     'nonlocal_plane_weight_and_skew_frobenius_identities_checked':True,
     'nine_toy_full_clock_histories_checked':True,
     'source_hashes_and_all_exact_bounds_checked':True,
     'two_production_plane_compact_DAG_streams_counted_both_signs':True,
     'same_common_K':cfg['K'],'retained_L':cfg['Lbase'].bit_length(),
     'K_equal_eta_and_common_last_g':True,
     'original_H1_membership_or_fixed_FN_proved':False,
     'native_smooth_variations_stationarity_proved':False,'giant_production_words_executed':False,
     'physical_C_closed':False,'GR_closed':False}
(P/'B79_ALL_PLANE_AUDIT.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'])
