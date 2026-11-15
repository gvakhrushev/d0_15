#!/usr/bin/env python3
"""Field-bound A49 paid family; consumes a separate GlobalSource.

The source argument must be the NEW parameterized source object.  Its
upper/error values and CODE-control-only theorem are explicit caller-owned
premises; this module cannot prove physical admission or field stationarity.
"""
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
import sys
sys.dont_write_bytecode=True
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
sys.path.insert(0,str(D/'round49'))
import two_bit_paid_family as paid

def source_positive_margin(error):
    """Conditional on B91 ||DB||<=1748 and base Mideal_b>67/100."""
    if type(error) is not F or error<0 or error>=F(1,1<<3421):
        raise ValueError('need certified canonical core error <2^-3421')
    drift=F(2*1748*52,1<<32)
    lower=F(67,100)-drift-error
    assert lower>F(669,1000)>F(2,3)
    return {'base_gt':F(67,100),'source_drift_lt':drift,
            'actual_diagonal_lower_gt':lower,'simple_uniform_lower':F(669,1000)}

def configuration(api,uniform_core_upper):
    """Use a caller-certified common upper for all requested fields.

    No claim is made that one field's inventory is already uniform.
    Upper must bound the provided source's actual core count; exact padded
    length belongs to the NEW paid family, not to the unpadded source.
    """
    n=sum(x['stop']-x['start'] for x in api.birth_blocks())
    sam=tuple(api.physical_wire(q) for q in api.namespace()['layout']['SAM'])
    old_sam=tuple(paid.source.physical_wire(q) for q in paid.source.namespace()['layout']['SAM'])
    m=len(sam)
    if n!=11893774624 or m!=5376 or sam!=old_sam:
        raise ValueError('A47 controls require the unchanged A48 wire/birth binding')
    u=api.upper_inventory_and_error()
    actual=Counter(u['W_G_CX_upper']);common=Counter(uniform_core_upper)
    if any(type(v) is not int or v<0 for v in common.values()):raise ValueError('invalid upper')
    if any(actual[k]>common[k] for k in actual):raise ValueError('supplied common upper is too small')
    if set(actual)-{'G','CX'} or set(common)-{'G','CX'}:raise ValueError('expected G/CX upper')
    margin=source_positive_margin(u['full_canonical_compressed_error'])
    _,q,_=paid.target.a41.uniform_grid();k8=paid.native.Macros().ks['pi8']
    if k8>q:raise ValueError('post grid upper is invalid')
    stars=4*((1<<m)-1);L=1<<(m-1)
    post=Counter(G=stars*L*q,CX=4*(((1<<m)-1)*(m-1)*L+2*(m*L-(1<<m)+1)))
    probe=paid.old.plane_upper(m,q,k8)
    coreL=sum(common.values())+4;postL=sum(post.values())+4;probeL=sum(probe.values())+4
    controlL=int(paid.control.control_plan()['each_padded_control_calls_hex'],16)+4
    base=coreL+postL+probeL+4*controlL;Nbase=n+base;debt=m+(m+1)//2
    K=4*(Nbase.bit_length()+3208+1700+20+75+1+debt)
    return {'n':n,'sam':sam,'m':m,'coreL':coreL,'controlL':controlL,
            'postL':postL,'probeL':probeL,'Lbase':base,'Nbase':Nbase,'K':K,
            'dimension_debt':debt,'core_upper':common,'post_upper':post,
            'probe_upper':probe,'q':q,'k8':k8,'positive_margin':margin,
            'post_error':F(stars*L,1<<20000)}

class RegularPaidFamily:
    def __init__(self,api,field,uniform_core_upper):
        # Each instance owns its field-bound source and its actual M(Y).
        # No global cache keyed only by the old A48 source can be reused.
        self.api=api
        self.source=api.GlobalSource(field)
        self.field_object=self.source.field
        self.field_packet=self.field_object.encode()
        self.cfg=configuration(api,uniform_core_upper)
        self._target=None

    def _guard(self):
        if self.source.field is not self.field_object:
            raise RuntimeError('source field changed after binding')
        sources=getattr(self.source,'sources',None)
        if sources is not None:
            if sources.field is not self.field_object:
                raise RuntimeError('nested source field changed after binding')
            components=getattr(sources,'components',None)
            if components is not None and components.field is not self.field_object:
                raise RuntimeError('component field changed after binding')

    def actual_core_target(self):
        self._guard()
        if self._target is None:
            self._target=paid.target.ActualDiagonal(self.cfg['n'],self.cfg['sam'],self.source.core_blocks)
        return self._target

    def actual_post_blocks(self):
        self._guard()
        yield from paid.target.post_blocks(self.actual_core_target())

    def actual_probe_blocks(self,plane,sign):
        self._guard()
        if sign not in (-1,1):raise ValueError('post probe needs signed endpoint')
        yield from paid.old.plane_blocks(*plane,paid.probe_power(sign,self.cfg['m']),
                                         self.cfg['sam'],paid.native.Macros())

    def blocks(self,*,arm='centre',sign=0,axis=0,plane=None,keep_marks=False):
        self._guard()
        yield from paid.family_blocks(self.cfg,self.source.compiled_core_with_cuts,
                 self.actual_post_blocks,paid.raw_control_factory,self.actual_probe_blocks,
                 arm=arm,sign=sign,axis=axis,plane=plane,keep_marks=keep_marks)

    def execution_stages(self,**label):
        self._guard()
        yield from paid.execution_stages(self.cfg,lambda:self.blocks(**label))

    def bounds(self):
        """Algebraic uniform post/heat envelopes, conditional on source proof."""
        self._guard();cfg=self.cfg
        step=F(1,1<<1700);gs=F(1,1<<3208);z=F(1,1<<20);m=cfg['m']
        e=cfg['post_error'];assert e<F(1,1<<9247)
        final_corner_lower=cfg['positive_margin']['actual_diagonal_lower_gt']-e
        assert final_corner_lower>F(2,3)
        mu=F((1<<(m-1))+40*m,1<<20000);delta=e+mu;half=(m+1)//2
        post_l2=(1<<(half+1))*delta/gs+(1<<m)*delta*delta/(2*step*gs)
        post_dual=(1<<half)*post_l2
        gamma0=F(8,3)*z*gs
        heat=F(6*cfg['Nbase'],359)/(step*gamma0)*F(1,1<<(cfg['K']//4))
        heat_dual=(1<<cfg['dimension_debt'])*heat
        assert post_dual<F(1,1<<661) and heat_dual<F(1,1<<75)
        return {'post_operator_error':e,'post_skew_dual_error':post_dual,
                'heat_full_skew_dual_error':heat_dual,
                'normalization_gamma0_lower_without_pK':gamma0,
                'actual_M_positive_lower':cfg['positive_margin']['actual_diagonal_lower_gt'],
                'post_corner_lower':final_corner_lower}
