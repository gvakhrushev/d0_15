#!/usr/bin/env python3
"""Explicit paid preparation of the original CAR vacuum/Fourier128 state.

This fixes a concrete unitary extension of that original state preparation.
It does NOT identify its paid history or marked full-column prefixes with an
unprovided earlier vacuum protocol. Fresh RIGHT7 belongs to this preparation;
unknown oldRIGHT and SAM remain exact spectators at every primitive.
"""
from pathlib import Path
from collections import Counter
from functools import lru_cache
from fractions import Fraction
import hashlib,importlib.util,json,sys
P=Path(__file__).resolve().parent;D=P.parent
B=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open')
s=importlib.util.spec_from_file_location('a23_nb',D/'round14/native_boolean.py');nb=importlib.util.module_from_spec(s);sys.modules[s.name]=nb;s.loader.exec_module(nb)
def layout():
    return {'SAM':list(range(2688)),'internal_SITE':list(range(2688,2696)),'grade':list(range(2696,2700)),
            'RIGHT':list(range(2700,2707)),'port':2707,'spin':[2708,2709],'oldRIGHT_witness':2710,'qubits':2711}
def validate(lay,extra_external=()):
    groups=[lay['SAM'],lay['internal_SITE'],lay['grade'],lay['RIGHT'],[lay['port'],*lay['spin'],lay['oldRIGHT_witness']],list(extra_external)]
    wires=[q for g in groups for q in g];assert len(wires)==len(set(wires)) and all(type(q) is int and 0<=q<lay['qubits'] for q in wires)
    assert len(lay['internal_SITE'])==8 and len(lay['grade'])==4 and len(lay['RIGHT'])==7 and len(lay['spin'])==2
@lru_cache(maxsize=1)
def inputs():
    return {'kappa':json.loads((B/'round21/ORIGINAL_FOURIER128_L4.json').read_text())['kappa'],
            'boolean_k':int(json.loads((D/'round14/NATIVE_BOOLEAN_ANGLE.json').read_text())['k']),
            'phase_k':int(json.loads((P/'FOURIER_PHASE_CERTIFICATE.json').read_text())['k'])}
def commands(kappa,lay,k):
    assert len(kappa)==64 and all(len(row)==4 and all(v in range(4) for v in row) for row in kappa)
    for pair,row in enumerate(kappa):
        for mu,value in enumerate(row):
            for high in (0,1):
                a=(value*(1<<high))%4
                if a==0:continue
                bit=2*(3-mu)+high
                yield {'pair':pair,'mu':mu,'site_bit':bit,'coefficient':a,'K':7,
                       'controls':lay['RIGHT'][1:]+[lay['internal_SITE'][bit]],
                       'pattern':[(pair>>j)&1 for j in range(6)]+[1],
                       'target':lay['RIGHT'][0],'k':a*k}
def inverse(t,depth,lay):
    for _ in range(depth):t=nb.inverse_literal(t,lay['port'],tuple(lay['spin']))
    return t
def rotation_blocks(cmd,lay,depth=0):
    K=cmd['K'];assert K==len(cmd['controls'])==len(cmd['pattern'])
    assert type(depth) is int and depth>=0
    for mask in (reversed(range(1<<K)) if depth%2 else range(1<<K)):
        subset=[j for j in range(K) if mask>>j&1];cx=[nb.gate('CX',cmd['controls'][j],cmd['target']) for j in subset]
        sign=(-1)**sum(cmd['pattern'][j] for j in subset)
        t=nb.seq(*cx,nb.rotation_power(cmd['target'],sign*cmd['k'],lay['port'],tuple(lay['spin'])),*reversed(cx))
        yield inverse(t,depth,lay)
def fixed_blocks(stage,lay,boolean_k):
    port=lay['port'];spin=tuple(lay['spin'])
    if stage=='RAW':return [nb.rotation_power(q,-1,port,spin) for q in lay['internal_SITE']+lay['grade']+lay['RIGHT']]
    if stage=='H':return [nb.boolean_word('H',boolean_k,target=q,port=port,spin=spin) for q in lay['internal_SITE']+lay['RIGHT'][1:]]
    assert stage=='VAC';g=lay['grade']
    return [nb.gate('G',g[0]),*[nb.gate('CX',g[0],q) for q in g[1:]],nb.boolean_word('X',boolean_k,target=g[0],port=port,spin=spin)]
def prefix_blocks(lay=None,depth=0,extra_external=()):
    lay=layout() if lay is None else lay;validate(lay,extra_external);x=inputs()
    assert type(depth) is int and depth>=0
    stages=['RAW','H','VAC','FOURIER']
    for stage in (reversed(stages) if depth%2 else stages):
        if stage=='FOURIER':
            rows=list(commands(x['kappa'],lay,x['phase_k']))
            for cmd in (reversed(rows) if depth%2 else rows):yield from rotation_blocks(cmd,lay,depth)
        else:
            rows=fixed_blocks(stage,lay,x['boolean_k'])
            for t in (reversed(rows) if depth%2 else rows):yield inverse(t,depth,lay)
