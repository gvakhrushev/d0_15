#!/usr/bin/env python3
"""All outgoing real SAM planes at FIXED A39 native centre and preparation.

Finite indexed G/CX providers for every a<b; no enumeration of 2^(2m)
planes. Signed probes share one exact original positive-G target exponent.
"""
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
import hashlib,json,sys
P=Path(__file__).resolve().parent;D=P.parent
sys.path.insert(0,str(D/'round39'))
import post_sam_assembly as old
m,anchor=old.m,old.anchor


def popcount(n):return bin(n).count('1')


class Plane:
    def __init__(self,a,b,power,assembly):
        self.base=assembly;self.l=assembly.l;self.mac=assembly.m
        self.size=self.l.sam_count
        assert self.size>=4 and 0<=a<b<(1<<self.size)
        assert type(power) is int and power>0
        self.a,self.b,self.power=a,b,power
        difference=a^b;self.pivot=(difference&-difference).bit_length()-1
        self.target=self.l.sam[self.pivot]
        self.controls=anchor.Ranges(range(self.l.sam.start,self.target),range(self.target+1,self.l.sam.stop))
        self.work=range(self.l.scratch.start,self.l.scratch.start+self.size-3)
        self.borrowed=anchor.Ranges(range(self.l.flag,self.l.flag+1),self.work)
        assert self.work.stop<self.l.scratch.stop
        assert len(self.controls)==self.size-1 and len(self.borrowed)==self.size-2

    def affine(self,inverse=False):
        # First translate a to zero, then send a xor b to the pivot vector.
        ops=[('X',self.l.sam[j]) for j in range(self.size) if (self.a>>j)&1]
        ops += [('CX',self.target,self.l.sam[j]) for j in range(self.size)
                if j!=self.pivot and ((self.a^self.b)>>j)&1]
        yield from (reversed(ops) if inverse else ops)

    def native_ir(self,op):
        return anchor.logical_native(op,self.l.helper,self.mac)

    def blocks(self,inverse=False):
        yield from self.base.rotations(self.borrowed,True)
        for op in self.affine():yield self.native_ir(op)
        for op in anchor.b.zero_predicate_ir(self.controls,self.l.flag,self.work):yield self.native_ir(op)
        # Repeat independently compiled controlled G or G^T, NOT the adjoint
        # of the newly lengthened approximate forward macro.
        yield m.repeat(self.power,self.mac.controlled_g(self.l.flag,self.target,inverse))
        for op in anchor.b.zero_predicate_ir(self.controls,self.l.flag,self.work,reverse=True):yield self.native_ir(op)
        for op in self.affine(True):yield self.native_ir(op)
        yield from self.base.rotations(self.borrowed)

    def budget(self):
        return budget(self.size,self.power,popcount(self.a),popcount(self.a^self.b),self.mac)


def budget(size,power,ones_a,ones_difference,mac):
    assert size>=4 and 0<=ones_a<=size and 1<=ones_difference<=size and power>0
    k=mac.ks
    return Counter(G=power*(k['half_theta']+k['minus_half_theta'])+(size-2)*(k['minus_theta']+1)
                     +(40*ones_a+400*size-920)*k['pi8'],
                   CX=2*power+4*ones_a+2*ones_difference+116*size-280,
                   E=2*power+401*size-922+40*ones_a)


def configuration(base_config=None,power=None):
    base_config=base_config or old.pair_configuration()
    aa,post,preL,postL,Lbase,Nbase,Kold=base_config
    centre=aa['centre'];size=centre.l.sam_count
    power=old.previous.powers()[0] if power is None else power
    upper=budget(size,power,size,size,centre.m)
    probeL=upper['G']+upper['CX']+4
    newL=Lbase+probeL;newN=centre.l.total+newL
    half=(size+1)//2;dimension_debt=size+half
    K=4*(newN.bit_length()+3158+1638+75+1+dimension_debt)
    return {'base_config':base_config,'power':power,'upper':upper,'probeL':probeL,
            'Lbase':newL,'Nbase':newN,'K':K,'dimension_debt':dimension_debt}


