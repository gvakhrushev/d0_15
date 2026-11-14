#!/usr/bin/env python3
"""Full finite positive G/CX post-SAM histories on canonical RAW births.

The production word is specified by finite lazy providers, not expanded or
run.  No implicit resets, oracles, selections or dirty-scratch claims.
"""
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
from dataclasses import dataclass
from functools import lru_cache
import hashlib,json,sys
P=Path(__file__).resolve().parent;D=P.parent
sys.path.insert(0,str(D/'round38'))
import gcx_post_macros as m
import gcx_anchor_phase as anchor
sys.path.insert(0,str(D/'round32'))
import finite_book_comparison as previous


@dataclass(frozen=True)
class Layout:
    old: int=10407050782
    sam_count: int=2688

    def __post_init__(self):
        assert self.old>=self.sam_count+3 and self.sam_count>=3

    @property
    def sam(self):return range(2,2+self.sam_count)
    @property
    def work_count(self):return self.old-self.sam_count
    @property
    def copy(self):return range(self.old,self.old+self.work_count)
    @property
    def branch(self):return self.copy.stop
    @property
    def flag(self):return self.branch+1
    @property
    def rebit(self):return self.branch+2
    @property
    def helper(self):return self.branch+3
    @property
    def scratch(self):return range(self.branch+4,self.branch+4+self.old-1)
    @property
    def total(self):return self.scratch.stop
    @property
    def clean(self):return anchor.Ranges(range(self.branch,self.branch+2),self.scratch)
    @property
    def final_wire(self):return self.scratch[-1]

    def copy_wire(self,q):
        assert type(q) is int and 0<=q<self.old
        if q in self.sam:return q
        return self.copy.start+q if q<2 else self.copy.start+q-self.sam_count

    def controls(self,kind):
        assert kind in ('good','start','chi')
        born={'good':(self.copy,), 'start':(self.sam,self.copy),'chi':(self.sam,)}[kind]
        all_ranges=born+(() if kind=='chi' else (range(self.branch,self.branch+1),))
        return anchor.Ranges(*all_ranges),anchor.Ranges(*born)

    def records(self):
        return [{'role':'original_A30_all_RAW','start':0,'stop':self.old},
                {'role':'copied_A30_WORK_RAW','start':self.copy.start,'stop':self.copy.stop},
                {'role':'LCU_branch_RAW','start':self.branch,'stop':self.branch+1},
                {'role':'comparator_flag_RAW','start':self.flag,'stop':self.flag+1},
                {'role':'phase_rebit_RAW','start':self.rebit,'stop':self.rebit+1},
                {'role':'all_column_macro_helper_RAW','start':self.helper,'stop':self.helper+1},
                {'role':'shared_comparator_scratch_RAW','start':self.scratch.start,'stop':self.scratch.stop}]


def amplifier_tokens(level,inverse=False):
    """Chronological exact target recursion; each inverse lowered separately."""
    assert type(level) is int and level>=0
    if level==0:
        if not inverse:yield ('P',False)
        yield ('beta',False);yield ('W',inverse);yield ('beta',True)
        if inverse:yield ('P',True)
        return
    if not inverse:
        yield from amplifier_tokens(level-1)
        yield ('phase','good',False,False)
        yield from amplifier_tokens(level-1,True)
        yield ('phase','start',False,False)
        yield from amplifier_tokens(level-1)
    else:
        yield from amplifier_tokens(level-1,True)
        yield ('phase','start',True,False)
        yield from amplifier_tokens(level-1)
        yield ('phase','good',True,False)
        yield from amplifier_tokens(level-1,True)


def post_tokens(level=9):
    yield ('clean',False)
    yield from amplifier_tokens(level,True)
    yield ('phase','start',False,True)
    yield from amplifier_tokens(level)
    yield ('P',True)
    yield ('phase','chi',False,True)
    yield ('clean',True)


def identity_padding(length,l):
    assert type(length) is int and (length==0 or length>=4)
    twos,fives=previous.identity_counts(length)
    a,b,c=l.branch,l.flag,l.helper
    A,B,C=m.gate('CX',a,b),m.gate('CX',b,c),m.gate('CX',a,c)
    if twos:yield m.repeat(twos,m.seq(A,A))
    if fives:yield m.seq(A,B,A,B,C)


