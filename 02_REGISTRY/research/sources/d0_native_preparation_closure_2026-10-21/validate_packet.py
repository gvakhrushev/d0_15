from pathlib import Path
import hashlib,json,os,platform,subprocess,sys
import numpy,scipy,sympy
root=Path(__file__).resolve().parent
code=root/'check_native_preparation.py'
text=code.read_text()
env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
mutations={
 'replace_native_preparation_by_flat':('inv=np.linalg.inv(Delta);zz=tr(inv);rho=inv/zz','inv=np.linalg.inv(Delta);zz=tr(inv);rho=I/16'),
 'freeze_induced_preparation_jet':('dinv=-inv@dDelta@inv;drho=dinv/zz-inv*tr(dinv)/zz**2','dinv=-inv@dDelta@inv;drho=np.zeros_like(I)'),
 'drop_paid_boundary_corrector':('Yv=solve(MM,vec(E-kap*I));Y=herm(unvec(Yv))','Yv=solve(MM,vec(E-kap*I));Y=np.zeros_like(I)'),
 'erase_noncommuting_normalizer':('correction=-c*eta*eps**2*A@(T(Delta)-Delta)@A','N2=Nc.copy()\n    correction=-c*eta*eps**2*A@(T(Delta)-Delta)@A')}
checks=[]
for name,(old,new) in mutations.items():
 if text.count(old)!=1:raise RuntimeError('nonunique mutation '+name)
 path=root/('_mutation_'+name+'.py');path.write_text(text.replace(old,new))
 run=subprocess.run([sys.executable,str(path)],env=env,capture_output=True,text=True,timeout=35)
 path.unlink()
 if run.returncode==0:raise RuntimeError('mutation survived '+name)
 checks.append({'name':name,'returncode':run.returncode,'failure':run.stderr.strip().splitlines()[-1]})
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((root/'RESULT.json').read_text())
if (root/'RESULT.json').read_bytes()!=(root/'RESULT_OPTIMIZED.json').read_bytes():raise RuntimeError('optimized differs')
files=['PROOF.md','check_native_preparation.py','RESULT.json','RESULT_OPTIMIZED.json']
validation={'status':'PASS','input_commit':r['input_commit'],'check_count':r['check_count'],
 'normal_and_optimized_byte_identical':True,'author_runs_only':True,'independent_review':False,
 'mutation_checks':checks,'sha256':{p:digest(root/p) for p in files},
 'environment':{'python':platform.python_version(),'sympy':sympy.__version__,'numpy':numpy.__version__,'scipy':scipy.__version__},
 'scope':r['scope'],'not_run':['previous full scientific suites','Lean','repository-wide CI'],
 'errors_corrected_before_final_run':['canonicalized exact complex rational matrix identities','used the full Hermitian probability derivative rather than assuming each half trace real']}
(root/'VALIDATION.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'PASS','check_count':r['check_count'],'rejected_mutations':checks},indent=2))
