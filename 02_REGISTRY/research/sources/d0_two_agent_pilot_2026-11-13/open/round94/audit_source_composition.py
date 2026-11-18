#!/usr/bin/env python3
"""Independent finite-structure and rational-budget audit of A48 SOURCE/core."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from hashlib import sha256
import itertools,json,sys
P=Path(__file__).resolve().parent;A=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round48');sys.path.insert(0,str(A))
import two_bit_source_native as s
import two_bit_global_source as g
cplan=json.loads((A/'TWO_BIT_SOURCE_COMPONENT_PLAN.json').read_text());p=json.loads((A/'TWO_BIT_GLOBAL_SOURCE_PLAN.json').read_text());ns=g.namespace();lay=ns['layout']
assert len(lay['SAM'])==5376 and g.birth_blocks()[-1]['role']=='two_bit_high_CODE_RAW'
# Default standalone alias and namespace validity after A48 correction.
default=s.choi_layout();assert default['all_SAM']==default['SAM'] and len(default['SAM'])==5376
s.validate_choi(default)

assert sum(x['stop']-x['start'] for x in g.birth_blocks())==11893774624
for j in range(2688):assert g.physical_wire(lay['SAM'][j])==2+j and g.physical_wire(lay['SAM'][2688+j])==11893771936+j
assert ns['SC6_local_to_global']==g.previous.namespace()['SC6_local_to_global']
slots=Counter(x['kind'] for x in ns['source_slots']);assert slots=={'Choi':1440,'CAR':128}
stages=g.previous.stages();kinds=Counter(x['kind'] for x in stages);assert kinds['SOURCE']==1568 and kinds['SITE']==1 and kinds['REPORT']==8 and kinds['SIGMA']==8
# Coframe and proper-link source sectors are orthogonal address blocks.
specs,cat=g.s.link.fixed_and_catalogue();cf=s.local.library('COFRAME')['catalogue_templates']
for bank,section in cat.items():
 proper={row['address'] for row in section['fixed']}|{row['address'] for row in section['variable']};coframe={row['address'] for row in cf[bank]}
 assert not proper&coframe,(bank,'overlap')
# Actual recursion traversal instrumented with symbolic unit records. The
# underlying local G/CX grammar is checked separately by audit_local_inventory.
oldfixed=s.old.adapter.fixed;oldomega=s.omega_blocks;oldinvert=s.local.invert
s.old.adapter.fixed=lambda *args,**kw:{'H':{'tag':'H'},'good':[{'tag':'G'}],'start':[{'tag':'S'}],'correction':{'tag':'C'}}
s.omega_blocks=lambda bank,lay,d:iter([{'tag':'O','depth':d}])
s.local.invert=lambda tree,d,lay:{'tag':tree['tag'],'depth':d}
try:
 forward=list(s.half_blocks('f',levels=9,depth=0));reverse=list(s.half_blocks('f',levels=9,depth=1))
 assert reverse==[{'tag':z['tag'],'depth':z['depth']+1} for z in reversed(forward)]
 q=Counter(z['tag'] for z in forward);assert q=={'O':3**9,'H':2*3**9,'G':(3**9-1)//2,'S':(3**9-1)//2,'C':1}
finally:s.old.adapter.fixed=oldfixed;s.omega_blocks=oldomega;s.local.invert=oldinvert
# Independent rational recomputation from literal stored prefix receipt.
delta=F(1,1<<3456);eps=F(1,1<<4096);prefix=s.inputs()['prefix'];ep=F(int(prefix['prefix_error_L1_numerator_hex'],16),1<<prefix['precision_bits'])
L=19683;select=max(26*delta,102*F(1,1<<3460));loader=ep+select
half=F(1,1<<9841)+L*loader+(2*L+(2*L-2)*23+1)*eps
choi=4*half+2*delta;car=24*delta+43*eps;site=18*delta;source=1440*choi+128*car+site
expected={'controlled_Omega':loader,'half_vector_anchor_isometry':half,'Choi_declared_DATA_fibre':choi,'CAR_declared_DATA_fibre':car,'SITE_all_columns':site,'all1440Choi_128CAR_SITE':source}
def decode(row):return F(int(row['numerator_hex'],16),int(row['denominator_hex'],16))
for key,v in expected.items():assert decode(cplan['error_bounds'][key])==v
assert source<F(1,1<<3423)
def counter(row,base=10):return Counter({k:int(v,base) for k,v in row.items()})
def inv(c):return Counter(G_port=c['G_port']+c['G_other'],G_other=0,CX=c['CX']+6*c['G_other'],SourceI=3*c['SourceI']+4*(c['G_port']+c['G_other']))
def scale(c,n):return Counter({k:n*v for k,v in c.items()})
sourcecost=counter(cplan['all_SOURCE_forward_componentwise_upper']);report=json.loads((g.D/'round17/GLOBAL_REPORT_COMPILATION.json').read_text());rp=counter(report['native_forward_resources']);r=len(g.previous.resource_wires());assert r==34112
Aupper=sourcecost+scale(rp,8)+Counter(G_port=8,CX=48,SourceI=32)+Counter(G_other=r,G_port=r,CX=6*r,SourceI=4*r)+Counter(G_port=5889,CX=4096,SourceI=8196)
W=Aupper+inv(Aupper)+Counter(SourceI=2)
assert +Aupper==+counter(p['counts_componentwise_upper_not_actual']['A_profile_upper'])
assert +W==+counter(p['counts_componentwise_upper_not_actual']['W_profile_upper'])
k=g.compiler().k;units=8*W['SourceI'];new=Counter(G=W['G_port']+W['G_other']+k*units,CX=W['CX']+W['SourceI'])
assert +new==+counter(p['W_G_CX_componentwise_upper'],16) and sum(new.values()).bit_length()==24272
prefix_profile=sourcecost+Counter(G_port=8,CX=48,SourceI=32)+Counter(G_other=r)
prefix_error=source+F(8*prefix_profile['SourceI'],1<<20000)
assert decode(p['errors']['full_SOURCE_DATA_fibre_prefix_error'])==prefix_error and prefix_error<F(1,1<<3423)
replacement=F(units,1<<20000);known=report['seven_report_all_known_approximate_macros'];assert known%7==0
eta=source+F(8*(known//7),1<<4096);eB=2*eta+replacement
assert decode(p['errors']['replacement_error'])==replacement and decode(p['errors']['full_canonical_compressed_error'])==eB
assert replacement<F(1,1<<15800) and eB<F(1,1<<3421) and eB<F(1,1<<3300)
assert p['exact_numeric_full_inventory_evaluated'] is False and p['full_new_mark_clock_postprocessing_family_compiled'] is False
out={'status':'PASS_A48_SOURCE_COMPONENT_AND_CORE_STRUCTURE_CONDITIONAL_BUDGET','all_2688_physical_CODE_pairs_checked':True,'default_choi_layout_alias_repaired_and_validated':True,'RAW_births':11893774624,'source_slots':dict(slots),'coframe_link_address_sets_disjoint':True,'level9_forward_and_literal_inverse_symbolic_tokens':len(forward),'level9_omega_occurrences':q['O'],'ideal_phase_corrected_vector_error_lt':'2^-9841','source_error_lt':'2^-3423','full_SOURCE_DATA_fibre_G_CX_prefix_error_lt':'2^-3423','source_error_claim_scope':'declared private canonical fibre, conditional on inherited A22/A24/B45/source target contracts','W_call_count_componentwise_upper_bit_length':24272,'SourceI_replacement_error_lt':'2^-15800','canonical_compressed_eB_lt':'2^-3421','actual_numeric_full_inventory_evaluated':False,'marked_clock_post_family_or_corner_error_proved':False,'physical_C_closed':False,'GR_closed':False}
(P/'SOURCE_COMPOSITION_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
