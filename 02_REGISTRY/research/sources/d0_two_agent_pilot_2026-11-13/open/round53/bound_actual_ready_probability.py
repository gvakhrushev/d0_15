#!/usr/bin/env python3
"""Uniform actual READY probability bound; never assert an exact scalar effect."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');O=P.parent
files=[D/'round17/GLOBAL_REPORT_COMPILATION.json',D/'round16/SOURCE_SELECT_COMPILATION.json',D/'round15/PREPROCESSOR_READY_COMPOSITION.json',D/'round25/H1_NAMESPACE_PLAN.json',O/'round52/GLOBAL_HYBRID_FIBRES_CHECK.json',P/'READY_GAIN_INTEGER_INDEPENDENT_CHECK.json',P/'IDEAL_READY_EFFECT_STRUCTURE_CHECK.json'];h=lambda p:sha256(p.read_bytes()).hexdigest();pins={str(q):h(q) for q in files};report,select,pre,ns,partition,ideal,effect=[json.loads(f.read_text()) for f in files]
K=report['all_READY_flags'];assert K==10249327
previous=select['seven_report_all_known_approximate_macros'];combined=report['seven_report_all_known_approximate_macros'];assert combined==previous+7*(2*K-3+1)==162754649904 and combined%7==0
per=combined//7;assert per==23250664272 and per<2**35
epsilon=F(per,2**4096);dev=2*epsilon;assert epsilon<F(1,2**4061) and dev<F(1,2**4060)
lo=F(74068,100000);hi=F(74069,100000);roughlo=F(74067,100000);roughhi=F(74070,100000);assert 0<roughlo<lo-dev and hi+dev<roughhi<1
lower=roughlo**7;upper=roughhi**7;assert lower>F(12228,100000) and upper<F(12232,100000)
assert partition['report_local_arena_disjoint_across_all7'] and effect['SC6_never_targets_READY_or_REPORT'] and len(ns['reports'])==7
assert ideal['alpha_interval_strict']=='0.74068 < alpha < 0.74069'
for path,digest in pins.items():assert h(Path(path))==digest
out={'status':'PASS_UNIFORM_APPROXIMATE_NATIVE_READY_BOUND','input_sha256':pins,'seven_report_approximate_macro_count':combined,'per_report_count':per,'native_per_report_isometry_error_lt':'2^-4061','READY_effect_distance_to_ideal_scalar_I_lt':'2^-4060','per_report_READY_probability_on_arbitrary_external_input':'0.74067 < P_actual < 0.74070','joint_all_seven_READY_probability':'0.12228 < P_actual_joint < 0.12232','logic':'For each actual report with its own canonical fresh RAW resource arena, E_ready differs in operator norm by at most 2 epsilon from alpha I, uniformly over source/SITE/SAM/aux/Spin and previous retained records. Future report resources stay fresh; old READY flags are not targeted later. Apply the interval conditionally to each retained success event; SC6 only controls on the flags.','exact_actual_effect_scalar_or_field_independent':False,'physical_RAW_births_or_original_moment_law_proved':False,'physical_C_closed':False,'GR_closed':False}
(P/'READY_NATIVE_APPROX_INTERVAL.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'per_report_error_lt':'2^-4061','actual_joint':out['joint_all_seven_READY_probability']}))
