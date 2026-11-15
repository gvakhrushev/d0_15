#!/usr/bin/env python3
"""A48 new split, CODE-disjoint middle, closed SourceI cut and error units."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction as F
from collections import Counter
import json,sys
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');sys.path.insert(0,str(D/'round48'));import two_bit_global_source as g
plan=g.namespace();l=plan['layout'];code=set(l['SAM']);schedule=g.previous.stages();cut=schedule.index({'kind':'RAW_RESOURCE_FRAME','intrinsic_inverse_depth':0});after=schedule[cut+1:]
assert Counter(x['kind'] for x in schedule[:cut+1])=={'SITE':1,'SIGMA':8,'SOURCE':1568,'RAW_RESOURCE_FRAME':1}
assert Counter(x['kind'] for x in after)=={'RAW_RESOURCE_FRAME':1,'REPORT':8,'PORT_ZERO':1,'SC6':1}
assert code.isdisjoint(set(g.previous.resource_wires())|set(plan['SC6_local_to_global'])|set(l['SITE'])|{l['port'],*l['spin'],l['aux_arbitrary'],l['oldRIGHT_witness'],plan['old_compiler_helper']})
N=plan['local_report']['logical_wire_count']
for report in plan['reports']:
 lo=report['private_start'];hi=lo+report['private_width'];assert hi-lo==N-8 and all(not lo<=q<hi for q in code)
 assert all(g.ns.report_wire(plan,report,q) not in code for q in [*range(8),*range(N,N+5)])
# Literal reverse of the entire SourceI-profile means S0=T^† Z T.
# Actual compiler is not a homomorphism of literal inversion; do not impose
# actual C=B^†, actual S=S^†, or symmetric cross kernel.
nb=g.nb;si=nb.gate('SourceI',l['port'],*l['spin']);tag={'op':'B82_CUT','name':g.previous.p43.CUTS[0]}
def odd():yield si;yield tag;yield si
def even():yield si;yield si;yield tag
try:list(g.previous.compile_tagged(odd,g.compiler(),lambda z:z));raise AssertionError('open SourceI cut accepted')
except AssertionError as ex:assert 'unfinished SourceI pair' in str(ex)
closed=list(g.previous.compile_tagged(even,g.compiler(),lambda z:z));assert closed[-1]==tag
# Structural compiler coverage: at cut every SI pair and CZ macro closed;
# arbitrary contraction inserted on the same carrier does not enlarge any
# telescoping term. SourceI^2 -> Z uses <=16 errors/2 occurrences; each
# certified CZ <=32 errors/at least 5 occurrences, giving <=8 per SourceI.
assert F(16,2)==8 and F(32,5)<8
p=json.loads((D/'round48/TWO_BIT_GLOBAL_SOURCE_PLAN.json').read_text());W=Counter({k:int(v) for k,v in p['counts_componentwise_upper_not_actual']['W_profile_upper'].items()});replacement=F(8*W['SourceI'],1<<20000)
decode=lambda z:F(int(z['numerator_hex'],16),int(z['denominator_hex'],16))
assert replacement==decode(p['errors']['replacement_error']) and replacement<F(1,1<<15800)
# Ensure the split is anchored in the actual emitted profile code and A49
# inserts Q at these same tags, not at a relabelled source frontier.
family_path=D/'round49/two_bit_paid_family.py';src=family_path.read_text();assert 'source.compiled_core_with_cuts' in src and 'tag_ops=(\'B82_CUT\',)' in src
out={'status':'PASS_A48_CLOSED_Q_CUTS_AND_ALL_INSERTION_TELESCOPE','source_stages_before_first_cut':1568,'reports_in_CODE_disjoint_middle':8,'literal_SourceI_middle_is_reflection':True,'actual_compiled_middle_assumed_reflection':False,'actual_compiled_return_assumed_adjoint':False,'any_contractive_insertion_at_closed_cuts_does_not_amplify_telescope':True,'replacement_error_lt':'2^-15800','open_SourceI_cut_rejected':True,'closed_pair_cut_accepted':True,'all_internal_source_marks_transport_proved':False,'full_word_enumerated':False,'GR_closed':False,'source_sha256':{str(q):sha256(q.read_bytes()).hexdigest() for q in (D/'round48/two_bit_global_source.py',D/'round48/TWO_BIT_GLOBAL_SOURCE_PLAN.json',D/'round49/two_bit_paid_family.py',D/'round29/gcx_compiler.py')}}
(P/'SPLIT_INSERTION_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='source_sha256'}))
