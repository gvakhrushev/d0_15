#!/usr/bin/env python3
"""Repeat A14 exact checker in isolation with literal native Spin L_i."""
from pathlib import Path
from hashlib import sha256
import tempfile,subprocess,shutil,json,sympy as s
P=Path(__file__).resolve().parent;ROOT=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13');base=Path('02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round14');native=Path('02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py')
J=s.Matrix([[0,-1],[1,0]]);model=s.diag(J,J);actual=s.diag(J,-J);W=s.diag(1,1,1,-1);assert W*model*W==actual and W*W==s.eye(4)
# Since W acts only on Spin, it commutes with G and CX (ordinary wires), so
# every actual SourceI word is conjugate by this same W to the old diagnostic.
checker=ROOT/base/'check_native_boolean.py';source=checker.read_text();old='if (index>>(N-1-SPIN[1]))&1:value=-value';new='if ((index>>(N-1-SPIN[0]))^(index>>(N-1-SPIN[1])))&1:value=-value';assert source.count(old)==1
files=[base/'native_boolean.py',native];sha=lambda p:sha256(p.read_bytes()).hexdigest();orig=ROOT/base/'NATIVE_BOOLEAN_CHECK.json';oldhash=sha(orig)
with tempfile.TemporaryDirectory(prefix='a14-spin-',dir=P) as td:
 tmp=Path(td)
 for f in files:(tmp/f).parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/f,tmp/f)
 work=tmp/base;(work/'check_native_boolean.py').write_text(source.replace(old,new))
 r=subprocess.run(['python3','-B','-W','error','check_native_boolean.py'],cwd=work,text=True,capture_output=True,check=True)
 result=json.loads((work/'NATIVE_BOOLEAN_CHECK.json').read_text());original=json.loads(orig.read_text());assert result==original and sha(orig)==oldhash
out={'status':'PASS_A14_EXACT_CHECK_WITH_LITERAL_SPIN','original_checker_used_spin_basis':'diag(J,J), conjugate representation','corrected_checker_used':'literal diag(J,-J)','conjugator':'diag(1,1,1,-1) on Spin','corrected_all_column_total':result['all_exact_columns_total'],'corrected_results_equal_original_json':True,'original_files_modified':False,'stdout':r.stdout.strip(),'scope':'exact small k=1,2 actual native words; huge-k approximation certificate is separate','GR_closed':False}
(P/'A14_TRUE_SPIN_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