def price(t,port):
    if t['op']=='seq':
        c=Counter()
        for child in t['children']:c.update(price(child,port))
        return c
    if t['op']=='repeat':return Counter({q:int(t['count'])*v for q,v in price(t['child'],port).items()})
    return Counter({('G_port' if t['wires'][0]==port else 'G_other') if t['op']=='G' else t['op']:1})
def inverse_price(c):return Counter({'G_port':c['G_port']+c['G_other'],'G_other':0,'CX':c['CX']+6*c['G_other'],'SourceI':3*c['SourceI']+4*(c['G_port']+c['G_other'])})
def inventory(lay=None):
    lay=layout() if lay is None else lay;validate(lay);x=inputs();stages={}
    for stage in ('RAW','H','VAC'):
        c=Counter()
        for t in fixed_blocks(stage,lay,x['boolean_k']):c.update(price(t,lay['port']))
        stages[stage]=c
    c=Counter()
    for cmd in commands(x['kappa'],lay,x['phase_k']):
        assert any(cmd['pattern']);K=cmd['K'];N=1<<K;negative=N//2
        c.update({'G_port':negative*cmd['k'],'G_other':negative*cmd['k'],'CX':K*N+6*negative,'SourceI':4*negative})
    stages['FOURIER']=c;full=Counter()
    for c in stages.values():full.update(c)
    stages['prefix_forward']=full;stages['prefix_literal_inverse']=inverse_price(full)
    return stages
def error_bound():
    sums=[sum(z+(2*z)%4 for z in row) for row in inputs()['kappa']];M=max(sums);assert M==18
    error=M*Fraction(1,2**3264)+15*Fraction(1,2**4096)
    assert error<Fraction(1,2**3259) and 112*error<Fraction(1,2**3252)
    return M,error
def main():
    l=layout();validate(l);x=inputs();cmd=list(commands(x['kappa'],l,x['phase_k']));M,e=error_bound();h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    pins=[Path(__file__),P/'FOURIER_PHASE_CERTIFICATE.json',D/'round14/native_boolean.py',D/'round14/NATIVE_BOOLEAN_ANGLE.json',B/'round21/ORIGINAL_FOURIER128_L4.json',B/'round25/targets.py']
    out={'status':'NATIVE_ORIGINAL_CAR_VACUUM_FOURIER_STATE_PREPARATION','source_sha256':{str(p):h(p) for p in pins},'layout':l,
         'fresh_RAW_wires':19,'internal_SITE_bits':8,'grade_bits':4,'fresh_RIGHT_bits':7,'extra_clean_work':0,
         'RIGHT_encoding':'r=2*pair+type; type=RIGHT[0], pair bits RIGHT[1:7]',
         'site_encoding':'index=64*x0+16*x1+4*x2+x3; x_mu low bit=2*(3-mu)',
         'chronology':['RAW inverse19','H on internal SITE8 and RIGHT pair6','G grade0; CX grade0 to grade1,2,3; X grade0','controlled type rotations by (pi/2)*kappa_pair dot x'],
         'original_target_amplitude':'m_star[grade] * (cos/sin(pi*kappa_pair dot x/2))[type] /128',
         'explicit_full_column_extension':'Fourier type rotation, not a claim of equality to an earlier unprovided paid prefix',
         'phase_macros':len(cmd),'phase_control_width':7,'angle_coefficient_sum':sum(z['coefficient'] for z in cmd),
         'max_active_angle_coefficient_sum':M,'H_macros':14,'X_macros':1,
         'operator_error_to_declared_extension_lt':'2^-3259','all112_prefix_error_lt':'2^-3252',
         'error_numerator_hex':hex(e.numerator),'error_denominator_hex':hex(e.denominator),
         'native_inventories':{name:{key:str(v[key]) for key in ('G_port','G_other','CX','SourceI')} for name,v in inventory(l).items()},
         'unknown_oldRIGHT_and_SAM_exact_spectators':True,'fresh_RIGHT_is_prepared_not_protected_unknown_input':True,
         'external_PF_SITE_weights_applied_to_internal_SITE':False,'old_prefix_history_or_price_equivalence_proved':False,
         'full_giant_word_executed':False,'physical_H1_marked_binding_proved':False,'physical_C_closed':False,'GR_closed':False}
    (P/'CAR_VACUUM_PREFIX_PLAN.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('status','phase_macros','max_active_angle_coefficient_sum','operator_error_to_declared_extension_lt')}))
if __name__=='__main__':main()
