#!/usr/bin/env python3
"""Read-only replay of the three NEW calculations and focused negative controls."""
from __future__ import annotations
import hashlib,json,math,os,shutil,subprocess,sys,tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent
ENV=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
CASES=(('check_absolute_completion.py','matrix_result.json'),
       ('check_native_root_transport.py','root_result.json'),
       ('check_primary_reference.py','primary_result.json'))

def require(ok,label):
    if not bool(ok): raise ArithmeticError(label)

def integrity(root):
    data=json.loads((root/'SHA256SUMS.json').read_text())
    for name,expected in data.items():
        require(hashlib.sha256((root/name).read_bytes()).hexdigest()==expected,'content changed: '+name)
    return data

def compare(actual,expected,path='root'):
    require(type(actual) is type(expected),'type mismatch: '+path)
    if isinstance(expected,dict):
        require(actual.keys()==expected.keys(),'schema mismatch: '+path)
        for key in expected:compare(actual[key],expected[key],path+'.'+key)
    elif isinstance(expected,list):
        require(len(actual)==len(expected),'length mismatch: '+path)
        for j,(a,e) in enumerate(zip(actual,expected)):compare(a,e,path+f'[{j}]')
    elif isinstance(expected,float):
        require(math.isfinite(actual),'nonfinite: '+path)
        # The checker itself enforces the individual mathematical tolerances.
        # Whole-value finite differences have platform-dependent cancellation.
        atol=1e-6 if 'whole_HJR_fd_error' in path else 1e-10
        require(abs(actual-expected)<=atol+1e-8*abs(expected),'numeric receipt mismatch: '+path)
    else:require(actual==expected,'exact receipt mismatch: '+path)

def run(script,root=ROOT,optimized=False):
    command=[sys.executable]+(['-O'] if optimized else [])+[str(root/script)]
    return subprocess.run(command,cwd=root,env=ENV,capture_output=True,text=True,timeout=120)

def controls():
    mathematical=[
      ('check_absolute_completion.py',
       'source_ratio=REF*(np.trace(np.linalg.solve(h,dh))-np.trace(np.linalg.solve(m,dm))).real',
       'source_ratio=-REF*np.trace(np.linalg.solve(m,dm)).real',
       'full complementary source incl normalizer'),
      ('check_absolute_completion.py',
       'f=np.eye(16)-ret; df=-dret',
       'f=ret; df=dret',
       'true complementary determinant ratio'),
      ('check_native_root_transport.py','n=8192; m=2*n; ref=128',
       'n=8192; m=2*n; ref=1','original known root scale equation'),
      ('check_primary_reference.py','    return f,pairs',
       '    f[:,55]=0\n    return f,pairs','full initial RIGHT Gram')]
    done=[]
    for script,old,new,label in mathematical:
        with tempfile.TemporaryDirectory(prefix='d0-semantic-') as tmp:
            target=Path(tmp)
            for file in ROOT.glob('*.py'):shutil.copy2(file,target/file.name)
            content=(target/script).read_text()
            require(content.count(old)==1,'unambiguous mutation anchor')
            (target/script).write_text(content.replace(old,new))
            trial=run(script,target)
            require(trial.returncode!=0 and label in trial.stderr,
                    'semantic mutation was not rejected by its mathematical assertion: '+label)
            done.append(label)
    for filename in ('PROOF.md','primary_result.json'):
        with tempfile.TemporaryDirectory(prefix='d0-integrity-') as tmp:
            target=Path(tmp)
            for name in json.loads((ROOT/'SHA256SUMS.json').read_text()):
                shutil.copy2(ROOT/name,target/name)
            shutil.copy2(ROOT/'SHA256SUMS.json',target/'SHA256SUMS.json')
            with (target/filename).open('ab') as f:f.write(b'\nchanged copy\n')
            failed=False
            try:integrity(target)
            except ArithmeticError:failed=True
            require(failed,'modified proof/receipt accepted')
            done.append('integrity: '+filename)
    return done

def main():
    before=integrity(ROOT)
    results=[]
    for script,receipt in CASES:
        normal=run(script);optimized=run(script,optimized=True)
        require(normal.returncode==0,normal.stderr)
        require(optimized.returncode==0,optimized.stderr)
        require(normal.stdout==optimized.stdout,'normal/-O mismatch: '+script)
        actual=json.loads(normal.stdout)
        compare(actual,json.loads((ROOT/receipt).read_text()))
        results.append({'script':script,'normal_and_optimized_equal':True,'saved_receipt_matches':True})
    rejected=controls()
    require(integrity(ROOT)==before,'tracked files changed during replay')
    result={'status':'PASS','new_calculations':results,'rejected_controls':rejected,
            'tracked_source_and_receipt_bytes_unchanged':True,
            'inherited_expensive_suites_replayed':False,
            'independent_review':False,'remote_CI':False,'GR_closed':False}
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
