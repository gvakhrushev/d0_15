from pathlib import Path
import os,subprocess,sys,time
root=Path('/Users/grigorijvahrusev/.codex/worktrees/d0-proof-architecture-followup/d0-main-assembly-audit/03_FORMALIZATION')
source=Path('/private/tmp/d0-2bc-lean-receipt-worktree/03_FORMALIZATION')
output=Path('/tmp/d0-repeated-public-lean-v2'); output.mkdir(exist_ok=True)
env=os.environ.copy();search=subprocess.check_output(['lake','env','printenv','LEAN_PATH'],cwd=root,text=True).strip();lean=subprocess.check_output(['lake','env','which','lean'],cwd=root,text=True).strip();env['LEAN_PATH']=str(output)+os.pathsep+search
for module in ['D0/Research/TaskFaithfulReporterProductEquality','D0/Research/TaskFaithfulRepeatedReporterDerivative','D0/All']:
 target=output/(module+'.olean');target.parent.mkdir(parents=True,exist_ok=True)
 cmd=[lean,'-R',str(source),'-o',str(target),str(source/(module+'.lean'))]
 with open('/tmp/d0-repeated-public-'+module.rsplit('/',1)[-1]+'.log','wb') as f:
  start=time.monotonic();result=subprocess.run(cmd,cwd=root,env=env,stdout=f,stderr=subprocess.STDOUT)
 print(module,'exit',result.returncode,'seconds',round(time.monotonic()-start,2),flush=True)
 if result.returncode:sys.exit(result.returncode)
collector=output/'check_axioms.lean';collector.write_text('import D0.All\n#print axioms D0.Research.taskReturnProduct_price_repeated_affine\n#print axioms D0.Research.taskReturnProduct_price_absent_label\n#print axioms D0.Research.taskReturnProduct_price_repeated_count_1\n#print axioms D0.Research.taskReturnProduct_price_repeated_count_2\n')
with open('/tmp/d0-repeated-public-axioms.log','wb') as f:
 result=subprocess.run([lean,str(collector)],cwd=root,env=env,stdout=f,stderr=subprocess.STDOUT)
print('collector exit',result.returncode,flush=True)
sys.exit(result.returncode)
