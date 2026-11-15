#!/usr/bin/env python3
"""Complete two-bit SOURCE component providers, before global clock binding.

Actual G/CX/SourceI blocks, level-nine coherent preparation, paid RAW inputs,
and literal integer inverse depths. Proper-link powers are computed lazily
by B93's certified finite algorithm. Its numeric full inventory has not
been run, so aggregate resource records are explicitly upper bounds.
"""
from pathlib import Path
from collections import Counter
from functools import lru_cache
from fractions import Fraction as F
import gzip,json,sys
sys.dont_write_bytecode=True
import two_bit_local_native as local
t=local.t;P=Path(__file__).resolve().parent;D=t.D;B=t.loc.B;nb=local.nb
sys.path.insert(0,str(D/'round21'));sys.path.insert(0,str(D/'round22'))
old=t.load('a48_old_choi_loader',D/'round21/choi_loader.py')
gray=t.load('a48_gray',D/'round22/gray_reflection.py')
vac=t.load('a48_vacuum',D/'round23/car_vacuum_prefix.py')
site=t.load('a48_site_native',B/'round45/site_native.py')
link=t.load('a48_two_bit_link',B/'round93/proper_link_two_bit_native.py')
BANKS=('y+','y-','f','0','x+','x-','q')

@lru_cache(None)
def inputs():
    with gzip.open(P/'RETUNED_SITE_LIBRARY.json.gz','rt') as f:slib=json.load(f)
    return {'prefix':json.loads((D/'round19/CHOI_PREFIX_CERTIFICATE.json').read_text()),
      'fixed':json.loads((P/'RETUNED_FIXED_ANGLES.json').read_text())['fixed_angles'],
      'level9':json.loads((P/'LEVEL9_CORRECTION_CERTIFICATE.json').read_text()),
      'phase':json.loads((B/'round39/ADAPTER_PHASE_CERTIFICATE.json').read_text()),
      'h_k':int(json.loads((D/'round14/NATIVE_BOOLEAN_ANGLE.json').read_text())['k']),
      'local_plan':json.loads((P/'TWO_BIT_LOCAL_NATIVE_PLAN.json').read_text()),
      'proper_upper':json.loads((B/'round93/PROPER_LINK_RESOURCE_UPPER.json').read_text()),
      'site':slib}

def choi_layout():return local.extend_layout(old.layout())
def car_layout():return local.material_layout()
def data(lay):return lay['address']+lay['choi_input']+lay['choi_output']
def private(lay):return [lay['branch'],lay['phase_rebit'],*lay['comparator_scratch']]

def validate_choi(lay,extra_external=()):
    assert len(lay['SAM'])==5376 and lay['all_SAM']==lay['SAM']
    wires=[*lay['SAM'],*data(lay),*private(lay),lay['port'],*lay['spin'],
           lay['aux_arbitrary'],lay['oldRIGHT_witness'],*extra_external]
    assert len(wires)==len(set(wires)) and all(type(q) is int and 0<=q<lay['qubits'] for q in wires)
    assert len(data(lay))==22 and len(private(lay))==24
    assert lay['modes']==lay['choi_output'][:4] and lay['julia_flag']==lay['choi_output'][4]

def omega_blocks(bank,lay=None,depth=0):
    assert bank in BANKS and type(depth) is int and depth>=0
    lay=choi_layout() if lay is None else lay;validate_choi(lay);odd=depth%2
    stages=['prefix','coframe','link']
    for stage in (reversed(stages) if odd else stages):
        if stage=='coframe':yield from local.coframe_blocks(bank,lay,True,depth)
        else:
            stream=(old.prefix.prefix_blocks(inputs()['prefix'],lay,True,bool(odd)) if stage=='prefix'
                    else link.bank_blocks(bank,lay,reverse=bool(odd)))
            for tree in stream:yield local.invert(tree,depth-odd,lay)