class Assembly:
    def __init__(self,power,*,sam_index=2,level=9,layout=None,macros=None,W_factory=None,W_counts=None):
        assert type(power) is int and power>=0
        self.power,self.level=power,level
        self.l=layout or Layout();self.m=macros or m.Macros()
        assert 0<=sam_index<self.l.sam_count
        self.sam=self.l.sam[sam_index]
        self.W_factory=W_factory or m.actual_W_factory
        self.W_counts=Counter(W_counts or m.a30_owner().inventory()['W_new'])

    def rotations(self,wires,inverse=False):
        # B74 Ranges exposes finite indexed access; its sentinel is an
        # AssertionError, so Python's implicit sequence iterator is invalid.
        for i in range(len(wires)):
            q=wires[i]
            yield self.m.angle(q,'minus_theta') if inverse else m.gate('G',q)

    def controlled_W(self,inverse=False):
        blocks=m.reverse_replay(self.W_factory) if inverse else self.W_factory()
        for tree in blocks:
            result,_=self.m.lower(tree,inverse=inverse,control=self.l.branch,
                                 helper=self.l.helper,wire_map=self.l.copy_wire)
            yield result

    def phase(self,kind,inverse=False,reflection=False):
        controls,born=self.l.controls(kind)
        # B^T first, phase in the zero basis, then B; branch is already zero.
        yield from self.rotations(born,True)
        yield from anchor.zero_phase_blocks(controls,self.l.flag,self.l.scratch,
                    self.l.rebit,self.l.helper,inverse=inverse,reflection=reflection,macro=self.m)
        yield from self.rotations(born)

    def lower(self,token,omit_final_restore=False):
        kind=token[0]
        if kind=='P':
            if self.power==0:return
            leaf=self.m.angle(self.sam,'minus_theta') if token[1] else m.gate('G',self.sam)
            yield m.repeat(self.power,leaf)
        elif kind=='W':yield from self.controlled_W(token[1])
        elif kind=='beta':yield self.m.angle(self.l.branch,'minus_beta' if token[1] else 'beta')
        elif kind=='phase':yield from self.phase(*token[1:])
        else:
            assert kind=='clean'
            wires=self.l.clean
            for i in range(len(wires)):
                if omit_final_restore and token[1] and i==len(wires)-1:continue
                yield m.gate('G',wires[i]) if token[1] else self.m.angle(wires[i],'minus_theta')

    def post_blocks(self,omit_final_restore=False):
        for token in post_tokens(self.level):yield from self.lower(token,omit_final_restore)

    def token_budget(self,token):
        kind=token[0];ks=self.m.ks;km=ks['minus_theta']
        if kind=='P':return Counter(G=self.power*(km if token[1] else 1),E=self.power if token[1] else 0)
        if kind=='W':
            g,c=self.W_counts['G'],self.W_counts['CX']
            return Counter(G=g*(ks['half_theta']+ks['minus_half_theta'])+100*c*ks['pi8'],CX=2*g+28*c,E=2*g+100*c)
        if kind=='beta':return Counter(G=ks['minus_beta'] if token[1] else ks['beta'],E=1)
        if kind=='phase':
            controls,born=self.l.controls(token[1]);v=anchor.budget(len(controls),self.m,token[3]);b=len(born)
            return Counter(G=v['G']+b*(km+1),CX=v['CX'],E=v['error_units']+b)
        assert kind=='clean'
        n=len(self.l.clean)
        return Counter(G=n*(1 if token[1] else km),E=0 if token[1] else n)

    @lru_cache(None)
    def amplifier_budget(self,level,inverse=False):
        if level==0:
            return sum((self.token_budget(t) for t in amplifier_tokens(0,inverse)),Counter())
        a=self.amplifier_budget(level-1,False);b=self.amplifier_budget(level-1,True)
        phase=self.token_budget(('phase','good',inverse,False))+self.token_budget(('phase','start',inverse,False))
        return a+b+(b if inverse else a)+phase

    def post_budget(self):
        out=self.amplifier_budget(self.level,False)+self.amplifier_budget(self.level,True)
        for t in [('clean',False),('phase','start',False,True),('P',True),('phase','chi',False,True),('clean',True)]:
            out.update(self.token_budget(t))
        return out


def pair_configuration(sam_index=2):
    plus,minus=previous.powers()
    aa={name:Assembly(power,sam_index=sam_index) for name,power in [('centre',0),('plus',plus),('minus',minus)]}
    return align_family(aa)


def align_family(aa):
    assert set(aa)=={'centre','plus','minus'}
    reference=aa['plus']
    assert all(a.l==reference.l and a.W_counts==reference.W_counts and a.level==reference.level for a in aa.values())
    post={name:a.post_budget() for name,a in aa.items()}
    pre_length=max(a.power for a in aa.values())+4
    post_length=max(v['G']+v['CX'] for v in post.values())+4
    core_counts=aa['plus'].W_counts
    Lbase=pre_length+sum(core_counts.values())+post_length
    n=aa['plus'].l.total;Nbase=n+Lbase;bits=Nbase.bit_length()
    K=4*(bits+3158+1638+75+1)
    return aa,post,pre_length,post_length,Lbase,Nbase,K