def before_final_blocks(a,b,sign,config=None):
    assert sign in ('centre','plus','minus')
    cfg=config or configuration();base=cfg['base_config'];centre=base[0]['centre']
    plane=Plane(a,b,cfg['power'],centre)
    yield from old.endpoint_blocks('centre',configuration=base)
    length=0
    if sign!='centre':
        yield from plane.blocks(inverse=sign=='minus')
        c=plane.budget();length=c['G']+c['CX']
    yield from old.identity_padding(cfg['probeL']-length,centre.l)


def execution_stages(a,b,sign,config=None):
    cfg=config or configuration();centre=cfg['base_config'][0]['centre'];l=centre.l
    for row in l.records():
        for q in range(row['start'],row['stop']):
            yield {'kind':'canonical_RAW_birth','wire':q,'role':row['role'],'carrier_qubits_after':q+1}
    for block in before_final_blocks(a,b,sign,cfg):
        for gate in old.primitive_leaves(block):yield {'kind':'square_unitary_edge','gate':gate}
    for k in range(cfg['K']):
        q=l.total+k
        yield {'kind':'canonical_RAW_birth','wire':q,'role':'late_retention','carrier_qubits_after':q+1}
        yield {'kind':'square_unitary_edge','gate':m.gate('G',q)}
    yield {'kind':'final_unitary_g','gate':m.gate('G',l.final_wire)}


def decode(v):return F(int(v['numerator_hex'],16),int(v['denominator_hex'],16))


