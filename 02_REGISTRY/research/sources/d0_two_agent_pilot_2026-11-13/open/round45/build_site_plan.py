#!/usr/bin/env python3
"""Pin exact raw/native SITE grammar, complete cost and all-column bounds."""
from pathlib import Path
from fractions import Fraction
from hashlib import sha256
import importlib.util,sys,json
import site_native as n
import site_targets as t
P=Path(__file__).resolve().parent;lib=n.library();lay=n.layout();inv=n.inventory(lib,lay);delta=Fraction(1,2**3264);site_error=18*delta;assert site_error<Fraction(1,2**3259)
assert inv['RAW_inverse8']=={'G_port':8,'CX':48,'SourceI':32};assert inv['R_zero']['CX']==256 and inv['R_zero']['G_other']==256*int(lib['reflection_phase']['k']) and inv['R_zero']['SourceI']==0
assert +inv['SITE_literal_inverse']==+n.inv(inv['SITE_forward'])
D=t.D/'round21/choi_loader.py';sp=importlib.util.spec_from_file_location('b45_a21_binding',D);m=importlib.util.module_from_spec(sp);sys.modules[sp.name]=m;sp.loader.exec_module(m);joint=n.bind_to_choi(m.layout(),list(range(2739,2747)),2747)
sha=lambda p:sha256(Path(p).read_bytes()).hexdigest();files=[P/'site_targets.py',P/'certify_site_angles.py',P/'SITE_ANGLE_LIBRARY.json.gz',P/'site_native.py',t.PF,t.D/'round14/native_boolean.py',t.B/'round25/targets.py',D]
axes=('G_port','G_other','CX','SourceI')
out={'status':'ACTUAL_NATIVE_SITE_WRITER_ALL_COLUMNS','source_sha256':{str(p):sha(p) for p in files},'standalone_layout':lay,'example_A21_bound_layout':joint,'SITE_index_formula':'64*x0+16*x1+4*x2+x3','PF_total':10946,'PF_anchor_count':34,'tree_nodes':255,'distinct_tree_angles':len(lib['angles']),'tree_max_controls':7,'reflection_controls':8,'reflection_native_grammar':'closed Gray cycle: 256 G^k blocks, 256 CX, zero SourceI in forward','chronology':['RAW G^-1 on each SITE wire','R_0 via Gray-cycle aux phase','literal U^-1','R_0 via Gray-cycle aux phase','U'],'target':'O_chi (G^tensor8)^T on all 256 columns','input_born_v_not_silently_replaced':True,'per_angle_error_le':'2^-3264','tree_operator_error_le':'8*2^-3264','site_operator_error_le':'18*2^-3264','site_operator_error_lt':'2^-3259','error_numerator_hex':hex(site_error.numerator),'error_denominator_hex':hex(site_error.denominator),'all_external_factors_preserved_in_operator_norm':True,'no_extra_clean_scratch':True,'native_inventories':{name:{key:str(value[key]) for key in axes} for name,value in inv.items()},'native_inverse_is_literal':True,'full_giant_word_executed':False,'physical_H1_admission_proved':False,'physical_C_closed':False,'GR_closed':False}
(P/'SITE_NATIVE_PLAN.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'tree_nodes':255,'operator_error_lt':out['site_operator_error_lt'],'R_CX':inv['R_zero']['CX']}))