def endpoint_blocks(sign,sam_index=2,configuration=None):
    aa,post,preL,postL,_,_,_=configuration or pair_configuration(sam_index)
    a=aa[sign]
    if a.power:yield m.repeat(a.power,m.gate('G',a.sam))
    yield from identity_padding(preL-a.power,a.l)
    yield from a.W_factory()
    yield from a.post_blocks(omit_final_restore=True)
    yield from identity_padding(postL-post[sign]['G']-post[sign]['CX'],a.l)


def primitive_leaves(tree):
    if tree['op']=='seq':
        for t in tree['children']:yield from primitive_leaves(t)
    elif tree['op']=='repeat':
        for _ in range(m.count_value(tree['count'])):yield from primitive_leaves(tree['child'])
    else:
        assert tree['op'] in ('G','CX');yield tree


def execution_stages(sign,sam_index=2,configuration=None):
    configuration=configuration or pair_configuration(sam_index)
    aa,_,_,_,_,_,K=configuration;a=aa[sign]
    for row in a.l.records():
        for wire in range(row['start'],row['stop']):
            yield {'kind':'canonical_RAW_birth','wire':wire,'role':row['role'],
                   'carrier_qubits_after':wire+1,'isometry':'x -> x tensor (sqrt(p),p)'}
    for block in endpoint_blocks(sign,sam_index,configuration):
        for gate in primitive_leaves(block):yield {'kind':'square_unitary_edge','gate':gate}
    for k in range(K):
        wire=a.l.total+k
        yield {'kind':'canonical_RAW_birth','wire':wire,'role':'late_retention','carrier_qubits_after':wire+1}
        yield {'kind':'square_unitary_edge','gate':m.gate('G',wire)}
    yield {'kind':'final_unitary_g','gate':m.gate('G',a.l.final_wire)}


def encode(v):
    v=F(v);return {'numerator_hex':hex(v.numerator),'denominator_hex':hex(v.denominator)}