def build():
    cfg=configuration();centre=cfg['base_config'][0]['centre'];l=centre.l;size=l.sam_count
    prior=json.loads((D/'round39/POST_SAM_ASSEMBLY_PLAN.json').read_text())
    e0=decode(prior['bounds']['full_post_vector_error'])
    mu=F(cfg['upper']['E'],1<<20000)
    delta=e0+mu
    assert mu<F(1,1<<15120) and delta<F(1,1<<6023)
    z,t,gs=F(1,1<<20),F(1,1<<1618),F(1,1<<3158)
    angle=F(1,1<<4852)
    assert angle<t # ||G^n-I||<=t+angle<2t; inverse target uses SAME n.
    half=(size+1)//2;debt=size+half
    # Row bound: 2 sqrt(w_ab) delta/gs + delta^2/(2tgs).
    # Sum w_ab=d-1 and number of planes<d^2. The trace-norm bound below
    # includes sqrt(d) times the entire Euclidean finite-row norm.
    J_l2=(1<<(half+1))*delta/gs+(1<<size)*delta*delta/(2*t*gs)
    J_dual=(1<<half)*J_l2
    assert J_dual<F(1,1<<175)
    gamma=F(8,3)*z*gs
    heat_row=F(6*cfg['Nbase'],359)/(t*gamma)*F(1,1<<(cfg['K']//4))
    heat_dual=(1<<debt)*heat_row
    assert heat_row<F(1,1<<(debt+76)) and heat_dual<F(1,1<<76)
    total=J_dual+heat_dual
    assert total<F(1,1<<75)
    assert cfg['Nbase'].bit_length()==31740 and cfg['K']==162576
    assert cfg['dimension_debt']==4032
    p=Plane(0,1,cfg['power'],centre);cb=p.budget()
    oldcounts=Counter({k:int(v,16) for k,v in prior['actual_gate_counts_with_retention_hex']['centre'].items()})
    oldcounts['G']-=prior['late_retention_pairs']
    counts={}
    for sign in ('centre','plus','minus'):
        probe=Counter() if sign=='centre' else cb
        c=Counter(oldcounts)
        c.update({'G':probe['G']+cfg['K'],'CX':probe['CX']+cfg['probeL']-probe['G']-probe['CX']})
        assert sum(c.values())==cfg['Lbase']+cfg['K']
        counts[sign]={k:hex(v) for k,v in c.items()}
    pins=[Path(__file__),D/'round39/post_sam_assembly.py',D/'round39/POST_SAM_ASSEMBLY_PLAN.json',
          D/'round39/POST_SAM_ASSEMBLY_CHECK.json',D/'round38/POST_ANGLE_CERTIFICATE.json',
          D/'round38/gcx_post_macros.py',anchor.B,
          old.previous.core.g.B/'round63/SUFFICIENT_ENDPOINT_G_CERTIFICATE.json',
          old.previous.core.g.B/'round76/B76_UNIFORM_REBIT_CLEAN_SECTOR_RU.md',
          D.parents[1]/'d0_retained_response_concentration_2026-10-28/RAW_CYLINDER_REALIZATION_RU.md']
    return {'status':'EXPLICIT_INDEPENDENT_ALL_SAM_PLANE_FULL_PRICE_FINITE_COVECTOR_BOUND',
            'phase':'native realization and independent source completion on one fixed finite carrier',
            'fixed_upstream':'A39 exact-input native centre, entire original preparation/core/post fixed',
            'SAM_bits':size,'SAM_real_dimension':'d=2^2688','indexed_planes':'0<=a<b<d',
            'number_of_independent_plane_rows':'d*(d-1)/2',
            'basis':'X_ab=|b><a|-|a><b|; operator norm1, Frobenius norm sqrt(2)',
            'positive_original_G_exponent_hex':hex(cfg['power']),
            'minus_target_exact_inverse_of_plus_target':True,
            'minus_compiled_word_exact_adjoint_claimed':False,
            'same_n_avoids_asymmetric_angle_error':True,
            'no_extra_births':True,'borrowed_born_to_zero_bits':size-2,
            'borrowed_bits_restored_with_full_vector_error':True,
            'post_probe_never_addresses_original_WORK_or_deferred_last_G':True,
            'probe_upper_counts_and_error_units_hex':{k:hex(v) for k,v in cfg['upper'].items()},
            'probe_common_call_length_hex':hex(cfg['probeL']),
            'new_Lbase_hex':hex(cfg['Lbase']),'new_Nbase_hex':hex(cfg['Nbase']),
            'Nbase_bit_length':cfg['Nbase'].bit_length(),'early_births':l.total,
            'late_retention_pairs':cfg['K'],'dimension_debt_bits':debt,
            'actual_clock_layers_N_hex':hex(cfg['Nbase']+2*cfg['K']),
            'clock_dimension':'2^n*(Lbase-3+4*2^K)-1','final_dimension':'2^(n+K)',
            'last_actual_g':{'op':'G','wire':l.final_wire},
            'example_plane_0_1_complete_counts_with_retention_hex':counts,
            'all_planes_and_signs_common_clock_and_eta':True,
            'all_original_RAW_marks_and_complete_prefix_before_probe_equal':True,
            'original_A30_RAW_checkpoint_layer_hex':prior['original_RAW_checkpoint_layer_hex'],
            'gain':'Gamma_red=4zp^K c_ref gs/(1-z+zp^K q_centre), new common K',
            'weight_identity':'w_ab=chi_a^2+chi_b^2; sum_{a<b}w_ab=d-1',
            'uniform_feedback_row_bound':'2 sqrt(w_ab) delta/(gs)+delta^2/(2tgs)',
            'full_finite_covector_dual_bound_definition':'A=1/2 sum row_ab X_ab; |Tr A^T X|<=||A||_*||X||op<=sqrt(d)||rows||2||X||op',
            'bounds':{k:old.encode(v) for k,v in {'probe_native_error':mu,'combined_vector_error':delta,
                        'feedback_all_row_l2':J_l2,'feedback_full_covector_dual':J_dual,
                        'heat_each_row':heat_row,'heat_full_covector_dual':heat_dual,
                        'full_H_plus_J_finite_covector_dual':total}.items()},
            'feedback_full_covector_dual_strict_lt':'2^-175',
            'heat_full_covector_dual_strict_lt':'2^-76',
            'full_H_plus_J_finite_covector_dual_strict_lt':'2^-75',
            'norm_scope':'linear functional formed from declared Givens-plane finite contrasts, dual of SAM skew operator norm; all d(d-1)/2 rows included',
            'not_claimed':'exact stationarity, arbitrary finite rotations, native smooth derivative, old-WORK/source/reader/scene variations, task admission, Cost-Info selection or refinement',
            'giant_production_words_or_all_planes_materialized':False,
            'physical_C_closed':False,'GR_closed':False,
            'source_sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in pins}}


if __name__=='__main__':
    out=build();(P/'INDEPENDENT_POST_PLANES_PLAN.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('status','SAM_bits','early_births','late_retention_pairs',
          'full_H_plus_J_finite_covector_dual_strict_lt')}))
