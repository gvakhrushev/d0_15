#!/usr/bin/env python3
"""Execute actual mathematical mutations, without changing tracked inputs."""
from pathlib import Path
import json
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
source=HERE/'check_golden_curvature.py'
text=source.read_text(encoding='utf8')
cases=[
 ('ordered_sign','(False, True): -1','(False, True): 1','golden signed moment 1'),
 ('quartic_scale','HIGH_SCALE_POWER = 4','HIGH_SCALE_POWER = 3','exact finite scalar curvature'),
 ('frozen_calibration','KEEP_CALIBRATION_JET = True','KEEP_CALIBRATION_JET = False',
  'moving event normalizer and scale jets retained'),
 ('frozen_blank','KEEP_BLANK_JET = True','KEEP_BLANK_JET = False','moving blank raw mass retained'),
 ('pending_loss','[w+(True,) for w in ready]+pending','[w+(True,) for w in ready]',
  'cut 4 full cylinder'),
 ('active_normal_loss','for A in shapes for w in product','for A in shapes[:1] for w in product',
  'complete golden trace polynomial')]
reports=[]
with tempfile.TemporaryDirectory(prefix='d0-golden-curvature-mutants-') as td:
    for name,old,new,expected in cases:
        if text.count(old)!=1:
            raise RuntimeError('Mutation anchor ambiguous: '+name)
        target=Path(td)/(name+'.py')
        target.write_text(text.replace(old,new),encoding='utf8')
        wrapper=("import pathlib,sys; ns={'__name__':'__main__','__file__':sys.argv[2]}; "
                 "exec(compile(pathlib.Path(sys.argv[1]).read_text(),sys.argv[2],'exec'),ns)")
        cmd=[sys.executable]+(['-O'] if sys.flags.optimize else [])
        run=subprocess.run(cmd+['-c',wrapper,str(target),str(source)],
                           text=True,capture_output=True,timeout=120)
        if run.returncode==0 or 'ArithmeticError:' not in run.stderr or expected not in run.stderr:
            raise ArithmeticError('Mutation was not rejected mathematically: '+name+'\n'+run.stderr)
        reports.append({'name':name,'rejected':True,'failure':run.stderr.strip().splitlines()[-1]})
print(json.dumps({'mathematical_mutants':reports,'count':len(reports)},indent=2,sort_keys=True))
