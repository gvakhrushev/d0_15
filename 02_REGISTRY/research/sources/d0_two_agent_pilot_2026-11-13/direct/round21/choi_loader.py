#!/usr/bin/env python3
"""Concrete full controlled Omega and coherent half-vector native generators.

Every source provider is pinned code + a finite catalogue of explicit integer
powers. Providers stream actual native DAG blocks; none is a free oracle.
Literal inversion depth is retained through all nested adapter calls.
"""
from pathlib import Path
from collections import Counter
from functools import lru_cache
from fractions import Fraction
import hashlib,importlib.util,json,sys
P=Path(__file__).resolve().parent;D=P.parent
B=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open')
sys.path.insert(0,str(D/'round20'))
def load(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
prefix=load('a21_prefix',D/'round19/choi_prefix.py')
coframe=load('a21_coframe',D/'round20/coframe_native.py')
link=load('a21_link',B/'round42/proper_link_native.py')
adapter=load('a21_adapter',B/'round39/adapter_native.py');nb=prefix.nb
def layout():
    l=prefix.layout();l.update({'all_SAM':l['SAM'],'modes':l['choi_output'][:4],'julia_flag':l['choi_output'][4],
                               'phase_rebit':2716,'comparator_scratch':list(range(2717,2739)),'qubits':2739})
    return l
def adapter_layout(lay=None):
    l=layout() if lay is None else lay;data=l['address']+l['choi_input']+l['choi_output']
    return {'branch':l['branch'],'rebit':l['phase_rebit'],'data':data,'V_private':[],
            'external':l['SAM'],'start_controls':[l['branch'],*data],
            'predicate_flag':l['comparator_scratch'][0],'predicate_work':l['comparator_scratch'][1:],
            'port':l['port'],'spin':l['spin'],'aux_arbitrary':l['aux_arbitrary'],
            'oldRIGHT_witness':l['oldRIGHT_witness'],'qubits':l['qubits']}
@lru_cache(maxsize=1)
def inputs():
    return {'prefix':json.loads((D/'round19/CHOI_PREFIX_CERTIFICATE.json').read_text()),
            'coframe':json.loads((D/'round20/COFRAME_ANGLE_LIBRARY.json').read_text()),
            'link':link.library(),'phase':json.loads((B/'round39/ADAPTER_PHASE_CERTIFICATE.json').read_text()),
            'h_k':int(json.loads((D/'round14/NATIVE_BOOLEAN_ANGLE.json').read_text())['k'])}
def inverted(tree,depth,lay):
    for _ in range(depth):tree=nb.inverse_literal(tree,lay['port'],tuple(lay['spin']))
    return tree
def omega_blocks(bank,lay=None,inverse_depth=0):
    """Actual complete branch-controlled loader, all original source sectors."""
    assert bank in ('y+','y-','f','0','x+','x-','q') and type(inverse_depth) is int and inverse_depth>=0
    l=layout() if lay is None else lay;x=inputs();odd=bool(inverse_depth%2)
    stages=('link','coframe','prefix') if odd else ('prefix','coframe','link')
    for stage in stages:
        if stage=='prefix':stream=prefix.prefix_blocks(x['prefix'],l,controlled=True,reverse=odd)
        elif stage=='coframe':stream=coframe.select_blocks(bank,x['coframe'],l,controlled=True,reverse=odd)
        else:stream=link.bank_blocks(bank,x['link'],l,reverse=odd)
        # The provider has already applied one literal inversion when odd.
        for tree in stream:yield inverted(tree,inverse_depth-int(odd),l)
def half_blocks(bank,lay=None,levels=8,inverse_depth=0):
    """B39 chronology with this concrete finite provider in place of a DAG.

    The provider is re-entered at every occurrence; there is no skipped
    source call, success measurement, discarded failure or inverse reduction.
    """
    assert type(levels) is int and 0<=levels<=8 and type(inverse_depth) is int and inverse_depth>=0
    l=layout() if lay is None else lay;x=inputs();al=adapter_layout(l)
    fixed=adapter.fixed(al,int(x['phase']['phase_k']),int(x['phase']['correction_l']),x['h_k'])
    def leaf(blocks,depth):
        for block in (reversed(blocks) if depth%2 else blocks):yield inverted(block,depth,l)
    def walk(n,depth):
        if n==0:
            yield from leaf([fixed['H']],depth)
            yield from omega_blocks(bank,l,depth)
            yield from leaf([fixed['H']],depth);return
        children=[('A',0),('G',0),('A',1),('S',0),('A',0)]
        for kind,extra in (reversed(children) if depth%2 else children):
            if kind=='A':yield from walk(n-1,depth+extra)
            else:yield from leaf(fixed['good'] if kind=='G' else fixed['start'],depth)
    if inverse_depth%2:
        yield from leaf([fixed['correction']],inverse_depth);yield from walk(levels,inverse_depth)
    else:
        yield from walk(levels,inverse_depth);yield from leaf([fixed['correction']],inverse_depth)
def counts(bank):
    pre=json.loads((D/'round19/CHOI_PREFIX_PLAN.json').read_text())['actual_native_resources']['controlled']['forward']
    cf=json.loads((D/'round20/COFRAME_NATIVE_PLAN.json').read_text())['banks'][bank]['native_forward']
    li=json.loads((B/'round42/PROPER_LINK_NATIVE_RESOURCES.json').read_text())['banks'][bank]['forward']
    cv=Counter()
    for part in (pre,cf,li):cv.update({k:int(v) for k,v in part.items()})
    x=inputs();half,reverse=adapter.native_budget(0,int(x['phase']['phase_k']),int(x['phase']['correction_l']),x['h_k'],cv)
    return cv,adapter.raw_inverse_counts(cv),half,reverse
def error_bounds():
    x=inputs();cert=x['prefix'];prefix_error=Fraction(int(cert['prefix_error_L1_numerator_hex'],16),1<<cert['precision_bits'])
    delta=Fraction(1,2**3264);select_error=max(26*delta,101*delta);loader=prefix_error+select_error
    half=Fraction(1,2**3280)+6561*loader+(13122+13120*23+1)*Fraction(1,2**4096)
    assert select_error<Fraction(1,2**3257) and loader<Fraction(1,2**3250) and half<Fraction(1,2**3230)
    return prefix_error,select_error,loader,half
def main():
    l=layout();al=adapter_layout(l);x=inputs();errors=error_bounds();h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    private=[l['branch'],l['phase_rebit'],*l['comparator_scratch']]
    assert len(private)==24 and len(al['data'])==22 and len(al['predicate_work'])==21
    namespaces=[l['SAM'],al['data'],private,[l['port'],*l['spin'],l['aux_arbitrary'],l['oldRIGHT_witness']]]
    flat=[q for group in namespaces for q in group];assert len(flat)==len(set(flat))==l['qubits']
    pinpaths=[Path(__file__),D/'round19/choi_prefix.py',D/'round19/CHOI_PREFIX_CERTIFICATE.json',D/'round19/CHOI_PREFIX_PLAN.json',
              D/'round20/coframe_native.py',D/'round20/COFRAME_ANGLE_LIBRARY.json',D/'round20/COFRAME_NATIVE_PLAN.json',
              B/'round42/proper_link_native.py',B/'round42/PROPER_LINK_ANGLE_LIBRARY.json.gz',B/'round42/PROPER_LINK_NATIVE_RESOURCES.json',
              B/'round42/B42_CHECKPOINT.json',B/'round39/adapter_native.py',B/'round39/ADAPTER_PHASE_CERTIFICATE.json',
              B/'round39/ADAPTER_NATIVE_GRAMMAR.json',D/'round14/native_boolean.py',D/'round14/NATIVE_BOOLEAN_ANGLE.json']
    banks={}
    for bank in ('y+','y-','f','0','x+','x-','q'):
        values=counts(bank)
        banks[bank]={key:{axis:str(value[axis]) for axis in ('G_port','G_other','CX','SourceI')} for key,value in zip(('Omega_forward','Omega_literal_inverse','half_forward','half_literal_inverse'),values)}
    out={'status':'CONCRETE_COHERENT_FULL_OMEGA_AND_HALF_VECTOR_GENERATORS',
         'source_and_library_sha256':{str(p):h(p) for p in pinpaths},'layout':l,'B39_adapter_layout':al,
         'Omega_chronology':['A19 controlled address/Bell prefix','A20 coframe SELECT','B42 proper-link SELECT'],
         'Omega_private_clean_work':0,'half_vector_private_clean_wires':private,'half_vector_private_clean_work':24,
         'strict_Omega_branch0_identity':True,'Omega_rebit_and_comparator_exact_spectators':True,
         'Omega_uniform_full_operator_error_lt':'2^-3250','half_vector_uniform_joint_anchor_isometry_error_lt':'2^-3230',
         'half_vector_anchor_overlap_constant':'c=1/sqrt65568','half_vector_fixed_point_levels':8,
         'error_numerators_hex':[hex(e.numerator) for e in errors],'error_denominators_hex':[hex(e.denominator) for e in errors],
         'banks':banks,'B39_new24_RAW_zero_inventory_separate':{'G_port':'24','G_other':'0','CX':'144','SourceI':'96'},
         'input_DATA22_RAW_inverse_inventory_separate':{'G_port':'22','G_other':'0','CX':'132','SourceI':'88'},
         'RAW_initialization_included_in_unitary_counts':False,'all_native_calls_retained':True,
         'native_representation':'Finite bounded generators of actual seq/repeat/G/CX/SourceI DAG blocks; no unresolved loader oracle; giant flat DAG not materialized.',
         'B35_outer_joint_reflection_anchor_width':46,'B35_extra_comparator_clean_wires_required':45,
         'B35_outer_reflection_compiled_here':False,'full_original_RAW_Choi_bank_compiled_here':False,
         'full_H1_alpha_and_original_physical_history_proved':False,'full_giant_word_executed':False,
         'physical_C_closed':False,'GR_closed':False}
    (P/'CHOI_LOADER_PLAN.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'Omega_error_lt':out['Omega_uniform_full_operator_error_lt'],'half_error_lt':out['half_vector_uniform_joint_anchor_isometry_error_lt'],'half_private_work':24}))
if __name__=='__main__':main()
