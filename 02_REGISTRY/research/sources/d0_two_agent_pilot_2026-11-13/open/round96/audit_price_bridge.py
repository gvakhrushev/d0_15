#!/usr/bin/env python3
"""Independent A49 c_ref, actual corner, gain and shared-bank arithmetic."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');A=D/'round49'
bridge=json.loads((A/'CORNER_AND_PRICE_BRIDGE.json').read_text());gp=json.loads((D/'round48/TWO_BIT_GLOBAL_SOURCE_PLAN.json').read_text());cp=json.loads((D/'round47/FULL_VECTOR_CONTROL_PLAN.json').read_text());plan=json.loads((A/'TWO_BIT_PAID_FAMILY_PLAN.json').read_text())
for name,h in bridge['source_sha256'].items():assert sha256(Path(name).read_bytes()).hexdigest()==h,name
decode=lambda r:F(int(r['numerator_hex'],16),int(r['denominator_hex'],16))
e=decode(gp['errors']['full_canonical_compressed_error']);epre=decode(gp['errors']['full_SOURCE_DATA_fibre_prefix_error']);eps=decode(cp['control_vs_exp_tX_error']);post=decode(plan['bounds']['post_full_operator_error'])
lower=F(67,100)-e;assert decode(bridge['mathematical_cold_corner_error'])==e and decode(bridge['actual_M_entry_lower'])==lower
assert e<F(1,1<<3421)<F(1,1<<3298) and lower-post>F(2,3)
# p in (0,1), p²+p=1 implies p^7=13p−8. p<0.618034 via exact squares.
u=F(618034,10**6);assert (2*u+1)**2>5
cref=1-8*(13*u-8);assert cref>F(2,3)
# eta=z*p^K<z and |c0|<=1, so denominator 1-z+eta*c0²<=1.
z=F(1,1<<20);gs=F(1,1<<3208);assert 4*z*cref*gs>F(8,3)*z*gs
# The same SOURCE is used in ±; this is a local interface bound, not full price.
t=F(1,1<<1700);interface=2*epre/gs+2*eps/(t*gs)
assert interface==decode(bridge['same_shared_bank_control_interface_over_g_error']) and interface<F(1,1<<189)
assert bridge['interface_is_not_complete_physical_cost_source'] and not bridge['full_Cost_Info_selection_proved']
out={'status':'PASS_A49_TYPED_CORNER_GAIN_AND_SHARED_BANK_BRIDGE','actual_cold_corner_error_lt':'2^-3421','all_actual_CODE_diagonal_entries_gt':'2/3','fixed_actual_post_centre_gt':'2/3','gain_lower_coefficient':'(8/3)*z*2^-3208*p^K','shared_bank_control_interface_lt':'2^-189','full_physical_cost_source_or_original_marks_proved':False,'physical_C_closed':False,'GR_closed':False}
(P/'PRICE_BRIDGE_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
