#!/usr/bin/env python3
"""Add checked local research to the existing #310 branch; never force-push."""
from pathlib import Path
import argparse,hashlib,json,os,shutil,subprocess,sys
HERE=Path(__file__).resolve().parent
BRANCH='exp/a4d-joint-response-resolvent'
def git(repo,*args):
 r=subprocess.run(['git',*args],cwd=repo,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 if r.returncode:raise RuntimeError(r.stderr.strip() or 'git command failed: '+' '.join(args))
 return r.stdout.strip()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('repository',type=Path);ap.add_argument('--push',action='store_true');ap.add_argument('--replay',action='store_true');a=ap.parse_args();repo=a.repository.resolve()
 hashes=json.loads((HERE/'SHA256.json').read_text())
 for name,want in hashes.items():
  if hashlib.sha256((HERE/name).read_bytes()).hexdigest()!=want:raise RuntimeError('bundle hash mismatch: '+name)
 if git(repo,'branch','--show-current')!=BRANCH:raise RuntimeError('Switch to the existing #310 execution branch first; no branch is created here.')
 remote=git(repo,'remote','get-url','origin').rstrip('/').removesuffix('.git')
 if remote not in ('https://github.com/gvakhrushev/d0_15','git@github.com:gvakhrushev/d0_15'):raise RuntimeError('Unexpected repository remote')
 if git(repo,'status','--porcelain'):raise RuntimeError('Working tree must be clean; no files have been changed.')
 git(repo,'fetch','origin',BRANCH)
 if git(repo,'rev-parse','HEAD')!=git(repo,'rev-parse','origin/'+BRANCH):raise RuntimeError('Synchronize this branch normally before import; no reset/rebase is performed.')
 plans=[]
 for name,want in hashes.items():
  if not name.startswith('repo/'):continue
  rel=Path(name).relative_to('repo');target=repo/rel
  if target.exists():
   if hashlib.sha256(target.read_bytes()).hexdigest()!=want:raise RuntimeError('Existing differing file; review required: '+str(rel))
  else:plans.append((rel,HERE/name,target))
 if not plans:print('All delivered files already match.');return
 for rel,source,target in plans:target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
 if a.replay:
  env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'}
  for f in ['a4d_full4d_verified_intake_check.py','a4d_joint_lattice_ward_resonance_check.py']:
   subprocess.run([sys.executable,str(repo/'02_REGISTRY/research/certificates'/f)],cwd=repo,env=env,check=True)
 git(repo,'add','--',*[str(x[0]) for x in plans]);git(repo,'diff','--cached','--check')
 git(repo,'commit','-m','research(a4d): exact joint Ward and two-mode resonance reduction')
 own=git(repo,'rev-parse','HEAD');print('Local commit:',own)
 if a.push:
  git(repo,'push','origin','HEAD:refs/heads/'+BRANCH)
  git(repo,'fetch','origin',BRANCH)
  git(repo,'merge-base','--is-ancestor',own,'origin/'+BRANCH)
  print('Published commit verified in remote branch:',own)
  print('Remote head:',git(repo,'rev-parse','origin/'+BRANCH))
 else:print('Not pushed. --push is required for remote publication.')
if __name__=='__main__':main()
