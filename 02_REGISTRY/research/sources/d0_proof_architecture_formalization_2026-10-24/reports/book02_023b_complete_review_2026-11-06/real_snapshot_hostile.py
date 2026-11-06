"""Exercise real Git snapshots; use only a disposable shared clone.

Creates unreferenced test commits/objects in --repo; no references are moved.
The selected --snapshot must include this reviewed correction.
"""
import argparse, json, os, subprocess, tempfile
from pathlib import Path
parser=argparse.ArgumentParser()
parser.add_argument('--repo', required=True, help='disposable shared clone')
parser.add_argument('--snapshot', required=True)
parser.add_argument('--helper', required=True, help='path to c0_reconciliation.py under test')
args=parser.parse_args()
repo=str(Path(args.repo).resolve())
helper=str(Path(args.helper).resolve())
base=args.snapshot
root='02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/reports/book02_023b_complete_review_2026-11-06/'
primary='02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md'

def git(*args, data=None, env=None):
 return subprocess.run(['git','-C',repo,*args],input=data,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True,env=env).stdout

def view(ref, book=None):
 args=['python3.13',helper,'--repo',repo,'--snapshot',ref,'--kernel-sections']
 if book: args += ['--kernel-book',book]
 p=subprocess.run(args,capture_output=True,check=False)
 if p.stderr: raise Exception(p.stderr.decode())
 return json.loads(p.stdout)

def mutated_commit(path, mode):
 with tempfile.TemporaryDirectory() as d:
  env=dict(os.environ, GIT_INDEX_FILE=d+'/index', GIT_AUTHOR_NAME='Review Test', GIT_AUTHOR_EMAIL='test@example.invalid', GIT_COMMITTER_NAME='Review Test', GIT_COMMITTER_EMAIL='test@example.invalid')
  git('read-tree',base,env=env)
  if mode=='delete': git('update-index','--force-remove','--',path,env=env)
  else:
   content=git('show',base+':'+path)
   content=(content.replace(b'book02_023b_complete_review_2026-11-06/SUMMARY_RU.md',b'missing-reviewed-file',1) if mode=='pointer' else content+b'hostile\n')
   h=git('hash-object','-w','--stdin',data=content,env=env).decode().strip()
   git('update-index','--add','--cacheinfo','100644,'+h+','+path,env=env)
  tree=git('write-tree',env=env).decode().strip()
  return git('commit-tree',tree,'-p',base,data=b'hostile review fixture\n',env=env).decode().strip()

v=view(base)
assert len(v['units'])==30 and v['scope']['c0_acceptance_assessment']=='not_evaluated'
r={x['atom']:x for x in v['units']}
assert 'logically equivalent' in r['Interpretation.translate_future_observation']['statement']
assert 'equals the actual' in r['Interpretation.translate_future_observation']['historical_statement']
assert r['Interpretation.verifiedRun_image']['reviewed_proof_dependency']['declaration'].endswith('verifiedStateImageEquiv_representedState')
assert all(x['semantic_acceptance']=='pending_independent_review' for x in v['units'])
assert [x['check'] for x in v['issues']]==['current_compiled_evidence']
print('PASS actual view: 30 candidates, corrections, unresolved historical inventory, no acceptance')
for path, mode in [(root+'SUMMARY_RU.md','modify'),(root+'SUMMARY_RU.md','delete'),(root+'d0-book02-represented-emptyword.lean','modify'),(primary,'pointer')]:
 ref=mutated_commit(path,mode); v=view(ref)
 assert v['checks']['source_and_primary']['state']=='unresolved' and not v['units'], (mode,v['issues'])
 print('PASS rejects',path,mode, v['checks']['source_and_primary']['reason'])
