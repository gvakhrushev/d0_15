#!/usr/bin/env python3
"""Isolated replay and consuming-parent audit of the B39 conditional adapter."""
from pathlib import Path
from fractions import Fraction
import hashlib,json,shutil,subprocess,sys,tempfile
P=Path(__file__).resolve().parent
B=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13')
R=B/'02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open/round39'
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
pins={p.name:h(p) for p in sorted(R.iterdir()) if p.is_file()}
jobs=[('verify_adapter_phases.py','ADAPTER_PHASE_INDEPENDENT_CHECK.json'),
      ('check_fixed_point_math.py','FIXED_POINT_MATH_CHECK.json'),
      ('build_adapter_grammar.py','ADAPTER_NATIVE_GRAMMAR.json'),
      ('check_adapter_grammar.py','ADAPTER_GRAMMAR_CHECK.json')]
reports=[]
with tempfile.TemporaryDirectory(prefix='d0-a19-b39-review-') as tmp:
    dst=Path(tmp)/'round39';shutil.copytree(R,dst)
    for script,output in jobs:
        done=subprocess.run([sys.executable,'-B','-W','error',script],cwd=dst,text=True,capture_output=True)
        assert done.returncode==0,(script,done.stdout[-1500:],done.stderr[-1500:])
        actual=json.loads((dst/output).read_text());expected=json.loads((R/output).read_text())
        assert actual==expected,(script,'isolated JSON mismatch')
        reports.append({'script':script,'output':output,'output_sha256':h(R/output),'isolated_JSON_identical':True})
        print('B39 isolated replay passed',script,flush=True)
assert all(h(R/name)==digest for name,digest in pins.items())
grammar=json.loads((R/'ADAPTER_NATIVE_GRAMMAR.json').read_text());lay=grammar['layout']
assert set(lay['start_controls'])=={lay['branch'],*lay['data'],*lay['V_private']}
assert not set(lay['start_controls'])&{lay['rebit'],lay['predicate_flag'],*lay['predicate_work']}
assert len(lay['data'])==22 and not lay['V_private']
assert len(grammar['new_RAW_v_wires'])==24
# Exact root-side budget consumption; Qpre from A17 is not substituted for
# the still unproved full H1 success probability.
d=Fraction(1,2**4096);dv=Fraction(1,2**3250);N=23+32768
eta=Fraction(1,2**3280)+6561*dv+(13122+13120*N+1)*d
assert eta<Fraction(1,2**3230)
prefix=Fraction(1,2**4091);select=Fraction(1,2**3251)
assert prefix+select<dv
# Ideal normalized-output error²=2(1-sqrt(1-e))<2e, not merely e.
# e<2^-6561 therefore the complete phase-corrected output error<2^-3280.
assert 2*Fraction(1,2**6561)==Fraction(1,2**6560)
out={'status':'PASS_ROOT_CONSUMPTION_OF_CONDITIONAL_B39_ADAPTER',
     'B_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=B,text=True).strip(),
     'pinned_files_sha256':pins,'isolated_replays':reports,
     'full_normalized_output_error_ideal_lt':'2^-3280 (includes good-component normalization and retained failure)',
     'comparator_hybrid_review':'compare actual phase blocks on clean ideal prefixes; do not apply their clean-subspace estimate directly on dirty actual prefixes',
     'anchor_only_stability_review':'X -> (I+(t-1)XX†) R_Q X is 3-Lipschitz on isometries; comparator and realification rebit must be exact spectators of A0',
     'conditional_adapter_error_lt':'2^-3230',
     'sufficient_loader_supplier_budget':{'A19_actual_prefix_error_lt':'2^-4091','missing_full_controlled_Julia_SELECT_error_le':'2^-3251','sum_lt':'2^-3250'},
     'needs_disjoint_rebit_comparator_and_arbitrary_aux':True,
     'A19_prefix_is_not_full_loader':True,'full_loader_and_actual_joint_namespace_compiled':False,
     'full_H1_alpha_lower_bound_proved':False,'physical_C_closed':False,'GR_closed':False}
(P/'ROOT_REVIEW_B39.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'isolated_replays':len(reports),'conditional_adapter_error_lt':out['conditional_adapter_error_lt']}))