def build():
    aa,post,preL,postL,Lbase,Nbase,K=pair_configuration();a=aa['plus'];l=a.l
    assert l.total==31221149661 and len(l.clean)==10407050783
    native=max(v['E'] for v in post.values())*F(1,1<<20000)
    assert native<F(1,1<<8329)
    sigma=F(1,1<<3014);fp=F(1,1<<6560)
    vector=5*sigma*sigma+4*fp+native
    assert vector<F(1,1<<6024)
    z,t,gs=F(1,1<<20),F(1,1<<1618),F(1,1<<3158)
    native_feedback=vector*vector/(2*t*gs)
    post_feedback=vector/gs
    assert native_feedback<F(1,1<<7273) and post_feedback<F(1,1<<2866)
    qbracket=8/(1-z)+24*z/(1-z)**2+16*z*z/(1-z)**3
    taylor=t*t*qbracket/(16*gs)
    angular=F(1,1<<4852)/(t*gs)
    gamma_lower=F(8,3)*z*gs
    heat=F(6*Nbase,359)/(t*gamma_lower)*F(1,1<<(K//4))
    assert F(5,6)**4<F(1,2) and heat<F(1,1<<76)
    total=native_feedback+taylor+angular+heat
    assert total<F(1,1<<74) and 55*total<F(1,1<<68)
    corrected=55*total
    cov_lower=F(1,1<<46)-corrected
    cov_upper=F(1,1<<16)+corrected
    geom_error=F(1,1<<15)+corrected
    assert cov_lower>F(1,1<<47) and cov_upper<F(1,1<<15) and geom_error<F(1,1<<14)
    counts={}
    for name,budget in post.items():
        postpad=postL-budget['G']-budget['CX'];prepad=preL-aa[name].power
        assert postpad>=4 and prepad>=4
        count=Counter(a.W_counts)
        count.update({'G':aa[name].power+budget['G']+K,'CX':budget['CX']+prepad+postpad})
        assert sum(count.values())==Lbase+K
        counts[name]={k:hex(v) for k,v in count.items()}
    source=m.a30_owner();cplan=source.build()
    marks=l.total+preL+int(cplan['joint_RAW_source_checkpoint_native_prefix_calls'])
    pins=[Path(__file__),D/'round38/gcx_post_macros.py',D/'round38/gcx_anchor_phase.py',
          D/'round38/POST_ANGLE_CERTIFICATE.json',D/'round38/GCX_POST_MACROS_CHECK.json',
          D/'round37/POST_SAM_REDUCTION_PLAN.json',D/'round32/finite_book_comparison.py',
          D/'round30/COMMON_SOURCE_MARKED_PLAN.json',anchor.B,
          anchor.B.parent/'B74_NATIVE_POST_SAM_AMPLIFICATION_RU.md',
          anchor.B.parent.parent/'round76/B76_UNIFORM_REBIT_CLEAN_SECTOR_RU.md',
          anchor.B.parent.parent/'round76/B76_SCOPE_CHECK.json',
          previous.core.g.B/'round63/SUFFICIENT_ENDPOINT_G_CERTIFICATE.json',
          D.parents[1]/'d0_retained_response_concentration_2026-10-28/RAW_CYLINDER_REALIZATION_RU.md']
    return {'status':'EXPLICIT_FINITE_POST_SAM_NATIVE_PAIR_WITH_FULL_GROWING_CLOCK_BOUNDS',
            'initial_history':{'H0':'C','Omega0':1,'P0':'I_1','prior_stages':0},
            'exact_input_native_centre_included':True,
            'centre_P':'empty rotation word with paid exact identity padding; no free identity stage',
            'native_alphabet':['G','CX'],'post_target':'R_chi P^T R_h_a; occupied-vector alternative, not all-column A37 Ustar',
            'post_chronology':'paid born-to-zero; A9^T; R_start; A9; P^T; R_chi; paid zero-to-born',
            'shared_comparator_clean_sector_invariant_for_exact_targets':True,
            'approximate_backward_words_equal_forward_adjoints_claimed':False,
            'phase_rebit_uniformity_required_and_owned_by_B76':True,
            'birth_layout':l.records(),'early_births':l.total,'late_retention_pairs':K,
            'all_births_included_in_clock_and_heat':True,'post_never_addresses_original_WORK':True,
            'fixed_point_levels':9,'controlled_W_calls_in_post':39366,
            'P_powers_hex':{n:hex(x.power) for n,x in aa.items()},
            'post_counts_and_error_units_hex':{n:{k:hex(v) for k,v in c.items()} for n,c in post.items()},
            'equalized_pre_call_count_hex':hex(preL),'equalized_post_call_count_hex':hex(postL),
            'actual_gate_counts_with_retention_hex':counts,'Lbase_hex':hex(Lbase),'Nbase_hex':hex(Nbase),
            'Nbase_bit_length':Nbase.bit_length(),'actual_clock_layers_N_hex':hex(Nbase+2*K),
            'clock_dimension':'2^n*(Lbase-3+4*2^K)-1','final_dimension':'2^(n+K)',
            'final_actual_g':{'op':'G','wire':l.final_wire},
            'original_RAW_checkpoint_layer_hex':hex(marks),
            'original_checkpoint_effects':'same A30 effects tensor I_new; common layer, same actual pre P source geometry',
            'retained_cold_return':'p^(K/2) c_hat(P)',
            'feedback':'-log(1-z+z*p^K*c_hat(P)^2)',
            'all_mode_heat':'beta^-1 log[359D+2 Tr_(33D) exp(-beta Delta0(T))]; beta=2p^2',
            'comparison_gain':'Gamma_red=4*z*p^K*c_ref*g*s/(1-z+z*p^K*q_center), inherited A37',
            'bounds':{k:encode(v) for k,v in {'post_native_error':native,'full_post_vector_error':vector,
                       'post_feedback_unit_skew_row':post_feedback,'native_feedback_fd_error':native_feedback,
                       'analytic_fd_truncation':taylor,'incoming_angle_fd_error':angular,
                       'all_mode_heat_fd_error':heat,'complete_finite_comparison_error':total,
                       'corrected_2688_error':corrected,'specified_covector_norm_lower':cov_lower,
                       'specified_covector_norm_upper':cov_upper,'specified_covector_geometric_error':geom_error}.items()},
            'post_vector_error_strict_lt':'2^-6024','post_feedback_unit_skew_row_strict_lt':'2^-2866',
            'full_price_reduced_feedback_fd_error_strict_lt':'2^-74',
            'corrected_2688_fd_error_strict_lt':'2^-68',
            'specified_2688_finite_covector_norm_interval':['2^-47','2^-15'],
            'specified_covector_to_actual_mean_geometric_source_strict_lt':'2^-14',
            'geometric_comparison_scope':'consumes A37/A31 fixed h=1/4 chart only; not all independent native rows or refinement',
            'finite_comparison_scope':'paired co-moving P and U_alt(P), actual full H+J endpoints; not fixed-U incoming derivative',
            'full_heat_independent_post_stationarity_proved':False,
            'same_complete_original_task_membership_proved':False,'full_joint_SAM_terminal_output_preserved':False,
            'Cost_Info_binding_proved':False,'native_smooth_family_or_refinement_proved':False,
            'production_word_expanded_or_run':False,'absolute_huge_heat_trace_evaluated':False,
            'physical_C_closed':False,'GR_closed':False,
            'source_sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in pins}}


if __name__=='__main__':
    out=build();(P/'POST_SAM_ASSEMBLY_PLAN.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('status','early_births','late_retention_pairs','Nbase_bit_length',
          'post_vector_error_strict_lt','full_price_reduced_feedback_fd_error_strict_lt')}))
