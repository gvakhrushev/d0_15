#!/usr/bin/env python3
"""Manifest linking emitted original H.1 components and precise missing inputs."""
from pathlib import Path
import hashlib,json

d=Path(__file__).resolve().parent
c=json.loads((d/'COMPONENT_RESULT.json').read_text())
g=json.loads((d/'REFERENCE_METADATA.json').read_text())
j=json.loads((d/'JULIA_TARGET_RESULT.json').read_text())
chart=json.loads((d/'CHART_ENVELOPE_RESULT.json').read_text())
site=json.loads((d/'SITE_LOADER_RESULT.json').read_text())
fourier=json.loads((d/'PF_FOURIER_CHECK.json').read_text())
assert c['comparator']['forward_calls']==18176 and g['site_count']==256 and j['sites']==256
assert chart['m']==2688
# Candidate literal address allocation for already specified front resources.
# It is not a final H.1 birth schedule: the original bank allocation/order is
# unresolved, so no unknown bank births or resulting final E0 are invented.
births=[{'wire':19,'role':'SOURCE_PORT'}]
births += [{'wire':i,'role':('selector' if i<5 else 'READY_REPORT')} for i in range(19)]
births += [{'wire':23+i,'role':'SAM','sam_index':i} for i in range(chart['m'])]
births += [{'wire':2711+i,'role':'SITE','site_bit':i} for i in range(8)]
assert len(births)==2716 and len({r['wire'] for r in births})==len(births)
with (d/'CANDIDATE_PREFIX_BIRTHS.jsonl').open('w') as f:
    for k,row in enumerate(births):
        row['candidate_stage']=k;row['embedding']='v=(sqrt(p),p)'
        f.write(json.dumps(row,separators=(',',':'))+'\n')
manifest={'status':'PARTIAL_DAG_NOT_AN_EXECUTABLE_COMPLETE_H1',
 'selection':{'mesh_L':4,'h':'1/4','native_site_depth_n':20,
              'field_centre':'original Brinkmann owner section 7.2, sigma=1/100, AW=3/100, nu=3/5',
              'sam_cube':'H.1 Y_b=chi^-1(chi(Y0)+s(b-p^2 1)); candidate m=2688,s=2^-30 with geometric slack certified',
              'note':'L=4 is smallest dyadic L in the cited Fourier128 owner; not a proof of global H.1 minimality'},
 'local_comparator_address_map':{'scope':'exact existing SC6 23-wire local interface, must be bound into actual H.1 allocation',
              'selector':[0,1,2,3,4],'ready':[5,7,9,11,13,15,17],
              'report':[6,8,10,12,14,16,18],'port':19,'spin':[20,21],'oldright':[22]},
 'candidate_prefix_allocation':{'initial_unknown':[20,21,22],'oldright':[22],
              'births':'CANDIDATE_PREFIX_BIRTHS.jsonl','birth_count':2716,
              'SAM_range':[23,2710],'SITE_range':[2711,2718],
              'r_t_reserved':[2719,2720],
              'scope':'candidate prefix only; original bank birth order/addresses not determined, so not a complete input or execution'},
 'ordered_nodes':[
  {'id':'pf_original','kind':'source_data','status':'exact_address_export','artifact':'ORIGINAL_F_R_N20_L4.jsonl','births':'not an executed bank word'},
  {'id':'central_geometry','kind':'source_target','status':'numeric_candidate_centre_only','artifact':'BRINKMANN_L4_CENTRE.jsonl'},
  {'id':'julia_centre','kind':'source_target','status':'numeric_full_columns_not_native','artifact':'CENTRE_JULIA32_TARGETS_NUMERIC.npz'},
  {'id':'sam_site','kind':'paid_loader','status':'numeric_all_column_target_only',
   'artifact':'SITE_LOADER_L4_CENTRE_NUMERIC.npz',
   'reason':'native site loader word, true marked frontiers and full-bank compatibility are unresolved'},
  {'id':'seven_banks_forward','kind':'paid_geometry_writer','slots':['y_plus','y_minus','f','zero','x_plus','x_minus','q'],
   'status':'unresolved','reason':'full H_f/H_q sign machinery, all regenerated Choi/CAR banks, factory/READY, tolerance and prefixes not emitted'},
  {'id':'port_inverse','kind':'native_local_macro','status':'exact_5_calls_after_binding','word':['SourceI','SourceI','G(port)','SourceI','SourceI']},
  {'id':'predicate_forward','kind':'native_local_word','status':'emitted_exact','artifact':'SC6_FORWARD.jsonl','calls':18176},
  {'id':'nps_pointer_copy','kind':'native_macro','status':'exact_after_binding','word':['CX(port,r)']},
  {'id':'pre_sign','kind':'mark','status':'logical_event_known','event':'P(port=1)','physical_stage':'requires expanded seven-bank word'},
  {'id':'central_sign','kind':'native_macro','status':'exact_after_binding','word':['SourceI(port,spin)','SourceI(port,spin)']},
  {'id':'predicate_reverse','kind':'native_local_word','status':'emitted_exact','artifact':'SC6_INVERSE.jsonl','calls':18176},
  {'id':'seven_banks_backward','kind':'paid_geometry_inverse','status':'unresolved','reason':'independent A_b slot and literal backward mark/address mapping'},
  {'id':'site_unprepare','kind':'paid_loader_inverse','status':'unresolved'},
  {'id':'nps_E0','kind':'native_macro','status':'exact_after_binding','word':['CX(r,t)','G(t)','CX(r,t)']},
  {'id':'echo_recovery_archive','kind':'native_continuation','status':'partial','reason':'echo and reader exist, full conditional bank recovery and future-mark transport not compiled'}],
 'marks_and_seal':{'original_source_ready_site_presign':'parametric owner marks A_(b,t),O_t; full finite stage/address/readback list unresolved',
                   'prior_oldRIGHT':'immutable on all G/CX/SourceI; dynamic exact range from original history required',
                   'later_reader_and_seal':'actual required readers, address deadlines and physical registration versus coherent marks not emitted'},
 'pf_fourier_boundary':{'naive_nonuniform_weighted_uniform_fourier_gram':fourier['max_entry_residual_rational'],
                        'note':'SITE and CAR/RIGHT may be separate; do not claim this diagnostic invalidates the owner'},
 'calibration':{'reference_Q':c['reference_only']['Q_ref_zero_Xi'],
                'reference_noisy_q':c['reference_only']['noisy_q_ref_zero_Xi'],
                'reference_limit_not_positive_s_sampler':True,
                'F_h':g['F_h_rational'],'r_x':g['r_x'],'r_y':g['r_y'],
                'delta_times_Lambda':g['delta_h_times_Lambda_h'],
                'g_times_Lambda2_over_actual_alpha2':g['g_times_Lambda_h_squared_over_alpha_h_squared'],
                'actual_Lambda_h':'unresolved source-operator certified bound',
                'actual_full_alpha_h':'unresolved full ten-sign factory readiness',
                'actual_q_and_source':'not computed for positive-s compiled geometric packet'},
 'full_gate_dag_emitted':False,'full_H1_mark_transport_certified':False,'physical_C_closed':False,'GR_closed':False}
(d/'PARTIAL_H1_DAG.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print('PASS: exact comparator and original PF are linked; full H.1 remains explicitly unresolved.')
