#!/usr/bin/env python3
"""Consume the all-target A27 moment law on A48's four-valued chart.

This closes the mathematical cold-corner accuracy gate of the chosen
typed SOURCE. It does not identify original physical marked maps or prove
that the constructed Book H+J family is selected Cost-Info.
"""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json,sys
sys.dont_write_bytecode=True
import two_bit_paid_family as p
P=Path(__file__).resolve().parent;D=P.parent;B=p.source.t.loc.B

def main():
    # For a=p^2 in (0,1), new extremes are -3a*sigma,3(1-a)*sigma.
    # 3 sigma < s embeds all four digits in the OLD asymmetric cube.
    sigma=F(1,1<<80);s=F(1,1<<30);assert 3*sigma<s
    a47=json.loads((D/'round47/FULL_VECTOR_CONTROL_PLAN.json').read_text())
    assert a47['vertices_inside_old_continuous_cube']
    plan=p.source.namespace();old=p.source.previous.namespace()
    assert plan['SC6_local_to_global']==old['SC6_local_to_global']
    assert len(plan['reports'])==8
    mapping=set(plan['SC6_local_to_global']);fresh=plan['reports'][-1]
    assert not mapping.intersection((fresh['all_READY'],fresh['REPORT']))
    # A27's leaf identities use the target entries and copy tensor products,
    # not the number of labels or the former binary label names.
    err=p.source.upper_inventory_and_error()['full_canonical_compressed_error']
    assert err<F(1,1<<3421) and err<F(1,1<<3298)
    lower=F(67,100)-err;assert lower>F(2,3)
    # Old c_ref=1-8*kappa*p^7; kappa<1 and p^7=13p-8.
    cref_lower=1-8*(13*F(618034,10**6)-8);assert cref_lower>F(2,3)
    gs=F(1,1<<3208);z=F(1,1<<20);cfg=p.production_configuration()
    assert lower-cfg['post_error']>F(2,3)
    # Actual positive native centre c0hat obeys 0<c0hat<=1. Consequently
    # the declared same-reader gain Gamma has the stated p^K lower bound.
    gamma_coefficient=4*z*cref_lower*gs
    assert gamma_coefficient>F(8,3)*z*gs
    source_error=p.source.upper_inventory_and_error()['full_SOURCE_DATA_fibre_prefix_error']
    controls=p.control.control_plan();decode=lambda x:F(int(x['numerator_hex'],16),int(x['denominator_hex'],16))
    ep=decode(controls['control_vs_exp_tX_error']);step=F(1,1<<1700)
    interface=2*source_error/gs+2*ep/(step*gs)
    assert interface<F(1,1<<189)
    files=[Path(__file__),D/'round27/PREPARED_SOURCE_MOMENT_LAW_RU.md',
      D/'round26/FULL_READY_GAIN_CHECK.json',B/'round29/BUDGET_CERTIFICATE.json',
      D/'round46/independent_current_bank.py',D/'round46/RESULT.json',
      D/'round47/FULL_VECTOR_CONTROL_PLAN.json',D/'round48/TWO_BIT_GLOBAL_SOURCE_PLAN.json',
      D/'round48/ROOT_REVIEW_B94.json',P/'two_bit_paid_family.py',P/'TWO_BIT_PAID_FAMILY_PLAN.json']
    out={'status':'TYPED_FOUR_VALUED_IDEAL_MOMENT_LAW_AND_ACTUAL_CORNER_GATE',
      'ideal_corner':'c_b=1-2*kappa9*p^7*(4+sum_x w_x Xi_bx)',
      'same_original_reporter_polynomial':True,'same_original_source_copy_slots_and_moments':True,
      'reference_fields_and_gain_coefficient_changed':False,
      'g_lower':'2^-3128','g_sigma_lower':'2^-3208',
      'new_vertices_inside_original_cube':True,
      'fresh_eighth_REPORT_cancelled_only_in_ideal_closed_comparator':True,
      'actual_compiled_eighth_REPORT_error_included':True,
      'mathematical_cold_corner_error':p.encode(err),'mathematical_cold_corner_error_lt':'2^-3421',
      'A47_complete_corner_error_gate_lt_2pow_minus3298':True,
      'actual_M_entry_lower':p.encode(lower),'actual_M_entry_gt':'2/3',
      'CODE_diagonal_requirement':'proved compositionally by SOURCE/REPORT/compiler footprints; separately audited in B96',
      'actual_centre_after_fixed_post_gt':'2/3',
      'same_reader_Gamma':'4*z*p^K*c_ref*g*sigma/(1-z+z*p^K*c0hat^2)',
      'same_reader_Gamma_lower':'(8/3)*z*2^-3208*p^K',
      'same_shared_bank_control_interface_over_g_error':p.encode(interface),
      'same_shared_bank_control_interface_over_g_error_lt':'2^-189',
      'interface_is_not_complete_physical_cost_source':True,
      'scope':'A27/B54 prepared product source/report theorem on A48 declared typed/private RAW fibre and A46 ideal fresh-REPORT commutation',
      'original_Dnu_or_full_vacuum_extension_identity_proved':False,
      'all_independent_price_rows_zero':False,'full_Cost_Info_selection_proved':False,
      'physical_C_closed':False,'GR_closed':False,
      'source_sha256':{str(f):sha256(f.read_bytes()).hexdigest() for f in files}}
    (P/'CORNER_AND_PRICE_BRIDGE.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('status','mathematical_cold_corner_error_lt','actual_M_entry_gt','same_shared_bank_control_interface_over_g_error_lt')}))

if __name__=='__main__':main()
