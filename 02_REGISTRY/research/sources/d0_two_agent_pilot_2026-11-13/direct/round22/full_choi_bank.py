#!/usr/bin/env python3
"""Full original RAW Choi bank, with a paid joint-anchor reflection.

The operator contract covers every original DATA column with the 24 U-private
wires initially zero, and arbitrary (possibly entangled) external factors.
raw_prepared_blocks additionally pays for those 24 zeros from native RAW v.
Every inverse is the literal inverse of the actual emitted primitive history.
"""
from pathlib import Path
from collections import Counter
from fractions import Fraction
from functools import lru_cache
import hashlib,importlib.util,json,sys
import gray_reflection as reflection
P=Path(__file__).resolve().parent;D=P.parent
s=importlib.util.spec_from_file_location('a22_choi_loader',D/'round21/choi_loader.py');c=importlib.util.module_from_spec(s);sys.modules[s.name]=c;s.loader.exec_module(c)
nb=c.nb
def layout():return c.layout()
def data(lay):return lay['address']+lay['choi_input']+lay['choi_output']
def private(lay):return [lay['branch'],lay['phase_rebit'],*lay['comparator_scratch']]
def validate(lay,extra_external=()):
    wires=[*lay['SAM'],*data(lay),*private(lay),lay['port'],*lay['spin'],lay['aux_arbitrary'],lay['oldRIGHT_witness'],*extra_external]
    assert len(wires)==len(set(wires)) and all(type(q) is int and 0<=q<lay['qubits'] for q in wires)
    assert len(data(lay))==22 and len(private(lay))==24
    assert len(lay['SAM'])==2688 and len(lay['address'])==12 and len(lay['choi_input'])==len(lay['choi_output'])==5
    assert lay['all_SAM']==lay['SAM'] and lay['modes']==lay['choi_output'][:4] and lay['julia_flag']==lay['choi_output'][4]
    reflection.validate(data(lay)+private(lay),lay['aux_arbitrary'],lay['port'],tuple(lay['spin']),[*lay['SAM'],lay['oldRIGHT_witness'],*extra_external])
@lru_cache(maxsize=1)
def reflection_certificate():return json.loads((P/'GRAY_REFLECTION_CERTIFICATE.json').read_text())
def reflection_k():return int(reflection_certificate()['entries']['46']['k'])
def inverse(tree,depth,lay):return c.inverted(tree,depth,lay)
def raw_zero_blocks(wires,lay,depth=0):
    assert type(depth) is int and depth>=0
    for q in (reversed(wires) if depth%2 else wires):
        yield inverse(nb.rotation_power(q,-1,lay['port'],tuple(lay['spin'])),depth,lay)
def joint_reflection_blocks(lay,depth=0,extra_external=()):
    yield from reflection.blocks(data(lay)+private(lay),lay['aux_arbitrary'],reflection_k(),lay['port'],tuple(lay['spin']),
                                 [*lay['SAM'],lay['oldRIGHT_witness'],*extra_external],depth)
def stage_schedule(depth=0,initialize_private=False):
    assert type(depth) is int and depth>=0
    stages=([('PRIVATE_RAW',0)] if initialize_private else [])+[('DATA_RAW',0),('R',0),('U',1),('R',0),('U',0)]
    return [(kind,depth+intrinsic) for kind,intrinsic in (reversed(stages) if depth%2 else stages)]
def bank_blocks(bank,lay=None,depth=0,extra_external=(),initialize_private=False):
    """Finite lazy native generator; 2^46 Gray terms are not materialized."""
    lay=layout() if lay is None else lay;validate(lay,extra_external)
    assert bank in ('y+','y-','f','0','x+','x-','q')
    for kind,d in stage_schedule(depth,initialize_private):
        if kind=='PRIVATE_RAW':yield from raw_zero_blocks(private(lay),lay,d)
        elif kind=='DATA_RAW':yield from raw_zero_blocks(data(lay),lay,d)
        elif kind=='R':yield from joint_reflection_blocks(lay,d,extra_external)
        else:yield from c.half_blocks(bank,lay,levels=8,inverse_depth=d)