def half_blocks(bank,lay=None,levels=9,depth=0):
    assert type(levels) is int and 0<=levels<=9 and type(depth) is int and depth>=0
    lay=choi_layout() if lay is None else lay;x=inputs();al=old.adapter_layout(lay)
    fixed=old.adapter.fixed(al,int(x['phase']['phase_k']),int(x['level9']['correction_l']),x['h_k'])
    # Non-nine levels exist only for structural checks; their final phase
    # correction is deliberately NOT claimed to prepare the ideal half-vector.
    def leaf(blocks,d):
        for tree in (reversed(blocks) if d%2 else blocks):yield local.invert(tree,d,lay)
    def walk(n,d):
        if n==0:
            yield from leaf([fixed['H']],d);yield from omega_blocks(bank,lay,d)
            yield from leaf([fixed['H']],d);return
        children=[('A',0),('G',0),('A',1),('S',0),('A',0)]
        for kind,extra in (reversed(children) if d%2 else children):
            if kind=='A':yield from walk(n-1,d+extra)
            else:yield from leaf(fixed['good'] if kind=='G' else fixed['start'],d)
    if depth%2:
        yield from leaf([fixed['correction']],depth);yield from walk(levels,depth)
    else:
        yield from walk(levels,depth);yield from leaf([fixed['correction']],depth)

def raw_blocks(wires,lay,depth=0):
    for q in (reversed(wires) if depth%2 else wires):
        yield local.invert(nb.rotation_power(q,-1,lay['port'],tuple(lay['spin'])),depth,lay)

def choi_blocks(bank,lay=None,depth=0,extra_external=()):
    lay=choi_layout() if lay is None else lay;validate_choi(lay,extra_external)
    stages=[('PRIVATE_RAW',0),('DATA_RAW',0),('R',0),('U',1),('R',0),('U',0)]
    for kind,d in (reversed(stages) if depth%2 else stages):
        d+=depth
        if kind=='PRIVATE_RAW':yield from raw_blocks(private(lay),lay,d)
        elif kind=='DATA_RAW':yield from raw_blocks(data(lay),lay,d)
        elif kind=='R':
            k=int(inputs()['fixed']['joint_reflection_pi']['k'])
            yield from gray.blocks(data(lay)+private(lay),lay['aux_arbitrary'],k,
              lay['port'],tuple(lay['spin']),[*lay['SAM'],lay['oldRIGHT_witness'],*extra_external],d)
        else:yield from half_blocks(bank,lay,9,d)

def vacuum_blocks(lay,depth=0):
    x=inputs();k=int(x['fixed']['fourier_pi_over_2']['k']);kappa=vac.inputs()['kappa']
    stages=['RAW','H','VAC','FOURIER']
    for stage in (reversed(stages) if depth%2 else stages):
        if stage=='FOURIER':
            rows=list(vac.commands(kappa,lay,k))
            for cmd in (reversed(rows) if depth%2 else rows):yield from vac.rotation_blocks(cmd,lay,depth)
        else:
            rows=vac.fixed_blocks(stage,lay,x['h_k'])
            for tree in (reversed(rows) if depth%2 else rows):yield local.invert(tree,depth,lay)

def car_blocks(bank,lay=None,depth=0,extra_external=()):
    lay=car_layout() if lay is None else lay
    pv=[lay['predicate_flag'],*lay['predicate_work']]
    vac.validate(lay,[*pv,lay['native_aux_arbitrary'],*extra_external]);assert len(lay['SAM'])==5376
    stages=['PRIVATE_RAW','VACUUM','FRAME']
    for stage in (reversed(stages) if depth%2 else stages):
        if stage=='PRIVATE_RAW':yield from raw_blocks(pv,lay,depth)
        elif stage=='VACUUM':yield from vacuum_blocks(lay,depth)
        else:yield from local.frame_blocks(bank,lay,depth)

def site_blocks(lay=None,depth=0):yield from site.site_blocks(inputs()['site'],lay,depth)

def counter(row,base=10):return Counter({k:int(v,base) for k,v in row.items()})
def inv(c):return local.prep.raw_inverse_counts(c)
def times(c,n):return Counter({k:n*v for k,v in c.items()})
def raw_counts(n):return Counter(G_port=n,CX=6*n,SourceI=4*n)

def choi_inventory_upper(bank):
    x=inputs();cv=Counter()
    for tree in old.prefix.prefix_blocks(x['prefix'],choi_layout(),True):
        cv.update(old.prefix.resource(tree,choi_layout()['port']))
    cv.update(counter(x['local_plan']['coframe'][bank]['native_forward']))
    cv.update(counter(x['proper_upper']['bank_bounds'][bank]['forward_componentwise_upper_hex'],16))
    half,hi=old.adapter.native_budget(0,int(x['phase']['phase_k']),
        int(x['level9']['correction_l']),x['h_k'],cv,levels=9)
    r=gray.counts(46,int(x['fixed']['joint_reflection_pi']['k']))
    full=raw_counts(46)+times(r,2)+half+hi
    return {'Omega_forward_upper':cv,'half_forward_upper':half,
      'source_forward_upper':full,'source_literal_inverse_upper':inv(full)}

