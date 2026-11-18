#!/usr/bin/env python3
"""Compose all seven full CAR maps from A18, B37 and B35 reflections.

The three reflection predicate wires are incoming computational zeros.
Their physical RAW preparation, the original vacuum/Fourier prefix, marks
and birth admission remain separate. U_m and U_star use no private work.
"""
from pathlib import Path
from collections import Counter
import hashlib,importlib.util,json,sys
import material_preparation as m
import material_targets as t
P=Path(__file__).resolve().parent;D=P.parent
def load(name,path):
    sp=importlib.util.spec_from_file_location(name,path);obj=importlib.util.module_from_spec(sp);sys.modules[name]=obj;sp.loader.exec_module(obj);return obj
anchors=load('a18_b35_anchor',t.B/'round35/anchor_reflection.py')
h=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()

def layout():
    lay=m.layout();lay.update({'predicate_flag':2711,'predicate_work':[2712,2713],
                               'native_aux_arbitrary':2714,'qubits':2715})
    return lay

def remap(tree,mapper):
    if tree['op']=='seq':return m.nb.seq(*(remap(c,mapper) for c in tree['children']))
    if tree['op']=='repeat':return m.nb.repeat(int(tree['count']),remap(tree['child'],mapper))
    return m.nb.gate(tree['op'],*(mapper[w] for w in tree['wires']))

def fixed_components(lay=None):
    lay=layout() if lay is None else lay
    star=json.loads((t.B/'round37/CAR_USTAR_NATIVE.json').read_text())
    mapper=lay['grade']+[lay['port'],*lay['spin'],lay['oldRIGHT_witness']]
    U=remap(star['forward_DAG'],mapper);Ui=remap(star['literal_raw_inverse_DAG'],mapper)
    assert Ui==m.nb.inverse_literal(U,lay['port'],tuple(lay['spin']))
    k=int(json.loads((D/'round14/NATIVE_BOOLEAN_ANGLE.json').read_text())['k'])
    R=anchors.build(lay['grade'],1,lay['predicate_flag'],lay['predicate_work'],
                    lay['port'],tuple(lay['spin']),lay['native_aux_arbitrary'],k,
                    protected=lay['SAM']+lay['internal_SITE']+lay['RIGHT']+[lay['oldRIGHT_witness']])['native_DAG']
    return U,Ui,R

def frame_blocks(bank,library,lay=None):
    assert bank in ('y+','y-','f','0','x+','x-','q')
    lay=layout() if lay is None else lay;U,Ui,R=fixed_components(lay)
    # Mathematical M=R_(u_m)R_(u_star). Chronology is right-to-left.
    yield Ui;yield R;yield U
    if bank in ('q','y+','y-'):yield from m.preparation_blocks(bank,library,lay,True)
    else:yield Ui
    yield R
    if bank in ('q','y+','y-'):yield from m.preparation_blocks(bank,library,lay)
    else:yield U

def resource(tree,port):
    if tree['op']=='seq':
        out=Counter()
        for c in tree['children']:out.update(resource(c,port))
        return out
    if tree['op']=='repeat':return Counter({q:int(tree['count'])*v for q,v in resource(tree['child'],port).items()})
    if tree['op']=='G':return Counter({'G_port' if tree['wires'][0]==port else 'G_other':1})
    return Counter({tree['op']:1})

def main():
    lib=json.loads((P/'MATERIAL_PREPARATION_LIBRARY.json').read_text());lay=layout();U,Ui,R=fixed_components(lay)
    ur=resource(U,lay['port']);uir=resource(Ui,lay['port']);rr=resource(R,lay['port'])
    inv=m.inventory(lib);banks={};all_copies=Counter()
    for bank in ('y+','y-','f','0','x+','x-','q'):
        f=Counter(ur);f.update(uir);f.update({q:2*v for q,v in rr.items()})
        if bank in inv:
            for stage in ['native_forward','native_literal_inverse']:f.update({q:int(v) for q,v in inv[bank][stage].items()})
        else:f.update(ur);f.update(uir)
        banks[bank]={'native_forward':{q:str(v) for q,v in f.items()},
                      'native_literal_inverse':{q:str(v) for q,v in m.raw_inverse_counts(f).items()},
                      'endpoint_is_exact_identity':bank in ('f','0','x+','x-'),
                      'error_on_declared_clean_predicate_inputs_le':'0' if bank in ('f','0','x+','x-') else '28*2^-4096'}
        all_copies.update({q:16*v for q,v in f.items()})
    out={'status':'FINITE_NATIVE_SEVEN_CAR_FRAME_GRAMMARS','layout':lay,
         'inputs_sha256':{str(f):h(f) for f in [P/'material_preparation.py',P/'MATERIAL_PREPARATION_LIBRARY.json',t.B/'round35/anchor_reflection.py',t.B/'round37/CAR_USTAR_NATIVE.json',D/'round14/NATIVE_BOOLEAN_ANGLE.json']},
         'chronology':['actual U_star literal inverse','actual joint grade1 reflection','actual U_star','actual U_m literal inverse','same actual grade1 reflection','actual U_m'],
         'predicate_zero_wires_required':[lay['predicate_flag'],*lay['predicate_work']],
         'predicate_zero_preparation_included':False,'native_aux_may_be_arbitrary_entangled':True,
         'banks':banks,'112_CAR_copy_conservative_forward_inventory':{q:str(v) for q,v in all_copies.items()},
         '112_CAR_copy_conservative_error_lt':'2^-4084',
         'target_is_B25_full_grade_map_tensor_I_RIGHT':True,'fixed_identity_banks_still_keep_all_paid_stages':True,
         'original_CAR_vacuum_Fourier_prefix_included':False,'full_physical_birth_mark_clock_admission_proved':False,
         'full_H1_writer_emitted':False,'physical_C_closed':False,'GR_closed':False}
    assert 112*28<2**12
    (P/'CAR_FRAME_PLAN.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'banks':len(banks),'predicate_zero_inputs':3,'conservative_error':out['112_CAR_copy_conservative_error_lt']}))

if __name__=='__main__':main()