def raw_prepared_blocks(bank,lay=None,depth=0,extra_external=()):
    yield from bank_blocks(bank,lay,depth,extra_external,initialize_private=True)
def raw_counts(n):return Counter({'G_port':n,'G_other':0,'CX':6*n,'SourceI':4*n})
def inventory(bank):
    cv,cvi,u,ui=c.counts(bank);r=reflection.counts(46,reflection_k());raw=raw_counts(22);clean=raw_counts(24)
    full=raw+r+ui+r+u;prepared=clean+full
    return {'DATA22_RAW_inverse':raw,'private24_RAW_to_zero':clean,'R_joint46':r,'R_joint46_literal_inverse':reflection.inverse_counts(r),
            'U_half_forward':u,'U_half_literal_inverse':ui,'bank_forward':full,'bank_literal_inverse':reflection.inverse_counts(full),
            'RAW_prepared_forward':prepared,'RAW_prepared_literal_inverse':reflection.inverse_counts(prepared)}
def errors():
    eta=c.error_bounds()[3];delta=Fraction(1,2**3264);bank=4*eta+2*delta;copies=1260*bank
    assert bank<Fraction(1,2**3227) and copies<Fraction(1,2**3216)
    return eta,delta,bank,copies
def main():
    l=layout();validate(l);eta,delta,error,copies=errors();h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    pinpaths=[Path(__file__),P/'gray_reflection.py',P/'GRAY_REFLECTION_CERTIFICATE.json',P/'GRAY_REFLECTION_CHECK.json',
              D/'round21/choi_loader.py',D/'round21/CHOI_LOADER_PLAN.json',D/'round21/CHOI_LOADER_CHECK.json']
    native={}
    for bank in ('y+','y-','f','0','x+','x-','q'):
        native[bank]={name:{axis:str(v[axis]) for axis in ('G_port','G_other','CX','SourceI')} for name,v in inventory(bank).items()}
    out={'status':'CONCRETE_FULL_ORIGINAL_RAW_CHOI_BANK_NATIVE_GENERATOR','source_sha256':{str(p):h(p) for p in pinpaths},
         'layout':l,'chronology':['DATA22 RAW inverse','joint-anchor R46','actual U literal inverse','joint-anchor R46','actual U'],
         'original_target':'O_b (G dagger)^tensor22 on every original DATA column; private24 initially zero; arbitrary external',
         'canonical_orientation':'O_b=R_u R_r, u=(r+Omega)/sqrt(2(1+1/sqrt65568))',
         'original_DATA_columns':1<<22,'all_SAM_sectors':True,'includes_padding_RAW_mixed_columns':True,
         'joint_anchor_wires':data(l)+private(l),'joint_anchor_width':46,'new_reflection_clean_work':0,
         'U_private_clean_work':24,'RAW_prepared_generator_pays_private_initialization':True,
         'private24_RAW_initialization_must_be_bound_to_actual_births':True,
         'R_is_not_exact_involution':True,'integer_literal_inverse_depths_preserved':True,
         'unitary_operator_error_on_clean_private_lt':'2^-3227','all1260_Choi_error_lt':'2^-3216',
         'error_formula':'4 eta_U +2 delta_R; for 1260 copies use 5040 eta_U+2520 delta_R',
         'exact_error_numerators_hex':[hex(q.numerator) for q in (eta,delta,error,copies)],
         'exact_error_denominators_hex':[hex(q.denominator) for q in (eta,delta,error,copies)],
         'native_inventories':native,'initialization_and_DATA_RAW_are_not_free':True,
         'native_terms_per_R46':str(1<<46),'native_G_blocks_per_R46':str(1<<46),'native_CX_per_R46':str(1<<46),
         'giant_R46_sequence_enumerated':False,'full_giant_word_executed':False,'Lean_proof_claimed':False,
         'same_physical_H1_admission_proved':False,'full_H1_alpha_known':False,'physical_C_closed':False,'GR_closed':False}
    (P/'FULL_CHOI_BANK_PLAN.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({key:out[key] for key in ('status','new_reflection_clean_work','unitary_operator_error_on_clean_private_lt','all1260_Choi_error_lt')}))
if __name__=='__main__':main()