def car_inventory(bank):
    lay=car_layout();x=inputs();v=Counter()
    for stage in ('RAW','H','VAC'):
        for tree in vac.fixed_blocks(stage,lay,x['h_k']):v.update(vac.price(tree,lay['port']))
    for cmd in vac.commands(vac.inputs()['kappa'],lay,int(x['fixed']['fourier_pi_over_2']['k'])):
        K=cmd['K'];N=1<<K;neg=N//2;assert any(cmd['pattern'])
        v.update(G_port=neg*cmd['k'],G_other=neg*cmd['k'],CX=K*N+6*neg,SourceI=4*neg)
    full=raw_counts(3)+v+counter(x['local_plan']['material']['frames'][bank]['native_forward'])
    return {'vacuum_prefix_forward':v,'source_forward':full,'source_literal_inverse':inv(full)}

def error_bounds():
    x=inputs();delta=F(1,1<<3456);eps=F(1,1<<4096);pre=x['prefix']
    epre=F(int(pre['prefix_error_L1_numerator_hex'],16),1<<pre['precision_bits'])
    # Coframe/link occupy disjoint orthogonal address sectors, so maximum.
    select=max(26*delta,102*F(1,1<<3460));loader=epre+select
    L=3**9;half=F(1,1<<9841)+L*loader+(2*L+(2*L-2)*23+1)*eps
    choi=4*half+2*delta
    car=24*delta+43*eps # both U_m, all fixed frame terms, Fourier and H/X.
    site_error=18*delta
    full_source=1440*choi+128*car+site_error
    assert full_source<F(1,1<<3423)
    return {'controlled_Omega':loader,'half_vector_anchor_isometry':half,
      'Choi_declared_DATA_fibre':choi,'CAR_declared_DATA_fibre':car,
      'SITE_all_columns':site_error,'all1440Choi_128CAR_SITE':full_source}

def encode_error(x):return {'numerator_hex':hex(x.numerator),'denominator_hex':hex(x.denominator)}

def main():
    co={b:choi_inventory_upper(b) for b in BANKS};ca={b:car_inventory(b) for b in BANKS}
    total=site.inventory(inputs()['site'])['SITE_forward']
    for bank in BANKS:
        total.update(times(co[bank]['source_forward_upper'],180))
        total.update(times(ca[bank]['source_forward'],16))
    total.update(times(co['f']['source_forward_upper'],180))
    total.update(times(ca['q']['source_forward'],16))
    out={'status':'COMPLETE_TWO_BIT_SOURCE_COMPONENT_PROVIDERS_WITH_RIGOROUS_ERROR',
      'CODE_bits':5376,'half_vector_levels':9,'Choi_copies':1440,'CAR_copies':128,
      'full_source_component_error_lt':'2^-3423',
      'error_bounds':{k:encode_error(v) for k,v in error_bounds().items()},
      'Choi_componentwise_resource_upper':{b:{k:local.stringify(v) for k,v in rows.items()} for b,rows in co.items()},
      'CAR_exact_resource_counts':{b:{k:local.stringify(v) for k,v in rows.items()} for b,rows in ca.items()},
      'all_SOURCE_forward_componentwise_upper':local.stringify(total),
      'all_SOURCE_literal_inverse_componentwise_upper':local.stringify(inv(total)),
      'aggregate_counts_are_upper_not_actual':True,'proper_link_exact_numeric_full_inventory_evaluated':False,
      'all_declared_DATA_columns_and_external_entanglement_covered':True,
      'private_inputs_scope':'Choi private24 and CAR predicate3 initially native RAW; paid inverse included',
      'arbitrary_dirty_private_operator_claim':False,'original_unprovided_vacuum_extension_identified':False,
      'level9_correction_recomputed':True,'all_literal_inverse_depths_retained':True,
      'global_two_bit_birth_namespace_bound':False,'SourceI_replaced_by_G_CX_here':False,
      'new_full_SOURCE_compiled':False,'full_expanded_words_executed':False,
      'physical_C_closed':False,'GR_closed':False}
    (P/'TWO_BIT_SOURCE_COMPONENT_PLAN.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'full_source_component_error_lt':out['full_source_component_error_lt'],
      'SOURCE_forward_SourceI_upper_bits':total['SourceI'].bit_length(),
      'SOURCE_inverse_SourceI_upper_bits':inv(total)['SourceI'].bit_length()}))

if __name__=='__main__':main()
